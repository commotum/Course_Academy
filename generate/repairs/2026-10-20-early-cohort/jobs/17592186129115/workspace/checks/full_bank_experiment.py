import itertools,json,random,time
from pathlib import Path
W=Path(__file__).resolve().parents[1]
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
refs=[m for m in range(65536) if ref(m)];print('REF',len(refs),flush=True)
ops={n:[sum(1<<c for c in cells) for cells in itertools.combinations(range(16),n)] for n in (2,3)}
# correct must erase n nonzero entries; match all options zero count=0
valid={o:{m|o for m in refs if not m&o and not ref(m|o)} for oo in ops.values() for o in oo}
rg=random.Random(888);report={};banks=[]
for n,oo in ops.items():
 oo=[o for o in oo if valid[o]];success=0;coverage=set();examples=[]
 for _ in range(20000):
  b=rg.sample(oo,5);u=0
  for o in b:u|=o
  ws=[]
  for i,o in enumerate(b):
   v=[m for m in valid[o] if m&u==u and all(not ref(m&~p) for j,p in enumerate(b) if i!=j)]
   if not v:break
   ws.append(v)
  if len(ws)==5:
   success+=1;coverage.update(m for ww in ws for m in ww)
   if len(examples)<3:examples.append({'bank':b,'support_counts':[len(v) for v in ws]})
   banks.append({'bank':b,'witnesses':ws})
 report[n]={'eligible_operations':len(oo),'successes':success,'trials':20000,'masks_covered':len(coverage),'examples':examples}
print(json.dumps(report));(W/'evidence/repair2/full-bank-experiment.json').write_text(json.dumps(report,indent=2));(W/'evidence/repair2/full-bank-examples.json').write_text(json.dumps(banks))
