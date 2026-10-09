"""Saved q-38665 preserves opposite paired signs through DOM and comparison.

The native review's plain-minus diagnosis is contradicted by these authentic
captures. Unicode minus-plus is valid output; it need not serialize as TeX.
"""
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from playwright.sync_api import sync_playwright

from core import compare_answers, normalize
from edn import loads


EVIDENCE = Path(__file__).resolve().parents[2] / 'reference/mathacademy/question-capture-workers/linear/14071697'


class MinusPlusExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = Path(__file__).with_name('dom.js').read_text()
        cls.runtime = sync_playwright().start()
        cls.browser = cls.runtime.chromium.launch(headless=True)
        cls.context = cls.browser.new_context(java_script_enabled=False)
        cls.context.route('**/*', lambda route: route.abort())
        cls.page = cls.context.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.runtime.stop()

    def extract(self, markup):
        self.page.set_content('<div id="fixture">' + markup + '</div>')
        return self.page.locator('#fixture > *').evaluate(self.source)

    def test_authentic_widgets_and_history_keep_every_minus_plus(self):
        for name in ('q-38665-before.json', 'q-38665-after.json', 'history-q-38665.json'):
            with self.subTest(name=name):
                saved = json.loads((EVIDENCE / name).read_text())
                fresh = self.extract(saved['html'])
                self.assertEqual(fresh['errors'], [])
                self.assertEqual(fresh['problem'], saved['problem'])
                self.assertEqual(fresh['worked_solution'], saved['worked_solution'])
                self.assertEqual(fresh['result'], saved['result'])
                self.assertEqual(fresh['fields'], saved['fields'])
                if fresh['fields']:
                    choices = fresh['fields'][0]['choices']
                    self.assertEqual([c['value'].count('∓') for c in choices], [2, 2, 2, 1, 1])
                    self.assertTrue(all('<mo>∓</mo>' in c['html'] for c in choices))
                if fresh['worked_solution']:
                    self.assertEqual(fresh['worked_solution'].count('∓'), 2)

    def test_mathml_signs_have_distinct_extracted_values(self):
        item = self.extract('<div><div class="questionText"><math>'
                            '<mo>∓</mo><mn>2</mn><mo>±</mo><mn>3</mn><mo>−</mo><mn>4</mn>'
                            '</math></div></div>')
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['problem'], r'$∓2\pm 3-4$')

    def test_unicode_tex_and_wrong_sign_comparisons(self):
        saved = json.loads((EVIDENCE / 'q-38665-before.json').read_text())
        for choice in saved['fields'][0]['choices']:
            original = choice['value']
            tex = original.replace('∓', r'\mp ')
            with self.subTest(option=choice['option']), patch('native_comparison.compare') as native:
                self.assertEqual(normalize(original, 'text'), normalize(tex, 'text'))
                self.assertEqual(compare_answers(original, tex, 'text'), {'outcome': 'equivalent'})
                for other in ('-', '−', '±', r'\pm '):
                    changed = original.replace('∓', other)
                    self.assertNotEqual(normalize(original, 'text'), normalize(changed, 'text'))
                    self.assertEqual(compare_answers(original, changed, 'text'), {'outcome': 'different'})
                native.assert_not_called()

    def test_saved_database_snapshots_preserve_signs(self):
        for name in ('questions.edn', 'questions-after.edn'):
            with self.subTest(name=name):
                rows = loads((EVIDENCE / 'edb-import' / name).read_text())
                matches = [row[0] for row in rows if row[0].get(':question/math-academy-id') == 'q-38665']
                self.assertEqual(len(matches), 1)
                field = matches[0][':question/answer-fields'][0]
                correct = field[':answer-field/correct'][':answer/value']
                self.assertEqual(correct.count('∓') + correct.count(r'\mp'), 2)
                self.assertEqual(sorted(v[':answer/value'].count('∓') + v[':answer/value'].count(r'\mp')
                                        for v in field[':answer-field/choices']), [1, 1, 2, 2, 2])


if __name__ == '__main__':
    unittest.main()
