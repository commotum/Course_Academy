"""Assemble the review from independently saved observations; no package writes."""
import json,pathlib,hashlib,collections,re
R=pathlib.Path(__file__).resolve().parent; B=R.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.load(open(R/p))
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n')

# Include the full restored-profile delivery coverage, in addition to raw/random/batch.
coverage=load('variation-coverage.json');shortcuts=load('shortcut-results.json')
exec((R/'variation_metrics.py').read_text().split('stages=')[0],globals())
rs=load('delivery-controlled/accepted.json');shortcuts['controlled_delivered']=metrics(rs)
coverage['controlled_delivered']={'count':len(rs),'profiles':dict(collections.Counter(r['generation']['source_profile'] for r in rs)),'roles':dict(collections.Counter(str(r['generation']['instance']['role']) for r in rs)),'masks':dict(collections.Counter(str(r['generation']['instance']['parameters']['mask']) for r in rs))}
save('shortcut-results.json',shortcuts);save('variation-coverage.json',coverage)

# Reconcile the exact actual-DOM order for the normalized batch and ID counterfactual.
ui=load('ui-order-results.json')
def dom_order(path):
    html=(R/path).read_text(); tags=re.findall(r'<input\b[^>]*type="radio"[^>]*>',html)
    return [re.search(r'value="([^"]+)"',s)[1] for s in tags]
for i,case in enumerate(ui['stages']['batch_delivered'],1):
    assert dom_order(f'render-delivered/question-{i:03}.html')==case['ordered_choice_ids']
probe=load('ui-id-probe.json');case=probe['records'][3]['cases'][0]
assert dom_order('render-id-counterfactual-2/question-001.html')==case['ordered_choice_ids']
assert case['correct_position']==2 and ui['stages']['batch_delivered'][3]['correct_position']==0
save('ui-dom-verification.json',{'passed':True,'normalized_batch_dom_matches':5,'id_counterfactual':{'same_record_index':3,'old_fixture_item_id':4,'new_fixture_item_id':1,'old_correct_position':0,'new_correct_position':2,'same_mathematical_answer':True},'limits':'Actual renderer and actual choiceOrder agree. Fixture IDs are not future database task-item IDs; positions are not a stable property of this batch.'})

inv=json.load(open(B/'source/inventory.json'));iq=inv['questions']
save('inventory-assessment.json',{'basis':inv['basis'],'question_count':len(iq),'questions':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'math_academy_id':q.get(':question/math-academy-id'),'generation_metadata_fields':[k for k in q if 'generat' in k]} for q in iq],'assessment':'Retained defect is missing source replay, now repaired. No per-instance generated mathematical or shortcut defect demonstrated. Original source questions are not relabeled as generated.','not_tested':'Five inventory records without Math Academy IDs lack generation metadata; no seed/parameter reproduction or generator attribution is claimed for them. Empty affected_questions means none demonstrated, not a proof of absence of other defects.'})
save('affected-inventory.json',{'affected_questions':[]})

viewed=[f'render/question-{i:03}.png' for i in range(1,7)]+[f'render-rest/question-{i:03}.png' for i in range(1,9)]+['render-rest/question-011.png','render-delivered/question-002.png','render-id-counterfactual-2/question-001.png']
renderreports=['render/rendering.json','render-rest/rendering.json','render-delivered/rendering.json','render-id-counterfactual-2/rendering.json']
assert all(load(p)['passed'] for p in renderreports)
save('visual-inspection.json',{'screenshots_viewed':viewed,'reports':renderreports,'observations':'All five raw batch screenshots, all three relevant/irrelevant pair groups, normalized restored RREF and canonical example inspected. Equations, signs, augmented bars, radio controls, vector/text choices and row-operation stages display correctly. Canonical example has no invented radio bank. Same normalized vector record moves from first to third position when only fixture task-item ID changes.','failures':[]})

sa=load('source-analysis.json')
probes=[]
def addprobe(cue,subgroup,scope,strategy,correct,total,disposition,conclusion,refs):
    probes.append(dict(cue=cue,subgroup=subgroup,scope=scope,strategy=strategy,correct=correct,total=total,baseline=.2,disposition=disposition,conclusion='Blind five-choice baseline is 0.2. '+conclusion,sample_refs=refs))
