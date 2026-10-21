"""Independent checks read learner-visible matrices, not generation parameters."""
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186129114/workspace')
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = ROOT.parent
E = Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186129114/review-1-policy-2-2ccad43c714003de/author-check')
E.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))
import generator as g


def load(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


def run(args):
    p = subprocess.run([str(x) for x in args], cwd=ROOT, text=True,
                       capture_output=True)
    with (E / 'commands.log').open('a') as out:
        out.write(json.dumps([str(x) for x in args]) + '\n')
        out.write(p.stdout + p.stderr + f'\nexit={p.returncode}\n')
    assert p.returncode == 0, p.stdout[-2000:] + p.stderr[-2000:]
    return p


def matrices(text):
    return [[[int(x.strip()) for x in row.split('&')]
             for row in body.split(r'\\')]
            for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S)]


def valid(m):
    # Inspect nonzero cells independently and compare EVERY pair of rows.
    pivots = [min([j for j, v in enumerate(row) if v] or [len(row)]) for row in m]
    width = len(m[0])
    return all(a < b or a == b == width for i, a in enumerate(pivots) for b in pivots[i+1:])


def field_value(f):
    c = f[':answer-field/correct']
    aid = c[':answer/id'] if isinstance(c, dict) else c[1]
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == aid)


def examine(r, solution=True):
    q = r.get('question', r)
    neg = '**not**' in q[':question/problem']
    rows = {}
    for f in q[':question/answer-fields']:
        label = re.search(r'\$([ABC])\s*=', f[':answer-field/key'])[1]
        m = matrices(f[':answer-field/key'])[0]
        yes = valid(m) != neg
        assert field_value(f) == str(yes).lower(), (q[':question/id'], label)
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices']) == ['false', 'true']
        if solution:
            assert matrices(q[':question/worked-solution'])['ABC'.index(label)] == m
            # Source prose sometimes has doubled spaces.
            normalized = re.sub(r'\s+', ' ', q[':question/worked-solution'])
            status = f'- The matrix ${label}$ is ' + ('in' if valid(m) else 'not in') + ' row echelon form'
            assert status in normalized, (label, status)
        rows[label] = {'selected': yes, 'shape': [len(m), len(m[0])]}
    assert set(rows) == set('ABC') and any(x['selected'] for x in rows.values())
    return {'subset': ''.join(x for x in 'ABC' if rows[x]['selected']),
            'polarity': neg, 'shapes': [rows[x]['shape'] for x in 'ABC']}


def coverage(records):
    result = {}
    groups = {'all': records}
    for r in records:
        info = examine(r)
        groups.setdefault('polarity/' + str(info['polarity']), []).append(r)
        groups.setdefault('shapes/' + json.dumps([info['polarity'], info['shapes']]), []).append(r)
    for name, group in groups.items():
        subsets = [examine(r)['subset'] for r in group]
        roles = {x: {'selected': sum(x in s for s in subsets),
                     'unselected': sum(x not in s for s in subsets)} for x in 'ABC'}
        assert len(group) < 3 or all(v['selected'] and v['unselected'] for v in roles.values()), (name, roles)
        result[name] = {'count': len(group), 'subsets': subsets, 'roles': roles,
                        'coverage_claim': len(group) >= 3}
    return result


def delivery(records, name, inventory=None):
    path = E / (name + '.json')
    save(path, records)
    target = E / name
    run([sys.executable, REPO / 'generate/pipeline/check_delivery.py',
         '--input', path, '--source', JOB / 'source/source.json',
         '--inventory', inventory or JOB / 'source/inventory.json',
         '--difficulty', 'easy', '--output', target,
         '--asset-root', ROOT, '--math-root', '/media/jake/SSD/EDB/math'])
    return load(target / 'accepted.json')


def grader(records, name):
    cases = []
    for i, r in enumerate(records):
        info = examine(r)
        checks = []
        for j, f in enumerate(r['question'][':question/answer-fields']):
            label = re.search(r'\$([ABC])\s*=', f[':answer-field/key'])[1]
            for a in f[':answer-field/choices']:
                correct = (a[':answer/value'] == 'true') == (label in info['subset'])
                checks.append({'field_index': j, 'submitted_answer_id': a[':answer/id'],
                               'expected': 'accepted' if correct else 'rejected',
                               'purpose': 'Independent visible matrix witness; both checkbox actions'})
        cases.append({'label': f'{name}-{i}', 'record': r, 'checks': checks})
    path = E / (name + '-grader-input.json')
    save(path, cases)
    run([REPO / 'generate/runs/current/check-engine', path, E / (name + '-grader-results.json')])
