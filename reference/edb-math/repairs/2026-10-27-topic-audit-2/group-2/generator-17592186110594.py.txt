#!/usr/bin/env python3
"""Seeded, relocatable, offline exponential-equation generator."""
import argparse
import copy
import json
import math
import random
import sys
import uuid
from fractions import Fraction
from pathlib import Path
from math_format import checked_math_content, normalize_prose, normalize_tex

VERSION = '1.3.0'
KP = {'db_id': 17592186110594, 'id': '9a7784d8-f6a4-5e45-b03e-d76a27372c48',
      'title': 'Finding Approximate Solutions to Exponential Equations Using Logarithms'}
SOURCE = '918c847a-dee1-5e90-aa75-e08ca9d39fd8'
NS = uuid.UUID(KP['id'])

def ident(value):
    return str(uuid.uuid5(NS, value))

def decimal(value):
    value = f'{value:.3f}'
    return '0.000' if value == '-0.000' else value

def exponent(k, c, v, layout):
    term = ('-' if k < 0 else '') + (str(abs(k)) if abs(k) != 1 else '') + v
    if not c:
        return term
    if layout == 'constant-first':
        return str(c) + ('+' if k > 0 else '-') + (str(abs(k)) if abs(k) != 1 else '') + v
    return term + ('+' if c > 0 else '-') + str(abs(c))

def rational(f):
    if f.denominator == 1:
        return str(f.numerator)
    return ('-' if f < 0 else '') + rf'\frac{{{abs(f.numerator)}}}{{{f.denominator}}}'

def radical(b, p, n):
    if n == 1:
        return str(b) if p == 1 else rf'{b}^{{{p}}}'
    inner = str(b) if p == 1 else rf'{b}^{{{p}}}'
    return (r'\sqrt' if n == 2 else rf'\sqrt[{n}]') + '{' + inner + '}'

def solution(params):
    a,b,k,c,v,layout = [params[key] for key in ('a','b','k','c','variable','layout')]
    p,n = params.get('p',1),params.get('n',2)
    ex = exponent(k,c,v,layout)
    rhs = radical(b,p,n)
    power = str(b) if n == p == 1 else rf'{b}^{{{rational(Fraction(p,n))}}}'
    reduced = ('' if n == p == 1 else rational(Fraction(p,n))) + rf'\log_{{{a}}}({b})'
    logratio = rf'\frac{{{str(p) if p != 1 else ""}\log({b})}}{{{str(n) if n != 1 else ""}\log({a})}}'
    kterm = exponent(k,0,v,layout)
    isolate = logratio + (('+' + str(abs(c))) if c < 0 else ('-' + str(c)) if c > 0 else '')
    f = Fraction(p,n*k)
    numerator = (str(abs(f.numerator)) if abs(f.numerator) != 1 else '') + rf'\log({b})'
    denominator = (str(f.denominator) if f.denominator != 1 else '') + rf'\log({a})'
    final = ('-' if f < 0 else '') + rf'\frac{{{numerator}}}{{{denominator}}}'
    const = Fraction(-c,k)
    if const:
        final += ('+' if const > 0 else '-') + rational(abs(const))
    value = decimal((p/n*math.log(b)/math.log(a)-c)/k)
    text = rf'''Taking $\log_{{{a}}}$ of both sides of the equation gives:

$$
\begin{{aligned}}
{a}^{{{ex}}} &= {rhs} \\
\log_{{{a}}}\left({a}^{{{ex}}}\right) &= \log_{{{a}}}\left({rhs}\right) \\
{ex} &= \log_{{{a}}}\left({power}\right)
\end{{aligned}}
$$
'''
    if n != 1 or p != 1:
        text += rf'''
Then, we apply the power rule to the right-hand side:

$$
{ex}={reduced}
$$
'''
    rows = [rf'{ex} &= {logratio}']
    if c:
        rows.append(rf'{kterm} &= {isolate}')
    if k != 1 or c:
        rows.append(rf'{v} &= {final}')
    linear_rows = (' '+chr(92)*2+'\n').join(rows)
    text += rf'''
Next, we rewrite the right-hand side using the change of base formula and then solve for ${v}:$

$$
\begin{{aligned}}
{linear_rows}
\end{{aligned}}
$$

Evaluating the above on a calculator gives

$$
{v}\approx {value}
$$

rounded to $3$ decimal places.'''
    return normalize_prose(text)

def bank_values(params):
    a,b,k,c = [params[key] for key in ('a','b','k','c')]
    t = math.log(b)/math.log(a)
    correct = (t/2-c)/k
    inverse = (1/(2*t)-c)/k
    raw = [correct, -correct, (t-c)/k, inverse, -inverse]
    return [decimal(x) for x in raw]

