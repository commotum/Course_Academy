"""Freeze the complete requested four-lesson scope and its proposed repairs."""
import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;S1=json.loads((H/'lesson.json').read_text());S2=json.loads((H/'expanded-scope/current.json').read_text());questions=S1['questions']+S2['questions'];contents=S1['contents']+S2['contents'];first=json.loads((H/'lesson-proposals.json').read_text());pending=json.loads((H/'expanded-scope/layout-proposals.json').read_text())+json.loads((H/'completion-proposals.json').read_text());changes={(p['entity'],':'+p['attribute']):p['after']for p in first+pending};controls=[];render=[];native=[]
def patch(o):
 if isinstance(o,list):return[patch(x)for x in o]
 if not isinstance(o,dict):return o
 n={k:patch(v)for k,v in o.items()}
 for k in list(n):
  if(n.get(':db/id'),k)in changes:n[k]=changes[n[':db/id'],k]
 for(e,k),v in changes.items():
  if n.get(':db/id')==e:n[k]={':db/id':v}if k==':answer-field/correct'else v
 return n
qs=patch(questions)
for q in qs:
 fields=[]
 for f in q.get(':question/answer-fields',[]):
  choices=[{'id':a[':db/id'],'value':a[':answer/value'],'type':a[':answer/type'][':db/ident'].split('/')[-1]}for a in f[':answer-field/choices']];right=f.get(':answer-field/correct',{}).get(':db/id');assert right is not None
  fields.append({'id':f[':db/id'],'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':choices,'correctAnswer':next(a for a in choices if a['id']==right)})
 if any(f['type']=='blank'for f in fields):controls.append({'entity':q[':db/id'],'problem':q[':question/problem'],'fields':fields,'repaired':(q[':db/id'],':question/problem')in changes,'expected_tables':q[':question/problem'].count('<table')})
 for a in[':question/problem',':question/worked-solution']:
  assert q.get(a),(q[':db/id'],'Incomplete question after repair',a)
  render.append({'entity':q[':db/id'],'attribute':a[1:],'value':q[a],'fields':fields})
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:render.append({'entity':a[':db/id'],'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type'][':db/ident']==':answer.type/math'})
 rec=copy.deepcopy(q);checks=[]
 for i,f in enumerate(rec.get(':question/answer-fields',[])):
  right=f[':answer-field/correct'][':db/id'];a=next(a for a in f[':answer-field/choices']if a[':db/id']==right);f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',a[':answer/id']]
  for b in f[':answer-field/choices']:b[':answer/type']=b[':answer/type'][':db/ident']
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Preserved canonical value accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect value rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':b[':answer/id'],'expected':'accepted'if b[':db/id']==right else'rejected','purpose':'Every owned option graded'}for b in f[':answer-field/choices'])
 if checks:native.append({'label':str(q[':db/id']),'record':{'question':rec,'knowledge_point':{'title':'Full requested lesson review'},'generation':{'template':'verified-existing-or-authored-completion'}},'checks':checks})
for c in contents:
 if ':tutorial/content'in c:render.append({'entity':c[':db/id'],'attribute':'tutorial/content','value':c[':tutorial/content']})
D=H/'full-review';D.mkdir(exist_ok=True)
for name,rows in [('proposed-questions',qs),('controls-input',controls),('render-input',render),('grading-input',native)]: (D/(name+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
B=D/'repair';B.mkdir(exist_ok=True);(B/'plan.json').write_text(json.dumps({'cas':pending,'questions':sorted({p['entity']for p in pending if p['attribute'].startswith('question/')})},indent=2)+'\n')
print('Full scope:',len(qs),'questions/examples;',sum(':tutorial/content'in c for c in contents),'tutorials;',len(render),'render fields;',len(controls),'blank prompts;',len(native),'gradable questions;',len(pending),'pending changes')
