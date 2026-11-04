#!/usr/bin/env python3
"""Seeded degree sine-expansion generator. Exact coefficients use Z[sqrt2,sqrt3]/2."""
import argparse
from collections import defaultdict
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '2.0.0'
KP = {'db_id':17592186059662, 'id':'69e91ce7-259a-5a11-bb79-7e6ad7ea86d4',
      'title':'Simplifying Expressions in Degrees Using the Sum and Difference Formulas'}
Z = (0,0,0)
SPECIAL = (30,45,60,120,135,150,210,225,240,300,315,330)
# Integer numerators; denominator 2. No CAS rewriting of operator arguments.
FIRST = {0:((2,0,0),Z),30:((0,0,1),(1,0,0)),45:((0,1,0),(0,1,0)),
         60:((1,0,0),(0,0,1)),90:(Z,(2,0,0))}
def scale(v,k): return tuple(k*x for x in v)
def add(v,w): return tuple(a+b for a,b in zip(v,w))
def pair(t):
    t %= 360
    if t<=90: return FIRST[t]
    if t<=180:
        c,s=FIRST[180-t];return scale(c,-1),s
    if t<=270:
        c,s=FIRST[t-180];return scale(c,-1),scale(s,-1)
    c,s=FIRST[360-t];return c,scale(s,-1)

