"""Controlled substitution models for the three remaining topic478 KPs.

New records are authored exact-entry exercises, not transported source banks.
Every answer is rendered once and used verbatim as the solution's final result.
The immutable packages bundle this helper, formatting, and their scope evidence.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import uuid

import sympy as s

from trig_format import normalize_prose, normalize_tex

X, U = s.symbols('x u', real=True)
R, PI = s.Rational, s.pi
VERSION = '3.0.0-substitution-models'
TRIG = ('sin', 'cos', 'sec2', 'csc2', 'sec_tan', 'csc_cot')
RECIP = TRIG[2:]
CASE = {
    17592186068916: {band: RECIP for band in ('easy', 'moderate', 'hard')},
    17592186068917: {
        'easy': TRIG,
        'moderate': TRIG + ('sqrt_cos', 'sqrt_sin'),
        'hard': TRIG + ('reciprocal_sec2', 'reciprocal_sin'),
    },
    17592186068918: {
        'easy': ('sin', 'cos', 'shift_sin', 'shift_cos'),
        'moderate': ('sin2', 'cos2', 'cos3', 'tan', 'sec', 'csc', 'cot2', 'tan2'),
        'hard': ('sin2', 'cos3', 'sec', 'csc', 'cot2', 'tan2', 'nested_tan', 'rearranged'),
    },
}


def tex(value):
    return normalize_tex(s.latex(value))


def times(coefficient, expression):
    coefficient = s.sympify(coefficient)
    if coefficient == 1:
        return expression
    if coefficient == -1:
        return '-' + expression
    return tex(coefficient) + r'\left(' + expression + r'\right)'


def g(kind, z):
    fn = lambda name: getattr(s, name)(z, evaluate=False)
    return {'sin': lambda: fn('sin'), 'cos': lambda: fn('cos'),
            'sec2': lambda: fn('sec')**2, 'csc2': lambda: fn('csc')**2,
            'sec_tan': lambda: fn('sec')*fn('tan'),
            'csc_cot': lambda: fn('csc')*fn('cot')}[kind]()


def h(kind, z):
    fn = lambda name: getattr(s, name)(z, evaluate=False)
    return {'sin': lambda: -fn('cos'), 'cos': lambda: fn('sin'),
            'sec2': lambda: fn('tan'), 'csc2': lambda: -fn('cot'),
            'sec_tan': lambda: fn('sec'), 'csc_cot': lambda: -fn('csc')}[kind]()


def logabs(z):
    return r'\ln\left|' + tex(z) + r'\right|'


def integral(body, var='x', lo=None, hi=None):
    limits = '' if lo is None else '_{' + tex(lo) + '}^{' + tex(hi) + '}'
    return r'\int' + limits + ' ' + body + r'\,\mathrm{d}' + var


def task_key(body, lo=None, hi=None):
    return hashlib.sha256(json.dumps([s.srepr(s.trigsimp(body)),
        None if lo is None else s.srepr(s.simplify(lo)),
        None if hi is None else s.srepr(s.simplify(hi))]).encode()).hexdigest()


def endpoints(kind, band, rng):
    if kind in ('csc2', 'csc_cot'):
        pairs = ((PI/6, PI/4), (PI/4, PI/3), (PI/6, PI/3))
        if band == 'moderate':
            pairs += ((PI/4, PI/2), (PI/3, PI/2))
    else:
        pairs = ((PI/6, PI/4), (PI/4, PI/3), (0, PI/3), (0, PI/4))
        if band == 'hard':
            pairs = pairs[:2]  # two nonzero, different endpoint contributions
    return rng.choice(pairs)


def reciprocal(band, case, rng, index):
    a = rng.choice((2, 3, 4, 5, 6))
    b = rng.choice((0, PI/6, -PI/4)) if band == 'easy' else s.Integer(0)
    A = s.Integer(rng.randint(1, 7))
    if band == 'hard':
        a = rng.choice((R(1, 2), R(1, 3), R(2, 3), R(3, 2)))
        b = rng.choice((PI/6, -PI/6, PI/4, -PI/4))
        A = rng.choice((R(2, 3), R(3, 2), R(5, 3), R(5, 2)))
    A *= rng.choice((-1, 1))
    # Sign is scheduled independently of family; each family sees both signs.
    a = s.sympify(a) * (-1 if index % 2 else 1)
    inner = a*X+b
    r = s.cancel(A/a)
    lo = hi = None
    if band != 'easy':
        left, right = endpoints(case, band, rng)
        u0, u1 = (right, left) if a < 0 else (left, right)
        lo, hi = s.simplify((u0-b)/a), s.simplify((u1-b)/a)
    return dict(kind=case, inner=inner, du=s.diff(inner, X), factor=r,
        body=A*g(case, inner), transformed=g(case, U), primitive_u=r*h(case, U),
        primitive=r*h(case, inner), lo=lo, hi=hi,
        slots={'a': str(a), 'b': str(b), 'A': str(A)},
        support=['q-10143', 'q-2203', 'q-13663', 'q-350053', 'q-350055', 'q-13524', 'q-346368', 'q-350060'])


def products(band, case, rng, index):
    root = case.startswith('sqrt_')
    inverse = case.startswith('reciprocal_')
    kind = case.split('_', 1)[1] if root or inverse else case
    a = s.Integer(rng.randint(2, 5))
    n = rng.choice((2, 3))
    b = rng.choice((-PI/6, -PI/4)) if band == 'hard' and not inverse else (
        rng.choice((0, PI/6, -PI/6)) if band == 'moderate' else s.Integer(0))
    sign = -1 if index % 2 else 1
    if root:
        inner = a*s.sqrt(X)+b
        A = sign*s.Integer(rng.randint(1, 5))
        outer = A/s.sqrt(X)
    elif inverse:
        inner = a/X+b
        A = sign*s.Integer(rng.randint(1, 5))
        outer = A/X**2
    else:
        if band == 'easy':
            a = s.Integer(rng.randint(1, 4))
            A = sign*a*n*rng.choice((1, 2, 3))
        else:
            A = sign*s.Integer(rng.randint(1, 9))
            if A % (a*n) == 0:
                A += sign
        inner = a*X**n+b
        outer = A*X**(n-1)
    du = s.diff(inner, X)
    r = s.cancel(outer/du)
    assert not r.has(X)
    lo = hi = None
    if band == 'hard' and not inverse:
        u0, u1 = endpoints(kind, 'hard', rng)
        lo, hi = s.simplify(((u0-b)/a)**R(1, n)), s.simplify(((u1-b)/a)**R(1, n))
    return dict(kind=kind, inner=inner, du=du, factor=r,
        body=outer*g(kind, inner), transformed=g(kind, U), primitive_u=r*h(kind, U),
        primitive=r*h(kind, inner), lo=lo, hi=hi,
        slots={'a': str(a), 'b': str(b), 'A': str(A), 'power': n, 'inner_role': 'sqrt' if root else 'reciprocal' if inverse else 'power'},
        support=['q-13461', 'q-13474', 'q-13464', 'q-13471', 'q-13460', 'q-13467', 'q-13470', 'q-2377', 'q-3038', 'q-13544', 'q-350883', 'q-350203'])


def quotients(band, case, rng, index):
    a = s.Integer(rng.randint(2, 5))
    b = rng.choice((PI/6, -PI/6)) if case.startswith('shift_') else s.Integer(0)
    theta = a*X**2 if case == 'nested_tan' else a*X+b
    d, e = s.Integer(rng.randint(2, 5)), s.Integer(rng.randint(1, 4))
    if band == 'easy':
        kind = case.removeprefix('shift_')
        inner = getattr(s, kind)(theta, evaluate=False)
    elif case == 'rearranged':
        inner = s.tan(theta, evaluate=False)+d
        kind = 'tan'
    else:
        kind = 'tan' if case == 'nested_tan' else case.rstrip('23')
        power = 3 if case == 'cos3' else 2 if case.endswith('2') else 1
        inner = d+e*getattr(s, kind)(theta, evaluate=False)**power
    # Render familiar derivative rules directly. SymPy's tan derivative normal
    # form (1+tan^2) would add an unnecessary trig-identity conversion.
    rearranged = case == 'rearranged'
    fn = getattr(s, kind)(theta, evaluate=False)
    derivative_fn = {
        'sin': s.cos(theta, evaluate=False), 'cos': -s.sin(theta, evaluate=False),
        'tan': s.sec(theta, evaluate=False)**2,
        'sec': s.sec(theta, evaluate=False)*s.tan(theta, evaluate=False),
        'csc': -s.csc(theta, evaluate=False)*s.cot(theta, evaluate=False),
        'cot': -s.csc(theta, evaluate=False)**2,
    }[kind]
    du = s.diff(theta, X)*derivative_fn
    if band != 'easy' and not rearranged:
        du *= e*power*fn**(power-1)
    # Choose a small displayed numerator coefficient, then derive the matching
    # factor. Choosing the factor first creates gratuitous nested fractions and
    # coefficients such as 160/3 in otherwise elementary f-prime/f questions.
    scale = a if band == 'easy' or rearranged else a*e*(2 if case == 'nested_tan' else power)
    choices = [s.Integer(n) for n in range(1,10) if band == 'easy' or n % scale != 0]
    A = rng.choice(choices) * (-1 if index % 2 else 1)
    r = s.cancel(A/scale)
    transformed = 1-d/U if rearranged else 1/U
    # The rational rearrangement is a separate supported reasoning case.
    body = r*du*(1-d/inner) if rearranged else r*du/inner
    if rearranged:
        body = r*a*s.sec(theta, evaluate=False)**2*s.tan(theta, evaluate=False)/inner
    lo = hi = None
    if band == 'hard' and not rearranged:
        pairs = {
            'sin': ((0, PI/2), (PI/6, PI/2), (0, PI/6)),
            'cos': ((0, PI/3), (PI/3, PI/2), (0, PI/2)),
            'sec': ((0, PI/3), (0, PI/4), (PI/4, PI/3)),
            'csc': ((PI/6, PI/2), (PI/6, PI/4), (PI/4, PI/2)),
            'cot': ((PI/4, PI/2), (PI/6, PI/4), (PI/3, PI/2)),
            'tan': ((0, PI/4), (PI/6, PI/4), (0, PI/6)),
        }
        t0, t1 = rng.choice(pairs[kind])
        if case == 'nested_tan':
            lo, hi = s.sqrt(t0/a), s.sqrt(t1/a)
        else:
            lo, hi = s.simplify((t0-b)/a), s.simplify((t1-b)/a)
    primitive_u = r*(U-d*s.log(U)) if rearranged else r*s.log(U)
    primitive = primitive_u.subs(U, inner)
    # Preserve numerator and denominator as sampled, even if cancellation or a
    # trig identity would yield a different-looking integrand.
    numerator = r*a*s.sec(theta, evaluate=False)**2*s.tan(theta, evaluate=False) if rearranged else r*du
    return dict(kind=case, inner=inner, du=du, factor=r, body=body,
        body_tex=r'\frac{' + tex(numerator) + '}{' + tex(inner) + '}',
        transformed=transformed, primitive_u=primitive_u, primitive=primitive, lo=lo, hi=hi,
        rearranged=rearranged, d=d, theta=theta,
        slots={'a': str(a), 'b': str(b), 'offset': str(d), 'scale': str(e), 'numerator_coefficient': str(A), 'factor': str(r), 'inner_role': 'quadratic' if case == 'nested_tan' else 'affine'},
        support=['q-49557', 'q-113998', 'q-350887', 'q-350901', 'q-350904', 'q-350908', 'q-350892', 'q-113987', 'q-114004', 'q-73679', 'q-113997'])


def render(kp, band, case, instance, seed, evidence):
    m = instance
    inner, du, r, lo, hi = (m[k] for k in ('inner', 'du', 'factor', 'lo', 'hi'))
    definite = lo is not None
    body = m.get('body_tex', tex(m['body']))
    task = integral(body, lo=lo, hi=hi)
    quotient = kp == 17592186068918
    sol = 'Let $u=' + tex(inner) + '$. Then\n\n$$\n' + r'\frac{\mathrm{d}u}{\mathrm{d}x}=' + tex(du) + '.\n$$\n\n'
    if du.could_extract_minus_sign():
        sol += 'The negative derivative is included in the factor outside the new integral.\n\n'
    if definite:
        u0, u1 = (s.simplify(inner.subs(X, value)) for value in (lo, hi))
        sol += 'Change both bounds:\n\n$$\n' + r'\begin{aligned}x=' + tex(lo) + r'&\Longrightarrow u=' + tex(u0) + r'\\x=' + tex(hi) + r'&\Longrightarrow u=' + tex(u1) + r'\end{aligned}' + '\n$$\n\n'
        if u0 > u1:
            sol += 'The transformed bounds decrease; keep their order when subtracting endpoint values.\n\n'
    if m.get('rearranged'):
        d = m['d']
        sol += 'Since $' + tex(s.tan(m['theta'], evaluate=False)) + '=u-' + tex(d) + '$, the remaining quotient is\n\n$$\n' + r'\frac{u-' + tex(d) + r'}{u}=1-\frac{' + tex(d) + '}{u}.\n$$\n\n'
    transformed = integral(tex(m['transformed']), 'u', u0 if definite else None, u1 if definite else None)
    sol += 'Substituting, including the required constant factor, gives\n\n$$\n' + r'\begin{aligned}&' + task + r'\\&=' + times(r, transformed) + r'.\end{aligned}' + '\n$$\n\n'
    if quotient:
        if m.get('rearranged'):
            primitive_u_tex = times(r, 'u-' + times(m['d'], logabs(U)))
            answer_tex = times(r, tex(inner) + '-' + times(m['d'], logabs(inner))) + '+C'
        else:
            primitive_u_tex = times(r, logabs(U))
            answer_tex = times(r, logabs(inner)) + '+C'
    else:
        primitive_u_tex = tex(m['primitive_u'])
        answer_tex = tex(m['primitive']) + '+C'
    if not definite:
        sol += 'Integrate with respect to $u$:\n\n$$\n' + times(r, integral(tex(m['transformed']), 'u')) + '=' + primitive_u_tex + '+C.\n$$\n\n'
        sol += 'Substitute back:\n\n$$\n' + answer_tex + '.\n$$'
        answer = m['primitive']
    elif quotient:
        assert u0 > 0 and u1 > 0
        ratio = s.cancel(u1/u0)
        answer_tex = times(r, r'\ln\left(' + tex(ratio) + r'\right)')
        answer = r*s.log(ratio)
        sol += 'Both new bounds are positive, so absolute values may be omitted. Evaluate:\n\n$$\n' + times(r, r'\left[\ln u\right]_{' + tex(u0) + '}^{' + tex(u1) + '}') + '=' + times(r, r'\ln\left(' + tex(u1) + r'\right)-\ln\left(' + tex(u0) + r'\right)') + '.\n$$\n\n'
        sol += r'Using $\ln A-\ln B=\ln(A/B)$ gives' + '\n\n$$\n' + answer_tex + '.\n$$'
    else:
        first, last = (s.simplify(m['primitive_u'].subs(U, value)) for value in (u0, u1))
        answer = s.simplify(last-first)
        answer_tex = tex(answer)
        sol += 'Integrate and evaluate at both bounds:\n\n$$\n' + r'\left[' + primitive_u_tex + r'\right]_{' + tex(u0) + '}^{' + tex(u1) + '}=' + r'\left(' + tex(last) + r'\right)-\left(' + tex(first) + r'\right).' + '\n$$\n\n'
        sol += 'Simplifying gives\n\n$$\n' + answer_tex + '.\n$$'
    # An exact-entry answer is authored from this derivation, not scaled from
    # a second source bank. There is one canonical answer, hence no alias collision.
    problem = ('Evaluate exactly.' if definite else 'Find an antiderivative.') + '\n\n$$\n' + task + '\n$$\n\n{{field-1}}'
    if not definite:
        # The existing learner grader recognizes this external +C contract and
        # accepts numeric constant shifts, including a constant absorbed after
        # back-substitution. Asking for the whole F+C expression uses ordinary
        # equality and would unfairly reject some valid antiderivative families.
        problem += ' $+C$'
        assert answer_tex.endswith('+C')
        answer_tex = answer_tex[:-2]
    fp = task_key(m['body'], lo, hi)
    uid = lambda role: str(uuid.uuid5(uuid.UUID(evidence['kp']['id']), VERSION + ':' + fp + ':' + role))
    aid = uid('answer')
    q = {':question/id': uid('question'), ':question/problem': normalize_prose(problem),
         ':question/worked-solution': normalize_prose(sol), ':question/difficulty': ':question.difficulty/'+band,
         ':question/answer-fields': [{':answer-field/id': uid('field'), ':answer-field/key': 'field-1',
             ':answer-field/type': ':answer-field.type/blank',
             ':answer-field/choices': [{':answer/id': aid, ':answer/type': ':answer.type/math', ':answer/value': normalize_tex(answer_tex)}],
             ':answer-field/correct': [':answer/id', aid]}]}
    return {'knowledge_point': evidence['kp'], 'question': q, 'generation': {
        'version': VERSION, 'seed': seed, 'template': case, 'family': case,
        'parameters': m['slots'], 'mathematical_fingerprint': fp,
        'source_questions': m['support'], 'source_basis': evidence['basis'],
        'band_origin': evidence['band_origin'][band], 'batch_contract': 'trig-substitution-v3',
        'response_policy': 'Authored exact-entry extension; no transported distractor bank or source-fidelity claim',
        'domain': 'Connected real intervals avoiding trig poles and denominator zeros; x>0 for square roots; x!=0 for reciprocals. All definite intervals lie in a single safe component.',
        'model': {key: str(value) if value is not None else None for key, value in
                  dict(integrand=m['body'], substitution=inner, derivative=du, transformed=m['transformed'],
                       factor=r, primitive=m['primitive'], lower=lo, upper=hi, result=answer).items()},
        'dependencies': {'sympy': s.__version__}}}


def generate(kp, band, seed=0, template=None, *, evidence, index=0, attempt=0):
    if band not in CASE[kp]:
        raise ValueError('Unsupported difficulty')
    cases = CASE[kp][band]
    if template is not None and template not in cases:
        raise ValueError('Unsupported template for this difficulty')
    case = template or cases[index % len(cases)]
    rng = random.Random(f'{seed}:{kp}:{band}:{case}:{index}:{attempt}')
    builder = {17592186068916: reciprocal, 17592186068917: products, 17592186068918: quotients}[kp]
    instance = builder(band, case, rng, index // len(cases))
    return render(kp, band, case, instance, seed, evidence)


def batch(kp, band, count=8, seed=0, *, evidence, template=None):
    if type(count) is not int or not 1 <= count <= 200:
        raise ValueError('Count must be an integer from 1 through 200')
    if band not in CASE[kp]:
        raise ValueError('Unsupported difficulty')
    seen = set(evidence['excluded_tasks'])
    shapes = set()
    records = []
    order = list(CASE[kp][band])
    random.Random(f'{seed}:{kp}:{band}:families').shuffle(order)
    for index in range(count):
        for attempt in range(300):
            record = generate(kp, band, seed, template or order[index % len(order)], evidence=evidence,
                              index=index + (len(order) if seed % 2 else 0), attempt=attempt)
            m = record['generation']
            if m['mathematical_fingerprint'] in seen:
                continue
            shape = (m['family'], m['model']['substitution'], m['model']['lower'], m['model']['upper'])
            if shape in shapes:
                continue  # a changed amplitude alone is not fresh practice
            # Zero definite outcomes do not pad this practice pool.
            if m['model']['lower'] is not None and s.sympify(m['model']['result']) == 0:
                continue
            seen.add(m['mathematical_fingerprint'])
            shapes.add(shape)
            records.append(record)
            break
        else:
            raise ValueError('Insufficient distinct tasks; no duplicate padding')
    return records


def cli(kp, folder):
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', required=True, choices=('easy', 'moderate', 'hard'))
    parser.add_argument('--count', type=int, default=8)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--template')
    parser.add_argument('--format', choices=('json', 'markdown'), default='json')
    args = parser.parse_args()
    evidence = json.loads((Path(folder)/'source-evidence.json').read_text())
    records = batch(kp, args.difficulty, args.count, args.seed, evidence=evidence, template=args.template)
    if args.format == 'json':
        print(json.dumps(records, indent=2))
    else:
        print('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
