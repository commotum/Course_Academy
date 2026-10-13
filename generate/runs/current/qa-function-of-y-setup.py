"""Root full source banks, supported default families, correct setups and stages."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'function-of-y-readback.py','reader')
n=dict(records=0,choices=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,default_families={})
def answer(raw,missing):
 return p.scalar(raw) if missing else p.integral(raw)
def check(rec):
 q=rec['question'];g=rec['generation'];details=p.prompt(q[':question/problem']);F,curve,bounds,ft,speed,correct,missing,prefix=details;f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];forms=[answer(a[':answer/value'],missing) for a in choices];assert len(forms)==5
 if missing:
  expected=s.simplify(correct/prefix);good=[p.equal(z,expected,bounds) for z in forms];assert all(not p.equal(z,w,bounds) for i,z in enumerate(forms) for w in forms[:i])
 else:
  values=[p.value(fn,a,b) for a,b,fn,var in forms];expected=p.value(correct,*bounds);good=[p.same_value(z,expected) for z in values];assert all(not p.same_value(z,w) for i,z in enumerate(values) for w in values[:i])
 assert sum(good)==1,(g['template'],forms,details)
 if ':answer-field/correct' in f:
  selected=next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1]);assert good[selected]
  if not missing:
   a,b,fn,var=forms[selected];assert var==p.t and p.equal(a,bounds[0]) and p.equal(b,bounds[1]) and p.equal(fn,correct,bounds)
 else:assert g['evidence_only'] and not g['eligible_for_learning']
 if ':question/worked-solution' in q:
  stages=p.stages(q[':question/worked-solution'],details)
  for k,v in stages.items():n[k]=n.get(k,0)+v
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186179709;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec);q=rec['question'];o=olds[c['source_id']]
  for attr in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (attr in q)==(attr in o)
   if attr in o:assert q[attr]==(o[attr][':db/ident'] if attr.endswith('difficulty') else o[attr])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert value==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
  check(g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters={'density_scale':3}))
 for rec in json.load(open(D/'review.json')):check(rec.get('record',rec))
 for level in ('easy','moderate','hard'):
  families=set()
  for seed in range(14):
   rec=g.generate(level,seed=140000+seed);check(rec);families.add(rec['generation']['template'])
  n['default_families'][level]=sorted(families)
  for template in {'easy':['authored_line','authored_line_monomial','authored_affine'],'moderate':['authored_power','authored_log','authored_scaled_log','authored_reciprocal'],'hard':['authored_shifted_power']}[level]:check(g.generate(level,seed=910001,template=template))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
