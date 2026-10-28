#!/usr/bin/env python3
"""Seeded period practice. Exact rational construction, no database or assets.

Adapted from the supplied period draft's affine-input/reciprocal-scaling method.
The investigation's quotient/combination exemplars define authored later bands.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
import random
import uuid
import sys
sys.dont_write_bytecode = True
from math_format import normalize_prose, normalize_tex, checked_math_content

VERSION = 'period-affine-v3'
LEVELS = ('easy', 'moderate', 'hard')
KP = {'db_id': 17592186129122, 'id': '1eeb42af-74ee-53d7-af9f-be171f77968f',
      'title': 'Calculating the Period of a Transformed Sinusoidal Function'}
SOURCES = ['4126b1b4-8e8d-506d-b0ce-d7e1e1256bf6', '53685d44-d788-5019-bc63-97c441bd2453',
           'e0d5cec2-04d5-542c-903e-28cdf3f5b313', '72d5418e-aa83-5e26-b56d-9365871c6a6c',
           'e356a361-0054-56e0-9326-4eab7969f279', 'd2e89257-c187-56d5-921c-62533d1cff56',
           'dd575496-3e51-5d55-95e8-6967d72b5129', '4851a756-0bff-5da4-b5af-2f3ab439405d']
EXEMPLARS = {'easy': '25c6f907-f9a8-57c3-84ea-5d2e3bfdb8fb',
             'moderate': 'ae18bc12-5543-5207-adf2-555a013f582a',
             'hard': '3308dd07-d8ab-58f8-b4c0-58def5f9da3d'}
# Each tuple is a whole authored error profile, chosen before parameters.
COMMON = [('half', 'double', 'multiply_frequency', 'amplitude_as_frequency'),
          ('half', 'ignore_frequency', 'amplitude_divisor', 'amplitude_multiplier'),
          ('double', 'multiply_frequency', 'amplitude_divisor', 'amplitude_as_frequency'),
          ('half', 'double', 'quarter', 'multiply_frequency')]
PROFILES = {'easy': COMMON,
            'moderate': COMMON + [('omit_divisor', 'half', 'amplitude_divisor', 'double')],
            'hard': COMMON + [('first_term_only', 'second_term_only', 'half', 'double')]}

class Rejected(ValueError):
    pass

def texr(value):
    value = F(value)
    if value.denominator == 1:
        return str(value.numerator)
    return ('-' if value < 0 else '') + r'\frac{' + str(abs(value.numerator)) + '}{' + str(value.denominator) + '}'

def texperiod(value, unit):
    value = F(value)
    if unit == 'degree':
        return (texr(value) if value.denominator == 1 else r'\left(' + texr(value) + r'\right)') + r'^{\circ}'
    n, d = value.numerator, value.denominator
    num = ('' if abs(n) == 1 else str(abs(n))) + r'\pi'
    return ('-' if n < 0 else '') + (num if d == 1 else r'\frac{' + num + '}{' + str(d) + '}')

def ax(b):
    b = F(b)
    return 'x' if b == 1 else '-x' if b == -1 else texr(b) + 'x'

def signed(value, formatter=texr):
    value = F(value)
    return '' if value == 0 else ('+' if value > 0 else '-') + formatter(abs(value))

def phase(c, unit):
    return texperiod(c, 'rad') if unit == 'rad' else texperiod(c, 'degree')

def coeff(p):
    return F(p['n'], p['d']) + (F(p['m'], p['e']) if p['level'] == 'hard' else 0)

def argument(p):
    c = F(p['c'])
    ctext = signed(c, lambda v: phase(v, p['unit']))
    if p['level'] == 'easy':
        return ax(F(p['n'], p['d'])) + ctext
    first = r'\frac{' + ax(p['n']) + ctext + '}{' + str(p['d']) + '}'
    if p['level'] == 'hard':
        first += signed(F(p['m'], p['e']), lambda v: ax(v))
    return first

def operations(p):
    base = F(2 if p['unit'] == 'rad' else 360)
    b, a = abs(coeff(p)), abs(F(p['a']))
    t = base / b
    values = {'correct': t, 'half': t / 2, 'double': 2 * t, 'quarter': t / 4,
              'multiply_frequency': base * b, 'ignore_frequency': base,
              'amplitude_divisor': t / a, 'amplitude_multiplier': t * a,
              'amplitude_as_frequency': base / a}
    if p['level'] == 'moderate':
        values['omit_divisor'] = base / abs(p['n'])
    if p['level'] == 'hard':
        values['first_term_only'] = base / abs(F(p['n'], p['d']))
        values['second_term_only'] = base / abs(F(p['m'], p['e']))
    return values

def derivation(p):
    """The displayed argument remains unchanged; only its affine coefficient is collected."""
    b, unit, c = coeff(p), p['unit'], F(p['c'])
    inner = argument(p)
    if p['level'] == 'easy':
        intro = 'Read the coefficient of $x$ inside the ' + ('sine' if p['trig'] == 'sin' else 'cosine') + ':\n\n$$\nB=' + texr(b) + '.\n$$'
        stages = [r'B=' + texr(b)]
    else:
        distributed = ax(F(p['n'], p['d'])) + signed(c / p['d'], lambda v: phase(v, unit))
        if p['level'] == 'hard':
            distributed += signed(F(p['m'], p['e']), lambda v: ax(v))
        final = ax(b) + signed(c / p['d'], lambda v: phase(v, unit))
        rows = [inner + '&=' + distributed]
        if p['level'] == 'hard':
            rows.append('&=' + r'\left(' + texr(F(p['n'], p['d'])) + signed(F(p['m'], p['e'])) + r'\right)x' + signed(c / p['d'], lambda v: phase(v, unit)))
        if p['level'] == 'hard':
            rows.append('&=' + final + '.')
        else:
            rows[-1] += '.'
        intro = ('Divide the entire argument to recover the coefficient of $x$:' if p['level'] == 'moderate'
                 else 'Combine both $x$ terms inside the argument before finding the period:')
        intro += '\n\n$$\n' + r'\begin{aligned}' + '\n' + ('\\\\\n'.join(rows)) + '\n' + r'\end{aligned}' + '\n$$\n\nThus $B=' + texr(b) + '.$'
        stages = rows + ['B=' + texr(b)]
    base = r'2\pi' if unit == 'rad' else r'360^{\circ}'
    t = texperiod(operations(p)['correct'], unit)
    formula = r'T=\frac{' + base + r'}{|B|}=\frac{' + base + '}{' + texr(abs(b)) + '}=' + t + '.'
    solution = intro + '\n\nThe period is a positive length. ' + (r'One full turn is $360^{\circ}$ in degrees.' if unit == 'degree' else r'One full turn is $2\pi$ in radians.')
    solution += '\n\n$$\n' + formula + '\n$$\n\nThe outside multiplier and the constant shifts do not change the period.'
    return solution, stages + [formula], t

@checked_math_content
def make_record(p, profile=0, seed=0, bank=None, source_ids=None):
    p = dict(p)
    if p['level'] not in LEVELS or p['unit'] not in ('rad', 'degree') or p['trig'] not in ('sin', 'cos'):
        raise ValueError('Unknown instructional family')
    if not F(p['a']) or not coeff(p) or p['d'] <= 0:
        raise Rejected('Nonconstant sinusoid and positive denominator required')
    values = operations(p)
    recipes = ['correct', *PROFILES[p['level']][profile]]
    raw = [values[name] for name in recipes] if bank is None else list(map(F, bank))
    if len(raw) != 5 or len(set(raw)) != 5 or raw.count(values['correct']) != 1:
        raise Rejected('A whole bank must contain five distinct values and one correct answer')
    inside = argument(p)
    function = ('' if F(p['a']) == 1 else '-' if F(p['a']) == -1 else texr(p['a'])) + '\\' + p['trig'] + r'\left(' + inside + r'\right)' + signed(p['v'])
    prompt = 'Calculate the period of the function\n\n$$\nf(x)=' + function + '.\n$$'
    prompt += '\n\nAngles are measured in ' + ('degrees.' if p['unit'] == 'degree' else 'radians.')
    solution, steps, final = derivation(p)
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    options = [normalize_tex(texperiod(v, p['unit'])) for v in raw]
    final = normalize_tex(final)
    identity = hashlib.sha256(json.dumps([VERSION, p['level'], prompt, solution, sorted(options)], ensure_ascii=False).encode()).hexdigest()
    uid = lambda suffix: str(uuid.uuid5(uuid.NAMESPACE_URL, VERSION + ':' + identity + ':' + suffix))
    answers = [{':answer/id': uid('option:' + text), ':answer/type': ':answer.type/math', ':answer/value': text} for text in options]
    correct = answers[raw.index(values['correct'])][':answer/id']
    random.Random(seed).shuffle(answers)
    return {'knowledge_point': dict(KP), 'question': {
        ':question/id': uid('question'), ':question/problem': prompt, ':question/worked-solution': solution,
        ':question/difficulty': ':question.difficulty/' + p['level'],
        ':question/answer-fields': [{':answer-field/id': uid('selection'), ':answer-field/key': 'selection',
            ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': answers,
            ':answer-field/correct': [':answer/id', correct]}]},
        'generation': {'version': VERSION, 'seed': seed, 'template': p['level'], 'parameters': p,
            'profile': 'source-bank-replay' if bank is not None else profile, 'recipes': recipes if bank is None else [],
            'source_ids': source_ids or [EXEMPLARS[p['level']]], 'ordered_steps': steps,
            'displayed_final': final, 'frequency': str(coeff(p)), 'period_coefficient': str(values['correct']),
            'necessary_conversions': [], 'authored_extension': bank is None,
            'mathematical_task_fingerprint': p['level'] + ':' + p['unit'] + ':' + str(coeff(p))}}

EASY_FREQUENCIES = [(n, d) for n, d in [(1, 2), (1, 3), (2, 3), (3, 4), (4, 3), (5, 3), (4, 7), (5, 4), (3, 2), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (8, 1), (9, 1)]]

def sample(level, role, rng):
    unit, trig, direction, relation = role
    p = {'level': level, 'unit': unit, 'trig': trig, 'a': str(rng.choice([-4, -3, -2, -1, 1, 2, 3, 4, F(1, 2), F(1, 3)])),
         'v': rng.choice([-4, -2, 0, 1, 3]), 'c': str(rng.choice([F(-1, 2), F(-1, 3), F(1, 6), F(1, 3), F(1, 2)])) if unit == 'rad' else str(rng.choice([-60, -45, -30, 20, 30, 60]))}
    if level == 'easy':
        p['n'], p['d'] = rng.choice(EASY_FREQUENCIES)
    elif level == 'moderate':
        p['n'], p['d'] = direction * rng.choice([1, 2, 3, 4, 5]), rng.choice([2, 3, 4])
    else:
        # Sample the requested sign/term relationship before incidental data.
        choices = []
        for n, d, m, e in itertools.product([-4, -3, -2, -1, 1, 2, 3, 4], [2, 3, 4], [-3, -2, -1, 1, 2, 3], [2, 3, 4]):
            b = F(n, d) + F(m, e)
            if b and (b > 0) == (direction > 0) and (n*m > 0) == (relation == 'same') and abs(b) <= 3:
                choices.append((n, d, m, e))
        p['n'], p['d'], p['m'], p['e'] = rng.choice(choices)
    return p

def _candidate_batch(level, count, rng):
    if level not in LEVELS or count < 1:
        raise ValueError('Choose a supported band and positive count')
    roles = list(itertools.product(['rad', 'degree'], ['sin', 'cos'], [1] if level == 'easy' else [-1, 1], ['direct'] if level != 'hard' else ['same', 'opposing']))
    records, tasks, deck = [], set(), []
    for i in range(count):
        if not deck:
            deck = roles.copy()
            rng.shuffle(deck)
        role = deck.pop()
        profile = rng.randrange(len(PROFILES[level]))
        for attempt in range(3000):
            p = sample(level, role, rng)
            try:
                record = make_record(p, profile, rng.getrandbits(63))
            except Rejected:
                continue
            task = record['generation']['mathematical_task_fingerprint']
            if task in tasks:
                continue
            tasks.add(task)
            records.append(record)
            break
        else:
            raise ValueError('Requested batch exceeds distinct supported tasks for this role')
    return records


def batch_has_shortcut(records):
    """Inspect only bank layout/shape cues within visible instructional families.

    A two-record subgroup can already be the complete delivered practice pool.
    Singleton cells cannot establish a repeatable action and are left unconstrained.
    Numeric rank uses magnitudes only, never the target coefficient as a cue.
    """
    from collections import Counter
    rows = []
    for record in records:
        p = record['generation']['parameters']
        values = operations(p)
        field = record['question'][':question/answer-fields'][0]
        choices = field[':answer-field/choices']
        numeric = {normalize_tex(texperiod(v, p['unit'])): v for v in values.values()}
        bank = [numeric[a[':answer/value']] for a in choices]
        key = values['correct']
        nums, dens = Counter(v.numerator for v in bank), Counter(v.denominator for v in bank)
        modal = [v for v in bank if nums[v.numerator] == max(nums.values())
                 and dens[v.denominator] == max(dens.values())]
        geometric = [v for v in bank if any(a != v and b != v and a != b and a*b == v*v
                                           for a in bank for b in bank)]
        rows.append(dict(unit=p['unit'], trig=p['trig'],
                         region='below' if abs(coeff(p)) < 1 else 'equal' if abs(coeff(p)) == 1 else 'above',
                         rank=sorted(bank).index(key), position=bank.index(key),
                         modal=len(modal) == 1 and modal[0] == key,
                         geometric=len(geometric) == 1 and geometric[0] == key))
    groups = [rows]
    for fields in [('unit',), ('trig',), ('unit', 'trig'), ('region',)]:
        for role in set(tuple(row[k] for k in fields) for row in rows):
            groups.append([row for row in rows if tuple(row[k] for k in fields) == role])
    for group in groups:
        if len(group) < 2:
            continue
        if any(len({row[cue] for row in group}) == 1 for cue in ['rank', 'position']):
            return True
        if any(all(row[cue] for row in group) for cue in ['modal', 'geometric']):
            return True
    return False


def generate_batch(level, count, seed):
    # A single seeded random stream controls all rejection and resampling.
    # Resample complete plausible banks, never add arbitrary filler distractors.
    rng = random.Random(seed)
    for _ in range(2048):
        records = _candidate_batch(level, count, rng)
        if not batch_has_shortcut(records):
            return records
    raise ValueError('Cannot construct a batch without a repeated bank-only shortcut')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=[*LEVELS, 'unclassified', 'all'], default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    levels = LEVELS if args.difficulty == 'all' else ['easy' if args.difficulty == 'unclassified' else args.difficulty]
    result = [r for level in levels for r in generate_batch(level, args.count, args.seed)]
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
