#!/usr/bin/env python3
"""Exercise all response classes, source replays, and duplicate-prevention edges."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'Cargo.toml').exists())
PACKAGE = HERE.parent.parent / 'generators' / '17592186198347'
OLD = Path('/media/jake/SSD/EDB/math/generators/4c/4c62f973f7abf289b15bfa656ba36cbee1a68139ee43ffdbdd834dae35e2d951')
sys.path.insert(0, str(PACKAGE))
sys.dont_write_bytecode = True


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


g = module('repaired_slope_classification', PACKAGE / 'generator.py')
old = module('old_slope_classification', OLD / 'generator.py')


def rows(record):
    body = re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', record['question'][':question/problem'], re.S)[1]
    return [r.strip() for r in body.split(r'\\')]


def coefficients(row):
    lhs, expression = row.replace(' ', '').split('&=')
    assert lhs == 'y'
    m = b = 0
    for term in re.findall(r'[+-]?[^+-]+', expression):
        if term.endswith('x'):
            value = term[:-1]
            m += 1 if value in ('', '+') else -1 if value == '-' else int(value)
        else:
            b += int(term)
    return m, b


def verify(record):
    first, second = rows(record)
    assert first != second
    m1, b1 = coefficients(first)
    m2, b2 = coefficients(second)
    params = record['generation']['parameters']
    assert (m1, b1, m2, b2) == tuple(params[k] for k in ('m1', 'b1', 'm2', 'b2'))
    relation = 'intersecting' if m1 != m2 else 'coincident' if b1 == b2 else 'parallel'
    assert record['generation']['relation'] == relation
    expected = {
        'parallel': ('are parallel', 'no solutions', 'inconsistent'),
        'intersecting': ('intersect at one point', 'only one solution', 'consistent independent'),
        'coincident': ('coincide with each other', 'infinitely many solutions', 'consistent dependent'),
    }[relation]
    q = record['question']
    assert q[':question/difficulty'] == ':question.difficulty/easy'
    assert len(q[':question/answer-fields']) == 3
    owned_ids = [q[':question/id']]
    checks = []
    for index, field in enumerate(q[':question/answer-fields']):
        assert field[':answer-field/type'] == ':answer-field.type/select'
        assert field[':answer-field/key'] == f'field-{index + 1}'
        assert '{{' + field[':answer-field/key'] + '}}' in q[':question/problem']
        choices = field[':answer-field/choices']
        assert tuple(a[':answer/value'] for a in choices) == old.BANKS[index]
        key = field[':answer-field/correct'][1]
        assert next(a[':answer/value'] for a in choices if a[':answer/id'] == key) == expected[index]
        owned_ids += [field[':answer-field/id']] + [a[':answer/id'] for a in choices]
        checks += [{'field_index': index, 'submitted_answer_id': a[':answer/id'],
                    'expected': 'accepted' if a[':answer/value'] == expected[index] else 'rejected',
                    'purpose': 'Independently classified line equations'} for a in choices]
    assert len(owned_ids) == len(set(owned_ids))
    if relation == 'coincident':
        assert b1 != 0 and params['intercept_first'] is True
        assert first.replace(' ', '').startswith(f'y&={b1}')
        assert 'same slopes' in q[':question/worked-solution']
        assert f'same $y$-intercepts (${b1}$)' in q[':question/worked-solution']
    prior = old.generate(m1, b1, m2, b2, params['intercept_first'])
    assert q == prior['question']  # Changed display selection only, not content or keys.
    assert g.generate(**params, seed=876)['question'] == q
    return {'label': q[':question/id'], 'record': record, 'checks': checks}


def reject(callback):
    try:
        callback()
    except ValueError:
        return
    raise AssertionError('Invalid request accepted')


def main():
    assert g.MAX_INSTANCES == 46344
    original_replays = old.replay_sources()
    replays = g.replay_sources()
    assert [r['question'] for r in replays] == [r['question'] for r in original_replays]
    records = list(replays)
    # Every supported coincident line must be rendered with distinct rows,
    # regardless of the caller's requested term ordering.
    for m, b, intercept_first in itertools.product(g.SLOPES, g.INTERCEPTS, (False, True)):
        if b == 0:
            reject(lambda: g.generate(m, b, m, b, intercept_first))
        else:
            records.append(g.generate(m, b, m, b, intercept_first))
    for seed in range(24):
        batch = g.sample(40, seed)
        assert batch == g.sample(40, seed)
        assert batch[:12] == g.sample(12, seed)
        assert {r['generation']['relation'] for r in batch} == set(g.RELATIONS)
        assert len({r['question'][':question/id'] for r in batch}) == len(batch)
        records.extend(batch)
    # Keep zero intercepts in the other two classes; these are useful examples.
    records += [g.generate(4, 0, 4, 9), g.generate(4, 0, -4, 0)]
    records.append(g.generate(4, 9, 4, 9, False))
    assert rows(records[-1]) == ['y &=9 + 4x', 'y &=4x + 9']
    assert g.sample(0, 1) == []
    reject(lambda: g.sample(-1, 1))
    reject(lambda: g.sample(g.MAX_INSTANCES + 1, 1))
    reject(lambda: g.sample(1, 1, 'moderate'))
    # Traverse the entire finite sampling domain without storing 46k full
    # questions. This catches an exhausted-pool loop or a duplicate line pair.
    public_generate = g.generate
    try:
        g.generate = lambda m1, b1, m2, b2, *args, **kwargs: (m1, b1, m2, b2)
        full_domain = g.sample(g.MAX_INSTANCES, 23)
    finally:
        g.generate = public_generate
    unordered = {tuple(sorted(((m1, b1), (m2, b2)))) for m1, b1, m2, b2 in full_domain}
    assert len(unordered) == g.MAX_INSTANCES
    assert all(not (m1 == m2 and b1 == b2 == 0) for m1, b1, m2, b2 in full_domain)
    classes = Counter('intersecting' if m1 != m2 else 'coincident' if b1 == b2 else 'parallel'
                      for m1, b1, m2, b2 in full_domain)
    assert classes == {'parallel': 2736, 'coincident': 288, 'intersecting': 43320}
    for difficulty in ('easy', 'unclassified'):
        output = subprocess.check_output([sys.executable, '-B', str(PACKAGE / 'generator.py'), '--count', '9',
                                          '--seed', '25', '--difficulty', difficulty, '--format', 'json'], text=True)
        cli = json.loads(output)
        assert cli == g.sample(9, 25, difficulty)
        records.extend(cli)
    fixtures = [verify(r) for r in records]
    native = ROOT / 'generate/scratch/17592186073778/check-engine'
    input_path, report_path = HERE / 'native-input.json', HERE / 'native-report.json'
    input_path.write_text(json.dumps(fixtures) + '\n')
    subprocess.run([str(native), str(input_path), str(report_path)], check=True)
    report = json.loads(report_path.read_text())
    assert report['documented_unresolved_checks'] == 0
    verification = {
        'status': 'passed', 'generator_version': g.VERSION,
        'generator_sha256': hashlib.sha256((PACKAGE / 'generator.py').read_bytes()).hexdigest(),
        'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in PACKAGE.iterdir() if p.is_file()},
        'unchanged_source_replays': len(replays), 'validated_records': len(records),
        'coincident_render_checks': 576, 'rejected_zero_intercept_coincident_requests': 32,
        'random_seeds': 24, 'random_records': 960, 'full_sampling_domain_instances': len(full_domain),
        'full_sampling_domain_relations': dict(classes),
        'cli_difficulties_checked': ['easy', 'unclassified'], 'native_harness': str(native.relative_to(ROOT)),
        'native_harness_sha256': hashlib.sha256(native.read_bytes()).hexdigest(),
        'native_accepted_checks': report['accepted_checks'], 'native_rejected_checks': report['rejected_checks'],
        'native_unresolved_checks': report['documented_unresolved_checks'],
        'target_question': {'db_id': 17592186567796, 'old_first_row': 'y &=4x + 9',
                            'new_first_row': 'y &=9 + 4x', 'second_row': 'y &=4x + 9',
                            'solution_and_correct_responses': 'unchanged'},
        'database_writes': 0,
    }
    (HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
