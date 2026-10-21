#!/usr/bin/env python3
"""Relocatable, database-free radical-to-unit-fraction practice generator."""
import argparse
import json
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import random
import uuid

from math_format import checked_math_content, normalize_prose, normalize_tex

KP = {'db_id': 17592186152131, 'id': 'e2d7fb12-c66c-524e-b9f6-1b86972c3520',
      'title': 'Converting a Radical to a Unit Fraction Exponent'}
VERSION = '1.3.0'
TEMPLATES = ('indexed-equation', 'indexed-what', 'square-equation')
SOURCES = {'indexed-equation': 'q-69218', 'indexed-what': 'q-69158', 'square-equation': 'q-69219'}


def domain(template, case=None):
    if template not in TEMPLATES:
        raise ValueError('Unknown template')
    values = list(range(2, 16))
    if template == 'square-equation':
        values += ['1.2', '1.4', '1.5', '1.6', '1.8', '2.5', '3.5', '4.5', '7.5']
    return [(x, n) for x in values
            for n in ([2] if template == 'square-equation' else range(3, 11))
            if (template == 'square-equation' or (x != n and (x, n) != (2, 4)))
            and (case is None or ('x<n' if Fraction(x) < n else ('x=n' if Fraction(x) == n else 'x>n')) == case)]


def power(base, numerator, denominator):
    return f'{{{base}}}^{{{numerator}/{denominator}}}'


def square_neighbors(x):
    """Both orientations of each same-appearance pair are eligible targets."""
    values = [a for a, _ in domain('square-equation') if isinstance(a, str) == isinstance(x, str)]
    i = values.index(x)
    return {d: values[i+d] for d in (-1, 1) if 0 <= i+d < len(values)}


@lru_cache(maxsize=1)
def indexed_profiles():
    """Complete banks permit all four prompt targets without duplicate values."""
    eligible = set(domain('indexed-equation'))
    result = []
    for bases in combinations(range(2, 16), 2):
        for indices in combinations(range(3, 11), 2):
            targets = list(product(bases, indices))
            if not all(target in eligible for target in targets):
                continue
            # a^(1/n) = b^(1/m) iff a^m = b^n for positive bases.
            if any(a**m == b**n for (a, n), (b, m) in combinations(targets, 2)):
                continue
            result.append((bases, indices))
    return tuple(result)


def bank(x, n, profile, foil_index=None, base_direction=1, inverted_base='target', indexed_bank=None):
    result = [power(x, 1, n), power(n, 1, x), power(x, n, 1), power(n, x, 1)]
    if profile == 'indexed-grid':
        bases = tuple(indexed_bank['bases'])
        indices = tuple(indexed_bank['indices'])
        if (bases, indices) not in indexed_profiles() or x not in bases or n not in indices:
            raise ValueError('Indexed bank must support every base/index assignment')
        u, v = indexed_bank['foil_numerator'], indexed_bank['foil_denominator']
        if u not in bases or v not in indices:
            raise ValueError('Indexed foil parameters must belong to the bank')
        result = [power(x, 1, n)] + [power(a, 1, b) for a, b in product(bases, indices) if (a, b) != (x, n)]
        # This source-style distractor is independent of which prompt is asked.
        result.append(power(1, u, v))
    elif profile == 'unit-base':
        result.append(power(1, x, n))
    elif profile == 'square-division':
        value = Fraction(x) / n
        result.append(str(value.numerator) if value.denominator == 1 else
                      rf'\frac{{{value.numerator}}}{{{value.denominator}}}')
    elif profile == 'square-index-confusion':
        if n != 2 or foil_index not in (1, 3, 4, 5):
            raise ValueError('Square foil index must be 1, 3, 4 or 5')
        if base_direction not in (-1, 1):
            raise ValueError('Base direction must be -1 or 1')
        # Pair only eligible targets; out-of-domain foils create answer-only cues.
        neighbors = square_neighbors(x)
        if base_direction not in neighbors:
            raise ValueError('Square base direction leaves the practice domain')
        other_base = neighbors[base_direction]
        if inverted_base not in ('target', 'other'):
            raise ValueError('Inverted base must be target or other')
        c = x if inverted_base == 'target' else other_base
        result = [power(x, 1, n), power(other_base, 1, n),
                  power(x, 1, foil_index), power(other_base, 1, foil_index), power(c, n, 1)]
    else:
        raise ValueError('Unknown profile')
    return result


