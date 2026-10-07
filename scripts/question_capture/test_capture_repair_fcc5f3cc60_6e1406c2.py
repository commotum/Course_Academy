import re
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

EVIDENCE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14014428/diagnostics/1791397174128437310/page.html')
SOURCE = Path(__file__).with_name('dom.js')

class RightEnclosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        saved = EVIDENCE.read_text()
        matches = re.findall(r'<menclose notation="right"[^>]*>.*?</menclose>', saved, re.S)
        if len(matches) != 1:
            raise AssertionError('Expected exactly one saved right enclosure')
        cls.markup = matches[0]
        cls.extractor = SOURCE.read_text()
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

    def extract(self, markup):
        self.page.set_content('<div id="fixture"><div class="exampleExplanation"><math xmlns="http://www.w3.org/1998/Math/MathML">' + markup + '</math></div></div>', wait_until='domcontentloaded')
        return self.page.locator('#fixture').evaluate(self.extractor)

    def test_saved_border_and_complete_table(self):
        item = self.extract(self.markup)
        self.assertEqual(item['errors'], [])
        inner = re.sub(r'^<menclose[^>]*>|</menclose>$', '', self.markup)
        plain = self.extract(inner)
        self.assertEqual(plain['errors'], [])
        self.assertEqual(item['worked_solution'], '$' + r'\left.' + plain['worked_solution'][1:-1] + r'\right|' + '$')
        self.assertEqual(self.markup.count('<mtr>'), 3)
        self.assertEqual(self.markup.count('<mtd>'), 12)
        self.assertEqual(item['worked_solution'].count(' & '), 9)
        self.assertIn(r'\text{max}', item['worked_solution'])
        self.assertIn(r'\frac{1}{2}e', item['worked_solution'])

    def test_combined_enclosure_still_rejected(self):
        item = self.extract(self.markup.replace('notation="right"', 'notation="right radical"'))
        self.assertIn('Unsupported MathML enclosure', item['errors'])

    def test_unsupported_enclosure_still_rejected(self):
        item = self.extract(self.markup.replace('notation="right"', 'notation="radical"'))
        self.assertIn('Unsupported MathML enclosure', item['errors'])

if __name__ == '__main__':
    unittest.main()
