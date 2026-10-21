#!/usr/bin/env python3
"""Seeded, relocatable pivot-column practice. See instructional-account.md."""
import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path
import random
import re
import uuid

from math_format import matrix_tex, normalize_prose, validate_generated_record

VERSION = '1.0.0'
KP = 17592186124480
KP_UUID = 'b1a557d6-52f3-5df3-8088-5b875296e72e'
SHAPES = {'moderate': [(3, 3), (3, 4), (4, 4)],
          'hard': [(3, 4), (4, 4), (4, 5), (4, 6), (5, 5)]}
PROFILES = {'moderate': ['checkbox_swap'],
            'hard': ['checkbox_swap', 'checkbox_eliminate', 'checkbox_mixed',
                     'radio_swap', 'radio_eliminate', 'radio_mixed']}


def leading(row):
    return next((j for j, x in enumerate(row) if x), len(row))


def reduce_matrix(matrix):
    """REF with exact arithmetic; record every row operation and resulting matrix."""
    a = [[Fraction(x) for x in row] for row in matrix]
    m, n = len(a), len(a[0])
    trace, pivots, row = [], [], 0
    while row < m:
        pick = min(range(row, m), key=lambda i: leading(a[i]))
        col = leading(a[pick])
        if col == n:
            break
        if pick != row:
            a[row], a[pick] = a[pick], a[row]
            trace.append((('swap', row, pick), [r[:] for r in a]))
        for i in range(row + 1, m):
            if a[i][col]:
                multiplier = -a[i][col] / a[row][col]
                a[i] = [x + multiplier * y for x, y in zip(a[i], a[row])]
                trace.append((('add', i, row, multiplier), [r[:] for r in a]))
        pivots.append(col)
        row += 1
    return a, pivots, trace


def number_tex(value):
    f = Fraction(value)
    if f.denominator == 1:
        return str(f.numerator)
    return ('-' if f < 0 else '') + r'\frac{' + str(abs(f.numerator)) + '}{' + str(f.denominator) + '}'


def matrix_math(matrix):
    return matrix_tex([[number_tex(x) for x in row] for row in matrix])


def ordinal(j):
    return '$' + str(j) + '$' + {1: 'st', 2: 'nd', 3: 'rd'}.get(j, 'th')


def words(items):
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return ' and '.join(items)
    return ', '.join(items[:-1]) + ', and ' + items[-1]


def subset_value(subset, n):
    return words([ordinal(j + 1) for j in sorted(subset)]) + (' only' if len(subset) < n else '')


def solution(matrix, name, pivots, trace):
    wide = len(matrix[0]) >= 5
    rows = [name + ('=' if wide else ' & =') + matrix_math(matrix)]
    for operation, after in trace:
        if operation[0] == 'swap':
            annotation = 'R_{' + str(operation[1] + 1) + r'}\leftrightarrow R_{' + str(operation[2] + 1) + '}'
        else:
            _, target, source, k = operation
            # Parenthesized signed coefficients avoid ambiguous double signs.
            term = ('R_{' + str(source + 1) + '}') if k == 1 else '(' + number_tex(k) + ')R_{' + str(source + 1) + '}'
            annotation = 'R_{' + str(target + 1) + '}:=R_{' + str(target + 1) + '}+' + term
        if wide:
            rows.extend([annotation, r'\sim ' + matrix_math(after)])
        else:
            rows[-1] += ' && ' + annotation
            rows.append(r' & \sim ' + matrix_math(after))
    environment = 'gathered' if wide else 'aligned'
    chain = r'\begin{' + environment + '}' + r' \\ '.join(rows) + r'\end{' + environment + '}'
    cols = words([ordinal(j + 1) for j in pivots])
    return (f'First, we need to convert ${name}$ to row echelon form:\n\n$$\n' + chain + '\n$$\n\n'
            f'Looking at the row echelon form, we see that ${name}$ has ${len(pivots)}$ pivots. '
            f'In particular, the pivot columns are the {cols} columns.')


def identity(parent, text):
    return str(uuid.uuid5(uuid.UUID(parent), text))


