"""Independent displayed-matrix, raw-source, sampling and native-grader review.

Read-only with respect to the generator, application, and database. Outputs live
beside this script. No validator implementation from the generator is imported.
"""
from pathlib import Path
from collections import Counter
import copy
import hashlib
import importlib.util
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
GENERATOR = ROOT / 'generate/scratch/17592186119771.py'
spec = importlib.util.spec_from_file_location('triangular_under_review', GENERATOR)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def parse(text):
    found = re.findall(r'([AC])\s*=\s*\[?\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\2\}', text, re.S)
    assert len(found) == 1, 'Exactly one printed matrix required'
    name, layout, body = found[0]
    matrix = [[int(value.strip()) for value in row.split('&')] for row in body.split(r'\\')]
    assert all(len(row) == len(matrix) for row in matrix), 'Matrix must be square'
    return matrix, name, layout


def family(matrix):
    n = len(matrix)
    upper = all(matrix[i][j] == 0 for i in range(n) for j in range(i))
    lower = all(matrix[i][j] == 0 for i in range(n) for j in range(i + 1, n))
    identity = all(matrix[i][j] == int(i == j) for i in range(n) for j in range(n))
    return 'identity' if identity else 'diagonal' if upper and lower else 'upper' if upper else 'lower' if lower else 'other'


def pattern(matrix):
    return (len(matrix), family(matrix), tuple((i, j) for i, row in enumerate(matrix) for j, value in enumerate(row) if i != j and value))


def normalize(question):
    q = copy.deepcopy(question)
    q.pop(':question/id')
    if isinstance(q.get(':question/difficulty'), dict):
        q[':question/difficulty'] = q[':question/difficulty'][':db/ident']
    for f in q[':question/answer-fields']:
        f.pop(':answer-field/id')
        if isinstance(f[':answer-field/type'], dict):
            f[':answer-field/type'] = f[':answer-field/type'][':db/ident']
        if ':answer-field/correct' in f:
            correct = f[':answer-field/correct']
            f[':answer-field/correct'] = correct[':answer/value'] if isinstance(correct, dict) else next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == correct[1])
        for a in f[':answer-field/choices']:
            a.pop(':answer/id')
            if isinstance(a[':answer/type'], dict):
                a[':answer/type'] = a[':answer/type'][':db/ident']
        f[':answer-field/choices'].sort(key=lambda a: a[':answer/value'])
    return q


LABELS = {'lower': 'Lower triangular matrix', 'upper': 'Upper triangular matrix', 'diagonal': 'Diagonal matrix'}
DIMENSIONS = {'easy': 2, 'moderate': 3, 'hard': 4}


def native_fixture(label, rec):
    checks = []
    for i, f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index': i, 'submitted_answer_id': a[':answer/id'],
                           'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
                           'purpose': 'independently checked printed matrix, complete five-label radio bank'})
    return {'label': label, 'record': rec, 'checks': checks}


def verify_normal(rec, level):
    q = rec['question']
    matrix, name, layout = parse(q[':question/problem'])
    n = len(matrix)
    kind = family(matrix)
    assert n == DIMENSIONS[level]
    assert kind in LABELS
    assert all(matrix[i][i] != 0 for i in range(n))
    if kind != 'diagonal':
        assert sum(bool(value) for i, row in enumerate(matrix) for j, value in enumerate(row) if i != j) >= (n * (n - 1) + 3) // 4
    assert rec['generation']['template'] == kind
    assert not rec['generation']['evidence_only'] and rec['generation']['eligible_for_learning']
    assert q[':question/difficulty'] == ':question.difficulty/' + level
    assert 'most specific' in q[':question/problem']
    assert len(q[':question/answer-fields']) == 1
    f = q[':question/answer-fields'][0]
    assert f[':answer-field/type'] == ':answer-field.type/radio'
    assert sorted(a[':answer/value'] for a in f[':answer-field/choices']) == sorted([*LABELS.values(), 'Identity matrix', 'Other'])
    keyed = next(a for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1])
    assert keyed[':answer/value'] == LABELS[kind]
    assert parse(q[':question/worked-solution']) == (matrix, name, layout)
    region = {'lower': 'above', 'upper': 'below', 'diagonal': 'above and below'}[kind]
    assert f'entries {region} the diagonal' in q[':question/worked-solution']
    if kind != 'diagonal':
        witness = re.search(r'\$\{([ac])\}_\{(\d)(\d)\}=(-?\d+)\\ne 0\.\$', q[':question/worked-solution'])
        assert witness
        i, j, value = int(witness[2]) - 1, int(witness[3]) - 1, int(witness[4])
        assert witness[1] == name.lower() and matrix[i][j] == value != 0
        assert i > j if kind == 'lower' else i < j
    return kind, pattern(matrix)


