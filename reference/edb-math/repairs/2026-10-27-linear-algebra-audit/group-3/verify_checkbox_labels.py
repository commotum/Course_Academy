import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=Path.cwd();D=json.loads((H/'snapshot.json').read_text());C=json.loads((H/'checkbox-labels-current.json').read_text());P=json.loads((H/'checkbox-label-proposals.json').read_text());current={f['entity']:f for f in C['labels']};after={p['entity']:p['after']for p in P};idents=dict(json.loads((H/'idents.json').read_text()));out=[]
for oq in D['questions']:
 if not any(f[':db/id']in current for f in oq.get(':question/answer-fields',[])):continue
 q=copy.deepcopy(oq);checks=[]
 for i,f in enumerate(q[':question/answer-fields']):
  f[':answer-field/type']=idents[f[':answer-field/type'][':db/id']]
  for a in f[':answer-field/choices']:a[':answer/type']=idents[a[':answer/type'][':db/id']]
  if f[':db/id']not in current:continue
  c=current[f[':db/id']];f[':answer-field/key']=after.get(f[':db/id'],c['value']);right=c['correct'];a=next(a for a in f[':answer-field/choices']if a[':db/id']==right);f[':answer-field/correct']=[':answer/id',a[':answer/id']];checks.extend({'field_index':i,'submitted_answer_id':a2[':answer/id'],'expected':'accepted'if a2[':db/id']==right else'rejected','purpose':'Canonical Boolean grading after label-only correction'}for a2 in f[':answer-field/choices'])
 out.append({'label':str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Linear algebra checkbox label audit'},'generation':{'template':'checkbox-label-audit'}},'checks':checks})
(H/'checkbox-label-grading-input.json').write_text(json.dumps(out,indent=2));subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'checkbox-label-grading-input.json'),str(H/'checkbox-label-grading.json')],check=True)
records=json.loads((H/'checkbox-generator-samples.json').read_text());out=[]
for i,r in enumerate(records):
 checks=[]
 for j,f in enumerate(r['question'][':question/answer-fields']):
  right=f[':answer-field/correct'][1];checks.extend({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==right else'rejected'}for a in f[':answer-field/choices'])
 out.append({'label':'label-generator-'+str(i),'record':r,'checks':checks})
(H/'checkbox-generator-grading-input.json').write_text(json.dumps(out,indent=2));subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'checkbox-generator-grading-input.json'),str(H/'checkbox-generator-grading.json')],check=True)
# Field-only generators use UUIDs; supply those identities directly to actual controls.
fields=[]
for r in records:
 for f in r['question'][':question/answer-fields']:
  typ=f[':answer-field/type'].get(':db/ident')if isinstance(f[':answer-field/type'],dict)else f[':answer-field/type']
  if typ!=':answer-field.type/checkbox':continue
  fields.append({'entity':f[':answer-field/id'],'attribute':'answer-field/key','value':f[':answer-field/key'],'question':r['question'][':question/id'],'bare':False,'choices':[{'id':a[':answer/id'],'entityId':a[':answer/id'],'type':'text','value':a[':answer/value']}for a in f[':answer-field/choices']]})
(H/'checkbox-generator-label-fields.json').write_text(json.dumps(fields,indent=2));print('current labels',len(current),'label repairs',len(P),'generated labels',len(fields))
