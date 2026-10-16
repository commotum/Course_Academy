#!/usr/bin/env python3
"""Seeded special-matrix recognition; every label can qualify or fail."""
import argparse
import json
import random
import re
import sys
import uuid
from pathlib import Path

try:
    import sympy as sp
except ModuleNotFoundError:
    import os
    interpreter = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    os.execv(str(interpreter), [str(interpreter), str(Path(__file__).resolve()), *sys.argv[1:]])

if Path(__file__).with_name('math_format.py').is_file():
    from math_format import matrix_operands
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.question_capture.math_format import matrix_operands

KP_ID = 17592186087697
KP_UUID = '09fa0899-a3d2-584f-8cdd-a471f8cfd16b'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
SUPPORTED_LEVELS = ('easy',)
VERSION = '2.0.0'
HERE = Path(__file__).with_suffix('')
TEMPLATE_FILE = HERE / 'templates.json' if HERE.is_dir() else Path(__file__).with_name('templates.json')
TEMPLATES = json.loads(TEMPLATE_FILE.read_text())
PATTERN = r'([A-Z])\s*=\s*\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}'


def arrays(text):
    out = {}
    for match in re.finditer(PATTERN, text):
        raw = re.sub(r'\\text\{[^}]*\}', '', match[2])
        out[match[1]] = [[v.strip() for v in row.strip().split('&')] for row in raw.split('\\\\')]
    return out


def properties(rows):
    matrix = sp.Matrix([[sp.Rational(v) for v in row] for row in rows])
    square = matrix.rows == matrix.cols
    diagonal = square and all(matrix[i,j] == 0 for i in range(matrix.rows) for j in range(matrix.cols) if i != j)
    return diagonal, square and matrix == sp.eye(matrix.rows)


def role_of(rows):
    diagonal, identity = properties(rows)
    return 'rectangular' if len(rows) != len(rows[0]) else 'identity' if identity else 'diagonal' if diagonal else 'offdiagonal'


def fingerprint_text(text):
    kind = 'identity' if 'identity matrices?' in text else 'diagonal'
    # Label/order changes and irrelevant magnitude changes cannot replenish a pool.
    items = [(len(rows), len(rows[0]), tuple(tuple(0 if sp.Rational(v) == 0 else 1 if sp.Rational(v) == 1 else 2 for v in row) for row in rows)) for rows in arrays(text).values()]
    return json.dumps([kind, sorted(items)], separators=(',', ':'))


def sample_matrix(rng, role):
    r = c = rng.randint(2, 4)
    if role == 'rectangular':
        r, c = rng.choice([(a,b) for a in range(2,5) for b in range(2,5) if a != b])
    rows = [['0'] * c for _ in range(r)]
    for i in range(min(r,c)):
        rows[i][i] = '1' if role == 'identity' else rng.choice(['0','1','2','3','-2'])
    if role == 'diagonal' and all(rows[i][i] == '1' for i in range(r)):
        i = rng.randrange(r)
        rows[i][i] = '2'
    witness = None
    if role == 'offdiagonal':
        cells = rng.sample([(i,j) for i in range(r) for j in range(c) if i != j], rng.randint(1,2))
        for i,j in cells:
            rows[i][j] = rng.choice(['1','2','-1','5','7'])
        i,j = rng.choice(cells)
        witness = [i+1,j+1]
    return rows, witness


def explain(kind, labels, matrices, witnesses):
    bullets, selected = [], []
    for label, rows, witness in zip(labels, matrices, witnesses):
        diagonal, identity = properties(rows)
        correct = identity if kind == 'identity' else diagonal
        article = 'an' if kind == 'identity' else 'a'
        prefix = f'- ${label}$ is ' + ('' if correct else '*not* ') + f'{article} {kind} matrix. '
        if len(rows) != len(rows[0]):
            reason = "It is not a square matrix: it has " + str(len(rows)) + ' rows and ' + str(len(rows[0])) + ' columns.'
        elif not diagonal:
            i,j = witness
            reason = 'It is square, but an entry off the main diagonal is nonzero: $' + '{' + label.lower() + '}_{' + str(i) + str(j) + '}=' + rows[i-1][j-1] + r'\ne 0$.'
        elif kind == 'identity' and not identity:
            i = next(i for i in range(len(rows)) if sp.Rational(rows[i][i]) != 1)
            reason = 'It is diagonal, but its diagonal entries are not all ones: $' + '{' + label.lower() + '}_{' + str(i+1) + str(i+1) + '}=' + rows[i][i] + r'\ne 1$.'
        elif kind == 'identity':
            reason = 'It is square, every main diagonal entry is one, and every off-diagonal entry is zero.'
        else:
            reason = 'It is square and every off-diagonal entry is zero.'
            if identity:
                reason += ' It is also an identity matrix; identity matrices are diagonal matrices.'
        bullets.append(prefix + reason)
        if correct:
            selected.append(label)
    if not selected:
        conclusion = f'Therefore, none of the given matrices are {kind} matrices.'
    else:
        names = ' and '.join('$' + name + '$' for name in selected)
        conclusion = 'Therefore, ' + ('only ' if len(selected) < 3 else '') + names + (' is ' if len(selected) == 1 else ' are ') + (('an ' if kind == 'identity' else 'a ') + kind + ' matrix.' if len(selected) == 1 else kind + ' matrices.')
    return '\n\n'.join(bullets + [conclusion])


