#!/usr/bin/env python3
"""Portable seeded generator for classification of two linear equations."""
import argparse
from fractions import Fraction as Q
import json
import random
import uuid
from math_format import checked_math_content, normalize_prose, system_tex

VERSION = '1.0.2'
KP_ID = 17592186198348
TITLE = 'Classifying Systems Using Consistency and Dependency Terminology'
LABELS = ('inconsistent', 'consistent independent', 'consistent dependent')
MULTIPLIERS = tuple(Q(v) for v in ('-3','-2','-1','-1/2','-1/3','1/3','1/2','1','2','3'))
SOURCES = ('b99e7b41-579d-5810-b39e-9c4f595ea791', '127d9f27-4818-5fd8-bdfc-a496df1a7d59')
CANONICAL = '81cc631d-2430-5db0-aa17-718a6f090c42'
IMAGE = 'images/16/1692fbea298339ff839cf2f14986d51af45d1ec72b2b7d0de179336bdef40c0e.png'
INTRO = '''A system of equations is *consistent* if it has at least one solution. Otherwise, it is called *inconsistent*.

Consistent systems, in turn, can be of the following two types:

- When a system of equations has a *single* solution, it is called *consistent independent*.
- When a system of equations has an *infinite number* of solutions, it is called *consistent dependent*.

We can summarize these definitions using the diagram shown below.

![](''' + IMAGE + ')'


def tex(n):
    n = Q(n)
    if n.denominator == 1:
        return str(n.numerator)
    return ('-' if n < 0 else '') + rf'\frac{{{abs(n.numerator)}}}{{{n.denominator}}}'


def expr(*terms):
    """Signed linear expression; each term is (exact coefficient, TeX atom)."""
    out = ''
    for coeff, atom in terms:
        coeff = Q(coeff)
        if not coeff:
            continue
        term = ('' if atom and abs(coeff) == 1 else tex(abs(coeff))) + atom
        out += (('-' if coeff < 0 else '') if not out else (' - ' if coeff < 0 else ' + ')) + term
    return out or '0'


def display(rows, brace=False):
    if brace:
        value = system_tex(rows)
    else:
        value = r'\begin{aligned}' + r' \\ '.join(row.replace('=', '&=', 1) for row in rows) + r'\end{aligned}'
    return '$$\n' + value + '\n$$'


def equations(params, layout):
    a,b,c,d,e,f = params
    if layout == 'standard':
        return [f'{expr((a,"x"),(b,"y"))} = {c}', f'{expr((d,"x"),(e,"y"))} = {f}']
    if layout == 'rearranged':
        return [f'{expr((a,"x"))} = {expr((c,""),(-b,"y"))}', f'{expr((e,"y"))} = {expr((f,""),(-d,"x"))}']
    if layout == 'canonical':
        return [f'{expr((a,"x"),(b,"y"),(-c,""))} = 0', f'{expr((d,"x"),(e,"y"))} = {f}']
    raise ValueError('Unknown layout')


def classify(params):
    a,b,c,d,e,f = params
    # Substitute x = p + q y into equation 2.
    p,q = Q(c,a), Q(-b,a)
    constant, coefficient = d*p, d*q+e
    result = LABELS[1] if coefficient else LABELS[2] if constant == f else LABELS[0]
    return result, p, q, constant, coefficient


def solution(params, layout):
    a,b,c,d,e,f = params
    label,p,q,constant,coefficient = classify(params)
    eqs = equations(params, layout)
    isolated = expr((p,''),(q,'y'))
    rearranged = expr((c,''),(-b,'y'))
    first = [eqs[0]]
    if a != 1 and eqs[0] != f'{expr((a,"x"))} = {rearranged}':
        first.append(f'{expr((a,"x"))} = {rearranged}')
    first.append(f'x = {isolated}')
    first = [row for i,row in enumerate(first) if i == 0 or row != first[i-1]]
    # Maintain each layout's supplied second equation during substitution.
    substituted_x = r'\left(' + isolated + r'\right)'
    if layout == 'rearranged':
        rows = [eqs[1], f'{expr((e,"y"))} = {expr((f,""),(-d,substituted_x))}',
                f'{expr((e,"y"))} = {expr((f,""),(-d*p,""),(-d*q,"y"))}',
                f'{expr((coefficient,"y"))} = {tex(f-constant)}']
    else:
        rows = [eqs[1], f'{expr((d,substituted_x),(e,"y"))} = {f}',
                f'{expr((constant,""),(d*q,"y"),(e,"y"))} = {f}']
        if coefficient:
            rows.append(f'{expr((coefficient,"y"))} = {tex(f-constant)}')
        else:
            rows.append(f'{tex(constant)} = {f}')
    if coefficient:
        final_row = f'y = {tex((f-constant)/coefficient)}'
        if rows[-1] != final_row:
            rows.append(final_row)
        conclusion = ('Because we obtained a single value of $y$, and $x$ is determined by '
                      f'$x={isolated}$, there is exactly one solution to the system. Therefore, the system is {label}.')
    elif label == LABELS[2]:
        conclusion = ('Because we obtained a true statement, we conclude that there are infinitely many solutions '
                      'to the system. Therefore, the system is consistent dependent.')
    else:
        conclusion = ('Because we obtained a false statement, we conclude that there are no solutions '
                      'to the system. Therefore, the system is inconsistent.')
    return normalize_prose(INTRO + '\n\nWe will solve the system using substitution.\n\n'
        'First, we can solve the first equation for $x$, as follows:\n\n' + display(first) +
        '\n\nThen, we can substitute\n\n' + display([f'x={isolated}']) +
        '\n\ninto the second equation to obtain an equation that we can solve for $y$:\n\n' +
        display(rows) + '\n\n' + conclusion)


