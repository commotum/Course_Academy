"""SVG arrow shafts are drawing parts, never extra minus operators."""
import importlib.util
from pathlib import Path
import unittest

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
RECOVERY = ROOT / 'reference/edb-math/repairs/2026-10-22-math-images'
spec = importlib.util.spec_from_file_location('vector_reconstruction', RECOVERY / 'reconstruct.py')
reconstruction = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reconstruction)


class VectorArrowTests(unittest.TestCase):
    def test_saved_source_recovers_one_wide_arrow(self):
        soup = BeautifulSoup((Path(__file__).parent / 'fixtures/stretched-vector-arrow.svg').read_text(), 'html.parser')
        math = reconstruction.node(soup.find(attrs={'data-mml-node': 'math'}), soup)
        self.assertEqual(reconstruction.conv.mathml(str(math)), r'\overrightarrow{A X}')

    def test_separate_arrow_and_minus_remain_separate(self):
        soup = BeautifulSoup('<g data-mml-node="mo"><path data-c="2192"></path><path data-c="2212"></path></g>', 'html.parser')
        self.assertEqual(reconstruction.glyphs(soup.g), '→−')

    def test_real_subtraction_below_arrow_is_preserved(self):
        soup = BeautifulSoup((Path(__file__).parent / 'fixtures/stretched-vector-arrow.svg').read_text(), 'html.parser')
        base = soup.find(attrs={'data-mml-node': 'mrow'})
        minus = BeautifulSoup('<g data-mml-node="mo"><path data-c="2212"></path></g>', 'html.parser').g
        base.insert(1, minus)
        math = reconstruction.node(soup.find(attrs={'data-mml-node': 'math'}), soup)
        self.assertEqual(reconstruction.conv.mathml(str(math)), r'\overrightarrow{A - X}')


if __name__ == '__main__':
    unittest.main()