def generate(difficulty='easy', seed=0, template=None, parameters=None, profile=None, selection=None):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Only easy is supported')
    rng = random.Random(seed)
    template = template or rng.choice(list(TEMPLATES))
    t = TEMPLATES[template]
    if profile not in (None, template):
        raise ValueError('Unknown checkbox profile')
    if selection is not None and (type(selection) is not int or not 0 <= selection <= 7):
        raise ValueError('Selection must be a three-bit mask, 0 through 7')
    if parameters is None:
        selection = rng.randrange(8) if selection is None else selection
        # Uniform subset sampling includes none, each singleton, each pair, and all.
        positives = ('identity',) if t['kind'] == 'identity' else ('diagonal','identity')
        negatives = ('diagonal','offdiagonal','rectangular') if t['kind'] == 'identity' else ('offdiagonal','rectangular')
        roles = [rng.choice(positives if selection & (1 << i) else negatives) for i in range(3)]
        for _ in range(1000):
            sampled = [sample_matrix(rng, role) for role in roles]
            matrices, witnesses = map(list, zip(*sampled))
            if sum(len(m)*len(m[0]) for m in matrices) <= 36:
                parameters = {'matrices': matrices, 'witnesses': witnesses}
                break
        else:
            raise ValueError('Could not sample within the easy inspection workload')
    p = json.loads(json.dumps(parameters))
    matrices, witnesses, labels = p['matrices'], p['witnesses'], t['labels']
    if len(matrices) != 3 or len(witnesses) != 3:
        raise ValueError('Three matrices and witness slots required')
    for rows, witness in zip(matrices, witnesses):
        if not 2 <= len(rows) <= 4 or any(not 2 <= len(row) <= 4 for row in rows) or len({len(row) for row in rows}) != 1:
            raise ValueError('Outside bounded shape domain')
        if any(sp.Rational(v) not in range(-3,8) for row in rows for v in row):
            raise ValueError('Outside bounded entry domain')
        role = role_of(rows)
        if role == 'offdiagonal':
            if witness is None or len(witness) != 2:
                raise ValueError('Missing nonzero off-diagonal witness')
            i,j = witness
            if type(i) is not int or type(j) is not int or i == j or not 1 <= i <= len(rows) or not 1 <= j <= len(rows[0]) or sp.Rational(rows[i-1][j-1]) == 0:
                raise ValueError('Invalid off-diagonal witness')
        elif witness is not None:
            raise ValueError('Unexpected witness')
    if sum(len(m)*len(m[0]) for m in matrices) > 36:
        raise ValueError('Exceeds easy inspection workload')
    actual = sum(1 << i for i,m in enumerate(matrices) if properties(m)[int(t['kind'] == 'identity')])
    if selection is not None and actual != selection:
        raise ValueError('Supplied matrices disagree with requested selection')
    if p == t['parameters']:
        # Historical source replay remains exact; ordinary sampling has variable roles.
        problem, worked = t['problem'], t['worked_solution']
    else:
        rendered = [label + '=' + r'\begin{bmatrix}' + r' \\ '.join(' & '.join(row) for row in rows) + r'\end{bmatrix}' for label,rows in zip(labels,matrices)]
        problem = f'Which of the following are {t["kind"]} matrices?\n\n' + matrix_operands(rendered, stacked=True) + '\n\nSelect all that apply.'
        worked = explain(t['kind'], labels, matrices, witnesses)
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID), json.dumps([problem,worked], sort_keys=True)))
    fields = []
    for label,rows in zip(labels,matrices):
        correct = properties(rows)[int(t['kind'] == 'identity')]
        fid = str(uuid.uuid5(uuid.UUID(qid), 'field:' + label))
        choices = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid),value)), ':answer/type': ':answer.type/text', ':answer/value': value} for value in ('false','true')]
        fields.append({':answer-field/id':fid, ':answer-field/key':label, ':answer-field/type':':answer-field.type/checkbox', ':answer-field/choices':choices, ':answer-field/correct':[':answer/id',choices[int(correct)][':answer/id']]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Identifying a Special Square Matrix'}, 'question':{':question/id':qid, ':question/problem':problem, ':question/worked-solution':worked, ':question/difficulty':':question.difficulty/easy', ':question/answer-fields':fields}, 'generation':{'version':VERSION, 'template':template, 'bank_profile':template, 'seed':seed, 'parameters':p, 'roles':[role_of(m) for m in matrices], 'selection':actual, 'parameter_fingerprint':fingerprint_text(problem), 'source_basis':t['basis'], 'sympy_version':sp.__version__}}


def batch(difficulty, count, seed):
    if difficulty not in SUPPORTED_LEVELS or not 0 <= count <= 1000:
        raise ValueError('Unsupported difficulty or count outside 0..1000')
    records, used = [], set()
    for n in range(20000):
        if len(records) >= count:
            break
        record = generate(difficulty, seed+n, template=list(TEMPLATES)[n % len(TEMPLATES)])
        fingerprint = record['generation']['parameter_fingerprint']
        if fingerprint not in used:
            records.append(record); used.add(fingerprint)
    if len(records) != count:
        raise ValueError('Distinct-question search exhausted')
    return records


def markdown(record):
    return record['question'][':question/problem'] + '\n\n' + record['question'][':question/worked-solution']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json','markdown'], default='json')
    args = parser.parse_args()
    records = batch(args.difficulty, args.count, args.seed)
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(map(markdown, records)))
