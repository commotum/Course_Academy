#!/usr/bin/env python3
"""Seeded real-domain practice. Runtime is self-contained and standard-library only."""
import argparse
import hashlib
import json
import math
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = 17592186124640
NS = uuid.UUID('88f2bc84-03e8-5921-81e2-683a09195279')
FAMILIES = {'easy': ['polynomial', 'rational', 'radical'],
            'moderate': ['log_den', 'reciprocal_log', 'log_exp', 'log_interval', 'log_root'],
            'hard': ['inverse', 'inverse_root', 'inverse_reciprocal']}
SOURCES = {'polynomial': ['q-158438','q-158573','q-158566','q-158569'],
           'rational':['q-158567'], 'radical':['q-158565'],
           'log_den':['q-158180','q-158186'], 'reciprocal_log':['q-158577','q-158183'],
           'log_exp':['q-158185'], 'log_interval':['q-158191'], 'log_root':['e-11029'],
           'inverse':['q-158181','q-158580'], 'inverse_root':['q-158589'],
           'inverse_reciprocal':['q-158583']}

def uid(s):
    return str(uuid.uuid5(NS, s))

def linear(a, b, c=0, squared=False):
    parts=[]
    for coefficient, variable in [(a, 'x'), (b, 'y')]:
        if not coefficient: continue
        body = variable + ('^{2}' if squared and variable == 'x' else '')
        term = (str(abs(coefficient)) if abs(coefficient)!=1 else '') + body
        parts.append(('-' if coefficient<0 else ('+' if parts else '')) + term)
    if c: parts.append(('+' if c>0 and parts else '')+str(c))
    return ''.join(parts) or '0'

def shifted(variable, c):
    return variable + (('+' if c>0 else '')+str(c) if c else '')

def domain(conditions):
    if not conditions: return r'\mathbb{R}^{2}'
    if len(conditions)>1:
        return r'\left\{(x,y)\in\mathbb{R}^{2}:\,\begin{aligned}' + r' \\ '.join('&'+c for c in conditions) + r'\end{aligned}\right\}'
    return r'\{(x,y)\in\mathbb{R}^{2}:\,' + conditions[0] + r'\}'

def outer(name, argument):
    if name == 'exp': return 'e^{'+argument+'}'
    if name == 'two': return '2^{'+argument+'}'
    return '\\'+name+r'\left('+argument+r'\right)'

