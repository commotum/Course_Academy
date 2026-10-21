#!/usr/bin/env python3
"""Seeded easy leading-entry sums; see instructional-account.md.

No medium/hard escalation. Integer arithmetic, row selection, and a five-option
radio bank retain the observed backbone. Choice profiles are explicitly numeric
offset patterns, with unresolved cognitive interpretations, not invented errors.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import uuid
from math_format import normalize_prose, checked_math_content
import sympy as sp

KP_ID = 17592186129176
KP_UUID = '31c3678b-4f00-54d6-bb84-c7718fd622cb'
TITLE = 'Identifying the Leading Entries of a Matrix'
VERSION = '1.1.1'
HERE = Path(__file__).resolve().parent
SOURCE = json.loads((HERE / 'source.json').read_text())
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def parse(prompt):
    body = re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', prompt, re.S)[1]
    matrix = [[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
    rows = [int(n)-1 for n in re.findall(r'\$(\d)\$(?:st|nd|rd|th)', prompt.split('rows')[0])]
    return {'matrix': matrix, 'rows': rows}


def leading(matrix, rows):
    return [next(x for x in matrix[r] if x) for r in rows]


def validate_parameters(parameters, n):
    m, rows = parameters['matrix'], parameters['rows']
    if (len(m) != 4 or any(len(row) != 4 or not any(row) or
            any(type(x) is not int or not -9 <= x <= 9 for x in row) for row in m)
            or len(rows) != n or rows != sorted(set(rows)) or
            any(type(r) is not int or not 0 <= r < 4 for r in rows)):
        raise ValueError('Expected a nonzero-row 4x4 integer matrix in [-9,9] and distinct sorted eligible rows')


def task_fingerprint(parameters):
    # Ignore seeds, distractors, formatting and even changes confined to unqueried
    # rows or trailing entries. Only requested rows, first-nonzero columns and
    # their values determine semantic novelty.
    m, rows = parameters['matrix'], parameters['rows']
    return digest({'rows': rows, 'leading': [next((j, x) for j, x in enumerate(m[r]) if x) for r in rows]})


# Build every profile from the complete captured snapshot, including its bank.
# checks/source_coverage.py compares against an independent capture fixture.
CASES = {}
for q in SOURCE['record'][':knowledge-point/questions']:
    p = parse(q[':question/problem'])
    answer = int(sum(map(sp.Integer, leading(p['matrix'], p['rows']))))
    bank = [int(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
    assert len(bank) == len(set(bank)) == 5 and answer in bank
    mid = q[':question/math-academy-id']
    CASES[mid] = {'source': q, 'parameters': p, 'answer': answer,
                  'offsets': [a-answer for a in bank],
                  'template': 'sum_' + str(len(p['rows'])) + '_rows'}


def ordinal(i):
    # Keep number and suffix in one MathJax object so a narrow line cannot split 3/rd.
    return '$' + str(i+1) + r'\text{' + ('st', 'nd', 'rd', 'th')[i] + '}$'


def join(items):
    if len(items) == 2:
        return ' and '.join(items)
    # Keep list punctuation with its inline math object across browser line wraps.
    comma = lambda item: item[:-1] + ',$' if item.endswith('$') else item + ','
    return ' '.join(comma(item) for item in items[:-1]) + ' and ' + items[-1]


def matrix_latex(matrix):
    return r'\begin{bmatrix}' + r' \\ '.join(' & '.join(map(str, row)) for row in matrix) + r'\end{bmatrix}'


@checked_math_content
def generate(level='easy', seed=0, template=None, parameters=None, profile=None, replay=False, anchor_rank=None):
    if level != 'easy':
        raise ValueError('Unsupported difficulty: only easy source-backed integer leading-entry sums are validated')
    rng = random.Random(seed)
    eligible = [name for name, c in CASES.items() if template is None or c['template'] == template]
    if profile is None:
        if not eligible:
            raise ValueError('Unsupported template')
        profile = rng.choice(sorted(eligible))
    if profile not in eligible:
        raise ValueError('Profile does not belong to the requested template')
    case = CASES[profile]
    n = len(case['parameters']['rows'])
    source_bank = sorted(case['answer'] + offset for offset in case['offsets'])
    if parameters is not None:
        validate_parameters(parameters, n)
    if replay:
        original_rank = source_bank.index(case['answer'])
        if anchor_rank is not None and anchor_rank != original_rank:
            raise ValueError('Replay must preserve the source key rank')
        anchor_rank = original_rank
    elif anchor_rank is None:
        if parameters is None:
            anchor_rank = rng.randrange(5)
        else:
            total = sum(leading(parameters['matrix'], parameters['rows']))
            compatible = [i for i in range(5) if all(-9*n <= total+b-source_bank[i] <= 9*n for b in source_bank)]
            anchor_rank = rng.choice(compatible)
    if type(anchor_rank) is not int or not 0 <= anchor_rank < 5:
        raise ValueError('Expected a bank anchor rank from 0 to 4')
    sampling_attempts = 0
    if parameters is None:
        # Documented same-method generalization: each leading column is eligible;
        # every row remains nonzero. No new operation or reasoning stage is added.
        rows = sorted(rng.sample(range(4), n))
        columns = [rng.randrange(4) for _ in range(4)]
        # Keep the selected roles and complete bank shape. Only fill compatible
        # values so numerical range alone cannot eliminate a distractor.
        while True:
            sampling_attempts += 1
            if sampling_attempts > 1000:
                raise RuntimeError('Compatible value sampler exhausted')
            matrix = []
            for col in columns:
                matrix.append([0]*col + [rng.choice([i for i in range(-9, 10) if i])] +
                              [rng.randint(-9, 9) for _ in range(3-col)])
            total = sum(leading(matrix, rows))
            if all(-9*n <= total+b-source_bank[anchor_rank] <= 9*n for b in source_bank):
                break
        parameters = {'matrix': matrix, 'rows': rows}
    parameters = json.loads(json.dumps(parameters))
    m, rows = parameters['matrix'], parameters['rows']
    validate_parameters(parameters, n)
    values = leading(m, rows)
    correct = int(sum(map(sp.Integer, values)))
    offsets = [value - source_bank[anchor_rank] for value in source_bank]
    bank = [correct + offset for offset in offsets]
    if any(not -9*n <= b <= 9*n for b in bank):
        raise ValueError('Explicit bank anchor is incompatible with the possible sum range')
    assert len(set(bank)) == 5 and bank.count(correct) == 1
    matrix = matrix_latex(m)
    row_text = join([ordinal(i) for i in rows])
    prompt = f'What is the sum of the leading entries of the {row_text} rows in the matrix $A,$ given below?\n\n$$\nA={matrix}\n$$'
    summands = '+'.join(str(x) if x >= 0 or i == 0 else '('+str(x)+')' for i, x in enumerate(values))
    solution = (f'The first non-zero entry of each row (from left to right) is the leading entry. \n\n'
                f'Therefore, the leading entries of the {row_text} rows of $A$ are '
                + join(['$'+str(x)+'$' for x in values]) + ', respectively.\n\n$$\nA='
                + matrix + '\n$$\n\n' + f'So, the answer is ${summands}={correct}.$')
    if replay:
        if parameters != case['parameters']:
            raise ValueError('Exact source replay requires its original parameters')
        # Preserve incidental source typography/layout as an explicit replay mode.
        prompt = case['source'][':question/problem']
        solution = case['source'].get(':question/worked-solution', solution)
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    fp = task_fingerprint(parameters)
    # A bank is part of authored identity; it never establishes task distinctness.
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID), VERSION + digest({'prompt': prompt, 'solution': solution, 'bank': sorted(bank), 'profile': profile})))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    answers = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), str(x))),
                ':answer/type': ':answer.type/math', ':answer/value': str(x)} for x in bank]
    rng.shuffle(answers)
    correct_id = next(a[':answer/id'] for a in answers if a[':answer/value'] == str(correct))
    question = {':question/id': qid, ':question/difficulty': ':question.difficulty/easy',
                ':question/problem': prompt, ':question/worked-solution': solution,
                ':question/answer-fields': [{':answer-field/id': fid, ':answer-field/key': 'selection',
                    ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': answers,
                    ':answer-field/correct': [':answer/id', correct_id]}]}
    if replay:
        source_level = case['source'].get(':question/difficulty')
        if source_level is None:
            question.pop(':question/difficulty')
        else:
            question[':question/difficulty'] = source_level[':db/ident']
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE}, 'question': question,
            'generation': {'version': VERSION, 'seed': seed, 'template': case['template'],
                'bank_profile': profile, 'parameters': parameters, 'source_ids': [profile],
                'source_basis': SOURCE['basis'], 'lineage': LINEAGE, 'sympy_version': sp.__version__,
                'parameter_fingerprint': fp, 'plot_requirement': 'none', 'source_replay': replay,
                'bank_recipe': 'correct + source_bank_value - selected_source_anchor',
                'bank_anchor_rank': anchor_rank, 'bank_offsets': offsets,
                'value_sampling_attempts': sampling_attempts,
                'source_difficulty_missing': ':question/difficulty' not in case['source'],
                'reconstructed_source_fields': [key for key in (':question/worked-solution',)
                    if replay and key not in case['source']] +
                    ([':answer-field/correct'] if replay and ':answer-field/correct' not in case['source'][':question/answer-fields'][0] else []),
                'domain': '4x4; integers [-9,9]; no zero rows; two or three distinct selected rows',
                'generalization': 'All eligible row subsets and leading columns; complete translated source bank shapes with variable anchor'}}


def generate_easy(seed=0, **kwargs):
    return generate('easy', seed, **kwargs)


def markdown(rec):
    q = rec['question']
    f = q[':question/answer-fields'][0]
    return q[':question/problem'] + '\n\n' + '\n'.join(
        '- ' + a[':answer/value'] + (' (correct)' if a[':answer/id'] == f[':answer-field/correct'][1] else '')
        for a in f[':answer-field/choices']) + '\n\n' + q[':question/worked-solution']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=['easy', 'moderate', 'hard'], default='easy')
    parser.add_argument('--template', choices=['sum_2_rows', 'sum_3_rows'])
    parser.add_argument('--profile', choices=sorted(CASES))
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    args = parser.parse_args()
    if args.count < 1 or args.difficulty != 'easy':
        parser.error('Only easy is supported; count must be positive.')
    records, seen = [], set()
    for i in itertools.count():
        if len(records) == args.count:
            break
        if i > max(1000, args.count * 100):
            raise RuntimeError('Bounded sampler exhausted; remaining shortage is explicit')
        rec = generate('easy', args.seed + i, args.template, profile=args.profile)
        fp = rec['generation']['parameter_fingerprint']
        if fp not in seen:
            seen.add(fp)
            records.append(rec)
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(map(markdown, records)))


if __name__ == '__main__':
    main()
