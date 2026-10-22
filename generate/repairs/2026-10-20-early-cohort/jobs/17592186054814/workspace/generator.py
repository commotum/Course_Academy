#!/usr/bin/env python3
"""Seeded, relocatable special-number-set membership generator (no writes)."""
import argparse
from decimal import Decimal
from fractions import Fraction
import json
from math import isqrt
from pathlib import Path
import random
import uuid

from math_format import checked_math_content, normalize_prose, validate_generated_record

VERSION = '1.0.0'
DATA = json.loads(Path(__file__).with_name('source-cases.json').read_text())
KP_UUID = uuid.UUID(DATA['kp_uuid'])
IMAGE = 'images/67/67ef97be4b21a74feaae15f3ff30d5077fc1316874df8de79155316a621e4487.png'
NAMES = {'N': 'Natural numbers', 'Z': 'Integers', 'Q': 'Rational numbers',
         'R': 'Real numbers', 'C': 'Complex numbers'}
PATTERNS = {'natural': 'NZQRC', 'integer': 'ZQRC', 'rational': 'QRC',
            'irrational': 'RC', 'nonreal': 'C'}
FAMILIES = {'natural': ('integer', 'fraction', 'decimal', 'radical'),
            'integer': ('integer', 'fraction', 'decimal', 'radical'),
            'rational': ('fraction', 'decimal'), 'irrational': ('radical', 'pi'),
            'nonreal': ('radical',)}


def uid(*values):
    return str(uuid.uuid5(KP_UUID, json.dumps(values, sort_keys=True, ensure_ascii=False)))


def number(p):
    """One source of mathematical truth, independent of sampled case annotation."""
    family = p['family']
    if family == 'integer':
        x = Fraction(p['n']); tex = str(p['n'])
    elif family == 'fraction':
        n, d = p['n'], p['d']
        if d <= 0: raise ValueError('positive denominator required')
        x = Fraction(n, d)
        tex = ('-' if n < 0 else '') + rf'\frac{{{abs(n)}}}{{{d}}}'
    elif family == 'decimal':
        x = Fraction(p['units'], 100)
        tex = format(Decimal(p['units']) / 100, '.2f')
    elif family == 'pi':
        return ('-' if p['sign'] < 0 else '') + r'\pi', 'irrational', None
    elif family == 'radical':
        n = p['n']; tex = rf'\sqrt{{{n}}}'
        if n < 0:
            if isqrt(-n) ** 2 != -n: raise ValueError('nonreal replay uses square magnitudes')
            return tex, 'nonreal', None
        r = isqrt(n)
        if r * r != n: return tex, 'irrational', None
        x = Fraction(r)
    else:
        raise ValueError('unknown family')
    case = 'natural' if x.denominator == 1 and x > 0 else 'integer' if x.denominator == 1 else 'rational'
    return tex, case, x


def frac_tex(x):
    if x.denominator == 1: return str(x.numerator)
    return ('-' if x < 0 else '') + rf'\frac{{{abs(x.numerator)}}}{{{x.denominator}}}'


def memberships(tex, included, labels):
    statements = [tex + (r'\in ' if s in included else r'\notin ') + s for s in labels]
    rows = [r'\qquad '.join(statements[i:i+2]) for i in range(0, len(statements), 2)]
    return rows[0] if len(rows) == 1 else r'\begin{gathered}' + r' \\ '.join(rows) + r'\end{gathered}'


def display(tex):
    return '$$\n' + tex + '\n$$'


