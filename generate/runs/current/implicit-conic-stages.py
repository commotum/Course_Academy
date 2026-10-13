"""Root actual conic equations and every formal implicit-derivative input/stage."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('p',Path(__file__).with_name('conic-slope-readback.py'));p=importlib.util.module_from_spec(z);z.loader.exec_module(p)
x,y=p.x,p.y;M=p.p.u
D=r'\frac{\text{d}y}{\text{d}x}';OP=r'\frac{\text{d}}{\text{d}x}'
def scalar(t):return p.scalar(t.strip().rstrip('.,'))
def same(a,b):return s.cancel(a-b)==0

def parse_solution(solution):
 displays=re.findall(r'\$\$\s*(.*?)\s*\$\$',solution,re.S);assert len(displays)==2
 equations=displays[0].split('⟹');curves=[]
 for eq in equations:
  a,b=eq.split('=');left,right=scalar(a.replace(r'\,','')),scalar(b.replace(r'\,',''));curves.append(left-right)
 curve=s.expand(curves[-1]);alpha,beta=curve.coeff(x,2),curve.coeff(y,2);assert alpha>0 and beta>0 and curve.coeff(x*y)==0
 h,k=-curve.coeff(x)/(2*alpha),-curve.coeff(y)/(2*beta);at=s.simplify(curve.subs({x:h,y:k}));a,b=s.sqrt(-at/alpha),s.sqrt(-at/beta);assert a>0 and b>0
 for c in curves:
  ratio=s.cancel(c/curve);assert ratio.free_symbols==set() and ratio!=0
 # The last displayed standard equation is the exact formal operator input.
 last=equations[-1].split('=');lhs,rhs=[scalar(t.replace(r'\,','')) for t in last];answer=p.slope(curve);inputs=[];rows=displays[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
 def read(text,ops):
  while OP in text:
   pos=text.index(OP);start=pos+len(OP);assert text[start]=='(';depth=1;i=start+1
   while depth:
    depth+=(text[i]=='(')-(text[i]==')');i+=1
   arg=scalar(text[start+1:i-1]);ops.append(arg);derivative=s.diff(arg,x)+s.diff(arg,y)*M
   text=text[:pos]+'('+s.latex(derivative)+')'+text[i:]
  return scalar(text.replace(D,'u'))
 for j,row in enumerate(rows):
  lt,rt=row.split('&',1);assert rt.strip().startswith('=');ops=[];A,B=read(lt,ops),read(rt.strip()[1:],ops);assert same((A-B).subs(M,answer),0),(row,answer)
  if j==0:assert len(ops)==2 and same(ops[0],lhs) and same(ops[1],rhs)
  elif j==1:
   assert len(ops)==2 and same(ops[0],alpha*(x-h)**2) and same(ops[1],beta*(y-k)**2)
  else:assert not ops
  inputs+=ops
 assert len(inputs)==4
 assert same(read(rows[-1].split('&',1)[1].strip()[1:],[]),answer)
 # Read the stated center/lengths in the prose as well as the equation.
 if 'centered at the origin' in solution:assert h==k==0
 else:
  center=re.search(r'centered at \$\((.*?),(.*?)\)\$',solution);assert center and same(scalar(center[1]),h) and same(scalar(center[2]),k)
 if 'radius of' in solution:
  radius=re.search(r'radius of \$(.*?)\$',solution)[1];assert same(scalar(radius),a) and same(a,b)
 else:
  axes=re.search(r'semiaxes \$(.*?)\$ and \$(.*?)\$',solution);assert axes and same(scalar(axes[1]),a) and same(scalar(axes[2]),b)
 return dict(curve=curve,answer=answer,h=h,k=k,a=a,b=b,formal_inputs=len(inputs),stages=len(rows),equations=len(curves))
