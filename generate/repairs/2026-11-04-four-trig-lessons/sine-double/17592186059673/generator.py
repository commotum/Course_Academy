#!/usr/bin/env python3
"""Seeded, relocatable double-angle ratio practice. No I/O except CLI JSON."""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = '5f9683d9-05b9-5a42-9f81-0170a15dfac1'
TITLE = 'Using the Double-Angle Formula to Simplify Ratios'
NS = uuid.UUID(KP)
SOURCES = {
 'direct':['dde407ba-34c3-55d5-a98c-cb0e2c5bb577','25afbebc-fd44-53f2-ab04-01a0bc5e8356','ceef643d-5955-5dc4-9610-8fc14edd1b2d'],
 'quotient':['95efa6da-7216-501c-8391-1e0cbd18db0c'],
 'inverse':['b2050e06-0476-56c1-a7a1-1d0ef234a4b2','11defe63-9b06-5fba-87b6-5807bf8b34d3','1a84df43-c63e-5997-bb62-0b42cedd5faa'],
 'square':['83d0963d-a8db-5840-a576-ccf3c21b5f89'],
 'product':['610fb667-dafb-57bd-85ea-670b2220cc0c'],
 'complement':['df53af64-a7fb-5920-a9ae-4765f5d7236c','20492e7a-2ad5-5346-9935-34abf42dcea6'],
 'binomial':['4eaa49cb-94d5-5c4a-8e77-4592aca20df1']}

def frac(a,b): return r'\frac{'+str(a)+'}{'+str(b)+'}'
def scale(k,t):
    k=Fraction(k)
    if k==1:return t
    if k==-1:return '-'+t
    return (str(k.numerator) if k.denominator==1 else frac(k.numerator,k.denominator))+t

def angle(p,m=1):
    if p['unit']=='deg': return str(p['angle']*m)+r'^\circ'
    f=Fraction(m,p['angle'])
    return (r'\pi' if f.numerator==1 else str(f.numerator)+r'\pi') if f.denominator==1 else frac((str(f.numerator) if f.numerator!=1 else '')+r'\pi', f.denominator)

def trig(f,a,power=1): return '\\'+f+(('^'+str(power)) if power!=1 else '')+r'\left('+a+r'\right)'

