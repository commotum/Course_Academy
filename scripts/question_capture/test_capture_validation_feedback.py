"""Failed baseline fixture errors must not veto all-green candidate validation."""
import json
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch
import test_capture_maintenance as maintenance
from capture_repair import prepare
from core import atomic_json

class ValidationFeedbackTests(unittest.TestCase):
    setUp=maintenance.CaptureMaintenanceTests.setUp
    tearDown=maintenance.CaptureMaintenanceTests.tearDown
    failure=maintenance.CaptureMaintenanceTests.failure
    cli=maintenance.CaptureMaintenanceTests.cli

    def candidate(self):
        self.result={'status':'repair','summary':'Targeted fixture regression repair.','file':'math_notation.py',
            'edits':[{'old':'without algebra.','new':'without guessing algebra.'}],
            'regression_test':'import unittest\nclass Regression(unittest.TestCase):\n def test_bug(self): self.fail("original failure")\n'}

    def record(self):
        records=json.loads((self.args.state_dir/'capture-repair/failures.json').read_text())
        return next(iter(records.values()))

    def test_mixed_baseline_failure_and_error_can_reach_all_green_candidate(self):
        self.failure();self.candidate()
        with patch('capture_repair.run_cli',side_effect=self.cli), \
             patch('capture_repair.run_tests',side_effect=[(1,'FAIL: original\nERROR: fixture sentinel'),(0,'OK')]) as tests:
            plan=prepare(self.args,self.pacer)
        self.assertIsNotNone(plan)
        self.assertEqual(tests.call_count,2)
        record=self.record()
        self.assertEqual(record['status'],'tested')
        self.assertEqual(record['validation_feedback']['baseline']['returncode'],1)
        self.assertEqual(record['validation_feedback']['candidate']['returncode'],0)

    def test_candidate_errors_still_reject_patch_and_next_turn_receives_feedback(self):
        self.failure();self.candidate()
        with patch('capture_repair.run_cli',side_effect=self.cli), \
             patch('capture_repair.run_tests',side_effect=[(1,'ERROR: baseline fixture'),(1,'ERROR: candidate fixture sentinel')]):
            with self.assertRaisesRegex(ValueError,'failed offline tests'):
                prepare(self.args,self.pacer)
        record=self.record();self.assertEqual(record['status'],'failed')
        self.assertIn('candidate fixture sentinel',record['validation_feedback']['candidate']['output'])
        payloads=[]
        self.result.update(status='blocked',summary='Needs corrected fixture')
        def cli(command,**kwargs):
            payloads.append(json.loads(kwargs['input'][kwargs['input'].index('{'):]))
            return self.cli(command,**kwargs)
        with patch('capture_repair.run_cli',side_effect=cli):
            self.assertIsNone(prepare(self.args,self.pacer))
        previous=payloads[0]['previous_attempt']
        self.assertIn('baseline fixture',previous['validation_feedback']['baseline']['output'])
        self.assertIn('candidate fixture sentinel',previous['validation_feedback']['candidate']['output'])
        self.assertIn('resume',self.commands[-1])

    def test_passing_baseline_does_not_produce_applicable_patch(self):
        self.failure();self.candidate()
        with patch('capture_repair.run_cli',side_effect=self.cli),patch('capture_repair.run_tests',return_value=(0,'OK')) as tests:
            with self.assertRaisesRegex(ValueError,'must fail on original code'):
                prepare(self.args,self.pacer)
        self.assertEqual(tests.call_count,1)
        self.assertEqual(self.record()['status'],'failed')

    def test_validation_timeout_persists_feedback_and_rejects_patch(self):
        self.failure();self.candidate()
        with patch('capture_repair.run_cli',side_effect=self.cli), \
             patch('capture_repair.run_tests',side_effect=[(1,'FAIL: original'),subprocess.TimeoutExpired('tests',300)]):
            with self.assertRaises(subprocess.TimeoutExpired):
                prepare(self.args,self.pacer)
        record=self.record();self.assertEqual(record['status'],'failed')
        self.assertIn('TimeoutExpired',record['validation_feedback']['candidate']['error'])

    def test_previous_legacy_test_logs_are_backfilled_into_agent_input(self):
        _,diagnostic=self.failure()
        from capture_repair import failure_key,evidence_version,source_version
        report=json.loads(diagnostic.read_text());old=self.root/'legacy-job';old.mkdir()
        (old/'before-tests.txt').write_text('FAIL: prompt identity\nERROR: Recovered sentinel')
        atomic_json(self.args.state_dir/'capture-repair/failures.json',{
            failure_key(report):{'attempts':1,'status':'failed','job':str(old),
                'source_version':source_version(),'evidence_version':evidence_version(diagnostic)}})
        inputs=[]
        def cli(command,**kwargs):
            inputs.append(json.loads(kwargs['input'][kwargs['input'].index('{'):]))
            return self.cli(command,**kwargs)
        with patch('capture_repair.run_cli',side_effect=cli):
            self.assertIsNone(prepare(self.args,self.pacer))
        self.assertIn('Recovered sentinel',inputs[0]['previous_attempt']['validation_feedback']['baseline']['output'])

if __name__=='__main__':unittest.main()
