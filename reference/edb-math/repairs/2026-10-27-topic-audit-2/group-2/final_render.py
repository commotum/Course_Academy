import json
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());ps={(p['entity'],p['attribute']):p['after']for p in json.loads((H/'proposals.json').read_text())};fields={}
for a in D['activities']:
 for c in a['contents']:
  if ':tutorial/content'in c:fields[c[':db/id'],'tutorial/content']={'entity':c[':db/id'],'attribute':'tutorial/content','value':ps.get((c[':db/id'],'tutorial/content'),c[':tutorial/content'])}
for q in json.loads((H/'proposed-questions.json').read_text()):
 for a in['question/problem','question/worked-solution']:
  if ':'+a in q:fields[q[':db/id'],a]={'entity':q[':db/id'],'attribute':a,'value':q[':'+a]}
 for f in q.get(':question/answer-fields',[]):
  if f[':answer-field/type'][':db/ident']!=':answer-field.type/blank':fields[f[':db/id'],'answer-field/key']={'entity':f[':db/id'],'attribute':'answer-field/key','value':f[':answer-field/key']}
  for a in f.get(':answer-field/choices',[]):
   e=a.get(':db/id',a[':answer/id']);fields[e,'answer/value']={'entity':e,'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type'][':db/ident']==':answer.type/math'}
   if ':answer/feedback'in a:fields[e,'answer/feedback']={'entity':e,'attribute':'answer/feedback','value':a[':answer/feedback']}
(H/'final-render-input.json').write_text(json.dumps(list(fields.values()),indent=2)+'\n');print(len(fields))
