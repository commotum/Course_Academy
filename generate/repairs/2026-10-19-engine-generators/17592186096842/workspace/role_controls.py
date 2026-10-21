"""Within-layout controls: hold mathematical evidence fixed and vary bank role."""
import json,collections
from pathlib import Path
import sympy as sp
import generator as g
from validate import independent,key,field,grading,save
from validation_math import displayed,equal
rs=json.load(open('evidence/probe-records.json'));controls=[];cases=[];report=[]
for name,spec in g.TEMPLATES.items():
 if spec['field']!='radio':continue
 base=next(r for r in rs if r['generation']['template']==name)
 params=base['generation']['parameters'];group=[];ranks=[]
 for role in range(5):
  r=g.generate(spec['level'],seed=role+500,template=name,parameters=params,profile='scale_bank',bank_role=role)
  expected=independent(r);group.append(r);cases.append(grading(r,expected,'controlled bank role '+name+' '+str(role)))
  vals=[displayed(a[':answer/value']) for a in field(r)[':answer-field/choices']]
  if any(v.has(g.X) for v in vals):
   # Independent parser symbol x has identical assumptions to generator X.
   point=next(p for p in list(range(-25,26))+[sp.Rational(k,16) for k in range(-15,16) if k] if all(v.subs(g.X,p).is_real and v.subs(g.X,p).is_finite for v in vals))
   vals=[v.subs(g.X,point) for v in vals]
  index=field(r)[':answer-field/choices'].index(key(r))
  ranks.append(sorted(range(5),key=lambda i:float(vals[i])).index(index))
 assert len(set(ranks))==5,(name,ranks)
 assert all(equal(displayed(key(r)[':answer/value']),displayed(key(group[0])[':answer/value'])) for r in group)
 report.append({'template':name,'fixed_parameters':params,'roles':[0,1,2,3,4],'observed_numeric_ranks':ranks,'mathematical_answer_preserved':True,'semantic_instances':1})
 controls+=group
save('role-control-records.json',controls);save('role-control-grader-input.json',cases);save('role-controls.json',report)
print('Passed',len(report),'fixed-data layout controls;',len(controls),'records; all five ranks per layout')
