import json,re,collections
from pathlib import Path
import sympy as sp
OUT=Path('reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-next/reviews');f=OUT/'text-cases.json';data=json.load(open(f))
def scalar(s):
 s=re.sub(r'\\text\{[^}]*\}|\\,|\s','',s)
 s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
 s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s);s=s.replace('{','(').replace('}',')')
 return sp.sympify(s,rational=True)
def matrix(text):
 t=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S).group(1)
 return sp.Matrix([[scalar(v)for v in row.split('&')]for row in re.split(r'\\\\',t)])
def elementary(M):
 n,m=M.shape
 if n!=m:return False
 I=sp.eye(n);D=M-I;diff=[(i,j)for i in range(n)for j in range(n)if D[i,j]!=0]
 if len(diff)==1:
  i,j=diff[0];return i!=j or M[i,i]!=0
 for i in range(n):
  for j in range(i+1,n):
   S=I.copy();S.row_swap(i,j)
   if S==M:return True
 return False
def echelon(M):
 piv=[];seen_zero=False
 for row in M.tolist():
  nz=[i for i,v in enumerate(row)if v!=0]
  if not nz:seen_zero=True;continue
  if seen_zero:return False
  piv.append(nz[0])
 return all(a<b for a,b in zip(piv,piv[1:]))
def block(M,kind):
 n,m=M.shape
 if n!=m:return False
 for k in range(1,n):
  upper=all(M[i,j]==0 for i in range(k)for j in range(k,n));lower=all(M[i,j]==0 for i in range(k,n)for j in range(k))
  if (kind=='diagonal'and upper and lower)or(kind=='upper'and lower)or(kind=='lower'and upper):return True
 return False
count=0;conflicts=[];skip=[]
for q in data['questions']:
 if q['classification']!='finite_named_matrices':continue
 title=q['kps'][0]['title'];p=q['source_problem'];proofs=[]
 if q['reason'].startswith('Independent exact matrix calculation'):
  q['decision']='convert';q['reason']='Finite source cases; exact matrix calculation supports the existing database key.';q['proposed_prompt']=p+'\n\nSelect all that apply.'
 for a in q['atomic_options']:
  M=matrix(a['text']);n,m=M.shape;truth=None;proof=''
  if title=='Identifying a Square Matrix':truth=n==m;proof=f'Exact shape {n}×{m}; square iff row and column counts agree.'
  elif title=='Identifying a Special Square Matrix':
   if 'diagonal'in p:truth=n==m and all(M[i,j]==0 for i in range(n)for j in range(m)if i!=j);proof=f'Shape {n}×{m}; all off-diagonal entries vanish: {truth}.'
  elif 'Singular Matrices'in title:
   if 'not** have an inverse'in p:truth=n!=m or M.det()==0;proof=f'Shape {n}×{m}; determinant '+(str(M.det())if n==m else 'undefined (nonsquare)')+'. Noninvertible iff nonsquare or determinant zero.'
   else:truth=n==m and M.det()==0;proof=f'Shape {n}×{m}; determinant '+(str(M.det())if n==m else 'undefined (nonsquare)')+'. Singular requires square and determinant zero.'
  elif 'Elementary'in title:truth=elementary(M);proof='Compared exactly with identity after one row swap, one nonzero row scaling, or one row addition; admissible single-operation result='+str(truth)+'.'
  elif 'Row Echelon Form'in title:
   E=M[:,:-1]if 'Augmented Matrices'in title or 'coefficient matrices'in p else M;truth=echelon(E)
   if '**not** in row echelon'in p:truth=not truth
   proof=f'Exact nonzero-row pivot indices and bottom-zero-row test on '+('coefficient block'if E!=M else 'displayed matrix')+': echelon='+str(echelon(E))+'.'
  elif 'Block Diagonal'in title:kind='lower'if 'block lower'in p else 'upper'if 'block upper'in p else 'diagonal';truth=block(M,kind);proof='Tested each proper contiguous partition for zero '+kind+' off-blocks; exists='+str(truth)+'.'
  elif 'Symmetric Matrices'in title:truth=n==m and M==M.T;proof='Entrywise exact comparison with transpose: symmetric='+str(truth)+'.'
  elif 'Zero Matrix'in title:truth=all(v==0 for v in M);proof='Every exact entry is zero='+str(truth)+'.'
  elif 'Jordan Blocks'in title:
   truth=n==m and all(M[i,j]==(M[0,0]if i==j else 1 if j==i+1 else 0)for i in range(n)for j in range(m));proof='Tested constant diagonal, unit superdiagonal, and zero elsewhere: Jordan block='+str(truth)+'.'
  elif 'Matrices of Quadratic Forms'in title:
   dim=int(re.search(r'\{R\}\^\{([234])\}',p).group(1));truth=n==m==dim and M==M.T;proof=f'Source convention uses symmetric {dim}×{dim} quadratic-form matrix: shape={n}×{m}, symmetric={n==m and M==M.T}.'
  elif 'Orthogonal Projection Matrix'in title:truth=n==m and M==M.T and M*M==M;proof='Exact symmetric and idempotent tests: '+str(truth)+'.'
  elif 'Stochastic Vectors and Stochastic Matrices'in title:truth=all(v>=0 for v in M)and all(sum(M[:,j])==1 for j in range(m));proof='Exact nonnegative-entry and unit column-sum test: '+str(truth)+'.'
  elif 'Given Rank'in title:
   rank=int(re.search(r'rank of \$(\d+)',p).group(1));truth=M.rank()==rank;proof=f'Exact rank={M.rank()}; requested={rank}.'
  if truth is not None:
   count+=1;a['proof']=proof;a['independent_truth']=bool(truth)
   if bool(truth)!=a['truth']:conflicts.append((q['ma_id'],a['label'],proof,q['correct_labels']));q['decision']='needs_evidence';q['reason']='Independent exact matrix calculation conflicts with database key; investigate before conversion.';q['proposed_prompt']=p
  else:skip.append(q['ma_id'])
 q['key_evidence']['independent_matrix_verification']=all('independent_truth'in a for a in q['atomic_options'])
data['counts']['decisions']=dict(collections.Counter(q['decision']for q in data['questions']));data['counts']['independently_checked_matrix_atoms']=count
f.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print('checked atoms',count,'conflicts',conflicts,'skip unique',sorted(set(skip)))
