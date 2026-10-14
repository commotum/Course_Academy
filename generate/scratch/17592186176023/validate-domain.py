import importlib.util,json
import sympy as s
from pathlib import Path
spec=importlib.util.spec_from_file_location('g','generate/scratch/17592186176023.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,r,th=g.X,g.Y,g.R,g.T
# Enumerate the complete bounded mathematical domain, excluding nuisances,
# equivalent cubic coefficient masks and bank/presentation aliases.
finite={}
for level in ['easy','moderate','hard']:
 seen=set();instances=0
 for name,f in g.FAMILIES.items():
  if f['level']!=level:continue
  ss=[1,4,9,16,25]if level=='easy'else [1,2,4,9,16,25]if level=='moderate'else[4,9,16,25]
  angular=[(0,'1/6'),(0,'1/3'),(0,'2/3')]if name=='q-126747'else[(0,'1/2'),('1/2',1),(0,1)]if name=='q-126756'else[(g.anchor(name)['lo'],g.anchor(name)['hi'])]
  for cc in range(1,5 if level=='easy'else 7):
   for ss0 in ss:
    aa=range(1,int(s.sqrt(ss0)))if name=='q-126758'else[0]
    for aa0 in aa:
     for ll,hh in angular:
      p=g.exact(dict(c=cc,s=ss0,inner=aa0,lo=ll,hi=hh))
      try:g.check_scope(level,name,p);g.bank(f,p,g.answer_value(f,p))
      except ValueError:continue
      P,Q,_,_=g.components(name,p);key=(s.srepr(s.expand(P-P.subs(y,0))),s.srepr(s.expand(Q-Q.subs(x,0))),*(str(p[k])for k in ['s','inner','lo','hi']))
      seen.add(key);instances+=1
 finite[level]={'distinct_assessed_tasks':len(seen),'eligible_template_instances':instances}
assert {l:v['distinct_assessed_tasks']for l,v in finite.items()}=={'easy':20,'moderate':108,'hard':204}

(g.BASE/'finite-domain.json').write_text(json.dumps(finite,indent=2)+'\n');print(finite)
