"""Root parses a displayed parameter system and verifies elimination and rank claims."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_constant_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,y,k=p.x,p.y,p.k
INNER=re.compile(r'\\begin\{aligned\}((?:(?!\\begin\{aligned\}).)*?)\\end\{aligned\}',re.S)
MATRIX=re.compile(r'\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',re.S)
def math(raw):return p.scalar(raw.strip().lstrip('&').strip().rstrip('.,'))
def eqmatrix(body):
 rows=[]
 for row in body.split(r'\\'):
  a,b=row.strip().lstrip('&').split('=',1);e=s.expand(math(a)-math(b));r=[e.coeff(x),e.coeff(y),-e.subs({x:0,y:0})];assert s.expand(e-r[0]*x-r[1]*y+r[2])==0;rows.append(r)
 return s.Matrix(rows)
def read(text):
 groups=[m[1] for m in INNER.finditer(text) if '=' in m[1]];assert len(groups)==1;M=eqmatrix(groups[0]);assert M.shape==(2,3)
 det=s.factor(M[:,:-1].det());assert s.Poly(det,k).degree()==1;roots=s.solve(det,k);assert len(roots)==1;root=roots[0]
 dependent='consistent dependent' in text
 assert ('inconsistent' in text)!=dependent
 assert valid(M,root,dependent);return M,root,dependent

def valid(M,value,dependent):
 m=M.subs(k,value);a=m[:,:-1].rank();b=m.rank();return (a==b<2) if dependent else a<b

def stages(text,M,root,dependent):
 mats=[s.Matrix([[math(v) for v in row.split('&')] for row in m[1].split(r'\\')]) for m in MATRIX.finditer(text) if '&' in m[1] and '=' not in m[1]]
 ops=[]
 pat=r'\{R\}_\{(\d)\}\s*&?\s*(?::=(.*?)(?=\\\\|\\end\{aligned\})|(?:↔|\\leftrightarrow)\s*\{R\}_\{(\d)\})'
 for m in re.finditer(pat,text,re.S):
  target=int(m[1])-1
  if m[3]:ops.append(('swap',target,int(m[3])-1));continue
  v=math(re.sub(r'\{R\}_\{([12])\}',lambda z:'x' if z[1]=='1' else 'y',m[2]));poly=s.Poly(v,x,y);assert poly.total_degree()==1 and poly.TC()==0;ops.append(('replace',target,[v.coeff(x),v.coeff(y)]))
 assert len(mats)==len(ops)+2 and mats[0]==mats[1]==M,(mats,ops,M)
 for i,op in enumerate(ops):
  out=mats[i+1].copy()
  if op[0]=='swap':out.row_swap(op[1],op[2])
  else:out[op[1],:]=sum((op[2][j]*mats[i+1].row(j) for j in range(2)),s.zeros(1,3))
  assert s.simplify(out-mats[i+2])==s.zeros(2,3),(i,out,mats[i+2])
 assert mats[-1][1,0]==0 and mats[-1].subs(k,root)[1,1]==0
 if dependent:assert mats[-1].subs(k,root)[1,2]==0
 else:assert mats[-1].subs(k,root)[1,2]!=0
 systems=0
 for m in INNER.finditer(text):
  if '=' in m[1]:
   mat=eqmatrix(m[1]);assert mat.rref()[0]==M.rref()[0] or mat.rref()[0]==mats[-1].rref()[0],(mat,M);systems+=mat.rows
 claims=0;inline=0
 for raw in re.findall(r'(?<!\$)\$([^$]*?)\$(?!\$)',text):
  if re.match(r'k\s*=',raw):assert s.simplify(math(raw.split('=',1)[1])-root)==0,raw;claims+=1
  elif '=' in raw and not any(c in raw for c in ('\\begin','\\in')):
   a,b=raw.split('=',1);e=s.expand(math(a)-math(b));coeff=s.Matrix([[e.coeff(x),e.coeff(y),-e.subs({x:0,y:0})]])
   assert s.expand(e-coeff[0,0]*x-coeff[0,1]*y+coeff[0,2])==0,raw
   candidates=[row for mat in (M,mats[-1],M.subs(k,root),mats[-1].subs(k,root)) for row in [mat.row(i) for i in range(mat.rows)]]
   def proportional(row):
    j=next((j for j,v in enumerate(row) if v!=0),None)
    if j is None:return coeff==s.zeros(1,3)
    ratio=s.cancel(coeff[j]/row[j]);return ratio!=0 and s.simplify(coeff-ratio*row)==s.zeros(1,3)
   assert coeff==s.zeros(1,3) or any(proportional(row) for row in candidates),raw;inline+=1
 assert claims>=2
 return dict(matrix_stages=len(mats),row_operations=len(ops),corresponding_equations=systems,parameter_claims=claims,inline_equations=inline)
