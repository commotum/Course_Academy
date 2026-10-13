#!/usr/bin/env python3
"""Perpendicular line through a point: validated text-only RHS blank families.

Easy has a target on the y-axis; moderate requires translating a nonzero
x-coordinate. Hard and unresolved source radio/diagram families are excluded.
Mathematical identity is the resulting line, independent of seed, layout, or
which pair of points describes the reference direction. No database writes.
"""
import argparse
import hashlib
import json
import random
import re
import sys
import uuid
from pathlib import Path

if __name__ == '__main__' and sys.prefix == sys.base_prefix:
    import os
    executable = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    os.execv(str(executable), [str(executable), str(Path(__file__).resolve()), *sys.argv[1:]])
import sympy as sp

KP_ID = 17592186175923
KP_UUID = '44b9b212-27c4-5d6d-a221-cd85c25fc956'
TITLE = 'Finding the Equation of a Line Perpendicular to a Line Through Two Points'
VERSION = '1.0.0'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
HERE = Path(__file__).resolve().with_suffix('')
SOURCE = json.loads((HERE / 'source.json').read_text())
SOURCES = {q[':question/math-academy-id']: q for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS = ('easy', 'moderate')
TEMPLATES = {'q-215768': 'easy', 'q-237224': 'easy', 'q-237225': 'easy', 'q-237036': 'moderate'}
X, Y = sp.symbols('x y', real=True)
DOMAIN = {'coordinates': 'integers -8..8', 'reference': 'distinct points with nonzero dx and dy',
          'easy': 'target x=0; signed integral coordinates and exact rational slopes',
          'moderate': 'target x!=0; same slope calculation followed by point-slope distribution',
          'extensions': 'both signs of target coordinates; moderate rational slopes inferred from rated radio sources, with the observed RHS blank response',
          'identity': 'exact reduced target slope and intercept; reference translation, source layout, field order and seed excluded'}

def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(text):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), text))

def tex(x):
    return sp.latex(sp.sympify(x)).replace('- ', '-')

def points(text):
    return [list(map(int, p)) for p in re.findall(r'\$\((-?\d+),\s*(-?\d+)\)', text)]

def source_parameters(mid):
    p, a, b = points(SOURCES[mid][':question/problem'])
    return {'P': p, 'A': a, 'B': b}

def parameters(p, level):
    if set(p) != {'P', 'A', 'B'}:
        raise ValueError('Three points required')
    if any(len(z) != 2 or any(type(n) != int or not -8 <= n <= 8 for n in z) for z in p.values()):
        raise ValueError('Bounded integral coordinates required')
    if (p['P'][0] == 0) != (level == 'easy'):
        raise ValueError('Difficulty/target coordinate mismatch')
    if p['A'][0] == p['B'][0] or p['A'][1] == p['B'][1]:
        raise ValueError('Vertical and horizontal reference lines are outside supported source families')
    return {k: list(z) for k, z in p.items()}

def values(p):
    h, k = p['P']; a, b = p['A']; c, d = p['B']
    reference = sp.Rational(d-b, c-a)
    slope = -1/reference
    intercept = k-slope*h
    return reference, slope, intercept

def task_key(p):
    _, m, b = values(p)
    return digest({'slope': str(m), 'intercept': str(b)})

def fingerprint_text(problem):
    coordinates = points(problem)
    if len(coordinates) != 3:
        raise ValueError('Missing reference point coordinates or diagram')
    return task_key(dict(zip(('P', 'A', 'B'), coordinates)))

def sub(left, right):
    return str(left) + '-' + ('(' + str(right) + ')' if right < 0 else str(right))

def simplified_sub(left, right):
    return str(left) + ('+' + str(-right) if right < 0 else '-' + str(right))

def coord(p):
    return '(' + ','.join(map(str, p)) + ')'

def render(template, p):
    original = SOURCES[template]
    old = source_parameters(template)
    h, k = p['P']; a, b = p['A']; c, d = p['B']
    r, m, intercept = values(p)
    text = original[':question/problem']
    # Replace only coordinate math tokens; retain prompt wording and RHS field.
    iterator = iter([p['P'], p['A'], p['B']])
    text = re.sub(r'\((-?\d+),\s*(-?\d+)\)', lambda _: coord(next(iterator)), text)
    solution = original[':question/worked-solution']
    iterator = iter([p['A'], p['B'], p['P']])
    solution = re.sub(r'\((-?\d+),\s*(-?\d+)\)', lambda _: coord(next(iterator)), solution)
    fraction = lambda n, den: r'\frac{' + n + '}{' + den + '}'
    rows = [r'{m}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}}',
            ' & =' + fraction(sub(d,b), sub(c,a))]
    if template != 'q-237036':
        rows.append(' & =' + fraction(simplified_sub(d,b), simplified_sub(c,a)))
    if template in ('q-215768', 'q-237036'):
        rows.append(' & =' + fraction(str(d-b), str(c-a)))
    rows.append(' & =' + tex(r))
    slope_display = r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}'
    reciprocal_display = r'm\cdot (' + tex(r) + r')=-1\,⇒\,m=' + tex(m) + '.'
    # Each row is the same equation; simplification is computed exactly.
    left = 'y' if k == 0 else 'y' + ('-' + str(k) if k > 0 else '+' + str(-k))
    shifted = 'x' if h == 0 else 'x' + ('-' + str(h) if h > 0 else '+' + str(-h))
    rows = [r'y-{y}_{1} & =m(x-{x}_{1})',
            'y-' + ('(' + str(k) + ')' if k < 0 else str(k)) + ' & =' + tex(m) + '(' + sub('x',h) + ')']
    if template == 'q-237036':
        rows.append(left + ' & =' + tex(m) + '(' + shifted + ')')
    rows.extend([left + ' & =' + tex(sp.expand(m*(X-h))),
                 'y & =' + tex(m*X+intercept)])
    answer_display = r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}'
    displays = iter([slope_display, reciprocal_display, answer_display])
    solution = re.sub(r'\$\$\n.*?\n\$\$', lambda _: '$$\n' + next(displays) + '\n$$', solution, flags=re.S)
    return text, solution