def make_instance(family, p):
    """Ordered derivation and candidate error domains from a shared instance."""
    u, v, w = p['u'], p['v'], p['w']
    op=p.get('op','exp'); power=p.get('power',1); numerator=p.get('numerator','1')
    zero=v+r'\ne 0'; pos=u+'>0'; nonneg=u+r'\ge 0'
    allplane=[]
    steps=[]; conversions=[]
    if family=='polynomial':
        expr=outer(op,u); correct=[]
        steps=[f'The polynomial ${u}$ is defined for every real pair. The outer function is defined for every real input, so it adds no restriction.']
        errors=[[pos],[u+r'\ne 0'],[u+'<1'],[u+'>1'],[u+'=0'],[u+'<0']]
        if p.get('nonnegative_polynomial'):
            # For a sum of squares, >0 and !=0 are equivalent. Keep only one.
            errors=[[pos],[u+'<1'],[u+'>1'],[u+'=0'],[u+r'<2\pi']]
    elif family=='rational':
        arg=r'\frac{'+u+'}{'+v+'}';expr=outer(op,arg);correct=[zero]
        steps=[f'The inner quotient requires ${zero}$. The outer function is defined for every real input and adds no further restriction.']
        errors=[[],[v+'>0'],[v+r'\ge 0'],[u+r'\ne 0'],[v+'<0'],[zero,u+r'\ne 0']]
    elif family=='radical':
        expr=outer(op,(p.get('root_sum','')+'+' if p.get('root_sum') else '')+r'\sqrt{'+u+'}');correct=[nonneg]
        steps=[f'The square root requires ${nonneg}$. The outer function is defined for every real input and adds no further restriction.']
        errors=[[],[pos],[u+r'\ne 0'],[u+'<0'],[r'0\le '+u+r'\le 1']]
    elif family in ('log_den','log_interval','log_exp','log_root'):
        log=r'\ln\left('+u+r'\right)'
        if power==2: log=r'\left('+log+r'\right)^{2}'
        den=v if power!=2 else r'\left('+v+r'\right)^{3}'
        if family=='log_exp': den=outer('exp',v)
        if family=='log_root': den=r'\sqrt{'+v+'}'
        expr=r'\frac{'+log+'}{'+den+'}'
        correct=[pos]
        steps=[f'The logarithm requires ${pos}$.']
        if family=='log_exp':
            steps += [f'The denominator ${den}$ is positive for every real input, so it never vanishes.']
            errors=[[],[u+r'\ne 0'],[u+r'\ge 0'],[pos,zero],[u+r'\ne 0',zero],[pos,u+r'\ne 1']]
        else:
            restriction=v+'>0' if family=='log_root' else zero
            correct += [restriction]
            if family=='log_root':
                steps += [f'The denominator square root requires both ${v}'+r'\ge 0$ and $\sqrt{'+v+r'}\ne 0$. Together these give $'+restriction+'$.']
                conversions=['nonnegative radicand and nonzero square root give positive radicand']
                errors=[[pos],[u+r'\ge 0',restriction],[pos,v+r'\ge 0'],[pos,zero],[u+r'\ne 0',restriction],[pos,restriction,u+r'\ne 1']]
            else:
                steps += [f'The denominator must be nonzero, so ${restriction}$.']
                errors=[[pos],[u+r'\ge 0',zero],[pos,v+'>0'],[u+r'\ne 0',zero],[],[pos,zero,u+r'\ne 1']]
    elif family=='reciprocal_log':
        expr=r'\frac{'+numerator+r'}{\ln\left('+u+r'\right)}'
        correct=[pos,u+r'\ne 1']
        steps=[f'The logarithm requires ${pos}$. Its value is a denominator, so it must also be nonzero.',
               f'On positive inputs, $'+r'\ln\left('+u+r'\right)=0$ exactly when $'+u+'=1$. Thus we must exclude $'+u+'=1$, even when the numerator is zero.']
        conversions=['logarithm zero exactly at argument one']
        errors=[[pos],[u+r'\ne 0',u+r'\ne 1'],[u+'>1'],[],[u+r'\ge 0',u+r'\ne 1']]
    else:
        if family=='inverse': arg=u; inner=[];inner_step='The inner polynomial is defined everywhere.'
        elif family=='inverse_root':
            arg=w+r'+\sqrt{'+v+'}';inner=[v+r'\ge 0'];inner_step=f'The inner square root requires ${inner[0]}$.'
        else:
            arg=r'\frac{1}{'+v+'}';inner=[zero];inner_step=f'The inner quotient requires ${zero}$.'
        expr=outer(op,arg)
        closed=r'-1\le '+arg+r'\le 1';strict='-1<'+arg+'<1'
        correct=[closed]+inner
        steps=[inner_step, f'The input of $\\{op}$ must lie in the closed interval $[-1,1]$, including both endpoints. Therefore ${closed}$.']
        range1=r'0\le '+arg+r'\le \pi';range2=r'-\frac{\pi}{2}\le '+arg+r'\le \frac{\pi}{2}'
        errors=[[strict]+inner,[range1]+inner,[range2]+inner,[],[closed]+inner+[(('x' if family=='inverse' else w))+r'\ne 0']]
        if family=='inverse': errors += [[closed,w+'>0'],[arg+r'\ne 0']]
        if family=='inverse_root': errors += [[closed,v+'>0'],[r'-1\le '+w+'+'+v+r'\le 1']+inner]
        if family=='inverse_reciprocal': errors += [[zero],[r'0<'+arg+r'\le 1',zero]]
    return {'expression':expr, 'correct':correct, 'errors':errors, 'steps':steps, 'conversions':conversions}


