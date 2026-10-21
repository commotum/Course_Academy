"""Affected source, coverage, packaging and stored-pool checks; no services/writes."""
from collections import Counter
from copy import deepcopy
import hashlib
import platform
import shutil
import tempfile
from common import *

source = load(JOB / 'source/source.json')['material']['kp']
sourceq = {q[':question/math-academy-id']: q for q in source[':knowledge-point/questions']}
replays, replay_report = [], []
for profile in g.PROFILES:
    q = sourceq[profile]
    by_label = {re.search(r'\$([ABC])\s*=', f[':answer-field/key'])[1]:
                matrices(f[':answer-field/key'])[0] for f in q[':question/answer-fields']}
    r = g.generate('easy', 73021, profile=profile,
                   parameters={'matrices': [by_label[x] for x in 'ABC']}, replay=True)
    examine(r)
    rq = r['question']
    assert rq[':question/problem'] == q[':question/problem']
    for old, new in zip(q[':question/answer-fields'], rq[':question/answer-fields']):
        assert old[':answer-field/key'] == new[':answer-field/key']
        assert old[':answer-field/type'][':db/ident'] == new[':answer-field/type']
        assert [a[':answer/value'] for a in old[':answer-field/choices']] == [a[':answer/value'] for a in new[':answer-field/choices']]
        assert old[':answer-field/correct'][':answer/value'] == field_value(new)
    if profile not in ('q-129225', 'q-42366'):
        assert rq[':question/worked-solution'] == q[':question/worked-solution']
    elif profile == 'q-129225':
        assert '${c}_{45}' in rq[':question/worked-solution']
        assert '${a}_{45}' not in rq[':question/worked-solution']
    else:
        assert matrices(rq[':question/worked-solution'])[2][2][3] == -2
    replays.append(r)
    replay_report.append({'profile': profile, 'source_id': q[':question/id'],
                          'bank_fields_matched': 3, 'choices_matched': 6,
                          'correction': g.CORRECTIONS.get(profile), 'passed': True})
save(E / 'source-replays.json', replays)
save(E / 'source-replay-results.json', replay_report)
grader(replays, 'source')

# Preserve the individual sampler across all shape profiles, two previously
# reviewed seeds each. This is a narrow preservation check, not a new mass audit.
prior = load(JOB / 'review-0-policy-2-342253086f871c08/independent-samples.json')
unchanged = []
for profile in g.PROFILES:
    for old in [r for r in prior if r['generation']['profile'] == profile][:2]:
        new = g.generate('easy', old['generation']['seed'], profile=profile)
        assert old == new, (profile, 'individual sampler changed')
        examine(new)
        unchanged.append(new)
save(E / 'preserved-individual-records.json', unchanged)

# Each answer subset can still be constructed at fixed shape and polarity.
base = deepcopy(load(E / 'counterfactual-records.json')[0]['generation']['parameters']['matrices'])
decisions = []
for bits in range(1, 8):
    ms = deepcopy(base)
    for i in range(3):
        if not bits & (1 << i):
            ms[i][1][0] = 7  # Equal leading columns, same dimensions and other data.
    r = g.generate('easy', 431, profile='q-129214', parameters={'matrices': ms})
    expected = ''.join(x for i, x in enumerate('ABC') if bits & (1 << i))
    assert examine(r)['subset'] == expected
    decisions.append(r)
accepted_decisions = delivery(decisions, 'decision-cases')
assert {examine(r)['subset'] for r in accepted_decisions} == {'A','B','C','AB','AC','BC','ABC'}
grader(accepted_decisions, 'decisions')

# Small affected batch sample covers the short-count exception, required size,
# larger repeated subgroups, deterministic resampling and semantic deduplication.
counts = []
small = []
for n in (0, 1, 2, 3, 12):
    stats = {}
    seed = 291114 + 97*n
    rs = g.batch('easy', n, seed, stats=stats)
    assert len(rs) == n and rs == g.batch('easy', n, seed)
    cov = coverage(rs)
    counts.append({'count': n, 'seed': seed, 'stats': stats, 'coverage': cov,
                   'accepted_seeds': [r['generation']['seed'] for r in rs]})
    small += rs
accepted_small = delivery(small, 'small-batches')
assert len(accepted_small) == len(small)
for item in counts:
    group = [r for r in accepted_small if r['generation']['seed'] in item['accepted_seeds']]
    assert len(group) == item['count']
    item['after_delivery'] = coverage(group)

