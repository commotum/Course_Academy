"""Compare bounded relation reads with the former scalar reads at one basis."""
import hashlib
import threading
from pathlib import Path
from scripts.config import Config
from scripts.database.client import EDBClient, ACTIVITY_PULL
from scripts.database.edn import dumps
from scripts.storage import atomic_json

root=Path(__file__).resolve().parent/'batched-snapshot-read'
client=EDBClient(Config(),threading.Event())
identity=client.status()
basis=identity['basis']
topics=[665,774,5916]
queries={
 'topics':'''[:find (pull ?t [* {:topic/knowledge-points [*
 {:knowledge-point/canonical-example [:db/id :question/id :question/math-academy-id]}
 {:knowledge-point/questions [:db/id :question/id :question/math-academy-id]}]}])
 :in $ ?id :where [?t :topic/math-academy-id ?id]]''',
 'activities':'[:find (pull ?a '+ACTIVITY_PULL+''') :in $ ?id
 :where [?t :topic/math-academy-id ?id] [?a :activity/scope ?t]]'''}
findings=[]
for name,query in queries.items():
 scalar=[]
 for tid in topics:
  scalar+=client.query(query,[tid],root,name+'-scalar-'+str(tid),basis)
 grouped=client.query(query.replace(':in $ ?id',':in $ [?id ...]'),[topics],root,name+'-batched',basis)
 canonical=lambda rows:sorted(dumps(row) for row in rows)
 assert canonical(scalar)==canonical(grouped),name+' returned different entities'
 findings.append({'relation':name,'rows':len(grouped),'identical':True,
                  'sha256':hashlib.sha256(dumps(canonical(grouped)).encode()).hexdigest()})
atomic_json(root/'verification.json',{'identity':identity,'topics':topics,'reads':findings})
print({'basis':basis,'lineage':identity['lineage'],'reads':findings})
