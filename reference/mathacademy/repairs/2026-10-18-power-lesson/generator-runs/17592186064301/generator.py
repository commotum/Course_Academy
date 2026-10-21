#!/usr/bin/env python3
"""Relocatable positive-integer power-rule generator; no database or asset writes."""
import argparse
from fractions import Fraction
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random
import uuid

from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.1.0'
SOURCE = json.loads(Path(__file__).with_name('source-data.json').read_text())
KP = SOURCE['kp']
TEMPLATES = ('symbolic-equals', 'symbolic-question', 'numeric')
PROFILES = dict(zip(TEMPLATES, ('S1', 'S2', 'N')))
BASES = ('x', 'y', 'z', 'a', 'b')


def power(base, exponent):
    if exponent == 0:
        return '1'
    if exponent == 1:
        return str(base)
    return f'{base}^{{{exponent}}}'


def numeric_exponents(base, offsets):
    banks = {2: {(-1,): (1,4,6,8,9), (1,): (4,6,8,9,10)},
             3: {(-1,): (1,2,4,5,6), (1,): (3,4,5,6,7)}}
    return banks[base][tuple(offsets)]


def bank_values(template, base, m, n, offsets, *, source_replay=False):
    p = m * n
    if template == 'symbolic-equals':
        return [p, m+n, m-n, n, p+offsets[0]]
    if template == 'symbolic-question':
        return [p, m+n, n-m, 1, p+offsets[0]]
    if source_replay:
        return [Fraction(base ** p), Fraction(1, base),
                Fraction(base ** (p+offsets[0])), Fraction(p+1),
                Fraction(base ** (p+offsets[1]))]
    exponents = numeric_exponents(base, offsets)
    if p not in exponents:
        raise ValueError('Correct power absent from numeric bank')
    return [Fraction(base ** p)] + [Fraction(base ** k) for k in exponents if k != p]


def side_cases(template):
    return ((-1,), (1,)) if template == 'numeric' else ((-2,), (-1,), (1,), (2,))


@lru_cache(None)
def domain(template, offsets):
    """Enumerate compatible values: profiles/sides are never lost to resampling."""
    results = []
    numeric = template == 'numeric'
    bases = range(2, 4) if numeric else ('x',)
    for base, m, n in itertools.product(bases, range(2, 5 if numeric else 6), range(2, 5 if numeric else 6)):
        if numeric and (m*n > 9 or base ** (m*n) > 729):
            continue
        bank = bank_values(template, base, m, n, offsets)
        if len(set(bank)) == 5:
            results.append((base, m, n))
    if not results:
        raise ValueError('Empty compatible domain')
    return tuple(results)


def identity(tag, value):
    return str(uuid.uuid5(uuid.UUID(KP['id']), tag + json.dumps(value, sort_keys=True)))


