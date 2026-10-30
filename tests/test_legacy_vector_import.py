"""The retained MA lesson importer must preserve vector fonts and accents."""
import importlib.util
import os
from pathlib import Path
import sys
import unittest

from bs4 import BeautifulSoup

PIPELINE = Path(__file__).resolve().parents[2] / 'MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py'
SOURCE = Path(os.environ.get('VECTOR_IMPORT_TEST_SOURCE', PIPELINE))


@unittest.skipUnless(SOURCE.exists(), 'Sibling MA capture pipeline is unavailable')
class LegacyVectorImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('legacy_vector_import_test', PIPELINE)
        cls.module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = cls.module
        # The importer locates its repository from __file__. A staged source
        # override tests the exact patch without modifying the sibling repo.
        exec(compile(SOURCE.read_text(), str(PIPELINE), 'exec'), vars(cls.module))

    def render(self, markup):
        return self.module.mathml_to_text(BeautifulSoup(markup, 'html.parser').find())

    def test_vector_font_preserves_scalar_parameter(self):
        self.assertEqual(self.render('<math><mi mathvariant="bold">r</mi><mo>=</mo><mi>t</mi>'
                                     '<mi mathvariant="bold">v</mi></math>'), r'\mathbf{r} = t\mathbf{v}')
        self.assertEqual(self.render('<mi>v</mi>'), 'v')

    def test_accents_on_operator_and_parent_preserve_whole_base(self):
        for parent, operator in [('', 'accent="true"'), ('accent="true"', ''), ('', '')]:
            for mark, command in [('→', 'overrightarrow'), ('―', 'overline'), ('↔', 'overleftrightarrow')]:
                with self.subTest(parent=parent, operator=operator, mark=mark):
                    self.assertEqual(self.render(f'<mover {parent}><mrow><mi>P</mi><mi>Q</mi></mrow>'
                                                 f'<mo {operator}>{mark}</mo></mover>'), '\\' + command + '{PQ}')

    def test_short_vector_arrow_stays_short(self):
        self.assertEqual(self.render('<mover><mi>v</mi><mo stretchy="false">→</mo></mover>'), r'\vec{v}')

    def test_scalar_minus_sign_and_grouped_exponent_are_unchanged(self):
        self.assertEqual(self.render('<math><mi>a</mi><mo>−</mo><mi>b</mi></math>'), 'a − b')
        self.assertEqual(self.render('<msup><mi>x</mi><mrow><mi>n</mi><mo>+</mo><mn>1</mn></mrow></msup>'), 'x^{n + 1}')


if __name__ == '__main__':
    unittest.main()
