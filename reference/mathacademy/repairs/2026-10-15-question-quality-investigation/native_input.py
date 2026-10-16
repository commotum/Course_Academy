import json
from pathlib import Path
H=Path(__file__).resolve().parent;qs=json.loads((H/'questions.json').read_text());entities={}
def add(x):
 if isinstance(x,list):return [add(v) for v in x]
 if not isinstance(x,dict):return x
 if ':db/id' not in x:return x
 eid=x[':db/id'];record=entities.setdefault(str(eid),{})
 for k,v in x.items():
  if k==':db/id' or '/_' in k:continue
  record[k[1:]]=add(v)
 return eid
for q in qs:add(q)
(H/'native-input.json').write_text(json.dumps({'basis':json.loads((H/'snapshot.json').read_text())['basis'],'entities':entities,'questions':[q[':db/id'] for q in qs]},indent=2)+'\n')
