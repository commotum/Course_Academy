#!/usr/bin/env python3
"""Relocatable, database-free exponential rearrangement generator; see instructional-account.md."""
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import json
from pathlib import Path
import random
import uuid
from math_format import checked_math_content, normalize_prose, normalize_tex

KP = {'db_id':17592186110595, 'id':'7d076e5d-9d08-5355-b813-d1749feb0803',
      'title':'Finding Solutions to Exponential Equations when Rearrangement is Required'}
VERSION = '1.2.0'
F = Fraction
SCALARS = [F(1,2),F(2,3),F(3,4),F(3,2),F(2),F(5,2),F(3),F(4),F(5)]
SPECS = {
 'q-1117':dict(template='scaled',b=10,A='1',m=2,n=0,S=3,R=65,v='x',profile='source1117'),
 'q-66830':dict(template='exact',b=3,A='4',m=1,n=0,S=6,R=30,v='y',profile='source66830'),
 'q-66832':dict(template='exact',b=4,A='3',m=1,n=0,S=-14,R=19,v='y',profile='source66832'),
 'q-31891':dict(template='shifted',b=5,A='1',m=2,n=3,S=-13,R=25,v='a',profile='source31891'),
 'q-974':dict(template='rounded',b=3,A='5/2',m=1,n=0,S=0,R=5,v='x',profile='source974'),
 'q-100254':dict(template='scaled',b=7,A='1',m=5,n=0,S=8,R=34,v='x',profile='source100254'),
}


def uid(text): return str(uuid.uuid5(uuid.NAMESPACE_URL, 'ca-exp-rearrangement/'+text))
def tex(q):
    q=F(q)
    return str(q.numerator) if q.denominator==1 else rf'\frac{{{q.numerator}}}{{{q.denominator}}}'
def decimal(q):
    q=F(q)
    return Decimal(q.numerator)/Decimal(q.denominator)
def logb(t,b): return decimal(t).ln()/Decimal(b).ln()
def calc(p):
    with localcontext() as ctx:
        ctx.prec=60
        t=(F(p['R'])-F(p['S']))/F(p['A'])
        if t<=0 or p['b']<=1 or p['m']==0: raise ValueError('invalid logarithm domain')
        L=logb(t,p['b']); r=(L-Decimal(p['n']))/Decimal(p['m'])
        return t,+L,+r

def rounded(x):
    with localcontext() as ctx:
        ctx.prec=60
        s=f'{x:.3f}'
        return '0.000' if s=='-0.000' else s

def plus(n): return ('+' if n>=0 else '-')+tex(abs(F(n))) if n else ''
def power(p):
    v=p['v'];m=p['m'];n=p['n']
    exponent=(v if m==1 else f'{m}{v}')+plus(n)
    return rf"{p['b']}^{{{exponent}}}"
def lhs(p):
    A=F(p['A']);pw=power(p)
    return (pw if A==1 else tex(A)+r'\cdot '+pw)+plus(p['S'])
def logtex(b,t):return rf'\log_{{{b}}}\left({tex(t)}\right)'

def bank(p,t,L,r):
    v=p['v'];b=p['b'];A=F(p['A']);R=F(p['R']);S=F(p['S']);profile=p['profile']
    if profile=='source66832':
        args=[t,R-S,R+S]
        if any(x<=0 for x in args) or A==1 or t==1:raise ValueError('undefined exact-bank option')
        vals=[v+'='+logtex(b,t), v+'='+rf'\frac{{{tex(A)}}}{{{logtex(b,A)}}}',v+'='+logtex(b,R-S),v+'='+logtex(b,R+S),v+'='+rf'\frac{{1}}{{{logtex(b,t)}}}']
        nums=[L,decimal(A)/logb(A,b),logb(R-S,b),logb(R+S,b),1/L]
    elif profile=='source66830':
        args=[t,R/(A+S),R+S,R-S,(R+S)/A]
        vals=[v+'='+logtex(b,z) for z in args];nums=[logb(z,b) for z in args]
    elif profile=='source1117':
        W=logb(R+S,b);m=Decimal(p['m'])
        # Source distractors use truncated intermediate logs, not final rounding.
        Lt=L.quantize(Decimal('.001'),rounding='ROUND_DOWN')
        Wt=W.quantize(Decimal('.001'),rounding='ROUND_DOWN')
        nums=[r,Lt,m*Lt,Wt,Wt/m]; vals=[rounded(z) for z in nums]
    elif profile=='source31891':
        nums=[r,-r,p['m']*r,-p['m']*r,L]; vals=[rounded(z) for z in nums]
    elif profile in ('source974','source100254'):
        # Deliberately bounded source replay. No invented parameter rule for opaque options.
        ref=SPECS['q-974' if profile=='source974' else 'q-100254']
        if any(p[k]!=ref[k] for k in ref): raise ValueError('opaque bank is available only at original parameters')
        if profile=='source974': nums=[r,1/r,-1/r,(decimal(t)/Decimal(b)).log10(),Decimal('0.527')]
        else: nums=[r,Decimal('0.353'),Decimal('0.533'),Decimal('0.303'),Decimal('0.350')]
        vals=[rounded(z) for z in nums]
    elif profile=='log-candidates-v2':
        args=[F(z) for z in p['candidate_targets']]
        if len(args)!=5 or len(set(args))!=5 or min(args)<=0 or t not in args:
            raise ValueError('incompatible exact candidates')
        args=[t]+[z for z in args if z!=t]
        vals=[v+'='+logtex(b,z) for z in args];nums=[logb(z,b) for z in args]
    elif profile=='root-candidates-v2':
        rhs=p['candidate_rhs']
        if len(rhs)!=5 or len(set(rhs))!=5 or p['R'] not in rhs:
            raise ValueError('incompatible RHS candidates')
        rhs=[p['R']]+[z for z in rhs if z!=p['R']]
        nums=[(logb((F(z)-S)/A,b)-p['n'])/p['m'] for z in rhs]
        vals=[rounded(z) for z in nums]
    else: raise ValueError('unknown profile')
    if len(set(vals))!=5 or any(abs(nums[i]-nums[j])<Decimal('1e-30') for i in range(5) for j in range(i)):
        raise ValueError('colliding bank')
    return vals


