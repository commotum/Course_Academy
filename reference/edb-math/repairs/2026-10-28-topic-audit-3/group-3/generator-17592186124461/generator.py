#!/usr/bin/env python3
"""Unit normals: direct partials, combined partials, then product/chain partials.

All bands require differentiation, evaluation, and normalization. Imported source
labels are retained only in immutable source evidence, not used as a capability cap.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import uuid
import sympy as s
from math_format import checked_math_content, normalize_prose, normalize_tex

X,Y=s.symbols('x y',real=True)
ROOT=Path(__file__).resolve().parent
VERSION='unit-normal-verified-4-audit9837'
FAMILIES={'easy':('quadratic',),'moderate':('mixed','logmix'),'hard':('expsin',)}
LEVELS=tuple(FAMILIES)

def tex(z): return s.latex(s.sympify(z),ln_notation=True)
def vec(a,b):
    return r'\left('+tex(a)+r'\right)\,i+\left('+tex(b)+r'\right)\,j'
def uid(data):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+json.dumps(data,sort_keys=True,ensure_ascii=False)))
def simp(z):return s.simplify(s.expand_trig(z))
def unit(a,b):
    n=simp(a*a+b*b)
    if n==0:raise ValueError('zero gradient')
    return tuple(simp(v/s.sqrt(n)) for v in (a,b))
def same(a,b):return all(simp(u-v)==0 for u,v in zip(a,b))
def normal(v,g):return simp(v[0]**2+v[1]**2-1)==0 and simp(v[0]*g[1]-v[1]*g[0])==0

def construction(level,rng,parameters=None,template=None):
    family=template or rng.choice(FAMILIES[level])
    if family not in FAMILIES[level]:raise ValueError('family unavailable at difficulty')
    if parameters is None:
        p,q=rng.randint(-2,2),rng.randint(-2,2)
        if family=='quadratic':
            z=dict(A=rng.choice([-2,-1,1,2]),B=rng.choice([-2,-1,1,2]),C=rng.randint(-3,3),D=rng.randint(-3,3),K=rng.randint(-3,3),p=p,q=q)
        elif family=='mixed':
            z=dict(A=rng.choice([-2,-1,1,2]),B=rng.choice([-2,-1,1,2]),M=rng.choice([-2,-1,1,2]),C=rng.randint(-2,2),D=rng.randint(-2,2),K=rng.randint(-3,3),p=p,q=q)
        elif family=='logmix':
            k=rng.choice([-2,-1,1,2]);p=rng.choice([1,2,3])-k*q
            z=dict(k=k,m=rng.choice([-2,-1,1,2]),K=rng.randint(-3,3),p=p,q=q)
        else:
            z=dict(a=rng.choice([-1,1]),b=rng.choice([-1,1]),c=rng.choice([-1,1]),d=rng.choice([-1,1]),angle=rng.choice(['pi/6','pi/3','-pi/6','-pi/3','2*pi/3','5*pi/6']),q=rng.choice(['0','pi/6','-pi/6']),K=rng.randint(-2,2))
    else:z=dict(parameters)
    if family in ('quadratic','mixed'):
        required={'A','B','C','D','K','p','q'}|({'M'} if family=='mixed' else set())
        if set(z)!=required:raise ValueError('invalid polynomial parameter keys')
        if any(type(v)!=int for v in z.values()):raise ValueError('polynomial parameters must be integers')
        if not all(1<=abs(z[k])<=2 for k in ('A','B')) or max(abs(z[k]) for k in ('C','D','K'))>3 or max(abs(z[k]) for k in ('p','q'))>2:raise ValueError('bounded polynomial parameters')
        if family=='mixed' and not 1<=abs(z['M'])<=2:raise ValueError('nonzero small mixed coefficient')
        f=z['A']*X**2+z['B']*Y**2+z['C']*X+z['D']*Y+z['K']+z.get('M',0)*X*Y
        p,q=map(s.Integer,(z['p'],z['q']))
        refs=['e-3432','q-36311'] if family=='quadratic' else ['q-130710','q-129910','q-36378']
    elif family=='logmix':
        if set(z)!={'k','m','K','p','q'} or any(type(v)!=int for v in z.values()):raise ValueError('invalid logmix parameters')
        if not (1<=abs(z['k'])<=2 and 1<=abs(z['m'])<=2 and abs(z['K'])<=3 and abs(z['q'])<=2 and abs(z['p'])<=7 and 1<=z['p']+z['k']*z['q']<=3):raise ValueError('log argument and workload bounds')
        f=s.log(X+z['k']*Y)-z['m']*X*Y+z['K'];p,q=map(s.Integer,(z['p'],z['q']));refs=['q-71384','investigation moderate exemplar 04354a68-ec3e-5c52-a17c-60e0397b6d6e']
    else:
        if set(z)!={'a','b','c','d','angle','q','K'}:raise ValueError('invalid expsin parameters')
        if any(type(z[k])!=int or z[k] not in (-1,1) for k in ('a','b','c','d')) or type(z['K'])!=int or abs(z['K'])>2:raise ValueError('unit chain factors')
        if z['angle'] not in ['pi/6','pi/3','-pi/6','-pi/3','2*pi/3','5*pi/6'] or z['q'] not in ['0','pi/6','-pi/6']:raise ValueError('familiar exact angles')
        if z['a']*z['d']==z['b']*z['c']:raise ValueError('hard combines independent exponential and trigonometric arguments')
        q=s.sympify(z['q']);p=(s.sympify(z['angle'])-z['d']*q)/z['c']
        f=s.exp(z['a']*X+z['b']*Y)*s.sin(z['c']*X+z['d']*Y)+z['K'];refs=['q-71376','q-71381','prerequisite e-3131 and e-3150','investigation hard exemplar 7e80eb4c-cde7-5721-a8e4-918dc716189e']
    partials=tuple(s.diff(f,t) for t in (X,Y));subs={X:p,Y:q}
    if family=='expsin':
        factor=s.exp(z['a']*p+z['b']*q)/2
        # A positive common factor is removed only after it is displayed.
        g=tuple(simp(v.subs(subs)/factor) for v in partials)
    else:factor=s.Integer(1);g=tuple(simp(v.subs(subs)) for v in partials)
    if g==(0,0):raise ValueError('zero gradient')
    return family,z,f,p,q,partials,g,factor,refs

def error_pool(f,p,q,partials,g,factor):
    """Actual derivative mistakes, then normalization; no arbitrary numeric filler.

    All choices are unit vectors. Knowing only length cannot select the key.
    Sign errors, exchanged partials, dropped summands, omitted power factors,
    product-rule omissions, and wrong-coordinate evaluation are plausible errors.
    """
    subs={X:p,Y:q};component_errors=[]
    for index,(t,d) in enumerate(zip((X,Y),partials)):
        errors=[('negate partial',-d),('exchange partials',partials[1-index])]
        terms=s.Add.make_args(s.expand(d))
        for term in terms:
            if len(terms)>1:errors.append(('omit derivative summand',d-term))
            errors.append(('reverse derivative summand sign',d-2*term))
        for term in s.Add.make_args(s.expand(f)):
            power=term.as_powers_dict().get(t,s.Integer(0))
            if power.is_Integer and power>1:
                dt=s.diff(term,t);errors.append(('omit power multiplier',d-dt+dt/power))
        errors.append(('exchange evaluation coordinates',d.xreplace({X:Y,Y:X})))
        component_errors.append([(name,simp(v.subs(subs)/factor)) for name,v in errors])
    candidates=[]; directions=set()
    ga,gb=map(float,g); gm=(ga*ga+gb*gb)**0.5
    def add(name,a,b):
        if a==b==0 or not all(v.is_real and v.is_finite and v.is_algebraic for v in (a,b)):return
        fa,fb=map(float,(a,b)); mag=(fa*fa+fb*fb)**0.5
        if mag<1e-12:return
        signature=(round(fa/mag,10),round(fb/mag,10))
        if abs(fa*gb-fb*ga)<1e-10*mag*gm or signature in directions:return
        directions.add(signature);candidates.append((name,unit(a,b)))
    add('exchange gradient components',g[1],g[0])
    for name,v in component_errors[0]:add('x: '+name,v,g[1])
    for name,v in component_errors[1]:add('y: '+name,g[0],v)
    for (n,a),(m,b) in zip(component_errors[0],component_errors[1]):add('both: '+n+' / '+m,a,b)
    return candidates

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if profile and profile.startswith('observed-'):
        # Historical replay remains available only as evidence, never sampled.
        from source_replay import generate as replay
        return replay('easy',seed,template,field_type,parameters,profile)
    if level not in LEVELS:raise ValueError('unknown difficulty')
    if profile is not None:raise ValueError('only evidence replay profiles supported')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
    rng=random.Random(seed)
    for attempt in range(100):
        try:
            family,z,f,p,q,partials,g,factor,refs=construction(level,rng,parameters,template)
            pool=error_pool(f,p,q,partials,g,factor)
            if len(pool)<4:raise ValueError('not enough distinct plausible derivative errors')
            break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('no complete bank after bounded resampling')
    correct=unit(*g);bank=[('normal',correct)]+rng.sample(pool,4);rng.shuffle(bank)
    ft=tex(f);pt=tex(p)+','+tex(q)
    problem='Find a unit normal vector to the level curve of the function $f(x,y)='+ft+'$ that passes through the point $(x,y)=('+pt+')$.'
    pre='The gradient at the specified point is normal to the level curve. Differentiate before substituting the coordinates.'
    if family=='logmix':pre+=' Here the logarithm has positive argument $'+tex(p+z['k']*q)+'$, so the function is differentiable near the point.'
    rows=[r'f_x(x,y)&='+tex(s.collect(partials[0],list(partials[0].atoms(s.exp))) if family=='expsin' else partials[0]),r'f_y(x,y)&='+tex(s.collect(partials[1],list(partials[1].atoms(s.exp))) if family=='expsin' else partials[1]),r'\nabla f('+pt+r')&='+vec(*(simp(v.subs({X:p,Y:q})) for v in partials))]
    if family=='expsin':
        # Evaluate the argument actually displayed by SymPy, which may orient
        # sin(-x+y) as -sin(x-y). Never apply an unshown parity conversion.
        argument=next(iter(f.atoms(s.sin))).args[0];angle=simp(argument.subs({X:p,Y:q}));pre+=' Apply both product and chain rules to each partial derivative.'
        rows=rows[:2]+[r'\sin('+tex(angle)+r')&='+tex(s.sin(angle)),r'\cos('+tex(angle)+r')&='+tex(s.cos(angle)),r'\nabla f('+pt+r')&='+tex(factor)+r'\,\mathbf v',r'\mathbf v&='+vec(*g),r'\|\mathbf v\|^2&=\left('+tex(g[0])+r'\right)^2+\left('+tex(g[1])+r'\right)^2',r'&='+tex(simp(g[0]**2+g[1]**2)),r'\|\nabla f('+pt+r')\|&='+tex(simp(factor*s.sqrt(simp(g[0]**2+g[1]**2))))]
    else:
        rows.append(r'\|\nabla f('+pt+r')\|&='+r'\sqrt{\left('+tex(g[0])+r'\right)^2+\left('+tex(g[1])+r'\right)^2}')
        rows.append(r'&='+tex(s.sqrt(simp(g[0]**2+g[1]**2))))
    worked=pre+'\n\n$$\n'+r'\begin{aligned}'+'\n'+r' \\ '.join(rows)+'\n'+r'\end{aligned}'+'\n$$\n\n'
    worked+='This gradient is nonzero. Divide it by its magnitude'
    if family=='expsin':worked+='; the common exponential factor is positive and cancels'
    worked+=':\n\n$$\n'+r'\begin{aligned}'+r'\mathbf n&=\frac{\nabla f('+pt+r')}{\|\nabla f('+pt+r')\|}'+r' \\ &=\frac{'+vec(*g)+r'}{'+tex(s.sqrt(simp(g[0]**2+g[1]**2)))+'}'+r' \\ &='+vec(*correct)+'\n'+r'\end{aligned}'+'\n$$\n\nIts negative is also a unit normal. Exactly one displayed choice is a unit vector parallel to the gradient.'
    problem=normalize_prose(problem);worked=normalize_prose(worked)
    values=[normalize_tex(vec(*v)) for _,v in bank]
    qid=uid({'level':level,'problem':problem,'bank':sorted(values)});fid=uid([qid,'selection'])
    choices=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    index=next(i for i,(name,v) in enumerate(bank) if name=='normal')
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[index][':answer/id']]}]}
    return {'knowledge_point':{'db_id':17592186124461,'id':'d5baf28d-c2c0-57bd-9433-c47043009f0d','title':'Finding a Normal Vector to a Level Curve'},'question':question,'generation':{'version':VERSION,'seed':seed,'difficulty':level,'template':family,'parameters':z,'source_ids':refs,'authored_level':True,'attempts':attempt+1,'recipes':[name for name,_ in bank],'bank_components':[[str(a),str(b)] for _,(a,b) in bank]}}

def generate_easy(**kwargs):return generate('easy',**kwargs)
def generate_moderate(**kwargs):return generate('moderate',**kwargs)
def generate_hard(**kwargs):return generate('hard',**kwargs)

def batch(level,seed,count,template=None,profile=None):
    """Deterministic fresh tasks with varied correct positions and component ranks.

    Resample whole genuine banks, never insert implausible filler or change keys.
    Five-item batches cannot be answered throughout by one numerical rank or slot.
    """
    if profile:return [generate(level,seed+i,template,profile=profile) for i in range(count)]
    records=[];positions=set();ranks=set();seen=set()
    for i in range(count):
        for retry in range(80):
            r=generate(level,seed+i+retry*100003,template,profile=profile)
            q=r['question'];f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];key=f[':answer-field/correct'][1];pos=next(k for k,v in enumerate(cs) if v[':answer/id']==key)
            # Every vector has the same explicit component form. Rank the real
            # x component without normal-vector or target knowledge.
            xs=[float(s.sympify(v[0])) for v in r['generation']['bank_components']];rank=sum(x<xs[pos]-1e-10 for x in xs)
            duplicate=q[':question/problem'] in seen
            if not profile and (duplicate or (i in (1,2) and (pos in positions or rank in ranks))):continue
            records.append(r);positions.add(pos);ranks.add(rank);seen.add(q[':question/problem']);break
        else:raise ValueError('cannot construct varied deterministic batch')
    return records

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=(*LEVELS,'all'),default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('json','markdown'),default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
    if a.count<1:p.error('count must be positive')
    records=[r for level in (LEVELS if a.difficulty=='all' else (a.difficulty,)) for r in batch(level,a.seed,a.count,a.template,a.profile)]
    if a.format=='json':print(json.dumps(records,ensure_ascii=False,indent=2))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\n'.join(chr(65+i)+'. $'+v[':answer/value']+'$' for i,v in enumerate(q[':question/answer-fields'][0][':answer-field/choices'])));print(q[':question/worked-solution'])
