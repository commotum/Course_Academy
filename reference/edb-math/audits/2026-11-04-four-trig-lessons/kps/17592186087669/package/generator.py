#!/usr/bin/env python3
"""Seeded cosine double-angle practice. Pure standard-library runtime; no assets."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '1.0.0'
KP = {'db_id':17592186087669, 'id':'5ec37c5e-8a40-58a7-8af3-4457cd5da43f',
      'title':'Using the Double-Angle Formula to Simplify Expressions'}
SOURCE = {'easy':['d5d50fd1-bc8e-514c-8dca-56cd8a6999fe','d38b6d10-21f4-5ec6-94ba-9141257529fc'],
          'moderate':['6bb4ecb6-0b76-51e4-aa33-5be6f12e1dbb','cf1faff6-afe0-59ea-a58f-f8289c637840','a4d26858-a337-5218-af76-0e3d4aac3fca'],
          'hard':['6876b3d3-10b5-5357-a52d-52e5ecb514f0']}
NS = uuid.UUID('7c26a387-7f9a-4ccf-9b57-e6fdc2823cd5')

def uid(s): return str(uuid.uuid5(NS, s))
def frac(n):
    n = F(n)
    sign = '-' if n < 0 else ''
    n = abs(n)
    return sign + (str(n.numerator) if n.denominator == 1 else rf'\frac{{{n.numerator}}}{{{n.denominator}}}')

def angle(a, unit):
    a = F(a)
    if unit == 'degrees': return frac(a) + r'^\circ'
    if a == 0: return '0'
    sign = '-' if a < 0 else ''
    a = abs(a)
    numerator = (str(a.numerator) if a.numerator != 1 else '') + r'\pi'
    return sign + (numerator if a.denominator == 1 else rf'\frac{{{numerator}}}{{{a.denominator}}}')

def coefficient(c, radical=False):
    c=F(c)
    if not radical: return '' if c == 1 else frac(c)
    n = ('' if c.numerator == 1 else str(c.numerator)) + r'\sqrt{3}'
    return n if c.denominator == 1 else rf'\frac{{{n}}}{{{c.denominator}}}'

def trig(c, a, unit, radical=False, power=1, function='cos'):
    return coefficient(c,radical) + '\\' + function + (rf'^{{{power}}}' if power != 1 else '') + r'\left(' + angle(a,unit) + r'\right)'

def display(s): return '$$\n' + s + '\n$$'
def aligned(rows): return display('\\begin{aligned}\n' + ' \\\\\n'.join(rows) + '\n\\end{aligned}')

def value(c,a,unit,radical=False):
    z = float(a) * (math.pi/180 if unit == 'degrees' else math.pi)
    return float(c)*(math.sqrt(3) if radical else 1)*math.cos(z)

def make(difficulty, c, a, unit, radical=False, bank=None, order=None, provenance=None):
    """One derivation drives the question, key, and final form. a is the original angle."""
    c,a=F(c),F(a)
    p=4 if difficulty=='hard' else 2
    raw = trig(c,a,unit,radical,p) + '-' + trig(c,a,unit,radical,p,'sin')
    diff = trig(1,a,unit,False,2)+'-'+trig(1,a,unit,False,2,'sin')
    sumsq = trig(1,a,unit,False,2)+'+'+trig(1,a,unit,False,2,'sin')
    front = coefficient(c,radical)
    factored = front+r'\left('+diff+r'\right)'
    final=trig(c,2*a,unit,radical)
    pieces=[]
    if difficulty=='hard':
        pieces += ['Use the difference of squares, then the Pythagorean identity.',
            aligned(['&'+raw, '&='+front+r'\left('+diff+r'\right)', r'&\qquad\cdot\left('+sumsq+r'\right)']),
            'Since $'+sumsq+'=1$, this reduces to', display(factored+'.')]
    elif c!=1 or radical:
        pieces += ['Factor out the common coefficient:', aligned(['&'+raw,'&='+factored+'.'])]
    pieces += ['Recall the **double-angle formula for cosine**:', display(r'\cos^2 x-\sin^2 x=\cos(2x).'),
               'Substitute $x='+angle(a,unit)+'$ and double the angle:',
               aligned(['&'+factored, '&='+front+r'\cos\left(2\cdot '+angle(a,unit)+r'\right)', '&='+final+'.']),
               'Only the angle doubles; the common coefficient stays outside the cosine.']
    problem=normalize_prose('Express\n\n'+display(raw)+'\n\nas a single trigonometric ratio.')
    solution=normalize_prose('\n\n'.join(pieces))
    if bank is None: bank=[(c,2*a)]
    values=[normalize_tex(trig(b,t,unit,radical)) for b,t in bank]
    assert final in values
    correct_index=values.index(final)
    if order is None: order=list(range(len(bank)))
    fingerprint=hashlib.sha256(json.dumps([problem,solution,values],ensure_ascii=False).encode()).hexdigest()
    qid=uid(fingerprint)
    answers=[{':answer/id':uid(qid+':answer:'+str(i)), ':answer/type':':answer.type/math', ':answer/value':values[i]} for i in order]
    record={'knowledge_point':KP.copy(), 'question':{
        ':question/id':qid, ':question/problem':problem, ':question/worked-solution':solution,
        ':question/difficulty':':question.difficulty/'+difficulty,
        ':question/answer-fields':[{':answer-field/id':uid(qid+':field'), ':answer-field/key':'selection',
            ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':answers,
            ':answer-field/correct':[':answer/id',uid(qid+':answer:'+str(correct_index))]}]},
        'generation':{'version':VERSION, 'template':difficulty+'-cosine-difference',
            'parameters':{'coefficient':str(c),'radical':radical,'angle':str(a),'unit':unit,'power':p},
            'source_question_ids':provenance or SOURCE[difficulty], 'authored_bank':True,
            'domain':'real angle; no quotient/domain restriction', 'final':final}}
    return validate_generated_record(record)

def group(rng,difficulty,unit):
    # Assign the answer-bearing role before compatible incidental parameters.
    roles=[1,2,3] if difficulty=='easy' else list(range(5))
    rng.shuffle(roles)
    for _ in range(500):
        base=F(rng.randint(3,21)) if unit=='degrees' else F(rng.choice([1,2,3]),rng.choice([11,13,17,19,23,29,31]))
        if difficulty=='easy': c,radical=F(1),False
        elif difficulty=='hard': c,radical=F(rng.choice([2,4,6])),False
        else: c,radical=rng.choice([(F(3),False),(F(5),False),(F(5,2),False),(F(1),True)])
        bank = [(c,base*2**j) for j in range(5)] if difficulty=='easy' else [
            (c,base),(c,2*base),(c,4*base),(2*c,base),(2*c,2*base)]
        evaluated=[value(b,t,unit,radical) for b,t in bank]
        if all(abs(v-w)>1e-9 for i,v in enumerate(evaluated) for w in evaluated[:i]): break
    else: raise RuntimeError('No unambiguous bank')
    order=list(range(5)); rng.shuffle(order)
    result=[]
    for role in roles:
        b,t=bank[role]
        r=make(difficulty,b,t/2,unit,radical,bank,order)
        r['generation'].update({'bank_profile':('angle-ladder' if difficulty=='easy' else 'factor-angle-cross'),
            'role':role,'base_angle':str(base),'base_coefficient':str(c)})
        result.append(r)
    return result

def generate(difficulty,count,seed):
    if difficulty=='unclassified': difficulty='moderate'
    if count<0: raise ValueError('count must be nonnegative')
    rng=random.Random(seed); out=[];seen=set(); attempts=0
    units=['degrees','radians']; rng.shuffle(units)
    while len(out)<count:
        unit=units[attempts%2]; attempts+=1
        if attempts>10000: raise ValueError('Requested batch exceeds supported unique construction budget')
        for r in group(rng,difficulty,unit):
            semantic=r['question'][':question/problem']
            if semantic in seen: continue
            seen.add(semantic); r['generation'].update({'seed':seed,'index':len(out)})
            out.append(r)
            if len(out)==count: break
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json'],default='json');args=p.parse_args()
    print(json.dumps(generate(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
