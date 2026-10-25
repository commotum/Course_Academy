"""Regression gates for the demonstrated scaffolding/difficulty failures."""
import copy,json
from pathlib import Path
import unittest
from scripts.substitution_pedagogy_batch_policy import validate_delivery_batch,KPS
H=Path(__file__).resolve().parents[1]/'reference/edb-math/repairs/2026-10-25-restore-substitution-recognition'
def rows(kp):
 h=H.with_name('2026-10-25-inverse-bank-balance')if kp in(17592186064218,17592186064219,17592186064220,17592186064250)else H
 return json.loads((h/str(kp)/'accepted-pool.json').read_text())
class SubstitutionPedagogyPolicyTests(unittest.TestCase):
 def test_reviewed_delivered_pools_pass(self):
  for kp in KPS:validate_delivery_batch(rows(kp),kp)
 def test_routine_endpoint_values_belong_in_feedback(self):
  kp=17592186064220;r=rows(kp)[16]
  self.assertNotIn('Endpoint values:',r['question'][':question/problem'])
  self.assertIn('Endpoint values:',r['question'][':question/worked-solution'])
  r['question'][':question/problem']+='\n\nEndpoint values: $\\arcsin(1/2)=\\pi/6$.'
  with self.assertRaisesRegex(ValueError,'hints'):validate_delivery_batch([r],kp)
 def test_simple_logarithmic_derivative_is_not_a_complex_hard_case(self):
  kp=17592186184351;r=rows(kp)[16];r['generation']['family']='log_base'
  with self.assertRaisesRegex(ValueError,'Family'):validate_delivery_batch([r],kp)
 def test_fractional_numerator_composition_is_rejected(self):
  kp=17592186064218;r=rows(kp)[16];r['generation']['parameters']['numerator']='3/2'
  with self.assertRaisesRegex(ValueError,'fractional'):validate_delivery_batch([r],kp)
 def test_blanket_primitive_hints_are_rejected_and_final_key_is_required(self):
  kp=17592186184349;r=rows(kp)[8];r['question'][':question/problem']+='\n\nYou may use $\\int e^u\\,du=e^u+C$. '
  with self.assertRaises(ValueError):validate_delivery_batch([r],kp)
  r=rows(kp)[8];r['question'][':question/worked-solution']+='\n\n$$1$$'
  with self.assertRaisesRegex(ValueError,'key'):validate_delivery_batch([r],kp)
 def test_fixed_answer_bank_profile_is_rejected(self):
  kp=17592186064218;old=rows(kp)[:8]
  for r in old:r['generation']['bank_recipes']=['correct','wrong_sign','double_factor','omit_inner','double_inner']
  with self.assertRaisesRegex(ValueError,'profiles'):validate_delivery_batch(old,kp)
 def test_task_clones_are_rejected(self):
  kp=17592186184350;r=rows(kp)[0]
  with self.assertRaisesRegex(ValueError,'Duplicate'):validate_delivery_batch([r,copy.deepcopy(r)],kp)
if __name__=='__main__':unittest.main()