@checked_math_content
def generate(template, base, m, n, offsets, *, correct_position=0, seed=0, distractor_order=None, source_index=None):
    if template not in TEMPLATES:
        raise ValueError('Unsupported template')
    if type(m) is not int or type(n) is not int or m < 2 or n < 2:
        raise ValueError('Positive integer input exponents >=2 required')
    if not 0 <= correct_position < 5:
        raise ValueError('Choice position must be 0..4')
    numeric = template == 'numeric'
    if numeric and (type(base) is not int or base < 2):
        raise ValueError('Positive integer numeric base >=2 required')
    if not numeric and base not in BASES:
        raise ValueError('Unsupported symbolic base')
    values = bank_values(template, base, m, n, offsets, source_replay=source_index is not None)
    if len(set(values)) != 5:
        raise ValueError('Bank collision')
    p = m*n
    expression = rf'\left({base}^{{{m}}}\right)^{{{n}}}'
    if template == 'symbolic-equals':
        problem = f'${expression}=$'
    elif template == 'symbolic-question':
        problem = f'What is ${expression}$?'
    else:
        problem = f'Simplify ${expression}$.'
    intro = (f'First, we multiply the exponents and then we calculate the resulting power of ${base}$.'
             if numeric else 'We multiply the exponents, as follows:')
    steps = [expression, rf'{base}^{{{m}\cdot {n}}}', power(base, p)]
    if numeric:
        steps.append(str(base ** p))
    solution = intro + '\n\n$$\n\\begin{aligned}\n' + steps[0]
    for step in steps[1:]:
        solution += ' &= ' + step + r' \\' + '\n'
    solution = solution.rstrip('\n').removesuffix(r' \\') + '\n\\end{aligned}\n$$'
    problem, solution = normalize_prose(problem), normalize_prose(solution)
    if numeric:
        def tex(v):
            return str(v.numerator) if v.denominator == 1 else rf'\frac{{{v.numerator}}}{{{v.denominator}}}'
    else:
        def tex(v):
            return power(base, v)
    texts = [normalize_tex(tex(v)) for v in values]
    # Identity includes the complete bank and solution, independent of order/seed.
    qid = identity('question:', [problem, solution, sorted(texts)])
    fid = identity('field:', [qid, 'selection'])
    answers = [{':answer/id': identity('answer:', [fid, t]), ':answer/type': ':answer.type/math', ':answer/value': t} for t in texts]
    order = list(distractor_order if distractor_order is not None else range(1, 5))
    if sorted(order) != [1, 2, 3, 4]:
        raise ValueError('distractor_order must be a permutation of 1..4')
    order.insert(correct_position, 0)
    profile = ('N-source' if source_index is not None else ('N-low' if offsets[0] < 0 else 'N-high')) if numeric else PROFILES[template]
    params = {'template': template, 'profile': profile, 'base': base, 'm': m, 'n': n, 'offsets': list(offsets)}
    source = next(c for c in SOURCE['cases'] if c['parameters']['template'] == template)['source']
    metadata = {'version': VERSION, 'template': template, 'profile': profile, 'seed': seed,
                'parameters': params, 'source_question_id': source[':question/id'],
                'source_difficulty': source.get(':question/difficulty', {}).get(':db/ident'),
                'correct_position': correct_position, 'correct_rank': sorted(values).index(values[0])+1,
                'domain': 'instructional-account.md', 'bank_extension': source_index is None,
                'distractor_recipes': ((['1/b', 'b^(mn+d1)', 'mn+1', 'b^(mn+d2)'] if source_index is not None
                                       else [f'b^{k}' for k in numeric_exponents(base, offsets) if k != p]) if numeric
                                      else {'S1': ['m+n', 'm-n', 'n', 'mn+d'],
                                            'S2': ['m+n', 'n-m', '1', 'mn+d']}[PROFILES[template]])}
    if source_index is not None:
        metadata['source_replay_index'] = source_index
        metadata['missing_source_fields_repaired'] = source_index == 1
    return {'knowledge_point': KP.copy(), 'question': {':question/id': qid,
            ':question/difficulty': ':question.difficulty/easy', ':question/problem': problem,
            ':question/worked-solution': solution, ':question/answer-fields': [{':answer-field/id': fid,
            ':answer-field/key': 'selection', ':answer-field/type': ':answer-field.type/radio',
            ':answer-field/choices': [answers[i] for i in order],
            ':answer-field/correct': [':answer/id', answers[0][':answer/id']]}]},
            'generation': metadata, 'assets': []}


def replay():
    return [generate(**{k:v for k,v in case['parameters'].items() if k != 'profile'}, source_index=i) for i, case in enumerate(SOURCE['cases'])]


def sample(difficulty, count, seed):
    if difficulty not in ('easy', 'unclassified'):
        raise ValueError(f'Unsupported difficulty: {difficulty}; supported: easy')
    if count < 0:
        raise ValueError('count must be nonnegative')
    rng = random.Random(seed)
    result = []
    seen = set()
    attempts = 0
    while len(result) < count:
        attempts += 1
        if attempts > max(1000, count*100):
            raise ValueError('Requested batch exceeds practical unique sampling capacity')
        template = rng.choice(TEMPLATES)
        offsets = rng.choice(side_cases(template))
        position = rng.randrange(5)
        base, m, n = rng.choice(domain(template, offsets))
        if template != 'numeric':
            base = rng.choice(BASES)
        order = list(range(1, 5))
        rng.shuffle(order)
        record = generate(template, base, m, n, offsets, correct_position=position, seed=seed, distractor_order=order)
        qid = record['question'][':question/id']
        if qid in seen:
            continue
        seen.add(qid)
        record['generation']['batch_draw_number'] = attempts
        result.append(record)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy', choices=('easy', 'moderate', 'hard', 'unclassified'))
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json',), default='json')
    parser.add_argument('--replay-source', action='store_true', help='Replay original parameters and complete banks')
    args = parser.parse_args()
    try:
        if args.difficulty not in ('easy', 'unclassified'):
            raise ValueError(f'Unsupported difficulty: {args.difficulty}; supported: easy')
        records = replay() if args.replay_source else sample(args.difficulty, args.count, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
