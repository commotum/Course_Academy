"""MathQuill readback regressions from saved capture evidence."""
import unittest

from scripts.browser.entry import normalized_math, write_math


class ReadbackControl:
    def __init__(self, observed):
        self.observed = observed

    def evaluate(self, script, value):
        return self.observed


class MathSubscriptTests(unittest.TestCase):
    def test_captured_logarithm_readback_accepts_single_token_braces(self):
        # Linear task 14267030, question q-228738: MathQuill dropped the
        # optional braces around base 4 inside the fraction.
        expected = r'\frac{\log_{4}(2x+10)}{3}'
        observed = r'\frac{\log_4(2x+10)}{3}'
        self.assertEqual(write_math(ReadbackControl(observed), expected, []), observed)

    def test_single_token_subscripts_accept_letters_and_digits(self):
        for expected, observed in [('x_{i}', 'x_i'), ('x_{4}', 'x_4'),
                                   ('a_{i}^{2}', 'a_i^2')]:
            with self.subTest(expected=expected):
                self.assertEqual(normalized_math(expected), normalized_math(observed))

    def test_subscript_group_scope_is_preserved(self):
        for left, right in [('x_12', 'x_{12}'), ('x_ab', 'x_{ab}'),
                            ('x_a+b', 'x_{a+b}'), ('x_{i+1}', 'x_i+1'),
                            (r'\log_2(x)', r'\log_3(x)')]:
            with self.subTest(left=left, right=right):
                self.assertNotEqual(normalized_math(left), normalized_math(right))
        self.assertEqual(normalized_math('x_12'), normalized_math('x_{1}2'))
        self.assertEqual(normalized_math('x_ab'), normalized_math('x_{a}b'))

    def test_changed_logarithm_base_still_fails_readback(self):
        with self.assertRaisesRegex(ValueError, 'Math editor readback differs'):
            write_math(ReadbackControl(r'\frac{\log_3(2x+10)}{3}'),
                       r'\frac{\log_{4}(2x+10)}{3}', [])

    def test_literal_underscore_is_not_a_subscript(self):
        self.assertNotEqual(normalized_math(r'x\_a'), normalized_math(r'x\_{a}'))


if __name__ == '__main__':
    unittest.main()
