#!/usr/bin/env python3
"""Calculator change-of-base practice. All runtime dependencies are local or stdlib."""
import argparse
from functools import lru_cache
from math import gcd
from decimal import Decimal, localcontext, ROUND_HALF_UP
import json
from pathlib import Path
import random
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

KP = {'db_id': 17592186054745, 'id': 'bccd26ff-1dc5-5817-962b-a1ef1f46b2fb',
      'title': 'Evaluating a Logarithm With a Calculator Using the Change of Base Formula'}
PROFILES = {'p2': (2, [128, 135, 148, 163, 188], 'q-100672'),
            'p3': (3, [714, 765, 812, 893, 917], 'q-108372')}
VERSION = '1.1.0-nontrivial-change-of-base'


def primitive_base(n):
    """Unique integer root after removing the gcd of prime exponents."""
    factors = []
    divisor = 2
    while divisor * divisor <= n:
        exponent = 0
        while n % divisor == 0:
            n //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor += 1
    if n > 1:
        factors.append((n, 1))
    common = 0
    for _, exponent in factors:
        common = gcd(common, exponent)
    root = 1
    for prime, exponent in factors:
        root *= prime ** (exponent // common)
    return root


def requires_change_of_base(a, x):
    # Common logarithms need no base conversion; equal/common-power inputs can
    # be evaluated by logarithm identities instead of the assessed method.
    return a != 10 and x > 1 and primitive_base(a) != primitive_base(x)


def evaluate(a, x, places):
    with localcontext() as ctx:
        ctx.prec = 60
        numerator, denominator = Decimal(x).log10(), Decimal(a).log10()
        value = numerator / denominator
        answer = value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)
        return answer, numerator, denominator


def region(a, x):
    return 'below' if x < a else 'equal' if x == a else 'above'


@checked_math_content
def generate(a, x, places, *, profile='blank', rank=0, seed=0,
             source=None, notice=False):
    if not (isinstance(a, int) and isinstance(x, int) and a > 1 and x > 0 and places in (2, 3)):
        raise ValueError('Positive integer inputs, base > 1 and 2 or 3 places required')
    if not (source or {}).get('source_replay') and not requires_change_of_base(a, x):
        raise ValueError('Standalone practice must require change of base; identity/common-power shortcuts are excluded')
    if profile not in ('blank', *PROFILES):
        raise ValueError('Unsupported response profile')
    if profile != 'blank' and (places != PROFILES[profile][0] or rank not in range(5)):
        raise ValueError('Profile precision / correct rank mismatch')
    answer, numerator, denominator = evaluate(a, x, places)
    fmt = lambda v: normalize_tex(f'{v:.{places}f}')
    correct_value = fmt(answer)
    values = [correct_value]
    if profile != 'blank':
        lattice = PROFILES[profile][1]
        unit = Decimal(1).scaleb(-places)
        values = [fmt(answer + (point - lattice[rank]) * unit) for point in lattice]
    key = 'field-1' if profile == 'blank' else 'selection'
    kind = 'blank' if profile == 'blank' else 'radio'
    expression = rf'\log_{{{a}}}({x})'
    prompt = f'Use a calculator to evaluate ${expression}$ rounded to ${places}$ decimal places.'
    if kind == 'blank':
        prompt += f'\n\n${expression} \\approx$\n{{{{{key}}}}}'
    if notice:
        prompt += '\n\n> A scientific calculator is required to answer this question.'
    def intermediate(value):
        if value == value.to_integral():
            return str(int(value))
        return f'{value:.{places + 3}f}'
    solution = (
        f"Let's calculate ${expression}$ by changing the base ${a}$ to the common logarithm (base $10$).\n\n"
        'We use the change of base formula:\n\n$$\n'
        r'\log_a X=\frac{\log_b X}{\log_b a}' + '\n$$\n\n'
        f'In our case, $a={a},$ $X={x},$ $b=10.$ So, we have\n\n$$\n'
        + rf'\begin{{aligned}}{expression} & =\frac{{\log_{{10}}({x})}}{{\log_{{10}}({a})}}'
        + r' \\ & =' + rf'\frac{{\log({x})}}{{\log({a})}}'
        + r' \\ & \approx ' + rf'\frac{{{intermediate(numerator)}}}{{{intermediate(denominator)}}}'
        + r' \\ & \approx ' + correct_value + r'\end{aligned}' + '\n$$'
    )
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    # Stable across order/seed; complete bank affects identity, since it is authored content.
    semantic = json.dumps([prompt, sorted(values), correct_value], separators=(',', ':'))
    qid = uuid.uuid5(uuid.UUID(KP['id']), semantic)
    fid = uuid.uuid5(qid, 'field:' + key)
    choices = [{':answer/id': str(uuid.uuid5(fid, value)), ':answer/type': ':answer.type/math',
                ':answer/value': value} for value in values]
    correct = next(c[':answer/id'] for c in choices if c[':answer/value'] == correct_value)
    random.Random(seed).shuffle(choices)
    metadata = {'generator_version': VERSION, 'template': kind, 'profile': profile,
                'parameters': {'a': a, 'x': x, 'places': places}, 'region': region(a, x),
                'correct_rank': rank if kind == 'radio' else None, 'seed': seed,
                'source_ids': [PROFILES[profile][2] if kind == 'radio' else 'q-262883'],
                'domain': 'integer a>1, X>1; a!=10; no common integer-power base for a and X',
                'sampling_policy': 'Practice requires numerical change of base; replay retains original evidence.',
                'dependencies': {'python': '3.13.5', 'packages': {}}}
    if source:
        metadata.update(source)
    return {'knowledge_point': KP, 'question': {
        ':question/id': str(qid), ':question/difficulty': ':question.difficulty/easy',
        ':question/problem': prompt, ':question/worked-solution': solution,
        ':question/requires-calculator': True,
        ':question/answer-fields': [{':answer-field/id': str(fid), ':answer-field/key': key,
            ':answer-field/type': ':answer-field.type/' + kind,
            ':answer-field/choices': choices, ':answer-field/correct': [':answer/id', correct]}]},
        'generation': metadata, 'assets': {}}


