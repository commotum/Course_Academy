"""Assemble reviewed conclusions and verify the evidence contract; no package writes."""
import sys
sys.dont_write_bytecode=True
import json,pathlib,hashlib
import revision_audit as R
A=R.A;H=R.HERE
load=R.load;save=R.save
# Independent evidence assertions, not a rerun of generator tests.
assert all(x['passed'] for x in load(H/'math-results.json')['cases'])
assert all(x['passed'] for x in load(H/'delivery-math-results.json'))
assert load(H/'render/rendering.json')['passed'] and load(H/'render-inspection.json')['passed']
assert load(H/'packaging-results.json')['original_package_unchanged']
assert A.snapshot()==load(H/'package-before.json')
strict=load(H/'strict-regression-execution.json');assert [r['exit_code'] for r in strict]==[1,1,0,0]
raw=load(H/'grader-report.json');delivered=load(H/'delivered-grader-report.json')
assert (raw['accepted_checks'],raw['rejected_checks'],delivered['accepted_checks'],delivered['rejected_checks'])==(64,260,50,200)
assert raw['database_writes']==delivered['database_writes']==0
checks=[]
for fn,log in [('checks/repair_checks.py','author-repair-check.log'),('checks/canonical_coverage.py','author-canonical-check.log')]:
 digest=hashlib.sha256((R.PKG/fn).read_bytes()).hexdigest();before=next(c for c in load(R.JOB/'repair-preflight.json')['checks'] if c['script']==fn);assert digest==before['sha256'];assert (H/log).stat().st_size
 checks.append({'script':fn,'sha256':digest,'copy_sha256':hashlib.sha256((H/'author-check-copy'/fn).read_bytes()).hexdigest(),'run_command':f'{sys.executable} author-check-copy/{fn}','exit_code':0,'stdout_log':log,'preflight_matches_current':True})
save('author-check-verification.json',{'retained_findings':load(R.JOB/'repair-history.json')['findings'],'preflight_scripts':checks,'independent_fail_then_pass_execution':'strict-regression-execution.json','interpretation':'Copied unmodified author checks reran under evidence_root. Independent strict regressions additionally fail both historical constructions for the stated substantive reason and pass current. Author pass alone is not treated as acceptance.'})
# Fixed-bank orbits test not only the previous cue, but any deterministic bank-only predictor.
probes=[]
for filename in ['shortcut-results.json','delivery-shortcut-results.json']:
 for x in load(H/filename):
  scope='overall' if x['template']=='overall' else 'within_template'
  probes.append({'cue':x['strategy'],'subgroup':x['dataset']+' / '+x['template'],'scope':scope,'strategy':{'first_position':'Choose the first displayed equation.','smallest_abs':'Choose the unique smallest absolute exponential coefficient.','largest_abs':'Choose the unique largest absolute exponential coefficient.','smallest_signed':'Choose the most negative exponential coefficient.','largest_signed':'Choose the most positive exponential coefficient.','double_exponent':'Choose the unique exponential whose doubled exponent also occurs.'}[x['strategy']], 'correct':x['correct'],'total':x['total'],'baseline':0.2,'disposition':'not_predictive','conclusion':'Random single selection among five has success probability 0.2. These are finite observed successes, with abstention counted incorrect; small default/batch subgroups do not estimate a population rate. In each identical-bank five-target orbit every coefficient can be correct and each tested bank-only strategy succeeds 1/5. Code independently selects P uniformly from a preselected coefficient bank before forcing, so these cues do not determine the key; all sampled easy attempts accepted first try. Delivery retained every distinct target in the controlled orbits. The same fresh seeds across four templates share bank draws and are not 24 independent coefficient-bank draws.','sample_refs':[filename,'counterfactual-records.json']})
