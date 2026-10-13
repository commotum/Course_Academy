"""Parent readback of exp/log products including all source fragments/banks."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186096618;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_exp_log_product_readback',R/'product-readback.py');g=module('root_exp_log_product_generator',D.with_suffix('.py'));s=p.s;x=p.x
counts=dict(instances=0,complete_values=0,source_questions=0,source_values=0,source_fields=0,source_existing_refs=0,source_missing_refs=0,source_exact_prompts=0,source_exact_solutions=0,source_derived_solutions=0)
def fn(prompt):
 m=re.search(r'f\(x\)\s*=\s*(.*?)\$',prompt,re.S);assert m,prompt;return p.scalar(m[1])
def signatures(text):return [p.normalize(row).count("'") for row in re.search(r'\$\$(.*?)\$\$',text,re.S)[1].split(r'\\')]
def check(record):
 q=record['question'];meta=record['generation'];F=fn(q[':question/problem']);df=s.diff(F,x);worked=q[':question/worked-solution'];stats=p.stages(worked,F);assert stats['derivative_rows'] in (3,4)
 for key,n in stats.items():counts[key]=counts.get(key,0)+n
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1;vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']]
 if f[':answer-field/type'].endswith('/radio'):
  good=[p.same(v,df) for v in vals];assert sum(good)==1
  for n,a in enumerate(vals):assert all(not p.same(a,b) for b in vals[:n])
 else:
  good=[]
  for z in f[':answer-field/choices']:
   lhs,rhs=p.blank_complete(q[':question/problem'],z[':answer/value'],F);assert p.same(lhs,df);good.append(p.same(rhs,df))
  assert all(good)
 assert good[next(n for n,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
 if q[':question/difficulty']!= ':question.difficulty/easy':
  factors=p.definitions(worked);u,v=factors['u'],factors['v'];assert u.is_polynomial(x);terms=s.Poly(u,x).terms()
  assert len(terms)==(2 if q[':question/difficulty'].endswith('/moderate') else 3);assert s.Poly(u,x).degree() in (2,3,4)
  assert v==s.exp(x) or s.simplify(v/s.log(x)).is_number and not (v/s.log(x)).has(x)
  assert stats['derivative_rows']==4 and stats['formal_rows']>=2
 counts['instances']+=1;counts['complete_values']+=len(vals);return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];q=check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']));assert q[':question/problem']==old[':question/problem'];counts['source_exact_prompts']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];assert signatures(q[':question/worked-solution'])==signatures(old[':question/worked-solution']);counts['source_exact_solutions']+=1
 else:counts['source_derived_solutions']+=1
 for of,nf in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  remaining=[p.scalar(z[':answer/value']) for z in nf[':answer-field/choices']]
  for z in of[':answer-field/choices']:
   A=p.scalar(z[':answer/value']);n=next(n for n,B in enumerate(remaining) if p.same(A,B));remaining.pop(n)
  assert not remaining
  if of.get(':answer-field/correct'):
   actual=p.scalar(next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]));assert p.same(actual,p.scalar(of[':answer-field/correct'][':answer/value']));counts['source_existing_refs']+=1
  else:counts['source_missing_refs']+=1
  counts['source_fields']+=1;counts['source_values']+=len(of[':answer-field/choices'])
 counts['source_questions']+=1
review=json.loads((D/'review.json').read_text())
for record in review if isinstance(review,list) else review['generated_variants']:
 if record.get('kind')!='original':check(record.get('record',record))
for record in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(record)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
