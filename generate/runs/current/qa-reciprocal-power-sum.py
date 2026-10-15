"""Root full source-bank, integral-stage and semantic-domain audit."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186105716;D=R.parents[2]/f'generate/scratch/{K}'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_sum_gen',D.with_suffix('.py'));P=load('root_sum_math',R/'elementary-integral-readback.py');x=P.x;xp=s.Symbol('root_sum_positive_x',positive=True)
def eq(a,b):return P.eq(a.subs(x,xp),b.subs(x,xp),True)
N=dict(records=0,integral_sides=0,primitive_sides=0,formal_inputs=0,values=0,pairs=0,banks=0)
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};fidelity=dict(banks=0,values=0,solutions=0,prompts=0,existing_keys=0)
def prose(t):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$[^$]*\$','<MATH>',t,flags=re.S)).strip()
for c in json.load(open(D/'source-cases.json')):
 q=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile'])['question'];o=olds[c['source_id']];assert q[':question/problem']==G.fmt.normalize_prose(G.clean(o[':question/problem']));fidelity['prompts']+=1
 if ':question/worked-solution'in o:
  assert q[':question/worked-solution']==G.fmt.normalize_prose(G.clean(o[':question/worked-solution']));fidelity['solutions']+=1
 for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
  nv=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];ov=[P.scalar(a[':answer/value'])for a in of[':answer-field/choices']];assert len(ov)==len(nv)and all(sum(eq(v,w)for w in nv)==1 for v in ov),('sourcebankgap',c['source_id'],ov,nv)
  if ':answer-field/correct'in of:
   v=P.scalar(of[':answer-field/correct'][':answer/value']);assert eq(v,next(w for a,w in zip(f[':answer-field/choices'],nv)if a[':answer/id']==f[':answer-field/correct'][1]));fidelity['existing_keys']+=1
  fidelity['banks']+=1;fidelity['values']+=len(ov)
seen={l:set()for l in ('easy','moderate','hard')}
def check(r):
 q,m=r['question'],r['generation'];body,var=P.prompt(q[':question/problem']);assert var==x
 for key,value in P.stages(q[':question/worked-solution'],body,var,positive=True).items():N[key]+=value
 assert len(q[':question/answer-fields'])==1;f=q[':question/answer-fields'][0];assert f[':answer-field/type'].endswith('/radio')and len(f[':answer-field/choices'])==5
 values=[P.derivative(P.scalar(a[':answer/value']),x)for a in f[':answer-field/choices']];hits=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if eq(v,body)];assert hits==[f[':answer-field/correct'][1]],(m['template'],hits,body,values)
 for i,v in enumerate(values):
  for w in values[:i]:assert not eq(v,w),('equivalentprimitivechoices',m['template'],m['parameters']);N['pairs']+=1
 N['records']+=1;N['values']+=len(values);N['banks']+=1;seen[q[':question/difficulty'].split('/')[-1]].add(str(s.expand(s.powdenest(body.subs(x,xp),force=True))))
for name,spec in G.TEMPLATES.items():
 for p in G.DOMAINS[name]:check(G.generate(spec['level'],template=name,parameters=p))
for level in seen:
 assert len(seen[level])=={'easy':157,'moderate':24,'hard':24}[level]
 for seed in range(18):check(G.generate(level,seed))
 batch=G.generate_batch(level,count=len(seen[level]),seed=39);assert len({r['generation']['mathematical_task_fingerprint']for r in batch})==len(seen[level])
 try:G.generate_batch(level,count=len(seen[level])+1)
 except ValueError:pass
 else:raise AssertionError('finite capacity bypass')
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
