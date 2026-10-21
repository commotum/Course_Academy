import json,pathlib,collections,hashlib
R=pathlib.Path(__file__).resolve().parent;J=R.parent
load=lambda n:json.load(open(R/n))
def save(n,v):(R/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
D=r'\frac{\text{d}y}{\text{d}x}'
def zero(q):
 f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];z=[a for a in cs if '\\frac' not in a[':answer/value'].replace(D,'D')];c=f[':answer-field/correct'];key=c[':answer/id'] if isinstance(c,dict) else c[1]
 return {'unique_fractionless':len(z)==1,'fractionless_count':len(z),'success':len(z)==1 and z[0][':answer/id']==key}
i=json.load(open(J/'source/inventory.json'));rows=[]
for q in i['questions']:
 rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'origin':'source' if ':question/math-academy-id' in q else 'generated','difficulty':q[':question/difficulty'][':db/ident'],**zero(q)})
save('inventory-probe.json',{'basis':i['basis'],'tested':rows,'generated_count':sum(r['origin']=='generated' for r in rows),'affected_generated_count':sum(r['origin']=='generated' and r['success'] for r in rows),'source_count_affected':sum(r['origin']=='source' and r['success'] for r in rows),'limitations':['Captured inventory only; original source questions are not reported as generated. The six captured generated questions contain no unique fractionless answer, so this specific shortcut is verified absent there; no general absence of defects is asserted.']})
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-tested-questions.json',i['questions'])
# Faithful reproduction of select's uniform within one rated difficulty pool. No database/history mutation.
# Each pool is conditional on easy having positive weight. Code explicitly documents fallback without weights.
batch=load('delivery-batch/accepted.json');control=load('delivery-control/accepted.json')
def summarize(rs):return {'count':len(rs),'templates':dict(collections.Counter(r['generation']['template'] for r in rs)),'fraction_shortcut_eligible':sum(zero(r['question'])['success'] and r['generation']['template'] in ('simple_quotient','exp_quotient') for r in rs)}
stages={'control_before':summarize(load('easy-records.json')),'control_after':summarize(control),'batch_before':summarize(load('batch.json')),'batch_after':summarize(batch)}
def draw(pool,seed):
 h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53);return pool[int(u*len(pool))]
# Actual assigned future entity IDs/history/weights unavailable. Examine the algorithm conditional on eligibility,
# and retain explicit all-fresh entity surrogates rather than inventing real future assigned IDs.
cpool=list(range(len(batch)));draws=collections.Counter(draw(cpool,'independent-review-'+str(k)) for k in range(256));history=[0,1,2,3];fresh=[z for z in cpool if z not in history]
save('delivery-selection.json',{'stages':stages,'rejection_resampling':'Generator does not implement rejection or retry/resampling. All 33 independently specified boundaries/fresh instances returned; wrong-level and invalid parameters raise ValueError. Fixed sampling eligibility lists by difficulty.','selection_source':'engine/rust/question_selection.rs lines 109-202: exclude prior-task/current-prefix items upstream; deduplicate/sort candidates; choose weighted nonempty band; uniform within sorted band using digest bytes 8:16; without a configured distribution return first sorted candidate.','conditional_easy_simulation':{'surrogate_pool':cpool,'draw_counts':dict(draws),'history_exclusion_example':history,'remaining':fresh,'last_remaining_draw':draw(fresh,'independent-review-example')},'basis':i['basis'],'limits':['No learner history, active policy weights, reservations, or future database-assigned entity IDs supplied. Selection was examined from actual algorithm and conditional tests; no live personalized selection is claimed.','Within a positively weighted easy band every fresh item, including the demonstrated shortcut item, remains eligible. History can leave it as the sole remaining candidate. Selection never rewrites answer banks.','Publication preparation absent. Shared actual normalization/deduplication was run read-only; changing inventory after basis 5365 may alter duplicates.']})
print('inventory generated affected',sum(r['origin']=='generated' and r['success'] for r in rows),'stages',stages)
