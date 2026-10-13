"""Parent derives actual printed exponential derivatives and evaluates rows."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186096610;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_exponential_readback',R/'exponential-readback.py');g=module('reviewed_exponential_constant',D.with_suffix('.py'))
counts=dict(printed_instances=0,complete_values=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs_derived=0,source_raw_solution_matches=0,source_whitespace_solution_matches=0,source_prompts_exact=0)
def value(raw,name,point):
 if '=' in raw:
  lhs,raw=raw.split('=',1);assert lhs.strip() in (name+'′(x)',name+"'(x)",'{'+name+'}^{′}(x)',name+'^{′}(x)'),lhs
 return p.scalar(raw)
def check(r):
 q=r['question'];name,F,point=p.function_and_point(q[':question/problem']);derivative=p.s.diff(F,p.x);a=p.s.simplify(derivative/p.s.exp(p.x));assert not a.has(p.x) and a!=0 and p.s.diff(F-a*p.s.exp(p.x),p.x)==0
 expected=derivative if point is None else derivative.subs(p.x,point);f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 vals=[value(v[':answer/value'],name,point) for v in f[':answer-field/choices']];good=[p.p.equal(v,expected) for v in vals]
 if f[':answer-field/type']==':answer-field.type/radio':
  assert sum(good)==1
  for n,A in enumerate(vals):
   for B in vals[:n]:assert not p.p.equal(A,B),(q,A,B)
 else:assert all(good) and '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 assert good[next(n for n,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])]
 stages=p.stages(q[':question/worked-solution'],F,point);assert stages['derivative_rows']==4 and stages['operator_rows']>=3;assert (stages['evaluation_rows']>=3)==(point is not None)
 for key,n in stages.items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;counts['complete_values']+=len(vals);return q,name,point
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q,name,point=check(r);of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
 assert q[':question/problem']==old[':question/problem'];counts['source_prompts_exact']+=1
 remaining=[value(a[':answer/value'],name,point) for a in nf[':answer-field/choices']]
 for a in of[':answer-field/choices']:
  A=value(a[':answer/value'],name,point);index=next(k for k,B in enumerate(remaining) if p.p.equal(A,B));remaining.pop(index)
 assert not remaining
 if of.get(':answer-field/correct'):
  oldgood=value(of[':answer-field/correct'][':answer/value'],name,point);newgood=value(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]),name,point);assert p.p.equal(oldgood,newgood);counts['source_existing_refs']+=1
 else:counts['source_missing_refs_derived']+=1
 if old.get(':question/worked-solution'):
  A=old[':question/worked-solution'];B=q[':question/worked-solution'];assert re.sub(r'\s+','',A)==re.sub(r'\s+','',B);counts['source_whitespace_solution_matches']+=1;counts['source_raw_solution_matches']+=A==B
 counts['source_banks']+=1;counts['source_values']+=len(of[':answer-field/choices'])
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
