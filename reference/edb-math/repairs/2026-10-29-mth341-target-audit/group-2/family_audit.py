import json,re,sys,collections
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from algebra import matrices,scalar,equations,filled,fill,symbols
from check_algebra import expr
S=json.loads((H/(sys.argv[1]if len(sys.argv)>1 else'current.json')).read_text());qs={q[':db/id']:q for q in S['questions']};topics={q:t for t,k,q in S['links']};checks=[];fails=[];review=[]
def rec(q,kind,ok,**detail):
 r={'question':q[':db/id'],'kind':kind,'ok':bool(ok),**detail};checks.append(r)
 if not ok:fails.append(r)
def normalized_ops(t):
 t=re.sub(r'\{R\}_\{(\d+)\}|R_\{(\d+)\}',lambda m:'R_'+(m[1]or m[2]),t);return t

def operation(t,a):
 t=normalized_ops(t);swap=re.search(r'R_(\d+)\s*&?\s*(?:↔|\\leftrightarrow)\s*R_(\d+)',t)
 if swap:b=a.copy();b.row_swap(int(swap[1])-1,int(swap[2])-1);return b,swap[0]
 m=re.search(r'R_(\d+)\s*&?\s*:=([^&]*?)(?:\\\\|$)',t)
 if not m:return None,None
 rhs=m[2].strip();rhs=re.split(r'[,;:$]|\\end',rhs)[0];names='xyab';rhs=re.sub(r'R_(\d+)',lambda mm:names[int(mm[1])-1],rhs)
 try:v=scalar(rhs)
 except Exception:return None,None
 b=a.copy();row=sp.zeros(1,a.cols)
 for i in range(a.rows):row+=v.coeff(symbols[names[i]])*a[i,:]
 b[int(m[1])-1,:]=row;return b,m[0]
