"""Root strict scalar reader for power-rule integrals, radicals and formal derivatives."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('p',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(z);z.loader.exec_module(p)
x=s.Symbol('x',positive=True);C=p.u
DER=r'\frac{\text{d}}{\text{d}x}'
def group(t,start,open='{',close='}'):
 assert t[start]==open;depth=1;end=start+1
 while depth:
  assert end<len(t);depth+=(t[end]==open)-(t[end]==close);end+=1
 return t[start+1:end-1],end
def scalar(t):
 t=t.strip().rstrip('.,').replace('✓','').replace('C','u')
 while r'\sqrt' in t:
  at=t.index(r'\sqrt');start=at+5;index=2
  if t[start]=='[':v,start=group(t,start,'[',']');index=int(v)
  rad,end=group(t,start);t=t[:at]+'('+scalar_tex(rad)+')^{1/'+str(index)+'}'+t[end:]
 return p.scalar(t).subs(p.x,x)
def scalar_tex(t):return s.latex(scalar(t))
def value(t):
 t=t.strip().rstrip('.,').replace('✓','')
 while DER in t:
  at=t.index(DER);arg,end=group(t,at+len(DER),'(',')');d=s.diff(scalar(arg),x);t=t[:at]+'('+s.latex(d)+')'+t[end:]
 if t.startswith(r'\int '):
  assert t.endswith(r'\,\text{d}x'),t
  integrand=scalar(t[5:-len(r'\,\text{d}x')]);return s.integrate(integrand,x)
 return scalar(t)
def eq(a,b):return s.simplify(a-b)==0
def same_derivative(a,b):return eq(s.diff(a-b,x),0)
