"""Strict regression tests for demonstrated defects. Both must pass on a repaired package.
Run with: /home/jake/Developer/Course_Academy/.venv/bin/python -B regression_tests.py
"""
import sys,json,unittest
sys.dont_write_bytecode=True
from review_generator import E,JOB,W,loadg,read
G=loadg(W/'17592186184219.py')
class GeneratorRegressions(unittest.TestCase):
 def test_all_current_source_banks_replay(self):
  qs=json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
  missing=[]
  for q in qs:
   d=read(q);p={k:d[k] for k in ('m','n','k','target')};matched=False
   for profile in G.PROFILES:
    if G.ORIGINAL[profile]['target']!=p['target']:continue
    try:r=G.generate('easy',template=p['target'],profile=profile,parameters=p)
    except ValueError:continue
    matched |= sorted(read(r)['values'])==sorted(d['values']) and read(r)['c']==d['c']
   if not matched:missing.append(q[':question/id'])
  self.assertEqual(missing,[],f'Complete current source banks unavailable: {missing}')
 def test_rank_consecutive_bank_does_not_fix_correct_role(self):
  rs=[G.generate('easy',seed=i,template='rank',profile='q-141220') for i in range(829001,829017)]
  matching=[]
  for r in rs:
   d=read(r);vs=sorted(d['values'])
   if all(b-a==1 for a,b in zip(vs,vs[1:])):matching.append(vs[-2]==d['c'])
  if matching:self.assertLess(sum(matching),len(matching),'Choose second-largest in consecutive rank banks bypasses the theorem for every tested instance')
if __name__=='__main__':unittest.main(verbosity=2)
