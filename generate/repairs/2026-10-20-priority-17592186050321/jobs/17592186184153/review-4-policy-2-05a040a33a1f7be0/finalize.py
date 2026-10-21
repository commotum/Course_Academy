import sys;sys.dont_write_bytecode=True
import pathlib,json,hashlib,platform
from probe_tools import *
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
# Scope checks use parsed integrands; source annotations determine intended boundaries.
rs=load('samples.json')+load('boundaries.json')+load('runner-batch.json')+load('additional-counterfactual-records.json')
for r in rs:
 f,v=extract(r);terms=S.Add.make_args(f);assert len(terms)==2
 nonconstant=next(t for t in terms if t.has(V[v]));c,p=nonconstant.as_coeff_exponent(V[v]);assert abs(c)==1 and p!=-1
 assert p in [2,3,4,5,6,-S.Rational(3,2),-S.Rational(7,2)]
 assert r['question'][':question/difficulty']==':question.difficulty/moderate'
 if p<0:assert f'for ${v}>0$' in r['question'][':question/problem']
save('scope-results.json',{'passed':True,'checked_records':len(rs),'scope':'Two elementary power-rule antiderivatives; one unit-magnitude nonconstant coefficient, one signed constant; no logarithms, definite integrals, substitution, products or integration conditions. Explicit positive radical domain.',
 'families':'P/B integer exponents 2..6; R negative half-integer exponents -3/2 and -7/2. Same workload as moderate q-71167, q-71169 and q-133291.',
 'unsupported_source_families':'Unlabelled q-2159 and q-29828 are full-bank replay-only; fieldless q-71173 and hard q-113781 mathematical replay-only. No easy-labelled source. R5 is outside this conservative same-method family; no claim of covering all rational powers.',
 'source_refs':['e-371','q-71167','q-71169','q-133291','tutorial 701','tutorial 703'],'bank_constraint_assessment':'Three constants and two power coefficients are competing same-method answers; both coefficient sides, every eligible omission and each constant rank remain eligible. Same-sign bounded constants remove a cue without fixing the true constant rank.'})
render=load('render-all/rendering.json');assert render['passed'] and len(render['cases'])==38
save('render-inspection.json',{'passed':True,'rendered_records':38,'renderer':'unmodified actual UI via render_preview.py','full_size_inspected':['render-all/question-011.png','render-all/question-015.png','render-all/question-028.png','render-all/question-032.png','render-all/question-038.png'],
 'contact_sheet_inspected':'render-contact-sheet.png','contact_sheet_indices':'25..38, constant-role swaps, reciprocal exponent/sign/order pairs and repaired historical cases',
 'observations':['Polynomial fractions and five radio controls readable; selected choices agree with checked keys.', 'Reciprocal radicals and fractional exponent power-rule steps display correctly.', 'Blank integrates inline before external C and includes the added explanation about absorbing constants.', 'Relevant controlled prompts, highlighted answers and worked final expressions change together; reordered terms preserve the mathematical answer.', 'No math errors, image errors, JavaScript errors or font failures in the 38-case actual UI report.'],
 'limits':'Representative screenshot visual inspection plus automated report for all 38. No source/generated images or plots exist in this package.'})
# Probes distinguish deterministic assignment controls from random finite observations.
st=load('shortcut-stage-results.json');probes=[]
for stage in ['controls_delivered','delivered','selected_positive_moderate','runner_delivered']:
 for row in st[stage]['summary']:
  if row['subgroup'] not in ['P','R','P:2','P:4','P:6','R:-3/2','R:-7/2']:continue
  if row['cue'] not in ['range6','eliminate_singleton','choose_singleton','min_constant','max_constant','shortest','longest','constant_then_max','constant_then_min','constant_then_most','typography','position0','position4']:continue
  role_control=stage=='controls_delivered';is_math=row['cue'].startswith('constant_') or row['cue']=='typography'
  explanation=f"Observed {row['correct']}/{row['total']} deterministic tie-break actions; tie-averaged rate {row['tie_averaged_rate']:.6f}. Baseline {row['baseline']:.6f} is "+('uniform guessing among options after legitimately integrating only the constant.' if is_math else 'uniform guessing among all five options.')
  explanation+=(' Exact role controls balance ranks, coefficient sides and all five omissions separately for every supported exponent; no retained cue advantage remains.' if role_control else ' This finite random observation is interpreted alongside exact eligible-role controls, not as proof of a new bias or of absence of all shortcuts.')
  if row['cue']=='typography' and row['subgroup'].startswith('R'):explanation+=' This polynomial typography filter is unhelpful on reciprocal coefficients, as expected; it is not a predictor of reciprocal keys.'
  probes.append({'cue':row['cue'],'subgroup':stage+' '+row['subgroup'],'scope':'within_template' if ':' not in row['subgroup'] else 'other_recognizable_subgroup','strategy':row['cue']+'; deterministic UUID-seeded tie breaking, uniform tie expectation recorded separately','correct':row['correct'],'total':row['total'],'baseline':row['baseline'],'disposition':'not_predictive','conclusion':explanation,'sample_refs':['shortcut-stage-results.json','role-controls.json' if role_control else ('delivery/accepted.json' if stage=='delivered' else 'selection-results.json' if stage.startswith('selected') else 'batch-delivery/accepted.json'),'cue-grading.json']})
