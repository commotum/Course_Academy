"""Regressions for source TeX damaged at the Markdown boundary."""
import json
from pathlib import Path
import unittest

from math_format import MATH, normalize_math_boundaries, validate_math_boundaries


class MathBoundaryTests(unittest.TestCase):
    def check(self, source, expected):
        self.assertEqual(normalize_math_boundaries(source), expected)
        self.assertEqual(normalize_math_boundaries(expected), expected)
        validate_math_boundaries(expected)

    def test_reported_solution_keeps_all_derivation_rows(self):
        root = Path(__file__).resolve().parents[2]
        source = json.loads((root / 'reference/edb-math/audits/2026-10-23-solution-latex-17592186233932/question.json').read_text())[':question/worked-solution']
        result = normalize_math_boundaries(source)
        validate_math_boundaries(result)
        self.assertEqual(result.count(r'\\[5pt]'), source.count(r'\\[5pt]'))
        self.assertNotIn(r'\begin{align*}', result)
        self.assertNotIn(r'\eqalign', result)
        self.assertEqual(result.count(r'\begin{aligned}'), 2)
        self.assertIn(r'\pi\sqrt{2}', result)

    def test_row_spacing_does_not_hide_a_following_environment(self):
        source = '\\begin{align}x&=1\\\\[5pt]\n\\end{align}\n\n\\begin{align}y&=2\\end{align}\n\\[z=3\\]'
        result = normalize_math_boundaries(source)
        self.assertEqual(result.count('$$'), 4)
        validate_math_boundaries(result)

    def test_adjacent_math_and_valid_numeric_displays_are_not_currency(self):
        for source in ('$1$$9$$2$', '$0$-$9$', '$21$-$30$', '$$123$$', '$x=$\n{{field-1}}', '$$x=1\\\\[5pt]y=2$$'):
            self.check(source, source)

    def test_currency_and_percent_glyphs_are_content(self):
        self.check('Price $$50$; discount $12%=12/100$.', r'Price $\$50$; discount $12\%=12/100$.')
        self.check(r'Cost $\[math]25$ and $\[/math]100$.', r'Cost $\$25$ and $\$100$.')
        self.check('The cost is $$$\n{{value}}.', 'The cost is \\$\n{{value}}.')
        self.check('The painter paid approximately $\n{{value}}$\\,$ per day.', 'The painter paid approximately \\$\n{{value}}$\\,$ per day.')
        self.check(r'The profit is $270\cdot $1\,000=$270\,000.$',
                   r'The profit is $270\cdot \$1\,000=\$270\,000.$')

    def test_spacing_formulas_around_a_quantity_are_not_currency(self):
        self.check('Produce$\\,$\n{{value}}$\\,$ cakes for a profit of $$50$.',
                   'Produce$\\,$\n{{value}}$\\,$ cakes for a profit of $\\$50$.')

    def test_legacy_inline_markers_inside_math_do_not_nest_delimiters(self):
        self.check(r'$\frac{10}{[math]7[/math]}$', r'$\frac{10}{7}$')
        self.check('Use [math]x+1[/math].', 'Use $x+1$.')

    def test_empty_cells_and_rows_remain_empty(self):
        self.check('| $x$ | $$ |\n| $$? | $y$ |', '| $x$ |  |\n| ? | $y$ |')
        self.check('$1$$9$\\\\$2$', '$1$$9$<br>$2$')

    def test_unclosed_math_is_rejected_without_inventing_an_equation(self):
        for source in ('$x+1', r'\begin{align}x=1', r'\begin{align}x=1\end{matrix}'):
            self.assertEqual(normalize_math_boundaries(source), source)
            with self.assertRaises(ValueError):
                validate_math_boundaries(source)

    def test_validation_rejects_bare_environments_even_without_mathjax_errors(self):
        with self.assertRaisesRegex(ValueError, 'Unprotected'):
            validate_math_boundaries(r'\begin{align}x&=1\\y&=2\end{align}')
        with self.assertRaisesRegex(ValueError, 'percentage'):
            validate_math_boundaries('$12%=12/100$')
