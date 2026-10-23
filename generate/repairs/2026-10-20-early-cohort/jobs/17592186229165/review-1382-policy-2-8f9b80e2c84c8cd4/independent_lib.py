"""Independent read-only generator audit. Run with the job's Python interpreter."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys, json, re, importlib.util, pathlib, hashlib, collections, subprocess
sys.dont_write_bytecode=True
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
ROOT=pathlib.Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(name,value):
 (ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
spec=importlib.util.spec_from_file_location('reviewed_generator',JOB/'workspace/17592186229165.py')
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
x=S.Symbol('x',real=True)
def texparse(t):
 t=t.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\alpha','a').replace(r'\beta','b')
 def group(pos):
  assert t[pos]=='{',t[pos:]
  depth=1;end=pos+1
  while depth:
   depth+=(t[end]=='{')-(t[end]=='}');end+=1
  return t[pos+1:end-1],end
 while r'\frac' in t:
  p=t.index(r'\frac');a,e=group(p+5);b,e2=group(e)
  t=t[:p]+'(('+str(texparse(a))+')/('+str(texparse(b))+'))'+t[e2:]
 t=t.replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(t,local_dict={'x':x,'e':S.E,'a':S.Symbol('a'),'b':S.Symbol('b')},transformations=standard_transformations+(implicit_multiplication_application,))
def answers(r):return [a[':answer/value'] for a in r['question'][':question/answer-fields'][0].get(':answer-field/choices',[])]
def params_from_prompt(r):
 text=r['question'][':question/problem']
 eq=text.split('$$')[1].split(r',\,')[0]
 lhs,rhs=eq.split('=');coeff=lhs.split('′}')[1].replace('y','');hc=texparse(coeff+'1' if coeff in ['+','-'] else coeff)
 v=int(re.search(r'y\(0\)=(-?\d+)',text)[1])
 return -hc,texparse(rhs),v
def checkmath(r):
 h,forcing,v=params_from_prompt(r)
 rows=[]
 for ans in answers(r):
  y=texparse(ans)
  rows.append({'answer':ans,'ode_residual':str(S.simplify(S.diff(y,x)-h*y-forcing)),'initial_residual':str(S.simplify(y.subs(x,0)-v))})
 # Last displayed solution must independently match the answer bank.
 last=re.findall(r'\$\$\s*(.*?)\s*\$\$',r['question'][':question/worked-solution'],re.S)[-1]
 ylast=texparse(last.split('=',1)[1]);final_ok=all(S.simplify(ylast-texparse(a))==0 for a in answers(r))
 return {'id':r['question'][':question/id'],'parameters_from_prompt':{'h':str(h),'forcing':str(forcing),'v':v},'answers':rows,'final_solution_matches':final_ok,'passed':final_ok and all(z['ode_residual']=='0' and z['initial_residual']=='0' for z in rows)}

