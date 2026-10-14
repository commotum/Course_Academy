#!/usr/bin/env python3
"""Source-backed easy matrix echelon identification, with semantic deduplication.

CLI: .venv/bin/python generate/scratch/17592186129113.py --difficulty easy
     --count 5 --seed 0 --format json
Moderate/hard are bounded capability exceptions, not filled reserves.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import uuid
import sys
try:
    import sympy as sp
except ModuleNotFoundError:
    # The application may invoke its public CLI from the system Python.
    # Use this repository's configured dependencies without changing app code.
    import os
    import sys
    runtime = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if __name__ == '__main__' and runtime.is_file():
        os.execv(str(runtime), [str(runtime), str(Path(__file__).resolve()), *sys.argv[1:]])
    raise

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts/question_capture'))
from math_format import checked_math_content, normalize_prose

HERE = Path(__file__).with_suffix('')
S = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186129113
KP_UUID = S['record'][':knowledge-point/id']
VERSION = 'augmented-coefficient-echelon-1.0.0'
SOURCES = {q[':question/math-academy-id']: q for q in S['record'][':knowledge-point/questions']}
EXCLUDED = {'q-42026': 'Unrated radio source: missing correct answer and worked solution; retained unchanged.'}
PROFILES = tuple(t for t in SOURCES if t not in EXCLUDED)
MATRIX = re.compile(r'\\left\[\\begin\{array\}\{c+\|c\}(.*?)\\end\{array\}\\right\]', re.S)
CORRECTIONS = {p: 'Explicit coefficient-matrix wording replaces ambiguous augmented-matrix wording in variants; original source retained in replay.' for p in PROFILES if p != 'q-72575'}

def coefficient(m):
    return [row[:-1] for row in m]

def matrices(text):
    result = []
    for body in MATRIX.findall(text):
        rows = [[int(sp.Integer(x.strip())) for x in row.split('&')] for row in body.split(r'\\')]
        assert rows and len({len(row) for row in rows}) == 1
        result.append(rows)
    return result

def leading(m):
    return [next((j for j, v in enumerate(row) if v != 0), None) for row in m]

def facts(m):
    pivots = leading(m)
    zero = next((i for i, p in enumerate(pivots) if p is None and any(q is not None for q in pivots[i+1:])), None)
    previous = None
    bad = None
    for i, p in enumerate(pivots):
        if p is None:
            continue
        if previous is not None and p <= previous and bad is None:
            bad = (i, p)
        previous = p
    return {'echelon': zero is None and bad is None, 'zero_witness': zero, 'pivot_witness': bad}

def original(profile):
    return {'matrices': matrices(SOURCES[profile][':question/problem'])}

def roles(profile):
    return [facts(coefficient(m)) for m in original(profile)['matrices']]

def pivot_domain(m):
    """Retain nonzero-row order and pivot weak order; vary actual columns/zero positions."""
    p = leading(coefficient(m))
    nonzero = [x for x in p if x is not None]
    distinct = sorted(set(nonzero))
    ranks = [distinct.index(x) for x in nonzero]
    z = len(p) - len(nonzero)
    invalid_zero = facts(coefficient(m))['zero_witness'] is not None
    positions = itertools.combinations(range(len(p)), z) if invalid_zero else [tuple(range(len(nonzero), len(p)))]
    positions = list(positions)
    out = []
    for columns in itertools.combinations(range(len(m[0])-1), len(distinct)):
        for zeros in positions:
            it = iter(columns[r] for r in ranks)
            candidate = [None if i in zeros else next(it) for i in range(len(p))]
            if invalid_zero and not any(v is None and any(q is not None for q in candidate[i+1:]) for i, v in enumerate(candidate)):
                continue
            out.append(candidate)
    assert p in out
    return out

def sample(profile, rng):
    out = []
    for m in original(profile)['matrices']:
        p = rng.choice(pivot_domain(m))
        rows = []
        for pivot in p:
            if pivot is None:
                rows.append([0] * (len(m[0])-1) + [rng.randint(-9,9)])
            else:
                row = [0] * pivot + [rng.choice(tuple(range(-9, 0)) + tuple(range(1, 10)))]
                row += [rng.randint(-9, 9) for _ in range(len(m[0]) - pivot - 1)]
                rows.append(row)
        out.append(rows)
    return {'matrices': out}

def latex(m):
    return r'\left[\begin{array}{'+ 'c'*(len(m[0])-1) + '|c}' + r' \\ '.join(' & '.join(map(str, row)) for row in m) + r'\end{array}\right]'

def fingerprint(q):
    # Signs, magnitudes, trailing entries, seed, profile, UUID and matrix-label
    # permutations cannot manufacture another echelon-identification task.
    ms = matrices(q[':question/problem'])
    assert len(ms) == 3
    signatures = sorted([(len(m), len(m[0]), tuple(-1 if p is None else p for p in leading(coefficient(m)))) for m in ms])
    return json.dumps(['not' if '**not**' in q[':question/problem'] else 'in', signatures], separators=(',', ':'))

def render(profile, p, replay=False):
    source = SOURCES[profile]
    ms = p['matrices']
    originals = original(profile)['matrices']
    assert len(ms) == 3
    for old, new in zip(originals, ms):
        assert len(new) == len(old) and all(len(row) == len(old[0]) for row in new)
        assert leading(coefficient(new)) in pivot_domain(old)
        assert all(type(v) is int and -99 <= v <= 99 for row in new for v in row)
    if replay:
        assert p == original(profile)
        return source[':question/problem'], source[':question/worked-solution']
    it = iter(ms)
    prompt = MATRIX.sub(lambda _: latex(next(it)), source[':question/problem'])
    if profile != 'q-72575':
        first, rest = prompt.split('\n', 1)
        polarity = '**not** in' if '**not**' in first else 'in'
        prompt = 'Which of the following augmented matrices have coefficient matrices that are '+polarity+' row echelon form? Treat the final column of each augmented matrix as its constants column.\n'+rest
    solution = source[':question/worked-solution']
    if profile != 'q-72575':
        solution = solution.replace('Remember that an augmented matrix is in row echelon form if its coefficient matrix satisfies the following conditions:', 'A coefficient matrix, obtained by omitting the final column of its augmented matrix, is in row echelon form if it satisfies the following conditions:')
    it = iter(ms)
    solution = MATRIX.sub(lambda _: latex(next(it)), solution)
    names = ['first', 'second', 'third', 'fourth', 'fifth']
    for label, old, new in zip('ABC', originals, ms):
        oldc, newc = coefficient(old), coefficient(new)
        oldfacts, newfacts = facts(oldc), facts(newc)
        pattern = r'- The (?:coefficient matrix of|matrix) \$'+label+r'\$.*?(?=\n\n)'
        match = re.search(pattern, solution, re.S)
        assert match, (profile,label)
        sentence = match[0].replace('The matrix $', 'The coefficient matrix of $')
        if 'row contains only zeros' in sentence:
            assert oldfacts['zero_witness'] is not None and newfacts['zero_witness'] is not None
            sentence = sentence.replace(names[oldfacts['zero_witness']]+' row', names[newfacts['zero_witness']]+' row')
        elif re.search(r'\$\{[abc]\}_\{\d\d\}',sentence):
            witness = re.search(r'\$\{[abc]\}_\{(\d)(\d)\}',sentence)
            oldrow = int(witness[1])-1
            rank = sum(v is not None for v in leading(oldc)[:oldrow])
            i = [i for i,v in enumerate(leading(newc)) if v is not None][rank]
            j = leading(newc)[i]
            assert facts(newc)['pivot_witness'] is not None
            sentence = re.sub(r'\$\{[abc]\}_\{\d\d\}',lambda _: '${'+label.lower()+'}_{'+str(i+1)+str(j+1)+'}',sentence)
        elif 'leading entries of its first two rows' in sentence:
            cols = leading(newc)
            assert cols[0] is not None and cols[1] is not None and cols[1] <= cols[0]
            sentence = re.sub(r'columns \$\d\$ and \$\d,\$',lambda _: 'columns $'+str(cols[0]+1)+'$ and $'+str(cols[1]+1)+',$',sentence)
        solution = solution[:match.start()] + sentence + solution[match.end():]
    if profile != 'q-72575':
        def conclusion(match):
            subject, verb, negative = match.groups()
            return subject + (' has a coefficient matrix that is ' if verb=='is' else ' have coefficient matrices that are ') + (negative or '') + 'in row echelon form.'
        solution = re.sub(r'(Therefore, .*?) (are|is) (\*\*not\*\* )?in row echelon form\.',conclusion,solution)
    return prompt, solution

@checked_math_content
def generate(difficulty, seed, profile=None, parameters=None, replay=False):
    if difficulty != 'easy':
        raise ValueError('Unsupported difficulty '+difficulty+': no validated source-backed workload band.')
    rng = random.Random(seed)
    profile = profile or rng.choice(PROFILES)
    assert profile in PROFILES
    p = parameters if parameters is not None else sample(profile, rng)
    problem, solution = render(profile, p, replay)
    problem, solution = normalize_prose(problem), normalize_prose(solution)
    negate = '**not**' in problem
    # IDs use the full authored givens (not seeds); semantic fingerprint separately
    # prevents cosmetic variants being accepted into inventory.
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID), VERSION+'|'+problem+'|'+solution))
    fields = []
    for key, m in zip('ABC', p['matrices']):
        yes = facts(coefficient(m))['echelon'] != negate
        fid = str(uuid.uuid5(uuid.UUID(qid), 'field/'+key))
        answers = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), value)), ':answer/type': ':answer.type/text', ':answer/value': value} for value in ('false', 'true')]
        fields.append({':answer-field/id': fid, ':answer-field/key': key, ':answer-field/type': ':answer-field.type/checkbox', ':answer-field/choices': answers,
                       ':answer-field/correct': [':answer/id', answers[int(yes)][':answer/id']]})
    q = {':question/id': qid, ':question/problem': problem, ':question/worked-solution': solution, ':question/difficulty': ':question.difficulty/easy', ':question/answer-fields': fields}
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': S['record'][':knowledge-point/title']}, 'question': q,
            'generation': {'version': VERSION, 'seed': seed, 'template': ('explicit-coefficient-not' if profile=='q-72575' else 'select-not-coefficient-echelon' if negate else 'select-coefficient-echelon'), 'profile': profile,
                           'source_db_id': SOURCES[profile][':db/id'], 'parameters': p, 'replay': replay, 'source_correction': CORRECTIONS.get(profile),
                           'mathematical_fingerprint': fingerprint(q), 'assets': [], 'dependencies': {'sympy': sp.__version__}}}

def batch(difficulty, count, seed):
    if difficulty != 'easy':
        raise ValueError('Unsupported difficulty '+difficulty)
    assert 0 <= count <= 1000
    out, seen = [], set()
    for offset in range(max(200, 50*count)):
        if len(out) == count:
            break
        r = generate(difficulty, seed+offset, PROFILES[offset % len(PROFILES)])
        fp = r['generation']['mathematical_fingerprint']
        if fp not in seen:
            seen.add(fp)
            out.append(r)
    if len(out) != count:
        raise ValueError('Bounded structural sampler produced '+str(len(out))+' of '+str(count)+' distinct tasks; shortage remains explicit.')
    return out

def markdown(r):
    return r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']

def main():
    a = argparse.ArgumentParser()
    a.add_argument('--difficulty', required=True)
    a.add_argument('--count', type=int, default=5)
    a.add_argument('--seed', type=int, default=0)
    a.add_argument('--format', choices=('json', 'markdown'), default='json')
    args = a.parse_args()
    records = batch(args.difficulty, args.count, args.seed)
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(map(markdown, records)))

if __name__ == '__main__':
    main()
