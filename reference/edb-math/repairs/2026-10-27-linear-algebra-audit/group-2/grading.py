import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());keys=json.loads((H/'missing-key-repairs.json').read_text());pm={(p['entity'],':'+p['attribute']):p['after']for p in P};km={k['field']:k['answer']for k in keys};out=[];unresolved=[]
for q0 in D['questions']:
 q=copy.deepcopy(q0)
 if any(not f.get(':answer-field/correct')and f[':db/id']not in km for f in q.get(':question/answer-fields',[])):unresolved.append(q[':db/id']);continue
 for a in ['question/problem','question/worked-solution']:
  if (q[':db/id'],':'+a)in pm:q[':'+a]=pm[q[':db/id'],':'+a]
 checks=[]
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  if f[':db/id']in km:f[':answer-field/correct']=next(a for a in f[':answer-field/choices']if a[':db/id']==km[f[':db/id']])
  if (f[':db/id'],':answer-field/key')in pm:f[':answer-field/key']=pm[f[':db/id'],':answer-field/key']
  right=f[':answer-field/correct'];f[':answer-field/correct']=[':answer/id',right[':answer/id']];f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':right[':answer/value'],'expected':'accepted','purpose':'Unchanged canonical value accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect entry rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==right[':answer/id']else'rejected','purpose':'All existing choices checked'}for a in f[':answer-field/choices'])
 if checks:out.append({'label':str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Linear algebra formatting audit'},'generation':{'template':'group-2-audit'}},'checks':checks})
for record in json.loads((H/'generator-samples.json').read_text()):
 q=record['question'];checks=[]
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  aid=f[':answer-field/correct'][1];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==aid)
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Staged generated canonical accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Staged generated incorrect rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==aid else'rejected','purpose':'All generated choices checked'}for a in f[':answer-field/choices'])
 out.append({'label':q[':question/id'],'record':record,'checks':checks})
(H/'grading-input.json').write_text(json.dumps(out,indent=2)+'\n');subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'grading-input.json'),str(H/'grading.json')],check=True);print('checked records',len(out),'checks',sum(len(o['checks'])for o in out),'unresolved missing key',unresolved)
