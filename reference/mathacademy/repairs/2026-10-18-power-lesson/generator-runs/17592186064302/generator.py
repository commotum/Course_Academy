#!/usr/bin/env python3
"""Relocatable, database-free signed power-rule question generator."""
import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path
import random
import sys
import uuid

from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.0.0'
KP = {'db_id': 17592186064302, 'id': '5abe4cbe-7495-5723-88cd-f97796f8ef49',
      'title': 'Using the Power Rule with Negative Exponents'}
NS = uuid.UUID(KP['id'])
SIGNS = {'positive-negative': (1, -1), 'negative-positive': (-1, 1),
         'negative-negative': (-1, -1)}
RECIPES = ('reverse-sign', 'add', 'negative-add', 'subtract', 'reverse-subtract',
           'outer-plus-one', 'outer-minus-one', 'inner-plus-one', 'inner-minus-one')
SOURCE_SPECS = [
    ('exponent', 2, -3, 'a', 'k', 'easy'),
    ('exponent', -3, 5, 'y', 'n', 'easy'),
    ('exponent', 4, -2, 'y', 'k', 'easy'),
    ('power', 6, -3, 'z', 'k', 'easy'),
    ('exponent', -3, 5, 'x', 'k', 'easy'),
    ('zero-factor', -3, -3, 'q', 'k', 'moderate'),
]
SOURCE_RECIPES = [
    ('reverse-sign', 'subtract', 'reverse-subtract', 'add'),
    ('reverse-sign', 'negative-add', 'add', 'reverse-subtract'),
    ('reverse-sign', 'subtract', 'reverse-subtract', 'negative-add'),
    ('reverse-sign', 'outer-plus-one', 'add', 'source-absolute-ratio'),
    ('reverse-sign', 'subtract', 'reverse-subtract', 'add'),
    ('reverse-sign', 'add', 'source-negative-inner', 'undefined'),
]


def uid(value):
    return str(uuid.uuid5(NS, value))


def power(base, exponent):
    return f'{{{base}}}^{{{exponent}}}'


def nested(base, inner, outer):
    return f'({power(base, inner)})^{{{outer}}}'


def values(a, b):
    return dict(zip(RECIPES, (-a*b, a+b, -a-b, a-b, b-a,
                            a*(b+1), a*(b-1), (a+1)*b, (a-1)*b))) | {
                                'undefined': None, 'source-absolute-ratio': Fraction(abs(a), abs(b)),
                                'source-negative-inner': -a}


def bank_exponents(a, b, recipes):
    return [a*b] + [values(a, b)[r] for r in recipes]


def compatible(a, b, recipes):
    vals = bank_exponents(a, b, recipes)
    return len(set(vals)) == 5


def solution(i):
    a, b, base = i['inner'], i['outer'], i['base']
    p = a*b
    mult = f'{power(base, f"({a})\\cdot ({b})")}'
    last = power(base, p)
    if i['template'] == 'zero-factor':
        inactive = i['inactive']
        terms = [power(inactive, 0), power(base, a)]
        simplified = [r'1', power(base, a)]
        if i['active_position'] == 0:
            terms.reverse(); simplified.reverse()
        original = f'({"".join(terms)})^{{{b}}}'
        inside = r'\cdot '.join(simplified)
        chain = [original, f'({inside})^{{{b}}}', nested(base, a, b), mult, last]
        intro = ('First, we simplify the expression inside the parenthesis and then we apply the power rule')
    else:
        chain = [nested(base, a, b), mult, last]
        intro = 'We multiply the exponents, as follows:'
    # Conventional chained equalities, instead of the captured trailing equals signs.
    display = chain[0] + r' &= ' + chain[1]
    display += ''.join(r' \\ &= ' + term for term in chain[2:])
    result = intro + '\n\n$$\n' + r'\begin{aligned}' + display + r'\end{aligned}' + '\n$$'
    if i['template'] == 'exponent':
        result += f'\n\nHence, ${i["exponent_name"]}={p}.$'
    return result