def derive(p):
    a,b=angle(p),angle(p,2)
    s,c=trig('sin',a),trig('cos',a)
    f=p['role']; g='cos' if f=='sin' else 'sin'
    F,G=trig(f,a),trig(g,a)
    fs,gs=('s','c') if f=='sin' else ('c','s')
    k=p.get('k',1); t=p.get('sign',1); sign='+' if t==1 else '-'
    D=trig('sin',b)
    fam=p['family']
    if fam in ('direct','product'):
        E=frac(D,scale(k,G)) if fam=='direct' else scale(Fraction(1,k),D+trig('sec' if g=='cos' else 'csc',a))
        key=scale(Fraction(2,k),F)
        steps=[frac('2sc',scale(k,gs)),scale(Fraction(2,k),fs),key]
        if fam=='product':steps.insert(0,scale(Fraction(1,k),'2sc'+frac(1,gs)))
        note='Expand the doubled sine and cancel the common factor.'
    elif fam=='quotient':
        q='cot' if f=='sin' else 'tan'
        E=frac(D,trig(q,a));key=scale(2,trig(f,a,2))
        steps=[frac('2sc',frac(gs,fs)),scale(2,fs+'^2'),key]
        note='Rewrite the quotient ratio before cancelling.'
    elif fam=='inverse':
        E=F+trig('csc',b) if p.get('product') else frac(F,D)
        h='sec' if f=='sin' else 'csc'
        key=scale(Fraction(1,2),trig(h,a))
        steps=[frac(fs,'2sc'),frac(1,'2'+gs),key]
        if p.get('product'):steps.insert(0,fs+frac(1,'2sc'))
        note='Expand the denominator, cancel, then use the reciprocal definition.'
    elif fam=='square':
        E=frac(D,trig(g,a,2));key=scale(2,trig('tan' if f=='sin' else 'cot',a))
        steps=[frac('2sc',gs+'^2'),frac('2'+fs,gs),key]
        note='Cancel one factor of the squared denominator, then rewrite the quotient.'
    elif fam=='complement':
        # role is the function occurring in the denominator's binomial.
        q='tan' if f=='cos' else 'cot'
        E=frac(D+trig(q,a),scale(k,r'\left(1'+sign+F+r'\right)'))
        B=r'\left(1'+sign+F+r'\right)'
        key=scale(Fraction(2,k),r'\left(1'+('-' if t==1 else '+')+F+r'\right)')
        small='1'+sign+fs
        steps=[frac('2sc'+frac(gs,fs),scale(k,'('+small+')')),frac('2'+gs+'^2',scale(k,'('+small+')')),
               scale(Fraction(2,k),frac('1-'+fs+'^2','('+small+')')),
               scale(Fraction(2,k),frac('(1-'+fs+')(1+'+fs+')','('+small+')')),
               scale(Fraction(2,k),'(1'+('-' if t==1 else '+')+fs+')'),key]
        note='Rewrite the quotient ratio and cancel. Use $s^2+c^2=1$, factor the difference of squares, then cancel the matching binomial.'
    elif fam=='binomial':
        q='cot' if f=='cos' else 'tan'
        E=frac(D+trig(q,a)+'-1',F+sign+G)
        key=F+('-' if t==1 else '+')+G
        steps=[frac('2sc'+frac(fs,gs)+'-1',fs+sign+gs),frac('2'+fs+'^2-1',fs+sign+gs),frac(fs+'^2-'+gs+'^2',fs+sign+gs),frac('('+fs+'-'+gs+')('+fs+'+'+gs+')',fs+sign+gs),fs+('-' if t==1 else '+')+gs,key]
        note='Rewrite the quotient ratio and use $s^2+c^2=1$ to obtain a difference of squares. Factor before cancelling.'
    else: raise ValueError(fam)
    return E,key,steps,note

class InvalidBank(ValueError): pass

