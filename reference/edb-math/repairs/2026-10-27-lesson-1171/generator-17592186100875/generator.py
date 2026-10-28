#!/usr/bin/env python3
"""Seeded, relocatable identity-matrix practice. No writes or database access."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
from math_format import (matrix_tex, matrix_operands, matrix_answer, normalize_prose,
                         normalize_tex, normalize_matrix_answer_tables, validate_generated_record)

KP = 17592186100875
NAMESPACE = uuid.UUID('1f2f5234-df9c-5269-8702-30b4dde9a2ca')
VERSION = 'identity-2.1-layout'
BANDS = ('easy', 'moderate', 'hard')
HERE = Path(__file__).resolve().parent

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

def uid(value):
    return str(uuid.uuid5(NAMESPACE, digest(value)))

def mat(m):
    return matrix_tex(m, augmented=False)

def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

def transpose(m):
    return [list(row) for row in zip(*m)]

def transforms(m):
    """Complete spatial-error profile pool; no values are introduced or negated."""
    t = transpose(m)
    return [('reverse rows', m[::-1]), ('reverse columns', [r[::-1] for r in m]),
            ('reverse rows and columns', [r[::-1] for r in m[::-1]]),
            ('transpose', t), ('transpose then reverse rows', t[::-1]),
            ('transpose then reverse columns', [r[::-1] for r in t]),
            ('transpose then reverse both', [r[::-1] for r in t[::-1]])]

def product(label, e, side):
    return e + label if side == 'left' else label + e

def dot(m, side, i, j):
    n = len(m)
    if side == 'left':
        return '+'.join(str(int(i == k)) + r'\cdot(' + str(m[k][j]) + ')' for k in range(n))
    return '+'.join('(' + str(m[i][k]) + r')\cdot' + str(int(k == j)) for k in range(n))

def expansion(m, side):
    return [[dot(m, side, i, j) for j in range(len(m))] for i in range(len(m))]

def finish(level, prompt, solution, specs, generation):
    prompt, solution = normalize_prose(normalize_matrix_answer_tables(prompt)), normalize_prose(solution)
    normalized = []
    for key, kind, answers, right in specs:
        answers = [(normalize_tex(v) if typ == 'math' else normalize_prose(v), typ) for v, typ in answers]
        normalized.append((key, kind, answers, right))
    qid = uid([VERSION, level, prompt, solution, normalized])
    fields = []
    for key, kind, answers, right in normalized:
        fid = uid([qid, key])
        choices = [{':answer/id': uid([fid, v, typ]), ':answer/type': ':answer.type/' + typ,
                    ':answer/value': v} for v, typ in answers]
        fields.append({':answer-field/id': fid, ':answer-field/key': key,
                       ':answer-field/type': ':answer-field.type/' + kind,
                       ':answer-field/choices': choices,
                       ':answer-field/correct': [':answer/id', choices[right][':answer/id']]})
    result = {'knowledge_point': {'db_id': KP, 'title': 'Multiplying a Matrix by the Identity Matrix'},
              'question': {':question/id': qid, ':question/difficulty': ':question.difficulty/' + level,
                           ':question/problem': prompt, ':question/worked-solution': solution,
                           ':question/answer-fields': fields},
              'generation': {'version': VERSION, **generation}}
    return validate_generated_record(result)

def make(level, rng, n, side, m=None, target=None, label=None, response=None):
    assert level in BANDS and n in (2, 3) and side in ('left', 'right')
    label = label or rng.choice(['A', 'B', 'D', 'G', 'M', 'Q'])
    e = ('I_' + str(n)) if level == 'easy' else rng.choice(['C', 'E', 'H'])
    p = product(label, e, side)
    if m is None:
        m = ([[f'a_{{{i+1}{j+1}}}' for j in range(n)] for i in range(n)] if level == 'hard'
             else [[rng.randint(-6, 6) for _ in range(n)] for _ in range(n)])
    assert len(m) == n and all(len(row) == n for row in m)
    base = mat(m)
    operands = [label + '=' + base] if level == 'easy' else [label + '=' + base, e + '=' + mat(identity(n))]
    given = matrix_operands(operands, stacked=True)
    header = (f'Calculate ${p}$, given that ${e}$ is the ${n} \\times {n}$ identity matrix.'
              if level == 'easy' else f'Calculate ${p}$ and enter all its entries.')
    prompt = header + '\n\n' + given
    recognition = (f'${e}$ is the corresponding identity matrix.' if level == 'easy' else
                   f'${e}$ has ones on its diagonal and zeros elsewhere, so ${e}=I_{n}$.')
    solution = (recognition + f' Both matrices are ${n} \\times {n}$, so the product is defined. '
                'Multiplication by the corresponding identity leaves every entry unchanged.\n\n$$\n' +
                p + '=' + label + '=' + base + '.\n$$')
    specs = []
    profile = None
    if level == 'hard':
        i, j = target if target is not None else (rng.randrange(n), rng.randrange(n))
        prompt = (f'Let the entries of ${label}$ be arbitrary real numbers, and let\n\n' + given +
                  f'\n\nA student claims that the zero entries of ${e}$ erase the off-diagonal entries of ${label}$ '
                  f'in the product ${p}$. Which answer gives both the correct product and the correct '
                  f'**row-column calculation** for its entry in **row {i+1}, column {j+1}**?')
        others = [(r, c) for r in range(n) for c in range(n) if (r, c) != (i, j)]
        rng.shuffle(others)
        other, third = others[:2]
        # Symmetric paired entry bank: target and comparison have identical
        # answer-frequency roles. Matching the final subscript leaves two
        # choices, and checking equation truth alone leaves three choices.
        roles = [((i, j), (i, j)), (other, (i, j)),
                 (other, other), ((i, j), other), (third, third)]
        bank = []
        for (r, c), (u, v) in roles:
            bank.append((f'${p}={label}$; the requested entry is $' + dot(m, side, r, c) + '=' + str(m[u][v]) + '$.',
                         'text', ((r, c), (u, v)), 'row-column'))
        rng.shuffle(bank)
        correct = next(k for k, (_, _, role, _) in enumerate(bank) if role == ((i, j), (i, j)))
        specs = [('selection', 'radio', [(v, typ) for v, typ, _, _ in bank], correct)]
        rows = [f'({p})_{{{r+1}{c+1}}}' + '&=' + dot(m, side, r, c) + '=' + str(m[r][c])
                for r in range(n) for c in range(n)]
        solution = (recognition + f' Both matrices are ${n} \\times {n}$. Row-column multiplication gives\n\n$$\n' +
                    r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}' + '\n$$\n\nTherefore,\n\n$$\n' +
                    p + '=' + base + '=' + label + '.\n$$\n\n' +
                    f'For row ${i+1}$ and column ${j+1}$, the calculation is $' + dot(m, side, i, j) + '=' +
                    str(m[i][j]) + '$. The zero factors remove the other summands, not the off-diagonal entries of the product. '
                    'A true calculation of another entry does not justify the requested entry. Distinct entries are arbitrary independent real numbers, so the crossed equations need not hold.')
        profile = 'requested-entry-proof'
    elif level == 'easy' and (response or rng.choice(['radio', 'blank'])) == 'radio':
        unique = {base}
        alternatives = []
        for name, value in transforms(m):
            t = mat(value)
            if t not in unique:
                unique.add(t)
                alternatives.append((name, t))
        if len(alternatives) < 4:
            raise ValueError('Not enough distinct spatial errors for radio; use blanks or resample')
        rng.shuffle(alternatives)
        bank = [('identity', base)] + alternatives[:4]
        rng.shuffle(bank)
        correct = next(k for k, (name, _) in enumerate(bank) if name == 'identity')
        specs = [('selection', 'radio', [(v, 'math') for _, v in bank], correct)]
        profile = [name for name, _ in bank]
    else:
        grid = [[f'{{{{entry-{i+1}-{j+1}}}}}' for j in range(n)] for i in range(n)]
        prompt += '\n\n' + matrix_answer(p, grid)
        specs = [(f'entry-{i+1}-{j+1}', 'blank', [(str(m[i][j]), 'math')], 0)
                 for i in range(n) for j in range(n)]
        if level == 'moderate':
            solution += ('\n\nFor example, its first entry is $' + dot(m, side, 0, 0) + '=' + str(m[0][0]) + '$.')
    return finish(level, prompt, solution, specs,
                  {'family': profile or 'entry-construction', 'order': n, 'side': side,
                   'parameters': m, 'target': list(target) if target is not None else None,
                   'source_support': ['5383efb1-6e51-562a-bf79-9ab8cba87ed7',
                                      '4c2408f2-4c4d-5bc6-bd0c-e649f5e542f1']})

def replay(source_id):
    """Complete eligible original cases, with presentation normalized, not resampled."""
    old = next(q for q in json.loads((HERE / 'source_cases.json').read_text())
               if q[':question/math-academy-id'] == source_id)
    prompt = old[':question/problem']
    fs = old[':question/answer-fields']
    if all(f[':answer-field/type'][':db/ident'].endswith('/blank') for f in fs):
        prompt = normalize_matrix_answer_tables(prompt)
        if 'matrix-answer-brackets' not in prompt:
            raise ValueError('Source replay requires a complete rectangular answer matrix')
    specs = []
    for f in fs:
        choices = f[':answer-field/choices']
        correct_id = f[':answer-field/correct'][':answer/id']
        specs.append((f[':answer-field/key'], f[':answer-field/type'][':db/ident'].split('/')[-1],
                      [(a[':answer/value'], a[':answer/type'][':db/ident'].split('/')[-1]) for a in choices],
                      next(i for i,a in enumerate(choices) if a[':answer/id'] == correct_id)))
    return finish('easy', prompt, old[':question/worked-solution'], specs,
                  {'replay': source_id, 'source_question': old[':question/id']})

def batch(level, count, seed):
    if level == 'unclassified':
        level = 'easy'
    if level not in BANDS or not 0 <= count <= (26 if level == 'hard' else 100):
        raise ValueError('Invalid band/count; hard has 26 distinct side/order/target roles, other bands allow 0..100')
    rng = random.Random(seed)
    groups = [(n, side) for n in (2, 3) for side in ('left', 'right')]
    targets = {g: [(i, j) for i in range(g[0]) for j in range(g[0])] for g in groups}
    for pool in targets.values():
        rng.shuffle(pool)
    records, seen = [], set()
    while len(records) < count:
        active = [g for g in groups if level != 'hard' or targets[g]]
        rng.shuffle(active)
        for n, side in active:
            if len(records) == count:
                break
            target = targets[(n, side)].pop() if level == 'hard' else None
            for _ in range(100):
                try:
                    r = make(level, rng, n, side, target=target)
                except ValueError:
                    continue
                # Numeric identity side, labels and answer form do not create a new task.
                semantic = digest([r['generation']['parameters'], target if level == 'hard' else None,
                                   side if level == 'hard' else None])
                if semantic not in seen:
                    seen.add(semantic)
                    records.append(r)
                    break
            else:
                raise ValueError('Unable to construct a distinct complete bank')
    return records

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty', default='easy', choices=(*BANDS, 'unclassified'))
    p.add_argument('--count', type=int, default=1)
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--format', choices=['json'], default='json')
    p.add_argument('--replay', help='Complete imported Math Academy question ID')
    a = p.parse_args()
    print(json.dumps([replay(a.replay)] if a.replay else batch(a.difficulty, a.count, a.seed), indent=2))

if __name__ == '__main__':
    main()