def build_record(matrix, name, band, response='checkbox', bank=None, *, profile=None,
                 seed=None, source=None, prompt=None, field_order=None, extra=None):
    _, pivots, trace = reduce_matrix(matrix)
    n = len(matrix[0])
    if prompt is None:
        prompt = (f'What are the pivot columns of the matrix ${name},$ given by\n\n$$\n'
                  + name + '=' + matrix_math(matrix) + '?\n$$\n')
        if response == 'checkbox':
            prompt += '\nSelect all that apply.'
    q = {':question/difficulty': ':question.difficulty/' + band,
         ':question/problem': normalize_prose(prompt),
         ':question/worked-solution': normalize_prose(solution(matrix, name, pivots, trace))}
    field_specs = []
    if response == 'checkbox':
        for j in (field_order if field_order is not None else range(n)):
            key = f'Column {j + 1}: $' + matrix_math([[r[j]] for r in matrix]) + '$'
            field_specs.append((key, ['false', 'true'], 'true' if j in pivots else 'false'))
    else:
        if bank is None or len(bank) != 5 or len(set(map(tuple, bank))) != 5:
            raise ValueError('Radio requires five distinct subsets')
        field_specs.append(('selection', [subset_value(s, n) for s in bank], subset_value(pivots, n)))
    content = json.dumps([q, field_specs], sort_keys=True)
    qid = identity(KP_UUID, content)
    q[':question/id'] = qid
    fields = []
    for key, values, correct in field_specs:
        fid = identity(qid, key)
        choices = [{':answer/id': identity(fid, value), ':answer/type': ':answer.type/text',
                    ':answer/value': value} for value in values]
        fields.append({':answer-field/id': fid, ':answer-field/key': key,
                       ':answer-field/type': ':answer-field.type/' + response,
                       ':answer-field/choices': choices,
                       ':answer-field/correct': [':answer/id', next(a[':answer/id'] for a in choices if a[':answer/value'] == correct)]})
    q[':question/answer-fields'] = fields
    meta = {'generator': VERSION, 'seed': seed, 'profile': profile,
            'template': 'pivot_columns_' + response,
            'matrix': matrix, 'matrix_name': name, 'pivots': pivots,
            'shape': [len(matrix), n], 'source_ids': source or [],
            'operations': [[str(x) for x in op] for op, _ in trace]}
    if extra:
        meta.update(extra)
    return validate_generated_record({'knowledge_point': {'db_id': KP, 'id': KP_UUID},
                                      'question': q, 'generation': meta})


def source_cases():
    return json.loads(Path(__file__).with_name('source_cases.json').read_text())


def replay(case):
    q = case['question']
    fs = q[':question/answer-fields']
    kind = fs[0][':answer-field/type'][':db/ident'].split('/')[-1]
    bank = None
    order = None
    if kind == 'radio':
        bank = [[int(j) - 1 for j in re.findall(r'\$(\d+)\$', a[':answer/value'])]
                for a in fs[0][':answer-field/choices']]
    else:
        order = [int(re.search(r'Column (\d+)', f[':answer-field/key'])[1]) - 1 for f in fs]
    return build_record(case['matrix'], case['label'], case['band'], kind, bank,
                        profile='source_' + case['source_id'], source=[case['source_id']],
                        prompt=q[':question/problem'], field_order=order)


