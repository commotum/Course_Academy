from independent import *
import math
load=lambda n:json.load(open(ROOT/n))
old=JOB/'review-1-policy-2-22438d1e0e264086'
shutil.copy2(old/'reused/independent-samples.json',ROOT/'reused/independent-samples.json')
shutil.copy2(old/'reused/scope-results.json',ROOT/'reused/scope-results.json')
fresh=load('delivery-independent/accepted.json');batch=load('delivery-batch/accepted.json');ret=load('delivery-retained/accepted.json');prior=load('reused/independent-samples.json')
assert len(fresh)==32 and len(batch)==len(ret)==5
probes=[]
def add(cue,sub,scope,strategy,wins,total,base,conclusion,refs,disposition='not_predictive'):
 probes.append(dict(cue=cue,subgroup=sub,scope=scope,strategy=strategy,correct=wins,total=total,baseline=base,disposition=disposition,conclusion=conclusion,sample_refs=refs))
def candidates(r,kind):
 return [i for i,v in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if (o:=op(v[':answer/value']))[0]==kind and (kind=='swap' or sum(c!=0 for c in o[2])==2)]
for name,rs,ref in [('fresh post-delivery',fresh,'delivery-independent/accepted.json'),('exact current batch',batch,'delivery-batch/accepted.json'),('retained proposal stream repaired',ret,'delivery-retained/accepted.json')]:
 pos,n=collections.Counter(analyze(r)['position'] for r in rs).most_common(1)[0]
 add('stored answer position',name,'overall',f'Always select position {pos}',n,len(rs),.2,'Five-way uniform guessing is 0.2; post-hoc best fixed position does not solve this pool.',[ref])
 for sign in [-1,1]:
  wins=0
  for r in rs:
   vs=r['question'][':question/answer-fields'][0][':answer-field/choices']; guesses=[]
   for i in candidates(r,'linear'):
    o=op(vs[i][':answer/value'])
    if any(k!=o[1] and c*sign>0 for k,c in enumerate(o[2])):guesses.append(i)
   guess=guesses[0] if guesses else 0;wins+=guess==analyze(r)['position']
  add('coefficient sign',name,'overall',f'Choose first distinct-row addition with sign {sign}, else first choice',wins,len(rs),.2,'Five-way random baseline; sign alone does not determine cancellation. Choosing a matching coefficient from actual entries is the intended skill.',[ref])
# Conditional probes independently distinguish all recognizable source banks.
for sid in sorted({r['generation']['bank_profile'] for r in fresh}):
 rs=[r for r in fresh if r['generation']['bank_profile']==sid]
 assert {'linear','swap'}=={analyze(r)['kind'] for r in rs}
 for kind in ['linear','swap']:
  wins=sum(bool(candidates(r,kind)) and candidates(r,kind)[0]==analyze(r)['position'] for r in rs)
  add('operation shape',sid,'within_template',f'Always choose first visible {kind} candidate without reading matrix/target',wins,len(rs),.2,'Five-way baseline 0.2. Each profile contains both successful addition and swap decisions, refuting a fixed operation-shape rule. This sample is a scheduler regression, not an exhaustive search of all coefficients.', ['fresh-samples.json','delivery-independent/accepted.json','scheduler-results.json'])
# Earlier unchanged arithmetic rules supply complete eligible-slot coverage.
groups=collections.defaultdict(list)
for r in prior+load('reused/fresh-samples.json'):groups[r['generation']['bank_profile']].append(r)
for sid,rs in groups.items():
 counts=collections.Counter(r['generation']['parameters']['winner'] for r in rs);w,n=counts.most_common(1)[0]
 add('recognizable bank and coefficient/donor role',sid,'within_template',f'Always choose original source operation slot {w}, locating its expression after row relabeling',n,len(rs),1/len(counts),'Comparison baseline is uniform over observed eligible roles. No role is universally correct. These prior independent samples are reused because source_data and generate() are unchanged, with current equality controls in unchanged-control-results.json.', ['reused/independent-samples.json','reused/fresh-samples.json','revision-diff.json','unchanged-control-results.json'])
