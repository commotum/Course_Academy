#!/usr/bin/env python3
"""Seeded, relocatable quotient-rule questions. No network, assets, or DB writes."""
import argparse
import copy
from fractions import Fraction
import json
from pathlib import Path
import random
import re
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.2.0'
SYMBOLIC_PROFILES = ('natural-varied', 'explicit-base-varied')
ARGUMENT_POOL = tuple(range(3, 21))
RESULT_POOL = tuple(sorted({c*d for c in range(2, 10) for d in (2, 3, 4)}))
KP = {'db_id': 17592186110591, 'id': '1da4785a-0124-517b-9dba-ba012853b83a',
      'title': 'Combining Logarithms With Coefficients Using the Quotient Rule'}
NAMESPACE = uuid.UUID(KP['id'])
SOURCES = {'natural-varied': '692975c7-d71f-5bff-afaa-3fff34d21e62',
           'explicit-base-varied': 'fb60160d-829d-5fa4-af5a-fa923f366d6b',
           'evaluation-varied': 'f70da637-39bf-585b-b7da-8cee169442e1',
           'natural': '692975c7-d71f-5bff-afaa-3fff34d21e62',
           'quotient-evaluation': 'f70da637-39bf-585b-b7da-8cee169442e1',
           'power-arguments': 'c4b3fb73-1f52-59aa-aefb-60ecb06c495d',
           'historical-base': 'fb60160d-829d-5fa4-af5a-fa923f366d6b'}


def identity(value):
    return str(uuid.uuid5(NAMESPACE, json.dumps(value, sort_keys=True, ensure_ascii=False)))


def tex_number(value):
    q = Fraction(value)
    return str(q.numerator) if q.denominator == 1 else rf'\frac{{{q.numerator}}}{{{q.denominator}}}'


def logarithm(base, arg, coefficient=1):
    op = r'\ln' if base == 'e' else rf'\log_{{{base}}}'
    return (str(coefficient) if coefficient != 1 else '') + op + rf'({arg})'


def factors(value):
    """Exact signature for a rational number's formal prime logarithm."""
    q = Fraction(value)
    if q <= 0:
        raise ValueError('logarithm argument must be positive')
    out = {}
    for v, sign in ((q.numerator, 1), (q.denominator, -1)):
        p = 2
        while p * p <= v:
            while v % p == 0:
                out[p] = out.get(p, 0) + sign
                v //= p
            p += 1
        if v > 1:
            out[v] = out.get(v, 0) + sign
    return out


def log_signature(coef, value):
    return tuple(sorted((p, coef * e) for p, e in factors(value).items() if e))


def bank(instance):
    c, a, b = (instance[k] for k in ('c', 'a', 'b'))
    profile, base = instance['profile'], instance['base']
    q = Fraction(a, b)
    if profile in ('natural', 'historical-base') + SYMBOLIC_PROFILES:
        if profile in SYMBOLIC_PROFILES:
            specs = [('correct', c, q)] + [('argument-foil', c, Fraction(x)) for x in instance['foil_arguments']] + [('coefficient-omission-foil', 1, Fraction(x)) for x in instance['bare_arguments']]
        elif profile == 'natural':
            specs = [('correct', c, q), ('coefficient-inside', 1, c*q),
                     ('subtract-arguments', c, a-b), ('drop-and-subtract', 1, a-b),
                     ('second-term', c, b)]
        else:
            # Replay only. Never infer a sampling law from the isolated 2/3 option.
            if (c, base, a, b) != (4, 4, 12, 2):
                raise ValueError('Historical base bank supports source replay only')
            specs = [('correct', c, q), ('subtract-arguments', c, a-b),
                     ('unresolved-source-literal', 1, Fraction(2, 3)),
                     ('coefficient-inside', 1, c*q), ('reverse-quotient', c, 1/q)]
        values = [{'recipe': role, 'coefficient': coef, 'argument': str(arg),
                   'value': logarithm(base, tex_number(arg), coef),
                   'signature': log_signature(coef, arg)} for role, coef, arg in specs]
    else:
        d = instance['d']
        if q != base ** d:
            raise ValueError('Quotient is not the declared base power')
        if profile == 'evaluation-varied':
            specs = [('correct', c*d)] + [('numeric-foil', x) for x in instance['numeric_foils']]
        elif profile == 'quotient-evaluation':
            specs = [('correct', c*d), ('double-product', 2*c*d),
                     ('sum', c+d), ('square-coefficient', c*c), ('sum-plus-two', c+d+2)]
        elif profile == 'power-arguments':
            specs = [('correct', c*d), ('one', 1), ('one-exponent-less', c*(d-1)),
                     ('coefficient', c), ('two-exponents-less', c*(d-2))]
        else:
            raise ValueError('unknown profile')
        values = [{'recipe': role, 'number': value, 'value': str(value),
                   'signature': value} for role, value in specs]
    if len({str(v['signature']) for v in values}) != 5:
        raise ValueError('equivalent choices')
    return values


