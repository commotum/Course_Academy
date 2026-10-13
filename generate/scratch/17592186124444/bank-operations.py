#!/usr/bin/env python3
"""Independently verify complete authored banks from actual displayed functions."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('bank_readback',D/'display_parser.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
V=(p.x,p.y,p.z);B=(p.i,p.j,p.k)
def scalar(t):return p.scalar(re.sub(r'\\text\{[^}]*\}','',t).replace(r'\mathbf','').replace('⁡',''))
def vector(t):
 a=s.expand(scalar(t));return tuple(a.coeff(v) for v in B)
def eq(a,b):
 d=s.sympify(a)-s.sympify(b)
 if d==0:return True
 if d.subs({p.x:9,p.y:10,p.z:11}).is_zero is False:return False
 return s.simplify(d)==0
counts={'whole_authored_banks':0,'independently_matched_options':0}
for fixture in json.loads((D/'native-input.json').read_text()):
 r=fixture['record'];m=r['generation'];q=r['question']
 if m['bank_profile']!='authored_method':continue
 F=scalar(re.search(r'[fgh]\(x,y,z\)\s*=([^$]+)',q[':question/problem'])[1].rstrip('.,'))
 pt=re.search(r'at the point \$\((.*?)\)\$',q[':question/problem']);point=tuple(scalar(t) for t in pt[1].split(',')) if pt else None;subs=dict(zip(V,point)) if point else {};ev=lambda d:s.simplify(d.subs(subs))
 G=tuple(ev(s.diff(F,v)) for v in V);family=m['template']
 if family=='polynomial':
  terms=[sum(term for term in s.Add.make_args(s.expand(F)) if term.has(v)) for v in V]
  expected=[G,tuple(term/v for term,v in zip(terms,V)),*[tuple(-a if i==j else a for j,a in enumerate(G)) for i in range(3)]]
 elif family=='quotient':
  N,Dn=s.fraction(F)
  expected=[G,tuple(ev((Dn*s.diff(N,v)+N*s.diff(Dn,v))/Dn**2) for v in V),tuple(ev(Dn*s.diff(N,v)-N*s.diff(Dn,v)) for v in V),tuple(ev(-N*s.diff(Dn,v)/Dn**2) for v in V),tuple(ev(s.diff(N,v)/Dn) for v in V)]
 elif family=='sqrt_product':
  R=s.expand(F**2);translated=[]
  for v in V:
   poly=s.Poly(R,v);assert poly.degree()==1;translated.append(v+s.cancel(poly.nth(0)/poly.nth(1)))
  u,v,w=translated
  expected=[G,tuple(2*a for a in G),tuple(s.diff(R,t)/2 for t in V),(F*u/2,F*v/2,F*w/2),(1/(2*F),G[1],G[2])]
 elif family=='product_log':expected=[G,(F,F,G[2]),(G[0],F,G[2]),(G[0],G[1],F),(G[1],G[0],G[2])]
 elif family=='log_point':expected=[G,tuple(2*a for a in G),*[tuple(-a if i==j else a for j,a in enumerate(G)) for i in range(3)]]
 elif family=='sine_point':expected=[G,*[tuple(-a if i==j else a for j,a in enumerate(G)) for i in range(3)],tuple(-a for a in G)]
 elif family=='expcos_point':
  a,b,c=point;co,si=s.cos(b*c),s.sin(b*c);E=s.exp(a*b);v=(b*co,a*co-c*si,-b*si)
  assert F==s.exp(p.x*p.y)*s.cos(p.y*p.z)
  expected=[G,v,tuple(s.exp(2*a*b)*d for d in v),tuple(-d for d in G),(E*b*co,E*(b*co-c*si),-E*b*si)]
 else:raise AssertionError(family)
 displayed=[vector(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
 assert len(expected)==len(displayed)==5
 assert all(sum(all(eq(a,b) for a,b in zip(e,d)) for d in displayed)==1 for e in expected),(fixture['label'],expected,displayed)
 counts['whole_authored_banks']+=1;counts['independently_matched_options']+=5
(D/'bank-operation-report.json').write_text(json.dumps({'status':'pass',**counts},indent=2)+'\n');print(counts)
