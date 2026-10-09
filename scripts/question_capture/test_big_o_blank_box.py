"""Actual Big-O example preserves visible boxes around nested phantom titles."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from playwright.sync_api import sync_playwright
from browser import CaptureBrowser, EXTRACT

FIXTURE=Path(__file__).parent/'fixtures/big-o-blank-box/example-21715.html'

class BigOBlankBoxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pw=sync_playwright().start();cls.browser=cls.pw.chromium.launch(headless=True)
    @classmethod
    def tearDownClass(cls):
        cls.browser.close();cls.pw.stop()
    def setUp(self):
        self.page=self.browser.new_page();self.page.route('**/*',lambda r:r.abort())
    def tearDown(self):self.page.close()
    def test_saved_example_preserves_visible_blank_boxes_and_source_solution(self):
        self.page.set_content(FIXTURE.read_text())
        scope=self.page.locator('#step-e21715')
        item=scope.evaluate(EXTRACT)
        self.assertEqual(item['errors'],[])
        self.assertEqual(len(item['assets']),4)
        self.assertEqual(item['problem'].count('![](@asset-'),4)
        self.assertNotIn('XXXX',item['problem'])
        self.assertIn(r'e^{x} = \mathcal O(1)',item['problem'])
        # These are actual source mistakes. Capture must retain them for review.
        self.assertIn('L1 and L3',item['worked_solution'])
        self.assertIn(r'\text{L4}',item['worked_solution'])
        reader=CaptureBrowser(self.page,SimpleNamespace(timeout_ms=3000),None,None)
        with tempfile.TemporaryDirectory() as work:
            saved,_=reader.read(scope,work,'example-21715')
            self.assertEqual(saved['errors'],[])
            self.assertEqual(len(saved['assets']),4)
            self.assertTrue(all(Path(a['path']).is_file() for a in saved['assets']))
            self.assertTrue(all(Path(a['original_svg_path']).read_text()==a['html'] for a in saved['assets']))
            self.assertNotIn('@asset-',saved['problem'])
    def test_mathml_phantom_spacer_remains_invisible(self):
        self.page.set_content('<div id="test"><div class="exampleQuestion">'
            '<mjx-container><mjx-assistive-mml><math><mrow><mi>x</mi><mphantom>'
            '<mi>X</mi><mi>X</mi></mphantom><mo>+</mo><mn>1</mn></mrow></math>'
            '</mjx-assistive-mml></mjx-container></div></div>')
        item=self.page.locator('#test').evaluate(EXTRACT)
        self.assertEqual(item['errors'],[])
        self.assertEqual(item['problem'],'$x+1$')
        self.assertEqual(item['assets'],[])
