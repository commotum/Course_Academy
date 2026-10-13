#!/usr/bin/env python3
"""Bounded source-bank generator for negative integer affine powers.

Easy and moderate retain their source difficulty, coefficient, slope and power.
Only the signed nonzero intercept varies, as documented in the local contract.
Seed, choice order and bank identity never establish mathematical novelty.
"""
import argparse
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as sp

KP_ID = 17592186064204
KP_UUID = '387d85df-b839-5837-89b9-5e4bb4daa073'
TITLE = 'Integrating an Algebraic Function With Negative Integer Exponent'
VERSION = 'negative-integer-affine-v1'
PACKAGE = Path(__file__).with_suffix('')
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
PROFILES = json.loads((PACKAGE / 'contract.json').read_text())['profiles']

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def ident(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), digest(value)))

def affine(a, b):
    if a < 0:
        return str(b) + ('-x' if a == -1 else str(a) + 'x')
    return ('x' if a == 1 else str(a) + 'x') + ('+' if b > 0 else '') + str(b)

def fingerprint(parameters):
    n, a, b, m = parameters
    # Normalize the entire rational integrand, not its spelling or bank.
    x = sp.Symbol('x', real=True)
    return digest(['rational-integrand', sp.srepr(sp.cancel(sp.Rational(n) / (a*x+b)**m))])

def allowed(profile, parameters):
    if len(parameters) != 4 or any(type(v) != int for v in parameters):
        return False
    n, a, b, m = parameters
    pn, pa, pb, pm = profile['parameters']
    lo, hi = profile['bounds']
    return (n, a, m) == (pn, pa, pm) and lo <= b <= hi

def generate(difficulty='easy', seed=0, template=None, parameters=None):
    if difficulty not in ('easy', 'moderate'):
        raise ValueError('Unsupported difficulty; see capabilities.json')
    rng = random.Random(seed)
    eligible = [sid for sid, p in PROFILES.items() if p['level'] == difficulty]
    sid = template if template is not None else rng.choice(eligible)
    if sid not in eligible:
        raise ValueError('Template does not support this difficulty')
    t = PROFILES[sid]
    if parameters is None:
        parameters = list(t['parameters'])
        parameters[2] = rng.randint(*t['bounds'])
    if not allowed(t, parameters):
        raise ValueError('Outside the validated bounded intercept family')
    n, a, b, m = parameters
    # Compute correct mathematical value first, before rendering the source bank.
    x = sp.Symbol('x', real=True)
    primitive = sp.Rational(n, a*(1-m)) * (a*x+b)**(1-m)
    render = lambda mask: mask.replace('@@L@@', affine(a, b))
    values = [render(option['mask']) for option in t['bank']]
    fp = fingerprint(parameters)
    prompt, solution = render(t['prompt']), render(t['solution'])
    qid = ident(['question', VERSION, prompt, solution, sorted(values)])
    fid = ident([qid, 'field', 'selection'])
    choices = [{':answer/id': ident([fid, value]), ':answer/type': ':answer.type/math', ':answer/value': value} for value in values]
    correct = next(i for i, option in enumerate(t['bank']) if option['correct'])
    q = {':question/id': qid, ':question/problem': prompt, ':question/worked-solution': solution,
         ':question/difficulty': ':question.difficulty/' + difficulty,
         ':question/answer-fields': [{':answer-field/id': fid, ':answer-field/key': 'selection',
             ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
             ':answer-field/correct': [':answer/id', choices[correct][':answer/id']]}]}
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE}, 'question': q,
            'generation': {'version': VERSION, 'seed': seed, 'template': sid, 'profile': sid,
                'parameters': parameters, 'source_ids': [sid], 'domain': f'x real; x != {sp.Rational(-b,a)}; one antiderivative family on each connected interval',
                'mathematical_fingerprint': fp, 'primitive': str(primitive), 'sympy': sp.__version__,
                'source_correction': t['source_correction'], 'sampling_policy': t['sampling_policy']}}

def batch(difficulty, count, seed):
    if difficulty not in ('easy', 'moderate') or count < 1:
        raise ValueError('Supported difficulty and positive count required')
    candidates = []
    for sid, t in PROFILES.items():
        if t['level'] == difficulty:
            for b in range(t['bounds'][0], t['bounds'][1]+1):
                p = list(t['parameters']); p[2] = b
                candidates.append((sid, p))
    random.Random(seed).shuffle(candidates)
    records, used = [], set()
    for sid, p in candidates:
        r = generate(difficulty, seed, sid, p)
        fp = r['generation']['mathematical_fingerprint']
        if fp not in used:
            records.append(r); used.add(fp)
        if len(records) == count:
            return records
    raise ValueError(f'Finite family has only {len(records)} distinct integrands; shortage remains explicit')

def markdown(rec):
    q = rec['question']
    return q[':question/problem'] + '\n\n' + '\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']) + '\n\n' + q[':question/worked-solution']

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--difficulty', default='easy'); p.add_argument('--count', type=int, default=1)
    p.add_argument('--seed', type=int, default=0); p.add_argument('--format', choices=['json', 'markdown'], default='json')
    args = p.parse_args(); records = batch(args.difficulty, args.count, args.seed)
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(map(markdown, records)))