for stage in ['controlled','controlled_delivered']:
    for profile in ['q-20589','q-20598']:
        for strategy in ['lex_min','lex_max','majority_coordinates']:
            x=next(x for x in shortcuts[stage] if x['subgroup']=='profile:'+profile and x['strategy']==strategy)
            addprobe('Candidate extrema/coordinate frequency',stage+':'+profile,'within_template',strategy,x['correct'],x['total'],'not_predictive','All five eligible solution roles occur four times; bank-only rule has counterexamples within this restored profile.', ['controlled-records.json' if stage=='controlled' else 'delivery-controlled/accepted.json','shortcut-results.json'])
# Historical conditional evidence is reused only for unchanged bank/profile construction.
prior=load('prior-shortcut-results.json')
for x in prior['controlled']:
    if x['subgroup'].startswith('profile:') and x['strategy']=='majority_coordinates':
        addprobe('Bank coordinate frequency',x['subgroup']+' (unchanged profile, reused evidence)','within_template',x['strategy'],x['correct'],x['total'],'not_predictive','Previous independent controlled sample covers each role. All twelve profile objects and the bank_points construction are unchanged; fresh regression records check current rendering/math. This is reused evidence, not a new exhaustive audit.',['prior-controlled-records.json','prior-shortcut-results.json','provenance.json'])
for stage in ['batch','batch_delivered']:
    for strategy in ['lex_min','lex_max','majority_coordinates']:
        x=next(x for x in shortcuts[stage] if x['subgroup']=='overall' and x['strategy']==strategy)
        addprobe('Bank arrangement',stage,'overall',strategy,x['correct'],x['total'],'not_predictive','No tested bank-only strategy answers every member of the exact five-item pool.',['runner-batch.json' if stage=='batch' else 'delivery-batch/accepted.json','shortcut-results.json'])
for stage in ['batch','batch_delivered','delivered']:
    rows=ui['stages'][stage]
    for shape in ['all','rref','vector']:
        group=[x for x in rows if shape=='all' or x['template']==shape]
        if not group:continue
        counts=collections.Counter(x['correct_position'] for x in group);pos,n=counts.most_common(1)[0]
        text='Actual UI order; different positions occur in this group.'
        if stage=='batch_delivered' and shape=='vector':
            text='All three normalized vectors happen to be first at preview item IDs 3/4/5. This is a fixture-ID effect: each fixed record occupies all five positions across IDs 1..20, and the actual renderer moves the fourth record from first to third when its item ID becomes 1. It does not establish a stable delivered-batch cue; production IDs are unallocated.'
        addprobe('Visible answer position',stage+':'+shape,'overall' if shape=='all' else 'other_recognizable_subgroup',f'always position {pos+1}',n,len(group),'not_predictive',text,['ui-order-results.json','ui-id-probe.json','ui-dom-verification.json','delivery-batch/accepted.json'])
