"""Parent reads supplied-gradient tasks, whole banks and every actual stage."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186124593;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
h=module('root_supplied_given',P/'supplied-gradient-readback.py');p=h.p;g=module('root_supplied_gen',D.with_suffix('.py'))
C=dict(records=0,actual_gradients_curves_points=0,choices=0,whole_method_banks=0,observed_scaled_banks=0,solution_blocks=0,solution_equalities=0,formal_rows=0,prose_substitutions=0,point_prose_slots=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,known_raw_basis_errors=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
OPS={'component_sign':('correct','omit_x','omit_y','reverse_x','reverse_y'),'velocity_omission':('correct','omit_dx','omit_dy','omit_both_velocities','sum_velocity'),'dot_arithmetic':('correct','subtract_y','negative_dot','product_terms','sum_gradient'),'chain_input':('correct','position_dot','second_derivative_dot','swapped_velocity','gradient_norm_squared')}
def check(r):
 q=r['question'];d=h.given(q[':question/problem']);at=d['point'];answer=d['evaluated'];meta=r['generation'];name=meta['template'];profile=meta['bank_profile'];f=q[':question/answer-fields'][0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vals)==5 and sum(p.equal(z,answer) for z in vals)==1 and not any(p.equal(z,w) for i,z in enumerate(vals) for w in vals[:i]);good=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert p.equal(p.scalar(good[':answer/value']),answer)
 sol=q[':question/worked-solution']
 if profile=='raw_observed_q-94878':
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);bad=blocks[4];body=bad.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');row=body.split(r'\\')[1];rhs=row.split('=',1)[1];pair=p.topdot(p.clean(rhs));assert pair and not p.equal(p.vector(pair[1].strip()[1:-1]),d['derivative']);fixed=bad.replace(r'(-\frac{1}{\sqrt{t}})i)',r'(-\frac{1}{\sqrt{t}})j)');assert fixed!=bad;sol=sol.replace('$$'+bad+'$$','$$'+fixed+'$$');C['known_raw_basis_errors']+=1
 counts=p.solution(sol,d);assert counts['blocks']==6 and counts['prose_substitutions']==2
 for k,v in counts.items():C[{'blocks':'solution_blocks','equalities':'solution_equalities'}.get(k,k)]+=v
 for span in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S):
  if re.match(r't\s*=',span):assert p.equal(p.scalar(span.split('=',1)[1]),at);C['point_prose_slots']+=1
 if profile in OPS:
  gx,gy=[z.subs(p.t,at) for z in d['composed'][:2]];vx,vy=[z.subs(p.t,at) for z in d['derivative'][:2]];A,B=gx*vx,gy*vy
  ops=dict(correct=A+B,omit_x=B,omit_y=A,reverse_x=-A+B,reverse_y=A-B,omit_dx=gx+B,omit_dy=A+gy,omit_both_velocities=gx+gy,sum_velocity=vx+vy,subtract_y=A-B,negative_dot=-A-B,product_terms=A*B,sum_gradient=gx+gy,position_dot=gx*d['R'][0].subs(p.t,at)+gy*d['R'][1].subs(p.t,at),second_derivative_dot=gx*s.diff(d['R'][0],p.t,2).subs(p.t,at)+gy*s.diff(d['R'][1],p.t,2).subs(p.t,at),swapped_velocity=gx*vy+gy*vx,gradient_norm_squared=gx**2+gy**2)
  assert all(sum(p.equal(ops[z],w) for w in vals)==1 for z in OPS[profile]),(name,profile,meta['parameters'],{z:str(ops[z]) for z in OPS[profile]},[str(w) for w in vals]);assert meta['eligible_for_learning'] and not meta['evidence_only'];C['whole_method_banks']+=1
  level=q[':question/difficulty'].split('/')[-1];assert level==g.TEMPLATES[name]
  if level=='hard':
   assert all(len(s.Add.make_args(s.expand(z)))==2 for z in d['G'][:2]),d['G'];assert name in ('coupled_trig','product_exp') and all(2<=s.Rational(meta['parameters'][z])<=3 for z in ('a','b','d'))
 else:
  base=h.given(sources[meta['source_ids'][0]][':question/problem']);c=s.Rational(meta['parameters']['c']);k=s.Rational(meta['parameters']['time_scale']);assert c in (1,2,3) and k in (1,2,3);assert p.equal(d['G'],c*base['G']) and p.equal(d['R'],base['R'].subs(p.t,k*p.t)) and p.equal(at,base['point']/k);assert all(sum(p.equal(c*k*p.scalar(v[':answer/value']),w) for w in vals)==1 for v in sources[meta['source_ids'][0]][':question/answer-fields'][0][':answer-field/choices']);assert meta['evidence_only'] and not meta['eligible_for_learning'];C['observed_scaled_banks']+=1
 C['records']+=1;C['actual_gradients_curves_points']+=1;C['choices']+=5;return q
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['math_academy_id']];assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution'];C['source_prompts']+=1;C['source_solutions']+=1;of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_values']+=5;C['source_banks']+=1;C['source_keys']+=1
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for name,level in g.TEMPLATES.items():
 for seed in range(4):check(g.generate(level,seed+593,template=name))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
