import json,math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[6]/'scripts/question_capture'))
from solver import Solver
HERE=Path(__file__).parent
class MathematicalRecoveryTests(unittest.TestCase):
 def test_original_real_domain_invalid(self):
  item=json.loads((HERE/'original/q-128452-before.json').read_text())
  self.assertIn(r'\operatorname{ln}⁡(2t)',item['problem']);self.assertIn('t=-1',item['problem'])
  with self.assertRaises(ValueError):math.log(-2)
 def test_original_uncertainty_still_rejected(self):
  item=json.loads((HERE/'original/q-128452-before.json').read_text());answer=json.loads((HERE/'original/q-128452/solve-answer.json').read_text())
  with self.assertRaisesRegex(ValueError,'Solver is uncertain'):Solver.validate(item,answer)
 def test_exact_corrected_components(self):
  self.assertEqual(-8/math.sqrt(4)-(-3),-1)
  self.assertEqual(2*math.pi*math.cos(-math.pi)+2*math.pi,0)
  self.assertEqual(2/(-1)+2*(-1),-4)
 def test_local_corrected_log_derivative(self):
  def log_component(t):return 2*math.log(abs(2*t))-(1-t*t)
  h=1e-5
  self.assertAlmostEqual((log_component(-1+h)-log_component(-1-h))/(2*h),-4,places=8)
 def test_same_solver_session_preserved(self):
  old=json.loads((HERE/'original/solver-session/state.json').read_text());new=json.loads((HERE.parent/'solver-session/state.json').read_text())
  self.assertEqual(old['session_id'],new['session_id'])
 def test_source_expected_choice_is_separately_labeled(self):
  answer=json.loads((HERE.parent/'q-128452/source-error-review-answer.json').read_text())
  self.assertIn('undefined',answer['explanation']);self.assertIn('verified repair',answer['explanation'])
  self.assertEqual(answer['answers'][0]['correct_value'],'⟨-1,0,-4⟩')
if __name__=='__main__':unittest.main()
