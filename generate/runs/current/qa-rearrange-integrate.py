"""Parent reads printed ODEs, full explicit banks and each worked stage."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186068841;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_rearrange_reader',R/'separable-ode-parser.py');g=module('reviewed_rearrange_generator',D.with_suffix('.py'))
counts=dict(printed_instances=0,complete_choices=0,source_banks=0,source_values=0,source_existing_refs=0,source_solutions_exact=0,source_prompts_exact=0,conditional_raw_domain_instances=0,raw_signed_constant_teaching_rows=0,raw_duplicate_wrong_banks=0)
def check(r):
 q=r['question'];meta=r['generation'];f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 rhs=p.ode(q[':question/problem']);conditions=p.positive_conditions(q[':question/problem'])
 observed=meta['bank_profile']=='observed'
 if observed and meta['template'] in ('q-8303','q-79665','q-8304'):
  normal=g.generate(q[':question/difficulty'].split('/')[-1],template=meta['template'],parameters=meta['parameters'])
  assert p.equal(p.ode(normal['question'][':question/problem']),rhs)
  conditions=p.positive_conditions(normal['question'][':question/problem']);counts['conditional_raw_domain_instances']+=1
 choices=f[':answer-field/choices'];forms=[];good=[]
 for a in choices:
  if f[':answer-field/type']==':answer-field.type/blank':
   assert meta['template']=='q-128191'
   fragment=a[':answer/value'];assert f[':answer-field/key'] in q[':question/problem']
   pieces=p.blocks(q[':question/problem']);left=next(v for v in pieces if v.startswith('y=') and v.endswith('('));right=next(v for v in pieces if v.startswith('+K)'))
   forms.append(p.solution(left+'('+fragment+')'+right))
  else:forms.append(p.solution(a[':answer/value']))
  good.append(all(p.full_family(F,rhs,conditions) for F in forms[-1]));counts['complete_choices']+=1
 assert sum(good)==1 and next(a[':answer/id'] for a,v in zip(choices,good) if v)==f[':answer-field/correct'][1],(meta,good,rhs)
 if not observed:
  for i,A in enumerate(forms):
   for B in forms[:i]:assert not (len(A)==len(B) and all(p.family_equal(a,b) for a,b in zip(A,B))),(meta,A,B)
 elif meta['template']=='q-3854':counts['raw_duplicate_wrong_banks']+=1
 if observed and meta['template']=='q-158009':counts['raw_signed_constant_teaching_rows']+=1
 stages=p.stages(q[':question/worked-solution'],rhs,conditions)
 assert stages['ode_rows']>=2 and stages['integral_rows']>=2 and stages['primitive_rows']>=1 and stages['explicit_family_rows']>=1,(meta,stages)
 for key,n in stages.items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;return q
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=check(r);of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
 assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
 remaining=list(nf[':answer-field/choices'])
 for a in of[':answer-field/choices']:
  def same(b):
   if nf[':answer-field/type']==':answer-field.type/blank':return p.equal(p.scalar(a[':answer/value']),p.scalar(b[':answer/value']))
   A,B=p.solution(a[':answer/value']),p.solution(b[':answer/value']);return len(A)==len(B) and all(p.equal(v,w) for v,w in zip(A,B))
  index=next(i for i,b in enumerate(remaining) if same(b));remaining.pop(index)
 assert not remaining
 a=of[':answer-field/correct'][':answer/value'];b=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert p.equal(p.scalar(a) if '=' not in a else p.solution(a)[0],p.scalar(b) if '=' not in b else p.solution(b)[0])
 counts['source_banks']+=1;counts['source_values']+=len(of[':answer-field/choices']);counts['source_existing_refs']+=1;counts['source_solutions_exact']+=1;counts['source_prompts_exact']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['raw_domain_omission_sources']=['q-8303','q-79665','q-8304'];counts['source_wrong_family_duplicates']=['q-3854'];counts['raw_signed_constant_teaching_source']='q-158009';counts['database_writes']=0
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
