import json,re
import sympy as S
x,y,z=S.symbols("x y z")
def expr(t):
 t=t.strip().replace('−','-')
 t=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',t)
 t=re.sub(r'(\d)\s*([xyz])',r'\1*\2',t)
 return S.sympify(t,locals={'x':x,'y':y,'z':z})
def prompt(q):
 t=q[':question/problem'].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
 out=[]
 for line in t.split('\\\\'):
  a,b=line.replace('&','').split('='); a=expr(a);out.append([a.coeff(v) for v in (x,y,z)]+[expr(b)])
 return S.Matrix(out)
def matrices(t):
 if r'\\begin' in t:t=t.replace('\\\\','\\')
 pat=r'\\begin\{(?:bmatrix|array)\}(?:\{[^}]*\})?(.*?)\\end\{(?:bmatrix|array)\}'
 return [S.Matrix([[expr(v) for v in row.split('&')] for row in body.split('\\\\')]) for body in re.findall(pat,t,re.S)]
def semantic(t):
 if t=='No solution':return t
 return str(matrices(t)[0].tolist())
def correct_index(q):
 f=q[':question/answer-fields'][0]; k=f[':answer-field/correct'];k=k[':answer/id'] if isinstance(k,dict) else k[1]
 return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==k)
def check(r):
 q=r['question'];m=prompt(q);red,piv=m.rref();f=q[':question/answer-fields'][0]; hits=[]
 for a in f[':answer-field/choices']:
  t=a[':answer/value']
  if t=='No solution':hits.append(False);continue
  v=matrices(t)[0]
  hits.append(v==red if v.shape==(3,4) else v.shape==(3,1) and m[:,:3]*v==m[:,3] and v[2]==z)
 states=[a for a in matrices(q[':question/worked-solution']) if a.shape==(3,4)]
 errs=[]
 if piv!=(0,1):errs.append('pivot/rank')
 if sum(hits)!=1 or not hits[correct_index(q)]:errs.append('bank/key')
 if not states or states[0]!=m or states[-1]!=red or any(a.rref()[0]!=red for a in states):errs.append('solution matrices')
 # Inspect the actual displayed operation labels, not metadata or generator trace.
 ops=re.findall(r'(R_\{\d\}(?:\\leftrightarrow R_\{\d\}|:=.*?))\\qquad M\\sim',q[':question/worked-solution'])
 if ops:
  states=[a for j,a in enumerate(states) if j==0 or a!=states[j-1]]
  if len(ops)!=len(states)-1:errs.append('trace count')
  for before,after,op in zip(states,states[1:],ops):
   b=before.copy();i=int(re.search(r'R_\{(\d)\}',op)[1])-1
   if 'leftrightarrow' in op:b.row_swap(i,int(re.findall(r'R_\{(\d)\}',op)[1])-1)
   else:
    k=expr(re.search(r'\\left\((.*?)\\right\)',op)[1])
    if ':=R_' in op:b[i,:]=b[i,:]+k*b[int(re.findall(r'R_\{(\d)\}',op)[-1])-1,:]
    else:b[i,:]=k*b[i,:]
   if b!=after:errs.append('operation '+op)
 return {'id':q[':question/id'],'template':r['generation'].get('template'),'index':correct_index(q),'matrix':m.tolist(),'rref':red.tolist(),'errors':errs,'vector': 'and then solve' in q[':question/problem']}
