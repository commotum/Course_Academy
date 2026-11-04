#!/usr/bin/env python3
"""Basic cosine double-angle difference; deterministic, relocatable, offline."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import uuid
from fractions import Fraction as F
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '2.0.0'
KP = {'db_id':17592186087669,'id':'5ec37c5e-8a40-58a7-8af3-4457cd5da43f',
      'title':'Using the Double-Angle Formula to Simplify Expressions'}
NS = uuid.UUID('7c26a387-7f9a-4ccf-9b57-e6fdc2823cd5')
# Complete profiles, selected as a unit before parameter sampling. Each pair
# is (outside-factor error, angle ratio relative to the correct angle).
ERRORS = [(F(1), F(1,4)), (F(1), F(1,2)), (F(1), F(3,2)), (F(1), F(2)),
          (F(1,2), F(1)), (F(2), F(1)), (F(1,2), F(1,2)),
          (F(2), F(1,2)), (F(2), F(2))]
# Every bank retains a genuine angle decision: the correct outside coefficient
# occurs on a second option too. This also covers coefficient-free easy/hard.
PROFILES = [p for p in itertools.combinations(ERRORS, 4)
            if any(c==1 for c,r in p)]


def uid(s): return str(uuid.uuid5(NS,s))
def frac(x):
    x=F(x)
    return str(x.numerator) if x.denominator==1 else rf'\frac{{{x.numerator}}}{{{x.denominator}}}'

def angle(x,unit):
    x=F(x)
    if unit=='deg': return frac(x)+r'^\circ'
    n,d=x.numerator,x.denominator
    sign='-' if n<0 else ''
    top=(str(abs(n)) if abs(n)!=1 else '')+r'\pi'
    return sign+(top if d==1 else rf'\frac{{{top}}}{{{d}}}') if n else '0'

def coefficient(kind,n,mult=F(1)):
    c=F(n)*mult if kind=='rational' else F(mult)
    if kind=='rational': return frac(c)
    root=rf'\sqrt{{{n}}}'
    if c==1: return root
    if c.denominator==1: return str(c.numerator)+root
    top=(str(c.numerator) if c.numerator!=1 else '')+root
    return rf'\frac{{{top}}}{{{c.denominator}}}'

def product(c,t): return t if c=='1' else c+t

def trig(x,unit,fn='cos',power=None):
    p='^'+str(power) if power else ''
    return rf'\{fn}'+p+rf'\left({angle(x,unit)}\right)'

def block(rows): return '$$\n'+r'\begin{aligned}'+'\n'+r'\\'.join(rows)+'\n'+r'\end{aligned}'+'\n$$'


def finish(problem,solution,values,key,difficulty,metadata):
    problem,solution=map(normalize_prose,(problem,solution))
    values=[normalize_tex(v) for v in values]; key=normalize_tex(key)
    signature=json.dumps([difficulty,problem,values,key],ensure_ascii=False)
    qid=uid(signature)
    choices=[{':answer/id':uid(qid+':'+str(i)+':'+v),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
    correct=next(a[':answer/id'] for a in choices if a[':answer/value']==key)
    record={'knowledge_point':KP.copy(),'question':{':question/id':qid,
        ':question/difficulty':':question.difficulty/'+difficulty,
        ':question/problem':problem,':question/worked-solution':solution,
        ':question/answer-fields':[{':answer-field/id':uid(qid+':field'),':answer-field/key':'selection',
          ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,
          ':answer-field/correct':[':answer/id',correct]}]},
        'generation':{'generator_version':VERSION,**metadata}}
    return validate_generated_record(record)


def construct(difficulty,form,x,unit,kind='rational',n=F(1),profile=None,rng=None,reordered=False):
    """A single source-supported identity application, with an optional factor."""
    x=F(x); rng=rng or random.Random(0)
    if difficulty=='easy': kind,n='rational',F(1)
    a=coefficient(kind,n); twoa=coefficient(kind,n,F(2))
    ct=trig(x,unit,'cos',2); st=trig(x,unit,'sin',2)
    pattern=ct+'-'+st
    identity=r'\cos^2 x-\sin^2 x=\cos(2x)'
    key=product(a,trig(2*x,unit))
    expr=product(a,ct)+'-'+product(a,st)
    if reordered: expr='-'+product(a,st)+'+'+product(a,ct)
    solution=''
    if a!='1' or reordered:
        factored=product(a,rf'\left({pattern}\right)')
        solution='Collect the common factor:\n\n'+block(['&'+expr,'&='+factored])+'\n\n'
    solution+='Use the cosine double-angle formula:\n\n$$\n'+identity+'\n$$\n\n'
    solution+='Substitute $x='+angle(x,unit)+'$:\n\n'+block([pattern+'&='+rf'\cos\left(2\cdot {angle(x,unit)}\right)',
            '&='+trig(2*x,unit)])
    if a!='1':
        solution+='\n\nKeep the outside factor:\n\n'+block([a+rf'\left({pattern}\right)'+'&='+key])
    profile=profile if profile is not None else rng.choice(PROFILES)
    roles=[(F(1),F(1)),*profile]
    val=[product(coefficient(kind,n,c),trig(2*x*r,unit)) for c,r in roles]
    numeric=[float(c)*(float(F(n)) if kind=='rational' else math.sqrt(n))*math.cos(float(2*x*r)*(math.pi/180 if unit=='deg' else math.pi)) for c,r in roles]
    if any(abs(v-w)<1e-9 for i,v in enumerate(numeric) for w in numeric[:i]):
        raise ValueError('Equivalent choices; reject complete bank')
    rng.shuffle(val)
    refs=[17592186345258,17592186598626] if difficulty=='easy' else [17592186256392,17592186256393,17592186256394,17592186345214]
    return finish('Express $'+expr+'$ as a single trigonometric ratio.',solution,val,key,difficulty,
      {'template':form+'-'+difficulty,'profile':[[str(c),str(r)] for c,r in profile],
       'parameters':{'form':form,'x':str(x),'unit':unit,'coefficient_kind':kind,'n':str(n),'reordered':reordered},
       'source_question_ids':refs,'source_support':'direct imported family' if difficulty!='hard' else 'authored same-operation continuation of imported moderate families; no imported hard anchors',
       'authored_profile':True})


def sample_angle(difficulty,unit,rng):
    if unit=='deg': return F(rng.randint(10,170))
    d=rng.choice([5,6,7,8,9,10,11,12,15,16,18,20,24])
    return F(rng.randint(1,2*d-1),d)


def bank_predictions(record):
    """Bank-only cues. Construction checks use the same roles as the bank;
    independent review tests parse the actual displayed expressions instead.
    """
    p=record['generation']['parameters']; x=F(p['x']); unit=p['unit']
    band=record['question'][':question/difficulty'].rsplit('/',1)[-1]
    k=2
    kind,n=p['coefficient_kind'],F(p['n'])
    profile=[tuple(map(F,pair)) for pair in record['generation']['profile']]
    rolemap={normalize_tex(product(coefficient(kind,n,c),trig(k*x*r,unit))):(c,k*x*r)
             for c,r in [(F(1),F(1)),*profile]}
    field=record['question'][':question/answer-fields'][0]
    choices=field[':answer-field/choices']
    correct=next(i for i,a in enumerate(choices) if a[':answer/id']==field[':answer-field/correct'][1])
    cs,args=zip(*(rolemap[a[':answer/value']] for a in choices))
    nums=[float(c)*(float(n) if kind=='rational' else math.sqrt(n))*math.cos(float(a)*(math.pi/180 if unit=='deg' else math.pi)) for c,a in zip(cs,args)]
    def unique(values,which):
        v=which(values); candidates=[i for i,a in enumerate(values) if a==v]
        return candidates[0] if len(candidates)==1 else None
    predictions={f'position-{i+1}':i for i in range(5)}
    for rank,i in enumerate(sorted(range(5),key=lambda i:nums[i])): predictions[f'value-rank-{rank+1}']=i
    for label,values in [('angle',args),('length',[len(a[':answer/value']) for a in choices])]:
        predictions['minimum-'+label]=unique(values,min);predictions['maximum-'+label]=unique(values,max)
    modes=lambda values:{a for a,c in Counter(values).items() if c==max(Counter(values).values())}
    mc,ma=modes(cs),modes(args); candidates=[i for i in range(5) if cs[i] in mc and args[i] in ma]
    predictions['modal-intersection']=candidates[0] if len(candidates)==1 else None
    for label,sign in [('positive',1),('negative',-1)]:
        candidates=[i for i,a in enumerate(nums) if sign*a>1e-12]
        predictions['unique-'+label]=candidates[0] if len(candidates)==1 else None
        paired=[i for i,a in enumerate(nums) if sign*a>1e-12 and any(abs(a+b)<1e-12 for j,b in enumerate(nums) if i!=j)]
        predictions['paired-'+label]=paired[0] if len(paired)==1 else None
    return correct,predictions


def batch_shortcuts(records):
    """A repeated visible subgroup needs a counterexample to a fixed cue.
    Singletons cannot satisfy such a condition and are deliberately exempt.
    """
    groups={'overall':records}
    for name,get in [('form',lambda r:r['generation']['parameters']['form']),
                     ('unit',lambda r:r['generation']['parameters']['unit']),
                     ('radical',lambda r:r['generation']['parameters']['coefficient_kind']=='sqrt')]:
        for value in {get(r) for r in records}:
            groups[name+'='+str(value)]=[r for r in records if get(r)==value]
    failures=[]
    for name,group in groups.items():
        if len(group)<2:continue
        cues=[bank_predictions(r) for r in group]
        for strategy in cues[0][1]:
            if all(predictions[strategy]==correct for correct,predictions in cues): failures.append((name,strategy))
    return failures


def generate(difficulty,count,seed):
    if count<0: raise ValueError('count must be nonnegative')
    rng=random.Random(seed); records=[]; seen=set(); rejected=0
    # Cycle shuffled decision strata, independently of incidental numeric values.
    strata=list(itertools.product(['difference'],['deg','rad']))
    rng.shuffle(strata)
    for i in range(count):
        form,unit=strata[i%len(strata)]
        profile=rng.choice(PROFILES)
        x=sample_angle(difficulty,unit,rng)
        kind,n='rational',F(1)
        if difficulty in ('moderate','hard'):
            kind,n=rng.choice([('rational',F(2)),('rational',F(3)),('rational',F(4)),
                ('rational',F(5)),('rational',F(1,2)),('rational',F(1,3)),('rational',F(1,4)),
                ('sqrt',2),('sqrt',3),('sqrt',5)])
        if difficulty=='hard':
            kind,n=rng.choice([('rational',F(3,2)),('rational',F(2,3)),('rational',F(5,3)),('rational',F(3,4)),('sqrt',2),('sqrt',3)])
        reordered=difficulty=='hard' and rng.choice([False,True])
        for attempt in range(1000):
            try: rec=construct(difficulty,form,x,unit,kind,n,profile,rng,reordered)
            except ValueError:
                rejected+=1
                profile=rng.choice(PROFILES)
                # Some periodic angles collapse every available error bank.
                # Leave an unproductive angle without narrowing the domain or
                # discarding legitimate zero/cancellation outcomes wholesale.
                if (attempt+1)%32==0:
                    x=sample_angle(difficulty,unit,rng)
                continue
            # A prompt denotes a semantic instance, independent of the bank.
            semantic=rec['question'][':question/problem']
            if semantic in seen:
                x=sample_angle(difficulty,unit,rng)
                continue
            seen.add(semantic); records.append(rec); break
        else: raise RuntimeError('Unable to construct a distinct valid bank')
    # Keep the independently sampled mathematical givens. Only resample whole
    # plausible error profiles/order when the finite delivered batch has a cue.
    # The source instances, scalar/sign outcomes and strata remain eligible.
    rebalanced=0
    for cycle in range(1000):
        if not batch_shortcuts(records):break
        rebalanced+=1
        rebuilt=[]
        for previous in records:
            p=previous['generation']['parameters']
            for attempt in range(1000):
                try:
                    r=construct(difficulty,p['form'],F(p['x']),p['unit'],p['coefficient_kind'],F(p['n']),rng.choice(PROFILES),rng,p.get('reordered',False))
                    rebuilt.append(r);break
                except ValueError:rejected+=1
            else:raise RuntimeError('Unable to rebuild a distinct plausible error bank')
        records=rebuilt
    else:raise RuntimeError('Unable to construct a batch without a fixed answer-bank cue')
    for r in records: r['generation'].update({'seed':seed,'batch_count':count,'batch_rejected_banks':rejected,'batch_rebalanced':rebalanced})
    return records



def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='easy')
    p.add_argument('--count',type=int,default=5); p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json'],default='json')
    a=p.parse_args()
    if a.count<0: p.error('count must be nonnegative')
    records=generate('easy' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
