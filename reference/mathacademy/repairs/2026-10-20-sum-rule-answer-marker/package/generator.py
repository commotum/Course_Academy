#!/usr/bin/env python3
"""Seeded, relocatable sum-rule generator. No writes, assets, or database access."""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import random
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.4.2'
CONSTANT_TRIPLES = tuple(combinations(range(1, 7), 3))
BLANK_EXPLANATION = ('Any additive constant in an antiderivative can be absorbed '
                     'into the displayed arbitrary constant $C$.')
KP = {'db_id': 17592186184153, 'id': '0db9b1c3-1e31-53f6-9fc2-1c611e2f9398',
      'title': 'Computing an Integral Using the Sum Rule'}
SOURCES = {'P': 'q-71167', 'R': 'q-71169', 'B': 'q-133291'}


def frac(q):
    q = F(q)
    if q < 0:
        return '-' + frac(-q)
    return str(q.numerator) if q.denominator == 1 else rf'\frac{{{q.numerator}}}{{{q.denominator}}}'


def power(v, p, radical=True):
    p = F(p)
    if p == 0:
        return '1'
    assert p > 0
    base = v if p.numerator == 1 else rf'{v}^{{{p.numerator}}}'
    if p.denominator == 1:
        return base
    if not radical:
        return rf'{v}^{{{frac(p)}}}'
    return rf'\sqrt{{{base}}}' if p.denominator == 2 else rf'\sqrt[{p.denominator}]{{{base}}}'


def term(c, p, v, radical=True):
    c, p = F(c), F(p)
    c = abs(c)
    if p == 0:
        return frac(c)
    num = '' if c.numerator == 1 else str(c.numerator)
    den = '' if c.denominator == 1 else str(c.denominator)
    if p < 0:
        den += power(v, -p, radical)
        num = num or '1'
    else:
        num += power(v, p, radical)
    return rf'\frac{{{num}}}{{{den}}}' if den else num


def expression(terms, v, radical=True):
    parts = []
    for c, p in terms:
        c = F(c)
        if not c:
            continue
        sign = '-' if c < 0 else ('+' if parts else '')
        parts.append(sign + term(c, p, v, radical))
    return ''.join(parts) or '0'


def data(terms):
    return [[str(F(c)), str(F(p))] for c, p in terms]


def factor_domain(profile, n):
    # Polynomial errors use competing small divisors: fraction typography must
    # not expose the true divisor (in particular, for n=4 and n=6).
    if profile == 'P':
        return tuple(F(n + 1, d) for d in range(2, 10) if d != n + 1)
    if profile == 'R':
        if n == 3:
            return tuple(F(c,2) for c in (1,3,4,5,6))
        return tuple(F(n-2,d) for d in (3,7,9))
    return tuple(map(F, ('1/3', '1/2', '2/3', '3/2', '2', '3')))


def instance(profile, n, s, k, variable='x', constant_first=True, bank='grid', offset=None, factors=None, omitted_row=1, omitted_col=None, second_offset=None):
    if profile not in SOURCES or s not in (-1, 1) or k not in (*range(-6, 0), *range(1, 7)):
        raise ValueError('unsupported instance')
    if n not in ((3, 7) if profile == 'R' else (2, 3, 4, 5, 6)):
        raise ValueError('unsupported exponent')
    if variable not in ('x', 'y', 't') or (profile == 'B' and variable != 't'):
        raise ValueError('unsupported variable')
    paired_grid = profile in ('P','R') and bank == 'grid'
    eligible_offsets = [c-k for c in range(-6,7) if c*k>0 and c != k]
    if offset is None:
        offset = min(eligible_offsets, key=lambda d: (abs(d), d)) if paired_grid else 1
    if second_offset is None and paired_grid:
        second_offset = next(d for d in eligible_offsets if d != offset)
    if omitted_col is None:
        omitted_col = 1 if paired_grid else 2
    if factors is None:
        if paired_grid:
            factors = (F(n+1,n),) if profile == 'P' else ((F(1,2),) if n==3 else (F(n-2,3),))
        else:
            factors = (F(n+1,n), F(n+1,n+2)) if profile == 'P' else (F(1,2), F(2))
    if paired_grid:
        valid_grid = offset in eligible_offsets and second_offset in eligible_offsets and second_offset != offset and omitted_row in (0,1,2) and omitted_col in (0,1) and (omitted_row,omitted_col) != (0,0)
    else:
        valid_grid = omitted_row in (0,1) and omitted_col in (1,2) and second_offset is None
    factor_count = 1 if paired_grid else 2
    if bank not in ('grid','source') or (not paired_grid and offset not in (-3,-2,-1,1,2,3)) or len(factors)!=factor_count or len(set(map(F,factors)))!=factor_count or any(F(f) not in factor_domain(profile,n) for f in factors) or not valid_grid:
        raise ValueError('unsupported bank assignment')
    return dict(profile=profile, n=n, s=s, k=k, variable=variable, constant_first=constant_first, bank=bank, offset=offset, factors=list(map(str,factors)), omitted_row=omitted_row, omitted_col=omitted_col, second_offset=second_offset)


