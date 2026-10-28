#!/usr/bin/env python3
"""Seeded IVP identification: source constant fitting and joint verification.

All runtime files are package-local. No services, database, or assets are used.
"""
import argparse
import copy
import hashlib
import itertools
import json
import random
import re
import uuid
import sympy as sp
import legacy_easy as easy
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = 'ivp-constant-5'
X = easy.X
TEX = easy.tex
KP = {'db_id': easy.KP_ID, 'id': easy.KP_UUID, 'title': easy.TITLE}
BANDS = ('easy', 'moderate', 'hard')
EASY_TEMPLATES = tuple(k for k,v in easy.TEMPLATES.items() if v['level']=='easy' and k not in ('q-141055','q-141117'))
SHAPE = ((0,0),(0,1),(1,0),(1,1),(2,0))

def uid(s):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, s))

def finalize(record):
    """Normalize before deriving the public identities, including owned answers."""
    r=copy.deepcopy(record);q=r['question']
    q[':question/problem']=normalize_prose(q[':question/problem'])
    q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
    for f in q[':question/answer-fields']:
        old=f[':answer-field/correct'][1]
        key=next(a for a in f[':answer-field/choices'] if a[':answer/id']==old)
        for a in f[':answer-field/choices']:
            a[':answer/value']=normalize_tex(a[':answer/value'])
        f['_correct_value']=key[':answer/value']
    payload=[q[':question/problem'],q[':question/worked-solution'],q[':question/difficulty'],
             [(f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),f['_correct_value']) for f in q[':question/answer-fields']]]
    h=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    q[':question/id']=uid(h)
    for f in q[':question/answer-fields']:
        f[':answer-field/id']=uid(h+'/'+f[':answer-field/key'])
        cv=f.pop('_correct_value')
        for a in f[':answer-field/choices']:
            a[':answer/id']=uid(f[':answer-field/id']+'/'+a[':answer/value'])
            if a[':answer/value']==cv:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
    r['generation'].update(version=VERSION,content_hash=h)
    return validate_generated_record(r)

def easy_record(seed, template=None, parameters=None, replay=False):
    rng=random.Random(seed)
    template=template or rng.choice(EASY_TEMPLATES)
    if replay:
        parameters=parameters or easy.source_parameters(template)
    r=easy.generate('easy',seed,template=template,parameters=parameters,
                    profile='observed:'+template if replay else None)
    if replay and ':question/worked-solution' not in r['question']:
        raise ValueError('partial imports are not complete replay cases')
    q=r['question'];g=r['generation'];p=g['parameters'];f=easy.TEMPLATES[template]['family']
    # Remove source operator typos even in normalized replay (stored source unchanged).
    for k in (':question/problem',':question/worked-solution'):
        q[k]=q[k].replace('\u2061','').replace('Asin',r'A\sin').replace('Acos',r'A\cos')
    if not replay:
        domain=g['domain']
        if f in ('power','invpower'):
            domain='x>0' if sp.sympify(p['u'])>0 else 'x<0'
            interval=' on $'+domain+'$'
        elif f=='recip':
            domain=r'A'+('+' if sp.sympify(p['k'])>0 else '-')+r'x\ne0'
            interval=' on the interval containing the initial point where $'+domain+'$'
        elif f=='log':
            domain='A+x>0'; interval=' on the interval where $'+domain+'$'
        elif f in ('sin','cos'):
            domain=(r'\sin' if f=='sin' else r'\cos')+'('+easy.coeff(sp.sympify(p['k']),'x')+r')\ne0'
            interval=' on the interval containing the initial point where $'+domain+'$'
        else:interval=' for all real $x$'
        q[':question/problem']=q[':question/problem'].replace('initial value problem\n','initial value problem'+interval+'\n',1)
        # Build final form by substituting A into the already displayed supplied family.
        parts,a=easy.components(template,f,{k:easy.exact(v) for k,v in p.items()},normal=True)
        staged=re.search(r'A\s*&\s*=(.*?)\.\s*\\end\{aligned\}',parts['stages'],re.S)
        staged_value=staged[1].strip() if staged else TEX(a)
        if f=='exp' and normalize_tex(staged_value).replace(' ','')!=normalize_tex(TEX(a)).replace(' ',''):
            q[':question/worked-solution']+='\n\nUsing the exponent rule to rewrite the same constant,\n\n$$\nA='+staged_value+'='+TEX(a)+'.\n$$'
            g['necessary_conversions']=[{'from':staged_value,'to':TEX(a),'support':'source q-352655 and q-352656 exponent isolation'}]
        form=parts['given'].split('=',1)[1].replace('A','('+TEX(a)+')')
        q[':question/worked-solution']+='\n\nTherefore, the solution is $y='+form+'$ on the stated interval.'
    g.update(source={'database':'math','basis':7119,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},family=f)
    return finalize(r)


