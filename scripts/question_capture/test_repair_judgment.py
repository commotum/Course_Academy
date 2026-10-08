"""Interrupted checkpoints reach recovery; routine repairs validate focused evidence."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from capture_repair import apply, evidence_version, failure_key, next_failure, prepare, safe_resume, source_version, validation_names
from core import atomic_json
import test_capture_maintenance as maintenance


class RepairJudgmentTests(unittest.TestCase):
    def test_resume_preserves_uncertain_checkpoint_for_reader_judgment(self):
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp)/'17';diagnostic=directory/'diagnostics/1/error.json'
            diagnostic.parent.mkdir(parents=True)
            state={'questions':{'q-17':{'status':'submitting','before':{'problem':'Find x'}}},
                   'pending_continue':{'source_step':'q-17'},'test_submission_status':'confirming'}
            atomic_json(directory/'state.json',state)
            original=(directory/'state.json').read_bytes()
            self.assertEqual(safe_resume({'diagnostic':str(diagnostic)}),str(directory.resolve()))
            self.assertEqual((directory/'state.json').read_bytes(),original)

    def test_focused_validation_by_default_and_full_only_when_needed(self):
        selected=validation_names(['browser.py'],'test_observed_failure',{})
        self.assertIn('test_observed_failure',selected.split(','))
        self.assertIn('test_unfinished_recovery',selected.split(','))
        self.assertNotEqual(selected,'discover')
        self.assertEqual(validation_names(['browser.py'],'test_observed_failure',{'validation':'full'}),'discover')
        self.assertEqual(validation_names(['browser.py','dom.js','assessment.py'],'test_observed_failure',{}),'discover')

    def fixture(self):
        fixture=maintenance.CaptureMaintenanceTests();fixture.setUp();self.addCleanup(fixture.tearDown)
        return fixture

    def test_new_checkpoint_evidence_revisits_previously_blocked_diagnosis(self):
        fixture=self.fixture();directory,diagnostic=fixture.failure()
        report=json.loads(diagnostic.read_text());key=failure_key(report)
        ledger={key:{'status':'blocked','attempts':2,'source_version':source_version(),
                     'evidence_version':evidence_version(diagnostic)}}
        self.assertIsNone(next_failure(fixture.args,ledger))
        atomic_json(directory/'state.json',{'task_id':1,'questions':{'q-1':{'actual_result':'Correct'}}})
        self.assertEqual(next_failure(fixture.args,ledger)[0],diagnostic)

    def test_related_multifile_fix_is_staged_with_focused_validation(self):
        fixture=self.fixture();fixture.failure()
        fixture.result={'status':'repair','summary':'Two-file targeted repair.','file':'','edits':[],
                        'patches':[{'file':'math_notation.py','edits':[{'old':'without algebra.','new':'without symbolic algebra.'}]},
                                   {'file':'browser.py','edits':[{'old':'class CaptureBrowser:','new':'class CaptureBrowser:  # tested recovery'}]}],
                        'regression_test':'import unittest','validation':'focused'}
        with patch('capture_repair.run_cli',side_effect=fixture.cli), \
             patch('capture_repair.run_tests',side_effect=[(1,'FAIL: observed failure'),(0,'OK')]) as tests:
            plan=prepare(fixture.args,fixture.pacer)
        self.assertEqual([item['file'] for item in plan['patches']],['math_notation.py','browser.py'])
        self.assertNotEqual(tests.call_args_list[1].args[1],'discover')
        self.assertIn('without symbolic algebra.',plan['patches'][0]['candidate'])

    def test_absolute_allowed_source_path_reaches_candidate_validation(self):
        import capture_repair
        fixture=self.fixture();fixture.failure()
        fixture.result={'status':'repair','summary':'Targeted recovery.','file':str((capture_repair.PACKAGE/'browser.py').resolve()),
                        'edits':[{'old':'class CaptureBrowser:','new':'class CaptureBrowser:  # tested recovery'}],
                        'regression_test':'import unittest','validation':'focused'}
        with patch('capture_repair.run_cli',side_effect=fixture.cli), \
             patch('capture_repair.run_tests',side_effect=[(1,'FAIL: observed failure'),(0,'OK')]) as tests:
            plan=prepare(fixture.args,fixture.pacer)
        self.assertEqual(plan['file'],'browser.py')
        self.assertEqual(tests.call_count,2)

    def test_absolute_path_outside_allowed_package_is_rejected(self):
        fixture=self.fixture();fixture.failure()
        fixture.result={'status':'repair','summary':'Invalid target.','file':str(fixture.root/'browser.py'),
                        'edits':[{'old':'class CaptureBrowser:','new':'changed'}],'regression_test':'import unittest'}
        with patch('capture_repair.run_cli',side_effect=fixture.cli), \
             patch('capture_repair.run_tests') as tests,self.assertRaisesRegex(ValueError,'allowed source patches'):
            prepare(fixture.args,fixture.pacer)
        tests.assert_not_called()

    def test_interrupted_repair_without_session_identity_restarts_diagnosis(self):
        fixture=self.fixture();fixture.failure()
        directory=fixture.args.state_dir/'capture-repair';directory.mkdir(parents=True)
        atomic_json(directory/'session.json',{'session_id':None,'pending_turn':{'events':str(directory/'missing-events.jsonl')}})
        with patch('capture_repair.run_cli',side_effect=fixture.cli):
            self.assertIsNone(prepare(fixture.args,fixture.pacer))
        restored=json.loads((directory/'session.json').read_text())
        self.assertEqual(restored['session_id'],fixture.sid)
        self.assertEqual(len(restored['interrupted_turns']),1)

    def test_multifile_application_checks_all_sources_before_changing_any(self):
        with tempfile.TemporaryDirectory() as temp:
            package=Path(temp);(package/'a.py').write_text('a');(package/'b.py').write_text('changed')
            plan={'patches':[{'file':'a.py','original':'a','candidate':'new-a'},
                             {'file':'b.py','original':'b','candidate':'new-b'}],
                  'test_name':'test_regression','regression_test':'import unittest'}
            with patch('capture_repair.PACKAGE',package),self.assertRaisesRegex(ValueError,'source changed'):
                apply(plan)
            self.assertEqual((package/'a.py').read_text(),'a')


if __name__=='__main__':unittest.main()