def mathematics(i):
    p = F(-i['n'], 2) if i['profile'] == 'R' else F(i['n'])
    s, k = F(i['s']), F(i['k'])
    q, a = p + 1, s / (p + 1)
    # Every expression is stored constant term then nonconstant term.
    integrand = [(k, 0), (s, p)]
    correct = [(k, 1), (a, q)]
    if i['profile'] == 'P':
        banks = [[(k, 1), (s, q)], [(k, 2), (s/2, q)], [(k, 0), (a, p)],
                 correct, [(k, 1), (-2*s/p, q)]]
        correct_index = 3
    elif i['profile'] == 'R':
        banks = [[(k-1, 1), (a/2, q)], [(-k, 1), (s, p)], [(-1, 1), (a/2, q)],
                 [(k, 1), (a/2, -q)], correct]
        correct_index = 4
    else:
        banks, correct_index = [correct], 0
    if i['profile'] != 'B' and i.get('bank') == 'grid':
        constants = [k, k + i['offset']]
        constants.append(k + i['second_offset'])
        coefficients = [a, *(a*F(f) for f in i['factors'])]
        banks = [[(c,1),(b,q)] for row,c in enumerate(constants) for col,b in enumerate(coefficients)
                 if (row,col) != (i['omitted_row'],i['omitted_col'])]
        correct_index = 0
    return integrand, correct, banks, correct_index


def ordered(terms, i):
    return terms if i['constant_first'] else list(reversed(terms))


def solution(i, integrand, correct):
    v = i['variable']
    given = expression(ordered(integrand, i), v)
    converted = expression(ordered(integrand, i), v, radical=False)
    pieces, rules = [], []
    for c, p in ordered(integrand, i):
        prefix = '-' if c < 0 else ('+' if pieces else '')
        coef = '' if abs(c) == 1 else str(abs(c))
        pieces.append(prefix + coef + rf'\int {power(v, p) if p > 0 else ("1" if p == 0 else v+"^{"+frac(p)+"}")}\,\mathrm{{d}}{v}')
        # Source stages explicitly show p+1 and division before simplification.
        exponent = frac(p)
        base = rf'\frac{{{v}^{{{exponent}+1}}}}{{({exponent}+1)}}'
        rules.append(prefix + coef + base)
    final = expression(ordered(correct, i), v)
    opening = 'Applying the sum rule, we compute the sum of the integrals of each function:'
    if i['profile'] == 'B':
        opening = rf'We know that $y\prime(t)={given}$.'.replace(r'y\prime', r"y'") + '\n\n' + opening
    rows = [rf'\int \left({given}\right)\,\mathrm{{d}}{v} &= \int \left({converted}\right)\,\mathrm{{d}}{v}',
            '&= ' + ''.join(pieces), '&= ' + ''.join(rules) + '+C', '&= ' + final + '+C']
    result = opening + '\n\n$$\n' + r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}' + '\n$$'
    return result + ('\n\n' + BLANK_EXPLANATION if i['profile'] == 'B' else '')


