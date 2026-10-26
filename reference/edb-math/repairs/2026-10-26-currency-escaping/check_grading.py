import copy,json
from pathlib import Path
H=Path(__file__).resolve().parent;repairs={f['entity']:f for f in json.loads((H/'fields.json').read_text())};qs=json.loads((H/'questions.json').read_text());native=[];skipped=[]
for original in qs:
 fs=original.get(':question/answer-fields',[])
 if not fs or any(not f.get(':answer-field/correct')for f in fs):skipped.append({'entity':original[':db/id'],'reason':'Preexisting missing answer fields or correct links; preserved unchanged'});continue
 for phase in ['before','after']:
  q=copy.deepcopy(original);checks=[]
  for i,f in enumerate(q[':question/answer-fields']):
   cid=f[':answer-field/correct'][':answer/id'];f[':answer-field/correct']=[':answer/id',cid]
   for a in f[':answer-field/choices']:
    if phase=='after'and a[':db/id']in repairs:a[':answer/value']=repairs[a[':db/id']]['after']
   kind=f[':answer-field/type'][':db/ident']
   if kind.endswith('/radio')or kind.endswith('/select'):
    checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else'rejected','purpose':'Same choice identity '+phase+' literal-currency repair'}for a in f[':answer-field/choices'])
   else:raise ValueError((q[':db/id'],kind))
  native.append({'label':phase+':'+str(q[':db/id']),'record':{'question':q,'knowledge_point':{'title':'Currency-label preservation'},'generation':{'template':'source-answer-escaping'}},'checks':checks})
(H/'native-grading-input.json').write_text(json.dumps(native,indent=2)+'\n');(H/'preexisting-incomplete.json').write_text(json.dumps(skipped,indent=2)+'\n');print('Before/after cases',len(native),'preexisting incomplete questions',len(skipped))