def uid(s):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy/classification/' + s))


@checked_math_content
def generate(params, layout='standard', *, seed=None, source_id=None):
    params = tuple(params)
    if len(params) != 6 or any(type(v) is not int for v in params):
        raise ValueError('Six integer coefficients required')
    if any(params[i] == 0 for i in (0,1,3,4)):
        raise ValueError('Both variable coefficients in each equation must be nonzero')
    rows = equations(params, layout)
    if rows[0] == rows[1]:
        raise ValueError('The two displayed equations must be distinct')
    label = classify(params)[0]
    prefix = ('Determine whether the following system of equations is consistent or inconsistent. '
              'If it is consistent, indicate whether it is consistent dependent or consistent independent.'
              if layout == 'canonical' else 'Consider the following system of equations.')
    prompt = normalize_prose(prefix + '\n\n' + display(rows,True) +
                             '\n\nThis system of equations is {{field-1}}.')
    worked = solution(params, layout)
    question_id = uid(prompt + '\n' + worked)
    field_id = uid(question_id + '/field-1')
    choices = [{':answer/id':uid(field_id+'/'+v), ':answer/type':':answer.type/text', ':answer/value':v} for v in LABELS]
    return {'knowledge_point':{'db_id':KP_ID,'id':'043ca35d-acf2-5503-871a-1f15b379186f','title':TITLE},
        'question':{':question/id':question_id, ':question/difficulty':':question.difficulty/moderate',
                    ':question/problem':prompt, ':question/worked-solution':worked,
                    ':question/answer-fields':[{':answer-field/id':field_id, ':answer-field/key':'field-1',
                      ':answer-field/type':':answer-field.type/select', ':answer-field/choices':choices,
                      ':answer-field/correct':[':answer/id',next(v[':answer/id'] for v in choices if v[':answer/value']==label)]}]},
        'generation':{'generator_version':VERSION,'template':layout,'bank_profile':'three-classifications',
            'seed':seed, 'parameters':dict(zip('ABCDEF',params)), 'domain':'real x,y; nonzero integer variable coefficients',
            'difficulty':'moderate','source_difficulty':None,'source_question_ids':list(SOURCES),
            'canonical_example_id':CANONICAL,'replay_source_id':source_id,
            'source_basis':2861, 'dependencies':{'python':'3.13.5','packages':{}},
            'solution_provenance':'authored from canonical substitution stages; practice solutions absent'}}


def sample(rng, outcome, layout='standard'):
    small = [v for v in range(-6,7) if v]
    large = [v for v in range(-12,13) if v]
    while True:
        a,b,c = rng.choice(small),rng.choice(small),rng.randint(-12,12)
        if outcome == LABELS[1]:
            d,e,f = rng.choice(large),rng.choice(large),rng.randint(-24,24)
            if a*e == b*d:
                continue
            y = Q(a*f-d*c,a*e-b*d)
            if y.denominator > 12 or abs(y) > 12:
                continue
        else:
            k = rng.choice(MULTIPLIERS)
            d,e = k*a,k*b
            f = k*c + (rng.choice([-3,-2,-1,1,2,3]) if outcome == LABELS[0] else 0)
            if any(v.denominator != 1 for v in (d,e,f)):
                continue
            d,e,f = int(d),int(e),int(f)
            if max(abs(d),abs(e))>12 or abs(f)>24:
                continue
        params = (a,b,c,d,e,f)
        rows = equations(params, layout)
        if rows[0] == rows[1]:
            continue
        return params


def semantic_key(params):
    a,b,c,d,e,f = params
    return tuple(sorted(((Q(b,a),Q(c,a)),(Q(e,d),Q(f,d)))))


def batch(difficulty, count, seed):
    if difficulty not in ('moderate','unclassified'):
        raise ValueError('Unsupported difficulty; supported band: moderate')
    if count < 0:
        raise ValueError('count must be nonnegative')
    rng = random.Random(seed)
    # Cycle a shuffled cross product to exercise all outcomes and all three source-supported layouts.
    profiles = [(layout,label) for layout in ('standard','rearranged','canonical') for label in LABELS]
    rng.shuffle(profiles)
    records, seen = [], set()
    for i in range(count):
        layout,label = profiles[i % len(profiles)]
        for attempt in range(10000):
            params = sample(rng,label,layout)
            key = semantic_key(params)
            if key not in seen:
                seen.add(key)
                records.append(generate(params,layout,seed=seed))
                break
        else:
            raise ValueError('Unique instance domain exhausted')
    return records


def replay():
    return [generate((6,-3,-3,-2,1,1),'standard',source_id=SOURCES[0]),
            generate((6,-2,4,12,3,9),'rearranged',source_id=SOURCES[1])]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='moderate',choices=['unclassified','easy','moderate','hard'])
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    args = parser.parse_args()
    try:
        records = batch(args.difficulty,args.count,args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
