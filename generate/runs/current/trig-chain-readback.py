"""Root independent trig composition bindings, formal factors and scalar readback."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('root_trig_chain_scalar',Path(__file__).with_name('ode-scalar-parser.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
x,u=P.x,P.u

def group(t,at):
 assert t[at] in '({';depth=1;j=at+1
 while depth:
  assert j<len(t);depth+=(t[j] in '({')-(t[j] in ')}');j+=1
 return t[at+1:j-1],j

def clean(t):
 t=t.strip().rstrip('.,?').replace('′',"'").replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\dfrac',r'\frac').replace(r'\prime',"'")
 t=t.replace(r'\textrm d ',r'\mathrm{d}')
 t=re.sub(r'\\(?:text|mathrm)\{d\}\s*',r'\\mathrm{d}',t)
 t=re.sub(r'\\(?:begin|end)\{aligned\}','',t)
 t=t.replace(r'\qquad',',').replace(r'\quad',',').replace(r'\,\text{and}\,',',').replace(r'\text{and}',',').replace(r'\,',',')
 for cmd in (r'\bbox',r'\eqalign'):
  while cmd in t:
   at=t.index(cmd);start=at+len(cmd)
   if start<len(t) and t[start]=='[':start=t.index(']',start)+1
   arg,end=group(t,start);t=t[:at]+arg+t[end:]
 return t

def scalar(t):return P.scalar(clean(t).replace('[','(').replace(']',')'))
def eq(a,b):
 delta=s.expand(a-b)
 if delta==0:return True
 return s.simplify(s.trigsimp(delta,method='fu'))==0

def givens(prompt):
 t=clean(prompt)
 m=re.search(r'\$(?:f\(x\)|y)\s*=\s*(.*?)\$',t);assert m,prompt
 fun=scalar(m[1]);at=None;y0=None
 target=re.search(r'at (?:the point where )?\$x\s*=\s*(.*?)\$',t)
 if target:at=scalar(target[1])
 else:
  target=re.search(r'at the point \$(.*?)\$',t)
  if target:
   coords=target[1].strip().rstrip('.')
   if coords.startswith('(') and coords.endswith(')'):coords=coords[1:-1]
   pieces=coords.split(',');assert len(pieces)==2
   at,y0=map(scalar,pieces);assert eq(fun.subs(x,at),y0)
 return fun,at,y0

def bindings(sol,fun):
 # Read the printed auxiliary definition; the original direct split sum keeps g/h.
 text=clean(sol)
 defs={name:scalar(value) for name,value in re.findall(r'\$([gh])\(x\)=(.*?)\$',text)}
 defs.setdefault('f',fun);defs.setdefault('y',fun)
 if 'g' in defs:assert 'h' in defs and eq(defs['g']+defs['h'],fun)
 m=re.search(r'(?:\$\$|\\\[)\s*([fgy])\s*=\s*(.*?)\s*,+\s*u\s*=\s*(.*?)\s*(?:\$\$|\\\])',text,re.S);assert m,sol
 label,outer,inner=m[1],scalar(m[2]),scalar(m[3]);assert outer.free_symbols<={u} and inner.free_symbols<={x}
 assert eq(outer.subs(u,inner),defs[label]);return defs,label,outer,inner

def value(raw,defs,label,outer,inner):
 text=clean(raw).strip().rstrip('.,')
 pattern=r'\\frac\{\\mathrm\{d\}([fgyuh])\}\{\\mathrm\{d\}([xu])\}'
 def formal(m):
  name,var=m[1],m[2]
  if name=='u':assert var=='x';result=s.diff(inner,x)
  elif var=='u':assert name==label or name in ('f','y') and label in ('f','y');result=s.diff(outer,u)
  else:result=s.diff(defs[name],x)
  return '('+s.latex(result)+')'
 text=re.sub(pattern,formal,text)
 # Scalar f/g/h and their concrete prime evaluation inputs.
 def named(m):
  name,isprime,arg=m[1],bool(m[2]),m[3];expr=defs[name];expr=s.diff(expr,x) if isprime else expr;return '('+s.latex(expr.subs(x,scalar(arg)))+')'
 text=re.sub(r'\{?([fgyh])\}?(\^\{\x27\}|\x27)?\((.*?)\)',named,text)
 text=re.sub(r'\{?([fygh])\}?(?:\^\{\x27\}|\x27)',lambda m:'('+s.latex(s.diff(defs[m[1]],x))+')',text)
 if text=='m':return s.Symbol('m')
 if text=='y':return defs['y']
 return scalar(text)
