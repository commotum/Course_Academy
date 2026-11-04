#!/usr/bin/env python3
"""Seeded exact-value practice. All runtime resources are local to this file."""
import argparse
import copy
import hashlib
import json
import random
import uuid
from pathlib import Path

import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id': 17592186059674, 'id': '4c898bbf-004c-5905-a0a0-761adefc8bd8'}
ROOT = Path(__file__).resolve().parent
# Select signed exact-value categories before compatible angles.
GROUPS = ((30, 150), (45, 135), (210, 330), (225, 315))
VALUES = (s.Rational(1, 2), s.sqrt(2)/2, s.sqrt(3)/2, -s.Rational(1, 2), -s.sqrt(2)/2, -s.sqrt(3)/2, s.Integer(1), -s.Integer(1))
SOURCES = {
 'product': ['2a04b487-4a85-5ba7-af3b-ed0dfdddcb78', 'bee80a09-9428-5ae7-9598-757e90d1cdc6', '7de355f4-68ed-5d8f-8bd0-5f9d51794ae9', '234490c5-571f-5c2b-abd3-fc18f2b6c526'],
 'square': ['9f5ad5b9-cf75-5c20-a9c5-6e5d15578fe2', '83f3d502-62d9-5e1b-a7be-52d9144a4c16', '5fc8ff6e-fc33-5efd-ab02-f17a877d633b'],
 'sin_sec': ['ad1365bd-d309-5764-8412-78c271945c47', 'c456891a-3eac-5005-ae95-48c26bfb98c5', '92df499c-114f-5a8f-9fd7-333656e7d6b8'],
 'cos_csc': ['c8b170de-4305-57f7-8f86-f2f06478c4e5']}


def tex(value):
    return normalize_tex(s.latex(s.simplify(value)))


def angle(degrees, unit):
    if unit == 'degrees':
        return tex(s.Rational(degrees)) + r'^{\circ}'
    return tex(s.Rational(degrees, 180)*s.pi)


def trig(name, argument):
    return '\\' + name + r'\left(' + argument + r'\right)'


def display(value):
    return '$$\n' + value + '\n$$'


def aligned(rows):
    return display(r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}')


def banks(family, k, v, sign, profile, rng):
    """Whole authored profiles, with mathematical error values, never filler."""
    if family == 'square':
        y = s.simplify(1 + sign*v)
        candidates = [(1-sign*v, 'opposite cross-term sign'),
                      (s.Integer(1), 'omit the cross term'),
                      (1+sign*v/2, 'lose one factor of two'),
                      (1+2*sign*v, 'double the cross term again')]
        angles = [(1+sign*w, 'wrong special-angle value or quadrant') for w in VALUES]
    else:
        y = s.simplify(k*v/2)
        candidates = [(-y, 'wrong quadrant sign'), (2*y, 'omit division by two'),
                      (y/2, 'divide by two twice'), (-2*y, 'wrong sign and missing half')]
        angles = [(k*w/2, 'wrong special-angle value or quadrant') for w in VALUES]
    primary = angles if profile == 'angle' else candidates
    secondary = candidates if profile == 'angle' else angles
    rng.shuffle(primary)
    rng.shuffle(secondary)
    chosen, seen = [], {tex(y)}
    # Angle profiles deliberately have multiple valid family values; mixed
    # profiles combine scale/sign errors and two mistaken angle evaluations.
    sequence = primary + secondary if profile == 'angle' else primary[:2] + secondary + primary[2:]
    for value, reason in sequence:
        t = tex(value)
        if t not in seen:
            chosen.append((t, reason)); seen.add(t)
        if len(chosen) == 4:
            break
    if len(chosen) != 4:
        raise ValueError('Cannot construct five distinct plausible alternatives')
    # A learner knowing the finite authored answer family must still distinguish
    # at least two options by evaluating the expression. These are genuine
    # wrong-angle/sign alternatives, not arbitrary numerical padding.
    target = (s.Rational(1,2), s.sqrt(2)/2, -s.Rational(1,2), -s.sqrt(2)/2)
    possible = [1+w for w in target] if family == 'square' else [k*w/2 for w in target]
    valid_alternatives = [tex(z) for z in possible if tex(z) != tex(y)]
    if not any(value in valid_alternatives for value, _ in chosen):
        replacement = rng.choice(valid_alternatives)
        chosen[-1] = (replacement, 'wrong special-angle value or quadrant')
    chosen.append((tex(y), 'correct'))
    rng.shuffle(chosen)
    return chosen


