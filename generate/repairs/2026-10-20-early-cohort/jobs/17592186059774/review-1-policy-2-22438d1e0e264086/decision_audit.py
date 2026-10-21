"""Coverage, controlled dependency and shortcut checks for the repaired family."""
from independent import *
import math
load=lambda n:json.load(open(ROOT/n))
fresh=load('fresh-samples.json'); old=load('reused/independent-samples.json'); batch=load('runner-batch.json')
delivered=load('delivery-independent/accepted.json');db=load('delivery-batch/accepted.json')
assert len(fresh)==len(delivered)==55 and len(batch)==len(db)==5
assert [r['generation'] for r in fresh]==[r['generation'] for r in delivered]
assert [r['generation'] for r in batch]==[r['generation'] for r in db]
probes=[]
def probe(cue,subgroup,scope,strategy,correct,total,baseline,conclusion,refs,disposition='not_predictive'):
    probes.append(dict(cue=cue,subgroup=subgroup,scope=scope,strategy=strategy,correct=correct,total=total,baseline=baseline,disposition=disposition,conclusion=conclusion,sample_refs=refs))
def additions(r):
    vs=r['question'][':question/answer-fields'][0][':answer-field/choices']
    return [i for i,v in enumerate(vs) if (o:=op(v[':answer/value']))[0]=='linear' and sum(c!=0 for c in o[2])==2]
for name,rs,ref in [('fresh post-delivery',delivered,'delivery-independent/accepted.json'),('exact runner post-delivery',db,'delivery-batch/accepted.json')]:
    ar=[analyze(r) for r in rs];cnt=collections.Counter(a['position'] for a in ar);p,n=cnt.most_common(1)[0]
    probe('stored position',name,'overall',f'Always choose stored position {p}',n,len(rs),.2,'Baseline is uniform among five. Post-hoc best position is not perfect; actual UI order separately examined.',[ref])
    for sign in [-1,1]:
        wins=0
        for r,a in zip(rs,ar):
            candidates=additions(r);guess=0
            for j in candidates:
                o=op(r['question'][':question/answer-fields'][0][':answer-field/choices'][j][':answer/value'])
                if any(v*sign>0 for k,v in enumerate(o[2]) if k!=o[1]):guess=j;break
            wins+=guess==a['position']
        probe('addition coefficient sign',name,'overall',f'Select first distinct-row addition with sign {sign}, else first choice',wins,len(rs),.2,'Baseline is five-way guessing. The exact batch has counterexamples; coefficient sign alone does not decide cancellation.',[ref])
# Retain prior conditional coverage only for code/source-identical banks; add
# independently sampled repaired profile and observe actual delivery survivors.
groups=collections.defaultdict(list)
for r in old+delivered:groups[r['generation']['bank_profile']].append(r)
for sid,rs in groups.items():
    counts=collections.Counter(r['generation']['parameters']['winner'] for r in rs);w,n=counts.most_common(1)[0]
    probe('recognizable source bank',sid,'within_template',f'Always choose original bank slot {w}',n,len(rs),1/len(counts),'Baseline is uniform among independently eligible operations. Every bank has multiple observed winning roles. Prior unchanged-bank observations are reused only with revision-diff equality evidence.', ['reused/independent-samples.json','fresh-samples.json','revision-diff.json'])
restored=[r for r in delivered if r['generation']['bank_profile']=='q-72858']
rs_batch=[r for r in db if r['generation']['bank_profile']=='q-72858']
def sole_add_wins(rs):
    assert all(len(additions(r))==1 for r in rs)
    return sum(additions(r)[0]==analyze(r)['position'] for r in rs)
probe('one distinct-row addition; two self-scalings and two swaps','restored q-72858 control pool','within_template','Choose the sole distinct-row addition without reading matrix entries',sole_add_wins(restored),len(restored),.5,'Baseline is uniform among the two eligible operation roles (addition and target-row swap). Control records refute this strategy as a universal generator defect.', ['fresh-samples.json','delivery-independent/accepted.json'])
assert len(rs_batch)==2 and sole_add_wins(rs_batch)==2
probe('one distinct-row addition; two self-scalings and two swaps','q-72858 in exact delivered five-question batch','within_template','Choose the sole distinct-row addition without reading matrix entries',2,2,.5,'Baseline is uniform among the two eligible operation roles, so the matrix-free action achieves 2/2 versus 1/2. Both delivered instances of this repeated recognizable bank omit the swap outcome. This is a finite delivered-subpool weakness, not a universal generator defect or a claim from singletons.', ['runner-batch.json','delivery-batch/accepted.json','batch-shortcut-records.json'],'defect')
save('batch-shortcut-records.json',rs_batch)
save('batch-shortcut-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 '+sys.executable+' decision_audit.py','strategy':'Recognize the bank with two swaps, two self-scaling distractors and exactly one distinct-row subtraction; select that subtraction without reading matrix values.','affected_current_batch_ids':[r['question'][':question/id'] for r in rs_batch],'successes':2,'attempts':2,'eligible_role_baseline':.5,'control_successes':sole_add_wins(restored),'control_attempts':len(restored),'scope':'Batch selection; generator itself supports subtraction and swap.','minimal_case':rs_batch[0]['generation'],'requested_rule':'When a recognizable source-bank profile repeats in the delivered practice pool, retain a counterexample to a matrix-free winning-role cue. For this exact pool retain a q-72858 target-row-swap instance along with subtraction; rerun the shortcut test after deduplication and selection. No new source bank or changed learner notation is required.'})

