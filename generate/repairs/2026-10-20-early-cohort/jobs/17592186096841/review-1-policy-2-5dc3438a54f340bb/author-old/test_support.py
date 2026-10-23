import sys,os,json,re,hashlib,importlib.util,platform,subprocess,shutil
from pathlib import Path
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
ROOT=Path('/home/jake/Developer/Course_Academy');E=Path(__file__).resolve().parent;W=E
sys.path.insert(0,str(W))
import generator as g
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
x,t=s.symbols('x t')
def save(name,obj): (E/name).write_text(json.dumps(obj,indent=2,default=str))
def read(name):return json.loads((E/name).read_text())
def parse(v):
 v=v.replace('\\\\','\\').replace('\\left','').replace('\\right','').replace(',','').replace('y=','')
 v=v.replace('{)}',')')
 v=re.sub(r'\^\{([^{}]+)\}',r'^(\1)',v)
 while '\\frac' in v:
  m=re.search(r'\\(?:d?frac)\{([^{}]*)\}\{([^{}]*)\}',v)
  if not m:raise ValueError(v)
  v=v[:m.start()]+'(('+m[1]+')/('+m[2]+'))'+v[m.end():]
 v=re.sub(r'\^\{([^{}]+)\}',r'^(\1)',v).replace('{','').replace('}','')
 return parse_expr(v,local_dict={'x':x,'t':t}, transformations=standard_transformations+(convert_xor,implicit_multiplication_application))
def expected(q):
 p=q[':question/problem']
 if 'f(x)=' in p.replace(' ',''):
  f=re.search(r'f\(x\)\s*=\s*(.*?)\$',p)[1].rstrip('.,');v=x
 else:f=re.search(r'\[([^\]]+)\]',p)[1];v=t
 f=parse(f);d=s.diff(f,v)
 point=re.search(r'point\s*\$\(([-\d]+),([^)]*)\)',p)
 if point:
  z=int(point[1]);y=parse(point[2]);assert s.expand(f.subs(v,z)-y)==0
  return s.expand(d.subs(v,z)*v+y-d.subs(v,z)*z) if 'equation' in p else d.subs(v,z)
 return s.expand(d)
def correct(q):
 f=q[':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else c[':answer/id']
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def check_record(r):
 q=r['question'];e=expected(q);f=q[':question/answer-fields'][0];vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 matches=[a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if s.expand(v-e)==0]
 return {'id':q[':question/id'],'template':r['generation']['template'],'expected':str(e),'key_correct':s.expand(parse(correct(q)[':answer/value'])-e)==0,'unique_correct':len(matches)==1,'distinct':len({str(s.expand(v)) for v in vals})==len(vals)}
def make_grading(r,label):
 q=r['question'];f=q[':question/answer-fields'][0];e=expected(q)
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if s.expand(parse(a[':answer/value'])-e)==0 else 'rejected','purpose':'independently differentiated displayed prompt'} for a in f[':answer-field/choices']]
 else:
  checks=[{'submitted':v,'expected':out,'purpose':purpose} for v,out,purpose in [(correct(q)[':answer/value'],'accepted','displayed factored form'),(s.sstr(s.expand(e)).replace('**','^'),'accepted','expanded polynomial'),(s.sstr(s.factor(e)).replace('**','^'),'accepted','alternative factored expression'),(s.sstr(s.expand(e+1)).replace('**','^'),'rejected','off-by-one polynomial'),('0','accepted' if e==0 else 'rejected','zero response')]]
 return {'label':label,'record':r,'checks':checks}
