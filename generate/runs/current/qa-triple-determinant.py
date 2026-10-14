"""Root actual matrix rows, signed cofactor stages and complete wrong operations."""
import re,json,hashlib,sys,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186105736;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);sys.modules[name]=m;z.loader.exec_module(m);return m
b=load(R/'qa-parametric-scalar-line.py','triple_det_base');p=load(R/'triangle-readback.py','triple_det_parent');v=p.p;ARRAY=re.compile(r'\|\\begin\{aligned\}((?:(?!\\begin\{).)*?)\\end\{aligned\}\|',re.S)
C={k:0 for k in ('records','input_arrays','cofactor_minors','numeric_stages','signed_components','choices','whole_banks','hard_guards')}
def split(raw):
 depth=0;at=0;out=[]
 for j,ch in enumerate(raw):
  depth+=(ch in '({')-(ch in ')}')
  if j and depth==0 and ch in '+-':out.append(raw[at:j]);at=j
 out.append(raw[at:]);return out

def check(rec):
 q=rec['question'];text=q[':question/problem'];vectors={n:s.Matrix([v.scalar(c) for c in body.split(',')]) for n,body in re.findall(r'([a-z])\s*=\s*⟨(.*?)⟩',text)};assert len(vectors)==3;order=re.search(r'Find \$([a-z])\s*\\cdot\s*\(([a-z])\s*\\times\s*([a-z])',text);assert order;M=s.Matrix.vstack(*(vectors[n].T for n in order.groups()));answer=M.det();minors=[M.minor_submatrix(0,j) for j in range(3)];terms=[(-1)**j*M[0,j]*minors[j].det() for j in range(3)];sol=q[':question/worked-solution'];assert 'Remember that the scalar triple product' in sol and 'So, we have' in sol
 arrays=[]
 def save(m):arrays.append(m[0]);return 'MATRIX'+str(len(arrays)-1)
 block=ARRAY.sub(save,re.search(r'\$\$(.*?)\$\$',sol,re.S)[1]);assert len(arrays)==4
 actual=[]
 for raw in arrays:actual.append(s.Matrix([[v.scalar(cell) for cell in row.split('&')] for row in ARRAY.fullmatch(raw)[1].split(chr(92)*2)]))
 assert actual==[M]+minors;C['input_arrays']+=1;C['cofactor_minors']+=3
 rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').split(chr(92)*2)
 for idx,row in enumerate(rows):
  if '=' not in row:continue
  rhs=row.split('=',1)[1].strip().rstrip('.,');rhs=re.sub(r'MATRIX(\d+)',lambda m:arrays[int(m[1])],rhs);got=p.expression(rhs,dict(kind='vectors',vals={},arrows={},scalars={}));assert s.simplify(got-answer)==0,(row,got,answer);C['numeric_stages']+=1
  if idx>1:
   components=split(rhs)
   if len(components)==3:
    vals=[v.scalar(t) for t in components];assert vals==terms,(rhs,vals,terms);C['signed_components']+=3
 f=q[':question/answer-fields'][0];vs=[v.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(vs))==len(vs);ref=f[':answer-field/correct'][1];assert next(a[':answer/id'] for a,value in zip(f[':answer-field/choices'],vs) if value==answer)==ref
 if f[':answer-field/type'].endswith('/radio'):
  active=[j for j in range(3) if M[0,j]!=0];unweighted=sum((-1)**j*minors[j].det() for j in range(3));profile=rec['generation']['profile']
  if profile=='cofactor_signs':
   wrong=sum((-1)**j*M[0,j]*(minors[j][0,0]*minors[j][1,1]+minors[j][0,1]*minors[j][1,0]) for j in range(3));bank=[answer,-answer,answer-2*terms[active[0]],unweighted,wrong]
  else:assert profile=='omit_terms';bank=[answer,-answer,answer-terms[active[0]],answer-terms[active[1]],unweighted]
  assert set(vs)==set(bank);C['whole_banks']+=1
 else:assert '{{'+f[':answer-field/key']+'}}' in text and vs==[answer]
 if q[':question/difficulty'].endswith('/hard'):assert all(2<=abs(z)<=6 for z in M) and all(abs(z)>=4 for z in M[0,:]) and sum(bool(z<0) for z in M)>=3;C['hard_guards']+=1
 C['choices']+=len(vs);C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_det_gen');source=b.raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for fam,lev in g.LEVELS.items():records.append(g.generate(lev,template=fam,seed=537))
 for z in records:check(z)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
