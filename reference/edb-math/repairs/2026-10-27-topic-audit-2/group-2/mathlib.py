import re,sys,functools
import sympy as S
sys.path.insert(0,'/tmp/course-academy-kp17592186192790-checkdeps')
from sympy.parsing.latex import parse_latex
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parents[5]/'scripts'))
from question_capture.math_format import MATH
x,y,z,t,h,C,A,D=S.symbols('x y z t h C A D',real=True)
SYMS={v.name:v for v in [x,y,z,t,h,C,A,D]}
def clean(v):
 v=str(v).strip().strip('$');v=v.replace('∂',r'\partial ').replace('π',r'\pi ').replace('∞',r'\infty ').replace('−','-').replace('⁡','').replace('⁢','').replace('∈',r'\in ').replace('′',r'\prime ')
 v=re.sub(r'\\(?:text|textrm|mathrm|rm)\s*\{\s*d\s*\}', 'd',v);v=re.sub(r'\\(?:textrm|mathrm|rm)\s+d\b','d',v)
 v=re.sub(r'\\operatorname\s*\{(sin|cos|tan|sec|csc|cot|ln|log|exp|sinh|cosh|arcsin|arccos|arctan)\}',lambda m:'\\'+m[1]+' ',v)
 v=re.sub(r'\\color\{[^{}]*\}|\\hspace\{[^{}]*\}|\\(?:displaystyle|textstyle|quad|qquad)\b','',v);v=re.sub(r'\\[,;!:]',' ',v)
 v=re.sub(r'(\\(?:ln|log)\s*\{\([^{}]*\)\})\s*\^\s*\{([0-9]+)\}',r'(\1)^{\2}',v)
 v=re.sub(r'([xy])\\prime\s*',lambda m:m[1]+"'",v)
 v=re.sub(r'\\int(?=[A-Za-z])',lambda m:m[0]+' ',v)
 v=re.sub(r'\{?([xy])\}?\s*\^\s*\{\s*\\prime\s*\}',r"\1'",v)
 v=re.sub(r'(?<![A-Za-z])\{(sin|cos|tan|sec|csc|cot|ln|log|exp)\}(?=\s*\^)',lambda m:'\\'+m[1]+' ',v)
 v=re.sub(r'\\(?:left|right|big|Big|bigg|Bigg)(?:[lrm])?\b','',v)
 v=re.sub(r'\{\s*(\\(?:sin|cos|tan|sec|csc|cot|ln|log|exp))\s*\}',r'\1 ',v)
 v=re.sub(r'\\frac\\pi\s*([0-9])',r'\\frac{\\pi}{\1}',v)
 # x(y+h) is multiplication in multivariable formulas. ODE y(x) is handled before parsing.
 v=re.sub(r'(?<![A-Za-z\\_])([xyz])\s*\(',r'\1\\cdot(',v)
 v=re.sub(r"\{?([xy])\}?\s*\^\s*\{\s*'\s*\}",r"\1'",v)
 return v.rstrip('.,?; ')
@functools.lru_cache(maxsize=30000)
def parse(v):
 expr=parse_latex(clean(v),strict=True)
 reps={s:SYMS.get(s.name,S.E if s.name=='e'else S.pi if s.name=='pi'else s)for s in expr.atoms(S.Symbol)}
 expr=expr.xreplace(reps)
 for app in list(expr.atoms(S.Function)):
  if app.func.__name__ in ['pi','e'] and len(app.args)==1:expr=expr.xreplace({app:(S.pi if app.func.__name__=='pi'else S.E)*app.args[0]})
 return expr

def maths(v):return [(m,m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1])for m in MATH.finditer(v)]
def rhs(v):
 e=parse(v)
 return e.rhs if isinstance(e,S.Equality)else e

def simple(v):return S.simplify(S.trigsimp(v))
def equivalent(a,b):return simple(a-b)==0

def equation(v):
 v=re.sub(r"y\s*'",'D',clean(v))
 e=parse(re.sub(r'y\s*\(\s*x\s*\)', 'y',v))
 if not isinstance(e,S.Equality):raise ValueError('No equality')
 f=e.lhs-e.rhs
 for deriv in list(f.atoms(S.Derivative)):
  if str(deriv.expr)in ['y','y(x)']and len(deriv.variables)==1:f=f.xreplace({deriv:D})
 f=f.xreplace({s:D for s in f.free_symbols if s.name in ["y'",'yprime']})
 for app in list(f.atoms(S.Function)):
  if app.func.__name__=='y'and app.args==(x,):f=f.xreplace({app:y})
 return f

def ode(problem):
 failures=[]
 for _,v in maths(problem):
  vv=clean(v)
  if not re.search(r"dy|y\s*'",vv):continue
  # Initial values and explicit domain clauses follow the ODE in the same display.
  vv=vv.split(',',1)[0]
  vv=re.split(r',\s*(?:y\s*\(|[xy]\s*\\(?:gt|ge|ne)|[xy]\s*[><])',vv)[0]
  try:f=equation(vv)
  except Exception as ex:failures.append(str(ex));continue
  if D in f.free_symbols:return f,vv
 raise ValueError('No parseable first-order ODE: '+str(failures)[:150])

def explicit_solution(v):
 e=parse(re.sub(r'^y\s*\(\s*x\s*\)\s*=', 'y=',v))
 if isinstance(e,S.Equality):
  if e.lhs==y or getattr(e.lhs,'func',None).__name__=='y':return e.rhs
  raise ValueError('Solution is implicit')
 return e

def residual(f,sol):return simple(f.subs({y:sol,D:S.diff(sol,x)},simultaneous=True))

def initial_values(problem):
 out=[]
 for _,v in maths(problem):
  for m in re.finditer(r'y\s*\(([^()]*)\)\s*=\s*([^,;\n]+)',clean(v).replace(r'y\cdot(', 'y(')):
   try:xx=parse(m[1]);yy=parse(m[2]);
   except Exception:continue
   if not xx.free_symbols and not yy.free_symbols:out.append((xx,yy))
 return list(dict.fromkeys(out))
