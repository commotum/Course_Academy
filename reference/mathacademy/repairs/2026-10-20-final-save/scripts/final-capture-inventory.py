from pathlib import Path
from collections import Counter
import time
from scripts.config import Config
from scripts.storage import read_json,atomic_json
from scripts.outbox import target_id,FINAL
from scripts.monitor_data import capture_integrity
root=Path('reference/mathacademy/repairs/2026-10-20-final-save')
ids=set();counts=Counter();errors=[];empty=[]
for account in ('foundations','linear','multivariable','differential'):
 c=Config(account=account)
 for marker in c.output_root.glob('*/capture-complete.json'):
  p=marker.parent;q=read_json(p/'content.json')
  for bucket in ('questions','reference_questions','canonical_examples'):
   counts[bucket]+=len(q.get(bucket,[]))
   for record in q.get(bucket,[]):
    mid=record.get('math_academy_id')
    if mid:ids.add(mid)
    if record.get('errors'):errors.append({'directory':str(p),'id':mid,'errors':record['errors']})
  if not q.get('questions'):empty.append(str(p))
  counts['activities']+=1
atomic_json(root/'source-inventory.json',{'counts':dict(counts),'unique_source_ids':sorted(ids),'records_with_errors':errors,'empty_activities':empty,'at':time.time()})
print(dict(counts),'unique source IDs',len(ids),'with extraction errors',len(errors),'empty',empty)
