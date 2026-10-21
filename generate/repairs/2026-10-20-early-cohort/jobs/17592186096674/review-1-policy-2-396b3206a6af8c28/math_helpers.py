import re
import sympy as sp
def matrices(s):
 out=[]
 for m in re.finditer(r'\\begin\{(bmatrix|array)\}(?:\{[^}]*\})?(.*?)\\end\{\1\}',s,re.S):
  out.append([[int(x.strip()) for x in row.split('&')] for row in m[2].split(r'\\')])
 return out

def system(s):
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S)[1]
 rows=[]
 for row in block.split(r'\\'):
  left,right=row.replace('&','').split('=');right=right.strip().rstrip('.')
  coeff=[]
  for var in 'xyz':
   m=re.search(r'([+-]?\d*)'+var,left.replace(' ',''));c=m[1] if m else '0';coeff.append(int(c+'1') if c in ('','+','-') else int(c))
  rows.append(coeff+[int(right)])
 return rows

def triple(v):
 ms=matrices(v)
 if ms:return [r[3] for r in ms[0]]
 if 'langle' in v or '⟨' in v:return list(map(int,re.findall(r'-?\d+',v)))
 return [int(re.search(var+r'\s*=\s*(-?\d+)',v)[1]) for var in 'xyz']

def check(r):
 q=r['question'];M=sp.Matrix(system(q[':question/problem']));target=list(M.rref()[0][:,3]);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];ts=[triple(c[':answer/value']) for c in choices];correct=[c[':answer/id'] for c,t in zip(choices,ts) if t==target]
 assert len(correct)==1 and correct[0]==f[':answer-field/correct'][1]
 assert len(set(map(tuple,ts)))==5
 ms=matrices(q[':question/worked-solution']);assert ms[0]==M.tolist();assert ms[-1]==M.rref()[0].tolist()
 # Independently parse each displayed row operation and check its resulting full matrix.
 ops=re.findall(r'R_\{(\d)\}:=R_\{\d\}([+-])(\d*)R_\{(\d)\}',q[':question/worked-solution'])
 assert len(ops)==len(ms)-1
 for before,after,(t,sign,n,p) in zip(ms,ms[1:],ops):
  expected=[row[:] for row in before];factor=(int(n) if n else 1)*(1 if sign=='+' else -1);expected[int(t)-1]=[x+factor*y for x,y in zip(before[int(t)-1],before[int(p)-1])];assert expected==after
 return {'id':q[':question/id'],'solution':list(map(int,target)),'steps':len(ops),'profile':r['generation']['source_profile'],'correct_position':next(i for i,c in enumerate(choices) if c[':answer/id']==correct[0])}
