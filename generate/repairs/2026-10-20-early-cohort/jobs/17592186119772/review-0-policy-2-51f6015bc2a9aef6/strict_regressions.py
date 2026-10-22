#!/usr/bin/env python3
"""Strict repair acceptance tests. Current package must fail these tests."""
import importlib.util,json,sys,copy
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;W=E.parent/'workspace';sys.path.insert(0,str(W))
s=importlib.util.spec_from_file_location('strict_target',W/'17592186119772.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def correct_label(r):
 f=r['question'][':question/answer-fields'][0];aid=f[':answer-field/correct'][1]
 return next(a[':answer/value'][0] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
results=[]
# Explicit minimal valid upper bank; A becomes sole upper matrix after A/E swap.
p={'criterion':'upper','matrices':{'A':[[1,0],[1,1]],'B':[[2,0],[1,2]],'C':[[3,1],[1,3]],'D':[[4,1],[1,4]],'E':[[5,1],[0,5]]}}
p['matrices']['A'],p['matrices']['E']=p['matrices']['E'],p['matrices']['A']
try:
 r=m.generate_easy(seed=20261022,profile='q-126354',parameters=p)
 assert correct_label(r)=='A','A must become correct'
 assert 'Notice that $A$' in r['question'][':question/worked-solution'],'solution must follow A'
 results.append({'test':'valid_role_swap_accepted','passed':True})
except Exception as e:results.append({'test':'valid_role_swap_accepted','passed':False,'error':str(e),'parameters':p})
for profile in ['q-68743','q-68748']:
 try:
  r=m.generate_easy(seed=19673,profile='raw:'+profile)
  results.append({'test':'source_profile_'+profile,'passed':True})
 except Exception as e:results.append({'test':'source_profile_'+profile,'passed':False,'error':str(e)})
batch=json.load(open(E/'delivery-batch/accepted.json'))
labels=[correct_label(r) for r in batch]
results.append({'test':'batch_not_answered_by_one_label','passed':len(set(labels))>1,'labels':labels,'reason':'The current all-D batch permits an answer action without inspecting any matrix.'})
(E/'strict-regression-report.json').write_text(json.dumps({'command':sys.executable+' strict_regressions.py','tests':results,'passed':all(x['passed'] for x in results)},indent=2)+'\n')
print(json.dumps({'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results)}));sys.exit(0 if all(x['passed'] for x in results) else 1)
