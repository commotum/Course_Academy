"""Root reads actual pointwise rate tasks, full banks and every displayed stage."""
import importlib.util,json,re,copy
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186124471;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_point_chain',P/'vector-chain-readback.py');g=module('root_point_chain_gen',D.with_suffix('.py'))
C=dict(records=0,actual_functions_and_curves=0,choices=0,whole_method_banks=0,observed_scaled_banks=0,solution_blocks=0,solution_equalities=0,formal_rows=0,prose_substitutions=0,point_prose_slots=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0,known_raw_formal_errors=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def check(r):
 q=r['question'];d=p.given(q[':question/problem']);times=[p.scalar(v.split('=',1)[1]) for v in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S) if re.match(r't\s*=',v)];assert len(times)==1;at=times[0];A=d['answer'].subs(p.t,at);assert at.is_real is True and not A.has(s.zoo,s.nan,s.oo);meta=r['generation'];name=meta['template'];profile=meta['bank_profile'];f=q[':question/answer-fields'][0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vals)==5 and sum(p.equal(z,A) for z in vals)==1 and not any(p.equal(z,w) for i,z in enumerate(vals) for w in vals[:i]);raw=profile.endswith(('_raw','_raw_omission'))
 if ':answer-field/correct' in f:
  good=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert p.equal(p.scalar(good[':answer/value']),A);sol=q[':question/worked-solution']
  if raw and name in ('radical_square','log_norm'):
   # Known source first formal velocity row is false. Check its actual mismatch,
   # omit only that documented row from mathematical oracle, retain every other.
   block=re.findall(r'\$\$(.*?)\$\$',sol,re.S)[3];row=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')[0];rhs=row.split('=',1)[1].replace('&','');assert not p.equal(p.expression(rhs,d),d['derivative']);replacement='\n'+r'\begin{aligned}'+g.VEL+block.split(r'\\',1)[1]
   sol=sol.replace('$$'+block+'$$','$$'+replacement+'$$',1);C['known_raw_formal_errors']+=1
  counts=p.solution(sol,d);assert counts['blocks']==6 and counts['prose_substitutions']==(3 if d['F'].has(p.z) else 2)
  for k,v in counts.items():C[{'blocks':'solution_blocks','equalities':'solution_equalities'}.get(k,k)]+=v
  for span in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S):
   if re.match(r't\s*=',span):assert p.equal(p.scalar(span.split('=',1)[1]),at);C['point_prose_slots']+=1
 else:assert ':question/difficulty' not in q and ':question/worked-solution' not in q and raw and meta['evidence_only'] and not meta['eligible_for_learning'];C['raw_missing_assessments']+=1
 G=d['composed'];rd=d['derivative'];terms=[a*b for a,b in zip(G,rd)];n=3 if d['F'].has(p.z) else 2
 if not raw:
  if name in ('radical_square','log_norm'):wrong=[terms[0],terms[2],sum(G),sum(a*b*b for a,b in zip(G,rd))]
  elif n==2:wrong=[terms[0],terms[1],sum(G),terms[0]-terms[1]]
  else:wrong=[sum(terms[1:]),sum(terms[:-1]),sum(G),sum(terms[:-1])-terms[-1]]
  bank=[A]+[s.simplify(z.subs(p.t,at)) for z in wrong];assert all(sum(p.equal(z,w) for w in vals)==1 for z in bank);C['whole_method_banks']+=1;assert meta['eligible_for_learning']
  level=q[':question/difficulty'].split('/')[-1];assert level==dict(quadratic_affine='easy',quotient='moderate',trig_powers='moderate',square_difference='moderate',sine_difference='moderate',triple_product='hard',radical_square='hard',log_norm='hard',mixed_product='hard')[name]
  if level=='easy':assert s.Poly(d['F'],p.x,p.y).monoms()==[(2,0),(0,2)] and all(1<=abs(c)<=4 and c.is_Integer for c in s.Poly(d['F'],p.x,p.y).coeffs()) and all(s.Poly(v,p.t).degree()==1 for v in d['R'][:2]) and at in (-2,-1,0,1,2)
  if name in ('quotient','triple_product','sine_difference'):assert at in (1,4,9)
  if name=='trig_powers':assert at in (s.pi/6,s.pi/4,s.pi/3,2*s.pi/3,3*s.pi/4)
  if name=='radical_square':assert at in (2,3) and s.expand(d['R'][2]**2).subs(p.t,at) in (1,4)
 else:
  sid=meta['source_ids'][0];base=p.given(sources[sid][':question/problem']);scale=s.simplify(d['F']/base['F']);assert scale in (1,2,3,4) and d['R']==base['R'];bank=[scale*p.scalar(z[':answer/value']) for z in sources[sid][':question/answer-fields'][0][':answer-field/choices']];assert all(sum(p.equal(z,w) for w in vals)==1 for z in bank);C['observed_scaled_banks']+=1;assert meta['evidence_only'] and not meta['eligible_for_learning']
 C['records']+=1;C['actual_functions_and_curves']+=1;C['choices']+=5;return q
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_math_academy_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old);of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_values']+=5;C['source_banks']+=1
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for name,level in g.TEMPLATES.items():
 for seed in range(8):check(g.generate(level,seed+661,template=name))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
