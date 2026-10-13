"""Parent product-rule readback including supplied answer fragments."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186096617;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_product_readback',R/'product-readback.py');g=module('reviewed_trig_product',D.with_suffix('.py'));s=p.s;x=p.x
counts=dict(instances=0,complete_values=0,source_values=0,source_fields=0,existing_refs=0,missing_refs=0,fieldless_repair=0,source_prompts_raw_exact=0,source_prompt_prose=0,source_exact_solutions=0,source_ordered_solution_prose=0,source_derived_solutions=0,raw_wrong_lhs_instances=0)
def prose(text):return re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)','[MATH]',text,flags=re.S)
def signatures(text):
 block=re.search(r'\$\$(.*?)\$\$',text,re.S)[1];return [p.normalize(row).count("'") for row in block.split(r'\\')]
def check(record):
 q=record['question'];meta=record['generation'];prompt=q[':question/problem'];F=p.question_function(prompt);df=s.diff(F,x);worked=q[':question/worked-solution'];raw=(meta['template']=='q-319350' and meta['profile']=='observed_raw')
 stages=p.stages(worked,F,raw);assert stages['derivative_rows']==4 and stages['formal_rows']==2;counts['raw_wrong_lhs_instances']+=int(raw)
 for name,n in stages.items():counts[name]=counts.get(name,0)+n
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']]
 if f[':answer-field/type'].endswith('/radio'):
  good=[p.same(v,df) for v in vals];assert sum(good)==1
  for n,a in enumerate(vals):assert all(not p.same(a,b) for b in vals[:n])
 else:
  assert '{{'+f[':answer-field/key']+'}}' in prompt
  if prompt.split('\n\n',1)[1].lstrip().startswith("$f'(x)"):
   good=[p.same(v,df) for v in vals]
  else:
   good=[]
   for z in f[':answer-field/choices']:
    lhs,rhs=p.blank_complete(prompt,z[':answer/value']);assert p.same(lhs,df);good.append(p.same(rhs,df))
  assert all(good)
 assert good[next(n for n,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
 functions=p.definitions(worked);u,v=functions['u'],functions['v']
 if not meta['template'].startswith('q-'):
  assert u.is_polynomial(x) and len(s.Poly(u,x).terms())==2
  trig=[node for node in s.preorder_traversal(v) if node.func in (s.sin,s.cos,s.tan)];assert len(trig)==1 and trig[0].args==(x,)
  if q[':question/difficulty'].endswith('/moderate'):assert v==trig[0] and s.Poly(u,x).degree() in (2,3,4) and s.Poly(u,x).coeff_monomial(1)!=0
  else:assert v-trig[0]!=0 and not (v-trig[0]).has(x) and s.Poly(u,x).coeff_monomial(x)!=0
 counts['instances']+=1;counts['complete_values']+=len(vals);return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];q=check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
 if c['source_id']=='q-71004':assert q[':question/problem'].startswith(old[':question/problem']);counts['fieldless_repair']+=1
 else:assert prose(q[':question/problem'])==prose(old[':question/problem']);assert p.same(p.question_function(q[':question/problem']),p.question_function(old[':question/problem']));counts['source_prompts_raw_exact']+=int(q[':question/problem']==old[':question/problem']);counts['source_prompt_prose']+=1
 if old.get(':question/worked-solution'):
  assert prose(q[':question/worked-solution'])==prose(old[':question/worked-solution']);assert signatures(q[':question/worked-solution'])==signatures(old[':question/worked-solution']);counts['source_exact_solutions']+=int(q[':question/worked-solution']==old[':question/worked-solution']);counts['source_ordered_solution_prose']+=1
 else:counts['source_derived_solutions']+=1
 for of,nf in zip(old.get(':question/answer-fields',[]),q[':question/answer-fields']):
  remaining=[p.scalar(a[':answer/value']) for a in nf[':answer-field/choices']]
  for a in of[':answer-field/choices']:
   A=p.scalar(a[':answer/value']);index=next(n for n,B in enumerate(remaining) if p.same(A,B));remaining.pop(index)
  assert not remaining;counts['source_fields']+=1;counts['source_values']+=len(of[':answer-field/choices'])
  if of.get(':answer-field/correct'):
   B=p.scalar(next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]));assert p.same(B,p.scalar(of[':answer-field/correct'][':answer/value']));counts['existing_refs']+=1
  else:counts['missing_refs']+=1
review=json.loads((D/'review.json').read_text())
for record in review['generated_variants']:check(record.get('record',record))
for record in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(record)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
