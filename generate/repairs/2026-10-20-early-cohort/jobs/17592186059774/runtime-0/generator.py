"""Seeded single-entry row-operation decisions; source banks stay complete.

Adapted from the supplied 17592186059774.py: retains its operation parser,
exact matrix application, coherent row relabeling, and source replay. The new
sampler chooses the winning operation before sampling its decisive evidence.
No file writes, external imports, network access or database access occur.
"""
import argparse
import hashlib
import itertools
import json
import random
import re
import uuid
from pathlib import Path

import sympy as sp
from math_format import (checked_math_content, matrix_tex, normalize_prose,
                         normalize_tex)

KP_ID = 17592186059774
KP_UUID = '0464b51e-8568-521e-96a5-a65c04569c2a'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'row-operation-generator-v2'))
VERSION = '2.0.0'
SUPPORTED_LEVELS = ('hard',)
SOURCE = json.loads(Path(__file__).with_name('source_data.json').read_text())
ALL_CASES = {q[':question/math-academy-id']: q
             for q in SOURCE[':knowledge-point/questions']}
CASES = {sid: q for sid, q in ALL_CASES.items()
         if q.get(':question/difficulty') and q.get(':question/worked-solution')
         and q[':question/answer-fields'][0].get(':answer-field/correct')}
MAT = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)


def matrices(text):
    return [sp.Matrix([[sp.Rational(re.sub(
        r'\\frac\{(-?\d+)\}\{(\d+)\}', r'\1/\2',
        cell.replace(r'\,', '').strip())) for cell in row.split('&')]
        for row in body.split(r'\\')]) for body in MAT.findall(text)]


def latex(matrix):
    return matrix_tex([[sp.latex(matrix[i, j]) for j in range(matrix.cols)]
                       for i in range(matrix.rows)], augmented=False)


def operation(text):
    """Parse the actual source operation, including its rational coefficient."""
    text = text.replace(r'\\frac', r'\frac')  # broken incomplete-source capture
    text = re.sub(r'\{R\}_\{([123])\}|R_\{([123])\}',
                  lambda m: 'r' + (m[1] or m[2]), text)
    text = re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', text)
    text = text.replace(r'\cdot', '*').replace(' ', '')
    if '↔' in text or r'\leftrightarrow' in text:
        a, b = re.split('↔|' + re.escape(r'\leftrightarrow'), text)
        return ('swap', int(a[1:]) - 1, int(b[1:]) - 1)
    lhs, rhs = text.split(':=')
    i = int(lhs[1:]) - 1
    rhs = re.sub(r'(\d|\))(?=r)', r'\1*', rhs)
    rs = sp.symbols('r1 r2 r3')
    expr = sp.sympify(rhs, locals=dict(zip(('r1', 'r2', 'r3'), rs)))
    cs = tuple(sp.expand(expr).coeff(r) for r in rs)
    if sp.expand(expr) != sum(c * r for c, r in zip(cs, rs)):
        raise ValueError('Nonlinear row expression')
    return ('replace', i, cs)


def apply(matrix, op):
    result = matrix.copy()
    if op[0] == 'swap':
        result.row_swap(op[1], op[2])
    else:
        row = sp.zeros(1, matrix.cols)
        for j, coefficient in enumerate(op[2]):
            row += coefficient * matrix[j, :]
        result[op[1], :] = row
    return result


def target(text):
    m = re.search(r'(?:a\}|a)_\{([123])([123])\}', text)
    if not m:
        raise ValueError('Missing target entry')
    return int(m[1]) - 1, int(m[2]) - 1


def permute_text(text, rows):
    inverse = {old: new for new, old in enumerate(rows)}
    return re.sub(r'(\{R\}_\{|R_\{)([123])(\})',
                  lambda m: m[1] + str(inverse[int(m[2]) - 1] + 1) + m[3], text)


def source_values(sid):
    return [a[':answer/value'] for a in
            ALL_CASES[sid][':question/answer-fields'][0][':answer-field/choices']]


def eligible_winners(sid):
    t, _ = target(ALL_CASES[sid][':question/problem'])
    eligible = []
    for index, value in enumerate(source_values(sid)):
        op = operation(value)
        if op[0] == 'swap':
            good = t in op[1:]
        else:
            cs = op[2]
            good = (op[1] == t and cs[t] == 1 and
                    sum(bool(cs[s]) for s in range(3) if s != t) == 1)
        if good:
            eligible.append(index)
    return eligible


