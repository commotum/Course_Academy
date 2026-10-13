"""Parent reads complete printed exponential-polynomial tasks and stage order."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186096611;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_exp_polynomial_readback',R/'exponential-readback.py');g=module('reviewed_exp_polynomial',D.with_suffix('.py'))
counts=dict(printed_instances=0,complete_values=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs_derived=0,source_raw_solution_matches=0,source_prose_matches=0,source_stage_sequences=0,source_prompts_exact=0,contextual_source_instances=0,legacy_wrong_blank_alias_instances=0)
def fn(q,meta):
 text=q[':question/problem'];template=meta['template'];observed=meta['profile'].startswith('observed_')
 if observed and template=='difference':
  A=p.scalar(next(b[2:] for b in p.p.blocks(text) if b.startswith('A=')));B=p.scalar(next(b[2:].rstrip('.,') for b in p.p.blocks(text) if b.startswith('B=')));F=B*p.s.exp(p.x)-p.x**3-A*p.x;counts['contextual_source_instances']+=1;return 'k',F,None
 if observed and template=='branch':
  # The source worked solution provides its omitted preceding branch definition.
  block=next(b for b in p.p.blocks(q[':question/worked-solution']) if b.startswith('f(x)='));F=p.scalar(block.split('=',1)[1]);counts['contextual_source_instances']+=1;return 'f',F,None
 return p.function_and_point(text)
def value(raw):return p.scalar(raw.split('=',1)[-1])
def formation(text,F,prompt):
 blocks=p.p.blocks(text);first=next((b for b in blocks if 'g(x)-f(x)' in b and '=' in b),None)
 if first is None:return 0
 defs={}
 for b in p.p.blocks(prompt):
  m=re.fullmatch(r'([fg])\(x\)=(.+)',b.strip().rstrip('.,'))
  if m:defs[m[1]]=p.scalar(m[2])
 if not defs:
  A=p.scalar(next(b[2:] for b in p.p.blocks(prompt) if b.startswith('A=')));B=p.scalar(next(b[2:].rstrip('.,') for b in p.p.blocks(prompt) if b.startswith('B=')));defs={'f':p.x**3+A*p.x,'g':B*p.s.exp(p.x)}
 rows=p.p.clean(first).split(r'\\')
 for row in rows:
  raw=row.split('=',1)[1];subs={}
  for n,(name,val) in enumerate(defs.items()):
   slot=('i','j')[n];raw=raw.replace(name+'(x)','('+slot+')');subs[p.p.p.locals_[slot]]=val
  assert p.p.equal(p.scalar(raw).subs(subs),F),(row,F)
 return len(rows)
def check(r):
 q=r['question'];meta=r['generation'];name,F,point=fn(q,meta);df=p.s.diff(F,p.x);a=df.coeff(p.s.exp(p.x));poly=p.s.expand(F-a*p.s.exp(p.x));assert a!=0 and not a.has(p.x) and poly.is_polynomial(p.x) and p.s.degree(poly,p.x)>=2
 expected=df if point is None else df.subs(p.x,point);f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 vals=[value(v[':answer/value']) for v in f[':answer-field/choices']];good=[p.p.equal(v,expected) for v in vals]
 if f[':answer-field/type']==':answer-field.type/radio':
  assert sum(good)==1
  for n,A in enumerate(vals):
   for B in vals[:n]:assert not p.p.equal(A,B),(q,A,B)
 else:
  assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  if meta['template']=='slope_seventh' and meta['profile'].startswith('observed_'):
   assert len(vals)==2 and sum(good)==1 and any(p.p.equal(v,df) for v in vals);counts['legacy_wrong_blank_alias_instances']+=1
  else:assert all(good)
 assert good[next(n for n,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])]
 stages=p.stages(q[':question/worked-solution'],F,point);assert stages['derivative_rows']>=3 and stages['operator_rows']>=2;assert (stages['evaluation_rows']>=3)==(point is not None)
 stages['function_formation_rows']=formation(q[':question/worked-solution'],F,q[':question/problem'])
 for key,n in stages.items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;counts['complete_values']+=len(vals);return q,stages
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
def signature(text):
 return [[row.count(r'\frac{\text{d}}') for row in p.p.clean(b).split(r'\\')] for b in p.p.blocks(text) if r'\begin{aligned}' in b]
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q,stages=check(r);of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];counts['source_prompts_exact']+=q[':question/problem']==old[':question/problem']
 remaining=[value(a[':answer/value']) for a in nf[':answer-field/choices']]
 for a in of[':answer-field/choices']:
  A=value(a[':answer/value']);index=next(k for k,B in enumerate(remaining) if p.p.equal(A,B));remaining.pop(index)
 assert not remaining
 if of.get(':answer-field/correct'):
  oldgood=value(of[':answer-field/correct'][':answer/value']);newgood=value(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]));assert p.p.equal(oldgood,newgood);counts['source_existing_refs']+=1
 else:counts['source_missing_refs_derived']+=1
 if old.get(':question/worked-solution'):
  A=old[':question/worked-solution'];B=q[':question/worked-solution'];assert p.p.MATH.sub('',A)==p.p.MATH.sub('',B);assert signature(A)==signature(B);counts['source_prose_matches']+=1;counts['source_stage_sequences']+=1;counts['source_raw_solution_matches']+=A==B
 counts['source_banks']+=1;counts['source_values']+=len(of[':answer-field/choices'])
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['source_omitted_contexts']=['q-167636','q-167694'];counts['supported_source_math_repair']='q-167636 missing derivative-argument closing parenthesis';counts['source_wrong_blank_alias']='q-304035 derivative is not evaluated slope';counts['database_writes']=0
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
