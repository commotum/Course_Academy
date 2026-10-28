"""Source braces keep their full span and centered labels in every importer.

Run with a Python environment containing BeautifulSoup and Playwright; no
application server, live source site, or database is used.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'tests/fixtures/mathml-braces.json'
SOURCES = {
    'question_capture': ROOT / 'scripts/question_capture/dom.js',
    'capture': ROOT / 'capture/scripts/browser/extract.js',
}
SPEC = importlib.util.spec_from_file_location('historical_import', ROOT / 'scripts/import_historical_question_content.py')
HISTORY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HISTORY)


class MathMLBraceImportTests(unittest.TestCase):
    def test_zero_rule_fraction_keeps_stack_instead_of_division(self):
        self.assert_formula('<mfrac linethickness="0"><mi>n</mi><mi>k</mi></mfrac>',
                            r'\genfrac{}{}{0pt}{}{n}{k}')

    def test_unruled_data_columns_keep_source_alignment(self):
        self.assert_formula('<mtable columnalign="left center right" columnspacing="1em"><mtr><mtd><mi>x</mi></mtd><mtd><mn>1</mn></mtd><mtd><mn>2</mn></mtd></mtr><mtr><mtd><mi>y</mi></mtd><mtd><mn>3</mn></mtd><mtd><mn>4</mn></mtd></mtr></mtable>',
                            r'\begin{array}{lcr}x & 1 & 2 \\ y & 3 & 4\end{array}')

    def test_piecewise_brace_keeps_value_and_condition_columns(self):
        self.assert_formula('<mrow><mo>{</mo><mtable><mtr><mtd><mn>0</mn></mtd><mtd><mi>x</mi><mo>&lt;</mo><mn>1</mn></mtd></mtr><mtr><mtd><mn>2</mn></mtd><mtd><mi>x</mi><mo>≥</mo><mn>1</mn></mtd></mtr></mtable></mrow>',
                            r'\begin{cases}0 & x<1 \\ 2 & x\ge 1\end{cases}')

    def test_block_limit_preserves_operator_and_display_in_every_importer(self):
        formula = '<math display="block"><munder><mo>lim</mo><mrow><mi>x</mi><mo>→</mo><mn>2</mn></mrow></munder><mi>f</mi></math>'
        for name, source in self.sources.items():
            self.page.set_content('<div id="fixture"><div class="questionWidget-text">' + formula + '</div></div>')
            result = self.page.locator('#fixture').evaluate(source)
            with self.subTest(importer=name):
                self.assertEqual(result['problem'], '$$\n' + r'\lim_{x\to 2}f' + '\n$$')
        self.assertEqual(HISTORY.Renderer(None).text(BeautifulSoup(formula, 'html.parser').math),
                         '$$\n' + r'\lim_{x\to 2}f' + '\n$$')

    def test_instructional_colors_remain_scoped_to_matrix_entries(self):
        self.assert_formula('<mtable><mtr><mtd><mstyle mathcolor="blue"><mn>2</mn></mstyle></mtd>'
                            '<mtd><mn>3</mn></mtd></mtr><mtr><mtd><mn mathcolor="#4169E1">4</mn></mtd>'
                            '<mtd><mn mathbackground="lightgray">5</mn></mtd></mtr></mtable>',
                            r'\begin{aligned}{\color{blue}2} & 3 \\ {\color[HTML]{4169E1}4} & \bbox[lightgray, 2pt]{5}\end{aligned}')

    def test_vector_basis_and_domain_fonts_remain_distinct(self):
        self.assert_formula('<mi mathvariant="bold">v</mi><msub><mi mathvariant="script">B</mi><mn>1</mn></msub>'
                            '<mi mathvariant="double-struck">R</mi><mi mathvariant="bold" mathcolor="red">β</mi>',
                            r'\mathbf{v}{\mathcal{B}}_{1}\mathbb{R}\mathbf{{\color{red}β}}')

    def test_nested_source_color_and_background_keep_both_cues(self):
        self.assert_formula('<mstyle mathbackground="#ffe"><mstyle mathcolor="red"><mn>7</mn></mstyle></mstyle><mn>8</mn>',
                            r'\bbox[#ffe, 2pt]{{\color{red}7}}8')

    def test_powered_named_functions_keep_observed_application_marker(self):
        self.assert_formula('<msup><mi>csc</mi><mn>2</mn></msup><mo>⁡</mo><mi>x</mi>',
                            r'{\operatorname{csc}}^{2}x')
        self.assert_formula('<msub><mstyle><mi>log</mi></mstyle><mn>2</mn></msub><mo>⁡</mo><mi>x</mi>',
                            r'{\operatorname{log}}_{2}x')
        self.assert_formula('<msup><mi>x</mi><mi>csc</mi></msup><mo>⁡</mo><mi>y</mi>',
                            r'{x}^{csc}y')
        self.assert_formula('<msup><mi>csc</mi><mn>2</mn></msup><mi>x</mi>', r'{csc}^{2}x')

    def test_literal_currency_and_percent_are_escaped_by_every_importer(self):
        self.assert_formula('<mtext>$</mtext><mn>12</mn><mo>%</mo>', r'\text{\$}12\%')
        self.assert_formula('<mtext>12% off</mtext>', r'\text{12\% off}')
        self.assert_formula('<mo>{</mo><mi>x</mi><mo>}</mo>', r'\{x\}')
        self.assert_formula('<mtext># orders</mtext>', r'\text{\# orders}')

    @classmethod
    def setUpClass(cls):
        cls.runtime = sync_playwright().start()
        try:
            cls.browser = cls.runtime.chromium.launch(headless=True)
        except Exception:
            cls.runtime.stop()
            raise
        cls.sources = {name: path.read_text() for name, path in SOURCES.items()}

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.runtime.stop()

    def setUp(self):
        self.context = self.browser.new_context()
        self.context.route('**/*', lambda route: route.abort())
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def extract_all(self, formula):
        self.page.set_content('<div id="fixture"><div class="questionWidget-text">' + formula + '</div></div>')
        node = self.page.locator('#fixture')
        before = node.inner_html()
        values = {}
        for name, source in self.sources.items():
            result = node.evaluate(source)
            self.assertEqual(result['errors'], [], name)
            self.assertEqual(node.inner_html(), before, name)
            self.assertEqual(result['fields'], [], name)
            values[name] = result['problem'].strip('$\n')
        renderer = HISTORY.Renderer(None)
        values['history'] = renderer.m(BeautifulSoup(formula, 'html.parser').find('math'))
        self.assertEqual(renderer.errors, [])
        return values

    def assert_formula(self, body, expected):
        values = self.extract_all('<math>' + body + '</math>')
        for name, value in values.items():
            with self.subTest(importer=name):
                self.assertEqual(value, expected)
        return values

    def brace(self, body='<mi>a</mi><mo>+</mo><mi>b</mi>', *, over=False, label=None, attrs=''):
        tag, glyph = ('mover', '⏞') if over else ('munder', '⏟')
        result = '<' + tag + attrs + '><mrow>' + body + '</mrow><mo>' + glyph + '</mo></' + tag + '>'
        if label is not None:
            result = '<' + tag + '><mrow data-mjx-texclass="OP">' + result + '</mrow>' + label + '</' + tag + '>'
        return result

    def test_authentic_tutorial_braces_scope_complete_limits_and_keep_both_labels(self):
        fixture = json.loads(FIXTURE.read_text())
        source = ROOT / fixture['source']
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), fixture['source_sha256'])
        self.assertEqual(hashlib.sha256(fixture['mathml'].encode()).hexdigest(), fixture['mathml_sha256'])
        source_math = [str(m) for m in BeautifulSoup(source.read_text(), 'html.parser').find_all('math') if '⏟' in m.get_text()]
        self.assertIn(fixture['mathml'], source_math)
        self.assertNotIn('accentunder=', fixture['mathml'])
        for name, value in self.extract_all(fixture['mathml']).items():
            with self.subTest(importer=name):
                self.assertEqual(value.count(r'\underbrace{'), 2)
                self.assertIn(r'\underbrace{\lim_{h\to 0}\frac{\operatorname{cos}', value)
                self.assertIn(r'(h)-1}{h}}_{0}', value)
                self.assertIn(r'\underbrace{\lim_{h\to 0}\frac{\operatorname{sin}', value)
                self.assertIn(r'(h)}{h}}_{1}', value)
                self.assertNotIn('⏟', value)
                self.assertNotIn(r'{\underbrace', value)

    def test_labeled_and_unlabeled_braces_do_not_depend_on_accent_attributes(self):
        for over in (False, True):
            command, script, attr = (r'\overbrace', '^', 'accent') if over else (r'\underbrace', '_', 'accentunder')
            for attrs in ('', ' ' + attr + '="true"'):
                for label in (None, '<mn>0</mn>'):
                    with self.subTest(over=over, attrs=attrs, label=label):
                        self.assert_formula(self.brace(over=over, label=label, attrs=attrs),
                                            command + '{a+b}' + (script + '{0}' if label else ''))

    def test_nested_braces_and_label_expressions_keep_their_own_groups(self):
        inner = self.brace('<mfrac><mi>x</mi><mn>2</mn></mfrac>', label='<msub><mi>n</mi><mi>i</mi></msub>')
        outer = self.brace(inner + '<mo>+</mo><msup><mi>y</mi><mn>2</mn></msup>', over=True,
                           label='<mrow><mi>N</mi><mo>=</mo><mfrac><mn>1</mn><mn>2</mn></mfrac></mrow>')
        self.assert_formula(outer + '<msub><mi>z</mi><mn>3</mn></msub>',
                            r'\overbrace{\underbrace{\frac{x}{2}}_{{n}_{i}}+{y}^{2}}^{N=\frac{1}{2}}{z}_{3}')

    def test_transparent_wrappers_and_stacked_labels_preserve_limits(self):
        brace = self.brace(label='<mn>0</mn>')
        self.assert_formula('<munder><mrow><semantics><mstyle>' + self.brace() +
                            '</mstyle><annotation encoding="application/x-tex">source</annotation></semantics></mrow><mn>1</mn></munder>',
                            r'\underbrace{a+b}_{1}')
        self.assert_formula('<munder>' + brace + '<mi>n</mi></munder>', r'\underset{n}{\underbrace{a+b}_{0}}')
        over = self.brace(over=True, label='<mn>1</mn>')
        self.assert_formula('<mover>' + over + '<mi>n</mi></mover>', r'\overset{n}{\overbrace{a+b}^{1}}')

    def test_ordinary_scripts_limits_and_nonbrace_oversets_are_unchanged(self):
        self.assert_formula('<msub><mi>x</mi><mi>i</mi></msub><msup><mi>y</mi><mn>2</mn></msup>'
                            '<msubsup><mi>a</mi><mi>i</mi><mn>3</mn></msubsup>'
                            '<munder><mo>lim</mo><mrow><mi>x</mi><mo>→</mo><mn>0</mn></mrow></munder>'
                            '<munderover><mo>∑</mo><mi>i</mi><mi>n</mi></munderover>'
                            '<mover><mi>x</mi><mi>y</mi></mover>',
                            r'{x}_{i}{y}^{2}{a}_{i}^{3}\lim_{x\to 0}{\sum }_{i}^{n}\overset{y}{x}')

    def test_brace_glyph_must_be_the_accent_operator_not_label_prose(self):
        self.assert_formula('<munder><mi>x</mi><mtext>⏟</mtext></munder>'
                            '<mover><mi>y</mi><mtext>⏞</mtext></mover>',
                            r'{x}_{\text{⏟}}\overset{\text{⏞}}{y}')

    def test_operator_only_brace_styling_is_preserved_as_an_explicit_review_gap(self):
        # This importer supports source colors. A color on just the glyph
        # cannot become a color around the entire semantic brace expression.
        for over in (False, True):
            tag, glyph = ('mover', '⏞') if over else ('munder', '⏟')
            for attribute, value, expected_accent in (
                ('mathcolor', 'red', r'{\color{red}' + glyph + '}'),
                ('mathbackground', '#ffe', r'\bbox[#ffe, 2pt]{' + glyph + '}'),
            ):
                with self.subTest(over=over, attribute=attribute):
                    formula = '<math><' + tag + '><mrow><mi>a</mi><mo>+</mo><mi>b</mi></mrow><mo ' + attribute + '="' + value + '">' + glyph + '</mo></' + tag + '></math>'
                    self.page.set_content('<div id="fixture"><div class="questionWidget-text">' + formula + '</div></div>')
                    results = [self.page.locator('#fixture').evaluate(source) for source in self.sources.values()]
                    for result in results:self.assertEqual(result['errors'], ['Unsupported styled MathML brace: ' + attribute])
                    expected = r'\overset{' + expected_accent + '}{a+b}' if over else '{a+b}_{' + expected_accent + '}'
                    for result in results:self.assertEqual(result['problem'], '$' + expected + '$')
                    renderer=HISTORY.Renderer(None)
                    self.assertEqual(renderer.m(BeautifulSoup(formula,'html.parser').math), expected)
                    self.assertEqual(renderer.errors, ['Unsupported styled MathML brace: ' + attribute])
        # An inherited/no-op color does not prevent faithful brace conversion.
        self.page.set_content('<div id="fixture"><div class="questionWidget-text"><math><munder><mi>x</mi><mo mathcolor="inherit">⏟</mo></munder></math></div></div>')
        result = self.page.locator('#fixture').evaluate(self.sources['question_capture'])
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['problem'], r'$\underbrace{x}$')

    def test_vendored_mathjax_braces_span_expression_and_center_labels(self):
        body = ''.join('<mi>' + letter + '</mi><mo>+</mo>' for letter in 'abcdefg') + '<mi>h</mi>'
        values = []
        for over in (False, True):
            values.extend(self.extract_all('<math>' + self.brace(body, over=over, label='<mn>1</mn>') + '</math>').values())
        self.page.set_content('<div id="rendered"></div>')
        self.page.evaluate('window.MathJax={startup:{typeset:false}}')
        self.page.add_script_tag(content=(ROOT / 'ui/vendor/mathjax/tex-svg.js').read_text())
        results = self.page.evaluate('''async values => {
          await MathJax.startup.promise;
          const results=[];
          for (const tex of values) {
            const node=await MathJax.tex2svgPromise(tex);
            document.querySelector('#rendered').append(node);
            const boxes=[...node.querySelectorAll('svg g[data-mml-node="munder"],svg g[data-mml-node="mover"]')].map(n => {
              const [base,decoration]=[...n.children].map(child=>child.getBoundingClientRect());
              return {baseWidth:base.width,decorationWidth:decoration.width,
                centerDifference:Math.abs((base.left+base.width/2)-(decoration.left+decoration.width/2))};
            });
            results.push({tex,errors:node.querySelectorAll('[data-mml-node="merror"]').length,boxes});
          }
          return results;
        }''', values)
        for result in results:
            with self.subTest(tex=result['tex']):
                self.assertEqual(result['errors'], 0)
                self.assertEqual(len(result['boxes']), 2)
                label, brace = result['boxes']
                self.assertGreater(brace['decorationWidth'] / brace['baseWidth'], .95)
                self.assertLess(label['decorationWidth'] / label['baseWidth'], .1)
                self.assertLess(label['centerDifference'], 2)


if __name__ == '__main__':
    unittest.main()