def generate(level, seed=0, template=None, parameters=None, profile=None):
    if level not in SUPPORTED_LEVELS:
        raise ValueError('Unsupported hard: no calibrated and validated harder family; see capabilities.json')
    if profile is not None:
        raise ValueError('Blanks have no distractor profile')
    rng = random.Random(seed)
    template = template or rng.choice([t for t, l in TEMPLATES.items() if l == level])
    if TEMPLATES.get(template) != level:
        raise ValueError('Unsupported template/difficulty')
    if parameters is None:
        for _ in range(200):
            p = {'P': [0 if level == 'easy' else rng.choice([n for n in range(-8,9) if n]), rng.randint(-8,8)],
                 'A': [rng.randint(-8,8), rng.randint(-8,8)], 'B': [rng.randint(-8,8), rng.randint(-8,8)]}
            try:
                globals()['parameters'](p, level)
                break
            except ValueError:
                continue
        else:
            raise ValueError('Bounded sampler exhausted')
    else:
        p = parameters
    p = globals()['parameters'](p, level)
    problem, solution = render(template, p)
    _, m, b = values(p)
    answer = tex(m*X+b)
    content = digest({'problem': problem, 'solution': solution, 'answer': answer, 'level': level})
    qid = uid('question:' + content); fid = uid(qid + ':field:field-1'); aid = uid(fid + ':answer:' + answer)
    question = {':question/id': qid, ':question/problem': problem, ':question/worked-solution': solution,
                ':question/difficulty': ':question.difficulty/' + level,
                ':question/answer-fields': [{':answer-field/id': fid, ':answer-field/key': 'field-1',
                ':answer-field/type': ':answer-field.type/blank', ':answer-field/choices': [{':answer/id': aid,
                ':answer/type': ':answer.type/math', ':answer/value': answer}], ':answer-field/correct': [':answer/id', aid]}]}
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE}, 'question': question,
            'generation': {'version': VERSION, 'seed': seed, 'template': template, 'parameters': p,
            'bank_profile': None, 'source_question': template, 'source_basis': SOURCE['basis'], 'source_lineage': SOURCE['lineage'],
            'parameter_fingerprint': task_key(p), 'content_fingerprint': content, 'domain': DOMAIN,
            'dependencies': {'python': sys.version.split()[0], 'sympy': sp.__version__}, 'plot_rating': 'none',
            'difficulty_origin': 'observed easy y-axis target vs moderate translated target; bounded rational extension'}}

def batch(level, count, seed=0, **kwargs):
    if type(count) != int or not 1 <= count <= 100:
        raise ValueError('Batch count must be 1..100')
    out = []; seen = set()
    for i in range(2000):
        rec = generate(level, seed+i, **kwargs)
        key = rec['generation']['parameter_fingerprint']
        if key not in seen:
            seen.add(key); out.append(rec)
        if len(out) == count:
            return out
    raise ValueError('Finite limit: ' + str(len(out)) + ' distinct lines in 2000 attempts')

def generate_easy(seed=0, **kwargs): return generate('easy', seed, **kwargs)
def generate_moderate(seed=0, **kwargs): return generate('moderate', seed, **kwargs)
def generate_hard(*args, **kwargs): raise ValueError('Unsupported hard; see capabilities.json')

def markdown(rec):
    q = rec['question']; answer = q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
    return q[':question/problem'] + '\n\nAnswer: $' + answer + '$\n\n' + q[':question/worked-solution']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', choices=('easy','moderate','hard','all'), default='all')
    parser.add_argument('--count', type=int, default=1); parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--template', choices=list(TEMPLATES)); parser.add_argument('--format', choices=('json','markdown'), default='json')
    args = parser.parse_args()
    levels = SUPPORTED_LEVELS if args.difficulty == 'all' else (args.difficulty,)
    records = [r for level in levels for r in batch(level, args.count, args.seed, template=args.template)]
    print(json.dumps(records, indent=2) if args.format == 'json' else '\n\n---\n\n'.join(map(markdown, records)))

if __name__ == '__main__': main()
