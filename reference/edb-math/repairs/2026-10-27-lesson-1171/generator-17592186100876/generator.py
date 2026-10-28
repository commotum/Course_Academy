#!/usr/bin/env python3
"""Identity-vector selection, with local source replay and seeded batch output."""
import argparse
import copy
import hashlib
import json
import math
import random
import re
import uuid
from pathlib import Path
from math_format import normalize_prose, normalize_tex, matrix_tex, matrix_answer, normalize_matrix_answer_tables, validate_generated_record

KP = 17592186100876
TITLE = 'Multiplying a Matrix by a Column or Row of the Identity Matrix'
VERSION = 'identity-selection-4-layout'
NS = uuid.UUID('89362140-1a17-56fd-a9ab-4da336112bee')
SOURCE = json.loads(Path(__file__).with_name('source_cases.json').read_text())
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
TEMPLATES = {'easy': ('column-radio', 'column-blank', 'rotation-radio'),
             'moderate': ('row-radio', 'row-blank3', 'row-blank4'),
             'hard': ('cell-radio',)}
POOL = [str(i) for i in range(-9, 10)] + [r'\frac{1}{2}', r'-\frac{3}{2}',
        r'\sqrt{2}', r'-\sqrt{3}', r'2\sqrt{5}', r'-2\sqrt{2}', '3.5', '-2.5']
SYMBOLS = [r'\pi', r'-\frac{\pi}{2}', 'e', r'-e', r'\frac{e}{3}', r'\ln(2)', r'-\ln(3)']


def uid(value):
    return str(uuid.uuid5(NS, json.dumps(value, sort_keys=True, ensure_ascii=True)))


def matrices(text):
    return [[[x.strip() for x in row.split('&')] for row in m[1].split(r'\\')]
            for m in MATRIX.finditer(text)]


def tex(rows):
    return matrix_tex(rows, augmented=False)


def vec(n, j, column):
    return [[str(int(i == j))] for i in range(n)] if column else [[str(int(i == j)) for i in range(n)]]


def col(m, j):
    return [[row[j]] for row in m]


def dot(xs, j):
    return '+'.join('(' + x + r')\cdot ' + str(int(i == j)) for i, x in enumerate(xs))


def display(x):
    return '$$\n' + x + '\n$$'


def seal(problem, solution, level, values, correct_index, metadata, field_keys=None):
    # Normalize BEFORE deriving any content identity. Source DB IDs are never reused.
    problem = normalize_prose(normalize_matrix_answer_tables(problem))
    solution = normalize_prose(solution)
    values = [[normalize_tex(v) for v in bank] for bank in values]
    identity = [VERSION, level, problem, solution, values, correct_index]
    qid = uid(identity)
    fields = []
    for i, bank in enumerate(values):
        key = field_keys[i] if field_keys else ('selection' if len(bank) > 1 else 'field-' + str(i + 1))
        fid = uid([qid, key])
        answers = [{':answer/id': uid([fid, v]), ':answer/type': ':answer.type/math', ':answer/value': v} for v in bank]
        fields.append({':answer-field/id': fid, ':answer-field/key': key,
                       ':answer-field/type': ':answer-field.type/' + ('radio' if len(bank) > 1 else 'blank'),
                       ':answer-field/choices': answers,
                       ':answer-field/correct': [':answer/id', answers[correct_index[i]][':answer/id']]})
    record = {'knowledge_point': {'db_id': KP, 'title': TITLE},
              'question': {':question/id': qid, ':question/problem': problem, ':question/worked-solution': solution,
                           ':question/difficulty': ':question.difficulty/' + level, ':question/answer-fields': fields},
              'generation': {'version': VERSION, **metadata}}
    return validate_generated_record(record)