for name,rs,ref in [('current exact batch',batch,'delivery-batch/accepted.json'),('repaired retained stream',ret,'delivery-retained/accepted.json'),('fresh controls',fresh,'delivery-independent/accepted.json')]:
 group=[r for r in rs if r['generation']['bank_profile']=='q-72858'];assert len(group)>=2
 assert all(len(candidates(r,'linear'))==1 for r in group)
 wins=sum(candidates(r,'linear')[0]==analyze(r)['position'] for r in group)
 assert 0<wins<len(group)
 add('two swaps, two self-scalings and one subtraction',name+' q-72858','within_template','Choose the sole distinct-row subtraction, ignoring matrix and target',wins,len(group),.5,'Comparison baseline 0.5 chooses between the two eligible operation roles. The exact current and retained proposal groups both contain a swap counterexample, so the previous 2/2 shortcut is defeated.',[ref])
# Actual UI hashed choice order, not only storage order.
ui=[]
for i,r in enumerate(load('render-records.json')):
 html=(ROOT/f'render/question-{i+1:03}.html').read_text();ids=re.findall(r'<input\b[^>]*type="radio"[^>]*value="([^"]+)"',html)
 key=r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
 assert len(ids)==5 and key in ids
 ui.append({'index':i,'id':r['question'][':question/id'],'position':ids.index(key),'answer_ids':ids})
save('ui-order-results.json',ui)
pos,n=collections.Counter(r['position'] for r in ui[:5]).most_common(1)[0]
add('actual UI answer position','current exact batch','overall',f'Always choose displayed position {pos}',n,5,.2,'Baseline is 0.2 among five; actual UI reordering has counterexamples to the best constant position.',['render-records.json','ui-order-results.json'])
save('shortcut-results.json',{'probes':probes,'batch_profile_counts':dict(collections.Counter(r['generation']['bank_profile'] for r in batch)),'stage_counts':{'fresh_raw':32,'fresh_delivered':32,'exact_batch_raw':5,'exact_batch_delivered':5,'prior_stream_raw':5,'prior_stream_delivered':5}})
# Read-only deterministic learner selection reproduction against captured usable
# hard pool, with explicit hypothetical future IDs/ranks and policy assumptions.
inv=json.load(open(JOB/'source/inventory.json'));qs=inv['questions'];src=json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions'];source_ids={q[':question/id'] for q in src}
usable=[q for q in qs if q.get(':question/worked-solution') and all(f.get(':answer-field/correct') for f in q.get(':question/answer-fields',[])) and not q.get(':question/retired',False)]
pool=sorted(q[':db/id'] for q in usable if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/hard')
def pick(ids,seed):
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 return ids[math.floor(u*len(ids))] if ids else None
sim=[]
for seen in [set(),set(pool[:5])]:
 ids=[x for x in pool if x not in seen]
 sim.append({'pool':'captured usable hard inventory','seen':sorted(seen),'candidate_ids':ids,'draw_counts':dict(collections.Counter(pick(ids,f'independent-select-{i}') for i in range(512)))})
draws=[pick(list(range(5)),f'independent-delivered-{i}') for i in range(512)]
roles=collections.Counter(analyze(batch[i])['kind'] for i in draws if batch[i]['generation']['bank_profile']=='q-72858')
assert set(roles)=={'swap','linear'}
sim.append({'pool':'hypothetical appended current batch; entity ID ranks 0..4 in record order','draw_counts':dict(collections.Counter(draws)),'q72858_roles':dict(roles)})
# Combined captured pool plus appended IDs with preserved proposed record order.
future_ids=list(range(max(pool)+1,max(pool)+6));combined=pool+future_ids
for seen in [set(),set(pool)]:
 ids=[x for x in combined if x not in seen];counts=collections.Counter(pick(ids,f'independent-combined-{i}') for i in range(512))
 rr=collections.Counter(analyze(batch[future_ids.index(q)])['kind'] for q,n in counts.items() if q in future_ids and batch[future_ids.index(q)]['generation']['bank_profile']=='q-72858' for _ in range(n))
 assert set(rr)=={'swap','linear'}
 sim.append({'pool':'captured plus hypothetical appended current batch','seen':sorted(seen),'future_ids':future_ids,'draw_counts':dict(counts),'new_q72858_roles':dict(rr)})
save('selection-results.json',{'basis':inv['basis'],'inventory_count':len(qs),'usable_count':len(usable),'rules':'learning.rs excludes seen, invalid and retired. question_selection.rs sorts/dedupes IDs; positive hard weight with all hard candidates uses SHA256 bytes 8..16 uniform draw. No weights chooses smallest ID; zero hard weight excludes hard with no unrated fallback here.','simulations':sim,'seed_ranges':['independent-select-{i}','independent-delivered-{i}','independent-combined-{i}'],'range':'i=0..511','limits':['Live policy, learner history, future entity IDs and later inventory are unavailable; all simulations explicitly conditional.','Non-adversarial histories can leave any finite pool with one decision after others have been seen; no claim of universal balanced user histories.','Actual publication absent; check_delivery reproduced applicable normalization/deduplication read-only.']})
extras=[q for q in qs if q[':question/id'] not in source_ids];review=[]
for q in extras:
 ops=[op(v[':answer/value']) for v in q[':question/answer-fields'][0][':answer-field/choices']]
 sig=sum(o[0]=='swap' for o in ops)==2 and sum(o[0]=='linear' and sum(c!=0 for c in o[2])==1 for o in ops)==2
 review.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'q72858_cue_signature':sig,'generation_metadata_present':bool(q.get('generation'))})
