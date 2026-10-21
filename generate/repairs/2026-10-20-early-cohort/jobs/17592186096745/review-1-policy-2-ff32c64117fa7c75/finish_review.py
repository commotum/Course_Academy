"""Assemble and validate this review's report from completed independent checks."""
import hashlib, json
from pathlib import Path
from review_math import check, correct_index, prompt, semantic

ROOT = Path(__file__).resolve().parent
REPO = Path('/home/jake/Developer/Course_Academy')
PY = str(REPO / '.venv/bin/python')
def load(p): return json.loads((ROOT / p).read_text())
def save(p, value): (ROOT / p).write_text(json.dumps(value, indent=2, default=str) + '\n')

assert load('source-verification.json')['passed']
assert len(load('source-replay-results.json')) == 17
assert all(r['passed'] for r in load('source-replay-results.json'))
assert not load('math-results.json')['failures']
assert not any(r['errors'] for r in load('shortcut-controls-math.json'))
assert load('grader-all-results.json')['accepted_checks'] == 59
assert load('grader-all-results.json')['rejected_checks'] == 236
assert load('render/rendering.json')['passed']
assert len(load('render/rendering.json')['cases']) == 15
assert all(r['rejected'] for r in load('generator-rejection.json'))
assert load('regression-verification.json')['current']['exit'] == 0
assert load('regression-verification.json')['failing_example']['exit'] == 1

delivery = []
for inp, out in [('independent-samples.json', 'delivery-independent'), ('runner-batch.json', 'delivery-batch'), ('counterfactual-records.json', 'delivery-counterfactual'), ('shortcut-controls.json', 'delivery-controls')]:
    raw = load(inp); accepted = load(out + '/accepted.json')
    assert len(raw) == len(accepted)
    for before, after in zip(raw, accepted):
        a, b = before['question'], after['question']
        same = prompt(a) == prompt(b) and correct_index(a) == correct_index(b) and [semantic(x[':answer/value']) for x in a[':question/answer-fields'][0][':answer-field/choices']] == [semantic(x[':answer/value']) for x in b[':question/answer-fields'][0][':answer-field/choices']]
        result = check(after)
        assert same and not result['errors']
        delivery.append({'stage': out, 'raw_id': a[':question/id'], 'accepted_id': b[':question/id'], 'same_prompt_answer_bank_key': same, 'math': result})
save('delivery-semantic-results.json', {'command': 'finish_review.py', 'records': delivery, 'passed': True})

save('affected-inventory.json', {'affected_questions': []})
inventory = load('inventory-audit.json')
inventory['conclusion'] = 'No affected generated instance demonstrated for retained missing-source API capability; repair now supports both profiles. Five captured non-source records pass independent math. Historical seeds/generation metadata absent, so absence of other historical defects is not certified.'
save('inventory-audit.json', inventory)
save('visual-inspection.json', {'renderer': 'Unmodified UI, MathJax/fonts settled', 'automated_cases': 15, 'all_passed': True, 'screenshots_inspected': ['render/question-' + n + '.png' for n in ['001','003','006','007','008','009','010','011','014','015']], 'observations': ['Both restored source profiles display complete five-choice banks and original worked reductions.', 'Both response families and all controlled-pair prompts/results legible; relevant changes reverse signs and alter the selected mathematical result, while row reorder/sign changes preserve the result.', 'No visible clipping or TeX error; radio controls and matrices/parameter vectors display correctly.', 'Green feedback is produced by the preview after submitting the key; it is not a pre-answer cue.'], 'limits': ['Desktop rendering inspected; no claim for every viewport or seed.']})
save('scope-results.json', {'basis': 'source-analysis.json; tutorial 3949 and all 17 assessed questions', 'records_checked': 59, 'result': 'Consistent rank-two 3x3 systems; pivots in x,y, free z; matrix and vector response families; five radio choices. Source-shaped normalization, swaps, elimination and conditional backward clearing preserved. No additional operators, prerequisites or response requirements.', 'restored_cases': {'q-74625': 'Second pivot already normalized; backward clearing needed.', 'q-131634': 'Second pivot scaling needed; backward entry already zero.'}, 'boundaries': 'Explicit slopes -3/+3, intercepts -4/+4, and all-zero affine candidate checked in the bank; out-of-domain parameters rejected. Sample domain conservative; full source values replay.'})
pkg = ROOT.parent / 'workspace'
hashes = {str(p.relative_to(pkg)): hashlib.sha256(p.read_bytes()).hexdigest() for p in pkg.rglob('*') if p.is_file()}
assert hashes == load('package-hashes-before.json')
save('package-hashes-after.json', hashes)