@checked_math_content
def generate(i, rng=None, *, source=None):
    """Render all content from one shared mathematical instance."""
    rng = rng or random.Random(0)
    a, b, base = i['inner'], i['outer'], i['base']
    template = i['template']
    if template == 'exponent':
        name = i['exponent_name']
        problem = f'If ${nested(base, a, b)}={power(base, name)}$, then ${name}=$'
        domain = f'Assume ${base}\\ne 0$.\n\n'
    elif template == 'power':
        problem = f'${nested(base, a, b)}=$'
        domain = f'Assume ${base}\\ne 0$.\n\n'
    elif template == 'zero-factor':
        terms = [power(i['inactive'], 0), power(base, a)]
        if i['active_position'] == 0:
            terms.reverse()
        problem = f'Which of the following is equivalent to $({"".join(terms)})^{{{b}}}$?'
        domain = f'Assume ${base}\\ne 0$ and ${i["inactive"]}\\ne 0$.\n\n'
    else:
        raise ValueError('Unknown template')
    entries = bank_exponents(a, b, i['recipes'])
    typed = [((':answer.type/text', 'undefined') if e is None else
              (':answer.type/math', str(e) if template == 'exponent' else power(base, e))) for e in entries]
    if source is not None:
        problem = source[':question/problem']
        domain = ''
    typed = [(kind, normalize_tex(value) if kind == ':answer.type/math' else value) for kind, value in typed]
    correct_value = normalize_tex(str(a*b) if template == 'exponent' else power(base, a*b))
    correct = (':answer.type/math', correct_value)
    assert len(typed) == len(set(typed)) == 5 and correct in typed
    problem = normalize_prose(domain + problem)
    worked = normalize_prose(solution(i))
    # Identity includes the complete bank, not the seed, shuffle, or metadata.
    identity = json.dumps([template, problem, sorted(typed)], separators=(',', ':'))
    qid, fid = uid(identity), uid(identity + ':selection')
    choices = [{':answer/id': uid(fid + ':' + kind + ':' + value),
                ':answer/type': kind, ':answer/value': value} for kind, value in typed]
    key = next(c[':answer/id'] for c in choices if (c[':answer/type'], c[':answer/value']) == correct)
    if source is None:
        rng.shuffle(choices)
    field = {':answer-field/id': fid, ':answer-field/key': 'selection',
             ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
             ':answer-field/correct': [':answer/id', key]}
    generation = {'version': VERSION, 'template': template, 'parameters': dict(i),
                  'profile': 'signed-error-bank-v1' if source is None else 'source:' + source[':question/id'],
                  'source_ids': source_ids(template), 'domain': 'nonzero real bases; integer exponents',
                  'dependencies': {'python': '3.13.5', 'packages': {}}}
    if source is not None:
        generation.update(source_id=source[':question/id'],
                          original_difficulty=source.get(':question/difficulty'),
                          inferred_missing_fields=[k for k in (':question/difficulty', ':question/worked-solution') if k not in source])
        if ':answer-field/correct' not in source[':question/answer-fields'][0]:
            generation['inferred_missing_fields'].append(':answer-field/correct')
    return {'knowledge_point': KP, 'question': {':question/id': qid,
            ':question/difficulty': ':question.difficulty/' + i['difficulty'],
            ':question/problem': problem, ':question/worked-solution': worked,
            ':question/answer-fields': [field]}, 'generation': generation, 'assets': {}}


def source_questions():
    return json.loads(Path(__file__).with_name('source-data.json').read_text())[':knowledge-point/questions']


def source_ids(template):
    return [q[':question/id'] for q, spec in zip(source_questions(), SOURCE_SPECS) if spec[0] == template]


def replay_sources():
    records = []
    for q, (template, a, b, base, name, difficulty), recipes in zip(source_questions(), SOURCE_SPECS, SOURCE_RECIPES):
        i = dict(template=template, inner=a, outer=b, base=base, exponent_name=name,
                 difficulty=difficulty, inactive='p', active_position=1, recipes=recipes)
        records.append(generate(i, source=q))
    return records


def sample_instance(rng, difficulty):
    if difficulty not in ('easy', 'moderate'):
        raise ValueError('Unsupported difficulty: ' + difficulty)
    template = rng.choice(('exponent', 'power')) if difficulty == 'easy' else 'zero-factor'
    case = rng.choice(tuple(SIGNS))
    sa, sb = SIGNS[case]
    pool = RECIPES + (('undefined',) if template == 'zero-factor' else ())
    # Choose a whole bank assignment first; then enumerate compatible values.
    profile_rejections = 0
    while True:
        recipes = tuple(rng.sample(pool, 4))
        eligible = [(sa*a, sb*b) for a, b in itertools.product(range(1, 7), repeat=2)
                    if compatible(sa*a, sb*b, recipes)]
        if eligible:
            break
        profile_rejections += 1
    a, b = rng.choice(eligible)
    base = rng.choice(('a', 'x', 'y', 'z'))
    inactive = None
    active_position = None
    if template == 'zero-factor':
        pair = rng.choice((('p', 'q'), ('x', 'y')))
        active_identity = rng.randrange(2)
        base, inactive = pair[active_identity], pair[1-active_identity]
        active_position = rng.randrange(2)
    return dict(template=template, difficulty=difficulty, sign_case=case, inner=a, outer=b,
                base=base, inactive=inactive, active_position=active_position,
                exponent_name=rng.choice(('k', 'n', 'm')), recipes=list(recipes),
                compatible_parameters=len(eligible), profile_rejections=profile_rejections)


def batch(difficulty, count, seed):
    if count < 0:
        raise ValueError('count must be nonnegative')
    rng = random.Random(seed)
    result = []
    for index in range(count):
        i = sample_instance(rng, difficulty)
        record = generate(i, rng)
        record['generation'].update(seed=seed, index=index)
        result.append(record)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=('easy', 'moderate', 'hard', 'unclassified'), default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json',), default='json')
    parser.add_argument('--replay-source', action='store_true')
    args = parser.parse_args()
    if args.difficulty == 'hard':
        parser.error('hard is unsupported: no source evidence for that band')
    records = replay_sources() if args.replay_source else batch('easy' if args.difficulty == 'unclassified' else args.difficulty, args.count, args.seed)
    json.dump(records, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == '__main__':
    main()
