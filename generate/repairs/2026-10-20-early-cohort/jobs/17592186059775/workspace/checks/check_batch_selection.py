"""Strict visible-record regression for finding 9e827407d5429a1f8827.

No services, DB writes or runtime-package mutations. --input also checks the
archived failure and the actual normalized delivery output independently.
"""
import argparse
import collections
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_repair import E, JOB, REPO, g, key, save, v


def inspect(records):
    rows = []
    for r in records:
        q = r['question']
        supplied, = v.printed_matrices(q[':question/problem'])
        field = q[':question/answer-fields'][0]
        choices = field[':answer-field/choices']
        ordered = sorted(choices, key=lambda a: v.printed_matrices(a[':answer/value'])[0][1, 2])
        correct = key(r)
        rank = next(i for i, a in enumerate(ordered) if a == correct)
        position = choices.index(correct)
        guessed = ordered[3 if supplied[0, 0] == 1 else 0]
        # Recognizable family derives from visible coefficients and task shape.
        family = (tuple(map(str, supplied[:, :2])), 'and then solve' in q[':question/problem'])
        rows.append({'id': q[':question/id'], 'family': family,
                     'rank': rank, 'position': position,
                     'shortcut_hit': guessed == correct,
                     'upper_row': tuple(map(str, supplied[0, :])),
                     'lower_rhs': str(supplied[1, 2]),
                     'bank': tuple(a[':answer/value'] for a in choices)})
    return rows


def strict_shortcut(records):
    rows = inspect(records)
    hits = sum(r['shortcut_hit'] for r in rows)
    assert rows and hits < len(rows), 'Reported pivot/rank shortcut answers every member'
    return {'correct': hits, 'total': len(rows), 'random_baseline': 0.2}


def contrast_bank(records):
    rows = inspect(records)
    assert len(rows) == 5
    assert len({r['family'] for r in rows}) == 1
    assert len({r['bank'] for r in rows}) == 1
    assert len({r['upper_row'] for r in rows}) == 1
    assert len({r['lower_rhs'] for r in rows}) == 5
    assert {r['rank'] for r in rows} == set(range(5)), 'Fixed-rank family shortcut'
    assert {r['position'] for r in rows} == set(range(5)), 'Fixed-position family shortcut'
    for r in records:
        v.independent(r)  # Exact elimination, every intermediate and unique key.
    return {'family': rows[0]['family'], 'ranks': [r['rank'] for r in rows],
            'positions': [r['position'] for r in rows],
            'lower_rhs': [r['lower_rhs'] for r in rows],
            'fixed_ordered_bank_and_upper_row': True,
            'pivot_shortcut': strict_shortcut(records)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path)
    args = parser.parse_args()
    if args.input:
        records = json.loads(args.input.read_text())
        print(json.dumps(strict_shortcut(records)))
        return
    failing_seed = 4258185931
    sample = g.batch('easy', 5, failing_seed)
    save('batch-repair-records.json', sample)
    report = {'finding_id': '9e827407d5429a1f8827', 'seed': failing_seed,
              'raw_exact_batch': contrast_bank(sample), 'profiles': {}}
    for band, seed in [('easy', 0), ('moderate', 17)]:
        catalog = g.candidates(band, seed)
        total = len({g.fingerprint(r['question']) for r in catalog})
        full = g.batch(band, total, seed)
        # No source family or semantic instance was sacrificed to repair selection.
        def signature(r):
            m, = v.printed_matrices(r['question'][':question/problem'])
            normalized = []
            for i in range(2):
                row = list(m[i, :]); pivot = next(z for z in row if z)
                normalized.append(tuple(str(z/pivot) for z in row))
            return ('and then solve' in r['question'][':question/problem'], tuple(sorted(normalized)))
        assert len(full) == total == len({signature(r) for r in full})
        assert {signature(r) for r in full} == {signature(r) for r in catalog}
        profiles = {sid for sid in g.CASES if g.level(sid) == band}
        prefix = full[:5*len(profiles)]
        assert {r['generation']['template'] for r in prefix} == profiles
        groups = [contrast_bank(prefix[i:i+5]) for i in range(0, len(prefix), 5)]
        report['profiles'][band] = {'seed': seed, 'semantic_instances_preserved': total,
                                    'complete_prefix_banks': groups}
        # Any repeated visible family in the tested pool has several answer roles.
        grouped = collections.defaultdict(list)
        for row in inspect(full):
            grouped[row['family']].append(row)
        for family, rows in grouped.items():
            assert {r['rank'] for r in rows} == set(range(5)), family
            assert len({r['position'] for r in rows}) > 1, family
    # Exercise the publisher's actual captured-inventory/difficulty filters.
    out = E/'delivery-batch-repair'
    command = [sys.executable, str(REPO/'generate/pipeline/check_delivery.py'),
               '--input', str(E/'batch-repair-records.json'),
               '--source', str(JOB/'source/source.json'),
               '--inventory', str(JOB/'source/inventory.json'), '--difficulty', 'easy',
               '--output', str(out), '--asset-root', str(E/'assets'),
               '--math-root', '/media/jake/SSD/EDB/math']
    subprocess.run(command, check=True)
    accepted = json.loads((out/'accepted.json').read_text())
    report['delivered_exact_batch'] = contrast_bank(accepted)
    report['delivery_command'] = command
    report['delivery'] = json.loads((out/'delivery.json').read_text())
    native = [{'label': 'actual delivered batch '+str(i), 'record': r,
               'checks': v.checks(r)} for i, r in enumerate(accepted)]
    save('batch-repair-native-input.json', native)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),
                    str(E/'batch-repair-native-input.json'),
                    str(E/'batch-repair-native-report.json')], check=True)
    report['native_responses'] = sum(len(c['checks']) for c in native)
    save('batch-selection-regression.json', report)
    print(json.dumps({'passed': True, 'raw': report['raw_exact_batch']['pivot_shortcut'],
                      'delivered': report['delivered_exact_batch']['pivot_shortcut'],
                      'profiles_checked': 10, 'native_responses': report['native_responses']}))


if __name__ == '__main__':
    main()
