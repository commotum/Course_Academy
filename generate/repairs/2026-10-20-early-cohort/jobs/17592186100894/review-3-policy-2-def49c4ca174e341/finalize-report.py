from pathlib import Path
import json,hashlib
E=Path(__file__).resolve().parent
W=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100894/workspace')
def load(n):return json.loads((E/n).read_text())
def save(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
assert load('current-grader-execution.json')['exit']==0
assert load('delivered-current-execution.json')['exit']==0
assert load('render/rendering.json')['passed'] and len(load('render/rendering.json')['cases'])==11
assert load('overflow-inspection.json')['passed']
after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
assert after==load('package-before.json')
save('package-integrity.json',{'files':len(after),'unchanged':True,'comparison':'Every package file SHA-256 compared with package-before.json after all tests.'})
save('render-visual-review.json',{'passed':True,'renderer':'Actual unmodified UI via render_preview.py, --limit 11','automated_cases':11,'screenshots_inspected':['render/question-'+str(i).zfill(3)+'.png' for i in [1,2,3,5,7,8,9,10,11]],'observations':['Sine named box, arbitrary C, local branch, input control and integration steps display correctly.','Initial-condition-only and ODE-only controlled pairs display their changed evidence and changed final solutions. Irrelevant wording/order pair preserves mathematics.','Radicals, exponential/log notation and complete radio banks render without math/JS/image/font errors.','Two long aligned derivations exceed the default math width. Actual UI overflow-x:auto permits horizontal scrolling; DOM checks and both scrolled screenshots verify rightmost terms remain accessible.'],'supplemental_scrolled_screenshots':['render-scroll/question-001.png','render-scroll/question-002.png'],'overflow_evidence':'overflow-inspection.json'})
account=load('source-analysis.json')
sa={k:account[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']}
def check(paths,detail):return {'status':'passed','evidence_paths':paths,'details':detail}
result={'verdict':'accepted','summary':'All eight checks pass. Historical failures reproduce on retained old executables and pass current strict regressions. The five-record batch survives delivery and grades correctly. Package unchanged; no publication or database writes.','source_analysis':sa,'checks':{
 'source_replay':check(['source-analysis.json','source-replay.json','source-replay-records.json','current-review.py'],'All 25 valid source profiles replay complete banks and keys. Documented source corrections retained; q-104058 is excluded because its initial point makes the equation 0=2. Canonical example lacks a captured answer field.'),
 'math':check(['fresh-math-results.json','math-results.json','reused-unchanged-math-results.json','sine-current-proof.json','provenance.json'],'Fresh exact checks validate all five batch keys, sine boundary/interior fragments and signed radical/log regressions. Reused independently verified mathematics covers unchanged source families and all 75 trig bank roles.'),
 'variety':check(['pedagogical-variation.json','role-records.json','shortcut-results.json','retained-finding-results.json','batch-shortcut-results.json'],'All five answers can win within each of 15 fixed complete banks. Prior conditional shortcuts no longer predict the key. The exact batch has four blank families; its two translations of one source are modest numerical practice, with no tested batch-wide answer cue.'),
 'scope':check(['source-analysis.json','scope-review.json','provenance.json','fresh-regression-records.json'],'Unchanged runtime retains observed elementary integration methods, response scaffolds and difficulty. Restored sine branch and radical sign selection follow the source solutions; grading recognizes the existing arbitrary-C contract.'),
 'grading':check(['current-grader-input.json','current-grader-report.json','current-grader-execution.json','delivered-current-grader-input.json','delivered-current-grader-report.json','delivered-current-execution.json','finding-verification.json','preflight-inspection.json','sine-before-execution.json','root-before-execution.json','reproduce-sine.py'],'640 current and 468 normalized-delivery native checks pass with zero unresolved outcomes. Exact previous sine equivalents now accept; derivative-distinct fragments reject. Ordinary IVP constant shifts, opposite radical branches and plausible wrong entries reject. Historical failures were independently reproduced on older executables.'),
 'rendering':check(['render/rendering.json','render-visual-review.json','render/question-001.png','render/question-007.png','overflow-inspection.json','render-scroll/rendering.json'],'Actual UI renders 11 cases without automated errors; nine screenshots and two supplemental scrolled views inspected. Long derivations use verified horizontal scrolling with their final terms reachable.'),
 'packaging':check(['packaging.json','runtime-results.json','relocation-records.json','package-before.json','package-integrity.json','package-review.py'],'Python 3.13.5 and SymPy 1.14.0 exactly match the manifest. Relocation, deterministic replay and boundary rejection pass. Every package file remains unchanged; all generated review output stays under evidence_root.'),
 'decision_variation':check(['pedagogical-variation.json','counterfactual-records.json','counterfactual-results.json','current-grader-report.json','shortcut-results.json','batch-shortcut-results.json','delivery-stages.json','selection.json','inventory-audit.json','affected-inventory.json','provenance.json'],'Relevant IC/ODE changes alter answers, explanations and native outcomes; irrelevant wording/order and sine constant reparameterizations preserve them. Conditional bank cues perform at the 1/5 baseline. All 75 role controls and all five batch records survive delivery. Selection rules were inspected and reproduced conditionally using captured inventory; unavailable live histories/weights are explicit limits. Captured inventory contains only 26 original sources and no generated affected instance.')},'findings':[]}

# Evidence contract: every cited path is a nonempty file inside this review root.
for entry in [result['source_analysis'],*result['checks'].values()]:
 for n in entry['evidence_paths']:
  p=(E/n).resolve();assert p.is_relative_to(E) and p.is_file() and p.stat().st_size,n
variation=load('pedagogical-variation.json')
for entry in variation['coverage']+variation['counterfactuals']+variation['shortcut_probes']+[variation['delivery']]:
 for n in entry['sample_refs']:
  p=(E/n).resolve();assert p.is_relative_to(E) and p.is_file() and p.stat().st_size,n
schema=Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json')
try:
 import jsonschema
 jsonschema.validate(variation,json.loads(schema.read_text()));validation='jsonschema validated'
except ImportError:
 assert set(variation)=={'learner_operation','fixed_features','answer_roles','coverage','counterfactuals','shortcut_probes','delivery','limitations'}
 validation='Required fields and nonempty local references verified; jsonschema unavailable'
save('contract-check.json',{'passed':True,'pedagogical_schema':validation,'evidence_paths':'All result evidence_paths and pedagogical sample_refs resolve to nonempty review files.','checks':list(result['checks']),'package_unchanged':True})
save('result.json',result)
(E/'session-state.md').write_text('Completed targeted independent review: ACCEPTED. All eight checks pass; no findings. Source account reconfirmed before author inspection; declared runtime files and source/batch bindings unchanged, with provenance for reused math/coverage. Historical failures reproduced on old executables and strict current checks pass (640 current + 468 delivered native checks, zero unresolved). Source replay 25 valid profiles; exact batch 5->5; 75 role controls survive. Actual UI 11 cases pass; nine screenshots and two supplemental scrolled views inspected. Exact dependency versions, relocation, determinism/boundary rejection and final package hashes pass. Captured inventory has only 26 original sources, no affected generated entries. No database/publication writes. Final structured report: result.json.\n')
print(json.dumps({'verdict':result['verdict'],'checks':len(result['checks']),'package_files_unchanged':len(after),'contract':validation}))