x=next(x for x in shortcuts['controlled'] if x['subgroup']=='profile:q-20598' and x['strategy']=='unique_z')
addprobe('Unique candidate matching displayed z','restored q-20598 subset','within_template','read z and select sole candidate with that z',x['correct'],x['total'],'intended_skill','Reading z from the last triangular equation is valid mathematical evidence and legitimate partial elimination. Other answer roles need more coordinates; this is not a label/layout cue.',['controlled-records.json','shortcut-results.json'])
pv={'learner_operation':sa['learner_operation'],'fixed_features':[
 {'feature':'Already-echelon nonsingular 3x3 system in x,y,z order','justification':'Target KP and tutorial f74e6075-9c2a-5495-ab21-470711559f2a prescribe backward elimination of three pivots.'},
 {'feature':'Unit pivots and two/three integer elimination steps in practice','justification':'All captured practice questions have unit pivots. q-131586 and q-131588 demonstrate skipped zero entries; restricting workload to the observed easy practice is defensible. Broader introduction includes pivot scaling.'},
 {'feature':'Five-choice radio, observed RREF/vector/text forms','justification':'All 14 source question banks use this response contract. Canonical e-4709 is fieldless and replay-only.'}],
 'answer_roles':[
 {'role':'Which candidate triple is the solution','eligible_variation':'Each of the five distinct source bank triples may solve the system when RHS changes. Original key/role is incidental.','observed':'Each restored profile covers all five roles under every coefficient mask; all survive delivery.'},
 {'role':'Which above-pivot entries require elimination','eligible_variation':'a12,a13,a23 signs/magnitudes vary independently, including supported single-zero masks.','observed':'All four masks and ±5 coefficient/translation boundaries and scales 1/2 exercised on restored profiles.'},
 {'role':'Visible correct position','eligible_variation':'No mathematically fixed answer position; actual UI reorders choices using task/field/choice IDs.','observed':'Raw random arrays favor late positions due seed correlation, but actual UI has counterexamples. Conditional normalized-vector preview coincidence was explicitly challenged with changed item IDs.'}],
 'coverage':[
 {'case':'Restored q-20589 and q-20598 role/mask cross product','sample_refs':['controlled-records.json','delivery-controlled/accepted.json','variation-coverage.json'],'result':'2 profiles × 5 roles × 4 masks; all 40 unique records survive. Twelve unchanged-profile regression items also survive.'},
 {'case':'Fresh sampler and exact runner batch','sample_refs':['random-records.json','runner-batch.json','delivery-sample/accepted.json','delivery-batch/accepted.json','variation-coverage.json'],'result':'28/28 random and 5/5 runner records survive. Batch roles 0/1/3; masks [1,1,0] and [0,1,1]; four profiles and distinct non-sign-only systems. Small pool need not exhaust all eligible cases.'}],
 'counterfactuals':[
 {'kind':'relevant','change':'For text/RREF/vector, hold A, complete bank, seed, shift and scale fixed; switch solution role 0 to 1 and derive RHS.','expected':'Displayed RHS, final result and accepted candidate change; old answer rejected.','observed':'All three pairs satisfy exact visible-equation math and every displayed operation; native grader rejects old answer and accepts new answer; screenshots inspected.','status':'passed','justification':'RHS is relevant evidence determining the unique solution, while the source correct candidate is incidental.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render/rendering.json','render-rest/rendering.json']},
 {'kind':'irrelevant','change':'Preserve solution and bank; negate off-diagonal coefficients [2,-3,1] and recompute RHS.','expected':'Equations and elimination operations change while accepted solution triple remains unchanged.','observed':'All three shapes preserve mathematical response and native acceptance, with changed prompts, row operations, matrices and rendered explanations. UUIDs and positions may change.','status':'passed','justification':'Different upper triangular systems can encode the same solution; the particular coefficient representation is irrelevant to which bank triple is correct.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-results.json','render-rest/rendering.json']},
 {'kind':'irrelevant','change':'Change only task-item ID from 4 to 1 for the same normalized vector question.','expected':'Answer and explanation preserved; visible ordering may change.','observed':'Actual UI moves correct choice from first to third, defeating the apparent choose-first vector subgroup cue without changing content or grader key.','status':'passed','justification':'Task identity has no mathematical role; actual UI includes it in choice ordering.','sample_refs':['delivery-batch/accepted.json','render-id-counterfactual-2.json','ui-id-probe.json','ui-dom-verification.json','render-id-counterfactual-2/rendering.json']}],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['generator parameter rejection and batch duplicate resampling','actual publication prepare_records, captured inventory deduplication and normalization','requested easy filtering','actual UI choice ordering','question_selection.rs positive/zero easy weight, unconfigured policy and history exclusion branches'],'sample_refs':['controlled-records.json','random-records.json','runner-batch.json','delivery-controlled/delivery.json','delivery-sample/delivery.json','delivery-batch/delivery.json','selection-analysis.json','ui-id-probe.json'],'result':'52/52 controlled, 28/28 random and 5/5 batch survive captured basis 5370; no decision-case suppression. All are easy. Conditional positive easy selection is uniform over fresh easy members, independent of answer roles. Zero easy weight excludes the band; unconfigured policy chooses first entity; history removes seen IDs. No live policy/history or future allocated IDs supplied, so exact future order is not asserted.'},
 'limitations':['Finite tests do not prove absence of all shortcuts.','Selection analyzed from actual code; future policy, history, allocated IDs and changing inventory cannot be predicted from this offline capture.','Five unattributed inventory records were not reproduced; empty affected_questions means no demonstrated generated-instance defect.','Unchanged profile coverage partly reuses prior independently bound evidence, with explicit provenance.']}