def calculator_bank(params, spec):
    """Authored numerical errors; gap geometry carries no assigned key role."""
    a,b,k,c = [params[key] for key in ('a','b','k','c')]
    target = round(float(decimal((params.get('p',1)/params.get('n',2)*math.log(b)/math.log(a)-c)/k))*1000)
    rank = spec['correct_rank']
    gaps = spec['gaps_thousandths']
    if rank not in range(5) or len(gaps) != 4 or any(type(d) is not int or d < 1 for d in gaps):
        raise ValueError('Invalid calculator bank specification')
    low, high = (1,25) if spec['profile']=='N1' else (63,125)
    if spec['profile'] not in ('N1','N2') or any(not low <= d <= high for d in gaps):
        raise ValueError('Calculator gaps outside profile domain')
    sums = [0]
    for d in gaps:
        sums.append(sums[-1]+d)
    ticks = [target + offset - sums[rank] for offset in sums]
    # A bank-wide predicate: its validity is identical for every hypothetical
    # key in this same visible bank. Never scale gaps using the actual key.
    if not (all(t > 0 for t in ticks) or all(t < 0 for t in ticks)):
        raise ValueError('Calculator bank must be wholly positive or wholly negative')
    return [decimal(t/1000) for t in ticks]

@checked_math_content
def make_record(params, *, seed=None, order=None, values=None, difficulty='moderate', source_id=SOURCE, bank_spec=None):
    """One instance controls its prompt, answer, complete bank and solution."""
    a,b,k,c,v,layout = [params[key] for key in ('a','b','k','c','variable','layout')]
    p,n = params.get('p',1),params.get('n',2)
    correct_value = decimal((p/n*math.log(b)/math.log(a)-c)/k)
    values = calculator_bank(params, bank_spec) if bank_spec is not None else bank_values(params) if values is None else values
    if len(values) != 5 or len(set(float(v) for v in values)) != 5 or correct_value not in values:
        raise ValueError('Ambiguous complete bank')
    problem = normalize_prose(rf'Given that ${a}^{{{exponent(k,c,v,layout)}}}={radical(b,p,n)},$ find the value of ${v}$ rounded to $3$ decimal places.')
    signature = json.dumps([problem, sorted(values)], separators=(',',':'))
    qid = ident(signature)
    fid = ident(qid + '/selection')
    choices = [{':answer/id': ident(fid + '/' + value), ':answer/type': ':answer.type/math',
                ':answer/value': normalize_tex(value)} for value in values]
    if order is not None:
        choices = [choices[i] for i in order]
    question = {':question/id': qid, ':question/problem': problem,
                ':question/worked-solution': solution(params), ':question/requires-calculator': True,
                ':question/answer-fields': [{':answer-field/id':fid, ':answer-field/key':'selection',
                    ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices,
                    ':answer-field/correct':[':answer/id',ident(fid + '/' + correct_value)]}]}
    if difficulty is not None:
        question[':question/difficulty'] = ':question.difficulty/' + difficulty
    return {'knowledge_point':copy.deepcopy(KP), 'question':question,
            'generation':{'generator_version':VERSION,'template':('integer-single' if n == 1 else 'square-root-affine' if n == 2 else 'rational-power-affine'),
                'bank_profile':bank_spec['profile'] if bank_spec else 'M1' if values == bank_values(params) and n == 2 else 'original-literal-bank',
                'bank_spec':copy.deepcopy(bank_spec),
                'seed':seed,'parameters':copy.deepcopy(params),'source_question_ids':[source_id],
                'domain':'a,b>1; k!=0; principal positive radical',
                'dependency_versions':{'python':'3.13.5','packages':{}}}}

def common_power(a,b):
    # Equal prime supports with proportional exponent vectors admit a common base.
    def factors(v):
        out = {}; d = 2
        while d*d <= v:
            while v%d == 0:
                out[d] = out.get(d,0)+1; v //= d
            d += 1
        if v > 1: out[v] = out.get(v,0)+1
        return out
    f,g = factors(a),factors(b)
    return set(f)==set(g) and len({Fraction(f[t],g[t]) for t in f})==1

def sample_parameters(rng, difficulty='moderate'):
    # Pick decision cases before compatible numeric values.
    log_case = rng.choice(('below-one','above-one'))
    ksign = rng.choice((-1,1))
    csign = rng.choice((-1,1))
    layout = rng.choice(('constant-first','variable-first'))
    a = rng.choice([v for v in range(2,14) if v != 10])
    eligible = list(range(2,a)) if log_case == 'below-one' else list(range(a+1,48))
    if not eligible:
        return None  # base 2 has no integer radicand >1 below it
    b = rng.choice(eligible)
    if common_power(a,b):
        return None
    p,n = (1,1) if difficulty=='easy' else (1,2) if difficulty=='moderate' else rng.choice(((2,3),(1,4),(3,4)))
    return {'a':a,'b':b,'k':1 if difficulty=='easy' else ksign*rng.randint(2,4),
            'c':0 if difficulty=='easy' else csign*rng.randint(1,4),
            'variable':rng.choice(('x','y','z')),'layout':layout,'p':p,'n':n}

