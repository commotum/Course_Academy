"""Focused changed-profile checks plus a small sample of preserved profiles."""
from collections import Counter, defaultdict
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
from source_coverage import ROOT, g, read_task, witness
E = ROOT / 'evidence'


def save(name, value):
    (E / name).write_text(json.dumps(value, indent=2)+'\n')


def coverage(records):
    items = [witness(r) for r in records]
    return {'count': len(items),
            'semantic_instances': len({json.dumps([x['rows'], list(zip(x['columns'], x['entries']))]) for x in items}),
            'rows': dict(Counter(str(x['rows']) for x in items)),
            'columns': dict(Counter(str(c) for x in items for c in x['columns'])),
            'ranks': dict(Counter(str(x['rank']) for x in items)),
            'positions': dict(Counter(str(x['position']) for x in items)),
            'sum_signs': dict(Counter(str((x['total']>0)-(x['total']<0)) for x in items))}


def shortcuts(records):
    groups = defaultdict(list)
    for record in records:
        a = witness(record)
        groups['template/'+str(len(a['rows']))].append(a)
        bank = sorted(a['bank'])
        groups['visible-bank-gaps/'+str([v-u for u, v in zip(bank, bank[1:])])].append(a)
    results = {}
    for name, items in groups.items():
        strategies = {**{'position '+str(i): (lambda a, i=i: a['bank'][i]) for i in range(5)},
                      **{'rank '+str(i): (lambda a, i=i: sorted(a['bank'])[i]) for i in range(5)},
                      'diagonal': lambda a: sum(a['matrix'][r][r] for r in a['rows']),
                      'first column': lambda a: sum(a['matrix'][r][0] for r in a['rows']),
                      'last column': lambda a: sum(a['matrix'][r][-1] for r in a['rows']),
                      'ignore requested rows': lambda a: sum(next(x for x in row if x) for row in a['matrix'])}
        counts = {key: sum(fn(a)==a['total'] for a in items) for key, fn in strategies.items()}
        results[name] = {'attempts': len(items), 'correct': counts,
                         'uniform_choice_baseline': 0.2,
                         'interpretation': 'finite sample; small bank subgroups are descriptive only'}
        if len(items) >= 8:
            assert max(counts.values()) < len(items), (name, counts)
    return results


def main():
    sources = json.loads((E / 'source-cases.json').read_text())
    original = {q[':question/math-academy-id']:q for q in sources}
    normal = [g.generate(seed=8800+i, profile='q-129207') for i in range(30)]
    normal += [g.generate(seed=9900+i, profile=p) for i, p in enumerate(sorted(original)) if p!='q-129207']
    # Check every new/retained bank against independently captured full shapes.
    for record in normal:
        profile = record['generation']['bank_profile']
        expected = sorted(int(a[':answer/value']) for a in original[profile][':question/answer-fields'][0][':answer-field/choices'])
        bank = sorted(witness(record)['bank'])
        assert [x-bank[0] for x in bank] == [x-expected[0] for x in expected]
    before = coverage(normal[:30])
    assert set(before['ranks']) == set(before['positions']) == set(map(str, range(5)))
    assert len(before['rows']) == 4 and set(before['columns']) == set(map(str, range(4)))
    assert set(before['sum_signs']) == {'-1', '0', '1'}
    assert before['semantic_instances'] == 30
    save('normal-records.json', normal)
    save('normal-coverage.json', {'new_profile': before, 'all': coverage(normal)})
    save('shortcuts-before.json', shortcuts(normal))

    matrix, rows = read_task(original['q-129207'][':question/problem'])
    base = {'matrix': matrix, 'rows': rows}
    cases = [('base', base, 3)]
    p = copy.deepcopy(base); p['matrix'][1][1] = 8
    cases.append(('leading value', p, 4))
    p = copy.deepcopy(base); p['matrix'][1][0] = 5
    cases.append(('earlier nonzero', p, 1))
    p = copy.deepcopy(base); p['rows'] = [0, 1, 2]
    cases.append(('changed target, same matrix', p, 12))
    p = copy.deepcopy(base); p['matrix'][1][3] = -9
    cases.append(('trailing entry', p, 3))
    p = copy.deepcopy(base); p['matrix'][0] = [9, 8, 7, 6]
    cases.append(('unselected row', p, 3))
    controlled = []
    results = []
    for label, params, expected in cases:
        record = g.generate(seed=817, profile='q-129207', parameters=params, anchor_rank=2)
        assert witness(record)['total'] == expected
        controlled.append(record)
        results.append({'case': label, 'expected': expected, 'visible_witness': witness(record)})
    for a, b in [(0, 1), (0, 2), (0, 3)]:
        assert controlled[a]['question'][':question/problem'] != controlled[b]['question'][':question/problem']
        assert controlled[a]['question'][':question/worked-solution'] != controlled[b]['question'][':question/worked-solution']
        assert witness(controlled[a])['bank'] != witness(controlled[b])['bank']
    for a, b in [(0, 4), (0, 5)]:
        assert witness(controlled[a])['bank'] == witness(controlled[b])['bank']
    # Each anchor remains reachable with the mathematical task held constant.
    anchors = [g.generate(seed=817, profile='q-129207', parameters=base, anchor_rank=i) for i in range(5)]
    assert [witness(r)['rank'] for r in anchors] == list(range(5))
    assert len({r['question'][':question/problem'] for r in anchors}) == 1
    save('counterfactual-records.json', controlled+anchors)
    save('counterfactual-results.json', results)

    replays = json.loads((E / 'source-replay-records.json').read_text())
    grade = []
    for i, record in enumerate(replays+normal+controlled+anchors):
        observed = witness(record)
        grade.append({'label': f'independent visible sum {i}: {observed["total"]}', 'record': record,
                      'checks': [{'submitted_answer_id': a[':answer/id'],
                                  'expected': 'accepted' if int(a[':answer/value'])==observed['total'] else 'rejected',
                                  'purpose': 'independent first-nonzero sum; every radio option'}
                                 for a in record['question'][':question/answer-fields'][0][':answer-field/choices']]})
    save('grader-input.json', grade)
    save('render-records.json', [replays[-1], normal[1], controlled[3]])
    assert g.generate(seed=8800, profile='q-129207') == normal[0]
    manifest = json.loads((ROOT / 'package.json').read_text())
    relocated = E / 'relocated-package'
    relocated.mkdir(exist_ok=True)
    for name in manifest['files']:
        shutil.copyfile(ROOT / name, relocated / name)
    args = ['--difficulty', 'easy', '--count', '5', '--seed', '817', '--format', 'json']
    local = subprocess.run([sys.executable, '-B', str(ROOT/'generator.py'), *args], capture_output=True, text=True, check=True)
    moved = subprocess.run([sys.executable, '-B', str(relocated/'generator.py'), *args], cwd=relocated, capture_output=True, text=True, check=True)
    assert local.stdout == moved.stdout
    save('batch-records.json', json.loads(local.stdout))
    save('packaging-results.json', {'deterministic': True, 'relocation_identical': True,
                                   'python': sys.version.split()[0], 'sympy': g.sp.__version__,
                                   'manifest': manifest, 'cli_count': len(json.loads(local.stdout)),
                                   'value_sampling_attempts_max': max(r['generation']['value_sampling_attempts'] for r in normal)})
    print(json.dumps({'normal': len(normal), 'new_profile_coverage': before,
                      'controlled': len(controlled), 'anchors': len(anchors), 'grader_records': len(grade)}))


if __name__ == '__main__':
    main()