save('pedagogical-variation.json',pv)

hashes={str(p.relative_to(B/'workspace')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (B/'workspace').rglob('*') if p.is_file()}
save('package-hashes-after.json',hashes);assert hashes==load('package-hashes-before.json')
checks={
 'source_replay':(['source-replay.json','source-replay-records.json','repair-regression-results.json','review.py','reproduce_missing.py'],'All 15 source cases replay; 70 choices and captured operative stages match. q-20589 inferred key/explanation documented; canonical remains fieldless. Retained KeyErrors reproduced on old package and absent currently.'),
 'math':(['math-results.json','delivered-math.json','review.py','post_delivery.py'],'Independent Fraction elimination checks 109 raw/replay/pair records and 85 normalized survivors, including every displayed row operation and unique correct choice; no failures.'),
 'variety':(['variation-coverage.json','controlled-records.json','random-records.json','runner-batch.json','delivery-controlled/delivery.json','delivery-sample/delivery.json','delivery-batch/delivery.json','selection-analysis.json'],'Restored profiles cover every role/mask combination. All 52 controlled, 28 random and 5 runner records survive actual filtering; conditional learner selection examined with recorded limits.'),
 'scope':(['source-analysis.json','scope.json','math-results.json'],'Restored practice stays within observed easy integer backward elimination and radio representations; canonical is replay-only.'),
 'grading':(['grader-input.json','grader-results.json','counterfactual-results.json'],'Native grader: 196 expected acceptances and 775 expected rejections, zero unresolved. Includes normalized survivors and explicit prior-answer counterfactual responses. All practice fields are radio; free-entry equivalence is inapplicable.'),
 'rendering':(['visual-inspection.json']+renderreports,'Unmodified UI renders representatives, all counterfactual pairs, all five raw and normalized batch members and fieldless canonical example. Screenshots inspected; no math/control/solution defects.'),
 'packaging':(['packaging.json','package-hashes-before.json','package-hashes-after.json','provenance.json'],'Exact Python/SymPy versions match nested manifest dependencies; deterministic replay, relocation and rejection checks pass. Package byte hashes unchanged; no publication or database writes.'),
 'decision_variation':(['pedagogical-variation.json','shortcut-results.json','ui-order-results.json','ui-id-probe.json','ui-dom-verification.json','counterfactual-results.json','affected-inventory.json','inventory-assessment.json'],'Relevant/irrelevant pairs pass math, actual grading and rendering. Conditional restored-profile and exact-batch probes challenge bank geometry and visible position. Apparent normalized-vector position cue depends on fixture task IDs; no stable incidental shortcut demonstrated.')}
result={'verdict':'accepted','summary':'The retained source-coverage failure is repaired. All eight checks pass within documented offline limits; no remaining defect demonstrated. Package unchanged.','source_analysis':{k:sa[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':{k:{'status':'passed','evidence_paths':paths,'details':detail} for k,(paths,detail) in checks.items()},'findings':[]}
save('review-result.json',result)
(R/'session-state.md').write_text('Completed focused revision audit. Retained omission reproduced on old package, fixed currently. All 15 source cases/70 choices replay. 109 raw and 85 delivered math checks; native grader 196 accept/775 reject. Delivery controlled52/random28/batch5 all survive. UI/screenshots and conditional position counterfactual checked. Package hashes unchanged. Verdict accepted in review-result.json; pedagogical-variation.json records limits. No database writes or publication.\n')
print(json.dumps({'verdict':result['verdict'],'checks':len(checks),'shortcut_probes':len(probes),'package_unchanged':True}))
