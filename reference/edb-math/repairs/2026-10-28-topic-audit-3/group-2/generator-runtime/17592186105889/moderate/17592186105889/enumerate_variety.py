"""Exhaustive canonical task count, excluding incidental rectangles and aliases."""
import importlib.util,itertools,json,hashlib,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
by_template={};unions={level:set() for level in ['easy','moderate','hard']}
for t,l in g.TEMPLATES.items():
 domain=[-2,-1,1,2,'sqrt(2)','-sqrt(2)'] if l=='easy' else [-2,-1,1,2]
 keys=['a','b','k'] if l=='easy' else ['a','b','c','k']+(['l'] if l=='hard' else [])
 hashes=set();count=0
 for values in itertools.product(domain,repeat=len(keys)):
  p=dict(zip(keys,map(str,values)));p['bounds']=[0,1,0,1]
  f,gr,dx,dy,m,pref,ans=g.model(t,p)
  obj={'response':'integrand setup','substituted_scalar':g.s.srepr(g.s.expand(pref)),'squared_metric':g.s.srepr(g.s.expand(1+dx**2+dy**2))}
  hashes.add(hashlib.sha256(json.dumps(obj,sort_keys=True).encode()).hexdigest());count+=1
 unions[l].update(hashes);by_template[t]={'level':l,'coefficient_tuples':count,'canonical_assessed_tasks':len(hashes),'domain':domain}
report={'by_template':by_template,'unique_tasks_by_level':{l:len(h) for l,h in unions.items()},'incidental_bounds_counted':False,'seed_bank_order_letter_aliases_counted':False,'method':'exhaustive nonzero coefficient catalog; canonical substituted scalar and squared metric; duplicate sign symmetries removed'}
(HERE/'variety.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['unique_tasks_by_level'])
