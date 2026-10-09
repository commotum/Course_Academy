"""A proven example stays valid when another displayed example also qualifies."""
import copy
from fractions import Fraction
import unittest
from solver import INSTRUCTIONS, Solver


class NonuniqueExampleTests(unittest.TestCase):
    def setUp(self):
        self.item = {'problem': 'Find a vector parallel to x=t/3-2, y=5-4t, z=2t+1/7.',
                     'fields': [{'key': 'selection', 'type': 'radio', 'choices': [
                         {'option': 'd', 'type': 'math', 'value': '(-1/3,4,-2)'},
                         {'option': 'e', 'type': 'math', 'value': '(1/3,-4,2)'},
                         {'option': 'c', 'type': 'math', 'value': '(1/3,4,2)'}]}]}
        self.answer = {'confident': True, 'explanation': 'e is the coefficient vector; d is its negative.',
                       'answers': [{'key': 'selection', 'correct_option': 'e',
                                    'correct_value': '(1/3,-4,2)', 'value_type': 'math',
                                    'wrong_value': '(1/3,4,2)', 'correct_keys': [], 'wrong_keys': []}]}

    def test_selected_example_proven_despite_second_parallel_choice(self):
        v = (Fraction(1, 3), Fraction(-4), Fraction(2))
        d = tuple(-x for x in v)
        self.assertEqual({x / y for x, y in zip(d, v)}, {Fraction(-1)})
        c = (Fraction(1, 3), Fraction(4), Fraction(2))
        self.assertGreater(len({x / y for x, y in zip(c, v)}), 1)
        Solver.validate(self.item, self.answer)
        self.assertIn('multiple valid displayed choices do not make a proven valid choice', INSTRUCTIONS)
        self.assertIn('Do not infer which option the server accepts', INSTRUCTIONS)

    def test_unresolved_validity_still_stops(self):
        answer = copy.deepcopy(self.answer)
        answer['confident'] = False
        with self.assertRaisesRegex(ValueError, 'uncertain'):
            Solver.validate(self.item, answer)
        self.assertIn("selected answer's mathematical validity is unresolved", INSTRUCTIONS)

    def test_missing_or_mismatched_choice_still_stops(self):
        answer = copy.deepcopy(self.answer)
        answer['answers'][0]['correct_option'] = 'c'
        with self.assertRaisesRegex(ValueError, 'exact displayed choice'):
            Solver.validate(self.item, answer)
        self.item['fields'][0]['choices'] = self.item['fields'][0]['choices'][:1]
        with self.assertRaisesRegex(ValueError, 'exact displayed choice'):
            Solver.validate(self.item, self.answer)


if __name__ == '__main__':
    unittest.main()
