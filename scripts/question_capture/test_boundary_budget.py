"""Offline regressions: repairs yield to live work and budgeted imports stay queued."""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from capture import arguments, idle_capture_repair, run
from core import atomic_json
from saved_imports import read_json, sweep
import test_adaptive_run as adaptive_tests
import test_saved_imports as saved_tests


class BoundaryTests(unittest.TestCase):
    def test_idle_boundary_performs_only_one_diagnosis(self):
        with tempfile.TemporaryDirectory() as work:
            args = arguments(['run','--state-dir',work+'/state','--output',work+'/capture'])
            with patch('capture_repair.next_failure',side_effect=[('first',{},'one'),('second',{},'two')]) as failure, \
                 patch('capture_repair.cooldown') as cooldown:
                inspected = idle_capture_repair(args,Mock(),[{'task_id':1}],0,set(),set())
            self.assertTrue(inspected)
            failure.assert_called_once()
            cooldown.assert_called_once()
            self.assertEqual(cooldown.call_args.kwargs,{'pause':False})

    def test_live_queue_refresh_selects_new_lesson_before_second_diagnosis(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            for task in (1,2):
                atomic_json(root/'capture'/str(task)/'state.json',{'task_id':task,'topic_id':task,
                    'task_type':'lesson','deferred_error':{'phase':'activity','message':'saved failure'}})
            args = arguments(['run','--state-dir',str(root/'state'),'--output',str(root/'capture'),
                              '--limit','1'])
            helper = adaptive_tests.AdaptiveRunTests()
            fixture = helper.fixture(work,[1,2,3])
            original_queue = fixture[0].queue
            observations = [0]
            def queue(browser):
                observations[0] += 1
                items = original_queue(browser)
                return items[:2] if observations[0] == 1 else items
            fixture[0].queue = queue
            with patch('capture_repair.next_failure',return_value=('first',{},'one')) as failure:
                selected,cooldown = helper.execute(args,fixture)
            self.assertEqual(selected,[3])
            self.assertGreaterEqual(observations[0],2)
            failure.assert_called_once()
            cooldown.assert_called_once()

    def test_startup_budget_is_one_and_manual_sweep_is_unbounded(self):
        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            args = arguments(['run','--state-dir',str(root/'state'),'--output',str(root/'captures')])
            with patch('capture.Database'), patch('saved_imports.sweep',return_value=[]) as inspect, \
                 patch('playwright.sync_api.sync_playwright',side_effect=RuntimeError('queue phase reached')):
                with self.assertRaisesRegex(RuntimeError,'queue phase reached'):
                    run(args)
            self.assertEqual(inspect.call_args.kwargs['repair_budget'],1)
            args.command = 'sweep-saved'
            with patch('capture.Database'), patch('saved_imports.sweep',return_value=[]) as inspect, \
                 contextlib.redirect_stdout(io.StringIO()):
                run(args)
            self.assertIsNone(inspect.call_args.kwargs['repair_budget'])


class ImportBudgetTests(unittest.TestCase):
    setUp = saved_tests.SavedImportTests.setUp
    capture = saved_tests.SavedImportTests.capture

    def test_successful_direct_import_does_not_consume_model_budget(self):
        self.args.no_import_repair = False
        self.capture(1)
        self.capture(2)
        third,_,_ = self.capture(3)
        def import_content(content,*_):
            if content['task_id'] == 1:
                return {'already_complete':True,'database_writes':0}
            raise ValueError('notation conflict')
        self.db.import_content.side_effect = import_content
        with patch('import_repair.repair',return_value=False) as repair:
            result = sweep(self.db,self.args,trigger='startup',repair_budget=1)
        repair.assert_called_once()
        self.assertEqual([row['status'] for row in result],['complete','deferred','repair_pending'])
        ledger = read_json(self.args.state_dir/'saved-import-attempts.json')
        self.assertEqual(ledger[str(third.resolve())]['status'],'repair_pending')

    def test_postponed_model_repair_is_revisited_with_unchanged_evidence(self):
        self.args.no_import_repair = False
        first,_,_ = self.capture(1)
        second,_,_ = self.capture(2)
        self.db.import_content.side_effect = ValueError('notation conflict')
        with patch('import_repair.repair',return_value=False) as repair:
            initial = sweep(self.db,self.args,trigger='startup',repair_budget=1)
        self.assertEqual([row['status'] for row in initial],['deferred','repair_pending'])
        self.db.import_content.reset_mock()
        self.db.import_content.side_effect = [ValueError('notation conflict'),
            {'already_complete':True,'database_writes':0}]
        with patch('import_repair.repair',return_value=True) as repair:
            recovered = sweep(self.db,self.args,trigger='activity-boundary',repair_budget=1)
        repair.assert_called_once()
        self.assertEqual(recovered,[{'directory':str(second),'status':'complete','error':None}])
        self.assertEqual([call.args[1].parent for call in self.db.import_content.call_args_list],[second,second])
        self.assertTrue(read_json(second/'state.json')['import_complete'])
        self.assertFalse(read_json(first/'state.json').get('import_complete'))

    def test_zero_budget_keeps_missing_imports_pending_without_models(self):
        self.args.no_import_repair = False
        self.capture(1)
        self.db.import_content.side_effect = ValueError('notation conflict')
        with patch('import_repair.repair') as repair:
            initial = sweep(self.db,self.args,trigger='startup',repair_budget=0)
            again = sweep(self.db,self.args,trigger='startup',repair_budget=0)
        repair.assert_not_called()
        self.assertEqual(initial[0]['status'],'repair_pending')
        self.assertEqual(again,[])
        self.assertEqual(self.db.import_content.call_count,1)

    def test_unbounded_later_sweep_recovers_every_postponed_import(self):
        self.args.no_import_repair = False
        for task in (1,2,3): self.capture(task)
        self.db.import_content.side_effect = ValueError('notation conflict')
        with patch('import_repair.repair') as repair:
            initial = sweep(self.db,self.args,trigger='startup',repair_budget=0)
        repair.assert_not_called()
        self.assertEqual([row['status'] for row in initial],['repair_pending']*3)
        self.db.import_content.side_effect = [ValueError('notation conflict'),
            {'already_complete':True,'database_writes':0}]*3
        with patch('import_repair.repair',return_value=True) as repair:
            recovered = sweep(self.db,self.args,trigger='periodic')
        self.assertEqual(repair.call_count,3)
        self.assertEqual([row['status'] for row in recovered],['complete']*3)


if __name__ == '__main__': unittest.main()
