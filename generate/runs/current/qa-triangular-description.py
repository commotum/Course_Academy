"""Independent actual-matrix regions, repeated arrays, and concrete witnesses."""
import json,re,hashlib,itertools,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186119771
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
def matrix(text):
 z=re.findall(r'([A-Z])\s*=\s*\[?\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\2\}',text,re.S);assert len(z)==1
 name,layout,body=z[0];rows=[[s.Integer(v.strip()) for v in row.split('&')] for row in body.split(r'\\')];M=s.Matrix(rows);assert M.rows==M.cols;return name,M
LABELS={'Identity matrix','Diagonal matrix','Upper triangular matrix','Lower triangular matrix','Other'}
def best(M):
 n=M.rows;upper=all(M[i,j]==0 for i in range(n) for j in range(n) if i>j);lower=all(M[i,j]==0 for i in range(n) for j in range(n) if i<j)
 return 'Identity matrix' if M==s.eye(n) else 'Diagonal matrix' if upper and lower else 'Upper triangular matrix' if upper else 'Lower triangular matrix' if lower else 'Other'
def raw(g):
 originals=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,unrated=0,missing_keys=0)
 for case in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  old=next(z for z in originals if case['source_id']==z[':question/math-academy-id']);q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert q[':question/problem']==old[':question/problem'];C['prompts']+=1
  for key in (':question/difficulty',':question/worked-solution'):assert (key in q)==(key in old)
  if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];C['solutions']+=1
  if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
  else:C['unrated']+=1
  assert len(q[':question/answer-fields'])==len(old[':question/answer-fields']);name,M=matrix(q[':question/problem']);answer=best(M)
  for f,f0 in zip(q[':question/answer-fields'],old[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert set(a[':answer/value'] for a in f[':answer-field/choices'])==LABELS;assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   if ':answer-field/correct' in f0:assert f0[':answer-field/correct'][':answer/value']==answer and next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==answer;C['keys']+=1
   else:C['missing_keys']+=1
   C['fields']+=1;C['values']+=len(f[':answer-field/choices'])
 return C
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','triangleparentgen');source=raw(g);C=dict(records=0,actual_region_cells=0,repeated_matrices=0,witnesses=0,complete_banks=0,choices=0,branches={})
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];name,M=matrix(q[':question/problem']);n=M.rows;answer=best(M);assert answer in LABELS-{'Identity matrix','Other'};level=q[':question/difficulty'].split('/')[-1]
  assert (n in (2,3) and answer!='Diagonal matrix') if level=='easy' else (n==3 and answer=='Diagonal matrix') if level=='moderate' else n==4
  sol=q[':question/worked-solution'];assert matrix(sol)==(name,M);C['repeated_matrices']+=1;region=re.search(r'all entries (above and below|above|below) the diagonal',sol);assert region
  want='above and below' if answer=='Diagonal matrix' else 'above' if answer=='Lower triangular matrix' else 'below';assert region[1]==want
  cells=[(i,j) for i in range(n) for j in range(n) if i!=j and (want=='above and below' or want=='above' and i<j or want=='below' and i>j)];assert all(M[i,j]==0 for i,j in cells);C['actual_region_cells']+=len(cells)
  assert ('Therefore, it is '+('an' if answer=='Upper triangular matrix' else 'a')+' '+answer.lower()+'.') in sol
  if answer!='Diagonal matrix':
   z=re.search(r'\$\{([ac])\}_\{(\d)(\d)\}=(-?\d+)\\ne 0\.\$',sol);assert z;char,i,j,value=z.groups();i,j=int(i)-1,int(j)-1;assert char==name.lower() and M[i,j]==int(value)!=0 and (i>j if answer=='Lower triangular matrix' else i<j);C['witnesses']+=1
  assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio';assert set(a[':answer/value'] for a in f[':answer-field/choices'])==LABELS and len(f[':answer-field/choices'])==5
  for a in f[':answer-field/choices']:assert (a[':answer/value']==answer)==(a[':answer/id']==f[':answer-field/correct'][1]);C['choices']+=1
  assert 'most specific listed description' in q[':question/problem'];C['complete_banks']+=1;C['records']+=1;C['branches'][answer]=C['branches'].get(answer,0)+1
 # Changing irrelevant strict-triangle diagonal entries cannot create tasks.
 pp={'matrix':[[2,0,0],[4,1,0],[0,-3,0]],'letter':'A','layout':'aligned'};a=g.generate_easy(template='lower',parameters=pp);pp['matrix']=[[0,0,0],[4,-9,0],[0,-3,1]];b=g.generate_easy(template='lower',parameters=pp);assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