def construct(level, template, m, target, rng, second=None, wrong_rows=None):
    n = len(m)
    if template not in TEMPLATES[level] or any(len(row) != n for row in m):
        raise ValueError('Invalid template or square matrix')
    if not 0 <= target < n:
        raise ValueError('Invalid target')
    column = template.startswith(('column', 'rotation'))
    hard = template == 'cell-radio'
    selector = vec(n, target, column)
    if hard:
        if second is None or not 0 <= second < n:
            raise ValueError('Invalid second selector')
        problem = 'Calculate the product $(LM)R$, where\n' + display('L=' + tex(vec(n, target, False)))
        problem += '\n' + display('M=' + tex(m)) + '\nand\n' + display('R=' + tex(vec(n, second, True)))
        problem += '\nSelect the resulting $1\\times1$ matrix.'
        out = [[m[target][second]]]
        solution = f'The row $L$ is row ${target+1}$ of $I_{n}$. Left multiplication selects row ${target+1}$ of $M$:\n'
        solution += display('LM=' + tex([m[target]]))
        solution += f'\nThe column $R$ is column ${second+1}$ of $I_{n}$. Right multiplication selects entry ${second+1}$ of that row:\n'
        solution += display('(LM)R=' + tex(out))
        solution += '\nThe single entry is the dot product\n' + display(dot(m[target], second) + '=' + out[0][0])
        # Wrong cells model wrong row, wrong column, or swapped indices. Choose roles before values.
        wrong = [(target, c) for c in range(n) if c != second] + [(r, second) for r in range(n) if r != target]
        if target != second:
            wrong = [(second, target)] + rng.sample(wrong, 3)
        bank = [tex(out)] + [tex([[m[r][c]]]) for r, c in wrong]
        profile = 'wrong-cells'
    else:
        a, b = (m, selector) if column else (selector, m)
        out = col(m, target) if column else [m[target][:]]
        problem = 'Find the product $AB$, if\n' + display('A=' + tex(a)) + '\nand\n' + display('B=' + tex(b))
        orientation = 'column' if column else 'row'
        name = 'B' if column else 'A'
        matrix_name = 'A' if column else 'B'
        side = 'right' if column else 'left'
        solution = f'The matrix ${name}$ is {orientation} ${target+1}$ of $I_{n}$. Multiplying on the {side} selects {orientation} ${target+1}$ of ${matrix_name}$:\n'
        solution += display('AB=' + tex(out)) + '\nCheck the entries by row-by-column multiplication:\n'
        xs = m if column else list(map(list, zip(*m)))
        entries = sum(out, [])
        solution += display(r'\begin{aligned}' + r' \\ '.join(dot(row, target) + '&=' + v for row, v in zip(xs, entries)) + r'\end{aligned}')
        if 'blank' in template:
            keys = ['{{field-' + str(i+1) + '}}' for i in range(n)]
            grid = [[key] for key in keys] if column else [keys]
            problem += '\nEnter the entries from ' + ('top to bottom.' if column else 'left to right.') + '\n\n' + matrix_answer('AB', grid)
            return seal(problem, solution, level, [[v] for v in entries], [0]*n,
                        {'template': template, 'target': target, 'domain': 'exact real entries; copying, no scalar evaluation'})
        correct = tex(out)
        if template == 'rotation-radio':
            columns = [col(m, c) for c in range(n)]
            altered = [[[v.replace(r'\sqrt{2}', '1')] for v, in c] for c in columns if any(r'\sqrt' in v for v, in c)]
            bank = [tex(c) for c in columns + altered]
            profile = 'columns-and-root-omission'
        else:
            indices = list(wrong_rows) if wrong_rows is not None else rng.sample(range(n), 2)
            ordinary = [col(m, c) for c in range(n)] if column else [[row] for row in m]
            confused = [[[x] for x in m[r]] for r in indices] if column else [[[m[r][c] for r in range(n)]] for c in indices]
            bank = [tex(c) for c in ordinary + confused]
            profile = 'columns-and-copied-rows' if column else 'rows-and-copied-columns'
    if hard:
        correct = tex(out)
    bank = [normalize_tex(v) for v in bank]
    if len(bank) != 5 or len(set(bank)) != 5:
        raise ValueError('choice collision')
    rng.shuffle(bank)
    return seal(problem, solution, level, [bank], [bank.index(normalize_tex(correct))],
                {'template': template, 'profile': profile, 'target': target, 'second_target': second,
                 'domain': 'exact real entries; copying, no scalar evaluation'})


