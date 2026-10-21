#!/usr/bin/env python3
"""Seeded, relocatable quotient-rule practice. No filesystem writes or assets."""
import argparse
from fractions import Fraction
import json
import math
import random
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.2.0'
KP = {'db_id': 17592186110590, 'id': '7c0acf69-d973-56b7-bdb3-a5804709c6da',
      'title': 'Combining Logarithms Using the Quotient Rule'}
SOURCES = {'easy': '15c5c76c-d78d-5592-bdec-a5d9824a4594',
           'moderate': '1ffe9f61-1ba3-54d9-b9af-4cad3fb8f150'}
RULE = r'\log_n(a)-\log_n(b)=\log_n\left(\frac{a}{b}\right)'
NAMESPACE = uuid.UUID('e4b807f1-0d12-42b5-83b2-e0bcc3e73a77')


def frac(n):
    n = Fraction(n)
    return str(n.numerator) if n.denominator == 1 else rf'\frac{{{n.numerator}}}{{{n.denominator}}}'


def log(base, arg):
    return rf'\log_{{{base}}}\left({arg}\right)'


def power(n):
    return '1' if n == 0 else ('x' if n == 1 else rf'x^{{{n}}}')


def error_exponents(p,q):
    return [e for e in range(p+q+3) if e not in (p-q,p,q,p+q)]


def numeric_values(a, b, profile):
    q = Fraction(a, b)
    if profile == 'numeric-distinct':
        return [q, 1/q, Fraction(a+b), Fraction(abs(a-b)), Fraction(a*b)]
    if profile == 'numeric-equal':
        return [q, Fraction(a+b), Fraction(a*b), Fraction(a), Fraction(1,a)]
    raise ValueError('Unknown numeric production profile')


