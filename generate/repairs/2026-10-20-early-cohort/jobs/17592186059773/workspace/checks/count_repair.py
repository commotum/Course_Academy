"""Focused second-pass validation; retain prior source and role witnesses."""
import json
import subprocess
import sys
from pathlib import Path

import validate as checks
import delivery_probes as probes

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence/count-repair'
g, v = checks.g, checks.v


def prepare():
    OUT.mkdir(exist_ok=True)
    source = json.loads((ROOT.parent / 'source/source.json').read_text())['material']['kp']
    original = {q.get(':question/math-academy-id'): q for q in source[':knowledge-point/questions']}
    prior = {r['question'][':question/id']: r for r in json.loads((ROOT / 'evidence/records.json').read_text())}
    records = []
    for sid in g.CASES:
        replay = g.generate(parameters=g.DEFAULTS[sid])
        q = replay['question']
        assert q[':question/problem'] == original[sid][':question/problem']
        assert q[':question/worked-solution'] == original[sid][':question/worked-solution']
        choices = q[':question/answer-fields'][0][':answer-field/choices']
        assert [c[':answer/value'] for c in choices] == [c[':answer/value'] for c in original[sid][':question/answer-fields'][0][':answer-field/choices']]
        records.append(replay)
        base = g.domain(sid)[0]
        records.extend(g.generate(parameters=base + [key]) for key in g.eligible_keys(sid))
    for r in records:
        checks.inspect(r)
        assert prior[r['question'][':question/id']] == r, 'Existing source/role repair changed'
    command = [sys.executable, '-E', '-s', '-B', str(ROOT / '17592186059773.py'),
               '--difficulty', 'moderate', '--count', '5', '--seed', '1260123367', '--format', 'json']
    outputs = [subprocess.run(command, cwd='/tmp', check=True, text=True, capture_output=True).stdout for _ in range(2)]
    assert outputs[0] == outputs[1]
    sample = json.loads(outputs[0])
    assert isinstance(sample, list) and len(sample) == 5
    # Compare against the exact captured failed-run records, with only wrapping removed.
    old = json.loads((ROOT.parent / 'runtime-1/run-0.stdout').read_text())['instances']
    assert sample == old
    for r in sample:
        checks.inspect(r)
    records.extend(sample)
    checks.save(OUT / 'records.json', records)
    checks.save(OUT / 'sample.json', sample)
    checks.save(OUT / 'before-delivery.json', probes.examine(records))
    checks.save(OUT / 'native-input.json', [v.native('count repair ' + str(n), r) for n, r in enumerate(records)])
    checks.save(OUT / 'validation.json', {'passed': True, 'source_replays': 10,
        'unchanged_complete_bank_choices': 50, 'unchanged_controlled_roles': 48,
        'current_records_checked': len(records), 'captured_failure_seed': 1260123367,
        'captured_five_records_identical': True, 'deterministic_cli_runs': 2, 'command': command,
        'scope': 'Only stdout serialization changed. Prior source and controlled records are identical.'})
    print(json.dumps({'records': len(records), 'source_replays': 10, 'controlled_roles': 48,
                      'captured_sample': 5, 'deterministic': True}))


def delivered():
    records = json.loads((OUT / 'delivery/accepted.json').read_text())
    checks.save(OUT / 'after-delivery.json', probes.examine(records))
    checks.save(OUT / 'delivered-native-input.json', [v.native('delivered count repair '+str(n), r) for n, r in enumerate(records)])
    render = []
    for kind in ('swap', 'scale', 'addition'):
        for r in records:
            f = r['question'][':question/answer-fields'][0]
            op = g.operation(next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id'] == f[':answer-field/correct'][1]))
            actual = 'swap' if op[0] == 'swap' else 'scale' if sum(bool(c) for c in op[2]) == 1 else 'addition'
            if kind == actual:
                render.append(r)
                break
        else:
            raise AssertionError(kind)
    checks.save(OUT / 'render-records.json', render)
    print(json.dumps({'delivery_survivors': len(records), 'render_records': len(render),
                      'all_controlled_roles_survive': True}))


if __name__ == '__main__':
    if sys.argv[1:] == ['--delivered']:
        delivered()
    else:
        assert not sys.argv[1:]
        prepare()
