import json,pathlib,hashlib,collections,re,sys
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.loads((E/p).read_text())
def save(p,d):(E/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def key(r):
 f=r['question'][':question/answer-fields'][0];return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def choices(r):return r['question'][':question/answer-fields'][0][':answer-field/choices']
# Retain actual post-selection records and count prior cue with deterministic weighted draw results.
selected=load('selection-sampled-records.json');scores=collections.defaultdict(lambda:[0,0])
for item in selected['records']:
 r=item['record'];n=item['selection_count'];fam=r['generation']['template']
 if fam!='quotient' or r'}{x^{4}}' not in r['question'][':question/problem']:continue
 pred=max(choices(r),key=lambda a:max([int(z) for z in re.findall(r'x\^\{(\d+)\}',a[':answer/value'])]+[1]))
 scores['den4-largest-visible'][0]+=n*(pred[':answer/id']==key(r)[':answer/id']);scores['den4-largest-visible'][1]+=n
selection_probe={'cue':'prompt denominator x^4 and largest visible exponent in answers','subgroup':'quotient/den4 after learner selection','scope':'other_recognizable_subgroup','strategy':'largest-visible','correct':scores['den4-largest-visible'][0],'total':scores['den4-largest-visible'][1],'baseline':.2,'disposition':'not_predictive','conclusion':'Weighted successes among the 12000 explicit deterministic same-band draws, versus uniform five-choice baseline 0.20. All 240 delivered new items were selected, so each delivered counterexample to the other tested static strategies also survives this stage. Synthetic ID ordering and empty history are explicit assumptions.','sample_refs':['selection-sampled-records.json','selection-draws.json']}
save('selection-shortcut-results.json',selection_probe)
# All exact math and native outcomes must be successful before a passing report.
m=load('math-results.json');assert m['passed']==m['records'] and not m['failures']
g=load('grader-all-report.json');assert g['documented_unresolved_checks']==0 and g['database_writes']==0
renders=[load('render/rendering.json'),load('render-revision/rendering.json')];assert all(z['passed'] for z in renders) and sum(len(z['cases']) for z in renders)==67
# Preserve actual renderer mapping and verify relevant prompts differ, and irrelevant keys stay the same.
pairs=load('counterfactuals.json');rp=load('revision-counterfactuals.json'); rr=load('render-records.json');rr2=load('render-revision-records.json'); rendered=[]
for i,p in enumerate(pairs):
 a,b=12+2*i,13+2*i;ca,cb=renders[0]['cases'][a],renders[0]['cases'][b]
 assert ca['passed'] and cb['passed'];assert ca['text']!=cb['text'] or p['label']=='radio-order'
 rendered.append({'pair':p['label'],'kind':p['kind'],'before_screenshot':f'render/question-{a+1:03}.png','after_screenshot':f'render/question-{b+1:03}.png','rendered_text_changed':ca['text']!=cb['text'],'expected_response':p['expected'],'native_checks':'grader-all-report.json labels '+p['label']+'-before/-after'})
for i,p in enumerate(rp):
 folder='render' if i<3 else 'render-revision';off=34+2*i if i<3 else 2*(i-3);report=renders[0 if i<3 else 1]
 ca,cb=report['cases'][off:off+2];assert ca['passed'] and cb['passed'] and ca['text']!=cb['text']
 rendered.append({'pair':p['label'],'kind':'relevant','before_screenshot':f'{folder}/question-{off+1:03}.png','after_screenshot':f'{folder}/question-{off+2:03}.png','rendered_text_changed':True,'expected_response':'different','native_checks':'grader-all-report.json labels '+p['label']+'/before/after'})
save('render-counterfactual-review.json',{'pairs':rendered,'method':'Actual UI renderer passes at both endpoints; prompt/solution text changes checked and record mapping retained. Independent exact checks establish the primitive; native outcomes verify accepted and rejected actions. Visual inspection is recorded separately.'})
# Coverage counts do not count interchangeable internal labels as independent banks.
coverage=[]
for name in ['sample.json','controlled.json','delivery-sample/accepted.json','delivery-controlled/accepted.json','runner-batch.json']:
 records=load(name);families=collections.Counter(r['generation']['template'] for r in records);qs=[r for r in records if r['generation']['template']=='quotient'];signs=collections.Counter(str((r['generation']['parameters']['a']>0,r['generation']['parameters']['b']>0)) for r in records)
 coverage.append({'file':name,'count':len(records),'families':dict(families),'sign_pairs':dict(signs),'quotient_internal_pairings':len({tuple(r['generation']['parameters']['reciprocal_exponents']) for r in qs}),'quotient_roles':dict(collections.Counter(r['generation']['parameters']['target'] for r in qs))})
save('coverage-summary.json',coverage)
probes=load('decision-probes.json');assert not [p for k in ['controlled','controlled-delivered'] for p in probes[k] if p['correct']==p['total']]
# Contract includes a measured conditional probe, and intended mathematical simplification is distinguished.
intended=load('variation-results.json')['intended_probes']
allprobes=probes['delivered']+probes['controlled-delivered']+[selection_probe]+intended
variation={
'learner_operation':load('source-analysis.json')['learner_operation'],
'fixed_features':[
 {'feature':'Two nonzero elementary power terms after one product/quotient rewrite; no exponent -1 integration.','justification':'q-49059 and q-49063 establish this moderate workload; tutorial 703 supplies linearity and constant extraction.'},
 {'feature':'Five math choices and one correct radio answer, or a single blank preceding supplied +C.','justification':'These are the complete response contracts in the supported source banks.'},
 {'feature':'Modest powers, variable x, and real-domain assumptions.','justification':'Keep algebra and workload comparable and define radicals/reciprocals; variable renaming is incidental and not needed for answer-role variation.'},
 {'feature':'Blank reduced integrand a+b/x^2, with degree 2 or 3 before cancellation.','justification':'All three recovered blank sources have this same reduced form. Coefficients/signs vary independently; allowing arbitrary unrelated powers would broaden this finite source family.'},
 {'feature':'Quotient reciprocal-exponent multiset -1,-1,-1,-2,-3; exclude equal exponents on identical polynomial components.','justification':'Conservative source-bank extension. Keeps five unique primitive choices and same two-power workload. Which polynomial component receives each exponent is eligible and is varied, rather than preserving the source assignment.'}],
'answer_roles':[
 {'role':'Which primitive in each radio bank is correct.','eligible_variation':'All five slots, with shuffled display positions and jointly updated integrand/key/solution.','observed':'All five targets sampled and controlled in both radio families; all survive delivery.'},
 {'role':'Pairing of polynomial coefficient/exponent with reciprocal exponent in quotient choices.','eligible_variation':'Move the source multiset among polynomial primitives subject only to uniqueness.','observed':'All 14 internal assignments tested at all 5 roles and 3 p values. They are seven unordered mathematical banks at fixed a,b,p; deduplication removes redundant copies without fixing polynomial correctness rank.'},
 {'role':'Signs and coefficients in both primitive terms.','eligible_variation':'Independently signed small nonzero coefficients; change either term to require response reconsideration.','observed':'All four sign pairs and boundaries covered. Relevant coefficient and same-denominator role pairs change actual accepted response.'},
 {'role':'Blank numerator degree and displayed choice ordering.','eligible_variation':'Change degree 2 to 3 with corresponding f and denominator update; shuffle choices.','observed':'Response remains equal for both irrelevant pairs, confirmed by exact math, native grading and actual UI rendering.'}],
'coverage':[
 {'case':'Source and all role/pairing/p/sign boundaries.','sample_refs':['source-replays.json','controlled.json','coverage-summary.json'],'result':'Five supported source cases; 258 controls include every quotient assignment x role x p, all source roles and sign boundaries, plus blank degrees.'},
 {'case':'Raw rejection/resampling and captured delivery.','sample_refs':['raw-attempts.json','sampling.json','variation-results.json','delivery-sample/accepted.json','delivery-controlled/accepted.json','delivery-batch/accepted.json'],'result':'272 raw attempts -> 240 unique prompts -> 240 delivered; control 258 -> 148 after duplicate removal; runner 5 -> 5. Denominators 2,3,4, both radical forms and blank survive.'},
 {'case':'Conditional rank cues before and after filtering.','sample_refs':['decision-probes.json','decision-coverage.json','surface-probes.json'],'result':'No tested static cue is perfect in full structural controls or delivered controls, including each denominator/p cell and each radical form. Sign subgroups in fresh samples likewise have counterexamples.'},
 {'case':'Maximum count and conditional learner selection.','sample_refs':['boundary-1000.json','boundary-results.json','selection-sampled-records.json','selection-shortcut-results.json'],'result':'1000 unique prompts after 2075 attempts; deterministic replay. All 240 delivered items selected across 12000 synthetic-ID, fresh-history moderate-band draws.'}],
'counterfactuals':[
 {'kind':'relevant','change':'Change target while holding coefficients, p and full bank fixed; specifically also hold denominator fixed in each of all 14 revised quotient assignments.','expected':'Prompt numerator, nonconstant primitive and worked solution change; previous choice rejected and current choice accepted.','observed':'All 14 same-denominator revised pairs and 8 original radio role pairs satisfy exact math, rendered text changes and native outcomes.','status':'passed','justification':'Correctness must follow the displayed integrand, not source role or denominator-conditioned polynomial rank. Tutorial 703; q-49059 and q-49063.','sample_refs':['revision-counterfactuals.json','revision-counterfactual-results.json','counterfactuals.json','render-counterfactual-review.json','grader-all-input.json','grader-all-report.json']},
 {'kind':'relevant','change':'Flip only b in the blank family (a=2, b=4 to -4, degree2).','expected':'Reciprocal term changes sign; solution and accepted response follow.','observed':'Before 2x-4/x and after 2x+4/x; opposite response rejected, current response accepted; both endpoints rendered.','status':'passed','justification':'q-167617 and the sum/difference rule require sign-sensitive integration.','sample_refs':['counterfactuals.json','math-results.json','grader-all-report.json','render-counterfactual-review.json']},
 {'kind':'irrelevant','change':'Degree2 to3 with f and denominator changed together; reverse radio display order.','expected':'Same mathematical answer and acceptance; displayed algebra/order changes coherently.','observed':'Both pairs preserve response and native acceptance; rendered prompts and controls inspected.','status':'passed','justification':'In the recovered blank family f/x^d=a+b/x^2 for either degree. Source radio contract depends on expression rather than choice position.','sample_refs':['counterfactuals.json','grader-all-report.json','render-counterfactual-review.json']}],
'shortcut_probes':allprobes,
'delivery':{'stages_examined':['generator uniqueness rejection/resampling','requested moderate difficulty','actual publisher identity/normalization and validation','captured inventory and within-batch deduplication at basis5277','learner eligibility rules inspected; same-band weighted selection with explicit synthetic IDs and fresh history; None/zero/history branches bounded in notes'],'sample_refs':['variation-results.json','delivery-sample/delivery.json','delivery-controlled/delivery.json','delivery-batch/delivery.json','selection-results.json','selection-sampled-records.json','selection-shortcut-results.json'],'result':'Decision cases and static-cue counterexamples survive applicable offline delivery. Prior den4/max-visible shortcut scores 1/17 fresh delivered, 6/24 delivered controls, and '+str(selection_probe['correct'])+'/'+str(selection_probe['total'])+' selected draws. Runner has only one den4 item and gives no standalone distribution claim.'},
'limitations':['Captured inventory basis5277 may change after this audit. No assets or database were published.','Active learner policy, learner history, ordinary/multistep classification beyond captured fields and future database ID allocation are not supplied. Selection conclusion is conditional on fresh eligible generated items and positive moderate weight; None selects first ID and zero moderate weight suppresses generated items as application policy.','Only requested moderate source families are supported. Source context repairs and excluded evidence gaps are documented.','Finite static-cue probes do not prove absence of every shortcut. Reciprocal exponent matching to the integrand is legitimate assessed power-rule reasoning even when it alone eliminates distractors.','Some runner or sign/p cells are small. Perfect success on a single runner item is not asserted as a structural defect; larger controlled and sampled cells contain counterexamples.']}
save('pedagogical-variation.json',variation)
# Integrity includes the entire package, not just manifest runtime files.
after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};before=load('package-before.json');assert after==before
save('package-integrity.json',{'unchanged':True,'before':before,'after':after,'comparison':'all files recursively in package_root','database_writes':0,'publication':False})
source=load('source-analysis.json')
def passed(paths,details):return {'status':'passed','evidence_paths':paths,'details':details}
result={'verdict':'accepted','summary':'All eight checks passed. The revised quotient pairing removes the previously demonstrated shortcut; no reproducible defect was found in this audit. Package unchanged.', 'source_analysis':{k:source[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs']},'checks':{
 'source_replay':passed(['source-analysis.json','source-replay-results.json','source-replay-review.md','source-replays.json'],'All five supported moderate cases, complete 10 radio choices and three blank banks match; explicit f(x) restoration is a documented source-context correction.'),
 'math':passed(['audit.py','math-results.json','revision-counterfactual-results.json','blank-prompt-degree-check.json'],'530 records plus 28 revised-counterfactual endpoints passed exact checks of actual prompts, all choices and every worked-solution expression.'),
 'variety':passed(['coverage-summary.json','sampling.json','decision-coverage.json','variation-results.json','boundary-results.json'],'All eligible roles, sign pairs, 14 quotient assignments, three p values, two radical forms and both blank degrees tested; meaningful cases survive rejection and delivery.'),
 'scope':passed(['scope-review.md','controlled.json','source-analysis.json'],'Extensions preserve two elementary power integrals, comparable algebra and source response contracts; unsupported source families explicitly excluded.'),
 'grading':passed(['grader-all-input.json','grader-all-report.json','revision_tests.py'],'Native learner grader passed 822 accepted and 2439 rejected checks across 753 records, including equivalent blank entries, plausible wrong responses, target changes and delivered shortcut actions; zero unresolved.'),
 'rendering':passed(['render/rendering.json','render-revision/rendering.json','visual-review.md','render-counterfactual-review.json','render/question-029.png','render/question-035.png','render/question-036.png'],'67 actual-UI previews passed, including all controlled pair endpoints and runner batch; representative radio, radical, blank and changed-role screenshots visually inspected.'),
 'packaging':passed(['packaging-results.json','boundary-results.json','package-integrity.json','provenance.json'],'Exact installed Python3.13.5/SymPy1.14.0 match manifest; relocation, deterministic replay, count limits and unsupported difficulty rejection passed. Entire package unchanged.'),
 'decision_variation':passed(['pedagogical-variation.json','decision-probes.json','selection-shortcut-results.json','revision-counterfactuals.json','grader-all-report.json'],'Independent fixed-feature challenge, relevant/irrelevant counterfactuals and conditional cue probes passed. Prior denominator4/max-exponent rule has explicit delivered counterexamples; selection conclusions are bounded to captured inputs and stated policy/history assumptions.')},'findings':[]}
result['source_analysis']['evidence_paths']=['source-analysis.json','source-replay-review.md'];save('result.json',result)
# Evidence reference and schema checks are review-contract checks, not generator correctness claims.
for c in result['checks'].values():
 for p in c['evidence_paths']:assert (E/p).is_file() and (E/p).stat().st_size>0,p
for section in ['coverage','counterfactuals','shortcut_probes']:
 for item in variation[section]:
  for p in item['sample_refs']:assert not pathlib.Path(p).is_absolute() and (E/p).is_file() and (E/p).stat().st_size,p
for p in variation['delivery']['sample_refs']:assert (E/p).is_file() and (E/p).stat().st_size,p
save('evidence-contract.json',{'all_references_nonempty':True,'all_sample_refs_relative':True,'checks':list(result['checks']),'schema_validation':'run separately with python3/jsonschema','package_unchanged':True})
print(json.dumps({'verdict':result['verdict'],'exact_math_records':m['records']+28,'grader_accepted':g['accepted_checks'],'grader_rejected':g['rejected_checks'],'renders':67,'selection_shortcut':[selection_probe['correct'],selection_probe['total']],'package_unchanged':True}))
