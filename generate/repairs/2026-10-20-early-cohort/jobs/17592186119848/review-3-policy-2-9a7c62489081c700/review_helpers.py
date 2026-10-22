import re
from fractions import Fraction
def norm(t):
 t=t.replace('\\\\begin','\\begin').replace('\\\\end','\\end');return t.replace('\\\\\\\\','\\\\')
pat=re.compile(r'([A-E])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def matrices(q):
 texts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  texts.append(f[':answer-field/key']);texts.extend(a[':answer/value'] for a in f[':answer-field/choices'])
 ans={}
 for t in texts:
  for label,body in pat.findall(norm(t)):ans[label]=[[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
 return ans
def rank(m):
 a=[list(map(Fraction,row)) for row in m];r=0
 for c in range(len(a[0])):
  k=next((i for i in range(r,len(a)) if a[i][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
  for i in range(r+1,len(a)):
   v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r
def correct(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def labels(t):return sorted(set(re.findall(r'\$([A-E])\$',t)))
def expected(q,f):
 r=int(re.search(r'rank of \$(\d+)',q[':question/problem'])[1]);ms=matrices(q);matches=sorted(k for k,m in ms.items() if rank(m)==r)
 def right(a):
  if f[':answer-field/type'].endswith('/checkbox'):
   labs=list(matrices({':question/problem':f[':answer-field/key']}));truth=labs[0] in matches if labs else not matches
   return a[':answer/value']==str(truth).lower()
  am=matrices({':question/problem':a[':answer/value']})
  return list(am)==matches if am else labels(a[':answer/value'])==matches
 return [a for a in f[':answer-field/choices'] if right(a)]
