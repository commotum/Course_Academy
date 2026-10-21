#!/usr/bin/env python3
"""Seeded, relocatable power-rule question generator; no external state or assets."""
import argparse
from fractions import Fraction as F
from functools import lru_cache
import itertools
import json
from math import gcd
from pathlib import Path
import random
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

KP = {'db_id': 17592186064304, 'id': 'acc85958-ad98-5ce2-912c-e2ba70d025ca',
      'title': 'Simplifying Challenging Expressions Using the Power Rule'}
SOURCE = {'A': 'q-23277', 'B': 'q-22798', 'R': 'q-34432'}
NAMESPACE = uuid.UUID(KP['id'])
VERSION = '1.2.0'


def tex(value):
    value = F(value)
    sign = '-' if value < 0 else ''
    value = abs(value)
    return sign + (str(value.numerator) if value.denominator == 1 else
                   rf'\frac{{{value.numerator}}}{{{value.denominator}}}')


def power(base, value):
    return rf'{{{base}}}^{{{tex(value)}}}'


def bank(profile, values, *, key_slot=None, peer_bank=None):
    if profile in ('A', 'B'):
        p, q, r = values
        k = F(p*r-q)
        if key_slot is not None:
            if key_slot not in range(4):
                raise ValueError('S-neighbor key slot must be 0..3')
            return [k+i-key_slot for i in range(4)] + [F(p, q)], k
        if profile == 'A':
            return [F(p*r)-F(q, 2), F(p*r, q), k, F(p), F(p*r+q)], k
        return [F(p+r+q), k, F(p+r-q), F(2*p*r-q), F(p*r+q)], k
    a, b, c = values
    k = F(a, b*c)
    if peer_bank is not None:
        peers = radical_banks()[c, sign_case(k)][peer_bank]
        if key_slot not in range(5) or tuple(values) != peers[key_slot]:
            raise ValueError('R-peer target must match the selected bank role')
        return [F(x, y*z) for x, y, z in peers], k
    return [abs(1/k), abs(k), -abs(k), k*F(b, c), -abs(1/k)], k


def sign_case(key):
    return 'negative' if key < 0 else 'positive' if key > 0 else 'zero'


@lru_cache(None)
def radical_banks():
    """Every complete peer bank permits each of its five members as target."""
    result = {}
    for c, sign in itertools.product(range(2, 6), (-1, 1)):
        values = [(sign*a, b, c) for a, b in
                  itertools.product(range(2, 13), range(2, 8))
                  if gcd(a, b) == 1 and F(a, b*c).denominator != 1]
        values.sort(key=lambda v: F(v[0], v[1]*v[2]))
        result[c, sign_case(sign)] = [
            tuple(values[(start+i) % len(values)] for i in range(5))
            for start in range(len(values))]
    return result


@lru_cache(None)
def pools(key_slot=None):
    result = {}
    for profile in ('A', 'B'):
        for case in ('negative', 'zero', 'positive'):
            result[profile, case] = []
        for values in itertools.product(range(2, 15), tuple(range(-16, 0, 2))+tuple(range(2, 17, 2)), range(2, 5)):
            choices, k = bank(profile, values, key_slot=key_slot)
            if len(set(choices)) == 5:
                result[profile, sign_case(k)].append(values)
    for case in ('negative', 'positive'):
        result['R', case] = []
    for a, b, c in itertools.product(range(2, 13), range(2, 8), range(2, 6)):
        if gcd(a, b) != 1 or F(a, b*c).denominator == 1:
            continue
        for sign in (-1, 1):
            values = (sign*a, b, c)
            choices, k = bank('R', values)
            if len(set(choices)) == 5:
                result['R', sign_case(k)].append(values)
    assert all(result.values())
    return result


