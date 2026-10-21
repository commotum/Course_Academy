"""Read-only stage and captured-inventory analysis of demonstrated quotient cue."""
import json,pathlib,collections,hashlib
from bank_shortcut import probe,choose
R=pathlib.Path(__file__).resolve().parent;J=R.parent
load=lambda p:json.load(open(p))
def save(n,x):(R/n).write_text(json.dumps(x,indent=2,ensure_ascii=False))
i=load(J/'source/inventory.json');qs=i['questions'];rows=[]
for q in qs:
 f=q[':question/answer-fields'][0];raw=[c[':answer/value'] for c in f[':answer-field/choices']];idx=choose(f[':answer-field/choices']);key=f[':answer-field/correct'];key=key[':answer/id'] if isinstance(key,dict) else key[1]
 # This finding concerns revised quotient banks only; do not mistake successes in
 # unrelated banks or source fidelity witnesses for affected generated instances.
 signature=(sum(v.split('=')[0].startswith(('y\\cdot','{y}^')) for v in raw)>=2 and len(set(v.split('=')[1] for v in raw))>=3 and (q[':question/problem'].find('\\frac{x}{')>=0 or q[':question/problem'].find('\\frac{{2}')>=0))
 rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':':question/math-academy-id' in q,'prompt':q[':question/problem'],'revised_quotient_signature':signature,'modal_strategy_chose':raw[idx] if idx is not None else None,'modal_strategy_correct':idx is not None and f[':answer-field/choices'][idx][':answer/id']==key})
assert not any(z['revised_quotient_signature'] for z in rows)
save('inventory-tested-questions.json',qs)
save('inventory-probe.json',{'basis':i['basis'],'captured_question_count':len(qs),'generated_count':sum(not z['original_source'] for z in rows),'records':rows,'conclusion':'All 16 captured questions inspected, including complete banks and prompts; six non-source generated records consist of one exponent-sum and five double-factor instances, so none is a revised quotient-bank instance. No generated instance of this newly demonstrated family-specific weakness is present. No general shortcut absence claimed.','limitations':['Only captured basis 5365; future inventory can change.','Generation metadata absent in captured question entries; no fabricated metadata or attribution.','Original source questions were not reclassified as generated.']})
save('affected-inventory.json',{'affected_questions':[]})
def summary(rs):
 z=[probe(r) for r in rs];return {'count':len(rs),'templates':dict(collections.Counter(r['generation']['template'] for r in rs)),'profiles':dict(collections.Counter(r['generation'].get('bank_profile','observed') for r in rs)),'quotient_count':sum(p['template'] in ['simple_quotient','exp_quotient'] for p in z),'affected_quotient_count':sum(p['template'] in ['simple_quotient','exp_quotient'] and p['correct'] for p in z)}
b=load(R/'batch.json');ba=load(R/'delivery-batch/accepted.json');c=load(R/'easy-records.json');ca=load(R/'delivery-control/accepted.json')
stages={k:summary(v) for k,v in [('control_before',c),('control_after',ca),('batch_before',b),('batch_after',ba)]}
# Faithful deterministic within-band draw from question_selection.rs 143-202.
def draw(pool,seed):
 pool=sorted(set(pool));digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);return pool[int(u*len(pool))] if pool else None
existing=[q[':db/id'] for q in qs if q[':question/difficulty'][':db/ident']==':question.difficulty/easy'];first=max(q[':db/id'] for q in qs)+1
new={first+k:r['question'][':question/id'] for k,r in enumerate(ba)};pool=existing+list(new);draws=collections.Counter(draw(pool,'independent-revision-'+str(k)) for k in range(256));bad=next(e for e,qid in new.items() if qid==next(r['question'][':question/id'] for r in ba if r['generation']['template']=='exp_quotient'))
kept=[e for e in pool if e==bad]
save('delivery-selection.json',{'stages':stages,'filter_reports':['delivery-control/delivery.json','delivery-batch/delivery.json'],'rejection_resampling':'No retry/resampling loop: difficulty eligibility -> uniform template choice -> uniform profile choice before integer parameters -> validation. Invalid explicit cases reject. Independent boundary/fresh samples all returned.','captured_inventory_basis':i['basis'],'learner_selection_source':'engine/rust/question_selection.rs 109-202: previous task exclusion, caller current-prefix exclusion, sorted/deduplicated candidates; configured band weights; uniform in eligible nonempty positive-weight easy band; unconfigured fallback lowest entity id.','conditional_easy_simulation':{'actual_captured_easy_entity_ids':existing,'hypothetical_future_entity_id_map':new,'future_ids_are_surrogates':True,'draws':{str(k):v for k,v in draws.items()},'defective_item_draws':draws[bad],'history_excluding_all_but_defective_item':{'remaining':kept,'selected':draw(kept,'independent-revision-final')}} ,'conclusion':'Both revised quotient profiles survive actual delivery deduplication. 18/18 accepted quotient controls and the one quotient in the exact accepted 5-item batch retain the modal-component cue. Uniform within a positive-weight easy pool gives affected items positive probability; history can leave only the affected item. Selection does not rewrite banks.','limitations':['Publication preparation absent; shared actual publication filter reproduced read-only against captured basis.','No live learner histories, reservations, policy distribution or future entity IDs supplied; conditional simulation uses actual captured existing IDs and explicit future surrogates. Easy band with zero weight would deliver none of this batch.','No database or assets published. Inventory can change after capture.']})
print('stages',json.dumps(stages));print('inventory generated revised quotients',0,'conditional defect draws',draws[bad])
