import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];out=[]
for record in json.loads((H/'generator-samples.json').read_text()):
 record=copy.deepcopy(record);q=record['question'];checks=[]
 for f in q.get(':question/answer-fields',[]):
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f.get(':answer-field/choices',[]):
   if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  right=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':right[':answer/value'],'expected':'accepted','purpose':'Generated canonical value accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect scalar rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==right[':answer/id']else'rejected','purpose':'Generated answer key dispatch'}for a in f[':answer-field/choices'])
 out.append({'label':str(q[':question/id']),'record':record,'checks':checks})
(H/'generator-grading-input.json').write_text(json.dumps(out,indent=2));subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'generator-grading-input.json'),str(H/'generator-grading.json')],check=True)
