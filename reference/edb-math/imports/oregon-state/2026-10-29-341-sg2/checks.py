from pathlib import Path
import json,sys
R=Path('/home/jake/Developer/Course_Academy');H=R/'reference/edb-math/imports/oregon-state/2026-10-29-341-sg2';T=Path('/tmp/ingest-341-me2')
entities=json.loads((H/'entities.json').read_text());byid={r[':db/id']:r for r in entities};cases=[];render=[]
for e in entities:
 for attr in [':question/problem',':question/worked-solution',':answer/value',':answer/feedback',':tutorial/content',':multistep/context']:
  if attr in e:render.append({'id':e[':db/id'],'attribute':attr,'text':('$'+e[attr]+'$')if attr==':answer/value'and e.get(':answer/type')==':answer.type/math'else e[attr]})
 if ':question/id'not in e:continue
 fs=[];check=[]
 for i,fid in enumerate(e[':question/answer-fields']):
  f=byid[fid];choices=[]
  for aid in f[':answer-field/choices']:
   a=byid[aid];choices.append({':answer/id':a[':answer/id']['$uuid'],':answer/type':a[':answer/type'],':answer/value':a[':answer/value']})
  fs.append({':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',byid[f[':answer-field/correct']][':answer/id']['$uuid']]})
  if f[':answer-field/type'].endswith('/free'):continue
  correct=choices[0][':answer/value']
  wrong='9'
  check.extend([{'field_index':i,'submitted':correct,'expected':'accepted','purpose':'canonical exact math answer'}, {'field_index':i,'submitted':wrong,'expected':'rejected','purpose':'wrong determinant sign'}])
 if check:cases.append({'label':e[':db/id'],'record':{'question':{':question/problem':e[':question/problem'],':question/answer-fields':fs},'knowledge_point':{'title':'MTH 341 Mini Exam 2 Review'},'generation':{'template':'imported-assignment'}},'checks':check})
(T/'grading-input.json').write_text(json.dumps(cases));(T/'render-cases.json').write_text(json.dumps(render));print('Prepared',sum(len(c['checks'])//2 for c in cases),'math fields and',len(render),'render fields.')
