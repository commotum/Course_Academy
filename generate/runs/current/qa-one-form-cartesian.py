"""Parent's Cartesian one-form audit reads the printed curve/form and all rows."""
import importlib.util,json
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186179674;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('parent_cart_math',R/'one-form-parser.py');g=module('parent_cart_generator',D.with_suffix('.py'))
counts={'printed_instances':0,'source_prompts':0,'source_solutions':0,'raw_source_banks':0,'raw_source_values':0,'raw_duplicate_wrong_banks':0,'eligible_repaired_banks':0,'eligible_original_value_matches':0,'scalar_bank_values':0}
def value(text):return p.scalar(text.replace('\\\\','\\'))
def check(r,raw=False):
 q=r['question'];P,Q=p.oneform(q[':question/problem']);path,lim,curve,points=p.cartesian(q[':question/problem'],q[':question/worked-solution']);f=p.evaluate_form(P,Q,path);I=s.integrate(f,(p.t,*lim));field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==5
 values=[value(a[':answer/value']) for a in field[':answer-field/choices']];counts['scalar_bank_values']+=len(values)
 selected=[v for a,v in zip(field[':answer-field/choices'],values) if a[':answer/id']==field[':answer-field/correct'][1]];assert len(selected)==1 and p.equivalent(selected[0],I),(q[':question/problem'],selected,I)
 collisions=[(i,j) for i,v in enumerate(values) for j,w in enumerate(values[:i]) if p.equivalent(v,w)]
 if raw and r['generation']['template']=='sqrt_linear':assert len(collisions)==1 and not p.equivalent(values[collisions[0][0]],I);counts['raw_duplicate_wrong_banks']+=1
 else:assert not collisions,(q,values)
 for key,n in p.stages(q[':question/worked-solution'],P,Q,path,lim).items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=check(r,raw=True)
 for key,ct in ((':question/problem','source_prompts'),(':question/worked-solution','source_solutions')):assert q[key]==old[key],(case,key);counts[ct]+=1
 field=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in field[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices']);counts['raw_source_banks']+=1;counts['raw_source_values']+=5
 nc=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert nc==field[':answer-field/correct'][':answer/value']
 er=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile='observed_repaired');eq=check(er);counts['eligible_repaired_banks']+=1;ev=[value(a[':answer/value']) for a in eq[':question/answer-fields'][0][':answer-field/choices']];
 for a in field[':answer-field/choices']:
  matches=[i for i,v in enumerate(ev) if p.equivalent(value(a[':answer/value']),v)]
  if matches:ev.pop(matches[0]);counts['eligible_original_value_matches']+=1
for item in json.loads((D/'review.json').read_text()):
 r=item.get('record',item)
 if r['generation']['profile']=='raw_observed':continue
 check(r)
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
