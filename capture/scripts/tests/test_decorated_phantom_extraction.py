"""Keep visible source containers while their original contents remain hidden."""
import base64
import hashlib
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urlparse

from scripts.browser.adapter import EXTRACT
from scripts.database.text import markdown as database_markdown

REPO = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).parent / 'fixtures/decorated-phantom-mathml.json'


class DecoratedPhantomTests(unittest.TestCase):
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
        self.requests = []
        def route(request):
            url = urlparse(request.request.url)
            if url.netloc != 'offline.local':
                request.abort()
            elif url.path == '/':
                request.fulfill(body='<div id="rendered"></div>', content_type='text/html')
            elif url.path.startswith('/ui/') and (REPO / url.path.lstrip('/')).is_file():
                self.requests.append(url.path)
                request.fulfill(path=str(REPO / url.path.lstrip('/')), content_type='application/javascript')
            else:
                request.abort()
        self.context.route('**/*', route)
        self.page = self.context.new_page()

    def tearDown(self):
        self.context.close()

    def extract(self, mathml):
        self.page.set_content('<div id="q" class="questionWidget"><div class="questionWidget-text">' + mathml + '</div></div>')
        root = self.page.locator('#q')
        original = root.inner_html()
        record = root.evaluate(EXTRACT)
        self.assertEqual(root.inner_html(), original)
        return record

    @staticmethod
    def boxed(child='<mphantom><mi>A</mi></mphantom>', decoration='mathbackground="lightgray"', padding='height="+2pt" depth="+2pt" lspace="2pt" width="+4pt"'):
        return '<math><mstyle ' + decoration + '><mpadded ' + padding + '>' + child + '</mpadded></mstyle></math>'

    def test_all_eighteen_original_mathml_sources_keep_visible_containers_and_hidden_width(self):
        rows = json.loads(FIXTURES.read_text())
        self.assertEqual(len(rows), 18)
        for row in rows:
            with self.subTest(question=row['id']):
                for html, sha in zip(row['mathml'], row['mathml_sha256']):
                    self.assertEqual(hashlib.sha256(html.encode()).hexdigest(), sha)
                record = self.extract(''.join(row['mathml']))
                self.assertEqual(record['errors'], [])
                self.assertIn(r'\phantom{', record['problem'])
                if row['id'] in ('q-104514', 'q-104516', 'q-17317', 'q-114506'):
                    self.assertIn(r'\enclose{longdiv}', record['problem'])
                else:
                    self.assertIn(r'\bbox[', record['problem'])
                if row['id'] == 'q-78561':
                    self.assertIn(r'\mathbf{q}', record['problem'])
                    self.assertIn(r'\bbox[2pt,lightgray]', record['problem'])
                    self.assertIn(r'\color{blue}', record['problem'])

    def test_bare_and_plain_fenced_phantoms_keep_existing_behavior(self):
        record = self.extract('<math><mi>x</mi><mphantom><mi>A</mi></mphantom><mo>+</mo><mrow><mo>[</mo><mphantom><mi>B</mi></mphantom><mo>]</mo></mrow></math>')
        self.assertEqual(record['errors'], [])
        self.assertEqual(record['problem'], '$x+[]$')
        self.assertNotIn('phantom', record['problem'])

    def test_calculator_square_root_button_preserves_visible_root_and_hidden_radicand(self):
        child = '<mstyle mathcolor="gray"><msqrt><mrow data-mjx-texclass="ORD"><mphantom><mi>a</mi></mphantom></mrow></msqrt></mstyle>'
        record = self.extract(self.boxed(child))
        self.assertEqual(record['errors'], [])
        self.assertIn(r'\color{gray}{\sqrt{\phantom{a}}}', record['problem'])
        self.assertIn(r'\bbox[2pt,lightgray]', record['problem'])
        changed = self.extract(self.boxed(child.replace('<msqrt>', '<msqrt mathsize="2em">')))
        self.assertTrue(any('geometry attributes' in error for error in changed['errors']))

    def test_unpadded_gray_phantom_keeps_original_width_without_adding_padding(self):
        source = '<math><mstyle mathbackground="gray"><mrow data-mjx-texclass="ORD"><mphantom><mn>00</mn></mphantom></mrow></mstyle></math>'
        record = self.extract(source)
        self.assertEqual(record['errors'], [])
        self.assertEqual(record['problem'], r'$\bbox[gray]{\phantom{00}}$')
        host = self.ui_render(record['problem'])
        self.assertEqual(host.locator('mjx-assistive-mml mpadded').count(), 0)
        self.assertEqual(host.locator('mjx-assistive-mml mstyle[mathbackground="gray"] mphantom mn').text_content(), '00')
        self.assertEqual(host.locator('svg rect[fill="gray"]').count(), 1)
        self.assertEqual(host.locator('svg use').count(), 0)
        changed = self.extract(source.replace('data-mjx-texclass="ORD"', 'style="transform:scale(2)"'))
        self.assertIn('Unsupported decorated MathML phantom: padding container', changed['errors'])

    def test_spacing_only_mathml_does_not_create_empty_markdown_delimiters(self):
        from scripts.database.math_content import prose
        spacing = '<mrow><mphantom><mfrac><mi>x</mi><mi>y</mi></mfrac></mphantom></mrow>'
        for formula in ('<math>' + spacing + '</math>',
                        '<mjx-container><mjx-assistive-mml><math>' + spacing + '</math></mjx-assistive-mml></mjx-container>'):
            record = self.extract('Divide.<span>' + formula + '</span><p>Answer below.</p>')
            self.assertEqual(record['errors'], [])
            self.assertNotIn('$', record['problem'])
            self.assertEqual(prose(record['problem']), record['problem'])

    def test_completed_empty_mathjax_svg_is_not_a_missing_graphic(self):
        svg = '<svg width="0.036ex" height="0.036ex" viewBox="0 0 16 16"><g><g data-mml-node="math"></g></g></svg>'
        record = self.extract('<mjx-container jax="SVG">'+svg+'</mjx-container><p>Actual tutorial content.</p>')
        self.assertEqual(record['errors'], [])
        self.assertEqual(record['assets'], [])
        self.assertEqual(record['problem'], 'Actual tutorial content.')
        for altered in [svg.replace('0 0 16 16','0 0 32 16'),
                        svg.replace('data-mml-node="math"></g>','data-mml-node="math"><g data-mml-node="mi"></g></g>'),
                        svg.replace('data-mml-node="math"','data-mml-node="unknown"')]:
            with self.subTest(source=altered):
                record = self.extract('<mjx-container jax="SVG">'+altered+'</mjx-container>')
                self.assertEqual(len(record['assets']), 1)

    def test_mathjax_solid_color_width_border_order_preserves_the_box(self):
        first=self.extract(self.boxed(decoration='style="border:1pt solid black"'))
        reordered=self.extract(self.boxed(decoration='style="border:solid black 1pt"'))
        self.assertEqual(reordered['errors'],[])
        self.assertEqual(first['problem'],reordered['problem'])
        self.assertIn(r'\bbox[2pt,border:1pt solid black]',reordered['problem'])

    def test_source_border_without_explicit_color_preserves_inherited_color(self):
        record = self.extract(self.boxed(decoration='style="border:1pt solid"'))
        self.assertEqual(record['errors'], [])
        self.assertIn(r'\bbox[2pt,border:1pt solid]{\phantom{A}}', record['problem'])

    def test_broken_currency_title_retains_original_visible_svg(self):
        for token in (r'\[math]', r'\[/math]'):
            svg = '<svg viewBox="0 0 20 20"><title>' + token + '6.42</title><path d="M0 0L1 1"/></svg>'
            record = self.extract('<mjx-container jax="SVG">' + svg + '</mjx-container>')
            self.assertEqual(record['errors'], [])
            self.assertEqual(len(record['assets']), 1)
            self.assertEqual(record['problem'], '![](@asset-0@)')

    def test_unknown_css_or_invalid_color_is_an_explicit_gap(self):
        for decoration in ('style="border:1pt solid black; transform:scale(2)"',
                           'style="border:1pt solid banana"',
                           'mathbackground="banana"', 'mathbackground="inherit"',
                           'mathbackground="currentColor"', 'mathbackground="lightgray" mathsize="2em"'):
            with self.subTest(decoration=decoration):
                record = self.extract(self.boxed(decoration=decoration))
                self.assertTrue(any('Unsupported decorated MathML phantom' in e for e in record['errors']))
                self.assertTrue(all('problem' in parts for parts in record['extraction_error_parts'].values()))

    def test_asymmetric_decimal_or_unknown_padding_is_an_explicit_gap(self):
        for padding in ('height="+2pt" depth="+3pt" lspace="2pt" width="+4pt"',
                        'height="+2.5pt" depth="+2.5pt" lspace="2.5pt" width="+5pt"',
                        'height="+2pt" depth="+2pt" lspace="2pt" width="+5pt"',
                        'height="+2pt" depth="+2pt" lspace="2pt" width="+4pt" voffset="2pt"'):
            with self.subTest(padding=padding):
                record = self.extract(self.boxed(padding=padding))
                self.assertTrue(record['errors'])

    def test_unknown_hidden_geometry_is_not_approximated(self):
        for child in ('<mphantom><mspace width="2em"/></mphantom>',
                      '<mphantom><mspace/></mphantom>',
                      '<mphantom><mpadded width="3em"><mi>A</mi></mpadded></mphantom>',
                      '<mphantom><msup mathsize="2em"><mi>A</mi><mn>2</mn></msup></mphantom>',
                      '<mphantom style="transform:scale(2)"><mi>A</mi></mphantom>',
                      '<mphantom><mi mathvariant="double-struck">A</mi></mphantom>'):
            with self.subTest(child=child):
                self.assertTrue(self.extract(self.boxed(child))['errors'])

    def test_fixed_phantom_bar_in_long_division_keeps_source_spacing(self):
        source = ('<math><menclose notation="longdiv"><mn>5</mn>'
                  '<mphantom><mrow data-mjx-texclass="ORD"><mo stretchy="false">|</mo></mrow></mphantom>'
                  '<mn>0</mn><mphantom><mo stretchy="false">|</mo></mphantom>'
                  '<mn>4</mn></menclose></math>')
        record = self.extract(source)
        self.assertEqual(record['errors'], [])
        self.assertEqual(record['problem'], r'$\enclose{longdiv}{5\phantom{|}0\phantom{|}4}$')
        host = self.ui_render(record['problem'])
        self.assertEqual(host.locator('svg [data-mml-node="mphantom"]').count(), 2)
        self.assertEqual(host.locator('svg [data-mml-node="mphantom"] use').count(), 0)

    def test_stretchy_or_other_operator_geometry_still_requires_support(self):
        for attributes in ('stretchy="true"', 'stretchy="false" minsize="2em"',
                           'stretchy="false" maxsize="3em"'):
            with self.subTest(attributes=attributes):
                record = self.extract(self.boxed('<mphantom><mo ' + attributes + '>|</mo></mphantom>'))
                self.assertTrue(record['errors'])

    def test_both_color_and_bold_preserve_the_hidden_source_width(self):
        record = self.extract(self.boxed('<mphantom><mi mathcolor="blue" mathvariant="bold">q</mi></mphantom>'))
        self.assertEqual(record['errors'], [])
        self.assertIn(r'\phantom{\color{blue}{\mathbf{q}}}', record['problem'])

    def ui_render(self, source, fields=None):
        # Run the repository's actual markdown and typeset bodies, actual
        # configuration and local vendored dependencies. No live UI/API calls.
        self.page.goto('http://offline.local/')
        def module_url(path, substitutions=()):
            code = path.read_text()
            for before, after in substitutions:
                code = code.replace(before, after)
            return 'data:text/javascript;base64,' + base64.b64encode(code.encode()).decode()
        self.page.evaluate('async url => {window.marked=(await import(url)).marked;}', module_url(REPO / 'ui/vendor/marked/marked.esm.js'))
        self.page.evaluate('async url => {window.inlinePrompt=(await import(url)).inlinePrompt;}', module_url(REPO / 'ui/question-fields.js'))
        self.page.evaluate('async url => {window.romanLists=(await import(url)).romanLists;}', module_url(REPO / 'ui/prose-lists.js', [("import { marked } from './vendor/marked/marked.esm.js';", 'const marked=window.marked;')]))
        self.page.add_script_tag(url='http://offline.local/ui/vendor/dompurify/purify.min.js')
        self.page.add_script_tag(url='http://offline.local/ui/mathjax-config.js')
        ui = (REPO / 'ui/activity.js').read_text()
        functions = [re.search(r'function ' + name + r'\([^\n]*\) \{[\s\S]*?\n\}', ui).group()
                     for name in ('el', 'assetURL', 'fieldLabel', 'markdown', 'loadMath', 'typeset')]
        escape = next(line for line in ui.splitlines() if line.startswith('function escapeHTML('))
        self.page.add_script_tag(content='let mathLoader=null;let typesetting=Promise.resolve();\n' + escape + '\n' + '\n'.join(functions) + '\nif(!crypto.randomUUID)crypto.randomUUID=()=>"offline-token";window.renderSource=markdown;window.typesetSource=typeset;')
        self.page.evaluate('''async ({source,fields}) => {
          const host=document.querySelector('#rendered');host.append(renderSource(source,fields));
          await typesetSource(host);
        }''', {'source': source, 'fields': fields or []})
        self.assertEqual(self.page.locator('.math-error,[data-mml-node="merror"]').count(), 0)
        return self.page.locator('#rendered')

    def test_actual_ui_config_keeps_exact_shading_padding_and_bold_phantom_invisible(self):
        source = self.extract(self.boxed('<mphantom><mi mathcolor="blue" mathvariant="bold">q</mi></mphantom>'))['problem']
        host = self.ui_render(database_markdown(source))
        self.assertIn('/ui/vendor/mathjax/input/tex/extensions/bbox.js', self.requests)
        self.assertEqual(host.locator('svg use').count(), 0)
        self.assertEqual(host.locator('svg [data-mml-node="mphantom"]').count(), 1)
        self.assertEqual(host.locator('svg rect[fill="lightgray"]').count(), 1)
        padded = host.locator('mjx-assistive-mml mpadded')
        self.assertEqual([padded.get_attribute(a) for a in ('height','depth','lspace','width')], ['+2pt','+2pt','2pt','+4pt'])
        self.assertEqual(host.locator('mjx-assistive-mml mphantom mi').get_attribute('mathvariant'), 'bold')
        self.assertEqual(host.locator('mjx-assistive-mml [mathcolor="blue"]').count(), 1)

    def test_actual_ui_config_keeps_original_border_and_field_locations(self):
        row = next(x for x in json.loads(FIXTURES.read_text()) if x['id']=='q-118389')
        expression = self.extract(''.join(row['mathml']))['problem']
        # The original border marker and a captured answer location coexist.
        host = self.ui_render(database_markdown('Choose {{field-1}}.\n\n' + expression), [{'key':'field-1','type':'select','choices':[]}])
        self.assertEqual(host.locator('.field-location[data-field-key="field-1"]').count(), 1)
        self.assertGreater(host.locator('svg use').count(), 0)
        self.assertEqual(host.locator('svg [data-mml-node="mphantom"] use').count(), 0)
        style = host.locator('mjx-assistive-mml mstyle[style]').first.get_attribute('style')
        self.assertEqual(style, 'border:1pt solid black')
        padded = host.locator('mjx-assistive-mml mpadded')
        self.assertEqual([padded.get_attribute(a) for a in ('height','depth','lspace','width')], ['+3pt','+3pt','3pt','+6pt'])
        self.assertEqual(host.locator('svg [data-mml-node="mphantom"]').count(), 1)

    def test_actual_ui_long_division_enclosure_keeps_hidden_width(self):
        row = next(x for x in json.loads(FIXTURES.read_text()) if x['id']=='q-104514')
        source = self.extract(''.join(row['mathml']))['problem']
        host = self.ui_render(database_markdown(source))
        self.assertIn('/ui/vendor/mathjax/input/tex/extensions/enclose.js', self.requests)
        self.assertEqual(host.locator('mjx-assistive-mml menclose').count(), 1)
        self.assertEqual(host.locator('mjx-assistive-mml menclose').get_attribute('notation') or 'longdiv', 'longdiv')
        self.assertEqual(host.locator('svg [data-mml-node="menclose"]').count(), 1)
        self.assertEqual(host.locator('svg [data-mml-node="mphantom"]').count(), 1)
        self.assertEqual(host.locator('svg [data-mml-node="mphantom"] use').count(), 0)
        self.assertEqual(host.locator('mjx-assistive-mml mtext[mathcolor="red"]').count(), 0)

    def test_actual_ui_preserves_original_bottom_right_enclosure(self):
        fixture = json.loads((FIXTURES.parent / 'source-bottom-right-enclosure.json').read_text())
        self.assertEqual(hashlib.sha256(fixture['mathml'].encode()).hexdigest(), fixture['mathml_sha256'])
        source = self.extract(fixture['mathml'])['problem']
        self.assertIn(r'\enclose{bottom right}{-2}', source)
        host = self.ui_render(database_markdown(source))
        self.assertEqual(host.locator('mjx-assistive-mml menclose').get_attribute('notation'), 'bottom right')
        self.assertEqual(host.locator('svg [data-mml-node="menclose"]').count(), 1)
        self.assertEqual(host.locator('mjx-assistive-mml mtext[mathcolor="red"]').count(), 0)

    def test_actual_factorial_solution_renders_both_original_cancellations(self):
        fixture = json.loads((FIXTURES.parent / 'factorial-cancel-source.json').read_text())
        self.assertEqual(fixture['math_academy_id'], 'q-73014')
        source = fixture['worked_solution']
        self.assertEqual(hashlib.sha256(source.encode()).hexdigest(), fixture['text_sha256'])
        self.assertEqual(source.count(r'\cancel{8!}'), 2)
        host = self.ui_render(database_markdown(source))
        self.assertIn('/ui/vendor/mathjax/input/tex/extensions/cancel.js', self.requests)
        canceled = host.locator('mjx-assistive-mml menclose[notation="updiagonalstrike"]')
        self.assertEqual(canceled.count(), 2)
        self.assertEqual(canceled.all_text_contents(), ['8!', '8!'])
        self.assertEqual(host.locator('svg [data-mml-node="menclose"]').count(), 2)
        self.assertEqual(host.locator('mjx-assistive-mml mtext[mathcolor="red"]').count(), 0)
        self.assertIn('990', host.locator('mjx-assistive-mml').last.inner_text())
