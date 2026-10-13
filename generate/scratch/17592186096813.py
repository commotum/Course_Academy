#!/usr/bin/env python3
"""Normalize an abstract nonzero vector using its supplied magnitude.

Read-only scratch implementation of steps 3–7, math basis 1356. Both observed
practice sources are unrated and have no keys/solutions. Raw evidence profiles
preserve those omissions; they are never eligible for learning. Their complete
five-option banks use parameterized expression masks, not source payload lookup.
The q-11376 scaling expressions are observed shapes, with unresolved error intent.

Authored E/M/H levels differ only in reciprocal number forms: integer, reduced
noninteger rational, and squarefree radical magnitude. All keep the canonical
one-operation normalization method. Names/endpoint labels are incidental and do
not inflate mathematical task counts. No component, diagram or sum questions.

Explicit parameters must obey the same workload bounds as sampling. Seed only
selects parameters and shuffles choices; identity includes actual prompt, fixed
solution and complete bank, and excludes order/seed/profile aliases. Every bank
is complete and tested before output. Sources, extraction and validation live in
the adjacent 17592186096813 directory. No EDB access or writes are implemented.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import uuid

import sympy as sp

KP_ID = 17592186096813
KP_UUID = '48a66a99-6b4a-5ad5-8922-6f48006ff183'
TITLE = 'Finding a Unit Vector Parallel to a Given Vector'
VERSION = 'known-magnitude-unit-vector-1'
# Stable registration identity derived from the existing KP UUID.
GENERATOR_ID = '69c0d337-c0c7-5401-85a9-e535b8ad24e1'
SOURCE = {'database': 'math', 'basis': 1356,
          'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES = ('named', 'directed')
PROFILES = ('normalization', 'direction_errors', 'raw_named', 'raw_directed')
RADICANDS = (2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19)
PARAMETER_DOMAINS = {
    'easy': [{'m': m} for m in range(2, 31)],
    'moderate': [{'p': p, 'q': q} for p in range(3, 21)
                 for q in range(2, 10) if p > q and math.gcd(p, q) == 1],
    'hard': [{'k': k, 'd': d} for k in range(1, 6) for d in RADICANDS],
}


def tex(value):
    return sp.latex(sp.sympify(value))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def uid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'unit-vector/' + value))


def parameters_for(level, template, parameters, rng):
    p = dict(rng.choice(PARAMETER_DOMAINS[level]) if parameters is None else parameters)
    keys = {'easy': {'m'}, 'moderate': {'p', 'q'}, 'hard': {'k', 'd'}}[level]
    if set(p) - (keys | {'label'}) or not keys <= set(p):
        raise ValueError('Parameters require exactly the level components and optional label')
    if any(type(p[key]) is not int for key in keys):
        raise ValueError('Integer parameter components required')
    if {key: p[key] for key in keys} not in PARAMETER_DOMAINS[level]:
        raise ValueError('Parameters outside authored level workload bounds')
    label = p.setdefault('label', 'a' if template == 'named' else 'AB')
    allowed = ('a', 'b', 'c', 'v', 'w') if template == 'named' else ('AB', 'CD', 'PQ', 'RS')
    if label not in allowed:
        raise ValueError('Unsupported vector label')
    magnitude = (sp.Integer(p['m']) if level == 'easy' else
                 sp.Rational(p['p'], p['q']) if level == 'moderate' else
                 p['k'] * sp.sqrt(p['d']))
    return p, magnitude


def product(coefficient, vector):
    """Complete scalar component before vector label; never concatenate numerals."""
    c = sp.sympify(coefficient)
    if c == 1:
        return vector
    if c == -1:
        return '-' + vector
    return tex(c) + vector


def bank(m, vector, reverse, profile):
    """Whole banks; the first component is a recipe name, never learner feedback."""
    correct = product(1 / m, vector)
    if profile == 'raw_named':
        # Observed masks only: 2m/4m intent cannot be inferred from one scalar bank.
        return [('multiply_magnitude', product(m, vector)),
                ('omit_vector', tex(1 / m)),
                ('observed_2m_denominator', product(1 / (2 * m), vector)),
                ('observed_4m_denominator', product(1 / (4 * m), vector)),
                ('correct', correct)]
    if profile == 'raw_directed':
        return [('unchanged', vector), ('multiply_reversed', product(m, reverse)),
                ('negate', '-' + vector), ('correct', correct),
                ('negated_multiply_reversed', product(-m, reverse))]
    if profile == 'direction_errors':
        return [('unchanged', vector), ('negate', '-' + vector),
                ('multiply_magnitude', product(m, vector)),
                ('negated_multiply', product(-m, vector)), ('correct', correct)]
    return [('multiply_magnitude', product(m, vector)), ('omit_vector', tex(1 / m)),
            ('divide_squared_magnitude', product(1 / m**2, vector)),
            ('unchanged', vector), ('correct', correct)]


def generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None):
    if level not in PARAMETER_DOMAINS:
        raise ValueError('Level must be easy, moderate or hard')
    if field_type not in (None, 'radio', ':answer-field.type/radio'):
        raise ValueError('Observed response layout supports radio only')
    rng = random.Random(seed)
    profile = profile or 'normalization'
    if profile not in PROFILES:
        raise ValueError('Unknown complete bank profile')
    if template is None:
        template = (profile.removeprefix('raw_') if profile.startswith('raw_')
                    else rng.choice(TEMPLATES))
    if template not in TEMPLATES:
        raise ValueError('Unknown template')
    raw = profile.startswith('raw_')
    if raw and (level != 'easy' or profile != 'raw_' + template):
        raise ValueError('Observed evidence profiles use matching template and integer magnitude')
    p, m = parameters_for(level, template, parameters, rng)
    label = p['label']
    if template == 'named':
        vector = label if raw else r'\mathbf{' + label + '}'
        reverse = None
    else:
        vector = label + '^(→)' if raw else r'\overrightarrow{' + label + '}'
        reverse = label[::-1] + '^(→)' if raw else r'\overrightarrow{' + label[::-1] + '}'
    prompt = f'The vector ${vector}$ has magnitude ${tex(m)}$. '
    prompt += (f'Find a unit vector that is parallel to ${vector}$.' if template == 'named'
               else f'Which of the following is a unit vector that is parallel to ${vector}$?')
    choices = bank(m, vector, reverse, profile)
    solution = None
    if not raw:
        solution = (f'To obtain the unit vector that is parallel to ${vector}$, '
                    f'we divide ${vector}$ by its length:\n\n$$\n'
                    + r'\mathbf{u}=\dfrac{' + vector + r'}{\mid \,' + vector
                    + r'\, \mid}=\dfrac{1}{' + tex(m) + '}' + vector
                    + ('' if level == 'easy' else '=' + product(1 / m, vector)) + '\n$$')
    # Raw records deliberately omit keys/solutions/ratings that were not captured.
    content = {'version': VERSION, 'prompt': prompt, 'solution': solution,
               'bank': sorted(value for _, value in choices),
               'difficulty': None if raw else level, 'type': ':answer-field.type/radio'}
    fingerprint = digest(content)
    qid, fid = uid(fingerprint), uid(fingerprint + '/selection')
    answers = [{':answer/id': uid(fid + '/' + value), ':answer/type': ':answer.type/math',
                ':answer/value': value} for _, value in choices]
    if len({a[':answer/id'] for a in answers}) != 5:
        raise ValueError('Reject complete bank with repeated choices')
    correct_id = answers[next(i for i, (recipe, _) in enumerate(choices)
                             if recipe == 'correct')][':answer/id']
    rng.shuffle(answers)
    field = {':answer-field/id': fid, ':answer-field/key': 'selection',
             ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': answers}
    question = {':question/id': qid, ':question/problem': prompt,
                ':question/answer-fields': [field]}
    if not raw:
        field[':answer-field/correct'] = [':answer/id', correct_id]
        question[':question/difficulty'] = ':question.difficulty/' + level
        question[':question/worked-solution'] = solution
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
            'question': question,
            'generation': {'version': VERSION, 'source': SOURCE, 'seed': seed,
                           'template': template, 'profile': profile, 'parameters': p,
                           'evidence_only': raw, 'eligible_for_learning': not raw,
                           'authored_level': level, 'observed_level': None,
                           'origin': 'observed expression-mask replay' if raw else 'authored',
                           'source_ids': ['q-11376' if template == 'named' else 'q-12202'],
                           'recipes': [recipe for recipe, _ in choices],
                           'inferred_correct_value': product(1 / m, vector),
                           'inferred_correct_status': 'independent mathematics; no observed key',
                           'domain': 'known magnitude > 1; nonzero abstract vector',
                           'plot_rating': 'none', 'content_fingerprint': fingerprint,
                           'mathematical_fingerprint': digest({'operation': 'normalize_known_magnitude',
                                                              'magnitude': sp.srepr(m)}),
                           'dependencies': {'sympy': sp.__version__}}}


# EASY — authored integer reciprocal workload, including both unrated originals.
def generate_easy(seed=0, template=None, field_type=None, parameters=None, profile=None):
    return generate('easy', seed, template, field_type, parameters, profile)


# MODERATE — authored reduced noninteger rational magnitude, invert numerator/denominator.
def generate_moderate(seed=0, template=None, field_type=None, parameters=None, profile=None):
    return generate('moderate', seed, template, field_type, parameters, profile)


# HARD — authored supplied squarefree-radical magnitude; exact reciprocal recognition.
# The magnitude is never computed from coordinates, components, a plot or a sum.
def generate_hard(seed=0, template=None, field_type=None, parameters=None, profile=None):
    return generate('hard', seed, template, field_type, parameters, profile)


def markdown(record):
    q, g = record['question'], record['generation']
    f = q[':question/answer-fields'][0]
    rows = [f"### {g['authored_level']} / {g['template']} / {g['profile']}",
            q[':question/problem'], '']
    rows += [f'{letter}. ${answer[":answer/value"]}$' for letter, answer in
             zip('ABCDE', f[':answer-field/choices'])]
    if g['evidence_only']:
        rows += ['', 'Evidence replay: original correct ref, worked solution and rating absent.']
    else:
        correct = next(letter for letter, answer in zip('ABCDE', f[':answer-field/choices'])
                       if answer[':answer/id'] == f[':answer-field/correct'][1])
        rows += ['', 'Correct: ' + correct, '', q[':question/worked-solution']]
    return '\n'.join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=('easy', 'moderate', 'hard', 'all'), default='all')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--format', choices=('markdown', 'json'), default='markdown')
    parser.add_argument('--template', choices=TEMPLATES)
    parser.add_argument('--profile', choices=PROFILES)
    args = parser.parse_args()
    if args.count < 1:
        parser.error('count must be positive')
    levels = list(PARAMETER_DOMAINS) if args.difficulty == 'all' else [args.difficulty]
    records = [generate(level, args.seed + i, args.template, profile=args.profile)
               for level in levels for i in range(args.count)]
    print(json.dumps(records, indent=2, ensure_ascii=False) if args.format == 'json'
          else '\n\n'.join(markdown(record) for record in records))


if __name__ == '__main__':
    main()
