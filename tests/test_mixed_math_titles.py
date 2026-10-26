"""A source formula's literal operators and partial MathML must stay together."""
import sys,unittest
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parents[1]/'reference/edb-math/repairs/2026-10-26-mixed-math-titles';sys.path.insert(0,str(H))
from reconstruct import reconstruct

def title(before,math,after):return BeautifulSoup('<title>'+before+'<mjx-container><mjx-assistive-mml><math>'+math+'</math></mjx-assistive-mml></mjx-container>'+after+'</title>','html.parser').title
class MixedTitleTests(unittest.TestCase):
 def test_full_determinant_rule_and_colors_survive(self):
  table='<mtable><mtr><mtd><mstyle mathcolor="blue"><mi>a</mi></mstyle></mtd><mtd><mi>b</mi></mtd></mtr><mtr><mtd><mi>c</mi></mtd><mtd><mi>d</mi></mtd></mtr></mtable>'
  value=reconstruct(title(r'\det(A)=\left|',table,r'\right|=ad-bc'))
  self.assertIn(r'\det(A)=\begin{vmatrix}',value);self.assertIn(r'{\color{blue}{a}}',value);self.assertTrue(value.endswith('=ad-bc'))
 def test_prefix_fraction_and_suffix_survive(self):
  value=reconstruct(title('x=', '<mfrac><mn>1</mn><mn>2</mn></mfrac>', '+C'))
  self.assertEqual(value,r'x=\frac{1}{2}+C')
 def test_all_fragments_and_literal_operators_survive(self):
  node=BeautifulSoup('<title>A=<mjx-container><mjx-assistive-mml><math><mi>x</mi></math></mjx-assistive-mml></mjx-container>+<mjx-container><mjx-assistive-mml><math><mi>y</mi></math></mjx-assistive-mml></mjx-container>=B</title>','html.parser').title
  self.assertEqual(reconstruct(node),'A=x+y=B')
 def test_phantom_and_explicit_space_are_not_silently_erased(self):
  value=reconstruct(title(r'\fbox{','<mphantom><mi>x</mi><mspace width="2em"/></mphantom>','}'))
  self.assertEqual(value,r'\fbox{\phantom{x\hspace{2em}}}')
 def test_unknown_structures_are_gaps(self):
  with self.assertRaises(ValueError):reconstruct(title('', '<mspace height="3em"/>','+x'))
  with self.assertRaises(ValueError):reconstruct(BeautifulSoup('<title>A=<span><math><mi>x</mi></math></span>+1</title>','html.parser').title)
if __name__=='__main__':unittest.main()
