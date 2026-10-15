"""Root original banks, nonlinear u/du, transformed bounds and signed endpoints."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068917;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_nonlin_trig_gen',D.with_suffix('.py'));H=load('root_nonlin_trig_math',R/'nonlinear-trig-integral-readback.py');T=H.T;P=H.P;x=P.x
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,prompts=0,incomplete=0)
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];r=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']);q=r['question'];assert q[':question/problem']==o[':question/problem'];fidelity['prompts']+=1;f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']and f[':answer-field/key']==of[':answer-field/key'];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
 if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fidelity['keys']+=1
 else:assert ':answer-field/correct'not in f
 if ':question/worked-solution'in o:assert q[':question/worked-solution']==o[':question/worked-solution'];H.check(o);fidelity['solutions']+=1
 else:assert ':question/worked-solution'not in q;fidelity['incomplete']+=1
N=dict(records=0,values=0,pairs=0,blanks=0,evidence_only=0);seen={l:set()for l in G.SUPPORTED_LEVELS}
def check(r):
 q,m=r['question'],r['generation'];F,expected,counts=H.check(q)
 for k,v in counts.items():N[k]=N.get(k,0)+v
 f=q[':question/answer-fields'][0];vals=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];ds=[P.derivative(v,x)if expected is None else v for v in vals];answer=F if expected is None else expected;assert [a[':answer/id']for a,d in zip(f[':answer-field/choices'],ds)if T.eq(d,answer)]==[f[':answer-field/correct'][1]]
 for i,d in enumerate(ds):
  for e in ds[:i]:assert not T.eq(d,e);N['pairs']+=1
 assert m['evidence_only']==(not m['eligible_for_learning']);N['evidence_only']+=m['evidence_only'];N['records']+=1;N['values']+=len(vals);N['blanks']+=f[':answer-field/type'].endswith('/blank')
 if not m['evidence_only']:seen[q[':question/difficulty'].split('/')[-1]].add(str(F)+'|'+str(T.given(q)[1:]))
for i,e in enumerate(json.load(open(D/'native-input.json'))):
 check(e['record'])
 if i%60==0:print('Root nonlinear trig actual stages read',i,flush=True)
for level in G.SUPPORTED_LEVELS:
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},scope='Authored easy exact derivative factor from immediately preceding nonlinear tutorial; moderate same nonlinear substitution with nonunit adjustment; hard source reciprocal negative differential or definite transformed endpoints. Original opaque zero-answer banks retained in explicit bounded evidence profiles; normal nonzero endpoints and complete method banks separately authored.',native_scope='Actual ownedID radio choices and canonical/equivalent scalar blanks measured separately from foreign/malformed/radio mathtext unresolved diagnostics. All standard mathematical native checks pass.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