def worked(p,t,L,r):
    v=p['v'];b=p['b'];A=F(p['A']);S=F(p['S']);R=F(p['R']);pw=power(p)
    rows=[lhs(p)+'&='+tex(R)]
    if S:rows.append((pw if A==1 else tex(A)+r'\cdot '+pw)+'&='+tex(R-S))
    if A!=1: rows.append(pw+'&='+tex(t))
    st='First, we rearrange our equation into a form that is more convenient for logarithms, as follows:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
    exponent=(v if p['m']==1 else str(p['m'])+v)+plus(p['n'])
    lg=logtex(b,t)
    st+=f'\n\nNow, we take $\\log_{{{b}}}$ of both sides of the equation:\n\n$$\n'+r'\begin{aligned}'+rf'\log_{{{b}}}\left({pw}\right)&={lg} \\ {exponent}&={lg}'+r'\end{aligned}'+'\n$$'
    if p['template']=='exact':return st+f'\n\nTherefore, the solution is ${v}={lg}$.'
    ratio=rf'\frac{{\log\left({tex(t)}\right)}}{{\log\left({b}\right)}}'
    rows=[exponent+'&='+ratio]
    if p['n']:rows.append(str(p['m'])+v+'&='+ratio+plus(-p['n']))
    result=ratio if p['m']==1 else rf'\frac{{{ratio}{plus(-p["n"])}}}{{{p["m"]}}}'
    if p['m']!=1:rows.append(v+'&='+result)
    st+='\n\nNext, we rewrite the right-hand side using the change of base formula'+(' and solve for $'+v+'$' if p['m']!=1 else '')+':\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
    return st+'\n\nEvaluating the above on a calculator gives\n\n$$\n'+v+r'\approx '+rounded(r)+'\n$$\n\nrounded to $3$ decimal places.'



