#!/usr/bin/env python3
"""Seeded exact-tangent practice. See instructional-account.md for scope."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = '6b97e00a-b343-5b04-b475-3aaa038995ca'
NAMESPACE = uuid.UUID(KP)
SOURCES = json.loads(Path(__file__).with_name('source-banks.json').read_text())
ROOT3 = r'\sqrt{3}'
TANS = {30:(0,F(1,3)),45:(1,0),60:(0,1),120:(0,-1),135:(-1,0),150:(0,F(-1,3)),
        210:(0,F(1,3)),225:(1,0),240:(0,1),300:(0,-1),315:(-1,0),330:(0,F(-1,3))}
RESULTS = [(2,1),(2,-1),(-2,1),(-2,-1)]
EXTRAS = [r'\frac{\sqrt{3}}{2}', r'\sqrt{3} - 4', r'3 - \sqrt{3}',
          r'\frac{3\sqrt{3} - 2}{2}', r'\frac{\sqrt{3} - 2}{2}', r'-\sqrt{3}',
          r'-\frac{\sqrt{3} - 2}{2}']
EXTRA_VALUES = [(0,F(1,2)),(-4,1),(3,-1),(-1,F(3,2)),
                (-1,F(1,2)),(0,-1),(1,F(-1,2))]


def add(x,y): return (x[0]+y[0],x[1]+y[1])
def scale(x,k): return (x[0]*k,x[1]*k)
def mul(x,y): return (x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def rat(n):
    n=F(n)
    return str(n.numerator) if n.denominator==1 else rf'\frac{{{n.numerator}}}{{{n.denominator}}}'
def surd(x):
    a,b=map(F,x)
    text=rat(a) if a else ''
    if b:
        coeff='' if abs(b)==1 else rat(abs(b))
        term=coeff+ROOT3
        text += (' + ' if b>0 else ' - ') + term if text else ('-' if b<0 else '')+term
    return text or '0'
def par(t): return rf'\left({t}\right)'
def frac(n,d): return rf'\frac{{{n}}}{{{d}}}'
def angle(degrees,unit):
    if unit=='degrees': return rf'{degrees}^\circ'
    f=F(degrees,180)
    n=(str(f.numerator) if f.numerator!=1 else '')+r'\pi'
    return n if f.denominator==1 else frac(n,str(f.denominator))
def tan(t): return rf'\tan\left({t}\right)'
def align(rows): return '$$\n'+r'\begin{aligned}'+'\n'+(' \\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'
def uid(text): return str(uuid.uuid5(NAMESPACE,text))


def interval(value):
    number=float(value[0])+float(value[1])*math.sqrt(3)
    return (number>0,abs(number)<1)


def candidate_pool():
    """Shared complete-bank ingredients, with exact values and source lineage."""
    pool={}
    def put(value,recipe,refs=()):
        item=pool.setdefault(value,{'tex':surd(value),'recipes':[],'sources':set()})
        item['recipes'].append(recipe);item['sources'].update(refs)
    for value in RESULTS:
        put(value,'other exact tangent result')
        for factor in [F(1,2),2]:
            put(scale(value,factor),'lost factor of two: '+str(factor))
        for shift in [-1,1]:
            put(add(value,(shift,0)),'integer term off by one in expansion/reduction')
        put(scale(mul(value,value),1 if interval(value)[0] else -1),
            'squared magnitude instead of requested tangent, retaining quadrant sign')
    for tex,value in zip(EXTRAS,EXTRA_VALUES):
        refs=[s['ma_id'] for s in SOURCES if normalize_tex(tex) in map(normalize_tex,s['bank'])]
        put(value,'captured source distractor',refs)
        put(scale(value,-1),'source distractor with quadrant sign reversed',refs)
    return pool


def extension_bank(result,rng,bank_values=None):
    pool=candidate_pool()
    if bank_values is None:
        # A bank must be usable for two different target values. Construct it
        # symmetrically from the unordered pair, so option shapes and distractor
        # roles cannot identify which member is the answer without the prompt.
        partner=rng.choice([v for v in RESULTS if v!=result])
        pair=sorted([result,partner])
        errors=[v for v in pool if v not in RESULTS]
        selected=list(pair)
        for possible_key in pair:
            competing=[v for v in errors if interval(v)==interval(possible_key)
                       and r'\frac' not in pool[v]['tex']]
            selected.append(rng.choice(competing))
        selected.append(rng.choice([v for v in errors if v not in selected]))
    else:
        by_tex={normalize_tex(p['tex']):v for v,p in pool.items()}
        selected=[by_tex[normalize_tex(tex)] for tex in bank_values]
    if len(selected)!=5 or len(set(selected))!=5 or result not in selected:
        raise ValueError('Extension bank must contain five distinct values including the key')
    possible_keys=[v for v in selected if v in RESULTS]
    if len(possible_keys)<2:
        raise ValueError('Extension bank exposes the answer through the exact-value family')
    for possible_key in possible_keys:
        if sum(interval(v)==interval(possible_key) and r'\frac' not in pool[v]['tex']
               for v in selected)<2:
            raise ValueError('Every possible target needs a fraction-free interval competitor')
    if sum(interval(v)==interval(result) for v in selected)<2:
        raise ValueError('Extension bank exposes the answer through coarse tangent bounds')
    if sum(interval(v)==interval(result) and r'\frac' not in pool[v]['tex'] for v in selected)<2:
        raise ValueError('Extension bank exposes the answer through fraction typography')
    refs=set().union(*(pool[v]['sources'] for v in selected if v!=result))
    return [pool[v]['tex'] for v in selected],refs

def instance(x,y,op):
    s=1 if op=='+' else -1
    target=x+s*y
    u,v=TANS[x],TANS[y]
    n=add(u,scale(v,s)); d=add((1,0),scale(mul(u,v),-s))
    # Clear thirds in numerator and denominator before conjugate multiplication.
    factor=3 if any(F(z).denominator==3 for z in (*n,*d)) else 1
    n=scale(n,factor); d=scale(d,factor)
    conj=(d[0],-d[1]); expanded=mul(n,conj); denom=mul(d,conj)
    assert denom[1]==0 and denom[0]!=0
    result=scale(expanded,F(1,denom[0]))
    assert result in RESULTS
    return dict(x=x,y=y,op=op,target=target,u=u,v=v,n=n,d=d,conj=conj,
                expanded=expanded,denom=denom[0],result=result,factor=factor)


def catalog():
    rows=[]
    for x in TANS:
        for y in TANS:
            if (x%90==45)==(y%90==45): continue
            for op,s in [('+',1),('-',-1)]:
                if x+s*y not in [15,75,105,165,195,255,285,345]: continue
                for unit in ['degrees','radians']: rows.append((x,y,op,unit))
    return rows


def make(x,y,op,unit,rng=None,profile='extension',bank_values=None,seed=None):
    rng=rng or random.Random(0)
    p=instance(x,y,op)
    t,a,b=[angle(z,unit) for z in (p['target'],x,y)]
    u,v=map(surd,(p['u'],p['v']))
    opposite='-' if op=='+' else '+'
    formula=frac(r'\tan x '+op+r' \tan y',r'1 '+opposite+r' \tan x\tan y')
    n,d,c=map(surd,(p['n'],p['d'],p['conj']))
    final=surd(p['result'])
    prompt=f'What is the exact value of ${tan(t)}$?\n\n*Hint:* Use the fact that ${t} = {a} {op} {b}$.'
    substitution=frac(par(u)+' '+op+' '+par(v),'1 '+opposite+' '+par(u)+par(v))
    first=[tan(t)+' &= '+tan(a+' '+op+' '+b),
           '&= '+frac(tan(a)+' '+op+' '+tan(b),'1 '+opposite+' '+tan(a)+tan(b)),
           '&= '+substitution]
    name='sum' if op=='+' else 'difference'
    solution=f'Recall the {name} formula for tangent:\n\n$${tan("x "+op+" y")} = {formula}$$\n\n'
    solution+=f'Apply it with $x={a}$ and $y={b}$. The special-angle values are ${tan(a)}={u}$ and ${tan(b)}={v}$.\n\n'+align(first)
    if p['factor']==3:
        solution+='\n\nMultiply the numerator and denominator by $3$ to clear the fractions:\n\n'
        solution+=align([tan(t)+' &= '+frac('3'+par(par(u)+' '+op+' '+par(v)),'3'+par('1 '+opposite+' '+par(u)+par(v))), '&= '+frac(n,d)])
    else:
        solution+='\n\nCombining the terms gives\n\n'+align([tan(t)+' &= '+frac(n,d)])
    solution+='\n\nMultiply by the conjugate of the denominator, expand, and simplify:\n\n'
    solution+=align([tan(t)+' &= '+frac(n,d)+r'\cdot '+frac(c,c),
                     '&= '+frac(par(n)+par(c),par(d)+par(c)),
                     '&= '+frac(surd(p['expanded']),rat(p['denom'])),
                     '&= '+final])
    if profile=='extension':
        values,contributing_sources=extension_bank(p['result'],rng,bank_values)
        refs=[{'id':'e-3521','db_id':17592186059495},{'id':'2561','db_id':17592186060890}]
        # Include only standalone banks that contribute an actual distractor recipe.
        refs += [{'id':s['ma_id'],'db_id':s['db_id'],'uuid':s['uuid']} for s in SOURCES
                 if s['ma_id'] in contributing_sources]
    else:
        source=next(s for s in SOURCES if s['ma_id']==profile)
        if (x,y,op,unit)!=tuple(source['parameters']): raise ValueError('Source banks are replay-only profiles')
        values=source['bank']
        refs=[{'id':source['ma_id'],'db_id':source['db_id'],'uuid':source['uuid']},
              {'id':'e-3521','db_id':17592186059495},{'id':'2561','db_id':17592186060890}]
    values=list(map(normalize_tex,values)); rng.shuffle(values)
    # Normalize all learner content BEFORE creating content identities.
    prompt=normalize_prose(prompt); solution=normalize_prose(solution); final=normalize_tex(final)
    identity=json.dumps([prompt,solution,sorted(values)],ensure_ascii=False)
    qid=uid(identity); fid=uid(qid+'/selection')
    choices=[{':answer/id':uid(fid+'/'+z),':answer/type':':answer.type/math',':answer/value':z} for z in values]
    # Replay q-43382 uses -sqrt(3)-2 rather than the canonical -2-sqrt(3).
    correct_value=normalize_tex(next(s['key'] for s in SOURCES if s['ma_id']==profile)) if profile!='extension' else final
    correct=next(z[':answer/id'] for z in choices if z[':answer/value']==correct_value)
    record={'knowledge_point':{'db_id':17592186059664,'id':KP},
            'question':{':question/id':qid,':question/difficulty':':question.difficulty/moderate',
                        ':question/problem':prompt,':question/worked-solution':solution,
                        ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',
                        ':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,
                        ':answer-field/correct':[':answer/id',correct]}]},
            'generation':{'version':3,'seed':seed,'template':'hinted-exact-tangent','bank_profile':profile,
                          'parameters':{'x':x,'y':y,'operation':op,'unit':unit,'target':p['target']},
                          'result_class':[int(z) for z in p['result']], 'source_questions':refs,
                          'source_difficulty':None,'final_display':final,
                          'derivation':{'clears_thirds':p['factor']==3,'rationalizes':True}}}
    # Explicitly show the harmless term reorder if needed for source-bank replay.
    if correct_value!=final:
        record['question'][':question/worked-solution']=normalize_prose(solution+f'\n\nReordering the two terms gives ${final}={correct_value}$.')
        record['generation']['final_display']=correct_value
    return validate_generated_record(record)


def generate(count,seed,difficulty='moderate'):
    if difficulty=='unclassified': difficulty='moderate'
    if difficulty!='moderate': raise ValueError('Unsupported difficulty: '+difficulty)
    pool=defaultdict(list)
    for args in catalog(): pool[instance(*args[:3])['result']].append(args)
    if not 0<=count<=sum(map(len,pool.values())): raise ValueError('Count exceeds finite catalog of '+str(sum(map(len,pool.values()))))
    rng=random.Random(seed)
    for rows in pool.values(): rng.shuffle(rows)
    records=[]
    while len(records)<count:
        classes=[z for z in RESULTS if pool[z]]; rng.shuffle(classes)
        for key in classes:
            if len(records)==count: break
            records.append(make(*pool[key].pop(),rng=rng,seed=seed))
    return records


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--difficulty',required=True)
    ap.add_argument('--count',type=int,required=True)
    ap.add_argument('--seed',type=int,required=True)
    ap.add_argument('--format',choices=['json'],required=True)
    a=ap.parse_args()
    try: records=generate(a.count,a.seed,a.difficulty)
    except ValueError as e: ap.error(str(e))
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
