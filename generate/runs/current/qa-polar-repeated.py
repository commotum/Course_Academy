"""Parent mathematical/source QA of supplied repeated polar integrals."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186129198;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_polar_evaluation',P/'polar-evaluation-readback.py');g=module('root_polar_repeated',D.with_suffix('.py'))
R,T=p.R,p.T;C=dict(instances=0,displayed_choices=0,printed_integral_nodes=0,endpoint_primitives=0,equal_stage_sides=0,formal_identities=0,authored_complete_banks=0,source_banks=0,source_choices=0,source_exact_prompts=0,source_exact_solutions=0,source_refs=0,source_missing_refs=0)
def check(rec):
 q=rec['question'];spans=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S);raw=next(z for z in spans if r'\int' in z).strip().removesuffix('=')
 answer,nodes,_=p.read(raw);assert len(nodes)==2
 radial=next(z for z in nodes if z[1]==R);angular=next(z for z in nodes if z[1]==T);f,_,L,U=radial;h,_,a,b=angular
 # A source homogeneous scale can sit outside both integral operators.
 unscaled=p.integrate(h,T,a,b);scale=s.simplify(answer/unscaled);assert scale.is_number and scale!=0
 fields=q[':question/answer-fields'];assert len(fields)==1;field=fields[0];values=[p.read(z[':answer/value'])[0] for z in field[':answer-field/choices']]
 assert len(values)==5 and all(v.is_finite for v in values)
 assert all(not p.equal(v,w) for i,v in enumerate(values) for w in values[i+1:])
 assert [z[':answer/id'] for z,v in zip(field[':answer-field/choices'],values) if p.equal(v,answer)]==[field[':answer-field/correct'][1]];C['displayed_choices']+=5
 radial_primitives=angular_primitives=0
 for block in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
  if r'\begin{aligned}' not in block:
   lhs,rhs=block.strip().rstrip('.').split('=',1);assert p.equal(p.read(lhs)[0],p.read(rhs)[0]);C['formal_identities']+=1;continue
  body=block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
  for row in body.split('\\\\'):
   lhs,rhs=row.split('&',1);rhs=rhs.strip();assert rhs.startswith('=')
   for side in (lhs,rhs[1:]):
    if not side.strip():continue
    value,ns,primitives=p.read(side);assert p.equal(value,answer),(rec['generation']['template'],side,value,answer);C['equal_stage_sides']+=1;C['printed_integral_nodes']+=len(ns)
    for primitive,var,lo,hi in primitives:
     original=f if var==R else h;ratio=s.simplify(s.trigsimp(s.diff(primitive,var)/original));assert not ratio.has(var) and ratio!=0,(primitive,original,ratio)
     if var==R:assert p.equal(lo,L) and p.equal(hi,U);radial_primitives+=1
     else:assert p.equal(lo,a) and p.equal(hi,b);angular_primitives+=1
     C['endpoint_primitives']+=1
 assert radial_primitives and angular_primitives
 if rec['generation']['bank_origin']=='authored':
  n=s.degree(f,R);P0=s.integrate(f,R);Phi=P0.subs(R,U);F=s.integrate(h,T)
  extra=p.integrate(Phi,T,a,b) if L.has(s.csc(T)) else p.integrate(p.integrate(R*f,R,L,U),T,a,b)
  expected=[answer,(n+1)*answer,extra,-answer,F.subs(T,b)/2-F.subs(T,a)]
  assert all(sum(p.equal(v,w) for w in values)==1 for v in expected),(rec['generation']['template'],expected,values);C['authored_complete_banks']+=1
 if q[':question/difficulty'].endswith('/hard'):
  assert s.degree(f,R)==1 and p.equal(a,0) and b in (s.pi/12,s.pi/8,s.pi/6)
  assert U.has(s.sin(2*T)) or U.has(s.cos(2*T));assert len(re.findall(r'\$\$',q[':question/worked-solution']))==8
 C['instances']+=1;return q
source={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 old=source[case['source_id']];q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));assert q[':question/problem']==old[':question/problem'];C['source_exact_prompts']+=1
 assert sorted(z[':answer/value'] for z in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(z[':answer/value'] for z in old[':question/answer-fields'][0][':answer-field/choices']);C['source_banks']+=1;C['source_choices']+=5
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_exact_solutions']+=1
 oldref=old[':question/answer-fields'][0].get(':answer-field/correct')
 if oldref:
  f=q[':question/answer-fields'][0];value=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert p.equal(p.read(value)[0],p.read(oldref[':answer/value'])[0]);C['source_refs']+=1
 else:C['source_missing_refs']+=1
for rec in json.loads((D/'review.json').read_text())+json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(rec)
for level in ('easy','moderate','hard'):
 for seed in range(80,100):check(g.generate(level,seed))
freeze=json.loads((D/'freeze.json').read_text())
for path,digest in {**freeze['artifacts'],**freeze['source_context_sha256']}.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
C['frozen_hashes_verified']=len(freeze['artifacts'])+len(freeze['source_context_sha256']);C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
