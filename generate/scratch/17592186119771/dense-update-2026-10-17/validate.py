"""V3 focused checks. Read-only with respect to EDB; writes local evidence only."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import uuid
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[3]
spec = importlib.util.spec_from_file_location('original_validator', D.parent / 'validate.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
g = old.g


def write(name, value):
    (D / name).write_text(json.dumps(value, indent=2) + '\n')


def rejected(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError('Invalid generation call was accepted')


def normal(rec):
    q, meta = rec['question'], rec['generation']
    matrix, letter, layout = old.read(q[':question/problem'])
    n = len(matrix)
    label = old.expected(matrix)
    level = q[':question/difficulty'].split('/')[-1]
    assert n == {'easy': 2, 'moderate': 3, 'hard': 4}[level]
    assert all(matrix[i][i] != 0 for i in range(n))
    assert label in g.FAMILIES.values()
    if label != 'Diagonal matrix':
        assert sum(v != 0 for i, row in enumerate(matrix) for j, v in enumerate(row) if i != j) >= {2: 1, 3: 2, 4: 3}[n]
    assert layout == 'bmatrix'
    assert meta['parameters'] == {'matrix': matrix, 'letter': letter, 'layout': layout}
    assert meta['parameter_fingerprint'] == g.task_key(matrix)
    assert not meta['evidence_only'] and meta['eligible_for_learning']
    assert g.CRITERION in q[':question/problem']
    assert '$$\n' + letter + r' = \begin{bmatrix}' in q[':question/problem']
    assert r'\begin{aligned}' not in q[':question/problem']
    assert ':question/math-academy-id' not in q
    fields = q[':question/answer-fields']
    assert len(fields) == 1
    f = fields[0]
    assert f[':answer-field/key'] == 'selection'
    assert f[':answer-field/type'] == ':answer-field.type/radio'
    choices = f[':answer-field/choices']
    assert sorted(a[':answer/value'] for a in choices) == sorted(g.LABELS)
    ids = [a[':answer/id'] for a in choices]
    assert len(set(ids)) == 5
    for value in [q[':question/id'], f[':answer-field/id'], *ids]:
        uuid.UUID(value)
    assert f[':answer-field/correct'][0] == ':answer/id'
    assert next(a[':answer/value'] for a in choices if a[':answer/id'] == f[':answer-field/correct'][1]) == label
    sol = q[':question/worked-solution']
    old.balanced(q[':question/problem'])
    old.balanced(sol)
    assert old.read(sol) == (matrix, letter, layout)
    region = 'above and below' if label == 'Diagonal matrix' else 'above' if label == 'Lower triangular matrix' else 'below'
    assert f'all entries {region} the diagonal are' in sol
    assert f'Therefore, it is {"an" if label == "Upper triangular matrix" else "a"} {label.lower()}.' in sol
    if label != 'Diagonal matrix':
        witness = re.search(r'\$\{([ac])\}_\{(\d)(\d)\}=(-?\d+)\\ne 0\.\$', sol)
        assert witness
        i, j, value = int(witness[2]) - 1, int(witness[3]) - 1, int(witness[4])
        assert matrix[i][j] == value != 0
        assert (i > j) if label == 'Lower triangular matrix' else (i < j)
    return label


def main():
    native, raw, review, source_normal = [], [], [], []
    for sid, source in g.SOURCES.items():
        params = g.parse_matrix(source[':question/problem'])
        rec = g.generate(g.source_levels(sid), parameters=params, profile='raw:' + sid)
        old.structural(rec, raw=True)
        assert old.normalize_replay(rec['question']) == old.normalize_source_question(source)
        raw.append(rec)
        keyed = copy.deepcopy(rec)
        keyed['question'][':question/answer-fields'] = [f for f in keyed['question'][':question/answer-fields'] if ':answer-field/correct' in f]
        if keyed['question'][':question/answer-fields']:
            native.append({'label': 'Original source ' + sid, 'record': keyed, 'checks': old.checks(keyed)})
        altered = copy.deepcopy(params)
        altered['letter'] = 'C' if params['letter'] == 'A' else 'A'
        rejected(lambda: g.generate(g.source_levels(sid), parameters=altered, profile='raw:' + sid))
        # Source profiles retain source dimension/family but cannot bypass normal guards.
        level = {2: 'easy', 3: 'moderate', 4: 'hard'}[len(params['matrix'])]
        try:
            replay = g.generate(level, parameters=params, profile='source:' + sid)
        except ValueError as error:
            source_normal.append({'source_id': sid, 'normal_original_parameters': 'rejected', 'reason': str(error)})
        else:
            normal(replay)
            source_normal.append({'source_id': sid, 'normal_original_parameters': 'accepted', 'difficulty': level})
            native.append({'label': 'Normal compliant source ' + sid, 'record': replay, 'checks': old.checks(replay)})

    counts, families, batch_counts, sampled, correct_positions, letters = {}, {}, {}, {}, set(), set()
    total_sampled = 0
    for level in g.SUPPORTED_LEVELS:
        entries = g.catalog(level)
        counts[level] = len(entries)
        families[level] = dict(Counter(kind for kind, _ in entries))
        assert set(families[level]) == set(g.FAMILIES)
        fingerprints = set()
        for index, (kind, pattern) in enumerate(entries):
            rec = g.generate(level, seed=index, template=kind, parameters={'matrix': [list(row) for row in pattern], 'letter': 'A', 'layout': 'aligned'})
            normal(rec)
            assert rec['generation']['parameter_fingerprint'] not in fingerprints
            fingerprints.add(rec['generation']['parameter_fingerprint'])
            native.append({'label': f'{level} structural case {index}', 'record': rec, 'checks': old.checks(rec)})
        family_counts = Counter()
        for seed in range(1000):
            rec = g.generate(level, seed=seed)
            normal(rec)
            family_counts[rec['generation']['template']] += 1
            letters.add(rec['generation']['parameters']['letter'])
            f = rec['question'][':question/answer-fields'][0]
            correct_positions.add(next(i for i, a in enumerate(f[':answer-field/choices']) if a[':answer/id'] == f[':answer-field/correct'][1]))
            total_sampled += 1
        assert 350 <= family_counts['upper'] <= 450
        assert 350 <= family_counts['lower'] <= 450
        assert 150 <= family_counts['diagonal'] <= 250
        sampled[level] = dict(family_counts)
        batch_counts[level] = []
        for count in range(1, len(entries) + 1):
            records = g.batch(level, count, seed=1729)
            fps = [r['generation']['parameter_fingerprint'] for r in records]
            assert len(set(fps)) == count
            mix = Counter(r['generation']['template'] for r in records)
            if count >= 2:
                assert mix['diagonal'] < count / 2
                assert abs(mix['upper'] - mix['lower']) <= 1
            assert mix['diagonal'] <= 1
            batch_counts[level].append({'count': count, 'families': dict(mix)})
        rejected(lambda: g.batch(level, len(entries) + 1))
        # Exclude catalog cases before choosing the family plan, as replenishment does.
        exclude = [g.task_key(p) for kind, p in entries if kind in ('upper', 'diagonal')]
        remaining = len(entries) - len(exclude)
        leftovers = g.batch(level, remaining, exclude_fingerprints=exclude)
        assert all(r['generation']['template'] == 'lower' for r in leftovers)
        assert not set(exclude).intersection(r['generation']['parameter_fingerprint'] for r in leftovers)
        rejected(lambda: g.batch(level, remaining + 1, exclude_fingerprints=exclude))
        review.extend({'label': f'{level} {kind}', 'record': g.generate(level, seed=42, template=kind)} for kind in g.FAMILIES)

    assert counts == {'easy': 3, 'moderate': 9, 'hard': 85}
    assert correct_positions == set(range(5)) and letters == {'A', 'C'}
    for excluded_family in ('upper', 'lower'):
        excluded = [g.task_key(pattern) for kind, pattern in g.catalog('easy') if kind == excluded_family]
        remaining = g.batch('easy', 2, exclude_fingerprints=excluded)
        assert Counter(r['generation']['template'] for r in remaining) == Counter({'diagonal': 1, 'lower' if excluded_family == 'upper' else 'upper': 1})
        assert not set(excluded).intersection(r['generation']['parameter_fingerprint'] for r in remaining)
    rejected(lambda: g.batch('easy', 5))
    rejected(lambda: g.batch('easy', 1, seed=True))
    invalid = [
        ('moderate', [[0, 0, 0], [0, -2, 0], [0, 0, 0]]),
        ('moderate', [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        ('moderate', [[2, 3, 0], [0, 4, 0], [0, 0, 5]]),
        ('hard', [[2, 3, 0, 0], [0, 4, 0, 0], [0, 0, 5, 6], [0, 0, 0, 7]]),
        ('easy', [[1, 0], [0, 1]]),
        ('easy', [[2, 3], [4, 5]]),
        ('easy', [[2, 0, 0], [0, 3, 0], [0, 0, 4]]),
    ]
    for level, matrix in invalid:
        rejected(lambda: g.generate(level, parameters={'matrix': matrix, 'letter': 'A', 'layout': 'aligned'}))
    diagonal_source = next(sid for sid, q in g.SOURCES.items() if g.family(g.parse_matrix(q[':question/problem'])['matrix']) == 'diagonal')
    rejected(lambda: g.generate('moderate', parameters={'matrix': invalid[0][1], 'letter': 'A', 'layout': 'aligned'}, profile='source:' + diagonal_source))

    matrix = [[2, 3, 4], [0, 5, 0], [0, 0, 6]]
    variants = [matrix, [list(row) for row in zip(*matrix)], [[2, 0, 0], [0, 5, 0], [0, 0, 6]]]
    counterfactuals = [g.generate('moderate', parameters={'matrix': m, 'letter': 'A', 'layout': 'aligned'}) for m in variants]
    assert [normal(rec) for rec in counterfactuals] == ['Upper triangular matrix', 'Lower triangular matrix', 'Diagonal matrix']
    assert len({r['generation']['parameter_fingerprint'] for r in counterfactuals}) == 3
    incidental = [[-1 if i == j else -v for j, v in enumerate(row)] for i, row in enumerate(matrix)]
    assert g.task_key(matrix) == g.task_key(incidental)
    for layout in ('aligned', 'bmatrix'):
        rec = g.generate('moderate', parameters={'matrix': incidental, 'letter': 'C', 'layout': layout})
        assert normal(rec) == 'Upper triangular matrix'
    assert g.task_key([[1, 0, 0], [0, 2, 0], [0, 0, 3]]) == g.task_key([[2, 0, 0], [0, 1, 0], [0, 0, -9]])

    # Reuse successful native evidence only when its complete fixture bytes match.
    same_native = (D / 'engine-input.json').exists() and json.loads((D / 'engine-input.json').read_text()) == native and (D / 'native-grading.json').exists()
    write('engine-input.json', native)
    if not same_native:
        subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(D / 'engine-input.json'), str(D / 'native-grading.json')], check=True)
    engine = json.loads((D / 'native-grading.json').read_text())
    assert engine['documented_unresolved_checks'] == 0
    write('source-replay.json', raw)
    write('source-normal-policy.json', source_normal)
    write('review-samples.json', review)
    (D / 'review-samples.md').write_text('\n\n---\n\n'.join('## ' + r['label'] + '\n\n' + g.markdown(r['record']) for r in review) + '\n')
    write('pedagogical-variation.json', {'family_sampling_1000_each_level': sampled, 'finite_family_counts': families, 'all_batch_sizes': batch_counts, 'counterfactuals': counterfactuals, 'post_exclusion_selection_checked': True, 'incidental_value_label_layout_fingerprint_invariance': True})
    sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    result = {
        'status': 'pass', 'version': g.VERSION, 'source_full_raw_replays': len(raw),
        'raw_modified_parameters_rejected': len(raw), 'source_normal_policy': source_normal,
        'meaningful_catalog_counts': counts, 'full_catalog_patterns_verified': sum(counts.values()),
        'sampled_normal_records_verified': total_sampled, 'family_sampling': sampled,
        'all_finite_batch_sizes_verified': sum(counts.values()), 'invalid_matrix_cases_rejected': len(invalid),
        'source_profile_sparse_bypass_rejected': True, 'easy_five_task_request_rejected': True,
        'depleted_easy_two_task_remainder_verified': ['lower+diagonal', 'upper+diagonal'],
        'native_records': len(native), 'native_grading': {k: engine[k] for k in ('accepted_checks', 'rejected_checks', 'documented_unresolved_checks', 'entry_point')},
        'hashes': {'generator': sha(D.parent.with_suffix('.py')), 'validator': sha(__file__), 'source': sha(D.parent / 'source.json'), 'grader_binary': sha(ROOT / 'generate/runs/current/check-engine')},
        'limitations': ['Normal level ratings follow authored 2/3/4 size workload; raw originals preserve captured ratings.', 'Independent family weights are 40/40/20. Unique structural batches retain at most one diagonal contrast and balance upper/lower as remaining supply permits; deduplication changes proportions.', 'Easy supports only three unique structures. Numerical changes and diagonal unit positions are not fresh tasks.', 'Two raw source fields lack a captured correct key; only originally keyed source fields are graded. Raw replay is evidence-only and cannot supply learning content.']}
    write('validation.json', result)
    write('capabilities.json', {'version': g.VERSION, 'levels': list(g.SUPPORTED_LEVELS), 'field_types': ['radio'], 'profiles': ['five-labels'] + ['raw:' + s for s in g.SOURCES] + ['source:' + s for s in g.SOURCES], 'meaningful_catalog_counts': counts, 'independent_family_weights': g.FAMILY_WEIGHTS, 'source_basis': g.SOURCE['basis'], 'normal_source_policy': 'Normal density and size guards apply; exact original rendering/ratings are available only as evidence-only raw replay.'})
    print(json.dumps({k: result[k] for k in ('status', 'meaningful_catalog_counts', 'source_full_raw_replays', 'sampled_normal_records_verified', 'native_records', 'native_grading')}))


if __name__ == '__main__':
    main()
