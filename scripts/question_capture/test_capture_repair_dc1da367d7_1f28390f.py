import ast
import unittest
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import browser
from browser import click_select_frame, click_select_option

ROOT = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/linear/14095701/diagnostics')
CENTER = "    frame.evaluate(\"n => n.scrollIntoView({block:'center', inline:'nearest', behavior:'instant'})\")\n"

class ClosingMenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        before = BeautifulSoup((ROOT/'1791636822186365570/page.html').read_text(), 'html.parser')
        after = BeautifulSoup((ROOT/'1791637011965868141/page.html').read_text(), 'html.parser')
        menus = [m for m in before.select('.selectListOptions') if 'visibility: visible' in m.get('style','')]
        self.assertEqual(len(menus), 1)
        self.assertIn('top: 651px', menus[0]['style'])
        self.assertFalse(any('visibility: visible' in m.get('style','') for m in after.select('.selectListOptions')))
        options = menus[0].select(':scope > .selectListOption')
        self.assertEqual(len(options), 5)
        self.assertTrue(all('height: 55px' in o['style'] for o in options))
        # Local geometry and scroll-closure reproduction; never execute saved scripts.
        markup = ''.join('<div class="option">'+str(o)+'</div>' for o in options)
        self.page = self.browser.new_page(viewport={'width':1280,'height':720})
        self.page.route('**/*', lambda route: route.abort())
        self.page.set_default_timeout(500)
        self.page.set_content('''<style>
        body{height:1800px;margin:0}#frame{position:absolute;left:511px;top:586px;width:116px;height:65px;background:white}
        #menu{position:absolute;left:511px;top:651px;width:116px;visibility:hidden;background:white}
        .option{height:55px;box-sizing:border-box}#cover{display:none;position:fixed;inset:0;z-index:2000;background:white}
        </style><div id="frame"></div><div id="menu">'''+markup+'''</div><div id="cover"></div>
        <script>
        window.selected=null;
        const menu=document.getElementById('menu');
        window.addEventListener('scroll',()=>menu.style.visibility='hidden');
        document.getElementById('frame').onclick=()=>menu.style.visibility='visible';
        document.querySelectorAll('#menu > .option').forEach((o,i)=>o.onclick=()=>window.selected=i);
        </script>''')
        self.frame = self.page.locator('#frame')
        self.option = self.page.query_selector_all('#menu > .option')[3]

    def tearDown(self):
        self.page.close()

    def test_original_option_scroll_closes_menu(self):
        source = Path(browser.__file__).read_text()
        node = next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='click_select_frame')
        namespace = {}
        exec(ast.get_source_segment(source,node).replace(CENTER,'',1),namespace)
        namespace['click_select_frame'](self.frame)
        # Scroll events may hide the menu before hit testing or before the
        # subsequent actionable click. Both must stop without selecting.
        with self.assertRaises((ValueError, PlaywrightTimeout)):
            click_select_option(self.option)
        self.assertIsNone(self.page.evaluate('window.selected'))
        self.assertEqual(self.page.locator('#menu').evaluate("n=>getComputedStyle(n).visibility"),'hidden')

    def test_position_before_open_selects_exact_option(self):
        click_select_frame(self.frame)
        click_select_option(self.option)
        self.assertEqual(self.page.evaluate('window.selected'),3)

    def test_covered_option_still_rejected(self):
        click_select_frame(self.frame)
        self.page.locator('#cover').evaluate("n=>n.style.display='block'")
        with self.assertRaisesRegex(ValueError,'no exposed click target'):
            click_select_option(self.option)
        self.assertIsNone(self.page.evaluate('window.selected'))

    def test_hidden_menu_still_rejected(self):
        click_select_frame(self.frame)
        self.page.locator('#menu').evaluate("n=>n.style.visibility='hidden'")
        with self.assertRaisesRegex(ValueError,'no exposed click target'):
            click_select_option(self.option)
        self.assertIsNone(self.page.evaluate('window.selected'))

if __name__=='__main__':
    unittest.main()
