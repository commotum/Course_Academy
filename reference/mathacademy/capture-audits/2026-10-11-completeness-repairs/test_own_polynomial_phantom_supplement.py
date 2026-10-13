from copy import deepcopy
from pathlib import Path
import json,unittest
from playwright.sync_api import sync_playwright
from literal_brace_source_supplement import refresh_own_polynomial_phantom
ROOT=Path(__file__).resolve().parent
class OwnPolynomialPhantom(unittest.TestCase):
 def test_exact_original_external_source_restores_only_its_hidden_width(self):
  content=json.loads((ROOT.parents[1]/'capture/linear/14120023/content.json').read_text())
  original=next(q for q in content['questions'] if q['math_academy_id']=='q-114506')
  with sync_playwright() as pw:
   browser=pw.chromium.launch(headless=True);context=browser.new_context();context.route('**/*',lambda route:route.abort());page=context.new_page()
   current,certificate=refresh_own_polynomial_phantom(original,deepcopy(original),page,ROOT/'literal-brace-local-tests')
   self.assertIsNotNone(certificate);self.assertFalse(certificate['grade_transfer'])
   self.assertEqual(current['answer_fields'],original['answer_fields'])
   self.assertEqual(current['problem'],original['problem'])
   self.assertEqual(current['worked_solution'],original['worked_solution'].replace(certificate['exact_original_longdiv_span'],certificate['exact_restored_longdiv_span']))
   forged=deepcopy(original);forged['math_academy_id']='q-114507'
   self.assertIsNone(refresh_own_polynomial_phantom(forged,deepcopy(forged),page,ROOT/'literal-brace-local-tests')[1])
   forged=deepcopy(original);forged['worked_solution']=forged['worked_solution'].replace('x+6','x+7')
   self.assertIsNone(refresh_own_polynomial_phantom(forged,deepcopy(forged),page,ROOT/'literal-brace-local-tests')[1])
   browser.close()
if __name__=='__main__':unittest.main()
