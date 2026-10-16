import importlib.util,json,hashlib,shutil
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('replenish',H/'replenish.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
path=H/'reference/pre-generation';inv=r.inventory(path/'inventory.json');kp=r.read_kp(path,inv['basis']);counts=r.count(kp,path,inv['basis']);used={r.task(q) for q in kp[':knowledge-point/questions']};records=[]
for l in r.LEVELS:
 added=0
 for offset in range(200):
  rec=r.g.generate(l,seed=int(r.JOB.name[:8],16)+offset);fp=r.task(rec['question'])
  if fp in used:continue
  r.v.check(rec);records.append(rec);used.add(fp);added+=1
  if added==6:break
 assert added==6
(H/'review-candidates.json').write_text(json.dumps(records,indent=2)+'\n')
review=[]
for c in json.loads((H/'source-cases.json').read_text()):
 l=r.g.TEMPLATES[c['template']]['level']
 for profile in ['raw-source','observed']:
  review.append(r.g.generate(l,template=c['template'],parameters=c['parameters'],profile=profile))
review+=records
(H/'render-records.json').write_text(json.dumps(review)+'\n')
print(json.dumps({'basis':inv['basis'],'validated_inventory':counts,'review_candidates':len(records)},indent=2))
