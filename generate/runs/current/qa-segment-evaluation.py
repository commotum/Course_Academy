"""Root checks actual 2D segment integrands, banks, primitives and endpoint terms."""
import hashlib,importlib.util,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186179670;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);sys.modules[n]=m;spec.loader.exec_module(m);return m
P=mod('root_eval_segment',R/'segment-readback.py');G=mod('root_eval_generator',D.with_suffix('.py'));F=mod('root_eval_fidelity',R/'root-source-fidelity.py');O,Fid=F.check(G,K,D)
def primitive(z,axis=P.t):
 z=z.replace(r'\left','').replace(r'\right','');co,body=z.split('[',1);body,tail=body.rsplit(']',1);assert tail in ('_0^1','_{0}^{1}') or tail.startswith('_{'),tail
 co=P.scalar(co) if co.strip() else s.Integer(1);return co*P.scalar(body),co,P.scalar(body),tail
C=dict(records=0,choice_values=0,bank_pairs=0,source_prose_masks=0,primitive_derivatives=0,endpoint_sides=0,endpoint_components=0,substitution_bounds=0)
rows=json.load(open(R/f'qa/{K}-sampled.json'))
# Include each supported family at original values where the normal whole bank is eligible.
for sid,(level,f,p) in G.ANCHORS.items():
 try:rows.append(G.generate(level,template=f,parameters=p))
 except ValueError:pass
for r in rows:
 q,m=r['question'],r['generation'];fn,A,B,path,dr,speed,h=P.objects(q[':question/problem'],2);expected=P.value(speed*s.Integral(h,(P.t,0,1)));t=P.t;x,y=path
 F=q[':question/answer-fields'][0];vals=[P.scalar(a[':answer/value']) for a in F[':answer-field/choices']];assert len(vals)==5
 assert [a[':answer/id'] for a,v in zip(F[':answer-field/choices'],vals) if P.same(v,expected)]==[F[':answer-field/correct'][1]]
 for i,v in enumerate(vals):
  assert v.is_real is True and v.is_finite is True
  for w in vals[i+1:]:assert not P.same(v,w);C['bank_pairs']+=1
 f=m['template'];iv=s.simplify(expected/speed);prim=s.integrate(h,t) if f not in ('secant','matched_exponential') else None
 if f=='product':
  H=s.Poly(s.expand(h),t);a,b,c=H.all_coeffs();wrong=[expected,iv,speed*(a/3+c),speed*(b/2+c),speed*(a/2+b/2+c)]
 elif f=='linear':wrong=[expected,iv,speed*h.subs(t,0),speed*h.subs(t,1),speed*prim.subs(t,s.Rational(1,2))]
 elif f=='odd_linear':
  a=A[0];c=fn.coeff(P.p.x);wrong=[0,-2*c*a*a,2*c*a*a,c*a*a,c*a]
 elif f=='radical':
  a=A[0];b=s.simplify(h.subs(t,1)-a);wrong=[expected,iv,speed*(a+b),speed*(a+b/2),speed*(a+3*b/2)]
 elif f=='exponential':
  arg=next(iter(h.atoms(s.exp))).args[0];k=s.diff(arg,t);wrong=[expected,iv,speed*s.exp(k)/k,speed*(s.exp(2*k)-1)/k,speed*(s.exp(k)+1)/k]
 elif f=='secant':
  arg=P.scalar(re.search(r'using the substitution \$u=(.*?)\$',q[':question/worked-solution'])[1]);k=s.diff(arg,t);delta=s.tan(k);wrong=[expected,iv,speed*k*delta,delta*k,speed*delta]
 else:
  arg=next(iter(h.atoms(s.exp))).args[0];lo,hi=arg.subs(t,0),arg.subs(t,1);wrong=[expected,iv,speed*(s.exp(hi)+s.exp(lo)),speed*(s.exp(hi)-s.exp(lo+1)),dr[0]*(s.exp(hi)-s.exp(lo))]
 assert all(any(P.same(v,w) for w in vals) for v in wrong),(f,vals,wrong)
 sol=q[':question/worked-solution'];counts,bs,ri=P.stages(sol,fn,A,B,path,dr,speed,h,2)
 for k,v in counts.items():C[k]=C.get(k,0)+v
 if f in ('secant','matched_exponential'):
  assert len(bs)==6 and len(ri)==3;er=P.rows(bs[5]);assert len(er)==(5 if f=='secant' else 4)
  u=P.p.u;arg=P.scalar(re.search(r'using the substitution \$u=(.*?)\$',sol)[1]);du=s.diff(arg,t);lo,hi=arg.subs(t,0),arg.subs(t,1)
  actual=P.complete(er[0]);integ=next(iter(actual.atoms(s.Integral)));assert integ.limits==((u,lo,hi),);assert P.same(P.value(actual),expected);C['substitution_bounds']+=2
  pp,co,body,tail=primitive(er[1],u);assert P.same(s.diff(pp,u),actual/integ*integ.function);C['primitive_derivatives']+=1
  for row in er[2:]:assert P.same(P.scalar(row),expected);C['endpoint_sides']+=1
  if f=='matched_exponential':
   exps=re.findall(r'e\^\{([^{}]+)\}',er[2]);assert len(exps)==2 and P.scalar(exps[0])==hi and P.scalar(exps[1])==lo;C['endpoint_components']+=2
  else:
   angles=re.findall(r'\\tan\((.*?)\)',er[2]);assert len(angles)==2 and P.scalar(angles[0])==hi and P.scalar(angles[1])==lo;C['endpoint_components']+=2
 else:
  assert len(bs)==5 and len(ri)==6
  pp,co,body,tail=primitive(ri[3]);assert tail=='_0^1';assert P.same(s.diff(pp,t),speed*h);C['primitive_derivatives']+=1
  assert P.same(P.scalar(ri[4]),expected) and P.same(P.scalar(ri[5]),expected);C['endpoint_sides']+=2
  # Independently read the upper/lower evaluation totals, then every uncollected term.
  groups=P.q.outer(ri[4]);assert groups
  if f=='radical':
   assert '+' in groups[0];parts=groups[0].split('+');assert len(parts)==2 and P.scalar(parts[0])==1
   b=s.simplify(h.subs(t,1)-A[0]);assert P.scalar(parts[1])==2*b/(3*A[0]);C['endpoint_components']+=2
  if f=='product':
   upper=P.q.outer(groups[0]);assert len(upper)==3
   terms=s.Poly(body,t).terms();expected_terms=[c for (power,),c in terms if power]
   assert len(expected_terms)==3 and all(any(P.same(P.scalar(v),c) for c in expected_terms) for v in upper);C['endpoint_components']+=3
 sid={'product':'q-76564','radical':'q-123363','exponential':'q-123366','secant':'q-76605','matched_exponential':'q-76650'}.get(f)
 if sid:assert P.mask(sol)==P.mask(O[sid][':question/worked-solution']);C['source_prose_masks']+=1
 C['records']+=1;C['choice_values']+=5
out={'passed':True,'source_fidelity':Fid,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
