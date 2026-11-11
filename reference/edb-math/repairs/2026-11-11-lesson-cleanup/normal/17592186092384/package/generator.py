#!/usr/bin/env python3
"""Seeded exact normal-slope practice; no repository or database runtime access."""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
import math_format as fmt

HERE = Path(__file__).resolve().parent
SOURCE = json.loads((HERE / 'source-cases.json').read_text())
KP = {'db_id': 17592186092384, 'id': SOURCE['kp'][':knowledge-point/id'],
      'title': SOURCE['kp'][':knowledge-point/title']}
VERSION = '3.0.0'
LEVELS = ('easy', 'moderate', 'hard')

def tex(v):
    v = F(v)
    sign = '-' if v < 0 else ''
    return sign + (str(abs(v.numerator)) if v.denominator == 1 else
                   r'\frac{' + str(abs(v.numerator)) + '}{' + str(v.denominator) + '}')

def poly(terms, variable='x'):
    """Keep the learner's power-rule representation, including negative powers."""
    out = ''
    for c, e in terms:
        c, e = F(c), F(e)
        if not c:
            continue
        sign = '-' if c < 0 else '+' if out else ''
        monomial = '' if not e else variable if e == 1 else variable + '^{' + tex(e) + '}'
        coefficient = '' if monomial and abs(c) == 1 else tex(abs(c))
        out += sign + coefficient + monomial
    return out or '0'

def power(v, e):
    v, e = F(v), F(e)
    if e.denominator == 1:
        return v ** e.numerator
    if e.denominator != 2 or v <= 0:
        raise ValueError('Outside rational square-root evaluation domain')
    from math import isqrt
    a, b = isqrt(v.numerator), isqrt(v.denominator)
    if a*a != v.numerator or b*b != v.denominator:
        raise ValueError('Evaluation must have an exact rational square root')
    return F(a, b) ** e.numerator

def value(terms, t):
    return sum((F(c) * power(t, e) for c, e in terms), F(0))

def instance(level, p):
    """Construct ordered algebra before presentation; no CAS normalization."""
    t = F(p['t'])
    if level == 'easy':
        terms = [(p['a'], 2), (p['b'], 1), (p['c'], 0)]
        printed = poly(terms)
        expansion = []
    elif level == 'moderate':
        b, c = p['b'], p['c']
        terms = [(1, 3), (b+c, 2), (b*c, 1)]
        printed = '(' + poly([(1,1),(b,0)]) + ')(' + poly([(1,2),(c,1)]) + ')'
        expansion = [poly([(1,3),(c,2),(b,2),(b*c,1)]), poly(terms)]
    elif level == 'hard':
        b, sign = p['b'], p['sign']
        terms = [(sign,F(3,2)), (2*sign*b,F(1,2)), (sign*b*b,F(-1,2))]
        printed = ('-' if sign < 0 else '') + r'\frac{(' + poly([(1,1),(b,0)]) + r')^2}{\sqrt{x}}'
        numerator = poly([(sign,2),(2*sign*b,1),(sign*b*b,0)])
        expansion = [r'\frac{' + numerator + r'}{x^{1/2}}', poly(terms)]
    else:
        raise ValueError('Unknown difficulty')
    derivative = [(F(c)*F(e), F(e)-1) for c,e in terms if e and c]
    y, m = value(terms,t), value(derivative,t)
    if not m:
        raise ValueError('Normal is vertical; outside scalar-slope response contract')
    return {'terms':terms, 'derivative':derivative, 'printed':printed, 'expansion':expansion,
            't':t, 'y':y, 'm':m, 'answer':-1/m}

def display(body):
    return '$$\n' + body + '\n$$'

def aligned(rows):
    return display(r'\begin{aligned}' + '\n' + ('\\\\\n').join(rows) + '\n' + r'\end{aligned}')

