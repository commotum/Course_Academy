#!/usr/bin/env python3
"""Seeded square-matrix recognition; adapted from supplied square-recognition draft.
No database, images, repository runtime imports, or generated asset files.
"""
import argparse
import hashlib
import itertools
import json
import random
import re
import sys
import uuid
from pathlib import Path
from math_format import matrix_tex, normalize_prose, checked_math_content, FORMAT_VERSION

SOURCE = json.loads(Path(__file__).with_name('source-data.json').read_text())
KP_ID = 17592186087696
KP_UUID = '3ca13445-0218-5950-967e-a68bcfec32c7'
VERSION = 'square-recognition-v3'
NS = uuid.UUID(KP_UUID)
SUPPORTED_LEVELS = ('easy',)
SUPPORTED_TEMPLATES = ('three-checkbox', 'three-radio')
SHAPES = tuple(itertools.product(range(1, 6), repeat=2))
RADIO_SUBSETS = ((0, 2), (), (0, 1), (1,), (0,))
ENTRIES = tuple(map(str, range(-10, 11))) + ('0.1', '0.2', '0.5', '1.5', r'\sqrt{2}', r'-\sqrt{2}', r'\sqrt{3}')
QS = {q[':question/math-academy-id']: q for q in SOURCE['kp'][':knowledge-point/questions']}


def parse_matrices(text):
    pairs = []
    for match in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S):
        rows = [[cell.strip() for cell in row.split('&')] for row in match[2].split(r'\\')]
        shape(rows)
        pairs.append((match[1], rows))
    return pairs


def shape(matrix):
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError('nonrectangular matrix')
    return len(matrix), len(matrix[0])


def uid(value):
    return str(uuid.uuid5(NS, json.dumps(value, sort_keys=True, separators=(',', ':'))))


def subset_text(indices, labels):
    names = ['$' + labels[i] + '$' for i in sorted(indices)]
    return ' and '.join(names) + ' only' if names else 'None'


def chosen_of(p):
    return tuple(i for i, matrix in enumerate(p['matrices']) if len(matrix) == len(matrix[0]))


def conclusion(labels, chosen):
    names = ['$' + labels[i] + '$' for i in chosen]
    if not names:
        return 'none of these matrices are square matrices.'
    if len(names) == 1:
        return 'only ' + names[0] + ' is a square matrix.'
    if len(names) == 3:
        return ', '.join(names[:-1]) + ', and ' + names[-1] + ' are square matrices.'
    return 'only ' + ' and '.join(names) + ' are square matrices.'


def solution_of(p, template):
    steps = []
    for label, matrix in zip(p['labels'], p['matrices']):
        rows, cols = shape(matrix)
        if template == 'three-radio':
            steps.append(f'- ${label}$ is ' + ('' if rows == cols else 'not ') + 'a square matrix.')
            continue
        if rows == cols:
            reason = 'is a square matrix since it has the same number of rows and columns.'
            end = 'so it is a'
        else:
            reason = 'is *not* a square matrix since the numbers of rows and columns are not the same.'
            end = "so it's a"
        rn, cn = ('row' if rows == 1 else 'rows'), ('column' if cols == 1 else 'columns')
        steps.append(f'- ${label}$ {reason} It has ${rows}$ {rn} and ${cols}$ {cn}, {end} ${rows}\\times {cols}$ matrix.')
    chosen = chosen_of(p)
    if template == 'three-radio' and len(chosen) == 1:
        tail = '$' + p['labels'][chosen[0]] + '$ satisfies the definition.'
    else:
        tail = conclusion(p['labels'], chosen)
    return normalize_prose('\n\n'.join(steps) + '\n\nTherefore, ' + tail)


def bank_of(p):
    roles = p.get('bank_roles', [0, 1, 2])
    return tuple(tuple(sorted(roles[i] for i in subset)) for subset in RADIO_SUBSETS)


def sample(rng, template):
    # Decision assignment precedes dimensions, labels and entries.
    p = {'bank_roles': rng.sample(range(3), 3)} if template == 'three-radio' else {}
    chosen = rng.choice(bank_of(p)) if template == 'three-radio' else tuple(i for i in range(3) if rng.getrandbits(1))
    dimensions = [rng.choice([d for d in SHAPES if (d[0] == d[1]) == (i in chosen)]) for i in range(3)]
    p['labels'] = sorted(rng.sample('ABCDEFGHJKLMNPQRSTUVWXYZ', 3))
    p['matrices'] = []
    for rows, cols in dimensions:
        # Appearance is sampled independently of membership, including special-looking distractors.
        appearance = rng.choice(('general', 'general', 'zero', 'diagonal'))
        matrix = [[rng.choice(ENTRIES) if appearance == 'general' or (appearance == 'diagonal' and r == c) else '0'
                   for c in range(cols)] for r in range(rows)]
        p['matrices'].append(matrix)
    p['none_instruction'] = True
    return p


