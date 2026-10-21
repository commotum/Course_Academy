#!/usr/bin/env python3
"""Seeded product/power logarithm questions; all runtime helpers are local."""
import argparse
import json
import random
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

KP = {'db_id': 17592186054622, 'id': '4dc94edb-007d-5fe5-b9ca-9ed754adc457'}
NAMESPACE = uuid.UUID(KP['id'])
VALUES = tuple(range(-6, 0)) + tuple(range(1, 7))
BASES = (2, 3, 5, 7, 10)
SOURCES = {'numeric': '841f3191-5c7e-5e47-b725-127033cb9a73',
           'symbolic': '9796dfce-fb6b-57bd-b442-e9278daaaa20',
           'expand': '21c18a11-6bc1-5de0-bcda-f9622b617f6d',
           'condense': 'c8f2e17a-2817-5868-a9e3-61bbc105efb0'}


def linear(t, c):
    s = '' if t == 0 else ('k' if t == 1 else '-k' if t == -1 else f'{t}k')
    if c:
        s += ('+' if c > 0 and s else '') + str(c)
    return s or '0'


def power(z, p):
    return z if p == 1 else f'{z}^{{{p}}}'


def log(base, arg):
    return rf'\log_{{{base}}}\left({arg}\right)'


def weighted(p, value):
    term = log(p['base'], value)
    exponent = p['a'] if value == 'x' else p['b']
    return term if exponent == 1 else f'{exponent}{term}'


def answer_pairs(family, p):
    """Exact (coefficient of k, constant) representations, in source bank order."""
    a, b = p['a'], p['b']
    if family == 'numeric':
        u, v = p['u'], p['v']
        return [(0, a*u+v), (0, a*u), (0, b*u), (0, a*u+b*v), (0, a+b+u+v)], 3
    symbol = p['symbol']
    t, w = (a, b) if symbol == 'x' else (b, a)
    n, exponent = p['n'], max(a, b)
    return [(exponent+n, 0), (t, w*n), (t, -w*n), (t, exponent+n), (exponent*n, 0)], 1


def true_pair(family, p):
    if family == 'numeric':
        return (0,p['a']*p['u']+p['b']*p['v'])
    t,w=(p['a'],p['b']) if p['symbol']=='x' else (p['b'],p['a'])
    return (t,w*p['n'])


def bank(family, p):
    if family in ('numeric','symbolic') and 'role_bank' in p:
        roles,key=p['role_bank'],p['role_key']
        if len(roles)!=5 or not 0<=key<5:
            raise ValueError('Five candidate roles and a selected role are required')
        pairs=[true_pair(family,candidate) for candidate in roles]
        if len(set(pairs))!=5 or true_pair(family,p)!=pairs[key]:
            raise ValueError('Equivalent bank choices or inconsistent selected role')
        return [linear(*pair) for pair in pairs],key
    if family in ('numeric', 'symbolic'):
        pairs, key = answer_pairs(family, p)
        if len(set(pairs)) != 5:
            raise ValueError('Equivalent bank choices')
        return [linear(*pair) for pair in pairs], key
    if family == 'expand':
        c, z, exponent = p['c'], p['z'], p['p']
        L = lambda arg: rf'\log ({arg})'
        return [L(f'{c} + {z}^{{{exponent}}}'), L(c)+f' + {z}'+L(exponent),
                L(f'{c} + {exponent}{z}'), L(c)+f' + {exponent}'+L(z),
                f'{exponent}'+L(c)+L(z)], 3
    if family == 'condense':
        a, b, base = p['a'], p['b'], p['base']
        L = lambda arg: rf'\log_{{{base}}} ({arg})'
        return [L(f'x^{{{a}}} + y^{{{b}}}'), L(f'{a}x + {b}y'),
                L(f'x^{{{a}}}y^{{{b}}}'), f'{a+b}'+L('xy'), L(f'{a*b}xy')], 2
    raise ValueError('Unknown family')