@checked_math_content
def build(profile, values, *, names=None, order=None, source_prompt=None, key_slot=None, peer_bank=None):
    """Render one shared mathematical instance, also used for controlled replay."""
    values = tuple(values)
    if peer_bank is not None and profile != 'R':
        raise ValueError('Only R-peer has a peer bank')
    if key_slot is not None and profile == 'R' and peer_bank is None:
        raise ValueError('R key slot requires a peer bank')
    choices, k = bank(profile, values, key_slot=key_slot, peer_bank=peer_bank)
    if len(set(choices)) != 5:
        raise ValueError('Colliding source-bank recipes')
    if profile in ('A', 'B'):
        p, q, r = values
        base, numerator, denominator = names or ('a', 't', 's')
        target = rf'\frac{{{power(numerator, r)}}}{{{denominator}}}'
        substituted = rf'\frac{{\left({power(base, p)}\right)^{{{r}}}}}{{{power(base, q)}}}'
        problem = (f'For ${base}>1$, given that ${power(base, p)}={numerator}$ and '
                   f'${power(base, q)}={denominator}$, what is the value of ${target}$?')
        solution = ('First, we carry out the substitution\n\n$$\n'
                    f'{target}={substituted}\n$$\n\n'
                    'Then, we apply the power rule followed by the quotient rule:\n\n$$\n'
                    r'\begin{aligned}' + substituted + ' &= '
                    + rf'\frac{{{base}^{{{p}\cdot {r}}}}}{{{power(base, q)}}}'
                    + r' \\ &= ' + rf'\frac{{{power(base, p*r)}}}{{{power(base, q)}}}'
                    + r' \\ &= ' + (rf'{base}^{{{p*r}-({q})}}' if q<0 else rf'{base}^{{{p*r}-{q}}}')
                    + r' \\ &= ' + power(base, k) + r'\end{aligned}' + '\n$$')
        answer_values = [power(base, v) for v in choices]
        difficulty = 'moderate'
        names = (base, numerator, denominator)
    elif profile == 'R':
        a, b, c = values
        base, target = names or ('z', 'k')
        h = F(a, b)
        root = rf'\sqrt[{c}]{{{power(base, h)}}}' if c != 2 else rf'\sqrt{{{power(base, h)}}}'
        problem = f'For ${base}>1$, if ${root}={base}^{{{target}}}$, then ${target}=$'
        solution = ('First, we express the radical as a fractional power and then we apply the power rule:\n\n$$\n'
                    r'\begin{aligned}' + root + ' &= '
                    + rf'\left({power(base, h)}\right)^{{1/{c}}}'
                    + r' \\ &= ' + rf'{base}^{{\left({tex(h)}\right)\left(\frac{{1}}{{{c}}}\right)}}'
                    + r' \\ &= ' + power(base, k) + r'\end{aligned}'
                    + f'\n$$\n\nHence, ${target}={tex(k)}$.')
        answer_values = [tex(v) for v in choices]
        difficulty = 'hard'
        names = (base, target)
    else:
        raise ValueError('Unknown profile')
    problem = normalize_prose(source_prompt or problem)
    solution = normalize_prose(solution)
    answer_values = [normalize_tex(v) for v in answer_values]
    identity = json.dumps([problem, sorted(answer_values)], separators=(',', ':'))
    qid = uuid.uuid5(NAMESPACE, identity)
    fid = uuid.uuid5(qid, 'selection')
    answers = [{':answer/id': str(uuid.uuid5(fid, v)), ':answer/type': ':answer.type/math',
                ':answer/value': v} for v in answer_values]
    correct = answers[choices.index(k)][':answer/id']
    order = list(range(5)) if order is None else list(order)
    if sorted(order) != list(range(5)):
        raise ValueError('Order must be a permutation')
    return {'knowledge_point': KP.copy(), 'question': {
        ':question/id': str(qid), ':question/difficulty': ':question.difficulty/' + difficulty,
        ':question/problem': problem, ':question/worked-solution': solution,
        ':question/answer-fields': [{':answer-field/id': str(fid), ':answer-field/key': 'selection',
            ':answer-field/type': ':answer-field.type/radio',
            ':answer-field/choices': [answers[i] for i in order],
            ':answer-field/correct': [':answer/id', correct]}]},
        'generation': {'generator_version': VERSION, 'template': 'radical' if profile == 'R' else 'substitution',
            'profile': profile, 'bank_profile': 'R-peer' if peer_bank is not None else 'S-neighbor' if key_slot is not None else profile,
            'peer_bank': peer_bank,
            'key_slot': key_slot, 'parameters': list(values), 'names': list(names), 'order': order,
            'case': sign_case(k), 'source_reference': SOURCE[profile],
            'source_difficulty': difficulty, 'domain': f'{names[0]}>1',
            'key_rational': [k.numerator, k.denominator], 'dependencies': {'python': '3.13.5', 'packages': {}}}}


def replay_sources():
    source = {q[':question/math-academy-id']: q for q in
              json.loads(Path(__file__).with_name('source_cases.json').read_text())}
    instances = [('A', (12, 4, 3), ('a', 't', 's')), ('B', (9, 2, 3), ('b', 'x', 'y')),
                 ('R', (-6, 5, 3), ('z', 'k'))]
    return [build(profile, values, names=names, source_prompt=source[SOURCE[profile]][':question/problem'])
            for profile, values, names in instances]


def generate(difficulty, count, seed):
    if difficulty == 'unclassified':
        difficulty = 'moderate'
    if difficulty not in ('moderate', 'hard'):
        raise ValueError('Supported difficulty bands: moderate, hard')
    if count < 0:
        raise ValueError('Count must be nonnegative')
    rng = random.Random(seed)
    result, seen = [], set()
    attempts = 0
    while len(result) < count:
        attempts += 1
        if attempts > max(1000, 100*count):
            raise ValueError('Requested count exceeds practical unique instance capacity')
        profile = rng.choice(('A', 'B')) if difficulty == 'moderate' else 'R'
        case = rng.choice(('negative', 'zero', 'positive') if difficulty == 'moderate' else ('negative', 'positive'))
        if difficulty == 'moderate':
            key_slot = rng.randrange(4)
            peer_bank = None
            values = rng.choice(pools(key_slot)[profile, case])
        else:
            key_slot = rng.randrange(5)
            c = rng.choice(range(2, 6))
            peer_bank = rng.randrange(len(radical_banks()[c, case]))
            values = radical_banks()[c, case][peer_bank][key_slot]
        names = rng.choice((('a', 't', 's'), ('b', 'x', 'y'))) if difficulty == 'moderate' else rng.choice((('z', 'k'), ('x', 'n')))
        semantic = ('radical' if profile == 'R' else 'substitution', values)
        if semantic in seen:
            continue
        order = list(range(5)); rng.shuffle(order)
        record = build(profile, values, names=names, order=order, key_slot=key_slot, peer_bank=peer_bank)
        record['generation'].update(seed=seed, sample_index=len(result), sampler_attempt=attempts)
        result.append(record); seen.add(semantic)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='moderate', choices=['unclassified', 'easy', 'moderate', 'hard'])
    parser.add_argument('--count', default=5, type=int)
    parser.add_argument('--seed', default=0, type=int)
    parser.add_argument('--format', choices=['json'], default='json')
    parser.add_argument('--replay-source', action='store_true')
    args = parser.parse_args()
    try:
        records = replay_sources() if args.replay_source else generate(args.difficulty, args.count, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(records, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