# Constant fitting throughout: family guarantee and exact A response are fixed.
# Labels are an authored relative progression; imported easy coverage is unchanged.
FAMILIES = {'easy': ('power','exp','sin'),
            'moderate': ('power','invpower','exp','sin','cos'),
            'hard': ('recip','log')}

def sample_parameters(level,family,rng):
    b=rng.choice([-3,-2,-1,0,1,2,3])
    if level=='easy':
        if family=='power': return dict(k=rng.choice([1,2,3,4]),u=rng.choice([-1,1]),b=b)
        if family=='exp': return dict(k=rng.choice([-3,-2,-1,1,2,3]),u=0,b=b)
        k=rng.choice([1,2,3]);return dict(k=k,u=sp.pi/(2*k),b=b)
    if level=='moderate':
        if family in ('power','invpower'):return dict(k=rng.choice([2,3]),u=rng.choice([-2,2]),b=b)
        if family=='exp':return dict(k=rng.choice([-2,-1,1,2]),u=rng.choice([-1,1]),b=b)
        k=rng.choice([1,2,3]);angle=rng.choice([sp.pi/6,sp.pi/4,sp.pi/3,2*sp.pi/3,3*sp.pi/4])
        return dict(k=k,u=angle/k,b=b)
    if family=='recip':return dict(k=rng.choice([-1,1]),u=rng.choice([-2,-1,1,2]),b=rng.choice([-3,-2,-1,1,2,3]))
    return dict(k=1,u=rng.choice([-2,-1,1,2]),b=rng.choice([-2,-1,1,2]))