@checked_math_content
def build(family, p, order=None):
    """Build at explicit parameters for source replay and counterfactual probes."""
    values, correct_index = bank(family, p)
    if family in ('numeric', 'symbolic'):
        a, b, base = p['a'], p['b'], p['base']
        if family == 'numeric':
            givens = [('x', str(p['u'])), ('y', str(p['v']))]
        else:
            givens = [('x', 'k' if p['symbol'] == 'x' else str(p['n'])),
                      ('y', 'k' if p['symbol'] == 'y' else str(p['n']))]
        if p.get('reverse', False):
            givens.reverse()
        given_text = [f'${log(base, z)}={v}$' for z, v in givens]
        target = log(base, power('x', a)+power('y', b))
        problem = f'If {given_text[0]} and {given_text[1]}, then ${target}=$'
        expanded = weighted(p, 'x')+'+'+weighted(p, 'y')
        if family == 'numeric':
            dot = lambda e, n: rf'{e}\cdot '+(f'({n})' if n < 0 else str(n))
            substituted = dot(a, p['u'])+'+'+dot(b, p['v'])
        else:
            t, w = (a, b) if p['symbol'] == 'x' else (b, a)
            symbolic = linear(t, 0)
            numerical = (rf'{w}\cdot ' if w != 1 else '') + (f'({p["n"]})' if p['n'] < 0 else str(p['n']))
            substituted = symbolic+'+'+numerical if p['symbol'] == 'x' else numerical+'+'+symbolic
        laws = ('The laws of logarithms are:\n\n'
                r'- $\log_n(a)+\log_n(b)=\log_n(ab)$ - the product rule'+'\n\n'+
                r'- $\log_n(a)-\log_n(b)=\log_n(\frac{a}{b})$ - the quotient rule'+'\n\n'+
                r'- $\log_n(c^m)=m\log_n(c)$ - the power rule')
        solution = (laws+'\n\nNote that $'+target+'$ can be rewritten using the product and power rules as follows:\n\n$$\n'+
                    r'\begin{aligned}'+target+' &='+log(base,power('x',a))+'+'+log(base,power('y',b))+
                    r' \\ &='+expanded+r'\end{aligned}'+'\n$$\n\nNow, since '+given_text[0]+' and '+given_text[1]+', we conclude that\n\n$$\n'+
                    expanded+'='+substituted+'='+values[correct_index]+'.\n$$\n\nTherefore,\n\n$$\n'+target+'='+values[correct_index]+'.\n$$')
    elif family == 'expand':
        c, z, exponent = p['c'], p['z'], p['p']
        target = rf'\log ({c}{z}^{{{exponent}}})'
        problem = f'What is ${target}$?'
        solution = ('Using the product rule, then the power rule, we obtain\n\n$$\n'+
                    target+rf'=\log ({c})+\log ({z}^{{{exponent}}})='+values[correct_index]+'.\n$$')
    else:
        a, b, base = p['a'], p['b'], p['base']
        expr = rf'{a}\log_{{{base}}} (x) + {b}\log_{{{base}}} (y)'
        problem = f'Express ${expr}$ as a single logarithm.'
        solution = ('Using the power rule for logarithms, we can rewrite both terms:\n\n$$\n'+expr+'='+
                    log(base,power('x',a))+'+'+log(base,power('y',b))+'.\n$$\n\nNow, using the product rule, we combine the two terms:\n\n$$\n'+expr+'='+values[correct_index]+'.\n$$')
    problem, solution = normalize_prose(problem), normalize_prose(solution)
    values = [normalize_tex(v) for v in values]
    # Identity includes the full bank, not the seed, display order, or metadata.
    identity = json.dumps([problem, sorted(values), values[correct_index]], sort_keys=True)
    qid = str(uuid.uuid5(NAMESPACE, identity))
    fid = str(uuid.uuid5(uuid.UUID(qid), 'selection'))
    answers = [{':answer/id': str(uuid.uuid5(uuid.UUID(fid), value)),
                ':answer/type': ':answer.type/math', ':answer/value': value} for value in values]
    choice_order = list(range(5)) if order is None else order
    if sorted(choice_order) != list(range(5)):
        raise ValueError('Invalid choice permutation')
    field = {':answer-field/id': fid, ':answer-field/key': 'selection',
             ':answer-field/type': ':answer-field.type/radio',
             ':answer-field/choices': [answers[i] for i in choice_order],
             ':answer-field/correct': [':answer/id', answers[correct_index][':answer/id']]}
    question = {':question/id': qid, ':question/problem': problem,
                ':question/worked-solution': solution, ':question/answer-fields': [field]}
    if family in ('numeric', 'symbolic'):
        question[':question/difficulty'] = ':question.difficulty/hard'
    return {'knowledge_point': KP, 'question': question, 'assets': {},
            'generation': {'version': '2.0.0', 'template': family, 'bank_profile': 'same-skill-role-bank' if 'role_bank' in p else family+'-source-bank',
                           'parameters': dict(p), 'source_question_id': SOURCES[family],
                           'domain': 'x>0,y>0; common base>1', 'replay_only': family in ('expand','condense')}}


def draw_role_bank(rng, family):
    """Assemble five distinct possible answers before choosing which to assess."""
    roles,seen=[],set()
    base=rng.choice(BASES)
    reverse=bool(rng.getrandbits(1))
    sign_u,sign_v=rng.choice((-1,1)),rng.choice((-1,1))
    symbol,powered=rng.choice(('x','y')),rng.choice(('x','y'))
    numeric_sign=rng.choice((-1,1))
    for _ in range(1000):
        if family == 'numeric':
            a,b = rng.sample(range(2,6), 2)
            p = dict(a=a, b=b, u=sign_u*rng.randint(1,6), v=sign_v*rng.randint(1,6))
        elif family == 'symbolic':
            exponent = rng.randint(2,5)
            p = dict(a=exponent if powered=='x' else 1, b=exponent if powered=='y' else 1,
                     symbol=symbol, n=numeric_sign*rng.randint(1,6))
        else:raise ValueError('Unsupported sampled family')
        pair=true_pair(family,p)
        if pair in seen:continue
        p.update(base=base,reverse=reverse)
        roles.append(p);seen.add(pair)
        if len(roles)==5:return roles
    raise ValueError('Could not draw a distinct role bank')


def build_role_bank(family, roles, key, order=None):
    p=dict(roles[key]);p.update(role_bank=roles,role_key=key)
    return build(family,p,order)


@checked_math_content
def generate(rng, difficulty='hard', *, stats=None):
    if difficulty!='hard':raise ValueError('Unsupported difficulty: '+difficulty)
    family=rng.choice(('numeric','symbolic'))
    roles=draw_role_bank(rng,family)
    # Key selection is independent of all visible bank properties, including
    # coefficient/constant ordering within symbolic subgroups.
    key=rng.randrange(5)
    if stats is not None:stats['attempts']=stats.get('attempts',0)+1
    return build_role_bank(family,roles,key,rng.sample(range(5),5))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='hard', choices=('easy','moderate','hard'))
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=('json',), default='json')
    args=parser.parse_args()
    if not 0<=args.count<=1000:
        parser.error('count must be in 0..1000')
    if args.difficulty != 'hard':
        parser.error('only hard is supported')
    rng=random.Random(args.seed)
    records=[generate(rng,args.difficulty) for _ in range(args.count)]
    for i,r in enumerate(records):
        r['generation'].update(seed=args.seed,index=i,python='3.13.5')
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
