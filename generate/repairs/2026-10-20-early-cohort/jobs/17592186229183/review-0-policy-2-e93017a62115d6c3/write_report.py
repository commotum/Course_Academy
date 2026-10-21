#!/usr/bin/env python3
"""Assemble review artifacts from completed independent checks."""
import json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;J=R.parent
def load(p):return json.loads((R/p).read_text())
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n')
a=load('source-analysis.json');stages=load('delivery-selection-results.json')['stages']
probes=[]
def probe(subgroup,scope,correct,total,refs):
    return {'cue':'Numerical order of the five displayed masses','subgroup':subgroup,'scope':scope,
      'strategy':'Select the third-smallest mass without using the physical data or solving the ODE.',
      'correct':correct,'total':total,'baseline':0.2,'disposition':'defect',
      'conclusion':f'{correct}/{total} correct versus uniform five-choice guessing at 0.2. Sorting answer values bypasses modeling, integration, initial conditions and overflow-time evaluation. The bank algebra forces two distractors below and two above the correct mass; this is an incidental authored arrangement, not the intended skill.',
      'sample_refs':refs}
probes.append(probe('all independent easy samples','overall',28,28,['sample-records.json','sampling-summary.json']))
for t,v in stages['independent_after']['templates'].items():
    probes.append(probe('normal method bank / '+t,'within_template',v['median_correct'],v['count'],['delivery-sample/accepted.json','sampling-summary.json']))
probes.append(probe('exact runner batch after shared delivery filtering','other_recognizable_subgroup',5,5,['delivery-batch/accepted.json','delivery-selection-results.json']))
for t,v in stages['batch_after']['templates'].items():
    probes.append(probe('exact batch / '+t,'within_template',v['median_correct'],v['count'],['delivery-batch/accepted.json','delivery-selection-results.json']))