assert not any(x['q72858_cue_signature'] for x in review)
save('inventory-records.json',extras)
save('inventory-review.json',{'basis':inv['basis'],'source_count':len(source_ids),'non_source_checks':review,'conclusion':'All five non-source inventory records inspected: none has the demonstrated q-72858 bank-shape weakness. Verified absence of that retained finding in captured non-source inventory, not an assertion that all unrelated weaknesses were retested. Original source q-72858 is not classified as generated.','provenance_gap':'Captured non-source records have no generation metadata; no invented generation provenance or affected-record claim.'})
save('affected-inventory.json',{'affected_questions':[]})
# Actual UI and native outcomes explicitly bind counterfactuals.
grade=load('grader-results.json');assert grade['accepted_checks']==58 and grade['rejected_checks']==232 and grade['documented_unresolved_checks']==0
cf=load('counterfactual-results.json');cf.update({'native_grading':'All five choices in each controlled record tested; correct switches/preservation match independent arithmetic.','actual_UI':'render questions 006-010 show all controlled prompts, choices and updated solution matrices.','status':'passed'});save('counterfactual-results.json',cf)
save('render-inspection.json',{'renderer_passed':load('render/rendering.json')['passed'],'cases':11,'screenshots_inspected':['render/contact-sheet.jpg','render/question-004.png','render/question-010.png','render/question-011.png'],'observations':'All five exact delivered questions plus three matrix-change counterfactuals, identical-matrix target-only pair and fractional source replay display legible matrix entries, indices, radio options and full solution matrices. Swap explanations cite correct donor/target, and fractions render properly.','limits':'Finite representative review; no assets used.'})
save('scope-results.json',{'fixed_skill':'one elementary operation zeroing one 3x3 integer-matrix entry; five radio choices','supported_successful_swaps':'canonical e-4696 explicitly explains swap succeeds iff donor has target-column zero; tutorial defines swaps. It does not add operators or reasoning stages.','current_variations':'Zero target, distinct-row replacements, signed coefficients, simple fractions, nonzero self-scalings as distractors, row/column permutations and eligible swaps. Same intended workload.','incomplete_source':'q-20392 inferred replay-only; no invented original key/solution claimed.','boundaries':'Prior generate() and source_data unchanged; current equality controls and source replays rechecked.','evidence':'source-analysis.json; reused/scope-results.json; revision.diff; counterfactual-records.json'})
ped={'learner_operation':load('source-analysis.json')['learner_operation'],'fixed_features':load('source-analysis.json')['fixed_features'],
'answer_roles':[{'role':'Target coordinate','eligible_variation':'All nine coordinates and target-only change with displayed matrix/bank fixed','observed':'Prior all-nine coverage reused with unchanged generate; current target-only pair switches subtraction to swap.'},{'role':'Successful operation','eligible_variation':'All eligible listed replacements and swaps, with decisive entries rather than fixed operation shape determining correctness','observed':'Both operation kinds survive fresh scheduler and delivery in ten banks; exact repeated q-72858 subgroup 1 subtraction and 1 swap.'},{'role':'Correct position','eligible_variation':'Stored order and actual UI hashing','observed':'No perfect constant position in fresh/current/retained pools; actual UI order inspected.'}],
'coverage':[{'case':sid,'sample_refs':['fresh-samples.json','delivery-independent/accepted.json','scheduler-results.json'],'result':str(dict(collections.Counter(analyze(r)['kind'] for r in fresh if r['generation']['bank_profile']==sid)))} for sid in sorted(g.CASES)]+[{'case':'exact five-item runner batch','sample_refs':['runner-batch.json','delivery-batch/accepted.json','shortcut-results.json'],'result':'All five survive; repeated q-72858 has both decisions; sole subtraction cue 1/2.'},{'case':'unchanged complete source/eligible-slot domain','sample_refs':['source-replays.json','source-replay-results.json','reused/independent-samples.json','reused/fresh-samples.json','revision-diff.json'],'result':'All eleven banks replay, including q-72858; prior independently tested winning-slot and nine-target coverage reused only for unchanged generate/source rules.'}],
'counterfactuals':[{'kind':'relevant','change':'q-72858 a13:3->4 and a33:3->0; target a23 and other columns/bank fixed.','expected':'Subtraction becomes incorrect and target-row/third-row swap becomes unique correct.','observed':'Visible prompts, explanations and resulting matrices update; native grader accepts the new swap and rejects old subtraction. Actual UI cases 006-007 show the change.','status':'passed','justification':'Canonical e-4696 makes swap eligibility depend on zero donor and replacement on cancellation.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-records.json']},{'kind':'relevant','change':'Only target a21->a23 with identical displayed matrix and full answer bank.','expected':'Unique correct subtraction switches to target-row/third-row swap.','observed':'Native outcomes, displayed target, choice key and full worked row outcome all follow the target; actual UI cases 009-010.','status':'passed','justification':'Source questions ask about the specified entry, not an arbitrary zero elsewhere.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-records.json']},{'kind':'irrelevant','change':'Change a11:2->-9 and a12:1->8, leaving target-column values fixed.','expected':'Correct subtraction and learner grading preserved; other columns of worked matrix update.','observed':'Unique response unchanged with proper full-row arithmetic; native correct/wrong outcomes preserved, actual UI cases 006/008.','status':'passed','justification':'Only the target-column entries determine target cancellation; whole row still changes under the source operation.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-records.json']}],
'shortcut_probes':probes,
'delivery':{'stages_examined':['winner selection and uniqueness rejection/resampling','batch winner-kind scheduling and semantic deduplication','requested hard difficulty filtering','actual publication normalization/validation and captured inventory deduplication','seen/usability/retirement gates','conditional weighted learner selection','actual UI answer order'],'sample_refs':['scheduler-results.json','rejection-results.json','coverage.json','delivery-batch/delivery.json','delivery-independent/delivery.json','delivery-retained/delivery.json','selection-results.json','ui-order-results.json'],'result':'32/32 independent controls, 5/5 current batch and 5/5 repaired retained proposals survive. Both decision cases retained per repeated control bank; exact repeated q-72858 also retains subtraction and swap. Positive-hard-weight conditional selections reach both roles; history/policy limits explicit.'},
'limitations':['Finite audit cannot exclude every possible shortcut.','q-20392 lacks original solution/key/difficulty and is only an explicitly inferred replay.','No live publication exists; read-only filtering uses captured basis 5360. Later inventory may change deduplication.','Learner history/policy and future IDs unavailable; selection statements use explicit conditional scenarios.','The prior finite-batch defect is resolved on this exact batch; no guarantee that every arbitrary pool/history has balanced cases.']}
save('pedagogical-variation.json',ped)
for s in ['coverage','counterfactuals','shortcut_probes']:
 for v in ped[s]:
  for p in v['sample_refs']:assert (ROOT/p).is_file() and (ROOT/p).stat().st_size and not Path(p).is_absolute()
for p in ped['delivery']['sample_refs']:assert (ROOT/p).is_file() and (ROOT/p).stat().st_size
save('decision-validation.json',{'all_relative_refs_nonempty':True,'conditional_probes':sum(p['scope']!='overall' for p in probes),'fresh_roles_per_bank':'both swap and linear in all ten','exact_q72858_shortcut':'1/2','result':'passed; schema validation pending'})
(ROOT/'session-state.md').write_text('Completed source/math/scheduler/delivery/native grading (58 accepted,232 rejected), eleven actual-UI renders and screenshot inspection, controlled dependencies, conditional shortcuts, captured inventory and learner-selection simulations. Both prior defects resolved. All evidence under evidence_root; final contract/package immutability checks pending.\n')
print(json.dumps({'probes':len(probes),'conditional_probes':sum(p['scope']!='overall' for p in probes),'native_checks':290,'inventory_extras':len(extras),'current_q72858':dict(collections.Counter(analyze(r)['kind'] for r in batch if r['generation']['bank_profile']=='q-72858'))}))