def sample(rng, band, seed=None, profile=None, shape=None, pivots=None, rank=None,
           elimination_case=None):
    profile = profile or rng.choice(PROFILES[band])
    if profile not in PROFILES[band]:
        raise ValueError('Unsupported profile for difficulty')
    response, reduction = profile.split('_')
    m, n = shape or ((4, 4) if response == 'radio' else rng.choice(SHAPES[band]))
    rank = len(pivots) if pivots is not None else (rank or rng.randint(2, min(m, n - 1)))
    chosen = sorted(pivots) if pivots is not None else sorted(rng.sample(range(n), rank))
    if not (2 <= rank <= min(m, n - 1)) or len(set(chosen)) != rank or not all(0 <= p < n for p in chosen):
        raise ValueError('Inadmissible pivot assignment')
    if reduction != 'swap':
        elimination_case = elimination_case or rng.choice(['new_pivot'] + (['zero_row'] if rank < m else []))
        if elimination_case not in ('new_pivot', 'zero_row') or (elimination_case == 'zero_row' and rank == m):
            raise ValueError('Inadmissible elimination case')
    # Choose the full radio profile before numerical data. Both size groups can win.
    bank, multiplicity = None, None
    if response == 'radio':
        multiplicity = rng.choice([2, 3])
        same = [list(s) for s in itertools.combinations(range(n), rank) if list(s) != chosen]
        other_rank = 5 - rank
        other = [list(s) for s in itertools.combinations(range(n), other_rank)]
        bank = [chosen] + rng.sample(same, multiplicity - 1) + rng.sample(other, 5 - multiplicity)
        rng.shuffle(bank)
    # Build small echelon data compatible with the already assigned answer roles.
    rejected = 0
    while rejected < 300:
        e = [[0] * n for _ in range(m)]
        for i, col in enumerate(chosen):
            e[i][col] = rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
            for j in range(col + 1, n):
                e[i][j] = rng.randint(-5, 5)
        a = [r[:] for r in e]
        if reduction in ('eliminate', 'mixed'):
            # Inverse additions create hidden leading entries; count remains bounded.
            targets = range(1, rank) if elimination_case == 'new_pivot' else range(rank, m)
            pairs = [(s, t) for t in targets for s in range(min(t, rank))]
            amount = 1 if reduction == 'mixed' else rng.choice([1, 2])
            for s, t in rng.sample(pairs, min(amount, len(pairs))):
                k = rng.choice([-2, -1, 1, 2])
                a[t] = [x + k * y for x, y in zip(a[t], a[s])]
        if reduction in ('swap', 'mixed'):
            swaps = 1 if band == 'moderate' or reduction == 'mixed' else rng.choice([1, 2])
            for _ in range(swaps):
                i, j = rng.sample(range(m), 2)
                a[i], a[j] = a[j], a[i]
        _, actual, trace = reduce_matrix(a)
        adds = sum(op[0] == 'add' for op, _ in trace)
        swaps = len(trace) - adds
        valid = actual == chosen and max(abs(x) for r in a for x in r) <= 16
        valid &= (1 <= swaps <= (1 if band == 'moderate' else 2) and adds == 0) if reduction == 'swap' else (
            swaps == 0 and 1 <= adds <= 2) if reduction == 'eliminate' else (swaps == 1 and adds == 1)
        if valid:
            return build_record(a, rng.choice(['A', 'B', 'P']), band, response, bank,
                                profile=profile, seed=seed,
                                source=['q-131300', 'q-35754', 'q-73636', 'q-35731', 'q-35757', 'q-73637'] if band == 'moderate' else
                                ['e-4706', 'q-35732', 'q-35734', 'q-131305', 'q-35753', 'q-131303'],
                                extra={'rejections': rejected, 'rank': rank, 'bank_profile': 'binary' if response == 'checkbox' else 'authored_two_size_groups',
                                       'key_size_multiplicity': multiplicity, 'elimination_case': elimination_case,
                                       'bounds': 'entries -16..16; 1..2 row operations'})
        rejected += 1
    raise RuntimeError('Unable to realize the chosen roles within workload bounds')


def generate(difficulty, count, seed):
    if difficulty not in PROFILES:
        raise ValueError('Supported difficulties: moderate, hard; easy is unsupported')
    rng = random.Random(seed)
    return [sample(rng, difficulty, seed=seed) for _ in range(count)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='moderate', choices=['easy', 'moderate', 'hard'])
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    parser.add_argument('--replay-source', help='Source q-ID, or all; preserves original difficulty')
    args = parser.parse_args()
    if args.count < 0:
        parser.error('count must be nonnegative')
    if args.replay_source:
        cases = [c for c in source_cases() if args.replay_source in ('all', c['source_id'])]
        if not cases:
            parser.error('unknown source ID')
        records = [replay(c) for c in cases]
    else:
        if args.difficulty == 'easy':
            parser.error('easy is unsupported by the source evidence')
        records = generate(args.difficulty, args.count, args.seed)
    print(json.dumps(records, ensure_ascii=False, indent=2))



# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__':
    main()
