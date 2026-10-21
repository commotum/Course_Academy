#!/usr/bin/env python3
"""Seeded moderate natural-logarithm equation practice; no filesystem writes."""
import argparse
import copy
import json
from pathlib import Path
import random
import uuid
from fractions import Fraction
from math_format import checked_math_content, normalize_prose, normalize_tex

KP_ID = '4d8c6c93-9d15-5482-8130-25bb9cabf008'
SOURCE_ID = 'ba9070de-c707-5661-a14c-cac1b4371745'
VERSION = '1.0.1'

def identity(text):
    return str(uuid.uuid5(uuid.UUID(KP_ID), text))

def term(a, v):
    return ('-' if a < 0 else '') + (str(abs(a)) if abs(a) != 1 else '') + v

def exponent(a, b, v, order):
    av = term(a, v)
    if order == 'constant-first':
        return str(b) + ('+' if a > 0 else '') + av
    return av + ('+' if b > 0 else '') + str(b)

def log(n):
    return rf'\ln({n})'

def numerator(b, n):
    return log(n) + ('+' + str(-b) if b < 0 else '-' + str(b))

def answer(a, b, n):
    top = numerator(b,n) if a > 0 else str(b) + '-' + log(n)
    return rf'\frac{{{top}}}{{{abs(a)}}}'

def rational(q):
    q = Fraction(q)
    sign = '-' if q < 0 else ''
    return sign + (str(abs(q.numerator)) if q.denominator == 1 else rf'\frac{{{abs(q.numerator)}}}{{{q.denominator}}}')

def distributed(a,b,n):
    constant = rational(Fraction(-b,a))
    coefficient = Fraction(1,a)
    return constant + ('+' if coefficient > 0 else '-') + rational(abs(coefficient)) + log(n)

@checked_math_content
def build(a, b, n, v='y', order='constant-first', *, replay=False, seed=None):
    if not (2 <= abs(a) <= 7 and 1 <= abs(b) <= 9 and 2 <= n <= 30):
        raise ValueError('Parameters outside the supported moderate domain')
    if v not in ('x','y','t') or order not in ('constant-first','variable-first'):
        raise ValueError('Invalid presentation slot')
    exp = exponent(a,b,v,order)
    result = answer(a,b,n)
    problem = f'Find the **exact** solution of the equation $e^{{{exp}}}={n}.$\n\n${v}=$\n{{{{field-1}}}}'
    solution = (
        'First, we find the natural logarithm $(\\ln)$ of both sides of the equation:\n\n'
        '$$\n' + rf'\begin{{aligned}}e^{{{exp}}}&={n} \\ \ln(e^{{{exp}}})&={log(n)}\end{{aligned}}' + '\n$$\n\n'
        'Now, we use the fact that $\\ln(e^u)=u$ to simplify the left-hand side. This gives\n\n'
        '$$\n' + exp + '=' + log(n) + '.\n$$\n\n'
        f'Finally, we solve for ${v},$ as follows:\n\n$$\n'
        + rf'\begin{{aligned}}{exp}&={log(n)} \\ {term(a,v)}&={numerator(b,n)} \\ {v}&=\frac{{1}}{{{a}}}\left({numerator(b,n)}\right) \\ {v}&={distributed(a,b,n)}\end{{aligned}}'
        + f'\n$$\n\nTherefore, the solution is ${v}={distributed(a,b,n)}.$'
    )
    if replay:
        if (a,b,n,v,order) != (-5,4,21,'y','constant-first'):
            raise ValueError('Replay must use original parameters')
        original = json.loads(Path(__file__).with_name('source-replay.json').read_text())
        problem = original[':question/problem']
        solution = original[':question/worked-solution']
        result = original[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
    problem, solution, result = normalize_prose(problem), normalize_prose(solution), normalize_tex(result)
    qid = identity(problem + '\n' + result)
    fid = identity(qid + '/field-1')
    aid = identity(fid + '/' + result)
    field = {':answer-field/id':fid, ':answer-field/key':'field-1',
             ':answer-field/type':':answer-field.type/blank',
             ':answer-field/choices':[{':answer/id':aid, ':answer/type':':answer.type/math', ':answer/value':result}],
             ':answer-field/correct':[':answer/id',aid]}
    return {'knowledge_point':{'db_id':17592186087689,'id':KP_ID,
                              'title':'Finding Exact Solutions to Exponential Equations Using the Natural Logarithm'},
            'question':{':question/id':qid, ':question/difficulty':':question.difficulty/moderate',
                        ':question/problem':problem, ':question/worked-solution':solution, ':question/answer-fields':[field]},
            'generation':{'generator_version':VERSION, 'template':'affine-integer-rhs-blank',
                          'profile':'source-blank', 'source_question_ids':[SOURCE_ID],
                          'parameters':{'a':a,'b':b,'n':n,'variable':v,'order':order},
                          'decision_case':('positive' if a>0 else 'negative')+'-coefficient/'+('positive' if b>0 else 'negative')+'-offset',
                          'seed':seed, 'source_replay':replay, 'dependencies':{'python':'3.13.5','packages':{}}},
            'assets':{}}

def generate(count, seed, difficulty='moderate'):
    if difficulty == 'unclassified':
        difficulty = 'moderate'
    if difficulty != 'moderate':
        raise ValueError('Unsupported difficulty: '+difficulty+'; only moderate is supported')
    if not 0 <= count <= 6264:
        raise ValueError('count must be in 0..6264 (finite semantic family)')
    rng = random.Random(seed)
    # Choose the eligible sign roles first, then compatible values. No mathematical rejection.
    seen, records = set(), []
    while len(records) < count:
        sa,sb = rng.choice([(1,1),(1,-1),(-1,1),(-1,-1)])
        a,b,n = sa*rng.randint(2,7), sb*rng.randint(1,9), rng.randint(2,30)
        if (a,b,n) in seen:
            continue
        seen.add((a,b,n))
        records.append(build(a,b,n,rng.choice(('x','y','t')),rng.choice(('constant-first','variable-first')),seed=seed))
    return records

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='moderate')
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    parser.add_argument('--replay-source', action='store_true')
    args = parser.parse_args()
    if args.replay_source:
        if args.difficulty not in ('moderate','unclassified'):
            parser.error('source replay is moderate')
        records = [build(-5,4,21,replay=True,seed=args.seed)]
    else:
        try:
            records = generate(args.count,args.seed,args.difficulty)
        except ValueError as exc:
            parser.error(str(exc))
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
