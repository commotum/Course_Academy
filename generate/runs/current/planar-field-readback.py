"""Parent's literal displayed vector-field/parser and qualitative predicates."""
import importlib.util,re
from pathlib import Path
sp=importlib.util.spec_from_file_location('root_planar_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p);s=p.s;x,y=p.x,p.y

def scalar(raw):
 raw=re.sub(r'\|([^|]+)\|',r'Abs(\1)',raw).replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin')
 return p.scalar(raw.replace(r'\!',''))
def vector(raw):
 val=s.expand(scalar(raw));pair=(val.coeff(p.i),val.coeff(p.j));assert s.simplify(val-pair[0]*p.i-pair[1]*p.j)==0,raw;return pair

def formula(raw):
 m=re.fullmatch(r'([A-Za-z])\(\s*x\s*,\s*y\s*\)\s*=\s*(.*)',raw.strip().rstrip('.,'));assert m,raw;return m[1],vector(m[2])
def spans(text):return [a or b for a,b in re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*)\$',text)]
def formulas(text):
 out=[]
 for body in spans(text):
  for chunk in re.split(r'\\,\s*(?=[A-Za-z]\()',body):
   chunk=chunk.strip()
   if re.match(r'^[A-Za-z]\(\s*x\s*,\s*y\s*\)\s*=',chunk):out.append(formula(chunk))
 return out

def prose_predicates(text):
 predicates=[]
 # Constant all-location sign statements.
 for axis,sign in re.findall(r'(horizontal|vertical) component.*?is (positive|negative|zero) for',text):
  idx=0 if axis=='horizontal' else 1
  def predicate(pair,idx=idx,sign=sign):
   e=pair[idx];return not e.free_symbols and (e>0 if sign=='positive' else e<0 if sign=='negative' else e==0)
  predicates.append(predicate)
 # Location-dependent component magnitude, holding the other coordinate fixed.
 for dep,axis in re.findall(r'(?:move away from the origin in the|As we move away from the origin in the) (horizontal|vertical) direction, (?:our vectors\x27|their) (horizontal|vertical) components.*?get longer',text):
  var=x if dep=='horizontal' else y;idx=0 if axis=='horizontal' else 1
  def predicate(pair,var=var,idx=idx):
   e=pair[idx];return e.free_symbols=={var} and s.Poly(e,var).degree()==1 and e.subs(var,0)==0
  predicates.append(predicate)
 for axis,sign,var in re.findall(r'(horizontal|vertical) component is (positive|negative) where \$(x|y)>0',text):
  idx=0 if axis=='horizontal' else 1;var=x if var=='x' else y
  def predicate(pair,var=var,idx=idx,sign=sign):
   e=pair[idx];return e.free_symbols=={var} and e.subs(var,0)==0 and s.Poly(e,var).degree()==1 and (e.coeff(var)>0 if sign=='positive' else e.coeff(var)<0)
  predicates.append(predicate)
 assert predicates,text;return predicates
