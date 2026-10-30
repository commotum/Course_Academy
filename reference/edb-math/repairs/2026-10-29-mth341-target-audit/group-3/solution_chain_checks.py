import json,re,runpy
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;M=runpy.run_path(str(H/'math_review.py'));qs=M['qs'];plain=M['plain'];scalar=M['scalar'];vecs=M['vecs'];vector=M['vector'];syms=M['syms'];checks=[];bad=[]
def closed(t):
 t=plain(t).strip().rstrip('.')
 if r'\begin{array}'in t:
  a=re.search(r'\\begin\{array\}\{[clr]+\}([\s\S]*?)\\end\{array\}',t)
  if a:
   rows=[[c.strip()for c in row.split('&')]for row in a[1].split(r'\\')]
   if len(rows)==3 and all(len(r)==3 for r in rows)and all(n in rows[0][i]for i,n in enumerate('ijk')):
    return sp.Matrix([scalar(x)for x in rows[1]]).cross(sp.Matrix([scalar(x)for x in rows[2]]))
 vs=vecs(t)
 if vs:
  if len(vs)==1:
   start,end,v=vs[0];pre=t[:start].strip();post=t[end:].strip();assert not post
   k=scalar(pre)if pre else 1;assert not k.free_symbols;return k*v
  assert len(vs)==2
  a,b=vs;pre=t[:a[0]].strip();mid=t[a[1]:b[0]].strip();post=t[b[1]:].strip();assert not pre and not post
  if mid=='+':return a[2]+b[2]
  if mid=='-':return a[2]-b[2]
  if mid==r'\times':return a[2].cross(b[2])
  if mid=='*':return a[2].dot(b[2])
  raise ValueError('unsupported vector op')
 e=scalar(t);assert e.free_symbols<=set(syms[n]for n in'ijk')
 if e.free_symbols:return vector(t)
 return e
for q in qs:
 for block in re.findall(r'\$\$([\s\S]*?)\$\$',q[':question/worked-solution']):
  if r'\begin{aligned}'not in block:continue
  body=block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];prior=None;prior_text=None
  # Do not split rows inside a nested matrix/array.
  depth=0;rows=[];start=0
  token=re.compile(r'\\(?:begin|end)\{[^{}]+\}|\\\\')
  for m in token.finditer(body):
   if m[0].startswith(r'\begin'):depth+=1
   elif m[0].startswith(r'\end'):depth-=1
   elif depth==0:rows.append(body[start:m.start()]);start=m.end()
  rows.append(body[start:])
  for row in rows:
   if '='not in row:prior=None;continue
   left,right=row.split('=',1);left=left.replace('&','').strip();right=right.strip()
   try:value=closed(right)
   except Exception:prior=None;continue
   if not left and prior is not None:
    eq=value==prior if isinstance(value,sp.MatrixBase)else sp.simplify(value-prior)==0 if not isinstance(prior,sp.MatrixBase)else False
    rec={'entity':q[':db/id'],'previous_expression':prior_text,'next_expression':right,'previous_value':str(prior),'next_value':str(value),'equal':bool(eq)}
    (checks if eq else bad).append(rec)
   prior=value;prior_text=right
(H/'solution-chain-verification.json').write_text(json.dumps({'passed':not bad,'closed_numeric_chain_steps':len(checks),'checks':checks,'failures':bad,'database_writes':0},indent=2)+'\n');print('Closed numeric solution-chain checks',len(checks),'failures',len(bad));print(bad)
