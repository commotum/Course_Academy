import collections, itertools,json,random,sys
from pathlib import Path
sys.dont_write_bytecode=True
from regressions import W,ref_after
def ref(bits):
 p=-1;zero=False
 for i in range(4):
  r=(bits>>(4*i))&15
  if not r:zero=True
  else:
   j=(r&-r).bit_length()-1
   if zero or j<=p:return False
   p=j
 return True
refs=[m for m in range(65536) if ref(m)]
ops={n:[tuple(b) for b in itertools.combinations(range(16),n)] for n in (2,3)}
valid={}
for oo in ops.values():
 for o in oo:
  ob=sum(1<<c for c in o)
  ss=[sum(1<<c for c in sub) for n in range(1,len(o)+1) for sub in itertools.combinations(o,n)]
  valid[o]={r|sub for r in refs if not r&ob for sub in ss if not ref(r|sub)}
masks=sorted(set.union(*valid.values()))
rng=random.Random(5588);rows=[];attempts=0
for _ in range(16):
 n=rng.choice((2,3));z=rng.choice((False,True));pool=[o for o in ops[n] if any((m>>12==0)==z for m in valid[o])]
 print('group',n,z,flush=True)
 while True:
  attempts+=1;common=rng.randrange(16);local=[o for o in pool if common in o];b=rng.sample(local,5);supports=[]
  for i,o in enumerate(b):
   ss=valid[o].difference(*(valid[p] for p in b if p!=o));ss=[m for m in ss if (m>>12==0)==z]
   # A correct operation must never be the sole option with fewest no-ops.
   ss=[m for m in ss if sum(bool(m&1<<c) for c in o)>=2]
   ss=[m for m in ss if sum(sum(not m & 1<<c for c in p)<=sum(not m & 1<<c for c in o) for p in b)>=2]
   if not ss:break
   supports.append(sorted(ss))
  if len(supports)==5:break
  if attempts>5000:raise Exception('too many attempts')
 ci=rng.randrange(5);m=rng.choice(supports[ci]);zero=[sum(not m&1<<c for c in p) for p in b]
 rows.append({'size':n,'zero_row':z,'rank':sorted(b).index(b[ci]),'noops':zero,'key':ci,'fewest_noops':zero.index(min(zero))==ci})
print(json.dumps({'attempts':attempts,'ranks':dict(collections.Counter(r['rank'] for r in rows)),'fewest_noop_hits':sum(r['fewest_noops'] for r in rows),'n':len(rows),'noop_vectors':dict(collections.Counter(str(sorted(r['noops'])) for r in rows))}));(W/'evidence/repair2/sampler-experiment.json').write_text(json.dumps(rows,indent=2))
