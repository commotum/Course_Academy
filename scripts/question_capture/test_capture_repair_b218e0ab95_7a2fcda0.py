import ast
import json
import re
import unittest
from pathlib import Path


class PiExponentNotationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = Path(__file__).with_name('browser.py')
        notation = {}
        notation_source = source.with_name('math_notation.py')
        exec(compile(notation_source.read_text(), str(notation_source), 'exec'), notation)
        node = next(n for n in ast.parse(source.read_text()).body
                    if isinstance(n, ast.FunctionDef) and n.name == 'normalize_mathquill')
        namespace = {'re': re, 'normalize': notation['identity']}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(source), 'exec'), namespace)
        cls.normalize = staticmethod(namespace['normalize_mathquill'])
        report = json.loads(Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14042486/diagnostics/1791452285306398878/error.json').read_text())
        observed, intended = report['message'].split('stop before Submit: ', 1)[1].split(' != ')
        cls.observed = ast.literal_eval(observed)
        cls.intended = ast.literal_eval(intended)

    def test_saved_exponent_fraction_is_equivalent(self):
        self.assertEqual(self.observed, r'e^{\frac{3\pi}{2}}-1')
        self.assertEqual(self.intended, r'e^{3\pi/2}-1')
        self.assertEqual(self.normalize(self.observed), self.normalize(self.intended))

    def test_unsafe_grouping_still_differs(self):
        for value in (r'e^{3\pi}/2-1', r'e^{3\pi/2t}-1',
                      r'e^{3\pi/2/2}-1', r'e^{3\pi+1/2}-1',
                      r'e^{\frac{3\pi}{3}}-1'):
            with self.subTest(value=value):
                self.assertNotEqual(self.normalize(value), self.normalize(self.observed))

    def test_existing_variable_exponent_identity_is_preserved(self):
        self.assertEqual(self.normalize(r'e^{x/2}'),
                         self.normalize(r'e^{\frac{x}{2}}'))

    def test_plain_letters_do_not_become_pi(self):
        self.assertNotEqual(self.normalize(r'e^{3pi/2}-1'),
                            self.normalize(self.observed))


if __name__ == '__main__':
    unittest.main()
