import json
from pathlib import Path
from generator_publish import Publisher,KP_PULL,jsonable
H=Path('generate/reports/lesson-quality-audit-2026-11-11');scope=json.loads((H/'coverage-inventory.json').read_text());p=Publisher.from_environment();status=p.client.status();basis=status['basis'];ids=[x['kp'] for x in scope]
rows=p.client.query('[:find (pull ?kp '+KP_PULL+') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',[ids],H,'closing-kps',basis);current={k[':db/id']:jsonable(k) for (k,) in rows}
def canon(x):
 if isinstance(x,dict):return {k:canon(v) for k,v in sorted(x.items())}
 if isinstance(x,list):return sorted([canon(v) for v in x],key=lambda v:json.dumps(v,sort_keys=True))
 return x
result=[]
for s in scope:
 old=json.loads(Path(s['snapshot']).read_text());new=current[s['kp']]
 result.append({'kp':s['kp'],'registration_unchanged':canon(old.get(':knowledge-point/question-generator'))==canon(new.get(':knowledge-point/question-generator')),'stored_pool_unchanged':canon(old[':knowledge-point/questions'])==canon(new[':knowledge-point/questions'])})
r={'audited_basis':json.loads((H/'status.json').read_text())['basis'],'closing_basis':basis,'passed':all(v['registration_unchanged'] and v['stored_pool_unchanged'] for v in result),'results':result,'database_writes':0}
(H/'closing-verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
