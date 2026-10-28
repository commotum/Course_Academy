import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());members=json.loads((H/'membership-proposals.json').read_text());main={(p['entity'],p['attribute']):p for p in json.loads((H/'proposals.json').read_text())};keys={p['entity']:p for p in json.loads((H/'missing-key-proposals.json').read_text())};cases=[]
for m in members:
 q=copy.deepcopy(next(q for q in D['questions']if q[':db/id']==m['entity']));f=next(f for f in q[':question/answer-fields']if f[':db/id']==m['retract_value']);q[':question/answer-fields']=[f]
 for attr in ['question/problem','question/worked-solution']:
  if(q[':db/id'],attr)in main:q[':'+attr]=main[q[':db/id'],attr]['after']
 right=keys[f[':db/id']]['after'];checks=[];f[':answer-field/type']=f[':answer-field/type'][':db/ident']
 for a in f[':answer-field/choices']:
  if(a[':db/id'],'answer/value')in main:a[':answer/value']=main[a[':db/id'],'answer/value']['after']
  a[':answer/type']=a[':answer/type'][':db/ident'];checks.append({'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':db/id']==right else'rejected','purpose':'Archived bank AFTER source-format/exponent restoration and independent canonical completion'})
 f[':answer-field/correct']=[':answer/id',next(a[':answer/id']for a in f[':answer-field/choices']if a[':db/id']==right)]
 cases.append({'label':str(q[':db/id']),'record':{'knowledge_point':{'title':'Archived old bank validation'},'question':q,'generation':{'template':'archived-after-bank'}},'checks':checks})
(H/'archived-grading-input.json').write_text(json.dumps(cases,indent=2)+'\n');subprocess.run([str(H.parent/'check-engine'),str(H/'archived-grading-input.json'),str(H/'archived-grading.json')],check=True)
