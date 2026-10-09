import copy
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
from browser import CaptureBrowser

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/differential/14069003')
MID = 'q-343341'


class FinalizeRevealedProofTests(unittest.TestCase):
    def setUp(self):
        self.state = json.loads((ROOT / 'diagnostics/1791519559430219638/state.json').read_text())
        self.record = self.state['questions'][MID]
        self.verified = json.loads((ROOT / MID / 'verify-answer.json').read_text())
        self.reader = CaptureBrowser.__new__(CaptureBrowser)
        self.reader.solver = SimpleNamespace(solve=Mock(return_value=self.verified))

    def test_saved_failure_and_complete_recovery(self):
        original = {a['key']: a for a in self.record['decision']['answers']}
        self.assertEqual(list(original), ['field-1'])
        with self.assertRaises(KeyError):
            original['field-2']
        before = copy.deepcopy(self.record['before'])
        stages = copy.deepcopy(self.record['proof_stages'])
        predicted = copy.deepcopy(self.record['decision']['answers'])
        CaptureBrowser.finalize_question(self.reader, self.state, ROOT, MID, self.record)
        self.assertTrue(self.record['finalized'])
        self.assertEqual(self.record['predicted_answers'], predicted)
        self.assertEqual(self.record['before'], before)
        self.assertEqual(self.record['proof_stages'], stages)
        self.assertEqual(self.record['actual_result'], 'Incorrect')
        self.assertEqual(self.record['intended'], 'W')
        self.assertEqual(len(self.record['decision']['answers']), 4)
        for actual, verified in zip(self.record['decision']['answers'], self.verified['answers']):
            for key in ('key', 'correct_value', 'correct_option', 'value_type'):
                self.assertEqual(actual[key], verified[key])
        self.assertEqual(self.record['decision']['answers'][0]['wrong_value'], predicted[0]['wrong_value'])
        self.assertEqual(len(self.record['content']['answer_fields']), 4)
        self.assertTrue(all(f['correct_origin'] == 'model_interpretation'
                            for f in self.record['content']['answer_fields']))
        self.reader.solver.solve.assert_called_once()

    def test_incomplete_verification_rejected_before_mutation(self):
        self.verified['answers'].pop()
        original = copy.deepcopy(self.record['decision'])
        with self.assertRaisesRegex(ValueError, 'exactly the observed fields'):
            CaptureBrowser.finalize_question(self.reader, self.state, ROOT, MID, self.record)
        self.assertEqual(self.record['decision'], original)
        self.assertNotIn('finalized', self.record)

    def test_unavailable_choice_rejected_before_mutation(self):
        self.verified['answers'][1]['correct_option'] = 'missing'
        original = copy.deepcopy(self.record['decision'])
        with self.assertRaisesRegex(ValueError, 'exact displayed choice'):
            CaptureBrowser.finalize_question(self.reader, self.state, ROOT, MID, self.record)
        self.assertEqual(self.record['decision'], original)
        self.assertNotIn('finalized', self.record)


if __name__ == '__main__':
    unittest.main()
