"""Exhaust individual endpoint components in final displayed records."""
import importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
counts={'normal':0,'raw':0}
def check(r):
 q=r['question'];f,lo,hi=v.p.integral(q[':question/problem'])
 if lo is None:return False
 F=v.canonical_primitive(f,v.x);rr=v.rows(q[':question/worked-solution']);t=r['generation']['template'];idx=5 if t in ('q-13533','q-13537') else 4
 for i in [idx]+([] if t=='q-13533' else [idx+1]):
  a,b=v.endpoint_components(rr[i]);assert v.eq(a,F.subs(v.x,hi)) and v.eq(b,F.subs(v.x,lo)),(t,i,rr[i])
 return True
for r in json.loads((H/'full-domain-records.json').read_text()):counts['normal']+=check(r)
for t in g.SOURCES:
 for p in g.domain(t,True):counts['raw']+=check(g.generate(g.LEVELS[t],template=t,parameters=p,profile='observed_raw'))
v.save('endpoint-validation.json',dict(status='passed',complete_bounded_endpoint_instances=counts,correlated_error_mutation='Separately verified: equal +1 errors at both endpoints preserve the total but are rejected.'))
print(counts)