def clean_source(text):
    text = text.replace('{log}', r'\log').replace(r'\operatorname{ln}', r'\ln').replace('\u2061', '')
    return normalize_prose(text)


def solution(i):
    c, a, b, base = (i[k] for k in ('c', 'a', 'b', 'base'))
    q = Fraction(a, b)
    log = lambda x, k=1: logarithm(base, x, k)
    expr = log(a, c) + '-' + log(b, c)
    rule = (r'\ln(a)-\ln(b)=\ln\left(\frac{a}{b}\right)' if base == 'e' else
            r'\log_n(a)-\log_n(b)=\log_n\left(\frac{a}{b}\right)')
    name = 'natural logarithms' if base == 'e' else 'logarithms'
    text = (f"First, let's recall the quotient rule for {name}:\n\n$$\n{rule}\n$$\n\n"
            'If we factor the given expression and use the quotient rule for logarithms, we get:\n\n$$\n' +
            r'\begin{aligned}' + expr + '&=' + str(c) + r'\bigl(' + log(a) + '-' + log(b) + r'\bigr)' +
            r' \\ &=' + log(rf'\frac{{{a}}}{{{b}}}', c) + r' \\ &=' + log(tex_number(q), c) +
            '\\end{aligned}\n$$\n\n')
    if i['difficulty'] == 'moderate':
        d = i['d']
        text += (rf'Now, since ${base}^{{{d}}}={tex_number(q)}$, then ${log(tex_number(q))}={d}$. Therefore:' +
                 '\n\n$$\n' + log(tex_number(q), c) + rf'={c}\cdot {d}={c*d}.' + '\n$$')
    else:
        text += 'Therefore:\n\n$$\n' + expr + '=' + log(tex_number(q), c) + '\n$$'
    return normalize_prose(text)


@checked_math_content
def generate(instance, seed=0, source=None):
    i = copy.deepcopy(instance)
    values = bank(i)
    expr = logarithm(i['base'], i['a'], i['c']) + ' - ' + logarithm(i['base'], i['b'], i['c'])
    prompt = f'Express ${expr}$ as a single logarithm.' if i['difficulty'] == 'easy' else f'${expr}=$'
    worked = solution(i)
    if source:
        prompt = clean_source(source[':question/problem'])
        if source.get(':question/worked-solution'):
            worked = clean_source(source[':question/worked-solution'])
    prompt, worked = normalize_prose(prompt), normalize_prose(worked)
    # Identities depend on normalized mathematical content, not option order or RNG seed.
    qid = identity([prompt, sorted(v['value'] for v in values)])
    fid = identity([qid, 'selection'])
    choices = [{':answer/id': identity([fid, normalize_tex(v['value'])]),
                ':answer/type': ':answer.type/math', ':answer/value': normalize_tex(v['value'])} for v in values]
    correct = choices[0][':answer/id']
    random.Random(seed).shuffle(choices)
    original_band = source.get(':question/difficulty', {}).get(':db/ident') if source else None
    return {'knowledge_point': KP.copy(), 'question': {
        ':question/id': qid, ':question/problem': prompt, ':question/worked-solution': worked,
        ':question/difficulty': ':question.difficulty/' + i['difficulty'], ':question/answer-fields': [{
            ':answer-field/id': fid, ':answer-field/key': 'selection',
            ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
            ':answer-field/correct': [':answer/id', correct]}]},
        'generation': {'generator_version': VERSION, 'template': i['profile'], 'seed': seed,
            'parameters': i, 'source_question_ids': [source[':question/id'] if source else SOURCES[i['profile']]],
            'source_difficulty': original_band if source else ('unlabeled' if i['profile'] == 'power-arguments' else i['difficulty']),
            'replay_only': bool(source), 'bank_origin': 'authored complete profile' if i['profile'].endswith('-varied') else 'observed source bank', 'bank_recipes': [{k: v for k, v in x.items() if k != 'signature'} for x in values],
            'domains': 'positive integer arguments; equal c>=2; common base e or integer n>1',
            'semantic_instance': [i['profile'], i['c'], i['base'], i['a'], i['b']]}}


