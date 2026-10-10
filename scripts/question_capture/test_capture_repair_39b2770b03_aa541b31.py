import ast
import copy
import json
import unittest
from pathlib import Path
import solver
from solver import Solver, restored_choice_identity
from core import normalize

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/linear/14095809/diagnostics/1791637376659021701/state.json')

class PowerSetRestorationTests(unittest.TestCase):
    def setUp(self):
        record = json.loads(EVIDENCE.read_text())['questions']['q-105123']
        self.item = copy.deepcopy(record['before'])
        self.answer = copy.deepcopy(record['decision'])
        self.choices = self.item['fields'][0]['choices']
        self.assertEqual(self.answer['answers'][0]['correct_option'], 'a')
        self.assertEqual(self.choices[0]['value'], '{∅,{k},{m},{o},{k,m},{k,o},{m,o},{k,m,o}}')
        self.assertEqual(self.choices[2]['value'], '{∅,k,m,o,{k,m},{k,o},{m,o},{k,m,o}}')

    def test_original_identity_collapses_singletons(self):
        source = Path(solver.__file__).read_text()
        node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'restored_choice_identity')
        namespace = {'re': solver.re, 'normalize': normalize}
        original = ast.get_source_segment(source, node).replace('[{}∅A-Za-z0-9,', '[{}A-Za-z0-9,', 1)
        exec(original, namespace)
        identity = namespace['restored_choice_identity']
        a, c = self.choices[0], self.choices[2]
        self.assertEqual(identity(a['value'], a['type'], a.get('html','')), identity(c['value'], c['type'], c.get('html','')))

    def test_saved_answer_restores_without_mutating_evidence(self):
        snapshot = copy.deepcopy((self.item, self.answer))
        result = Solver.reuse_answer(self.item, self.answer, self.item)
        self.assertEqual(result['answers'][0]['correct_option'], 'a')
        self.assertEqual((self.item, self.answer), snapshot)

    def test_shuffled_letters_follow_set_value(self):
        saved = copy.deepcopy(self.item)
        self.choices[0]['option'] = 'z'
        result = Solver.reuse_answer(self.item, self.answer, saved)
        self.assertEqual(result['answers'][0]['correct_option'], 'z')

    def test_elements_cannot_replace_singleton_subsets(self):
        saved = copy.deepcopy(self.item)
        self.item['fields'][0]['choices'] = self.choices[1:]
        with self.assertRaisesRegex(ValueError, 'does not match exactly one restored choice'):
            Solver.reuse_answer(self.item, self.answer, saved)

    def test_duplicate_correct_choices_remain_ambiguous(self):
        saved = copy.deepcopy(self.item)
        duplicate = copy.deepcopy(self.choices[0])
        duplicate['option'] = 'z'
        self.choices.append(duplicate)
        with self.assertRaisesRegex(ValueError, 'does not match exactly one restored choice'):
            Solver.reuse_answer(self.item, self.answer, saved)

if __name__ == '__main__':
    unittest.main()
