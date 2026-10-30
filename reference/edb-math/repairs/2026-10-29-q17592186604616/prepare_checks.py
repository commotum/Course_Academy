import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;S=json.loads((H/'lesson.json').read_text());ps=json.loads((H/'lesson-proposals.json').read_text());changes={p['entity']:p['after']for p in ps};ev={r['entity']:r for r in json.loads((H/'source-reconstruction.json').read_text())};controls=[];render=[];grading=[]
for q in S['questions']:
 fields=[]
 for f in q.get(':question/answer-fields',[]):
  choices=[{'id':a[':db/id'],'value':a[':answer/value'],'type':a[':answer/type'][':db/ident'].split('/')[-1]}for a in f[':answer-field/choices']];right=f.get(':answer-field/correct',{}).get(':db/id');fields.append({'id':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':choices,'correctAnswer':next((a for a in choices if a['id']==right),None)})
 if q[':db/id']in changes:controls.append({'entity':q[':db/id'],'problem':changes[q[':db/id']],'fields':fields,'repaired':True,'expected_tables':3 if ev[q[':db/id']]['kind']=='matrix_product'else 1})
 for a in[':question/problem',':question/worked-solution']:render.append({'entity':q[':db/id'],'attribute':a[1:],'value':changes.get(q[':db/id'],q.get(a,''))if a==':question/problem'else q.get(a,''),'fields':fields})
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:render.append({'entity':a[':db/id'],'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type'][':db/ident']==':answer.type/math'})
 for phase in['before','after']:
  if any(not f.get(':answer-field/correct')for f in q.get(':question/answer-fields',[])):continue
  rec=copy.deepcopy(q)
  if phase=='after'and q[':db/id']in changes:rec[':question/problem']=changes[q[':db/id']]
  checks=[]
  for i,f in enumerate(rec.get(':question/answer-fields',[])):
   right=f.get(':answer-field/correct',{}).get(':db/id');bank=f[':answer-field/choices'];a=next((a for a in bank if a[':db/id']==right),None);assert a,(q[':db/id'],f[':db/id'])
   f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',a[':answer/id']]
   for b in bank:b[':answer/type']=b[':answer/type'][':db/ident']
   if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Preserved canonical blank value'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect value rejected'}])
   else:checks.extend({'field_index':i,'submitted_answer_id':b[':answer/id'],'expected':'accepted'if b[':db/id']==right else'rejected','purpose':'Every owned option remains correctly keyed'}for b in bank)
  if checks:grading.append({'label':phase+'-'+str(q[':db/id']),'record':{'question':rec,'knowledge_point':{'title':'Matrix lesson repair'},'generation':{'template':'source-layout'}},'checks':checks})
for c in S['contents']:
 if ':tutorial/content'in c:render.append({'entity':c[':db/id'],'attribute':'tutorial/content','value':c[':tutorial/content']})
for name,data in [('controls-input',controls),('render-input',render),('grading-input',grading)]: (H/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
D=H/'lesson-repair';D.mkdir(exist_ok=True);(D/'plan.json').write_text(json.dumps({'cas':ps,'questions':list(changes)},indent=2)+'\n');print('Prepared',len(controls),'control prompts;',len(render),'rendered fields;',len(grading),'gradeable question phases')