@checked_math_content
def generate(x, n, template, *, order_seed=0, seed=None, foil_index=3, base_direction=None, inverted_base='target', source_bank=False, indexed_bank=None):
    if (x, n) not in domain(template):
        raise ValueError('Parameters outside supported nondegenerate domain')
    square = template == 'square-equation'
    profile = ('square-division' if source_bank else 'square-index-confusion') if square else ('unit-base' if source_bank else 'indexed-grid')
    if profile == 'indexed-grid' and indexed_bank is None:
        bases, indices = next((a, b) for a, b in indexed_profiles() if x in a and n in b)
        indexed_bank = {'bases': bases, 'indices': indices,
                        'foil_numerator': bases[0], 'foil_denominator': indices[0]}
    if profile == 'square-division' and x in (2, 4):
        raise ValueError('Degenerate source square-division bank')
    if profile == 'square-index-confusion' and base_direction is None:
        base_direction = 1 if 1 in square_neighbors(x) else -1
    radical = rf'\sqrt{{{x}}}' if square else rf'\sqrt[{n}]{{{x}}}'
    indexed = rf'\sqrt[{n}]{{{x}}}'
    prompt = f'What is ${radical}$?' if template == 'indexed-what' else f'${radical}=$'
    values = [normalize_tex(v) for v in bank(x, n, profile, foil_index, base_direction, inverted_base, indexed_bank)]
    correct = values[0]
    solution = (r'The radical $\sqrt[n]{x}$ can be written using a fractional exponent as ${x}^{1/n}.$'
                '\n\n' + rf'Comparing $\sqrt[n]{{x}}$ with ${indexed},$ we get $x={x},$ and $n={n}.$ Therefore,'
                '\n\n$$\n' + (radical + '=' if square else '') + indexed + '=' + correct + '\n$$')
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    identity = json.dumps([template, x, n, profile, prompt, solution, sorted(values)], sort_keys=True)
    qid = uuid.uuid5(uuid.UUID(KP['id']), identity)
    fid = uuid.uuid5(qid, 'selection')
    choices = [{':answer/id': str(uuid.uuid5(fid, value)), ':answer/type': ':answer.type/math',
                ':answer/value': value} for value in values]
    correct_id = choices[0][':answer/id']
    random.Random(order_seed).shuffle(choices)
    return {'knowledge_point': dict(KP), 'question': {
        ':question/id': str(qid), ':question/difficulty': ':question.difficulty/easy',
        ':question/problem': prompt, ':question/worked-solution': solution,
        ':question/answer-fields': [{':answer-field/id': str(fid), ':answer-field/key': 'selection',
          ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
          ':answer-field/correct': [':answer/id', correct_id]}]},
        'generation': {'generator_version': VERSION, 'template': template, 'profile': profile,
           'indexed_bank': indexed_bank if profile == 'indexed-grid' else None,
           'seed': seed, 'order_seed': order_seed, 'parameters': {'x': x, 'n': n},
           'foil_index': foil_index if profile == 'square-index-confusion' else None,
           'base_direction': base_direction if profile == 'square-index-confusion' else None,
           'inverted_base': inverted_base if profile == 'square-index-confusion' else None,
           'foil_case': ('below-index' if foil_index < n else 'above-index') if profile == 'square-index-confusion' else None,
           'decision_case': 'x<n' if Fraction(x) < n else ('x=n' if Fraction(x) == n else 'x>n'), 'source_question': SOURCES[template],
           'source_difficulty': None if template == 'indexed-what' else 'easy',
           'domain': 'indexed x=2..15,n=3..10,x!=n,(x,n)!=(2,4); square n=2,x=2..15 or declared positive decimals, neighboring eligible bases'}}


