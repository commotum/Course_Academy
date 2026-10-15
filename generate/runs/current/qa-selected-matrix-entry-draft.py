import sys
sys.dont_write_bytecode=True
import json,re,copy,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186100873;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
h=load('root_selected_integer_math',R/'qa-full-matrix-product-draft.py');arrays=h.arrays;matrix=h.matrix;number=h.number
counts=dict(records=0,source_values=0,source_banks=0,source_keys=0,missing_source_keys=0,source_solutions=0,ordered_operand_factors=0,evaluated_terms=0,scalar_stages=0,whole_banks=0,indexed_full_product_contexts=0,raw_imprecise_full_product_contexts=0)
def terms(text):
 out=[];depth=0;start=0
 for i,ch in enumerate(text):
  if ch in '({[':depth+=1
  elif ch in ')}]':depth-=1
  elif ch in '+-' and depth==0 and text[start:i].strip():out.append(text[start:i]);start=i
 assert depth==0;out.append(text[start:]);return out

def given(q):
 ar=arrays(q[':question/problem']);assert len(ar)==2;A,B=map(matrix,ar);m=re.search(r'\{?([a-z])\}?_\{([1-5])([1-5])\}',q[':question/problem']);assert m;i,j=int(m[2]),int(m[3]);assert 1<=i<=A.rows and 1<=j<=B.cols and A.cols==B.rows
 return A,B,i,j,m[1]
def check(record):
 q=record['question'];meta=record['generation'];A,B,i,j,letter=given(q);row=list(A[i-1,:]);col=list(B[:,j-1]);products=[a*b for a,b in zip(row,col)];target=sum(products);f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1;values=[number(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(values))==len(values)
 if ':answer-field/correct' in f:assert number(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))==target
 if not meta['evidence_only']:
  assert sum(v==target for v in values)==1
  if f[':answer-field/type'].endswith('/radio'):
   profile=meta['bank_profile']
   if profile=='method-omit-sign':expected=[target,sum(products[:-1]),sum(map(abs,products)),-target,sum(row)+sum(col)]
   else:assert profile=='method-reverse-column';expected=[target,sum(x*y for x,y in zip(row,col[::-1])),products[0],sum(products[1:]),sum(x*x for x in row)]
   assert set(values)==set(expected);counts['whole_banks']+=1
  level=q[':question/difficulty'].split('/')[-1];assert max(map(abs,row+col))<=10 and max(map(abs,products))<=30 and sum(map(abs,products))<=58
  if level=='easy':assert sum(v!=0 for v in products)>=2 and (len(products)!=3 or any(abs(a)<=1 or abs(b)<=1 for a,b in zip(row,col)))
  else:
   assert len(products)==3 and all(2<=abs(v)<=6 for v in row+col)
   if level=='moderate':assert max(map(abs,products))<=16 and 12<=sum(map(abs,products))<=36
   else:assert level=='hard' and 37<=sum(map(abs,products))<=58 and min(products)<0<max(products)
 if ':question/worked-solution' in q:
  text=q[':question/worked-solution'];body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[1];safe=re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',lambda m:m[0].replace(chr(92)*2,'§ROW§'),body,flags=re.S);rows=[z.replace('§ROW§',chr(92)*2) for z in safe.split(chr(92)*2)];assert len(rows)==5
  rhs=[line.split('=',1)[1].strip() for line in rows];assert re.search(r'_\{'+str(i)+str(j)+r'\}',rows[0].split('=',1)[0]);full=arrays(rhs[0]);assert len(full)==2 and matrix(full[0])==A and matrix(full[1])==B
  if meta['evidence_only']:counts['raw_imprecise_full_product_contexts']+=1
  else:
   # A scalar entry must equal the selected entry of the complete product.
   assert re.search(r'_\{'+str(i)+str(j)+r'\}\s*$',rhs[0]),rhs[0];counts['indexed_full_product_contexts']+=1
  selected=arrays(rhs[1]);assert len(selected)==2 and matrix(selected[0])==s.Matrix([row]) and matrix(selected[1])==s.Matrix(col)
  shownterms=terms(rhs[2]);assert len(shownterms)==len(products)
  for k,term in enumerate(shownterms):
   term=term.strip().removeprefix('+').strip()
   if r'\cdot' in term:a,b=map(number,term.split(r'\cdot'))
   else:
    m=re.fullmatch(r'\s*(\(-?\d+\)|-?\d+)\((-?\d+)\)\s*',term);assert m,term;a,b=number(m[1]),number(m[2])
   assert (a,b)==(row[k],col[k]);counts['ordered_operand_factors']+=2
  assert [number(z) for z in terms(rhs[3])]==products;assert number(rhs[4].rstrip('.'))==target;counts['evaluated_terms']+=len(products);counts['scalar_stages']+=3
  assert '$'+str(i)+'$'+('st' if i==1 else 'nd' if i==2 else 'rd' if i==3 else 'th')+' row' in text
  assert '$'+str(j)+'$'+('st' if j==1 else 'nd' if j==2 else 'rd' if j==3 else 'th')+' column' in text
 counts['records']+=1

if __name__=='__main__':
 g=load('root_selected_entry_generation',D.with_suffix('.py'));fmt=load('root_selected_entry_format',R.parents[2]/'scripts/question_capture/math_format.py');src=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert src==json.loads((D/'source.json').read_text());originals={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.loads((D/'source-cases.json').read_text()):
  r=g.generate(c.get('level',c.get('difficulty')),template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')));q=r['question'];old=originals[c.get('math_academy_id',c['source_id'])];check(r);of,nf=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert of[':answer-field/key']==nf[':answer-field/key'] and of[':answer-field/type'][':db/ident']==nf[':answer-field/type'];assert sorted(number(a[':answer/value']) for a in of[':answer-field/choices'])==sorted(number(a[':answer/value']) for a in nf[':answer-field/choices']);counts['source_values']+=len(of[':answer-field/choices']);counts['source_banks']+=1
  assert q[':question/problem']==fmt.normalize_prose(old[':question/problem'])
  for key in (':question/worked-solution',':question/difficulty'):assert(key in old)==(key in q)
  if ':question/worked-solution' in old:assert q[':question/worked-solution']==fmt.normalize_prose(old[':question/worked-solution']);counts['source_solutions']+=1
  if ':answer-field/correct' in of:
   actual=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert number(actual)==number(of[':answer-field/correct'][':answer/value']);counts['source_keys']+=1
  else:assert ':answer-field/correct' not in nf;counts['missing_source_keys']+=1
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for r in samples:check(r)
 for name,srcq in g.SOURCES.items():
  anchor=g.params(srcq)
  for i in range(1,len(anchor['A'])+1):
   for j in range(1,len(anchor['B'][0])+1):
    pars=copy.deepcopy(anchor);pars.update(row=i,column=j)
    try:r=g.generate('easy',template=name,parameters=pars)
    except ValueError:continue
    check(r);counts['held_matrix_changed_targets']=counts.get('held_matrix_changed_targets',0)+1
 probe=copy.deepcopy(samples[0]);text=probe['question'][':question/worked-solution'];bad=re.sub(r'(\\right\))_\{[1-5][1-5]\}',r'\1',text,count=1);assert text!=bad;probe['question'][':question/worked-solution']=bad;saved=copy.deepcopy(counts)
 try:check(probe)
 except AssertionError:pass
 else:raise AssertionError('Unindexed matrix product survived scalar equality')
 counts=saved;counts.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_missing_context_index_rejected=True,database_writes=0)
 (R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
