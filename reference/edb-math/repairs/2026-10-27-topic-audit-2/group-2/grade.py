import copy,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];out=[]
for original in json.loads((H/'proposed-questions.json').read_text()):
 fs=original.get(':question/answer-fields',[])
 if not fs or any(not f.get(':answer-field/correct')for f in fs):continue
 q=copy.deepcopy(original);checks=[]
 for i,f in enumerate(q[':question/answer-fields']):
  right=f[':answer-field/correct'];f[':answer-field/correct']=[':answer/id',right[':answer/id']];f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f.get(':answer-field/choices',[]):a[':answer/type']=a[':answer/type'][':db/ident']
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':i,'submitted':right[':answer/value'],'expected':'accepted','purpose':'Exact canonical mathematical expression accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect scalar/function rejected'}])
  else:checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==right[':answer/id']else'rejected','purpose':'Existing owned bank choices graded against verified/stored canonical link'}for a in f.get(':answer-field/choices',[]))
 out.append({'label':str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Calculus and ODE audit'},'generation':{'template':'existing-entity-audit'}},'checks':checks})
(H/'grading-input.json').write_text(json.dumps(out,indent=2)+'\n');subprocess.run([str(H.parent/'check-engine'),str(H/'grading-input.json'),str(H/'grading.json')],check=True)
