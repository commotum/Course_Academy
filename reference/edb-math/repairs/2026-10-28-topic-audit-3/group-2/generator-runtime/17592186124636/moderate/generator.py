#!/usr/bin/env python3
"""Seeded real-domain practice; runtime uses only the Python standard library."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import random
import re
from collections import Counter
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186124636, 'id':'0e593685-f5ca-5501-94bf-7cb4d49e935b',
      'title':'The Domain of a Function Involving Reciprocals and Radicals'}
EXPRS = {'x':'x', 'y':'y', 'sum':'x+y', 'diff':'x-y', 'linear':'2x+y',
         'radial':'x^2+y^2', 'hyperbola':'x^2-y^2', 'product':'xy',
         'square':'x^2', 'cube':'x^3', 'parabola':'y-x^2', 'cubicline':'2x^3-y'}
REL = {'ne':r'\ne', 'ge':r'\ge', 'le':r'\le', 'gt':'>', 'lt':'<', 'eq':'='}
SOURCES = {'rational':['83b99b1c-0bfd-5266-a9a8-e11b90bb0b2b','5a5f0a19-c9e6-5cb8-90ec-d158940d83f6'],
 'numroot':['5a22a64f-170d-5095-a7c1-d8735a6757c8','44bfd95c-9ee8-5b8e-91af-f8c6e58bbec3','0f0c6fb0-68b0-537c-ab8d-954592bf8ad5'],
 'denroot':['8022d60c-ad02-52ea-a2bc-6bcc108f5f02','7c169bcc-a581-55f9-b4fe-8fe294bcd657'],
 'bothroots':['c17e17b4-eb53-578b-9ce8-45c6b1ef40c4','cbb2ddad-ba55-5c7d-8280-316182c4f2ac'],
 'shifted':['4312adfd-d331-5073-842a-15da34b52fee','fa7bd088-d496-5862-80a0-cd20083b2754']}

def expr(name, swap=False):
    text=EXPRS[name]
    return text.translate(str.maketrans('xy','yx')) if swap else text

def evaluate(name,x,y,swap=False):
    if swap:x,y=y,x
    return {'x':lambda:x,'y':lambda:y,'sum':lambda:x+y,'diff':lambda:x-y,
      'linear':lambda:2*x+y,'radial':lambda:x*x+y*y,'hyperbola':lambda:x*x-y*y,
      'product':lambda:x*y,'square':lambda:x*x,'cube':lambda:x*x*x,
      'parabola':lambda:y-x*x,'cubicline':lambda:2*x*x*x-y}[name]()

def offset(e,t):
    return e + (('+'+str(-t)) if t<0 else ('-'+str(t)) if t else '')

def radicand(e,t,sign):
    if sign==1:return offset(e,t)
    # Preserve the input grouping when negating a multi-term expression.
    return str(t)+'-\\left('+e+'\\right)'

def cond(e,op,t,swap=False):return {'expr':e,'op':op,'rhs':t,'swap':swap}
def condition_tex(c):return expr(c['expr'],c['swap'])+REL[c['op']]+str(c['rhs'])
def domain(cs):
    if len(cs)>=3:
        rows=[expr(c['expr'],c['swap'])+' &'+REL[c['op']]+str(c['rhs']) for c in cs]
        return r'\left\{(x,y)\in\mathbb R^2\,:\,\begin{aligned}'+r'\\'.join(rows)+r'\end{aligned}\right\}'
    return r'\{(x,y)\in\mathbb R^2\,:\,'+(r',\ '.join(map(condition_tex,cs)) if cs else r'\text{no restrictions}')+r'\}'
def truth(cs,x,y):
    for c in cs:
        z=evaluate(c['expr'],x,y,c['swap'])-c['rhs']; eq=abs(z)<1e-8
        if not {'ne':not eq,'ge':z>=-1e-8,'le':z<=1e-8,'gt':z>1e-8,'lt':z<-1e-8,'eq':eq}[c['op']]:return False
    return True

def witnesses():
    vals=[i/2 for i in range(-16,17)]+[a*math.sqrt(n) for n in range(1,21) for a in [-1,1]]
    points=[(x,y) for x in vals for y in [-3,-2,-1,0,1,2,3]]
    points += [(y,x) for x,y in points]
    # Points on shifted radial levels and parabolic boundaries.
    points += [(a*math.sqrt(n-y*y),y) for n in range(1,26) for y in [-2,-1,0,1,2] if n>=y*y for a in [-1,1]]
    points += [(x,x*x) for x in [-2,-1,0,1,2]]
    return points
POINTS=witnesses()
def signature(cs):return bytes(truth(cs,*p) for p in POINTS)

def aligned(rows):return '$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'

def make_instance(level,rng,case=None,overrides=None):
    p={'level':level,'swap':rng.choice([False,True]),'numerator':rng.choice(['x+y','x^2+y','1','2x+y'])}
    if level=='easy':
        names=['linear','sum','diff','product','radial','hyperbola','square','cube']
        p.update(profile='rational',e=case or rng.choice(names),t=rng.choice([-2,-1,0,1,2]),squared=False)
        if p['e'] in ['radial','square']:p['t']=rng.choice([0,1,4])
        if p['e'] in ['sum','diff']:p['squared']=rng.choice([False,True])
    elif level=='moderate':
        p.update(profile=case or rng.choice(['numroot','denroot','bothroots']),e=rng.choice(['x','y','diff','parabola']),t=rng.choice([-1,0,1]),s=rng.choice([-1,1]),d=rng.choice(['radial','linear','cubicline']),b=rng.choice([1,2,4]),ds=rng.choice([-1,1]))
    else:
        sign,orientation=case if case else (rng.choice([-1,1]),rng.choice([-1,1]))
        p.update(profile='shifted',e=rng.choice(['x','y','diff']),t=0,s=rng.choice([-1,1]),d='radial',b=rng.choice([4,9]),ds=orientation,k=sign*rng.choice([1,2]))
        # Interior excluded circle must exist. Addition branch shares these instances.
        if p['b']==4 and abs(p['k'])==2:p['k']=sign
    p['bank_profile']=rng.choice(['local','paired'])
    if overrides:p.update(overrides)
    return p

def derive(p):
    sw=p['swap'];e=expr(p['e'],sw);t=p['t'];profile=p['profile']
    options=[];rows=[];notes=[]
    if profile=='rational':
        den=offset(e,t)
        if p['squared']:den=r'\left('+den+r'\right)^2'
        form=r'\dfrac{'+p['numerator']+'}{'+den+'}'
        key=[cond(p['e'],'ne',t,sw)]
        rows=[den+r'&\ne 0'+(r'\quad\Longleftrightarrow\quad '+e+r'\ne '+str(t) if den!=e else '')]
        notes=['The numerator is a polynomial and imposes no restriction. The complete denominator must be nonzero.']
        options=[([cond(p['e'],op,u,sw)],why) for op,u,why in [('eq',t,'selects the forbidden locus'),('gt',t,'requires a positive denominator'),('lt',t,'requires a negative denominator'),('ne',t+1,'moves the excluded locus'),('ne',t-1,'moves the excluded locus in the other direction')]]
        other='sum' if p['e']!='sum' else 'diff'
        options += [([cond(other,'ne',t,sw)],'changes the polynomial in the restriction'),([], 'ignores the denominator')]
    else:
        nr=radicand(e,t,p['s']);nc=cond(p['e'],'ge' if p['s']==1 else 'le',t,sw)
        d=expr(p['d'],sw);b=p['b'];dr=radicand(d,b,p['ds'])
        dc=cond(p['d'],'ge' if p['ds']==1 else 'le',b,sw)
        strict=cond(p['d'],'gt' if p['ds']==1 else 'lt',b,sw)
        if profile=='numroot':
            den=offset(d,b);form=r'\dfrac{\sqrt{'+nr+'}}{'+den+'}'
            dc=cond(p['d'],'ne',b,sw);key=[nc,dc]
            notes=['The numerator radicand must be nonnegative, and the polynomial denominator must be nonzero. A zero numerator is allowed.']
            rows=[nr+r'&\ge 0\quad\Longleftrightarrow\quad '+condition_tex(nc),den+r'&\ne 0\quad\Longleftrightarrow\quad '+condition_tex(dc)]
        elif profile=='denroot':
            form=r'\dfrac{'+p['numerator']+r'}{\sqrt{'+dr+'}}';key=[strict]
            notes=['The numerator is a polynomial. The denominator radicand must be nonnegative and its square root must be nonzero, so the radicand must be strictly positive.']
            rows=[dr+r'&>0\quad\Longleftrightarrow\quad '+condition_tex(strict)]
        elif profile=='bothroots':
            form=r'\dfrac{\sqrt{'+nr+r'}}{\sqrt{'+dr+'}}';key=[nc,strict];dc=strict
            notes=['The numerator radicand may equal zero. The denominator radicand must be strictly positive, since its square root is the complete denominator.']
            rows=[nr+r'&\ge 0\quad\Longleftrightarrow\quad '+condition_tex(nc),dr+r'&>0\quad\Longleftrightarrow\quad '+condition_tex(strict)]
        else:
            k=p['k'];den=offset(r'\sqrt{'+dr+'}',k)
            form=r'\dfrac{\sqrt{'+nr+'}}{'+den+'}';key=[nc,dc]
            notes=['Both radicands must be nonnegative. The complete shifted denominator must also be nonzero.']
            rows=[nr+r'&\ge 0\quad\Longleftrightarrow\quad '+condition_tex(nc),dr+r'&\ge 0\quad\Longleftrightarrow\quad '+condition_tex(dc)]
            excluded=cond(p['d'],'ne',b+p['ds']*k*k,sw)
            if k>0:
                key.append(excluded)
                rows += [den+r'&=0',r'\sqrt{'+dr+'}&='+str(k),dr+'&='+str(k*k),d+'&='+str(excluded['rhs'])]
                notes += ['The right side of the root equation is positive, so squaring is reversible. Exclude this level set. The radicand-zero boundary remains allowed wherever the numerator is real, since the denominator there is $'+str(-k)+'$.']
            else:
                rows += [den+r'&\ge '+str(-k)+'>0']
                notes += ['A principal square root is nonnegative. This denominator is always positive on the real-radicand region, so it has no zero to exclude. Squaring an equation with a negative right side would create extraneous points.']
            options += [([nc,dc]+([] if k>0 else [excluded]),'ignores the excluded level or squares a negative-root equation'),([nc,strict]+([excluded] if k>0 else []),'incorrectly excludes the radicand-zero boundary')]
            for u in [b-p['ds']*k*k,b+p['ds']*abs(k),k*k]:
                options.append(([nc,dc,cond(p['d'],'ne',u,sw)],'uses an incorrect excluded level'))
        # Whole-bank variants: alter one or both conditions. These are errors,
        # not arbitrary values added to the correct answer.
        for i,c in enumerate(key):
            for op in ['ge','gt','le','lt','ne','eq']:
                if op==c['op']:continue
                cs=copy.deepcopy(key);cs[i]['op']=op
                options.append((cs,'uses the wrong inequality or boundary for condition '+str(i+1)))
            cs=copy.deepcopy(key);cs[i]['rhs']+=1
            options.append((cs,'shifts boundary '+str(i+1)))
            cs=copy.deepcopy(key);cs.pop(i)
            options.append((cs,'omits condition '+str(i+1)))
        if len(key)>1:
            for op1,op2 in [('gt','ne'),('le','gt'),('ge','lt'),('lt','le')]:
                cs=copy.deepcopy(key);cs[0]['op']=op1;cs[1]['op']=op2
                options.append((cs,'misapplies both operation restrictions'))
        options.append(([],'ignores all operation restrictions'))
    return form,key,options,notes,rows

def uid(text):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/domain/v1/'+text))

def build(p,rng):
    form,key,candidates,notes,rows=derive(p)
    if p.get('bank_profile')=='paired' and len(key)>1:
        # A coherent pair of misconceptions: make the numerator boundary strict
        # or reverse its half-plane, and independently mishandle denominator sign.
        preferred=[]
        for op1 in (['gt','le'] if key[0]['op']=='ge' else ['lt','ge']):
            for op2 in [key[1]['op'], ('gt' if key[1]['op']=='ne' else 'ne')]:
                cs=copy.deepcopy(key);cs[0]['op']=op1;cs[1]['op']=op2
                preferred.append((cs,'paired numerator-boundary and denominator-region errors'))
        rng.shuffle(preferred)
    else:preferred=[]
    ks=signature(key);seen={ks};eligible=[]
    rng.shuffle(candidates)
    for cs,why in preferred+candidates:
        sig=signature(cs)
        if sig in seen or not any(sig):continue
        seen.add(sig);eligible.append((cs,why))
    if len(eligible)<4:raise ValueError('Not enough distinct nonempty error alternatives')
    # Sample a complete bank, rather than four paired errors which make the
    # correct numerator relation a uniquely occurring singleton (2,2,1).
    # Every multirestriction bank must contain another candidate with the
    # correct first relation. Also reject a unique modal-token giveaway.
    for bank_attempt in range(2000):
        errors=rng.sample(eligible,4)
        if len(key)>1 and not any(cs and cs[0]['op']==key[0]['op'] for cs,_ in errors):
            continue
        trial=[(key,'correct')]+errors
        lengths=[len(domain(cs)) for cs,_ in trial]
        if len(key)>1 and (lengths[0]>max(lengths[1:]) or lengths[0]<min(lengths[1:])):
            continue
        tokens=[set(re.findall(r'\\[A-Za-z]+|-?\d+|[xy]|[<>=]',domain(cs))) for cs,_ in trial]
        frequencies=Counter(token for ts in tokens for token in ts)
        scores=[sum(frequencies[token] for token in ts) for ts in tokens]
        if len(key)>1 and scores.count(max(scores))==1 and scores[0]==max(scores):
            continue
        bank=trial
        break
    else:
        raise ValueError('Cannot construct a plausible bank without incidental cues')
    rng.shuffle(bank)
    if 'position' in p:
        current=next(i for i,(_,why) in enumerate(bank) if why=='correct')
        bank.insert(p['position'],bank.pop(current))
    problem=normalize_prose('Find the domain of the function $f(x,y)='+form+'$.')
    solution=normalize_prose('\n\n'.join(notes[:1])+ '\n\n'+aligned(rows)+'\n\n'+'\n\n'.join(notes[1:])+'\n\nTherefore, the domain is\n\n$$\n'+domain(key)+'.\n$$')
    values=[normalize_tex(domain(cs)) if cs else 'The domain is the entire $xy$-plane.' for cs,_ in bank]
    identity=json.dumps([problem,solution,values],sort_keys=True)
    qid=uid(identity)
    answers=[{':answer/id':uid(qid+'/choice/'+str(i)),':answer/type':':answer.type/math' if cs else ':answer.type/text',':answer/value':v} for i,((cs,_),v) in enumerate(zip(bank,values))]
    correct=next(i for i,(_,why) in enumerate(bank) if why=='correct')
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+p['level'],':question/requires-calculator':False,
       ':question/answer-fields':[{':answer-field/id':uid(qid+'/field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]}]}
    record={'knowledge_point':KP,'question':q,'generation':{'version':'1.0.0','parameters':p,'profile':p['profile'],'source_ids':SOURCES[p['profile']], 'choice_errors':[why for cs,why in bank], 'ordered_path':{'conditions':[condition_tex(c) for c in key],'rows':rows,'final':normalize_tex(domain(key))}}}
    return validate_generated_record(record)

def semantic_key(p):
    active={'rational':['e','t','swap','squared'], 'numroot':['e','t','s','d','b','swap'], 'denroot':['d','b','ds','swap'], 'bothroots':['e','t','s','d','b','ds','swap'], 'shifted':['e','t','s','d','b','ds','k','swap']}
    return json.dumps([p['profile'],{k:p[k] for k in active[p['profile']]}],sort_keys=True)

def generate(difficulty,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    if difficulty=='unclassified':difficulty='moderate'
    rng=random.Random(seed)
    cases={'easy':['linear','sum','diff','product','radial','hyperbola','square','cube'], 'moderate':['numroot','denroot','bothroots'], 'hard':[(a,b) for a in [-1,1] for b in [-1,1]]}[difficulty][:]
    rng.shuffle(cases);records=[];seen=set();attempt=0;positions={};occurrences={}
    while len(records)<count:
        p=make_instance(difficulty,rng,cases[len(records)%len(cases)])
        p['bank_profile']=['local','paired'][(len(records)//len(cases))%2]
        position_group=str((p['ds'],p['k']>0)) if difficulty=='hard' else p['profile']
        if position_group not in positions:
            pool=list(range(5));random.Random(str(seed)+'/positions/'+position_group).shuffle(pool)
            positions[position_group]=pool;occurrences[position_group]=0
        p['position']=positions[position_group][occurrences[position_group]%5]
        rec=build(p,rng);semantic=semantic_key(p)
        attempt+=1
        if semantic in seen:
            if attempt>count*100+100:raise RuntimeError('Unique instance exhaustion')
            continue
        seen.add(semantic);occurrences[position_group]+=1;rec['generation'].update(seed=seed,index=len(records));records.append(rec)
    return records

def replay():
    return json.loads((Path(__file__).parent/'source-replay.json').read_text())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay-source',action='store_true');a=ap.parse_args()
    print(json.dumps(replay() if a.replay_source else generate(a.difficulty,a.count,a.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
