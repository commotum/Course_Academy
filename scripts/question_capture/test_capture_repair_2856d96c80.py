import json
import unittest
from pathlib import Path

from core import compare_answers

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/13996204')

class NegativeRoundingInstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.predicted = json.loads((ROOT / 'q-346090/solve-answer.json').read_text())['answers'][0]
        cls.verified = json.loads((ROOT / 'q-346090/verify-answer.json').read_text())['answers'][0]
        cls.prompt = json.loads((ROOT / 'q-346090-before.json').read_text())['problem']

    def compare(self, other, prompt=None):
        return compare_answers(self.predicted['correct_value'], other, 'math',
                               prompt=self.prompt if prompt is None else prompt)['outcome']

    def test_saved_exact_answers_are_equivalent(self):
        self.assertIn('Do not round the answer.', self.prompt)
        self.assertEqual(self.compare(self.verified['correct_value']), 'equivalent')

    def test_saved_wrong_answer_still_fails(self):
        self.assertNotEqual(self.compare(self.predicted['wrong_value']), 'equivalent')

    def test_positive_rounding_constraint_is_preserved(self):
        prompt = self.prompt.replace('Do not round the answer.', 'Round the answer to two decimal places.')
        self.assertNotEqual(self.compare(self.verified['correct_value'], prompt), 'equivalent')

    def test_other_form_constraints_are_preserved(self):
        prompt = self.prompt + ' Round the answer to two decimal places.'
        self.assertNotEqual(self.compare(self.verified['correct_value'], prompt), 'equivalent')

if __name__ == '__main__':
    unittest.main()
