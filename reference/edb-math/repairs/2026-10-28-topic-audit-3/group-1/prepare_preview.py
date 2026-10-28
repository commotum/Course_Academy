import copy,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import validate_math_structure
D=copy.deepcopy(json.loads((H/'current.json').read_text()));entities={}
def visit(x):
 if isinstance(x,dict):
  if ':db/id'in x:entities.setdefault(x[':db/id'],[]).append(x)
  for value in x.values():visit(value)
 elif isinstance(x,list):
  for value in x:visit(value)
visit(D)
for p in json.loads((H/'proposals.json').read_text()):
 objects=entities[p['entity']];assert objects
 for obj in objects:
  attr=':'+p['attribute'];
  if attr not in obj and p['before']is not None:continue
  assert obj.get(attr)==p['before'],(p['entity'],attr);obj[attr]=p['after']
for p in json.loads((H/'missing-key-proposals.json').read_text()):
 for f in [o for o in entities[p['entity']]if ':answer-field/id'in o]:
  assert ':answer-field/correct'not in f;f[':answer-field/correct']=next(a for a in f[':answer-field/choices']if a[':db/id']==p['after'])
for p in json.loads((H/'new-answer-proposals.json').read_text()):
 for f in [o for o in entities[p['field']]if ':answer-field/id'in o]:
  assert not f.get(':answer-field/choices');answer={':answer/id':p['answer_id'],':answer/type':{':db/id':17592186045498,':db/ident':p['answer_type']},':answer/value':p['answer_value']};f[':answer-field/choices']=[answer];f[':answer-field/correct']=answer
for p in json.loads((H/'membership-proposals.json').read_text()):
 for q in [o for o in entities[p['entity']]if ':question/id'in o]:
  assert sorted(f[':db/id']for f in q[':question/answer-fields'])==p['before'];q[':question/answer-fields']=[f for f in q[':question/answer-fields']if f[':db/id']in p['after']]
items=[]
for p in json.loads((H/'proposals.json').read_text()):items.append({'entity':p['entity'],'attribute':p['attribute'],'value':p['after'],'bare_math':p['attribute']=='answer/value'})
for p in json.loads((H/'new-answer-proposals.json').read_text()):items.append({'entity':p['answer_id'],'attribute':'answer/value','value':p['answer_value'],'bare_math':True})
for item in items:validate_math_structure(item['value'],bare_math=item['bare_math'])
(H/'staged-current.json').write_text(json.dumps(D,indent=2)+'\n');(H/'proposed-render-input.json').write_text(json.dumps(items,indent=2)+'\n');print('staged questions',len(D['questions']),'changedvalues',len(items))
