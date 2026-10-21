import sys
sys.dont_write_bytecode=True
import json,re,random,copy,pathlib,hashlib,subprocess,os,itertools
from fractions import Fraction as F
ROOT=pathlib.Path('/home/jake/Developer/Course_Academy')
PKG=pathlib.Path(__file__).resolve().parents[1]; JOB=PKG.parent; OUT=PKG/'evidence'
sys.path.insert(0,str(PKG));import generator as g

def save(n,x): (OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def digest():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.iterdir() if p.is_file()}
def numeric(s):
 s=s.strip().replace(' ','').replace('\\left','').replace('\\right','')
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 # Exact rational expression; reject all unrecognized syntax before eval.
 if not re.fullmatch(r'[\d+*/()\-]+',s):raise ValueError(s)
 s=re.sub(r'(?<=\d)\(', '*(',s);s=re.sub(r'\)(?=\d|\()',')*',s)
 s=s.replace('\\cdot','*')
 import ast
 def ev(n):
  if isinstance(n,ast.Constant):return F(n.value)
  if isinstance(n,ast.UnaryOp):return -ev(n.operand) if isinstance(n.op,ast.USub) else ev(n.operand)
  if isinstance(n,ast.BinOp):
   a,b=ev(n.left),ev(n.right)
   if isinstance(n.op,ast.Add):return a+b
   if isinstance(n.op,ast.Sub):return a-b
   if isinstance(n.op,ast.Mult):return a*b
   if isinstance(n.op,ast.Div):return a/b
  raise ValueError(n)
 return ev(ast.parse(s,mode='eval').body)
def matrices(s,expression=False):
 while '\\\\begin' in s:s=s.replace('\\\\','\\')
 matches=re.findall(r'\\begin\{(?:array|bmatrix)\}(?:\{[c|]+\})?(.*?)\\end\{(?:array|bmatrix)\}',s,re.S)
 result=[]
 for body in matches:
  # body row separators are \\ in normalized content, single slash in double-escaped source after above decoding.
  rows=re.split(r'\\\\|\\(?![a-zA-Z])',body.strip())
  try:result.append([[numeric(x.replace('\\cdot','*')) for x in row.split('&')] for row in rows if row.strip()])
  except Exception:
   if not expression:raise
 return result

def operations(prompt):
 p=prompt.split('What matrix results')[1]
 p=p.replace('{R}', 'R').replace('↔',r'\leftrightarrow').replace('&','').replace(' ','')
 p=re.sub(r'R_(\d)',r'R_{\1}',p)
 p=p.replace('\\\\','\n')
 token=r'R_\{(\d)\}'
 ops=[]
 for m in re.finditer(token+r'(?:\\leftrightarrow'+token+r'|:=([^$\n]*))',p):
  t=int(m[1])-1
  if m[2]:ops.append(('swap',t,int(m[2])-1));continue
  rhs=m[3].split('\\\\')[0].split('\\end')[0]
  rs=list(re.finditer(token,rhs))
  if len(rs)==2:
   coeff=rhs[rs[0].end():rs[1].start()].replace('\\cdot','').lstrip('+')
   ops.append(('add',t,int(rs[1][1])-1,numeric(coeff or '1')))
  elif len(rs)==1:
   coeff=rhs[:rs[0].start()].replace('\\cdot','')
   ops.append(('scale',t,numeric(coeff or '1')))
  else:raise ValueError(rhs)
 return ops

def expected(q):
 m=matrices(q[':question/problem'])[0]
 for op in operations(q[':question/problem']):
  if op[0]=='swap':_,a,b=op;m[a],m[b]=m[b],m[a]
  elif op[0]=='scale':_,t,k=op;m[t]=[k*x for x in m[t]]
  else:_,t,d,k=op;m[t]=[x+k*y for x,y in zip(m[t],m[d])]
 return m

def key(q):
 f=q[':question/answer-fields'][0];k=f[':answer-field/correct'];return k[':answer/id'] if isinstance(k,dict) else k[1]
def check(record):
 q=record['question'];want=expected(q);f=q[':question/answer-fields'][0]
 matches=[c[':answer/id'] for c in f[':answer-field/choices'] if matrices(c[':answer/value'])[0]==want]
 sol=matrices(q[':question/worked-solution'],True)
 return {'id':q[':question/id'],'ops':str(operations(q[':question/problem'])),'unique_correct':matches==[key(q)],'final_solution_correct':sol[-1]==want,'choices':len(f[':answer-field/choices'])}

