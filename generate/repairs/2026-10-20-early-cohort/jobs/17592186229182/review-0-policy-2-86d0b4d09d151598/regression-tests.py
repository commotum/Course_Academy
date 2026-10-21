"""Strict repair acceptance tests. Current package is expected to FAIL.

Run: /home/jake/Developer/Course_Academy/.venv/bin/python regression-tests.py
No package writes, asset publication, or database operations.
"""
import pathlib,sys,importlib.util,json,unittest
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
P=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186229182/workspace')
spec=importlib.util.spec_from_file_location('gen',P/'17592186229182.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class RepairAcceptance(unittest.TestCase):
 def test_positive_transient_is_eligible(self):
  # Easy target still alpha+beta=15. cV=12 gives beta=+3, no new method.
  r=g.generate('easy',619,parameters=dict(V=240,q0=15,c='0.05',rin=16,rout=24))
  self.assertIn('15',r['question'][':question/worked-solution'])
 def test_fractional_source_mass_is_eligible(self):
  # Source d0340e70-b947-5b25-8e24-a63ff0f87f38, Q(5)=341/85=4.01 kg.
  r=g.generate('hard',619,template='q-339400',parameters=dict(V=320,q0='2.2',c='0.05',rin=8,rout=4,T=5))
  self.assertIn('4.01',r['question'][':question/worked-solution'])
 def test_current_source_key_and_solution_replay(self):
  m=g.M['q-336738'];r=g.generate('hard',1943,template='q-336738',parameters=m['parameters'],profile='observed:q-336738')['question']
  self.assertIn(':answer-field/correct',r[':question/answer-fields'][0])
  self.assertIn(':question/worked-solution',r)
  self.assertEqual(r[':question/difficulty'],':question.difficulty/hard')
 def test_no_single_digit_rank_bypass(self):
  rows=[]
  for q,c in [(3,'0.04'),(3,'0.05'),(4,'0.05')]:
   r=g.generate('easy',733,parameters=dict(V=100,q0=q,c=c,rin=8,rout=12));f=r['question'][':question/answer-fields'][0]
   choices=f[':answer-field/choices'];correct=next(int(a[':answer/value']) for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);vals=sorted(int(a[':answer/value']) for a in choices)
   if all(0<v<10 for v in vals):rows.append(vals[1]==correct)
  self.assertFalse(rows and all(rows),'All eligible one-digit cases are solved by choosing second-smallest without reading the model')
if __name__=='__main__':unittest.main(verbosity=2)
