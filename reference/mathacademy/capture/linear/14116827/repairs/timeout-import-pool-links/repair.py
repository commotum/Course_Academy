import threading,json
from pathlib import Path
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.prepare import Plan,Snapshot,digest
from scripts.database.commit import Committer
from scripts.storage import atomic_json,file_lock
c=Config(account='linear');stop=threading.Event();client=EDBClient(c,stop)
d=c.output_root/'14116827/repairs/timeout-import-pool-links'
content={'topic_id':2673,'questions':[{'math_academy_id':x} for x in ['q-212950','q-212951']]}
with file_lock(c.database_lock):
 basis=client.basis();raw=client.snapshot(content,d/('snapshot-'+str(basis)),basis);s=Snapshot(raw)
 points=[p for p in s.entities.values() if ':knowledge-point/id' in p and p.get(':knowledge-point/canonical-example')]
 def point(example):
  found=[p for p in points if p.get(':knowledge-point/canonical-example',{}).get(':question/math-academy-id')==example]
  assert len(found)==1
  return found[0]
 bad,right=point('e-14580'),point('e-14585')
 plan=Plan(s);repaired=[]
 for mid in ['q-212950','q-212951']:
  q=[q for q in s.entities.values() if q.get(':question/math-academy-id')==mid];assert len(q)==1;q=q[0]
  owners={p[':db/id'] for p in q.get(':knowledge-point/_questions',[])}
  assert right[':db/id'] in owners, 'Correct pool membership must already exist'
  if bad[':db/id'] in owners:
   plan.retract(bad[':db/id'],'knowledge-point/questions',q[':db/id']);repaired.append(mid)
 batch=plan.finish();committer=Committer(c,client,d/'commit')
 if batch['forms']:
  committer.preview(batch,raw)
  atomic_json(d/'repair-plan.json',{'basis':basis,'questions':repaired,'evidence':['database/snapshot-286/questions-0.edn','content.json canonical_examples e-14580/e-14585','database/snapshot-803/questions-0.edn'],'reason':'Remove two practice-pool links introduced by the empty KP identity cache; correct memberships and UUIDs remain.'})
  request=committer.save_request(batch,raw,digest(batch));receipt=committer.submit(request);result=committer.verify_receipt(request,receipt)
  after=receipt[':edb/db-after-t']; fresh=Snapshot(client.snapshot(content,d/('snapshot-'+str(after)),after))
  for mid in repaired:
   q=next(q for q in fresh.entities.values() if q.get(':question/math-academy-id')==mid)
   owners={p[':db/id'] for p in q.get(':knowledge-point/_questions',[])}
   assert bad[':db/id'] not in owners and right[':db/id'] in owners
  result.update(status='verified',questions=repaired,basis_after=after,readback_confirmed=True)
  atomic_json(d/'result.json',result);committer.retire(request,'verified',result);print(json.dumps(result))
 else:print('No incorrect links remain')