def generate_batch(difficulty='easy', count=5, seed=0):
    if difficulty not in ('easy', 'unclassified'):
        raise ValueError('Only easy is supported')
    capacity = len({(str(x), n) for t in TEMPLATES for x, n in domain(t)})
    if count < 0 or count > capacity:
        raise ValueError(f'count must be between 0 and {capacity} distinct semantic instances')
    # Indexed items draw a complete bank, then a compatible prompt target.
    # Square items draw the foil case before the compatible radicand.
    # Build valid domains directly: there is no rejection loop.
    rng = random.Random(seed)
    records, used = [], set()
    for _ in range(count):
        eligible = {t: {c: [(x,n) for x,n in domain(t,c) if (str(x),n) not in used]
                        for c in ('x<n','x=n','x>n')} for t in TEMPLATES}
        template = rng.choice([t for t in TEMPLATES if any(eligible[t].values())])
        if template != 'square-equation':
            # Draw a complete bank before the prompt's answer-bearing roles.
            # Each base/index combination is a legitimate target. The base-1
            # foil is sampled independently, so it cannot encode the key.
            profiles = [(bases, indices) for bases, indices in indexed_profiles()
                        if any((str(x), n) not in used for x, n in product(bases, indices))]
            bases, indices = rng.choice(profiles)
            available = [(x, n) for x, n in product(bases, indices) if (str(x), n) not in used]
            x, n = rng.choice(available)
            indexed_bank = {'bases': bases, 'indices': indices,
                            'foil_numerator': rng.choice(bases), 'foil_denominator': rng.choice(indices)}
            used.add((str(x), n))
            records.append(generate(x, n, template, order_seed=rng.getrandbits(64), seed=seed,
                                    indexed_bank=indexed_bank))
            continue
        # Draw the distractor's index case before choosing the radicand.
        foil_case = rng.choice(('below-index', 'above-index')) if template == 'square-equation' else None
        foil_index = rng.choice((1,) if foil_case == 'below-index' else (3, 4, 5)) if foil_case else 3
        base_direction = rng.choice((-1, 1)) if foil_case else 1
        inverted_base = rng.choice(('target', 'other')) if foil_case else 'target'
        if foil_case:
            eligible[template] = {c: [(x,n) for x,n in values if base_direction in square_neighbors(x)]
                                  for c, values in eligible[template].items()}
            # At batch exhaustion only one orientation may remain available.
            if not any(eligible[template].values()):
                base_direction = -base_direction
                eligible[template] = {c: [(x,n) for x,n in domain(template,c)
                                         if (str(x),n) not in used and base_direction in square_neighbors(x)]
                                      for c in ('x<n','x=n','x>n')}
        case = rng.choice([c for c, values in eligible[template].items() if values])
        x, n = rng.choice(eligible[template][case])
        used.add((str(x), n))
        records.append(generate(x, n, template, order_seed=rng.getrandbits(64), seed=seed, foil_index=foil_index, base_direction=base_direction, inverted_base=inverted_base))
    return records


def source_replay():
    """Construct original parameters using the same templates and complete recipes."""
    originals = json.loads(Path(__file__).with_name('source_cases.json').read_text())['questions']
    records = [generate(2, 7, 'indexed-what', source_bank=True), generate(10, 2, 'square-equation', source_bank=True),
               generate(5, 3, 'indexed-equation', source_bank=True)]
    for record, original in zip(records, originals):
        record['generation']['source_id'] = original[':question/id']
        record['generation']['source_missing_fields'] = [k for k in (':question/difficulty', ':question/worked-solution') if k not in original]
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy', choices=('easy', 'moderate', 'hard', 'unclassified'))
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json',), default='json')
    args = parser.parse_args()
    try:
        records = generate_batch(args.difficulty, args.count, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