def fingerprint(question):
    """Assessed column and whole bank, modulo renaming and common scale."""
    matrix = matrices(question[':question/problem'])[0]
    t, c = target(question[':question/problem'])
    vals = [a[':answer/value'] for a in question[':question/answer-fields'][0]
            [':answer-field/choices']]
    candidates = []
    for tail in itertools.permutations([i for i in range(3) if i != t]):
        rows = [t, *tail]
        column = [str(matrix[i, c] / matrix[t, c]) for i in rows]
        bank = []
        for v in vals:
            op = operation(permute_text(v, rows))
            if op[0] == 'swap':
                bank.append(('swap', *sorted(op[1:])))
            else:
                bank.append(('replace', op[1], tuple(map(str, op[2]))))
        candidates.append(json.dumps([column, sorted(bank)], sort_keys=True))
    return hashlib.sha256(min(candidates).encode()).hexdigest()


def source_key(sid):
    field = ALL_CASES[sid][':question/answer-fields'][0]
    if field.get(':answer-field/correct'):
        return field[':answer-field/correct'][':answer/value']
    # Missing evidence is explicitly reconstructed, never called an observed key.
    m = matrices(ALL_CASES[sid][':question/problem'])[0]
    t, c = target(ALL_CASES[sid][':question/problem'])
    winners = [v for v in source_values(sid) if apply(m, operation(v))[t, c] == 0]
    if len(winners) != 1:
        raise ValueError('Cannot reconstruct source key')
    return winners[0]


def worked_solution(label, a, b, t, c, correct):
    op = operation(correct)
    entry = f'a_{{{t+1}{c+1}}}'
    if op[0] == 'swap':
        s = next(i for i in op[1:] if i != t)
        evidence = (f'The entry in row ${s+1}$, column ${c+1}$ is $0$. '
                    f'Switching rows ${t+1}$ and ${s+1}$ therefore makes ${entry}=0$.')
    else:
        s = next(i for i in range(3) if i != t and op[2][i])
        k = op[2][s]
        evidence = ('At the requested entry, this gives\n\n$$\n' + entry + '=' +
                    sp.latex(a[t, c]) + '+(' + sp.latex(k) + r')\cdot (' +
                    sp.latex(a[s, c]) + ')=0.\n$$')
    return normalize_prose(
        'Of the given options, we consider the row operation\n\n$$\n' + correct +
        '.\n$$\n\n' + evidence +
        '\n\nApplying the above row operation, we obtain the following:\n\n$$\n' +
        r'\begin{aligned}' + label + ' &=' + latex(a) + r'\qquad ' + correct +
        r' \\ &\sim ' + latex(b) + r'\end{aligned}' +
        '\n$$\n\nTherefore, the required row operation is\n\n$$\n' + correct + '.\n$$')


