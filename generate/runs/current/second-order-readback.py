"""Root reader for printed second-order ODEs, complete families and integrals."""
import importlib.util,re
from pathlib import Path
from functools import lru_cache
import sympy as s
sp=importlib.util.spec_from_file_location('root_second_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
X=p.x;F=p.u;D1=p.v;D2=p.t;C=p.z;D=p.y
SECOND=r'\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}';FIRST=r'\frac{\text{d}y}{\text{d}x}'
def normalize(raw):
 raw=raw.replace(SECOND,'t').replace(FIRST,'v').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').strip().rstrip('.,')
 raw=re.sub(r'\\[A-Za-z]+|[CDy]',lambda m:m[0] if m[0].startswith('\\') else {'C':'z','D':'y','y':'u'}[m[0]],raw)
 return raw.replace('{ln}^{',r'\ln^{')
def expression(raw):
 raw=normalize(raw)
 while r'\int' in raw:
  i=raw.index(r'\int');m=re.search(r'\\text\{d\}x',raw[i+4:]);assert m,raw;j=i+4+m.start();end=i+4+m.end();body=p.scalar(raw[i+4:j]) if raw[i+4:j].replace(r'\,','').strip() else s.Integer(1)
  a=s.expand(body).coeff(D2);b=s.expand(body).coeff(D1);assert not (a.has(X) or b.has(X));rest=s.expand(body-a*D2-b*D1);assert not rest.has(D2,D1,F)
  primitive=a*D1+b*F+sum(s.integrate(v,X) for v in s.Add.make_args(rest));raw=raw[:i]+'('+s.latex(primitive).replace(r'\log',r'\ln')+')'+raw[end:]
 return p.scalar(raw)
def forcing(prompt):
 blocks=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',prompt,re.S);eq=next(a or b for a,b in blocks if SECOND in (a or b));left,right=eq.split('=',1);r=s.expand(expression(left)-expression(right));coeff=r.coeff(D2);assert coeff!=0 and not coeff.has(C,D,F,D1,D2);G=s.cancel(-(r-coeff*D2)/coeff);assert not G.has(C,D,F,D1,D2);return G,coeff
@lru_cache(maxsize=None)
def primitive(G):return sum(s.integrate(z,X) for z in s.Add.make_args(s.expand(G)))
def answer(raw):
 left,right=raw.split('=',1);assert left.strip()=='y';return expression(right)
def sig(v):
 base=v.subs({C:0,D:0});basis=[s.diff(v,z) for z in (C,D)];assert not any(b.has(C,D) for b in basis);return s.expand(base),basis
def spans(v,basis):
 basis=[b for b in basis if b!=0]
 if not basis:return s.simplify(v)==0
 coeffs=s.symbols('a:'+str(len(basis)));res=s.expand(v-sum(c*b for c,b in zip(coeffs,basis)));sol=s.linsolve([res.subs(X,j) for j in (1,2,3)],coeffs)
 return any(s.simplify(res.subs(dict(zip(coeffs,values))))==0 for values in sol)
def equivalent(v,w):
 vb,vbasis=sig(v);wb,wbasis=sig(w);return spans(vb-wb,vbasis) and all(spans(a,wbasis) for a in vbasis) and all(spans(a,vbasis) for a in wbasis)
def valid(v,G):
 base,basis=sig(v)
 return s.simplify(s.diff(base,X,2)-G)==0 and all(s.simplify(s.diff(b,X,2))==0 for b in basis) and s.Matrix([[s.diff(b,X),b.subs(X,0)] for b in basis]).T.rank()==2
