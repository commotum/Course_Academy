import copy
import json
import unittest
from pathlib import Path

from solver import INSTRUCTIONS, Solver, recheck_choice_confidence

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/multivariable/14043502/q-72005')


class EquivalentDomainChoiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.item = json.loads((EVIDENCE / 'solve-before-choice-policy-input.json').read_text())
        cls.answer = json.loads((EVIDENCE / 'solve-before-choice-policy-answer.json').read_text())

    def test_original_cached_failure(self):
        self.assertIs(self.answer['confident'], False)
        self.assertEqual(self.answer['answers'][0]['correct_option'], 'e')
        with self.assertRaisesRegex(ValueError, 'Solver is uncertain'):
            Solver.reuse_answer(self.item, self.answer)

    def test_old_uncertain_choice_gets_one_policy_recheck(self):
        self.assertTrue(recheck_choice_confidence(self.item, self.answer, self.item))
        revised = dict(self.item, choice_confidence_policy='equivalent-choices-v1')
        self.assertFalse(recheck_choice_confidence(revised, self.answer, self.item))
        confident = dict(self.answer, confident=True)
        self.assertFalse(recheck_choice_confidence(self.item, confident, self.item))
        blank = {'fields': [{'key': 'field-1', 'type': 'blank'}]}
        self.assertFalse(recheck_choice_confidence(self.item, self.answer, blank))

    def test_proven_exact_displayed_answer_remains_valid(self):
        result = copy.deepcopy(self.answer)
        result['confident'] = True
        Solver.validate(self.item, result)
        self.assertIn('Equivalent displayed choices do not make a proven valid answer uncertain', INSTRUCTIONS)
        self.assertIn('Never invent an unavailable option', INSTRUCTIONS)

    def test_policy_does_not_force_confidence_or_allow_mismatched_choice(self):
        with self.assertRaisesRegex(ValueError, 'Solver is uncertain'):
            Solver.validate(self.item, self.answer)
        result = copy.deepcopy(self.answer)
        result['confident'] = True
        result['answers'][0]['correct_option'] = 'a'
        with self.assertRaisesRegex(ValueError, 'exact displayed choice'):
            Solver.validate(self.item, result)
        result['answers'][0]['correct_option'] = None
        with self.assertRaisesRegex(ValueError, 'exact displayed choice'):
            Solver.validate(self.item, result)


if __name__ == '__main__':
    unittest.main()
