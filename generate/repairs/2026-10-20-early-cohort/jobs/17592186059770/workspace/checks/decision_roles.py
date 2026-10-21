#!/usr/bin/env python3
"""Fixed-bank counterfactuals; independent target sets read from source banks."""
import json,itertools,subprocess
import validate as v
from pathlib import Path
g=v.g
source=json.loads((v.W/'../source/source.json').read_text())
qs={q.get(':question/math-academy-id'):q for q in source['material']['kp'][':knowledge-point/questions']}
records=[];reports=[]
for profile,(nums,_) in g.EASY_SOURCES.items():
 p=dict(zip('abcdef',nums))
 base=g.generate('easy',parameters=p,profile=profile)
 # Source choices, not generator's claimed target metadata, define independent expected targets.
 sourcevalues={v.matrix(a[':answer/value']) for a in qs[profile][':question/answer-fields'][0][':answer-field/choices']}
 eligible={m for m in sourcevalues if len(m)==2 and len(m[0])==3}
 recipe_names=[x['recipe'] for x in base['generation']['recipes']]
 actual=set()
 for recipe in recipe_names:
  try:r=g.generate('easy',parameters=p,profile=profile,target_recipe=recipe)
  except ValueError:continue
  assert {v.matrix(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']}==sourcevalues
  actual.add(v.witness(r));records.append(r)
 assert actual==eligible,(profile,actual,eligible)
 # Each orientation changes the error-bearing slot assignments, preserving target skill.
 for orientation in ('identity','row_swap','column_swap','both'):
  r=g.generate('easy',parameters=p,profile=profile,bank_orientation=orientation);v.witness(r);records.append(r)
 reports.append({'profile':profile,'fixed_bank_targets':len(actual),'eligible_source_bank_targets':len(eligible),'orientations_tested':4})
for template,profile in g.TEMPLATES.items():
 p=g.SOURCE_PARAMETERS[template];base=g.generate('moderate',template=template,parameters=p)
 bank={v.matrix(a[':answer/value']) for a in base['question'][':question/answer-fields'][0][':answer-field/choices']}
 eligible={m for m in bank if len(m[0])==3} if template=='coefficient' else {m for m in bank if len(m[0])==4 and m[0]==(1,-4,-1,0) and m[1][:3]==(-11,0,3)}
 actual=set()
 for item in base['generation']['recipes']:
  try:r=g.generate('moderate',template=template,parameters=p,target_recipe=item['recipe'])
  except ValueError:continue
  assert {v.matrix(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']}==bank
  actual.add(v.witness(r));records.append(r)
 assert actual==eligible,(profile,actual,eligible)
 for columns in itertools.permutations(range(3)):
  for rows in ([0,1],[1,0]):
   r=g.generate('moderate',template=template,parameters=p,role_assignment={'columns':list(columns),'rows':rows});v.witness(r);records.append(r)
 reports.append({'profile':profile,'fixed_bank_targets':len(actual),'eligible_source_template_targets':len(eligible),'variable_column_assignments':6,'equation_orders':2})
# Additional fixed banks outside inventory: delivery must retain every target role.
for profile in g.EASY_SOURCES:
 p=dict(zip('abcdef',[2,-3,5,-7,4,-6]));base=g.generate('easy',parameters=p,profile=profile)
 for item in base['generation']['recipes']:
  try:r=g.generate('easy',parameters=p,profile=profile,target_recipe=item['recipe'])
  except ValueError:continue
  v.witness(r);records.append(r)
for template in g.TEMPLATES:
 p=dict(zip('abcde',[6,-3,-5,7,-4])) if template=='coefficient' else dict(zip(['k','l','m','r'],[-6,5,-7,4]))
 base=g.generate('moderate',template=template,parameters=p)
 for item in base['generation']['recipes']:
  try:r=g.generate('moderate',template=template,parameters=p,target_recipe=item['recipe'])
  except ValueError:continue
  v.witness(r);records.append(r)
v.save('role-records-easy.json',[r for r in records if r['question'][':question/difficulty'].endswith('/easy')])
v.save('role-records-moderate.json',[r for r in records if r['question'][':question/difficulty'].endswith('/moderate')])
cases=[]
for r in records:
 target=v.witness(r)
 cases.append({'label':'controlled-answer-role','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if v.matrix(a[':answer/value'])==target else 'rejected','purpose':'fixed-bank target changes with visible prompt'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
v.save('role-native-input.json',cases);v.save('role-records.json',records)
result=subprocess.run([str(v.REPO/'generate/runs/current/check-engine'),str(v.E/'role-native-input.json'),str(v.E/'role-native-report.json')],capture_output=True,text=True)
assert result.returncode==0,result.stdout+result.stderr
v.save('decision-roles.json',{'status':'passed','records':len(records),'native_checks':5*len(records),'profiles':reports,'bank_only_predictors':'A fixed complete bank has multiple correct targets depending on the visible system, defeating all deterministic bank-only choices. Shape elimination is valid mathematical evidence; it does not determine one choice.'})
print('decision roles passed:',len(records),'visible-record checks and',5*len(records),'native checks')