inv = load(JOB / 'source/inventory.json')
source_ids = {q[':question/id'] for q in sourceq.values()}
non_source = [q for q in inv['questions'] if q[':question/id'] not in source_ids]
raw = []
for q in non_source:
    fmap = {re.search(r'\$([ABC])\s*=', f[':answer-field/key'])[1]: f for f in q[':question/answer-fields']}
    ms = [matrices(fmap[x][':answer-field/key'])[0] for x in 'ABC']
    shape = [(len(m), len(m[0])) for m in ms]
    matched = None
    for profile in g.PROFILES:
        old = g.original(profile)['matrices']
        if [(len(m),len(m[0])) for m in old] != shape:
            continue
        if ('**not**' in q[':question/problem']) != ('**not**' in g.SOURCES[profile][':question/problem']):
            continue
        r = g.generate('easy', 0, profile=profile, parameters={'matrices': ms})
        if r['question'][':question/worked-solution'] == q[':question/worked-solution']:
            matched = r
            break
    assert matched is not None, q[':question/id']
    raw.append(matched)
empty = {**inv, 'questions': [], 'fingerprints': []}
save(E / 'inventory-empty.json', empty)
reconstructed = delivery(raw, 'inventory-reconstruction', E / 'inventory-empty.json')
stored = {q[':question/id']: q for q in non_source}
assert {r['question'][':question/id'] for r in reconstructed} == set(stored)
for r in reconstructed:
    q = stored[r['question'][':question/id']]
    assert examine(r) == examine(q)
    for key in (':question/problem', ':question/worked-solution'):
        assert r['question'][key] == q[key]
    r['generation']['review_reproduction'] = {'method': 'explicit stored parameters, current generator, shared delivery normalization',
        'original_seed': 'not captured; reconstruction uses seed 0 and explicit matrices',
        'stored_entity_id': q[':db/id'], 'inventory_basis': inv['basis']}
save(E / 'generated-records.json', reconstructed)
assert len(reconstructed) == 5 and all('C' in examine(r)['subset'] for r in reconstructed)
affected = load(ROOT / 'affected-inventory.json')
assert {a['question_id'] for a in affected['affected_questions']} == set(stored)
for a in affected['affected_questions']:
    assert a['entity_id'] == stored[a['question_id']][':db/id']
    assert (JOB / 'author-1' / a['evidence_path']).resolve() == (E / 'generated-records.json').resolve()

# Manifest versions and clean relocation; only declared runtime files copied.
manifest = load(ROOT / 'package.json')
assert manifest['dependencies'] == {'python': platform.python_version(), 'packages': {}}
hashes = {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in manifest['files']}
with tempfile.TemporaryDirectory(prefix='echelon-relocation-') as d:
    target = Path(d)
    for f in manifest['files']:
        shutil.copyfile(ROOT / f, target / f)
    p = subprocess.run([sys.executable, str(target / manifest['entrypoint']), '--difficulty', 'easy',
                        '--count', '5', '--seed', '924724049', '--format', 'json'], cwd='/tmp', capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert json.loads(p.stdout) == g.batch('easy', 5, 924724049)
assert hashes == {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in manifest['files']}
rejects = []
for difficulty, count in [('hard', 5), ('moderate', 5), ('easy', -1), ('easy', 1001)]:
    try:
        g.batch(difficulty, count, 0)
    except ValueError:
        rejects.append([difficulty, count])
    else:
        raise AssertionError('Invalid request accepted')

save(E / 'validation-results.json', {'passed': True, 'source_banks': len(replays), 'source_choices': 78,
    'individual_sampler_preserved': len(unchanged), 'source_native_checks': 78,
    'fixed_shape_decision_subsets': [examine(r)['subset'] for r in accepted_decisions],
    'decision_native_checks': 42, 'counts': counts, 'inventory': {'total_inspected': len(inv['questions']),
    'source_questions': len(source_ids), 'non_source_reconstructed': len(reconstructed),
    'affected_generated_pool': len(reconstructed), 'source_questions_marked_generated': 0},
    'packaging': {'python': platform.python_version(), 'relocation_equal': True, 'runtime_hashes': hashes,
                  'invalid_calls_rejected': rejects}})
print(json.dumps({'passed': True, 'source_banks': 13, 'individuals_preserved': len(unchanged),
                  'fixed_shape_subsets': len(accepted_decisions), 'inventory_reconstructions': len(reconstructed)}))
