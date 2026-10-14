"""Root reads actual printed matrix shapes, membership banks and counted prose."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186087696;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
G=mod('root_square_generator',D.with_suffix('.py'));F=mod('root_square_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
C=dict(records=0,actual_shapes=0,fields=0,values=0,subset_pairs=0,solution_count_explanations=0,conclusions=0,level_checks=0)
def shapes(prompt):
 rows=[]
 for label,body in re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S):
  rr=body.split(chr(92)*2);cc=[len(r.split('&')) for r in rr];assert len(set(cc))==1;rows.append((label,len(rr),cc[0]))
 assert len(rows)==3 and len(set(l for l,r,c in rows))==3;return rows

def check(r,raw=False):
 q,m=r['question'],r['generation'];rows=shapes(q[':question/problem']);chosen={l for l,a,b in rows if a==b};C['actual_shapes']+=3
 fields=q[':question/answer-fields'];kind=fields[0][':answer-field/type'].split('/')[-1]
 if kind=='checkbox':
  assert len(fields)==3
  for f in fields:
   assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'};expected='true' if f[':answer-field/key'] in chosen else 'false';assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==expected;C['fields']+=1;C['values']+=2
 else:
  assert len(fields)==1;f=fields[0];vals=[set(re.findall(r'\$([A-Z])\$',a[':answer/value'])) for a in f[':answer-field/choices']];assert len(vals)==5 and sum(v==chosen for v in vals)==1
  for a,b in itertools.combinations(vals,2):assert a!=b;C['subset_pairs']+=1
  if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if v==chosen]==[f[':answer-field/correct'][1]]
  C['fields']+=1;C['values']+=5
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];bullets=re.findall(r'^- (.*?)$',sol,re.M);assert len(bullets)==3
  for b,(l,a,c) in zip(bullets,rows):
   assert b.startswith('$'+l+'$') and ('*not*' in b)==(a!=c)
   assert re.search(r'has \$(\d+)\$ rows? and \$(\d+)\$ columns?',b).groups()==(str(a),str(c))
   assert f'${a}\\times {c}$ matrix.' in b;C['solution_count_explanations']+=1
  final=sol.split('Therefore,')[-1];assert set(re.findall(r'\$([A-Z])\$',final))==chosen and ('none' in final)==(not chosen);C['conclusions']+=1
 if not raw and m['profile']=='boolean-membership':
  dims=[(a,b) for l,a,b in rows];level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert all(max(d)<=3 for d in dims) and any(a==1 for a,b in dims)
  elif level=='moderate':assert all(2<=min(d) and max(d)<=6 for d in dims) and len(chosen)==1 and any(a!=b and (b,a) in dims for a,b in dims)
  else:assert len({a for a,b in dims})==1 and 2<=dims[0][0]<=7 and len({b for a,b in dims})==3 and sorted(b for a,b in dims)[1]==dims[0][0] and max(b for a,b in dims)<=8
  C['level_checks']+=1
 C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for l in ('easy','moderate','hard'):
 for seed in (38,56,113):check(G.generate(l,seed))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']),True)
# Independently enumerate unordered shape capacities, ignoring all numerical entries.
caps={}
for l,bound in [('easy',3),('moderate',6),('hard',8)]:
 eligible=[]
 for dims in itertools.combinations_with_replacement(itertools.product(range(1,bound+1),repeat=2),3):
  if l=='easy':ok=any(a==1 for a,b in dims)
  elif l=='moderate':ok=all(min(d)>=2 for d in dims) and sum(a==b for a,b in dims)==1 and any(a!=b and (b,a) in dims for a,b in dims)
  else:ok=len({a for a,b in dims})==1 and 2<=dims[0][0]<=7 and len({b for a,b in dims})==3 and sorted(b for a,b in dims)[1]==dims[0][0]
  if ok:eligible.append(dims)
 caps[l]=len(eligible)
assert caps=={'easy':109,'moderate':50,'hard':56}
result={'status':'passed','source':fidelity,'readback':C,'independent_shape_capacities':caps,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
