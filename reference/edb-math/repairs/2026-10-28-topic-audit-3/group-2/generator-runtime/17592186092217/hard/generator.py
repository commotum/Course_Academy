#!/usr/bin/env python3
"""Relocatable seeded direct polar-to-Cartesian generator. No external state."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186092217,'id':'7f65d032-9acc-5fe6-b7c2-b8293576cb4c',
      'title':'Finding the Cartesian Coordinates of a Point Given in Polar Coordinates'}
VERSION = 'polar-projections-2.0'
K = sp.Symbol('k', positive=True)
# These are the learner's retrieved unit-circle values, not a CAS-selected route.
H=sp.Rational(1,2); A=sp.sqrt(3)/2; B=sp.sqrt(2)/2
UNIT = {0:(1,0),30:(A,H),45:(B,B),60:(H,A),90:(0,1),120:(-H,A),
        135:(-B,B),150:(-A,H),180:(-1,0),210:(-A,-H),225:(-B,-B),
        240:(-H,-A),270:(0,-1),300:(H,-A),315:(B,-B),330:(A,-H)}
ANGLES={'easy':(0,30,45,60,90,180,270),'moderate':(120,135,150,210,225,240,300,315,330),
        'hard':tuple(d for d in UNIT if d%90)}
SUPPORT=['0c11e98f-8b92-5ed1-bfd7-cca35a6dd373','bc48e845-b2a7-5e30-9c73-b7d842f4090c',
         '17592186048292','17592186048465']

def tex(x):
    return normalize_tex(sp.latex(sp.expand(x)))

def coordinates(radius, degrees):
    c,s=UNIT[degrees]
    return tuple(sp.expand(radius*t) for t in (c,s))

def pair(xy):
    return r'\left('+tex(xy[0])+','+tex(xy[1])+r'\right)'

def angle_tex(degrees,unit):
    return str(degrees)+r'^{\circ}' if unit=='degrees' else tex(sp.Rational(degrees,180)*sp.pi)

def uid(*x):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'ca:polar:v2:'+':'.join(map(str,x))))

def source_cases():
    return json.loads(Path(__file__).with_name('source-cases.json').read_text())

def make(level, radius, degrees, unit, response, seed=0, bank_angles=None, source=None, bank_scales=None):
    """One projection instance owns the prompt, all steps and both key components."""
    radius=sp.sympify(radius,locals={'k':K})
    if degrees not in UNIT or radius.is_positive is not True:
        raise ValueError('positive radius and familiar exact angle required')
    if unit not in ('degrees','radians') or response not in ('blank','radio'):
        raise ValueError('unknown response or angle unit')
    xy=coordinates(radius,degrees); at=angle_tex(degrees,unit); rt=tex(radius)
    symbolic=bool(radius.free_symbols)
    prompt='The point $P$ has polar coordinates $'+r'\left('+rt+','+at+r'\right)'+'$.'
    if symbolic:prompt+=' Here $k$ is a positive real number.'
    prompt+=' Find the exact Cartesian coordinates of $P$'+(' in terms of $k$.' if symbolic else '.')
    if response=='blank':prompt+='\n\nThe Cartesian coordinates are\n\n$(${{field-1}}$,$ {{field-2}}$)$.'
    solution='To convert from polar coordinates to Cartesian coordinates, use\n\n$$\nx=r\\cos\\theta,\\qquad y=r\\sin\\theta.\n$$'
    for name,fn,t,result in zip(('x','y'),('cos','sin'),UNIT[degrees],xy):
        solution+='\n\n'+('First' if name=='x' else 'Then')+' calculate the $'+name+'$-coordinate:\n\n$$\n'+r'\begin{aligned}'+'\n'
        solution+=name+'&='+rt+'\\'+fn+r'\left('+at+r'\right)'+r'\\'+'\n'
        solution+=' &='+rt+r'\left('+tex(t)+r'\right)'+r'\\'+'\n'
        solution+=' &='+tex(result)+'.\n'+r'\end{aligned}'+'\n$$'
    solution+='\n\nTherefore, the Cartesian coordinates are $'+pair(xy)+'$.'
    if source and source['source_name']=='exemplar-easy':
        solution+='\n\nThe lesson triangle explains the two projections.\n\n![](images/20/205b3684042b0ab0261a4d56800cd89a10a7816f8022befcf6c664337f834380.png)'
    field_specs=[]
    if response=='radio':
        if source:
            f=source['question'][':question/answer-fields'][0]
            values=[normalize_tex(a[':answer/value']) for a in f[':answer-field/choices']]
            correct=normalize_tex(f[':answer-field/correct'][':answer/value'])
        else:
            if bank_angles is None or len(bank_angles)!=5 or degrees not in bank_angles or len(set(bank_angles))!=5:
                raise ValueError('a complete five-angle bank containing the target is required')
            scales=bank_scales or [1]*5
            if len(scales)!=5 or scales[bank_angles.index(degrees)]!=1:raise ValueError('target must retain the supplied radius')
            values=[pair(coordinates(radius*scale,d)) for d,scale in zip(bank_angles,scales)];correct=pair(xy)
        random.Random(seed).shuffle(values)
        field_specs=[('selection',values,correct)]
    else:field_specs=[('field-1',[tex(xy[0])],tex(xy[0])),('field-2',[tex(xy[1])],tex(xy[1]))]
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    identity=hashlib.sha256(json.dumps([level,prompt,solution,field_specs],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    qid=uid(identity);fields=[]
    for key,values,correct in field_specs:
        fid=uid(qid,key)
        choices=[{':answer/id':uid(fid,v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+response,
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid,correct)]})
    q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,
       ':question/worked-solution':solution,':question/answer-fields':fields}
    record={'knowledge_point':dict(KP),'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,
        'template':('symbolic-' if symbolic else 'numeric-')+response,'profile':('source-'+source['source_name'] if source else 'coordinate-production' if response=='blank' else 'two-quadrant-projections-with-scale-error' if bank_scales else 'two-quadrant-projections'),
        'parameters':{'radius':str(radius),'degrees':degrees,'unit':unit},'bank_angles':bank_angles,'bank_scales':[str(v) for v in bank_scales] if bank_scales else None,
        'source_ids':[source['source_id']] if source else SUPPORT+(['ab27e4c8-0620-540c-9f5a-41d839c0c6f0'] if symbolic else []),
        'semantic_instance':[str(radius),degrees,response], 'domain':'positive radius; exact familiar angle; k>0 when present',
        'derivation':{'operator_inputs':{'cos':at,'sin':at},'trig_values':[tex(v) for v in UNIT[degrees]],
                      'products':[[rt,tex(t)] for t in UNIT[degrees]],'final_components':[tex(v) for v in xy],
                      'conversions':['exact unit-circle evaluation','distributive multiplication and square-root products']}}}
    validate_generated_record(record)
    return record

def bank_for(degrees,rng):
    # Choose a complete same-sign-count profile, then fill it; no pooled recipes.
    quadrant=degrees//90
    same=[d for d in UNIT if d%90 and d//90==quadrant and d!=degrees]
    count=rng.choice((2,3))
    other_q=rng.choice([q for q in range(4) if q!=quadrant])
    other=[d for d in UNIT if d%90 and d//90==other_q]
    return [degrees]+rng.sample(same,count-1)+rng.sample(other,5-count)

def generate_batch(difficulty,count,seed):
    level='moderate' if difficulty=='unclassified' else difficulty
    if level not in ANGLES or count<0:raise ValueError('invalid difficulty or count')
    rng=random.Random(seed);records=[];seen=set();seen_work=set();schedule=[]
    for i in range(count):
        if not schedule:
            schedule=list(ANGLES[level]);rng.shuffle(schedule)
        d=schedule.pop()
        # Batch role scheduling prevents repeated main angle calculations in a short batch.
        for _ in range(500):
            unit=rng.choice(('degrees','radians'))
            response='blank' if level=='hard' or not d%90 else ('radio' if level=='moderate' else rng.choice(('blank','radio')))
            if level=='hard':
                coefficient=rng.choice((1,2,3,4))
                root=(2 if d%90==45 else 3) if rng.choice((False,True)) else 1
                radius=coefficient*sp.sqrt(root)*K
            else:radius=sp.Integer(rng.choice((1,2,3,4,5,6,7,8,9,10,11,12)))
            semantic=(str(radius),d) # units and choice order never count as fresh mathematics.
            work=tuple(sorted(str(sp.simplify(abs(v))) for v in coordinates(radius,d)))
            if semantic not in seen and work not in seen_work:break
        else:raise ValueError('requested batch exceeds finite semantic capacity')
        seen.add(semantic);seen_work.add(work)
        bank=bank_for(d,rng) if response=='radio' else None
        scales=None
        if bank:
            # Source-supported loss/addition of the common factor 1/2. Keep
            # at least two correctly scaled options in the target quadrant.
            scales=[1]*5
            same_count=sum(v//90==d//90 for v in bank)
            eligible=[j for j in range(1,5) if bank[j]//90!=d//90 or same_count==3]
            scales[rng.choice(eligible)]=rng.choice((sp.Rational(1,2),sp.Integer(2)))
        records.append(make(level,radius,d,unit,response,rng.getrandbits(63),bank,bank_scales=scales))
    return records

def replay(case):
    response=case['question'][':question/answer-fields'][0][':answer-field/type'][':db/ident'].rsplit('/',1)[1]
    return make(case['difficulty'],case['radius'],case['degrees'],case['unit'],response,source=case)

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json')
    p.add_argument('--replay-source',action='store_true');a=p.parse_args()
    records=[replay(c) for c in source_cases()] if a.replay_source else generate_batch(a.difficulty,a.count,a.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