def record(problem, worked, values, correct_index, kind, difficulty, generation, rng=None):
    problem, worked = normalize_prose(problem), normalize_prose(worked)
    values = [normalize_tex(v) for v in values]
    if len(set(values)) != len(values):
        raise ValueError('coincident bank values')
    payload = json.dumps([problem, sorted(values), values[correct_index], kind, difficulty], sort_keys=True)
    qid = uuid.uuid5(uuid.UUID(KP['id']), payload)
    fid = uuid.uuid5(qid, 'field-1' if kind == 'blank' else 'selection')
    answers = [{':answer/id': str(uuid.uuid5(fid, value)), ':answer/type': ':answer.type/math', ':answer/value': value} for value in values]
    correct = answers[correct_index][':answer/id']
    if rng:
        rng.shuffle(answers)
    q = {':question/id': str(qid), ':question/problem': problem, ':question/worked-solution': worked,
         ':question/answer-fields': [{':answer-field/id': str(fid), ':answer-field/key': 'field-1' if kind == 'blank' else 'selection',
          ':answer-field/type': ':answer-field.type/' + kind, ':answer-field/choices': answers,
          ':answer-field/correct': [':answer/id', correct]}]}
    if difficulty:
        q[':question/difficulty'] = ':question.difficulty/' + difficulty
    return {'knowledge_point': KP, 'question': q, 'generation': generation, 'assets': {}}


@checked_math_content
def build(i, rng=None, seed=None):
    i = instance(**i)
    integrand, correct, banks, ci = mathematics(i)
    v = i['variable']
    given = expression(ordered(integrand, i), v)
    if i['profile'] == 'B':
        problem = rf"Given $y'(t)={given}$, find $y(t)$, the antiderivative of $y'(t)$." + '\n\n$y(t)=$\n{{field-1}}\n$+\\,C$'
    elif i['profile'] == 'R':
        problem = rf'Find the integral of ${given}$ for ${v}>0$.'
    else:
        problem = rf'$\displaystyle\int \left({given}\right)\,\mathrm{{d}}{v}=$'
    values = [expression(ordered(b, i), v) + ('' if i['profile'] == 'B' else '+C') for b in banks]
    generation = {'version': VERSION, 'seed': seed, 'template': i['profile'], 'profile': i['profile'] + ('-grid' if i['profile'] != 'B' and i.get('bank') == 'grid' else '-source'),
                  'source_refs': [SOURCES[i['profile']]], 'parameters': i,
                  'domain': f'{v}>0' if i['profile'] == 'R' else 'real',
                  'integrand_terms': data(integrand), 'answer_terms': data(correct),
                  'bank_terms': [data(b) for b in banks], 'correct_recipe': ci}
    return record(problem, solution(i, integrand, correct), values, ci, 'blank' if i['profile'] == 'B' else 'radio', 'moderate', generation, rng)


def generate(difficulty='moderate', count=5, seed=0):
    if difficulty != 'moderate':
        raise ValueError('Only moderate is supported; easy has no source labels and hard has no response fields.')
    if count < 0:
        raise ValueError('count must be nonnegative')
    rng = random.Random(seed)
    records = []
    for _ in range(count):
        profile = rng.choice(('P', 'R', 'B'))
        s = rng.choice((-1, 1))
        n = rng.choice((3, 7) if profile == 'R' else (2, 3, 4, 5, 6))
        if profile in ('P','R'):
            side = rng.choice((-1,1))
            factors = [rng.choice([f for f in factor_domain(profile,n) if (f > 1) == (side > 0)])]
            # Every non-key cell is equally eligible for omission. Excluding
            # the correct row would make the singleton constant always wrong.
            omitted_row, omitted_col = rng.choice(((0,1),(1,0),(1,1),(2,0),(2,1)))
        else:
            factors = rng.sample(factor_domain(profile,n),2)
            omitted_row, omitted_col = rng.choice((0,1)), rng.choice((1,2))
        ksign = rng.choice((-1, 1))
        second_offset = None
        if profile in ('P','R'):
            rank = rng.choice((0,1,2))
            constants = rng.choice(CONSTANT_TRIPLES)
            k = ksign * constants[rank]
            others = [ksign*c for j,c in enumerate(constants) if j != rank]
            rng.shuffle(others)
            offset, second_offset = (c-k for c in others)
        else:
            k = ksign * rng.randint(1, 6)
            offset = 1
        v = 't' if profile == 'B' else rng.choice(('x', 'y', 't'))
        i = instance(profile, n, s, k, v, rng.choice((True, False)), offset=offset, factors=factors, omitted_row=omitted_row, omitted_col=omitted_col, second_offset=second_offset)
        records.append(build(i, rng, seed))
    return records


