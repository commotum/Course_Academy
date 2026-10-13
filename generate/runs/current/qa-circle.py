"""Root comparison to immutable fields and visually inspected source arcs."""
import importlib.util,json,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186087784;D=R.parents[2]/f'generate/scratch/{K}'
def mod(name,p):
 z=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=mod('root_circle',D.with_suffix('.py'));p=mod('root_circle_parser',D/'validate.py')
# Angles inferred independently from every original prompt plot, not replay data.
ARCS={'q-78681':('0','1'),'q-79205':('1','3/2'),'q-106294':('0','1'),'q-275161':('1','2'),'q-321947':('0','7/6'),'q-321948':('0','1/2'),'q-321976':('1/2','2'),'q-79165':('0','1/4'),'q-79166':('0','3/2'),'q-79168':('0','5/4'),'q-79210':('0','1/2'),'q-79270':('0','1'),'q-79271':('0','1/2'),'q-79272':('0','1/2'),'q-106293':('1/2','1')}
raw=json.loads((R/'sources'/f'{K}.json').read_text())['record'];sources={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
n={'source_questions':0,'radio_banks':0,'radio_values':0,'blank_fragments':0,'known_correct_refs':0,'source_shared_prompts':0,'source_existing_solutions':0,'visually_inferred_source_domains':0,'generated_printed_curves_and_domains':0}
def read(r,domain):
 q=r['question'];a,b=map(s.Rational,domain);curve=p.displayed_equations(q[':question/problem']);assert len(curve)==1
 ((rx,h),(ry,k))=curve[0];assert rx==ry>0
 for f in q[':question/answer-fields']:
  correct=f[':answer-field/correct'][1];values=f[':answer-field/choices'];selected=next(v for v in values if v[':answer/id']==correct)
  if f[':answer-field/type'].endswith('/radio'):
   vs=[p.readinterval(v[':answer/value']) for v in values];assert len(set(vs))==5 and vs.count((a,b,True))==1
   assert p.readinterval(selected[':answer/value'])==(a,b,True)
  else:assert p.readangle(selected[':answer/value'])==(a if f[':answer-field/key']=='field-1' else b)
 assert p.displayed_equations(q[':question/worked-solution'])==[curve[0],curve[0]]
 # Exact curve origin/radius and swept endpoints from printed cos/sin curves.
 for asset in r['generation']['plots'].values():
  spec=json.loads((Path(asset['path']).parent/'spec.json').read_text());actual=spec['parameters']
  assert (actual['r'],actual['h'],actual['k'])==(rx,h,k)
  assert list(map(s.Rational,spec['solid_interval']))==[a,b];assert spec['closed_endpoints'] and spec['orientation']=='counterclockwise'
 for angle in (a,b):
  x=h+rx*s.cos(s.pi*angle);y=k+ry*s.sin(s.pi*angle);assert s.simplify((x-h)**2+(y-k)**2-rx**2)==0
 n['generated_printed_curves_and_domains']+=1
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];read(r,ARCS[c['source_id']]);n['visually_inferred_source_domains']+=1
 assert p.norm(old[':question/problem'])==p.norm(q[':question/problem']);n['source_shared_prompts']+=1
 if ':question/worked-solution' in old:assert p.norm(old[':question/worked-solution'])==p.norm(q[':question/worked-solution']);n['source_existing_solutions']+=1
 if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
 for of,f in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'] and f[':answer-field/key']==of[':answer-field/key']
  radio=f[':answer-field/type'].endswith('/radio');parse=p.readinterval if radio else p.readangle
  assert sorted(parse(a[':answer/value']) for a in of[':answer-field/choices'])==sorted(parse(a[':answer/value']) for a in f[':answer-field/choices'])
  if radio:n['radio_banks']+=1;n['radio_values']+=len(f[':answer-field/choices'])
  else:n['blank_fragments']+=1
  if ':answer-field/correct' in of:
   selected=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert parse(selected[':answer/value'])==parse(of[':answer-field/correct'][':answer/value']);n['known_correct_refs']+=1
 n['source_questions']+=1
records=json.loads((D/'review.json').read_text())
if isinstance(records,dict):records=records['generated_variants']+records.get('observed_profile_variants',[])
for r in records:
 spec=json.loads((Path(next(iter(r['generation']['plots'].values()))['path']).parent/'spec.json').read_text());read(r,spec['solid_interval'])
n['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
