import sys
sys.dont_write_bytecode=True
import review as v
import json,pathlib
R=v.R;read=v.read;save=v.save
before=read(R/'package-hashes-before.json');after=v.hashes();save('package-integrity.json',{'unchanged':before==after,'files_checked':len(before),'changed':[k for k in set(before)|set(after) if before.get(k)!=after.get(k)],'after':after});assert before==after
m=v.m
extra=[]
for args in [('moderate',5,1),('hard',5,1),('easy',0,1)]:
 try:m.batch(*args);passed=False
 except ValueError:passed=True
 extra.append({'arguments':args,'rejected':passed})
p=read(R/'packaging.json');p['invalid_batch_requests']=extra;p['package_unchanged']=True;save('packaging.json',p)
a=read(R/'source-analysis.json')
source_analysis={k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']}
def check(status,paths,details):return {'status':status,'evidence_paths':paths,'details':details}
result={'verdict':'revise','summary':'New boundary defect: a=1, b=0 renders as x0 throughout the question and solution. CLI seed 575 produces five malformed records that survive delivery filtering. Both previous findings are resolved; the runner’s current batch is valid. Package unchanged.','source_analysis':source_analysis,'checks':{
'source_replay':check('passed',['source-analysis.json','source-replay.json','source-replay-records.json','retained-findings-review.json'],'All six complete answer banks and captured prompts replay; existing solutions match. Canonical replay matches. Missing q-49511 key/solution reconstructed and independently differentiated.'),
'math':check('failed',['minimal-failure.json','math.json','zero-intercept-regression.py','zero-intercept-regression.json','delivered-zero-intercept-regression.json'],'generate(parameters=[2,1,0], seed=70519) emits 2/x0 and 2 ln|x0|+C. The intended denominator is x. All five CLI seed-575 records retain this defect after delivery. Sixty other checked records, including the actual runner batch, have unique correct antiderivatives.'),
'variety':check('passed',['coverage-and-shortcuts.json','samples.json','boundary-records.json','controls.json'],'Both new bank profiles vary eligible coefficient/argument roles. Positive nonunit slopes are now supported. Fresh samples cover both slope signs and multiple intercept cases; malformed zero-intercept output is reported separately under math.'),
'scope':check('passed',['scope.json','source-analysis.json'],'Construction preserves easy single-affine reciprocal substitution and five-choice radio responses. No additional integration operation or prerequisite was introduced.'),
'grading':check('passed',['grader-input.json','grader-report.json','malformed-grader-input.json','malformed-grader-report.json'],'Native grader accepted 60 independently verified correct choices and rejected 240 distractors. Radio-only response contract has no free-entry equivalents. It also accepts the malformed record’s declared UUID; this confirms the content defect is not blocked, not that its mathematics is valid.'),
'rendering':check('failed',['render/rendering.json','render-remaining/rendering.json','render-inspection.json','render/question-001.png'],'Actual UI visibly renders x0 in the denominator, choices and substitution solution. No MathJax syntax error occurs, but the displayed mathematics is wrong. Other inspected counterfactual and current-batch screens display correctly.'),
'packaging':check('passed',['packaging.json','package-integrity.json','relocation-command.json','retained-before.json','retained-current.json'],'Exact installed dependency versions match the manifest. Declared-file relocation, deterministic batch/replay, invalid-request rejection and unchanged package hashes verified. Retained regressions fail on the old package and pass on the revision.'),
'decision_variation':check('passed',['pedagogical-variation.json','coverage-and-shortcuts.json','counterfactuals.json','selection-analysis.json','delivery-batch/delivery.json','inventory-review.json','affected-inventory.json'],'Both controlled profiles change keys, prompts, solutions and native grading with relevant target changes; option-order changes preserve responses. The actual delivered batch uses each of five bank values as a key; historical shortcut succeeds 0/5. Conditional bank/position probes and selection limits are documented. Captured inventory contains no generated records.')},
'findings':[{'kind':'math','description':'The affine formatter emits x0 when a=1 and b=0. This changes the supported integrand n/x into n/(x·0), makes ln|x0| undefined, and accompanies it with the false statement d(x0)/dx=1. Both target expressions and distractor arguments use this formatter. The defect occurs in normal generation and survives publication filtering; it is not present in the runner’s current five-record batch.','source_refs':['tutorial 933683cf-f7fa-50f2-9f11-4522ca637c77: The General Formula','625c532a-d455-5b15-880d-e9fc5ae8ee72: reciprocal integration prerequisite','d6501a20-6ebd-5786-870e-3527423b6332'],'reproduction':'From evidence_root run /home/jake/Developer/Course_Academy/.venv/bin/python zero-intercept-regression.py (exits 1; explicit parameters [2,1,0], seed 70519). Normal CLI: the same Python executable ../workspace/17592186064206.py --difficulty easy --count 5 --seed 575 --format json. Complete CLI records are in cli-seed-575.json; delivery survivors in delivery-natural-boundary-records/accepted.json. Running zero-intercept-regression.py --candidate-records delivery-natural-boundary-records/accepted.json --output delivered-zero-intercept-regression.json fails 5/5. UI evidence: render/question-001.png.','requested_change':'Fix the shared denom(a,b) rule to render zero intercept correctly, including a=1, and propagate the corrected expression to prompts, every answer choice and solutions. Keep zero-intercept practice eligible. Adopt the retained executable regression and include unit/negative/nonunit slopes with zero intercept in boundary tests; verify native grading and actual rendered output after repair.'}]}
save('result.json',result)
# Validate the required evidence paths, not just JSON syntax.
import subprocess
subprocess.run(['python3','-c', 'import json,jsonschema;jsonschema.validate(json.load(open('+repr(str(R/'pedagogical-variation.json'))+')),json.load(open('+repr(str(v.REPO/'generate/pipeline/pedagogical-variation.schema.json'))+')))'],check=True)
paths=set(result['source_analysis']['evidence_paths'])
for c in result['checks'].values():paths.update(c['evidence_paths'])
def collect(x):
 if isinstance(x,dict):
  for k,val in x.items():
   if k=='sample_refs':paths.update(val)
   collect(val)
 elif isinstance(x,list):
  for val in x:collect(val)
collect(read(R/'pedagogical-variation.json'))
for rel in paths:
 p=R/rel;assert not pathlib.Path(rel).is_absolute() and p.is_file() and p.stat().st_size>0,rel
assert set(result['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
save('evidence-validation.json',{'pedagogical_variation_schema':'passed','nonempty_relative_evidence_files_checked':len(paths),'eight_checks_present':True,'package_unchanged':True,'finding_reproduction_exit_codes':{'minimal':1,'delivered_seed575':1,'retained_old':1,'retained_current':0}})
(R/'session-state.md').write_text('Completed review: revise. One demonstrated math/notation defect: denom(1,0) emits x0. Minimal [2,1,0], seed70519; normal CLI seed575 has 5/5 defective delivery survivors. Previous shortcut and positive-slope findings resolved. All eight checks assessed; actual UI inspected, native grader exercised, delivery/selection/inventory analyzed. No historical generated records present. result.json and schema/path-validated evidence saved. Package hashes unchanged.\n')
print(json.dumps({'verdict':result['verdict'],'checks':{k:c['status'] for k,c in result['checks'].items()},'findings':len(result['findings']),'evidence_files_validated':len(paths),'package_unchanged':True}))
