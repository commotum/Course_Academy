import sys
sys.dont_write_bytecode=True
import re,json,hashlib,copy,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186100872;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
helper=load('root_matrix_dimensions_annotations',R/'qa-matrix-dimensions-given-draft.py')
C=dict(records=0,prompt_cells=0,ordered_product_factors=0,progressive_matrix_cells=0,answer_values=0,whole_method_banks=0,source_values=0,source_fields=0,source_keys=0,source_missing_keys=0,source_solutions=0,raw_operand_typos=0,raw_early_reveal_masks=0)
def number(text):
 text=text.strip().replace(r'\,','')
 if text[:1] in ('+','-') and text[1:].lstrip().startswith('('):return (1 if text[0]=='+' else -1)*number(text[1:])
 while text.startswith('(') and text.endswith(')'):text=text[1:-1].strip()
 assert re.fullmatch(r'[+-]?\s*\d+',text),text
 return s.Integer(text.replace(' ',''))
def arrays(text):return [[[z.strip() for z in row.split('&')] for row in m[1].split(chr(92)*2)] for m in re.finditer(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def matrix(a):return s.Matrix([[number(z) for z in row] for row in a])
def signature(text):
 ar=arrays(text)
 if ar:
  assert len(ar)==1;M=matrix(ar[0]);return (M.shape,tuple(M))
 return ((1,1),(number(text),))
def table_roles(prompt,target):
 roles={};rows=[]
 for line in prompt.splitlines():
  if not line.startswith('|') or re.search(r'\|\s*---',line):continue
  cells=[]
  for cell in line.strip('|').split('|'):
   cell=cell.strip()
   if not cell or '=' in cell:continue
   cells.append(cell)
  rows.append(cells)
 assert len(rows)==target.rows and all(len(row)==target.cols for row in rows),(rows,target.shape)
 for i,row in enumerate(rows):
  for j,cell in enumerate(row):
   mt=re.fullmatch(r'\{\{(field-\d+)\}\}',cell)
   if mt:roles[mt[1]]=(i,j)
   else:assert number(cell.strip('$'))==target[i,j]
 return roles

def check(record):
 q=record['question'];meta=record['generation'];ar=arrays(q[':question/problem']);assert len(ar)==2;A,B=map(matrix,ar);assert A.cols==B.rows;target=A*B;rows,inner,cols=A.rows,A.cols,B.cols;C['prompt_cells']+=A.rows*A.cols+B.rows*B.cols
 labels=re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}',q[':question/problem']);assert len(labels)==2;product=''.join(labels)
 blank=q[':question/answer-fields'][0][':answer-field/type'].endswith('/blank');roles=table_roles(q[':question/problem'],target) if blank else {};targets=sorted(roles.values()) if blank else [(i,j) for i in range(rows) for j in range(cols)]
 for f in q[':question/answer-fields']:
  values=[signature(a[':answer/value']) for a in f[':answer-field/choices']];expected=((1,1),(target[roles[f[':answer-field/key']]],)) if blank else (target.shape,tuple(target));assert sum(v==expected for v in values)==1
  if ':answer-field/correct' in f:assert signature(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))==expected
  if not meta.get('evidence_only'):assert len(set(values))==len(values)
  if not blank and meta['profile']=='method-sign-omission':
   omitted=A[:,:-1]*B[:-1,:];alternating=A*s.diag(*[(-1)**i for i in range(inner)])*B;expected_bank=[target,target.T,-target,omitted,alternating];assert set(values)=={(m.shape,tuple(m)) for m in expected_bank};C['whole_method_banks']+=1
  C['answer_values']+=len(values)
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];assert re.search(r'\{\\(?:cdot|times)\s*\}_\{✓\}',sol);ann=helper.annotations(sol);assert [z[0] for z in ann]==[*labels,product];assert [tuple(z[1]) for z in ann]==[(rows,inner),(inner,cols),(rows,cols)]
  group=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert group;ms=arrays(group[1]);assert len(ms)==3*len(targets)
  dots=re.findall(r'\\,\s*([+-]?\s*\d+)\s*=\s*(.*?)(?=\\\\|\\end\{aligned\}|$)',group[1],re.S);assert len(dots)==len(targets),(len(dots),len(targets),group[1])
  for z,(i,j) in enumerate(targets):
   left,right,partial=ms[3*z:3*z+3]
   if meta['profile']=='observed-raw' and meta['template']=='q-129495' and z==len(targets)-1:
    bad=copy.deepcopy(A);bad[0,0]=-bad[0,0];bad[0,1]=-bad[0,1];assert matrix(left)==bad;C['raw_operand_typos']+=1
   else:assert matrix(left)==A
   assert matrix(right)==B;assert number(dots[z][0])==target[i,j]
   factors=dots[z][1].strip().rstrip(',')
   terms=re.split(r'\+(?=(?:[^()]|\([^()]*\))*$)',factors);assert len(terms)==inner,(factors,terms)
   for k,term in enumerate(terms):
    pair=term.split(r'\cdot');assert len(pair)==2 and number(pair[0])==A[i,k] and number(pair[1])==B[k,j],(i,j,k,pair,A,B);C['ordered_product_factors']+=2
   assert len(partial)==rows and all(len(row)==cols for row in partial)
   future=set(targets[z+1:])
   for rr in range(rows):
    for cc in range(cols):
     if meta['profile']=='observed-raw' and meta['template']=='q-317846' and z==0:
      star=(rr,cc) in {(0,1),(1,0)};C['raw_early_reveal_masks']+=1
     else:star=(rr,cc) in future
     if star:assert partial[rr][cc] in ('∗','*')
     else:assert number(partial[rr][cc])==target[rr,cc]
     C['progressive_matrix_cells']+=1
  final=arrays(sol)[-1];assert matrix(final)==target
 level=q.get(':question/difficulty',':question.difficulty/easy').split('/')[-1]
 if not meta.get('evidence_only'):
  if level=='moderate':cap=(6,12,24,18);assert (rows,inner,cols)==(2,3,2) and all(v!=0 for v in [*A,*B])
  elif level=='hard':cap=(5,10,20,18);assert (rows,inner,cols)==(2,4,2) and all(v!=0 for v in [*A,*B])
  else:
   base=original_parameters[meta['template']];oldA,oldB=map(s.Matrix,(base['A'],base['B']));assert [v==0 for v in A]==[v==0 for v in oldA] and [v==0 for v in B]==[v==0 for v in oldB];cap=source_caps[meta['template']]
  assert max(abs(v) for v in [*A,*B])<=cap[0]
  assert max(abs(A[i,k]*B[k,j]) for i in range(rows) for j in range(cols) for k in range(inner))<=cap[1]
  assert max(sum(abs(A[i,k]*B[k,j]) for k in range(inner)) for i in range(rows) for j in range(cols))<=cap[2] and max(abs(v) for v in target)<=cap[3]
 C['records']+=1