cfrefs=['counterfactual-records.json','counterfactual-results.json','math-results.json','grader-input.json','grader-report.json','render-input.json','render-inspection.json','render/rendering.json','delivery-counterfactuals/accepted.json','delivered-grader-report.json']
variation={
 'learner_operation':'Normalize the ODE, identify P and Q, integrate P to choose I with I′=PI, and identify the complete product-derivative equation (yI)′=IQ, stopping before solving y.',
 'fixed_features':[
  {'feature':'One radio response among five complete equations','justification':'All eight captured practice fields have this contract. Five alternatives require identifying the complete transformed equation without adding solution of the ODE.'},
  {'feature':'Constant P and exponential I within each easy template','justification':'Canonical e-21741 and constant-coefficient practice sources assess integration of a constant. Changing to reciprocal or linear P is already represented in preserved moderate templates and changes the integration operation; fixing the constant family does not fix the eligible signed coefficient.'},
  {'feature':'New easy authored bank has five exponentials with distinct logarithmic derivatives','justification':'An authored repair of the demonstrated bank cue. Every factor can be correct under eligible constant-P changes and all alternatives use the same elementary operation. Raw source banks remain executable separately for fidelity.'},
  {'feature':'Nonzero derivative coefficient; x>0 for scaled-by-x template','justification':'Division by the derivative coefficient must be valid. The source normalization operation is preserved on a working interval.'}
 ],
 'answer_roles':[
  {'role':'Coefficient whose exponential is the unique integrating factor','eligible_variation':'Any one of the five distinct eligible signed rational coefficients can equal P, with bank and Q fixed. Correct position also varies.','observed':'Four independent five-target orbits hold complete banks fixed and yield five different correct equations and solutions per template; every distinct target survives delivery.'},
  {'role':'Forcing factor Q and cancellation in IQ','eligible_variation':'Source-supported cosine, polynomial or exponential forcing by template. For exponential forcing vary b and c independently of P, allowing cancellation and noncancellation.','observed':'Canonical a=2,b=2,c=-2 replayed; controlled c change to +1 keeps I and changes IQ. Fresh/default and boundary exponential cases include independent rates and signs.'},
  {'role':'Unnormalized derivative coefficient','eligible_variation':'Standard and source-scaled constant families preserve A=1 or x by recognizable template, while P varies after division.','observed':'Scaled and unscaled polynomial templates tested with the same eligible P bank, including signed/rational coefficients.'}
 ],
 'coverage':[
  {'case':'All supported original material','sample_refs':['source-replay-records.json','source-replay-results.json','source-analysis.json'],'result':'All eight practice prompts, complete banks and six captured keys replay; two missing source keys are mathematically inferred. Canonical e-21741 reachable with correct four-stage solution; no canonical bank was captured.'},
  {'case':'Fresh requested easy families and unchanged-band regression','sample_refs':['samples.json','boundary-records.json','generator-rejection-trace.json'],'result':'24 easy records (six chosen seeds in each of four templates), six unchanged-family samples and four new-family boundaries checked. Signed/fractional/integer coefficients, polynomial/cosine/exponential Q, and scaled normalization occur. Trace shows one accepted construction attempt per sampled record.'},
  {'case':'Eligible correct-factor roles within each easy template','sample_refs':['counterfactual-records.json','counterfactual-results.json','delivery-counterfactuals/accepted.json'],'result':'All five controlled factors become correct with the same complete bank and Q in each of four templates; all distinct cases survive delivery.'},
  {'case':'Historical bank pool','sample_refs':['generated-records.json','affected-inventory.json','inventory-results.json','delivery-selection-results.json'],'result':'Nine historical generated records retained and compared against captured inventory; three old easy records still exhibit the original shortcut and remain selectable in conditioned scenarios. These are historical version records, not newly produced by the reviewed revision, and require downstream inventory remediation.'}
 ],
 'counterfactuals':[
  {'kind':'relevant','change':'Hold complete bank and Q fixed; assign P successively to -3,-1/2,1/3,1,2 in each easy template.','expected':'Prompt, integrating factor, correct equation, solution and actual native grader outcomes must follow the reassigned coefficient. Old correct equation must fail under a changed P.','observed':'Five different correct equations and solutions per family; exact equations verified, all options graded, and four explicit stale-response rejections passed. Relevant endpoints rendered for every family. Distinct targets retained by publisher.','status':'passed','justification':'Tutorial a7f8aa2e derives I′=IP. Source coefficient assignments are incidental; preserving the rule does not justify fixing which bank factor satisfies it.','sample_refs':cfrefs},
  {'kind':'relevant','change':'Keep P=2 and exponential bank fixed; change Q from 2exp(-2x) to 2exp(x).','expected':'I remains exp(2x); prompt forcing, correct RHS and solution follow Q, from cancelling to noncancelling product.','observed':'Printed-equation checks and native grading passed for both complete records; actual UI screenshots 004 and 010 display the changed Q and IQ with the same factor.','status':'passed','justification':'Tutorial a6a381ed Steps 3–4 multiply the normalized Q by the same I. Canonical cancellation is an example assignment, not an essential requirement.','sample_refs':cfrefs},
  {'kind':'irrelevant','change':'Change shuffle seed only, fixing template, explicit parameters and complete bank.','expected':'Choice ordering changes; prompt, worked solution and correct mathematical equation remain the same.','observed':'Exact prompt, solution and response equality, different displayed order, native acceptance of the correct equation and visual agreement in screenshots 001 and 009. Publisher removes the duplicate permutation as expected.','status':'passed','justification':'The radio position is incidental to I′=PI. Every substantive ODE coefficient affects the complete equation, so permutation is the applicable irrelevant dependency.','sample_refs':cfrefs}
 ],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['generator attempt validation and resampling','requested easy filtering','actual publisher normalization, validation and stable identities','captured inventory and within-batch deduplication','captured inventory freshness and difficulty-weighted selection scenarios; prospective-survivor scenarios'], 'sample_refs':['generator-rejection-trace.json','delivery-selection-results.json','delivery-samples/accepted.json','delivery-samples/delivery.json','delivery-batch/accepted.json','delivery-batch/delivery.json','delivery-counterfactuals/accepted.json','delivery-counterfactuals/delivery.json','delivery-shortcut-results.json','delivered-grader-report.json'],'result':'Fresh easy 24→24; runner 5→5; controlled 22→21 solely duplicate permutation. All distinct controlled target roles survive. No sampled easy resampling bias. Actual Rust selection rules use rating, identity and freshness, not factor shape or key; conditioned prospective scenarios retain all four easy families. No publication preparation exists. Captured old defective items remain recorded separately.'},
 'limitations':['Bounded revision review reuses original independent source analysis and unchanged-source replay evidence with provenance. No second exhaustive audit of unchanged moderate/hard construction.','No finite audit proves absence of every shortcut; chosen cues include within-template probes and controlled bank-only identifiability checks.','Same six fresh seeds across templates share coefficient-bank draws; subgroup repetitions are not independent statistical trials.','Source keys/solutions missing on two practice records were inferred from the displayed ODE, never asserted as observed source links.','No actual learner history or policy weights supplied; selection conditions are explicit scenarios, prospective database IDs are surrogate IDs, and future changing inventory may alter draws.','Captured historical inventory contains three affected generated easy records; current generator acceptance does not certify those old items or perform inventory repair.']
}
save('pedagogical-variation.json',variation)
# Basic recursive schema validation without adding a runtime dependency.
schema=load(R.REPO/'generate/pipeline/pedagogical-variation.schema.json')
def validate(v,s,p='$'):
 if 'enum' in s:assert v in s['enum'],(p,v)
 typ=s.get('type')
 if typ=='object':
  assert isinstance(v,dict),p
  for k in s.get('required',[]):assert k in v,(p,k)
  if s.get('additionalProperties')==False:assert not set(v)-set(s.get('properties',{})),p
  for k,x in v.items():
   if k in s.get('properties',{}):validate(x,s['properties'][k],p+'.'+k)
 elif typ=='array':
  assert isinstance(v,list) and len(v)>=s.get('minItems',0),p
  for i,x in enumerate(v):validate(x,s.get('items',{}),p+f'[{i}]')
 elif typ=='string':assert isinstance(v,str) and len(v)>=s.get('minLength',0),p
 elif typ in ('integer','number'):
  assert isinstance(v,int if typ=='integer' else (int,float)) and not isinstance(v,bool),p
  assert s.get('minimum',float('-inf'))<=v<=s.get('maximum',float('inf')),p
