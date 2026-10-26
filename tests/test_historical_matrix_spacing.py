import sys,unittest
from pathlib import Path
from bs4 import BeautifulSoup
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from import_historical_question_content import Renderer
class HistoricalMatrixTests(unittest.TestCase):
 def test_block_limit_keeps_operator_and_display_boundary(self):
  html='<math display="block"><munder><mo>lim</mo><mrow><mi>x</mi><mo>→</mo><mn>2</mn></mrow></munder><msup><mn>4</mn><mi>x</mi></msup></math>'
  result=Renderer(None).text(BeautifulSoup(html,'html.parser').math)
  self.assertEqual(result, '$$\n'+r'\lim_{x\to 2}{4}^{x}'+'\n$$')
 def test_determinant_keeps_four_separate_cells(self):
  html='<math><mo>|</mo><mtable><mtr><mtd><mn>5</mn></mtd><mtd><mo>−</mo><mn>9</mn></mtd></mtr><mtr><mtd><mo>−</mo><mn>3</mn></mtd><mtd><mn>7</mn></mtd></mtr></mtable><mo>|</mo><mo>=</mo></math>'
  result=Renderer(None).text(BeautifulSoup(html,'html.parser').math)
  self.assertEqual(result,r'$\begin{vmatrix}5 & -9 \\ -3 & 7\end{vmatrix}=$')
 def test_equation_alignment_remains_alignment(self):
  html='<math><mtable><mtr><mtd><mi>x</mi></mtd><mtd><mo>=</mo><mn>1</mn></mtd></mtr><mtr><mtd><mi>y</mi></mtd><mtd><mo>=</mo><mn>2</mn></mtd></mtr></mtable></math>'
  result=Renderer(None).text(BeautifulSoup(html,'html.parser').math)
  self.assertIn(r'\begin{aligned}',result);self.assertNotIn(r'\begin{vmatrix}',result)
if __name__=='__main__':unittest.main()
