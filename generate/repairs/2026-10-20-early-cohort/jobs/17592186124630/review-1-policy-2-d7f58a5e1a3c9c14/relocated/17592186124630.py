#!/usr/bin/env python3
"""Seeded finite recognition generator for parts of the invertible matrix theorem."""
import argparse
import hashlib
import json
import random
import uuid
from pathlib import Path
from math_format import checked_math_content, normalize_prose, normalize_tex

KP = 17592186124630
VERSION = '2.0.0'
SOURCE = json.loads(Path(__file__).with_name('source-data.json').read_text())
KP_UUID = SOURCE[':knowledge-point/id']
SOURCES = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions']}

# Exact source target assignments. Normal generation also supports the canonical dimension target.
TARGETS = {
    'q-140766': 'null-space-rhs', 'q-142468': 'null-space-rhs',
    'q-141344': 'invertibility-adjective',
    'q-141191': 'null-dimension-value', 'q-142471': 'null-dimension-value',
    'q-141348': 'column-space-lhs', 'q-141194': 'rank-rhs',
}
TARGETS.update({
    'q-141343': 'column-dimension-lhs', 'q-141192': 'column-dimension-value',
    'q-142302': 'invertibility-adjective', 'q-142357': 'column-space-lhs',
    'q-141345': 'null-space-lhs', 'q-141193': 'column-space-rhs',
    'q-141195': 'nullity-rhs', 'q-141346': 'null-space-rhs',
    'q-141347': 'null-dimension-value',
})
EXCLUDED = {
    'q-141343': 'Two dimension expressions equal n; source replay only.',
    'q-141192': 'TeX grouping duplicates n and 1; source replay only.',
    'q-142357': 'Three column-space choices equal R^n; source replay only.',
    'q-141345': 'Two null-space choices equal the zero subspace; source replay only.',
}
UNSUPPORTED = {
    'moderate': 'No observed or validated same-method Moderate backbone; recognition has no arithmetic parameter.',
    'hard': 'No observed or validated same-method Hard backbone; computations or proofs would change the assessed method.',
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), value))


def replay(source_id):
    """Exact source replay, with independent field-owned draft identities."""
    q = SOURCES[source_id]
    fid = uid('field:' + source_id)
    fields = []
    for f in q[':question/answer-fields']:
        choices = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), a[':answer/value'])),
                    ':answer/type': str(a[':answer/type'][':db/ident']),
                    ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']]
        correct = f[':answer-field/correct'][':answer/value']
        fields.append({':answer-field/id': fid, ':answer-field/key': f[':answer-field/key'],
                       ':answer-field/type': str(f[':answer-field/type'][':db/ident']),
                       ':answer-field/choices': choices,
                       ':answer-field/correct': [':answer/id', next(a[':answer/id'] for a in choices if a[':answer/value'] == correct)]})
    question = {':question/id': uid('question:' + source_id),
                ':question/problem': q[':question/problem'],
                ':question/worked-solution': q[':question/worked-solution'],
                ':question/difficulty': ':question.difficulty/easy',
                ':question/answer-fields': fields}
    return {'knowledge_point': {'id': KP, 'title': SOURCE[':knowledge-point/title']},
            'question': question,
            'generation': {'version': VERSION, 'template': TARGETS.get(source_id, 'excluded-source'),
                           'bank_profile': source_id, 'source': source_id, 'parameters': {},
                           'domain': 'n is a positive integer; A is a real n by n matrix',
                           'evidence_only': True, 'eligible_for_learning': False,
                           'supported_source': source_id in TARGETS and source_id not in EXCLUDED,
                           'exclusion': EXCLUDED.get(source_id),
                           'semantic_identity': TARGETS.get(source_id),
                           'source_basis': 5436}}



# Positions in the theorem. These are semantic target contracts, not seed variants.
TERMS = {
    'invertibility-adjective': 'invertible',
    'column-space-lhs': r'\operatorname{Col}(A)',
    'column-space-rhs': r'\mathbb{R}^{n}',
    'column-dimension-lhs': r'\dim(\operatorname{Col}(A))',
    'column-dimension-value': 'n',
    'rank-rhs': r'\operatorname{rank}(A)',
    'null-space-lhs': r'\operatorname{Null}(A)',
    'null-space-rhs': r'\{0\}',
    'null-dimension-lhs': r'\dim(\operatorname{Null}(A))',
    'null-dimension-value': '0',
    'nullity-rhs': r'\operatorname{nullity}(A)',
}
BANKS = {
    'adjective': ['invertibility-adjective'],
    'named': [ 'column-space-lhs', 'null-space-lhs', 'rank-rhs', 'nullity-rhs'],
    'dimensions': [ 'column-space-lhs', 'null-space-lhs', 'column-dimension-lhs', 'null-dimension-lhs'],
    'values': [ 'column-space-rhs', 'null-space-rhs', 'column-dimension-value', 'null-dimension-value'],
}
FINITE_CAPACITY = len(TERMS)
BLANK = r'\underline{\phantom{WWWW}}'