pv={'learner_operation':a['learner_operation'],'fixed_features':a['fixed_features'],
 'answer_roles':[{'role':'Correct numerical mass','eligible_variation':'Physical quantities and capacity vary; response must be derived from the mass-balance solution at overflow.','observed':'Independent prompt-derived mass checks pass for 38 generated records; capacity pair changes 100.0 to 116.2 lb.'},
 {'role':'Correct choice numerical rank','eligible_variation':'Source banks have different ranks; no physical or instructional reason requires two alternatives on each side. Distractor construction may change rank while preserving one correct choice.','observed':'Rank 3 in all 28 independent samples, all 5 batch items, and all 10 reproduced stored generated records; structural proof covers the full normal method domain.'},
 {'role':'Correct choice display position','eligible_variation':'Shuffling is incidental to the modeling skill.','observed':'Ordering changes in generator and actual UI. This does not remove the invariant numerical-rank cue.'},
 {'role':'Overflow capacity target','eligible_variation':'Keep the overflow target operation but vary capacity independently of other physical inputs.','observed':'Holding v90 q18 c0.5 rin18 rout12 fixed, H210→240 changes time20→25 and mass100.0→116.2; solution and grading track it.'}],
 'coverage':[{'case':'All seven normal easy prompt masks; four fixed seeds each','sample_refs':['sample-records.json','sampling-summary.json'],'result':'28 records, four distinct physical tasks replicated across seven contexts; median shortcut succeeds in every subgroup. No arbitrary diversity quota inferred.'},
 {'case':'Exact five-item runner batch','sample_refs':['batch-records.json','delivery-batch/accepted.json','delivery-selection-results.json'],'result':'All five accepted after requested-difficulty, validation, identity normalization and captured-inventory deduplication. Median shortcut answers every surviving record.'},
 {'case':'Smallest admitted offset/time boundary and whole-bank rejection rules','sample_refs':['minimal-records.json','runtime-results.json'],'result':'d2 a5 time5 case has sorted choices6.5,7.0,7.3,7.6,8.0; correct7.3. Rejection of rounded collisions preserves strict rank ordering.'},
 {'case':'Stored generated practice pool','sample_refs':['generated-records.json','inventory-results.json','affected-inventory.json'],'result':'Ten generated records reproduced with identical IDs and generation metadata, prompt/bank/key matches and solutions equivalent after shared scalable-parentheses normalization; all rank3. Original source items excluded.'}],
 'counterfactuals':[{'kind':'relevant','change':'Hold v90 q18 c0.5 rin18 rout12 and context fixed; change capacity210→240.','expected':'Overflow time20→25 and rounded mass100.0→116.2; prompt, solution and correct selectable answer update.','observed':'Expected dependencies verified in independent arithmetic, real UI screenshots006/007 and native option grading. Numerical rank remains3, exposing the shortcut despite correct dependencies.','status':'passed','justification':'Capacity determines overflow evaluation time in the canonical solution V(t_o)=H.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-input.json','grader-report.json','render/rendering.json']},
 {'kind':'irrelevant','change':'Halve both inflow18→9 and outflow12→6, keeping all masses, concentrations and volumes fixed.','expected':'Overflow time doubles20→40; overflow mass remains100.0 lb; correct logical numerical response preserved.','observed':'Time and solution change, mass and complete numerical bank preserved; same displayed mass accepted by the native grader; screenshots006/008 show consistent endpoints.','status':'passed','justification':'Canonical mass balance can be reparameterized by volume; common flow scaling changes elapsed time but not mass at a specified capacity.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-input.json','grader-report.json','render/rendering.json']},
 {'kind':'irrelevant','change':'Keep physical data fixed and change coolant/inhibitor reservoir context to flavoring tank.','expected':'Numerical solution and mass100.0 lb preserved, with prompt/solution nouns updated.','observed':'Independent calculation, native acceptance and screenshots006/009 confirm preserved numerical response and consistent context.','status':'passed','justification':'Names of well-mixed solutes and containers do not enter the source mass-balance equation.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-report.json','render/rendering.json']}],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['generator physical/arithmetic rejection and complete-bank collision rejection','requested easy difficulty','shared prepare_records validation and stable identities','captured basis5395 inventory and within-batch deduplication','Rust selection band/draw rules and history exclusion, conditional read-only scenarios','actual UI answer order and solution display','native learner grading'],
 'sample_refs':['runtime-results.json','delivery-sample/delivery.json','delivery-batch/delivery.json','delivery-selection-results.json','grader-report.json','render/rendering.json'],
 'result':'28/28 independent and 5/5 batch records survive filtering and retain the shortcut. Any nonempty subset of the normal generated family retains it. Faithful conditional selection scenarios show source inventory can dilute aggregate success, while the exact batch and generated-only pool remain completely vulnerable.'},
 'limitations':['No live learner history or policy weights captured. Selection scenarios state assumed weights/freshness; no claim about an individual learner. Structural rank result is independent of these missing values.',
 'Captured inventory basis5395; concurrent inventory changes can change deduplication and candidate frequencies.',
 'Fresh audit focuses on requested easy level. Stored moderate/hard records are replayed to establish inventory impact of the same bank rule; broader difficulty-scope claims are not made.',
 'Finite probes do not prove absence of all shortcuts; the demonstrated median shortcut is supported by an algebraic family-wide argument.',
 'Source q-336499 lacks a key and solution; independent mass95.2 is inference. Four supplied source bank profiles are unsupported, and raw q-336451 retains a second obsolete field.']}
save('pedagogical-variation.json',pv)
save('render-inspection.json',{'renderer_report':'render/rendering.json','actual_ui_cases':17,
 'inspected':['render/question-010.png','render-inspection/pairs-top-1.png','render-inspection/pairs-bottom-1.png','render-inspection/templates-top-1.png','render-inspection/templates-top-2.png','render-inspection/templates-bottom-1.png','render-inspection/templates-bottom-2.png','render-inspection/batch-top.png','render-inspection/batch-bottom.png'],
 'observations':'Five numerical radio controls and worked equations legible; no MathJax/JavaScript/image failures. All batch endpoints, all template endpoints and controlled before/after prompt/solution dependencies visually inspected. The median cue remains visible under actual UI shuffling.',
 'limitations':'Desktop preview at renderer default viewport; no diagrams in this family. No mobile visual certification.'})
