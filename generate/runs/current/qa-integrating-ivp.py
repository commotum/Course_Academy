"""Root independently audits the supplied ODE/IC, every bank and solution stage."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186087879;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('parent_ivp_math',R/'integrating-factor-parser.py');g=module('parent_ivp_generator',D.with_suffix('.py'))
counts={'printed_instances':0,'source_prompts':0,'source_banks':0,'source_values':0,'source_existing_refs':0,'source_missing_refs_derived':0,'source_prose_and_stage_sequences':0,'source_raw_ambiguous_banks':0}
def same(a,b,key):return p.same_factor(a,b) if key=='field-1' else p.positive_equal(p.scalar(a),p.scalar(b))
def check(r,raw=False):
 q=r['question'];P,Q=p.ode(q[':question/problem']);t,h=p.initial(q[':question/problem']);fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};assert set(fields)=={'field-1','field-2'}
 for key,f in fields.items():
  vs=[a[':answer/value'] for a in f[':answer-field/choices']];assert f[':answer-field/type']==':answer-field.type/select'
  if key=='field-1':good=[p.positive_equal(s.diff(p.scalar(v),p.x),P*p.scalar(v)) for v in vs]
  else:good=[p.positive_equal(s.diff(p.scalar(v),p.x)+P*p.scalar(v),Q) and p.positive_equal(p.scalar(v).subs(p.x,t),h) for v in vs]
  selected=[i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]];assert len(selected)==1 and good[selected[0]],(q,good)
  pairs=[(i,j) for i,v in enumerate(vs) for j,w in enumerate(vs[:i]) if same(v,w,key)]
  if raw and key=='field-2' and r['generation']['template'] in ('q-335811','q-335812'):assert len(pairs)==1 and sum(good)==2;counts['source_raw_ambiguous_banks']+=1
  else:assert not pairs and sum(good)==1,(q,vs,pairs,good)
 for key,n in p.stages(q[':question/worked-solution'],P,Q,True).items():counts[key]=counts.get(key,0)+n
 counts['antiderivative_rows']=counts.get('antiderivative_rows',0)+p.antiderivative_rows(q[':question/worked-solution'],P,Q)
 for key,n in p.initial_rows(q[':question/worked-solution'],P,Q,t,h).items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def mask(text):return re.sub(r'\s+',' ',p.p.MATH.sub('$MATH$',text)).strip()
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=check(r,raw=True);assert q[':question/problem']==old[':question/problem'];counts['source_prompts']+=1
 new={f[':answer-field/key']:f for f in q[':question/answer-fields']}
 for f in old[':question/answer-fields']:
  nf=new[f[':answer-field/key']];vs=[a[':answer/value'] for a in nf[':answer-field/choices']]
  for a in f[':answer-field/choices']:
   matches=[i for i,v in enumerate(vs) if same(v,a[':answer/value'],f[':answer-field/key'])];assert matches,(case,a,vs);vs.pop(matches[0]);counts['source_values']+=1
  assert not vs;counts['source_banks']+=1;nc=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])
  if f.get(':answer-field/correct'):assert same(nc,f[':answer-field/correct'][':answer/value'],f[':answer-field/key']);counts['source_existing_refs']+=1
  else:counts['source_missing_refs_derived']+=1
 if old.get(':question/worked-solution'):
  a=old[':question/worked-solution'];b=q[':question/worked-solution'];assert mask(a)==mask(b),(case['source_id'],mask(a),mask(b));P,Q=p.ode(old[':question/problem']);t,h=p.initial(old[':question/problem']);assert p.stages(a,P,Q,True)==p.stages(b,P,Q,True);assert p.antiderivative_rows(a,P,Q)==p.antiderivative_rows(b,P,Q);assert p.initial_rows(a,P,Q,t,h)==p.initial_rows(b,P,Q,t,h);counts['source_prose_and_stage_sequences']+=1
for item in json.loads((D/'review.json').read_text()):
 r=item.get('record',item);check(r,raw=r['generation']['profile']=='observed')
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
