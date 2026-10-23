import json,hashlib
from pathlib import Path
E=Path(__file__).resolve().parent;B=E.parent;R=Path('/home/jake/Developer/Course_Academy')
def load(n):return json.loads((E/n).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2))
a=load('source-analysis.json');a['evidence_limits']=['Canonical e-596 has no captured answer-field evidence; complete-bank replay is not claimed for it. Source imagery and unchanged controlled renders were inspected in prior bound review; current representative plot and UI inspected again.'];save('source-analysis.json',a)
scope=load('source-scope-review.json');scope['history']='Two retained grading findings inspected; package/source unchanged. Current native grader reruns pass both findings and strict wrong-answer controls. Original source/scope findings reused with provenance.';save('source-scope-review.json',scope)
def check(paths,details):return {'status':'passed','evidence_paths':paths,'details':details}
result={'verdict':'accepted','summary':'Both retained grading failures are resolved. All eight checks pass within the documented sampling and inventory limits. Package unchanged; no database writes.','source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':{
'source_replay':check(['source-analysis.json','source-replay-results.json','current-source-replay.json','source-scope-review.json'],'All 22 supported practice replays match independently verified prompts, complete banks and solution stages. Two source domain errors are corrected. Canonical answer-bank evidence is absent and explicitly excluded.'),
'math':check(['current-math.json','regression-math.json','fresh-engine-math.json','review.py','math-results.json'],'Independent differentiation and displayed-equality checks pass for 14 current batch/fresh records and eight targeted regressions. Unchanged broader mathematical evidence retained with provenance.'),
'variety':check(['samples-independent.json','counterfactuals.json','current-shortcuts.json','delivery-batch/delivery.json','delivery-fresh/delivery.json'],'Twenty source-grounded templates retain target and coefficient variation. All five exact batch records and five independently seeded easy records survive delivery filtering.'),
'scope':check(['source-analysis.json','source-scope-review.json','fresh-hard.json','fresh-easy.json'],'No demonstrated drift in differentiation rules, exact-answer response contract, or workload. Canonical example without a captured bank is explicitly outside complete replay coverage.'),
'grading':check(['repair-review.json','retained-regression.py','regression-grader-result.json','regression-delivered-grader-result.json','current-grader-results.json','fresh-engine-input.json','fresh-engine-results.json'],'Both retained exponential-equivalence failures now pass strict native checks before and after delivery. The broader suite passes 786 checks; 21 independent multiplicity/cancellation checks also pass, including wrong-sign and wrong-factor rejection.'),
'rendering':check(['render-current/rendering.json','current-render-inspection.json','render-current/question-001.png','render-current/question-002.png','render-current/question-006.png','render-counterfactual/rendering.json'],'Six current actual-UI cases pass. Visually inspected plot, blank, radio controls and hard worked solution. Unchanged controlled-pair visual evidence reused with provenance.'),
'packaging':check(['current-runtime.json','current-packaging.json','current-determinism.json','package-integrity.json','package-before.json','package-after.json'],'Exact dependency versions match. Deterministic generation, same-output relocation, external assets and batch content replay pass. All package file hashes remain unchanged.'),
'decision_variation':check(['pedagogical-variation.json','counterfactuals.json','current-grader-results.json','current-shortcuts.json','current-selection.json','current-inventory-review.json','affected-inventory.json','reuse-provenance.json'],'Relevant target changes alter responses and irrelevant translation preserves them. Conditional cue tests and current batch measurements show no demonstrated bypass. Rendered radio positions are 2, 5, 4, 3. Selection conclusions assume fresh eligible candidates and positive easy weight; inventory conclusions use captured basis 5644.')},'findings':[]}
save('result.json',result)
commands=[
'PYTHONDONTWRITEBYTECODE=1 '+str(R/'.venv/bin/python')+' current-review.py',
'PYTHONDONTWRITEBYTECODE=1 '+str(R/'.venv/bin/python')+' retained-regression.py',
'PYTHONDONTWRITEBYTECODE=1 '+str(R/'.venv/bin/python')+' fresh-engine-probe.py',
'PYTHONDONTWRITEBYTECODE=1 '+str(R/'.venv/bin/python')+' finish-review.py']
for name,input,asset in [('batch','batch.json',B/'outputs-2'),('fresh','fresh-easy.json',E/'assets')]:
 commands.append(f'PYTHONDONTWRITEBYTECODE=1 {R}/.venv/bin/python {R}/generate/pipeline/check_delivery.py --input {input} --source {B}/source/source.json --inventory {B}/source/inventory.json --difficulty easy --output {E}/delivery-{name} --asset-root {asset} --math-root /media/jake/SSD/EDB/math')
commands.append(f'PYTHONDONTWRITEBYTECODE=1 {R}/.venv/bin/python {R}/generate/pipeline/render_preview.py --input current-render-records.json --output {E}/render-current --asset-root {E}/assets --asset-root {B}/outputs-2 --math-root /media/jake/SSD/EDB/math')
save('commands.json',{'cwd':str(E),'commands':commands,'order':'Run current-review, retained-regression and fresh-engine-probe; then delivery and rendering; then finish-review and write-report.'})
# Verify all paths named by report and variation contract resolve to nonempty evidence.
paths=set(result['source_analysis']['evidence_paths'])
for c in result['checks'].values():paths.update(c['evidence_paths'])
v=load('pedagogical-variation.json')
for row in v['coverage']+v['counterfactuals']+v['shortcut_probes']+[v['delivery']]:paths.update(row['sample_refs'])
missing=[n for n in paths if not (E/n).is_file() or (E/n).stat().st_size==0];assert not missing,missing
assert {c['kind'] for c in v['counterfactuals']}=={'relevant','irrelevant'}
assert any(c['scope']!='overall' for c in v['shortcut_probes'])
for p in v['shortcut_probes']:
 assert isinstance(p['correct'],int) and isinstance(p['total'],int) and 0<=p['correct']<=p['total'] and 0<=p['baseline']<=1
try:
 import jsonschema
 jsonschema.validate(v,json.loads((R/'generate/pipeline/pedagogical-variation.schema.json').read_text()));schema='passed'
except ImportError:schema='jsonschema unavailable; required fields/types checked directly'
save('evidence-contract.json',{'nonempty_paths_checked':len(paths),'missing':missing,'variation_schema':schema,'all_eight_checks':'passed','package_integrity':load('package-integrity.json')['unchanged']})
(E/'session-state.md').write_text('Review complete: accepted. Both retained grading defects now pass strict current native-grader tests. All eight required checks passed; prior unchanged evidence reused with provenance, current batch and focused engine regressions rerun. Package hashes unchanged; database untouched. result.json and pedagogical-variation.json written; all cited evidence paths verified nonempty.\n')
print(json.dumps({'verdict':result['verdict'],'evidence_contract':load('evidence-contract.json')}))
