"""Root independently derives two-variable vector chain tasks and full printed stages."""
import importlib.util,json
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186124469;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_two_chain',P/'vector-chain-readback.py');g=module('root_two_chain_gen',D.with_suffix('.py'))
C=dict(records=0,actual_functions_and_curves=0,choices=0,whole_method_banks=0,solution_blocks=0,solution_equalities=0,formal_rows=0,prose_substitutions=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0)
def check(r):
 q=r['question'];d=p.given(q[':question/problem']);assert d['F'].free_symbols<={p.x,p.y} and d['R'][2]==0;f=q[':question/answer-fields'][0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vals)==5 and sum(p.equal(z,d['answer']) for z in vals)==1 and not any(p.equal(z,w) for i,z in enumerate(vals) for w in vals[:i])
 if ':answer-field/correct' in f:
  good=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert p.equal(p.scalar(good[':answer/value']),d['answer']);counts=p.solution(q[':question/worked-solution'],d);assert counts['blocks']==5 and counts['formal_rows']==2 and counts['prose_substitutions']==2
  for k,v in counts.items():C[{'blocks':'solution_blocks','equalities':'solution_equalities'}.get(k,k)]+=v
  level=q[':question/difficulty'].split('/')[-1]
  if level=='moderate':
   # Derive actual mixed polynomial and exponential/log coordinates from the givens.
   F=s.Poly(d['F'],p.x,p.y);assert set(F.monoms())=={(2,0),(1,2)};a,b=F.coeff_monomial(p.x**2),F.coeff_monomial(p.x*p.y**2);assert a.is_Integer and b.is_Integer and 1<=a<=3 and 1<=b<=3 and d['R'][0]==s.log(p.t);rate=s.simplify(d['R'][1].diff(p.t)/d['R'][1]);c=d['R'][1].subs(p.t,0);assert rate in (1,2) and c.is_Integer and 1<=c<=3
  elif level=='hard':
   assert d['F'].func==s.atan;arg=s.Poly(d['F'].args[0],p.x,p.y);assert arg.monoms()==[(1,2)];a=arg.coeffs()[0];assert a.is_Integer and 1<=a<=4;rate=s.simplify(d['R'][0].diff(p.t)/d['R'][0]);assert rate in (2,3,4,5) and d['R'][0].subs(p.t,0)==1 and d['R'][1].func==s.sin and s.diff(d['R'][1].args[0],p.t) in (2,3,4,5)
 else:
  assert ':question/difficulty' not in q and ':question/worked-solution' not in q and r['generation']['evidence_only'] and not r['generation']['eligible_for_learning'];C['raw_missing_assessments']+=1
 if r['generation']['profile']=='authored':
  G,H=d['composed'][:2];du,dv=d['derivative'][:2];bank=[d['answer'],G*du,G*du-H*dv,G+H,G*dv+H*du];assert all(sum(p.equal(z,w) for w in vals)==1 for z in bank);C['whole_method_banks']+=1;assert r['generation']['eligible_for_learning']
 else:assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
 C['records']+=1;C['actual_functions_and_curves']+=1;C['choices']+=5;return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['math_academy_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old);of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_values']+=5;C['source_banks']+=1
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for name in g.TEMPLATES:
 for seed in range(12):check(g.generate(g.LEVEL[name],seed+832,template=name))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