for q in S['questions']:
 tid=topics[q[':db/id']];text=q.get(':question/worked-solution','');prompt=q[':question/problem'];ms=matrices(prompt);sol=matrices(text)
 if tid==17592186048505 and ms:
  root=ms[0]['matrix'];vals=[]
  for f in q.get(':question/answer-fields',[]):
   for a in f[':answer-field/choices']:
    try:val=expr(a[':answer/value']);vals.append((a[':db/id'],val==root.det()))
    except Exception as e:review.append({'question':q[':db/id'],'kind':'det-choice','error':str(e)})
   correct=f.get(':answer-field/correct',{}).get(':db/id')
   if correct:rec(q,'determinant correct key',dict(vals).get(correct,False),determinant=str(root.det()),equivalent_choices=[a for a,v in vals if v])
  for m in sol:
   a=m['matrix'];ok=True
   if a.shape==root.shape:ok=a==root
   elif a.shape==(3,3):ok=a in[root.minor_submatrix(i,j)for i in range(4)for j in range(4)]
   elif a.shape==(2,2):ok=a in[b['matrix'].minor_submatrix(i,j)for b in sol if b['matrix'].shape==(3,3)for i in range(3)for j in range(3)]
   rec(q,'every displayed determinant is root or valid minor',ok,matrix=a.tolist())
 elif tid==17592186050376 and ms:
  a=ms[0]['matrix'];eigs=set(v for v in a.eigenvals()if v.is_real);f=q.get(':question/answer-fields',[None])[0]
  if f and f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
   eigenvals=a.eigenvals()
   for ff in q[':question/answer-fields']:
    key=ff[':answer-field/key'];m=re.search(r'\\lambda\s*=\s*([^$]+)',key);assert m,key;v=scalar(m[1]);mult=re.search(r'multiplicity \$(\d+)\$',key);expected=eigenvals.get(v,0)==int(mult[1])if mult else v in eigenvals;right=next(c for c in ff[':answer-field/choices']if c[':db/id']==ff[':answer-field/correct'][':db/id']);rec(q,'eigenvalue statement and algebraic multiplicity',right[':answer/value']==str(bool(expected)).lower(),statement=key,expected=bool(expected),eigenvalues={str(k):v for k,v in eigenvals.items()})
   f=None
  if f and 'statements are true'in prompt:
   # q-124558: I true (-5), II false (-1), III false (-3 is simple).
   right=next(c for c in f[':answer-field/choices']if c[':db/id']==f[':answer-field/correct'][':db/id']);ev=a.eigenvals();rec(q,'Roman eigenvalue statements',right[':answer/value']=='I only'and ev.get(-5)==1 and -1 not in ev and ev.get(-3)==1,eigenvalues={str(k):v for k,v in ev.items()});f=None
  if f:
   vals=[]
   for c in f[':answer-field/choices']:
    v=c[':answer/value'];m=re.search(r'\{([^{}]*)\}',v.replace(r'\{','{').replace(r'\}','}'))
    try:
     if '='in v:
      lhs,rhs=v.split('=',1);pol=expr(lhs)-expr(rhs);ratio=sp.cancel(pol/(a-sp.Symbol('lambda')*sp.eye(a.rows)).det());ok=ratio!=0 and not ratio.free_symbols
     else:
      ev=set(scalar(x)for x in m[1].split(','))if m else set();ok=ev==eigs
     vals.append((c[':db/id'],ok))
    except Exception as e:review.append({'question':q[':db/id'],'kind':'eigenvalue-choice','value':v,'error':str(e)})
   right=f.get(':answer-field/correct',{}).get(':db/id')
   if right:rec(q,'real eigenvalue set key',dict(vals).get(right,False),real_eigenvalues=sorted(map(str,eigs)),equivalent_choices=[a for a,v in vals if v])
 elif tid in[17592186048920,17592186050900]:
  numeric=[m for m in ms+sol if not m['matrix'].free_symbols];aug=[m for m in numeric if m['matrix'].cols==2*m['matrix'].rows]
  if aug:
   n=aug[0]['matrix'].rows;root=aug[0]['matrix'][:,:n]
   for m in aug:
    a=m['matrix'];rec(q,'augmented intermediate applies same operations to A and I',a[:,n:]*root==a[:,:n],matrix=a.tolist())
  # Each stated operation attached to a displayed matrix must produce the next displayed matrix.
  for attr,tt in [('problem',prompt),('solution',text)]:
   seq=matrices(tt)
   for first,second in zip(seq,seq[1:]):
    a,b=first['matrix'],second['matrix'];between=tt[first['end']:second['start']]
    if a==b and '$$'in between and between.rstrip().endswith(r':\quad'):continue
    out,op=operation(between,a)
    if out is not None and out.shape==b.shape:rec(q,'ordered row operation '+attr,out==b,operation=op,before=a.tolist(),after=b.tolist(),calculated=out.tolist())
  # Numeric final inverse in solution is checked directly when task asks inverse.
  if ('inverse'in prompt.lower())and numeric:
   if aug:root=aug[0]['matrix'][:,:aug[0]['matrix'].rows]
   else:root=ms[0]['matrix']if ms else None
   if root is not None and root.rows==root.cols:
    for m in sol:
     a=m['matrix']
     if a.shape==root.shape and ('^{-1}'in text[max(0,m['start']-100):m['start']]or'^{ -1}'in text[max(0,m['start']-100):m['start']]):rec(q,'displayed final inverse',root*a==sp.eye(root.rows)and a*root==sp.eye(root.rows),inverse=a.tolist())
 elif tid==17592186050944:
  try:rs=equations(prompt);x,y=symbols['x'],symbols['y'];a=sp.Matrix([[sp.expand(r).coeff(x),sp.expand(r).coeff(y)]for r in rs]);b=sp.Matrix([-sp.expand(r).subs({x:0,y:0})for r in rs]);expected=a.inv()*b;rec(q,'linear system unique solution exists',a.det()!=0,coefficient_matrix=a.tolist(),constant=b.tolist(),solution=expected.tolist())
  except Exception as e:review.append({'question':q[':db/id'],'kind':'system','error':str(e)});continue
  if q.get(':question/answer-fields')and all(f[':answer-field/type'][':db/ident']==':answer-field.type/radio'for f in q[':question/answer-fields']):
   for f in q[':question/answer-fields']:
    right=f.get(':answer-field/correct',{}).get(':db/id');vals=[]
    for c in f[':answer-field/choices']:
     v=re.sub(r'^.*?=','',c[':answer/value'],count=1)
     try:value=expr(v);vals.append((c[':db/id'],value==expected))
     except Exception as e:review.append({'question':q[':db/id'],'kind':'solution-choice','value':v,'error':str(e)})
    if right:rec(q,'inverse-system complete choice matches solution',dict(vals).get(right,False),matching_choices=[i for i,v in vals if v])
(H/('family-algebra-audit-after.json'if len(sys.argv)>1 else'family-algebra-audit.json')).write_text(json.dumps({'checks':checks,'failures':fails,'review':review},default=str,indent=2)+'\n');print('Checks',len(checks),'Failures',len(fails),'Review',len(review));print('\n'.join(str(r)for r in fails));print('REVIEW',review[:15])