def normal_record(level,seed,family=None,parameters=None):
    if level not in BANDS:raise ValueError('unsupported difficulty')
    rng=random.Random(seed);family=family or rng.choice(FAMILIES[level])
    if family not in FAMILIES[level]:raise ValueError('family outside band')
    p={key:easy.exact(value) for key,value in (parameters or sample_parameters(level,family,rng)).items()}
    if set(p)!={'k','u','b'}:raise ValueError('parameters require k,u,b')
    k,u,b=(p[z] for z in ('k','u','b'))
    if not k.is_Integer or k==0 or abs(k)>4 or not b.is_Rational or abs(b)>8 or b.q>4:raise ValueError('finite workload bounds')
    if family not in ('sin','cos') and (not u.is_Rational or abs(u)>3 or u.q>2):raise ValueError('input bounds')
    if family in ('power','invpower') and (k<1 or u==0):raise ValueError('nonzero power input required')
    if family=='recip' and (k not in (-1,1) or b==0):raise ValueError('reciprocal requires nonzero initial value and unit shift')
    if family=='log' and (k!=1 or not b.is_Integer or abs(b)>3):raise ValueError('logarithmic bounds')
    if family in ('sin','cos') and k*u not in (sp.pi/6,sp.pi/4,sp.pi/3,sp.pi/2,2*sp.pi/3,3*sp.pi/4):raise ValueError('familiar angle required')
    fun,rhs,a=easy.math_object(family,k,u,b)
    if a.is_finite is not True or a.is_real is not True:raise ValueError('initial condition must determine a finite real A')
    if family in ('sin','cos') and (sp.sin(k*u) if family=='sin' else sp.cos(k*u))==0:raise ValueError('zero factor')
    if family in ('power','invpower'):domain='x>0' if u>0 else 'x<0'
    elif family in ('sin','cos'):domain=TEX(sp.sin(k*X) if family=='sin' else sp.cos(k*X))+r'\ne0'
    elif family=='recip':domain=TEX(easy.A+k*X)+r'\ne0'
    elif family=='log':domain=r'A+x>0'
    else:domain='all real x'
    interval=('for all real $x$' if family=='exp' else 'on the interval containing the initial point where $'+domain+'$')
    condition='y('+TEX(u)+')='+TEX(b)
    problem='Consider the following initial value problem '+interval+':\n\n$$\n'+r'\frac{dy}{dx}='+TEX(rhs)+r',\qquad '+condition+'.\n$$\n\n'
    problem+='You are given that $y='+TEX(fun)+'$ is the solution family. What is the value of the constant $A$?\n\n$A=${{field-1}}'
    rows=[]
    if family in ('power','invpower','exp','sin','cos'):
        # Preserve the evaluation operation in the first row, before simplifying.
        if family=='power':evaluation='('+TEX(u)+')^{'+TEX(k)+'}'
        elif family=='invpower':evaluation=r'\frac{1}{('+TEX(u)+')^{'+TEX(k)+'}}'
        elif family=='exp':evaluation='e^{('+TEX(k)+')('+TEX(u)+')}'
        else:evaluation='\\'+family+r'\left(('+TEX(k)+')('+TEX(u)+r')\right)'
        factor=sp.simplify(fun.diff(easy.A).subs(X,u))
        rows=[TEX(b)+'&=A'+r'\cdot '+evaluation,
              TEX(b)+'&=A'+r'\cdot\left('+TEX(factor)+r'\right)',
              'A&='+r'\frac{'+TEX(b)+'}{'+TEX(factor)+'}='+TEX(a)]
    elif family=='recip':
        shift=k*u
        rows=[TEX(b)+r'&=\frac{1}{A+('+TEX(shift)+')}',
              'A+('+TEX(shift)+r')&=\frac{1}{'+TEX(b)+'}',
              r'A&=\frac{1}{'+TEX(b)+'}-('+TEX(shift)+')='+TEX(a)]
    else:
        rows=[TEX(b)+r'&=\ln\left(A+('+TEX(u)+r')\right)',
              'e^{'+TEX(b)+'}&=A+('+TEX(u)+')',
              'A&=e^{'+TEX(b)+'}-('+TEX(u)+')='+TEX(a)]
    solution='The supplied family satisfies the differential equation. Substitute $'+condition+'$ into it and solve for $A$:\n\n$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'.\n'+r'\end{aligned}'+'\n$$\n\n'
    # Substitute into the supplied expression without requiring any new rewrite.
    form=TEX(fun).replace('A',r'\left('+TEX(a)+r'\right)')
    solution+='Thus $A='+TEX(a)+'$, and the solution is $y='+form+'$ on the stated interval.'
    ans={':answer/id':'pending',':answer/type':':answer.type/math',':answer/value':TEX(a)}
    field={':answer-field/id':'pending',':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/choices':[ans],':answer-field/correct':[':answer/id','pending']}
    return finalize({'knowledge_point':KP,'question':{':question/id':'pending',':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]},'generation':{'seed':seed,'template':family+'_constant','family':family,'profile':'constant_fitting','parameters':{z:str(v) for z,v in p.items()},'domain':domain,'authored_level':True,'source':{'database':'math','basis':7119,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}}})

def generate(level,seed=0,**kwargs):
    if kwargs.get('replay'):
        if level!='easy':raise ValueError('source replay is easy only')
        return easy_record(seed,**kwargs)
    return normal_record(level,seed,**kwargs)

def batch(level,count,seed):
    if level not in BANDS:raise ValueError('unsupported difficulty')
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);records=[];seen=set();families=list(FAMILIES[level])
    # A shuffled cycle gives each batch the available evaluation/isolation cases.
    # Duplicates retry the same family, preserving its allotted decision case.
    while len(records)<count:
        if len(records)%len(families)==0:rng.shuffle(families)
        family=families[len(records)%len(families)]
        for attempt in range(1000):
            r=normal_record(level,rng.getrandbits(64),family=family);h=r['generation']['content_hash']
            if h not in seen:records.append(r);seen.add(h);break
        else:raise ValueError('requested batch exceeds distinct supported instances')
    return records

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=(*BANDS,'unclassified'),default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');a=p.parse_args()
    print(json.dumps(batch('easy' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed),indent=2))
