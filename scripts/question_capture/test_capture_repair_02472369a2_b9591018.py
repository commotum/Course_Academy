import json
import unittest
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from browser import click_select_option

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture-workers/linear/14095212/diagnostics/1791634412041756821/error.json')


class CoveredDropdownOptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.page = self.browser.new_page(viewport={'width':1280, 'height':720})
        self.page.route('**/*', lambda route: route.abort())
        self.page.set_default_timeout(300)
        # Offline reproduction of the recorded interception: a body-level
        # option overlaps another frame, which hides the menu on mousedown.
        self.page.set_content('''<style>
          #option {position:absolute;left:300px;top:250px;width:100px;height:60px;background:white;}
          #cover {position:absolute;left:330px;top:260px;width:40px;height:40px;z-index:2;background:gray;}
        </style>
        <div id="option"><span>intended</span></div>
        <div class="selectListFrame" id="cover"></div>
        <script>
          window.selected=null;
          document.getElementById('option').onclick=()=>window.selected='intended';
          document.getElementById('cover').onmousedown=()=>document.getElementById('option').style.display='none';
        </script>''')

    def tearDown(self):
        self.page.close()

    def test_saved_failure_reports_other_frame_interception(self):
        message = json.loads(EVIDENCE.read_text())['message']
        self.assertIn('selectListFrame-363837-8', message)
        self.assertIn('intercepts pointer events', message)
        self.assertIn('element is not visible', message)

    def test_original_center_click_fails(self):
        option = self.page.locator('#option').element_handle()
        with self.assertRaises(PlaywrightTimeout):
            option.click()
        self.assertIsNone(self.page.evaluate('window.selected'))

    def test_exposed_point_selects_exact_option(self):
        option = self.page.locator('#option').element_handle()
        click_select_option(option)
        self.assertEqual(self.page.evaluate('window.selected'), 'intended')

    def test_fully_covered_option_is_not_forced(self):
        self.page.locator('#cover').evaluate("n=>{n.style.left='300px';n.style.top='250px';n.style.width='100px';n.style.height='60px';}")
        with self.assertRaisesRegex(ValueError, 'no exposed click target'):
            click_select_option(self.page.locator('#option').element_handle())
        self.assertIsNone(self.page.evaluate('window.selected'))

    def test_hidden_option_is_rejected(self):
        self.page.locator('#option').evaluate("n=>n.style.display='none'")
        # Playwright may reject the hidden option while scrolling, before the
        # exposed-point check can raise its own error. Neither path may click.
        with self.assertRaises((ValueError, PlaywrightTimeout)) as rejected:
            click_select_option(self.page.locator('#option').element_handle())
        if isinstance(rejected.exception, ValueError):
            self.assertIn('no exposed click target', str(rejected.exception))
        self.assertIsNone(self.page.evaluate('window.selected'))


if __name__ == '__main__':
    unittest.main()
