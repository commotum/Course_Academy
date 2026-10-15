"""Root audit reads actual supplied functions, formal inputs, targets and full banks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059677;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_second_gen',D.with_suffix('.py'));P=load('root_second_math',R/'higher-derivative-readback.py');x=P.x
N=dict(records=0,equalities=0,operands=0,targets=0,values=0,pairs=0,banks=0,blanks=0,zero_targets=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fidelity=dict(raw=0,served_banks=0,served_values=0,served_solutions=0)
for sid,old in olds.items():assert G.generate(profile='observed_raw',source_id=sid)['question']==old;fidelity['raw']+=1
for name,(level,kind) in G.FAITHFUL_SPECS.items():
 r=G.generate(level,template=name,parameters={'scale':1});q=r['question'];old=olds[r['generation']['source_id']]
 assert q[':question/problem']==G._fmt.normalize_prose(old[':question/problem']);assert q[':question/worked-solution']==G._fmt.normalize_prose(old[':question/worked-solution']);fidelity['served_solutions']+=1
 f=q[':question/answer-fields'][0];o=old[':question/answer-fields'][0];assert f[':answer-field/key']==o[':answer-field/key'] and f[':answer-field/type']==o[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(G._fmt.normalize_tex(a[':answer/value']) for a in o[':answer-field/choices']);assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==G._fmt.normalize_tex(o[':answer-field/correct'][':answer/value']);fidelity['served_banks']+=1;fidelity['served_values']+=len(f[':answer-field/choices'])
def check(r):
 q,m=r['question'],r['generation'];positive=m['domain']=='x>0';name,base,fun=P.givens(q[':question/problem'],positive)
 prompt=P.clean(q[':question/problem']);requested=re.search(r"([fgh])('')\((x|-?\d+)\)",prompt);assert requested and requested[1]==name
 at=None if requested[3]=='x' else s.Integer(requested[3]);answer=s.diff(fun,x,2-base);answer=answer.subs(x,at) if at is not None else answer;N['zero_targets']+=int(answer==0)
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);orders=([base] if base else [])+list(range(base+1,3))+([2] if at is not None else [])
 assert len(blocks)==len(orders),(m['template'],len(blocks),orders)
 for i,(block,order) in enumerate(zip(blocks,orders)):
  for key,count in P.stage(block,fun,name,base,order,at if i==len(blocks)-1 and at is not None else None,positive).items():N[key]+=count
 if at is not None:assert re.search(r'x\s*=\s*'+str(at)+r'(?:\$|\s|,)',q[':question/worked-solution']),('missing prose evaluation target',at)
 assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];values=[P.scalar(a[':answer/value'],positive) for a in f[':answer-field/choices']];key=f[':answer-field/correct'][1];hits=[a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if P.eq(v,answer,positive)];assert hits==[key],(m['template'],answer,hits,key)
 for i,v in enumerate(values):
  for w in values[:i]:assert not P.eq(v,w,positive);N['pairs']+=1
 N['values']+=len(values);N['banks']+=1;N['blanks']+=int(f[':answer-field/type'].endswith('/blank'));N['records']+=1
for name,spec in G.SPECS.items():
 for p in G.valid_parameters(name):check(G.generate(spec[0],template=name,parameters=p))
for name,(level,kind) in G.FAITHFUL_SPECS.items():
 for scale in G._faithful.SCALES:check(G.generate(level,template=name,parameters={'scale':scale}))
for level in ('easy','moderate','hard'):
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