@checked_math_content
def build(p, difficulty=None, seed=0, source=None, shuffle=True):
    p=dict(p)
    with localcontext() as ctx:
        ctx.prec=60
        t,L,r=calc(p); values=bank(p,t,L,r)
    if source:
        prompt=source[':question/problem']
    elif p['template']=='exact':prompt=f"Find the exact solution to the equation ${lhs(p)}={tex(p['R'])}$."
    else:prompt=f"Given that ${lhs(p)}={tex(p['R'])}$, find the value of ${p['v']}$ rounded to $3$ decimal places."
    prompt=normalize_prose(prompt)
    solution=normalize_prose(worked(p,t,L,r))
    values=[normalize_tex(v) for v in values]
    identity=json.dumps([prompt,values],sort_keys=True)
    qid=uid(identity);fid=uid(qid+'/selection')
    choices=[{':answer/id':uid(fid+'/'+val),':answer/type':':answer.type/math',':answer/value':val} for val in values]
    correct=choices[0][':answer/id']
    if shuffle:random.Random(str(seed)+'/'+identity).shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field],':question/requires-calculator':source.get(':question/requires-calculator',p['template']!='exact') if source else p['template']!='exact'}
    if difficulty:q[':question/difficulty']=':question.difficulty/'+difficulty
    return {'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,'template':p['template'],'profile':p['profile'],'seed':seed,'parameters':p,'domain':{'base':'>1','isolated_argument':'>0'},'source_ids':[source[':question/id']] if source else [q[':question/id'] for q in source_cases() if SPECS[q[':question/math-academy-id']]['template']==p['template'] or (p['template']=='combined' and q[':question/math-academy-id'] in ('q-66832','q-31891'))], 'exact_target':str(t),'unrounded_root':str(r),'source_replay':source is not None}}


def source_cases():return json.loads(Path(__file__).with_name('source-cases.json').read_text())
def replay():
    result=[]
    for source in source_cases():
        p=SPECS[source[':question/math-academy-id']].copy()
        difficulty=source.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or None
        result.append(build(p,difficulty,source=source))
    return result


def sample_parameters(rng,difficulty):
    # Choose the answer-bearing role independently of all candidate-bank values.
    template=('combined' if difficulty=='hard' else rng.choice(['exact','rounded'] if difficulty=='easy' else ['scaled','shifted']))
    role=rng.randrange(5)
    p=dict(template=template,b=rng.randint(2,9),v=rng.choice(['x','y','a']),m=1,n=0,A='1',S=0,R=1)
    if template=='exact':
        region=rng.choice(['below','above'])
        A=rng.choice([a for a in SCALARS if (a<1)==(region=='below')])
        s=rng.choice([-1,1])*rng.randint(1,20)
        targets=[F(k)/A for k in range(1,25) if k+s>0]
        if len(targets)<5:raise ValueError('insufficient common exact candidates')
        candidates=sorted(rng.sample(targets,5))
        p.update(A=str(A),S=s,R=int(A*candidates[role])+s,
                 profile='log-candidates-v2',candidate_targets=[str(t) for t in candidates])
    else:
        if template=='rounded':
            p['A']=str(rng.choice(SCALARS));limit=30
        else:
            p.update(m=rng.randint(2,6),S=rng.choice([-1,1])*rng.randint(1,20));limit=70
            if template in ('shifted','combined'):p['n']=rng.choice([-1,1])*rng.randint(1,3)
            if template=='combined':
                p.update(A=str(rng.randint(2,4)),m=rng.choice([-3,-2,2,3]),S=rng.choice([-1,1])*rng.randint(1,9))
        # Collapse rounding collisions before assigning the key, never after it.
        candidates={}
        for R in range(1,limit+1):
            t=(F(R)-p['S'])/F(p['A'])
            if t<=0:continue
            # Calculator practice must require logarithms, not recognition of a power.
            if any(t**q==F(p['b'])**k for q in range(1,5) for k in range(-8,9)):continue
            _,_,root=calc(dict(p,R=R))
            candidates.setdefault(rounded(root),R)
        if len(candidates)<5:raise ValueError('insufficient common rounded candidates')
        rhs=sorted(rng.sample(list(candidates.values()),5))
        p.update(R=rhs[role],profile='root-candidates-v2',candidate_rhs=rhs)
    return p


def generate(difficulty,count,seed,stats=None):
    if difficulty not in ('easy','moderate','hard'):raise ValueError('unsupported difficulty: '+difficulty)
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);out=[];seen=set();reject={};attempts=0;roles={}
    while len(out)<count:
        attempts+=1
        if attempts>max(1000,count*200):raise RuntimeError('sampling exhausted')
        try:
            p=sample_parameters(rng,difficulty);rec=build(p,difficulty,seed)
            ident=rec['question'][':question/problem']
            if ident in seen:raise ValueError('duplicate equation')
            # A small delivered template pool must not teach a constant position or rank.
            field=rec['question'][':question/answer-fields'][0]
            choices=field[':answer-field/choices'];key=field[':answer-field/correct'][1]
            position=next(i for i,c in enumerate(choices) if c[':answer/id']==key)
            if p['template']=='exact':
                rank=sorted(map(F,p['candidate_targets'])).index(calc(p)[0])
            else:
                vals=sorted(Decimal(c[':answer/value']) for c in choices)
                rank=vals.index(Decimal(choices[position][':answer/value']))
            groups=['template/'+p['template']]
            if p['template']!='exact':
                signs=[Decimal(c[':answer/value']) for c in choices]
                profile=('positive' if min(signs)>0 else 'negative' if max(signs)<0 else 'mixed')
                groups.append('numeric-bank-signs/'+profile)
            if any(len(roles.get(group,[]))==1 and
                   (roles[group][0][0]==position or roles[group][0][1]==rank)
                   for group in groups):
                raise ValueError('constant early visible subgroup position or rank')
            for group in groups:roles.setdefault(group,[]).append((position,rank))
            seen.add(ident);out.append(rec)
        except ValueError as error:
            key=str(error);reject[key]=reject.get(key,0)+1
    if stats is not None:stats.update(attempts=attempts,accepted=len(out),rejected=reject)
    return out


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy')
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args()
    try:records=generate(args.difficulty,args.count,args.seed)
    except ValueError as error:parser.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
