"""Parent Decimal oracle from printed observations, independent of SymPy model."""
from decimal import Decimal as D,localcontext,ROUND_HALF_UP
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;S=R.parents[2]/'generate/scratch/17592186124675';kp=17592186124675
spec=importlib.util.spec_from_file_location('parent_growth',S.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def atom(t):
 t=t.replace(r'\,','')
 if t.startswith(r'\frac'):
  a,b=re.findall(r'\d+',t);return D(a)/D(b)
 return D(t)
def oracle(q,name):
 nums=[atom(t) for t in re.findall(r'\\frac\{\d+\}\{\d+\}|(?<![A-Za-z])\d+(?:\\,\d{3})*(?:\.\d+)?',q)]
 t0=D(0);time=None;target=None
 if name=='q-37400':k,a,_,n,time=nums
 elif name=='q-335282':k,a,_,n,target=nums
 elif name=='q-335280':a,aa,_,_,n,t1,n1,target=nums;assert a==aa;k=((a-n)/(a-n1)).ln()/t1
 elif name in ('q-15370','q-335542'):a,n,t1,n1,target,_=nums;k=((a-n)/(a-n1)).ln()/t1
 elif name=='q-335578':a,n,aa,t1,n1,target,_=nums;assert a==aa;k=((a-n)/(a-n1)).ln()/t1
 else:
  if name=='q-335619':a,n,t0,n1,t1,target=nums
  else:a,n,n1,t0,t1,time=nums
  k=((a-n)/(a-n1)).ln()/(t1-t0)
 result=a-(a-n)*(-k*(time-t0)).exp() if time is not None else t0+((a-n)/(a-target)).ln()/k
 return int(result.to_integral_value(rounding=ROUND_HALF_UP)),a,time
n=dict(source_banks=0,source_values=0,source_designations=0,source_solutions=0,displayed_default_instances=0)
def check(r):
 q=r['question'];name=r['generation']['template'];correct,a,time=oracle(q[':question/problem'],name);f=q[':question/answer-fields'][0]
 values=[]
 for ans in f[':answer-field/choices']:
  value=int(re.search(r'\$(-?\d+)',ans[':answer/value'])[1]);values.append(value)
  assert (value==correct)==(ans[':answer/id']==f[':answer-field/correct'][1])
  if r['generation']['bank_origin']=='authored':
   assert value>=0
   if time is not None:assert value<=a
   assert not re.search(r'\$1\$ (?:days|hours|minutes)',ans[':answer/value'])
 assert len(set(values))==5
raw=json.loads((R/'sources'/f'{kp}.json').read_text())['record'];qs={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
with localcontext() as ctx:
 ctx.prec=60
 for case in json.loads((S/'source-cases.json').read_text()):
  old=qs[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(r);q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);n['source_banks']+=1;n['source_values']+=5
  if ':answer-field/correct' in of:
   chosen=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert chosen[':answer/value']==of[':answer-field/correct'][':answer/value'];n['source_designations']+=1
  if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];n['source_solutions']+=1
 for name,t in g.TEMPLATES.items():
  for seed in range(12):check(g.generate(t['level'],seed,template=name));n['displayed_default_instances']+=1
(R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
