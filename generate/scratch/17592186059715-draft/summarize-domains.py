import hashlib,importlib.util,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
levels={}
for level in g.DOMAINS:
 families=list(g.FAMILIES) if level=='moderate' else (['graph_read'] if level=='hard' else [f for f in g.FAMILIES if f!='graph_read'])
 out={}
 for family in families:
  lo,hi=(0,6) if level=='easy' else (1,4) if level=='moderate' and family=='graph_read' else (-g.DOMAINS[level]['coordinate_bound'],g.DOMAINS[level]['coordinate_bound'])
  keys=set();displacements=set();norms=set();instances=0
  for x,y,u,v in itertools.product(range(lo,hi+1),repeat=4):
   ps=[[x,y],[u,v]]
   try:g.check_domain(level,family,ps)
   except ValueError:continue
   dx,dy=u-x,v-y;n=dx*dx+dy*dy;l1=abs(dx)+abs(dy)
   # Independent complete squared scalar values: square-root values and
   # positive integer values are injective under squaring on nonnegative domain.
   squares=[n,(u+x)**2+(v+y)**2,l1*l1,n*n,l1]
   if len(set(squares))!=5:continue
   sign=lambda z:1 if z>0 else -1 if z<0 else 0
   keys.add((dx,dy,sign(u),sign(x),sign(v),sign(y),family=='graph_read',g.DOMAINS[level]['grid_increment']))
   displacements.add((dx,dy));norms.add(n);instances+=1
  out[family]={'eligible_presentations':instances,'meaningful_tasks_excluding_translations_labels_banks_shuffle':len(keys),'directed_displacements':len(displacements),'distinct_squared_norms':len(norms)}
 levels[level]=out
(HERE/'domain-enumeration.json').write_text(json.dumps({'criterion':'directed displacement plus zero/positive/negative subtraction operand categories and actual graph scale-reading demand; common translations preserving those data excluded','levels':levels},indent=2)+'\n')
print(json.dumps(levels,indent=2))
