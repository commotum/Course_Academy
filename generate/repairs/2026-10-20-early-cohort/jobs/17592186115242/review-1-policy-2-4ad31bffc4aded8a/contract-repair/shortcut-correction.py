"""Bounded, read-only replay of the reported decision shortcut.

Run: <job-python> -B contract-repair/shortcut-correction.py --strict
Exit 1 means the exact delivered pool still contains the demonstrated defect.
No random search, package edits, publication, or database calls.
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
E = OUT.parent
JOB = E.parent
W = JOB / 'workspace'
read = lambda p: json.loads(p.read_text())


def inspect(r):
    q = r['question']
    body = q[':question/problem'].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
    rows = []
    for row in body.split(r'\\'):
        left, right = row.replace('&', '').replace(' ', '').split('=')
        rows.append((left, int(right.rstrip(', .'))))
    def coefficient(text):
        return -1 if text == '-' else 1 if text in ('', '+') else int(text)
    first = re.fullmatch(r'([+-]?\d*)x([+-]\d*)y', rows[0][0])
    second = re.fullmatch(r'([+-]?\d*)x\+ky', rows[1][0])
    assert first and second, 'This bounded probe only parses the captured easy family'
    a, b, d = coefficient(first[1]), coefficient(first[2]), coefficient(second[1])
    root = Fraction(b*d, a)
    residual = Fraction(rows[1][1]) - Fraction(d*rows[0][1], a)
    assert residual != 0
    field = q[':question/answer-fields'][0]
    choices = field[':answer-field/choices']
    key = next(c for c in choices if c[':answer/id'] == field[':answer-field/correct'][1])
    value = lambda c: Fraction(c[':answer/value'].split('=')[1])
    assert value(key) == root
    guess = (max if b*d/a > 0 else min)(choices, key=value)
    return dict(id=q[':question/id'], seed=r['generation']['seed'], parameters=r['generation']['parameters'],
                problem=q[':question/problem'], options=[c[':answer/value'] for c in choices],
                correct=key[':answer/value'], root=str(root), residual=str(residual),
                sign_group='same_sign' if b*d/a > 0 else 'opposite_sign',
                shortcut_answer=guess[':answer/value'], shortcut_correct=guess == key)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    batch = read(E/'runner-batch.json')
    assert batch == read(JOB/'samples.json'), 'Runner batch changed'
    delivered = read(E/'delivery-batch/accepted.json')
    # Publisher normalization intentionally assigns fresh public IDs.
    signature = lambda r: (r['generation']['seed'], r['question'][':question/problem'],
        tuple(sorted(c[':answer/value'] for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])))
    assert {signature(r) for r in delivered} == {signature(r) for r in batch}
    current = [inspect(r) for r in delivered]
    subgroup = [r for r in current if r['sign_group'] == 'opposite_sign']
    assert len(subgroup) == 2 and all(r['shortcut_correct'] for r in subgroup)
    # Replay precisely the two current seeds, rather than a new large audit.
    sys.path.insert(0, str(W))
    spec = importlib.util.spec_from_file_location('review_target', W/'17592186115242.py')
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    replayed = [gen.generate('easy', seed=r['seed']) for r in subgroup]
    originals = {r['question'][':question/id']: r for r in batch}
    for r in replayed:
        assert r == originals[r['question'][':question/id']]
    (OUT/'batch-counterexamples.json').write_text(json.dumps(replayed, indent=2)+'\n')
    historical = [inspect(r) for r in read(E/'generated-records.json')]
    assert len(historical) == 5 and all(r['shortcut_correct'] for r in historical)
    inventory = read(JOB/'source/inventory.json')
    by_id = {q[':question/id']: q for q in inventory['questions']}
    for r in read(E/'generated-records.json'):
        q = r['question']; stored = by_id[q[':question/id']]
        for name in [':question/problem', ':question/worked-solution']:
            assert q[name] == stored[name]
        f, sf = q[':question/answer-fields'][0], stored[':question/answer-fields'][0]
        assert f[':answer-field/correct'][1] == sf[':answer-field/correct'][':answer/id']
        assert sorted((c[':answer/id'], c[':answer/value']) for c in f[':answer-field/choices']) == sorted((c[':answer/id'], c[':answer/value']) for c in sf[':answer-field/choices'])
    # Existing evidence stores the exact per-file hashes; recheck every bound file.
    hashes = read(E/'package-unchanged.json')['hashes']
    changed = [name for name, digest in hashes.items() if not (W/name).is_file() or hashlib.sha256((W/name).read_bytes()).hexdigest() != digest]
    assert not changed, changed
    report = dict(command=f'{sys.executable} -B contract-repair/shortcut-correction.py --strict',
                  inventory_basis=inventory['basis'], batch=current, delivered_opposite_sign=subgroup,
                  current_seed_replays=2, historical_inventory=historical,
                  actual_batch_sign_strategy=dict(correct=sum(r['shortcut_correct'] for r in current),total=5,baseline=.2),
                  conditional_batch_strategy=dict(correct=2,total=2,baseline=.2),
                  historical_strategy=dict(correct=5,total=5,baseline=.2),
                  package_files_rechecked=len(hashes), package_unchanged=True,
                  strict_passed=not (len(subgroup) > 1 and all(r['shortcut_correct'] for r in subgroup))
                      and not all(r['shortcut_correct'] for r in historical),
                  interpretation='Current generator construction is repaired; these failures concern the finite delivered batch and still-selectable captured historical pool. Larger controls cannot waive either pool. No universal v3 sign shortcut claimed.')
    (OUT/'shortcut-correction-results.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['batch','delivered_opposite_sign','historical_inventory']}))
    return 1 if args.strict and not report['strict_passed'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
