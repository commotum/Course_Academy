import ast
import json
import re
import unittest
from pathlib import Path

from core import normalize

SOURCE = Path(__file__).with_name('browser.py')
ACTIVITY = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/multivariable/14041466')


def load_normalizer():
    parsed = ast.parse(SOURCE.read_text())
    functions = [n for n in parsed.body if isinstance(n, ast.FunctionDef)
                 and n.name == 'normalize_mathquill']
    if len(functions) != 1:
        raise AssertionError('Expected production MathQuill normalizer')
    namespace = {'re': re, 'normalize': normalize}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), 'exec'), namespace)
    return namespace['normalize_mathquill']


class SavedExponentEntryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # The immutable failure checkpoint survives a successful live resume.
        state = json.loads((ACTIVITY / 'diagnostics/1791445914936355510/state.json').read_text())
        record = state['questions']['q-355562']
        assert record['status'] == 'prepared'
        field = record['before']['fields'][0]
        assert field['tag'] == 'mathquill'
        cls.intended = field['submitted_value']
        cls.observed = field['observed_mathquill_latex']
        cls.wrong = record['decision']['answers'][0]['wrong_value']
        assert cls.intended == 'e^{x^2/2}'
        assert cls.observed.replace('\\\\', '\\') == r'e^{\frac{x^2}{2}}'
        cls.normalize_editor = staticmethod(load_normalizer())

    def test_original_saved_failure(self):
        self.assertNotEqual(normalize(self.observed), normalize(self.intended))

    def test_saved_entry_matches_with_candidate(self):
        self.assertEqual(self.normalize_editor(self.observed),
                         self.normalize_editor(self.intended))

    def test_wrong_values_and_changed_scope_still_fail(self):
        for value in (self.wrong, r'e^{x^2}/2', r'e^{x^{2/2}}',
                      r'e^{\frac{x^2}{3}}', r'e^{x^2/2x}', r'e^{x^2/2/3}',
                      r'e^{x^2+1/2}', r'e^{x^2/0}'):
            with self.subTest(value=value):
                self.assertNotEqual(self.normalize_editor(value),
                                    self.normalize_editor(self.observed))

    def test_quotients_outside_exponent_remain_distinct(self):
        self.assertNotEqual(self.normalize_editor('x^2/2'),
                            self.normalize_editor(r'\frac{x^2}{2}'))


if __name__ == '__main__':
    unittest.main()
