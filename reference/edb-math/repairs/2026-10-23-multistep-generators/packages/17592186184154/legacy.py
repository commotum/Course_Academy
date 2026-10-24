#!/usr/bin/env python3
"""Relocatable moderate two-term integration generator; no external writes."""
import argparse
import itertools
import json
import random
import uuid

import sympy as s
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.1.0'
KP = 'a58c0a18-4221-50f1-b31c-ae58d099d79d'
TITLE = 'Computing an Integral Using the Sum and Constant Factor Rules'
X = s.Symbol('x', positive=True)
R = s.Rational
SOURCE_RECIPROCALS = (-1, -2, -1, -1, -3)
# Distinct polynomial components may share reciprocal exponents; the two
# identical polynomial components (indices 1,2) must stay distinguishable.
QUOTIENT_PAIRINGS = tuple(sorted({v for v in itertools.permutations(SOURCE_RECIPROCALS)
                                  if v[1] != v[2]}))
SOURCES = {
    'quotient': ['c3b5e67d-32a5-5a89-860d-1eeac5fbca6e'],
    'radical': ['aa2d5333-814d-52c3-9ed1-e83660135b41'],
    'blank': ['221f7f46-e501-5c4b-9474-541896c7450d',
              '8913b80e-2bcb-5364-9080-3c746725b920',
              '002408ea-9be6-53e5-9b20-0951e4cd4bad'],
}


def bank(family, a, b, p=4, reciprocal_exponents=None):
    a, b = R(a), R(b)
    if family == 'quotient':
        choices = [[(a/p, p), (-b, -1)],
                [(a/(p-1), p-1), (-b, -2)],
                [(a/(p-1), p-1), (-b, -1)],
                [(a/p, p-1), (-b, -1)],
                [(a/(p+2), p+2), (-b, -3)]]
        exponents = SOURCE_RECIPROCALS if reciprocal_exponents is None else tuple(reciprocal_exponents)
        if exponents not in QUOTIENT_PAIRINGS:
            raise ValueError('Invalid quotient component assignment')
        return [[terms[0], (-b, e)] for terms, e in zip(choices, exponents)]
    if family == 'radical':
        return [[(2*a/5, R(5,2)), (2*b/3, R(3,2))],
                [(2*a/3, R(3,2)), (-2*b, R(-1,2))],
                [(2*a/3, R(3,2)), (2*b, R(-1,2))],
                [(5*a/2, R(5,2)), (3*b/2, R(3,2))],
                [(a/5, R(5,2)), (b/3, R(3,2))]]
    raise ValueError('Unknown bank family')


def expression(terms):
    return s.Add(*(c*X**p for c, p in terms))


def term_tex(c, p):
    """A positive coefficient times a power, in the sources' radical notation."""
    c, p = R(c), R(p)
    assert c > 0
    if p == 0:
        return s.latex(c)
    power = 'x' if abs(p) == 1 else (
        r'\sqrt{x}' if abs(p) == R(1,2) else
        (r'\sqrt{x^{' + str(abs(p.p)) + '}}' if p.q == 2 else
         'x^{' + str(abs(p)) + '}'))
    num = '' if c.p == 1 else str(c.p)
    if p > 0:
        num += power
        return num if c.q == 1 else r'\frac{' + num + '}{' + str(c.q) + '}'
    den = ('' if c.q == 1 else str(c.q)) + power
    return r'\frac{' + str(c.p) + '}{' + den + '}'


def sum_tex(terms):
    result = ''
    for c, p in terms:
        c = R(c)
        if not c:
            continue
        sign = '-' if c < 0 else ('+' if result else '')
        result += sign + term_tex(abs(c), p)
    return result or '0'


def power_tex(p):
    return '1' if p == 0 else ('x' if p == 1 else 'x^{' + s.latex(p) + '}')


def split_tex(terms):
    out = ''
    for c,p in terms:
        out += ('-' if c < 0 else ('+' if out else ''))
        out += ('' if abs(c) == 1 else s.latex(abs(c)))
        out += r'\int ' + power_tex(p) + r'\,\mathrm{d}x'
    return out


def applied_tex(terms):
    out = ''
    for c,p in terms:
        out += ('-' if c < 0 else ('+' if out else ''))
        out += ('' if abs(c) == 1 else s.latex(abs(c)))
        out += r'\left(\frac{' + power_tex(p+1) + '}{' + s.latex(p+1) + r'}\right)'
    return out + '+C'


