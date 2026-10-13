#!/usr/bin/env python3
"""Interpret a supplied derivative at an input: no differentiation or estimation.

Basis 1356. Six observed context/layout templates, five-choice text radio fields.
Observed profiles replay complete banks, including honestly documented anomalies.
Default authored profiles repair local/global prose and use defensible operations.
No EDB access. Read classification/template-extraction beside this script.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186064153
KP_UUID='2451a654-2255-5867-871d-54340dfeff81'
TITLE='Interpreting the Derivative of a Function in a Given Context'
VERSION='context-derivative-v1'
ROOT=Path(__file__).with_suffix('')
TEMPLATES={'app':'easy','walking':'easy','budget':'easy','car':'moderate',
           'price':'moderate','visitors':'moderate','ice':'hard','temperature':'hard',
           'signed_visitors':'hard'}
OBSERVED={'app':'q-48571','walking':'q-48615','car':'q-48688','price':'q-48691',
          'visitors':'q-48709','ice':'q-112091'}

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def num(value):
    value=sp.Rational(value)
    if value.q==1:
        return f'{int(value):,}'.replace(',',r'\,')
    # Domains use only terminating decimals or simple quotient distractors.
    denominator=int(value.q)
    for prime in (2,5):
        while denominator%prime==0: denominator//=prime
    if denominator==1: return str(float(value)).rstrip('0').rstrip('.')
    return r'\frac{'+str(value.p)+'}{'+str(value.q)+'}'

def parameters_for(template,rng):
    if template in ('price','visitors','signed_visitors'):
        rate=rng.choice([sp.Rational(n,10) for n in range(1,26)])
    elif template in ('ice','temperature'): rate=sp.Integer(rng.randint(2,25))
    elif template in ('app','budget'): rate=sp.Integer(rng.randrange(100,2100,50))
    else: rate=sp.Integer(rng.randrange(10,210,10))
    if TEMPLATES[template]=='hard': rate=-rate
    return {'input':rng.choice([2,4,5,8,10,16,20]),'rate':str(rate)}

def validate_parameters(template,p):
    if set(p)!={'input','rate'}: raise ValueError('Expected exactly input and rate')
    if isinstance(p['input'],bool) or not isinstance(p['input'],int) or not 2<=p['input']<=60:
        raise ValueError('input must be an integer between 2 and 60')
    try: r=sp.Rational(p['rate'])
    except (TypeError,ValueError): raise ValueError('rate must be an exact rational') from None
    if r==0 or (r<0)!=(TEMPLATES[template]=='hard'): raise ValueError('Level requires positive or negative rate')
    if template in ('price','visitors','signed_visitors'):
        if not sp.Rational(1,10)<=abs(r)<=5 or (abs(r)*100).q!=1:
            raise ValueError('Scaled rate must be 0.1 through 5 with at most two decimal places')
    elif r.q!=1 or not 2<=abs(r)<=5000: raise ValueError('rate must be an integer with magnitude 2 through 5000')
    return {'input':p['input'],'rate':str(r)}

def render(template,p,profile):
    """Every bank is constructed as a whole from the supplied input/rate.

    Choice meaning is (location, quantity, local/global/total/value, sign, magnitude,
    units). Only the correctly located local rate in dependent/input units follows.
    """
    t=p['input']; r=sp.Rational(p['rate']); a=num(t); b=num(abs(r)); signed=num(r)
    observed=profile=='observed'
    if template in ('app','car','walking'):
        if template=='app':
            f,v='U','t'; quantity='number of users'; unit='users'; time='hours'; per='hour'
            location=f'${a}$ hours after the launch'
            prompt=f'The function $U(t)$ models the number of users of a new mobile phone app, $t$ hours after launching the app. What is the best interpretation of ${{U}}^{{′}}({a})={signed}?$'
            opening='The function ${U}^{′}(t)$ represents the rate at which the number of users is changing at the moment $t$ hours after launch. '
            value=f'{location}, there are exactly ${b}$ users.'
            total=f'The number of users increased by ${b}$ during the first ${a}$ hours'
            constant=f'The number of users increased at a constant rate of ${num(r/t)}$ users per hour'
        elif template=='car':
            f,v='x','t';quantity='distance traveled';unit='meters';time='seconds';per='second'
            location=f'${a}$ seconds after the start of the journey'
            prompt=f'The function $x(t)$ models the number of meters traveled by a car, $t$ seconds after it sets off on a journey. What is the best interpretation of ${{x}}^{{′}}({a})={signed}?$'
            opening='The function ${x}^{′}(t)$ represents the rate at which the number of meters is changing at the moment $t$ seconds after starting its journey.'
            value=f'{location}, the car traveled ${b}$ meters.'
            total=f'The distance traveled increased by ${b}$ meters during the first ${a}$ seconds'
            constant=f'The distance traveled increased at a constant rate of ${num(t/r if observed else r/t)}$ meters per second'
        else:
            f,v='W','d';quantity='distance Sam walked';unit='meters';time='days';per='day'
            location=f'${a}$ days after taking up walking' if observed else f'On day ${a}$'
            prompt=f'Sam decides to take up walking. The function $W(d)$ models the number of meters Sam walks on day $d$. What is the best interpretation of $W^{{′}}({a}) = {signed}$?'
            if not observed: prompt=prompt.replace('models the number','is a continuous model of the number')
            opening="The function $W^{′}(d)$ represents the rate at which Sam's daily walking distance is changing on day $d$."
            value=f'Sam walked a distance of ${b}m$ on day ${a}$.'
            total=f'The distance Sam walked increased by ${b}$ meters after ${a}$ days'
            constant=f'{location}, the distance Sam walked increased at a constant rate of ${num(r/t)}$ meters per day'
        correct=f'{location}, the {quantity} increased at a rate of ${b}$ {unit} per {per}'
        wrong_sign=correct.replace('increased','decreased')
        if template=='car' and not observed:
            # Cumulative distance cannot decrease. The authored whole bank uses
            # the positive supplied input as a mistaken rate instead.
            wrong_sign=f'{location}, the {quantity} increased at a rate of ${a}$ {unit} per {per}'
        choices=[correct,constant,value,wrong_sign,total]
        derivative=f'${{{f}}}^{{′}}({a})={signed}$' if template!='walking' else f'$W^{{′}}({a}) = {signed}$'
        solution=opening+f'\n\nTherefore, {derivative} means:\n\n$\\,$ *{correct}*'
        meanings=['local','global_quotient' if not(template=='car' and observed) else 'global_reciprocal_quotient','value','input_as_rate' if template=='car' and not observed else 'opposite_sign','total']
    elif template in ('price','visitors','signed_visitors'):
        price=template=='price'; f,v=('P','v') if price else ('V','t')
        magnitude=num(abs(r)*(100 if price else 1000)); direction='increases' if r>0 else 'decreases'; past='increased' if r>0 else 'decreased'
        if price:
            prompt=f'The function $P(v)$ models the price of lemonade sold at a lemonade stand, in dollars, depending on the volume $v$ sold the previous day, in liters. What is the best interpretation of the statement below?\n\n$\\,$ *The slope of the tangent line to the graph of $P(v)$ at $v={a}$ is equal to ${signed}.$*'
            correct=f'When ${a}$ liters of lemonade are sold the previous day, the price {direction} at a rate of ${magnitude}$ cents per liter'
            choices=[correct,f'When the price of lemonade equals ${magnitude}$ cents, the amount sold decreases at a rate of ${a}$ liters per dollar',correct.replace('increases','decreases'),f'When ${a}$ liters of lemonade were sold the previous day, the price of lemonade is equal to ${magnitude}$ cents.',f'When the price of lemonade equals ${magnitude}$ cents, the amount sold increases at a rate of ${a}$ liters per dollar']
            conclusion=f'When ${a}$ liters of lemonade are sold the previous day, the price is increasing at a rate of ${magnitude}$ cents per liter.'
            meanings=['local','swapped_opposite','opposite_sign','value','swapped_same']
        else:
            prompt=f"The function $V(t)$ models the number of visitors, in thousands, to a new website, $t$ hours after the website's launch. What is the best interpretation of the statement below?\n\n$\\,$ *The slope of the tangent line to the graph of $V(t)$ at $t={a}$ is equal to ${signed}.$*"
            if template=='signed_visitors':
                prompt=prompt.replace('the number of visitors, in thousands, to a new website',
                                      'the number of visitors currently on a new website, in thousands')
            loc=f'${a}$ hours after launching, the number of visitors '
            correct=loc+f'{past} at a rate of ${magnitude}$ visitors per hour'
            opposite='decreased' if r>0 else 'increased'
            choices=[loc+f'{opposite} at a rate of ${magnitude}$ visitors per hour',loc+f'{past} by a total of ${magnitude}$ visitors',correct,loc+f'{past} at a constant rate of ${num(abs(r)*1000/t)}$ visitors per hour',loc+f'{opposite} by a total of ${magnitude}$ visitors']
            conclusion=correct+'.'; meanings=['opposite_sign','total','local','global_quotient','opposite_total']
        solution=f'The slope of the line tangent to the graph of ${f}({v})$ at ${v}={a}$ gives the derivative of ${f}({v})$ at ${v}={a}.$ So, we have that\n\n$$\n{{{f}}}^{{′}}({a})={signed}.\n$$\n\nWe can interpret the above statement as\n\n$\\,$ *{conclusion}*'
    elif template=='ice':
        prompt=f'The function $S(t)$ gives the area, in squared centimeters, of a thin sheet of ice as it melts $t$ minutes after observations start. What is the best interpretation of ${{S}}^{{′}}({a})={signed}?$'
        loc=f'${a}$ minutes after the observations began, the area of the sheet '
        correct=loc+f'decreases at a rate of ${b}$ squared centimeters per minute'
        choices=[loc+f'is ${b}$ squared centimeters',correct,f'${b}$ minutes after the observation began, the area of the sheet increases at a rate of ${a}$ squared centimeters per minute',f'During the first ${a}$ minutes of the observations, the area has constantly decreased at a rate of ${b}$ squared centimeters per minute',f'${b}$ minutes after the observations began, the area of the sheet is ${a}$ squared centimeters']
        change='decreasing' if observed else 'changing'
        solution=f'The function ${{S}}^{{′}}(t)$ represents the rate at which the area of the sheet is {change} $t$ minutes after the beginning of the observation.\n\nTherefore, since it is negative, ${{S}}^{{′}}({a})={signed}$ means:\n\n$\\,$ *{correct}.*'
        meanings=['value','local','swapped_opposite','global','swapped_value']
    elif template=='budget':
        prompt=f"The function $B(s)$ models a school's budget, in dollars, given the average number of students $s$ in each grade. What is the best interpretation of $B'({a})={signed}?$"
        correct=f'When the school has an average of ${a}$ students in each grade, its budget is increasing at a rate of ${b}$ dollars per student.'
        choices=[correct,correct.replace('increasing','decreasing'),f'When the school has an average of ${a}$ students in each grade, its budget is ${b}$ dollars.',f'The budget increased by ${b}$ dollars as the average rose from zero to ${a}$ students in each grade.',f'The budget increases at a constant rate of ${num(r/t)}$ dollars per student.']
        solution=f"The function $B'(s)$ represents the rate at which the budget is changing at the moment when the school has an average of exactly $s$ students in each grade.\n\nTherefore, $B'({a}) = {signed}$ means:\n\n*{correct}*"
        meanings=['local','opposite_sign','value','total','global_quotient']
    else:
        prompt=f'The function $T(t)$ models the temperature, in degrees Celsius, of a cooling cup of tea $t$ minutes after observations begin. What is the best interpretation of $T^{{′}}({a})={signed}$?'
        loc=f'${a}$ minutes after observations begin, the temperature '
        correct=loc+f'decreases at a rate of ${b}$ degrees Celsius per minute.'
        choices=[correct,correct.replace('decreases','increases'),loc+f'is ${b}$ degrees Celsius.',f'During the first ${a}$ minutes, the temperature decreased by ${b}$ degrees Celsius.',f'During the first ${a}$ minutes, the temperature decreased at a constant rate of ${b}$ degrees Celsius per minute.']
        solution=f'The function $T^{{′}}(t)$ represents the rate at which the temperature is changing $t$ minutes after observations begin.\n\nTherefore, since it is negative, $T^{{′}}({a})={signed}$ means:\n\n$\\,$ *{correct}*'
        meanings=['local','opposite_sign','value','total','global']
    if len(set(choices))!=5: raise ValueError('Whole bank rejected: duplicate choices')
    return prompt,solution,choices,meanings,choices.index(correct)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('Invalid level')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only radio fields supported')
    rng=random.Random(seed)
    eligible=[name for name,d in TEMPLATES.items() if d==level]
    if template is None:
        if profile=='observed': eligible=[x for x in eligible if x in OBSERVED]
        template=rng.choice(eligible)
    if template not in eligible: raise ValueError('Template is not in requested level')
    profile=profile or 'authored'
    if profile not in ('observed','authored') or (profile=='observed' and template not in OBSERVED): raise ValueError('Unsupported complete profile')
    for attempt in range(100):
        p=validate_parameters(template,parameters if parameters is not None else parameters_for(template,rng))
        try:
            prompt,solution,values,meanings,correct=render(template,p,profile)
            break
        except ValueError:
            if parameters is not None: raise
    else: raise ValueError('No eligible whole bank after 100 samples')
    # Bank/order/seed excluded from mathematical-task fingerprint.
    fingerprint=digest({'template':'visitors' if template=='signed_visitors' else template,'input':p['input'],'rate':p['rate']})
    content={'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct':values[correct]}
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),digest(content)))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/text',':answer/value':value} for value in values]
    correct_id=choices[correct][':answer/id']; rng.shuffle(choices)
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,
              ':question/problem':prompt,':question/worked-solution':solution,
              ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',
                 ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,
                 ':answer-field/correct':[':answer/id',correct_id]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
            'generation':{'version':VERSION,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},
                'level':level,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,
                'source_ids':[OBSERVED[template]] if template in OBSERVED else [],
                'mathematical_fingerprint':fingerprint,'content_hash':digest(content),
                'recipes':dict(zip(values,meanings)),'domain':'positive contextual input; local rate only; continuous contextual model',
                'plot_rating':'none','dependencies':{'sympy':sp.__version__}}}

# EASY: positive direct rates, no scaling; walking is explicitly modeled continuously.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE: observed direct car rate, tangent slope, dollars-to-cents / thousands scaling.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD: negative local derivative; sign plus contextual location and optional observed scale.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\nWorked solution:\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    parser.add_argument('--seed',type=int,default=0); parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    parser.add_argument('--template');parser.add_argument('--profile',choices=['observed','authored'])
    args=parser.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