math=load('math-results.json');save('scope-results.json',{'requested_difficulty':'easy',
 'source_reference':'source-analysis.json','tested_records':len(math['results']),
 'all_n_equal_2':all(int(r['prompt_parameters']['rout'])/(int(r['prompt_parameters']['rin'])-int(r['prompt_parameters']['rout']))==2 for r in math['results']),
 'method':'All tested prompts ask for solute mass at overflow, with concentrated inflow, well-mixed discharge, linear increasing volume and quadratic integrating factor. Full worked-solution stage order preserved in actual rendered templates.',
 'response':'Single five-option radio in normal easy samples and delivered batch.',
 'conclusion':'No demonstrated easy-level scope drift. Numerical-rank fixation is separately a pedagogical variation failure.'})
save('commands.json',{'cwd':str(R),'python':'/home/jake/Developer/Course_Academy/.venv/bin/python',
 'commands':['/home/jake/Developer/Course_Academy/.venv/bin/python review.py',
 '/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input sample-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-sample --math-root /media/jake/SSD/EDB/math',
 '/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math',
 '/home/jake/Developer/Course_Academy/.venv/bin/python finish_checks.py',
 '/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-report.json',
 '/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --limit 17 --math-root /media/jake/SSD/EDB/math',
 '/home/jake/Developer/Course_Academy/.venv/bin/python regression_checks.py'],
 'expected_regression_exit':1,'database_writes':0,'package_writes':0})
def ck(status,paths,details):return {'status':status,'evidence_paths':paths,'details':details}
refs=a['source_refs']
report={'verdict':'revise','summary':'Normal banks always make the third-smallest mass correct: 28/28 independent samples, 5/5 delivered batch items and ten reproduced stored generated questions. Source replay also omits four supplied cases and retains an obsolete extra field. Package unchanged.',
 'source_analysis':{k:a[k] for k in ('skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths')},
 'checks':{
 'source_replay':ck('failed',['source-replay-results.json','source-replay-records.json','regression-checks.json'],'Four supplied bank profiles raise Unknown template; q-336451 raw replay has two fields versus one captured field. Source gaps and legitimate unit corrections distinguished in source-analysis.json.'),
 'math':ck('passed',['math-results.json','counterfactual-results.json'],'38 generated records independently parsed from prompts; exact ODE/initial-condition residuals and rounded masses agree. Full source-parameter calculations also retained.'),
 'variety':ck('failed',['sampling-summary.json','delivery-selection-results.json','regression-checks.json'],'Numerical and context variation retains a universally correct median-choice action, including the exact surviving five-item batch.'),
 'scope':ck('passed',['scope-results.json','source-analysis.json','render-inspection.json'],'Tested easy variants preserve the overflow-modeling task, quadratic integrating factor and five-choice response workload.'),
 'grading':ck('passed',['grader-input.json','grader-report.json'],'Actual native grader: 20 expected acceptances and 69 expected rejections, zero unresolved, including delivered choices and controlled pairs. Radio responses have no free-entry equivalence contract.'),
 'rendering':ck('passed',['render/rendering.json','render-inspection.json'],'Actual unmodified UI rendered 17 records; screenshots inspected for batch, every template and controlled pairs. No rendering errors.'),
 'packaging':ck('passed',['packaging-results.json','runtime-results.json','package-before.json','package-after.json'],'Exact Python3.13.5/SymPy1.14.0 match nested manifest dependency declarations; relocation and deterministic replay pass. Original package files unchanged.'),
 'decision_variation':ck('failed',['pedagogical-variation.json','minimal-records.json','affected-inventory.json','generated-records.json'],'Relevant/irrelevant dependencies track correctly, but every normal bank forces correct numeric rank3; rejection, filtering, deduplication and selection cannot remove this family-wide bypass.')},
 'findings':[{'kind':'decision_shortcut','description':'Normal method_bank always places two distractors below and two above the correct rounded mass. Sorting the answer values yields the answer without modeling or integration. This affects every surviving batch member and ten demonstrated stored generated records.','source_refs':['bbf602f0-1101-55d5-a6b3-9bfc5731e9ec: Steps1–4 and overflow evaluation','47a16983-dbf1-596b-b57d-9f38439fdd0f: correct93.8 among five numerical alternatives','generate/principles.md: vary eligible answer-bearing relationships'],
 'reproduction':'Run /home/jake/Developer/Course_Academy/.venv/bin/python regression_checks.py (exit1). Minimal API case: generate("easy",seed=9041,template="q-336506",parameters={"H":"20","v":"10","q":"1","c":"0.4","rin":"6","rout":"4"}). Sorted choices6.5,7.0,7.3,7.6,8.0; correct7.3 is the median. Complete record: minimal-records.json. Family-wide proof: sampling-summary.json.',
 'requested_change':'Change whole-bank distractor construction so the correct numerical rank is not forced by the recipes and concentrated-inflow constraints. Preserve the physical/ODE skill and response shape; option shuffling alone cannot fix it. Replace the affected five-item batch and address the ten IDs in affected-inventory.json after independent validation.'},
 {'kind':'source_fidelity','description':'The package replays an older seven-case capture instead of all eleven supplied source cases. Four current source profiles are unknown; observed:q-336451 emits a second field with no key although the captured current source has one complete field.','source_refs':['98f92dde-10ee-5a2e-ae0c-afe47e1981a5','0b0e00ac-15e0-50ff-896e-2fb3f25eb38a','c3e80580-6c31-591c-a6d6-df75a9aede3a','36a65a87-c8d0-5bbf-adbe-0789f4e08164','6c55e9d5-5244-5391-84ab-9850b2ba8152'],
 'reproduction':'Run regression_checks.py. Minimal missing replay: generate("easy",seed=9041,profile="observed:q-336519") raises ValueError: Unknown template. profile="observed:q-336451" yields two fields, while source UUID98f92dde has one. Exact cases and complete available replays: source-replay-results.json and source-replay-records.json.',
 'requested_change':'Refresh source masks and explicit historical banks against the supplied source.json: add q-336519,q-336503,q-336500,q-336508 and align q-336451 field structure. Preserve missing q-336499 evidence as a documented gap and distinguish authored completion from observed content.'}]}
