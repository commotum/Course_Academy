"""Root verifies displayed ODEs, complete explicit families and worked rows."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186068840;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_explicit_ode_reader',R/'separable-ode-parser.py');g=module('reviewed_explicit_ode_generator',D.with_suffix('.py'))
counts=dict(printed_instances=0,complete_choices=0,source_banks=0,source_values=0,source_existing_refs=0,source_solutions_exact=0,source_missing_ode_reference_derived=0)
def check(r):
 q=r['question'];meta=r['generation'];f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 if meta['template']=='temperature_blank':
  for a in f[':answer-field/choices']:
   visible=re.sub(r'\\[A-Za-z]+','',a[':answer/value']);assert 'x' not in visible and 't' in visible,'temperature answer must use displayed time t'
  visible=' '.join(p.blocks(q[':question/worked-solution']));visible=re.sub(r'\\[A-Za-z]+','',visible);assert 'x' not in visible,'temperature worked mathematics must use t'
 if 'part 1' in q[':question/problem']:
  assert meta['template']=='temperature_blank';rhs=p.s.Rational(-3,100)*(p.y-25);counts['source_missing_ode_reference_derived']+=1
 else:rhs=p.ode(q[':question/problem'])
 choices=f[':answer-field/choices'];good=[];forms=[]
 for a in choices:
  if f[':answer-field/type']==':answer-field.type/blank':
   spans=p.blocks(q[':question/problem']);prefix=next(v for v in spans if re.search(r'T\s*=|T\\,',v));ambient=p.scalar(prefix.split('=')[1].split('+')[0].replace(r'\,',''));forms.append((ambient+p.K*p.scalar(a[':answer/value']),))
  else:forms.append(p.solution(a[':answer/value']))
  good.append(all(p.full_family(v,rhs) for v in forms[-1]));counts['complete_choices']+=1
 assert sum(good)==1 and next(a[':answer/id'] for a,v in zip(choices,good) if v)==f[':answer-field/correct'][1],(q,good,rhs)
 if not meta['bank_profile'].startswith('observed_'):
  for i,A in enumerate(forms):
   for B in forms[:i]:assert not (len(A)==len(B) and all(p.family_equal(a,b) for a,b in zip(A,B))),(q,A,B)
 stages=p.stages(q[':question/worked-solution'],rhs);assert stages['ode_rows']>=2 and stages['integral_rows']>=2 and stages['primitive_rows']>=2 and stages['explicit_family_rows']>=1
 for key,n in stages.items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;return q
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case.get('source_ma_id',case['source_id'])];level=case.get('level',case.get('difficulty',g.TEMPLATES[case['template']]['level']));r=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile')));q=check(r);of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
 assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution'];assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices']);assert next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
 counts['source_banks']+=1;counts['source_values']+=len(of[':answer-field/choices']);counts['source_existing_refs']+=1;counts['source_solutions_exact']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
