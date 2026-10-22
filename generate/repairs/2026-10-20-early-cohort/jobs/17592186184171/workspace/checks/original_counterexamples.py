#!/usr/bin/env python3
"""Exact retained inputs plus same-bank counterfactual for the repaired rule."""
import json,pathlib,importlib.util,sys,argparse
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('case',choices=['shortcut','source']);parser.add_argument('--package',type=pathlib.Path,default=E.parent);a=parser.parse_args()
sys.path.insert(0,str(a.package));spec=importlib.util.spec_from_file_location('candidate',a.package/'17592186184171.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
if a.case=='shortcut':
 r=g.generate('easy',seed=63271,profile='offset-minus2',parameters={'m':2,'n':4,'k':2})
 (E/'minimal-shortcut-record.json').write_text(json.dumps([r],indent=2)+'\n')
 f=r['question'][':question/answer-fields'][0];vs=sorted(int(c[':answer/value']) for c in f[':answer-field/choices']);actual=next(int(c[':answer/value']) for c in f[':answer-field/choices']if c[':answer/id']==f[':answer-field/correct'][1])
 print(json.dumps({'values':vs,'actual':actual,'bank_only_prediction':vs[1]}))
 other=g.generate('easy',seed=63271,profile='offset-minus2',parameters={'m':2,'n':4,'k':1},bank_anchor=0)
 of=other['question'][':question/answer-fields'][0]
 ov=sorted(int(c[':answer/value']) for c in of[':answer-field/choices'])
 oa=next(int(c[':answer/value']) for c in of[':answer-field/choices'] if c[':answer/id']==of[':answer-field/correct'][1])
 assert vs==ov and actual==4-2 and oa==4-1 and actual!=oa
 print(json.dumps({'counterfactual_values':ov,'counterfactual_actual':oa,'old_bank_rule_fails':oa!=ov[1]}))

else:
 p={'matrix':[[1,0],[0,0],[1,1],[0,0],[0,0]],'indices':[1,2]}
 try:r=g.generate('moderate',seed=63271,profile='one-through5',parameters=p)
 except Exception as ex:
  (E/'minimal-source-rejection.json').write_text(json.dumps({'source_id':'5e7c8be1-d271-506d-bfc9-fbf1881a88d8','parameters':p,'profile':'one-through5','expected':{'correct':3,'bank':[1,2,3,4,5]},'error':repr(ex)},indent=2)+'\n')
  raise AssertionError('Supplied q-142489 must replay: five-component null-space vector in x1,x2, rank 3, complete bank 1..5.') from ex
 (E/'minimal-source-record.json').write_text(json.dumps([r],indent=2)+'\n')
 f=r['question'][':question/answer-fields'][0]
 assert sorted(int(c[':answer/value'])for c in f[':answer-field/choices'])==[1,2,3,4,5]
 assert next(int(c[':answer/value'])for c in f[':answer-field/choices']if c[':answer/id']==f[':answer-field/correct'][1])==3