def solution(p):
    tex, case, x = number(p)
    inside = PATTERNS[case]
    recall = '\n\n'.join(f'- ${s}$ represents the set of **{NAMES[s].lower()}**.' for s in 'NZQRC')
    out = [f'![]({IMAGE})', 'Recall the following:', recall,
           'With that in mind, we note the following:']
    if case == 'nonreal':
        coefficient = isqrt(-p['n'])
        simplified = (str(coefficient) if coefficient != 1 else '') + r'\text{i}'
        out += [f'- First, we note that ${tex}={simplified}$ is a complex number. Therefore, we can write',
                display(memberships(tex, inside, 'C')),
                f'- Since the imaginary part of ${tex}$ is nonzero, it does *not* belong to $N,Z,Q,$ or $R.$ We can write',
                display(memberships(tex, inside, 'NZQR'))]
    elif case in ('natural', 'integer'):
        label = tex if tex == str(x.numerator) else tex + '=' + str(x.numerator)
        if case == 'natural':
            out += [f'- The number ${label}$ is a positive whole number, so it belongs to $N.$ We can write',
                    display(memberships(tex, inside, 'N')),
                    '- Every natural number is an integer, rational, real, and complex number. Consequently, we can write',
                    display(memberships(tex, inside, 'ZQRC'))]
        else:
            reason = 'zero' if x == 0 else 'negative'
            out += [f'- The number ${label}$ is {reason}, so it does *not* belong to $N,$ and we can write',
                    display(memberships(tex, inside, 'N')),
                    f'- However, ${x.numerator}$ is an integer, so it does belong to $Z,$ and we can write',
                    display(memberships(tex, inside, 'Z')),
                    f'- Every integer is a rational, real, and complex number. Consequently, ${tex}$ belongs to $Q,R,$ and $C,$ and we can write',
                    display(memberships(tex, inside, 'QRC'))]
    elif case == 'rational':
        if p['family'] == 'decimal':
            ratio = ('-' if p['units'] < 0 else '') + rf'\frac{{{abs(p["units"])}}}{{100}}'
        else:
            ratio = frac_tex(x)
        out += [f'- The number ${tex}$ is not an integer, so it does *not* belong to $Z$ nor to $N.$ We can write',
                display(memberships(tex, inside, 'NZ')),
                '- However, it can be written as the ratio of two integers:',
                display(tex + '=' + ratio),
                f'Consequently, ${tex}$ is a rational number, and we can write',
                display(memberships(tex, inside, 'Q')),
                f'- Every rational is a real and complex number. Consequently, ${tex}$ belongs to both $R$ and $C,$ and we can write',
                display(memberships(tex, inside, 'RC'))]
    else:
        reason = ('is a known irrational number' if p['family'] == 'pi' else
                  f'is irrational because ${p["n"]}$ is positive and not a perfect square')
        out += [f'- The number ${tex}$ is not an integer, so it does *not* belong to $Z$ nor to $N.$ We can write',
                display(memberships(tex, inside, 'NZ')),
                f'- Also, ${tex}$ {reason}. It cannot be written as the ratio of two integers, so it does *not* belong to $Q$ either:',
                display(memberships(tex, inside, 'Q')),
                f'- Every irrational number is both a real number and a complex number. Consequently, ${tex}$ belongs to both $R$ and $C,$ and we can write',
                display(memberships(tex, inside, 'RC'))]
    out += ['Therefore, the correct answer is ' + ('$' + ', '.join(inside) + '$') + (' only.' if len(inside) < 5 else '.')]
    return normalize_prose('\n\n'.join(out))


def field(label, correct, owner, values=('false', 'true'), kind='checkbox'):
    fid = uid(owner, 'field', label)
    choices = [{':answer/id': uid(fid, value), ':answer/type': ':answer.type/text',
                ':answer/value': value} for value in values]
    return {':answer-field/id': fid, ':answer-field/key': label,
            ':answer-field/type': ':answer-field.type/' + kind,
            ':answer-field/choices': choices,
            ':answer-field/correct': [':answer/id', next(a[':answer/id'] for a in choices if a[':answer/value'] == correct)]}


@checked_math_content
def build(p, order='NZQRC', seed=None):
    tex, case, _ = number(p)
    prompt = normalize_prose(f'To which of the following sets does the number ${tex}$ belong?\n\nSelect all that apply.')
    qid = uid(VERSION, prompt)
    fields = [field(f'{NAMES[s]} (${s}$)', str(s in PATTERNS[case]).lower(), qid) for s in order]
    return {'knowledge_point': {'db_id': DATA['kp_id'], 'id': DATA['kp_uuid'], 'title': DATA['title']},
            'question': {':question/id': qid, ':question/problem': prompt,
                         ':question/difficulty': ':question.difficulty/easy',
                         ':question/answer-fields': fields, ':question/worked-solution': solution(p)},
            'generation': {'generator': VERSION, 'template': 'special-sets-checkbox',
                           'profile': 'five-boolean-memberships', 'seed': seed, 'parameters': p,
                           'case': case, 'source_basis': DATA['basis'],
                           'source_question_ids': [q[':question/id'] for q in DATA['questions'] if ':question/difficulty' in q],
                           'dependencies': {'python': '3.13.5', 'packages': {}}}}


