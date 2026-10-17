"""Reuse independent generator QA and prove prompt-only generation changes."""
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.dont_write_bytecode = True

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def field_signature(record):
    f = record['question'][':question/answer-fields'][0]
    correct = f.get(':answer-field/correct', [None, None])[1]
    return {'key': f[':answer-field/key'], 'type': f[':answer-field/type'],
            'ordered_choices': [(a[':answer/type'], a[':answer/value']) for a in f.get(':answer-field/choices', [])],
            'correct_value': next((a[':answer/value'] for a in f.get(':answer-field/choices', []) if a[':answer/id'] == correct), None)}

report = []
examples = []
for kp in (17592186073777, 17592186073778):
    current = ROOT / 'generate/scratch' / f'{kp}.py'
    v = load('validation_' + str(kp), current.with_suffix('') / 'validate.py')
    g = v.g
    before = load('before_' + str(kp), HERE / 'before' / current.name)
    count = 0
    mutation_count = 0
    fingerprints = set()
    engine = []
    for level in ('easy', 'moderate', 'hard'):
        for template in ([None] if kp == 17592186073777 else g.TEMPLATES):
            for seed in range(20):
                old = before.generate(level, seed, template=template)
                new = g.generate(level, seed, template=template)
                v.check(new)
                assert old['generation']['parameters'] == new['generation']['parameters']
                fp = 'mathematical_fingerprint' if kp == 17592186073777 else 'parameter_fingerprint'
                assert old['generation'][fp] == new['generation'][fp]
                fingerprints.add(new['generation'][fp])
                assert old['question'][':question/difficulty'] == new['question'][':question/difficulty']
                assert old['question'][':question/worked-solution'] == new['question'][':question/worked-solution']
                assert field_signature(old) == field_signature(new)
                assert old['question'][':question/problem'] != new['question'][':question/problem']
                assert old['question'][':question/id'] != new['question'][':question/id']
                count += 1
                if seed == 0:
                    examples.append(new)
                    if kp == 17592186073778:
                        engine.append(v.native(new, level + '-' + str(template)))
                    else:
                        f = new['question'][':question/answer-fields'][0]
                        engine.append({'label': level, 'record': new, 'checks': [
                            {'submitted_answer_id': a[':answer/id'], 'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected', 'purpose': 'Unchanged categorical answer values after display-only edit'}
                            for a in f[':answer-field/choices']]})
                    mutated = copy.deepcopy(new)
                    prompt = mutated['question'][':question/problem']
                    marker = '&{}={}&' if kp == 17592186073777 else '&='
                    mutated['question'][':question/problem'] = prompt.replace(marker, marker + ' 1 +', 1)
                    if kp == 17592186073777:
                        v.refresh_identity(mutated)
                    try:
                        v.check(mutated)
                    except (AssertionError, ValueError):
                        mutation_count += 1
                    else:
                        raise AssertionError('Changed equation escaped the independent validator')
    raw_count = 0
    cases = json.loads((current.with_suffix('') / 'source-cases.json').read_text())
    for case in cases:
        level = case.get('level', case.get('authored_level'))
        args = dict(parameters=case['parameters'], template=case['template'], profile=case['bank_profile'])
        old, new = before.generate(level, **args), g.generate(level, **args)
        assert old == new, 'Raw source replay (including identities) must remain exact'
        v.check(new)
        raw_count += 1
    engine_path = HERE / f'{kp}-engine-input.json'
    engine_report = HERE / f'{kp}-engine-report.json'
    engine_path.write_text(json.dumps(engine, indent=2) + '\n')
    harness = ROOT / 'generate/runs/current/check-engine'
    subprocess.run([str(harness), str(engine_path), str(engine_report)], check=True, capture_output=True, text=True)
    native_result = json.loads(engine_report.read_text())
    assert native_result['documented_unresolved_checks'] == 0
    report.append({'knowledge_point': kp, 'learner_records_checked': count, 'distinct_mathematical_fingerprints': len(fingerprints),
                   'unchanged_parameters_fingerprints_difficulty_solutions_answer_values_order_and_correct_values': True,
                   'raw_source_replays_byte_equivalent': raw_count, 'mutated_equations_rejected': mutation_count,
                   'native': native_result, 'script_sha256': hashlib.sha256(current.read_bytes()).hexdigest(),
                   'identity_behavior': 'Learner content-derived IDs change with the revised prompt; raw replay IDs remain unchanged.',
                   'passed': True})
(HERE / 'examples.json').write_text(json.dumps(examples, indent=2) + '\n')
(HERE / 'verification.json').write_text(json.dumps({'passed': True, 'generators': report, 'no_database_writes': True}, indent=2) + '\n')
print(json.dumps({'passed': True, 'generators': [{k: x[k] for k in ('knowledge_point', 'learner_records_checked', 'raw_source_replays_byte_equivalent', 'mutated_equations_rejected')} for x in report]}))