def choices(p,key,rng):
    x=p['angle']*math.pi/180 if p['unit']=='deg' else math.pi/p['angle']
    fv={'sin':math.sin(x),'cos':math.cos(x),'tan':math.tan(x),'cot':1/math.tan(x),'sec':1/math.cos(x),'csc':1/math.sin(x)}
    a=angle(p);f=p['role'];g='cos' if f=='sin' else 'sin';k=p.get('k',1);t=p.get('sign',1);fam=p['family']
    profile=p['bank_profile'] if 'bank_profile' in p else rng.randrange(3)
    if fam in ('direct','product','quotient','inverse','square'):
        if fam in ('direct','product'): coef=Fraction(2,k);fn=f;power=1;wrong=g;recip='csc' if f=='sin' else 'sec'
        elif fam=='quotient':coef=Fraction(2);fn=f;power=2;wrong=g;recip='tan' if f=='sin' else 'cot'
        elif fam=='inverse':coef=Fraction(1,2);fn='sec' if f=='sin' else 'csc';power=1;wrong='csc' if fn=='sec' else 'sec';recip=g
        else:coef=Fraction(2);fn='tan' if f=='sin' else 'cot';power=1;wrong='cot' if fn=='tan' else 'tan';recip=f
        base=trig(fn,a,power)
        # Complete authored profiles. Each combines coefficient and function errors.
        profiles=[[(coef/2,fn,power),(coef*2,fn,power),(coef,wrong,power),(coef,recip,1)],
                  [(coef/2,fn,power),(coef,wrong,power),(coef/2,wrong,power),(coef*2,wrong,power)],
                  [(coef*2,fn,power),(coef,wrong,power),(coef*2,wrong,power),(coef/2,recip,1)]]
        wrongs=[scale(n,trig(h,a,pw)) for n,h,pw in profiles[profile]]
        values=[float(n)*fv[h]**pw for n,h,pw in profiles[profile]]
    elif fam=='complement':
        v=trig(f,a);w=trig(g,a);coef=Fraction(2,k)
        conjugate=r'\left(1'+('+' if t==1 else '-')+v+r'\right)'
        right=r'\left(1'+('-' if t==1 else '+')+v+r'\right)'
        other=r'\left(1'+('-' if t==1 else '+')+w+r'\right)'
        profiles=[[scale(coef,conjugate),scale(coef/2,right),scale(coef*2,right),scale(coef,other)],
                  [scale(coef,conjugate),scale(coef/2,right),scale(coef/2,conjugate),scale(coef,trig(f,a,2))],
                  [scale(coef,conjugate),scale(coef*2,right),scale(coef*2,conjugate),scale(coef,trig(f,a,2))]]
        wrongs=profiles[profile]
        rightval=1-t*fv[f];conjval=1+t*fv[f];otherval=1-t*fv[g];z=float(coef)
        values=[[z*conjval,z/2*rightval,z*2*rightval,z*otherval],[z*conjval,z/2*rightval,z/2*conjval,z*fv[f]**2],[z*conjval,z*2*rightval,z*2*conjval,z*fv[f]**2]][profile]
    else:
        v,w=trig(f,a),trig(g,a)
        # Complete sign-error bank: both members of each opposite pair.
        # No answer is singled out by absence of its negative or by grouping.
        conjugate=v+('+' if t==1 else '-')+w
        negative_key='-'+v+('+' if t==1 else '-')+w
        negative_conjugate='-'+v+('-' if t==1 else '+')+w
        # Illegal term cancellation (dropping one remaining term), or a
        # lost identity factor with the wrong binomial sign.
        error=[scale(2,v),scale(2,w),scale(2,r'\left('+conjugate+r'\right)')][profile]
        wrongs=[conjugate,negative_key,negative_conjugate,error]
        v,w=fv[f],fv[g];kv=v-t*w;cv=v+t*w
        values=[cv,-kv,-cv,[2*v,2*w,2*cv][profile]]
    bank=[key]+wrongs
    nums=[numeric(p)]+values
    if any(math.isclose(v,w,rel_tol=1e-10,abs_tol=1e-10) for i,v in enumerate(nums) for w in nums[i+1:]):raise InvalidBank('Coincident choices')
    return bank,profile

# Narrow runtime numeric sanity guard; independent symbolic verification is offline.
def numeric(p):
    x=p['angle']*math.pi/180 if p['unit']=='deg' else math.pi/p['angle']
    s,c=math.sin(x),math.cos(x);f=s if p['role']=='sin' else c;g=c if p['role']=='sin' else s;k=p.get('k',1);t=p.get('sign',1)
    fam=p['family']
    if fam in ('direct','product'):return 2*f/k
    if fam=='quotient':return 2*f*f
    if fam=='inverse':return 1/(2*g)
    if fam=='square':return 2*f/g
    if fam=='complement':return 2/k*(1-t*f)
    return f-t*g

def uid(s):return str(uuid.uuid5(NS,s))

