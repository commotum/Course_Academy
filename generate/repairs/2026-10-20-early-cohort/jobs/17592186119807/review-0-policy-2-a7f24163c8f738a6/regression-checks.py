import sys,json,pathlib
sys.dont_write_bytecode=True
import audit as a
import unittest
class RequiredCases(unittest.TestCase):
 def test_all_source_profiles(self):
  for q in a.source['material']['kp'][':knowledge-point/questions']:
   with self.subTest(source=q[':question/math-academy-id']):
    self.assertEqual(a.truth(a.g.generate('moderate',83,q[':question/math-academy-id'],{'translation':0})),q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])
 def test_consistency_role_can_change(self):
  target=[a.sp.Matrix([-1,3,5]),a.sp.Matrix([4,1,2]),a.sp.Matrix([3,4,7])]
  self.assertTrue(any('{c}_{1}' in r['question'][':question/problem'] and a.truth(r)!='No solution' for r in a.g.catalog()),'Every c/d-labelled family fixes No solution; source-grounded consistency flip (3,4,5) -> (3,4,7) demonstrates an eligible role reassignment')
 def test_actual_batch_has_counterexample_to_second_largest(self):
  rs=a.load(a.E/'batch.json')
  self.assertTrue(any(a.key(r)!=str(sorted(a.sp.Rational(o[':answer/value']) for o in a.choices(r) if o[':answer/type']==':answer.type/math')[-2]) for r in rs),'Every exact batch item is answered by second-largest numeric choice')
if __name__=='__main__':unittest.main()
