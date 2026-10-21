"""Meaningful scope/annotation regressions, including escaped/nested groups."""
import unittest
from repair_structured import transform


class StructuredBraceRepairTests(unittest.TestCase):
    def check(self, before, after, under=0, over=0):
        actual, evidence = transform(before)
        self.assertEqual(after, actual)
        self.assertEqual(under, evidence["counts"].get("underbrace", 0))
        self.assertEqual(over, evidence["counts"].get("overbrace", 0))
        self.assertTrue(evidence["exact_source_reconstruction"])
        # Reapplying must not flatten, reparent, or duplicate any annotation.
        self.assertEqual((actual, {}), (transform(actual)[0], transform(actual)[1]["counts"]))

    def test_full_limit_scope(self):
        self.check(r"\sin(x){{{lim}_{h\to 0}\frac{\cos(h)-1}{h}}_{⏟}}_{0}+y",
                   r"\sin(x)\underbrace{{lim}_{h\to 0}\frac{\cos(h)-1}{h}}_{0}+y", under=1)

    def test_nested_base_and_label_subscripts(self):
        self.check(r"{{x_{i}+{y}^{2}}_{⏟}}_{{A}_{1}}",
                   r"\underbrace{x_{i}+{y}^{2}}_{{A}_{1}}", under=1)

    def test_escaped_set_delimiters(self):
        self.check(r"{{\{x,{y}_{i}\}}_{⏟}}_{S}",
                   r"\underbrace{\{x,{y}_{i}\}}_{S}", under=1)

    def test_overbrace_label(self):
        self.check(r"\overset{{M}_{11}}{\overset{⏞}{\begin{bmatrix}2&4\\0&-1\end{bmatrix}}}",
                   r"\overbrace{\begin{bmatrix}2&4\\0&-1\end{bmatrix}}^{{M}_{11}}", over=1)

    def test_nested_accent_scopes(self):
        self.check(r"{{\overset{A}{\overset{⏞}{x}}+{{y}_{⏟}}_{B}}_{⏟}}_{C}",
                   r"\underbrace{\overbrace{x}^{A}+\underbrace{y}_{B}}_{C}", under=2, over=1)

    def test_accent_inside_annotation(self):
        self.check(r"{{x}_{⏟}}_{\overset{a}{\overset{⏞}{b}}}",
                   r"\underbrace{x}_{\overbrace{b}^{a}}", under=1, over=1)

    def test_unlabeled_accent_preserves_neighbor(self):
        self.check(r"{13x+5x}_{⏟}-2y+1", r"\underbrace{13x+5x}-2y+1", under=1)

    def test_underset_wrapper(self):
        self.check(r"\underset{A}{{x+y}_{⏟}}", r"\underbrace{x+y}_{A}", under=1)

    def test_redundant_group_only_removed_for_annotation(self):
        self.check(r"\frac{{{x}_{⏟}}_{A}}{b}", r"\frac{\underbrace{x}_{A}}{b}", under=1)

    def test_surrounding_prose_and_flattened_unchanged(self):
        text = "Prose {literal: 2}. $x_(⏟)_(a)+y^(⏞)^(b)+x_{2}+\\underbrace{z}_{3}$"
        self.check(text, text)


if __name__ == "__main__":
    unittest.main()