save('review-result.json',report)
# Evidence contract validation uses jsonschema if available; fallback structural checks.
schema=Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json')
validation={'required_top_fields':set(json.loads(schema.read_text())['required'])==set(pv)}
try:
 import jsonschema
 jsonschema.validate(pv,json.loads(schema.read_text()));validation['jsonschema']='passed'
except ImportError:validation['jsonschema']='not installed; explicit required fields and references validated'
allrefs=[]
for section in ('coverage','counterfactuals','shortcut_probes'):
 for item in pv[section]:allrefs.extend(item['sample_refs'])
allrefs+=pv['delivery']['sample_refs']
allrefs+=report['source_analysis']['evidence_paths']
for check in report['checks'].values():allrefs+=check['evidence_paths']
validation['all_evidence_nonempty']=all((R/p).is_file() and (R/p).stat().st_size>0 for p in allrefs)
validation['all_refs_relative']=all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in allrefs)
original={str(p.relative_to(J/'workspace')):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((J/'workspace').rglob('*')) if p.is_file()}
validation['package_unchanged']=original==load('package-before.json')
save('evidence-contract.json',validation);assert all(v for k,v in validation.items() if isinstance(v,bool))
(R/'session-state.md').write_text('Review complete: verdict revise. review-result.json contains eight named checks and two actionable findings. Main defect is a proved forced-median answer bank: 28/28 independent samples,5/5 delivered batch,10/10 reproduced stored generated records. Source replay fails four missing profiles and one obsolete duplicate field. Independent math, easy scope, native grading(20 accepted/69 rejected), actual UI rendering(17 screenshots), exact dependencies, deterministic replay and relocation passed. pedagogical-variation.json and affected-inventory.json saved; strict regression_checks.py exits1 on current demonstrated defects. Evidence contract checked; original package hash map unchanged. No package edits, asset publication or database writes.\n')
print(json.dumps({'verdict':report['verdict'],'checks':{k:v['status'] for k,v in report['checks'].items()},'contract':validation}))