def generate_batch(difficulty, count, seed):
    if difficulty not in ('easy','moderate','hard'):
        raise ValueError('Unsupported difficulty: ' + difficulty)
    if count < 0:
        raise ValueError('count must be nonnegative')
    rng = random.Random(seed)
    records, seen = [], set()
    # Stratify incidental answer roles within each deterministic CLI batch.
    ranks = list(range(5)); rng.shuffle(ranks)
    positions = list(range(5)); rng.shuffle(positions)
    attempts = 0
    reasons = {'no-compatible-radicand':0,'mixed-sign-or-zero-bank':0,'near-rounding-tie':0,'zero-answer':0,'within-batch-repeat':0}
    while len(records) < count:
        attempts += 1
        if attempts > max(1000,count*100):
            raise ValueError('Requested batch exceeds bounded sampling attempts')
        profile = rng.choice(('N1','N2'))
        correct_rank = ranks[len(records)%5]
        params = sample_parameters(rng, difficulty)
        if params is None:
            reasons['no-compatible-radicand'] += 1
            continue
        a,b,k,c = [params[x] for x in ('a','b','k','c')]
        target = round(float(decimal((params.get('p',1)/params.get('n',2)*math.log(b)/math.log(a)-c)/k))*1000)
        if target == 0:
            reasons['zero-answer'] += 1
            continue
        a,b,k,c = [params[x] for x in ('a','b','k','c')]
        exact = (params.get('p',1)/params.get('n',2)*math.log(b)/math.log(a)-c)/k
        if abs(abs(exact)*1000%1 - .5) < 1e-7:
            reasons['near-rounding-tie'] += 1
            continue
        semantic = (a,b,k,c,params['p'],params['n'])
        if semantic in seen:
            reasons['within-batch-repeat'] += 1
            continue
        low, high = (1,25) if profile=='N1' else (63,125)
        bank_spec = {'profile':profile,'correct_rank':correct_rank,
                     'gaps_thousandths':[rng.randint(low,high) for _ in range(4)]}
        try:
            calculator_bank(params, bank_spec)
        except ValueError:
            reasons['mixed-sign-or-zero-bank'] += 1
            continue
        order = [i for i in range(5) if i != correct_rank]; rng.shuffle(order)
        order.insert(positions[len(records)%5],correct_rank)
        record = make_record(params, seed=seed, order=order, bank_spec=bank_spec, difficulty=difficulty,
                             source_id=SOURCE if difficulty=='moderate' else 'a79179a7-413f-5ac6-bd50-9d67d2e0bd70' if difficulty=='easy' else 'fa39cf5e-b1cf-510a-a444-4f30da1c63f4')
        record['generation']['decision_case'] = {
            'log_comparison':'below-one' if b<a else 'above-one',
            'coefficient_sign':'negative' if k<0 else 'positive',
            'shift_sign':'negative' if c<0 else 'positive','layout':params['layout']}
        records.append(record);seen.add(semantic)
    for record in records:
        record['generation']['sampling'] = {'attempts':attempts, 'accepted':count,'rejections':reasons.copy()}
    return records

def replay_sources():
    """Preserve original parameters/banks; incomplete source labels remain absent.

    Only the moderate bank is a recovered generalizable profile. Other banks
    are explicitly literal replay and are not eligible for normal generation.
    """
    sources=json.loads(Path(__file__).with_name('source_cases.json').read_text())
    params=[(2,12,-3,2,'x',1,1,'constant-first'),(3,23,1,0,'y',1,1,'variable-first'),
            (3,2,-2,4,'x',1,2,'constant-first'),(11,3,-1,4,'y',1,4,'constant-first'),
            (11,7,2,-3,'x',2,3,'variable-first')]
    records=[]
    for original, row in zip(sources,params):
        d=dict(zip(('a','b','k','c','variable','p','n','layout'),row))
        diff=original.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or None
        raw_values=[a[':answer/value'] for a in original[':question/answer-fields'][0][':answer-field/choices']]
        r=make_record(d, values=None if original[':question/math-academy-id']=='q-66811' else raw_values,
                      difficulty=diff, source_id=original[':question/id'])
        # Exact source prompt, normalized only for the served math convention.
        r['question'][':question/problem']=normalize_prose(original[':question/problem'])
        r['generation']['replay_only']=True
        r['generation']['inferred_missing_fields']=[key for key in (':question/worked-solution',':question/difficulty') if key not in original]
        if ':answer-field/correct' not in original[':question/answer-fields'][0]:
            r['generation']['inferred_missing_fields'].append(':answer-field/correct')
        records.append(r)
    return records

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',required=True,choices=('easy','moderate','hard'))
    parser.add_argument('--count',required=True,type=int)
    parser.add_argument('--seed',required=True,type=int)
    parser.add_argument('--format',required=True,choices=('json',))
    args=parser.parse_args()
    try:
        records=generate_batch(args.difficulty,args.count,args.seed)
    except ValueError as e:
        parser.error(str(e))
    json.dump(records,sys.stdout,ensure_ascii=False,indent=2);sys.stdout.write('\n')

if __name__=='__main__':
    main()
