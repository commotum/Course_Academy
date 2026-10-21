import json,re,hashlib
from pathlib import Path
from collections import Counter,defaultdict
root=Path(__file__).resolve().parent

def load(n):return json.load(open(root/n))
def save(n,x):(root/n).write_text(json.dumps(x,indent=2)+'\n')
def fields(r):return r.get('question',r)[':question/answer-fields']
def selected(r):
 result=[]
 for f in fields(r):
  c=f[':answer-field/correct'];aid=c.get(':answer/id') if isinstance(c,dict) else c[1]
  truth=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)=='true'
  label=re.search(r'\$([ABC])\s*=',f[':answer-field/key'])[1]
  if truth:result.append(label)
 return ''.join(sorted(result))
def stats(rs):
 return {'total':len(rs),'subsets':dict(Counter(selected(r) for r in rs)),'roles':{x:sum(x in selected(r) for r in rs) for x in 'ABC'},'by_template':{t:{'total':len(ss),'subsets':dict(Counter(selected(r) for r in ss))} for t in sorted({r['generation']['template'] for r in rs}) for ss in [[r for r in rs if r['generation']['template']==t]]}}
stages={n:stats(load(p)) for n,p in [('raw_before_nonempty','pre-policy-samples.json'),('normal_batch_after_rejection','normal-batch.json'),('profile_samples_before_delivery','independent-samples.json'),('profile_samples_after_delivery','delivery-independent/accepted.json'),('runner_before_delivery','runner-batch.json'),('runner_after_delivery','delivery-batch/accepted.json')]}
inv=json.load(open(root.parent/'source/inventory.json'));rated=[];unrated=[]
for q in inv['questions']:
 (rated if q.get(':question/difficulty') else unrated).append(q)
rated.sort(key=lambda q:q[':db/id'])
# Faithful positive-easy-band branch, source question_selection.rs 125–199.
# All rated candidates are easy; for ANY positive easy weight the effective
# band is easy, uniform hash choice. No policy/history state is fabricated.
selection=[]
for n in range(256):
 seed=f'independent-selection-8421-{n}';d=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53)
 q=rated[int(u*len(rated))];selection.append({'seed':seed,'entity_id':q[':db/id'],'question_id':q[':question/id'],'selected':selected(q)})