def instance(family, doubled, unit='radians', k=2, sign=1, shape='radio', profile='mixed', rng=None, band=None):
    rng = rng or random.Random(0)
    k = s.sympify(k)
    x = angle(s.Rational(doubled, 2), unit)
    d = angle(doubled, unit)
    sx, cx = trig('sin', x), trig('cos', x)
    v = s.simplify(s.sin(s.Rational(doubled, 180)*s.pi))
    op = '+' if sign == 1 else '-'
    product = sx + cx
    if family == 'product':
        expression = ('' if k == 1 else tex(k)) + product
        y = s.simplify(k*v/2)
        intro = 'Use the double-angle formula for sine and keep the multiplier.'
        prefix = []
    elif family == 'square':
        expression = r'\left(' + sx + op + cx + r'\right)^2'
        y = s.simplify(1+sign*v)
        intro = 'Expand the square and use the Pythagorean identity.'
        prefix = [aligned([
            r'(\sin x' + op + r'\cos x)^2 &= \sin^2 x' + op + r'2\sin x\cos x+\cos^2 x',
            r'&=1' + op + r'2\sin x\cos x',
            r'&=1' + op + r'\sin(2x)'])]
    elif family in ('sin_sec', 'cos_csc'):
        num, den = ('sin', 'sec') if family == 'sin_sec' else ('cos', 'csc')
        expression = r'\frac{' + trig(num, x) + '}{' + trig(den, x) + '}'
        k = s.Integer(1)
        y = s.simplify(v/2)
        intro = 'Rewrite the reciprocal denominator to expose a sine–cosine product.'
        prefix = [display(r'\frac{' + trig(num, 'x') + '}{' + trig(den, 'x') + '}=' + trig(num, 'x') + r'\cdot\frac{1}{' + trig(den, 'x') + r'}=\sin x\cos x')]
    else:
        raise ValueError(family)
    band = band or {'product':'easy', 'square':'moderate', 'sin_sec':'hard', 'cos_csc':'hard'}[family]
    prompt = 'Without using a calculator, find the exact value of\n\n' + display(expression)
    if shape == 'blank':
        prompt += '\n\n' + display(expression + '=') + '\n{{value}}'
    rows = [r'2\sin x\cos x &=\sin(2x)', r'&=' + trig('sin', d), r'&=' + tex(v)]
    factor = '' if k/2==1 else tex(k/2)
    if family == 'square':
        final = aligned([expression + '&=1' + op + r'\left(' + tex(v) + r'\right)', '&=' + tex(y)])
    else:
        final = aligned([expression + '&=' + factor + r'\left(' + tex(v) + r'\right)', '&=' + tex(y)])
    solution = intro + '\n\nSet $x=' + x + '$.\n\n' + '\n\n'.join(prefix + [aligned(rows), 'Substitute this exact value:', final])
    bank = [(tex(y), 'correct')] if shape == 'blank' else banks(family, k, v, sign, profile, rng)
    return assemble(prompt, solution, band, shape, bank, {
        'template': family, 'parameters': {'doubled_degrees': doubled, 'unit': unit, 'multiplier': str(k), 'square_sign': sign},
        'profile': profile if shape == 'radio' else 'exact-entry',
        'source_question_ids': SOURCES[family], 'source_family_supported': True,
        'displayed_final': tex(y), 'doubled_value': tex(v),
        'shown_steps': ['reciprocal rewrite' if family.endswith(('sec', 'csc')) else 'binomial expansion and Pythagorean identity' if family == 'square' else 'coefficient scaling', 'sine double-angle identity', 'special-angle evaluation with quadrant sign', 'substitute and simplify'],
        'necessary_conversions': ['reciprocal definition'] if family in ('sin_sec','cos_csc') else ['binomial and Pythagorean expansion'] if family == 'square' else [],
        'domain': 'Real constant angle; both sine and cosine are nonzero.'})


