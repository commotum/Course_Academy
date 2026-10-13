"""Independent actual statements, matrices, proof regions and full subset banks."""
import json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186119784
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
def matrices(t):
 return [s.Matrix([[s.Integer(z.strip()) for z in row.split('&')] for row in body.split(r'\\')]) for mode,body in re.findall(r'\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\1\}',t,re.S)]
def parse(t):
 M=matrices(t);assert len(M)==1;A=M[0];z=re.findall(r'\$([^$]*)\$ is (upper triangular|lower triangular|diagonal)',t);assert len(z)==3
 return A,z
def expression(A,t):
 t=re.sub(r'[{}\s]','',t);name=next(z for z in t if z.isalpha() and z!='T');t=t.replace(name,'A');return {'A':A,'A^T':A.T,'A^T+A':A.T+A,'A+A^T':A+A.T,'A^T-A':A.T-A,'A-A^T':A-A.T}[t]
def cells(n,kind):return [(i,j) for i in range(n) for j in range(n) if i>j] if kind=='upper triangular' else [(i,j) for i in range(n) for j in range(n) if i<j] if kind=='lower triangular' else [(i,j) for i in range(n) for j in range(n) if i!=j]
def truth(M,kind):return all(M[i,j]==0 for i,j in cells(M.rows,kind))
def subset(t):return tuple(re.findall(r'\b(?:III|II|I)\b',t))
def raw(g):
 old=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,solutions=0,banks=0,values=0,keys=0,unrated=0,missing_keys=0)
 for c in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  src=next(z for z in old if c['source_id']==z[':question/math-academy-id']);level=src.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/hard').split('/')[-1];q=g.generate(level,template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')))['question'];assert q[':question/problem']==src[':question/problem'];C['prompts']+=1
  for key in (':question/difficulty',':question/worked-solution'):assert (key in q)==(key in src)
  if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution'];C['solutions']+=1
  if ':question/difficulty' in src:assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
  else:C['unrated']+=1
  A,ss=parse(q[':question/problem']);correct=tuple(k for k,(expr,kind) in zip(('I','II','III'),ss) if truth(expression(A,expr),kind));assert len(q[':question/answer-fields'])==len(src[':question/answer-fields'])==1
  f=q[':question/answer-fields'][0];f0=src[':question/answer-fields'][0];assert f[':answer-field/type']==f0[':answer-field/type'][':db/ident']==':answer-field.type/radio' and f[':answer-field/key']==f0[':answer-field/key'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
  if ':answer-field/correct' in f0:assert subset(f0[':answer-field/correct'][':answer/value'])==correct and next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];C['keys']+=1
  else:C['missing_keys']+=1
  C['banks']+=1;C['values']+=len(f[':answer-field/choices'])
 return C
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','statementsgen');source=raw(g);C=dict(records=0,statements=0,transformed_matrix_cells=0,proof_region_cells=0,reason_regions=0,conclusions=0,choices=0,whole_banks=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];A,ss=parse(q[':question/problem']);want=[expression(A,z) for z,k in ss];valid=[truth(M,k) for M,(z,k) in zip(want,ss)];correct=tuple(k for k,v in zip(('I','II','III'),valid) if v);sol=q[':question/worked-solution'];displayed=matrices(sol);assert displayed==want;C['transformed_matrix_cells']+=sum(M.rows*M.cols for M in displayed)
  proofs=re.split(r'- Statement (III|II|I) is ',sol)[1:];assert len(proofs)==6
  for i in range(3):
   numeral,proof=proofs[2*i:2*i+2];assert numeral==('I','II','III')[i] and proof.startswith('true' if valid[i] else 'false');M=want[i];kind=ss[i][1];region=cells(M.rows,kind);assert all(M[a,b]==0 for a,b in region)==valid[i];C['proof_region_cells']+=len(region)
   side='below' if kind=='upper triangular' else 'above' if kind=='lower triangular' else 'off';assert re.search(r'\b'+side+r'\b[^\n]*main diagonal',proof),proof;C['reason_regions']+=1
   # Reject a stale base referent: each proof's matrix label must match its
   # actual statement even when a transpose changes the forbidden side.
   actual=ss[i][0];names=re.findall(r'\$([^$]+)\$ has non-zero',proof)
   if names:assert re.sub(r'[{}\s]','',names[0])==re.sub(r'[{}\s]','',actual),(proof,actual)
   C['statements']+=1
  end=re.search(r'Therefore, the correct answer is "(.*?)"',sol);assert end and subset(end[1])==correct;C['conclusions']+=1
  assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio';banks=[]
  for a in f[':answer-field/choices']:
   value=subset(a[':answer/value']);assert value not in banks;assert (value==correct)==(a[':answer/id']==f[':answer-field/correct'][1]);banks.append(value);C['choices']+=1
  assert len(banks)==5 and banks.count(correct)==1;C['whole_banks']+=1;C['records']+=1
  level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert A.rows==3 and all(expression(A,z)==A for z,k in ss) and [k for z,k in ss]==['upper triangular','lower triangular','diagonal']
  elif level=='moderate':assert any('^' in z for z,k in ss) and all('+' not in z and '-' not in z for z,k in ss)
  else:assert any('+' in z or '-' in z for z,k in ss)
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
