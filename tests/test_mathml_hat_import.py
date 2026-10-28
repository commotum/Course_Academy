"""Archived MathML hats preserve stretch, complete bases, and source variants."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {'question_capture': ROOT / 'scripts/question_capture/dom.js',
           'capture': ROOT / 'capture/scripts/browser/extract.js'}
SPEC = importlib.util.spec_from_file_location('historical_hat_import', ROOT / 'scripts/import_historical_question_content.py')
HISTORY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HISTORY)


class MathMLHatImportTests(unittest.TestCase):
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
            self.assertEqual(node.inner_html(), before, name)
            self.assertEqual(result['fields'], [], name)
            values[name] = (result['problem'].strip('$\n'), result['errors'])
        renderer = HISTORY.Renderer(None)
        value = renderer.m(BeautifulSoup(formula, 'html.parser').find('math'))
        values['history'] = (value, renderer.errors)
        return values

    def assert_formula(self, body, expected):
        for name, (value, errors) in self.extract_all('<math>' + body + '</math>').items():
            with self.subTest(importer=name):
                self.assertEqual(errors, [])
                self.assertEqual(value, expected)

    def mathjax(self):
        self.page.set_content('<div id="rendered"></div>')
        self.page.evaluate('window.MathJax={startup:{typeset:false}}')
        self.page.add_script_tag(content=(ROOT / 'ui/vendor/mathjax/tex-svg.js').read_text())

    def test_saved_regression_sources_preserve_wide_narrow_and_bold_bases(self):
        fixtures = json.loads((ROOT / 'tests/fixtures/mathml-hats.json').read_text())
        for fixture in fixtures:
            with self.subTest(source=fixture['source']):
                self.assertEqual(hashlib.sha256(fixture['mathml'].encode()).hexdigest(), fixture['mathml_sha256'])
                # The external archive is copied into this fixture; the test
                # does not require a separate MA checkout to be installed.
                if not fixture.get('external_source'):
                    source = ROOT / fixture['source']
                    self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), fixture['source_sha256'])
                    content = source.read_text()
                    if source.suffix == '.json':
                        content = json.loads(content)['html']
                    soup = BeautifulSoup(content, 'html.parser')
                    self.assertIn(fixture['mathml'], [str(m) for m in soup.find_all('math')])
                for name, (value, errors) in self.extract_all(fixture['mathml']).items():
                    with self.subTest(importer=name):
                        self.assertEqual(errors, [])
                        self.assertNotIn(r'\overset{^}', value)
                        if fixture['kind'] == 'wide':
                            self.assertIn(r'\widehat{', value)
                            if fixture['selector'] == 'question-159393':
                                self.assertEqual(value, r'\widehat{\,y}={\widehat{\,\beta }}_{0}+{\widehat{\,\beta }}_{1}x=1-2.6x')
                        elif fixture['kind'] == 'narrow':
                            self.assertIn(r'\hat{\mathbfit{β}}', value)
                        else:
                            self.assertEqual(value, r'\hat{\mathbf{x}}')

    def test_stretchy_attribute_controls_hat_width_with_full_base(self):
        for attrs, command in [('', r'\widehat'), (' stretchy="true"', r'\widehat'), (' stretchy="false"', r'\hat')]:
            for mover_attrs in ('', ' accent="true"'):
                with self.subTest(attrs=attrs, mover_attrs=mover_attrs):
                    body = '<mover' + mover_attrs + '><mrow><mi>a</mi><mo>+</mo><mfrac><mi>b</mi><mn>2</mn></mfrac></mrow><mo' + attrs + '>^</mo></mover>'
                    self.assert_formula(body, command + r'{a+\frac{b}{2}}')

    def test_nested_hats_and_neighboring_scripts_keep_their_scope(self):
        self.assert_formula('<msub><mover><mrow><mover><mi>x</mi><mo stretchy="false">^</mo></mover><mo>+</mo><mi>y</mi></mrow><mo>^</mo></mover><mn>1</mn></msub>'
                            '<msup><mi>z</mi><mn>2</mn></msup>',
                            r'{\widehat{\hat{x}+y}}_{1}{z}^{2}')

    def test_ordinary_limits_scripts_and_oversets_are_unchanged(self):
        self.assert_formula('<munder><mo>lim</mo><mrow><mi>x</mi><mo>→</mo><mn>0</mn></mrow></munder>'
                            '<msup><mi>x</mi><mn>2</mn></msup><mover><mi>x</mi><mi>n</mi></mover>'
                            '<mover><mi>x</mi><mo>∧</mo></mover>',
                            r'\lim_{x\to 0}{x}^{2}\overset{n}{x}\overset{∧}{x}')

    def test_hat_must_be_an_operator_and_unsupported_source_styles_are_explicit(self):
        self.assert_formula('<mover><mi>x</mi><mtext>^</mtext></mover>', r'\overset{\text{^}}{x}')
        cases = [('mathcolor="red"', ''), ('mathbackground="yellow"', ''), ('minsize="3em"', ''), ('', 'accent="false"')]
        for accent_attrs, mover_attrs in cases:
            for name, (value, errors) in self.extract_all('<math><mover ' + mover_attrs + '><mi>x</mi><mo ' + accent_attrs + '>^</mo></mover></math>').items():
                with self.subTest(importer=name, attrs=(accent_attrs, mover_attrs)):
                    self.assertTrue(any(e.startswith('Unsupported MathML hat:') for e in errors))
                    self.assertNotIn(r'\widehat', value)
                    if name == 'question_capture' and accent_attrs.startswith('mathcolor'):
                        self.assertIn(r'\color{red}', value)
        for name, (_, errors) in self.extract_all('<math><mover><mrow><mi mathvariant="bold">x</mi><mo>+</mo><mi>y</mi></mrow><mo>^</mo></mover></math>').items():
            self.assertIn('Unsupported MathML hat: base mathvariant', errors, name)

    def test_existing_scoped_base_color_is_preserved_by_question_capture(self):
        self.page.set_content('<div id="fixture"><div class="questionWidget-text"><math><mover><mi mathcolor="red">x</mi><mo stretchy="false">^</mo></mover></math></div></div>')
        result = self.page.locator('#fixture').evaluate(self.sources['question_capture'])
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['problem'], r'$\hat{{\color{red}x}}$')

    def test_vendored_mathjax_confirms_stretch_geometry_and_base_variants(self):
        self.mathjax()
        results = self.page.evaluate(r'''async inputs => {
          await MathJax.startup.promise;
          const results=[];
          for (const tex of inputs) {
            const node=await MathJax.tex2svgPromise(tex);
            document.querySelector('#rendered').append(node);
            const mover=node.querySelector('svg g[data-mml-node="mover"]');
            const [base,accent]=[...mover.children].map(n=>n.getBoundingClientRect());
            const math=node.querySelector('mjx-assistive-mml math');
            results.push({tex,errors:node.querySelectorAll('[data-mml-node="merror"]').length,
              ratio:accent.width/base.width,stretchy:math.querySelector('mover > mo').getAttribute('stretchy'),
              variants:[...math.querySelectorAll('[mathvariant]')].map(n=>n.getAttribute('mathvariant')),
              mathml:math.outerHTML});
          }
          return results;
        }''', [r'\hat{abcdefgh}', r'\widehat{abcdefgh}', r'\hat{\mathbf{x}}', r'\hat{\mathbfit{β}}'])
        self.assertTrue(all(result['errors'] == 0 for result in results))
        self.assertLess(results[0]['ratio'], .3)
        # Wide hats use larger accent glyphs; MathJax caps their size over very
        # long bases, so they need not span every character as braces do.
        self.assertGreater(results[1]['ratio'], results[0]['ratio'] * 2)
        self.assertEqual(results[0]['stretchy'], 'false')
        self.assertIsNone(results[1]['stretchy'])
        self.assertIn('bold', results[2]['variants'])
        self.assertIn('bold-italic', results[3]['variants'])
        # Re-import the renderer's primary-source MathML and retain its exact
        # narrow/wide distinction, including source base font variants.
        for result in results:
            for name, (value, errors) in self.extract_all(result['mathml']).items():
                with self.subTest(importer=name, tex=result['tex']):
                    self.assertEqual(errors, [])
                    self.assertEqual(value.replace(' ', ''), result['tex'])


if __name__ == '__main__':
    unittest.main()
