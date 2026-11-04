#!/usr/bin/env python3
"""Seeded, relocatable double-angle product practice; no runtime third-party imports."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186059671, 'id':'143766e0-0ef5-5caf-b699-d394d4a707e9',
      'title':'Using the Double-Angle Formula to Simplify Products'}
SOURCES = {
 'direct':['188c3216-6730-58aa-bfa7-8985bab845cd','64c46307-6499-587a-8e3d-194000e8c499','feecaade-207a-51bf-96ee-61bce1de2e85','ff03781e-e811-57da-88cb-583d049585d0','71319f17-956d-5226-b02f-5e0082742e93','af0778bb-fb31-5795-b709-311385ef20eb'],
 'square':['807c1c95-6fea-5d65-a59b-b497c894ecc9'],
 'quotient':['984868e6-9b0d-5753-97a4-a56b885226b2']}

def frac(n):
    n=F(n)
    return str(n.numerator) if n.denominator==1 else (('-' if n<0 else '')+r'\frac{'+str(abs(n.numerator))+'}{'+str(n.denominator)+'}')

def angle(a, unit):
    a=F(a)
    if unit=='deg': return frac(a)+r'^\circ'
    sign='-' if a<0 else ''
    n=abs(a.numerator)
    top=('' if n==1 else str(n))+r'\pi'
    return sign+(top if a.denominator==1 else r'\frac{'+top+'}{'+str(a.denominator)+'}')

def trig(fun,a,unit,power=1):
    return '\\'+fun+('^{'+str(power)+'}' if power!=1 else '')+r'\left('+angle(a,unit)+r'\right)'

def term(c,body):
    c=F(c)
    if c==0:return '0'
    return ('' if c==1 else '-' if c==-1 else frac(c))+body

# specs: (coefficient, function, frequency of original argument, additive constant)
def expression(spec,a,unit):
    c,fun,freq,offset=spec
    if c==0:return frac(offset)
    t=term(c,trig(fun,F(a)*F(freq),unit))
    return (frac(offset)+('' if t.startswith('-') else '+')+t) if offset else t

def value(spec,a,unit):
    c,fun,freq,offset=spec
    x=float(F(a))* (math.pi/180 if unit=='deg' else math.pi)*float(freq)
    return float(offset)+float(c)*getattr(math,fun)(x)

def aligned(rows):
    return '$$\n'+r'\begin{aligned}'+'\n'+r' \\ '.join(rows)+'\n'+r'\end{aligned}'+'\n$$'

def make(level,family,a,unit,k=2,sign=1,order=False,profile='mixed',rng=None,bank=None):
    """A bank override is only for explicit original-parameter source replay."""
    rng=rng or random.Random(0);a=F(a);k=F(k)
    sa,ca=trig('sin',a,unit),trig('cos',a,unit)
    product=(ca+sa if order else sa+ca)
    common=r'\sin x\cos x'
    intro=r'Recall $2\sin x\cos x=\sin(2x)$.'
    put='Put $x='+angle(a,unit)+'$.'
    if family=='direct':
        key=(k/2,'sin',2,0)
        printed=term(k,product)
        problem='Express the following as a constant multiple of a single trigonometric ratio.\n\n$$\n'+printed+'\n$$'
        rows=[term(k,common)+' &='+term(k/2,r'\left[2\sin x\cos x\right]'),r'&='+term(k/2,r'\sin(2x)')]
        solution=put+' '+intro+'\n\n'+aligned(rows)
    elif family=='square':
        op='+' if sign==1 else '-'
        key=(k*sign,'sin',2,k)
        square=r'\left('+sa+op+ca+r'\right)^2'
        printed=term(k,square)
        problem='Simplify.\n\n$$\n'+printed+'\n$$'
        solution=put+' Expand the square and combine the squared terms.\n\n'+aligned([
            r'(\sin x'+op+r'\cos x)^2 &=\sin^2 x'+op+r'2\sin x\cos x+\cos^2 x',
            r'&=1'+op+r'2\sin x\cos x',
            r'&=1'+op+r'\sin(2x)'])+'\n\n'+r'Here $\sin^2 x+\cos^2 x=1$ and $2\sin x\cos x=\sin(2x)$.'
        if k!=1:
            solution+=' Multiply both terms by $'+frac(k)+'$.'
    elif family=='quotient':
        key=(k/2,'tan',2,0)
        printed=r'\frac{'+term(k,product)+'}{'+trig('cos',2*a,unit)+'}'
        problem='Simplify.\n\n$$\n'+printed+'\n$$'
        solution=put+' '+intro+'\n\n'+aligned([
            r'\frac{'+term(k,common)+r'}{\cos(2x)} &='+term(k/2,r'\frac{2\sin x\cos x}{\cos(2x)}'),
            '&='+term(k/2,r'\frac{\sin(2x)}{\cos(2x)}'),
            '&='+term(k/2,r'\tan(2x)')])+'\n\n'+r'The denominator is nonzero, and $\tan(2x)=\sin(2x)/\cos(2x)$.'
    else:raise ValueError(family)
    solution+='\n\nSubstitute $x='+angle(a,unit)+'$ and double the whole angle: $2x='+angle(2*a,unit)+'$. The result is\n\n$$\n'+expression(key,a,unit)+' .\n$$'
    c,fun,freq,offset=key
    # Every recipe is an actual algebra/identity error, including joint errors seen in source banks.
    recipes=[((c*2,fun,2,offset),'retain twice the required coefficient','scale'),
             ((c/2,fun,2,offset),'insert an extra half','scale'),
             ((-c,fun,2,offset),'reverse the sign','scale'),
             ((c,fun,1,offset),'fail to double the angle','angle'),
             ((c,fun,F(1,2),offset),'halve the angle instead of doubling','angle'),
             ((c,fun,4,offset),'double the angle twice','angle'),
             ((2*c,fun,1,offset),'retain the coefficient and fail to double','joint'),
             ((c/2,fun,1,offset),'insert an extra half and fail to double','joint'),
             ((2*c,fun,4,offset),'double both the coefficient and the doubled angle','joint'),
             ((c/2,fun,4,offset),'halve the coefficient and double the angle twice','joint'),
             ((c,'cos' if fun!='cos' else 'sin',2,offset),'use cosine instead of the required function','function')]
    # A sign error can accompany an angle or coefficient error too; otherwise the
    # only +/- pair always contains the correct choice, a bank-only clue.
    recipes += [(( -spec[0],spec[1],spec[2],spec[3]),
                 'reverse the sign and '+why, 'joint')
                for spec,why,kind in list(recipes) if kind in ('angle','scale','joint') and spec[0]!=-c]
    if family=='square':
        recipes += [((F(0),'sin',2,k),'drop the cross term','scale'),
                    ((c,'sin',2,0),'drop the squared terms','joint'),
                    ((c,'sin',2,-k),'reverse the sign of the squared terms','joint')]
    if bank is None:
        # Bias a profile without fixing any bank-only modal intersection or numerical rank.
        weighted=recipes+([r for r in recipes if r[2]==profile] if profile!='mixed' else [])
        for _ in range(200):
            selected=rng.sample(weighted,4)
            specs=[key]+[s for s,_,_ in selected]
            vals=[value(s,a,unit) for s in specs]
            distinct=all(abs(x-y)>1e-8 for i,x in enumerate(vals) for y in vals[:i])
            opposite_pairs=sum(abs(x+y)<1e-8 for i,x in enumerate(vals) for y in vals[:i])
            # One unique +/- pair supplies an incidental bank-only narrowing.
            # Zero pairs or multiple plausible pairs leave no unique counterpart cue.
            if distinct and opposite_pairs!=1:break
        else:raise ValueError('Cannot construct distinct plausible bank')
        bank=[(key,'correct')]+[(s,why) for s,why,_ in selected]
        rng.shuffle(bank)
    vals=[value(s,a,unit) for s,_ in bank]
    target=value(key,a,unit)
    if sum(abs(v-target)<1e-8 for v in vals)!=1 or any(abs(x-y)<1e-8 for i,x in enumerate(vals) for y in vals[:i]):
        raise ValueError('Degenerate bank')
    problem,solution=map(normalize_prose,(problem,solution))
    choices_values=[normalize_tex(expression(spec,a,unit)) for spec,_ in bank]
    # Normalize before identity; order is not mathematical identity.
    identity=json.dumps([level,problem,solution,sorted(choices_values)],sort_keys=True)
    token=hashlib.sha256(identity.encode()).hexdigest()
    uid=lambda role:str(uuid.uuid5(uuid.NAMESPACE_URL,'ca-double-angle-v1:'+token+':'+role))
    choices=[{':answer/id':uid('answer:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in choices_values]
    correct=next(ch for ch,(spec,_) in zip(choices,bank) if abs(value(spec,a,unit)-target)<1e-8)
    record={'knowledge_point':KP.copy(),'question':{
        ':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,
        ':question/problem':problem,':question/worked-solution':solution,
        ':question/answer-fields':[{
          ':answer-field/id':uid('field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
          ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct[':answer/id']]}]},
        'generation':{'generator':'double-angle-products-v2','family':family,'profile':profile,
          'parameters':{'a':str(a),'unit':unit,'k':str(k),'sign':sign,'order':order},
          'source_question_ids':SOURCES[family], 'domain':'numeric acute original angle; nonzero product; quotient denominator nonzero',
          'difficulty_basis':'imported structures; hard scalar bookkeeping is an authored adjacent band with no imported hard anchor',
          'authored_extension':level=='hard', 'choice_errors':{ch[':answer/id']:why for ch,(_,why) in zip(choices,bank)}}}
    return validate_generated_record(record)

def generate(level,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);records=[];seen=set();attempts=0
    families={'easy':['direct'],'moderate':['square','quotient'],'hard':['square','quotient']}[level]
    schedule=[]
    while len(records)<count:
        attempts+=1
        if attempts>max(1000,count*100):raise ValueError('Requested batch exceeds available distinct instances')
        if not schedule:
            schedule=families.copy();rng.shuffle(schedule)
        family=schedule[-1]
        sign=rng.choice([-1,1])
        k=rng.choice([2,4,6,8]) if level=='easy' else (F(1) if family=='square' else rng.choice([2,4])) if level=='moderate' else rng.choice([-3,-F(1,2),F(1,2),3])
        unit=rng.choice(['deg','rad'])
        a=F(rng.choice([7,11,13,17,19,23,26,28,31,34,37,41,49,53,58,62,67,71,76,79,82])) if unit=='deg' else rng.choice([F(1,5),F(2,5),F(1,6),F(1,7),F(2,7),F(3,7),F(1,9),F(2,9),F(4,9),F(1,11),F(2,11),F(3,11),F(4,11)])
        if family=='quotient' and abs(math.cos(2*float(a)*(math.pi/180 if unit=='deg' else math.pi)))<1e-8:continue
        try:r=make(level,family,a,unit,k,sign,rng.choice([False,True]),rng.choice(['scale','angle','mixed']),rng)
        except ValueError:continue
        semantic=(family,str(a),unit,str(k),sign if family=='square' else None)
        if semantic in seen:continue
        seen.add(semantic);schedule.pop();r['generation'].update(seed=seed,batch_index=len(records))
        records.append(r)
    return records

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json'],default='json');args=p.parse_args()
    print(json.dumps(generate(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
