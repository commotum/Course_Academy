import copy,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());pm={(p['entity'],':'+p['attribute']):p['after']for p in P};native=[];baseline=[];render=[];controls=[]
def patch(o):
 if isinstance(o,list):return[patch(x)for x in o]
 if not isinstance(o,dict):return o
 n={k:patch(v)for k,v in o.items()}
 for(e,k),v in pm.items():
  if n.get(':db/id')==e:n[k]={':db/id':v}if k==':answer-field/correct'else v
 return n
qs=patch(D['questions']);detached={x['value']for x in json.loads((H/'detachments.json').read_text())}
for q in qs:q[':question/answer-fields']=[f for f in q.get(':question/answer-fields',[])if f[':db/id']not in detached]
contents=patch(D['contents'])
for q in qs:
 fs=[]
 for f in q.get(':question/answer-fields',[]):
  choices=[{'id':a[':db/id'],'value':a[':answer/value'],'type':a[':answer/type'][':db/ident'].split('/')[-1]}for a in f[':answer-field/choices']];right=f.get(':answer-field/correct',{}).get(':db/id');assert right is not None
  fs.append({'id':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':choices,'correctAnswer':next(a for a in choices if a['id']==right)})
 controls.append({'entity':q[':db/id'],'problem':q[':question/problem'],'fields':fs,'repaired':(q[':db/id'],':question/problem')in pm,'expected_tables':q[':question/problem'].count('<table')})
 for attr in[':question/problem',':question/worked-solution']:assert q.get(attr);render.append({'entity':q[':db/id'],'attribute':attr[1:],'value':q[attr],'fields':fs})
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/ident'].endswith('checkbox'):render.append({'entity':f[':db/id'],'attribute':'answer-field/key','value':f[':answer-field/key']})
  for a in f[':answer-field/choices']:render.append({'entity':a[':db/id'],'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type'][':db/ident']==':answer.type/math'})
 rec=copy.deepcopy(q);checks=[]
 for i,f in enumerate(rec.get(':question/answer-fields',[])):
  right=f[':answer-field/correct'][':db/id'];a=next(a for a in f[':answer-field/choices']if a[':db/id']==right);f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',a[':answer/id']]
  for b in f[':answer-field/choices']:b[':answer/type']=b[':answer/type'][':db/ident']
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Canonical value accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':b[':answer/id'],'expected':'accepted'if b[':db/id']==right else'rejected','purpose':'Every owned option graded'}for b in f[':answer-field/choices'])
 if checks:
  fixture={'label':str(q[':db/id']),'record':{'question':rec,'knowledge_point':{'title':'MTH341 group 1 quality audit'},'generation':{'template':'verified-existing-or-authored-completion'}},'checks':checks};native.append(fixture)
  before=copy.deepcopy(fixture)
  for f in before['record']['question'].get(':question/answer-fields',[]):
   for a in f[':answer-field/choices']:
    p=next((p for p in P if p['entity']==a[':db/id']and p['attribute']=='answer/value'),None)
    if p:a[':answer/value']=p['before']
  baseline.append(before)
for c in contents:
 if ':tutorial/content'in c:render.append({'entity':c[':db/id'],'attribute':'tutorial/content','value':c[':tutorial/content']})
for name,rows in [('proposed-questions',qs),('controls-input',controls),('render-input',render),('grading-input',native),('grading-before-display-input',baseline)]: (H/(name+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
print('Questions',len(qs),'render fields',len(render),'native questions',len(native),'native checks',sum(len(r['checks'])for r in native))
