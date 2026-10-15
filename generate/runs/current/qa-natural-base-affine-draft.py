"""Root natural exponential affine domains, complete banks and individual endpoints."""
import sys,json,hashlib,importlib.util,re,itertools,copy
from pathlib import Path
from functools import lru_cache
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096655;D=R.parents[2]/f'generate/scratch/{K}-draft'
def load(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load('root_affine_natural_gen',D.with_suffix('.py'));H=load('root_affine_natural_math',R/'general-base-substitution-readback.py');T=load('root_affine_natural_limits',R/'trig-affine-integral-readback.py');B=load('root_affine_natural_primitive',R/'definite-elementary-readback.py');A=load('root_affine_natural_normalizer',R/'affine-power-integral-readback.py');P=H.P;x=P.x
@lru_cache(maxsize=40000)
def natural_equal(a,b):
 delta=s.expand(s.expand_power_exp((a-b).rewrite(s.exp)))
 return delta==0 or s.cancel(delta)==0
H.eq=natural_equal
T.primitive=B.primitive;T.D.primitive=B.primitive;T.eq=natural_equal
# Exponential endpoint rows also print a bare (upper)-(lower), without a common
# outer coefficient. Parse the actual two components before checking their sum.
original_components=T.endpoint_contributions
def exponential_components(raw):
 old=original_components(raw)
 if old is not None:return old
 text=B.clean(raw);depth=0
 for i,c in enumerate(text):
  if c in '+-'and i>0 and depth==0 and text[i-1]not in '+-*/^':return B.scalar(text[:i]),(1 if c=='+'else -1)*B.scalar(text[i+1:])
  depth+=(c in '({')-(c in ')}')
 return None
T.endpoint_contributions=exponential_components
source=json.load(open(D/'source.json'));manifest=json.load(open(R/'manifest.json'));assert source==json.load(open(R/manifest['source_snapshot_roots'][str(source['basis'])]/f'sources/{K}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']if ':question/math-academy-id'in q};fidelity=dict(banks=0,values=0,keys=0,solutions=0,incomplete=0)
for c in G.CASES:
 o=olds[c['template']];q=G.generate(c['level'],template=c['template'],parameters={'shift':0},profile='observed_raw')['question'];assert q[':question/problem']==o[':question/problem'];f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value']for a in f[':answer-field/choices'])==sorted(a[':answer/value']for a in of[':answer-field/choices']);fidelity['banks']+=1;fidelity['values']+=len(f[':answer-field/choices'])
 if ':answer-field/correct'in of:assert next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];fidelity['keys']+=1
 else:assert ':answer-field/correct'not in f
 if ':question/worked-solution'in o:assert q[':question/worked-solution']==o[':question/worked-solution'];fidelity['solutions']+=1
 else:assert ':question/worked-solution'not in q;fidelity['incomplete']+=1
N={};seen={l:set()for l in G.SUPPORTED_LEVELS};counter=0

def check(r,authored=False):
 global counter
 q=copy.deepcopy(r['question']);m=r['generation'];assert not m['evidence_only']and m['eligible_for_learning']
 for key in(':question/problem',':question/worked-solution'):q[key]=A.mathnorm(q[key]).replace(r'\quad\Longrightarrow\quad','⟹')
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']:a[':answer/value']=A.mathnorm(a[':answer/value'])
 F,lo,hi=T.given(q)
 if lo is None:F,U,n=H.indefinite(q)
 else:
  F,expected,n=T.check(q,False,True,False,False);n=dict(n,records=1);f=q[':question/answer-fields'][0];vals=[P.scalar(a[':answer/value'])for a in f[':answer-field/choices']];assert[a[':answer/id']for a,v in zip(f[':answer-field/choices'],vals)if H.eq(v,expected)]==[f[':answer-field/correct'][1]];n['values']=len(vals);n['pairs']=0
  for i,v in enumerate(vals):
   for w in vals[:i]:assert not H.eq(v,w);n['pairs']+=1
 for k,v in n.items():N[k]=N.get(k,0)+v
 if authored:seen[q[':question/difficulty'].split('/')[-1]].add((H.task(F),str(lo),str(hi)))
 counter+=1
 if counter%100==0:print('Root natural-base affine actual stages read',counter,flush=True)
for c in G.CASES:
 for shift in range(-4,5):check(G.generate(c['level'],template=c['template'],parameters={'shift':shift}))
for level in G.SUPPORTED_LEVELS:
 for a,kn,kd,b in itertools.product([z for z in range(-6,7)if z],[-4,-3,-2,-1,1,2,3,4],range(1,5),range(-3,4)):
  pairs=[None]if level=='easy'else[(L,H)for L in range(-2,2)for H in range(L+1,3)]
  for pair in pairs:
   p=dict(a=a,kn=kn,kd=kd,b=b)
   if pair:p.update(L=pair[0],H=pair[1])
   try:G.authored_bounds(level,p)
   except ValueError:continue
   if level=='easy'and abs(s.Rational(kn,kd))==1:continue
   check(G.generate(level,template='affine',parameters=p),True)
 for seed in range(18):check(G.generate(level,seed))
 expected={'easy':1008,'moderate':2640,'hard':1280}[level];assert len(seen[level])==expected,(level,len(seen[level]),expected)
result=dict(status='passed',source=fidelity,readback=N,capacity={l:len(v)for l,v in seen.items()},task_identity='Actual printed exponential logarithmic derivative and leading coefficient and actual supplied bounds, all authored finite parameter records independently parsed.',source_errors='Raw q13775/q30922 x-operand du and q51160 e^(2z) du errors preserved evidence-only; normal dx and explicit e^(2(u/2)) repairs checked on all nine coordinate shifts.',native_limitations='Representative native66accepted200rejected96expectedradio nonidentity errors;13/13 normal uncollected endpoint equivalents accepted,8 raw round/form equivalent restrictions separated. Full bounded rendered math reviewed; native coverage representative.',approval_scope='Local docs3–7; normal exact answer wording; hard authored same method fixed seven stages; no engine changes.',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
