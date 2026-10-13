"""Root's actual-prompt oracle for categorical perpendicular axis lines."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_axis_equation',Path(__file__).with_name('perpendicular-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
def fractions(raw):
 return re.sub(r'(?<![\d.])(\d+)\.(\d+)(?![\d.])',lambda m:r'\frac{'+str(int(m[1]+m[2]))+'}{'+str(10**len(m[2]))+'}',raw.strip().rstrip('.,?'))
def math(raw):return p.math(fractions(raw))
def equation(raw):return p.equation(fractions(raw))
def read(prompt):
 lines=[equation(z) for z in p.blocks(prompt) if z.count('=')==1 and ('x' in z or 'y' in z)];assert len(lines)==1
 reference=lines[0];A,B=p.normal(reference);assert (A==0)!=(B==0)
 raw=re.search(r'point \$\((.*?)\)',prompt);assert raw,prompt
 point=tuple(math(v) for v in raw[1].split(','));assert len(point)==2
 variable=p.p.y if B==0 else p.p.x;value=point[1 if B==0 else 0]
 return reference,point,variable,value
def check_solution(solution,reference,point,variable,value):
 counts={'orientation_claims':0,'coordinate_claims':0,'equation_conclusions':0}
 for raw,label in re.findall(r'line \$(.*?)\$ is a (vertical|horizontal) line',solution):
  expr=equation(raw);assert p.equivalent(expr,reference);A,B=p.normal(expr)
  assert label==('vertical' if B==0 else 'horizontal');counts['orientation_claims']+=1
 for raw in re.findall(r'perpendicular line must take the form \$(.*?)\$',solution):
  expr=equation(raw);A,B=p.normal(expr);assert (A==0)==(variable==p.p.y)
 for raw,axis,claimed in re.findall(r'point \$\((.*?)\),\$.*?\$([xy])\$-coordinate of \$(.*?)\$',solution):
  actual=tuple(math(v) for v in raw.split(','));assert actual==point
  assert p.p.locals_[axis]==variable and s.simplify(math(claimed)-value)==0;counts['coordinate_claims']+=1
 for raw in re.findall(r'perpendicular line is \$(.*?)\$',solution):
  assert p.equivalent(equation(raw),variable-value);counts['equation_conclusions']+=1
 return counts
