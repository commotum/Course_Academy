"""Read-only conditional reproduction of the inspected all-easy selection branch."""
import collections,hashlib,json
from pathlib import Path
from regressions import W,read
E=W/'evidence';rs=json.loads((E/'delivery-controls/accepted.json').read_text());batch=json.loads((E/'delivery-batch/accepted.json').read_text())
def select(pool,seed,weighted=True,easy_positive=True):
    pool=sorted(set(pool))
    if not pool:return None
    if not weighted:return pool[0]
    if not easy_positive:return None
    digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
    u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
    return pool[int(u*len(pool))]
result=[]
for label,records in [('controlled-survivors',rs),('fresh-batch',batch)]:
    # Entity IDs have not been allocated; these IDs are hypothetical, not database changes.
    pool=list(range(1000,1000+len(records)));draws=[];roles=collections.Counter();seen=set()
    for i in range(64):
        picked=select(pool,'author-repair/'+str(i));r=records[picked-1000];d=read(r);role=sorted(d['values']).index(d['c']);roles[role]+=1;seen.add(picked)
        draws.append({'seed':'author-repair/'+str(i),'hypothetical_entity_id':picked,'question_id':r['question'][':question/id'],'correct_sorted_role':role})
    result.append({'scenario':label,'eligible':len(pool),'unique_selected':len(seen),'selected_sorted_roles':dict(roles),'draws':draws,'no_weight_configuration_first_id':select(pool,'ignored',False),'zero_easy_weight':select(pool,'ignored',True,False)})
(E/'learner-selection.json').write_text(json.dumps({'implementation':'Read engine/rust/question_selection.rs::select and seen_before_task. Reproduce only the configured-positive-easy within-band SHA256 draw, no-policy first-ID fallback and zero-easy exclusion. All generated records are rated easy.','results':result,'sampler_rejection':'Normal generation has no rejection/resampling loop. For every bank and role, the n and m bounds admit every choice; rank feasibility was independently checked. Explicit invalid parameter requests reject. Delivery retained all 70 controls and five batch records.','limits':['Captured inventory has no learner histories or configured weight entities. New records have no allocated database IDs. These are conditional draws with hypothetical IDs, not native selection results or a prediction of live tasks.','Freshness excludes previous tasks and current prefix. Any such exclusion may remove individual cases. No claim is made that every arbitrary learner-specific subset retains every role.','Future live inventory and concurrent publication are untested.']},indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k!='draws'} for r in result]))