def parameters_of(q):
    text = q[':question/problem']
    pairs = parse_matrices(text)
    if not pairs:
        pairs = [parse_matrices(f[':answer-field/key'])[0] for f in q[':question/answer-fields']]
    pairs.sort()
    return {'labels': [label for label, _ in pairs], 'matrices': [m for _, m in pairs],
            'none_instruction': 'If none apply' in text, 'bank_roles': [0, 1, 2]}


def validate_parameters(p, template):
    if len(p['labels']) != 3 or len(set(p['labels'])) != 3 or any(not re.fullmatch('[A-Z]', l) for l in p['labels']):
        raise ValueError('three distinct capital labels required')
    if len(p['matrices']) != 3 or sorted(p.get('bank_roles', [0, 1, 2])) != [0, 1, 2]:
        raise ValueError('invalid matrix count or bank roles')
    for matrix in p['matrices']:
        if shape(matrix) not in SHAPES or any(x not in ENTRIES for row in matrix for x in row):
            raise ValueError('outside supported shape or entry domain')
    if template == 'three-radio' and chosen_of(p) not in bank_of(p):
        raise ValueError('complete source-profile bank does not express this subset')


@checked_math_content
def generate(level='easy', seed=0, template=None, parameters=None, replay_id=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('unsupported difficulty; supported: easy')
    rng = random.Random(seed)
    source_question = QS[replay_id] if replay_id else None
    if source_question:
        template = 'three-radio' if ':answer-field.type/radio' in str(source_question[':question/answer-fields'][0][':answer-field/type']) else 'three-checkbox'
        p = parameters_of(source_question)
    else:
        template = template or rng.choice(SUPPORTED_TEMPLATES)
        if template not in SUPPORTED_TEMPLATES:
            raise ValueError('unsupported template')
        p = json.loads(json.dumps(parameters)) if parameters is not None else sample(rng, template)
    validate_parameters(p, template)
    prompt = 'Which of the following are square matrices?'
    matrix_keys = ['$' + l + '=' + matrix_tex(m) + '$' for l, m in zip(p['labels'], p['matrices'])]
    if template == 'three-checkbox':
        prompt += '\n\nSelect all that apply.'
        if p.get('none_instruction', True):
            prompt += ' If none apply, leave all boxes unchecked.'
        specs = [(k, ('false', 'true'), 'true' if i in chosen_of(p) else 'false') for i, k in enumerate(matrix_keys)]
    else:
        # Preserve the source stacked operand layout and spacing at replay.
        prompt += '\n\n<div class="matrix-operands matrix-operands-stacked">\n' + '\n'.join(
            '<div>$' + l + ' =' + matrix_tex(m) + '$</div>' for l, m in zip(p['labels'], p['matrices'])) + '\n</div>'
        specs = [('selection', tuple(subset_text(s, p['labels']) for s in bank_of(p)), subset_text(chosen_of(p), p['labels']))]
    prompt = normalize_prose(prompt)
    solution = solution_of(p, template)
    difficulty = source_question.get(':question/difficulty') if source_question else ':question.difficulty/easy'
    if isinstance(difficulty, dict):
        difficulty = difficulty[':db/ident']
    qid = uid([VERSION, prompt, solution, difficulty, specs])
    fields = []
    for key, bank, correct in specs:
        fid = uid([qid, key])
        answers = [{':answer/id': uid([fid, value]), ':answer/type': ':answer.type/text', ':answer/value': value} for value in bank]
        rng.shuffle(answers)
        fields.append({':answer-field/id': fid, ':answer-field/key': key,
                       ':answer-field/type': ':answer-field.type/' + template.split('-')[1],
                       ':answer-field/choices': answers,
                       ':answer-field/correct': [':answer/id', next(a[':answer/id'] for a in answers if a[':answer/value'] == correct)]})
    q = {':question/id': qid, ':question/problem': prompt, ':question/worked-solution': solution, ':question/answer-fields': fields}
    if difficulty:
        q[':question/difficulty'] = difficulty
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': 'Identifying a Square Matrix'}, 'question': q,
            'generation': {'version': VERSION, 'seed': seed, 'level': level, 'template': template,
                           'profile': 'source-subset-bank' if template == 'three-radio' else 'boolean-membership',
                           'parameters': p, 'replay_id': replay_id, 'math_format': FORMAT_VERSION,
                           'source': {k: SOURCE[k] for k in ('database', 'lineage', 'basis')},
                           'source_references': [replay_id] if replay_id else (['q-7826'] if template == 'three-radio' else [s for s in QS if s != 'q-7826']),
                           'semantic_instance': [shape(m) for m in p['matrices']],
                           'runtime': {'python': sys.version.split()[0]}}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=SUPPORTED_LEVELS, default='easy')
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json',), default='json')
    args = parser.parse_args()
    if args.count < 1:
        parser.error('count must be positive')
    print(json.dumps([generate(args.difficulty, args.seed + i) for i in range(args.count)], indent=2))



# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__':
    main()