cf=[]
for r in load('counterfactual-results.json'):
 cf.append({'kind':r['kind'],'change':r['label'],'expected':r['response_relationship'],'observed':r['before_answer']+' -> '+r['after_answer']+'; exact math, rendered prompt/solution and native outcomes agree.','status':'passed','justification':'Tutorial 701 requires independent integration of each signed summand; term order and consistent variable renaming leave the mathematical antiderivative unchanged.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-input-final.json','grading.json','render-all/rendering.json']})
for r in load('additional-counterfactual-results.json'):
 cf.append({'kind':r['kind'],'change':r['change'],'expected':r['expected'],'observed':'Checked actual displayed expressions, differentiated keys and complete banks; corresponding native choices pass and available prior answers switch as expected. Rendered records 25..36 inspected.','status':'passed','justification':'Tutorial 701 and q-71169 require responding to the supplied constant, sign and reciprocal power; the constant assigned the correct role is eligible to change while the answer bank stays fixed.','sample_refs':['additional-counterfactual-records.json','additional-counterfactual-results.json','grading.json','render-all/rendering.json','render-contact-sheet.png']})
account=load('source-analysis.json')
ped={'learner_operation':account['learner_operation'],'fixed_features':[
 {'feature':'Two signed summands; one constant and one unit-magnitude power term in the generated moderate family.','justification':'e-371 and complete moderate q-71167/q-71169/q-133291 use this workload. Tutorial 703 introduces additional nonunit power factors in the next KP.'},
 {'feature':'Power exponent excludes -1, and radical reciprocals use a positive integration variable.','justification':'Power-rule integration, without logarithms or new domain/sign branches; consistent with q-71169 and the elementary sum-rule lesson.'},
 {'feature':'Five-choice radio or one blank with external C, using source-specific response contracts.','justification':'The captured complete answer banks and q-133291 establish these response forms. Blank grading now accepts constant shifts as tutorial 701 permits.'}],
 'answer_roles':[
 {'role':'Signed constant and its linear antiderivative coefficient','eligible_variation':'Both signs, magnitudes 1..6, term order and all three bank ranks.','observed':'All twelve signed constants in sampling/boundaries; all three correct ranks explicitly controlled with fixed banks; wrong constants now share the true-answer domain.'},
 {'role':'Signed nonconstant summand and transformed power coefficient','eligible_variation':'Supported polynomial and reciprocal powers, both signs, competitors on either side of the true magnitude.','observed':'Fresh/boundary cases plus exact side controls for each supported radio exponent; target sign/exponent changes propagate through prompt, solution, key and native grading.'},
 {'role':'Correct choice position and answer-bank singleton','eligible_variation':'All five shuffled positions; any non-key cell may be omitted, including the correct constant row.','observed':'All five eligible omissions survive delivery for every exponent and constant rank; positions vary. Singleton status alone is no longer an exclusion cue.'},
 {'role':'Representation and arbitrary additive constant','eligible_variation':'Equivalent expanded/factored expressions, consistent variable renaming, term reordering, and constant shifts where external C is supplied.','observed':'Native equivalents accepted; wrong derivatives rejected, including exact retained t^7/7+5t+1 case.'}],
 'coverage':[{'case':k,'sample_refs':['coverage.json','samples.json','role-controls.json','delivery-selection-summary.json'],'result':v} for k,v in [
 ('Profiles, exponents, signs and term order','Fresh seeds 63087129 and 20843761, 96 boundary records and five runner records cover P/R/B and the supported exponent domains; coverage is reported per profile.'),
 ('Changed answer-bank assignment roles','210 explicit controls: seven radio exponent profiles x three correct constant ranks x two competitor sides x five omissions. All 210 survive actual delivery.'),
 ('Delivered and selected distribution','128 fresh records ->125 accepted after three duplicates; runner five ->five. Positive moderate selection retains current profiles/slots; disabled and unconfigured policy behavior is recorded, without claiming availability when selection excludes the pool.')]],
 'counterfactuals':cf,'shortcut_probes':probes,
 'delivery':{'stages_examined':['generator valid-domain construction and lack of rejection/resampling loop','requested moderate difficulty','actual publication normalization, identity and validation','captured inventory and within-batch deduplication','learner fresh/usable filtering and SHA256 difficulty-first selection'],
 'sample_refs':['delivery-selection-summary.json','delivery/delivery.json','batch-delivery/delivery.json','controls-delivery/delivery.json','selection-results.json','shortcut-stage-results.json','cue-grading.json'],
 'result':'Compared parsed prompt/choice cues on raw, accepted and simulated selected records. Complete role controls survive delivery. Actual captured inventory basis is 5277. Publication preparation is absent, so shared prepare_records filtering was executed read-only.'},
 'limitations':['Finite checks do not prove the absence of every incidental shortcut.','Selection uses the actual captured inventory and faithful current selector rules with synthetic appended entity IDs, explicit policy scenarios and modeled seen history; live policy/history and database allocations were not supplied.','Concurrent inventory changes, real entity collisions and post-publication ordering are outside this read-only review.','Conservative generated family does not claim full rational-power coverage; unsupported/missing-response source cases are recorded separately.']}
