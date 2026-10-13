"""Actual whole-matrix/subset choices, repeated arrays and every false witness."""
import json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186119772
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
def matrices(t):
 result={}
 for name,body in re.findall(r'([A-E])\s*=\s*\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',t,re.S):
  M=s.Matrix([[s.Integer(z.strip()) for z in row.split('&')] for row in body.split(r'\\')]);assert M.rows==M.cols
  if name in result:assert result[name]==M
  result[name]=M
 return result
def criterion(t):
 z=re.search(r'(upper|lower) triangular',t);assert z;return z[1]
def eligible(M,kind):return all(M[i,j]==0 for i in range(M.rows) for j in range(M.cols) if (i>j if kind=='upper' else i<j))
def subset(t):return tuple(sorted(re.findall(r'\$([A-E])\$',t)))
def raw(g):
 old=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];C=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,missing_keys=0)
 for c in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  src=next(z for z in old if c['source_id']==z[':question/math-academy-id']);level=src[':question/difficulty'][':db/ident'].split('/')[-1];q=g.generate(level,template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')))['question'];assert q[':question/problem']==src[':question/problem'] and q[':question/worked-solution']==src[':question/worked-solution'];assert q[':question/difficulty']==src[':question/difficulty'][':db/ident'];C['prompts']+=1;C['solutions']+=1;assert len(q[':question/answer-fields'])==len(src[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],src[':question/answer-fields']):
   assert f[':answer-field/type']==f0[':answer-field/type'][':db/ident']==':answer-field.type/radio' and f[':answer-field/key']==f0[':answer-field/key'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   if ':answer-field/correct' in f0:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];C['keys']+=1
   else:C['missing_keys']+=1
   C['fields']+=1;C['values']+=len(f[':answer-field/choices'])
 return C
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','selectiongen');source=raw(g);C=dict(records=0,actual_matrix_cells=0,zero_region_cells=0,repeated_easy_matrices=0,concrete_witnesses=0,choices=0,whole_banks=0,hard_full_object_coverage=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];level=q[':question/difficulty'].split('/')[-1];kind=criterion(q[':question/problem']);assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio';choices=f[':answer-field/choices'];M={}
  if level=='easy':
   for a in choices:
    z=matrices(a[':answer/value']);assert len(z)==1;M.update(z)
  else:M=matrices(q[':question/problem'])
  assert set(M)==set('ABC' if level=='moderate' else 'ABCDE') and len({tuple(mat) for mat in M.values()})==len(M);good=tuple(sorted(label for label,mat in M.items() if eligible(mat,kind)));bad=tuple(sorted(set(M)-set(good)));assert len(good)==1 if level=='easy' else len(good) in (1,2) if level=='moderate' else len(good) in (2,3)
  C['actual_matrix_cells']+=sum(z.rows*z.cols for z in M.values());C['zero_region_cells']+=sum(z.rows*(z.rows-1)//2 for z in M.values())
  bank=[]
  for a in choices:
   value=tuple(matrices(a[':answer/value'])) if level=='easy' else subset(a[':answer/value']);assert value not in bank;bank.append(value);assert (value==good)==(a[':answer/id']==f[':answer-field/correct'][1]);C['choices']+=1
  assert len(bank)==5 and bank.count(good)==1;C['whole_banks']+=1
  sol=q[':question/worked-solution'];assert 'a upper triangular' not in sol and 'an lower triangular' not in sol and 'a upper triangular' not in q[':question/problem'] and 'an lower triangular' not in q[':question/problem']
  side='below' if kind=='upper' else 'above'
  if level=='easy':
   assert matrices(sol)==M;C['repeated_easy_matrices']+=5;assert re.search(r'Notice that \$([A-E])\$',sol)[1]==good[0];negative=sol.split('By contrast, matrices ',1)[1].split(' each',1)[0];assert subset(negative)==bad;assert 'entries *'+side+'*' in sol and 'non-zero entry '+side in sol
  else:
   positive=sol.split(' since ',1)[0];negative=sol.split('\n\n',1)[1].split(' since ',1)[0];assert subset(positive)==good and subset(negative)==bad;assert 'entries '+side+' the main diagonal are zeros' in sol and 'element '+side+' the main diagonal' in sol
   witness=[]
   for name,i,j,value in re.findall(r'\{([a-e])\}_\{([1-4])([1-4])\}\s*& =(-?\d+)\\ne 0',sol):
    name=name.upper();i,j=int(i)-1,int(j)-1;assert M[name][i,j]==int(value)!=0 and (i>j if kind=='upper' else i<j);witness.append(name);C['concrete_witnesses']+=1
   assert tuple(sorted(witness))==bad
   if level=='hard':assert all(z.rows==4 for z in M.values()) and set().union(*map(set,bank))==set(M);C['hard_full_object_coverage']+=1
  C['records']+=1
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
