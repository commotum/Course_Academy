#!/usr/bin/env python3
"""Relocatable seeded power-of-product practice, standard library only."""
import argparse
import hashlib
import re
import json
import math
import random
import uuid
from fractions import Fraction
from math_format import checked_math_content, normalize_tex, normalize_prose

VERSION = '1.1.1'
KP = {'db_id': 17592186129111, 'id': '525486fb-d976-57a5-b6bd-c33f19177a3f',
      'title': 'Applying the Power of Product Rule to Expressions with Fractions'}
NAMESPACE = uuid.UUID(KP['id'])
SOURCES = [
 ('c97f8543-9bdb-52c4-b17d-3d871ba2d7b7','integer','standard','what',9,2,5,6,None),
 ('176ffc94-567f-54c0-95d5-b097e9a1a0fd','fraction','fraction','what',3,7,2,4,None),
 ('0c9fa50a-f706-574b-a81a-64d392ef7788','integer','standard','equation',8,3,5,4,'easy'),
 ('79195c97-f47a-5a8c-930f-60cd5aaabae5','integer','repeated','equation',5,2,3,8,'easy'),
 ('c32986e7-9010-5588-b701-72ad7388c062','fraction','fraction','equation',4,7,5,5,'easy')]

def frac(a,b): return rf'\frac{{{a}}}{{{b}}}'
def power(a,n):
    return rf'\left({a}\right)^{{{n}}}' if '\\frac' in a else rf'{a}^{{{n}}}'
def prod(a,b): return a + r'\times ' + b

def components(p):
    a,b,c,n = (p[k] for k in ('a','b','c','n'))
    if p['kind']=='integer':
        left,right = str(a),frac(b,c)
        pair = (Fraction(a),Fraction(b,c))
        texts = {'correct':prod(power(left,n),power(right,n)),
                 'left_only':prod(power(left,n),right),
                 'right_only':prod(left,power(right,n)),
                 'numerator_only':prod(left,frac(power(str(b),n),c)),
                 'denominator_omitted':frac(prod(power(str(a),n),power(str(b),n)),c),
                 'repeated_numerator':frac(prod(power(str(b),n),power(str(b),n)),c)}
        values = {'correct': (pair[0]*pair[1])**n,
                  'left_only':pair[0]**n*pair[1], 'right_only':pair[0]*pair[1]**n,
                  'numerator_only':Fraction(a*b**n,c),
                  'denominator_omitted':Fraction(a**n*b**n,c),
                  'repeated_numerator':Fraction(b**(2*n),c)}
        recipes = ['correct','left_only','right_only','numerator_only',
                   'denominator_omitted' if p['profile']=='standard' else 'repeated_numerator']
    else:
        left,right = frac(a,b),frac(1,c)
        pair=(Fraction(a,b),Fraction(1,c))
        texts={'correct':prod(power(left,n),power(right,n)),
               'left_only':prod(power(left,n),right),
               'right_only':prod(left,power(right,n)),
               'numerator_only':frac(power(str(a),n),prod(str(b),str(c))),
               'denominator_only':frac(a,prod(power(str(b),n),power(str(c),n)))}
        values={'correct':(pair[0]*pair[1])**n, 'left_only':pair[0]**n*pair[1],
                'right_only':pair[0]*pair[1]**n, 'numerator_only':Fraction(a**n,b*c),
                'denominator_only':Fraction(a,b**n*c**n)}
        recipes=['correct','left_only','right_only','numerator_only','denominator_only']
    if p.get('reverse'):
        left,right=right,left
        # Keep error meanings tied to original factors, with displayed products reversed.
        for k in ('correct','left_only','right_only'):
            x,y=texts[k].split(r'\times ')
            texts[k]=prod(y,x)
    expression=rf'\left({prod(left,right)}\right)^{{{n}}}'
    return expression,texts,values,recipes

