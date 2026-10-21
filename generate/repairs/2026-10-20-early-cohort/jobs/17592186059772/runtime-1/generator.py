#!/usr/bin/env python3
"""Seeded, relocatable augmented-matrix row-operation generator."""
import argparse
import copy
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
import random
from pathlib import Path
import uuid

from math_format import checked_math_content, matrix_tex, normalize_prose, normalize_tex

import hard_ops
import moderate_ops

VERSION = '1.2.1'
KP = {'db_id': 17592186059772, 'id': 'c27a3f3c-77c7-55e9-8714-1f24c4a48063',
      'title': 'Applying Row Operations To an Augmented Matrix'}
SOURCES = {'swap': '926d4b45-89b4-5d26-9733-b0d97c69c160',
           'scale': '0f08a2c2-eb16-5d85-a714-beb36e4a0c94'}
FACTORS = tuple(str(n) for n in range(-8, 9) if n not in (0, 1)) + ('-1/2', '-1/3', '1/2', '1/3')
# Symmetric eligibility prevents the bank from identifying the key by its size.
DISTRACTOR_FACTORS = FACTORS
ORDINAL = ('first', 'second', 'third')


@lru_cache(maxsize=1)
def easy_source_data():
    return json.loads(Path(__file__).with_name('easy_sources.json').read_text())


def tex(value):
    x = Fraction(value)
    if x.denominator == 1:
        return str(x.numerator)
    return ('-' if x < 0 else '') + rf'\frac{{{abs(x.numerator)}}}{{{x.denominator}}}'


def matrix(rows):
    return matrix_tex([[tex(x) if not isinstance(x, str) else x for x in row]
                       for row in rows], augmented=True)


def source_instances():
    return [
        {'template': 'swap', 'matrix': [[4, -1, 9], [6, 5, -6], [-1, -9, 1]],
         'pair': [0, 1], 'letter': 'A'},
        {'template': 'scale', 'matrix': [[1, 3, 8, -1], [7, 1, -9, 4], [6, -3, 9, 0]],
         'target': 2, 'factor': '-1/3', 'columns': [0, 1, 2], 'extra_row': 0, 'letter': 'A'},
    ] + [copy.deepcopy(item['instance']) for item in easy_source_data()]


def bank(instance):
    """Return complete source-profile bank, correct index, and recipe names."""
    if instance['template'] == 'add':
        return moderate_ops.bank(instance)
    if instance['template'] in ('swap-add', 'scale-add'):
        return hard_ops.bank(instance)
    if instance.get('profile', '').startswith('source:'):
        item = next((x for x in easy_source_data()
                     if x['instance']['profile'] == instance['profile']), None)
        if item is None:
            raise ValueError('Unknown easy source bank profile')
        for name in ('template', 'matrix', 'target', 'factor'):
            if instance[name] != item['instance'][name]:
                raise ValueError('Source-only bank cannot be used with changed mathematical parameters')
        return copy.deepcopy(item['bank']), item['correct_index'], item['recipes'][:]
    m = [[Fraction(x) for x in row] for row in instance['matrix']]
    if instance['template'] == 'swap':
        i, j = instance['pair']
        u = next(r for r in range(3) if r not in (i, j))
        # Source permutations expressed relative to requested pair and untouched row.
        relative = ((1, 2, 0), (2, 0, 1), (0, 1, 2), (2, 1, 0), (1, 0, 2))
        roles = (i, j, u)
        result = []
        for permutation in relative:
            out = copy.deepcopy(m)
            for dest, source in enumerate(permutation):
                out[roles[dest]] = m[roles[source]][:]
            result.append(out)
        return result, 4, ['cycle-1', 'cycle-2', 'unchanged', 'wrong-pair', 'correct']
    t, k = instance['target'], Fraction(instance['factor'])
    if instance.get('profile') == 'scale-factor-comparison':
        factors = [k] + [Fraction(f) for f in instance['wrong_factors']]
        if len(factors) != 5 or len(set(factors)) != 5 or any(f in (0, 1) for f in factors):
            raise ValueError('Factor comparison requires five distinct nonidentity factors')
        result = [copy.deepcopy(m) for _ in factors]
        for out, factor in zip(result, factors):
            out[t] = [factor*x for x in m[t]]
        return result, 0, ['correct'] + ['wrong-factor:' + str(f) for f in factors[1:]]
    a, b, c = instance['columns']
    e = instance['extra_row']
    result = [copy.deepcopy(m) for _ in range(5)]
    result[0][t][c] *= k
    result[1][t][a] *= k
    for index in (2, 3):
        result[index][t] = [k*x for x in m[t]]
    result[2][e][b] *= k
    for row in result[4]:
        row[c] *= k
    return result, 3, ['partial-c', 'partial-a', 'extra-cell', 'correct', 'column-c']