@checked_math_content
def generate(difficulty='hard', seed=0, template=None, parameters=None):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: ' + difficulty)
    rng = random.Random(seed)
    parameters = dict(parameters or {})
    sid = parameters.get('source', template or rng.choice(list(CASES)))
    if sid not in ALL_CASES:
        raise ValueError('Unknown source profile')
    source = ALL_CASES[sid]
    original = matrices(source[':question/problem'])[0]
    t0, c0 = target(source[':question/problem'])
    values = source_values(sid)
    replay = parameters.get('replay', False)
    attempts = 0
    if replay:
        a = original.copy()
        winner = values.index(source_key(sid))
        rows, cols = list(range(3)), list(range(3))
        order = list(range(5))
    else:
        if sid not in CASES:
            raise ValueError('Incomplete source is replay-only')
        winner = parameters.get('winner', rng.choice(eligible_winners(sid)))
        if winner not in eligible_winners(sid):
            raise ValueError('Ineligible winning operation')
        win_op = operation(values[winner])
        a = original.copy()
        for attempts in range(1, 513):
            column = [rng.randint(-12, 12) for _ in range(3)]
            if win_op[0] == 'swap':
                s = next(i for i in win_op[1:] if i != t0)
                column[t0] = rng.choice([n for n in range(-12, 13) if n])
                column[s] = 0
            else:
                s = next(i for i in range(3) if i != t0 and win_op[2][i])
                k = win_op[2][s]
                donors = [n for n in range(-12, 13) if n and
                          (-k*n).is_Integer and abs(k*n) <= 12]
                column[s] = rng.choice(donors)
                column[t0] = -k * column[s]
            a[:, c0] = sp.Matrix(column)
            good = [i for i, v in enumerate(values)
                    if apply(a, operation(v))[t0, c0] == 0]
            if good == [winner]:
                break
        else:
            raise ValueError('No unambiguous column for chosen winner')
        for i in range(3):
            for j in range(3):
                if j != c0:
                    a[i, j] = rng.randint(-9, 9)
        # Explicit evidence is for reproducible source/boundary/counterfactual tests.
        if 'matrix' in parameters:
            a = sp.Matrix(parameters['matrix'])
        rows = parameters.get('rows', rng.sample(range(3), 3))
        cols = parameters.get('cols', rng.sample(range(3), 3))
        order = parameters.get('order', rng.sample(range(5), 5))
    if sorted(rows) != list(range(3)) or sorted(cols) != list(range(3)):
        raise ValueError('Invalid matrix permutation')
    if sorted(order) != list(range(5)):
        raise ValueError('Invalid choice order')
    good = [i for i, v in enumerate(values)
            if apply(a, operation(v))[t0, c0] == 0]
    if a.shape != (3, 3) or a[t0, c0] == 0 or good != [winner]:
        raise ValueError('Ambiguous or inconsistent instance')
    b = apply(a, operation(values[winner]))
    base_matrix = [[str(x) for x in a.row(i)] for i in range(3)]
    a, b = a[rows, cols], b[rows, cols]
    t, c = rows.index(t0), cols.index(c0)
    values = [normalize_tex(permute_text(v.replace(r'\\frac', r'\frac'), rows))
              for v in values]
    correct = values[winner]
    label = re.search(r'([A-Z])\s*=', source[':question/problem'])[1]
    if replay:
        problem = normalize_prose(source[':question/problem'])
        if sid == 'q-130301':
            counter = iter([a, b])
            solution = normalize_prose(MAT.sub(lambda _: latex(next(counter)),
                                              source[':question/worked-solution']))
        elif source.get(':question/worked-solution'):
            solution = normalize_prose(source[':question/worked-solution'])
        else:
            solution = worked_solution(label, a, b, t, c, correct)
    else:
        problem = normalize_prose('Given that\n\n$$\n' + label + '=' + latex(a) +
                  '\n$$\n\nwhich of the following elementary row operations makes '
                  + f'$a_{{{t+1}{c+1}}}=0$?')
        solution = worked_solution(label, a, b, t, c, correct)
    identity = json.dumps([problem, sorted(values), correct], ensure_ascii=False)
    qid = str(uuid.uuid5(uuid.UUID(GENERATOR_UUID), identity))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    answers = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), value)),
                ':answer/type': ':answer.type/math', ':answer/value': value}
               for value in values]
    field = {':answer-field/id': fid, ':answer-field/key': 'selection',
             ':answer-field/type': ':answer-field.type/radio',
             ':answer-field/choices': [answers[i] for i in order],
             ':answer-field/correct': [':answer/id', answers[winner][':answer/id']]}
    question = {':question/id': qid, ':question/problem': problem,
                ':question/worked-solution': solution,
                ':question/difficulty': ':question.difficulty/hard',
                ':question/answer-fields': [field]}
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID}, 'question': question,
            'generation': {'generator_id': GENERATOR_UUID, 'generator_version': VERSION,
                'seed': seed, 'template': 'single-entry-zero', 'bank_profile': sid,
                'source_question_id': source[':question/id'],
                'source_basis': SOURCE['basis'], 'source_difficulty':
                    source.get(':question/difficulty', {}).get(':db/ident'),
                'source_replay': replay, 'inferred_source_completion': sid not in CASES,
                'parameters': {'source': sid, 'winner': winner, 'matrix': base_matrix,
                               'rows': rows, 'cols': cols, 'order': order, 'replay': replay},
                'rejection_attempts': attempts, 'assets': [],
                'dependencies': {'sympy': sp.__version__},
                'mathematical_fingerprint': fingerprint(question)}}


def replay(sid):
    return generate(template=sid, parameters={'replay': True, 'source': sid})


def batch(difficulty, count, seed):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: ' + difficulty)
    if count < 0:
        raise ValueError('Count must be nonnegative')
    rng = random.Random(seed)
    seen, records = set(), []
    for _ in range(max(100, count * 100)):
        if len(records) == count:
            return records
        record = generate(difficulty, rng.getrandbits(64))
        semantic = record['generation']['mathematical_fingerprint']
        if semantic in seen:
            continue
        seen.add(semantic)
        records.append(record)
    raise ValueError('Insufficient distinct semantic instances')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', default='hard')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=59774)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    print(json.dumps(batch(args.difficulty, args.count, args.seed), indent=2))
