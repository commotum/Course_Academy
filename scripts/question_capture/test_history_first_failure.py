"""Bind a proof's first terminal failure without merging other grade outcomes."""
import copy
import json
import unittest
from pathlib import Path

from browser import history_result_matches


class FirstFailureHistoryTests(unittest.TestCase):
    def setUp(self):
        fixture = Path(__file__).parent/'fixtures/staged-proof/first-failure-no-credit.json'
        self.evidence = json.loads(fixture.read_text())
        self.record = copy.deepcopy(self.evidence['record'])

    def test_authentic_first_failure_binds_no_credit_without_changing_live_grade(self):
        self.assertIn('>No Credit</span>', self.evidence['history_grade_html'])
        original = copy.deepcopy(self.record)
        self.assertTrue(history_result_matches(self.record, 'No Credit'))
        self.assertEqual(self.record, original)
        self.assertEqual(self.record['actual_result'], 'Incorrect')
        for grade in ('Correct', 'Full Credit', 'Partial Credit'):
            self.assertFalse(history_result_matches(self.record, grade))

    def test_ordinary_incorrect_and_unattested_proof_stages_still_conflict(self):
        self.assertFalse(history_result_matches({'actual_result':'Incorrect'}, 'No Credit'))
        mutations = [
            lambda r:r.update(proof_stages=[{}]),
            lambda r:r['proof_stages'][0].update(outcome='accepted'),
            lambda r:r['proof_stages'][0]['observation'].update(result='Partial Credit'),
            lambda r:r['proof_stages'][0]['observation'].update(dom_id='another-question'),
            lambda r:r['after'].update(result='Correct'),
            lambda r:r['proof_stages'][0].update(submitted_keys=[]),
            lambda r:r['proof_stages'][0].update(submitted_keys=['missing-field']),
            lambda r:r['proof_stages'][0]['observation']['fields'][0].pop('submitted_value'),
            lambda r:r['proof_stages'][0]['observation']['fields'][1].update(source_result='Correct'),
            lambda r:r['proof_stages'].insert(0, {'outcome':'accepted'}),
            lambda r:r.update(actual_result='Partial Credit'),
        ]
        for mutation in mutations:
            record = copy.deepcopy(self.record)
            mutation(record)
            with self.subTest(record=record):
                self.assertFalse(history_result_matches(record, 'No Credit'))


if __name__ == '__main__':
    unittest.main()
