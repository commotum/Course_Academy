"""Root actual forcing identities and all source operation chains."""
import importlib.util,json,re,hashlib,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186087868;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_ho_parser');x,y,z=p.x,p.y,p.z;g=load(D.with_suffix('.py'),'root_ho_g');f=load(R/'root-source-fidelity.py','root_ho_fid');originals,S=f.check(g,K,D)
def scalar(v):return p.scalar(v.replace('{y}^{′}','z').strip().rstrip('.,'))
def equation(v):
 left,right=v.replace('&','').split('=');return scalar(left),scalar(right)
def normalized(v):
 left,right=equation(v);res=s.expand(left-right);a=res.coeff(z);assert a!=0 and not a.has(x,y,z);res=s.expand(res/a);assert s.diff(res,z)==1 and s.diff(res,y,2)==0
 return res,s.expand(-res.subs({y:0,z:0}))
def subset(v):return frozenset(re.findall(r'\b(?:III|II|I)\b',v))
C=dict(records=0,prompt_equations=0,forcing_identities=0,printed_operation_rows=0,displayed_forcing_functions=0,individual_classifications=0,choice_subsets=0,criterion_pairs=0,source_shared_prose=0)
records=json.load(open(R/f'qa/{K}-sampled.json'));records.extend(g.generate(r['level'],template=t,seed=n) for t,r in g.RECIPES.items() for n in (631,917))
for rec in records:
 q=rec['question'];md=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];level=q[':question/difficulty'].split('/')[-1]
 equations=re.findall(r'^- \$(.*?)\$',md,re.M);assert len(equations)==3;residuals,forcing=zip(*(normalized(e) for e in equations));C['prompt_equations']+=3;C['forcing_identities']+=3
 target='inhomogeneous' if re.search(r'are\s+inhomogeneous',md) else 'homogeneous';bits=[(Q!=0)==(target=='inhomogeneous') for Q in forcing];want=frozenset(n for n,v in zip(['I','II','III'],bits) if v)
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];subsets=[subset(a[':answer/value']) for a in choices];assert len(choices)==5 and len(set(subsets))==5;assert [a[':answer/id'] for a,b in zip(choices,subsets) if b==want]==[field[':answer-field/correct'][1]];C['choice_subsets']+=5;C['criterion_pairs']+=10
 blocks=re.split(r'- (?:First|Next|Finally), we consider',sol)[1:];assert len(blocks)==3
 for i,block in enumerate(blocks):
  for raw in re.findall(r'\$\$(.*?)\$\$',block,re.S):
   rows=raw.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(chr(92)*2) if r'\begin{aligned}' in raw else [raw]
   for row in rows:
    actual,Q=normalized(row);assert s.expand(actual-residuals[i])==0 and s.expand(Q-forcing[i])==0;C['printed_operation_rows']+=1
   if level=='hard' and len(rows)>1:assert len(rows)==4
  if level=='hard':
   Q=scalar(re.search(r'\$Q\(x\)=(.*?)\$',block)[1]);assert s.expand(Q-forcing[i])==0;assert ('not identically zero' in block)==(Q!=0);assert 'this equation is '+('inhomogeneous' if Q!=0 else 'homogeneous') in block;C['displayed_forcing_functions']+=1
  else:
   # Final classification is printed in the family-specific source sentence.
   text=re.sub(r'\$.*?\$','',block)
   if forcing[i]!=0:assert 'inhomogeneous' in text or re.search(r'not\W+homogeneous',text),(family,i,text)
   else:assert 'homogeneous' in text and 'inhomogeneous' not in text.split('Therefore,')[-1]
  C['individual_classifications']+=1
 conclusion=re.search(r'correct answer is "(.*?)"',sol)[1];assert subset(conclusion)==want
 if family in originals:
  clean=lambda v:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',v,flags=re.S)).strip();assert clean(sol)==clean(originals[family][':question/worked-solution']);C['source_shared_prose']+=1
 C['records']+=1
out=dict(status='passed',source=S,readback=C,finite_semantic_domain={'easy':6,'moderate':6,'hard':3},script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
