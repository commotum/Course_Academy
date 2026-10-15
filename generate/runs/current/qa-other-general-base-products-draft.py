"""Root all served exponential product stages, original banks and actual task aliases."""
import sys,json,hashlib,importlib.util,re
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186184350;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_other_exp_gen',D.with_suffix('.py'));H=load('root_other_exp_math',R/'general-base-substitution-readback.py');P=H.P;x=P.x
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,normal_source_solutions=0,incomplete=0)
for c in json.load(open(D/'source-cases.json')):
 o=olds[c['source_id']];q=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile'])['question'];assert q[':question/problem']==o[':question/problem'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
 if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fidelity['keys']+=1
 else:assert ':answer-field/correct'not in f
 if ':question/worked-solution'in o:
  assert q[':question/worked-solution']==o[':question/worked-solution'];fidelity['solutions']+=1
  p={key:G.DATA[c['template']][key]for key in G.DOMAINS[c['template']]};q=G.generate(c['level'],template=c['template'],parameters=p)['question'];assert q[':question/worked-solution']==G.fmt.normalize_prose(o[':question/worked-solution']);fidelity['normal_source_solutions']+=1
 else:assert ':question/worked-solution'not in q;fidelity['incomplete']+=1
N={};seen={l:set()for l in G.LEVELS}
def check(r):
 q,m=r['question'],r['generation'];F,U,n=H.indefinite(q)
 for k,v in n.items():N[k]=N.get(k,0)+v
 assert m['evidence_only']==(not m['eligible_for_learning'])
 if not m['evidence_only']:seen[q[':question/difficulty'].split('/')[-1]].add(H.task(F))
for i,e in enumerate(json.load(open(D/'native-input.json'))):
 check(e['record'])
 if i%100==0:print('Root other general-base products read',i,flush=True)
for level in G.LEVELS:
 for seed in range(18):check(G.generate(level,seed))
expected=json.load(open(D/'validation.json'))['finite_distinct_mathematical_tasks'];assert {l:len(v)for l,v in seen.items()}==expected,('actual prime-log task aliases', {l:len(v)for l,v in seen.items()},expected)
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},task_identity='Independent actual rendered integrand logarithmic derivative +leading nonzero coefficient, positive numeric base powers normalized through prime logarithms. Cross-profile/base/exponent aliases deduplicated.',scope='Authored hard negative quartic grounded canonical e14403, same ordered substitution steps and signed coefficient. q73800 missing metadata/solution authored separately; originals raw evidence only. Normal bank chain-factor/logarithm operations separate from transported observed banks.',native_scope='1243owned correct IDs accepted4972owned wrong IDs rejected;3729mathtext/foreign/malformed transport errors separately reported. No blank fields or blank equivalence claims.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
