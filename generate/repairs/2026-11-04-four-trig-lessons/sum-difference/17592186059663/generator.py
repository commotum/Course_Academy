#!/usr/bin/env python3
"""Seeded exact sine practice. Runtime is database-free and relocatable."""
import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = '213eda96-c41d-5361-9da9-8349617014f1'
SOURCES = {
 'easy':['d93d90d2-8105-59cb-a801-47640240ddbd','4bf1dbaf-6e61-5607-8543-7f1dda28cf3f'],
 'moderate':['2f345820-3d37-51b7-9bb6-51dedb3880f8','16e4e461-f621-53d1-96fa-7b2df72cfebc','996eb380-c7f3-58b2-8258-bc17318d5244','585e18d7-2aa5-5d3f-86ad-587ffce85678'],
 'hard':['97e8e577-5bc3-50c1-b8c6-66747cc71a22']}
# (signed numerator, squarefree radicand), common denominator 2.
SIN = {30:(1,1),45:(1,2),60:(1,3),120:(1,3),135:(1,2),150:(1,1),
       210:(-1,1),225:(-1,2),240:(-1,3),300:(-1,3),315:(-1,2),330:(-1,1)}
COS = {30:(1,3),45:(1,2),60:(1,1),120:(-1,1),135:(-1,2),150:(-1,3),
       210:(-1,3),225:(-1,2),240:(-1,1),300:(1,1),315:(1,2),330:(1,3)}


def uid(text):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy/sine-v1/'+text))


def angle(degrees, unit):
    if unit == 'degrees': return str(degrees)+r'^\circ'
    f=Fraction(degrees,180)
    n=abs(f.numerator)
    top=(str(n) if n!=1 else '')+r'\pi'
    result=top if f.denominator==1 else r'\frac{'+top+'}{'+str(f.denominator)+'}'
    return ('-' if f<0 else '')+result


def trig(func, deg, unit):
    return '\\'+func+r'\left('+angle(deg,unit)+r'\right)'


def ratio(pair):
    sign, rad=pair
    return ('-' if sign<0 else '')+r'\frac{'+('1' if rad==1 else r'\sqrt{'+str(rad)+'}')+'}{2}'


def product(a,b):
    return (a[0]*b[0],a[1]*b[1])


def single(pair):
    sign,rad=pair
    return ('-' if sign<0 else '')+r'\frac{\sqrt{'+str(rad)+'}}{4}'


def combined(p,q):
    terms={p[1]:p[0],q[1]:q[0]}
    a,b=terms[6],terms[2]
    # Never use symbolic normal forms to choose the learner's notation.
    body=('-' if a<0 else '')+r'\sqrt{6}'+('+' if b>0 else '-')+r'\sqrt{2}'
    return r'\frac{'+body+'}{4}'


def instance(a,b,op):
    t=a+op*b
    p=product(SIN[a],COS[b]); rawq=product(COS[a],SIN[b]); q=(op*rawq[0],rawq[1])
    return {'a':a,'b':b,'op':op,'target':t,'p':p,'q':q,'case':tuple(dict([ (p[1],p[0]),(q[1],q[0]) ])[r] for r in (6,2))}


def catalog():
    items=[]
    for a in SIN:
        for b in SIN:
            if (a%90==45)==(b%90==45): continue
            for op in (-1,1):
                t=a+op*b
                if not -360<t<360 or t%30==0 or t%45==0: continue
                items.append(instance(a,b,op))
    return items


