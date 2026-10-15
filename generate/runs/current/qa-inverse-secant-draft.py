"""Parent full arcsec banks and all stages on both connected real domains."""
import sys,json,hashlib,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186064250;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_asec_gen',D.with_suffix('.py'));H=load('root_asec_reader',R/'inverse-substitution-readback.py');s=H.s
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};N=dict(records=0,source_banks=0,source_values=0,source_keys=0,raw=0);tasks={l:set()for l in('easy','moderate','hard')}
def check(r,sid=None):
 assert r['knowledge_point']['db_id']==K;F,n,sig=H.check(r['question'],arcsec=True);N['records']+=1
 for k,v in n.items():N[k]=N.get(k,0)+v
 if sid:
  of=olds[sid][':question/answer-fields'][0];old=[H.signature(H.scalar(a[':answer/value']))for a in of[':answer-field/choices']];assert len(old)==len(sig)and all(sig.count(z)==1 for z in old);f=r['question'][':question/answer-fields'][0];correct=H.signature(H.scalar(of[':answer-field/correct'][':answer/value']));assert correct==H.signature(H.scalar(next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])));N['source_banks']+=1;N['source_values']+=len(sig);N['source_keys']+=1
 tasks[r['question'][':question/difficulty'].split('/')[-1]].add(s.srepr(F))
for sid,o in olds.items():
 case=next(c for c in json.load(open(D/'source-cases.json'))if c['source_id']==sid);q=case['record']['question'];assert q==o;N['raw']+=1;check(G.generate(G.difficulty(sid),profile=sid,parameters=G.source_parameters(sid)),sid)
 eligible=[p for p in G.all_parameters(sid)if G.eligible(sid,p)]
 for p in(eligible[0],eligible[-1]):check(G.generate(G.difficulty(sid),profile=sid,parameters=p))
for p in G.all_parameters('authored-e-direct'):check(G.generate('easy',profile='authored-e-direct',parameters=p))
for r in json.load(open(D/'independent-role-review.json')):check(r)
for level in tasks:
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),source_and_readback=N,sampled_actual_integrands={l:len(t)for l,t in tasks.items()},domain_proof='Principal arcsec represented independently as acos(1/z). Actual derivative/formal-integral equalities checked separately on x=+sqrt(1+w²)/k and x=-sqrt(1+w²)/k, w>0, covering both entire |kx|>1 components. Absolute-value scaling and each basic/formal primitive retain these domains.',scope='Observed inverse-secant normalization and linear substitution, independent small numerator/slope/denominator roles. Missing E authored direct matched-du with reduced small positive rational slopes, same method supported by preceding fraction arithmetic; no affine shifts or new branch operations.',native='All fieldsradio. Source17accept68reject and1303variants1303accept5212reject, no unresolved; publicmetadata/capacity adapters checked separately.',database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
