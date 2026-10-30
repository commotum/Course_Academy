import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());ps=json.loads((H/'proposals.json').read_text());changes={(p['entity'],':'+p['attribute']):p['after']for p in ps}
def patch(o):
 if isinstance(o,list):return[patch(x)for x in o]
 if not isinstance(o,dict):return o
 n={k:patch(v)for k,v in o.items()}
 for(e,k),v in changes.items():
  if n.get(':db/id')==e:n[k]={':db/id':v}if k==':answer-field/correct'else v
 return n
S=patch(S);qs=S['questions'];render=[];native=[];controls=[]
for q in qs:
 fields=[]
 for f in q.get(':question/answer-fields',[]):
  choices=[{'id':a[':db/id'],'value':a[':answer/value'],'type':a[':answer/type'][':db/ident'].split('/')[-1]}for a in f[':answer-field/choices']];right=f.get(':answer-field/correct',{}).get(':db/id');assert right is not None
  fields.append({'id':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':choices,'correctAnswer':next(a for a in choices if a['id']==right)})
 controls.append({'entity':q[':db/id'],'problem':q[':question/problem'],'fields':fields,'repaired':q[':db/id']in{p['entity']for p in json.loads((H/'layout-proposals.json').read_text())},'expected_tables':q[':question/problem'].count('<table')})
 for a in[':question/problem',':question/worked-solution']:
  assert q.get(a),(q[':db/id'],a);render.append({'entity':q[':db/id'],'attribute':a[1:],'value':q[a],'fields':fields})
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':render.append({'entity':f[':db/id'],'attribute':'answer-field/key','value':f[':answer-field/key']})
  for a in f[':answer-field/choices']:render.append({'entity':a[':db/id'],'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type'][':db/ident']==':answer.type/math'})
 rec=copy.deepcopy(q);checks=[]
 for i,f in enumerate(rec.get(':question/answer-fields',[])):
  right=f[':answer-field/correct'][':db/id'];a=next(a for a in f[':answer-field/choices']if a[':db/id']==right);f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',a[':answer/id']]
  for b in f[':answer-field/choices']:b[':answer/type']=b[':answer/type'][':db/ident']
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Canonical value accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect value rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':b[':answer/id'],'expected':'accepted'if b[':db/id']==right else'rejected','purpose':'Every owned option graded'}for b in f[':answer-field/choices'])
 if checks:native.append({'label':str(q[':db/id']),'record':{'question':rec,'knowledge_point':{'title':'MTH341 group 2 full audit'},'generation':{'template':'verified-existing-or-authored-completion'}},'checks':checks})
for c in S['contents']:
 if ':tutorial/content'in c:render.append({'entity':c[':db/id'],'attribute':'tutorial/content','value':c[':tutorial/content']})
for name,data in [('proposed-snapshot',S),('proposed-questions',qs),('render-input',render),('grading-input',native),('controls-input',controls)]: (H/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
print(len(qs),'questions',len(render),'render fragments',len(native),'native records')
