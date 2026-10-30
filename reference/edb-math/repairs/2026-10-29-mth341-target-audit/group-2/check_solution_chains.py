import json,re,sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from algebra import matrices,equations,symbols
from check_algebra import expr,chain_checks
from question_capture.math_format import ENV,MATH,environment,cells
S=json.loads((H/'proposed-snapshot.json').read_text());topics={q:t for t,k,q in S['links']};out=[];bad=[]
def record(q,kind,ok,**d):
 r={'question':q[':db/id'],'kind':kind,'ok':bool(ok),**d};out.append(r)
 if not ok:bad.append(r)
for q in S['questions']:
 tid=topics[q[':db/id']];sol=q[':question/worked-solution'];root=matrices(q[':question/problem']);root=root[0]['matrix']if root else None
 if tid==17592186050376 and root is not None:
  l=sp.Symbol('lambda');poly=(root-l*sp.eye(root.rows)).det()
  for block in MATH.finditer(sol):
   tt=block[0];edge=2 if tt.startswith('$$')else 1;tt=tt[edge:-edge];rows=[tt]
   if r'\begin{aligned}'in tt:
    p=tt.index(r'\begin{aligned}');span=environment(tt,p);rows=[''.join(r)for r in cells(tt[span[0]:span[1]])]
   for row in rows:
    if not re.search(r'=\s*0[.,]?\s*$',row):continue
    lhs=row.rsplit('=',1)[0].strip()
    try:v=expr(lhs)
    except Exception:continue
    if not v.free_symbols:continue
    ratio=sp.cancel(v/poly);record(q,'characteristic equation intermediate equivalent zero set',ratio!=0 and not ratio.free_symbols,expression=lhs,ratio=str(ratio))
 elif tid==17592186050944:
  rs=equations(q[':question/problem']);x,y=symbols['x'],symbols['y'];a=sp.Matrix([[sp.expand(r).coeff(x),sp.expand(r).coeff(y)]for r in rs]);b=sp.Matrix([-sp.expand(r).subs({x:0,y:0})for r in rs]);expected=a.inv()*b
  for block in MATH.finditer(sol):
   tt=block[0];edge=2 if tt.startswith('$$')else 1;tt=tt[edge:-edge]
   if r'\begin{aligned}'not in tt:continue
   p=tt.index(r'\begin{aligned}');span=environment(tt,p);rows=[''.join(r)for r in cells(tt[span[0]:span[1]])]
   in_solution=False
   for row in rows:
    if re.search(r'(?:x|mathbf\{x\}).*?=.*?(?:A.*?-1|A.*?−1)',row):in_solution=True
    if not in_solution:continue
    if '='not in row:continue
    rhs=row.split('=',1)[1]
    try:v=expr(rhs)
    except Exception:continue
    if isinstance(v,sp.MatrixBase):record(q,'inverse-system intermediate product',v==expected,expression=rhs,expected=expected.tolist(),actual=v.tolist())
 elif tid==17592186048505:
  checks,failures,unparsed=chain_checks(q)
  # This family contains numeric identities, not variable-assignment equations.
  for r in checks:record(q,'cofactor expansion arithmetic identity',r['ok'],expression=r['row'],expected=r['expected'],actual=r['actual'])
(H/'solution-chain-verification.json').write_text(json.dumps({'passed':not bad,'checks':out,'failures':bad},default=str,indent=2)+'\n');print('Solution chain checks',len(out),'failures',len(bad));print(bad)
