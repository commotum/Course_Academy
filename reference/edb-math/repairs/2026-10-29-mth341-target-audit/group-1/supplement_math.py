import json,re,sys,importlib.util
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('gm',H/'math_verify.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);D=m.D;out=[]
def add(q,kind,proof,ok=True):out.append({'entity':q[':db/id'],'identity':q.get(':question/math-academy-id'),'check':kind,'proof':str(proof),'passed':bool(ok)});assert ok,out[-1]
for q in D['questions']:
 kp=m.bykp[q[':db/id']];mid=m.bymid[q[':db/id']];v=m.pm.get((q[':db/id'],'question/problem'),q[':question/problem']);ms=[r[2]for r in m.mats(v)]
 if mid==1868 and kp==17592186124509 and ms:
  dims=[a.cols-a.rank()for a in ms]
  if'Find'in v:
   target=sum(dims);add(q,'sum-nullities',dims)
   for f,choices,right in m.qfields(q):vals=[a[':db/id']for a in choices if m.scalar(a[':answer/value'])==target];add(q,'sum-nullities-entire-bank',vals,vals==[right[':db/id']])
  else:
   claims=[int(x)for x in re.findall(r'=\s*(\d+)\.?\$',v)];truths=[x==y for x,y in zip(dims,claims)];add(q,'nullity-radio-statements',f'actual={dims},claims={claims},truths={truths}')
   for f,choices,right in m.qfields(q):
    indices=lambda a:[['I','II','III'].index(x)for x in re.findall(r'\b(?:III|II|I)\b',a)]
    vals=[a[':db/id']for a in choices if indices(a[':answer/value'])==[i for i,t in enumerate(truths)if t]];add(q,'nullity-radio-bank',vals,vals==[right[':db/id']])
 if mid==2103 and kp in[17592186133781,17592186133843]and ms:
  groups=[]
  for mm in m.MATH.finditer(v):
   vs=[r[2]for r in m.mats(mm[0])]
   if vs:groups.append(vs)
  truths=[];grams=[]
  for vs in groups:
   G=S.Matrix.hstack(*vs).T*S.Matrix.hstack(*vs);t=all(G[i,j]==0 for i in range(len(vs))for j in range(i))
   if kp==17592186133781:t=t and all(G[i,i]==1 for i in range(len(vs)))
   truths.append(t);grams.append(str(G))
  add(q,'radio-set-gram-matrices',f'grams={grams},truths={truths}')
  for f,choices,right in m.qfields(q):
   def indices(value):
    roman=re.findall(r'\b(?:III|II|I)\b',value)
    if roman:return[['I','II','III'].index(x)for x in roman]
    return[ord(x)-ord('U')for x in re.findall(r'\b[UVW]\b',value)]
   expected=[i for i,t in enumerate(truths)if t];vals=[a[':db/id']for a in choices if indices(a[':answer/value'])==expected];add(q,'radio-set-complete-bank',vals,vals==[right[':db/id']])
# Manual resolution of the two intentionally limited generic parser cases.
q=next(q for q in D['questions']if q[':db/id']==17592186119613);a,b=[r[2]for r in m.mats(q[':question/problem'])];target=a/3+b/2;add(q,'canonical-vector-combination',target,target==S.Matrix([-3,-1,5,-7,6]))
q=next(q for q in D['questions']if q[':db/id']==17592186133591);a,b=[r[2]for r in m.mats(q[':question/problem'])];x=S.Matrix([-1,1,0]);add(q,'canonical-orthogonal-extension',f'a·x={a.dot(x)},b·x={b.dot(x)},rank={S.Matrix.hstack(a,b,x).rank()}',a.dot(x)==b.dot(x)==0 and S.Matrix.hstack(a,b,x).rank()==3)
(H/'supplemental-math-verification.json').write_text(json.dumps({'passed':True,'checks':out},indent=2)+'\n');print('Supplemental exact checks',len(out))
