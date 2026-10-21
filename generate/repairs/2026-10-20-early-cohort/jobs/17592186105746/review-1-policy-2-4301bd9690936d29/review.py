import os,sys,json,hashlib,importlib.util,re,subprocess,shutil
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
PKG=Path(os.environ.get('REVIEW_PACKAGE',str(JOB/'workspace')))
sys.dont_write_bytecode=True
sys.path.insert(0,str(PKG))
spec=importlib.util.spec_from_file_location('reviewed',PKG/'17592186105746.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=S.symbols('x y')
def save(n,v): (ROOT/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def expr(s):
 s=s.strip().rstrip('.').replace('&','').replace(' ','').replace(r'\,','')
 s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
 s=re.sub(r'(\d|\))(?=[xy])',r'\1*',s)
 return S.sympify(s,locals={'x':x,'y':y})
def normalize(s):
 s=s.replace('\\\\begin','\\begin').replace('\\\\end','\\end').replace('\\\\in','\\in').replace('\\\\,','\\,').replace('\\\\infty','\\infty')
 return re.sub(r'\s+','',s)
def equations(q):
 b=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)[1]
 rows=[]
 for row in b.split(r'\\'):
  lhs,rhs=row.split('=');rows.append([expr(lhs).coeff(x),expr(lhs).coeff(y),expr(rhs)])
 return S.Matrix(rows)
def mats(text):
 return [S.Matrix([[expr(v) for v in row.split('&')] for row in m[2].split(r'\\')]) for m in re.finditer(r'\\begin\{(bmatrix|array)\}(?:\{[c|]+\})?(.*?)\\end\{\1\}',text,re.S)]
def solution_valid(v,a):
 if v=='No solution':return a[:,:2].rank()!=a.rank()
 ms=mats(v)
 if len(ms)!=2 or ms[1].shape!=(2,1):return False
 vv=ms[1];return a[:,:2].rank()==a.rank() and all(S.simplify(z)==0 for z in a[:,:2]*vv-a[:,2]) and any(z.has(y) for z in vv)
def correct_index(r):
 f=r['question'][':question/answer-fields'][0];c=f[':answer-field/correct'];aid=c[-1] if isinstance(c,list) else c[':answer/id']
 return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==aid)
def profile(r):return tuple(str(z) for z in equations(r['question'])[:,:2])
def mathcheck(r):
 q=r['question'];a=equations(q);f=q[':question/answer-fields'][0];banks=[solution_valid(c[':answer/value'],a) for c in f[':answer-field/choices']];idx=correct_index(r)
 ms=[m for m in mats(q[':question/worked-solution']) if m.shape==(2,3)]
 initial=ms[0]==a
 rows=all(m.rref()[0]==a.rref()[0] for m in ms)
 last=ms[-1];ref=last[1,0]==0 and last[1,1]==0 and last[0,0]!=0
 # Each displayed reduced equation and solved system must describe the same set.
 scalar=[]
 for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S):
  if 'bmatrix' in b or ':=' in b:continue
  rr=[]
  try:
   for row in b.split(r'\\'):
    lhs,rhs=row.split('=');v=expr(lhs)-expr(rhs);rr.append([v.coeff(x),v.coeff(y),-v.subs({x:0,y:0})])
   z=S.Matrix(rr);scalar.append(z.rref()[0]==a.rref()[0])
  except (ValueError,TypeError,S.SympifyError):pass
 return {'id':q[':question/id'],'generation':r['generation'],'matrix':a.tolist(),'valid_bank_indices':[i for i,v in enumerate(banks) if v],'key_index':idx,'initial_matrix_matches':initial,'matrix_chains_row_equivalent':rows,'final_ref':ref,'reduced_scalar_checks':scalar,'passed':banks==[i==idx for i in range(5)] and initial and rows and ref and all(scalar)}
