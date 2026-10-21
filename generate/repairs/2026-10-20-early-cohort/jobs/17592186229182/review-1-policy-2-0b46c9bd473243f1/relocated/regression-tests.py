"""Strict retained review regressions against the current package.

Run: /home/jake/Developer/Course_Academy/.venv/bin/python regression-tests.py
No package writes, asset publication, or database operations.
"""
import pathlib,sys,importlib.util,json,unittest
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
P=E
spec=importlib.util.spec_from_file_location('gen',P/'17592186229182.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sys.path.insert(0,str(P/'checks'))
from validate_repair import key,score
import math_witness as w
class RepairAcceptance(unittest.TestCase):
 def test_positive_transient_is_eligible(self):
  # All three signs, including the exact reported positive counterexample.
  for level,ma in [('easy','q-336439'),('moderate','q-336746'),('hard','q-339403')]:
   for q in [9,12,15]:
    p=dict(V=240,q0=q,c='0.05',rin=16,rout=24) if level!='hard' else dict(V=240,q0=q,c='0.05',rin=8,rout=4,T=5)
    r=g.generate(level,619,template=ma,parameters=p)
    w.check_math(r);w.formatting(r)
    if level=='easy':self.assertEqual(key(r),str(q))
 def test_fractional_source_mass_is_eligible(self):
  r=g.generate('hard',619,template='q-339400',parameters=dict(V=320,q0=2.2,c='0.05',rin=8,rout=4,T=5))
  self.assertEqual(key(r),r'4.01\,\text{kg}');w.check_math(r)
  r=g.generate('moderate',619,template='q-336746',parameters=dict(V=240,q0=9,c='0.025',rin=16,rout=24))
  self.assertEqual(key(r),'3');w.check_math(r)
 def test_current_source_key_and_solution_replay(self):
  source=json.loads((P.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
  for q in source:
   ma=q[':question/math-academy-id'];m=g.M[ma]
   r=g.generate(m['level'],1943,template=ma,parameters=m['parameters'],profile='observed:'+ma)
   rq=r['question'];f=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
   for name in [':question/problem',':question/worked-solution',':question/requires-calculator']:self.assertEqual(rq.get(name),q.get(name),(ma,name))
   self.assertEqual(rq.get(':question/difficulty'),q.get(':question/difficulty',{}).get(':db/ident'))
   self.assertEqual(sorted(a[':answer/value'] for a in f[':answer-field/choices']),sorted(a[':answer/value'] for a in rf[':answer-field/choices']))
   self.assertEqual(':answer-field/correct' in f,':answer-field/correct' in rf)
   if ':answer-field/correct' in f:self.assertEqual(key(r),f[':answer-field/correct'][':answer/value'])
 def test_no_single_digit_rank_bypass(self):
  # Retain exact review controls, then require nonvacuous rank changes within the subgroup.
  rows=[]
  for q,c in [(3,'0.04'),(3,'0.05'),(4,'0.05')]:
   r=g.generate('easy',733,parameters=dict(V=100,q0=q,c=c,rin=8,rout=12));self.assertEqual(key(r),str(q));rows.append(score(r))
  natural=g.generate('easy',8114,parameters=dict(V=100,q0=3,c='.04',rin=8,rout=12));self.assertEqual(key(natural),'3')
  for q in range(3,10):
   for seed in range(8):
    r=g.generate('easy',seed,parameters=dict(V=100,q0=q,c='.04',rin=8,rout=12));self.assertEqual(key(r),str(q));rows.append(score(r))
  single=[x for x in rows if x['single_digit']]
  self.assertGreaterEqual(len(single),5)
  self.assertGreaterEqual(len({x['rank'] for x in single}),3)
  self.assertFalse(all(x['rank']==2 for x in single))
if __name__=='__main__':unittest.main(verbosity=2)
