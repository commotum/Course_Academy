"""Independent readback of supplied matrices, operative stages and blank cells."""
import argparse,hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
P=module('root_matrix_arithmetic_scalar',R/'ode-scalar-parser.py')
def scalar(t):
 t=t.strip().rstrip('.,').strip()
 return s.Integer(1) if t=='' else s.Integer(-1) if t=='-' else P.scalar(t)
def matrices(t):
 out=[]
 for m in re.finditer(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',t,re.S):
  text=[[c.strip() for c in row.split('&')] for row in m[1].split(chr(92)*2)]
  width=len(text[0]);assert all(len(row)==width for row in text)
  out.append((s.Matrix([[scalar(c) for c in row] for row in text]),text))
 return out
def spans(t):return re.findall(r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',t)
def components(t):
 depth=0;positions=[]
 for i,c in enumerate(t):
  if c in '({':depth+=1
  elif c in ')}':depth-=1
  elif c in '+-' and i>0 and depth==0:positions.append(i)
 assert len(positions)==1,('Missing/changed entrywise addition stage',t)
 i=positions[0];return scalar(t[:i]),scalar(t[i:])
def run(K):
 D=R.parents[2]/f'generate/scratch/{K}';G=module('root_matrix_arithmetic_'+str(K),D.with_suffix('.py'));F=module('root_matrix_arithmetic_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
 C=dict(records=0,supplied_entries=0,repeated_input_entries=0,actual_product_operands=0,evaluated_scaled_entries=0,operative_combined_entries=0,collected_entries=0,choice_matrices=0,whole_bank_pairs=0,physical_blank_cells=0,provided_cells=0,actual_prose_coefficients=0)
 records=json.loads((R/f'qa/{K}-sampled.json').read_text());review=json.loads((D/'review.json').read_text())
 if isinstance(review,dict):review=review.get('generated',[])
 for row in review:
  r=row.get('record',row)
  if 'question' in r and r['question'].get(':question/worked-solution') and not r['generation'].get('evidence_only') and not r['generation'].get('raw_source_replay') and ':question/difficulty' in r['question']:records.append(r)
 for r in records:
  q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];inputs=matrices(prompt);first=spans(prompt)[0].strip().rstrip('.,');proof=matrices(sol)
  if K==17592186059740:
   assert len(inputs)==1;A=inputs[0][0];C['supplied_entries']+=len(A)
   factor=first.split(r'\begin{bmatrix}')[0] if r'\begin{bmatrix}' in first else first[:-1];k=scalar(factor);target=k*A
   assert len(proof)==3 and proof[0][0]==A;C['repeated_input_entries']+=len(A)
   products=proof[1][1]
   for i in range(A.rows):
    for j in range(A.cols):
     operands=products[i][j].split(r'\cdot');assert len(operands)==2 and scalar(operands[0])==k and scalar(operands[1])==A[i,j];C['actual_product_operands']+=2
   assert proof[1][0]==target and proof[2][0]==target;C['collected_entries']+=len(A)
   pre=spans(sol.split('$$')[0]);coefficient=pre[-1];assert scalar(coefficient)==k;C['actual_prose_coefficients']+=1
  else:
   assert K==17592186059742 and len(inputs)==2;A,B=[a[0] for a in inputs];assert A.shape==B.shape;C['supplied_entries']+=len(A)+len(B)
   m=re.fullmatch(r'(.*?)([A-Z])([+-])(.*?)([A-Z])',first);assert m,(first,'two-scalar expression')
   k,l=scalar(m[1]),scalar(m[4]);sign=1 if m[3]=='+' else -1;target=k*A+sign*l*B
   assert len(proof)==8 and proof[0][0]==A and proof[1][0]==B;C['repeated_input_entries']+=2*len(A)
   for literal,M,coefficient in [(proof[2][1],A,k),(proof[3][1],B,l)]:
    for i in range(M.rows):
     for j in range(M.cols):
      operands=literal[i][j].split(r'\cdot');assert len(operands)==2 and scalar(operands[0])==coefficient and scalar(operands[1])==M[i,j];C['actual_product_operands']+=2
   assert proof[4][0]==k*A and proof[5][0]==l*B;C['evaluated_scaled_entries']+=2*len(A)
   for i in range(A.rows):
    for j in range(A.cols):
     left,right=components(proof[6][1][i][j]);assert left==k*A[i,j] and right==sign*l*B[i,j];C['operative_combined_entries']+=1
   assert proof[6][0]==target and proof[7][0]==target;C['collected_entries']+=len(A)
   pre=spans(sol.split('$$')[0]);assert len(pre)>=4 and scalar(pre[1])==k and scalar(pre[3])==l
   assert ('then add' if sign==1 else 'then subtract') in sol;C['actual_prose_coefficients']+=2
  fields=q[':question/answer-fields']
  if fields[0][':answer-field/type'].endswith('/radio'):
   assert len(fields)==1;f=fields[0];bank=[]
   for a in f[':answer-field/choices']:
    ms=matrices(a[':answer/value']);assert len(ms)==1;M=ms[0][0];assert M.shape==target.shape;bank.append(tuple(M));assert (M==target)==(a[':answer/id']==f[':answer-field/correct'][1]);C['choice_matrices']+=1
   assert len(bank)==5 and len(set(bank))==5;C['whole_bank_pairs']+=10
  else:
   # Read matrix cells at their actual Markdown columns, not field enumeration order.
   rows=[]
   for raw in prompt.splitlines():
    if not raw.startswith('|') or '---' in raw:continue
    cells=raw.split('|')[1:-1];located=[]
    for j,c in enumerate(cells):
     c=c.strip()
     if '{{' in c or re.fullmatch(r'\$[^$=]+\$',c):located.append((j,c))
    if located:rows.append(located)
   assert len(rows)==target.rows and all(len(row)==target.cols for row in rows)
   assert all([j for j,_ in row]==[j for j,_ in rows[0]] for row in rows),('Staggered matrix blank layout',rows)
   by={f[':answer-field/key']:f for f in fields};seen=set()
   for i,row in enumerate(rows):
    for j,(_,text) in enumerate(row):
     if text.startswith('{{'):
      key=text.removeprefix('{{').removesuffix('}}');seen.add(key);f=by[key];assert len(f[':answer-field/choices'])==1
      a=f[':answer-field/choices'][0];assert a[':answer/id']==f[':answer-field/correct'][1] and scalar(a[':answer/value'])==target[i,j];C['physical_blank_cells']+=1
     else:assert scalar(text[1:-1])==target[i,j];C['provided_cells']+=1
   assert seen==set(by)
  C['records']+=1
 result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0}
 (R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('kps',nargs='+',type=int);o=a.parse_args()
 for k in o.kps:run(k)