def sample(level, rng, template=None, target=None, second=None):
    template = template or rng.choice(TEMPLATES[level])
    n = 4 if template == 'row-blank4' else 3
    target = rng.randrange(n) if target is None else target
    second = rng.randrange(n) if level == 'hard' and second is None else second
    for _ in range(300):
        if template == 'rotation-radio':
            a = r'\frac{\sqrt{2}}{2}'
            m = [[a, '-'+a, '0'], [a, a, '0'], ['0', '0', '1']]
            rng.shuffle(m)
            order = rng.sample(range(3), 3)
            m = [[row[c] for c in order] for row in m]
        else:
            pool = POOL + (SYMBOLS if n == 4 else [])
            m = [[rng.choice(pool) for _ in range(n)] for _ in range(n)]
        try:
            return construct(level, template, m, target, rng, second)
        except ValueError as e:
            if str(e) != 'choice collision':
                raise
    raise ValueError('Could not form distinct plausible choices')


def replay(source_id):
    q = next(q for q in SOURCE['questions'] if source_id in (q[':question/id'], q[':question/math-academy-id']))
    q = copy.deepcopy(q)
    # Existing source template extraction: matrices and selector locate the supported role.
    a, b = matrices(q[':question/problem'])[:2]
    column = len(b[0]) == 1
    m, v = (a, b) if column else (b, a)
    j = sum(v, []).index('1')
    out = col(m, j) if column else [m[j]]
    solution = q[':question/worked-solution'].replace('\u2061', '').replace('⁡', '')
    if source_id in ('q-130247', '2038a353-9df5-5f59-a4d0-04cb2cfa4cea'):
        match = MATRIX.search(solution)
        solution = solution[:match.start()] + tex(out) + solution[match.end():]
    fields = sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key'])
    banks = [[x[':answer/value'] for x in f[':answer-field/choices']] for f in fields]
    correct = [next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id'] == f[':answer-field/correct'][':answer/id']) for f in fields]
    return seal(q[':question/problem'].replace('⁡',''), solution, q[':question/difficulty'][':db/ident'].split('/')[-1],
                banks, correct, {'template': 'source-replay', 'source_question_id': q[':question/id'], 'source_basis': SOURCE['basis']},
                [f[':answer-field/key'] for f in fields])



def numeric_entry(value):
    """Numeric order only for batch bank-cue checks, never answer construction."""
    value = value.replace(' ', '')
    sign = -1 if value.startswith('-') else 1
    value = value.lstrip('+-')
    if value.startswith(r'\frac'):
        parts, depth = [], 0
        for i, char in enumerate(value[5:], 5):
            if char == '{':
                if depth == 0:
                    start = i + 1
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    parts.append(value[start:i])
        return sign * numeric_entry(parts[0]) / numeric_entry(parts[1])
    root = re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}', value)
    if root:
        return sign * int(root[1] or 1) * math.sqrt(int(root[2]))
    logarithm = re.fullmatch(r'\\ln\((\d+)\)', value)
    if logarithm:
        return sign * math.log(int(logarithm[1]))
    if value in (r'\pi', 'e'):
        return sign * (math.pi if value == r'\pi' else math.e)
    return sign * float(value)


