#!/usr/bin/env python3
"""Read-only generator representation audit; imports pure registered generators."""
import hashlib
import importlib.util
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
SNAPSHOT = json.loads((HERE / 'snapshot.json').read_text())
TOPIC = SNAPSHOT['scope'][0][0]
SAMPLES = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix(text):
    body = re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S)[1]
    return [[Fraction(x.strip()) for x in row.split('&')] for row in body.split(r'\\')]


def exact_pivots(rows):
    """Independent Fraction Gaussian elimination, independent of generator helpers."""
    a = [row[:] for row in rows]
    i = 0
    result = []
    for j in range(len(a[0])):
        row = next((k for k in range(i, len(a)) if a[k][j]), None)
        if row is None:
            continue
        a[i], a[row] = a[row], a[i]
        v = a[i][j]
        a[i] = [x / v for x in a[i]]
        for k in range(i + 1, len(a)):
            v = a[k][j]
            a[k] = [x - v * y for x, y in zip(a[k], a[i])]
        result.append(j + 1)
        i += 1
        if i == len(a):
            break
    return result


def subset(value, n):
    if value.startswith('All the columns'):
        return list(range(1, n + 1))
    values = [int(x) for x in re.findall(r'\$(\d+)\$(?:st|nd|rd|th)', value)]
    assert values and len(values) == len(set(values)) and all(1 <= x <= n for x in values), value
    return sorted(values)


def inspect(rec, kp, profile, kind):
    q = rec['question']
    rows = matrix(q[':question/problem'])
    pivots = exact_pivots(rows)
    expected = len(pivots) if kp == 17592186124479 else pivots if kp == 17592186124477 else [j for j in range(1, len(rows[0]) + 1) if j not in pivots]
    fields = q[':question/answer-fields']
    assert len(fields) == 1
    f = fields[0]
    assert f[':answer-field/type'] == ':answer-field.type/radio'
    decoded = {a[':answer/id']: int(a[':answer/value']) if kp == 17592186124479 else subset(a[':answer/value'], len(rows[0])) for a in f[':answer-field/choices']}
    key = f[':answer-field/correct'][1]
    assert decoded[key] == expected, (kp, profile, decoded[key], expected)
    assert len({json.dumps(v) for v in decoded.values()}) == len(decoded)
    # Exact matrix rank/column semantics validate the key without relying on solution prose.
    SAMPLES.append({'kp_id': kp, 'profile': profile, 'kind': kind, 'record': rec,
                    'independent_pivot_columns': pivots, 'expected_answer': expected,
                    'old_choice_mapping': decoded, 'correct_key_matches': True})


