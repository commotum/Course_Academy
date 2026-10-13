"""Preserve authored list references while reading saved DOM offline."""
import hashlib
import json
from pathlib import Path
import unittest

from scripts.browser.adapter import EXTRACT


class OrderedListExtractionTests(unittest.TestCase):
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
        scope = self.page.locator('#q, .questionWidget').first
        before = scope.inner_html()
        record = scope.evaluate(EXTRACT)
        self.assertEqual(scope.inner_html(), before)
        return record

    def test_actual_statement_fragments_preserve_roman_references_and_math(self):
        fixture = json.loads((Path(__file__).parent / 'fixtures/ordered-statement-lists.json').read_text())
        self.assertIn('list-style-type: upper-roman;', fixture['public_css'][0]['rule'])
        expected = {'q-38580': ('I. The degree of $F(x)$ is odd.', 'II. The degree of $F(x)$ is even.',
                               'III. The coefficient of the leading term is positive.'),
                    'q-103812': ('I. The range of the function is', 'II. $y=-1$ is the maximum value',
                                'III. $x=15\\pi $ is in the domain.'),
                    'q-12008': ('I. $T(kv)=kT(v)$', 'II. $T({v}_{1}+{v}_{2})=T({v}_{1})+T({v}_{2})$',
                               'III.')}
        for row in fixture['questions']:
            with self.subTest(question=row['question_id']):
                self.assertEqual(hashlib.sha256(row['html'].encode()).hexdigest(), row['html_sha256'])
                record = self.extract(row['html'])
                for text in expected[row['question_id']]:
                    self.assertIn(text, record['problem'])
                self.assertNotIn('- The degree', record['problem'])
                self.assertTrue(any('I' in choice['value'] for choice in record['fields'][0]['choices']))
                self.assertEqual([choice['value'] for choice in record['fields'][0]['choices']],
                    self.page.locator('.questionWidget-choiceText').all_text_contents())
                self.assertTrue(record['answer_fields_complete'])
                self.assertEqual(record['errors'], [])
                # Loading the exact scoped public rule yields the same labels.
                self.page.add_style_tag(content=fixture['public_css'][0]['rule'])
                styled = self.page.locator('.questionWidget').evaluate(EXTRACT)
                self.assertEqual(styled['problem'], record['problem'])

    def test_declared_types_start_values_and_item_resets(self):
        for kind, start, expected in [('1', 7, ['7\\.', '8\\.', '12\\.', '13\\.']),
                                       ('I', 3, ['III.', 'IV.', 'XII.', 'XIII.']),
                                       ('i', 3, ['iii.', 'iv.', 'xii.', 'xiii.']),
                                       ('A', 25, ['Y.', 'Z.', 'L.', 'M.']),
                                       ('a', 25, ['y.', 'z.', 'l.', 'm.'])]:
            with self.subTest(kind=kind):
                record = self.extract(f'<div id="q"><div class="questionText"><ol type="{kind}" start="{start}">'
                    '<li>First <math><mn>1</mn><mo>+</mo><mn>2</mn></math></li><li>Second</li>'
                    '<li value="12">Reset</li><li>Next</li></ol></div></div>')
                lines = record['problem'].split('\n\n')
                self.assertEqual(lines, [expected[0] + ' First $1+2$', expected[1] + ' Second',
                                         expected[2] + ' Reset', expected[3] + ' Next'])

    def test_nested_lists_use_independent_counters_and_keep_unordered_bullets(self):
        record = self.extract('<div id="q"><div class="questionText"><ol type="I" start="2">'
            '<li>Outer<ol type="a" start="26"><li>Inner</li><li value="28">Reset</li></ol></li>'
            '<li>Second<ul><li>Bullet</li></ul></li></ol></div></div>')
        self.assertEqual(record['problem'], 'II. Outer\n\n  z. Inner\n\n  ab. Reset\n\nIII. Second\n\n  - Bullet')
        unordered = self.extract('<div id="q"><div class="questionText"><ul><li>One</li><li>Two</li></ul></div></div>')
        self.assertEqual(unordered['problem'], '- One\n- Two')

    def test_reversed_list_and_nonpositive_roman_fallback(self):
        record = self.extract('<div id="q"><div class="questionText"><ol reversed type="I">'
            '<li>Third</li><li value="0">Zero</li><li>Negative</li></ol></div></div>')
        self.assertEqual(record['problem'], 'III. Third\n\n0\\. Zero\n\n-1\\. Negative')

    def test_observed_supported_css_is_respected_and_unknown_style_has_explicit_gap(self):
        record = self.extract('<div id="q"><div class="questionText"><ol style="list-style-type:lower-alpha" start="27">'
                              '<li>Alpha</li></ol></div></div>')
        self.assertEqual(record['problem'], 'aa. Alpha')
        record = self.extract('<div id="q"><div class="questionText"><ol class="questionStatements" style="list-style-type:decimal">'
                              '<li>Explicit decimal</li></ol></div></div>')
        self.assertEqual(record['problem'], '1\\. Explicit decimal')
        record = self.extract('<div id="q"><div class="questionText"><ol style="list-style-type:lower-greek">'
                              '<li>Original wording</li></ol></div></div>')
        self.assertEqual(record['problem'], 'Original wording')
        self.assertEqual(record['errors'], ['Unsupported ordered list style: lower-greek'])
        self.assertEqual(record['extraction_error_parts'], {'Unsupported ordered list style: lower-greek': ['problem']})


if __name__ == '__main__':
    unittest.main()
