"""The saved intersection-of-planes example retains its determinant bars."""
import json
import re
import unittest
from pathlib import Path

import test_capture_repair_fcc5f3cc60_4ded94b8 as determinant_fixture

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'reference/mathacademy/question-capture-workers/multivariable/14040648/diagnostics/1791440466042975273/current-question.json'


class IntersectionDeterminantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved = json.loads(EVIDENCE.read_text())
        matches = re.findall(r'<menclose\b[^>]*>.*?</menclose>', cls.saved['html'], re.S)
        if len(matches) != 1:
            raise AssertionError('Expected the single determinant in step-e5920')
        cls.markup = matches[0]
        cls.source = Path(__file__).with_name('dom.js').read_text()

    def render(self, markup, source=None):
        renderer = determinant_fixture.DeterminantEnclosureTests()
        renderer.source = self.source
        return renderer.render(markup, source)

    def test_saved_failure_reproduces_with_original_renderer(self):
        self.assertIn(determinant_fixture.ADDED, self.source)
        item = self.render(self.markup, self.source.replace(determinant_fixture.ADDED, ''))
        self.assertEqual(item['errors'], ['Unsupported MathML enclosure'])
        self.assertNotIn(r'\left|', item['value'])
        self.assertEqual(self.saved['dom_id'], 'step-e5920')

    def test_direction_determinant_preserves_rows_signs_and_bars(self):
        item = self.render(self.markup)
        self.assertEqual(item['errors'], [])
        self.assertEqual(item['value'].replace(r'\,', ''),
                         r'\left|\begin{aligned}i & j & k \\ 2 & 4 & 0 \\ 0 & 3 & -2\end{aligned}\right|')
        # The worked source independently identifies both normal vectors and
        # the result. Retain the source evidence rather than recomputing it.
        for value in (r'\langle 2,4,0 \rangle', r'\langle 0,3,-2 \rangle', '-8i+4j+6k'):
            self.assertIn(value, self.saved['worked_solution'])

    def test_unrecognized_additional_enclosures_still_defer(self):
        for notation in ('left', 'left right radical', 'radical'):
            with self.subTest(notation=notation):
                item = self.render(self.markup.replace('notation="left right"', 'notation="' + notation + '"'))
                self.assertEqual(item['errors'], ['Unsupported MathML enclosure'])


if __name__ == '__main__':
    unittest.main()