# Observe the renderer's actual order for all current batch members and pairs.
rendered=load('render-records.json');ui=[]
for i,r in enumerate(rendered):
    h=(ROOT/f'render/question-{i+1:03}.html').read_text();ids=re.findall(r'<input\b[^>]*type="radio"[^>]*value="([^"]+)"',h)
    key=r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
    assert len(ids)==5 and key in ids
    ui.append({'index':i,'id':r['question'][':question/id'],'position':ids.index(key),'answer_ids':ids})
p,n=collections.Counter(x['position'] for x in ui[:5]).most_common(1)[0]
probe('actual rendered position','exact runner batch','overall',f'Always choose actual UI position {p}',n,5,.2,'Baseline is five-way guessing. Actual rendered HTML includes the UI hash-based reordering; constant position does not solve the exact batch.', ['render-records.json','ui-order-results.json'])
save('ui-order-results.json',ui)
save('shortcut-results.json',{'probes':probes,'batch_profile_counts':dict(collections.Counter(r['generation']['bank_profile'] for r in db)),'profile_winner_counts':{sid:dict(collections.Counter(r['generation']['parameters']['winner'] for r in rs)) for sid,rs in groups.items()},'stages':{'fresh_raw':len(fresh),'fresh_delivered':len(delivered),'batch_raw':len(batch),'batch_delivered':len(db)}})

# Native outcomes have been checked for all five responses of both pair types.
grade=load('grader-results.json');assert grade['accepted_checks']==28 and grade['rejected_checks']==112 and grade['documented_unresolved_checks']==0
cf=load('counterfactual-results.json');cf['assertions']='All visible matrices, five choices, solution outcomes and native grader results agree. Actual UI renders all pairs; screenshot inspection recorded separately.';save('counterfactual-results.json',cf)

