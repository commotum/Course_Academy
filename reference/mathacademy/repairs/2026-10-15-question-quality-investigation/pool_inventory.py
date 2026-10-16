import json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'));from edn import loads
entities={};pools=[]
def add(x):
 if isinstance(x,list):return [add(v) for v in x]
 if not isinstance(x,dict):return x
 if ':db/id' not in x:return x
 eid=x[':db/id'];out=entities.setdefault(str(eid),{})
 for k,v in x.items():
  if k==':db/id' or '/_' in k:continue
  out[k[1:]]=add(v)
 return eid
for path in sorted(H.glob('kp-*.edn')):
 if path.name=='kp-pull.edn':continue
 kp=loads(path.read_text());add(kp);pools.append({'kp':kp[':db/id'],'title':kp[':knowledge-point/title'],'questions':[q[':db/id'] for q in kp.get(':knowledge-point/questions',[])]})
ids=sorted({q for p in pools for q in p['questions']});basis=json.loads((H/'snapshot.json').read_text())['basis']
(H/'pool-input.json').write_text(json.dumps({'basis':basis,'entities':entities,'questions':ids,'proposals':[]},indent=2,default=str)+'\n')
subprocess.run([str(H/'native-validation'),str(H/'pool-input.json'),str(H/'pool-native-report.json')],check=True)
checked={r['question']:r['current_validation_error'] for r in json.loads((H/'pool-native-report.json').read_text())['records']}
for p in pools:
 p['usable']=sum(checked[q] is None for q in p['questions']);p['blocked']=len(p['questions'])-p['usable']
 p['usable_by_level']={}
 for q in p['questions']:
  if checked[q] is not None:continue
  rating=entities[str(q)].get('question/difficulty');key=entities.get(str(rating),{}).get('db/ident','unrated') if rating is not None else 'unrated'
  p['usable_by_level'][key]=p['usable_by_level'].get(key,0)+1
(H/'pool-inventory.json').write_text(json.dumps(pools,indent=2)+'\n')
print(json.dumps({'skills':len(pools),'questions':len(ids),'usable':sum(p['usable'] for p in pools),'blocked':sum(p['blocked'] for p in pools),'minimum_usable_per_skill':min(p['usable'] for p in pools)}))
