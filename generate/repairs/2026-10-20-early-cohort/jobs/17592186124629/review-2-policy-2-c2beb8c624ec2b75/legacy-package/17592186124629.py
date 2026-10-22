"""Finite, source-backed invertible-matrix-theorem sentence generator.

Moderate only. CLI: --difficulty moderate --count 5 --seed 24629.
The three nullity-zero templates permit equivalent *given facts* not already
asked as conclusions. Numeric dimensions, statement order, and bank order are
not sampled to manufacture inventory. Full source banks and layouts replay.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid

HERE = Path(__file__).with_suffix('')
KP_ID = 17592186124629
KP_UUID = 'bb90e5b9-03fe-51cf-bc16-a293befacebc'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = '1.0.1'
SUPPORTED_LEVELS = ('moderate',)
SOURCE = json.loads((HERE / 'source.json').read_text())
EXCLUDED = {'q-47586': 'Unrated; no key or solution; keyed subset absent from bank.',
            'q-141342': 'Prompt nullity != 0, but three solution conditionals say nullity = 0.'}
CASES = {q[':question/math-academy-id']: q for q in SOURCE[':knowledge-point/questions']
         if q[':question/math-academy-id'] not in EXCLUDED}
ORIGINAL = r'\text{nullity}(A)=0'
# All these are equivalent for real square matrices; no numerical work is added.
PREMISES = {'nullity-zero': ORIGINAL, 'nonzero-determinant': r'det(A)\ne 0',
            'full-rank': r'\text{rank}(A)=n', 'trivial-null-space': r'\text{Null}(A)=\{0\}',
            'full-column-space': r'\text{Col}(A)={R}^{n}',
            'full-column-dimension': r'\text{dim(Col}(A))=n'}
DEFAULTS = {sid: {'premise': 'nullity-zero' if ORIGINAL in q[':question/problem'] else 'source'}
            for sid, q in CASES.items()}

def domain(sid):
    q = CASES[sid]
    if DEFAULTS[sid]['premise'] == 'source':
        return [DEFAULTS[sid]]
    # Giving the exact conclusion would reduce a theorem question to copying.
    tail = q[':question/problem'].split('Which of the following')[1]
    concepts = {'nonzero-determinant': 'det(A)', 'full-rank': r'\text{rank}(A)',
                'trivial-null-space': r'\text{Null}(A)',
                'full-column-space': r'\text{Col}(A)',
                'full-column-dimension': r'\text{dim(Col}(A))'}
    return [{'premise': p} for p in PREMISES if p not in concepts or concepts[p] not in tail]

def fingerprint(q):
    # The entire assessed sentence and propositions determine identity, ignoring
    # response type, banks, keys, seed and identities. No option-order variants.
    return hashlib.sha256(q[':question/problem'].replace('Select all that apply.', '').strip().encode()).hexdigest()

def generate(difficulty='moderate', seed=0, template=None, parameters=None):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty; only observed moderate method validated')
    rng = random.Random(seed)
    sid = template or rng.choice(sorted(CASES))
    p = parameters or rng.choice(domain(sid))
    if p not in domain(sid):
        raise ValueError('Outside validated finite premise domain')
    old = CASES[sid]
    prompt, solution = old[':question/problem'], old[':question/worked-solution']
    if p['premise'] not in ('source', 'nullity-zero'):
        premise = PREMISES[p['premise']]
        prompt = prompt.replace(ORIGINAL, premise)
        solution = solution.replace(ORIGINAL, premise)
    q = {':question/problem': prompt, ':question/worked-solution': solution,
         ':question/difficulty': ':question.difficulty/moderate'}
    identity = uuid.uuid5(uuid.UUID(GENERATOR_UUID), fingerprint(q))
    q[':question/id'] = str(identity)
    q[':question/answer-fields'] = []
    for f in sorted(old[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        fid = uuid.uuid5(identity, 'field:' + f[':answer-field/key'])
        choices = [{':answer/id': str(uuid.uuid5(fid, a[':answer/value'])),
                    ':answer/type': a[':answer/type'][':db/ident'], ':answer/value': a[':answer/value']}
                   for a in sorted(f[':answer-field/choices'], key=lambda a: a[':answer/value'])]
        correct = next(a[':answer/id'] for a in choices if a[':answer/value'] == f[':answer-field/correct'][':answer/value'])
        q[':question/answer-fields'].append({':answer-field/id': str(fid), ':answer-field/key': f[':answer-field/key'],
            ':answer-field/type': f[':answer-field/type'][':db/ident'], ':answer-field/choices': choices,
            ':answer-field/correct': [':answer/id', correct]})
    return {'question': q, 'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': SOURCE[':knowledge-point/title']},
            'generation': {'generator_id': GENERATOR_UUID, 'version': VERSION, 'seed': seed,
                           'template': sid, 'profile': sid, 'parameters': p,
                           'mathematical_fingerprint': fingerprint(q), 'domain': 'real square matrices, positive integer n',
                           'source_basis': 2657, 'plots': 'none'}}

def batch(difficulty='moderate', count=5, seed=0):
    if difficulty not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty')
    rows = [generate(difficulty, seed, sid, p) for sid in sorted(CASES) for p in domain(sid)]
    random.Random(seed).shuffle(rows)
    return rows[:count]

def markdown(rec):
    q = rec['question']
    return q[':question/problem'] + '\n\n' + '\n'.join(
        f"{f[':answer-field/key']}: " + ', '.join(a[':answer/value'] for a in f[':answer-field/choices'])
        for f in q[':question/answer-fields']) + '\n\n' + q[':question/worked-solution']


# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--difficulty', default='moderate')
    ap.add_argument('--count', type=int, default=5)
    ap.add_argument('--seed', type=int, default=24629)
    ap.add_argument('--format', choices=('json', 'markdown'), default='json')
    ap.add_argument('--markdown', action='store_true')
    args = ap.parse_args()
    rows = batch(args.difficulty, args.count, args.seed)
    print('\n\n---\n\n'.join(map(markdown, rows)) if args.markdown or args.format == 'markdown' else json.dumps(rows, indent=2))
