import sys
sys.dont_write_bytecode=True
import re,json,copy,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186100913;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
h=load('root_outer_integer',R/'qa-full-matrix-product-draft.py');arrays=h.arrays;matrix=h.matrix;number=h.number
C=dict(records=0,ordered_factors=0,partial_cells=0,whole_banks=0,source_values=0,source_fields=0,source_keys=0,source_missing_keys=0,source_solutions=0)
def sig(t):
 if 'undefined' in t.lower():return ('undefined',)
 a=arrays(t)
 if a:assert len(a)==1;v=matrix(a[0]);return(v.shape,tuple(v))
 return ((1,1),(number(t.strip('$\n[] ')),))
def rows(t):
 text=re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',lambda m:m[0].replace(chr(92)*2,'§'),t,flags=re.S)
 return [z.replace('§',chr(92)*2) for z in text.split(chr(92)*2)]
def factors(t,a,b):
 pair=t.strip().rstrip('.,').split(r'\cdot');assert len(pair)==2 and number(pair[0])==a and number(pair[1])==b,(t,a,b);C['ordered_factors']+=2

def check(r):
 q=r['question'];g=r['generation'];ar=arrays(q[':question/problem']);assert len(ar)==2;A,B=map(matrix,ar);defined=A.cols==B.rows;P=A*B if defined else None
 normal=not g['evidence_only']
 if normal:
  assert A.cols==1 and B.rows==1;level=q[':question/difficulty'].split('/')[-1];nonunit=sum(1 for a in A for b in B if abs(a)>1 and abs(b)>1);work=sum(abs(v)for v in P);assert max(map(abs,[*A,*B]))<=10 and max(map(abs,P))<=50 and work<=240
  if level=='easy':assert nonunit<=4 and work<=150
  elif level=='moderate':assert P.shape==(3,2) and nonunit==6 and max(map(abs,[*A,*B]))<=5 and max(map(abs,P))<=15 and work<=60
  else:assert level=='hard' and P.shape==(4,3) and nonunit>=8
  assert any(A) and any(B)
 blank=q[':question/answer-fields'][0][':answer-field/type'].endswith('/blank');roles={}
 if blank:
  rr=[]
  for line in q[':question/problem'].splitlines():
   if line.startswith('|') and not re.search(r'\|\s*---',line):rr.append([z.strip()for z in line.strip('|').split('|')if '{{'in z])
  assert len(rr)==P.rows and all(len(z)==P.cols for z in rr)
  roles={re.fullmatch(r'\{\{(field-\d+)\}\}',v)[1]:(i,j)for i,row in enumerate(rr)for j,v in enumerate(row)}
 for f in q[':question/answer-fields']:
  vals=[sig(z[':answer/value'])for z in f[':answer-field/choices']];wanted=((1,1),(P[roles[f[':answer-field/key']]],))if blank else (P.shape,tuple(P)) if defined else ('undefined',)
  # SymPy prints matrix in another environment, so build the signature directly.
  if not blank and defined:wanted=(P.shape,tuple(P))
  if ':answer-field/correct'in f:assert sig(next(z[':answer/value']for z in f[':answer-field/choices']if z[':answer/id']==f[':answer-field/correct'][1]))==wanted
  if normal:
   assert len(set(vals))==len(vals) and vals.count(wanted)==1
   if not blank:
    E=[P,P.T,s.Matrix([[a+b for b in B]for a in A]),-P];assert set(vals)=={(z.shape,tuple(z))for z in E}|{('undefined',)};C['whole_banks']+=1
 if ':question/worked-solution'in q:
  sol=q[':question/worked-solution']
  if not defined:assert 'undefined' in sol.lower()
  else:
   body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1];ms=arrays(body)
   if P.shape==(2,2):
    assert len(ms)==12
    for k in range(4):
     left,right,part=ms[3*k:3*k+3];assert matrix(left)==A and matrix(right)==B
     for i in range(2):
      for j in range(2):
       if 2*i+j<=k:assert number(part[i][j])==P[i,j]
       else:assert part[i][j]in('∗','*')
       C['partial_cells']+=1
    for k,row in enumerate(rows(body)):
     m=re.search(r'\\,\s*(-?\d+)\s*=\s*(.*?)\s*$',row);assert m,row;i,j=divmod(k,2);assert number(m[1])==P[i,j];factors(m[2],A[i,0],B[0,j])
    assert matrix(arrays(sol)[-1])==P
   else:
    assert len(ms)==4 and matrix(ms[0])==A and matrix(ms[1])==B and matrix(ms[3])==P
    assert len(ms[2])==P.rows and all(len(z)==P.cols for z in ms[2])
    for i,row in enumerate(ms[2]):
     for j,t in enumerate(row):factors(t,A[i,0],B[0,j])
   assert '$'+str(A.rows)+r'\times 1$ matrix'in sol or '$'+str(A.rows)+r'\times 1$'in sol
   assert '$1'+r'\times '+str(B.cols)+'$ matrix'in sol
 C['records']+=1

if __name__=='__main__':
 G=load('root_outer_generator',D.with_suffix('.py'));fmt=load('root_outer_format',R.parents[2]/'scripts/question_capture/math_format.py');src=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert src==json.loads((D/'source.json').read_text());originals={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.loads((D/'source-cases.json').read_text()):
  r=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];o=originals[c['source_id']];check(r);assert q[':question/problem']==fmt.normalize_prose(o[':question/problem'])
  for key in (':question/worked-solution',':question/difficulty'):assert(key in o)==(key in q)
  if ':question/worked-solution'in o:assert q[':question/worked-solution']==fmt.normalize_prose(o[':question/worked-solution']);C['source_solutions']+=1
  for of in o[':question/answer-fields']:
   nf=next(f for f in q[':question/answer-fields']if f[':answer-field/key']==of[':answer-field/key']);assert nf[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(map(repr,[sig(z[':answer/value'])for z in of[':answer-field/choices']]))==sorted(map(repr,[sig(z[':answer/value'])for z in nf[':answer-field/choices']]));C['source_values']+=len(of[':answer-field/choices']);C['source_fields']+=1
   if ':answer-field/correct'in of:assert sig(of[':answer-field/correct'][':answer/value'])==sig(next(z[':answer/value']for z in nf[':answer-field/choices']if z[':answer/id']==nf[':answer-field/correct'][1]));C['source_keys']+=1
   else:assert ':answer-field/correct'not in nf;C['source_missing_keys']+=1
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for r in samples:check(r)
 histogram={i:0 for i in range(5)};contracts=set()
 for seed in range(200):
  r=G.generate('easy',seed=seed);check(r);A,B=map(matrix,arrays(r['question'][':question/problem']));n=sum(1 for a in A for b in B if abs(a)>1 and abs(b)>1);histogram[n]+=1;contracts.add((A.rows,B.cols,n,r['question'][':question/answer-fields'][0][':answer-field/type']))
 assert all(histogram.values());C['easy_nonunit_histogram']=histogram;C['easy_attainable_contracts_sampled']=len(contracts)
 probe=copy.deepcopy(samples[0]);text=probe['question'][':question/worked-solution'];start=text.index(r'\begin{aligned}');bad=text[:start]+text[start:].replace(r'\cdot','+',1);assert bad!=text;probe['question'][':question/worked-solution']=bad;saved=copy.deepcopy(C)
 try:check(probe)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Wrong printed factor operation survived unchanged key')
 C=saved;C.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_wrong_product_operation_rejected=True,database_writes=0);(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
