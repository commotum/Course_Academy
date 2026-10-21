import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,pathlib,re,copy,collections,hashlib,subprocess,platform
from fractions import Fraction as F
E=pathlib.Path(__file__).resolve().parent; J=E.parent; P=J/'workspace'; R=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=str(R/'.venv/bin/python')
sys.dont_write_bytecode=True;sys.path.insert(0,str(P))
import generator as g, easy, hard

def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def mat(s):
 b=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)
 if not b:return None
 def number(x):
  x=x.strip();z=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',x)
  return F((-1 if z[1] else 1)*int(z[2]),int(z[3])) if z else F(x)
 return [[number(x) for x in row.split('&')] for row in re.split(r'\\\\',b[1])]
def matrixes(s):return [mat(x[0]) for x in re.findall(r'(\\begin\{bmatrix\}(.*?)\\end\{bmatrix\})',s,re.S) if not re.search(r'\\cdot|\)\(',x[1])]
def key(q):
 f=q[':question/answer-fields'][0]; c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def ops(prompt):
 # Independently parse delivered TeX, not generation metadata.
 tails=prompt.split('row operation',1)[1]; tails=tails.replace('s on',' on')
 chunks=re.findall(r'\$([^$]+)\$',tails,re.S)
 txt=next((v for v in chunks if 'R' in v), '')
 txt=re.sub(r'\{R\}_\{(\d)\}',r'R\1',txt);txt=txt.replace('&','').replace(' ','').replace('\\begin{aligned}','').replace('\\end{aligned}','')
 ans=[]
 for a,b in re.findall(r'R(\d)\\leftrightarrowR(\d)',txt):ans.append(('swap',int(a)-1,int(b)-1,None))
 for t,rhs in re.findall(r'R(\d):=(.*?)(?=\\\\|$)',txt):
  t=int(t)-1;add=re.fullmatch(r'R\d([+-])(\d*)R(\d)',rhs)
  if add:ans.append(('add',t,int(add[3])-1,int((add[1])+ (add[2] or '1'))))
  else:
   v=re.fullmatch(r'(.*?)R\d',rhs);factor=v[1];factor=re.sub(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',r'\1\2/\3',factor)
   ans.append(('scale',t,None,F(factor)))
 if not ans:raise ValueError(txt)
 return ans

def calc(q):
 m=mat(q[':question/problem']); out=copy.deepcopy(m)
 for typ,t,s,k in ops(q[':question/problem']):
  if typ=='swap':out[t],out[s]=out[s],out[t]
  if typ=='scale':out[t]=[k*x for x in out[t]]
  if typ=='add':out[t]=[x+k*y for x,y in zip(out[t],out[s])]
 return out

def verify(rec):
 q=rec['question'];expected=calc(q);f=q[':question/answer-fields'][0]; bank=[mat(a[':answer/value']) for a in f[':answer-field/choices']]
 return {'id':q[':question/id'],'expected':expected,'correct':mat(key(q)[':answer/value']),'key_correct':mat(key(q)[':answer/value'])==expected,'unique_correct':bank.count(expected)==1,'five_unique':len({str(x) for x in bank})==5,'solution_final_correct':mat(re.findall(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',q[':question/worked-solution'],re.S)[-1])==expected}