def identify(question):
    """Normalize before hashing; every field owns fresh choice identities."""
    question = copy.deepcopy(question)
    for k in (':question/problem', ':question/worked-solution'):
        question[k] = fmt.normalize_prose(question[k])
    for field in question[':question/answer-fields']:
        for choice in field[':answer-field/choices']:
            choice[':answer/value'] = fmt.normalize_tex(choice[':answer/value'])
    fmt.validate_generated_record({'question':question})
    content = json.dumps(question, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha256(content.encode()).hexdigest()
    qid = str(uuid.uuid5(uuid.UUID(KP['id']), VERSION + digest))
    question[':question/id'] = qid
    for field in question[':question/answer-fields']:
        old = field[':answer-field/correct'][1]
        fid = str(uuid.uuid5(uuid.UUID(qid),field[':answer-field/key']))
        field[':answer-field/id'] = fid
        for choice in field[':answer-field/choices']:
            prior = choice[':answer/id']
            choice[':answer/id'] = str(uuid.uuid5(uuid.UUID(fid),choice[':answer/value']))
            if prior == old:
                field[':answer-field/correct'] = [':answer/id',choice[':answer/id']]
    return question, digest

def generate(level, p, seed=0):
    z = instance(level,p)
    f,t,y,m,a = [z[k] for k in ('printed','t','y','m','answer')]
    point = r'\left(' + tex(t) + ',' + tex(y) + r'\right)'
    domain = r',\qquad x>0' if level=='hard' else ''
    prompt = "Find the slope $m'$ of the normal line to the curve\n\n" + display('y='+f+domain) + '\n\nat the point $'+point+"$. Give an exact answer.\n\n$m'=$\n{{field-1}}"
    work = 'Let $f(x)='+f+'$.'
    if z['expansion']:
        work += (' Expand and combine like terms before differentiating.' if level=='moderate' else
                 ' Expand the numerator and divide each term by $x^{1/2}$.')
        work += '\n\n' + aligned(['f(x)&='+z['expansion'][0], '&='+z['expansion'][1]])
    work += '\n\nApply the power rule:\n\n'+display("f'(x)="+poly(z['derivative']))
    substituted = poly(z['derivative'],r'\left('+tex(t)+r'\right)')
    evaluated = poly([(F(c)*power(t,e),0) for c,e in z['derivative']])
    work += '\n\nThe tangent slope at $'+point+'$ is\n\n'+aligned([
        "m=f'("+tex(t)+')&='+substituted, '&='+evaluated, '&='+tex(m)])
    work += '\n\nThe normal is perpendicular to the tangent, so take the negative reciprocal:\n\n'+aligned([
        r"m'&=-\frac{1}{m}", r'&=-\frac{1}{\left('+tex(m)+r'\right)}', '&='+tex(a)])
    question = {':question/problem':prompt, ':question/worked-solution':work,
                ':question/difficulty':':question.difficulty/'+level,
                ':question/answer-fields':[{':answer-field/key':'field-1',
                  ':answer-field/type':':answer-field.type/blank',
                  ':answer-field/correct':[':answer/id','key'],
                  ':answer-field/choices':[{':answer/id':'key',':answer/type':':answer.type/math',':answer/value':tex(a)}]}]}
    question,digest = identify(question)
    provenance=json.loads((HERE/'source-provenance.json').read_text())['bands'][level]
    refs=provenance['source_refs']
    return {'knowledge_point':KP, 'question':question,
            'generation':{'version':VERSION,'seed':seed,'template':level,'parameters':p,
                          'content_sha256':digest,'source_refs':refs,'source_inference':provenance['reason'],'source_basis':SOURCE['basis'],
                          'math_format':fmt.FORMAT_VERSION}}

def domain(level):
    if level=='easy':
        return [dict(a=a,b=b,c=c,t=t) for a,b,c,t in itertools.product(
            [-3,-2,-1,1,2,3],range(-5,6),range(-2,3),[-2,-1,1,2])]
    if level=='moderate':
        return [dict(b=b,c=c,t=t) for b,c in itertools.product([-3,-2,-1,1,2,3],repeat=2)
                for t in [-2,-1,1,2]]
    if level=='hard':
        return [dict(b=b,sign=sign,t=t) for b,sign,t in itertools.product([-3,-2,-1,1,2,3],[-1,1],[1,4,9])]
    raise ValueError('Unknown difficulty')

def batch(level,count,seed):
    if count<1:
        raise ValueError('Positive count required')
    params = domain(level)
    random.Random(seed).shuffle(params)
    rows=[]
    seen=set()
    # Each catalog has distinct functions and targets, including legitimate cancellation.
    for p in params:
        try:
            z=instance(level,p)
            semantic=(tuple((F(c),F(e)) for c,e in z['terms'] if c),z['t'])
            if semantic in seen:
                continue
            row=generate(level,p,seed)
        except ValueError as err:
            if 'Normal is vertical' in str(err):
                continue
            raise
        seen.add(semantic)
        rows.append(row)
        if len(rows)==count:
            return rows
    raise ValueError('Count exceeds distinct semantic capacity')

def replay_sources():
    """Complete captured evidence only; not random practice or database mutation."""
    rows=[]
    for original in SOURCE['questions']:
        q={k:copy.deepcopy(original[k]) for k in [':question/problem',':question/worked-solution']}
        if original[':question/math-academy-id']=='q-342153':
            q[':question/worked-solution']=q[':question/worked-solution'].replace(r'=\frac{1}{2\sqrt{{x}^{3}}}=', '=')
        q[':question/difficulty']=':question.difficulty/easy'
        fields=[]
        for old in original[':question/answer-fields']:
            ident=lambda v: v.get(':db/ident') if isinstance(v,dict) else v
            choices=[{':answer/id':str(i), ':answer/type':ident(a[':answer/type']),
                      ':answer/value':a[':answer/value']} for i,a in enumerate(old[':answer-field/choices'])]
            correct=old[':answer-field/correct'][':answer/id']
            index=next(i for i,a in enumerate(old[':answer-field/choices']) if a[':answer/id']==correct)
            fields.append({':answer-field/key':old[':answer-field/key'], ':answer-field/type':ident(old[':answer-field/type']),
                           ':answer-field/choices':choices, ':answer-field/correct':[':answer/id',str(index)]})
        q[':question/answer-fields']=fields
        q,digest=identify(q)
        rows.append({'knowledge_point':KP,'question':q,'generation':{'source_refs':[original[':question/id']],
                     'template':'source-replay','evidence_only':True,'content_sha256':digest}})
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',choices=[*LEVELS,'unclassified'],default='easy')
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--replay-sources',action='store_true')
    args=parser.parse_args()
    rows=replay_sources() if args.replay_sources else batch('easy' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(rows,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
