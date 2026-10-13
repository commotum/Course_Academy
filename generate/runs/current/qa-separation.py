"""Root separates response eligibility from equivalence of the underlying ODE."""
import importlib.util,json
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186068842;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_separation_readback',R/'separable-ode-parser.py');g=module('reviewed_separation_generator',D.with_suffix('.py'))
counts=dict(printed_instances=0,choices_checked=0,source_banks=0,source_values=0,source_designations=0,source_solutions_exact=0,equivalent_but_unseparated_wrong_options=0)
def assess(raw,rhs):
 lhs,right=raw.split('=',1);A,B=p.scalar(lhs),p.scalar(right);coef=s.diff(A,p.D)
 structural=(coef!=0 and not coef.has(p.x,p.D) and not B.has(p.y,p.D) and p.equal(A,coef*p.D))
 roots=s.solve(A-B,p.D);equivalent=len(roots)==1 and p.equal(roots[0],rhs)
 return structural and equivalent,equivalent,structural
def check(r):
 q=r['question'];rhs=p.ode(q[':question/problem']);f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio';choices=f[':answer-field/choices'];assert len(choices)==5
 accepted=[]
 for a in choices:
  valid,equivalent,structural=assess(a[':answer/value'],rhs)
  if valid:accepted.append(a[':answer/id'])
  elif equivalent and not structural:counts['equivalent_but_unseparated_wrong_options']+=1
 assert accepted==[f[':answer-field/correct'][1]],(q,accepted)
 stages=p.stages(q[':question/worked-solution'],rhs);assert stages['ode_rows']>=2 and stages['integral_rows']==stages['primitive_rows']==stages['explicit_family_rows']==0
 for key,n in stages.items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;counts['choices_checked']+=5;return q,rhs
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case.get('source_ma_id',case['source_id'])];r=g.generate(case.get('level',case.get('difficulty')),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile','observed')));q,rhs=check(r);of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
 assert old[':question/problem']==q[':question/problem'] and old[':question/worked-solution']==q[':question/worked-solution'];assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices']);assert next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];counts['source_banks']+=1;counts['source_values']+=5;counts['source_designations']+=1;counts['source_solutions_exact']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
