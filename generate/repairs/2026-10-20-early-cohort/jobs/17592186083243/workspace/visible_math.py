# Reused visible-prompt differentiation witness from prior review.py.
import os,sys,json,re,hashlib,platform,importlib.metadata,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PKG=ROOT
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(ROOT/'assets')
sys.path[:0]=[str(ROOT/'test-deps'),str(PKG)]
import generator as g
import sympy as s
from sympy.parsing.latex import parse_latex

def save(name,data): (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False))
def parse(v):
 v=v.replace('\u2061','').replace('′',"'")
 v=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc|ln)\}',r'\\\1',v)
 v=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}',r'\\\1',v)
 v=v.replace('\\,','').strip().rstrip('.,')
 v=re.sub(r'(?<![A-Za-z])t\s*(?=\\left\()', r't\\cdot ',v)
 v=v.replace(r'}\left(',r'}\cdot \left(')
 v=re.sub(r'(\\(?:sin|cos|tan|cot|sec|csc)(?:\^\{[0-9]+\})?)\s*\{t\}', r'\1(t)',v)
 z=parse_latex(v)
 return z.xreplace({a:(s.E if a.name=='e' else s.pi) for a in z.free_symbols if a.name in ('e','pi')})
def eq(x,y):return s.simplify(s.trigsimp(x-y))==0

def key(r):
 f=r['question'][':question/answer-fields'][0]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def mathcheck(r):
 q=r['question'];prompt=q[':question/problem'];fields=q[':question/answer-fields'];f=fields[0]
 block=re.findall(r'\$\$(.*?)\$\$',prompt,re.S)[0].strip()
 xs,ys=block[2:].split(r',\,y=');ys=ys.split(r',\,')[0]
 x,y=parse(xs),parse(ys);t=next(v for v in x.free_symbols|y.free_symbols if v.name=='t')
 target=re.search(r'where \$t=(.*?)\.\$',prompt).group(1);u=parse(target)
 dx,dy=s.diff(x,t),s.diff(y,t);m=s.simplify((dy/dx).subs(t,u));vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert dx.subs(t,u)!=0,(xs,ys,target)
 assert eq(parse(key(r)),m),('wrong key',key(r),str(m))
 assert sum(eq(v,m) for v in vals)==1
 assert all(not eq(a,b) for i,a in enumerate(vals) for b in vals[i+1:])
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
 last=blocks[-1].split('& =')[-1].replace(r'\end{aligned}','').strip().rstrip('.')
 assert eq(parse(last),m),('wrong solution',last,str(m))
 # Every displayed ratio and evaluated equality RHS, independently interpreted.
 checks=0
 for bi in [2,3]:
  for row in re.split(r'\\\\\s*&\s*=',blocks[bi].split('& =',1)[1]):
   row=row.replace(r'\end{aligned}','').strip().rstrip('.')
   z=parse(row);target_value=dy/dx if bi==2 else m
   assert eq(z,target_value),('bad displayed equality',bi,row,str(target_value))
   checks+=1
 return {'id':q[':question/id'],'template':r['generation']['template'],'answer':str(m),'displayed_rows':checks,'result':'passed'}

