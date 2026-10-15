"""Root complete general-base affine domains, actual ordered endpoints and task aliases."""
import sys,json,hashlib,importlib.util,re,itertools,copy
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096656;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_affine_general_gen',D.with_suffix('.py'));H=load('root_affine_general_math',R/'general-base-substitution-readback.py');T=load('root_affine_general_limits',R/'trig-affine-integral-readback.py');B=load('root_affine_general_primitive',R/'definite-elementary-readback.py');P=H.P;x=P.x
T.primitive=B.primitive;T.D.primitive=B.primitive;T.eq=H.eq
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,incomplete=0)
for c in G.CASES:
 o=olds[c['source_id']];q=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='observed_raw')['question'];assert q[':question/problem']==o[':question/problem'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
 if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fidelity['keys']+=1
 else:assert ':answer-field/correct'not in f
 if ':question/worked-solution'in o:assert q[':question/worked-solution']==o[':question/worked-solution'];fidelity['solutions']+=1
 else:assert ':question/worked-solution'not in q;fidelity['incomplete']+=1
N={};seen={l:set()for l in G.SUPPORTED_LEVELS};counter=0

def check(r,authored=False):
 global counter
 q=copy.deepcopy(r['question']);m=r['generation'];assert m['evidence_only']==(not m['eligible_for_learning'])
 if ':question/worked-solution'not in q:return
 q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\quad\Longrightarrow\quad','⟹')
 F,lo,hi=T.given(q)
 if lo is None:F,U,n=H.indefinite(q)
 else:
  F,expected,n=T.check(q,False,True,False);n=dict(n,records=1);f=q[':question/answer-fields'][0];vals=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if H.eq(v,expected)]==[f[':answer-field/correct'][1]];n['values']=len(vals);n['pairs']=0
  for i,v in enumerate(vals):
   for w in vals[:i]:assert not H.eq(v,w);n['pairs']+=1
 for k,v in n.items():N[k]=N.get(k,0)+v
 if authored:seen[q[':question/difficulty'].split('/')[-1]].add((H.task(F),str(lo),str(hi)))
 counter+=1
 if counter%100==0:print('Root general-base affine actual stages read',counter,flush=True)
for c in G.CASES:
 for base in range(2,10):
  for profile in('observed_raw','method'):
   try:r=G.generate(c['level'],template=c['template'],parameters={'n':base},profile=profile)
   except ValueError as e:assert '4096'in str(e);continue
   check(r)
for level in G.SUPPORTED_LEVELS:
 for base,k,b,a,bounds in itertools.product(range(2,7),(-3,-2,-1,1,2,3),range(-3,4),(1,)if level=='easy'else(1,2,3),(None,)if level=='easy'else((0,1),(0,2),(0,3),(1,2),(1,3))):
  p=dict(n=base,k=k,b=b,a=a)
  if bounds:p.update(L=bounds[0],H=bounds[1])
  try:G.authored_bounds(level,p)
  except ValueError:continue
  check(G.generate(level,template='affine',parameters=p),True)
 for seed in range(18):check(G.generate(level,seed))
 expected=json.load(open(D/'validation.json'))['domain']['authored_unique_math_tasks'][level];assert len(seen[level])==expected,(level,len(seen[level]),expected)
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},task_identity='Actual printed exponential logarithmic derivative and leading coefficient, prime logs and actual bounds; cross-base/slope/shift aliases deduplicated independently.',native_limitations='Native review46records/296checks:60accepted170rejected66expectedradio nonidentity errors;10valid raw-round equivalents rejected separately, all14 reviewed normal equivalent entries accepted. Native review coverage is representative, not full bounded-domain grading.',approval_scope='Local docs3–7; exact source wording restrictions remain only in raw evidence; normal Give an exact answer. No engine changes.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