def assemble(prompt, solution, band, shape, bank, metadata):
    # Normalize before identities. IDs depend on actual content, not a seed.
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    values = [(normalize_tex(v), reason) for v, reason in bank]
    content = [prompt, solution, band, shape, sorted(values)]
    qid = uuid.uuid5(uuid.UUID(KP['id']), json.dumps(content, sort_keys=True))
    fid = uuid.uuid5(qid, 'field:value')
    choices = [{':answer/id': str(uuid.uuid5(fid, value)), ':answer/type': ':answer.type/math', ':answer/value': value} for value, _ in values]
    key = next(a[':answer/id'] for a, (_, reason) in zip(choices, values) if reason == 'correct')
    field = {':answer-field/id': str(fid), ':answer-field/key': 'value', ':answer-field/type': ':answer-field.type/' + shape,
             ':answer-field/choices': choices, ':answer-field/correct': [':answer/id', key]}
    record = {'knowledge_point': KP, 'question': {':question/id': str(qid), ':question/problem': prompt,
        ':question/worked-solution': solution, ':question/difficulty': ':question.difficulty/' + band,
        ':question/answer-fields': [field]}, 'generation': {'version': '1.0.1', **metadata,
        'error_recipes': {a[':answer/id']: reason for a, (_, reason) in zip(choices, values)}}}
    return validate_generated_record(record)


def replay(source_id):
    cases = json.loads((ROOT/'source-replays.json').read_text())
    return copy.deepcopy(next(r for r in cases if r['generation']['source_question_ids'] == [source_id]))


def generate(difficulty, count, seed):
    if count < 0:
        raise ValueError('count must be nonnegative')
    if difficulty == 'unclassified':
        difficulty = 'easy'
    capacity = 56 if difficulty == 'easy' else 16
    if count > capacity:
        raise ValueError(f'Requested {count} unique semantic instances; this band supports {capacity}')
    rng = random.Random(seed)
    result, seen = [], set()
    categories = []
    attempts = 0
    while len(result) < count:
        if not categories:
            categories = list(range(len(GROUPS))); rng.shuffle(categories)
        category = categories.pop()
        doubled = rng.choice(GROUPS[category])
        family = 'product' if difficulty == 'easy' else 'square' if difficulty == 'moderate' else rng.choice(('sin_sec','cos_csc'))
        k = rng.choice([1,2,3,4,6,8,4*s.sqrt(3)]) if family == 'product' else 1
        sign = rng.choice((-1,1))
        unit = rng.choice(('degrees', 'radians'))
        shape = rng.choice(('radio','radio','blank'))
        # Same angle in different units, banks and response shapes is one semantic instance.
        semantic = (family, doubled, str(k), sign if family == 'square' else 1)
        attempts += 1
        if semantic in seen:
            if attempts > 100000:
                raise ValueError('Requested batch exceeds supported unique semantic instances')
            continue
        r = instance(family, doubled, unit, k, sign, shape, rng.choice(('angle','mixed')), rng, difficulty)
        r['generation'].update({'seed': seed, 'index': len(result)})
        seen.add(semantic); result.append(r)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', choices=('easy','moderate','hard','unclassified'), default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json',), default='json')
    parser.add_argument('--replay-source')
    a = parser.parse_args()
    records = [replay(a.replay_source)] if a.replay_source else generate(a.difficulty, a.count, a.seed)
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
