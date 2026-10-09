"""Saved MathQuill exponent entry and exact comparison boundary checks."""
import json
import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from browser import CaptureBrowser


class AffineExponentEntryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = json.loads((Path(__file__).parent /
                                   'fixtures/affine-exponent-entry.json').read_text())

    def verify(self, intended=None, observed=None, *, unfinished=False):
        field = {'key': 'field-1', 'type': 'blank', 'tag': 'mathquill',
                 'submitted_value': intended or self.evidence['intended']}
        record = {'before': {'problem': self.evidence['problem'], 'fields': [field]}}
        control = Mock()
        control.locator.return_value.count.return_value = int(unfinished)
        control.evaluate.return_value = (self.evidence['observed']
                                         if observed is None else observed)
        with patch('browser.answer_control', return_value=control):
            CaptureBrowser.verify_entered(Mock(), Mock(), record)
        return field

    def test_saved_affine_exponent_entry(self):
        self.assertEqual(self.verify()['observed_mathquill_latex'], self.evidence['observed'])

    def test_correct_answer_and_other_fraction_exponents(self):
        for intended, observed in [(r'e^{2-1/x}', r'e^{2-\frac{1}{x}}'),
                                    (r'e^{x^2/2}', r'e^{\frac{x^2}{2}}'),
                                    (r'e^{3+2/x}', r'e^{3+\frac{2}{x}}')]:
            with self.subTest(intended=intended):
                self.verify(intended, observed)

    def test_sign_denominator_and_scope_differences_stop(self):
        for observed in (r'e^{1+\frac{1}{x}}', r'e^{1-\frac{1}{2x}}',
                         r'e^{1-\frac{2}{x}}', r'\frac{e^{1-1}}{x}',
                         r'e^{\frac{1-1}{x}}', r'e^{1-\frac{1}{x^2}}', None):
            with self.subTest(observed=observed):
                if observed is None:
                    # Non-string MathQuill responses must also fail closed.
                    observed = 1
                with self.assertRaisesRegex(ValueError, 'stop before Submit'):
                    self.verify(observed=observed)

    def test_error_domains_are_not_cancelled(self):
        for intended, observed in [(r'e^{x/x}', 'e'),
                                    (r'e^{1-1/x}', r'e^{1-\frac{x-1}{x(x-1)}}'),
                                    (r'e^{1-1/x}', r'e^{1-\frac{1}{0}}')]:
            with self.subTest(observed=observed):
                with self.assertRaisesRegex(ValueError, 'stop before Submit'):
                    self.verify(intended, observed)

    def test_unavailable_comparison_stops(self):
        with patch.dict(os.environ, {'COURSE_ACADEMY_MATH_COMPARE_BIN': '/missing/exponent-helper'}):
            with self.assertRaisesRegex(ValueError, 'stop before Submit'):
                self.verify()

    def test_unfinished_command_stops_even_if_latex_matches(self):
        with self.assertRaisesRegex(ValueError, 'Unfinished MathQuill command'):
            self.verify(observed=self.evidence['intended'], unfinished=True)


if __name__ == '__main__':
    unittest.main()