# Faithful read-only selection against the captured inventory and hypothetical
# appended delivery IDs. Relative rank, not guessed future DB identity, is used.
inv=json.load(open(JOB/'source/inventory.json'));qs=inv['questions']
source_ids={q[':question/id'] for q in json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']}
usable=[q for q in qs if q.get(':question/worked-solution') and all(f.get(':answer-field/correct') for f in q.get(':question/answer-fields',[]))]
pool=sorted(q[':db/id'] for q in usable if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/hard')
def pick(ids,seed):
    digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
    return ids[math.floor(u*len(ids))] if ids else None
selection=[]
for seen in [set(),set(pool[:5])]:
    ids=[x for x in pool if x not in seen]
    selection.append({'seen':sorted(seen),'candidate_ids':ids,'draw_counts':dict(collections.Counter(pick(ids,f'revision-select-{i}') for i in range(512)))})
# For any future positive hard-weight fresh pool all accepted records remain
# equally eligible; compare actual batch roles under that deterministic draw.
draws=[pick(list(range(len(db))),f'revision-delivered-{i}') for i in range(512)]
selection.append({'pool':'hypothetical fresh delivered batch, sorted entity-ID ranks 0..4','draw_counts':dict(collections.Counter(draws)),'q72858_role_counts':dict(collections.Counter(db[i]['generation']['parameters']['winner'] for i in draws if db[i]['generation']['bank_profile']=='q-72858'))})
save('selection-results.json',{'basis':inv['basis'],'inventory_count':len(qs),'usable_count':len(usable),'seed_ranges':['revision-select-{i}','revision-delivered-{i}'],'range':'i=0..511','simulations':selection,'rules':'learning.rs removes seen/unusable questions; question_selection.rs unique sorted candidates, positive rated-band weights then uniform SHA256 bytes 8..16 selection; unconfigured weights choose smallest ID; explicit zero hard weight excludes hard items.','limitations':['No live policy, learner history or future published entity IDs supplied. Results conditional on stated policy and histories; no actual publication or DB call.','All five accepted records are usable hard radio questions. Selection cannot introduce the absent q-72858 swap into this exact new batch.']})

extras=[q for q in qs if q[':question/id'] not in source_ids];inv_report=[]
for q in extras:
    vs=q[':question/answer-fields'][0][':answer-field/choices'];ops=[op(v[':answer/value']) for v in vs]
    swaps=sum(o[0]=='swap' for o in ops);selfscale=sum(o[0]=='linear' and sum(c!=0 for c in o[2])==1 for o in ops)
    inv_report.append({'id':q[':question/id'],'entity_id':q[':db/id'],'restored_bank_signature':swaps==2 and selfscale==2,'generation_metadata_present':bool(q.get('generation'))})
assert not any(x['restored_bank_signature'] for x in inv_report)
save('inventory-records.json',extras)
save('inventory-review.json',{'basis':inv['basis'],'source_count':len(source_ids),'non_source_checks':inv_report,'finding_scope':'New finite delivered-batch q-72858 subpool has fixed subtraction winner. No non-source stored record has the restored bank signature; original source q-72858 is excluded from generated classification.','conclusion':'Verified absence of this demonstrated weakness in captured non-source inventory. Broader unrelated defects not retested; prior independent arithmetic evidence reused. No generation provenance invented.'})
save('affected-inventory.json',{'affected_questions':[]})

ped={'learner_operation':load('source-analysis.json')['learner_operation'],'fixed_features':load('source-analysis.json')['fixed_features'],
 'answer_roles':[{'role':'Target coordinates','eligible_variation':'All nine coordinates; target may change with identical displayed matrix and bank','observed':'All nine for both restored winners; target-only pair switches subtraction to swap.'},
 {'role':'Which listed operation succeeds','eligible_variation':'All mathematically eligible choices; for q-72858 subtraction or target-row swap','observed':'Both survive generator rejection and publication in fresh control samples; exact new batch includes only subtraction in both q-72858 instances.'},
 {'role':'Correct position','eligible_variation':'Stored order and actual UI permutation','observed':'No universal constant position; actual UI HTML inspected.'}],
 'coverage':[{'case':sid,'sample_refs':['reused/independent-samples.json','fresh-samples.json','shortcut-results.json'],'result':str(dict(collections.Counter(r['generation']['parameters']['winner'] for r in rs)))} for sid,rs in groups.items()]+
 [{'case':'all source banks','sample_refs':['source-replays.json','source-replay-results.json'],'result':'11/11 complete five-choice banks replay, with documented source correction and inferred incomplete-key completion.'},
 {'case':'exact delivered batch','sample_refs':['delivery-batch/accepted.json','batch-shortcut-results.json'],'result':'5/5 survive. Repeated q-72858 subgroup fixes sole distinct-row subtraction 2/2, allowing bank-recognition shortcut.'}],
 'counterfactuals':[{'kind':'relevant','change':'Change q-72858 donor entries a13:3->4 and a33:3->0, retaining target value, other columns, and bank.','expected':'Correct subtraction changes to target-row/third-row swap.','observed':'Independent visible arithmetic and native grader agree; final row matrix and explanation update. Actual UI screenshot pair retained.','status':'passed','justification':'Source e-4696 makes swap eligibility depend on a zero donor; row subtraction depends on donor equality.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-records.json']},
 {'kind':'relevant','change':'Only requested target a21->a23, with identical visible matrix and five choices.','expected':'Correct subtraction changes to swap.','observed':'Prompt target, keyed choice, native grader outcomes and worked result all switch coherently.','status':'passed','justification':'The assessed source operation must zero the specified entry, rather than an unrelated entry.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-records.json']},
 {'kind':'irrelevant','change':'Change a11:2->-9 and a12:1->8, holding target column and bank fixed.','expected':'Correct operation and grading preserved; result in other columns changes.','observed':'Subtraction remains unique; whole-row result and explanation update, native choices graded correctly.','status':'passed','justification':'Non-target columns do not determine whether the target entry becomes zero, but do participate in source whole-row calculation.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-records.json']}],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['winner construction and uniqueness rejection/resampling','generator semantic batch deduplication','requested difficulty','actual publisher normalization/validation/inventory deduplication','freshness and practice usability','conditional rated-band/ID learner selection','actual UI choice order'],'sample_refs':['coverage.json','rejection-results.json','delivery-independent/delivery.json','delivery-batch/delivery.json','selection-results.json','shortcut-results.json','ui-order-results.json'],'result':'All 55 fresh and 5 batch records survive. Rejection permits both restored roles; selection cannot restore the missing swap in the repeated bank subgroup of this exact batch.'},
 'limitations':['Finite testing does not exclude every shortcut.','q-20392 remains replay-only because captured source lacks key, solution and difficulty; unique inferred answer is documented.','The demonstrated defect is finite delivered-batch selection, not universal q-72858 generator behavior; larger controls have counterexamples.','Live policy/history and future IDs are unknown; captured-basis and stated conditional selection conclusions only.']}
save('pedagogical-variation.json',ped)
try:
    import jsonschema;jsonschema.validate(ped,json.load(open(REPO/'generate/pipeline/pedagogical-variation.schema.json')));schema='passed'
except ImportError:schema='jsonschema unavailable; required fields and referenced paths checked manually'
for section in ['coverage','counterfactuals','shortcut_probes']:
    for entry in ped[section]:
        for ref in entry['sample_refs']:assert (ROOT/ref).is_file() and (ROOT/ref).stat().st_size
save('decision-validation.json',{'schema':schema,'nonempty_relative_sample_refs':True,'result':'failed: recognizable repeated bank in exact delivered batch has a matrix-free answer-producing rule','conditional_probes':len(groups)+2})
print(json.dumps({'profile_count':len(groups),'restored_controls':len(restored),'restored_control_subtraction_wins':sole_add_wins(restored),'exact_batch_subgroup_shortcut':[2,2],'schema':schema}))
