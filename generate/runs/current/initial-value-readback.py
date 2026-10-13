"""Root actual supplied-family and initial-condition readback; no generator helpers."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('p',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(z);z.loader.exec_module(p)
x=p.x;y=p.y;A=p.u

def scalar(t):return p.scalar(t.strip().rstrip('.,?').replace('A','u'))
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0

def math_spans(t):return re.findall(r'\$\$\s*(.*?)\s*\$\$|(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',t,re.S)
def read_problem(prompt):
 spans=[a or b for a,b in math_spans(prompt)];ode=spans[0];rhs=scalar(ode.split('=',1)[1].split(',')[0]);condition=ode.split(',',1)[1].replace(r'\,','').strip();m=re.search(r'y\((.*?)\)\s*=\s*(.*)',condition,re.S);assert m,condition;point,value=scalar(m[1]),scalar(m[2]);family=scalar(spans[1].split('=',1)[1]);solutions=s.solve(s.Eq(family.subs(x,point),value),A);assert len(solutions)==1;answer=solutions[0]
 assert equal(s.diff(family,x),rhs.subs(y,family));assert equal(family.subs({x:point,A:answer},simultaneous=True),value)
 for expr in (family.subs({x:point,A:answer}),rhs.subs({x:point,y:value})):
  assert expr.is_real is not False and not expr.has(s.zoo,s.nan,s.oo)
 for log in family.atoms(s.log):assert s.simplify(log.args[0].subs({x:point,A:answer})).is_positive
 return rhs,point,value,family,answer

def check_solution(solution,problem):
 rhs,point,value,family,answer=problem;n=0
 for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',solution,re.S):
  if r'\begin{aligned}' not in block:
   assert block.startswith('y=') or block.startswith('y ='),block;assert all(equal(scalar(z),family.subs(A,answer)) for z in block.split('=')[1:]);n+=len(block.split('='))-1;continue
  rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
  for index,row in enumerate(rows):
   left,right=row.strip().split('& =',1)
   if index==0:assert scalar(left)==y and equal(scalar(right),family)
   else:
    a,b=scalar(left),scalar(right);assert not a.has(x) and not b.has(x),'Printed substitution row retains x'
    assert equal(a.subs(A,answer),b.subs(A,answer)),(row,answer)
   n+=1
 for tex in [a or b for a,b in math_spans(solution) if a or b]:
  if r'\begin{aligned}' in tex:continue
  tex=tex.replace(r'\,','').strip()
  if tex.startswith('y('):
   m=re.fullmatch(r'y\((.*?)\)=(.*)',tex.rstrip('.'));assert m and equal(scalar(m[1]),point) and equal(scalar(m[2]),value)
  elif tex.startswith('y=') or tex.startswith('y ='):assert all(equal(scalar(z),family.subs(A,answer)) or equal(scalar(z),family) for z in tex.split('=')[1:])
 return n
