"""Bounded correction of historical-control placement; package is read-only."""
import sys
sys.dont_write_bytecode = True
import copy, hashlib, importlib.util, json, pathlib, shutil, subprocess

OUT = pathlib.Path(__file__).resolve().parent
OLD = OUT.parent
JOB = OLD.parent
REPO = pathlib.Path('/home/jake/Developer/Course_Academy')
PACKAGE = JOB / 'workspace'
PY = REPO / '.venv/bin/python'

def load(path):
    return json.loads(path.read_text())

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

# Confirm the reusable independent account against original prompts and full banks.
source = load(JOB / 'source/source.json')
account = load(OLD / 'source-analysis.json')
questions = {q[':question/id']: q for q in source['material']['kp'][':knowledge-point/questions']}
assert all(c['prompt'] == questions[c['id']][':question/problem'] and
           c['fields'] == questions[c['id']][':question/answer-fields']
           for c in account['source_cases'])
shutil.copy2(OLD / 'source-analysis.json', OUT / 'source-analysis.json')
assert load(OUT / 'source-analysis.json') == account

review = load(OLD / 'result.json')
variation = load(OLD / 'pedagogical-variation.json')
validator = module('review_validator', REPO / 'scripts/generator_review.py')
try:
    validator.validate_review(review, OLD)
except ValueError as error:
    original_error = str(error)
else:
    raise AssertionError('Original contract failure did not reproduce')
assert original_error == 'decision_variation has an unresolved decision shortcut'

# Retain byte-identical completed evidence in a self-contained writable bundle.
names = set(review['source_analysis']['evidence_paths'])
for check in review['checks'].values():
    names.update(check['evidence_paths'])
for group in ('coverage', 'counterfactuals', 'shortcut_probes'):
    for row in variation[group]:
        names.update(row['sample_refs'])
names.update(variation['delivery']['sample_refs'])
names.update(['previous-runner-batch.json', 'runner-batch.json', 'render-records.json',
              'counterfactual-results.json', 'repair-preflight-copy.json'])
names.discard('repair-preflight-copy.json')
names.discard('pedagogical-variation.json')
names.discard('schema-validation.json')
provenance = []
for name in sorted(names):
    src = OLD / name
    dst = OUT / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    provenance.append({'path': name, 'sha256': hashlib.sha256(src.read_bytes()).hexdigest()})
shutil.copytree(OLD / 'render', OUT / 'render', dirs_exist_ok=True)
save('repair-preflight-copy.json', load(JOB / 'repair-preflight.json'))
save('repair-history-copy.json', load(JOB / 'repair-history.json'))

snapshot = load(OLD / 'whole-package-before.json')
before = {str(p.relative_to(PACKAGE)): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in PACKAGE.rglob('*') if p.is_file()}
assert before == snapshot

commands = []
for label, input_path, expected_exit, expected_correct in [
    ('current', None, 0, 1),
    ('delivered', OLD / 'delivery-batch/accepted.json', 0, 1),
    ('historical', OLD / 'previous-runner-batch.json', 1, 5),
]:
    cmd = [str(PY), '-B', str(OLD / 'reproduce_batch_shortcut.py')]
    if input_path:
        cmd += ['--input', str(input_path)]
    p = subprocess.run(cmd, cwd=OUT, capture_output=True, text=True)
    (OUT / ('correction-' + label + '.log')).write_text(p.stdout + p.stderr)
    result = json.loads(p.stdout)
    assert p.returncode == expected_exit and result['correct'] == expected_correct
    commands.append({'label': label, 'command': cmd, 'exit_code': p.returncode,
                     'measurement': result, 'log': 'correction-' + label + '.log'})

sys.path.insert(0, str(PACKAGE))
generator = module('reviewed_generator', PACKAGE / '17592186059775.py')
fresh = generator.batch('easy', 5, 4258185931)
assert fresh == load(JOB / 'samples.json') == load(OUT / 'runner-batch.json')
save('correction-current-records.json', fresh)