if __name__=='__main__':
 G=load('root_full_matrix_generator',D.with_suffix('.py'));fmt=load('root_full_matrix_format',R.parents[2]/'scripts/question_capture/math_format.py');src=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert src==json.loads((D/'source.json').read_text());originals={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']};specs=json.loads((D/'replay-specifications.json').read_text());original_parameters={k:v['parameters'] for k,v in specs.items()};source_caps={k:tuple(v['bounds'][x] for x in ('coefficient','product','dot_l1','result')) for k,v in specs.items()}
 for c in json.loads((D/'source-cases.json').read_text()):
  r=G.generate(c.get('level',c.get('difficulty')),template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')));q=r['question'];old=originals[c.get('math_academy_id',c['source_id'])];check(r)
  assert q[':question/problem']==fmt.normalize_prose(old[':question/problem'])
  for key in (':question/worked-solution',':question/difficulty'):assert (key in old)==(key in q)
  if ':question/worked-solution' in old:assert helper.prose(old[':question/worked-solution'])==helper.prose(q[':question/worked-solution']);C['source_solutions']+=1
  for of in old[':question/answer-fields']:
   nf=next(f for f in q[':question/answer-fields'] if f[':answer-field/key']==of[':answer-field/key']);assert nf[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(signature(z[':answer/value']) for z in nf[':answer-field/choices'])==sorted(signature(z[':answer/value']) for z in of[':answer-field/choices']);C['source_values']+=len(of[':answer-field/choices']);C['source_fields']+=1
   if ':answer-field/correct' in of:
    answer=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert signature(answer)==signature(of[':answer-field/correct'][':answer/value']);C['source_keys']+=1
   else:assert ':answer-field/correct' not in nf;C['source_missing_keys']+=1
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for r in samples:check(r)
 # Complete held-input coverage of supported target maps for partial products.
 import itertools
 for name,sp in specs.items():
  if not sp['blank']:continue
  base=sp['parameters'];cells=[(i,j) for i in range(len(base['A'])) for j in range(len(base['B'][0]))]
  for targetmap in itertools.combinations(cells,len(base['targets'])):
   pars=copy.deepcopy(base);pars['targets']=list(map(list,targetmap));check(G.generate('easy',template=name,parameters=pars));C['held_inputs_target_variants']=C.get('held_inputs_target_variants',0)+1
 probe=copy.deepcopy(samples[0]);text=probe['question'][':question/worked-solution'];start=text.index(r'\begin{aligned}');probe['question'][':question/worked-solution']=text[:start]+text[start:].replace(r'\cdot','+',1);assert text!=probe['question'][':question/worked-solution'];saved=copy.deepcopy(C)
 try:check(probe)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Missing dot factor survived unchanged key')
 C=saved;C.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_missing_dot_product_rejected=True,database_writes=0)
 (R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
