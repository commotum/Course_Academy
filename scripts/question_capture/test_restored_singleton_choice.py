"""Restoration preserves literal MathML fences and ordinary TeX grouping."""
import copy
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
from browser import CaptureBrowser
from core import normalize
from solver import Solver, restored_choice_identity

FIXTURE = Path(__file__).parent/'fixtures/restored-singleton-choice'


class RestoredSingletonTests(unittest.TestCase):
    def test_real_invertible_matrix_choices_restore_scalar_n(self):
        item = json.loads((FIXTURE/'question.json').read_text())
        answer = json.loads((FIXTURE/'answer.json').read_text())
        original = copy.deepcopy((item, answer))
        self.assertEqual(normalize('n'), normalize('{n}'))
        self.assertEqual(Solver.reuse_answer(item, answer), answer)
        self.assertEqual((item, answer), original)

    def item_answer(self, value):
        literal = '<math><mo fence="false">{</mo><mi>'+value+'</mi><mo>}</mo></math>'
        item = {'fields':[{'key':'selection','type':'radio','choices':[
            {'option':'a','type':'math','value':'{'+value+'}','html':literal},
            {'option':'b','type':'math','value':value,'html':'<math><mi>'+value+'</mi></math>'}]}]}
        answer = {'confident':True,'answers':[{'key':'selection','value_type':'math',
                  'correct_option':'b','correct_value':value}]}
        return item, answer

    def test_singletons_do_not_equal_scalars(self):
        for value in ('n','0','1'):
            with self.subTest(value=value):
                item, answer = self.item_answer(value)
                result = Solver.reuse_answer(item, answer)
                self.assertEqual(result['answers'][0]['correct_option'], 'b')
                answer['answers'][0].update(correct_option='a',correct_value='{'+value+'}')
                self.assertEqual(Solver.reuse_answer(item, answer)['answers'][0]['correct_option'], 'a')

    def test_shuffled_letters_use_captured_value_and_fences(self):
        item, answer = self.item_answer('n')
        saved = copy.deepcopy(item)
        item['fields'][0]['choices'][1]['option'] = 'z'
        self.assertEqual(Solver.reuse_answer(item, answer, saved)['answers'][0]['correct_option'], 'z')

    def test_legacy_literal_singleton_matches_explicit_fences(self):
        item, answer = self.item_answer('n')
        answer['answers'][0].update(correct_option='a',correct_value='{n}')
        saved = copy.deepcopy(item)
        item['fields'][0]['choices'][0]['value'] = r'\{n\}'
        self.assertEqual(Solver.reuse_answer(item, answer, saved)['answers'][0]['correct_value'], r'\{n\}')

    def test_duplicate_choices_and_missing_scalar_still_fail(self):
        item, answer = self.item_answer('n')
        saved = copy.deepcopy(item)
        item['fields'][0]['choices'].append(dict(item['fields'][0]['choices'][1],option='z'))
        with self.assertRaisesRegex(ValueError, 'exactly one restored choice'):
            Solver.reuse_answer(item, answer, saved)
        item['fields'][0]['choices'] = item['fields'][0]['choices'][:1]
        with self.assertRaisesRegex(ValueError, 'exactly one restored choice'):
            Solver.reuse_answer(item, answer, saved)

    def test_ordinary_groups_fraction_groups_and_sine_notation(self):
        pairs = [('{n}','n'), (r'\frac{{1}}{{2}}',r'\frac{1}{2}'),
                 (r'-\sin(t)',r'-\sin{(t)}')]
        for left, right in pairs:
            with self.subTest(left=left):
                self.assertEqual(restored_choice_identity(left,'math'), restored_choice_identity(right,'math'))
        self.assertNotEqual(restored_choice_identity(r'\{n\}','math'), restored_choice_identity('(n)','math'))
        self.assertNotEqual(restored_choice_identity(r'\{n\}','math'), restored_choice_identity(r'\{n,n\}','math'))

    def test_uncertain_answer_still_fails(self):
        item, answer = self.item_answer('n')
        answer['confident'] = False
        with self.assertRaisesRegex(ValueError, 'Solver is uncertain'):
            Solver.reuse_answer(item, answer)

    def test_saved_wrong_scalar_does_not_match_a_literal_singleton(self):
        item, answer = self.item_answer('0')
        field = item['fields'][0]
        field['choices'].append({'option':'c','type':'math','value':'n','dom_id':'correct'})
        for choice in field['choices']:
            choice.setdefault('dom_id',choice['option'])
        answer['answers'][0].update(correct_option='c',correct_value='n')
        record = {'before':item,'decision':answer,'intended':'W',
                  'wrong_choice':{'key':'selection','type':'math','value':'0'}}
        browser = CaptureBrowser.__new__(CaptureBrowser)
        browser.pacer = SimpleNamespace(wait=lambda *a:None,rng=Mock())
        with patch('browser.by_id') as by_id:
            browser.enter(object(),record)
        by_id.assert_called_once()
        self.assertEqual(by_id.call_args.args[1], 'b')
        browser.pacer.rng.choice.assert_not_called()
        self.assertEqual(field['submitted_value'], '0')

    def test_saved_wrong_literal_singleton_keeps_its_fences(self):
        item, answer = self.item_answer('0')
        field = item['fields'][0]
        field['choices'].append({'option':'c','type':'math','value':'n','dom_id':'correct'})
        for choice in field['choices']:
            choice.setdefault('dom_id',choice['option'])
        answer['answers'][0].update(correct_option='c',correct_value='n')
        record = {'before':item,'decision':answer,'intended':'W',
                  'wrong_choice':{'key':'selection','type':'math','value':'{0}'}}
        browser = CaptureBrowser.__new__(CaptureBrowser)
        browser.pacer = SimpleNamespace(wait=lambda *a:None,rng=Mock())
        with patch('browser.by_id') as by_id:
            browser.enter(object(),record)
        self.assertEqual(by_id.call_args.args[1], 'a')
        self.assertEqual(field['submitted_value'], '{0}')


if __name__ == '__main__':
    unittest.main()
