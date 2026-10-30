import json,copy
from pathlib import Path
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());changes=json.loads((H/'proposals.json').read_text())if(H/'proposals.json').exists()else[];changes={(p['entity'],':'+p['attribute']):p['after']for p in changes}
def patch(o):
 if isinstance(o,list):return[patch(v)for v in o]
 if not isinstance(o,dict):return o
 o={k:patch(v)for k,v in o.items()}
 for(e,a),v in changes.items():
  if o.get(':db/id')==e:o[a]={':db/id':v}if a==':answer-field/correct'else v
 return o
S=patch(S)
for q in S['questions']:
 if q[':db/id']==17592186120218:q[':question/answer-fields']=[f for f in q[':question/answer-fields']if f[':db/id']!=17592186117469]
render=[];native=[];controls=[]
for q in S['questions']:
 fields=[]
 for f in q.get(':question/answer-fields',[]):
  ch=[{'id':a[':db/id'],'value':a[':answer/value'],'type':a[':answer/type'][':db/ident'].split('/')[-1]}for a in f[':answer-field/choices']];right=f.get(':answer-field/correct',{}).get(':db/id');fields.append({'id':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':ch,'correctAnswer':next((a for a in ch if a['id']==right),None)})
 for a in[':question/problem',':question/worked-solution']:
  if q.get(a):render.append({'entity':q[':db/id'],'attribute':a[1:],'value':q[a],'fields':fields})
 controls.append({'entity':q[':db/id'],'problem':q[':question/problem'],'fields':fields,'expected_tables':q[':question/problem'].count('<table')})
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':render.append({'entity':f[':db/id'],'attribute':'answer-field/key','value':f[':answer-field/key']})
  for a in f[':answer-field/choices']:render.append({'entity':a[':db/id'],'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type'][':db/ident']==':answer.type/math'})
 rec=copy.deepcopy(q);checks=[]
 for i,f in enumerate(rec.get(':question/answer-fields',[])):
  right=f.get(':answer-field/correct',{}).get(':db/id')
  if right is None:continue
  a=next(a for a in f[':answer-field/choices']if a[':db/id']==right);f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',a[':answer/id']]
  for b in f[':answer-field/choices']:b[':answer/type']=b[':answer/type'][':db/ident']
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Canonical value accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect value rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':b[':answer/id'],'expected':'accepted'if b[':db/id']==right else'rejected','purpose':'Every owned option graded'}for b in f[':answer-field/choices'])
 if checks and all(isinstance(f.get(':answer-field/type'),str)for f in rec[':question/answer-fields']):native.append({'label':str(q[':db/id']),'record':{'question':rec,'knowledge_point':{'title':'Group 3 source and math review'},'generation':{'template':'verified-existing-or-authored-completion'}},'checks':checks})
for c in S['contents']:
 if ':tutorial/content'in c:render.append({'entity':c[':db/id'],'attribute':'tutorial/content','value':c[':tutorial/content']})
for name,v in [('proposed-questions',S['questions']),('render-input',render),('grading-input',native),('controls-input',controls)]: (H/(name+'.json')).write_text(json.dumps(v,indent=2)+'\n')
print(len(render),'render items',len(native),'grader fixtures')
