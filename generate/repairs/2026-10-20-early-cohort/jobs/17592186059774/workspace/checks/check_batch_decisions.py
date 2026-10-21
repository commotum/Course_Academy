"""Regression 7db753d2c3e5a969a0e7: inspect finite delivered decision groups.

Only writes evidence; delivery uses the shared database-free helper. The exact
reviewed proposal seeds drive the real batch function through its RNG boundary.
No generator records, arithmetic, keys, or delivery results are mocked.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path
import random
import subprocess
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generator as g
from checks.independent import analyze, op

OUT = ROOT / 'evidence/batch-repair'
REPO = ROOT.parents[5]
RANDOM = random.Random


def save(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, default=str))


def proposals(seeds, count=None):
    """Replay the reviewed proposal stream without depending on its unknown parent seed."""
    sentinel = 'retained proposal stream'
    stream = iter(seeds)
    class Outer:
        def getrandbits(self, bits):
            assert bits == 64
            return next(stream)
    with patch.object(g.random, 'Random', side_effect=lambda seed: Outer() if seed == sentinel else RANDOM(seed)):
        return g.batch('hard', len(seeds) if count is None else count, sentinel)


def visible_probe(records):
    groups = defaultdict(list)
    for r in records:
        a = analyze(r)
        f = r['question'][':question/answer-fields'][0]
        # This cue ignores both the matrix and the target coordinate.
        candidates = [i for i, v in enumerate(f[':answer-field/choices'])
                      if (o := op(v[':answer/value']))[0] == 'linear'
                      and sum(c != 0 for c in o[2]) == 2]
        groups[r['generation']['bank_profile']].append({
            'id': a['id'], 'kind': a['kind'], 'position': a['position'],
            'sole_distinct_row_cue': len(candidates) == 1 and candidates[0] == a['position']})
    report = {}
    for sid, group in groups.items():
        kinds = Counter(r['kind'] for r in group)
        report[sid] = {'count': len(group), 'kinds': dict(kinds),
                       'positions': dict(Counter(r['position'] for r in group)),
                       'cue_successes': sum(r['sole_distinct_row_cue'] for r in group),
                       'records': group}
        if len(group) > 1:
            assert set(kinds) == {'swap', 'linear'}, ('fixed operation case', sid, report[sid])
        if sid == 'q-72858' and len(group) > 1:
            assert 0 < report[sid]['cue_successes'] < len(group), report[sid]
    return report


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    retained = json.loads((OUT / 'retained-runner-batch.json').read_text())
    # Test current construction against the EXACT two failing instances first.
    for r in retained:
        p = r['generation']
        replay = g.generate(seed=p['seed'], parameters=p['parameters'])
        assert replay['question'] == r['question']
        analyze(replay)
    exact = proposals([r['generation']['seed'] for r in retained])
    save('exact-current-records.json', exact)
    try:
        exact_probe = visible_probe(exact)
    except AssertionError as error:
        save('regression-results.json', {'status': 'failed', 'finding': '7db753d2c3e5a969a0e7', 'failure': str(error)})
        raise
    assert exact_probe['q-72858']['count'] == 2

    # Every bank uses the same scheduler: find one ordinary seed per bank, then
    # repeat that proposal. A second case must be constructed before deduping.
    seeds = {}
    for seed in range(100):
        r = g.generate(seed=seed)
        seeds.setdefault(r['generation']['bank_profile'], seed)
        if set(seeds) == set(g.CASES):
            break
    assert set(seeds) == set(g.CASES), 'ordinary profile coverage incomplete'
    discovery_attempts = seed + 1
    family = []
    family_probes = {}
    for sid, seed in seeds.items():
        pair = proposals([seed, seed])
        family_probes[sid] = visible_probe(pair)[sid]
        assert len({r['generation']['mathematical_fingerprint'] for r in pair}) == 2
        family.extend(pair)
    ordinary = g.batch('hard', 5, 59774)
    ordinary_probe = visible_probe(ordinary)
    assert g.batch('hard', 0, 13) == []
    assert len(g.batch('hard', 1, 13)) == 1
    assert g.batch('hard', 5, 59774) == ordinary
    # The exact reviewed pool and the ordinary five-item pool are filtered
    # separately: pooled controls must never conceal a defective small batch.
    delivery_probes = {}
    for name, records in [('exact', exact), ('ordinary', ordinary), ('family', family)]:
        save(name + '-records.json', records)
        destination = OUT / ('delivery-' + name)
        command = [sys.executable, str(REPO / 'generate/pipeline/check_delivery.py'),
                   '--input', str(OUT / (name + '-records.json')),
                   '--source', str(ROOT.parent / 'source/source.json'),
                   '--inventory', str(ROOT.parent / 'source/inventory.json'),
                   '--difficulty', 'hard', '--output', str(destination),
                   '--math-root', '/media/jake/SSD/EDB/math']
        result = subprocess.run(command, capture_output=True, text=True)
        save('delivery-' + name + '-command.json', {'command': command, 'exit_code': result.returncode,
                                                  'stdout': result.stdout, 'stderr': result.stderr})
        assert result.returncode == 0, result.stderr
        accepted = json.loads((destination / 'accepted.json').read_text())
        assert len(accepted) == len(records), ('decision witness lost in delivery', name)
        delivery_probes[name] = visible_probe(accepted)
    all_records = exact + ordinary + family
    for r in all_records:
        meta = r['generation']
        assert g.generate(seed=meta['seed'], parameters=meta['parameters'])['question'] == r['question']
    save('regression-results.json', {'status': 'passed', 'finding': '7db753d2c3e5a969a0e7',
         'retained_replays': len(retained), 'exact_before_delivery': exact_probe,
         'ordinary_before_delivery': ordinary_probe, 'family_before_delivery': family_probes,
         'after_delivery': delivery_probes, 'ordinary_profile_seeds': seeds,
         'profile_discovery_attempts': discovery_attempts,
         'limits': ['No claim of both decisions within a single question.',
                    'Live history and policy may select subsets of any finite pool.']})
    save('grader-input.json', [
        {'label': str(i), 'record': r,
         'checks': [{'field_index': 0, 'submitted_answer_id': a[':answer/id'],
                     'expected': 'accepted' if j == analyze(r)['position'] else 'rejected',
                     'purpose': 'visible Fraction arithmetic on each candidate'}
                    for j, a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices'])]}
        for i, r in enumerate(all_records)])
    save('render-records.json', exact)
    print(json.dumps({'regression': 'passed', 'exact_restored_cue': str(exact_probe['q-72858']['cue_successes']) + '/2',
                      'family_banks': len(seeds), 'delivered_records': len(all_records)}))


if __name__ == '__main__':
    main()
