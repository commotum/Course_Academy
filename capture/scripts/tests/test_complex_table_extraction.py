"""Complex source tables retain cell ownership through capture and UI rendering."""
import base64
import hashlib
import json
from pathlib import Path
import re
import unittest

from scripts.browser.adapter import EXTRACT
from scripts.browser.assets import replace_markers
from scripts.database.text import markdown

REPO = Path(__file__).resolve().parents[3]
SHAPE = """root => [...root.querySelectorAll('table')].map(table => ({
  rows: [...table.querySelectorAll('tr')].filter(row => row.closest('table') === table).map(row =>
    [...row.children].filter(cell => ['td','th'].includes(cell.localName)).map(cell =>
      [cell.localName, cell.getAttribute('rowspan'), cell.getAttribute('colspan')]))
}))"""


class ComplexTableExtractionTests(unittest.TestCase):
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

    def extract(self, html, selector='#q'):
        self.page.set_content(html)
        scope = self.page.locator(selector)
        original = scope.inner_html()
        record = scope.evaluate(EXTRACT)
        self.assertEqual(scope.inner_html(), original)
        return record

    def ui_render(self, source, fields=None):
        # Execute the repository's actual renderer and vendored sanitizer;
        # imports are data URLs and every browser network request is blocked.
        self.page.set_content('<div id="rendered"></div>')
        def module_url(path, substitutions=()):
            code = path.read_text()
            for before, after in substitutions:
                code = code.replace(before, after)
            return 'data:text/javascript;base64,' + base64.b64encode(code.encode()).decode()
        self.page.evaluate('async url => {window.marked=(await import(url)).marked;}',
                           module_url(REPO / 'ui/vendor/marked/marked.esm.js'))
        self.page.evaluate('async url => {window.inlinePrompt=(await import(url)).inlinePrompt;}',
                           module_url(REPO / 'ui/question-fields.js'))
        self.page.evaluate('async url => {window.romanLists=(await import(url)).romanLists;}',
                           module_url(REPO / 'ui/prose-lists.js',
                             [("import { marked } from './vendor/marked/marked.esm.js';", 'const marked=window.marked;')]))
        self.page.add_script_tag(content=(REPO / 'ui/vendor/dompurify/purify.min.js').read_text())
        ui = (REPO / 'ui/activity.js').read_text()
        functions = [re.search(r'function ' + name + r'\([^\n]*\) \{[\s\S]*?\n\}', ui).group()
                     for name in ('assetURL', 'fieldLabel', 'markdown')]
        self.page.add_script_tag(content="""function el(tag, cls='', text) {
          const node=document.createElement(tag);node.className=cls;if(text!==undefined)node.textContent=text;return node;
        }
        function escapeHTML(value) {return String(value).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));}
        if(!crypto.randomUUID)crypto.randomUUID=()=> 'offline-test-token';
        """ + '\n'.join(functions) + '\nwindow.renderSource=markdown;')
        self.page.evaluate('''({source,fields}) => {
          const host=document.querySelector('#rendered');host.append(window.renderSource(source,fields));
          window.initialImageSources=[...host.querySelectorAll('img')].map(image=>image.getAttribute('src'));
        }''',
                           {'source': source, 'fields': fields or []})
        return self.page.locator('#rendered')

    def test_actual_span_and_nested_sources_keep_exact_table_ownership_downstream(self):
        rows = json.loads((Path(__file__).parent / 'fixtures/complex-source-tables.json').read_text())
        for row in rows:
            with self.subTest(question=row['question_id'], part=row['part']):
                self.assertEqual(hashlib.sha256(row['html'].encode()).hexdigest(), row['html_sha256'])
                selector = ('#questionExplanation-' + row['question_id'][2:] if row['part'] == 'history'
                            else '#step-' + row['question_id'].replace('-', ''))
                record = self.extract(row['html'], selector)
                root = self.page.locator(selector)
                source = root.locator('.questionWidget-text').first if row['part'] == 'before' else root
                original_shape = source.evaluate(SHAPE)
                value = record['worked_solution'] if row['part'] == 'history' else record['problem']
                self.assertIn('<table', value)
                self.assertEqual(record['errors'], [])
                normalized = markdown(value)
                self.assertEqual(markdown(normalized), normalized)
                if row['question_id'] == 'q-139689' and row['part'] == 'history':
                    self.assertEqual(normalized.split('<table', 1)[0].strip(), value.split('<table', 1)[0].strip())
                    self.assertEqual(normalized.rsplit('</table>', 1)[-1].strip(), value.rsplit('</table>', 1)[-1].strip())
                    original_rendered = self.ui_render(value)
                    original_lists = original_rendered.locator('ul > li').all_text_contents()
                    self.assertTrue(original_lists)
                rendered = self.ui_render(normalized)
                if row['question_id'] == 'q-139689' and row['part'] == 'history':
                    self.assertEqual(rendered.locator('ul > li').all_text_contents(), original_lists)
                self.assertEqual(rendered.evaluate(SHAPE), original_shape)
                self.assertNotIn('mjx-container', normalized)
                self.assertNotIn('style=', normalized)
                if row['question_id'] == 'q-139689':
                    self.assertIn('colspan="3"', normalized)
                    self.assertIn('rowspan="3"', normalized)
                    self.assertEqual(rendered.locator('td[rowspan="3"]').text_content(), 'From:')
                    self.assertEqual(rendered.locator('td[colspan="3"]').text_content(), 'To:')
                else:
                    self.assertEqual(len(original_shape), 3)
                    self.assertEqual(len(original_shape[0]['rows']), 1)
                for asset in row['assets']:
                    self.assertEqual(hashlib.sha256(Path(asset['path']).read_bytes()).hexdigest(), asset['sha256'])

    def test_nested_field_math_assets_and_plain_html_text_survive_exactly(self):
        record = self.extract('''<div id="q"><div class="questionText"><table><tr><td>
          <table><tr><td colspan="2"><b>Header &amp; &lt;literal&gt;</b></td></tr><tr>
          <td><math><mi>x</mi><mo>&lt;</mo><mn>2</mn></math></td><td><input id="answer"></td></tr>
          <tr><td><img src="/graphics/example.png"></td><td><i>Body</i><br>Next</td></tr></table>
          </td></tr></table></div></div>''')
        self.assertEqual(record['errors'], [])
        self.assertIn('$x<2$', record['problem'])
        self.assertIn('{{field-1}}', record['problem'])
        self.assertIn('<b>Header &amp; &lt;literal&gt;</b>', record['problem'])
        bound = replace_markers(record, {'@asset-0@': 'assets/example.png'})
        normalized = markdown(bound['problem'])
        self.assertIn('$x<2$', normalized)
        self.assertIn('{{field-1}}', normalized)
        self.assertIn('<img', normalized)
        rendered = self.ui_render(normalized, [{'key': 'field-1', 'type': 'blank'}])
        self.assertIn('$x<2$', rendered.text_content())
        self.assertIn('Header & <literal>', rendered.text_content())
        self.assertEqual(rendered.locator('[data-field-key="field-1"]').count(), 1)
        self.assertEqual(rendered.locator('td[colspan="2"] b').text_content(), 'Header & <literal>')
        self.assertEqual(self.page.evaluate('window.initialImageSources'), ['/api/asset?path=assets%2Fexample.png'])

    def test_complete_tex_alignment_escaped_dollars_and_placeholders_restore_exact_bytes(self):
        formulas = [r'$x<2$', r'$\begin{aligned}x&=1\\y&={{field-1}}\end{aligned}$', r'$\text{cost }\$5$']
        source = '<table><tr><td colspan="2">' + ' '.join(formulas) + r' prose \$7 &amp; &lt;plain&gt;</td></tr></table>'
        normalized = markdown(source)
        for formula in formulas:
            self.assertIn(formula, normalized)
        self.assertEqual(markdown(normalized), normalized)
        rendered = self.ui_render(normalized)
        for formula in formulas:
            self.assertIn(formula, rendered.text_content())
        self.assertIn('& <plain>', rendered.text_content())

    def test_mixed_markdown_around_complex_table_preserves_paragraph_and_list_boundaries(self):
        prefix = 'Original introduction.\n\n- First $x<2$.\n- Next {{field-1}}.\n\n'
        table = '<table><tr><td colspan="2">Inside\n HTML whitespace</td></tr></table>'
        suffix = '\n\nOriginal conclusion.\n\n- Final $y&=3$.\n- Diagram ![](assets/example.png).'
        normalized = markdown(prefix + table + suffix)
        self.assertEqual(normalized.split('<table', 1)[0].strip(), prefix.strip())
        self.assertEqual(normalized.rsplit('</table>', 1)[-1].strip(), suffix.strip())
        self.assertEqual(markdown(normalized), normalized)
        rendered = self.ui_render(normalized, [{'key': 'field-1', 'type': 'blank'}])
        self.assertEqual(rendered.locator('ul > li').count(), 4)
        self.assertEqual(rendered.locator('[data-field-key="field-1"]').count(), 1)
        self.assertIn('$x<2$', rendered.text_content())
        self.assertIn('$y&=3$', rendered.text_content())
        self.assertEqual(self.page.evaluate('window.initialImageSources'), ['/api/asset?path=assets%2Fexample.png'])

    def test_regular_tables_stay_markdown_and_unsupported_span_layouts_are_explicit(self):
        record = self.extract('<div id="q"><div class="questionText"><table><tr><th>A</th><th>B</th></tr>'
                              '<tr><td>1</td><td>2</td></tr></table></div></div>')
        self.assertEqual(record['problem'], '| A | B |\n| --- | --- |\n| 1 | 2 |')
        record = self.extract('<div id="q"><div class="questionText"><table><tr><td colspan="bad" style="grid-column:span 2">'
                              'Original</td></tr></table></div></div>')
        self.assertEqual(set(record['errors']), {'Unsupported table layout style', 'Unsupported table span: colspan=bad'})
        self.assertIn('Original', record['problem'])
        self.assertTrue(all(parts == ['problem'] for parts in record['extraction_error_parts'].values()))
        record = self.extract('<style>.custom-layout{display:grid}</style><div id="q"><div class="questionText">'
                              '<table class="custom-layout"><tr><td colspan="2">Source</td></tr></table></div></div>')
        self.assertIn('Unsupported table layout style', record['errors'])

    def test_source_feedback_and_learner_answers_do_not_enter_complex_table_prompt(self):
        record = self.extract('<div id="q"><div class="questionText"><table><tr><td colspan="2">Source'
                              '<div class="studentAnswer">Learner attempt</div><div class="questionWidget-feedback">Feedback</div>'
                              '</td></tr></table></div></div>')
        self.assertNotIn('Learner attempt', record['problem'])
        self.assertNotIn('Feedback', record['problem'])


if __name__ == '__main__':
    unittest.main()