@checked_math_content
def build(instance, *, order=None, seed=None):
    m = instance['matrix']
    letter = instance.get('letter', 'A')
    original = matrix(m)
    values, key, recipes = bank(instance)
    if len({matrix(v) for v in values}) != 5:
        raise ValueError('Degenerate instance: complete profile must contain five distinct matrices')
    if instance['template'] == 'add':
        problem, solution = moderate_ops.render(instance, matrix, tex)
        profile = instance['profile']
    elif instance['template'] in ('swap-add', 'scale-add'):
        problem, solution = hard_ops.render(instance, matrix, tex)
        profile = instance.get('profile', 'sequence-comparison')
    elif instance['template'] == 'swap':
        i, j = instance['pair']
        operation = rf'R_{{{i+1}}}\leftrightarrow R_{{{j+1}}}'
        interpretation = (f'The operation ${operation}$ means that we need to swap '
                          f'the {ORDINAL[i]} and {ORDINAL[j]} rows.')
        steps = original + rf'\,{operation} \\ &\sim ' + matrix(values[key])
        lead = 'Applying this row operation, we obtain the following:'
        profile = 'swap-permutations'
    else:
        t, k = instance['target'], tex(instance['factor'])
        operation = rf'R_{{{t+1}}}:={k}R_{{{t+1}}}'
        interpretation = (f'The operation ${operation}$ means that we need to multiply '
                          f'the {ORDINAL[t]} row of the matrix by ${k}.$')
        products = [[tex(x) for x in row] for row in m]
        products[t] = [k + r'\cdot ' + ('(' + tex(x) + ')' if Fraction(x) < 0 else tex(x)) for x in m[t]]
        steps = (original + rf'\,{operation} \\ &\sim ' + matrix(products)
                 + r' \\ &\sim ' + matrix(values[key]))
        lead = f'Multiplying the ${t+1}$' + ('st', 'nd', 'rd')[t] + f' row by ${k}$, we obtain the following:'
        profile = instance.get('profile', 'scale-partial-column')
    if instance['template'] not in ('add', 'swap-add', 'scale-add'):
        problem = (f'Consider the augmented matrix ${letter},$ given by\n\n$$\n'
                   f'{letter}={original}.\n$$\n\n'
                   f'What matrix results from carrying out the row operation ${operation}$ on ${letter}?$')
        solution = (interpretation + '\n\n' + lead + '\n\n$$\n'
                    + r'\begin{aligned}' + f'{letter} &= ' + steps + r'\end{aligned}' + '\n$$')
    problem, solution = normalize_prose(problem), normalize_prose(solution)
    answers = [normalize_tex(matrix(v)) for v in values]
    identity = json.dumps([problem, sorted(answers), answers[key]], separators=(',', ':'))
    qid = uuid.uuid5(uuid.UUID(KP['id']), identity)
    fid = uuid.uuid5(qid, 'field:selection')
    aids = [str(uuid.uuid5(fid, a)) for a in answers]
    order = list(range(5)) if order is None else list(order)
    if sorted(order) != list(range(5)):
        raise ValueError('Choice order must be a permutation')
    difficulty = ('moderate' if instance['template'] == 'add' else
                  'hard' if instance['template'] in ('swap-add', 'scale-add') else 'easy')
    source_ids = ([profile.removeprefix('source:')] if profile.startswith('source:') else
                  [x['instance']['profile'].removeprefix('source:') for x in moderate_ops.source_data()]
                  if difficulty == 'moderate' else
                  [hard_ops.HARD_SOURCES[profile]] if profile in hard_ops.HARD_SOURCES else
                  list(hard_ops.HARD_SOURCES.values()) if difficulty == 'hard' else [SOURCES[instance['template']]])
    question = {
        ':question/id': str(qid), ':question/difficulty': ':question.difficulty/' + difficulty,
        ':question/problem': problem, ':question/worked-solution': solution,
        ':question/answer-fields': [{':answer-field/id': str(fid), ':answer-field/key': 'selection',
            ':answer-field/type': ':answer-field.type/radio',
            ':answer-field/correct': [':answer/id', aids[key]],
            ':answer-field/choices': [{':answer/id': aids[i], ':answer/type': ':answer.type/math',
                                      ':answer/value': answers[i]} for i in order]}],
    }
    return {'knowledge_point': KP.copy(), 'question': question, 'assets': {},
            'generation': {'generator_version': VERSION, 'template': instance['template'],
                           'profile': profile, 'source_question_ids': source_ids,
                           'difficulty': difficulty, 'seed': seed, 'instance': copy.deepcopy(instance),
                           'recipes_in_display_order': [recipes[i] for i in order],
                           'semantic_hash': hashlib.sha256(json.dumps(
                               {k: v for k, v in instance.items() if k in ('template', 'matrix', 'pair', 'target', 'factor', 'donor', 'coefficient', 'scale')},
                               sort_keys=True).encode()).hexdigest()}}


