#!/usr/bin/env python3
"""Solving an inhibited decay model: source-faithful radios and authored hard radios.

No EDB writes. The observed scalar profiles preserve rounded offsets only; they
are explicitly opt-in evidence profiles and do not claim recovered error intent.
Default banks sample nearby integer errors with variable numeric ranks, without
restricting valid IVPs to accommodate fixed misconception recipes.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, uuid, sys
sys.dont_write_bytecode=True
from math_format import normalize_prose,normalize_tex
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import sympy as sp

VERSION='1.2.1'
ROOT=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((ROOT/'source.json').read_text())
KP=SNAPSHOT['record']
LEVELS=('easy','moderate','hard')
TEMPLATES={'exhaust':'easy','coffee':'easy','iron':'easy','cake':'easy','compressor':'easy',
           'body':'easy','bulb':'easy','pork':'moderate','bath':'moderate','outside':'moderate','water':'moderate','tea':'moderate','two_observations':'hard'}
ORIGINALS={
 'q-107121':('body',dict(ambient=21,initial=40,rate='0.06',time=4)),
 'q-107123':('pork',dict(ambient=24,initial=150,observed=100,target=60,time=15)),
 'q-107128':('exhaust',dict(ambient=74,initial=140,rate='0.08',time=3)),
 'q-15595':('coffee',dict(ambient=25,initial=100,rate='0.05',time=6)),
 'q-107118':('iron',dict(ambient=28,initial=140,rate='0.1',time=5)),
 'q-107120':('cake',dict(ambient=70,initial=340,rate='0.09',time=8)),
 'q-107129':('compressor',dict(ambient=21,initial=65,rate='0.12',time=8)),
 'q-15384':('bath',dict(ambient=10,initial=50,observed=40,target=30,time=5)),
 'q-107122':('outside',dict(ambient=15,initial=72,observed=54,target=25,time=2)),
 'q-15589':('water',dict(ambient=25,initial=100,observed=90,target=30,time=5)),
 'q-107125':('tea',dict(ambient=28,initial=60,observed=52,target=40,time=10))}
SOURCE_Q={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
CONTEXT={'exhaust':('exhaust pipe of a motorcycle','exhaust pipe','F','Fahrenheit'),'coffee':('cup of coffee','coffee','C','Celsius'),'iron':('cooling iron','iron','C','Celsius'),
'body':('body','body','C','Celsius'),'bulb':('fluorescent light bulb after turning off','bulb','C','Celsius'),
'cake':('fresh-baked cake','cake','F','Fahrenheit'),'compressor':('compressor of a refrigerator','compressor','C','Celsius')}
BANKS={sid:[int(__import__('re').search(r'\d+',a[':answer/value']).group()) for a in q[':question/answer-fields'][0][':answer-field/choices']] for sid,q in SOURCE_Q.items()}

def rounded(x): return int(sp.floor(sp.N(x,35)+sp.Rational(1,2)))
def tex(x): return sp.latex(sp.sympify(x)).replace(r'\log',r'\ln')
def frac(n,d,reduce=True):
    return tex(sp.Rational(n,d)) if reduce else rf'\frac{{{n}}}{{{d}}}'
def block(s): return '\n\n$$\n'+s+'\n$$'
def aligned(rows): return block(r'\begin{aligned}'+' \\\\ '.join(rows)+r'\end{aligned}')
def dec(x):
    q=sp.Rational(str(x)); return str(float(q)).rstrip('0').rstrip('.')
def uid(value): return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(value,sort_keys=True,ensure_ascii=False)))
def fingerprint(value): return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def guard(level,p):
    """Bounds apply equally to explicit inputs and sampling; no silent clamping."""
    expected={'easy':{'ambient','initial','rate','time'},'moderate':{'ambient','initial','observed','target','time'},'hard':{'ambient','observed','later','target','start','gap'}}[level]
    if set(p)!=expected: raise ValueError('Exact parameter keys required: '+str(sorted(expected)))
    for key in expected-{'rate'}:
        if isinstance(p[key],bool) or not isinstance(p[key],int): raise ValueError(key+' must be an integer')
    A=p['ambient']
    if not 5<=A<=80: raise ValueError('Positive ambient 5..80 required')
    if level!='hard':
        if not 1<=p['time']<=15 or not A+15<=p['initial']<=400: raise ValueError('Initial/time scope violation')
    if level=='easy':
        k=sp.Rational(str(p['rate']))
        if not sp.Rational(1,50)<=k<=sp.Rational(1,4) or 100*k!=int(100*k): raise ValueError('Hundredth rate .02..25 required')
    elif level=='moderate':
        if not A<p['target']<p['observed']<p['initial']: raise ValueError('Cooling order must be ambient < target < observed < initial')
    else:
        # Nonzero start, unequal nonintegral start/gap ratio preserves extra work.
        if not 1<=p['start']<=6 or not 2<=p['gap']<=6 or p['start']%p['gap']==0: raise ValueError('Nonzero nonintegral start/gap ratio required')
        if not A<p['target']<p['later'] or not A+10<=p['later']<p['observed']<=180 or not 15<=p['observed']-A<=120: raise ValueError('Hard temperature bounds violated')
        if not sp.Rational(1,3)<=sp.Rational(p['later']-A,p['observed']-A)<=sp.Rational(4,5): raise ValueError('Hard excess ratio 1/3..4/5 required')
        k=-sp.log(sp.Rational(p['later']-A,p['observed']-A))/p['gap']
        if float(A+(p['observed']-A)*sp.exp(k*p['start']))>400: raise ValueError('Implied initial temperature too high')


def base_solution(A,initial,k,U):
    """Common exact separated/integrated/exponentiated/initial-constant stages."""
    D=initial-A
    solution='First, we integrate our differential equation by separating the variables:'
    integral=rf'-\int {k}\,\text{{d}}t' if k!='k' else r'-k\int dt'
    solution+=aligned([rf'\frac{{dT}}{{T-{A}}} & =-{k}\,dt',rf'\int \frac{{dT}}{{T-{A}}} & ={integral}',rf'\operatorname{{ln}}⁡|T-{A}| & =-{k}t+C'])
    solution+=f'\n\nSince this is the solution to an inhibited decay equation, we have $T-{A}>0$ for all $t>0.$\nNext, we solve for $T(t),$ as follows:'
    solution+=aligned([rf'T-{A} & ={{e}}^{{-{k}t+C}}',rf'T-{A} & ={{e}}^{{C}}{{e}}^{{-{k}t}}',rf'T-{A} & =K{{e}}^{{-{k}t}}',rf'T & ={A}+K{{e}}^{{-{k}t}}'])
    solution+='\n\nNote that $K={e}^{C}$ is a constant of integration. '
    return solution

# ============================================================================
# EASY: observed initial IVP with decimal rate, one positive-time evaluation.
# ============================================================================
def build_easy(template,p):
    A,I,t=p['ambient'],p['initial'],p['time']; k=dec(p['rate']); D=I-A
    obj,short,U,name=CONTEXT[template]
    solution_obj='fluorescent light bulb' if template=='bulb' else obj
    pronoun='its temperature' if template in ('iron','exhaust') else f'the temperature of the {short}'
    prompt=f'The temperature $T(t),$ in degrees {name}, of {'an' if template=='exhaust' else 'a'} {obj} can be modeled by the differential equation'
    prompt+=block(rf'\frac{{dT}}{{dt}}=-{k}(T-{A})')
    prompt+=f'\n\nwhere $t>0$ is the time, measured in minutes. If the initial temperature of the {short} is ${{{I}}}^{{∘}}{U},$ calculate {pronoun} after ${t}$ minutes. Round your answer to the nearest integer.'
    x=sp.Rational(str(k))*t; exact=A+D*sp.exp(-x); answer=rounded(exact)
    solution=f"We're told that the temperature of the {solution_obj} is modeled by the inhibited decay equation"+block(rf'\frac{{dT}}{{dt}}=-{k}(T-{A}).')
    solution+='\n\n'+base_solution(A,I,k,U)
    solution+=f"\n\nWe're told that the initial temperature of the {short} was ${{{I}}}^{{∘}}{U}.$ So, we apply the initial condition $T(0)={I},$ and solve for $K:$"
    solution+=aligned([rf'{I} & ={A}+K{{e}}^{{0}}',rf'{I} & ={A}+K',rf'K & ={D}'])
    solution+='\n\nTherefore, the solution to our initial value problem is'+block(rf'T(t)={A}+{D}{{e}}^{{-{k}t}}.')
    solution+=f'\n\nFinally, the temperature of the {short} after $t={t}$ minutes is'+block(rf'T({t})={A}+{D}{{e}}^{{-{k}\cdot {t}}}≈{{{answer}}}^{{∘}}\text{{{U}}},')+'\n\nrounded to the nearest integer.'
    values=[answer]
    return prompt,solution,answer,values,lambda n:rf'{{{n}}}^{{∘}}\text{{{U}}}'

# ============================================================================
# MODERATE: observed two conditions to determine k, then solve target-time log.
# Four source prose layouts are peers, with identical analytical workload.
# ============================================================================
def build_moderate(template,p,raw_units=False):
    A,I,O,Z,t=(p[x] for x in ('ambient','initial','observed','target','time')); D=I-A; R=O-A; Q=Z-A
    U='F' if template=='outside' else 'C'; name='Fahrenheit' if U=='F' else 'Celsius'
    if template=='bath':
        intro=f'A thermometer is placed into a water bath and displays a reading of ${{{I}}}^{{∘}}C.$ The thermometer is then transferred to a ${{{A}}}^{{∘}}C$ water bath, and its reading begins to decrease. After ${t}$ minutes, the thermometer reading is ${{{O}}}^{{∘}}C.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${{{Z}}}^{{∘}}C?$ '
        who='thermometer'; initial='initial temperature reading'; observed=f'the thermometer reading is ${{{O}}}^{{∘}}{U}.$'; target=f'the thermometer reads ${{{Z}}}^{{∘}}{U}.$'; final=f'the thermometer will read ${{{Z}}}^{{∘}}{U}$'; since=f'the thermometer was transferred into the ${{{A}}}^{{∘}}C$ water bath.'
    elif template=='outside':
        intro=f'A thermometer is taken out of a room where the air temperature is ${{{I}}}^{{∘}}F$  and brought outside where the temperature is ${{{A}}}^{{∘}}F,$ and its reading begins to decrease. After ${t}$ minutes, the thermometer reading is ${{{O}}}^{{∘}}F.$ To the nearest minute, how long does it take for the thermometer to register a reading of ${{{Z}}}^{{∘}}F?$ '
        who='thermometer'; initial='initial temperature reading'; observed=f'the thermometer reading is ${{{O}}}^{{∘}}'+('C' if raw_units else U)+'.$'; target=f'the thermometer reads ${{{Z}}}^{{∘}}{U}.$'; final=f'the thermometer will read ${{{Z}}}^{{∘}}'+('C' if raw_units else U)+'$'; since=f'the thermometer was transferred outside to ${{{A}}}^{{∘}}F.$'
    elif template=='pork':
        intro=f'A pork leg is taken out of the oven with a temperature of ${{{I}}}^{{∘}}C,$ and placed in a room that maintains a temperature of ${{{A}}}^{{∘}}C$, and its temperature begins to decrease. After ${t}$ minutes, the  temperature of the pork leg is ${{{O}}}^{{∘}}C.$ To the nearest minute, how long does it take for the pork leg to have a temperature of ${{{Z}}}^{{∘}}C?$ '
        who='pork leg'; initial='initial temperature of the pork leg'; observed=f'the temperature of the pork leg is ${{{O}}}^{{∘}}C.$'; target=f'the pork leg has a temperature of ${{{Z}}}^{{∘}}C.$'; final=f'the pork leg will have a temperature of ${{{Z}}}^{{∘}}C$'; since=f'the pork leg was transferred into the ${{{A}}}^{{∘}}C$ room.'
    elif template=='water':
        intro=f'The water boils in a pan at a temperature of ${{{I}}}^{{∘}}C.$ The pan with water is then placed to a room with a temperature of ${{{A}}}^{{∘}}C,$ and the temperature of water decreases. After ${t}$ minutes, it cools to ${{{O}}}^{{∘}}C.$ To the nearest minute, how long does it take for the water to have a temperature of ${{{Z}}}^{{∘}}C?$ '
        who='water in the pan'; initial='initial temperature'; observed=f'it cools to ${{{O}}}^{{∘}}C.$'; target=f'the water has a temperature of ${{{Z}}}^{{∘}}C.$'; final=f'the temperature of water will be ${{{Z}}}^{{∘}}C$'; since='the water starts cooling.'
    else:
        intro=f'Simon measures the temperature of the tea in his cup, and the thermometer displays a reading of ${{{I}}}^{{∘}}C.$ After ${t}$ minutes, Simon repeats the measurement and the thermometer displays a reading of  ${{{O}}}^{{∘}}C.$ To the nearest minute, how long does it take for the tea to decrease its temperature to ${{{Z}}}^{{∘}}C$ if the temperature in the room is ${{{A}}}^{{∘}}C?$ '
        who="tea in Simon's cup"; initial='initial temperature reading'; observed=f'the thermometer reading is ${{{O}}}^{{∘}}C.$'; target=f'the temperature of the tea is ${{{Z}}}^{{∘}}C.$'; final=f'the tea will have a temperature of ${{{Z}}}^{{∘}}C$'; since='the first measurement.'
    reading='temperature reading' if template!='tea' else 'temperature'
    prompt=intro+f"\n\n*Hint: You may assume that the {reading} $T(t)$ of the {who} decreases at a rate that obeys Newton's law of cooling, where $T$ is measured in degrees {name} and $t>0$ is the time, in minutes, since {since}*"
    # Source outside explicitly retains 39/57 instead of reducing 13/19.
    ratio=frac(R,D,template!='outside'); target_ratio=frac(Q,D,template!='outside')
    k=-sp.log(sp.Rational(R,D))/t; target_time=-sp.log(sp.Rational(Q,D))/k; answer=rounded(target_time)
    solution="Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation"+block(r'\frac{\text{d}T}{\text{d}t}=-k(T-{T}_{S}),')
    solution+='\n\nwhere ${T}_{S}$ is the temperature of the surroundings, and $k>0$ is a constant of proportionality.'
    solution+=f'\n\nIn our case, ${{T}}_{{S}}={{{A}}}^{{∘}}\\text{{'+('C' if raw_units and template=='outside' else U)+'},$ and we have'+block(rf'\frac{{\text{{d}}T}}{{\text{{d}}t}}=-k(T-{A}).')
    solution+='\n\n'+base_solution(A,I,'k',U)
    solution+=f"\n\nWe're told that the {initial} was ${{{I}}}^{{∘}}{U}.$ So, we apply the initial condition $T(0)={I},$ and solve for $K:$"
    solution+=aligned([rf'{I} & ={A}+K{{e}}^{{0}}',rf'{I} & ={A}+K',rf'K & ={D}'])
    solution+='\n\nTherefore, we have the following expression for $T(t):$'+block(rf'T(t)={A}+{D}{{e}}^{{-kt}}')
    solution+=f"\n\nWe're also told that, after ${t}$ minutes, {observed} So, applying the condition $T({t})={O},$ we can solve for $k:$"
    solution+=aligned([rf'{O} & ={A}+{D}{{e}}^{{-{t}k}}',rf'{R} & ={D}{{e}}^{{-{t}k}}',rf'{ratio} & ={{e}}^{{-{t}k}}',rf'\operatorname{{ln}}⁡({ratio}) & =-{t}k',rf'k & =-\frac{{1}}{{{t}}}\operatorname{{ln}}⁡({ratio})'])
    solution+=f'\n\nFinally, let ${{t}}_{{1}}$ be the time when {target} Then, we have'
    solution+=aligned([rf'T({{t}}_{{1}}) & ={Z}',rf'{A}+{D}{{e}}^{{-k{{t}}_{{1}}}} & ={Z}',rf'{D}{{e}}^{{-k{{t}}_{{1}}}} & ={Q}',rf'{{e}}^{{-k{{t}}_{{1}}}} & ={target_ratio}',rf'-k{{t}}_{{1}} & =\operatorname{{ln}}⁡({target_ratio})',rf'{{t}}_{{1}} & =-\frac{{1}}{{k}}\operatorname{{ln}}⁡({target_ratio}).'])
    solution+=f'\n\nSubstituting in our value for $k,$ we conclude that {final} after'+block(rf'{{t}}_{{1}}=\frac{{-\operatorname{{ln}}⁡({target_ratio})}}{{-\frac{{1}}{{{t}}}\operatorname{{ln}}⁡({ratio})}}≈{answer}\,\text{{min}},')+'\n\nrounded to the nearest minute.'
    values=[answer]
    return prompt,solution,answer,values,lambda n:rf'{n}\,\text{{min}}'

# ============================================================================
# HARD (authored; no observed hard label): target time from two
# nonzero-time observations. Same separation, logarithms, exponential constant.
# Nonintegral start/gap ratio requires a nontrivial exponential K; radio only.
# ============================================================================
def build_hard(p):
    A,O,L,Z,a,h=(p[x] for x in ('ambient','observed','later','target','start','gap')); b=a+h; D=O-A; R=L-A
    ratio=sp.Rational(R,D); k=-sp.log(ratio)/h; K=D*sp.exp(k*a)
    prompt=f'A heated metal body cools in a room at ${{{A}}}^{{∘}}\\text{{C}}.$ Its temperature is ${{{O}}}^{{∘}}\\text{{C}}$ after ${a}$ minutes and ${{{L}}}^{{∘}}\\text{{C}}$ after ${b}$ minutes. The temperature $T(t)$, in degrees Celsius, obeys Newton\'s law of cooling, with $t$ measured in minutes since cooling began. To the nearest minute, how long after cooling began does the body reach ${{{Z}}}^{{∘}}\\text{{C}}$?'
    solution="Newton's law of cooling states that the rate at which the temperature $T(t)$ of a body changes is proportional to the difference between its temperature and its surroundings. Therefore, we have the inhibited decay equation"+block(rf'\frac{{dT}}{{dt}}=-k(T-{A}),\qquad k>0.')
    solution+='\n\n'+base_solution(A,O,'k','C')
    solution+=f'\n\nApply the two observed conditions $T({a})={O}$ and $T({b})={L}$:'
    solution+=aligned([rf'{O} & ={A}+Ke^{{-{a}k}}',rf'{D} & =Ke^{{-{a}k}}',rf'{L} & ={A}+Ke^{{-{b}k}}',rf'{R} & =Ke^{{-{b}k}}'])
    solution+='\n\nDivide the excess temperatures to eliminate $K$, then take natural logarithms:'
    solution+=aligned([rf'\frac{{{R}}}{{{D}}} & =\frac{{Ke^{{-{b}k}}}}{{Ke^{{-{a}k}}}}',rf'{tex(ratio)} & =e^{{-{h}k}}',rf'\ln({tex(ratio)}) & =-{h}k',rf'k & ={tex(k)}'])
    solution+=f'\n\nNow substitute this rate into $T({a})={O}$ to determine the constant:'
    Ktex=rf'{D}\left(\frac{{{D}}}{{{R}}}\right)^{{{frac(a,h)}}}'
    solution+=aligned([rf'{D} & =Ke^{{-{a}({tex(k)})}}',rf'K & ={D}e^{{{a}({tex(k)})}}',rf'K & ={Ktex}'])
    model=A+K*sp.exp(-k*sp.Symbol('t'))
    solution+='\n\nTherefore, the solution satisfying both observations is'+block(rf'T(t)={A}+{Ktex}e^{{-({tex(k)})t}}.')
    solution+='\n\nSubstituting the two observation times confirms the model:'+aligned([rf'T({a}) & ={A}+({Ktex})e^{{-({tex(k)})\cdot {a}}}={O}',rf'T({b}) & ={A}+({Ktex})e^{{-({tex(k)})\cdot {b}}}={L}'])
    Q=Z-A
    elapsed=a+h*sp.log(sp.Rational(Q,D))/sp.log(ratio); answer=rounded(elapsed)
    solution+=f'\n\nFinally, let ${{t}}_{{1}}$ be the time when the body reaches ${{{Z}}}^{{∘}}\\text{{C}}.$ Then, we have'
    solution+=aligned([rf'T({{t}}_{{1}}) & ={Z}',rf'{A}+Ke^{{-k{{t}}_{{1}}}} & ={Z}',rf'Ke^{{-k{{t}}_{{1}}}} & ={Q}',rf'e^{{-k{{t}}_{{1}}}} & =\frac{{{Q}}}{{K}}',rf'-k{{t}}_{{1}} & =\ln\left(\frac{{{Q}}}{{K}}\right)',rf'{{t}}_{{1}} & =-\frac{{1}}{{k}}\ln\left(\frac{{{Q}}}{{K}}\right)'])
    solution+='\n\nSubstitute the values of $K$ and $k$ to obtain the time measured since cooling began:'+aligned([rf'{{t}}_{{1}} & =-\frac{{1}}{{{tex(k)}}}\ln\left(\frac{{{Q}}}{{{Ktex}}}\right)',rf'{{t}}_{{1}} & ={a}+{h}\frac{{\ln({tex(sp.Rational(Q,D))})}}{{\ln({tex(ratio)})}}≈{answer}\,\text{{min}}.'])
    values=[answer]
    return prompt,solution,answer,values,lambda n:rf'{n}\,\text{{min}}'


def sample(level,rng,template):
    if level=='easy':
        A=rng.randint(15,35) if template not in ('cake','exhaust') else rng.randint(60,80)
        I=rng.randint(A+15,A+35) if template=='body' else rng.randint(60,100) if template=='bulb' else rng.randint(70,100) if template=='coffee' else rng.randint(100,200) if template=='iron' else rng.randint(250,370) if template=='cake' else rng.randint(120,220) if template=='exhaust' else rng.randint(65,100)
        return dict(ambient=A,initial=I,rate=dec(sp.Rational(rng.randint(3,20),100)),time=rng.randint(3,12))
    if level=='moderate':
        A=rng.randint(10,35); I=rng.randint(120,190) if template=='pork' else 100 if template=='water' else rng.randint(max(50,A+35),90) if template=='outside' else rng.randint(A+35,100)
        O=rng.randint(A+20,I-5); Z=rng.randint(A+3,O-8)
        return dict(ambient=A,initial=I,observed=O,target=Z,time=rng.randint(2,12))
    A=rng.randint(10,35); D=rng.randint(40,100); R=rng.randint(math.ceil(D/3),math.floor(4*D/5))
    return dict(ambient=A,observed=A+D,later=A+R,target=A+rng.randint(2,max(3,R//3)),start=rng.randint(1,6),gap=rng.randint(2,6))


def integer_bank(level,p,correct,rng,desired_below):
    """A whole scalar-error profile, independent of named misconception ranks.

    Endpoint-inclusive bounds reflect rounding, not a restriction on the IVP.
    Adapt the eligible rank to integer room instead of resampling mathematical data.
    """
    if level=='easy':
        lo,hi=p['ambient'],p['initial']
    else:
        lo=p['time'] if level=='moderate' else p['start']+p['gap']
        hi=max(correct+4,correct+max(6,(correct-lo)//2))
    # Build the spacing independently of the key's rank. Centering four errors
    # around the key would leave a nearest-midpoint heuristic even with varied ranks.
    room=min(correct-lo,hi-correct)
    cap=max(1,min(6,room//4))
    gaps=[rng.randint(1,cap) for _ in range(4)]
    offsets=[0]
    for gap in gaps:
        offsets.append(offsets[-1]+gap)
    eligible=[n for n in range(5)
              if correct-offsets[n]>=lo and correct+offsets[-1]-offsets[n]<=hi]
    below=desired_below if desired_below in eligible else rng.choice(eligible)
    return [correct+offset-offsets[below] for offset in offsets]



def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS: raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only source-supported radio fields are available')
    if profile is not None and profile not in SOURCE_Q: raise ValueError('Unknown explicit observed bank profile')
    if profile:
        implied=ORIGINALS[profile][0]
        if template and template!=implied: raise ValueError('Profile/template mismatch')
        template=implied
    rng=random.Random(seed)
    template=template or rng.choice([n for n,l in TEMPLATES.items() if l==level])
    if TEMPLATES.get(template)!=level: raise ValueError('Template difficulty mismatch')
    desired_below=rng.randrange(5)
    if profile and parameters is None:
        parameters=ORIGINALS[profile][1]
    for attempt in range(1000):
        p=dict(parameters) if parameters is not None else sample(level,rng,template)
        try:
            guard(level,p)
            if template=='water' and p['initial']!=100: raise ValueError('Boiling Celsius water requires initial 100')
            if template in ('coffee','tea','bath') and p['initial']>100: raise ValueError('Ordinary liquid Celsius temperature cannot exceed 100')
            if template=='outside' and not 50<=p['initial']<=90: raise ValueError('Ordinary room air initial temperature must be 50..90 Fahrenheit')
            if template=='compressor' and p['initial']>140: raise ValueError('Compressor context bound 140 Celsius')
            if template=='cake' and not 180<=p['initial']<=400: raise ValueError('Fresh baked Fahrenheit cake context bound')
            if level=='easy': prompt,solution,correct,values,render=build_easy(template,p)
            elif level=='moderate': prompt,solution,correct,values,render=build_moderate(template,p)
            else: prompt,solution,correct,values,render=build_hard(p)
            if profile:
                source_correct=int(__import__('re').search(r'\d+',SOURCE_Q[profile][':question/answer-fields'][0][':answer-field/correct'][':answer/value']).group())
                offsets=[v-source_correct for v in BANKS[profile]]
                values=[correct+delta for delta in offsets]
            else:
                values=integer_bank(level,p,correct,rng,desired_below)
            if len(set(values))!=5 or values.count(correct)!=1:
                raise ValueError('Bank must have five distinct integers and one correct value')
            break
        except ValueError:
            if parameters is not None: raise
    else: raise ValueError('No eligible complete bank after bounded sampling')
    prompt=prompt.replace('after $1$ minutes','after $1$ minute')
    solution=solution.replace('after $1$ minutes','after $1$ minute').replace('after $t=1$ minutes','after $t=1$ minute')
    # Math identity deliberately excludes layout/profile/options; unit scale belongs to task.
    mathematical={'level':level,'parameters':{k:str(sp.Rational(str(v))) if k=='rate' else v for k,v in p.items()}}
    if level=='easy': mathematical['parameters']['unit']='F' if template in ('cake','exhaust') else 'C'
    if level=='moderate': mathematical['parameters']['unit']='F' if template=='outside' else 'C'
    bank=[render(v) for v in values]; right=render(correct)
    prompt=normalize_prose(prompt);solution=normalize_prose(solution);bank=[normalize_tex(v)for v in bank];right=normalize_tex(right)
    content={'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'bank':sorted(bank),'correct':right}
    identity=uid(content); fid=uid([identity,'selection'])
    choices=[{':answer/id':uid([fid,value]),':answer/type':':answer.type/math',':answer/value':value} for value in bank]
    rng.shuffle(choices)
    question={':question/id':identity,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid([fid,right])]}]}
    return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile or 'authored_local_integers','origin':'authored_hard' if level=='hard' else 'observed_template','bank_origin':'observed_scalar_offsets_intent_underdetermined' if profile else 'authored_local_integers','source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'mathematical_fingerprint':fingerprint(mathematical),'content_fingerprint':fingerprint(content),'domain':'T(t)>ambient; positive rate; t>=0; observations strictly cooling','attempts':attempt+1,'source_refs':[SOURCE_Q[sid][':question/id'] for sid,(context,_) in ORIGINALS.items() if context==template] or [KP[':knowledge-point/canonical-example'][':question/id']],'recipes':['correct']+['rounded_correct_plus_'+str(v-correct) for v in values if v!=correct] if not profile else ['rounded_correct_plus_'+str(v-correct) for v in values]}}


def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Observed known-rate initial IVP, decimal rate and rounded temperature."""
    return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Observed rate calibration from initial/later readings, then target time."""
    return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Authored calibrated target time from two nonzero-time observations."""
    return generate('hard',seed,template,field_type,parameters,profile)


def markdown(r):
    q=r['question']; f=q[':question/answer-fields'][0]
    text=q[':question/problem']+'\n\n'
    for a in f[':answer-field/choices']: text+='- $'+a[':answer/value']+'$'+(' **(correct)**' if a[':answer/id']==f[':answer-field/correct'][1] else '')+'\n'
    return text+'\n**Worked solution**\n\n'+q[':question/worked-solution']

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['all',*LEVELS],default='all'); parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--count',type=int,default=1); parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    parser.add_argument('--template',choices=TEMPLATES); parser.add_argument('--profile',choices=SOURCE_Q)
    args=parser.parse_args()
    if args.count<1 or args.difficulty=='all' and (args.template or args.profile): parser.error('Positive count and specific level with template/profile required')
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in LEVELS if args.difficulty in ('all',l) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
