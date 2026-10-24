"""Saved-source matrix extraction, storage, and MathJax rendering regressions."""
import functools
import http.server
import json
import html
import threading
import unittest
import uuid
from pathlib import Path
from playwright.sync_api import sync_playwright
from core import build_content_transaction
from edn import dumps, loads

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).with_name('fixtures') / 'matrices'
TABLE = '<mtable><mtr><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mn>3</mn></mtd><mtd><mn>4</mn></mtd></mtr></mtable>'

class MatrixCaptureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = Path(__file__).with_name('dom.js').read_text()
        cls.runtime = sync_playwright().start()
        cls.browser = cls.runtime.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
        cls.context.route('**/*', lambda route: route.abort())
        cls.page = cls.context.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.runtime.stop()

    def extract(self, math):
        self.page.set_content('<div id="fixture"><div class="questionWidget-text">' + math + '</div></div>')
        return self.page.locator('#fixture').evaluate(self.source)

    def test_saved_four_by_three_matrix_retains_every_cell(self):
        item = self.extract((FIXTURES / 'introduction-mathml.html').read_text())
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['problem'], r'$\begin{bmatrix}2 & -1 & 0 \\ -5 & 0 & -2 \\ -1 & 8 & 1 \\ 0 & 3 & -7\end{bmatrix}$')

    def test_percent_identifier_is_literal_content_in_mathml(self):
        # Math Academy emits the percent as mi, not only mo or mtext.
        item = self.extract('<div class="questionText">A 30% discount is '
                            '<math><mn>30</mn><mi mathvariant="normal">%</mi></math>.'
                            '</div>')
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['problem'], r'A 30% discount is $30\%$.')

    def test_legacy_example_recovers_systems_without_images(self):
        self.page.set_content((FIXTURES / 'example-4683.html').read_text())
        item = self.page.locator('#step-17170').evaluate(self.source)
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['assets'], [])
        self.assertIn(r'\left\{\begin{aligned}x-2y &=1 \\ 2y &=-1\end{aligned}\right.', item['problem'])
        self.assertIn(r'\left\{\begin{aligned}x-2y &=1 \\ 0x+2y &=-1\end{aligned}\right.', item['worked_solution'])
        self.assertIn('1 & -2  ' + '\\\\' + '\n', item['worked_solution'])
        self.assertNotIn(r'\matrix', item['worked_solution'])

    def test_legacy_matrix_rows_vectors_and_nested_groups(self):
        for source, expected in [
            ('\\matrix{1 & -2 \\\n0 & 2}', '\\begin{matrix}1 & -2  \\\\\n0 & 2\\end{matrix}'),
            ('\\matrix{5 & -1 & 0 \\\n}', r'\begin{matrix}5 & -1 & 0  \end{matrix}'),
            ('\\matrix{5 \\ \n-1 \\ \n0 \\ \n}', '\\begin{matrix}5  \\\\\n-1  \\\\\n0  \\end{matrix}'),
            (r'\matrix{\frac{1}{2} & {\color{red}2}\cr 3 & 4}', r'\begin{matrix}\frac{1}{2} & {\color{red}2} \\  3 & 4\end{matrix}'),
            (r'\matrix{1 & 2} \matrix{3 & 4}', r'\begin{matrix}1 & 2\end{matrix} \begin{matrix}3 & 4\end{matrix}'),
        ]:
            with self.subTest(source=source):
                item = self.extract('<span class="mjpage"><svg><title>' + html.escape(source) + '</title></svg></span>')
                self.assertEqual(item['errors'], [])
                self.assertEqual(item['assets'], [])
                self.assertEqual(item['problem'], '$' + expected + '$')

    def test_legacy_augmented_example_recovers_divider_without_image(self):
        self.page.set_content((FIXTURES / 'example-4684.html').read_text())
        item = self.page.locator('#step-17171').evaluate(self.source)
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['assets'], [])
        self.assertIn(r'\left\{\begin{aligned}', item['problem'])
        self.assertIn(r'\left[\begin{array}{ccc|c}1 & 1 & -3 & 5 \\ -7 & -1 & 1 & 0 \\ 2 & 1 & -2 & -2\end{array}\right]', item['worked_solution'])

    def test_unknown_mixed_title_still_preserves_whole_formula(self):
        item = self.extract('<span class="mjpage"><svg><title>\\fbox{<mjx-container><math><mn>1</mn></math></mjx-container>}</title></svg></span>')
        self.assertEqual(len(item['assets']), 1)
        self.assertNotIn('$1$', item['problem'])
        item = self.extract('<span class="mjpage"><svg><title>\\eqalign{<mjx-container><math><mn>1</mn></math><math><mn>2</mn></math></mjx-container>}</title></svg></span>')
        self.assertEqual(len(item['assets']), 1)

    def test_remaining_lesson_examples_recover_systems_and_augmented_matrices(self):
        for qid, dom_id in [('4685', 'step-17173'), ('4686', 'step-17174')]:
            with self.subTest(qid=qid):
                self.page.set_content((FIXTURES / ('example-' + qid + '.html')).read_text())
                item = self.page.locator('#' + dom_id).evaluate(self.source)
                self.assertEqual(item['errors'], [])
                self.assertEqual(item['assets'], [])
                self.assertIn(r'\left\{\begin{aligned}', item['worked_solution'])
                if qid == '4685':
                    self.assertIn(r'\begin{array}{cc|c}5 & -4 & -12 \\ 3 & 1 & 1', item['problem'])
                else:
                    self.assertIn(r'\begin{array}{cccc|c}-1 & 0 & \frac{1}{2} & 0 & 0 \\ -1 & 3 & -4 & 0 & -5 \\ 0 & 0 & 0 & 1 & 1', item['worked_solution'])

    def test_complete_saved_widgets_retain_highlight_and_choices(self):
        for qid, value in [('question-13498', '7'), ('question-13503', '9')]:
            with self.subTest(qid=qid):
                self.page.set_content((FIXTURES / (qid + '.html')).read_text())
                item = self.page.locator('#' + qid).evaluate(self.source)
                self.assertEqual(item['errors'], [])
                self.assertIn(r'\begin{bmatrix}', item['problem'])
                self.assertEqual(item['problem'].count(r'\bbox['), 1)
                self.assertIn(r'\bbox[lightgray, 2pt]{' + value + '}', item['problem'])
                self.assertEqual(len(item['fields'][0]['choices']), 5)
                self.assertTrue(item['fields'][0]['choices_complete'])

    def test_colored_row_and_column_indices_remain_scoped(self):
        item = self.extract((FIXTURES / 'colored-indices-mathml.html').read_text())
        self.assertEqual(item['errors'], [])
        self.assertIn(r'{\color{blue}1}', item['problem'])
        self.assertIn(r'{\color{red}3}', item['problem'])
        self.assertIn(r'\begin{bmatrix}', item['problem'])

    def test_vector_hat_is_a_tex_accent(self):
        item = self.extract('<math><mover><mi>x</mi><mo>^</mo></mover></math>')
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['problem'], r'$\widehat{x}$')

    def test_system_without_empty_closing_delimiter_aligns_equals(self):
        table = '<mtable columnalign="left"><mtr><mtd><mi>x</mi><mo>+</mo><mn>3</mn><mi>y</mi><mo>=</mo><mn>7</mn></mtd></mtr><mtr><mtd><mn>2</mn><mi>x</mi><mo>+</mo><mn>0</mn><mi>y</mi><mo>=</mo><mn>4</mn></mtd></mtr></mtable>'
        for closing in ['', '<mo></mo>']:
            with self.subTest(closing=closing):
                item = self.extract('<math><mrow><mo>{</mo>' + table + closing + '</mrow></math>')
                self.assertEqual(item['errors'], [])
                self.assertEqual(item['problem'], r'$\left\{\begin{aligned}x+3y &=7 \\ 2x+0y &=4\end{aligned}\right.$')
        # The old nested-table capture emitted an unmatched literal "{" here.
        item = self.extract('<math><mtable><mtr><mtd><mo>{</mo>' + table + '</mtd></mtr></mtable></math>')
        # An mtd can itself be the system wrapper, without an enclosing mrow.
        self.assertEqual(item['errors'], [])
        self.assertIn(r'\left\{\begin{aligned}', item['problem'])

    def test_piecewise_values_keep_their_conditions(self):
        table = '<mtable columnalign="left left"><mtr><mtd><mi>x</mi></mtd><mtd><mtext>if x=1</mtext></mtd></mtr><mtr><mtd><mn>0</mn></mtd><mtd><mtext>otherwise</mtext></mtd></mtr></mtable>'
        item = self.extract('<math><mo>{</mo>' + table + '</math>')
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['problem'], r'$\begin{cases}x & \text{if x=1} \\ 0 & \text{otherwise}\end{cases}$')

    def test_coefficient_and_augmented_matrices_keep_separate_column_rules(self):
        coefficient = '<math><mo>[</mo>' + TABLE + '<mo>]</mo></math>'
        augmented = TABLE.replace('<mtable>', '<mtable columnlines="none solid">').replace('</mtd></mtr>', '</mtd><mtd><mn>7</mn></mtd></mtr>')
        item = self.extract('The coefficient matrix is ' + coefficient + '. The augmented matrix is <math><mo>[</mo>' + augmented + '<mo>]</mo></math>')
        self.assertEqual(item['errors'], [])
        self.assertIn(r'\begin{bmatrix}1 & 2 \\ 3 & 4\end{bmatrix}', item['problem'])
        self.assertIn(r'\begin{array}{cc|c}1 & 2 & 7 \\ 3 & 4 & 7\end{array}', item['problem'])

    def test_system_alignment_keeps_row_annotations(self):
        table = '<mtable columnalign="left left"><mtr><mtd><mi>x</mi><mo>=</mo><mn>1</mn></mtd><mtd><mtext>first condition</mtext></mtd></mtr><mtr><mtd><mi>y</mi><mo>=</mo><mn>2</mn></mtd><mtd><mtext>second condition</mtext></mtd></mtr></mtable>'
        item = self.extract('<math><mo>{</mo>' + table + '</math>')
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['problem'], r'$\left\{\begin{aligned}x &=1 && \text{first condition} \\ y &=2 && \text{second condition}\end{aligned}\right.$')

    def test_html_indentation_cannot_turn_formula_labels_into_code_blocks(self):
        item = self.extract('<p>Find the value.</p><p>\n                <math><mi>a</mi><mo>=</mo></math>\n        </p>')
        self.assertEqual(item['errors'], [])
        self.assertIn('$a=$', item['problem'])
        self.assertNotRegex(item['problem'], r'(?m)^ {4,}\$')
        item = self.extract('<p>Code:</p><pre><code>x\n    y</code></pre>')
        self.assertIn('x\n    y', item['problem'])

    def test_matrix_fences_wrappers_and_scripted_closing_fence(self):
        for opening, closing, environment in [('[', ']', 'bmatrix'), ('(', ')', 'pmatrix'), ('|', '|', 'vmatrix'), ('‖', '‖', 'Vmatrix'), ('{', '}', 'Bmatrix')]:
            with self.subTest(environment=environment):
                item = self.extract('<math><mrow><mi>A</mi><mo>=</mo><mo>' + opening + '</mo><mstyle>' + TABLE + '</mstyle><mo>' + closing + '</mo></mrow></math>')
                self.assertEqual(item['errors'], [])
                self.assertIn('A=\\begin{' + environment + '}1 & 2 \\\\ 3 & 4\\end{' + environment + '}', item['problem'])
        item = self.extract('<math><mo>[</mo>' + TABLE + '<msup><mo>]</mo><mi>T</mi></msup></math>')
        self.assertEqual(item['problem'], r'${\begin{bmatrix}1 & 2 \\ 3 & 4\end{bmatrix}}^{T}$')
        for attributes, environment in [('', 'pmatrix'), ('open="[" close="]"', 'bmatrix')]:
            item = self.extract('<math><mfenced ' + attributes + '>' + TABLE + '</mfenced></math>')
            self.assertIn('\\begin{' + environment + '}', item['problem'])

    def test_equation_layouts_keep_alignment_and_scalar_fences(self):
        item = self.extract('<math><mo>[</mo>' + TABLE.replace('<mtable>', '<mtable columnalign="right left">') + '<mo>]</mo></math>')
        self.assertIn(r'[\begin{aligned}', item['problem'])
        self.assertEqual(item['errors'], [])
        item = self.extract('<math><mfenced><mi>x</mi><mi>y</mi></mfenced></math>')
        self.assertEqual(item['problem'], '$(x,y)$')
        item = self.extract('<math><mo>{</mo><mtable columnalign="left"><mtr><mtd><mi>x</mi><mo>=</mo><mn>1</mn></mtd></mtr><mtr><mtd><mi>y</mi><mo>=</mo><mn>2</mn></mtd></mtr></mtable><mo></mo></math>')
        self.assertEqual(item['problem'], r'$\left\{\begin{aligned}x &=1 \\ y &=2\end{aligned}\right.$')

    def test_unknown_significant_matrix_style_requires_review(self):
        item = self.extract('<math><mo>[</mo>' + TABLE.replace('<mtable>', '<mtable columnlines="dashed">') + '<mo>]</mo></math>')
        self.assertEqual(item['errors'], ['Unsupported MathML table columnlines'])
        item = self.extract('<math><mstyle mathbackground="url(unknown)"><mn>1</mn></mstyle></math>')
        self.assertEqual(item['errors'], ['Unsupported MathML mathbackground: url(unknown)'])

    def test_augmented_matrix_divider_and_horizontal_lines_survive(self):
        item = self.extract('<math><mo>[</mo>' + TABLE.replace('<mtable>', '<mtable columnlines="solid" rowlines="solid">') + '<mo>]</mo></math>')
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['problem'], r'$\left[\begin{array}{c|c}1 & 2 \\ \hline 3 & 4\end{array}\right]$')
        item = self.extract('<math>' + TABLE.replace('<mtable>', '<mtable columnalign="center center" columnlines="solid">') + '</math>')
        self.assertEqual(item['problem'], r'$\begin{array}{c|c}1 & 2 \\ 3 & 4\end{array}$')

    def test_ragged_matrix_trims_only_empty_trailing_cells(self):
        table = TABLE.replace('</mtd></mtr>', '</mtd><mtd></mtd></mtr>', 1)
        item = self.extract('<math><mo>[</mo>' + table + '<mo>]</mo></math>')
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['problem'], r'$\begin{bmatrix}1 & 2 \\ 3 & 4\end{bmatrix}$')
        item = self.extract('<math><mo>[</mo>' + table.replace('<mtd></mtd>', '<mtd><mn>5</mn></mtd>') + '<mo>]</mo></math>')
        self.assertEqual(item['errors'], ['Ragged MathML matrix'])

    def test_storage_preserves_matrix_and_highlight_text(self):
        item = self.extract('<math><mo>[</mo>' + TABLE.replace('<mn>2</mn>', '<mstyle mathbackground="lightgray"><mn>2</mn></mstyle>') + '<mo>]</mo></math>')
        kp = uuid.UUID('1cc70bda-40cf-5860-9a47-25f290c71041')
        topic = {':topic/math-academy-id': 1167, ':topic/knowledge-points': [{':knowledge-point/id': kp, ':knowledge-point/title': 'Matrix entry'}]}
        content = {'topic_id': 1167, 'questions': [], 'canonical_examples': [{
            'math_academy_id': 'e-4373', 'knowledge_point_id': str(kp),
            'problem': item['problem'], 'worked_solution': 'The entry is $a_{12}=2$.',
        }]}
        forms, _ = build_content_transaction(content, {1167: topic}, {})
        stored = next(form for form in loads(dumps(forms)) if isinstance(form, dict) and ':question/problem' in form)
        self.assertEqual(stored[':question/problem'], item['problem'])
        self.assertIn(r'\bbox[lightgray, 2pt]{2}', stored[':question/problem'])

    def test_saved_matrix_roundtrips_through_app_mathjax(self):
        item = self.extract((FIXTURES / 'introduction-mathml.html').read_text())
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        origin = f'http://127.0.0.1:{server.server_port}'
        try:
            page = self.browser.new_page()
            page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(origin + '/') else route.abort())
            page.goto(origin + '/ui/learning.css')
            page.set_content('<div id="matrix"></div>')
            page.add_script_tag(url=origin + '/ui/mathjax-config.js')
            page.add_script_tag(url=origin + '/ui/vendor/mathjax/tex-svg.js')
            result = page.evaluate('''async text => {
              await MathJax.startup.promise; matrix.textContent=text;
              await MathJax.typesetPromise([matrix]); const tables=[];
              for(const item of MathJax.startup.document.math) item.root.walkTree(node=>{
                if(node.kind==='mtable') tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length,alignment:node.attributes.get('columnalign')});
              });
              return {tables,errors:matrix.querySelectorAll('[data-mml-node="merror"]').length};
            }''', item['problem'])
            self.assertEqual(result, {'tables': [{'rows': 4, 'columns': 3, 'alignment': 'center'}], 'errors': 0})
            page.close()
        finally:
            server.shutdown()
            server.server_close()

if __name__ == '__main__':
    unittest.main()