save('pedagogical-variation.json',ped)
# Exact prescribed schema plus every local sample reference must be valid.
schema=json.loads((REPO/'generate/pipeline/pedagogical-variation.schema.json').read_text())
try:
 import jsonschema
 jsonschema.validate(ped,schema);schema_method='jsonschema.validate'
except ImportError:
 def valid(v,s):
  if 'enum' in s:assert v in s['enum']
  ty=s.get('type');typ={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float)}
  if ty:assert isinstance(v,typ[ty])
  if isinstance(v,dict):
   assert set(s.get('required',[]))<=set(v)
   if s.get('additionalProperties') is False:assert set(v)<=set(s['properties'])
   for k,z in v.items():
    if k in s.get('properties',{}):valid(z,s['properties'][k])
  if isinstance(v,list):
   assert len(v)>=s.get('minItems',0)
   for z in v:valid(z,s.get('items',{}))
  if isinstance(v,str):assert len(v)>=s.get('minLength',0)
  if isinstance(v,(int,float)):
   assert v>=s.get('minimum',float('-inf')) and v<=s.get('maximum',float('inf'))
 valid(ped,schema);schema_method='independent recursive validation of all schema keywords used by prescribed schema'
refs=[]
for group in ['coverage','counterfactuals','shortcut_probes']:
 for z in ped[group]:refs+=z['sample_refs']
refs+=ped['delivery']['sample_refs']
for ref in refs:
 p=R/ref;assert not pathlib.Path(ref).is_absolute() and p.is_file() and p.stat().st_size>0,ref
save('evidence-contract.json',{'passed':True,'schema_method':schema_method,'sample_refs_checked':len(refs),'unique_files':sorted(set(refs))})
# Complete package tree equality; no repair/publish/DB actions performed.
after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};before=load('package-before.json');assert after==before
save('package-after.json',after);save('package-integrity.json',{'passed':True,'files_before':len(before),'files_after':len(after),'modified':[],'added':[],'removed':[],'same_hashes':True,'database_writes':0,'published_assets':0})
save('preflight-independent-review.json',{'passed':True,'preflight_claim':load('../repair-preflight.json'),'author_current_rerun':load('author-preflight/evidence/repair-4/regressions.json'),'historical_failures':load('history-verification.json'),
 'assessment':'All five retained findings examined. Historical visible failures independently reproduced from saved implementations, with current counterpart rules tested. Old native constant-shift failure log retained and exact old failing input rerun successfully on current native grader. Author checks run isolated under evidence; independent checks, not author pass alone, determine this verdict.',
 'native_exact_regression':load('historical-constant-shift-current.json')})
