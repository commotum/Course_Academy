"""Parent independently parses printed systems, banks and each matrix transition."""
import importlib.util,re
from pathlib import Path
import sympy as s
sp=importlib.util.spec_from_file_location('parent_gj_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
V=(p.x,p.y,p.z,p.u)
INNER=re.compile(r'\\begin\{aligned\}((?:(?!\\begin\{aligned\}).)*?)\\end\{aligned\}',re.S)
MATRIX=re.compile(r'\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',re.S)
def math(raw):
 raw=re.sub(r'\{x\}_\{([1234])\}',lambda m:str(V[int(m[1])-1]),raw).replace('w','u')
 return p.scalar(raw.strip().lstrip('&').strip().rstrip('.,'))
def residual(raw):
 a,b=raw.strip().lstrip('&').split('=',1);return s.expand(math(a)-math(b))
def system(text):
 groups=[m[1] for m in INNER.finditer(text) if '=' in m[1]]
 if groups:
  assert len(groups)==1;rows=groups[0].split(r'\\')
 else:
  a=re.search(r'\$\{(.*?)\$',text,re.S);assert a;rows=a[1].split(';')
 expr=[residual(z) for z in rows];used=set().union(*(e.free_symbols for e in expr));n=max(i+1 for i,v in enumerate(V) if v in used);assert used<=set(V[:n])
 mat=s.Matrix([[e.coeff(v) for v in V[:n]]+[-e.subs(dict.fromkeys(V,0))] for e in expr]);assert all(s.expand(e-sum(mat[i,j]*V[j] for j in range(n))+mat[i,-1])==0 for i,e in enumerate(expr));return mat

def vector(text):
 if text=='No solution':return None
 if r'\\begin' in text:text=text.replace('\\\\','\\')
 m=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',text,re.S);assert m,text
 return s.Matrix([math(z) for z in m[1].split(r'\\')])
def signature(vec):
 if vec is None:return 'No solution'
 syms=set().union(*(e.free_symbols for e in vec));assert len(syms)==1;v=next(iter(syms));d=vec.diff(v);point=vec.subs(v,0);j=next(i for i,z in enumerate(d) if z!=0);d=d/d[j];point=point-point[j]*d;return tuple(point),tuple(d)

def stages(text,M):
 mats=[s.Matrix([[math(v) for v in row.split('&')] for row in m[1].split(r'\\')]) for m in MATRIX.finditer(text) if '&' in m[1] and '=' not in m[1]]
 ops=[]
 for m in re.finditer(r'\{R\}_\{(\d)\}\s*&?\s*:=(.*?)(?=\\\\|\\end\{aligned\})',text,re.S):
  expr=re.sub(r'\{R\}_\{([1234])\}',lambda z:str(V[int(z[1])-1]),m[2]);v=math(expr);poly=s.Poly(v,*V);assert poly.total_degree()==1 and poly.TC()==0;ops.append((int(m[1])-1,[v.coeff(z) for z in V]))
 assert len(mats)==len(ops)+2 and mats[0]==mats[1]==M,(len(mats),len(ops),M)
 for i,(target,coeff) in enumerate(ops):
  before=mats[i+1];after=before.copy();after[target,:]=sum((coeff[j]*before.row(j) for j in range(before.rows)),s.zeros(1,before.cols));assert after==mats[i+2],(i,before,ops[i],after,mats[i+2])
 R,piv=M.rref();assert mats[-1]==R and M.cols-1 not in piv
 free=[j for j in range(M.cols-1) if j not in piv];assert len(free)==1
 sol=s.Matrix(V[:M.cols-1]);f=free[0]
 for i,j in enumerate(piv):sol[j]=R[i,-1]-R[i,f]*V[f]
 eqs=vecs=0
 for m in INNER.finditer(text):
  if '=' in m[1]:
   for row in m[1].split(r'\\'):
    e=residual(row);assert s.expand(e.subs(dict(zip(V,sol)),simultaneous=True))==0,row;eqs+=1
  elif '&' not in m[1]:
   vec=s.Matrix([math(z) for z in m[1].split(r'\\')]);assert vec.rows==sol.rows;assert vec==s.Matrix(V[:sol.rows]) or s.simplify(vec-sol)==s.zeros(sol.rows,1),(vec,sol);vecs+=vec.rows
 # Explicit inline solved equations must agree too, not only aligned systems.
 for raw in re.findall(r'(?<!\$)\$([^$]*?)\$(?!\$)',text):
  if re.match(r'(?:\{x\}_\{[1234]\}|[xyzw])\s*=',raw):
   assert s.expand(residual(raw).subs(dict(zip(V,sol)),simultaneous=True))==0,raw;eqs+=1
 return dict(matrix_stages=len(mats),row_operations=len(ops),solved_equations=eqs,vector_components=vecs)

def components(text):
 out=[]
 for m in INNER.finditer(text):
  if '=' in m[1]:out.append(('eqs',tuple(residual(row) for row in m[1].split(r'\\'))))
  elif '&' in m[1]:out.append(('matrix',tuple(tuple(math(v) for v in row.split('&')) for row in m[1].split(r'\\'))))
  else:out.append(('vector',tuple(math(z) for z in m[1].split(r'\\'))))
 return out

def prose(text):
 return re.sub(r'\$[^$]*\$','[INLINE]',re.sub(r'\$\$.*?\$\$','[MATH]',text,flags=re.S))
