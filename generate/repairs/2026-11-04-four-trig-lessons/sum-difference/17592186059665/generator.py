#!/usr/bin/env python3
"""Seeded cosine-shift practice. Runtime is relocatable and standard-library only."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from itertools import combinations
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186059665,'id':'831f9aa0-099e-5e0c-8a9d-c4828b629f64','title':'Simplifying Expressions in Radians Using the Sum and Difference Formulas'}
NS = uuid.UUID('84fa9977-edf7-4bda-8426-69362bba373d')
AXIS = (6,12,18)  # units pi/12
NONAXIS = (2,3,4,8,9,10,14,15,16,20,21,22)
# Exact (cosine, sine) values; arithmetic here is signs and selection only.
H=r'\frac{1}{2}'; R=r'\frac{\sqrt{3}}{2}'; Q=r'\frac{\sqrt{2}}{2}'
VALUES={2:(R,H),3:(Q,Q),4:(H,R),6:('0','1'),8:('-'+H,R),9:('-'+Q,Q),10:('-'+R,H),12:('-1','0'),14:('-'+R,'-'+H),15:('-'+Q,'-'+Q),16:('-'+H,'-'+R),18:('0','-1'),20:(H,'-'+R),21:(Q,'-'+Q),22:(R,'-'+H),24:('1','0')}

def uid(s): return str(uuid.uuid5(NS,s))
def neg(s): return s[1:] if s.startswith('-') else ('0' if s=='0' else '-'+s)
def angle(k):
    from fractions import Fraction
    f=Fraction(k,12)
    n=(str(f.numerator) if f.numerator!=1 else '')+r'\pi'
    return n if f.denominator==1 else r'\frac{'+n+'}{'+str(f.denominator)+'}'
def term(c,fn,v):
    if c=='0': return ''
    if c=='1': return '\\'+fn+' '+v
    if c=='-1': return '-\\'+fn+' '+v
    return c+'\\'+fn+' '+v

def expression(pair,v):
    # pair is (sine coefficient, cosine coefficient), exactly the output order.
    terms=[term(pair[0],'sin',v),term(pair[1],'cos',v)]
    out=''
    for t in filter(None,terms): out+=t if not out or t.startswith('-') else '+'+t
    return out or '0'

def derivation(k,sign,v,final):
    a=angle(k); c,s=VALUES[k]; op='-' if sign=='+' else '+'
    expr=r'\cos\left('+v+sign+a+r'\right)'
    formula=r'\cos(u'+sign+r'v)=\cos u\cos v'+op+r'\sin u\sin v'
    rows=[expr+'&=\\cos '+v+r'\cos\left('+a+r'\right)'+op+'\\sin '+v+r'\sin\left('+a+r'\right)',
          r'&=\cos '+v+r'\cdot\left('+c+r'\right)'+op+r'\sin '+v+r'\cdot\left('+s+r'\right)', '&='+final+'.']
    solution=('Use the '+('sum' if sign=='+' else 'difference')+' formula:\n\n$$\n'+formula+'\n$$\n\n'
              'With $u='+v+'$ and $v='+a+'$, the exact values are $\\cos('+a+')='+c+'$ and $\\sin('+a+')='+s+'$. Substitute and collect the terms in the requested order:\n\n$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$')
    return expr,formula,solution

def clean_record(problem,solution,difficulty,fields,meta):
    problem=normalize_prose(problem); solution=normalize_prose(solution)
    # Content identity excludes seed and metadata, after canonical formatting.
    content=[problem,solution,difficulty,[(f[':answer-field/key'],f[':answer-field/type'],[normalize_tex(a) for a in f['values']],normalize_tex(f['correct'])) for f in fields]]
    digest=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    fs=[]
    for f in fields:
        key=f[':answer-field/key']; vals=[normalize_tex(s) for s in f['values']]
        choices=[{':answer/id':uid(digest+key+s),':answer/type':':answer.type/math',':answer/value':s} for s in vals]
        correct=next(a for a in choices if a[':answer/value']==normalize_tex(f['correct']))
        fs.append({':answer-field/id':uid(digest+key),':answer-field/key':key,':answer-field/type':f[':answer-field/type'],':answer-field/choices':choices,':answer-field/correct':correct})
    q={':question/id':uid(digest),':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fs}
    return validate_generated_record({'knowledge_point':KP.copy(),'question':q,'generation':{'version':'2.0.0',**meta}})

def field(key,values,correct,kind='blank'):
    return {':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,'values':values,'correct':correct}

def error_pool(pair):
    """Complete authored error candidates, with their concrete misconception."""
    s,c=pair
    candidates=[((neg(s),c),'wrong sum/difference product sign'),((s,neg(c)),'wrong quadrant sign for cosine'),((neg(s),neg(c)),'wrong quadrant signs for both values'),((c,s),'swap exact sine/cosine values')]
    # Confusion among the three familiar reference angles, with quadrant signs retained.
    for ss,cc in [(H,R),(R,H),(Q,Q)]:
        candidates.append(((('-' if s.startswith('-') else '')+ss,('-' if c.startswith('-') else '')+cc),'confuse special-angle values'))
    out=[]; seen={pair}
    for p,why in candidates:
        if p not in seen: out.append((p,why)); seen.add(p)
    return out

def error_profiles(pair):
    """Plausible five-choice banks without a unique modal coefficient cue.

    A bank-only intersection of modal signed sine and cosine coefficients must
    leave several candidates. Screen complete profiles before option shuffling;
    every retained error still comes from this instance's misconception pool.
    """
    profiles=[]
    for errors in combinations(error_pool(pair),4):
        bank=[pair]+[p for p,_ in errors]
        sine=Counter(p[0] for p in bank); cosine=Counter(p[1] for p in bank)
        modes=[p for p in bank if sine[p[0]]==max(sine.values())
               and cosine[p[1]]==max(cosine.values())]
        if len(modes)!=1: profiles.append(errors)
    if not profiles: raise ValueError('No plausible distractor profile without a modal cue')
    return profiles

def make(difficulty,k,sign,v='x',shape=None,rng=None):
    rng=rng or random.Random(0)
    c,s=VALUES[k]; pair=(neg(s) if sign=='+' else s,c)
    final=expression(pair,v)
    expr,formula,solution=derivation(k,sign,v,final)
    lead='Express $'+expr+'$ in terms of $\\sin '+v+'$ '+('or' if k in AXIS else 'and')+' $\\cos '+v+'$.'
    meta={'parameters':{'angle_twelfths':k,'sign':sign,'variable':v},'domain':'variable real','support':'none','source_ids':['28e9089c-6417-5772-a8b3-173523505655'] if difficulty=='easy' else (['e50bbccc-38f5-586c-b552-2dd92be5a0c5','e3548f46-5f5c-5c9e-84fc-d32069c883d1'] if difficulty=='moderate' else ['31d126d7-a9c2-531e-862e-71990d0a9843','8f2cac98-d46c-5a68-832a-abb863407c09','41eed040-077a-55d8-92c4-de5f3f09a7a2'])}
    if difficulty=='easy':
        assert k in AXIS
        problem=lead
        vals=['\\sin '+v,'-\\sin '+v,'\\cos '+v,'-\\cos '+v,'0']; rng.shuffle(vals)
        fields=[field('selection',vals,final,'radio')]; shape='axis-radio'
    elif difficulty=='moderate':
        assert k in AXIS
        problem=lead+'\n\n$'+expr+'=$ {{field-1}}'
        fields=[field('field-1',[final],final)]; shape='axis-expression'
    else:
        assert k in NONAXIS
        shape=shape or rng.choice(['radio','coefficients'])
        if shape=='radio':
            # Select a complete five-option error profile before ordering its choices.
            errors=rng.choice(error_profiles(pair))
            vals=[final]+[expression(p,v) for p,_ in errors]; rng.shuffle(vals)
            problem=lead; fields=[field('selection',vals,final,'radio')]
            meta['error_profile']=[{'value':expression(p,v),'mistake':why} for p,why in errors]
        else:
            problem=lead+' Enter the signed coefficients.\n\n$'+expr+'=$ {{field-1}} $\\sin '+v+'\\,+$ {{field-2}} $\\cos '+v+'$'
            fields=[field('field-1',[pair[0]],pair[0]),field('field-2',[pair[1]],pair[1])]
    meta['template']=shape
    meta['displayed_final']=final
    return clean_record(problem,solution,difficulty,fields,meta)

def replay_sources():
    """Original parameters/full banks retained, with canonical formatting and owned IDs."""
    raw=json.loads(Path(__file__).with_name('source-cases.json').read_text())
    records=[]
    for q in raw:
        fields=[]
        for f in q[':question/answer-fields']:
            kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
            fields.append(field(f[':answer-field/key'],[a[':answer/value'] for a in f[':answer-field/choices']],f[':answer-field/correct'][':answer/value'],kind))
        records.append(clean_record(q[':question/problem'],q[':question/worked-solution'],q[':question/difficulty'][':db/ident'].split('/')[-1],fields,{'template':'source-replay','source_ids':[q[':question/id']]}))
    return records

def generate(difficulty,count,seed):
    if count<0: raise ValueError('count must be nonnegative')
    rng=random.Random(seed); out=[]
    angles=AXIS if difficulty!='hard' else NONAXIS
    capacity=2*len(angles)
    if count>capacity:raise ValueError(f'{difficulty} supports {capacity} mathematical shifts; requested {count}')
    # Each deck varies mathematical decisions before names and option presentation.
    while len(out)<count:
        deck=[(k,s) for k in angles for s in ['+','-']]; rng.shuffle(deck)
        for k,s in deck:
            shape=None if difficulty!='hard' else rng.choice(['radio','coefficients'])
            record=make(difficulty,k,s,'x',shape,rng)
            record['generation'].update(seed=seed,index=len(out),catalog_cycle=len(out)//len(deck),calibration='authored overlapping axis band; no easy imported anchor' if difficulty=='easy' else 'imported same-skill family')
            out.append(record)
            if len(out)==count: break
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate'); ap.add_argument('--count',type=int,default=5); ap.add_argument('--seed',type=int,default=0); ap.add_argument('--format',choices=['json'],default='json'); ap.add_argument('--replay-source',action='store_true'); a=ap.parse_args()
    records=replay_sources() if a.replay_source else generate('moderate' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
