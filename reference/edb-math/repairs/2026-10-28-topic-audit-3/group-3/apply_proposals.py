import collections,copy,json
from pathlib import Path
H=Path(__file__).resolve().parent;D=copy.deepcopy(json.loads((H/'snapshot.json').read_text()));nodes=collections.defaultdict(list)
def walk(o):
 if isinstance(o,dict):
  if ':db/id'in o:nodes[o[':db/id']].append(o)
  for v in o.values():walk(v)
 elif isinstance(o,list):
  for v in o:walk(v)
walk(D)
for r in json.loads((H/'duplicate-field-membership-proposals.json').read_text()):
 for n in nodes[r['entity']]:
  if ':question/answer-fields'in n:n[':question/answer-fields']=[f for f in n[':question/answer-fields']if f[':db/id']!=r['value']]
for r in json.loads((H/'missing-key-completions.json').read_text()):
 for n in nodes[r['field']]:n[':answer-field/correct']=copy.deepcopy(next(a for a in n[':answer-field/choices']if a[':db/id']==r['answer']))
for name in ['proposals.json','completion-solutions.json']:
 for r in json.loads((H/name).read_text()):
  attr=':'+r['attribute']
  for n in nodes[r['entity']]:
   if attr not in n and not(attr==':question/worked-solution'and':question/id'in n):continue
   assert n.get(attr)==r['before'],(name,r['entity'],attr);n[attr]=r['after']
(H/'proposed-snapshot.json').write_text(json.dumps(D,indent=2));fields=[];seen=set();idents=dict(json.loads((H/'idents.json').read_text()))
def fieldswalk(o):
 if isinstance(o,dict):
  e=o.get(':db/id');checkbox=o.get(':answer-field/type',{}).get(':db/id')==17592186408166
  for a,v in o.items():
   if isinstance(v,str)and(a in[':question/problem',':question/worked-solution',':tutorial/content',':multistep/context',':answer/value',':answer/feedback']or checkbox and a==':answer-field/key')and(e,a)not in seen:seen.add((e,a));fields.append({'entity':e,'attribute':a[1:],'value':v,'bare_math':a==':answer/value'and idents[o[':answer/type'][':db/id']]==':answer.type/math'})
   elif isinstance(v,(dict,list)):fieldswalk(v)
 elif isinstance(o,list):
  for v in o:fieldswalk(v)
fieldswalk(D['questions']);fieldswalk(D['content']);(H/'proposed-render-input.json').write_text(json.dumps(fields,indent=2));print('proposedvisiblefields',len(fields))
