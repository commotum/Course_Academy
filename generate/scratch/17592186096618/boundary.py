"""Explicit boundary and mathematical-identity checks, independent printed readback."""
from pathlib import Path
import importlib.util,json,sys
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
sys.path.insert(0,str(ROOT));import readback as rb
report=[]
for t,(level,ft,ids) in g.TEMPLATES.items():
 for hi in (False,True):
  p=g.defaults(t)
  for k in p:
   if k in ('b','d'):p[k]=10 if hi else 2
   elif k in ('a','h'):p[k]=-5 if hi else 1
   elif k=='c':p[k]=-5 if hi and level!='easy' else 6 if hi else 2
   elif k=='n':p[k]=(-4 if hi else -1) if t=='power_log_radio' else 4 if hi else 2
   elif k=='m':p[k]=p['n']-1 if hi else 1
   elif k=='k' and t not in ('power_exp_radio','base_log_negative_left_blank'):p[k]=3 if hi else 1
  r=g.generate(level,template=t,parameters=p);audit=rb.check(r);report.append({'template':t,'parameters':p,'printed_math':audit,'status':'pass'})
 for key in ('a','c','h'):
  if key not in g.defaults(t):continue
  if level=='easy' and key=='c':invalid_values=(0,7)
  else:invalid_values=(0,-6,6)
  for value in invalid_values:
   p=g.defaults(t);p[key]=value
   try:g.generate(level,template=t,parameters=p)
   except ValueError:report.append({'template':t,'invalid_parameter':{key:value},'status':'rejected'})
   else:raise AssertionError((t,p))
a=g.generate_easy(template='base_log_left_blank',parameters={'b':4,'d':3,'k':1});b=g.generate_easy(template='base_log_left_blank',parameters={'b':2,'d':3,'k':2})
assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
assert a['question'][':question/id']!=b['question'][':question/id']
left=g.generate_easy(template='power_exp_left_blank',parameters={'c':1,'n':2,'k':1});right=g.generate_easy(template='power_exp_right_blank',parameters={'c':1,'n':2,'k':1})
assert left['generation']['mathematical_fingerprint']==right['generation']['mathematical_fingerprint']
assert left['question'][':question/id']!=right['question'][':question/id']
report.append({'canonical_task_identity':'Equivalent 4^x and 2^(2x) products deduplicate; product-level key excludes supplied-fragment layout while presentation identity differs','status':'pass'})
(ROOT/'boundary-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: 32 explicit boundary readbacks, signed/zero bounds and canonical product identity')
