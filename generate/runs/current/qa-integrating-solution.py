"""Root reads actual ODE, complete IF/family banks and all evaluation stages."""
import importlib.util,json
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186087878;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('parent_solving_if_math',R/'integrating-factor-parser.py');g=module('parent_solving_if_generator',D.with_suffix('.py'))
counts={'printed_instances':0,'source_prompts':0,'source_full_solutions':0,'source_values':0,'source_notation_normalizations':0,'source_banks':0,'source_existing_designations':0,'source_missing_designations_derived':0,'raw_ambiguous_banks':0,'eligible_repaired_banks':0,'eligible_one_to_one_original_values':0}
def check(r,raw=False):
 q=r['question'];P,Q=p.ode(q[':question/problem']);fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};assert set(fields)=={'field-1','field-2'}
 for key,f in fields.items():
  assert f[':answer-field/type']==':answer-field.type/select';values=[a[':answer/value'] for a in f[':answer-field/choices']];same=p.same_factor if key=='field-1' else p.same_family
  if key=='field-1':good=[p.positive_equal(s.diff(p.scalar(v),p.x),P*p.scalar(v)) for v in values]
  else:good=[p.valid_solution(v,P,Q) for v in values]
  selected=[i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]];assert len(selected)==1 and good[selected[0]],(q,good)
  pairs=[(i,j) for i,v in enumerate(values) for j,w in enumerate(values[:i]) if same(v,w)]
  if raw and r['generation']['source_id']=='q-335409' and key=='field-2':assert len(pairs)==1 and sum(good)==2;counts['raw_ambiguous_banks']+=1
  else:assert not pairs and sum(good)==1,(q,values,pairs,good)
 for key,n in p.stages(q[':question/worked-solution'],P,Q,True).items():counts[key]=counts.get(key,0)+n
 counts['ibp_variable_definitions']=counts.get('ibp_variable_definitions',0)+p.ibp_variables(q[':question/worked-solution'])
 counts['antiderivative_rows']=counts.get('antiderivative_rows',0)+p.antiderivative_rows(q[':question/worked-solution'],P,Q);counts['printed_instances']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['original_bank_profile']);q=check(r,raw=True);assert q[':question/problem']==old[':question/problem'];counts['source_prompts']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'],case['source_id'];counts['source_full_solutions']+=1
 new={f[':answer-field/key']:f for f in q[':question/answer-fields']}
 for f in old[':question/answer-fields']:
  nf=new[f[':answer-field/key']];remaining=[a[':answer/value'] for a in nf[':answer-field/choices']];same=p.same_factor if f[':answer-field/key']=='field-1' else p.same_family
  for a in f[':answer-field/choices']:
   exact=[i for i,v in enumerate(remaining) if v==a[':answer/value']];matches=exact or [i for i,v in enumerate(remaining) if same(v,a[':answer/value'])];assert matches,(case,a,remaining);remaining.pop(matches[0]);counts['source_values']+=1;counts['source_notation_normalizations']+=not bool(exact)
  assert not remaining;counts['source_banks']+=1
  nc=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);same=p.same_factor if f[':answer-field/key']=='field-1' else p.same_family
  if f.get(':answer-field/correct'):assert same(nc,f[':answer-field/correct'][':answer/value']);counts['source_existing_designations']+=1
  else:counts['source_missing_designations_derived']+=1
 er=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);eq=check(er);en={f[':answer-field/key']:f for f in eq[':question/answer-fields']}
 for f in old[':question/answer-fields']:
  vals=[a[':answer/value'] for a in en[f[':answer-field/key']][':answer-field/choices']];same=p.same_factor if f[':answer-field/key']=='field-1' else p.same_family
  for a in f[':answer-field/choices']:
   matches=[i for i,v in enumerate(vals) if same(v,a[':answer/value'])]
   if matches:vals.pop(matches[0]);counts['eligible_one_to_one_original_values']+=1
  counts['eligible_repaired_banks']+=1
for item in json.loads((D/'review.json').read_text()):
 r=item.get('record',item)
 if r['generation']['bank_profile']=='q-335409':continue
 check(r)
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
