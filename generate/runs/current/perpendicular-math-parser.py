"""Parent reader for displayed line equations; independent of worker helpers."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_perp_scalar',Path(__file__).with_name('vector-math-parser.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def blocks(text):
 return [m[0][2:-2] if m[0].startswith('$$') else m[0][1:-1] for m in MATH.finditer(text)]
def math(raw):
 raw=raw.strip().rstrip('.,?').replace('&','')
 # Preserve TeX command names while mapping source parameter symbols to
 # already-supported, distinct variables. Implicit px/qx remain products.
 raw=re.sub(r'\\[A-Za-z]+|[pq]',lambda m:m[0] if m[0].startswith('\\') else {'p':'u','q':'v'}[m[0]],raw)
 return p.scalar(raw)
def equation(raw):
 assert raw.count('=')==1,raw
 lhs,rhs=raw.split('=');return s.expand(math(lhs)-math(rhs))
def equivalent(a,b):
 A=s.Poly(a,p.x,p.y);B=s.Poly(b,p.x,p.y)
 if A.is_zero or B.is_zero:return A.is_zero and B.is_zero
 if A.monoms()!=B.monoms():return False
 ratio=s.cancel(A.coeffs()[0]/B.coeffs()[0]);return ratio!=0 and s.simplify(a-ratio*b)==0
def normal(expression):
 poly=s.Poly(expression,p.x,p.y);assert poly.total_degree()==1,expression
 A=poly.coeff_monomial(p.x);B=poly.coeff_monomial(p.y);assert A!=0 or B!=0
 return A,B
def perpendicular(a,b):
 A,B=normal(a);C,D=normal(b);return s.simplify(A*C+B*D)==0
def prompt_lines(text):
 return [equation(z) for z in blocks(text) if z.count('=')==1 and ('x' in z or 'y' in z)]
def parameter_constraint(lines):
 assert len(lines)==2
 A,B=normal(lines[0]);C,D=normal(lines[1]);constraint=s.expand(A*C+B*D)
 unknowns=constraint.free_symbols;assert len(unknowns)==1,(lines,constraint)
 parameter=next(iter(unknowns));solutions=s.solve(constraint,parameter);assert len(solutions)==1
 result=solutions[0];assert result.is_real is True and result.is_finite is True
 assert all(normal(z.subs(parameter,result))!=(0,0) for z in lines)
 return parameter,result,constraint
def stage_checks(solution,lines,parameter=None,result=None):
 counts={'conversion_rows':0,'numerical_equalities':0,'parameter_equalities':0,'explicit_slope_claims':0}
 subs={parameter:result} if parameter is not None else {}
 for body in blocks(solution):
  if r'\begin{aligned}' in body:
   rows=body.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
   for row in rows:
    expr=equation(row)
    assert any(equivalent(expr,line) for line in lines),('Printed conversion',row,lines)
    counts['conversion_rows']+=1
  elif '=' in body and not ('x' in body or 'y' in body):
   # Source products may combine a condition and its solved value in one slot.
   for clause in re.split(r'⟹|⇒|\\(?:implies|Rightarrow|Longrightarrow)',body):
    if '=' not in clause:continue
    assert clause.count('=')==1,clause
    lhs,rhs=clause.split('=');a,b=math(lhs),math(rhs)
    assert s.simplify((a-b).subs(subs))==0,('Printed parameter/product step',clause,result)
    counts['parameter_equalities' if (a-b).free_symbols else 'numerical_equalities']+=1
 for match in re.finditer(r'line \$(.*?)\$[^$\n]*?(?:slope is|slope of| is) \$([^$]+)\$',solution):
  if match[1].count('=')!=1:continue
  A,B=normal(equation(match[1]));assert B!=0 and s.simplify(math(match[2])+A/B)==0,('Printed slope claim',match.groups())
  counts['explicit_slope_claims']+=1
 return counts
