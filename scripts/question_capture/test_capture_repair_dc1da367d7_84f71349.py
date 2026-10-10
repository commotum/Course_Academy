import ast
import unittest
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from browser import click_select_option

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/linear/14095701/diagnostics/1791636822186365570/page.html')

class OffscreenDropdownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        soup = BeautifulSoup(EVIDENCE.read_text(), 'html.parser')
        menus = [m for m in soup.select('.selectListOptions') if 'visibility: visible' in m.get('style', '')]
        self.assertEqual(len(menus), 1)
        menu = menus[0]
        self.assertIn('top: 651px', menu['style'])
        options = menu.select(':scope > .selectListOption')
        self.assertEqual(len(options), 5)
        self.assertTrue(all('height: 55px' in o['style'] for o in options))
        # Preserve captured choices and menu geometry; supply local rendering
        # dimensions because the saved MathJax CSS is an external asset.
        markup = ''.join('<div class="selectListOption" style="height:55px">' + str(o) + '</div>' for o in options)
        self.page = self.browser.new_page(viewport={'width':1280, 'height':720})
        self.page.route('**/*', lambda route: route.abort())
        self.page.set_default_timeout(500)
        self.page.set_content('<style>body{height:1800px;margin:0}#menu{position:absolute;left:511px;top:651px;width:116px;background:white}.selectListOption{box-sizing:border-box}#cover{display:none;position:fixed;inset:0;z-index:2000;background:white}</style><div id="menu">' + markup + '</div><div id="cover"></div>')
        self.page.evaluate('''() => {
            window.selected = null;
            document.querySelectorAll('#menu > .selectListOption').forEach((o,i) => o.onclick = () => window.selected = i);
        }''')
        self.option = self.page.query_selector_all('#menu > .selectListOption')[3]

    def tearDown(self):
        self.page.close()

    def test_original_helper_rejects_captured_offscreen_option(self):
        import browser
        source = Path(browser.__file__).read_text()
        node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'click_select_option')
        original = ast.get_source_segment(source, node).replace('    option.scroll_into_view_if_needed()\n', '', 1)
        namespace = {}
        exec(original, namespace)
        self.assertGreater(self.option.bounding_box()['y'], 720)
        with self.assertRaisesRegex(ValueError, 'no exposed click target'):
            namespace['click_select_option'](self.option)
        self.assertIsNone(self.page.evaluate('window.selected'))

    def test_scroll_then_hit_test_selects_exact_fourth_option(self):
        click_select_option(self.option)
        self.assertEqual(self.page.evaluate('window.selected'), 3)

    def test_scrolling_does_not_authorize_click_through_overlay(self):
        self.page.locator('#cover').evaluate("n => n.style.display = 'block'")
        with self.assertRaisesRegex(ValueError, 'no exposed click target'):
            click_select_option(self.option)
        self.assertIsNone(self.page.evaluate('window.selected'))

if __name__ == '__main__':
    unittest.main()
