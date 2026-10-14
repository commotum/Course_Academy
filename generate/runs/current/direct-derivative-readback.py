"""Root independent direct-derivative reader; displayed formal operands and actual points."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('root_direct_scalar',Path(__file__).with_name('ode-scalar-parser.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
x=P.x
DERS=[r'\frac{\text{d}}{\text{d}x}',r'\frac{\mathrm{d}}{\mathrm{d}x}',r'\frac{d}{dx}']
def clean(t):
 t=t.strip().rstrip('.,?').replace('′',"'").replace('⁡','').replace(r'\left','').replace(r'\right','');t=re.sub(r'\\\\(?=(?:frac|sqrt)\b)',r'\\',t)
 return t

def group(t,at):
 assert t[at] in '({';end=at+1;depth=1
 while depth:
  assert end<len(t);depth+=(t[end] in '({')-(t[end] in ')}');end+=1
 return t[at+1:end-1],end

def scalar(t):return P.scalar(clean(t))
def eq(a,b):
 delta=s.expand(a-b)
 if delta==0:return True
 return s.simplify(s.trigsimp(delta,method='fu'))==0

def given(prompt):
 m=re.search(r'\$(f\(x\)|y)\s*=\s*(.*?)\$',prompt)
 if m:name=m[1][0];fun=scalar(m[2])
 else:
  m=re.search(r'\$(?:\\frac\{(?:\\text\{d\}|d)\}\{(?:\\text\{d\}x|dx)\})\(',prompt);assert m,prompt
  funraw,end=group(prompt,m.end()-1);fun=scalar(funraw);name=None
 point=None
 for m in re.finditer(r'\$x\s*=\s*(.*?)\$',prompt):point=scalar(m[1])
 if point is not None:
  assert not point.free_symbols and fun.subs(x,point).is_finite
  if fun.has(s.tan,s.sec):assert s.simplify(s.cos(point))!=0
 return fun,point,name

def value(t,fun,name,counters,raw_wrong_label=False):
 t=clean(t);df=s.diff(fun,x)
 for der in DERS:
  while der in t:
   at=t.index(der);start=at+len(der)
   while start<len(t) and t[start].isspace():start+=1
   operand,end=group(t,start);arg=scalar(operand);counters['formal_derivative_inputs']+=1
   t=t[:at]+'('+s.latex(s.diff(arg,x))+')'+t[end:]
 pattern=r'\\frac\{(?:\\text\{d\}|d)([fy])\}\{(?:\\text\{d\}x|dx)\}|\{?([fy])\}?(?:\^\{\x27\}|\x27)(?:\((.*?)\))?'
 def label(m):
  labelname=m[1] or m[2]
  assert name is None or labelname==name or raw_wrong_label,(t,name,labelname)
  point=scalar(m[3]) if m[3] else x
  return '('+s.latex(df.subs(x,point))+')'
 t=re.sub(pattern,label,t)
 return scalar(t)

def stages(sol,fun,point,name,counters,raw_wrong_label=False):
 df=s.diff(fun,x);blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert blocks
 for index,b in enumerate(blocks):
  prev=None;actualtarget=df if index==0 or point is None else s.simplify(df.subs(x,point))
  for row in b.split(r'\\'):
   parts=row.replace('&','').strip().split('=');assert len(parts)>=2
   if parts[0].strip():a=value(parts[0],fun,name,counters,raw_wrong_label)
   else:assert prev is not None;a=prev
   vals=[value(v,fun,name,counters,raw_wrong_label) for v in parts[1:]]
   assert eq(a,actualtarget) and all(eq(v,actualtarget) for v in vals),(row,vals,actualtarget)
   prev=vals[-1];counters['derivative_equalities']+=len(vals)
  # First formal derivative evaluates the original supplied expression, not an alias.
  if index==0:
   first=b.split(r'\\')[0];der=next((z for z in DERS if z in first),None)
   if der:
    t=clean(first);at=t.index(der)+len(der);operand,_=group(t,at);assert eq(scalar(operand),fun);counters['given_formal_inputs']+=1
 if point is not None:
  assert len(blocks)>=2
  for raw in re.findall(r'(?:Evaluating at|when|at the point) \$x=(.*?)\$',sol):assert eq(scalar(raw),point)
  for raw in re.findall(r'(?:slope|rate of change) is \$(.*?)\$',sol):assert eq(scalar(raw),df.subs(x,point));counters['conclusions']+=1
