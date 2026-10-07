"""Queued old failures get a repair turn while fresh lessons still progress."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock,patch
import test_adaptive_run as adaptive
from capture import arguments,queued_capture_repair,run
from capture_repair import RestartWorker,evidence_version,failure_key,next_failure,source_version
from core import atomic_json

class QueuedBoundaryTests(unittest.TestCase):
    def failure(self,args,task):
        directory=args.output/str(task);diagnostic=directory/'diagnostics/1'
        report={'task_id':task,'phase':'activity','exception_type':'ValueError','message':'Saved failure '+str(task)}
        atomic_json(diagnostic/'error.json',report)
        atomic_json(directory/'state.json',{'task_id':task,'topic_id':task,'task_type':'lesson',
            'deferred_error':{'phase':'activity','diagnostics':str(diagnostic)},'questions':{}})
        return report

    def test_finished_capture_is_imported_before_repair_restarts_worker(self):
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--preview','--state-dir',work+'/state','--output',work+'/capture',
                            '--limit','2','--lesson-min','0','--lesson-max','0'])
            self.failure(args,1)
            browser,runtime,db,_=adaptive.AdaptiveRunTests().fixture(work,[1,3,4])
            with patch('capture.Database',return_value=db),patch('browser.CaptureBrowser',browser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime), \
                 patch('saved_imports.sweep',return_value=[]), \
                 patch('import_repair.import_with_repair',return_value={'previewed':True}) as importer, \
                 patch('capture_repair.cooldown') as repair, \
                 adaptive.contextlib.redirect_stdout(adaptive.io.StringIO()):
                def restart(*_args,**_kwargs):
                    self.assertEqual(importer.call_count,1)
                    state=json.loads((args.output/'3/state.json').read_text())
                    self.assertTrue(state['preview_complete'])
                    self.assertTrue(state['history_complete'])
                    raise RestartWorker(Path(work)/'batch.json')
                repair.side_effect=restart
                with self.assertRaises(RestartWorker):run(args)

    def test_old_queued_failure_gets_early_repair_without_new_failures(self):
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work+'/state','--output',work+'/capture',
                            '--limit','2','--lesson-min','0','--lesson-max','0'])
            self.failure(args,1)
            self.failure(args,6)  # Newer retired activity must not steal this turn.
            fixture=adaptive.AdaptiveRunTests().fixture(work,[1,3,4])
            selected,repair=adaptive.AdaptiveRunTests().execute(args,fixture)
            self.assertEqual(selected,[3,4])
            repair.assert_called_once()
            self.assertEqual(repair.call_args.kwargs,{'pause':False})
            scoped=repair.call_args.args[0]
            self.assertEqual(scoped.capture_repair_task_ids,{1})
            self.assertEqual(repair.call_args.args[2]['attempted'],1)
            self.assertEqual(next_failure(scoped,{},task_ids=scoped.capture_repair_task_ids)[1]['task_id'],1)

    def test_current_blocked_failure_does_not_repeat_judgment(self):
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work+'/state','--output',work+'/capture'])
            report=self.failure(args,1)
            atomic_json(args.state_dir/'capture-repair/failures.json',{
                failure_key(report):{'source_version':source_version(),
                    'evidence_version':evidence_version(args.output/'1/diagnostics/1/error.json'),
                    'status':'blocked','attempts':1}})
            with patch('capture_repair.cooldown') as repair:
                self.assertFalse(queued_capture_repair(args,Mock(),[{'task_id':1}],1,set(),set()))
            repair.assert_not_called()

    def test_healthy_queue_does_not_change_normal_twenty_activity_cadence(self):
        with tempfile.TemporaryDirectory() as work:
            args=arguments(['run','--state-dir',work+'/state','--output',work+'/capture'])
            with patch('capture_repair.cooldown') as repair,patch('capture_repair.next_failure') as inspect:
                self.assertFalse(queued_capture_repair(args,Mock(),[{'task_id':3}],1,set(),set()))
            repair.assert_not_called();inspect.assert_not_called()
            self.assertEqual(args.rest_every,20)

if __name__=='__main__':unittest.main()
