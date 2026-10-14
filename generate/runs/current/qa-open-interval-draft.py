"""Root compares every displayed bank as real sets and operative solution endpoints."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059826;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
P=mod('root_open_sets',R/'interval-readback.py');G=mod('root_open_generator',D.with_suffix('.py'));F=mod('root_open_fidelity',R/'root-source-fidelity.py')
originals,fidelity=F.check(G,K,D)
C=dict(records=0,displayed_banks=0,values=0,pair_checks=0,solution_relations=0,inline_endpoints=0,prose_masks=0,scope_checks=0)
def mask(t):
 t=re.sub(r'\$\$.*?\$\$','@DISPLAY@',t,flags=re.S);return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',t)).strip()
def check(r,raw=False):
 q,m=r['question'],r['generation'];target=P.task(q[':question/problem']);a,b=target.start,target.end;assert target.left_open and target.right_open
 f=q[':question/answer-fields'][0];vals=[P.meaning(x[':answer/value']) for x in f[':answer-field/choices']];assert len(vals)==5
 assert sum(v==target for v in vals)==1
 for v,w in itertools.combinations(vals,2):assert v!=w;C['pair_checks']+=1
 profile=m['bank_profile'].removeprefix('raw_');expected=[target,s.Interval(a,b),s.Interval(a,b,left_open=True),s.Interval(a,b,right_open=True)]
 expected.append(s.Interval.open(-b,-a) if profile=='compact_reflection' else s.Union(s.Interval.open(-s.oo,a),s.Interval.open(b,s.oo)) if profile=='membership' else s.Interval.open(-s.oo,b))
 assert all(v in vals for v in expected)
 if ':answer-field/correct' in f:assert [x[':answer/id'] for x,v in zip(f[':answer-field/choices'],vals) if v==target]==[f[':answer-field/correct'][1]]
 if not raw:
  level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert all(v.is_Integer and -12<=v<=12 for v in (a,b)) or a==-b and b**2 in (2,3,5,6,7,10,11,13)
  elif level=='moderate':assert sum(bool(v.is_Integer) for v in (a,b))==1 and all(-6<=v<=6 and v.is_Rational and v.q<=4 for v in (a,b))
  else:assert all(v.is_Rational and not v.is_Integer and -6<=v<=6 and 2<=v.q<=4 for v in (a,b)) and a.q!=b.q
  C['scope_checks']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==(2 if profile=='membership' else 3)
  for block in blocks:assert P.meaning(block)==target;C['solution_relations']+=1
  assert '*not* included' in sol or 'are *not* included' in sol
  if profile!='membership':
   matches=re.findall(r'endpoints \$(.*?)\$ and \$(.*?)\$',sol);assert len(matches)==1 and P.endpoint(matches[0][0])==a and P.endpoint(matches[0][1])==b;C['inline_endpoints']+=2
  old=originals[m['source_ids'][0]]
  if ':question/worked-solution' in old:assert mask(sol)==mask(old[':question/worked-solution']);C['prose_masks']+=1
 C['records']+=1;C['displayed_banks']+=1;C['values']+=5
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for profile in G.BANKS:
  for seed in (32,61,100):check(G.generate(level,seed,profile=profile))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate('easy',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']),True)
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
