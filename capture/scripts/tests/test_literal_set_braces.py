"""Literal source braces stay visible and cannot become control placeholders."""
import hashlib
import json
from pathlib import Path
import unittest

from scripts.activity.evidence import capture_gaps
from scripts.browser.adapter import EXTRACT
from scripts.database.evidence import authoritative_question, UnsupportedContent

REPO = Path(__file__).resolve().parents[3]


class LiteralSetBraces(unittest.TestCase):
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

    def extract(self, html):
        self.page.set_content(html)
        node = self.page.locator('#question-80447, #step-q1').first
        original = node.inner_html()
        result = node.evaluate(EXTRACT)
        self.assertEqual(original, node.inner_html())
        self.assertEqual(result['errors'], [])
        return result

    def prompt(self, math):
        return '<div id="step-q1"><div class="questionWidget-text">' + math + '</div></div>'

    def actual(self):
        fixture = json.loads((Path(__file__).parent / 'fixtures/literal-set-braces.json').read_text())
        self.assertEqual(hashlib.sha256(fixture['html'].encode()).hexdigest(), fixture['html_sha256'])
        return self.extract(fixture['html'])

    def question(self, problem):
        quote = 'Since $Y$ has $6$ elements, the cardinality is $|Y|=6.$'
        return {'math_academy_id': 'q-80447', 'problem': problem, 'worked_solution': quote,
            'answer_fields_complete': True, 'answer_fields': [{'key': 'selection', 'type': 'radio',
                'choices_complete': True, 'choices': [{'type': 'math', 'value': str(n)} for n in (2, 6, 8, 4)] + [{'type': 'text', 'value': 'Undefined'}],
                'correct_value': '6', 'correct_type': 'math', 'evidence': {'kind': 'worked_solution',
                    'value': '6', 'solution_quote': quote, 'source_file': '/authored-source.html', 'matches_worked_solution': True}}]}

    def test_actual_nested_sets_preserve_all_ten_literal_brace_glyphs(self):
        record = self.actual()
        self.assertEqual(record['problem'], r'If $Y=\{1,2,\{\{2\}\},3,2,4,\{\{∅\}\},4\}$, then $|Y|=$')
        self.assertEqual(record['problem'].count(r'\{') + record['problem'].count(r'\}'), 10)
        self.assertEqual(capture_gaps({'questions': [self.question(record['problem'])]}), [])

    def test_nested_literal_sets_are_not_control_keys_even_in_old_unescaped_text(self):
        q = self.question('If $Y={1,2,{{2}},3,2,4,{{∅}},4}$, then $|Y|=$')
        self.assertEqual(capture_gaps({'questions': [q]}), [])
        self.assertEqual(authoritative_question(q)['answer_fields'][0]['correct_value'], '6')

    def test_actual_missing_field_token_still_fails_capture_and_database(self):
        q = self.question('If $Y={1,2,{{2}},{{∅}}}$, then |Y|={{field-2}}')
        self.assertIn('answer_field_structure', capture_gaps({'questions': [q]})[0]['missing'])
        with self.assertRaisesRegex(UnsupportedContent, 'missing captured controls: field-2'):
            authoritative_question(q)

    def test_mfenced_literal_braces_and_scripted_closing_fence(self):
        record = self.extract(self.prompt('<math><mfenced open="{" close="}"><mi>x</mi><mn>2</mn></mfenced></math>'))
        self.assertEqual(record['problem'], r'$\{x,2\}$')
        record = self.extract(self.prompt('<math><mo>{</mo><mi>x</mi><msup><mo>}</mo><mn>2</mn></msup></math>'))
        self.assertEqual(record['problem'], r'$\{x\}^{2}$')

    def test_programmatic_fraction_text_and_power_groups_are_unchanged(self):
        record = self.extract(self.prompt('<math><mfrac><mi>x</mi><mn>2</mn></mfrac><mo>+</mo><mtext>word</mtext><mo>+</mo><msup><mi>y</mi><mn>3</mn></msup></math>'))
        self.assertEqual(record['problem'], r'$\frac{x}{2}+\text{word}+{y}^{3}$')

    def test_observed_custom_select_marker_binds_before_brace_escaping(self):
        html = self.prompt('''<mjx-container><div class="selectList" id="selectList-1-1"><div class="selectListFrame" id="selectListFrame-1-1">Select</div><div class="selectListOptions"><div class="selectListOption" id="option-a">yes</div><div class="selectListOption" id="option-b">no</div></div></div><mjx-assistive-mml><math><mrow><mo>{</mo><msub><mi>x</mi><mtext>(S1)</mtext></msub><mo>}</mo></mrow></math></mjx-assistive-mml></mjx-container>''')
        record = self.extract(html)
        self.assertEqual(record['problem'], '${{field-1}}$')
        self.assertEqual(record['fields'][0]['key'], 'field-1')
        self.assertEqual([c['value'] for c in record['fields'][0]['choices']], ['yes', 'no'])

    def test_vendored_ui_mathjax_renders_all_original_brace_glyphs(self):
        tex = self.actual()['problem'].split('$')[1]
        self.page.evaluate('window.MathJax={startup:{typeset:false}}')
        self.page.add_script_tag(content=(REPO / 'ui/vendor/mathjax/tex-svg.js').read_text())
        result = self.page.evaluate('''async tex => {await MathJax.startup.promise;const node=await MathJax.tex2svgPromise(tex);return {opening:node.querySelectorAll('use[data-c="7B"]').length,closing:node.querySelectorAll('use[data-c="7D"]').length,errors:node.querySelectorAll('[data-mml-node="merror"]').length};}''', tex)
        self.assertEqual(result, {'opening': 5, 'closing': 5, 'errors': 0})
