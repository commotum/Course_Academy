import ast
import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14040240')


class PoweredDenominatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = Path(__file__).with_name('browser.py')
        tree = ast.parse(source.read_text())
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'mathquill_keys')
        namespace = {'re': re}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), namespace)
        cls.keys = staticmethod(namespace['mathquill_keys'])
        state = json.loads((ROOT / 'state.json').read_text())

        def find(value):
            if isinstance(value, dict):
                if value.get('correct_value') == r'2+\frac{12}{(t+2)^3}' and 'correct_keys' in value:
                    return value
                for child in value.values():
                    result = find(child)
                    if result is not None:
                        return result
            elif isinstance(value, list):
                for child in value:
                    result = find(child)
                    if result is not None:
                        return result

        cls.answer = find(state)
        if cls.answer is None:
            raise AssertionError('Saved decision missing')

    def test_saved_correct_and_wrong_actions_keep_power_in_denominator(self):
        for kind in ('correct', 'wrong'):
            value = self.answer[kind + '_value']
            original = self.answer[kind + '_keys']
            snapshot = copy.deepcopy(original)
            fixed = self.keys(value, original)
            self.assertEqual(fixed, original[:3] + original[4:])
            self.assertEqual(original, snapshot)
            self.assertEqual(fixed[2]['text'], '(t+2)')
            self.assertEqual(fixed[3]['text'], '^3')
            self.assertEqual(fixed[-2:], [{'text': None, 'key': 'ArrowRight'}] * 2)

    def test_original_cursor_exit_is_the_unsafe_alternative(self):
        actions = self.answer['correct_keys']
        self.assertEqual(actions[2:5], [
            {'text': '(t+2)', 'key': None},
            {'text': None, 'key': 'ArrowRight'},
            {'text': '^3', 'key': None}])
        report = json.loads((ROOT / 'diagnostics/1791438059024765579/error.json').read_text())
        self.assertIn(r'\\left(t+2\\right)}^3', report['message'])
        self.assertNotEqual(actions, self.keys(self.answer['correct_value'], actions))

    def test_different_intention_does_not_rewrite_keys(self):
        actions = self.answer['correct_keys']
        for value in (r'2+\frac{12}{(t+2)}^3', r'2+\frac{12}{(t+2)^4}'):
            self.assertEqual(self.keys(value, actions), actions)

    def test_already_correct_actions_are_unchanged(self):
        actions = self.answer['correct_keys']
        corrected = actions[:3] + actions[4:]
        self.assertEqual(self.keys(self.answer['correct_value'], corrected), corrected)


if __name__ == '__main__':
    unittest.main()