def sample_parameters(rng):
    # Decision first: choose eligible membership, then compatible representation.
    case = rng.choice(tuple(PATTERNS))
    family = rng.choice(FAMILIES[case])
    p = {'family': family}
    if family == 'integer':
        p['n'] = rng.randint(1, 20) if case == 'natural' else rng.randint(-20, 0)
    elif family == 'fraction':
        d = rng.randint(2, 10)
        if case in ('natural', 'integer'):
            n = (rng.randint(1, 20) if case == 'natural' else rng.randint(-20, 0)) * d
        else:
            n = rng.choice([i for i in range(-40, 41) if i % d])
        p.update(n=n, d=d)
    elif family == 'decimal':
        if case in ('natural', 'integer'):
            u = 100 * (rng.randint(1, 20) if case == 'natural' else rng.randint(-20, 0))
        else:
            u = rng.choice([i for i in range(-2000, 2001) if i % 100])
        p['units'] = u
    elif family == 'pi':
        p['sign'] = rng.choice((-1, 1))
    elif case == 'natural':
        p['n'] = rng.randint(1, 12) ** 2
    elif case == 'integer':
        p['n'] = 0  # sqrt(nonnegative integer) cannot be negative.
    elif case == 'nonreal':
        p['n'] = -(rng.randint(1, 12) ** 2)
    else:
        p['n'] = rng.choice([i for i in range(2, 151) if isqrt(i) ** 2 != i])
    assert number(p)[1] == case
    return p


def generate(difficulty='easy', count=5, seed=0):
    if difficulty not in ('easy', 'unclassified'):
        raise ValueError('unsupported difficulty: only easy is source-justified')
    if count < 0: raise ValueError('count must be nonnegative')
    rng = random.Random(seed)
    records, seen, attempts = [], set(), 0
    while len(records) < count:
        attempts += 1
        if attempts > max(1000, count * 100):
            raise ValueError('requested count exceeds available semantic sample for this seed')
        p = sample_parameters(rng)
        tex = number(p)[0]
        if tex in seen: continue
        seen.add(tex)
        order = list('NZQRC'); rng.shuffle(order)
        rec = build(p, order, seed)
        rec['generation']['sampling_attempt'] = attempts
        records.append(rec)
    return records


SOURCE_PARAMETERS = [
    {'family': 'radical', 'n': -1}, {'family': 'integer', 'n': -5},
    {'family': 'radical', 'n': 121}, {'family': 'radical', 'n': -4},
    {'family': 'fraction', 'n': -27, 'd': 3}, {'family': 'pi', 'sign': 1}]


def replay_sources():
    """Original presentation/banks, computed keys; incomplete legacy item is archival."""
    records = []
    for source, p in zip(DATA['questions'], SOURCE_PARAMETERS):
        rec = build(p)
        q = rec['question']; qid = uid('source-replay', source[':question/id'])
        q[':question/id'] = qid
        q[':question/problem'] = normalize_prose(source[':question/problem'])
        q[':question/answer-fields'] = []
        included = PATTERNS[number(p)[1]]
        for sf in source[':question/answer-fields']:
            kind = sf[':answer-field/type'][':db/ident'].split('/')[-1]
            label = sf[':answer-field/key']
            values = [a[':answer/value'] for a in sf[':answer-field/choices']]
            if kind == 'checkbox':
                s = label.split('($')[1][0]
                correct = str(s in included).lower()
            else:
                correct = '$N, Z, Q, R$, and $C$'
            q[':question/answer-fields'].append(field(label, correct, qid, values, kind))
        if source.get(':question/worked-solution'):
            # Immutable replay wording is source evidence; all keys are recomputed.
            q[':question/worked-solution'] = normalize_prose(source[':question/worked-solution'])
        rec['generation'].update(source_replay=source[':question/id'], replay_only=True,
                                 original_difficulty=source.get(':question/difficulty'),
                                 inferred_repair=':question/worked-solution' not in source)
        records.append(validate_generated_record(rec))
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    parser.add_argument('--replay-sources', action='store_true', help='archival fidelity evidence, not a delivery batch')
    args = parser.parse_args()
    try:
        records = replay_sources() if args.replay_sources else generate(args.difficulty, args.count, args.seed)
    except ValueError as e:
        parser.error(str(e))
    print(json.dumps(records, ensure_ascii=False, indent=2))



# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__ == '__main__':
    main()
