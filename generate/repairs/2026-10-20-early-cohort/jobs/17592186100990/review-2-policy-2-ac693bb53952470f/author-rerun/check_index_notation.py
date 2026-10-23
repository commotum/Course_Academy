#!/usr/bin/env python3
"""Regress comma-index equivalence against current output and the real grader."""
import json
import os
from pathlib import Path
import subprocess

import check_repair as prior

W = Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100990/workspace')
E = Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100990/review-2-policy-2-ac693bb53952470f/author-rerun/comma')
E.mkdir(exist_ok=True)
COMMANDS = []


def save(name, value):
    path = E / name
    path.write_text(json.dumps(value, indent=2) + '\n')
    return path


def run(command):
    command = list(map(str, command))
    result = subprocess.run(command, capture_output=True, text=True,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
                                     COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(E / 'assets')))
    COMMANDS.append(dict(command=command, returncode=result.returncode,
                         stdout=result.stdout if '--format' not in command else '(records saved)',
                         stderr=result.stderr))
    save('commands.json', COMMANDS)
    assert result.returncode == 0, result.stderr or result.stdout
    return result.stdout


def grade(records, name):
    cases = []
    for r in records:
        fields = r['question'][':question/answer-fields']
        if len(fields) != 1 or not fields[0][':answer-field/type'].endswith('/blank'):
            continue
        m, n, i, j, b = prior.visible(r)  # Read the visible box; verify key/solution.
        alternatives = [
            (f'{b}_{{{i}{j}}}', 'accepted'),
            (f'{b}_{{{i},{j}}}', 'accepted'),
            (f'{{{b}}}_{{ {i} , {j} }}', 'accepted'),
            (f'{{{{{b}}}}}_{{{{{i}}},{{{j}}}}}', 'accepted'),
            (f'{b}_{{{i % m + 1},{j}}}', 'rejected'),
            (f'{b}_{{{i},{j % n + 1}}}', 'rejected'),
            (f'{"z" if b != "z" else "a"}_{{{i},{j}}}', 'rejected'),
            (str(prior.matrix(r['question'])[0][i - 1][j - 1]), 'rejected'),
            (f'{b}_{{{i},1{j}}}', 'rejected'),
            (f'{b}_{{{i},{j},1}}', 'rejected'),
            (f'{b}_{{{i},,{j}}}', 'rejected'),
        ]
        if i != j:
            alternatives.append((f'{b}_{{{j},{i}}}', 'rejected'))
        cases.append(dict(label=r['question'][':question/id'], record=r, checks=[
            dict(submitted=s, expected=e, purpose='ordered coordinates from visible highlight')
            for s, e in alternatives
        ]))
    assert cases, 'No symbolic fields tested'
    path = save(name + '-input.json', cases)
    run([prior.ENGINE, path, E / (name + '-report.json')])
    return len(cases)


def main():
    # The regression defaults to current CLI output, never the historical batch.
    args = [prior.PYTHON, '-B', W / '17592186100990.py', '--difficulty', 'easy',
            '--count', '5', '--seed', '3782988951', '--format', 'json']
    batch = json.loads(run(args))
    assert batch == json.loads(run(args)), 'CLI replay changed'
    path = save('prospective-batch.json', batch)
    run([prior.PYTHON, prior.ROOT / 'generate/pipeline/check_delivery.py',
         '--input', path, '--source', W.parent / 'source/source.json',
         '--inventory', W.parent / 'source/inventory.json', '--difficulty', 'easy',
         '--output', E / 'delivery', '--asset-root', E / 'assets',
         '--math-root', '/media/jake/SSD/EDB/math'])
    accepted_path = E / 'delivery/accepted.json'
    accepted = json.loads(accepted_path.read_text())
    assert len(accepted) == len(batch) == 5
    # Preserve the independent reviewer's exact candidate-record check.
    for label, candidate in [('raw', path), ('delivered', accepted_path)]:
        run([prior.PYTHON, '-B', E / 'regression_index_notation.py', candidate])
        for suffix in ('input', 'report', 'execution'):
            (E / f'retained-{label}-{suffix}.json').write_bytes(
                (E / f'comma-strict-{suffix}.json').read_bytes())
    counts = {'raw': grade(batch, 'raw'), 'delivered': grade(accepted, 'delivered')}
    # Exercise every eligible easy coordinate with the matrix and label fixed.
    controls = []
    for i in range(1, 5):
        for j in range(1, 5):
            p = dict(matrix=[[r * 4 + c - 8 for c in range(4)] for r in range(4)],
                     i=i, j=j, letter='A')
            controls.append(prior.g.generate('easy', 73, profile='completed:q-279556', parameters=p))
    controls += [prior.cli(73, 1, 'completed:' + sid)[0] for sid in ('q-279553', 'q-279556')]
    save('coordinate-controls.json', controls)
    counts['controls'] = grade(controls, 'controls')
    save('summary.json', dict(status='passed', tested_symbolic_records=counts,
                             control_targets=16, raw_records=len(batch),
                             delivered_records=len(accepted), deterministic_replay=True))
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