def make(p,level,rng,source_bank=None,choice_position=None):
    E,key,steps,note=derive(p)
    bank,profile=choices(p,key,rng) if source_bank is None else (source_bank,'source-replay')
    key=normalize_tex(key);bank=[normalize_tex(b) for b in bank]
    if bank.count(key)!=1: raise ValueError('Key not unique')
    rng.shuffle(bank)
    if choice_position is not None:
        current=bank.index(key)
        bank[current],bank[choice_position]=bank[choice_position],bank[current]
    a,b=angle(p),angle(p,2)
    reciprocal=''
    fam=p['family'];f=p['role'];g='cos' if f=='sin' else 'sin';fs,gs=('s','c') if f=='sin' else ('c','s')
    if fam=='product':reciprocal=' The reciprocal definition gives $'+trig('sec' if g=='cos' else 'csc',a)+'='+frac(1,gs)+'$.'
    elif fam=='inverse' and p.get('product'):reciprocal=' The reciprocal definition gives $'+trig('csc',b)+'='+frac(1,'2sc')+'$.'
    elif fam=='quotient':reciprocal=' Also, $'+trig('cot' if f=='sin' else 'tan',a)+'='+frac(gs,fs)+'$.'
    elif fam in ('complement','binomial'):
        q=('tan' if f=='cos' else 'cot') if fam=='complement' else ('cot' if f=='cos' else 'tan')
        ratio=frac(gs,fs) if fam=='complement' else frac(fs,gs)
        reciprocal=' Also, $'+trig(q,a)+'='+ratio+'$.'
    rows=[steps[0]+' &='+steps[1]]+['&='+s for s in steps[2:]]
    solution=(r'Write $s='+trig('sin',a)+r'$ and $c='+trig('cos',a)+r'$. The **double-angle formula** gives $'+trig('sin',b)+r'=2sc$.'+'\n\n'+reciprocal+'\n\n'+note+'\n\n$$\n'+r'\begin{aligned}'+'\n'+r' \\ '.join(rows)+'\n'+r'\end{aligned}'+'\n$$\n\n'+r'All cancellations use nonzero factors in the original expression.')
    problem=normalize_prose('Simplify.\n\n$$\n'+E+'\n$$')
    solution=normalize_prose(solution)
    identity=json.dumps([problem,bank,key],ensure_ascii=False,separators=(',',':'))
    qid=uid(identity)
    answers=[{':answer/id':uid(qid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
    record={'knowledge_point':{'id':KP,'db_id':17592186059673,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':uid(qid+':selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(qid+':'+key)]}]},'generation':{'version':2,'template':p['family'],'parameters':p,'bank_profile':profile,'source_question_ids':SOURCES[p['family']],'domain':'Original denominators and reciprocal functions must be defined; sampled angles are acute and nonspecial.','ordered_steps':steps,'displayed_final':key}}
    return validate_generated_record(record)

def plans(level):
    families={'easy':['direct','quotient'],'moderate':['inverse','square','product'],'hard':['complement','binomial']}[level]
    return [(fam,role,sign) for fam in families for role in ('sin','cos') for sign in ((1,-1) if fam in ('complement','binomial') else (1,))]

def generate(level,count,seed):
    rng=random.Random(seed);schedule=plans(level);rng.shuffle(schedule);profile_order=rng.sample(range(3),3);out=[];seen=set()
    position_orders={};family_counts={}
    for family,_,_ in schedule:
        if family not in position_orders:
            order=list(range(5))
            random.Random(str(seed)+':positions:'+family).shuffle(order)
            position_orders[family]=order;family_counts[family]=0
    # Compatible values follow the selected case. No seed-specific paths.
    for i in range(count):
        fam,role,sign=schedule[i%len(schedule)]
        for attempt in range(500):
            unit=rng.choice(['deg','rad']);a=rng.choice([n for n in range(17,74) if n not in (30,45,60)]) if unit=='deg' else rng.choice([7,9,11,13,14,15,16,17,18,19,20,22,24])
            p={'family':fam,'role':role,'sign':sign,'bank_profile':profile_order[i%3],'k':rng.choice([1,2]) if fam in ('direct','product','complement') else 1,'unit':unit,'angle':a}
            if fam=='inverse':p['product']=bool(rng.randrange(2))
            try:r=make(p,level,rng,choice_position=position_orders[fam][family_counts[fam]%5])
            except InvalidBank:continue
            radians_pi=Fraction(p['angle'],180) if unit=='deg' else Fraction(1,p['angle'])
            signature=json.dumps([p['family'],p['role'],p['sign'],p['k'],str(radians_pi),p.get('product')])
            # Distinct parameter instances, not answer-order clones.
            if signature in seen:continue
            seen.add(signature);family_counts[fam]+=1;r['generation']['seed']=seed;r['generation']['index']=i;out.append(r);break
        else:raise ValueError('Requested more distinct practice than bounded sampler supports')
    return out

def replay():
    data=json.loads((Path(__file__).parent/'source-profiles.json').read_text())
    return [make(d['parameters'],d['difficulty'],random.Random(0),d['choices']) for d in data]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json');parser.add_argument('--replay-source',action='store_true')
    args=parser.parse_args()
    if args.count<0:parser.error('--count must be nonnegative')
    print(json.dumps(replay() if args.replay_source else generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
