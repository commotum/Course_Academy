#!/usr/bin/env python3
"""Finite, source-backed recognition generator; no seed-only replenishment.

There are no numerical parameters in these theorem-recognition prompts. Each
supported target is already represented in the captured practice pool. Replay
is evidence-only; ordinary execution never republishes a captured task.
"""
import argparse
import copy
import hashlib
import json
import random
import uuid
from pathlib import Path

HERE = Path(__file__).with_suffix('')
KP = 17592186124630
VERSION = '1.0.0'
SOURCE = json.loads((HERE / 'reference/initial/kp.json').read_text())
KP_UUID = SOURCE[':knowledge-point/id']
SOURCES = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions']}

# Easy: five target/answer contracts, seven complete observed bank profiles.
# Left-hand objects and right-hand values remain separate templates.
TARGETS = {
    'q-140766': 'null-space-rhs', 'q-142468': 'null-space-rhs',
    'q-141344': 'invertibility-adjective',
    'q-141191': 'null-dimension-value', 'q-142471': 'null-dimension-value',
    'q-141348': 'column-space-lhs', 'q-141194': 'rank-rhs',
}
EXCLUDED = {
    'q-141343': 'Missing visible blank; dim(Col(A^-1)) and dim(Col(A)) both equal n.',
    'q-141192': 'Missing visible blank; n and {n} are identical scalar TeX values; 1 and {1} also duplicate.',
    'q-142302': 'Missing visible blank; same adjective task already represented by q-141344.',
    'q-142357': 'Col(A), Col(A^-1), and Col(A^n) all equal R^n for invertible A and positive integer n.',
    'q-141345': 'Null(A) and Null(A^-1) both equal the zero subspace for invertible A.',
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
                           'supported_source': source_id in TARGETS,
                           'exclusion': EXCLUDED.get(source_id),
                           'semantic_identity': TARGETS.get(source_id),
                           'source_basis': 2617}}


def generate(difficulty='easy', count=5, seed=0):
    """Execute the bounded generator, excluding every existing source task.

    A new distractor bank, symbol rename, option shuffle, or source profile does
    not create a new mathematical task. All five supported targets are already
    in the source bank, even if a learner has exhausted them.
    """
    if difficulty not in ('easy', 'moderate', 'hard'):
        raise ValueError('difficulty must be easy, moderate, or hard')
    if count < 0:
        raise ValueError('count must be nonnegative')
    targets = sorted(set(TARGETS.values()))
    random.Random(seed).shuffle(targets)
    existing_targets = set(TARGETS.values())
    fresh = [t for t in targets if t not in existing_targets]
    assert not fresh
    return {'knowledgePoint': KP, 'generator_version': VERSION,
            'outcome': 'unsupported' if difficulty in UNSUPPORTED else 'finite-limit',
            'difficulty': difficulty, 'requested': count, 'produced': 0,
            'instances': [], 'shortage_remaining': count,
            'supported_levels': ['easy'], 'unsupported_levels': UNSUPPORTED,
            'finite_distinct_supported_tasks': len(targets), 'new_distinct_tasks': 0,
            'exception': UNSUPPORTED.get(difficulty, 'All five validated target contracts already exist in source practice; no unoccupied parameter slots remain in this package.'),
            'scope': 'Bounded capability of this source-backed package; new evidence or separately validated extensions may reopen classification.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=['easy', 'moderate', 'hard'], default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json', 'markdown'], default='json')
    parser.add_argument('--replay', choices=sorted(SOURCES))
    args = parser.parse_args()
    result = replay(args.replay) if args.replay else generate(args.difficulty, args.count, args.seed)
    if args.format == 'json':
        print(json.dumps(result, indent=2))
    elif args.replay:
        print(result['question'][':question/problem'] + '\n\n' + result['question'][':question/worked-solution'])
    else:
        print(result['outcome'] + ': ' + result['exception'])


if __name__ == '__main__':
    main()
