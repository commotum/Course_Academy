"""Parent's displayed rational-function and complete real-root-set reader."""
import importlib.util,re
from pathlib import Path
import sympy as s
sp=importlib.util.spec_from_file_location('root_asymptote_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p);X=p.x

def clean(raw):return raw.strip().rstrip('.,').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').replace(r'\cancel','').replace('{)}',')').replace('[','(').replace(']',')').strip().rstrip('.,')
def expression(raw):return p.scalar(clean(raw))
def group(text,index):
 assert text[index]=='{';depth=1;j=index+1
 while depth:
  if text[j]=='{':depth+=1
  elif text[j]=='}':depth-=1
  j+=1
 return text[index+1:j-1],j

def function(prompt):
 m=re.search(r'([fgh])\(x\)\s*=([^$]+)',prompt);assert m;raw=clean(m[2]);value=expression(raw)
 if raw.startswith(r'\frac'):
  num,i=group(raw,5);den,j=group(raw,i)
  if j==len(raw):N,D=expression(num),expression(den)
  else:N,D=s.fraction(s.together(value))
 elif raw.count('/')==1:
  n,d=raw.split('/');N,D=expression(n),expression(d)
 else:N,D=s.fraction(s.together(value))
 assert s.simplify(value-N/D)==0
 return dict(name=m[1],raw=raw,value=value,numerator=N,denominator=D,domain=real_roots(D),poles=real_roots(s.fraction(s.cancel(value))[1]))

def real_roots(poly):
 z=s.Poly(poly,X);roots=s.polys.polytools.ground_roots(z)
 if sum(roots.values())!=z.degree():
  roots={r:1 for r in s.solve(z.as_expr(),X) if r.is_real}
 return frozenset(roots)

def rootset(raw):
 raw=clean(raw).replace('$','').replace('only','').replace(r'\,','').replace(r'\pm','±').replace(' and ', ',').strip()
 if 'no vertical asymptotes' in raw.lower():return frozenset()
 result=[]
 for part in raw.split(','):
  part=part.strip();assert part
  if '=' in part:
   lhs,rhs=part.split('=',1);assert lhs.strip()=='x'
  else:rhs=part
  if '±' in rhs:
   z=expression(rhs.replace('±',''));result.extend([z,-z])
  else:result.append(expression(rhs))
 assert all(not z.free_symbols and z.is_real for z in result)
 return frozenset(result)
