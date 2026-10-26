#!/usr/bin/env python3
"""Seeded continuous-compounding rate/time practice; no external runtime paths."""
import argparse
import hashlib
import json
import math
import random
import uuid
from math_format import normalize_prose, validate_generated_record

KP = '2c0a7b30-b6b4-584e-9816-506f8ec00813'
SOURCE = {
    'time': {'db_id': 17592186060056, 'id': '6b547ba8-6bef-5f97-b295-98d6170d064b', 'ma_id': 'q-1434'},
    'rate': {'db_id': 17592186060057, 'id': 'f32196ff-a1c3-58c8-8249-0c13bdced6e4', 'ma_id': 'q-1435'},
}
ORIGINAL = {'time': (102, 10, 9.5), 'rate': (10, 781, 14)}
OFFSETS = {'time': [-4, -2, 0, -15, -7], 'rate': [3, -5, 0, -10, 11]}
KEY_DOMAINS = {'time': (6, 191), 'rate': (8, 88)}

def sample_bank(family, rng):
    """Construct answer candidates before assigning which one is correct."""
    low, high = KEY_DOMAINS[family]
    width = rng.randint(8, 30)
    start = rng.randint(low, high - width)
    return sorted(rng.sample(range(start, start + width + 1), 5))

def compatible_parameters(family, target, rng):
    """Invert the rounding interval, then sample integer population evidence."""
    low_key, high_key = KEY_DOMAINS[family]
    if not low_key <= target <= high_key:
        raise ValueError('Target outside feasible key domain')
    if family == 'time':
        coefficients = [n / 10 for n in range(25, 181)
                        if n / 1000 * (target - .48) <= math.log(600 / 5)]
    else:
        coefficients = [n for n in range(5, 21)
                        if n * (target - .48) / 100 <= math.log(80)
                        and n * (target + .48) / 100 >= math.log(2)]
    for _ in range(10000):
        if family == 'time':
            initial, supplied = rng.randint(80, 600), rng.choice(coefficients)
            low = max(5, math.ceil(initial * math.exp(-supplied / 100 * (target + .48))))
            high = min(70, math.floor(initial * math.exp(-supplied / 100 * (target - .48))))
        else:
            initial, supplied = rng.randint(5, 40), rng.choice(coefficients)
            low = max(2 * initial, math.ceil(initial * math.exp(supplied * (target - .48) / 100)))
            high = min(80 * initial, math.floor(initial * math.exp(supplied * (target + .48) / 100)))
        if low > high:
            continue
        final = rng.randint(low, high)
        raw = math.log(final / initial) / (-supplied / 100) if family == 'time' else 100 * math.log(final / initial) / supplied
        if rounded(raw) == target and abs(raw % 1 - .5) >= .02:
            return initial, final, supplied
    raise RuntimeError(f'No compatible parameters for {family} target {target}')

def rounded(x):
    return math.floor(x + 0.5)

def display(rows):
    return '$$\n\\begin{aligned}\n' + ' \\\\\n'.join(rows) + '\n\\end{aligned}\n$$'

