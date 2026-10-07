import unittest
from pathlib import Path

from browser import EXTRACT
from playwright.sync_api import sync_playwright

PAGE = Path('/home/jake/Developer/Course_Academy/reference/mathacademy/question-capture/14004890/diagnostics/1791336566359855137/page.html')

class NestedSignTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runtime = sync_playwright().start()
        cls.browser = cls.runtime.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
        cls.context.route('**/*', lambda route: route.abort())
        cls.page = cls.context.new_page()
        cls.html = PAGE.read_text()

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.runtime.stop()

    def setUp(self):
        self.page.set_content(self.html, wait_until='domcontentloaded')
        self.scope = self.page.locator('#step-q121237')

    def test_saved_nested_tables_are_five_complete_choices(self):
        try:
            item = self.scope.evaluate(EXTRACT)
        except Exception as exc:
            self.fail('Saved sign-table extraction failed: ' + str(exc))
        self.assertEqual(item['errors'], [])
        field = next(f for f in item['fields'] if f['key'] == 'selection')
        self.assertEqual([c['option'] for c in field['choices']], list('abcde'))
        self.assertTrue(field['choices_complete'])
        for choice in field['choices']:
            original = self.scope.locator('#' + choice['dom_id']).locator('xpath=ancestor::tr[1]').locator('.questionWidget-choiceText')
            self.assertEqual(choice['html'], original.inner_html())
            self.assertEqual(original.locator('table tr').count(), 2)
            self.assertEqual(original.locator('table td').count(), 4)
            self.assertTrue(choice['value'])
        self.assertEqual(len({c['value'] for c in field['choices']}), 5)

    def test_missing_choice_circle_still_invalidates_extraction(self):
        self.scope.locator('.questionWidget-choiceLetterCircle').first.evaluate('n => n.remove()')
        item = self.scope.evaluate(EXTRACT)
        self.assertIn('Choice circle has no observed ID', item['errors'])
        field = next(f for f in item['fields'] if f['key'] == 'selection')
        self.assertEqual(len(field['choices']), 5)
        self.assertFalse(field['choices_complete'])

if __name__ == '__main__':
    unittest.main()