def run(kp):
    kid = kp[':db/id']
    registration = kp.get(':knowledge-point/question-generator')
    if not registration:
        return {'kp_id': kid, 'title': kp[':knowledge-point/title'],
                'registration': None, 'decision': 'no_generator',
                'reason': 'No question-generator registration exists at the captured database basis.',
                'manifest_path_exists': (ROOT / f'generate/scratch/{kid}.py').exists()}
    path = ROOT / registration[':question-generator/script']
    before = sha(path)
    spec = importlib.util.spec_from_file_location(f'audit_g_{kid}', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    start = len(SAMPLES)
    if kid == 17592186124477:
        profiles = sorted(mod.SOURCES)
        for profile in profiles:
            src = mod.SOURCES[profile]
            original = mod.matrix(src[':question/problem'])
            n = len(original[0])
            inspect(mod.generate('easy', profile=profile,
                                 parameters={'columns': list(range(1, n + 1)), 'matrix': original}),
                    kid, profile, 'source_parameters')
            for target in mod.targets(profile):
                rows = [[0] * n for _ in original]
                for i, p in enumerate(target):
                    rows[i][p - 1] = (-1 if i % 2 else 1) * (i + 1)
                    for j in range(p, n):
                        rows[i][j] = (i + 2 * j) % 9 - 4
                inspect(mod.generate('easy', seed=0, profile=profile,
                                     parameters={'columns': mod.permutation(profile, target), 'matrix': rows}),
                        kid, profile, 'every_supported_pivot_placement')
        levels = list(mod.LEVELS)
        description = 'One instructional template (pivot-columns-ref), 13 source bank profiles; all ask for the subset of pivot columns in supplied row echelon form.'
        dependencies = [path.with_suffix('') / 'source.json', path.with_suffix('') / 'capabilities.json']
    elif kid == 17592186124478:
        profiles = sorted(mod.CASES)
        for profile in profiles:
            inspect(mod.generate('easy', template=profile, parameters=mod.DEFAULTS[profile]), kid, profile, 'source_parameters')
            for seed in range(5):
                inspect(mod.generate('easy', seed=seed, template=profile), kid, profile, 'sampled_variant')
        levels = list(mod.SUPPORTED_LEVELS)
        description = 'One instructional template (non-pivot-column identification), 16 source bank profiles; all ask for the subset of non-pivot columns in supplied row echelon form.'
        dependencies = [path.with_suffix('') / n for n in ('source.json', 'snapshot.json', 'capabilities.json')]
    elif kid == 17592186124479:
        profiles = sorted(mod.TEMPLATES)
        for profile in profiles:
            inspect(mod.source_replay(profile), kid, profile, 'source_parameters')
            for seed in range(3):
                inspect(mod.generate('moderate', seed=seed, template=profile), kid, profile, 'sampled_variant')
        levels = list(mod.LEVELS)
        description = '16 source-specific elimination templates, four integer-count bank profiles; every branch asks for one number of pivot columns.'
        dependencies = [path.with_suffix('') / 'reference/source.json', path.with_suffix('') / 'template-extraction.json']
    else:
        raise AssertionError(('Unexpected registered KP', kid))
    assert sha(path) == before, 'Generator changed during audit'
    tested = SAMPLES[start:]
    result = {'kp_id': kid, 'title': kp[':knowledge-point/title'], 'registration': registration,
              'script_sha256': before, 'dependencies': {str(p.relative_to(ROOT)): sha(p) for p in dependencies},
              'supported_levels': levels, 'profiles': profiles, 'branch_review': description,
              'sample_count': len(tested), 'sample_kinds': dict(Counter(s['kind'] for s in tested)),
              'sample_field_types': [':answer-field.type/radio'], 'all_independent_checks_passed': True,
              'decision': 'retain_radio' if kid == 17592186124479 else 'strong_checkbox_candidate',
              'reason': 'The response is one scalar count, not a subset of columns.' if kid == 17592186124479 else 'Each matrix supplies a finite ordered universe of columns; radio options encode subsets. One checkbox per column preserves the task and all old selections.',
              'recommended_field_universe': None if kid == 17592186124479 else 'Every column of the displayed matrix in increasing column order, including columns absent from some old radio choices.',
              'solution_and_difficulty_policy': 'Preserve current mathematical question, solution, and difficulty; add Select all that apply for subset templates.',
              'code_review_complete': True}
    if kid == 17592186124478:
        result['source_anomaly'] = 'Historical generator snapshot q-35391 contains two selection fields, one missing a correct reference. Generator field(sid) explicitly selects its single keyed bank; generated outputs have one keyed field. The live basis-3212 question 17592186124880 has exactly one keyed radio field, 17592186368476. The historical duplicate is not a current migration blocker.'
    if kid == 17592186124479:
        result['excluded_source_profiles'] = mod.EXCLUDED
    return result


if __name__ == '__main__':
    results = [run(kp) for kp in TOPIC[':topic/knowledge-points']]
    sample_path = HERE / 'generator-samples.jsonl'
    sample_path.write_text(''.join(json.dumps(s, ensure_ascii=False) + '\n' for s in SAMPLES))
    result = {'database': SNAPSHOT['database'], 'lineage': SNAPSHOT['lineage'], 'basis': SNAPSHOT['basis'],
              'requested_entity': SNAPSHOT['requested_entity'], 'topic_id': TOPIC[':db/id'],
              'snapshot_sha256': sha(HERE / 'snapshot.json'),
              'scope': 'All four topic KPs and every generator registered at pinned basis; source inspection plus pure local samples, no live generation jobs or writes.',
              'registered_generators': sum(r['registration'] is not None for r in results),
              'decision_counts': dict(Counter(r['decision'] for r in results)),
              'sample_count': len(SAMPLES), 'all_independent_key_checks_passed': True,
              'verification': 'Parsed rendered matrix and all radio choice values; independent Fraction Gaussian elimination determined pivot columns/rank. Every sampled key matched its mathematical subset/count; every option mapped uniquely.',
              'generators': results, 'samples_path': str(sample_path.relative_to(ROOT)),
              'samples_sha256': sha(sample_path), 'database_writes': 0, 'generator_source_edits': 0}
    (HERE / 'generator-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('registered_generators', 'decision_counts', 'sample_count', 'all_independent_key_checks_passed')}, indent=2))
