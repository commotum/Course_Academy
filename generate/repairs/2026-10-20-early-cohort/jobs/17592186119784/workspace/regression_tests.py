#!/usr/bin/env python3
"""Strict acceptance regressions: current generator is expected to FAIL these.
Run: <job-python> -B regression_tests.py
No package edits, assets, or DB calls; imports suppress bytecode writes.
"""
import sys,pathlib,importlib.util,unittest
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;P=R
sys.path.insert(0,str(P))
spec=importlib.util.spec_from_file_location('generator_under_test',P/'17592186119784.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def values(r):
 out=[]
 for f in r['question'][':question/answer-fields']:
  aid=f[':answer-field/correct'][1]
  out.append(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid))
 return out
class AcceptanceRegressions(unittest.TestCase):
 def test_relevant_entry_can_change_decision(self):
  # Source lesson explicitly allows zeros on both sides; diagonal is both.
  before=g.generate('moderate',101,template='q-42091',parameters={'matrix':[[4,0,0],[1,1,0],[0,0,3]]})
  after=g.generate('moderate',101,template='q-42091',parameters={'matrix':[[4,0,0],[0,1,0],[0,0,3]]})
  self.assertEqual(values(before)[:3],['false','true','true'])
  self.assertEqual(values(after)[:3],['true','true','true'])
  self.assertIn('**true**',after['question'][':question/worked-solution'])
 def test_source_q126481_supported(self):
  r=g.generate('moderate',101,template='q-126481',parameters={'matrix':[[1,0,0,0],[0,2,0,0],[1,1,3,0],[1,1,0,4]]})
  self.assertEqual(sum(f[':answer-field/key']!='None of the above' for f in r['question'][':question/answer-fields']),3)
 def test_source_q126474_supported(self):
  r=g.generate('hard',101,template='q-126474',parameters={'matrix':[[-1,0,-5],[0,2,2],[5,-2,-4]]})
  self.assertTrue(any('+' in f[':answer-field/key'] for f in r['question'][':question/answer-fields']))
if __name__=='__main__': unittest.main(verbosity=2)