def bank_cues(record):
    """Successful simple bank-only strategies; ties identify no unique option."""
    field = record['question'][':question/answer-fields'][0]
    if field[':answer-field/type'] != ':answer-field.type/radio':
        return set()
    bank = field[':answer-field/choices']
    correct = next(i for i, a in enumerate(bank)
                   if a[':answer/id'] == field[':answer-field/correct'][1])
    entries = [sum(matrices(a[':answer/value'])[0], []) for a in bank]
    numbers = [[numeric_entry(x) for x in vector] for vector in entries]
    frequency = [{x: sum(v[j] == x for v in entries) for x in {v[j] for v in entries}}
                 for j in range(len(entries[0]))]
    scores = {
        'first': [v[0] for v in numbers],
        'sum': [sum(v) for v in numbers],
        'norm': [sum(x*x for x in v) for v in numbers],
        'lexicographic': [tuple(v) for v in numbers],
        'radicals': [a[':answer/value'].count(r'\sqrt') for a in bank],
        'zeros': [v.count(0) for v in numbers],
        'negatives': [sum(x < 0 for x in v) for v in numbers],
        'modal': [sum(frequency[j][x] for j, x in enumerate(v)) for v in entries],
    }
    cues = {('position', correct)}
    for name, values in scores.items():
        ordered = sorted(set(values))
        for rank in range(len(ordered)):
            if [i for i, x in enumerate(values) if x == ordered[rank]] == [correct]:
                cues.add((name, rank))
    pairs = [any(all(abs(x+y) < 1e-12 for x, y in zip(v, u))
                 for j, u in enumerate(numbers) if i != j) for i, v in enumerate(numbers)]
    for sign in (-1, 1):
        if [i for i, v in enumerate(numbers) if pairs[i]
            and next((x for x in v if x != 0), 0)*sign > 0] == [correct]:
            cues.add(('sign-pair', sign))
    if [i for i, v in enumerate(entries) if all(frequency[j][x] == max(frequency[j].values())
                                               for j, x in enumerate(v))] == [correct]:
        cues.add(('modal-intersection', 0))
    return cues

def batch(level, count, seed, template=None):
    if count < 0:
        raise ValueError('count must be nonnegative')
    rng = random.Random(seed)
    records, seen = [], set()
    # Plan answer-bearing roles independently of matrix entries and resampling.
    # Repeated recognizable families must not accidentally fix a selector index.
    families = list((template,) if template else TEMPLATES[level])
    family_order, role_orders, previous = [], {}, {}
    surviving_cues = {}
    for _ in range(max(1000, count*100)):
        if len(records) == count:
            return records
        if not family_order:
            family_order = rng.sample(families, len(families))
        family = family_order.pop()
        n = 4 if family == 'row-blank4' else 3
        roles = role_orders.setdefault(family, [])
        if not roles:
            if level == 'hard':
                # Three Latin cycles cover all cells; within each cycle both
                # selectors vary, including diagonal and off-diagonal cases.
                rows, columns = rng.sample(range(n), n), rng.sample(range(n), n)
                roles.extend((rows[i], columns[(i+shift) % n])
                             for shift in rng.sample(range(n), n) for i in range(n))
            else:
                roles.extend((i, None) for i in rng.sample(range(n), n))
            if previous.get(family) == roles[-1] and len(roles) > 1:
                roles[-1], roles[-2] = roles[-2], roles[-1]
        target, second = roles[-1]
        r = sample(level, rng, family, target, second)
        key = r['question'][':question/problem']
        cues = bank_cues(r)
        common = cues & surviving_cues.get(family, set())
        if common:
            # Retry this planned role, not a new target, so cue rejection cannot
            # silently suppress a legitimate selector or bank profile.
            family_order.append(family)
            continue
        if key not in seen:
            surviving_cues[family] = cues if family not in surviving_cues else common
            roles.pop()
            previous[family] = (target, second)
            r['generation'].update({'seed': seed, 'batch_index': len(records)})
            records.append(r)
            seen.add(key)
    raise ValueError('requested batch exceeds sampled family capacity')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--difficulty', choices=tuple(TEMPLATES)+('unclassified',), default='easy')
    p.add_argument('--count', type=int, default=1)
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--format', choices=('json',), default='json')
    p.add_argument('--replay')
    p.add_argument('--template')
    args = p.parse_args()
    level = 'easy' if args.difficulty == 'unclassified' else args.difficulty
    result = [replay(args.replay)] if args.replay else batch(level, args.count, args.seed, args.template)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
