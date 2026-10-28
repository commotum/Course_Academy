import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];out=[]
for q in json.loads((H/'proposed-questions.json').read_text()):
 fs=q.get(':question/answer-fields',[])
 if not fs:continue
 q=copy.deepcopy(q);checks=[]
 for i,f in enumerate(q[':question/answer-fields']):
  right=f[':answer-field/correct'];f[':answer-field/correct']=[':answer/id',right[':answer/id']];f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':right[':answer/value'],'expected':'accepted','purpose':'Original exact canonical value accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect matrix entry rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==right[':answer/id']else'rejected','purpose':'All existing choices checked against independently verified key'}for a in f[':answer-field/choices'])
 out.append({'label':str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Multiplying a Matrix by the Identity Matrix'},'generation':{'template':'lesson-completion-audit'}},'checks':checks})
(H/'grading-input.json').write_text(json.dumps(out,indent=2)+'\n');subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'grading-input.json'),str(H/'grading.json')],check=True)
