#!/usr/bin/env python3
"""Seeded, relocatable exact-entry 3x3 matrix-product practice.

Source replay is an explicit diagnostic mode, never a normal-sampling shortcut.
No assets or external writes are required.
"""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import (matrix_answer, matrix_operands, matrix_tex,
                         normalize_prose, normalize_tex, validate_generated_record)

VERSION = '1.1.0'
KP = {'db_id': 17592186059747, 'id': '9c7a77cf-163a-542a-b4a3-4274344b9cf8',
      'title': 'Multiplying 3x3 Square Matrices'}
CELLS = tuple(itertools.product(range(3), repeat=2))
NONZERO = (-3, -2, -1, 1, 2, 3)


def dot_terms(a, b, i, j):
    def factor(v):
        return str(v) if v >= 0 else '(' + str(v) + ')'
    return '+'.join(factor(a[i][k]) + r'\cdot' + factor(b[k][j]) for k in range(3))


def product(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def identify(record):
    """Content normalization must precede all owned deterministic identities."""
    q = record['question']
    for k in (':question/problem', ':question/worked-solution'):
        q[k] = normalize_prose(q[k])
    fields = q[':question/answer-fields']
    for f in fields:
        for c in f[':answer-field/choices']:
            c[':answer/value'] = normalize_tex(c[':answer/value'])
    signature = [q[':question/problem'], q[':question/worked-solution'],
                 q[':question/difficulty'],
                 [[f[':answer-field/key'], [c[':answer/value'] for c in f[':answer-field/choices']]] for f in fields]]
    root = uuid.uuid5(uuid.NAMESPACE_URL, 'ca-matmul-v1:' + json.dumps(signature, sort_keys=True))
    q[':question/id'] = str(root)
    for i, f in enumerate(fields):
        old = f[':answer-field/correct']
        old_id = old[1] if isinstance(old, list) else old[':answer/id']
        correct_index = next(n for n,c in enumerate(f[':answer-field/choices']) if c[':answer/id'] == old_id)
        f[':answer-field/id'] = str(uuid.uuid5(root, 'field:' + str(i)))
        for n,c in enumerate(f[':answer-field/choices']):
            c[':answer/id'] = str(uuid.uuid5(root, f'field:{i}:answer:{n}'))
        f[':answer-field/correct'] = [':answer/id', f[':answer-field/choices'][correct_index][':answer/id']]
    return validate_generated_record(record)


def build(a, b, targets, difficulty):
    """The single ordered derivation supplies prompt, grid, key and solution."""
    targets = sorted(tuple(c) for c in targets)
    c = product(a, b)
    fields = []
    grid = [[str(v) for v in row] for row in c]
    for n,(i,j) in enumerate(targets, 1):
        key = f'field-{n}'
        ans = {':answer/id': str(n), ':answer/type': ':answer.type/math', ':answer/value': str(c[i][j])}
        fields.append({':answer-field/key': key, ':answer-field/type': ':answer-field.type/blank',
                       ':answer-field/choices': [ans], ':answer-field/correct': [':answer/id', str(n)]})
        grid[i][j] = '{{' + key + '}}'
    prompt = 'Calculate $AB$, where\n\n' + matrix_operands(['A='+matrix_tex(a), 'B='+matrix_tex(b)], stacked=True)
    prompt += '\n\nComplete the product.\n\n' + matrix_answer('AB', grid)
    solution = 'Multiply each row of $A$ by each column of $B$, adding the three pairwise products.\n'
    for i in range(3):
        rows = [f'c_{{{i+1}{j+1}}} &= {dot_terms(a,b,i,j)} = {c[i][j]}' for j in range(3)]
        solution += '\n$$\n' + r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}' + '\n$$\n'
    solution += '\nTherefore,\n$$\nAB=' + matrix_tex(c) + '.\n$$\n'
    return identify({'knowledge_point': KP.copy(), 'question': {
        ':question/problem': prompt, ':question/worked-solution': solution,
        ':question/difficulty': ':question.difficulty/'+difficulty,
        ':question/answer-fields': fields},
        'generation': {'version': VERSION, 'template': 'positioned-product-blanks',
                       'parameters': {'A': a, 'B': b, 'targets': [list(t) for t in targets]},
                       'source_support': ['3b0c400c-89bd-504d-87c3-e0f24957d42b',
                                          '0d0bbd66-8521-57b9-82e2-4d2276785a6e']}})


def target_set(rng, difficulty):
    if difficulty == 'easy':
        cols = rng.sample(range(3), 3)
        return [(i,cols[i]) for i in range(3)]
    if difficulty == 'hard':
        return list(CELLS)
    while True:
        targets = rng.sample(CELLS, 5)
        if len({i for i,j in targets}) == len({j for i,j in targets}) == 3:
            return sorted(targets)


def sample(rng, difficulty):
    # Assign requested positions and structural zeros before sampling magnitudes.
    targets = target_set(rng, difficulty)
    while True:
        a_mask = [[True]*3 for _ in range(3)]
        b_mask = [[True]*3 for _ in range(3)]
        if difficulty != 'hard':
            for i in range(3):
                active = rng.sample(range(3), rng.choice((1,2) if difficulty == 'easy' else (2,3)))
                a_mask[i] = [k in active for k in range(3)]
            for j in range(3):
                active = rng.sample(range(3), rng.choice((2,3)))
                for k in range(3):
                    b_mask[k][j] = k in active
        term_counts = [sum(a_mask[i][k] and b_mask[k][j] for k in range(3)) for i,j in targets]
        if min(term_counts) < 1 or (difficulty == 'moderate' and max(term_counts) < 3):
            continue
        a = [[rng.choice(NONZERO) if active else 0 for active in row] for row in a_mask]
        b = [[rng.choice(NONZERO) if active else 0 for active in row] for row in b_mask]
        return build(a,b,targets,difficulty)


def replay(source_id):
    cases = json.loads(Path(__file__).with_name('source_cases.json').read_text())
    return identify(copy.deepcopy(cases[source_id]))


def generate(difficulty, count, seed):
    if difficulty not in ('easy','moderate','hard') or count < 0:
        raise ValueError('Expected a supported difficulty and nonnegative count')
    rng = random.Random(seed)
    result, seen = [], set()
    while len(result) < count:
        record = sample(rng, difficulty)
        signature = record['question'][':question/id']
        if signature not in seen:
            result.append(record)
            seen.add(signature)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=['easy','moderate','hard','unclassified'], default='moderate')
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    parser.add_argument('--replay-source', help='Diagnostic replay of one complete source UUID')
    args = parser.parse_args()
    if args.count < 0:
        parser.error('--count must be nonnegative')
    records = [replay(args.replay_source)] if args.replay_source else generate(
        'moderate' if args.difficulty == 'unclassified' else args.difficulty, args.count, args.seed)
    print(json.dumps(records, ensure_ascii=False))


if __name__ == '__main__':
    main()