report={'command':'python3 delivery_analysis.py','stages':stages,'selection_rules':{'implementation':'engine/rust/question_selection.rs lines 105–199','captured_basis':inv['basis'],'candidate_count':len(inv['questions']),'rated_easy':len(rated),'unrated':len(unrated),'freshness':'Assume no previously seen questions; actual per-learner history absent. seen_before_task removes questions by entity ID only. Removing a candidate can change pool proportions, not that candidate key.','weighted_selection':'Configured positive easy weight gives uniform choice within the easy band. All rated candidates are easy. Unrated source is unused while easy has positive weight. Unconfigured policy returns lowest entity ID. Positive easy is a conditional scenario, not a claim about an unavailable learner policy.','published_batch':'No entity IDs assigned to new records read-only; therefore exact post-insertion seeded mapping cannot be computed. All five are easy; positive-easy weighted selection gives equal conditional probability among the five. Selection cannot introduce a C-unselected record into that five-member subset.','full_captured_pool_subsets':dict(Counter(selected(q) for q in rated)),'full_captured_pool_C_selected':sum('C' in selected(q) for q in rated),'full_captured_pool_total':len(rated),'unconfigured_first_entity':rated[0][':db/id']},'selection_simulation':selection,'limitations':['No database writes or inferred learner history. Captured basis 5356 may change.','Full source+stored pool does contain C-unselected questions; the demonstrated fixed-C cue is confined to the exact incoming five-record batch and the reconstructed five non-source stored records.','No live entity IDs or learner policy were available for new records; exact future seed-to-entity mapping is unavailable, but the within-easy distribution and invariant are independent of those IDs.']}
save('delivery-analysis.json',report)
# Complete generated inventory reproductions preserve normalized IDs; original
# generation seeds are not captured, so report explicit-parameter reconstruction.
generated=load('inventory-identity/accepted.json');stored={q[':question/id']:q for q in inv['questions']}
affected=[]
for r in generated:
 q=r['question'];s=stored[q[':question/id']]; assert selected(r)==selected(s)
 r['generation']['review_reproduction']={'method':'explicit stored matrix parameters; current generator; publisher normalization','original_seed':'not captured','stored_entity_id':s[':db/id'],'inventory_basis':inv['basis']}
 affected.append({'question_id':q[':question/id'],'entity_id':s[':db/id'],'finding':'Member of the five captured non-source records in which C is selected in every item (5/5). This is a finite-pool role shortcut, not a wrong individual key or a universal generator claim.','reproduction':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory_probe.py; then check_delivery.py --input inventory-reproduction-input.json --source ../source/source.json --inventory inventory-empty-for-identity-check.json --difficulty easy --output inventory-identity --math-root /media/jake/SSD/EDB/math; then python3 delivery_analysis.py','evidence_path':'generated-records.json'})
save('generated-records.json',generated);save('affected-inventory.json',{'affected_questions':affected})
# Probe candidates: field-level actions are distinguished from whole-item success.
probes=[]
def add(cue,subgroup,scope,strategy,correct,total,baseline,disposition,conclusion,refs):probes.append(dict(cue=cue,subgroup=subgroup,scope=scope,strategy=strategy,correct=correct,total=total,baseline=baseline,disposition=disposition,conclusion=conclusion,sample_refs=refs))
b=load('delivery-batch/accepted.json');large=load('delivery-independent/accepted.json')
add('label C','exact delivered runner batch','overall','Always select C; classify A and B separately.',sum('C' in selected(r) for r in b),len(b),4/7,'defect','Correctness counts one C field per item, not whole-question completion. Baseline 4/7 is the role-selected probability under independent fair validity flags conditioned on a nonempty selection. C gives 5/5 correct actions with no matrix inspection in this finite batch. A/B still require classification. Larger controls do not waive this batch weakness.',['runner-batch.json','delivery-batch/accepted.json','batch-role-results.json','grader-results.json'])
for template in ['select-echelon','select-not-echelon']:
 group=[r for r in b if r['generation']['template']==template]
 add('label C and visible prompt polarity',template+' in exact delivered runner batch','within_template','Always select C.',sum('C' in selected(r) for r in group),len(group),4/7,'defect','Baseline 4/7 as above. This conditional probe preserves the fixed-C field action within each visible polarity group; the one-item not-in group alone is not evidence of a general family defect.',['delivery-batch/accepted.json','batch-role-results.json'])
add('label C','independent post-delivery control','overall','Always select C.',sum('C' in selected(r) for r in large),len(large),4/7,'not_predictive','Baseline 4/7 as above. 180 counterexamples show this is not a universal generator shortcut.',['delivery-independent/accepted.json','control-role-results.json'])
for t in ['select-echelon','select-not-echelon']:
 group=[r for r in large if r['generation']['template']==t]
 add('label C plus polarity',t+' independent control','within_template','Always select C.',sum('C' in selected(r) for r in group),len(group),4/7,'not_predictive','Baseline 4/7 as above; control has selected and unselected C within this recognizable template.',['delivery-independent/accepted.json','sampling-results.json'])
for p in sorted({r['generation']['profile'] for r in large}):
 group=[r for r in large if r['generation']['profile']==p];hist=Counter(selected(r) for r in group);best,n=hist.most_common(1)[0]
 add('matrix dimensions and prompt identify source shape profile',p,'other_recognizable_subgroup','Choose the most frequent fixed subset '+best+' for this shape profile.',n,len(group),1/7,'not_predictive','Baseline 1/7 is uniform guessing among seven nonempty subsets. This retrospective best fixed-subset probe has counterexamples; all seven subsets occur. Same seeds were used across profiles, so these groups are not independent statistical trials.',['delivery-independent/accepted.json','sampling-results.json'])
add('label C','five reconstructed non-source stored records','other_recognizable_subgroup','Always select C within this finite captured generated subset.',5,5,4/7,'defect','Baseline 4/7 as above. This subset is identified by inventory provenance, not necessarily recognizable in the learner UI. It establishes affected stored-pool membership; it does not show the strategy solves every question in the full captured bank.',['generated-records.json','inventory-probe-results.json'])
save('shortcut-probes.json',probes)
print(json.dumps({'stage_summary':{k:{'total':v['total'],'C_selected':v['roles']['C']} for k,v in stages.items()},'inventory_affected':len(affected),'full_pool_C_selected':report['selection_rules']['full_captured_pool_C_selected'],'full_pool_total':len(rated),'probes':len(probes)},indent=2))
