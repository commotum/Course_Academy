#!/usr/bin/env python3
"""Flux-integrand inventory: scale a complete observed field and choice bank.

The circle/side geometry and outward normal stay fixed for each source profile.
No integration, changed response contract, or new distractor mechanism is added.
The two context-dependent blanks are evidence only, never standalone samples.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import sympy as s
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations, implicit_multiplication_application,
    convert_xor,
)

HERE = Path(__file__).with_suffix('')
SNAPSHOT = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186179645
KP_UUID = 'f9c8ca56-5ea8-547c-80ab-6b1f1347447e'
NS = uuid.UUID(KP_UUID)
GENERATOR_UUID = str(uuid.uuid5(NS, 'flux-integrand-generator-v1'))
VERSION = '1.0.0'
SUPPORTED_LEVELS = ('easy', 'moderate')
SCALES = tuple(range(-8, 0)) + tuple(range(2, 9))
x, y = s.symbols('x y', real=True)
# P, Q, circle radius or side outward normal, level. Side 1=right, 2=top,
# 3=left, 4=bottom; these are mathematical sign/component roles, not shuffles.
DATA = {
    'q-126833': (x**2, -y**2, 1, 'easy'),
    'q-127049': (2*x**2, 2*y**2, 2, 'easy'),
    'q-127052': (3*x*y, -x**2, 1, 'easy'),
    'q-127056': (15*x*y, 5*x**2, 5, 'easy'),
    'q-127057': (4*x**2*y**2, 2*x**3*y, 2, 'easy'),
    'q-126850': (x**2, y**2, (1, 0), 'moderate'),
    'q-127050': (x**3, 3*y**2, (0, 1), 'moderate'),
    'q-127053': (x**3*y, -x*y**2, (-1, 0), 'moderate'),
    'q-127054': (x*y, -x**2*y, (0, -1), 'moderate'),
    'q-127058': (x**5*y**7, x*y**3, (1, 0), 'moderate'),
    'q-127059': ((x+y)**2, (x-y)**2, (0, 1), 'moderate'),
}
EXCLUDED = {
    'q-167889': 'Prompt requires the normal from part 5; element E and its normal are not supplied.',
    'q-168603': 'Prompt and inspected diagram supply the square but omit the vector field F.',
}
SOURCES = {q[':question/math-academy-id']: q for q in SNAPSHOT['record'][':knowledge-point/questions']}


def parse(value):
    value = value.replace(r'\,', '').replace(r'\left', '').replace(r'\right', '')
    while r'\frac' in value:
        previous = value
        value = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', value)
        assert value != previous, value
    return parse_expr(value.replace('{', '(').replace('}', ')'),
                      local_dict={'x': x, 'y': y},
                      transformations=standard_transformations + (implicit_multiplication_application, convert_xor))


def tex(expr):
    return s.latex(expr)


def mathematics(template, scale):
    p, q, geometry, level = DATA[template]
    p, q = scale*p, scale*q
    nx, ny = (x/s.Integer(geometry), y/s.Integer(geometry)) if level == 'easy' else geometry
    terms = (p*nx, q*ny)
    return p, q, nx, ny, terms, sum(terms)


def signature(template, scale):
    p, q, nx, ny, terms, answer = mathematics(template, scale)
    level = DATA[template][-1]
    # Ignore dimensions that do not affect side projection, bank order, UUIDs,
    # and seed. Circle tasks with the same normalized components also collide.
    values = (p / DATA[template][2], q / DATA[template][2]) if level == 'easy' else (p, q, nx, ny)
    return json.dumps([level] + [str(s.expand(z)) for z in values])


def rendered(template, scale):
    src = SOURCES[template]
    if scale == 1:
        return src[':question/problem'], src[':question/worked-solution']
    p, q, nx, ny, terms, answer = mathematics(template, scale)
    field = '(' + tex(p) + r')\,i+(' + tex(q) + r')\,j'
    prompt = src[':question/problem']
    start = prompt.index('F(x,y)=') + len('F(x,y)=')
    end = prompt.index('$', start)
    prompt = prompt[:start] + field + prompt[end:]
    solution = src[':question/worked-solution']
    prefix, rest = solution.split('In our case, we have', 1) if DATA[template][-1] == 'easy' else (None, None)
    if DATA[template][-1] == 'easy':
        integral = r'{∮}_{C}'
        normal = '(' + tex(nx) + r'\,i+' + tex(ny) + r'\,j)'
        prefix += 'In our case, we have\n\n'
    else:
        prefix = solution.split('Therefore,\n\n', 1)[0] + 'Therefore,\n\n'
        integral = re.search(r'\{\\int \}_\{\{C\}_\{\d\}\}', solution)[0]
        normal = { (1,0): 'i', (0,1): 'j', (-1,0): '(-i)', (0,-1): '(-j)' }[DATA[template][2]]
    lines = [integral + r'F\cdot n\,\text{d}s & =' + integral + '(' + field + r')\cdot ' + normal + r'\,\text{d}s']
    # Preserve the observed split-then-combine stage only where it occurs.
    if template in ('q-127052', 'q-127056', 'q-127057'):
        unsummed = tex(terms[0]) + ('-' + tex(-terms[1]) if terms[1].could_extract_minus_sign() else '+' + tex(terms[1]))
        lines.append(' & =' + integral + unsummed + r'\,\text{d}s')
    lines.append(' & =' + integral + tex(answer) + r'\,\text{d}s.')
    solution = prefix + '$$\n\\begin{aligned}' + r' \\ '.join(lines) + '\\end{aligned}\n$$\n\nTherefore, the missing expression is $' + tex(answer) + '.$'
    return prompt, solution


def generate(level, seed=0, template=None, parameters=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: ' + level)
    rng = random.Random(seed)
    eligible = sorted(k for k, d in DATA.items() if d[-1] == level)
    template = template or rng.choice(eligible)
    assert template in eligible
    scale = (parameters or {}).get('scale', rng.choice(SCALES))
    assert isinstance(scale, int) and scale in (1,) + SCALES
    src = SOURCES[template]
    sf = src[':question/answer-fields'][0]
    sig = signature(template, scale)
    profile = 'observed-whole-field-scale:' + template
    qid = str(uuid.uuid5(NS, VERSION + ':' + sig + ':' + profile))
    fid = str(uuid.uuid5(uuid.UUID(qid), sf[':answer-field/key']))
    choices = []
    correct = None
    for a in sf[':answer-field/choices']:
        value = a[':answer/value'] if scale == 1 else tex(scale*parse(a[':answer/value']))
        aid = str(uuid.uuid5(uuid.UUID(fid), str(s.expand(parse(value)))))
        choices.append({':answer/id': aid, ':answer/type': ':answer.type/math', ':answer/value': value})
        if a[':answer/id'] == sf[':answer-field/correct'][':answer/id']:
            correct = aid
    problem, solution = rendered(template, scale)
    return {
        'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': SNAPSHOT['record'][':knowledge-point/title']},
        'question': {':question/id': qid, ':question/difficulty': ':question.difficulty/' + level,
                     ':question/problem': problem, ':question/worked-solution': solution,
                     ':question/answer-fields': [{':answer-field/id': fid, ':answer-field/key': sf[':answer-field/key'],
                         ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
                         ':answer-field/correct': [':answer/id', correct]}]},
        'generation': {'generator_id': GENERATOR_UUID, 'version': VERSION, 'seed': seed, 'template': template,
                       'parameters': {'scale': scale}, 'profile': profile,
                       'mathematical_signature': sig, 'source_basis': SNAPSHOT['basis'],
                       'source_question_id': src[':question/id'], 'sympy_version': s.__version__,
                       'domains': 'x,y real; circle radius positive; outward normal as supplied or shown',
                       'generalization': 'One nonzero integer scales the entire field and complete observed bank; geometry fixed.'},
    }


def batch(level, count=5, seed=0):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported difficulty: ' + level)
    if count < 0:
        raise ValueError('Count must be nonnegative')
    if count == 0:
        return []
    pool = [(k, a) for k, d in sorted(DATA.items()) if d[-1] == level for a in SCALES]
    random.Random(seed).shuffle(pool)
    result, seen = [], set()
    for k, a in pool:
        r = generate(level, seed, k, {'scale': a})
        sig = r['generation']['mathematical_signature']
        if sig not in seen:
            seen.add(sig)
            result.append(r)
        if len(result) == count:
            return result
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--difficulty', choices=SUPPORTED_LEVELS, required=True)
    ap.add_argument('--count', type=int, default=5)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--format', choices=('json', 'markdown'), default='json')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    records = batch(args.difficulty, args.count, args.seed)
    if args.format == 'json':
        # The inventory worker saves this array as its .generated instances.
        payload = json.dumps(records, indent=2) + '\n'
    else:
        payload = '\n\n---\n\n'.join(r['question'][':question/problem'] + '\n\n' + r['question'][':question/worked-solution'] for r in records) + '\n'
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end='')
