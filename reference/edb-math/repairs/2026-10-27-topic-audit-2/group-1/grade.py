import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];out=[];skip=[]
D=json.loads((H/'current.json').read_text())
for q in D['questions']:
 if not q.get(':question/answer-fields'):continue
 q=copy.deepcopy(q);checks=[];fields=[]
 for f in q[':question/answer-fields']:
  if ':answer-field/correct'not in f:skip.append({'question':q[':db/id'],'field':f[':db/id'],'reason':'Missing canonical answer link'});continue
  fields.append(f);i=len(fields)-1;right=f[':answer-field/correct'];f[':answer-field/correct']=[':answer/id',right[':answer/id']];f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':right[':answer/value'],'expected':'accepted','purpose':'Exact existing canonical value accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect scalar rejected'}])
  elif f[':answer-field/type']in [':answer-field.type/radio',':answer-field.type/select',':answer-field.type/checkbox']:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==right[':answer/id']else'rejected','purpose':'Existing canonical key dispatch'}for a in f[':answer-field/choices'])
 q[':question/answer-fields']=fields
 if checks:out.append({'label':str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Linear algebra group 1 audit'},'generation':{'template':'group-1-audit'}},'checks':checks})
(H/'grading-input.json').write_text(json.dumps(out,indent=2));(H/'grading-skipped.json').write_text(json.dumps(skip,indent=2));subprocess.run([str(H.parent/'check-engine'),str(H/'grading-input.json'),str(H/'grading.json')],check=True)
