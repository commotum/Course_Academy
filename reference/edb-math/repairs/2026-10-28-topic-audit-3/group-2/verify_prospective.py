import copy,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;Q=json.loads((H/'proposed-questions.json').read_text());A=json.loads((H/'proposed-activities.json').read_text());grades=[];render=[];skips=[]
for q0 in Q:
 q=copy.deepcopy(q0);checks=[]
 for attr in[':question/problem',':question/worked-solution']:
  if attr in q:render.append({'entity':q[':db/id'],'attribute':attr[1:],'value':q[attr]})
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  f[':answer-field/type']=f[':answer-field/type'][':db/ident'];right=f.get(':answer-field/correct')
  if right:f[':answer-field/correct']=[':answer/id',right[':answer/id']]
  else:skips.append({'question':q[':db/id'],'field':f[':db/id'],'reason':'no canonical'});continue
  if f[':answer-field/type']==':answer-field.type/checkbox':render.append({'entity':f[':db/id'],'attribute':'answer-field/key','value':f[':answer-field/key']})
  for a in f.get(':answer-field/choices',[]):
   at=a[':answer/type'][':db/ident'];a[':answer/type']=at
   if at!=':answer.type/image'and a[':db/id']!=17592186675717:render.append({'entity':a[':db/id'],'attribute':'answer/value','value':a[':answer/value'],'bare_math':at==':answer.type/math'})
   if ':answer/feedback'in a:render.append({'entity':a[':db/id'],'attribute':'answer/feedback','value':a[':answer/feedback']})
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':right[':answer/value'],'expected':'accepted','purpose':'Prospective canonical math accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Wrong scalar rejected'}])
  elif f[':answer-field/type']!=':answer-field.type/free':checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==right[':answer/id']else'rejected','purpose':'Complete bank against prospective canonical'}for a in f.get(':answer-field/choices',[]))
 if checks:grades.append({'label':str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Audit3 group2 prospective'},'generation':{'template':'existing-entity-audit'}},'checks':checks})
for a in A:
 for c in a['contents']:
  if ':tutorial/content'in c:render.append({'entity':c[':db/id'],'attribute':'tutorial/content','value':c[':tutorial/content']})
(H/'prospective-grading-input.json').write_text(json.dumps(grades,indent=2)+'\n');(H/'prospective-render-input.json').write_text(json.dumps(render,indent=2)+'\n');(H/'prospective-contracts.json').write_text(json.dumps({'questions':len(Q),'gradeable_questions':len(grades),'render_fields':len(render),'missing_keys':skips,'preserved_historical_noncanonical_render_exclusions':[17592186675717],'reference_evidence':'reference-history/report.json'},indent=2)+'\n');print(len(grades),len(render),'missing keys',len(skips));subprocess.run([str(H.parent/'check-engine'),str(H/'prospective-grading-input.json'),str(H/'prospective-grading.json')],check=True)