def main():
    assert g.VERSION != 'triangular-description-2.0', 'Wait for author handoff'
    original_hash = hashlib.sha256(GENERATOR.read_bytes()).hexdigest()
    native, source_results = [], []
    sources = json.loads((ROOT / 'generate/scratch/17592186119771/source.json').read_text())['record'][':knowledge-point/questions']
    for source in sources:
        sid = source[':question/math-academy-id']
        matrix, name, layout = parse(source[':question/problem'])
        difficulty = source.get(':question/difficulty', ':question.difficulty/easy')
        level = (difficulty[':db/ident'] if isinstance(difficulty, dict) else difficulty).split('/')[-1]
        rec = g.generate(level, profile='raw:' + sid, parameters={'matrix': matrix, 'letter': name, 'layout': layout})
        assert normalize(rec['question']) == normalize(source), sid
        assert rec['generation']['evidence_only'] and not rec['generation']['eligible_for_learning']
        keyed = copy.deepcopy(rec)
        keyed['question'][':question/answer-fields'] = [f for f in keyed['question'][':question/answer-fields'] if ':answer-field/correct' in f]
        if keyed['question'][':question/answer-fields']:
            for f in keyed['question'][':question/answer-fields']:
                value = next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1])
                assert value == LABELS[family(matrix)]
            native.append(native_fixture('keyed source evidence ' + sid, keyed))
        source_results.append({'source': sid, 'exact_normalized_replay': True, 'keyed_fields': len(keyed['question'][':question/answer-fields'])})

    distribution, catalogs, visual = {}, {}, []
    for level in DIMENSIONS:
        counts, seen, selected = Counter(), {}, {}
        for seed in range(1000):
            rec = g.generate(level, seed)
            kind, shape = verify_normal(rec, level)
            counts[kind] += 1
            seen.setdefault(shape, rec)
            selected.setdefault(kind, rec)
        assert set(counts) == set(LABELS)
        assert 0.34 <= counts['upper'] / 1000 <= 0.46
        assert 0.34 <= counts['lower'] / 1000 <= 0.46
        assert 0.15 <= counts['diagonal'] / 1000 <= 0.25
        full = g.batch(level, len(g.catalog(level)), 107)
        batch_shapes = [verify_normal(rec, level)[1] for rec in full]
        assert len(set(batch_shapes)) == len(full) == len(seen)
        distribution[level] = dict(counts)
        catalogs[level] = {'sampled_unique_structures': len(seen), 'full_batch_count': len(full),
                           'full_batch_families': dict(Counter(family(parse(rec['question'][':question/problem'])[0]) for rec in full))}
        native += [native_fixture(f'normal {level} structure {i}', rec) for i, rec in enumerate(seen.values())]
        visual += [{'label': level + ' ' + kind, 'record': selected[kind]} for kind in ('upper', 'lower', 'diagonal')]

    refill_matrices = [
        ('upper', [[4, -3, 7], [0, -2, 0], [0, 0, 5]]),
        ('upper', [[-6, 2, 0], [0, 3, -4], [0, 0, 8]]),
        ('lower', [[5, 0, 0], [-2, -3, 0], [6, 0, 4]]),
        ('lower', [[-4, 0, 0], [0, 7, 0], [3, -5, 2]]),
    ]
    source_shapes = {pattern(parse(q[':question/problem'])[0]) for q in sources}
    refill = []
    for i, (kind, matrix) in enumerate(refill_matrices):
        rec = g.generate('moderate', 500 + i, template=kind,
                         parameters={'matrix': matrix, 'letter': 'A', 'layout': 'bmatrix'})
        _, shape = verify_normal(rec, 'moderate')
        assert shape not in source_shapes, 'Refill should add a new source support pattern'
        refill.append(rec)
        native.append(native_fixture('moderate refill ' + str(i + 1), rec))
    assert len({pattern(parse(rec['question'][':question/problem'])[0]) for rec in refill}) == 4
    save('records.json', refill)

    save('native-input.json', native)
    save('visual-cases.json', visual)
    deps = ROOT / 'target/release/deps'
    libs = {name: max(deps.glob('lib' + name + '-*.rlib'), key=lambda p: p.stat().st_mtime_ns) for name in ('course_academy_engine', 'serde_json')}
    command = ['rustc', '--edition=2024', '-O', str(ROOT / 'generate/runs/current/check-engine.rs')]
    for name, path in libs.items():
        command += ['--extern', name + '=' + str(path)]
    command += ['-L', 'dependency=' + str(deps), '-o', str(HERE / 'check-engine')]
    subprocess.run(command, check=True)
    subprocess.run([str(HERE / 'check-engine'), str(HERE / 'native-input.json'), str(HERE / 'native-grading.json')], check=True)
    grade = json.loads((HERE / 'native-grading.json').read_text())
    assert grade['documented_unresolved_checks'] == 0
    assert hashlib.sha256(GENERATOR.read_bytes()).hexdigest() == original_hash, 'Generator changed during review'
    report = {'passed': True, 'database_writes': 0, 'version': g.VERSION, 'generator_sha256': original_hash,
              'source_replay': source_results, 'sampled_normal_records': 3000,
              'family_distribution': distribution, 'structural_catalogs': catalogs,
              'refill_records': [{'id': rec['question'][':question/id'], 'template': rec['generation']['template'],
                                  'new_source_support': True} for rec in refill],
              'native_grading': {key: grade[key] for key in ('entry_point', 'accepted_checks', 'rejected_checks', 'documented_unresolved_checks')},
              'native_libraries': {name: str(path) for name, path in libs.items()},
              'native_grader_sha256': hashlib.sha256((HERE / 'check-engine').read_bytes()).hexdigest(),
              'limitations': ['The two originally unkeyed source fields remain unkeyed evidence; native grading covers only their nine keyed siblings.',
                             'Nonzero diagonals and denser triangles are authored normal-generator quality restrictions, not definitions of triangular matrices.',
                             'Numeric changes are presentation variation only; structural deduplication has finite 3/9/85 capacities.']}
    save('review.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
