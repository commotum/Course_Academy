import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from core import normalize
from solver import Solver


class RestoredSetChoices(unittest.TestCase):
    def setUp(self):
        # Transcribed from supplied current-question.json and saved decision.
        values = ['{a,b,c,d}', '{a,b,c}', '{b,c,d}',
                  '{{a},b,c,d}', '{{a},{b},{c},d}']
        self.item = {
            'problem': 'Which set is equivalent to $R={a,b,a,c,a,d}?$',
            'fields': [{'key': 'selection', 'type': 'radio',
                        'choices_complete': True,
                        'choices': [{'option': letter, 'type': 'math', 'value': value}
                                    for letter, value in zip('abcde', values)]}]
        }
        self.result = {
            'confident': True,
            'explanation': 'Ignoring repeated elements, R contains exactly a, b, c, and d. Therefore, option a contains the same elements as R.',
            'answers': [{'key': 'selection', 'correct_option': 'a',
                         'correct_value': '{a,b,c,d}', 'value_type': 'math',
                         'wrong_value': '{a,b,c}', 'correct_keys': [], 'wrong_keys': []}]
        }

    def test_original_matching_collides_on_supplied_evidence(self):
        choices = self.item['fields'][0]['choices']
        matches = [c['option'] for c in choices
                   if normalize(c['value'], c['type']) ==
                   normalize(self.result['answers'][0]['correct_value'], 'math')]
        self.assertEqual(matches, ['a', 'd', 'e'])

    def test_saved_answer_reuses_without_mutating_inputs(self):
        before = copy.deepcopy((self.item, self.result))
        self.assertEqual(Solver.reuse_answer(self.item, self.result), self.result)
        self.assertEqual((self.item, self.result), before)

    def test_shuffled_letters_follow_value(self):
        self.item['fields'][0]['choices'][0]['option'] = 'z'
        result = Solver.reuse_answer(self.item, self.result)
        self.assertEqual(result['answers'][0]['correct_option'], 'z')
        self.assertEqual(result['answers'][0]['wrong_value'], '{a,b,c}')

    def test_nested_singleton_is_not_the_saved_answer(self):
        for index in (3, 4):
            with self.subTest(index=index):
                item = copy.deepcopy(self.item)
                item['fields'][0]['choices'] = [item['fields'][0]['choices'][index]]
                with self.assertRaisesRegex(ValueError, 'exactly one restored choice'):
                    Solver.reuse_answer(item, self.result)

    def test_duplicate_correct_choices_still_fail(self):
        choice = copy.deepcopy(self.item['fields'][0]['choices'][0])
        choice['option'] = 'z'
        self.item['fields'][0]['choices'].append(choice)
        with self.assertRaisesRegex(ValueError, 'exactly one restored choice'):
            Solver.reuse_answer(self.item, self.result)

    def test_explicit_set_fences_match_legacy_visible_braces(self):
        self.item['fields'][0]['choices'][0]['value'] = r'\{a,b,c,d\}'
        result = Solver.reuse_answer(self.item, self.result)
        self.assertEqual(result['answers'][0]['correct_value'], r'\{a,b,c,d\}')


if __name__ == '__main__':
    unittest.main()
