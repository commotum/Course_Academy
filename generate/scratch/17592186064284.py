#!/usr/bin/env python3
"""Hard tangent-line replenishment for a composition of trigonometric functions.

Observed hard source q-48644 has no answer field. The blank RHS below is an
explicit authored field extension. Outer coefficients and inner phase shifts
extend that source; moderate banks are classified but outside this generator's
scope. Easy has no certified template. There are 54 distinct (a, phase) pairs;
seeds never establish distinctness. See the adjacent package for validation.
"""
import argparse
import hashlib
import json
import random
import uuid
import sympy as sp

KP_ID = 17592186064284
KP_UUID = 'a483e892-90f2-51f4-80cd-2b1200cd0c37'
TITLE = 'Differentiating a Composition of Trigonometric Functions Using the Chain Rule'
VERSION = 'trig-composition-tangent-v1'
GENERATOR_ID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
PHASES = ('0', '1/6', '1/4', '1/3', '2/3', '3/4')
SUPPORTED_DIFFICULTIES = ('hard',)

def uid(s):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), s))

def latex(v):
    return sp.latex(v)

def generate(difficulty='hard', seed=0, template=None, parameters=None):
    if difficulty != 'hard':
        raise ValueError('Only hard tangent-line questions are certified by this package')
    if template not in (None, 'phase-shifted-tangent'):
        raise ValueError('Unknown template')
    rng = random.Random(seed)
    p = dict(parameters) if parameters is not None else {'a': rng.randrange(1, 10), 'phase': rng.choice(PHASES)}
    if set(p) != {'a', 'phase'} or type(p['a']) is not int or p['a'] not in range(1, 10) or p['phase'] not in PHASES:
        raise ValueError('a must be an integer 1..9 and phase an allowed rational multiple of pi')
    a = sp.Integer(p['a']); b = sp.Rational(p['phase']) * sp.pi
    x = sp.Symbol('x', real=True)
    # Exact mathematics precedes presentation. All curves are smooth on R.
    curve = a * sp.cos(sp.sin(x) + b, evaluate=False)
    derivative = -a * sp.sin(sp.sin(x) + b) * sp.cos(x)
    height = sp.simplify(a * sp.cos(b))
    slope = sp.simplify(-a * sp.sin(b))
    rhs = sp.expand(slope * x + height)
    assert sp.trigsimp(sp.diff(curve, x) - derivative) == 0
    identity = hashlib.sha256(json.dumps({'kp': KP_UUID, 'task': 'tangent', 'a': int(a), 'phase': p['phase'], 'point_x': 0}, sort_keys=True).encode()).hexdigest()
    qid = uid('question/' + identity); fid = uid('field/' + identity + '/field-1')
    value = latex(rhs); aid = str(uuid.uuid5(uuid.UUID(fid), 'math/' + value))
    prompt = (f'Find the equation of the tangent to the curve $y={latex(curve)}$ '
              f'at the point $\\left(0,{latex(height)}\\right)$.\n\n'
              'Write the right-hand side of the equation in terms of $x$.\n\n$y=$ {{field-1}}')
    inner = sp.sin(x) + b
    coefficient = '' if a == 1 else str(a)
    solution = ('First, the slope of $y=f(x)$ at $x=0$ is given by $f\'(0)$.\n\n'
                'We calculate $f\'(x)$ using the chain rule. First, express $f(x)$ as the composite function\n\n'
                f'$$f={coefficient}\\cos u,\\qquad u={latex(inner)}.$$\n\n'
                'Differentiating gives\n\n'
                f'$$\\frac{{\\mathrm{{d}}f}}{{\\mathrm{{d}}u}}=-{coefficient}\\sin u,\\qquad '
                '\\frac{\\mathrm{d}u}{\\mathrm{d}x}=\\cos x.$$\n\n'
                'We now apply the chain rule:\n\n'
                f'$$f\'(x)=\\frac{{\\mathrm{{d}}f}}{{\\mathrm{{d}}u}}\\cdot '
                f'\\frac{{\\mathrm{{d}}u}}{{\\mathrm{{d}}x}}=-{coefficient}\\sin({latex(inner)})\\cos x.$$\n\n'
                f'Evaluating at $x=0$ gives $f\'(0)=-{coefficient}\\sin({latex(b)})={latex(slope)}$.\n\n'
                'Finally, use the point-slope equation:\n\n'
                f'$$y-\\left({latex(height)}\\right)=\\left({latex(slope)}\\right)(x-0),\\qquad y={value}.$$')
    field = {':answer-field/id': fid, ':answer-field/key': 'field-1', ':answer-field/type': ':answer-field.type/blank',
             ':answer-field/choices': [{':answer/id': aid, ':answer/type': ':answer.type/math', ':answer/value': value}],
             ':answer-field/correct': [':answer/id', aid]}
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
            'question': {':question/id': qid, ':question/difficulty': ':question.difficulty/hard', ':question/problem': prompt,
                         ':question/worked-solution': solution, ':question/answer-fields': [field]},
            'generation': {'version': VERSION, 'generator_id': GENERATOR_ID, 'seed': seed, 'template': 'phase-shifted-tangent',
                           'parameters': p, 'domain': 'x real; coefficient a is an integer 1..9; phase is an enumerated rational multiple of pi',
                           'source_ids': ['q-48644'], 'bank_profile': None, 'origin': 'authored hard source extension; source field missing',
                           'mathematical_fingerprint': identity, 'dependencies': {'sympy': sp.__version__}, 'plots': []}}

def generate_hard(seed=0, template=None, parameters=None):
    return generate('hard', seed, template, parameters)

def markdown(r):
    q = r['question']; f = q[':question/answer-fields'][0]
    return q[':question/problem'] + '\n\nAnswer: $' + f[':answer-field/choices'][0][':answer/value'] + '$\n\n' + q[':question/worked-solution']

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty', choices=['easy', 'moderate', 'hard', 'all'], default='hard')
    ap.add_argument('--seed', type=int, default=0); ap.add_argument('--count', type=int, default=1)
    ap.add_argument('--template', default='phase-shifted-tangent')
    ap.add_argument('--format', choices=['json', 'markdown'], default='json')
    args = ap.parse_args()
    if args.difficulty not in ('hard', 'all') or not 1 <= args.count <= 54:
        ap.error('hard only; count must be 1..54 (finite capability)')
    pairs = [{'a': a, 'phase': phase} for a in range(1, 10) for phase in PHASES]
    random.Random(args.seed).shuffle(pairs)
    records = [generate_hard(args.seed, args.template, p) for p in pairs[:args.count]]
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(map(markdown, records)))

if __name__ == '__main__':
    main()