def make_data(family, a, b, p=4, target=0, degree=3, reciprocal_exponents=None):
    if a == 0 or b == 0 or family not in SOURCES or not 0 <= target < 5:
        raise ValueError('Invalid instance')
    if family == 'blank':
        if degree not in (2,3):
            raise ValueError('Unsupported blank degree')
        terms = [(R(a),0), (R(b),-2)]
        numerator = sum_tex([(R(a),degree), (R(b),degree-2)])
        integrand = r'\frac{f(x)}{x^{' + str(degree) + '}}'
        rewritten = r'\frac{' + numerator + '}{x^{' + str(degree) + '}}'
        choices = [[(R(a),1),(-R(b),-1)]]
        target = 0
        preamble = f'Given $f(x)={numerator}$ and $x\\ne 0$, calculate the integral.\n\n'
        prompt = preamble + '$\\displaystyle \\int ' + integrand + r'\,\mathrm{d}x=$' + '\n{{field-1}}\n$+C.$'
    else:
        choices = bank(family,a,b,p,reciprocal_exponents)
        terms = [(c*e, e-1) for c,e in choices[target]]
        (aa,h),(bb,l) = terms
        if family == 'quotient':
            q = int(-l)
            numerator = sum_tex([(aa,int(h+q)), (bb,0)])
            integrand = r'\frac{' + numerator + '}{x^{' + str(q) + '}}'
            domain = r'x\ne 0'
        elif l == R(1,2):
            integrand = r'\sqrt{x}\left(' + sum_tex([(aa,1),(bb,0)]) + r'\right)'
            domain = 'x>0'
        else:
            integrand = r'\frac{' + sum_tex([(aa,2),(bb,0)]) + r'}{x\sqrt{x}}'
            domain = 'x>0'
        rewritten = None
        prompt = ('$\\displaystyle \\int ' + integrand + r'\,\mathrm{d}x=$' + '\n\nAssume $' + domain + '$.'
                  if family == 'quotient' else
                  'Calculate $\\displaystyle \\int ' + integrand + r'\,\mathrm{d}x$ for $' + domain + '$.')
    rows = [r'\int ' + integrand + r'\,\mathrm{d}x &= ' + (
        r'\int ' + rewritten + r'\,\mathrm{d}x' if rewritten else
        r'\int \left(' + s.latex(expression(terms)) + r'\right)\,\mathrm{d}x')]
    if rewritten:
        rows += [r'&=\int \left(' + s.latex(expression(terms)) + r'\right)\,\mathrm{d}x']
    rows += ['&=' + split_tex(terms), '&=' + applied_tex(terms),
             '&=' + sum_tex(choices[target]) + '+C.']
    solution = 'Using the sum and constant factor rules, we get\n\n$$\n' + r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}' + '\n$$'
    if family == 'blank':
        solution += '\n\nThe blank excludes the constant $C$, which is already supplied.'
    return prompt, solution, choices, target


@checked_math_content
def generate(family, a, b, p=4, target=0, degree=3, order=None, seed=None, reciprocal_exponents=None):
    prompt, solution, choices, target = make_data(family,a,b,p,target,degree,reciprocal_exponents)
    kind = 'blank' if family == 'blank' else 'radio'
    key = 'field-1' if kind == 'blank' else 'selection'
    prompt,solution = normalize_prose(prompt), normalize_prose(solution)
    values = [normalize_tex(sum_tex(c) + ('+C' if kind == 'radio' else '')) for c in choices]
    identity = json.dumps([prompt,sorted(values)],separators=(',',':'))
    qid = uuid.uuid5(uuid.UUID(KP),identity)
    fid = uuid.uuid5(qid,key)
    answers = [{':answer/id':str(uuid.uuid5(fid,v)), ':answer/type':':answer.type/math', ':answer/value':v} for v in values]
    correct = answers[target][':answer/id']
    order = list(range(len(answers))) if order is None else list(order)
    if sorted(order) != list(range(len(answers))):
        raise ValueError('Invalid choice order')
    field = {':answer-field/id':str(fid), ':answer-field/key':key,
             ':answer-field/type':':answer-field.type/'+kind,
             ':answer-field/choices':[answers[i] for i in order],
             ':answer-field/correct':[':answer/id',correct]}
    profile = ('source-shaped-role-variable' if kind=='radio' else 'self-contained-quotient')
    if family == 'quotient':
        profile = 'quotient-component-pairing-extension'
    return {'knowledge_point':{'db_id':17592186184154,'id':KP,'title':TITLE},
            'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/moderate',
                        ':question/problem':prompt,':question/worked-solution':solution,
                        ':question/answer-fields':[field]},
            'generation':{'generator_version':VERSION,'template':family,'profile':profile,
                          'seed':seed,'parameters':{'a':a,'b':b,'p':p,'target':target,'degree':degree,
                              **({'reciprocal_exponents':list(SOURCE_RECIPROCALS if reciprocal_exponents is None else reciprocal_exponents)} if family=='quotient' else {})},
                          'source_question_ids':SOURCES[family], 'domain':'x>0' if family=='radical' else 'x!=0',
                          'dependencies':{'python':'3.13.5','sympy':s.__version__}}}


def sample(count, seed, difficulty='moderate', audit=None):
    if difficulty not in ('moderate','unclassified'):
        raise ValueError('Only moderate difficulty is supported')
    if not 0 <= count <= 1000:
        raise ValueError('Count must be between 0 and 1000')
    rng = random.Random(seed)
    records, seen = [],set()
    attempts = 0
    rejected = {}
    while len(records)<count:
        attempts += 1
        if attempts > 100*max(count,1):
            raise RuntimeError('Unique instance budget exhausted')
        family = rng.choice(list(SOURCES))
        # Decide the answer-bearing assignment and signs before magnitudes.
        target = rng.randrange(5) if family != 'blank' else 0
        pairing = rng.choice(QUOTIENT_PAIRINGS) if family == 'quotient' else None
        sa,sb = rng.choice([-1,1]),rng.choice([-1,1])
        a = sa*rng.randint(1,4 if family!='quotient' else 3)
        b = sb*rng.randint(1,4 if family=='radical' else 8)
        p,degree = rng.choice([3,4,5]),rng.choice([2,3])
        order = list(range(1 if family=='blank' else 5));rng.shuffle(order)
        record = generate(family,a,b,p,target,degree,order,seed,reciprocal_exponents=pairing)
        # Prompt identity counts mathematics, never choice order or seed.
        signature = record['question'][':question/problem']
        if signature in seen:
            role = family + ':' + str(target)
            rejected[role] = rejected.get(role,0) + 1
            continue
        seen.add(signature); records.append(record)
    if audit is not None:
        audit.update({'attempts':attempts,'accepted':len(records),
                      'duplicate_prompt_rejections':attempts-len(records),'rejected_roles':rejected})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='moderate', choices=['easy','moderate','hard','unclassified'])
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    args = parser.parse_args()
    try:
        records = sample(args.count,args.seed,args.difficulty)
    except ValueError as e:
        parser.error(str(e))
    print(json.dumps(records,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
