import json
import os
import re
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

SOURCE = Path(os.environ.get('ENCLOSURE_TEST_SOURCE', Path(__file__).with_name('dom.js')))
EVIDENCE = Path(__file__).resolve().parents[2] / 'reference/mathacademy/question-capture/14065202/diagnostics/1791504810858543233/current-question.json'
ADDED = "        // The two borders group the synthetic-division root; retain both.\n        if (n.getAttribute('notation') === 'bottom right') return '\\\\enclose{bottom right}{' + cs.join('') + '}';\n"

class SyntheticDivisionEnclosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved = json.loads(EVIDENCE.read_text())
        cls.source = SOURCE.read_text()
        cls.markups = re.findall(r'<menclose\b[^>]*>.*?</menclose>', cls.saved['html'], re.S)
        assert cls.markups == ['<menclose notation="bottom right"><mn>5</mn></menclose>']
        cls.runtime = sync_playwright().start()
        cls.browser = cls.runtime.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
        cls.context.route('**/*', lambda route: route.abort())
        cls.page = cls.context.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.context.close(); cls.browser.close(); cls.runtime.stop()

    def extract(self, markup, source=None):
        self.page.set_content('<div id="fixture"><div class="exampleExplanation"><math>' + markup + '</math></div></div>')
        return self.page.locator('#fixture').evaluate(source or self.source)

    def test_original_saved_failure_reproduces(self):
        self.assertEqual(self.saved['result'], 'Correct')
        self.assertIn('Unsupported MathML enclosure', self.saved['errors'])
        self.assertIn('Unsupported MathML enclosure', self.extract(self.markups[0], self.source.replace(ADDED, ''))['errors'])

    def test_preserves_both_borders_and_root(self):
        item = self.extract(self.markups[0])
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['worked_solution'], r'$\enclose{bottom right}{5}$')
        self.assertNotEqual(item['worked_solution'], self.extract('<mn>5</mn>')['worked_solution'])

    def test_complete_original_graded_widget(self):
        self.page.set_content('<div id="fixture">' + self.saved['html'] + '</div>')
        item = self.page.locator('#fixture').evaluate(self.source)
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['result'], 'Correct')
        self.assertEqual(item['fields'], self.saved['fields'])
        self.assertEqual(item['problem'], self.saved['problem'])
        self.assertIn(r'\enclose{bottom right}{5}', item['worked_solution'])
        self.assertIn(r'\begin{aligned}', item['worked_solution'])

    def test_unknown_variants_still_fail(self):
        for notation in ('bottom', 'right bottom', 'bottom right radical', 'unknown', ''):
            with self.subTest(notation=notation):
                item = self.extract(self.markups[0].replace('bottom right', notation))
                self.assertEqual(item['errors'], ['Unsupported MathML enclosure'])

if __name__ == '__main__':
    unittest.main()
