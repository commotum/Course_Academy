#!/usr/bin/env python3
"""Finite, source-backed matrix-identity generator.

Only moderate/hard are supported. Dimension changes are previews, not fresh
mathematical tasks. The complete extracted finite bank is already in EDB;
the default fresh-only CLI therefore emits [] and reports the finite limit.
No statement mixing, new laws, relabeling or shuffling enlarges this bank.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import sys
import uuid

HERE = Path(__file__).with_suffix('')
S = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186115228
KP_UUID = S['record'][':knowledge-point/id']
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = 'matrix-identities-finite-1.0.0'
SOURCES = {q[':question/math-academy-id']: q for q in S['record'][':knowledge-point/questions']}
LEVELS = ('moderate', 'hard')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def fingerprint(q):
    """Ignore dimension, IDs, choice order, and statement order.

    Retain the expression structure: associativity itself is being assessed.
    A second conservative law-family check is documented in classification.
    """
    prompt = q[':question/problem']
    claims = re.findall(r'(?:\*\*(?:III|II|I)\.\*\*|(?<![A-Z])(?:III|II|I)\.)\s*\$([^$]+)\$', prompt)
    if not claims:  # canonical example uses unbulleted statements as well
        raise ValueError('Three explicit mathematical statements required')
    assert len(claims) == 3
    normalized = []
    for claim in claims:
        claim = re.sub(r'\{?I\}?_\{?\d+\}?', 'J', claim)
        claim = re.sub(r'[\s{}]', '', claim).replace(r'\cdot', '')
        normalized.append(claim)
    # Global alpha-renaming also cannot establish novelty.
    import itertools
    candidates = []
    for perm in itertools.permutations('ABC'):
        trans = str.maketrans(dict(zip('ABC', perm)))
        candidates.append(sorted(c.translate(trans) for c in normalized))
    return digest(min(candidates))


def uid(namespace, label):
    return str(uuid.uuid5(uuid.UUID(namespace), label))


def generate(difficulty, seed=0, template=None, parameters=None):
    if difficulty not in LEVELS:
        raise ValueError('Unsupported difficulty; no validated easy backbone')
    rng = random.Random(seed)
    eligible = [t for t, q in SOURCES.items() if q[':question/difficulty'][':db/ident'].endswith('/' + difficulty)]
    template = template or rng.choice(eligible)
    if template not in eligible:
        raise ValueError('Template/difficulty mismatch')
    src = SOURCES[template]
    original_n = int(re.search(r'(\d+)\s*\\times', src[':question/problem'])[1])
    n = (parameters or {}).get('n', original_n)
    if type(n) is not int or not 2 <= n <= 8:
        raise ValueError('Dimension must be an integer from 2 through 8')

    def render(text):
        if n == original_n:
            return text
        text = re.sub(r'\b' + str(original_n) + r'\s*\\times\s*' + str(original_n) + r'\b', lambda _: str(n) + r'\times ' + str(n), text)
        return text.replace('}_{' + str(original_n) + '}', '}_{' + str(n) + '}')

    q = {':question/problem': render(src[':question/problem']), ':question/worked-solution': render(src[':question/worked-solution']), ':question/difficulty': ':question.difficulty/' + difficulty}
    fp = fingerprint(q)
    qid = uid(KP_UUID, 'matrix-identity:' + fp)
    q[':question/id'] = qid
    fields = []
    for f in src[':question/answer-fields']:
        fid = uid(qid, 'field:' + f[':answer-field/key'])
        choices = [{':answer/id': uid(fid, 'answer:' + a[':answer/value']), ':answer/type': a[':answer/type'][':db/ident'], ':answer/value': a[':answer/value']} for a in f[':answer-field/choices']]
        correct = uid(fid, 'answer:' + f[':answer-field/correct'][':answer/value'])
        fields.append({':answer-field/id': fid, ':answer-field/key': f[':answer-field/key'], ':answer-field/type': f[':answer-field/type'][':db/ident'], ':answer-field/choices': choices, ':answer-field/correct': [':answer/id', correct]})
    q[':question/answer-fields'] = fields
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': S['record'][':knowledge-point/title']}, 'question': q,
            'generation': {'version': VERSION, 'seed': seed, 'template': template, 'profile': 'source-' + template,
                           'parameters': {'n': n}, 'domain': 'square matrices of order 2..8 over the real numbers',
                           'source_basis': S['basis'], 'source_question': template, 'mathematical_fingerprint': fp,
                           'fresh': False, 'finite_limit': 'Dimension, seed and identity do not change a universal matrix-law task.'}}


def fresh(difficulty, count, seed=0, excluded=()):
    if difficulty not in LEVELS:
        raise ValueError('Unsupported difficulty: ' + difficulty)
    if count < 0:
        raise ValueError('Nonnegative count required')
    # All templates derive from existing source questions. Never emit them as
    # fresh, even if an external caller omits the source bank from exclusions.
    used = {fingerprint(q) for q in SOURCES.values()} | set(excluded)
    out = []
    for t, q in SOURCES.items():
        if q[':question/difficulty'][':db/ident'].endswith('/' + difficulty):
            rec = generate(difficulty, seed, t)
            if rec['generation']['mathematical_fingerprint'] not in used:
                out.append(rec)
                used.add(rec['generation']['mathematical_fingerprint'])
                if len(out) >= count:
                    break
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', required=True, choices=('easy', 'moderate', 'hard'))
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--template', choices=tuple(SOURCES))
    parser.add_argument('--dimension', type=int)
    parser.add_argument('--preview-existing', action='store_true')
    args = parser.parse_args()
    if args.difficulty not in LEVELS:
        parser.error('easy is unsupported; no validated source-backed easy template')
    if args.preview_existing:
        result = [generate(args.difficulty, args.seed, args.template, {'n': args.dimension} if args.dimension else None)]
    else:
        result = fresh(args.difficulty, args.count, args.seed)
        print('finite-limit: 0 fresh tasks in the extracted source-backed domain; shortage remains explicit', file=sys.stderr)
    print(json.dumps(result, indent=2))



# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__':
    main()
