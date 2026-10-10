"""A shutdown drain resumes one started activity and never consumes fresh work."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import test_adaptive_run
from capture import arguments, run
from core import atomic_json
from diagnostic import diagnostic_decision, replaced_diagnostic_record


class FinishInProgressTests(unittest.TestCase):
    def args(self, root):
        return arguments(['run','--capture-only','--finish-in-progress',
                          '--resume',str(root/'capture/1'),'--output',str(root/'capture'),
                          '--state-dir',str(root/'state')])

    def test_requires_explicit_capture_only_resume(self):
        for values in ([],['--capture-only'],['--resume','/tmp/task'],
                       ['--resume','/tmp/task','--capture-only','--limit','2']):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                arguments(['run','--finish-in-progress',*values])

    def test_finishes_saved_activity_without_starting_new_queue_work(self):
        with tempfile.TemporaryDirectory() as work:
            root=Path(work);args=self.args(root)
            atomic_json(args.resume/'state.json',{'task_id':1,'topic_id':1,
                        'task_type':'lesson','activity_url':'https://mathacademy.com/tasks/1/topics/1/lesson',
                        'questions':{},'examples':{},'current_kp':'already-started'})
            browser,runtime,db,started=test_adaptive_run.AdaptiveRunTests().fixture(work,[2,3])
            with patch('capture.Database',return_value=db), patch('browser.CaptureBrowser',browser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime), \
                 patch('capture.queued_capture_repair') as repair, \
                 contextlib.redirect_stdout(io.StringIO()):
                run(args)
            self.assertEqual(started,[])
            repair.assert_not_called()
            self.assertFalse((args.output/'2').exists())
            state=json.loads((args.resume/'state.json').read_text())
            self.assertTrue(state['activity_complete'] and state['history_complete'] and state['import_deferred'])
            db.import_content.assert_not_called()

    def test_rejects_a_checkpoint_that_failed_before_starting(self):
        with tempfile.TemporaryDirectory() as work:
            root=Path(work);args=self.args(root)
            atomic_json(args.resume/'state.json',{'task_id':1,'topic_id':1,'questions':{},'examples':{}})
            with self.assertRaisesRegex(ValueError,'already started'), patch('capture.Database') as db:
                run(args)
            db.assert_not_called()

    def test_failed_resume_reports_failure_without_starting_other_work(self):
        with tempfile.TemporaryDirectory() as work:
            root=Path(work);args=self.args(root)
            atomic_json(args.resume/'state.json',{'task_id':1,'topic_id':1,
                        'task_type':'lesson','activity_url':'https://mathacademy.com/tasks/1/topics/1/lesson',
                        'questions':{},'examples':{},'current_kp':'already-started'})
            browser,runtime,db,started=test_adaptive_run.AdaptiveRunTests().fixture(work,[2],failures=[1])
            with patch('capture.Database',return_value=db), patch('browser.CaptureBrowser',browser), \
                 patch('playwright.sync_api.sync_playwright',return_value=runtime), \
                 patch('capture_repair.cooldown') as repair, \
                 self.assertRaisesRegex(ValueError,'Fixture capture failure'):
                run(args)
            self.assertEqual(started,[])
            repair.assert_not_called()

    def test_diagnostic_drain_skips_uncertainty_and_preserves_other_failures(self):
        reader=SimpleNamespace(args=SimpleNamespace(finish_in_progress=True),solver=Mock())
        reader.solver.solve.side_effect=ValueError('Solver is uncertain; question saved for review')
        decision=diagnostic_decision(reader,{},Path('/tmp/image'),Path('/tmp/question'),'solve')
        self.assertTrue(decision['diagnostic_finish_skip'])
        self.assertFalse(decision['confident'])
        self.assertEqual(decision['answers'],[])
        reader.args.finish_in_progress=False
        with self.assertRaises(ValueError):diagnostic_decision(reader,{},None,None,'solve')
        reader.args.finish_in_progress=True
        reader.solver.solve.side_effect=ValueError('Malformed fields')
        with self.assertRaisesRegex(ValueError,'Malformed fields'):
            diagnostic_decision(reader,{},None,None,'solve')

    def test_changed_diagnostic_slot_requires_new_unsubmitted_source_identity(self):
        record={'status':'captured','sequence_position':23,'source_question_id':342755,
                'before':{'problem':'old question'}}
        new=replaced_diagnostic_record(record,{'source_question_id':338907},
                                       {'problem':'replacement question'},'/tmp/new.png','question-023')
        self.assertEqual(new['source_question_id'],338907)
        self.assertEqual(record['before']['problem'],'old question')
        self.assertNotEqual(new['solver_directory'],'question-023')
        for unsafe in ({**record,'status':'submitting'}, {**record,'status':'graded'}):
            with self.assertRaises(ValueError):
                replaced_diagnostic_record(unsafe,{'source_question_id':338907},{},None,'question-023')
        with self.assertRaises(ValueError):
            replaced_diagnostic_record(record,{'source_question_id':342755},{},None,'question-023')
        with_answer={**record,'decision':{'answers':[1]}}
        fresh=replaced_diagnostic_record(with_answer,{'source_question_id':338907},{},None,'question-023')
        self.assertNotIn('decision',fresh)
        self.assertIn('decision',with_answer)


if __name__=='__main__':unittest.main()
