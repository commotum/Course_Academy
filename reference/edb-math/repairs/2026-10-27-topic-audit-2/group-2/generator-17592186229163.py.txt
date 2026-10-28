#!/usr/bin/env python3
"""Particular solutions with one resonant exponential; relocatable seeded package.

Adapted from scratch/17592186229163.py: coefficient formatting, trial/product-rule/
substitution stages, blank schema and field-owned UUIDs. Hard extends to three
modes per the supplied investigation rather than stacking signs/fractions.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import itertools
import math
import json
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP_ID = 17592186229163
KP_UUID = '3c7ce128-42e5-5a5a-8fa2-0e897504ff9d'
TITLE = 'Finding a Particular Solution When the Forcing Term is Part of the Complementary Solution'
VERSION = 'resonant-first-order-2.2'
DEFAULT = 'moderate'
LETTERS = [r'\alpha ', r'\beta ', r'\gamma ']

def coeff(value):
    v = Fraction(value)
    if v == 1: return ''
    if v == -1: return '-'
    if v.denominator == 1: return str(v.numerator)
    return ('-' if v < 0 else '') + r'\frac{' + str(abs(v.numerator)) + '}{' + str(v.denominator) + '}'

def term(value, body):
    return coeff(value) + body if value else '0'

def join(parts):
    return ''.join(('' if i == 0 or p.startswith('-') else '+') + p for i, p in enumerate(parts))

def exp(rate):
    return 'e^{' + term(rate, 'x') + '}'

def block(body):
    return '$$\n' + body + '\n$$'

def aligned(rows):
    return block('\\begin{aligned}\n' + '\\\\\n'.join(rows) + '\n\\end{aligned}')

def check_instance(level, r, modes):
    n = {'easy': 1, 'moderate': 2, 'hard': 3}[level]
    if type(r) is not int or not 1 <= abs(r) <= 6 or len(modes) != n:
        raise ValueError('Invalid rate or number of modes')
    rates = [s for s, _ in modes]
    if len(set(rates)) != n or rates.count(r) != 1:
        raise ValueError('Exactly one distinct forcing mode must resonate')
    if any(type(s) is not int or not 1 <= abs(s) <= 6 or type(f) is not int or not 1 <= abs(f) <= 30 for s, f in modes):
        raise ValueError('Bounded nonzero integer rates and forcing required')
    if any(abs(Fraction(f, 1 if s == r else s-r).numerator) > 30 or Fraction(f, 1 if s == r else s-r).denominator > 12 for s, f in modes):
        raise ValueError('Coefficient workload exceeded')

def build(level, r, modes, *, source_ids=(), replay_values=None):
    modes = [tuple(t) for t in modes]
    check_instance(level, r, modes)
    rhs = join([term(f, exp(s)) for s, f in modes])
    lhs = "y'" + join(['', term(-r, 'y')])
    bases = [('x' if s == r else '') + exp(s) for s, _ in modes]
    trial = join([a + b for a, b in zip(LETTERS, bases)])
    values = [Fraction(f, 1 if s == r else s-r) for s, f in modes]
    final = join([term(v, b) for v, b in zip(values, bases)])
    derivative_formal, derivative_product, derivative = [], [], []
    collected, reduced, equations, solved = [], [], [], []
    for a, (s, f), v in zip(LETTERS, modes, values):
        e = exp(s)
        if s == r:
            derivative_formal.append(a + '(x' + e + ")'")
            derivative_product.append(a + '(' + join([e, term(s, 'x' + e)]) + ')')
            derivative.append(a + '(' + join(['1', term(s, 'x')]) + ')' + e)
            collected.append('(' + join(['1', term(s, 'x'), term(-r, 'x')]) + ')' + a + e)
            reduced.append(a + e)
        else:
            derivative_formal.append(a + '(' + e + ")'")
            derivative_product.append(term(s, a + e))
            derivative.append(term(s, a + e))
            collected.append('(' + join([term(s, a), term(-r, a)]) + ')' + e)
            reduced.append(term(s-r, a + e))
        equations.append(term(1 if s == r else s-r, a) + '=' + str(f))
        solved.append(a + '=' + (coeff(v) if abs(v) != 1 else str(v.numerator)))
    d = join(derivative)
    if len(modes)==1:
        substitution_rows=[lhs.replace('y','y_p')+'&=('+d+')'+join(['',term(-r,'('+trial+')')]),
                           '&='+join(collected), '&='+join(reduced)+'='+rhs+'.']
    else:
        substitution_rows=[lhs.replace('y','y_p')+'&=('+d+')',
                           r'&\quad '+join(['',term(-r,'('+trial+')')]),
                           '&='+collected[0]]
        substitution_rows.extend(r'&\quad +'+part for part in collected[1:])
        substitution_rows.append('&='+join(reduced)+'.')
    resonant = exp(r)
    prompt = ('Given that the differential equation\n\n' + block(lhs + '=' + rhs + ',')
              + '\n\nhas the complementary solution $y_c(x)=A' + resonant
              + '$, find a particular solution. Do not add a multiple of the complementary solution.'
              + '\n\n$y_p(x)=$\n{{field-1}}')
    solution = ('The exponential $' + resonant + '$ occurs in the complementary solution. '
                + 'An unmodified trial for that mode would give zero on the left, so multiply '
                + 'only that trial by $x$.'
                + (' The other forcing exponentials do not occur in the complementary solution.' if len(modes)>1 else '')
                + ' Take\n\n' + block('y_p=' + trial + '.')
                + '\n\nDifferentiate, using the product rule on the resonant term:\n\n'
                + aligned(["y_p'&=" + join(derivative_formal), '&=' + join(derivative_product), '&=' + d + '.'])
                + '\n\nSubstitute into the differential equation and collect like exponentials:\n\n'
                + aligned(substitution_rows)
                + '\n\nThis must equal $'+rhs+'$. Equating the coefficient of each distinct exponential gives\n\n'
                + block(r',\qquad '.join(equations) + '.')
                + '\n\nSolving these coefficient equations,\n\n'
                + block(r',\qquad '.join(solved) + '.')
                + '\n\nTherefore, a particular solution is\n\n' + block('y_p(x)=' + final + '.'))
    # Shared normalization happens before identities, for source replay and practice.
    prompt, solution = normalize_prose(prompt), normalize_prose(solution)
    answer_values = [normalize_tex(v) for v in (replay_values or [final])]
    # Replay can preserve synonymous imported answers; normal practice has one.
    canonical = normalize_tex(final)
    content = json.dumps([level, prompt, solution, answer_values], ensure_ascii=False)
    qid = str(uuid.uuid5(uuid.UUID(KP_UUID), content))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'field-1'))
    answers = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), str(i) + ':' + v)),
                ':answer/type': ':answer.type/math', ':answer/value': v} for i,v in enumerate(answer_values)]
    record = {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
              'question': {':question/id': qid, ':question/difficulty': ':question.difficulty/' + level,
                           ':question/problem': prompt, ':question/worked-solution': solution,
                           ':question/answer-fields': [{':answer-field/id': fid, ':answer-field/key': 'field-1',
                           ':answer-field/type': ':answer-field.type/blank', ':answer-field/choices': answers,
                           ':answer-field/correct': [':answer/id', answers[0][':answer/id']]}]},
              'generation': {'version': VERSION, 'template': 'resonant_' + str(len(modes)) + '_mode',
                             'parameters': {'r': r, 'modes': modes}, 'source_ids': list(source_ids),
                             'domain': 'x real', 'canonical_derivation_final': canonical,
                             'authored_extension': level == 'hard', 'bank_profile': 'blank',
                             'content_fingerprint': hashlib.sha256(content.encode()).hexdigest()}}
    return validate_generated_record(record)

def signatures(level):
    rates = [-3,-2,-1,1,2,3] if level == 'hard' else list(range(-6,0)) + list(range(1,7))
    n = {'easy':1, 'moderate':2, 'hard':3}[level]
    return [(r, (r,) + others) for r in rates for others in itertools.combinations([s for s in rates if s != r], n-1)]

def batch_capacity(level):
    # Term order does not create another mathematical instance. Count each
    # operator/rate signature and the independent eligible forcing assignments.
    total = 0
    for r, rates in signatures(level):
        if level == 'easy':
            sizes = [11]
        elif level == 'moderate':
            sizes = [22] * len(rates)
        else:
            sizes = [sum(1 for b in range(-4, 5)
                         if b and abs(b * (1 if s == r else s-r)) <= 12)
                     for s in rates]
        total += math.prod(sizes)
    return total

def sample_batch(level, count, seed):
    if type(count) is not int or count < 1:
        raise ValueError('count must be a positive integer')
    capacity = batch_capacity(level)
    if count > capacity:
        raise ValueError(f'{level} supports at most {capacity} distinct instances; requested {count}')
    rng = random.Random(seed)
    catalog = signatures(level)
    output, seen = [], set()
    n = {'easy': 1, 'moderate': 2, 'hard': 3}[level]
    position_counts = {False: [0] * n, True: [0] * n}
    while len(output) < count:
        rng.shuffle(catalog)
        for r, rates in catalog:
            ordered = list(rates)
            rng.shuffle(ordered)  # resonance position is chosen before coefficients
            modes=[]
            for s in ordered:
                if level == 'easy': f = rng.randint(2,12)
                elif level == 'moderate': f = rng.choice([-1,1]) * rng.randint(2,12)
                else:
                    choices=[b for b in range(-4,5) if b and abs(b*(1 if s==r else s-r))<=12]
                    f = rng.choice(choices)*(1 if s==r else s-r)
                modes.append((s,f))
            # Canonical mathematical instance ignores term order.
            key=(r,tuple(sorted(modes)))
            if key in seen: continue
            seen.add(key)
            # A short delivered pool must not teach a fixed resonance position,
            # even conditionally on the visibly recognizable operator sign.
            counts = position_counts[r > 0]
            positions = [i for i, used in enumerate(counts) if used == min(counts)]
            position = rng.choice(positions)
            resonant = next(mode for mode in modes if mode[0] == r)
            modes = [mode for mode in modes if mode[0] != r]
            modes.insert(position, resonant)
            counts[position] += 1
            rec=build(level,r,modes)
            rec['generation']['seed']=seed
            rec['generation']['batch_index']=len(output)
            output.append(rec)
            if len(output)==count: return output
    return output

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty', choices=['easy','moderate','hard','unclassified','all'], default=DEFAULT)
    ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json')
    a=ap.parse_args()
    if a.count<1: ap.error('count must be positive')
    levels=['easy','moderate','hard'] if a.difficulty=='all' else [DEFAULT if a.difficulty=='unclassified' else a.difficulty]
    try:
        records=[record for level in levels for record in sample_batch(level,a.count,a.seed)]
    except ValueError as exc:
        ap.error(str(exc))
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
