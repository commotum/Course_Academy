import sys
sys.dont_write_bytecode=True
import json,re,hashlib,importlib.util,copy
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186100868;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=load('parent_variable_polynomial',R/'variable-matrix-scalar.py');s=p.s
C=dict(records=0,prompt_cells=0,printed_operand_cells=0,ordered_dot_factors=0,evaluated_individual_terms=0,collected_cells=0,answer_values=0,authored_banks=0,source_fields=0,source_values=0,source_keys=0,source_missing_keys=0,source_solutions=0)
def value(raw):return s.expand(p.scalar(raw))
def same(a,b):return s.expand(a-b)==0
def arrays(text):
 out=[]
 for m in re.finditer(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S):
  body=m[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  out.append([[z.strip() for z in row.split('&')] for row in body.split(chr(92)*2)])
 return out
def matrix(rows):return s.Matrix([[value(z) for z in row] for row in rows])
def signature(text):
 ar=arrays(text)
 if ar:assert len(ar)==1;return tuple(matrix(ar[0]))
 return (value(text),)
def equal(a,b):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
def terms(text):
 parts=[];depth=0;start=0
 for i,ch in enumerate(text):
  if ch in '({[':depth+=1
  elif ch in ')}]':depth-=1
  elif ch in '+-' and depth==0 and text[start:i].strip():parts.append(text[start:i]);start=i
 assert depth==0;parts.append(text[start:]);return parts

def check(record):
 q=record['question'];ar=arrays(q[':question/problem']);assert len(ar)>=2;A,V=map(matrix,ar[:2]);rows,cols=A.shape;assert rows==cols and rows in (2,3) and V.shape==(rows,1);target=A*V
 C['prompt_cells']+=rows*cols+rows
 for f in q[':question/answer-fields']:
  vals=[signature(z[':answer/value']) for z in f[':answer-field/choices']]
  for i,a in enumerate(vals):assert all(not equal(a,b) for b in vals[:i])
  wanted=tuple(target) if f[':answer-field/type'].endswith('/radio') else (target[int(f[':answer-field/key'].split('-')[-1])-1],)
  good=[equal(a,wanted) for a in vals];assert sum(good)==1
  if ':answer-field/correct' in f:assert good[next(i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  if record['generation']['profile']=='authored-operations' and len(vals)==5:
   T=list(target);bank=[T,[-z for z in T],list(A[:,1:]*V[1:,0]),list(A[:,:-1]*V[:-1,0])]
   sid=record['generation']['template']
   if sid=='q-127276':last=A*s.Matrix(list(V)[::-1])
   elif sid=='q-13556':last=s.Matrix(list(target)[::-1])
   elif sid=='q-127277':last=A*s.ones(rows,1)
   else:last=A*s.Matrix([-v if v.could_extract_minus_sign() else v for v in V])
   bank.append(list(last));assert all(sum(equal(a,b) for b in bank)==1 for a in vals);C['authored_banks']+=1
  C['answer_values']+=len(vals)
 sol=q[':question/worked-solution'];ar=arrays(sol);assert len(ar) in (4,5);assert matrix(ar[0])==A and matrix(ar[1])==V;C['printed_operand_cells']+=rows*cols+rows
 dot=ar[2];assert len(dot)==rows
 for i in range(rows):
  operands=terms(dot[i][0]);assert len(operands)==cols,(dot[i],operands)
  for j,term in enumerate(operands):
   factors=term.split(r'\cdot');assert len(factors)==2,term
   a,b=map(value,factors);assert same(a,A[i,j]) and same(b,V[j]);C['ordered_dot_factors']+=2
 if len(ar)==5:
  for i in range(rows):
   parts=terms(ar[3][i][0]);assert len(parts)==cols,(ar[3][i],parts)
   for j,z in enumerate(parts):assert same(value(z),A[i,j]*V[j]);C['evaluated_individual_terms']+=1
 assert matrix(ar[-1])==target;C['collected_cells']+=rows
 level=q[':question/difficulty'].split('/')[-1];caps={'easy':(3,6,6),'moderate':(6,6,7),'hard':(2,4,4)}[level]
 def maxcoef(expressions):
  out=0
  for z in expressions:
   syms=sorted(z.free_symbols,key=str);cs=s.Poly(s.expand(z),*syms).coeffs() if syms else [z];out=max(out,max(map(abs,cs)))
  return out
 assert maxcoef([*A,*V])<=caps[0] and maxcoef([A[i,j]*V[j] for i in range(rows) for j in range(cols)])<=caps[1] and maxcoef(target)<=caps[2]
 C['records']+=1

if __name__=='__main__':
 g=load('parent_variable_matrix_generator',D.with_suffix('.py'));f=load('parent_variable_format',R.parents[2]/'scripts/question_capture/math_format.py');source=json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text());assert source==json.loads((D/'source.json').read_text());originals={z[':question/math-academy-id']:z for z in source['record'][':knowledge-point/questions']}
 for case in json.loads((D/'source-cases.json').read_text()):
  r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile','observed')));check(r);q=r['question'];old=originals[case['source_id']]
  assert q[':question/problem']==f.normalize_prose(old[':question/problem'])
  if ':question/worked-solution' in old:
   # Mathematical glyph/collection normalization is independently checked above.
   mask=lambda text:re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)','[MATH]',text,flags=re.S)
   assert mask(q[':question/worked-solution'])==mask(old[':question/worked-solution']);assert len(arrays(q[':question/worked-solution']))==len(arrays(old[':question/worked-solution']));C['source_solutions']+=1
  for of,nf in zip(old[':question/answer-fields'],q[':question/answer-fields']):
   assert of[':answer-field/key']==nf[':answer-field/key'] and of[':answer-field/type'][':db/ident']==nf[':answer-field/type'];remaining=[signature(z[':answer/value']) for z in nf[':answer-field/choices']]
   for z in of[':answer-field/choices']:
    found=[i for i,a in enumerate(remaining) if equal(a,signature(z[':answer/value']))];assert len(found)==1;remaining.pop(found[0]);C['source_values']+=1
   assert not remaining;C['source_fields']+=1
   if ':answer-field/correct' in of:
    ans=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert equal(signature(ans),signature(of[':answer-field/correct'][':answer/value']));C['source_keys']+=1
   else:C['source_missing_keys']+=1
 samples=json.loads((R/'qa'/f'{K}-sampled.json').read_text())
 for z in samples:check(z)
 # Independently read every bounded hard row-gain combination, not just claims/counts.
 for name,t in g.TEMPLATES.items():
  if t['level']!='hard':continue
  for gains in g.HARD_ROW_GAINS[name]:
   baseline={'scales':{v:1 for v in t['variables']},'names':{v:v for v in t['variables']},'row_gains':list(gains)};check(g.generate('hard',template=name,parameters=baseline))
 mutant=copy.deepcopy(samples[0]);text=mutant['question'][':question/worked-solution'];mutant['question'][':question/worked-solution']=text.replace(r'\cdot','+',1);assert mutant['question'][':question/worked-solution']!=text;saved=copy.deepcopy(C)
 try:check(mutant)
 except AssertionError:pass
 else:raise AssertionError('Missing product survived unchanged key')
 C=saved;C.update(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),unchanged_key_missing_multiplication_rejected=True,database_writes=0)
 (R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