def sample(rng, template=None):
    template = template or rng.choice(('swap', 'scale'))
    # Decide instructional roles before compatible arithmetic data.
    inst = {'template': template}
    if template == 'swap':
        inst['pair'] = sorted(rng.sample(range(3), 2))
    else:
        inst.update(target=rng.randrange(3), factor=rng.choice(FACTORS),
                    profile='scale-factor-comparison')
        inst['wrong_factors'] = rng.sample([f for f in DISTRACTOR_FACTORS if f != inst['factor']], 4)
    for attempt in range(1, 1001):
        width = 3 if template == 'swap' else 4
        m = [[rng.randint(-9, 9) for _ in range(width)] for _ in range(3)]
        if template == 'scale':
            t = inst['target']
            # Compatibility must treat every possible key in this bank equally.
            d = math.lcm(*(Fraction(f).denominator for f in
                           [inst['factor']] + inst['wrong_factors']))
            bound = min(3, 9 // d)
            m[t] = [d*rng.randint(-bound, bound) for _ in range(width)]
            if sum(x != 0 for x in m[t]) < 2:
                continue
        inst['matrix'] = m
        vals, _, _ = bank(inst)
        if len({matrix(v) for v in vals}) == 5:
            inst['entry_attempts'] = attempt
            inst['letter'] = rng.choice(('A', 'M', 'N', 'T', 'U', 'V', 'X'))
            return inst
    raise RuntimeError('Unable to fill compatible entries for chosen roles')


@checked_math_content
def generate(rng, *, difficulty='easy', seed=None, template=None):
    if difficulty not in ('easy', 'moderate', 'hard', 'unclassified'):
        raise ValueError('Unsupported difficulty')
    if difficulty == 'unclassified':
        difficulty = 'hard'
    inst = (moderate_ops.sample(rng) if difficulty == 'moderate' else
            hard_ops.sample(rng, template) if difficulty == 'hard' else sample(rng, template))
    order = list(range(5))
    rng.shuffle(order)
    return build(inst, order=order, seed=seed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=('unclassified', 'easy', 'moderate', 'hard'), default='moderate')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json',), default='json')
    args = parser.parse_args()
    if args.count < 0:
        parser.error('--count must be nonnegative')
    rng = random.Random(args.seed)
    print(json.dumps([generate(rng, difficulty=args.difficulty, seed=args.seed)
                      for _ in range(args.count)], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
