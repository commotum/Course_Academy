"""Root determines classification from the actual printed system and statements."""
import importlib.util,re
from pathlib import Path
import sympy as s
sp=importlib.util.spec_from_file_location('parent_class_gj',Path(__file__).with_name('gauss-jordan-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
def truth(M):
 n=M.cols-1;a=M[:,:-1].rank();b=M.rank();return 'inconsistent' if a<b else 'dependent' if a<n else 'independent'
def canonical(M):return tuple(tuple(row) for row in M.rref()[0].tolist() if any(row))
def statements(text):
 tail=text.split('Which of the following statements are true?',1)[1];out=[]
 for line in tail.splitlines():
  if not line.strip():continue
  v=re.sub(r'^\s*(?:-\s*|[IV]+\.\s*)','',line).strip().rstrip('.');assert v.startswith('The system '),v
  if v in ('The system has no solution','The system is inconsistent'):out.append('inconsistent')
  elif v=='The system is consistent dependent':out.append('dependent')
  elif v in ('The system has a unique solution','The system is consistent independent'):out.append('independent')
  else:raise AssertionError(v)
 assert len(out)==3;return out

def subset(value):
 if value=='None':return frozenset()
 assert value.endswith(' only');parts=value[:-5].split(' and ');assert all(z in ['I','II','III'] for z in parts);return frozenset(['I','II','III'].index(z) for z in parts)

def stages(text,M):
 mats=[s.Matrix([[p.math(v) for v in row.split('&')] for row in m[1].split(r'\\')]) for m in p.MATRIX.finditer(text) if '&' in m[1] and '=' not in m[1]]
 ops=[]
 pat=r'\{R\}_\{(\d)\}\s*&?\s*(?::=(.*?)(?=\\\\|\\end\{aligned\})|(?:↔|\\leftrightarrow)\s*\{R\}_\{(\d)\})'
 for m in re.finditer(pat,text,re.S):
  target=int(m[1])-1
  if m[3]:ops.append(('swap',target,int(m[3])-1));continue
  expr=re.sub(r'\{R\}_\{([1234])\}',lambda z:str(p.V[int(z[1])-1]),m[2]);v=p.math(expr);poly=s.Poly(v,*p.V);assert poly.total_degree()==1 and poly.TC()==0;ops.append(('replace',target,[v.coeff(z) for z in p.V]))
 assert len(mats)==len(ops)+2 and mats[0]==mats[1]==M,(mats,ops)
 for i,op in enumerate(ops):
  before=mats[i+1];out=before.copy()
  if op[0]=='swap':out.row_swap(op[1],op[2])
  else:out[op[1],:]=sum((op[2][j]*before.row(j) for j in range(before.rows)),s.zeros(1,before.cols))
  assert out==mats[i+2],(i,out,mats[i+2])
 assert mats[-1].rref()[0]==M.rref()[0]
 for m in p.INNER.finditer(text):
  if '=' in m[1]:
   mat=p.system('$$'+r'\begin{aligned}'+m[1]+r'\end{aligned}'+'$$');assert canonical(mat)==canonical(M),(mat,M)
 kind=truth(M);claim=re.search(r'we conclude that the system is\s+\*?(consistent dependent|consistent independent|inconsistent)',text)
 if not claim:claim=re.search(r'we conclude that (?:our|the) system is\s+\*?(consistent dependent|consistent independent|inconsistent)',text)
 assert claim and {'consistent dependent':'dependent','consistent independent':'independent','inconsistent':'inconsistent'}[claim[1]]==kind,text
 R,piv=M.rref();n=M.cols-1;solution=s.Matrix(p.V[:n])
 if kind!='inconsistent':
  free=[j for j in range(n) if j not in piv]
  for i,j in enumerate(piv):solution[j]=R[i,-1]-sum(R[i,f]*p.V[f] for f in free)
 inline=0
 for block in re.findall(r'\$\$.*?\$\$|\$[^$]*\$',text,re.S):
  body=block.strip('$').strip()
  if '=' not in body or r'\begin' in body:continue
  for piece in body.split('⟹'):
   if '=' not in piece:continue
   e=p.residual(piece.replace(r'\,',''))
   if kind=='inconsistent':
    assert not e.free_symbols
    assert any(s.simplify(e-(sum(mats[-1][i,j]*p.V[j] for j in range(n))-mats[-1][i,-1]))==0 for i in range(M.rows)),piece
   else:assert s.expand(e.subs(dict(zip(p.V,solution)),simultaneous=True))==0,piece
   inline+=1
 return dict(matrix_stages=len(mats),row_operations=len(ops),classification_claims=1,inline_equations=inline)