def tex(v):
    if v==Z:return '0'
    divisor=2 if all(x%2==0 for x in v) else 1
    vs=[x//divisor for x in v]; denominator=2//divisor
    neg=next(x for x in vs if x)!=abs(next(x for x in vs if x))
    if all(x<=0 for x in vs): vs=[-x for x in vs]; outside='-'
    else: outside=''
    parts=[]
    for x,root in zip(vs,['',r'\sqrt{2}',r'\sqrt{3}']):
        if not x:continue
        term=(str(abs(x)) if abs(x)!=1 or not root else '')+root
        parts.append(('-' if x<0 else ('+' if parts else ''))+term)
    body=''.join(parts)
    return outside+(r'\frac{'+body+'}{2}' if denominator==2 else body)

def positive(v):return next(x for x in v if x)>0

def linear(a,b):
    parts=[]
    for v,f in [(a,r'\sin x'),(b,r'\cos x')]:
        if v==Z:continue
        # Signs of mixed-radical sums are not inferred from lexicographic order.
        # Parenthesize coefficient expressions; only extract a uniform minus.
        neg=all(x<=0 for x in v)
        value=scale(v,-1) if neg else v
        c=tex(value)
        if value==(2,0,0):c=''
        elif sum(x!=0 for x in value)>1:c=r'\left('+c+r'\right)'
        parts.append(('-' if neg else ('+' if parts else ''))+c+f)
    return ''.join(parts) or '0'

def shift(t):return r'\sin(x'+('+' if t>0 else '-')+str(abs(t))+r'^\circ)'
def display(body):return '$$\n'+body+'\n$$'
def aligned(rows):return display(r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}')
def expansion(t):
    c,s=pair(abs(t));a,b=pair(t);op='+' if t>0 else '-';angle=str(abs(t))+r'^\circ'
    return aligned([shift(t)+r'&=\sin x\cos '+angle+op+r'\cos x\sin '+angle,
        r'&=\sin x\cdot\left('+tex(c)+r'\right)'+op+r'\cos x\cdot\left('+tex(s)+r'\right)',
        '&='+linear(a,b)])
def identity(t):
    op='+' if t>0 else '-'
    return 'Use the '+('sum' if t>0 else 'difference')+' formula for sine:\n'+display(r'\sin(u'+op+r'v)=\sin u\cos v'+op+r'\cos u\sin v.')

def identity_uuid(content):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/sine-degrees/'+content))
def make_record(level,problem,solution,descriptors,meta):
    problem,solution=normalize_prose(problem),normalize_prose(solution)
    desc=[(key,kind,[normalize_tex(x) for x in vals],normalize_tex(correct)) for key,kind,vals,correct in descriptors]
    semantic=json.dumps([level,problem,solution,desc],ensure_ascii=False,separators=(',',':'))
    base=hashlib.sha256(semantic.encode()).hexdigest();fields=[]
    for i,(key,kind,values,correct) in enumerate(desc):
        assert len(set(values))==len(values) and correct in values
        choices=[{':answer/id':identity_uuid(base+f'/field/{i}/answer/{j}'),':answer/type':':answer.type/math',':answer/value':v} for j,v in enumerate(values)]
        fields.append({':answer-field/id':identity_uuid(base+f'/field/{i}'),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[values.index(correct)][':answer/id']]})
    return validate_generated_record({'knowledge_point':KP.copy(),'question':{':question/id':identity_uuid(base),':question/difficulty':':question.difficulty/'+level,
            ':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},
            'generation':{'version':VERSION,**meta}})

def instance(level,t,shape='blank',external=1,u=None,outer=-1,bank_sign=1,order_seed=0):
    a,b=pair(t);lhs=shift(t);solution=identity(t)+'\nApply it and substitute the exact special-angle values:\n'+expansion(t)
    desc=[];meta={'template':level+'-'+shape,'parameters':{'t':t,'shape':shape},'source_refs':['e-3518','q-141278','q-274570'] if level=='easy' else ['e-3518','q-329179','q-65438','q-141270']}
    if u is not None:
        raise ValueError('Only one shifted sine is in this KP family')
    if shape=='radio':
        if level=='easy':
            pairs=[((2,0,0),Z),((-2,0,0),Z),(Z,(2,0,0)),(Z,(-2,0,0)),((2,0,0),(2*bank_sign,0,0))]
            profile='four-signed-basis-plus-false-linearization'
        else:
            # Complete sign-error profile, plus a wrong-reference-angle evaluation.
            aa=tuple(abs(x) for x in a);bb=tuple(abs(x) for x in b)
            pairs=[(scale(aa,i),scale(bb,j)) for i in [-1,1] for j in [-1,1]]
            ref=45 if abs(t)%90!=45 else 30
            wrong_a,wrong_b=pair(ref)
            pairs.append((scale(wrong_a,bank_sign),scale(wrong_b,-bank_sign)))
            profile='four-sign-cases-plus-wrong-reference'
        vals=[linear(c,d) for c,d in pairs];key=linear(a,b)
        assert len(set(vals))==5 and key in vals
        random.Random(order_seed).shuffle(vals)
        problem='Express $'+lhs+r'$ using $\sin x$ and $\cos x$.'+'\n\n$'+lhs+'=$'
        desc=[('selection','radio',vals,key)];meta.update(bank_profile=profile)
        meta['parameters']['bank_sign']=bank_sign
    elif level=='easy':
        problem='Express $'+lhs+r'$ in terms of $\sin x$ or $\cos x$.'+'\n\n$'+lhs+'=$ {{field-1}}'
        desc=[('field-1','blank',[linear(a,b)],linear(a,b))]
    else:
        external=-1 if external==-1 and not positive(b) else 1
        second=scale(b,external)
        problem='Express $'+lhs+r'$ using $\sin x$ and $\cos x$. Enter exact coefficients, including their signs.'+'\n\n$'+lhs+'=$ {{field-1}} $\\sin x'+('+' if external==1 else '-')+'$ {{field-2}} $\\cos x$'
        desc=[('field-1','blank',[tex(a)],tex(a)),('field-2','blank',[tex(second)],tex(second))]
        solution+='\nThe '+('plus' if external==1 else 'minus')+' sign outside the second blank is supplied. The entries are $'+tex(a)+'$ and $'+tex(second)+'$, respectively.'
        meta['parameters']['external']=external
    return make_record(level,problem,solution,desc,meta)

@lru_cache(None)
def catalog(level):
    angles=(90,180,270) if level=='easy' else (SPECIAL if level=='moderate' else tuple(a for a in SPECIAL if a>90))
    return tuple(sign*a for sign in (-1,1) for a in angles)

def generate(level,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    capacity=len(catalog(level))
    if count>capacity:raise ValueError(f'{level} supports {capacity} mathematical shifts; requested {count}')
    rng=random.Random(seed);out=[];cycle=0
    while len(out)<count:
        deck=list(catalog(level));rng.shuffle(deck)
        for t in deck:
            shape=rng.choice(('blank','radio')) if level!='hard' else 'blank'
            e=-1 if shape=='blank' and level!='easy' and not positive(pair(t)[1]) and rng.randrange(2) else 1
            r=instance(level,t,shape,e,bank_sign=rng.choice((-1,1)),order_seed=rng.getrandbits(64))
            r['generation'].update(seed=seed,index=len(out),catalog_cycle=cycle,mathematical_capacity=capacity,
                calibration='authored overlapping single-shift band' if level=='hard' else 'imported same-skill family')
            out.append(r)
            if len(out)==count:break
        cycle+=1
    return out


def replay(source_id):
    case=next(x for x in json.loads(Path(__file__).with_name('source-cases.json').read_text()) if x['source_id']==source_id)
    return make_record(case['difficulty'],case['problem'],case['solution'],[(f['key'],f['kind'],f['values'],f['correct']) for f in case['fields']],
        {'template':'source-replay','source_refs':[source_id], 'source_db_id':case['db_id'],'source_question_uuid':case['uuid']})

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json')
    p.add_argument('--source-case',help='Replay an original complete source bank by its source ID')
    args=p.parse_args()
    if args.count<0:p.error('--count must be nonnegative')
    print(json.dumps([replay(args.source_case)] if args.source_case else generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