def make(family, initial, final, supplied, *, rank=2, position=2, rng=None, replay=False, bank=None):
    rng = rng or random.Random(0)
    if initial <= 0 or final <= 0 or supplied <= 0:
        raise ValueError('Positive counts and supplied coefficient required')
    ratio = rf'\frac{{{final}}}{{{initial}}}'
    if family == 'time':
        if final >= initial: raise ValueError('Decay requires a smaller final count')
        rate = -supplied / 100
        coefficient = f'{rate:.4f}'.rstrip('0').rstrip('.')
        pct = f'{supplied:g}'
        raw = math.log(final / initial) / rate
        key = rounded(raw)
        prompt = (f'There are currently ${initial}$ koalas living in a secluded forest, but their population is decreasing at a continuously compounded rate of ${pct}\\%$ per year. '
                  f'How many years must pass for there to be only ${final}$ koalas left in that forest? Round your answer to the nearest integer.')
        intro = f'The initial population is $P_0={initial}$ and the final population is $P={final}$. A decrease of ${pct}\\%$ per year means $r={coefficient}$, with $t$ in years.'
        rows = [r'P &= P_0e^{rt}', rf'{final} &= {initial}e^{{{coefficient}t}}',
                rf'e^{{{coefficient}t}} &= {ratio}', rf'\ln\left(e^{{{coefficient}t}}\right) &= \ln\left({ratio}\right)',
                rf'{coefficient}t &= \ln\left({ratio}\right)',
                rf't &= \frac{{\ln\left({ratio}\right)}}{{{coefficient}}}',
                rf't &\approx {raw:.5f}', rf't &\approx {key}\text{{ years}}']
        finish = f'Therefore, the time is approximately ${key}$ years.'
        choice_text = lambda n: f'${n}$ years'
    elif family == 'rate':
        if final <= initial: raise ValueError('Growth requires a larger final count')
        time = f'{supplied:g}'
        raw = 100 * math.log(final / initial) / supplied
        key = rounded(raw)
        prompt = (f'In a biology class, the teacher began the experiment with ${initial}$ bacteria in a petri dish. After ${time}$ minutes, the number of bacteria increased to ${final}$. '
                  'What was the continuously compounded growth rate of the bacteria? Round your answer to the nearest percent.')
        intro = f'The initial population is $P_0={initial}$, the final population is $P={final}$, and the elapsed time is $t={time}$ minutes. The decimal rate $r$ is per minute.'
        rows = [r'P &= P_0e^{rt}', rf'{final} &= {initial}e^{{{time}r}}',
                rf'e^{{{time}r}} &= {ratio}', rf'\ln\left(e^{{{time}r}}\right) &= \ln\left({ratio}\right)',
                rf'{time}r &= \ln\left({ratio}\right)', rf'r &= \frac{{\ln\left({ratio}\right)}}{{{time}}}',
                rf'r &\approx {raw/100:.7f}', rf'100r &\approx {raw:.5f}']
        finish = f'Converting the decimal rate to a percentage and rounding to the nearest percent gives approximately ${key}\\%$ per minute.'
        choice_text = lambda n: f'${n}\\%$ per minute'
    else:
        raise ValueError('Unknown family')
    if replay:
        values = [key + offset for offset in OFFSETS[family]]
    else:
        if not 0 <= rank <= 4 or not 0 <= position <= 4 or key < 6:
            raise ValueError('Invalid bank assignment')
        if bank is None:
            # Explicit-parameter construction for replay/counterfactual tools.
            # No fixed distance from the key: all other integers are possible.
            ceiling = max(KEY_DOMAINS[family][1], key + 4)
            values = rng.sample(range(1, key), rank) + rng.sample(range(key + 1, ceiling + 1), 4 - rank)
        else:
            if len(set(bank)) != 5 or key not in bank or any(n <= 0 for n in bank):
                raise ValueError('Bank must contain five distinct positive values including the key')
            if sorted(bank).index(key) != rank:
                raise ValueError('Bank key rank disagrees with selected rank')
            values = [n for n in bank if n != key]
        rng.shuffle(values)
        values.insert(position, key)
    prompt += '\n\n> A scientific calculator is required to answer this question.'
    solution = intro + '\n\nUse the continuously compounded growth equation, isolate the exponential, take natural logarithms, and solve:\n\n' + display(rows) + '\n\n' + finish
    prompt, solution = map(normalize_prose, (prompt, solution))
    texts = [normalize_prose(choice_text(n)) for n in values]
    content = json.dumps([prompt, solution, sorted(texts), choice_text(key)], ensure_ascii=False)
    qid = uuid.uuid5(uuid.UUID(KP), hashlib.sha256(content.encode()).hexdigest())
    fid = uuid.uuid5(qid, 'selection')
    answers = [{':answer/id': str(uuid.uuid5(fid, text)), ':answer/type': ':answer.type/text', ':answer/value': text} for text in texts]
    answer_id = answers[values.index(key)][':answer/id']
    record = {'knowledge_point': {'db_id': 17592186059797, 'id': KP}, 'question': {
        ':question/id': str(qid), ':question/difficulty': ':question.difficulty/moderate',
        ':question/requires-calculator': True, ':question/problem': prompt, ':question/worked-solution': solution,
        ':question/answer-fields': [{':answer-field/id': str(fid), ':answer-field/key': 'selection',
        ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': answers,
        ':answer-field/correct': [':answer/id', answer_id]}]},
        'generation': {'version': 2, 'template': family, 'profile': 'source-replay' if replay else 'bank-first-integers',
        'source_questions': [SOURCE[family]], 'source_difficulty': None,
        'parameters': {'initial': initial, 'final': final, 'supplied': supplied},
        'domains': 'positive unequal counts; positive supplied rate magnitude or duration',
        'displayed_final': choice_text(key), 'required_conversions': ['percent to signed decimal'] if family == 'time' else ['decimal to percent'],
        'source_support': ['e-5167', 'tutorial-3396', 'e-4103', 'e-4104']}}
    return validate_generated_record(record)

def cycle(rng):
    while True:
        values = list(range(5)); rng.shuffle(values)
        yield from values

def generate(count, seed, difficulty='moderate'):
    if difficulty == 'unclassified': difficulty = 'moderate'
    if difficulty != 'moderate': raise ValueError('Only moderate is source-supported')
    if count < 0: raise ValueError('Count cannot be negative')
    rng = random.Random(seed)
    ranks = {f: cycle(random.Random(rng.getrandbits(64))) for f in SOURCE}
    positions = {f: cycle(random.Random(rng.getrandbits(64))) for f in SOURCE}
    records, seen, rejected = [], set(), 0
    family_order = []
    while len(records) < count:
        if not family_order:
            family_order = list(SOURCE); rng.shuffle(family_order)
        family = family_order.pop()
        rank, position = next(ranks[family]), next(positions[family])
        bank = sample_bank(family, rng)
        target = bank[rank]
        for attempt in range(10000):
            initial, final, supplied = compatible_parameters(family, target, rng)
            record = make(family, initial, final, supplied, rank=rank, position=position, rng=rng, bank=bank)
            identity = (family, initial, final, supplied)
            if identity in seen:
                rejected += 1; continue
            seen.add(identity)
            record['generation'].update(seed=seed, index=len(records), rejected_before_acceptance=rejected)
            records.append(record)
            break
        else: raise RuntimeError('Sampling exhausted')
    return records

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty', default='moderate', choices=['unclassified', 'easy', 'moderate', 'hard'])
    p.add_argument('--count', type=int, required=True)
    p.add_argument('--seed', type=int, required=True)
    p.add_argument('--format', choices=['json'], default='json')
    args = p.parse_args()
    try: records = generate(args.count, args.seed, args.difficulty)
    except ValueError as e: p.error(str(e))
    print(json.dumps(records, indent=2, ensure_ascii=False))

if __name__ == '__main__': main()
