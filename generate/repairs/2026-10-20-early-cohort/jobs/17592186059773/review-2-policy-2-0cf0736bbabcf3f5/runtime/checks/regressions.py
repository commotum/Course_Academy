"""Executable CLI/runtime and bank-shortcut regressions; no services or mutation."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_generator():
    spec = importlib.util.spec_from_file_location('generator', ROOT / '17592186059773.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    g = load_generator()
    spec = importlib.util.spec_from_file_location('independent', ROOT / '17592186059773/validate.py')
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    counts = []
    for count, seed in ((5, 1260123367), (5, 0), (0, 0), (1, 17), (7, 23)):
        command = [sys.executable, '-E', '-s', '-B', str(ROOT / '17592186059773.py'),
                   '--difficulty', 'moderate', '--count', str(count),
                   '--seed', str(seed), '--format', 'json']
        completed = subprocess.run(command, capture_output=True, text=True, check=True, cwd='/tmp')
        records = json.loads(completed.stdout)
        assert isinstance(records, list), 'Runner requires a top-level JSON array'
        assert len(records) == count, (count, len(records))
        assert len({r['question'][':question/id'] for r in records}) == count
        for record in records:
            validator.independent(record)
        counts.append({'count': count, 'seed': seed, 'records_checked': len(records),
                       'command': command, 'passed': True})
    tested = {}
    for sid in g.CASES:
        p = g.domain(sid)[0]
        answers = set()
        targets = set()
        for key in g.eligible_keys(sid):
            record = g.generate(parameters=p + [key])
            validator.independent(record)
            q = record['question']; f = q[':question/answer-fields'][0]
            # Compare public records, not selected-key metadata.
            answers.add(next(a[':answer/value'] for a in f[':answer-field/choices']
                             if a[':answer/id'] == f[':answer-field/correct'][1]))
            targets.add(tuple(g.matrices(q[':question/problem'])[1]))
        assert len(answers) > 1 and len(targets) == len(answers), sid
        tested[sid] = len(answers)
    print(json.dumps({'cli': 'pass', 'top_level_array_counts': counts,
                      'bank_counterfactuals': tested}))

if __name__ == '__main__':
    main()
