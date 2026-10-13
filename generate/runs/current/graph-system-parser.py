"""Root reads displayed two-line systems independently of sampled coordinates."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('root_graph_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,y=p.x,p.y
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def blocks(text):return [(v[2:-2] if v.startswith('$$') else v[1:-1]).strip().rstrip('.,') for v in MATH.findall(text)]
def row(raw):
 a,b=raw.replace('&','').strip().split('=');e=s.expand(p.scalar(a)-p.scalar(b));P=s.Poly(e,x,y);assert P.total_degree()==1
 vals=[e.coeff(x),e.coeff(y),-e.subs({x:0,y:0})];scale=s.ilcm(*[v.q for v in vals]);ints=[int(v*scale) for v in vals];g=s.igcd(*ints);ints=[v//g for v in ints]
 if next(v for v in ints if v)!=abs(next(v for v in ints if v)):ints=[-v for v in ints]
 return tuple(ints)
def system(text):
 bs=blocks(text);body=next(b for b in bs if 'x' in b and 'y' in b and '=' in b)
 if r'\begin{array}' in body:body=body.split(r'\begin{array}{l}',1)[1].split(r'\end{array}',1)[0];rs=body.split(r'\\')
 else:rs=body.lstrip('{').split(';')
 assert len(rs)==2;rows=tuple(row(r) for r in rs);A=s.Matrix([r[:2] for r in rows]);assert A.det()!=0;answer=tuple(A.inv()*s.Matrix([r[2] for r in rows]));return rows,answer
def solution_points(text):
 points=[]
 for b in blocks(text):
  if b.startswith('(') and b.endswith(')') and ',' in b:
   values=tuple(p.scalar(v) for v in b[1:-1].split(','));assert len(values)==2;points.append(values)
 return points
