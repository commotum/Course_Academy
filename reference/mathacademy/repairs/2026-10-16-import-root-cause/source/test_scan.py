"""Falsifiable controls for exact source indicators, not broad math lint."""
import unittest
from bs4 import BeautifulSoup
import scan

MATH = '<math><mn>7</mn></math>'
ONE = '<mjx-container><mjx-assistive-mml>' + MATH + '</mjx-assistive-mml></mjx-container>'


class SourceScannerControls(unittest.TestCase):
    def test_pure_tex_title_is_not_mixed_loss(self):
        self.assertFalse(scan.title_info(r'A=\begin{bmatrix}1 & 2\\3 & 4\end{bmatrix}')[2])

    def test_single_fragment_punctuation_and_html_wrappers_are_safe(self):
        self.assertFalse(scan.title_info('<span> \n, ' + ONE + '</span>. ')[2])
        self.assertFalse(scan.title_info(ONE + '?!:')[2])

    def test_neutral_package_and_spacing_wrappers_are_safe(self):
        self.assertFalse(scan.title_info(r'\require{cancel}\quad\displaystyle{' + ONE + '}')[2])
        self.assertFalse(scan.title_info(r'\require{enclose}' + ONE + r'\,')[2])

    def test_known_owner_does_not_claim_following_footer(self):
        source = '<div id="step-1"><div>body</div></div><div>footer</div>'
        self.assertEqual(scan.owner_end(source, source.index('id=')), source.index('<div>footer'))

    def test_duplicates_inside_one_container_are_not_two_operands(self):
        content = '<mjx-container>' + MATH + '<mjx-assistive-mml>' + MATH + '</mjx-assistive-mml></mjx-container>'
        fragments, _, lost, _ = scan.title_info(content)
        self.assertEqual(len(fragments), 1)
        self.assertFalse(lost)

    def test_missing_assignment_and_second_operand_are_detected(self):
        self.assertTrue(scan.title_info('A=' + ONE)[2])
        self.assertTrue(scan.title_info(ONE + ' ' + ONE)[2])
        source = BeautifulSoup('<span class="mjpage"><svg><title>A=' + ONE + ', B=' + ONE + '</title></svg></span>', 'html.parser')
        self.assertEqual(scan.legacy.extract_math_from_node(source.span)[0], '7')

    def test_structural_predicates_keep_ordinary_fraction_and_matrix_as_controls(self):
        good = BeautifulSoup('<math><mfrac><mn>1</mn><mn>2</mn></mfrac></math>', 'html.parser').math
        old = scan.legacy.mathml_to_text(good)
        self.assertEqual(scan.mathml_mechanisms(good, old, scan.rendered_math(old)), [])
        bad = BeautifulSoup('<math><mfrac linethickness="0"><mn>1</mn><mn>2</mn></mfrac></math>', 'html.parser').math
        old = scan.legacy.mathml_to_text(bad)
        self.assertIn('mathml-zero-rule-fraction-made-visible', [v['code'] for v in scan.mathml_mechanisms(bad, old, scan.rendered_math(old))])

    def test_tex_comment_scope_is_lost_by_historical_placeholder_parser(self):
        value = 'a=1\n% source-only comment\nb=2'
        extracted = scan.md.extract_math_placeholder('[MATH: ' + value + ']')
        self.assertEqual(extracted, 'a=1 % source-only comment b=2')


if __name__ == '__main__':
    unittest.main()