# Immutable source replay. Missing fields are not silently invented.
SOURCE_MATH = {
    'q-2159': ('x', [(1, F(1, 2)), (-3, 0)], [(F(2, 3), F(3, 2)), (-3, 1)], 1),
    'q-29828': ('x', [(1, F(5, 2)), (1, F(-5, 2))], [(F(2, 7), F(7, 2)), (F(-2, 3), F(-3, 2))], 2),
    'q-113781': ('x', [(1, F(1, 4)), (-1, 5)], [(F(4, 5), F(5, 4)), (F(-1, 6), 6)], None),
    'q-71169': ('x', [(1, F(-3, 2)), (4, 0)], [(-2, F(-1, 2)), (4, 1)], 4),
    'q-71173': ('y', [(2, 0), (1, -5)], [(2, 1), (F(-1, 4), -4)], None),
    'q-133291': ('t', [(1, 2), (-2, 0)], [(F(1, 3), 3), (-2, 1)], 0),
    'q-71167': ('x', [(5, 0), (-1, 3)], [(5, 1), (F(-1, 4), 4)], 3),
}


def replay_sources():
    sources = json.loads(Path(__file__).with_name('source-data.json').read_text())
    result = []
    for q in sources:
        ref = q[':question/math-academy-id']
        v, integrand, correct, ci = SOURCE_MATH[ref]
        diff = q.get(':question/difficulty', {}).get(':db/ident', '').split('/')[-1] or None
        gen = {'version': VERSION, 'template': 'source-replay', 'source_refs': [ref], 'original_difficulty': diff,
               'integrand_terms': data(integrand), 'answer_terms': data(correct), 'variable': v}
        fields = q.get(':question/answer-fields')
        if not fields:
            result.append({'source_ref': ref, 'original_problem': q[':question/problem'],
                           'original_solution': q[':question/worked-solution'], 'math_only': True, 'generation': gen})
            continue
        f = fields[0]
        ci = next((j for j, a in enumerate(f[':answer-field/choices']) if a[':answer/id'] == f.get(':answer-field/correct', {}).get(':answer/id')), ci)
        values = [a[':answer/value'] for a in f[':answer-field/choices']]
        prompt = q[':question/problem']
        if ref == 'q-133291':
            prompt = "$y'(t)=t^2-2.$\n\n" + prompt
            gen['source_correction'] = 'Restored derivative supplied only by original worked solution.'
        worked = q.get(':question/worked-solution')
        if not worked:
            terms = [rf'\int {expression([(c,p)], v, False)}\,\mathrm{{d}}{v}' for c,p in integrand]
            worked = 'Applying the sum rule, integrate each power separately:\n\n$$\n' + ' + '.join(terms) + '=' + expression(correct,v) + '+C\n$$'
            gen['reconstructed'] = ['missing correct link', 'missing worked solution']
        if ref == 'q-133291':
            worked += '\n\n' + BLANK_EXPLANATION
        result.append(record(prompt, worked, values, ci, f[':answer-field/type'][':db/ident'].split('/')[-1], diff, gen))
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--difficulty', default='moderate', choices=['easy', 'moderate', 'hard'])
    p.add_argument('--count', default=5, type=int)
    p.add_argument('--seed', default=0, type=int)
    p.add_argument('--format', default='json', choices=['json'])
    p.add_argument('--replay-source', action='store_true')
    a = p.parse_args()
    try:
        records = replay_sources() if a.replay_source else generate(a.difficulty, a.count, a.seed)
    except ValueError as e:
        p.error(str(e))
    print(json.dumps(records, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
