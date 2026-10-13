import importlib.util,json
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
out={}
for n,(level,sid) in g.FAMILIES.items():
 if n=='unrated':continue
 tasks=set();valid=0;reject=0
 for a in range(1,4):
  for h in range(1,5):
   if n=='negative_cone' and h==1:continue
   p={'k':1,'a':a,'h':h};m=g.model(n,p)
   try:g.bank(n,m,p)
   except ValueError:reject+=4;continue
   for k in range(1,5):
    mm=g.model(n,dict(p,k=k));graph=mm['g'] if any(c.has(g.Z) for c in mm['c']) else s.simplify(mm['g']-mm['g'].subs({g.X:0,g.Y:0}))
    tasks.add(g.digest([level,g.tex(graph),[g.tex(c) for c in mm['c']],str(mm['dom']),str(mm['disk'])]));valid+=1
 out[n]={'level':level,'eligible_parameter_tuples':valid,'whole_bank_rejections':reject,'distinct_mathematical_tasks':len(tasks)}
(H/'variety.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
