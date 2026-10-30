"""The actual player must reject valid TeX with visibly undersized array fences."""
import importlib.util,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from question_capture.math_format import scalable_array_fences, scalable_table_fences
@unittest.skipUnless(importlib.util.find_spec('playwright'),'Playwright browser environment required')
class ArrayFenceGeometryTests(unittest.TestCase):
 def test_parser_success_is_not_array_layout_success(self):
  from check_math_rendering import check
  array=r'\begin{array}{cc|cc}1&0&1&0\\0&\frac{1}{12}&0&1\end{array}'
  bad=r'\begin{aligned}{}[N\mid I]&=['+array+r']&R_2:=12R_2\end{aligned}'
  good=scalable_array_fences(bad)
  result=check([{'entity':1,'value':'$$'+bad+'$$'},{'entity':2,'value':'$$'+good+'$$'}]);before,after=result['checks']
  self.assertEqual(before['errors'],[])
  self.assertEqual(after['errors'],[])
  self.assertTrue(before['matrix_layout_errors'])
  self.assertEqual(after['matrix_layout_errors'],[])
  self.assertEqual([x['entity']for x in result['failures']],[1])
  self.assertTrue(before['fence_geometry']);self.assertTrue(after['fence_geometry'])
  b=before['fence_geometry'][0];a=after['fence_geometry'][0]
  self.assertLess(min(b['fence_heights'])/b['table_height'],0.6)
  self.assertGreater(min(a['fence_heights'])/a['table_height'],0.8)
 def test_large_bracket_assembly_and_spaced_one_sided_brace(self):
  from check_math_rendering import check
  large=r'[\begin{array}{ccc|ccc}1&0&0&1&0&0\\0&1&3&0&1&0\\0&0&1&0&0&1\end{array}]'
  brace=r'\displaystyle \{\hspace{0.278em}\begin{aligned}\operatorname{Im}(T)&=R^8\\\operatorname{rank}(T)&=8\\\operatorname{Ker}(T)&=\{0\}\\\operatorname{nullity}(T)&=0\end{aligned}'
  result=check([{'entity':i,'value':'$$'+scalable_table_fences(v)+'$$'}for i,v in enumerate([large,brace])])
  self.assertTrue(result['passed'])
  for row in result['checks']:
   self.assertTrue(row['fence_geometry'])
   geometry=row['fence_geometry'][0]
   visible=[h for h in geometry['fence_heights']if h>1]
   self.assertTrue(visible)
   self.assertGreater(min(visible)/geometry['table_height'],0.8)
 def test_function_fence_is_checked_separately_from_the_correct_inner_matrix(self):
  from check_math_rendering import check
  bad=r'T(\begin{bmatrix}1\\2\\3\end{bmatrix})'
  result=check([{'entity':1,'value':'$$'+bad+'$$'},
                {'entity':2,'value':'$$'+scalable_table_fences(bad)+'$$'}])
  before,after=result['checks']
  ratios=lambda row:[min(h for h in g['fence_heights']if h>1)/g['table_height']
                    for g in row['fence_geometry']if g['table_height']>0 and any(h>1 for h in g['fence_heights'])]
  self.assertTrue(any(r<0.6 for r in ratios(before)))
  self.assertTrue(all(r>0.8 for r in ratios(after)))
  self.assertEqual(before['errors'],[])
  self.assertTrue(before['matrix_layout_errors'])
  self.assertEqual(after['matrix_layout_errors'],[])
if __name__=='__main__':unittest.main()