def sample(rng, difficulty):
    """Assign the quotient / exponent role before incidental prompt data."""
    if difficulty not in ('easy', 'moderate'):
        raise ValueError('unsupported difficulty: ' + difficulty)
    # The complete candidate set is independent of which member is the key.
    base = rng.choice(('e', rng.randint(2, 7))) if difficulty == 'easy' else None
    candidates = sorted(rng.sample(ARGUMENT_POOL, 3)) if difficulty == 'easy' else None
    rank = rng.randrange(3) if difficulty == 'easy' else None
    d = rng.choice((2, 3, 4)) if difficulty == 'moderate' else None
    rejected = 0
    for attempt in range(10000):
        c = rng.randint(2, 9)
        if difficulty == 'easy':
            q, b = candidates[rank], rng.randint(2, 20)
            profile = 'natural-varied' if base == 'e' else 'explicit-base-varied'
            i = dict(difficulty=difficulty, profile=profile, c=c, base=base, a=b*q, b=b,
                key_rank=rank, foil_arguments=[x for x in candidates if x != q],
                bare_arguments=rng.sample(range(2,501), 2),
                decision_case='argument-rank-' + str(rank))
        else:
            base, b = rng.randint(2, 7), rng.randint(2, 15)
            a = b * base ** d
            if a > 4000:
                rejected += 1
                continue
            result = c*d
            alternatives = [c*k for k in (2, 3, 4)]
            extras = rng.sample([x for x in RESULT_POOL if x not in alternatives], 2)
            foils = [x for x in alternatives if x != result] + extras
            i = dict(difficulty=difficulty, profile='evaluation-varied', c=c, base=base, a=a, b=b, d=d,
                key_rank=sum(x < result for x in foils), numeric_foils=foils,
                decision_case='exponent-' + str(d))
        try:
            bank(i)
        except ValueError:
            rejected += 1
            continue
        return i, rejected
    raise RuntimeError('failed to sample the selected decision case')


def batch(difficulty, count, seed):
    if difficulty == 'unclassified':
        difficulty = 'easy'
    if difficulty not in ('easy', 'moderate'):
        raise ValueError('hard is outside source-supported scope')
    rng, records = random.Random(seed), []
    for _ in range(count):
        i, rejected = sample(rng, difficulty)
        r = generate(i, rng.getrandbits(64))
        r['generation']['batch_seed'] = seed
        r['generation']['rejected_parameter_draws'] = rejected
        records.append(r)
    return records


REPLAY_INSTANCES = [
    dict(profile='power-arguments', difficulty='moderate', c=5, base=2, a=128, b=8, d=4),
    dict(profile='historical-base', difficulty='easy', c=4, base=4, a=12, b=2),
    dict(profile='quotient-evaluation', difficulty='moderate', c=6, base=5, a=100, b=4, d=2),
    dict(profile='natural', difficulty='easy', c=6, base='e', a=68, b=17)]


def replay():
    originals = json.loads(Path(__file__).with_name('source-replay.json').read_text())
    return [generate(i, 0, s) for i, s in zip(REPLAY_INSTANCES, originals)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty', default='easy', choices=['easy', 'moderate', 'hard', 'unclassified'])
    parser.add_argument('--count', type=int, default=5)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--format', choices=['json'], default='json')
    parser.add_argument('--replay-source', action='store_true')
    args = parser.parse_args()
    if args.count < 0:
        parser.error('--count must be nonnegative')
    try:
        records = replay() if args.replay_source else batch(args.difficulty, args.count, args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
