"""Independent readback of printed straight-segment scalar-integral components."""
import importlib.util,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent
def mod(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);sys.modules[n]=m;spec.loader.exec_module(m);return m
p=mod('root_segment_scalar',R/'ode-scalar-parser.py');t=p.t
q=mod('root_segment_vector',R/'qa-vector-line-stages.py')
# This module's helpers use a nonnegative t; keep this oracle's real t throughout.
q.t=t;q.p.locals_['t']=t

def scalar(z):return p.scalar(z.strip().rstrip('.,').replace('[','(').replace(']',')').replace(r'\cdot','*').replace(r'\quad','').replace(r'\!',''))
def same(a,b):return s.simplify(s.trigsimp(s.expand(a-b)))==0
def vec(z,n):return tuple(p.vector(z.strip().rstrip('.,').replace('[','(').replace(']',')'))[:n])
def blocks(sol):return re.findall(r'\$\$(.*?)\$\$',sol,re.S)
def rows(b):return q.rows(b)
def brace(z):return q.group(z)
def complete(z):
 z=re.sub(r'\\int_([0-9])\^([0-9])',lambda m:r'\int_{'+m[1]+'}^{'+m[2]+'}',z);z=z.replace(r'\displaystyle','').replace(r'{\int }',r'\int').replace(r'\text{d}', 'd').replace(r'\mathrm{d}','d').strip().rstrip('.,')
 if r'\int_' not in z:return scalar(z)
 co,tail=z.split(r'\int_',1);co=scalar(co) if co.strip() else s.Integer(1)
 lo,tail=brace(tail);assert tail.startswith('^');hi,tail=brace(tail[1:]);lo,hi=scalar(lo),scalar(hi)
 axis=p.u if re.search(r'du$',tail.strip()) else t
 tail=re.sub(r'\\,\s*d[tu]$|\s*d[tu]$', '',tail.strip());tail=re.sub(r'\\cdot\s*$','',tail)
 return co*s.Integral(scalar(tail),(axis,lo,hi))
def value(z):
 z=complete(z) if isinstance(z,str) else z
 return s.simplify(z.doit())
def integral_equal(a,b):
 # Equality of complete integrals includes coefficient and bounds. Keeps
 # invalid raw source options as formal evidence rather than claiming convergence.
 a,b=complete(a),complete(b)
 ia=list(a.atoms(s.Integral));ib=list(b.atoms(s.Integral))
 if not ia and not ib:return same(a,b)
 assert len(ia)==len(ib)==1
 return ia[0].limits==ib[0].limits and same(a/ia[0]*ia[0].function,b/ib[0]*ib[0].function)
def objects(prompt,n):
 match=re.search(r'f\(x,\s*y(?:,\s*z)?\)\s*=\s*(.*?)\$',prompt)
 if match:f=scalar(match[1])
 else:
  body=next(z for z in re.findall(r'\$([^$]+)\$',prompt) if r'\int' in z);body=body.replace(r'\displaystyle','').replace(r'{\int }',r'\int').replace(r'\int_(C)',r'\int_C');body=re.sub(r'\\int_(?:\{C\}|C)','',body);body=body.replace(r'\text{d}', 'd').replace(r'\mathrm{d}', 'd').replace(r'\,','').strip();assert body.endswith('ds');f=scalar(body[:-2])
 pts=re.search(r'from \$\((.*?)\)\$ to \$\((.*?)\)',prompt).groups();A,B=[tuple(scalar(v) for v in z.split(',')) for z in pts];assert len(A)==len(B)==n
 r=tuple(a+t*(b-a) for a,b in zip(A,B));dr=tuple(b-a for a,b in zip(A,B));speed=s.sqrt(sum(v*v for v in dr));h=s.simplify(f.subs(dict(zip((p.x,p.y,p.z),r)),simultaneous=True))
 return f,A,B,r,dr,speed,h

def derivative_vec(z,n):
 z=z.replace(r'\mathrm{d}',r'\text{d}');prefix=r'\frac{\text{d}}{\text{d}t}'
 while prefix in z:
  j=z.index(prefix);tail=z[j+len(prefix):];assert tail.startswith('(')
  body,end=q.outer(tail)[0],None
  # Get first balanced complete parenthesized derivative argument.
  depth=0
  for k,c in enumerate(tail):
   depth+=(c=='(')-(c==')')
   if depth==0:end=k+1;break
  body=tail[1:end-1];z=z[:j]+'('+s.latex(s.diff(scalar(body),t))+')'+tail[end:]
 return vec(z,n)
def stages(sol,f,A,B,r,dr,speed,h,n):
 C=dict(parametrization_rows=0,derivative_components=0,speed_rows=0,pullback_rows=0,setup_integrals=0,endpoint_prose=0)
 bs=blocks(sol);assert len(bs)>=5
 ra,rd,rf,ri=map(rows,bs[1:5]);avec='+'.join('('+s.latex(v)+')'+a for v,a in zip(A,'ijk'));bvec='+'.join('('+s.latex(v)+')'+a for v,a in zip(B,'ijk'))
 for z in ra:
  z=re.sub(r'\ba\b',lambda _: '('+avec+')',z);z=re.sub(r'\bb\b',lambda _: '('+bvec+')',z);assert all(same(v,w) for v,w in zip(vec(z,n),r)),('parameterization',z,r);C['parametrization_rows']+=1
 coord=re.search(r'Thus, we have that \$x=(.*?)\$.*?\$y=(.*?)\$(?:.*?\$z=(.*?)\$)? along the segment',sol)
 assert coord
 for z,w in zip(coord.groups()[:n],r):assert z is not None and same(scalar(z),w);C['endpoint_prose']+=1
 assert len(rd)>=6
 assert re.findall(r'\{d\}([xyz])',rd[0])==list('xyz'[:n])
 for got in (derivative_vec(rd[1],n),vec(rd[2],n)):
  assert all(same(v,w) for v,w in zip(got,dr));C['derivative_components']+=n
 for z in rd[4:]:assert same(scalar(z),speed),('speed',z,speed);C['speed_rows']+=1
 for z in rf:assert same(scalar(z),h),('pullback',z,h);C['pullback_rows']+=1
 assert len(ri)>=3
 for z in ri[1:3]:assert integral_equal(z,s.latex(speed)+r'\int_{0}^{1}'+s.latex(h)+r'\,dt'),('setup',z,speed,h);C['setup_integrals']+=1
 return C,bs,ri

def mask(text):
 text=re.sub(r'\$\$.*?\$\$','@DISPLAY@',text,flags=re.S);return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',text)).strip()