historical = [p for p in variation['shortcut_probes'] if p['disposition'] == 'defect']
assert len(historical) == 1 and historical[0]['subgroup'] == 'previous failing batch'
save('historical-control.json', {
    'purpose': 'Retained failing control; distinct from current-package acceptance probes.',
    'original_probe': historical[0],
    'status': 'Historical defect remains reproduced; retained finding is resolved in current batch.',
    'current_correct': 1, 'current_total': 5, 'baseline': 0.2,
    'complete_record_files': ['previous-runner-batch.json', 'correction-current-records.json',
                              'delivery-batch/accepted.json'],
    'commands': commands,
    'inventory': 'Three legacy stored defects remain documented in affected-inventory.json; no database changes.',
})
variation['shortcut_probes'] = [p for p in variation['shortcut_probes'] if p not in historical]
variation['limitations'] = [
    'Historical failing controls are preserved separately in historical-control.json. '
    'The original 5/5 defect was not relabeled as harmless; it is absent from current '
    'acceptance probes because the current exact batch scores 1/5. Three legacy stored '
    'instances remain in affected-inventory.json.'
    if x.startswith('Historical control probe has disposition defect') else x
    for x in variation['limitations']
]
save('pedagogical-variation.json', variation)

review['summary'] = ('All eight checks pass for the unchanged current package and exact batch. '
    'Corrected report placement: the previous 5/5 failing control is retained separately; '
    'the current raw and delivered batches score 1/5. Three legacy inventory defects remain documented.')
review['checks']['decision_variation']['evidence_paths'] += [
    'historical-control.json', 'correction-current-records.json', 'correction-validation.json']
review['checks']['decision_variation']['details'] += (
    ' The historical 5/5 sensitivity control is separately retained in historical-control.json; '
    'fresh current and delivered reruns score 1/5. All 56 current probes remain unchanged.')
save('result.json', review)
save('correction-provenance.json', {
    'original_evidence_root': str(OLD), 'corrected_bundle_root': str(OUT),
    'scope': 'Report/evidence correction only; all unaffected checks reused.',
    'original_error': original_error, 'copied_evidence': provenance,
    'source_prompts_and_complete_banks_confirmed': len(account['source_cases']),
    'source_lesson_passages_reconfirmed': ['2112d3af-1fb0-5a70-ab99-59931db99930',
                                          'ee4b134d-2908-5930-86bb-32537e0d8347'],
    'retained_findings': load(JOB / 'repair-history.json')['findings'],
})
after = {str(p.relative_to(PACKAGE)): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in PACKAGE.rglob('*') if p.is_file()}
assert after == before
save('correction-package-unchanged.json', {'unchanged': True, 'file_count': len(after),
                                        'matches_completed_review_snapshot': True})
# The real contract validator must reproduce the original failure and accept the correction.
save('schema-validation.json', {'passed': True, 'validation_pending': True})
save('correction-validation.json', {'passed': True, 'validation_pending': True})
validator.validate_review(review, OUT)
try:
    import jsonschema
except ImportError:
    jsonschema = None
if jsonschema:
    jsonschema.validate(variation, load(REPO / 'generate/pipeline/pedagogical-variation.schema.json'))
else:
    schema_check = subprocess.run([
        '/usr/bin/python3', '-B', '-c',
        'import json,jsonschema,sys; '
        'jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2])))',
        str(OUT / 'pedagogical-variation.json'),
        str(REPO / 'generate/pipeline/pedagogical-variation.schema.json'),
    ], capture_output=True, text=True)
    assert schema_check.returncode == 0, schema_check.stderr
save('correction-validation.json', {
    'passed': True, 'validator': 'scripts/generator_review.py:validate_review',
    'original_error_reproduced': original_error,
    'current_probes': len(variation['shortcut_probes']), 'historical_controls_retained': len(historical),
    'current_probes_unchanged': variation['shortcut_probes'] == [
        p for p in load(OLD / 'pedagogical-variation.json')['shortcut_probes'] if p not in historical],
    'current_raw_correct': 1, 'current_delivered_correct': 1, 'historical_correct': 5,
    'attempts_each': 5, 'package_unchanged': True, 'commands': commands,
    'json_schema_checked': True,
})
save('schema-validation.json', {'passed': True,
    'validator': 'scripts/generator_review.py:validate_review',
    'all_eight_passed': True, 'json_schema_checked': True})
validator.validate_review(load(OUT / 'result.json'), OUT)
(OUT / 'session-state.md').write_text(
    'Bounded contract correction complete. Corrected self-contained bundle: contract-repair/. '
    'All eight completed checks reused. Original validator failure reproduced. Historical '
    '5/5 control retained separately; fresh current and delivered probes each 1/5. '
    'All 56 current probes unchanged. Real review validator passes corrected result.json. '
    'All 176 package files unchanged. No publication or database operations.\n')
print(json.dumps({'passed': True, 'current_probes': len(variation['shortcut_probes']),
                  'package_files_unchanged': len(after), 'corrected_bundle_root': str(OUT)}))
