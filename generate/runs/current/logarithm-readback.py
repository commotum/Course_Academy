"""Root strict displayed-logarithm reader with actual derivative operators."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('root_log_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x=s.Symbol('x',positive=True);base=s.Symbol('base',positive=True)
def group(z,i,opening='(',closing=')'):
 assert z[i]==opening;start=i+1;depth=1;i+=1
 while depth:depth+=(z[i]==opening)-(z[i]==closing);i+=1
 return z[start:i-1],i
def scalar(z):
 z=z.strip().rstrip('.,').replace('⁡','').replace('\u00a0','').replace(r'\left','').replace(r'\right','').replace(r'\!','')
 z=re.sub(r'\\operatorname\{(ln|log)\}',lambda m:'\\'+m[1],z).replace('{log}',r'\log')
 z=re.sub(r'(?<![A-Za-z\\])ln',lambda _:r'\ln ',z)
 z=re.sub(r'\\log\s*_\{?(\d+|a)\}?\s*x',lambda m:r'\frac{\ln x}{\ln '+('u' if m[1]=='a' else m[1])+r'}',z)
 z=re.sub(r'\\log\s*x',lambda _:r'\frac{\ln x}{\ln 10}',z)
 z=re.sub(r'(?<![A-Za-z\\])log\s*x',lambda _:r'\frac{\ln x}{\ln 10}',z)
 z=z.replace(r'\ln a',r'\ln u')
 operator=r'\frac{\text{d}}{\text{d}x}'
 while operator in z:
  i=z.index(operator);j=i+len(operator);assert z[j]=='(',(z,j);body,end=group(z,j);derivative=s.diff(scalar(body),x);z=z[:i]+'('+s.latex(derivative)+')'+z[end:]
 return p.scalar(z).subs({p.x:x,p.u:base})
def eq(a,b):return s.simplify(a-b)==0