def passed(paths, details): return {'status': 'passed', 'evidence_paths': paths, 'details': details}
source = load('source-analysis.json')
report = {'verdict': 'accepted', 'summary': 'The two missing source profiles are restored. All eight checks pass on the revision and exact five-record batch; no remaining defect demonstrated. Package unchanged; no publication or database writes.', 'source_analysis': {k: source[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']}, 'checks': {
    'source_replay': passed(['source-analysis.json','source-verification.json','source-replay-results.json','replays.json','regression-verification.json','captured-source-comparison.json'], 'All 17 assessed prompts, complete ordered banks (85 choices), keys and worked matrix sequences match original source; supported row-label correction retained. Regression passes current package copy and fails the restored old omission fixture.'),
    'math': passed(['math-results.json','shortcut-controls-math.json','review_math.py','audit.py','delivery-semantic-results.json'], '59 raw records independently checked with exact SymPy reconstruction, including 17 source replays, 21 fresh samples, five exact batch records, six controlled-pair records and 10 cue controls. Unique valid option, RREF/affine vector and worked reductions pass. All 42 delivered test records preserve semantics and pass math.'),
    'variety': passed(['coverage-results.json','independent-samples.json','runner-batch.json','delivery-independent/delivery.json','delivery-batch/delivery.json','generator-rejection.json'], 'Fresh sample covers all 17 profiles, both response families, all five correct slots, signed/zero affine parameters and 21 distinct RREFs. Exact batch has five distinct RREFs: four vector and one matrix item. All fresh and batch records survive actual delivery filtering.'),
    'scope': passed(['source-analysis.json','scope-results.json','source-verification.json'], 'Restored profiles and tested variations preserve source-supported rank-two Gauss-Jordan workload and response forms. Fixed first two pivot columns are justified by tutorial scope; eligible slopes, constants and qualifying options vary.'),
    'grading': passed(['grader-all-input.json','grader-all-results.json'], 'Native grade_field accepts 59 independently verified keys and rejects 236 alternatives, including the old target after relevant changes. All assessed source fields are radio, so free-entry equivalent notation is inapplicable.'),
    'rendering': passed(['render/rendering.json','visual-inspection.json','render-input.json','render/question-014.png','render/question-015.png','render/question-007.png','render/question-010.png'], 'Actual UI renders 15 records, including all five batch records, all six controlled-pair records and both restored source replays. Automated checks pass; 10 representative screenshots inspected.'),
    'packaging': passed(['packaging-results.json','generator-rejection.json','relocation-samples.json','package-hashes-before.json','package-hashes-after.json','revision-comparison.json'], 'Exact declared Python 3.13.5 and SymPy 1.14.0 match runtime. Deterministic CLI, relocation, invalid-parameter rejection and JSON stdout checks pass. All recursive package hashes unchanged.'),
    'decision_variation': passed(['pedagogical-variation.json','counterfactual-records.json','counterfactual-results.json','decision-probe-results.json','shortcut-control-results.json','rendered-choice-results.json','learner-selection-results.json','selection-pool-results.json','delivery-semantic-results.json'], 'Relevant and irrelevant controlled changes follow through equations, answers, worked solutions, real grading and rendered controls in both families. Conditional position/length/sign/zero probes demonstrate no incidental shortcut, including the exact batch. Actual delivery preserves support; all 27 captured-plus-prospective records have support under fresh positive-hard-weight selection. Live policy/history and future IDs remain unobserved.')}, 'findings': []}

def validate(v, s, path='$'):
    t = s.get('type')
    if t:
        assert {'object': isinstance(v,dict), 'array': isinstance(v,list), 'string': isinstance(v,str), 'integer': type(v)==int, 'number': type(v) in (int,float), 'boolean': type(v)==bool}[t], (path,t)
    if 'enum' in s: assert v in s['enum'], path
    if 'minLength' in s: assert len(v) >= s['minLength'], path
    if 'minItems' in s: assert len(v) >= s['minItems'], path
    if 'minimum' in s: assert v >= s['minimum'], path
    if 'maximum' in s: assert v <= s['maximum'], path
    if isinstance(v,dict):
        for k in s.get('required',[]): assert k in v, (path,k)
        if s.get('additionalProperties') is False: assert not set(v)-set(s['properties']),path
        for k,c in v.items():
            if k in s.get('properties',{}): validate(c,s['properties'][k],path+'.'+k)
    elif isinstance(v,list):
        for j,c in enumerate(v): validate(c,s.get('items',{}),path+f'[{j}]')
def refs(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ('sample_refs','evidence_paths'):
                for p in v:
                    f=ROOT/p
                    assert not Path(p).is_absolute() and f.is_file() and f.stat().st_size>0,(k,p)
            else: refs(v)
    elif isinstance(o,list):
        for v in o: refs(v)
variation = load('pedagogical-variation.json')
validate(variation, json.loads((REPO/'generate/pipeline/pedagogical-variation.schema.json').read_text()))
refs(variation); refs(report)
assert len(report['checks']) == 8
save('review-result.json', report)
save('result.json', report)
save('evidence-contract.json', {'pedagogical_schema_valid': True, 'all_evidence_paths_nonempty': True, 'all_sample_refs_nonempty': True, 'eight_checks_passed': True, 'package_unchanged': True, 'retained_finding_reproduced_on_failing_fixture': True, 'retained_finding_resolved_current': True, 'native_checks': 295, 'render_cases': 15, 'affected_inventory_records_demonstrated': 0, 'limits': 'Captured basis 5370, unavailable historic generation metadata and live learner policy/history; no claim of exhaustive shortcut absence.'})
(ROOT/'session-state.md').write_text('Review complete: accepted; review-result.json and result.json contain final report. Source 17/17 full banks (85 choices) externally confirmed; prior omission regression fails isolated old fixture and passes current. Independent math 59 raw records and 42 post-delivery records; native grader 59 accepts/236 rejects; actual UI 15 cases, 10 screenshots inspected. Exact batch 5 distinct RREFs, 4 vector/1 matrix; all survive delivery; no tested batch shortcut. Both relevant/irrelevant pairs tested in each response family. Captured inventory 22 plus 5 prospective records retains support under positive hard weighting; live policy/history and future IDs unavailable. No affected generated inventory instance demonstrated for retained capability defect; no invented provenance. Recursive package hashes unchanged. No package edits, publication or database writes. Evidence schema/path contract passes.\n')
print(json.dumps({'verdict': report['verdict'], 'checks': {k:v['status'] for k,v in report['checks'].items()}, 'package_unchanged': True}))
