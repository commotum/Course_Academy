"""Root readback of displayed vector fields and formal divergence rows."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('p',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(z);z.loader.exec_module(p)
variables=(p.x,p.y,p.z);basis=(p.i,p.j,p.k)
def clean(t,evidence=False):
 if evidence:t=t.replace('\\\\','\\').replace('\\u2061','')
 t=t.replace('∂',r'\partial').replace('∇',r'\nabla');return t

def scalar(t,evidence=False):return p.scalar(clean(t,evidence))
def vector(t,evidence=False):
 v=s.expand(scalar(t,evidence));out=tuple(v.coeff(b) for b in basis);assert s.simplify(v-sum(a*b for a,b in zip(out,basis)))==0,t;return out

def field(prompt,evidence=False):
 m=re.search(r'\$(?:F|V)\s*=([^$]+)\$',prompt)
 if m:return vector(m[1].strip().rstrip('.,'),evidence)
 return None

def point(prompt,evidence=False):
 m=re.search(r'at the point \$\((.*?)\)\.?\$',prompt,re.S)
 if not m:return None
 return tuple(scalar(t,evidence) for t in m[1].replace(r'\,','').split(','))

def derivative_inputs(t):
 t=clean(t,True)
 pat=re.compile(r'\\frac\{\\partial\}\{\\partial\s*([xyz])\}\s*\(')
 result=[]
 for m in pat.finditer(t):
  level=1;end=m.end()
  while level and end<len(t):
   level+=(t[end]=='(')-(t[end]==')');end+=1
  assert level==0,t;result.append((m[1],t[m.end():end-1],m.start(),end))
 return t,result

def operator_rhs(t,components,evidence=False):
 t=clean(t,evidence)
 for name,var,component in zip('PQR',variables,components):
  for den,dvar in zip('xyz',variables):
   pat=r'\\frac\{\\partial\s*'+name+r'\}\{\\partial\s*'+den+r'\}'
   t=re.sub(pat,lambda m:r'('+s.latex(s.diff(component,dvar)).replace(r'\log',r'\ln')+')',t)
 t,inputs=derivative_inputs(t)
 for den,arg,start,end in reversed(inputs):
  derivative=s.diff(scalar(arg,evidence),{'x':p.x,'y':p.y,'z':p.z}[den]);t=t[:start]+'('+s.latex(derivative).replace(r'\log',r'\ln')+')'+t[end:]
 return scalar(t,evidence),inputs
