"""Root whole original banks, quotient stages, constant rewrites and each endpoint."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068918;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_trigquotient_gen',D.with_suffix('.py'));H=load('root_trigquotient_math',R/'trig-quotient-integral-readback.py');P=H.P;x=P.x
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,incomplete=0)
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];q=G.generate(c['difficulty'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question'];assert q[':question/problem']==o[':question/problem'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
 if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fidelity['keys']+=1
 else:assert ':answer-field/correct'not in f
 if ':question/worked-solution'in o:assert q[':question/worked-solution']==o[':question/worked-solution'];H.check(o);fidelity['solutions']+=1
 else:assert ':question/worked-solution'not in q;fidelity['incomplete']+=1
N=dict(records=0,values=0,pairs=0,blanks=0,raw_source_errors=0);seen={l:set()for l in G.LEVELS}
def check(r):
 q,m=r['question'],r['generation'];F,expected,n=H.check(q)
 for k,v in n.items():N[k]=N.get(k,0)+v
 assert m['evidence_only']==(not m['eligible_for_learning'])
 if m['evidence_only']:N['raw_source_errors']+=m['template']=='q-10045';return
 f=q[':question/answer-fields'][0];vals=[P.scalar(H.A.mathnorm(a[':answer/value']))for a in f[':answer-field/choices']];ds=[P.derivative(v,x)if expected is None else v for v in vals];answer=F if expected is None else expected;assert[a[':answer/id']for a,d in zip(f[':answer-field/choices'],ds)if H.eq(d,answer)]==[f[':answer-field/correct'][1]]
 for i,d in enumerate(ds):
  for e in ds[:i]:assert not H.eq(d,e);N['pairs']+=1
 N['records']+=1;N['values']+=len(vals);N['blanks']+=f[':answer-field/type'].endswith('/blank');seen[q[':question/difficulty'].split('/')[-1]].add(str(F)+'|'+str(H.T.given({**q,':question/problem':H.A.mathnorm(q[':question/problem'])})[1:]))
for i,e in enumerate(json.load(open(D/'native-input.json'))):
 check(e['record'])
 if i%40==0:print('Root trig quotient actual stages read',i,flush=True)
for level in G.LEVELS:
 for seed in range(18):check(G.generate(level,seed))
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},scope='Authored easy direct sine quotient and missing moderate familiar-angle secant/shifted-sine quotient preserve actual orderedlesson substitution/logarithm workload. Hard retains original definite/negative-reciprocal/nested-argument/u−constant-rewrite profiles. Historical ambiguous/nonreal banks kept exact ineligible evidence.',native_limitations={'records':175,'accepted':175,'rejected':665,'unresolved_nonidentity':408,'legitimate_blank_equivalents_unresolved':36,'detail':'Uncollected endpoint log differences remain a valid-math native compatibility gap under normal exact wording; raw round/form restrictions measured separately. No outputs excluded or engine changes.'},approval_scope='Local docs3–7 with true frozen blank-equivalence limitations disclosed.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
