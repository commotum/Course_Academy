"""Root fail-closed scalar and formal integral reader, independent of generators."""
import importlib.util,re
from pathlib import Path
import sympy as s
sp=importlib.util.spec_from_file_location('root_trig_base',Path(__file__).with_name('ode-scalar-parser.py'));P=importlib.util.module_from_spec(sp);sp.loader.exec_module(P)
CONST=P.v
def clean(t):
 t=t.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\displaystyle','').replace(r'\u2061','').replace('⁡','').replace(r'\theta','u').replace('θ','u');return re.sub(r'(?<![A-Za-z])C(?![A-Za-z])','v',t)
def scalar(t):return P.scalar(clean(t))
DIFFERENTIAL=r'(?:\\(?:text|textrm|mathrm)\{?d\}?\s*(\\theta|[xyzθt])|d\s*(\\theta|[xyzθt]))'
def integral(t):
 m=re.search(r'\\int\s*(.*?)'+DIFFERENTIAL,t,re.S);assert m,t;v=scalar(m[2] or m[3]);body=scalar(m[1]);assert v in (P.x,P.y,P.z,P.u,P.t) and not body.has(CONST)
 assert {f.args[0] for f in body.atoms(s.Function)}=={v},(t,body,v)
 return body,v
def primitive(body,v):
 out=0
 for term in s.Add.make_args(s.expand(body)):
  found=False
  for f,F in ((s.sin(v),-s.cos(v)),(s.cos(v),s.sin(v)),(s.sec(v)*s.tan(v),s.sec(v)),(s.csc(v)*s.cot(v),-s.csc(v)),(s.sec(v)**2,s.tan(v)),(s.csc(v)**2,-s.cot(v))):
   c=s.cancel(term/f)
   if not c.has(v):out+=c*F;found=True;break
  assert found,('outside fixed-argument direct primitives',term)
 return out
def expression(t):
 t=t.strip().replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');formal=[];z=t
 while r'\int' in z:
  start=z.index(r'\int');m=re.search(r'\\int\s*(.*?)'+DIFFERENTIAL,z[start:],re.S);assert m,z
  body,v=integral(m[0]);formal.append((body,v));val=primitive(body,v)
  z=z[:start]+'('+s.latex(val)+')'+z[start+m.end():]
 return scalar(z),formal
def zero(e):
 # Exact rational trig equality on declared connected intervals avoiding poles.
 args=sorted({f.args[0] for f in e.atoms(s.Function)},key=str);subs={};pairs=[]
 for j,v in enumerate(args):
  A,B=s.symbols('root_s'+str(j)+' root_c'+str(j));pairs.append((A,B));subs.update({s.sin(v):A,s.cos(v):B,s.tan(v):A/B,s.cot(v):B/A,s.sec(v):1/B,s.csc(v):1/A})
 num=s.fraction(s.cancel(e.xreplace(subs)))[0]
 for A,B in pairs:
  if num!=0:num=s.rem(num,A*A+B*B-1,A)
 return s.expand(num)==0
