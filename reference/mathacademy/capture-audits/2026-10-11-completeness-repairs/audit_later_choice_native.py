"""Read-only pinned ownership check, distinguishing pre-existing receipts."""
from pathlib import Path
import json,threading
from collections import defaultdict
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.database.edn import loads
from scripts.storage import atomic_json,read_json
ROOT=Path(__file__).resolve().parent;a=read_json(ROOT/'later-attribution-receipt-audit.json');groups=defaultdict(list)
for row in a['receipts']:
 if not row['choice_retractions']:continue
 req=Path(row['request']);receipt=loads((req.parent/'receipt.edn').read_text());idents=dict(loads((req.parents[2]/f'snapshot-{row["basis_before"]}'/'idents.edn').read_text()))
 for datom in receipt[':edb/tx-data']:
  if len(datom)==6 and not datom[5] and str(idents.get(datom[1]))==':answer-field/choices':
   groups[row['basis_before']].append({'task_id':row['task_id'],'answer_entity':datom[2],'field_entity':datom[0],'pre_existing_additional_archive_receipt':row.get('pre_existing_additional_archive_receipt',False)})
client=EDBClient(Config(account='multivariable'),threading.Event());basis=client.basis();directory=ROOT/'choice-ownership-final-pinned-readback'
query='[:find (pull ?a [* {:task-item/_responses [:db/id]} {:answer-field/_choices [:db/id :answer-field/id :answer-field/key]}]) :in $ [?a ...]]'
entities=sorted({x['answer_entity'] for rows in groups.values() for x in rows});after=client.query(query,[entities],directory,'after',basis);current={row[0][':db/id']:row[0] for row in after};checks=[]
for before_basis,rows in groups.items():
 previous=client.query(query,[sorted({x['answer_entity'] for x in rows})],directory,'before-'+str(before_basis),before_basis);previous={row[0][':db/id']:row[0] for row in previous}
 for row in rows:
  eid=row['answer_entity'];old,new=previous[eid],current[eid];keys=[':answer/id',':answer/type',':answer/value']
  check={**row,'basis_before':before_basis,'basis_after':basis,'before':old,'after':new,'no_response_owner_before':not old.get(':task-item/_responses'),'answer_entity_preserved':all(old.get(k)==new.get(k) for k in keys)}
  assert check['no_response_owner_before'] and check['answer_entity_preserved'],check
  checks.append(check)
atomic_json(ROOT/'later-choice-ownership-final-native-audit.json',json.loads(json.dumps({'basis_after':basis,'checks':checks,'repair_choice_retractions':sum(not x['pre_existing_additional_archive_receipt'] for x in checks),'pre_existing_additional_archive_choice_retractions':sum(x['pre_existing_additional_archive_receipt'] for x in checks)},default=str)))
print(json.dumps({'choices':len(checks),'all_unowned_before_and_entities_preserved':True,'basis_after':basis}))