def theorem(target=None):
    t = dict(TERMS)
    t['invertibility-adjective'] = r'\text{invertible}'
    if target is not None:
        t[target] = BLANK
    rows = [
        t['column-space-lhs'] + ' &=' + t['column-space-rhs'],
        t['column-dimension-lhs'] + ' &=' + t['column-dimension-value'] + '=' + t['rank-rhs'],
        t['null-space-lhs'] + ' &=' + t['null-space-rhs'],
        t['null-dimension-lhs'] + ' &=' + t['null-dimension-value'] + '=' + t['nullity-rhs'],
    ]
    return ('$$\n\\begin{gathered}A\\text{ is }' + t['invertibility-adjective'] +
            r' \\ \Updownarrow \\ \left\{\begin{aligned}' +
            r' \\ '.join(rows) + r'\end{aligned}\right.\end{gathered}' + '\n$$')


@checked_math_content
def make_record(target, bank_profile, seed=0):
    if target not in BANKS[bank_profile]:
        raise ValueError('Target is not covered by this complete authored bank')
    problem = normalize_prose(theorem(target) +
        '\n\nConsider the equivalence above, where $A$ is a real $n\\times n$ matrix and $n$ is a positive integer. '
        'Which of the following should be placed into the blank space to make a true statement?')
    answer = TERMS[target]
    conclusion = ('"invertible".' if target == 'invertibility-adjective' else '$' + answer + '$.')
    solution = normalize_prose('Recall that the *invertible matrix theorem* states the following:\n\n'
        '*Let $A$ be a real $n\\times n$ matrix. Then we have the following equivalence:*\n\n' +
        theorem() + '\n\nTherefore, the missing expression is ' + conclusion)
    if bank_profile == 'adjective':
        values = [(v, ':answer.type/text') for v in ['invertible', 'not invertible', 'diagonal', 'not identity', 'identity']]
    else:
        values = [(TERMS[t], ':answer.type/math') for t in BANKS[bank_profile]] + [('n+1', ':answer.type/math')]
    values = [(normalize_tex(v) if typ == ':answer.type/math' else v, typ) for v, typ in values]
    identity = digest([problem, sorted(values)])
    fid = uid('field:v2:' + identity)
    choices = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), typ + ':' + v)),
                ':answer/type': typ, ':answer/value': v} for v, typ in values]
    random.Random(seed).shuffle(choices)
    correct = next(a[':answer/id'] for a in choices if a[':answer/value'] == answer)
    refs = sorted(q for q, slot in TARGETS.items() if slot == target)
    if target == 'null-dimension-lhs':
        refs = ['e-9962']
    return {
        'knowledge_point': {'id': KP_UUID, 'db_id': KP, 'title': SOURCE[':knowledge-point/title']},
        'question': {':question/id': uid('question:v2:' + identity),
                     ':question/problem': problem, ':question/worked-solution': solution,
                     ':question/difficulty': ':question.difficulty/easy',
                     ':question/answer-fields': [{':answer-field/id': fid, ':answer-field/key': 'selection',
                         ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
                         ':answer-field/correct': [':answer/id', correct]}]},
        'generation': {'version': VERSION, 'seed': seed, 'template': 'missing-theorem-fragment',
                       'target': target, 'bank_profile': bank_profile, 'source_questions': refs,
                       'source_basis': 5436, 'parameters': {'target': target, 'bank_profile': bank_profile},
                       'domain': 'real n by n matrix; integer n >= 1',
                       'semantic_identity': target, 'finite_semantic_capacity': FINITE_CAPACITY,
                       'bank_origin': 'authored same-method extension',
                       'eligible_for_learning': True, 'evidence_only': False},
    }


def generate(difficulty='easy', count=5, seed=0):
    if difficulty != 'easy':
        raise ValueError(UNSUPPORTED.get(difficulty, 'Unsupported difficulty: ' + str(difficulty)))
    if count < 0:
        raise ValueError('count must be nonnegative')
    if count > FINITE_CAPACITY:
        raise ValueError(f'Finite limit: {FINITE_CAPACITY} distinct target contracts; requested {count}')
    rng = random.Random(seed)
    targets = rng.sample(sorted(TERMS), count)
    return [make_record(target, rng.choice([p for p, slots in BANKS.items() if target in slots]),
                        rng.getrandbits(64)) for target in targets]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=['easy', 'moderate', 'hard'], default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    parser.add_argument('--replay', choices=sorted(SOURCES))
    args = parser.parse_args()
    try:
        result = replay(args.replay) if args.replay else generate(args.difficulty, args.count, args.seed)
    except ValueError as error:
        parser.error(str(error))
    if args.format == 'json':
        print(json.dumps(result, indent=2))
    elif args.replay:
        print(result['question'][':question/problem'] + '\n\n' + result['question'][':question/worked-solution'])
    else:
        print('\n\n'.join(r['question'][':question/problem'] for r in result))


if __name__ == '__main__':
    main()