def samples(rng, family):
    # All affine denominator/radicand slots are surjective; shifts change real boundaries.
    a,b=rng.choice([-2,-1,1,2]),rng.choice([-2,-1,1,2]); c=rng.choice([-2,-1,0,1,2])
    coordinate=rng.choice(['x','y']);other='y' if coordinate=='x' else 'x'
    v=shifted(coordinate,rng.choice([-2,-1,0,1,2]));w=other
    if family in ('radical','log_exp','log_root','inverse_reciprocal'): u=linear(a,b,c)
    elif family=='log_interval': u=str(rng.choice([1,4,9]))+'-'+other+'^{2}'
    elif family=='log_den': u=linear(a,b,c) if rng.randrange(2) else shifted(other,c)
    elif family=='rational':u=other+'^{2}'
    else:u=rng.choice([linear(a,b,c),linear(a,b,c,True),'x^{2}-y^{2}','-x^{3}y'])
    if family=='inverse_reciprocal':v=linear(a,b,c)
    if family=='inverse_root':v=shifted(coordinate,c)
    nonnegative=False
    if family=='polynomial' and rng.randrange(4)==0:
        u=rng.choice(['x^{2}+y^{2}','2x^{2}+y^{2}','x^{2}+2y^{2}']);nonnegative=True
    op=rng.choice(['arcsin','arccos']) if family.startswith('inverse') else rng.choice(['exp','two','sin','cos'])
    return {'u':u,'v':v,'w':w,'op':op,'power':rng.choice([1,2]) if family=='log_den' else 1,
            'numerator':rng.choice(['1','x^{3}','y^{2}']),
            'root_sum':other if family=='radical' and rng.randrange(2) else '',
            'nonnegative_polynomial':nonnegative}


def record(family, p, difficulty, rng):
    d=make_instance(family,p)
    correct=normalize_tex(domain(d['correct']))
    # Select complete plausible profiles. No source's duplicate/implicit-domain bank is copied.
    errors=[]
    for conditions in d['errors']:
        value=normalize_tex(domain(conditions))
        if value!=correct and value not in errors: errors.append(value)
    rng.shuffle(errors)
    values=[correct]+errors[:4]
    if len(values)!=5: raise ValueError('Insufficient distinct alternatives')
    rng.shuffle(values)
    problem=normalize_prose('Find the domain of the function $f(x,y)='+d['expression']+'.$')
    rows=r' \\ '.join(condition for condition in d['correct'])
    solution='\n\n'.join(d['steps'])
    if rows:
        solution+='\n\nIntersecting these conditions gives\n\n$$\n'+r'\begin{aligned}'+rows+r'\end{aligned}'+'\n$$'
    solution+='\n\nTherefore, the domain is\n\n$$\n'+correct+'.\n$$'
    solution=normalize_prose(solution)
    identity=json.dumps([problem,sorted(values),correct],ensure_ascii=False,sort_keys=True)
    qid=uid('question:'+identity)
    choices=[{':answer/id':uid(qid+':'+val),':answer/type':':answer.type/math',':answer/value':val} for val in values]
    q={':question/id':qid, ':question/difficulty':':question.difficulty/'+difficulty,
       ':question/problem':problem, ':question/worked-solution':solution,
       ':question/answer-fields':[{':answer-field/id':uid(qid+':selection'), ':answer-field/key':'selection',
        ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices,
        ':answer-field/correct':[':answer/id',uid(qid+':'+correct)]}]}
    r={'knowledge_point':{'db_id':KP,'id':str(NS)},'question':q,
       'generation':{'family':family,'parameters':p,'sources':SOURCES[family], 'conversions':d['conversions']}}
    return validate_generated_record(r)


def generate(difficulty,count,seed):
    rng=random.Random(seed);families=list(FAMILIES[difficulty]);out=[];seen=set();attempts=0
    while len(out)<count:
        if len(out)%len(families)==0:rng.shuffle(families)
        family=families[len(out)%len(families)]
        attempts+=1
        if attempts>count*100+100:raise ValueError('Exhausted unique semantic instances')
        p=samples(rng,family)
        # Constraints above keep inner slots independent; visible-bank validation checks witnesses.
        r=record(family,p,difficulty,rng)
        # Prompt-based dedup prevents merely shuffled banks from masquerading as new exercises.
        fingerprint=r['question'][':question/problem']
        if fingerprint in seen:continue
        seen.add(fingerprint);out.append(r)
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json')
    a=p.parse_args()
    if a.count<0:p.error('--count must be nonnegative')
    print(json.dumps(generate('moderate' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed),ensure_ascii=False))
if __name__=='__main__':main()
