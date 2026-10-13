"""Root compares first integrals as complete arbitrary-constant relations."""
import importlib.util
from pathlib import Path
import sympy as s
sp=importlib.util.spec_from_file_location('root_implicit_base',Path(__file__).with_name('separable-ode-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
x,y,C,K=p.x,p.y,p.C,p.K
def relation(raw):
 E=p.equation(raw);assert not E.has(p.D)
 coef=s.diff(E,C)
 assert coef!=0 and not coef.has(x,y,C,K) and s.diff(E,C,2)==0,(raw,'nonadditive constant')
 return s.simplify(E-coef*C),coef
def positive_radicals(E,rhs):
 bases=set()
 for node in s.preorder_traversal(rhs):
  if isinstance(node,s.Pow) and node.exp.is_Rational and node.exp.q%2==0:
   base=node.base
   if sum(base.has(var) for var in (x,y))==1 and all(s.diff(base,var,2)==0 for var in (x,y)):bases.add(base)
 return p.on_positive_components(E,tuple(sorted(bases,key=str)))
def radical_conditions(rhs):
 return tuple(sorted({node.base for node in s.preorder_traversal(rhs) if isinstance(node,s.Pow) and node.exp.is_Rational and node.exp.q%2==0 and sum(node.base.has(var) for var in (x,y))==1 and all(s.diff(node.base,var,2)==0 for var in (x,y))},key=str))
def valid(raw,rhs):
 H,coef=relation(raw);Y=p.derivative(H,y)
 if Y==0:return False
 residual=p.derivative(H,x)+Y*rhs
 return p.equal(positive_radicals(residual,rhs),s.Integer(0))
def family_equal(a,b):
 A,c=relation(a);B,d=relation(b);difference=A/c-B/d
 return p.equal(p.derivative(difference,x),s.Integer(0)) and p.equal(p.derivative(difference,y),s.Integer(0))
