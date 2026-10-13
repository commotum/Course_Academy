"""Zero-rule MathML stacks retain their source notation in prompts and choices."""
import hashlib
import json
from pathlib import Path
import unittest

from scripts.browser.adapter import EXTRACT

REPO = Path(__file__).resolve().parents[3]


class ZeroBarFractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.playwright = sync_playwright().start()
        try:
            cls.browser = cls.playwright.chromium.launch(headless=True)
        except Exception:
            cls.playwright.stop()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.context.route('**/*', lambda route: route.abort())
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def extract(self, html, selector='#step-q1'):
        self.page.set_content(html)
        node = self.page.locator(selector)
        before = node.inner_html()
        result = node.evaluate(EXTRACT)
        self.assertEqual(node.inner_html(), before)
        return result

    def formula(self, thickness=None, *, fenced=False):
        attr = '' if thickness is None else ' linethickness="' + thickness + '"'
        fraction = '<mfrac' + attr + '><mn>7</mn><mn>2</mn></mfrac>'
        if fenced:
            fraction = '<mo>(</mo>' + fraction + '<mo>)</mo>'
        return '<math><mrow>' + fraction + '</mrow></math>'

    def prompt(self, formula):
        return '<div id="step-q1"><div class="questionWidget-text">' + formula + '</div></div>'

    def test_actual_four_binomial_prompts_preserve_visible_zero_rule_stacks(self):
        rows = json.loads((Path(__file__).parent / 'fixtures/zero-bar-fractions.json').read_text())
        for row in rows:
            with self.subTest(question=row['question_id']):
                self.assertEqual(hashlib.sha256(row['html'].encode()).hexdigest(), row['html_sha256'])
                result = self.extract(row['html'], '#' + row['dom_id'])
                visible = self.page.locator('#' + row['dom_id']).evaluate('''root =>
                    [...root.querySelectorAll('math mfrac[linethickness="0"]')]
                      .filter(node => !node.closest('mphantom')).length''')
                self.assertGreater(visible, 0)
                source_values = [result['problem']] + [str(choice['value'])
                    for field in result['fields'] for choice in field['choices']]
                self.assertEqual(sum(value.count('\\genfrac{}{}{0pt}{}') for value in source_values), visible)
                self.assertEqual(result['errors'], [])
                self.assertNotIn('\\binom', result['problem'])

    def test_valid_zero_lengths_preserve_unfenced_stack_and_original_parentheses(self):
        for thickness in ('0', ' 0 ', '0.0pt', '.0px', '+0em', '00.000mm', '0%', '0EX', '0in', '0cm', '0pc'):
            for fenced in (False, True):
                with self.subTest(thickness=thickness, fenced=fenced):
                    result = self.extract(self.prompt(self.formula(thickness, fenced=fenced)))
                    expected = '\\genfrac{}{}{0pt}{}{7}{2}'
                    self.assertEqual(result['problem'], '$' + ('(' + expected + ')' if fenced else expected) + '$')
                    self.assertEqual(result['errors'], [])

    def test_ordinary_positive_and_keyword_rule_fractions_remain_division(self):
        for thickness in (None, '1', '0.1pt', '.01px', 'thin', 'medium', 'thick'):
            with self.subTest(thickness=thickness):
                result = self.extract(self.prompt(self.formula(thickness)))
                self.assertEqual(result['problem'], '$\\frac{7}{2}$')
                self.assertEqual(result['errors'], [])

    def test_unsupported_or_negative_rule_attributes_are_explicit_gaps(self):
        for thickness in ('0banana', '-1pt', '-0px', 'calc(0px)', '0 pt'):
            with self.subTest(thickness=thickness):
                result = self.extract(self.prompt(self.formula(thickness)))
                self.assertIn('Unsupported MathML fraction line thickness: ' + thickness, result['errors'])
                self.assertEqual(result['problem'], '$\\frac{7}{2}$')
                self.assertNotIn('\\genfrac', result['problem'])

    def test_zero_rule_typed_select_choice_keeps_exact_math_type_and_placeholder(self):
        formula = self.formula('0', fenced=True)
        ordinary = self.formula()
        html = '''<div id="step-q1"><div class="questionWidget-text">Choose <div class="selectList" id="selectList-1-0"><div class="selectListFrame" id="frame-1">Select</div>
          <div class="selectListOptions"><div class="selectListOption" id="choice-a">''' + formula + '''</div>
          <div class="selectListOption" id="choice-b">''' + ordinary + '''</div></div></div></div></div>'''
        result = self.extract(html)
        self.assertEqual(result['problem'], 'Choose {{field-1}}')
        self.assertEqual([(choice['type'], choice['value']) for choice in result['fields'][0]['choices']],
                         [('math', '(\\genfrac{}{}{0pt}{}{7}{2})'), ('math', '\\frac{7}{2}')])
        self.assertEqual(result['errors'], [])

    def test_vendored_ui_mathjax_renders_stack_with_no_division_rule(self):
        self.page.set_content('<div id="rendered"></div>')
        self.page.evaluate('window.MathJax={startup:{typeset:false}}')
        self.page.add_script_tag(content=(REPO / 'ui/vendor/mathjax/tex-svg.js').read_text())
        result = self.page.evaluate('''async () => {
          await MathJax.startup.promise;
          const stack=await MathJax.tex2svgPromise('(\\\\genfrac{}{}{0pt}{}{7}{2})');
          const fraction=await MathJax.tex2svgPromise('\\\\frac{7}{2}');
          return {stackRules:stack.querySelectorAll('[data-mml-node="mfrac"] rect').length,
                  fractionRules:fraction.querySelectorAll('[data-mml-node="mfrac"] rect').length,
                  errors:stack.querySelectorAll('[data-mml-node="merror"]').length};
        }''')
        self.assertEqual(result, {'stackRules': 0, 'fractionRules': 1, 'errors': 0})