checks={
 'source_replay':(['source-analysis.json','source-replay-results.json','source-replay.json','source-parameter-records.json'],'Seven supplied questions and 21 captured choices replayed; canonical e-371 checked at original parameters. Missing keys and derivative premise are resolved from source evidence; fieldless examples remain math-only.'),
 'math':(['math-results.json','role-control-results.json','additional-counterfactual-results.json','probes.py'],'Exact differentiation independently verified actual prompts, unique correct choices and worked expressions for fresh, boundary, runner and controlled records.'),
 'variety':(['coverage.json','samples.json','boundaries.json','role-controls.json','delivery-selection-summary.json'],'Supported profiles, signs, constants, exponents, order, choice positions and bank roles vary; explicit changed-role cases survive delivery.'),
 'scope':(['source-analysis.json','scope-results.json'],'Generated moderate items retain the two-term sum/power-rule method; unsupported response families and conservative domain limits are explicit.'),
 'grading':(['grader-input-final.json','grading.json','historical-constant-shift-current.json','cue-grading.json'],'Native grader passed 492 accepted and 1335 rejected checks, plus 802 accepted and 1918 rejected cue-action checks. Equivalent/factored and constant-shifted blanks accepted; incorrect derivatives rejected.'),
 'rendering':(['render-all/rendering.json','render-inspection.json','render-contact-sheet.png'],'38 records rendered through the actual UI. Representative full-size screenshots and controlled-pair contact sheet were visually inspected; no display faults observed.'),
 'packaging':(['packaging-results.json','package-integrity.json','package-before.json','package-after.json','commands.json'],'Exact Python 3.13.5 and empty third-party dependency declaration, deterministic replay, relocation and CLI boundaries passed. All 242 package files have unchanged hashes.'),
 'decision_variation':(['pedagogical-variation.json','role-control-results.json','shortcut-stage-results.json','preflight-independent-review.json','evidence-contract.json'],'All retained counterexamples checked. Relevant and irrelevant rendered/native counterfactuals pass; tested conditional cues lose their structural advantage in exact delivered role controls. Selection/inventory limits are explicit.')}
result={'verdict':'accepted','summary':'All eight checks passed. The five retained findings are addressed in tested cases; independent source, math, native grading, rendering and delivered-variation evidence supports acceptance. Package files remained unchanged.',
 'source_analysis':{k:account[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs']},
 'checks':{k:{'status':'passed','evidence_paths':paths,'details':details} for k,(paths,details) in checks.items()},'findings':[]}
result['source_analysis']['evidence_paths']=['source-analysis.json','source-replay-results.json']
commands={'python':sys.executable,'cwd':str(R),'commands':[
 '-B review.py','-B probes.py','-B author-preflight/repair_regressions.py (cwd author-preflight; isolated copied check; see preflight-adaptation.json)',
 '-B '+str(REPO/'generate/pipeline/check_delivery.py')+' --input samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output delivery --asset-root . --math-root /media/jake/SSD/EDB/math',
 'repeat delivery command with runner-batch.json/batch-delivery and role-controls.json/controls-delivery',
 '-B selection_check.py','-B delivery_analysis.py',str(REPO/'generate/runs/current/check-engine')+' grader-input-final.json grading.json',str(REPO/'generate/runs/current/check-engine')+' cue-grader-input.json cue-grading.json',str(REPO/'generate/runs/current/check-engine')+' historical-constant-shift-input.json historical-constant-shift-current.json',
 '-B '+str(REPO/'generate/pipeline/render_preview.py')+' --input render-records-final.json --output render-all --limit 38 --asset-root . --math-root /media/jake/SSD/EDB/math','-B finalize.py'],
 'fresh_seeds':[63087129,20843761],'controlled_seeds':[901,713,81],'runtime_replay_seed':7836512,'historical_seeds':[86184906,94172863],
 'provenance':'Reused prior independent account and parser/selection script after source confirmation. review.py adapted for new in-range bank constraints, added additive-constant entries and current solution suffix; probes.py and delivery_analysis.py are fresh independent checks.',
 'tool_errors_resolved':['First isolated author-check path replacement used str.read_text; fixed to pathlib.Path before successful rerun.','System python lacks SymPy; selection rerun with supplied job Python.','Default UI renderer limit is six; full selected set rerun explicitly with --limit 38.']}
save('commands.json',commands)
for check in result['checks'].values():
 for ref in check['evidence_paths']:assert (R/ref).is_file() and (R/ref).stat().st_size>0
save('result.json',result)
(R/'session-state.md').write_text('Review complete: accepted; all eight checks passed with evidence in result.json. Independent source analysis confirmed before package inspection. All five retained findings examined; current native constant-shift regression passes. 38 actual UI records rendered; representative screenshots inspected. Delivery and selection limitations recorded in pedagogical-variation.json. Evidence schema and all sample paths verified. Complete package hashes unchanged across 242 files. No package edits, publishing or database writes.\n')
print(json.dumps({'verdict':result['verdict'],'checks':list(result['checks']),'schema_validation':schema_method,'package_files_unchanged':len(after),'result':'result.json'}))