validate(variation,schema)
def check(details,paths):return {'status':'passed','evidence_paths':paths,'details':details}
a=load(H/'source-analysis.json')
result={
 'verdict':'accepted',
 'summary':'The revision resolves both retained generator defects. All eight checks pass. Three affected historical inventory records remain documented separately; package unchanged and no database writes.',
 'source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
 'checks':{
  'source_replay':check('Eight complete practice banks and canonical replay verified; captured source gaps/corrections explicitly retained.',['source-analysis.json','source-replay-results.json','source-replay-records.json','strict-regression-execution.json','author-check-verification.json']),
  'math':check('Independent exact checks of 64 raw and 50 delivered records verify unique correctness and printed multiplication/product-derivative solution rows.',['math-results.json','delivery-math-results.json','samples.json','boundary-records.json']),
  'variety':check('Four easy families retain signed/rational coefficients, forcing and normalization variation. Fixed-bank target reassignment defeats the old bank cue and survives delivery.',['counterfactual-results.json','shortcut-results.json','delivery-selection-results.json','retained-findings-results.json']),
  'scope':check('Changed easy banks and canonical exponential forcing preserve source Steps 1–4 and workload; no ODE solving is added.',['scope-results.json','source-analysis.json','samples.json']),
  'grading':check('Native learner grader: 114 expected acceptances and 460 rejections, including stale responses after relevant changes and all delivered answer choices. Radio contract needs no free-entry equivalence test.',['grader-input.json','grader-report.json','delivered-grader-input.json','delivered-grader-report.json']),
  'rendering':check('Eleven actual UI screenshots passed automated and visual inspection, including each changed easy template, controlled pairs and canonical case.',['render/rendering.json','render-inspection.json','render-input.json']+[f'render/question-{i:03}.png' for i in range(1,12)]),
  'packaging':check('Exact Python/SymPy manifest versions, deterministic replay, 13 rejection boundaries and relocation using only declared runtime files pass; original package hashes unchanged.',['packaging-results.json','package-before.json','original-cli.json','relocated-cli.json','implementation.diff']),
  'decision_variation':check('Relevant and irrelevant dependencies, conditional cue probes and actual delivery/selection stages examined. Both strict regressions fail old code and pass current. Historical affected inventory is retained for separate remediation.',['pedagogical-variation.json','counterfactual-records.json','strict-regression-execution.json','delivery-shortcut-results.json','delivery-selection-results.json','affected-inventory.json','generated-records.json'])
 },
 'findings':[]
}
save('result.json',result)
# Every report and decision reference resolves to nonempty created evidence.
refs=[]
def walk(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k in ('sample_refs','evidence_paths'):refs.extend(x)
   else:walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(result);walk(variation)
for ref in refs:
 p=pathlib.Path(ref);assert not p.is_absolute() and '..' not in p.parts,ref
 assert (H/p).is_file() and (H/p).stat().st_size>0,ref
save('evidence-contract-check.json',{'pedagogical_schema_passed':True,'reference_count':len(refs),'all_relative_nonempty_files':True,'original_package_unchanged':A.snapshot()==load(H/'package-before.json'),'strict_regression_expected_exits':[1,1,0,0],'database_writes':0,'all_eight_checks_passed':True})
(H/'session-state.md').write_text('Review complete. result.json verdict accepted for current generator. All eight checks passed; both old defects independently reproduced then cleared. 64 raw + 50 delivered mathematical records; native 114 acceptances and 460 rejections; 11 actual UI screenshots inspected. Three historical affected inventory records retained with original metadata in affected-inventory.json and generated-records.json, separately from current-generator acceptance. All writes under evidence_root; package snapshot unchanged; no database or publication writes.\n')
print(json.dumps({'verdict':result['verdict'],'checks':{k:v['status'] for k,v in result['checks'].items()},'evidence_references':len(refs),'package_unchanged':True}))
