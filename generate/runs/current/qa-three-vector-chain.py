"""Root verifies actual three-coordinate functions, full choice banks and stages."""
import importlib.util,json
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186124470;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_three_chain',P/'vector-chain-readback.py');g=module('root_three_chain_gen',D.with_suffix('.py'))
C=dict(records=0,actual_functions_and_curves=0,choices=0,whole_method_banks=0,observed_transformed_banks=0,solution_blocks=0,solution_equalities=0,formal_rows=0,prose_substitutions=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0)
source_map={q[':db/id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
source_by_name=dict(zip(['pair_products','trig_product','constant_coordinate','quartic_trig','log_product','log_difference','exponential_cosine','log_exp'],source_map.values()))
def check(r):
 q=r['question'];d=p.given(q[':question/problem']);assert d['F'].free_symbols<={p.x,p.y,p.z} and d['F'].has(p.z);f=q[':question/answer-fields'][0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vals)==5 and sum(p.equal(z,d['answer']) for z in vals)==1 and not any(p.equal(z,w) for i,z in enumerate(vals) for w in vals[:i]);meta=r['generation'];name=meta['template'];profile=meta['profile']
 if ':answer-field/correct' in f:
  good=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert p.equal(p.scalar(good[':answer/value']),d['answer']);counts=p.solution(q[':question/worked-solution'],d);assert counts['blocks']==5 and counts['formal_rows']==2 and counts['prose_substitutions']==3
  for k,v in counts.items():C[{'blocks':'solution_blocks','equalities':'solution_equalities'}.get(k,k)]+=v
  level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':
   F=s.Poly(d['F'],p.x,p.y,p.z);assert set(F.monoms())=={(1,0,0),(0,1,0),(0,0,1)} and all(a.is_Integer and 1<=abs(a)<=3 for a in F.coeffs()) and d['R'][0]==p.t and d['R'][1]==p.t**2 and d['R'][2] in (p.t,p.t**2)
  else:
   assert name in source_by_name or name=='canonical_log'
   if name in source_by_name:base=p.given(source_by_name[name][':question/problem']);F=base['F'];R=base['R']
   else:F=p.x*p.z*s.log(p.y);R=s.Matrix([p.t**2,p.t,p.t**3])
   c=s.simplify(d['F']/F);assert c.is_Integer and 1<=abs(c)<=(4 if level=='hard' else 3)
   shifts=[h for h in range(-2,3) if all(p.equal(a,b.subs(p.t,p.t+h)) for a,b in zip(d['R'],R))];assert len(shifts)==1
 else:
  assert ':question/difficulty' not in q and ':question/worked-solution' not in q and meta['evidence_only'] and not meta['eligible_for_learning'];C['raw_missing_assessments']+=1
 G=d['composed'];R=d['R'];rd=d['derivative'];terms=[a*b for a,b in zip(G,rd)];A=d['answer']
 if not profile.startswith('observed'):
  ops={'correct':A,'omit_x':terms[1]+terms[2],'omit_y':terms[0]+terms[2],'omit_z':terms[0]+terms[1],'negate_x':-terms[0]+terms[1]+terms[2],'negate_y':terms[0]-terms[1]+terms[2],'negate_z':terms[0]+terms[1]-terms[2],'undifferentiated_curve':G.dot(R),'sum_gradient':sum(G),'omit_both_rates':terms[0],'omit_pair':terms[0],'lose_inner_chain':G[0]+terms[1]+terms[2],'lose_power_factor':terms[0]/3+terms[1]+terms[2]}
  names={'omit_chain':['correct','omit_x','omit_y','omit_z','undifferentiated_curve'],'sign_chain':['correct','negate_x','negate_y','negate_z','sum_gradient'],'constant_active':['correct','omit_x','lose_power_factor','undifferentiated_curve','sum_gradient'],'xy_active':['correct','omit_x','omit_y','undifferentiated_curve','sum_gradient'],'log_rates':['correct','omit_y','omit_both_rates','negate_x','undifferentiated_curve'],'paired_exp':['correct','omit_x','omit_pair','lose_inner_chain','sum_gradient']}[profile]
  assert all(sum(p.equal(ops[n],w) for w in vals)==1 for n in names);C['whole_method_banks']+=1;assert meta['eligible_for_learning']
 else:
  old=source_by_name[name];base=p.given(old[':question/problem']);c=s.simplify(d['F']/base['F']);hs=[h for h in range(-2,3) if all(p.equal(a,b.subs(p.t,p.t+h)) for a,b in zip(d['R'],base['R']))];assert len(hs)==1;bank=[c*p.scalar(z[':answer/value']).subs(p.t,p.t+hs[0]) for z in old[':question/answer-fields'][0][':answer-field/choices']];assert all(sum(p.equal(z,w) for w in vals)==1 for z in bank);C['observed_transformed_banks']+=1;assert meta['evidence_only'] and not meta['eligible_for_learning']
 C['records']+=1;C['actual_functions_and_curves']+=1;C['choices']+=5;return q
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=source_map[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old);of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_values']+=5;C['source_banks']+=1
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for level,names in g.LEVELS.items():
 for name in names:
  for seed in range(8):check(g.generate(level,seed+223,template=name))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