@checked_math_content
def build(p, order=None, source=None):
    expression,texts,values,recipes=components(p)
    solution_answer=texts["correct"]
    if len({values[r] for r in recipes})!=5: raise ValueError('ambiguous bank')
    prompt = f'What is ${expression}$?' if p['layout']=='what' else f'${expression}=$'
    n=p['n']
    solution=(f'To raise the product of two numbers to the power of ${n}$, '
              f'we can raise each number to the power of ${n},$ and then multiply:\n\n'
              f'$$\n{expression}={solution_answer}\n$$')
    prompt,solution=map(normalize_prose,(prompt,solution))
    texts={r:normalize_tex(texts[r]) for r in recipes}
    # Content identity ignores seed and choice order; bank differences are included.
    signature=json.dumps([prompt,sorted(texts.items())],sort_keys=True)
    qid=uuid.uuid5(NAMESPACE,signature)
    fid=uuid.uuid5(qid,'field:selection')
    choices=[{':answer/id':str(uuid.uuid5(fid,texts[r])), ':answer/type':':answer.type/math',
              ':answer/value':texts[r]} for r in (order or recipes)]
    q={':question/id':str(qid), ':question/problem':prompt,
       ':question/worked-solution':solution, ':question/difficulty':':question.difficulty/easy',
       ':question/answer-fields':[{':answer-field/id':str(fid), ':answer-field/key':'selection',
        ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices,
        ':answer-field/correct':[':answer/id',str(uuid.uuid5(fid,texts['correct']))]}]}
    return {'knowledge_point':KP,'question':q,'assets':{},'generation':{
        'version':VERSION,'template':p['kind']+'-'+p['layout'],'profile':p['profile'],
        'parameters':dict(p),'recipes':order or recipes,'source':source,
        'domain':'positive reduced proper fractions; exponent 2..8',
        'dependencies':{'python':'3.13.5','packages':{}}}}

def replay():
    records=[]
    for sid,kind,profile,layout,a,b,c,n,difficulty in SOURCES:
        p=dict(kind=kind,profile=profile,layout=layout,a=a,b=b,c=c,n=n,reverse=False)
        records.append(build(p,source={'question_id':sid,'original_difficulty':difficulty}))
    return records

def semantic(p):
    return (p['kind'],p['a'],p['b'],p['c'],p['n'])

def generate(difficulty='easy',count=5,seed=0):
    if difficulty!='easy': raise ValueError('Only source-supported easy difficulty is available')
    if count<0 or count>2248: raise ValueError('count must be 0..2248 (finite semantic family)')
    rng=random.Random(seed)
    result=[]; seen=set(); attempts=0
    while len(result)<count:
        attempts+=1
        if attempts>max(1000,count*100): raise ValueError('requested semantic family exhausted')
        # Select decision roles and complete bank before numerical slots.
        kind=rng.choice(['integer','fraction'])
        profile=rng.choice(['standard','repeated']) if kind=='integer' else 'fraction'
        layout=rng.choice(['what','equation']); reverse=rng.choice([False,True])
        a=rng.randint(2,9)
        if kind=='integer':
            c=rng.randint(3 if profile=='standard' else 2,9)
            b=rng.randint(2 if profile=='standard' else 1,c-1)
            if math.gcd(b,c)!=1: continue
        else:
            b=rng.randint(3,9); a=rng.randint(2,b-1); c=rng.randint(2,9)
            if math.gcd(a,b)!=1: continue
        p=dict(kind=kind,profile=profile,layout=layout,reverse=reverse,a=a,b=b,c=c,n=rng.randint(2,8))
        if semantic(p) in seen: continue
        try:
            recipes=components(p)[3][:]; rng.shuffle(recipes)
            record=build(p,recipes)
        except ValueError: continue
        record['generation'].update(seed=seed,attempt=attempts,source_references=[s[0] for s in SOURCES if s[1]==kind and s[2]==profile])
        result.append(record); seen.add(semantic(p))
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--difficulty',default='easy')
    ap.add_argument('--count',type=int,default=5); ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json'); ap.add_argument('--replay-source',action='store_true')
    args=ap.parse_args()
    try: data=replay() if args.replay_source else generate(args.difficulty,args.count,args.seed)
    except ValueError as exc: ap.error(str(exc))
    print(json.dumps(data,ensure_ascii=False,indent=2))
