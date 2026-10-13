"""Parent source fidelity and generated-system readback, independent math."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186073752;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_basic_system_reader',R/'system-readback.py');g=module('root_basic_system_generator',D.with_suffix('.py'));counts=dict(instances=0,source_values=0,source_fields=0,source_empty_fields_derived=0,source_existing_refs=0,source_missing_refs=0,source_raw_prompts=0,source_normalized_prompts=0,source_raw_solutions=0,source_normalized_solutions=0,source_derived_solutions=0)
def normalized_prompt(text):return re.sub(r'\s+','',text.replace('${','$\\{').replace('$$,',' $, $'))
def normalized_solution(text):return text.replace('{\\begin{aligned}',r'\{\begin{aligned}')
def check(r):
 stats,names,equations,sol=p.check(r)
 for k,n in stats.items():counts[k]=counts.get(k,0)+n
 level=r['question'][':question/difficulty'].split('/')[-1]
 if level=='hard':assert all(2<=z.q<=7 and abs(z)<=12 for z in sol.values())
 # Normal contextual prompts explicitly supply the prior equation.
 if r['generation']['template'].startswith('coefficient') and not str(r['generation']['bank_profile']).startswith('source_'):assert 'satisfy $b=' in r['question'][':question/problem']
 counts['instances']+=1;return r['question']
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];q=check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
 assert normalized_prompt(old[':question/problem'])==normalized_prompt(q[':question/problem']);counts['source_normalized_prompts']+=1;counts['source_raw_prompts']+=int(old[':question/problem']==q[':question/problem'])
 if old.get(':question/worked-solution'):
  assert normalized_solution(old[':question/worked-solution'])==q[':question/worked-solution'];counts['source_normalized_solutions']+=1;counts['source_raw_solutions']+=int(old[':question/worked-solution']==q[':question/worked-solution'])
 else:counts['source_derived_solutions']+=1
 for of in old[':question/answer-fields']:
  nf=next(z for z in q[':question/answer-fields'] if z[':answer-field/key']==of[':answer-field/key'])
  if not of.get(':answer-field/choices'):counts['source_empty_fields_derived']+=1;counts['source_missing_refs']+=1;continue
  a=sorted(p.p.scalar(z[':answer/value']) for z in of[':answer-field/choices']);b=sorted(p.p.scalar(z[':answer/value']) for z in nf[':answer-field/choices']);assert a==b
  if of.get(':answer-field/correct'):
   actual=p.p.scalar(next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]));assert actual==p.p.scalar(of[':answer-field/correct'][':answer/value']);counts['source_existing_refs']+=1
  else:counts['source_missing_refs']+=1
  counts['source_fields']+=1;counts['source_values']+=len(a)
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
