import json,copy,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;B=H/'bank-closure';q=json.loads((B/'prospective-questions.json').read_text());grading=[];fields=[]
for original in q:
 record=copy.deepcopy(original);checks=[]
 for a in['question/problem','question/worked-solution']:fields.append({'entity':record[':db/id'],'attribute':a,'value':record[':'+a]})
 for i,f in enumerate(record[':question/answer-fields']):
  correct=f[':answer-field/correct'];f[':answer-field/correct']=[':answer/id',correct[':answer/id']];f[':answer-field/type']=f[':answer-field/type'][':db/ident'];fields.append({'entity':f[':db/id'],'attribute':'answer-field/key','value':f[':answer-field/key']})
  for a in f[':answer-field/choices']:
   a[':answer/type']=a[':answer/type'][':db/ident'];fields.append({'entity':a.get(':db/id',a[':answer/id']),'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type']==':answer.type/math'});checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct[':answer/id']else'rejected','purpose':'Every retained source option and added independently verified canonical checked with current native grader'})
 grading.append({'label':str(record[':db/id']),'record':{'question':record,'knowledge_point':{'title':'Authored source-bank correction'},'generation':{'template':'bounded-bank-closure'}},'checks':checks})
(B/'grading-input.json').write_text(json.dumps(grading,indent=2)+'\n');(B/'render-input.json').write_text(json.dumps(fields,indent=2)+'\n');subprocess.run([str(H.parent/'check-engine'),str(B/'grading-input.json'),str(B/'grading.json')],check=True);print('render fields',len(fields))
