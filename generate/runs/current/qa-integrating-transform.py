"""Root actual-ODE/full-equation-bank and instructional-stage audit."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186087877;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('parent_transform_math',R/'integrating-factor-parser.py');g=module('parent_transform_generator',D.with_suffix('.py'))
counts={'printed_instances':0,'source_prompt_math':0,'source_values':0,'source_banks':0,'source_existing_designations':0,'source_missing_refs_derived':0,'source_full_prose_and_stage_sequences':0,'source_sign_repairs':0,'source_malformed_value_preserved':0,'raw_duplicate_banks':0}
def option(v):
 v=v.replace('\\\\','\\').replace(r'\u2061','').replace('⁡','')
 if r'\frac{d}{dx^{2}}' in v:
  a,b=p.transformed(v.replace(r'\frac{d}{dx^{2}}',r'\frac{d}{dx}'));return a,2*p.x*b
 return p.transformed(v)
def same(a,b):return all(p.positive_equal(z,w) for z,w in zip(option(a),option(b)))
def check(r,raw=False):
 q=r['question'];P,Q=p.ode(q[':question/problem']);f=q[':question/answer-fields'][0];vs=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vs)==5
 parsed=[option(v) for v in vs];good=[all(p.positive_equal(z,w) for z,w in zip(v,(P,Q))) for v in parsed];assert sum(good)==1
 selected=[i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]];assert len(selected)==1 and good[selected[0]]
 duplicates=[(i,j) for i,v in enumerate(vs) for j,w in enumerate(vs[:i]) if same(v,w)]
 if raw and duplicates:counts['raw_duplicate_banks']+=1
 else:assert not duplicates,(q,duplicates)
 for key,n in p.stages(q[':question/worked-solution'],P,Q).items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def mask(text):return re.sub(r'\s+',' ',p.p.MATH.sub('$MATH$',text)).strip()
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=sources[sid];level=case.get('level',case.get('difficulty',g.TEMPLATES[case['template']][0]));r=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=check(r,raw=True)
 assert all(p.positive_equal(z,w) for z,w in zip(p.ode(old[':question/problem']),p.ode(q[':question/problem'])));counts['source_prompt_math']+=1
 field=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];remaining=[a[':answer/value'] for a in nf[':answer-field/choices']]
 for a in field[':answer-field/choices']:
  matches=[i for i,v in enumerate(remaining) if same(v,a[':answer/value'])];assert matches,(sid,a,remaining);remaining.pop(matches[0]);counts['source_values']+=1
  if 'dx^{2}' in a[':answer/value']:counts['source_malformed_value_preserved']+=1
 assert not remaining;counts['source_banks']+=1;nc=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])
 if field.get(':answer-field/correct'):assert same(nc,field[':answer-field/correct'][':answer/value']);counts['source_existing_designations']+=1
 else:counts['source_missing_refs_derived']+=1
 if old.get(':question/worked-solution'):
  sol=old[':question/worked-solution'];fixed=sol.replace(r'+\frac{1}{2}{e}^{-x/2}',r'-\frac{1}{2}{e}^{-x/2}');P,Q=p.ode(old[':question/problem']);assert mask(fixed)==mask(q[':question/worked-solution']);assert p.stages(fixed,P,Q)==p.stages(q[':question/worked-solution'],P,Q);counts['source_full_prose_and_stage_sequences']+=1;counts['source_sign_repairs']+=fixed!=sol
for item in json.loads((D/'review.json').read_text()):
 r=item.get('record',item);check(r,raw=r['generation']['profile']=='observed_raw')
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
