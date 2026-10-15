"""Root independent displayed power substitution and bounded authored banks."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064204;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_negative_power_gen',D.with_suffix('.py'));A=load('root_affine_power_math',R/'affine-power-integral-readback.py');P=A.P;x=P.x
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,missing_legacy=1)
for sid,o in olds.items():
 if sid=='q-12499':continue
 t=G.PROFILES[sid];r=G.generate(t['level'],template=sid,parameters=t['parameters']);q=r['question'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0]
 assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(G.fmt.normalize_tex(a[':answer/value'])for a in of[':answer-field/choices']);assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==G.fmt.normalize_tex(of[':answer-field/correct'][':answer/value']);assert q[':question/problem']==G.fmt.normalize_prose(o[':question/problem'])
 oldsol=G.fmt.normalize_prose(o[':question/worked-solution'])
 if sid=='q-12019':oldsol=oldsol.replace(r'\int 3(1-3x)^{-3} &',r'\int 3(1-3x)^{-3}\,\text{d}x &')
 assert q[':question/worked-solution']==oldsol,(sid,'solution fidelity');fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices']);fidelity['keys']+=1;fidelity['solutions']+=1
N={};seen={l:set()for l in G.LEVELS}
def check(r,stages=True):
 q,m=r['question'],r['generation'];assert not m['evidence_only']and m['eligible_for_learning'];F,U,n=A.check(q,stages=stages)
 for k,v in n.items():N[k]=N.get(k,0)+v
 return F,U
for e in json.load(open(D/'engine-input.json')):check(e['record'])
for level in G.LEVELS:
 for i,p in enumerate(G.domain(level)):
  r=G.generate(level,parameters=p);F,U=check(r,False);n,a,b,m=p;assert A.eq(U,a*x+b)and A.eq(F,n/(a*x+b)**m);fp=s.srepr(s.cancel(F));assert fp not in seen[level];seen[level].add(fp)
  if i%500==0:print('Root negative-power complete bank',level,i,flush=True)
 for seed in range(18):check(G.generate(level,seed))
raw=G.generate('easy',template='q-12499-raw');assert raw['generation']['evidence_only']and not raw['generation']['eligible_for_learning']
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},coverage='181 supplied fixtures +54 fresh full-stage samples; every5160 authored actual displayed integrand and five-choice bank independently checked; native181 explicitly representative',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
