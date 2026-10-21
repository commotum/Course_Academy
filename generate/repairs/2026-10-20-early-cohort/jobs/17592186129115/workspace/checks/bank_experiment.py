import collections,itertools,json,random,time
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
masks=sorted({m for r in json.loads((W/'catalogue.json').read_text()) for m in r['masks']})
ops={n:[sum(1<<c for c in cells) for cells in itertools.combinations(range(16),n)] for n in (1,2,3)}
valid={o:sum(1<<i for i,m in enumerate(masks) if ref(m&~o)) for oo in ops.values() for o in oo}
rg=random.Random(888);report={};banks=[]
for n,oo in ops.items():
 oo=[o for o in oo if valid[o]];print('eligible',n,len(oo),flush=True);success=0;coverage=set();examples=[]
 for _ in range(10000 if len(oo)>=5 else 0):
  b=rg.sample(oo,5);w=[]
  for i,o in enumerate(b):
   v=valid[o]
   for j,p in enumerate(b):
    if j!=i:v &= ~valid[p]
   # all options have equal number of already-zero coordinates
   # No matching constraint in this experiment
   if not v:break
   w.append(v)
  if len(w)==5:
   success+=1
   for v in w:coverage.update(masks[k] for k in range(len(masks)) if v>>k&1)
   if len(examples)<3:examples.append({'bank':b,'support_counts':[v.bit_count() for v in w]})
   banks.append({'bank':b,'witnesses':[[masks[k] for k in range(len(masks)) if v>>k&1] for v in w]})
 report[n]={'eligible_operations':len(oo),'successes':success,'trials':10000,'masks_covered':len(coverage),'examples':examples}
print(json.dumps(report));(W/'evidence/repair2/bank-experiment.json').write_text(json.dumps(report,indent=2));(W/'evidence/repair2/bank-examples.json').write_text(json.dumps(banks))
