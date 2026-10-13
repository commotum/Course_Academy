"""Parent compares printed implicit first integrals and complete source banks."""
import importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186068844;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
i=module('root_implicit_reader',R/'implicit-ode-parser.py');p=i.p;g=module('reviewed_implicit_generator',D.with_suffix('.py'))
counts=dict(printed_instances=0,complete_choices=0,source_banks=0,source_values=0,source_existing_refs=0,source_prompts_exact=0,source_solutions_exact=0)
def check(r):
 q=r['question'];meta=r['generation'];rhs=p.ode(q[':question/problem']);fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio';values=[a[':answer/value'] for a in f[':answer-field/choices']]
 good=[i.valid(v,rhs) for v in values];assert sum(good)==1 and next(a[':answer/id'] for a,v in zip(f[':answer-field/choices'],good) if v)==f[':answer-field/correct'][1],(meta,good)
 for index,A in enumerate(values):
  for B in values[:index]:assert not i.family_equal(A,B),(meta,A,B)
 stages=p.stages(q[':question/worked-solution'],rhs,i.radical_conditions(rhs))
 assert stages['ode_rows']>=2 and stages['integral_rows']>=2 and stages['primitive_rows']>=2 and stages['explicit_family_rows']==0,(meta,stages)
 for key,n in stages.items():counts[key]=counts.get(key,0)+n
 counts['printed_instances']+=1;counts['complete_choices']+=len(values);return q
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=check(r);of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
 assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
 remaining=[a[':answer/value'] for a in nf[':answer-field/choices']]
 for a in of[':answer-field/choices']:
  def exact_equivalent(b):
   A,c=i.relation(a[':answer/value']);B,d=i.relation(b);return p.equal(A/c,B/d)
  index=next(k for k,b in enumerate(remaining) if exact_equivalent(b));remaining.pop(index)
 assert not remaining
 a=of[':answer-field/correct'][':answer/value'];b=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert i.family_equal(a,b)
 counts['source_banks']+=1;counts['source_values']+=len(of[':answer-field/choices']);counts['source_existing_refs']+=1;counts['source_prompts_exact']+=1;counts['source_solutions_exact']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['minimal_normal_domain_repair']='q-158116 y!=0 within stated sec/tan interval';counts['database_writes']=0
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
