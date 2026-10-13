"""Root strict same-angle rational-trig reader with circle parametrization."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('p',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(z);z.loader.exec_module(p)
S,C,v=s.symbols('S C v',real=True)
def scalar(t):
 t=t.strip().rstrip('.,').replace(r'\dfrac',r'\frac').replace(r'\cancel','').replace(r'\theta','t').replace(r'\phi','t').replace(r'\alpha','t').replace('θ','t');t=re.sub(r'(?<![A-Za-z])x(?![A-Za-z])','t',t)
 value=p.scalar(t);functions=value.atoms(s.sin,s.cos,s.tan,s.cot,s.sec,s.csc);assert all(f.args[0]==p.t for f in functions),(t,functions)
 return value.subs({s.sin(p.t):S,s.cos(p.t):C,s.tan(p.t):S/C,s.cot(p.t):C/S,s.sec(p.t):1/C,s.csc(p.t):1/S})
def canonical(expr):return s.cancel(s.sympify(expr).subs({S:2*v/(1+v*v),C:(1-v*v)/(1+v*v)}))
def equal(a,b):return canonical(a-b)==0
def group(t,i):
 assert t[i]=='{';depth=1;j=i+1
 while depth:
  depth+=(t[j]=='{')-(t[j]=='}');j+=1
 return t[i+1:j-1],j

def denominators(tex):
 out=[]
 for m in re.finditer(r'\\(?:d?frac)\{',tex):
  _,j=group(tex,m.end()-1);d,_=group(tex,j);out.append(scalar(d))
 return out
