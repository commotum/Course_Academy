"""Regression gates for the demonstrated scaffolding/difficulty failures."""
import copy,json
from pathlib import Path
import unittest
from scripts.substitution_pedagogy_batch_policy import validate_delivery_batch,KPS
H=Path(__file__).resolve().parents[1]/'reference/edb-math/repairs/2026-10-24-two-topic-pedagogy'
def rows(kp):return json.loads((H/str(kp)/'accepted-pool.json').read_text())
class SubstitutionPedagogyPolicyTests(unittest.TestCase):
 def test_reviewed_delivered_pools_pass(self):
  for kp in KPS:validate_delivery_batch(rows(kp),kp)
 def test_inverse_endpoint_support_cannot_be_hidden_in_feedback(self):
  kp=17592186064220;r=rows(kp)[16];r['question'][':question/problem']=r['question'][':question/problem'].replace('Endpoint values:','Recall:');r['generation']['provided_endpoint_values']=False
  with self.assertRaisesRegex(ValueError,'endpoint'):validate_delivery_batch([r],kp)
 def test_simple_logarithmic_derivative_is_not_a_complex_hard_case(self):
  kp=17592186184351;r=rows(kp)[16];r['generation']['family']='log_base'
  with self.assertRaisesRegex(ValueError,'Family'):validate_delivery_batch([r],kp)
 def test_fractional_numerator_composition_is_rejected(self):
  kp=17592186064218;r=rows(kp)[16];r['generation']['parameters']['numerator']='3/2'
  with self.assertRaisesRegex(ValueError,'fractional'):validate_delivery_batch([r],kp)
 def test_primitive_support_and_final_key_are_required(self):
  kp=17592186184349;r=rows(kp)[8];r['question'][':question/problem']=r['question'][':question/problem'].replace('You may use $','Recall $')
  with self.assertRaises(ValueError):validate_delivery_batch([r],kp)
  r=rows(kp)[8];r['question'][':question/worked-solution']+='\n\n$$1$$'
  with self.assertRaisesRegex(ValueError,'key'):validate_delivery_batch([r],kp)
 def test_task_clones_are_rejected(self):
  kp=17592186184350;r=rows(kp)[0]
  with self.assertRaisesRegex(ValueError,'Duplicate'):validate_delivery_batch([r,copy.deepcopy(r)],kp)
if __name__=='__main__':unittest.main()
