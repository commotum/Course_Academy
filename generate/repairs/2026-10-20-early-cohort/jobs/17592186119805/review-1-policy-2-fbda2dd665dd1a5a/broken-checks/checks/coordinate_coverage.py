"""Resolve missing delivered homogeneous coordinate roles with minimal new witnesses."""
from common import *
g=load_generator();pool=json.loads((E/'delivery-moderate/accepted.json').read_text());selected=[];report=[]
def roles(r):
 ans,res,(_,u,_,_,_)=solve(r['question']);pivot=next(i for i,x in enumerate(u) if x);t=res[pivot]/u[pivot]
 return pivot,{i for i,(x,y) in enumerate(zip(res,u)) if x!=t*y}
for sid in g.LEVELS['moderate']:
 n=len(g.CASES[sid]['a']);pivots=set();contradictions=set()
 for r in pool:
  if r['generation']['bank_profile']==sid:
   p,c=roles(r);pivots.add(p);contradictions.update(c)
 initial={'pivots':sorted(pivots),'contradictions':sorted(contradictions)};attempts=0
 for seed in range(100):
  if pivots==set(range(n)) and contradictions==set(range(n)):break
  r=g.generate('moderate',seed,sid);verify(r);attempts+=1;p,c=roles(r)
  if p not in pivots or c-contradictions:
   selected.append(r);pivots.add(p);contradictions.update(c)
 assert pivots==set(range(n)) and contradictions==set(range(n)),sid
 report.append({'profile':sid,'initial_delivered':initial,'additional_normal_seeds_checked':attempts,'pivots':sorted(pivots),'contradictions':sorted(contradictions)})
save('coordinate-records.json',selected);save('coordinate-coverage.json',{'passed':True,'profiles':report,'additional_records':len(selected),'purpose':'Fill concrete coordinate gaps in the small initial sample, not enlarge unrelated tests.'})
print(json.dumps({'passed':True,'additional_records':len(selected),'profiles':report}))
