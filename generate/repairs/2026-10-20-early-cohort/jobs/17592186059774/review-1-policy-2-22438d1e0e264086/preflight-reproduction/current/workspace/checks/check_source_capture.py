"""Regression 43e8c2b7435f7ef1bee2: capture completeness and restored decisions.

Run from any directory with the job Python. Writes only evidence. Mathematical
checks parse visible prompts, choices and solution matrices with Fraction.
"""
import itertools
import json
from pathlib import Path
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from checks.independent import analyze, apply, mats, op, target
import generator as g


def save(name, value):
    (ROOT / 'evidence' / name).write_text(json.dumps(value, indent=2, default=str))


def main():
    capture = json.loads((ROOT.parent / 'source/source.json').read_text())
    source = capture['material']['kp'][':knowledge-point/questions']
    restored = next(q for q in source if q[':question/math-academy-id'] == 'q-72858')
    # Exact retained failure first. Do not let metadata checks substitute for replay.
    replay = g.replay('q-72858')
    analysis = analyze(replay)
    assert mats(replay['question'][':question/problem'])[0] == mats(restored[':question/problem'])[0]
    assert analysis['row_outcome'][1] == [4, 3, 0]
    assert analysis['correct'] == g.normalize_tex('{R}_{2}:={R}_{2}-{R}_{1}')
    assert replay['generation']['source_replay'] is True
    assert replay['generation']['source_question_id'] == restored[':question/id']
    assert replay['generation']['source_basis'] == capture['basis']

    replays, bank_results = [], []
    for q in source:
        sid = q[':question/math-academy-id']
        r = g.replay(sid)
        a = analyze(r)
        f = r['question'][':question/answer-fields'][0]
        sf = q[':question/answer-fields'][0]
        before = [op(v[':answer/value']) for v in sf[':answer-field/choices']]
        after = [op(v[':answer/value']) for v in f[':answer-field/choices']]
        assert len(before) == len(after) == 5 and before == after, sid
        assert mats(q[':question/problem']) == mats(r['question'][':question/problem']), sid
        if sf.get(':answer-field/correct'):
            assert op(a['correct']) == op(sf[':answer-field/correct'][':answer/value']), sid
        if q.get(':question/difficulty'):
            assert r['generation']['source_difficulty'] == q[':question/difficulty'][':db/ident']
        replays.append(r)
        bank_results.append({'profile': sid, 'source_id': q[':question/id'],
                             'choices_matched': len(after), 'math': 'passed',
                             'inferred_completion': not bool(sf.get(':answer-field/correct'))})
    assert len(replays) == len(source) == 11
    save('source-replays.json', replays)
    save('source-replay-results.json', bank_results)

    # Source witness: only subtraction and target-row/third-row swap can win.
    values = [v[':answer/value'] for v in restored[':question/answer-fields'][0][':answer-field/choices']]
    assert [op(v) for v in values][2] == ('linear', 1, [0, -1, 0])
    assert [op(v) for v in values][4] == ('linear', 1, [0, Fraction(4, 3), 0])
    records = []
    for winner in [0, 1]:
        for t in range(3):
            for c in range(3):
                rows = list(range(3)); rows[1], rows[t] = rows[t], rows[1]
                cols = list(range(3)); cols[2], cols[c] = cols[c], cols[2]
                r = g.generate(seed=4200 + t * 3 + c, template='q-72858',
                               parameters={'winner': winner, 'rows': rows, 'cols': cols})
                a = analyze(r)
                assert a['target'] == f'{t+1}{c+1}'
                assert a['kind'] == ('linear' if winner == 0 else 'swap')
                assert len(r['question'][':question/answer-fields'][0][':answer-field/choices']) == 5
                records.append(r)
        for rows in itertools.permutations(range(3)):
            r = g.generate(seed=819, template='q-72858', parameters={'winner': winner, 'rows': list(rows)})
            analyze(r); records.append(r)

    # Switch donor evidence in the target column; a single change would leave
    # both operations successful or neither, so change two decisive entries.
    base = {'source': 'q-72858', 'rows': [0, 1, 2], 'cols': [0, 1, 2], 'order': [0, 1, 2, 3, 4]}
    instances = [dict(base, winner=0, matrix=[[2, 1, 3], [6, 4, 3], [1, 2, 3]]),
                 dict(base, winner=1, matrix=[[2, 1, 4], [6, 4, 3], [1, 2, 0]]),
                 dict(base, winner=0, matrix=[[9, -7, 3], [6, 4, 3], [1, 2, 3]])]
    cf = [g.generate(seed=21, parameters=p) for p in instances]
    aa = [analyze(r) for r in cf]
    assert aa[0]['correct'] != aa[1]['correct']
    assert aa[0]['correct'] == aa[2]['correct']
    for i in [0, 1]:
        assert cf[i]['question'][':question/worked-solution'] != cf[i+1]['question'][':question/worked-solution']
    # Change only the visible target, holding the displayed matrix and bank fixed.
    target_pair = [
        g.generate(seed=21, parameters=dict(base, winner=0,
            matrix=[[4, 1, 3], [3, 4, 3], [0, 2, 2]], cols=[2, 1, 0])),
        g.generate(seed=21, parameters=dict(base, winner=1,
            matrix=[[3, 1, 4], [3, 4, 3], [2, 2, 0]]))]
    ta = [analyze(r) for r in target_pair]
    assert ta[0]['target'] == '21' and ta[1]['target'] == '23'
    assert ta[0]['correct'] != ta[1]['correct']
    assert mats(target_pair[0]['question'][':question/problem']) == mats(target_pair[1]['question'][':question/problem'])
    assert [v[':answer/value'] for v in target_pair[0]['question'][':question/answer-fields'][0][':answer-field/choices']] == [v[':answer/value'] for v in target_pair[1]['question'][':question/answer-fields'][0][':answer-field/choices']]
    # Explicitly reject impossible self-scaling winners and ambiguous evidence.
    rejected = []
    invalid = [dict(base, winner=w) for w in [2, 3, 4]] + [
        dict(base, winner=0, matrix=[[2, 1, 3], [6, 4, 3], [1, 2, 0]]),
        dict(base, winner=0, matrix=[[2, 1, 0], [6, 4, 0], [1, 2, 3]])]
    for p in invalid:
        try:
            g.generate(seed=9, parameters=p)
        except ValueError as error:
            rejected.append(str(error))
        else:
            raise AssertionError(('invalid instance accepted', p))
    # The profile must be reachable via ordinary unforced sampling, not only replay.
    seed = 0
    while seed < 100:
        r = g.generate(seed=seed)
        if r['generation']['bank_profile'] == 'q-72858':
            analyze(r); records.append(r); break
        seed += 1
    assert seed < 100, 'restored profile unavailable in ordinary sampling'
    save('restored-profile-records.json', records)
    save('counterfactual-records.json', cf)
    save('changed-target-records.json', target_pair)
    save('repair-regression-results.json', {'finding': '43e8c2b7435f7ef1bee2',
        'status': 'passed', 'source_banks': len(replays), 'source_choices': 5 * len(replays),
        'restored_records': len(records), 'targets_per_winner': 9,
        'all_row_permutations_per_winner': 6, 'ordinary_sample_seed': seed,
        'rejection_cases': rejected, 'counterfactuals': aa, 'changed_target': ta})
    print(json.dumps({'regression': 'passed', 'banks': len(replays), 'restored_records': len(records)}))


if __name__ == '__main__':
    main()
