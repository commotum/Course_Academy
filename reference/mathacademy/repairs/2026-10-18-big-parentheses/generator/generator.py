#!/usr/bin/env python3
"""Seeded, database-free power-of-quotient practice. See instructional-account.md."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys
import uuid

sys.dont_write_bytecode = True

from math_format import checked_math_content, normalize_prose, normalize_tex

KP_UUID = 'bbc7c6e8-63c7-5ac4-9b65-f12c006b3fde'
KP = {'db_id': 17592186105742, 'id': KP_UUID, 'title': 'Applying the Power of Quotient Rule'}
VERSION = '1.0.1'
FORMS = ('division', 'fraction', 'interrogative')
SOURCE_SPECS = ((4, 11, 3, 'division', 'q-68453'),
                (3, 8, 7, 'interrogative', 'q-68456'),
                (5, 8, 9, 'fraction', 'q-68714'),
                (14, 9, 4, 'division', 'q-100726'))


def tex(text):
    # Repair only the documented capture typo; public answers are bare TeX.
    return normalize_tex(text.replace('÷', r'\div ').replace('\\\\times', r'\times'))


def prose(text):
    return normalize_prose(text.replace('÷', r'\div ').replace('\\\\times', r'\times'))


def power(a, n):
    return f'{{{a}}}^{{{n}}}'


def quotient(a, b, form):
    return f'{a}\\div {b}' if form == 'division' else f'\\frac{{{a}}}{{{b}}}'


def expression(a, b, n, form):
    inner = quotient(a, b, form)
    if form == 'division':
        return f'({inner})^{{{n}}}'
    if form == 'fraction':
        return f'{{({inner})}}^{{{n}}}'
    return f'({inner})^{{{n}}}'


def statement(a, b, n, form):
    expr = expression(a, b, n, form)
    return f'What is ${expr}$?' if form == 'interrogative' else f'${expr}=$'


def solution(a, b, n, form):
    if form == 'division':
        text = (f'To raise the quotient of two numbers to the power of ${n}$, '
                f'we must raise each number to the power of ${n},$ and then divide:')
    else:
        text = (f'To raise the fraction to the power of ${n}$, we must raise both '
                f'the numerator and the denominator to the power of ${n}:$')
    result = quotient(power(a, n), power(b, n), form)
    return prose(text + '\n\n$$\n' + expression(a, b, n, form) + '=' + result + '\n$$')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


@checked_math_content
def record(a, b, n, form, values, correct_index, metadata, prompt=None, worked=None):
    values = [tex(v) for v in values]
    problem = prose(prompt or statement(a, b, n, form))
    # Bank order and seed are not mathematical identity. Profile contents are.
    qid = uuid.uuid5(uuid.UUID(KP_UUID), digest([problem, sorted(values), values[correct_index]]))
    fid = uuid.uuid5(qid, 'field:selection')
    choices = [{':answer/id': str(uuid.uuid5(fid, v)), ':answer/type': ':answer.type/math',
                ':answer/value': v} for v in values]
    return {'knowledge_point': KP.copy(), 'question': {
        ':question/id': str(qid), ':question/problem': problem,
        ':question/worked-solution': prose(worked or solution(a, b, n, form)),
        ':question/difficulty': ':question.difficulty/easy',
        ':question/answer-fields': [{':answer-field/id': str(fid), ':answer-field/key': 'selection',
            ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
            ':answer-field/correct': [':answer/id', choices[correct_index][':answer/id']]}]},
        'assets': {}, 'generation': {'generator_version': VERSION, 'template': form,
            'parameters': {'a': a, 'b': b, 'n': n}, 'dependencies': {'python': '3.13.5', 'packages': {}},
            'domain': {'bases': [2, 15], 'exponents': [2, 9], 'unequal_bases': True}, **metadata}}


def build_instance(a, b, exponents, target_rank, form, one_sided=(0, 1), order=None):
    """The bank is invariant under changing target_rank, allowing controlled tests."""
    if not (2 <= a <= 15 and 2 <= b <= 15 and a != b and form in FORMS):
        raise ValueError('unsupported bases or presentation')
    e = tuple(exponents)
    if len(e) != 3 or sorted(set(e)) != list(e) or not all(2 <= x <= 9 for x in e):
        raise ValueError('three increasing distinct exponents in 2..9 required')
    if target_rank not in range(3) or any(x not in range(3) for x in one_sided):
        raise ValueError('unsupported role assignment')
    pairs = [(k, k) for k in e] + [(e[one_sided[0]], 1), (1, e[one_sided[1]])]
    exact = [Fraction(a**p, b**q) for p, q in pairs]
    if len(set(exact)) != 5:
        raise ValueError('numerically ambiguous answer bank')
    order = list(range(5)) if order is None else list(order)
    if sorted(order) != list(range(5)):
        raise ValueError('option order must be a permutation')
    values = [quotient(power(a, pairs[i][0]) if pairs[i][0] != 1 else a,
                       power(b, pairs[i][1]) if pairs[i][1] != 1 else b, form) for i in order]
    return record(a, b, e[target_rank], form, values, order.index(target_rank), {
        'profile': 'authored-exponent-matching-v1', 'source_profiles': ['q-68453', 'q-68456', 'q-68714', 'q-100726'],
        'target_rank': target_rank, 'exponents': e, 'one_sided': one_sided,
        'choice_power_pairs': [pairs[i] for i in order], 'choice_order': order})


def source_replay(index):
    """Reconstruct complete source banks by formulas at original parameters."""
    a, b, n, form, profile = SOURCE_SPECS[index]
    q = lambda x, y: quotient(x, y, form)
    both, numerator, denominator = q(power(a, n), power(b, n)), q(power(a, n), b), q(a, power(b, n))
    if profile == 'q-68453':
        values = [q(a, f'({b}+{n})'), q(a, f'({b}\\times {n})'), denominator, both, numerator]
    elif profile == 'q-100726':
        values = [q(a, b) + f'\\times {n}', denominator, numerator, q(a, b) + f'\\div {n}', both]
    elif profile == 'q-68714':
        values = [numerator, both, denominator, q(a*n, b+n), q(a*n, b*n)]
    else:
        values = [both, denominator, numerator, q(a*n, b*n), q(a*n, b)]
    original = json.loads(Path(__file__).with_name('source_data.json').read_text())[index]
    # Wording is replayed verbatim where observed. Missing content is reconstructed.
    worked = original.get(':question/worked-solution')
    return record(a, b, n, form, values, values.index(both), {
        'profile': profile, 'source_question_id': original[':question/id'],
        'source_difficulty': original.get(':question/difficulty'),
        'reconstructed_fields': [] if worked else ['correct', 'worked-solution', 'difficulty']},
        prompt=statement(a, b, n, form), worked=worked)


@checked_math_content
def generate(rng, difficulty='easy'):
    if difficulty != 'easy':
        raise ValueError('only easy is supported')
    # Decision roles precede values. No outcome is assigned from presentation.
    rank = rng.randrange(3)
    exponents = sorted(rng.sample(range(2, 10), 3))
    one_sided = (rng.randrange(3), rng.randrange(3))
    for _ in range(1000):
        a, b = rng.sample(range(2, 16), 2)
        try:
            item = build_instance(a, b, exponents, rank, rng.choice(FORMS), one_sided,
                                  rng.sample(range(5), 5))
            return item
        except ValueError as error:
            if str(error) != 'numerically ambiguous answer bank':
                raise
    raise RuntimeError('could not produce an unambiguous instance')


def batch(count, seed, difficulty='easy'):
    if difficulty != 'easy':
        raise ValueError('only easy is supported')
    if not 0 <= count <= 1456:
        raise ValueError('count must be between 0 and 1456')
    rng, records, seen = random.Random(seed), [], set()
    attempts = 0
    while len(records) < count:
        attempts += 1
        if attempts > max(100, count*20):
            raise RuntimeError('requested batch exhausted available practice')
        item = generate(rng, difficulty)
        p = item['generation']['parameters']
        semantic = (p['a'], p['b'], p['n'])
        if semantic in seen:
            continue
        seen.add(semantic)
        item['generation'].update(seed=seed, batch_index=len(records))
        records.append(item)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy', choices=['easy', 'moderate', 'hard'])
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    args = parser.parse_args()
    try:
        result = batch(args.count, args.seed, args.difficulty)
    except (ValueError, RuntimeError) as error:
        parser.error(str(error))
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == '__main__':
    main()
