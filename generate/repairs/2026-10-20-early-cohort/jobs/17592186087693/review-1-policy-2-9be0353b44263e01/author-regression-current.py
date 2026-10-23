"""Replay the supplied capture, never use the package's registry as the oracle."""
import argparse
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True
ROOT = Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186087693/workspace')
sys.path.insert(0, str(ROOT))
import generator


def norm(value):
    return re.sub(r'\s|[${}.]', '', value)


def matrix(question):
    body = re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', question[':question/problem'], re.S)[1]
    return [[cell.strip() for cell in row.split('&')] for row in body.split('\\\\')]


def enum(value):
    return value.get(':db/ident') if isinstance(value, dict) else value


def correct(field):
    value = field[':answer-field/correct']
    cid = value[':answer/id'] if isinstance(value, dict) else value[1]
    return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id'] == cid)


def check_math(record):
    q = record['question']
    cells = matrix(q)
    r, c = len(cells), len(cells[0])
    assert all(len(row) == c for row in cells)
    fs = q[':question/answer-fields']
    if enum(fs[0][':answer-field/type']).endswith('/radio'):
        assert len(fs) == 1
        bank = [norm(a[':answer/value']) for a in fs[0][':answer-field/choices']]
        assert len(set(bank)) == len(bank) == 5
        assert norm(correct(fs[0])) == f'{r}\\times{c}'
    else:
        assert {f[':answer-field/key']: correct(f) for f in fs} == {'field-1': str(r), 'field-2': str(c)}
    sol = norm(q[':question/worked-solution'])
    assert f'has{r}rowsand{c}columns' in sol
    assert f'{r}\\times{c}' in sol
    return r, c


def replay(source):
    qs = json.loads(source.read_text())['material']['kp'][':knowledge-point/questions']
    records = []
    for q in qs:
        sid = q[':question/math-academy-id']
        rec = generator.generate(seed=0, profile='observed-' + sid)
        rq = rec['question']
        assert matrix(rq) == matrix(q), sid
        check_math(rec)
        fs = {f[':answer-field/key']: f for f in q[':question/answer-fields']}
        rfs = {f[':answer-field/key']: f for f in rq[':question/answer-fields']}
        assert fs.keys() == rfs.keys(), sid
        for key, f in fs.items():
            rf = rfs[key]
            assert enum(f[':answer-field/type']) == enum(rf[':answer-field/type']), sid
            assert sorted(norm(a[':answer/value']) for a in f[':answer-field/choices']) == sorted(norm(a[':answer/value']) for a in rf[':answer-field/choices']), sid
            assert norm(correct(f)) == norm(correct(rf)), sid
        assert norm(q[':question/worked-solution']) == norm(rq[':question/worked-solution']), sid
        assert enum(q.get(':question/difficulty')) == enum(rq.get(':question/difficulty')), sid
        if 'Chelsea' in q[':question/problem']:
            assert 'Chelsea represents information using the following matrix:' in rq[':question/problem']
            assert 'table' not in rq[':question/problem']
        elif q[':question/problem'].startswith('Let'):
            assert rq[':question/problem'].startswith('Let')
        else:
            assert rq[':question/problem'].startswith('What are the dimensions of the matrix')
        records.append(rec)
    return records


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source', type=Path, default=ROOT.parent/'source/source.json')
    p.add_argument('--output', type=Path, default=ROOT/'evidence/source-replays.json')
    a = p.parse_args()
    records = replay(a.source)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(records, indent=2)+'\n')
    print(json.dumps({'source_profiles_passed': len(records), 'source': str(a.source)}))