def replay():
    """Original parameters and complete banks; missing fields are explicitly inferred."""
    data = json.loads(Path(__file__).with_name('source-data.json').read_text())
    records = []
    for row in data:
        source = row['original']
        records.append(generate(**row['parameters'], profile=row['profile'], rank=row['rank'],
            notice='scientific calculator is required' in source[':question/problem'],
            source={'source_ids': [source[':question/math-academy-id']],
                    'source_question_id': source[':question/id'],
                    'source_difficulty': source.get(':question/difficulty'),
                    'inferred_missing_field': not source.get(':question/answer-fields'),
                    'source_replay': True}))
    return records


@lru_cache(maxsize=1)
def parameter_pools():
    return {(profile, case): [(a, x) for a in range(3, 23) for x in range(4, 46)
        if requires_change_of_base(a, x) and region(a, x) == case
        and (profile != 'p2' or evaluate(a, x, 2)[0] >= Decimal('.65'))]
        for profile in ('blank', 'p2', 'p3') for case in ('below', 'above')}


def sample(count, seed, difficulty='easy'):
    if difficulty not in ('easy', 'unclassified'):
        raise ValueError('Only easy difficulty is supported')
    if count < 0:
        raise ValueError('Count must be nonnegative')
    rng = random.Random(seed)
    source_rows = json.loads(Path(__file__).with_name('source-data.json').read_text())
    seen = {(r['parameters']['a'], r['parameters']['x'], r['parameters']['places']) for r in source_rows}
    records = []
    # Select eligible rule case, template, bank and answer rank BEFORE compatible values.
    pools = parameter_pools()
    capacity = len({(a, x, places) for (profile, _), pairs in pools.items()
                    for a, x in pairs for places in ((2, 3) if profile == 'blank' else (PROFILES[profile][0],))} - seen)
    if count > capacity:
        raise ValueError('Count exceeds the conservative unique semantic capacity per call')
    for attempt in range(max(1000, count * 100)):
        if len(records) == count:
            return records
        profile = rng.choice(('blank', 'p2', 'p3'))
        case = rng.choice(('below', 'above'))
        rank = rng.randrange(5) if profile != 'blank' else 0
        places = rng.choice((2, 3)) if profile == 'blank' else PROFILES[profile][0]
        a, x = rng.choice(pools[profile, case])
        semantic = (a, x, places)
        if semantic in seen:
            continue
        seen.add(semantic)
        records.append(generate(a, x, places, profile=profile, rank=rank, seed=rng.getrandbits(64)))
    raise ValueError('Could not draw requested count without semantic duplicates')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy', choices=['easy', 'unclassified', 'moderate', 'hard'])
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    try:
        records = sample(args.count, args.seed, args.difficulty)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(records, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