def build(inst,difficulty,*,shape=None,unit=None,profile=(1,2),order_seed=0,replay_profile=None):
    a,b,op,t=(inst[k] for k in ('a','b','op','target'))
    p,q=inst['p'],inst['q']; unit=unit or ('radians' if difficulty=='easy' else 'degrees')
    shape=shape or 'radio'; symbol='+' if op==1 else '-'
    target=trig('sin',t,unit); split=angle(a,unit)+symbol+angle(b,unit)
    eq=angle(t,unit)+'='+split
    if difficulty=='hard' and shape!='radio':
        raise ValueError('The imported unhinted hard anchor uses radio response')
    if shape=='blank':
        prompt=f'Using the fact that ${eq}$, calculate the **exact** value of ${target}$ without a calculator.\n\n${target}=$ {{{{field-1}}}}'
    else:
        prompt=f'What is the exact value of ${target}$ without using a calculator?'
        if difficulty!='hard': prompt+=f'\n\n*Hint: Use the fact that ${eq}$.*'
    formula=r'\sin(x'+symbol+r'y)=\sin x\cos y'+symbol+r'\cos x\sin y'
    expansion=trig('sin',a,unit)+trig('cos',b,unit)+symbol+trig('cos',a,unit)+trig('sin',b,unit)
    def par(s):return r'\left('+s+r'\right)' if s.startswith('-') else s
    substitution=par(ratio(SIN[a]))+r'\cdot '+par(ratio(COS[b]))+symbol+par(ratio(COS[a]))+r'\cdot '+par(ratio(SIN[b]))
    signed_products=single(p)+('+' if q[0]>0 else '-')+single((1,q[1]))
    final=combined(p,q)
    steps=[r'\sin\left('+split+r'\right)',expansion,substitution,signed_products,final]
    solution=f'Write the angle as a sum or difference of special angles: ${eq}$.\n\nRecall the '+('sum' if op==1 else 'difference')+f' formula for sine:\n\n$${formula}$$\n\nSubstitute the signed unit-circle values, multiply, and combine:\n\n$$\n'+r'\begin{aligned}'+target+' &='+steps[0]+''.join(r' \\ &='+s for s in steps[1:])+r'\end{aligned}'+'\n$$'
    if shape=='radio':
        values=[combined((sp,p[1]),(sq,q[1])) for sp in (-1,1) for sq in (-1,1)]
        values.append(single(profile))
    else: values=[final]
    if replay_profile: values=source_values(inst,replay_profile)
    values=[normalize_tex(v) for v in values]
    final=normalize_tex(final);prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    # Content identity uses normalized prose and a complete unordered bank.
    payload=json.dumps([difficulty,shape,prompt,solution,sorted(values)],ensure_ascii=False)
    identity=hashlib.sha256(payload.encode()).hexdigest()
    fieldid=uid(identity+'/field'); key='field-1' if shape=='blank' else 'selection'
    choices=[{':answer/id':uid(fieldid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    random.Random(order_seed).shuffle(choices)
    field={':answer-field/id':fieldid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+shape,
           ':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fieldid+'/'+final)]}
    question={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+difficulty,
              ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]}
    return validate_generated_record({'knowledge_point':{'db_id':17592186059663,'id':KP},'question':question,
        'generation':{'version':'2.0.0','template':('guided-' if difficulty!='hard' else 'unhinted-')+shape,
            'source_question_ids':SOURCES[difficulty],'parameters':{'a':a,'b':b,'op':op,'target':t,'unit':unit},
            'profile':replay_profile or ('sign-grid/omit-'+str(profile[0])+'-sqrt'+str(profile[1]) if shape=='radio' else 'exact-entry'),
            'product_case':list(inst['case']),'domain':'real exact constants'}})


def source_values(inst,profile):
    """Extracted observed error profiles, used only for original-parameter replay.

    The hard mixed radical/denominator error has an unresolved cognitive cause;
    its observed expression transformation is retained, not relabelled as fact.
    """
    p,q=inst['p'],inst['q']
    correct=combined(p,q)
    wrongop=combined(p,(-q[0],q[1]))
    def neg(v):return '-'+r'\left('+v+r'\right)'
    def twice(v):return '2'+r'\left('+v+r'\right)'
    if profile=='source-easy-sum':
        return [wrongop,twice(correct),correct.replace(r'\sqrt{6}',r'\sqrt{3}'),twice(neg(wrongop)),correct]
    if profile=='source-easy-difference':
        return [neg(wrongop),neg(correct),correct,twice(single(p)),twice(single(q))]
    if profile=='source-moderate-negative':
        return [single(q),wrongop,neg(correct),correct,correct.replace(r'\sqrt{6}',r'\sqrt{3}')]
    if profile=='source-hard-sum':
        return [wrongop,correct,twice(wrongop.replace(r'\sqrt{2}',r'\sqrt{3}')),
                correct.replace(r'\sqrt{6}',r'\sqrt{3}'),correct.replace(r'\sqrt{6}','1')]
    raise ValueError(profile)


def semantic(it):
    a,b,op=it['a'],it['b'],it['op']
    return (min(a,b),max(a,b),op) if op==1 else (a,b,op)


def generate(difficulty,count,seed):
    if count<0: raise ValueError('count must be nonnegative')
    rng=random.Random(seed); all_items=catalog()
    if difficulty=='easy':
        all_items=[it for it in all_items if (it['a']<90 and it['b']<90) or (it['a']==210 and it['b']==45 and it['op']==-1)]
    capacity=len({it['target'] for it in all_items}) if difficulty=='hard' else len({semantic(it) for it in all_items})
    if count>capacity:raise ValueError(f'{difficulty} supports {capacity} mathematical instances; requested {count}')
    cases=sorted({it['case'] for it in all_items});rng.shuffle(cases)
    records=[]; used=set(); cursor=0
    last_slots={}; rank_coverage=defaultdict(set); case_coverage=defaultdict(set)
    profiles=[(sign,rad) for sign in (-1,1) for rad in (2,6)]
    def visible_groups(item,profile,shape='radio'):
        groups=[shape,(shape,'target-sign',item['target']<0)]
        if shape=='radio': groups.append(('single-term',profile))
        if difficulty!='hard': groups.append((shape,'hint-operation',item['op']))
        return groups
    def bank_rank(item,profile):
        value=sum(sign*math.sqrt(rad) for sign,rad in (item['p'],item['q']))/4
        bank=[(x*math.sqrt(6)+y*math.sqrt(2))/4 for x in (-1,1) for y in (-1,1)]
        bank.append(profile[0]*math.sqrt(profile[1])/4)
        return sum(x<value for x in bank)

    # Cover the four sign cases, skipping exhausted groups; choose compatible
    # values only after choosing the case. Never stall on an exhausted case.
    while len(records)<count:
        selected=None
        for offset in range(len(cases)):
            case=cases[(cursor+offset)%len(cases)]
            shape=('blank' if (len(records)//4+len(records)%4)%2==0 else 'radio') if difficulty=='moderate' else 'radio'
            def signature(it):
                return (it['target'],) if difficulty=='hard' else semantic(it)
            pool=[it for it in all_items if it['case']==case and signature(it) not in used]
            if pool:
                if shape=='radio':
                    pairs=[(item,profile) for item in pool for profile in profiles]
                    # A repeated printed-sign, hint or complete-bank subgroup
                    # must not teach a fixed numerical rank. Once its ranks
                    # differ, all its mathematically eligible instances remain.
                    varied=[(item,profile) for item,profile in pairs
                            if all(rank_coverage[group]!={bank_rank(item,profile)}
                                   and case_coverage[group]!={item['case']}
                                   for group in visible_groups(item,profile))]
                    selected,profile=rng.choice(varied or pairs)
                else:
                    varied=[item for item in pool if all(case_coverage[group]!={item['case']}
                            for group in visible_groups(item,None,shape))]
                    selected=rng.choice(varied or pool);profile=(1,2)
                used.add(signature(selected));cursor=(cursor+offset+1)%len(cases);break
        if selected is None:
            # The source-supported semantic family is finite. Repeated requests
            # replay the completed cycle; deduplication may reduce very big pools.
            raise ValueError('Finite mathematical family exhausted; reduce count')
        record=build(selected,difficulty,shape=shape,profile=profile,order_seed=rng.getrandbits(64))
        for group in visible_groups(selected,profile,shape):
            case_coverage[group].add(selected['case'])
        if shape=='radio':
            # Independent shuffles can accidentally make a whole small batch
            # answerable from target sign or hint layout. Vary ordinal slots
            # within each repeated visible group without changing its math bank.
            groups=visible_groups(selected,profile)
            rank=bank_rank(selected,profile)
            for group in groups: rank_coverage[group].add(rank)
            forbidden={last_slots[group] for group in groups if group in last_slots}
            allowed=[slot for slot in range(5) if slot not in forbidden]
            slot=rng.choice(allowed) # at most four preceding slots are excluded
            field=record['question'][':question/answer-fields'][0]
            choices=field[':answer-field/choices'];correct=field[':answer-field/correct'][1]
            answer=next(choice for choice in choices if choice[':answer/id']==correct)
            choices.remove(answer);choices.insert(slot,answer)
            for group in groups: last_slots[group]=slot
        record['generation'].update({'seed':seed,'index':len(records),'mathematical_capacity':capacity,'calibration':'imported unhinted single-identity family' if difficulty=='hard' else 'imported supplied-split family; overlapping arithmetic demand'})
        records.append(record)
    return records


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate')
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json');args=parser.parse_args()
    print(json.dumps(generate(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
