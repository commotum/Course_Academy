"""Parent banks, literal inverse operators, substitution and every operative stage."""
import sys,json,hashlib,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_inverse_gen',D.with_suffix('.py'));H=load('root_inverse_reader',R/'inverse-substitution-readback.py');s=H.s
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};N=dict(records=0,raw=0,banks=0,source_values=0,source_keys=0);tasks={l:set()for l in('easy','moderate','hard')}
def check(r,sid=None):
 F,n,sig=H.check(r['question']);N['records']+=1
 for k,v in n.items():N[k]=N.get(k,0)+v
 if sid:
  o=olds[sid];of=o[':question/answer-fields'][0];old=[H.signature(H.scalar(a[':answer/value']))for a in of[':answer-field/choices']];assert len(old)==len(sig)and all(sig.count(z)==1 for z in old);correct=H.signature(H.scalar(of[':answer-field/correct'][':answer/value']));f=r['question'][':question/answer-fields'][0];assert H.signature(H.scalar(next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])))==correct;N['banks']+=1;N['source_values']+=len(sig);N['source_keys']+=1
 tasks[r['question'][':question/difficulty'].split('/')[-1]].add(s.srepr(F))
for sid,o in olds.items():
 if K==17592186064218:
  assert G.source_record(sid,raw=True)==o;level=G.PROFILES[sid][0];params={'t':G.PROFILES[sid][2]};r=G.generate(level,profile=sid,parameters=params)
 else:
  c=next(c for c in json.load(open(D/'source-cases.json'))if c['source_id']==sid);level=G.PROFILES[sid]['difficulty'];params=G.PROFILES[sid]['parameters'];r=G.generate(level,template=sid,parameters=params)
 if K==17592186064219:
  assert r['question'][':question/problem']==G.normalize_prose(o[':question/problem'])and r['question'][':question/worked-solution']==G.normalize_prose(o[':question/worked-solution'])
 N['raw']+=1;check(r,sid)
if K==17592186064218:
 for sid in olds:
  for p in G.candidates(sid):check(G.generate(G.PROFILES[sid][0],profile=sid,parameters=p))
else:
 for sid in olds:
  pp=G.candidates(sid)
  for p in (pp[0],pp[len(pp)//2],pp[-1]):check(G.generate(G.PROFILES[sid]['difficulty'],template=sid,parameters=p))
for l in tasks:
 for seed in range(24):check(G.generate(l,seed))
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_integrands={l:len(t)for l,t in tasks.items()},scope='Actual linear inverse substitution, original inverse-function field contract and ordered elementary stages. Authored missing hard normalization uses known coefficient/radicand factoring, no new inverse function. Real domains/principal ranges retained.',native='All supported source/authored outputs radio; canonical owned IDs and wrongIDs pass. Hypothetical inverse-function blank diagnostics are separate response contracts, not normal generator failures.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