@checked_math_content
def build(difficulty, params, rng=None, profile=None, source_id=None, source_difficulty='auto', verb='Express'):
    """One shared instance determines problem, options, key and solution."""
    base = params['base']
    if difficulty == 'easy':
        a, b = params['a'], params['b']
        assert 2 <= base <= 9 and a > 0 and b > 0
        left, right = str(a), str(b)
        result = frac(Fraction(a,b))
        quotient = rf'\frac{{{a}}}{{{b}}}'
        profile = profile or ('numeric-equal' if a == b else 'numeric-distinct')
        if profile == 'source-easy':
            options = [log(base,result), log(base,str(a-b)), log(10,str(a*b)), log(10,str(a-b)), log(base,str(a*b))]
            # Common logarithms have no explicit base in the captured bank.
            options[2] = rf'\log\left({a*b}\right)'
            options[3] = rf'\log\left({a-b}\right)'
        elif profile == 'source-incomplete':
            # Source 21/3=7 at base 7; retain its evaluated numerical answer.
            assert (base,a,b) == (7,21,3)
            options = ['1', log(base,str(a-b)), str(a*b), '-1', str(a//b)]
        else:
            values = numeric_values(a,b,profile)
            if any(v <= 0 for v in values) or len(set(values)) != 5:
                raise ValueError('Degenerate numeric bank')
            options = [log(base,frac(v)) for v in values]
        comparison = 'equal' if a == b else ('ascending' if a < b else 'descending')
    elif difficulty == 'moderate':
        p,q = params['p'],params['q']
        assert 2 <= base <= 9 and 1 <= q < p <= 8
        left,right = power(p),power(q)
        result = power(p-q)
        quotient = rf'\frac{{{left}}}{{{right}}}'
        profile = profile or 'monomial-authored'
        if profile == 'monomial-source':
            # Source replay retains every original alternative.
            options = [log(base,result),log(base,left+'+'+right),log(base,right),log(base,left+'-'+right),log(base,left)]
        elif profile == 'monomial-authored':
            error = params.get('error_exponent',0)
            assert error in error_exponents(p,q)
            # A valid quotient may equal the denominator. Replace only its
            # duplicate option; never reject the mathematical decision case.
            denominator_option = q
            if p == 2*q:
                alternate = params.get('alternate_error_exponent',next(e for e in error_exponents(p,q) if e != error))
                assert alternate in error_exponents(p,q) and alternate != error
                denominator_option = alternate
            options = [log(base,result),log(base,power(p)),log(base,power(denominator_option)),
                       log(base,power(p+q)),log(base,power(error))]
        else:
            raise ValueError('Unknown monomial profile')
        comparison = 'gap-equals-q' if p-q == q else ('gap-below-q' if p-q < q else 'gap-above-q')
    else:
        raise ValueError('Unsupported difficulty: '+difficulty)
    expr = log(base,left)+' - '+log(base,right)
    problem = f'{verb} ${expr}$ as a single logarithm.'
    if difficulty == 'moderate':
        problem += ' Assume $x>0$.'
    line = expr + ' &= ' + log(base,quotient)
    if quotient != result:
        line += r' \\ &= ' + log(base,result)
    solution = "First, let's recall the quotient rule for logarithms:\n\n$$\n"+RULE+'\n$$\n\n'
    solution += 'Using the quotient rule for logarithms, the given expression can be rewritten as:\n\n$$\n'
    solution += r'\begin{aligned}'+line+r'\end{aligned}'+'\n$$'
    if profile == 'source-incomplete':
        solution += '\n\nHere $'+log(base,result)+'=1$; the source bank uses the evaluated value.'
    # Normalize all presentation before deriving field-owned stable identities.
    problem,solution = normalize_prose(problem),normalize_prose(solution)
    options = [normalize_tex(s) for s in options]
    assert len(set(options)) == 5
    key = options[0]
    digest = json.dumps([problem,solution,profile,sorted(options)],sort_keys=True)
    qid = uuid.uuid5(NAMESPACE,digest)
    fid = uuid.uuid5(qid,'field:selection')
    choices = [{':answer/id':str(uuid.uuid5(fid,s)),':answer/type':':answer.type/math',':answer/value':s} for s in options]
    correct_id = choices[0][':answer/id']
    if rng is not None:
        rng.shuffle(choices)
    field = {':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
             ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}
    question = {':question/id':str(qid),':question/problem':problem,':question/worked-solution':solution,
                ':question/answer-fields':[field]}
    if source_difficulty == 'auto':
        question[':question/difficulty'] = ':question.difficulty/'+difficulty
    elif source_difficulty is not None:
        question[':question/difficulty'] = source_difficulty
    return {'knowledge_point':dict(KP),'question':question,'generation':{
        'generator_version':VERSION,'template':'numeric-quotient' if difficulty=='easy' else 'monomial-quotient',
        'profile':profile,'parameters':dict(params),'decision_case':comparison,
        'source_question_ids':[source_id or SOURCES[difficulty]],
        'source_difficulty':difficulty if source_difficulty=='auto' else source_difficulty,
        'domain':'positive arguments; base > 1'+('; x>0' if difficulty=='moderate' else ''),
        'authored_extension': profile in ('numeric-distinct','numeric-equal','monomial-authored'),
        'correct_math':key}}


def candidates(case):
    out=[]
    for a in range(2,31):
        for b in range(2,31):
            ratio=Fraction(a,b)
            if case == 'equal' and a == b:
                pass
            elif case == 'coprime-ascending' and a < b and math.gcd(a,b)==1:
                pass
            elif case == 'coprime-descending' and a > b and math.gcd(a,b)==1:
                pass
            elif case == 'reducible-ascending' and a < b and math.gcd(a,b)>1:
                pass
            elif case == 'reducible-descending' and a > b and math.gcd(a,b)>1 and ratio.denominator>1:
                pass
            elif case == 'integer' and a>b and ratio.denominator==1:
                pass
            else:
                continue
            profile='numeric-equal' if a==b else 'numeric-distinct'
            values=numeric_values(a,b,profile)
            if len(set(values))==5 and min(values)>0:
                out.append((a,b))
    return out


NUMERIC_CASES = ('coprime-ascending','coprime-descending','reducible-ascending','reducible-descending','integer','equal')
NUMERIC_POOLS = {case:candidates(case) for case in NUMERIC_CASES}
MONOMIAL_POOLS = {
    'gap-below-q': [(p,q) for p in range(2,9) for q in range(1,p) if p-q < q],
    'gap-equals-q': [(p,q) for p in range(2,9) for q in range(1,p) if p-q == q],
    'gap-above-q': [(p,q) for p in range(2,9) for q in range(1,p) if p-q > q],
}


def generate(difficulty='easy',count=5,seed=0):
    if difficulty == 'unclassified':
        difficulty='easy'
    if difficulty not in ('easy','moderate'):
        raise ValueError('Only easy and moderate are supported; hard has no source evidence')
    if count < 0:
        raise ValueError('count must be nonnegative')
    capacity = sum(map(len,NUMERIC_POOLS.values()))*8 if difficulty=='easy' else sum(map(len,MONOMIAL_POOLS.values()))*8
    if count > capacity:
        raise ValueError(f'count exceeds finite semantic capacity {capacity}')
    rng=random.Random(seed)
    records=[]; seen=set(); attempts=0
    while len(records)<count:
        attempts += 1
        if attempts>max(10000,count*500):
            raise RuntimeError('Unique sampling exhausted; request a smaller count')
        if difficulty=='easy':
            case=rng.choice(NUMERIC_CASES)
            a,b=rng.choice(NUMERIC_POOLS[case])
            params={'base':rng.randint(2,9),'a':a,'b':b}
        else:
            case=rng.choice(tuple(MONOMIAL_POOLS))
            p,q=rng.choice(MONOMIAL_POOLS[case])
            params={'base':rng.randint(2,9),'p':p,'q':q,'error_exponent':rng.choice(error_exponents(p,q))}
            if p == 2*q:
                params['alternate_error_exponent']=rng.choice([e for e in error_exponents(p,q) if e!=params['error_exponent']])
        identity=tuple(sorted((k,v) for k,v in params.items() if k not in ('error_exponent','alternate_error_exponent')))
        if identity in seen:
            continue
        seen.add(identity)
        record=build(difficulty,params,rng)
        record['generation'].update(seed=seed,index=len(records),sampling_case=case,attempt_number=attempts,
                                    rejection_policy='prevalidated finite domains; repeated semantic instances resampled')
        records.append(record)
    return records


def replay_sources():
    specs=[('easy',{'base':7,'a':21,'b':3},'source-incomplete','994f05dc-d691-5526-bc6d-c292f700403b',None),
           ('moderate',{'base':2,'p':3,'q':1},'monomial-source',SOURCES['moderate'],':question.difficulty/moderate'),
           ('easy',{'base':2,'a':7,'b':5},'source-easy',SOURCES['easy'],':question.difficulty/easy')]
    return [build(d,p,profile=profile,source_id=sid,source_difficulty=band) for d,p,profile,sid,band in specs]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('unclassified','easy','moderate','hard'),default='easy')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json')
    args=parser.parse_args()
    try:
        result=generate(args.difficulty,args.count,args.seed)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
