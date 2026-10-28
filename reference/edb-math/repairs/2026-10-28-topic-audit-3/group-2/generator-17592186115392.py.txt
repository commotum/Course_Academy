#!/usr/bin/env python3
"""Seeded, relocatable vector/scalar chain-rule practice. No database access."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
import sympy as S
import core
from math_format import normalize_prose, normalize_tex, validate_generated_record

t,u=core.t,core.u
KP='a146d5d3-2562-5b8b-886e-4cf6519d3282'
VERSION='vector-chain-v3'
LEVELS=('easy','moderate','hard')

def eq(a,b):
    if a==b:return True
    diff=a-b
    # A numerical witness may prove inequality; equality still uses the CAS.
    witness=diff.subs({t:2,u:2}).evalf(60)
    if witness.is_finite and abs(witness)>S.Float('1e-30'):return False
    return S.simplify(diff)==0

def vec(v):
    return core.vector(v,'matrix')

def simple(x):
    # Keep trig/exponential inputs intact. Ordinary rational cancellation is
    # shown by the previous solution row; no trigonometric identities are used.
    if x.has(S.sin,S.cos,S.tan,S.sec):return x
    if x.has(S.exp):return S.powsimp(x,combine='exp')
    if x.is_polynomial(t):return S.expand(x)
    if x.is_rational_function(t):return S.factor(x)
    return x

def data(level,name,p,permutation=(0,1,2)):
    if level=='easy':
        f,h,_,_,_=core.math_data(name,p)
        domain={'sin_log_tan_power':r't\ne0\text{ and }\cos('+core.tex(h)+r')\ne0',
                'log_quadratic_log':r't>1',
                'reciprocal_log_reciprocal':r't\ne0\text{ and }'+core.tex(h+p.get('b',0))+'>0'}.get(name,None)
        point=None
    else:
        f=[p['c']*S.log(u),p['d']*u**2,S.Integer(p['e'])/u]
        if level=='hard':
            h=S.sqrt(p['b']+p['a']*t**2);point=None;domain=None
        elif name=='evaluated_exp':
            h=S.exp(p['a']*t);point=p['sign']*S.log(p['k'])/abs(p['a']);domain=None
        elif name=='evaluated_reciprocal':
            h=S.Integer(p['a'])/t;point=S.Integer(p['k']);domain=r't>0'
        else:raise ValueError(name)
    f=[f[i] for i in permutation]
    D=[S.sec(u)**2 if x==S.tan(u) else S.diff(x,u) for x in f]; hp=S.diff(h,t)
    sub=[x.subs(u,h) for x in D]
    C=[simple(x*hp) for x in sub]
    target=[S.simplify(x.subs(t,point)) for x in C] if point is not None else C
    return f,h,D,hp,sub,C,target,point,domain

def bank(f,h,D,hp,C,target,point,rng):
    # Select answer-bearing roles before error recipes or option order.
    active=[i for i,x in enumerate(target) if x!=0]
    i,j=rng.sample(active,2)
    def at(x):return S.simplify(x.subs(t,point)) if point is not None else simple(x)
    errors=[];labels=[]
    for k in (i,j):
        candidates=[(D[k].subs(u,h),'omit inner derivative'),
                    (C[k]*hp,'multiply by inner derivative twice'),
                    (-C[k],'reverse derivative sign'),
                    (D[k].subs(u,t)*hp,'substitute t for the inner input'),
                    (f[k].subs(u,h)*hp,'use component instead of its derivative')]
        rng.shuffle(candidates);eligible=[]
        for x,label in candidates:
            x=at(x)
            if x.has(S.zoo,S.nan,S.oo,-S.oo) or eq(x,target[k]):continue
            if any(eq(x,y[0]) for y in eligible):continue
            eligible.append((x,label))
        if len(eligible)<2:raise ValueError('resample: insufficient distinct component errors')
        errors.append([x[0] for x in eligible[:2]]);labels.append([x[1] for x in eligible[:2]])
    values=[];recipes=[]
    for x,y in ((None,None),(0,None),(None,0),(0,0),(1,1)):
        v=list(target);recipe=[]
        for k,index,pos in ((i,x,0),(j,y,1)):
            if index is not None:
                v[k]=errors[pos][index];recipe.append({'coordinate':k,'error':labels[pos][index]})
        values.append(v);recipes.append(recipe)
    if any(all(eq(a,b) for a,b in zip(v,w)) for n,v in enumerate(values) for w in values[:n]):
        raise ValueError('resample: equivalent vectors')
    return values,recipes

def build(level,name,p,seed,permutation=(0,1,2),response=None):
    f,h,D,hp,sub,C,target,point,domain=data(level,name,p,permutation)
    rng=random.Random(seed)
    response=response or ('blank' if level=='hard' else 'radio')
    if response=='radio':values,recipes=bank(f,h,D,hp,C,target,point,rng)
    else:values=None;recipes=None
    tx=core.tex
    prompt='Let $\\mathbf f(u)='+vec(f)+'$ and $u(t)='+tx(h)+'$. '
    prompt+='Find $(\\mathbf f\\circ u)\'(t)$.' if point is None else 'Find $(\\mathbf f\\circ u)\'('+tx(point)+')$.'
    if domain:prompt+=' Work on the real domain $'+domain+'$.'
    if response=='blank':
        prompt+='\n\nWrite\n\n'+core.block("(\\mathbf f\\circ u)'(t)="+r'\begin{bmatrix}A(t) \\ B(t) \\ C(t)\end{bmatrix}')
        for key in 'ABC':prompt+='\n\n$'+key+'(t)=$ {{'+key+'}}'
    solution='Differentiate the outer function component by component and the scalar inner function:\n\n'
    solution+=core.block(core.aligned([(r"\mathbf f'(u)",vec(D)),("u'(t)",tx(hp))]))
    if level=='hard':
        R=p['b']+p['a']*t**2
        solution+='\n\nThe scalar derivative uses the chain rule again:\n\n'+core.block("u'(t)="+r'\frac{1}{2\sqrt{'+tx(R)+'}}'+r'\cdot('+tx(S.diff(R,t))+')='+tx(hp))
    solution+='\n\nSubstitute the inner input and multiply **every component** by the same scalar derivative:\n\n'
    rows=[("(\\mathbf f\\circ u)'(t)",r"\mathbf f'(u(t))u'(t)"),('',vec(sub)+r'\cdot\left('+tx(hp)+r'\right)'),('',vec(C))]
    solution+=core.block(core.aligned(rows))
    if any(x.has(S.exp) for x in f) or h.has(S.exp):
        solution+='\n\nProducts and reciprocals of exponential factors simplify by adding or subtracting their exponents.'
        if h.has(S.exp):solution+=' Here $u(t)>0$.'
        if any(x.has(S.Pow) and any(z.exp==S.Rational(1,2) for z in x.atoms(S.Pow)) for x in f):solution+=' Taking the square root of a positive exponential halves its exponent.'
    if point is not None:
        hv=S.simplify(h.subs(t,point));dv=S.simplify(hp.subs(t,point));outer=[S.simplify(x.subs(u,hv)) for x in D]
        solution+='\n\nAt the requested point, evaluate the input and the multiplier separately:\n\n'
        solution+=core.block(core.aligned([('u('+tx(point)+')',tx(hv)),("u'("+tx(point)+')',tx(dv)),("(\\mathbf f\\circ u)'("+tx(point)+')',vec(outer)+r'\cdot\left('+tx(dv)+r'\right)'),('',vec(target))]))
    if level=='hard':solution+='\n\nCancel the common square root in the quadratic component. In the reciprocal component the denominator is the square-root input raised to $3/2$. All formulas hold for every real $t$ because $u(t)>0$.'
    return record(level,name,p,permutation,seed,prompt,solution,target,values,recipes,response,f,h,hp,point)

def record(level,name,p,permutation,seed,prompt,solution,target,values,recipes,response,f,h,hp,point):
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    # Identity binds normalized visible content, including complete answer banks.
    texts=[normalize_tex(vec(v)) for v in values] if response=='radio' else [normalize_tex(core.tex(x)) for x in target]
    content=json.dumps([VERSION,level,prompt,solution,sorted(texts) if response=='radio' else texts],ensure_ascii=False)
    qid=uuid.uuid5(uuid.UUID(KP),content);fields=[]
    for k in (['selection'] if response=='radio' else list('ABC')):
        fid=uuid.uuid5(qid,k);idx=0 if response=='radio' else 'ABC'.index(k)
        answers=[{':answer/id':str(uuid.uuid5(fid,value)),':answer/type':':answer.type/math',':answer/value':value} for value in (texts if response=='radio' else [texts[idx]])]
        cid=answers[0][':answer/id']
        if response=='radio':random.Random(seed).shuffle(answers)
        fields.append({':answer-field/id':str(fid),':answer-field/key':k,':answer-field/type':':answer-field.type/'+response,':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]})
    result={'knowledge_point':{'db_id':17592186115392,'id':KP,'title':'Using the Chain Rule for Differentiation'},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'template':name,'parameters':p,'permutation':list(permutation),'seed':seed,'source_question_ids':([core.QUESTIONS[core.SPECS[name][0]][':question/id']] if level=='easy' else ['54431f49-d58a-56d2-a215-6850fe5a1307'] if level=='moderate' else ['0454f514-e0b9-5c05-a760-abe18a9fdfa5']),'authored_level':level!='easy','bank_profile':'component-error-grid' if values else None,'recipes':recipes,'domain':'natural real domain of supplied functions','solution_path':{'outer':[S.sstr(x) for x in f],'inner':S.sstr(h),'inner_derivative':S.sstr(hp),'point':S.sstr(point) if point is not None else None,'displayed_final':[core.tex(x) for x in target],'conversions':['rational cancellation','exponent product/reciprocal rules'] if h.has(S.exp) else ['rational cancellation'],'steps':['differentiate outer components','differentiate inner function','substitute inner input','multiply all components']+(['evaluate at requested point'] if point is not None else [])}}}
    return validate_generated_record(result)

def sample_parameters(level,name,rng):
    if level=='easy':
        p=dict(core.SPECS[name][2]);p['a']=rng.choice([1,2,3,4])
        if name in ('linear_quadratic_affine','linear_quadratic_exp','log_reciprocal_exp','log_power_root_exp','cos_cube_log_exp'):p['a']*=rng.choice([-1,1])
        if name in ('linear_quadratic_affine','sin_cos_exp_affine') and abs(p['a'])==1:p['a']*=2
        for key in ('b','c','d','e'):
            if key in p:p[key]=rng.choice([-3,-2,-1,1,2,3]) if key=='b' and name!='reciprocal_log_reciprocal' else rng.randint(1,4)
        return p
    p={k:rng.choice([-2,-1,1,2]) for k in ('c','d','e')}
    if level=='hard':p.update(a=rng.choice([1,2,3]),b=rng.choice([1,2,3,4,5]))
    elif name=='evaluated_exp':p.update(a=rng.choice([-2,-1,1,2]),sign=rng.choice([-1,1]),k=rng.choice([2,3]))
    else:p.update(a=rng.choice([1,2,3]),k=rng.choice([1,2,3]))
    return p

def essential(record):
    # Remove additive constants and coordinate order. Shifts in the inner input
    # still count when they change an actual nonlinear component calculation.
    g=record['generation'];p=g['solution_path']; f=[S.sympify(x,locals={'u':u,'t':t}) for x in p['outer']]
    return (g['template'],p['inner'],p['point'],tuple(sorted(S.srepr(S.diff(x,u)) for x in f)))

def generate_batch(level,count,seed):
    if level=='unclassified':level='easy'
    if level not in LEVELS or count<1:raise ValueError('A valid level and positive count are required')
    rng=random.Random(seed);names=list(core.SPECS) if level=='easy' else ['evaluated_exp','evaluated_reciprocal'] if level=='moderate' else ['nested_radical']
    out=[];seen=set();order=[]
    for _ in range(count*100):
        if not order:order=names.copy();rng.shuffle(order)
        name=order[-1]
        p=sample_parameters(level,name,rng);perm=list(range(3));rng.shuffle(perm);item_seed=rng.randrange(2**63)
        try:r=build(level,name,p,item_seed,perm)
        except ValueError as exc:
            if str(exc).startswith('resample:'):continue
            raise
        key=essential(r)
        if key in seen:continue
        seen.add(key);out.append(r);order.pop()
        if len(out)==count:return out
    raise ValueError('Requested batch exceeds bounded semantic sampling capacity')

def replay(name,seed=0):
    p=dict(core.SPECS[name][2]);f,h,D,hp,C=core.math_data(name,p);style=core.SPECS[name][1]
    values=core.observed_bank(name,p,D,h,hp,C)
    correct=next(i for i,v in enumerate(values) if all(eq(S.sympify(x),y) for x,y in zip(v,C)))
    values=[values[correct]]+values[:correct]+values[correct+1:]
    prompt,solution,_=core.build_text(name,p,f,h,D,hp,C,style)
    # Preserve source representation and bank exactly, with normalized notation.
    r=record('easy',name,p,(0,1,2),seed,prompt,solution,C,values,None,'radio',f,h,hp,None)
    # record builds column vectors; use the original style for faithful replay.
    q=r['question'];fid=q[':question/answer-fields'][0][':answer-field/id'];field=q[':question/answer-fields'][0]
    texts=[normalize_tex(core.vector(v,style)) for v in values]
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),x)),':answer/type':':answer.type/math',':answer/value':x} for x in texts]
    field[':answer-field/choices']=answers;field[':answer-field/correct']=[':answer/id',answers[0][':answer/id']]
    r['generation']['bank_profile']='source-replay';return validate_generated_record(r)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=[*LEVELS,'unclassified','all'],default='easy')
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args()
    try:records=[r for level in (LEVELS if args.difficulty=='all' else [args.difficulty]) for r in generate_batch(level,args.count,args.seed)]
    except ValueError as exc:parser.error(str(exc))
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
