#!/usr/bin/env python3
"""Rewrite TWO exponential bases to a common base, then solve a linear equation.

Basis 1356. See adjacent evidence for full extraction, opaque historical banks,
source omissions, independent printed-math QA and real native grader results.
Observed profiles are evidence-only proportional bank continuations, with no
claim that the unknown historical distractor operations were recovered. Normal
output uses complete method-based authored banks. No EDB writes or plots.
"""
from __future__ import annotations
import argparse,sys, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186115219
KP_UUID='a8eebff2-97ca-599b-a819-04ff34f0c1c4'
TITLE='Solving Exponential Equations Containing Different Bases by Rewriting Two Exponents'
VERSION='two-exponents-1.0'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# b is the shared base; p,q its two powers; a*x+h,c*x+k the outer exponents.
# t is the right exponent for the product template. All fields are complete slots.
SPECS={
'q-66788':('moderate','coefficient',dict(b=2,p=2,q=3,a=1,h=1,c=2,k=0,var='x')),
'q-66893':('moderate','two_shifts',dict(b=2,p=4,q=5,a=1,h=-2,c=1,k=1,var='d')),
'q-100459':('hard','reciprocal',dict(b=6,p=3,q=2,a=3,h=4,c=6,k=-2,var='a')),
'q-3362':('hard','reciprocal',dict(b=3,p=3,q=4,a=2,h=2,c=-2,k=8,var='n')),
'q-100462':('moderate','two_shifts',dict(b=3,p=2,q=5,a=1,h=-4,c=1,k=3,var='d')),
'q-100468':('moderate','two_shifts',dict(b=5,p=2,q=4,a=1,h=-7,c=1,k=10,var='d')),
'q-110544':('easy','one_shift',dict(b=3,p=4,q=3,a=1,h=0,c=1,k=5,var='y')),
'q-3304':('hard','product',dict(b=2,p=3,q=2,a=1,h=0,c=2,k=-1,t=5,var='x')),
'q-66889':('easy','one_shift',dict(b=4,p=2,q=3,a=1,h=0,c=1,k=4,var='b')),
'q-66892':('easy','one_shift',dict(b=5,p=2,q=3,a=1,h=1,c=1,k=0,var='q')),
'q-66895':('moderate','coefficient',dict(b=3,p=4,q=3,a=3,h=0,c=1,k=5,var='m')),
'q-3090':('moderate','coefficient',dict(b=2,p=4,q=3,a=2,h=0,c=1,k=1,var='n')),
}

def tex(v):
    v=sp.Rational(v)
    sign='-' if v<0 else ''
    v=abs(v)
    return sign+(str(v.p) if v.q==1 else r'\frac{'+str(v.p)+'}{'+str(v.q)+'}')
def lin(a,h,v):
    lead=(v if a==1 else '-'+v if a==-1 else str(a)+v) if a else ''
    return lead+('+'+str(h) if h>0 and lead else str(h) if h else '')
def mul(n,a,h,v):
    return lin(n*a,0,v) if h==0 else str(n)+'('+lin(a,h,v)+')'
def frac(text):
    m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',text)
    return sp.Rational(int(m[2])*(-1 if m[1] else 1),int(m[3])) if m else sp.Rational(text)
def answer(p,kind):
    if kind=='product':return sp.Rational(p['t']-p['p']*p['h']-p['q']*p['k'],p['p']*p['a']+p['q']*p['c'])
    s=-1 if kind=='reciprocal' else 1
    return sp.Rational(s*p['q']*p['k']-p['p']*p['h'],p['p']*p['a']-s*p['q']*p['c'])

def values(p,kind,profile):
    correct=answer(p,kind)
    if profile.startswith('observed:'):
        sid=profile.split(':',1)[1]
        old=SPECS[sid][2]
        # Explicit opaque proportional continuation: preserves all historical values
        # without pretending that scalar evidence determines an error algorithm.
        ref=answer(old,SPECS[sid][1])
        return [frac(a[':answer/value'])*correct/ref for f in ORIGINALS[sid].get(':question/answer-fields',[]) for a in f[':answer-field/choices']]
    b,u,w,a,h,c,k=(p[x] for x in ('b','p','q','a','h','c','k'))
    if kind=='product':
        t=p['t'];D=u*a+w*c
        return [correct,sp.Rational(t-h-w*k,a+w*c),sp.Rational(t-u*h-k,u*a+c),sp.Rational(t-h-k,D),sp.Rational(t-u*h+w*k,u*a-w*c)]
    s=-1 if kind=='reciprocal' else 1
    D=u*a-s*w*c;N=s*w*k-u*h
    if kind=='reciprocal':
        return [correct,sp.Rational(w*k-u*h,u*a-w*c),sp.Rational(-k-h,D),-correct,sp.Rational(N,u*a-w*c)]
    return [correct,-correct,sp.Rational(s*k-h,D),sp.Rational(s*u*k-w*h,w*a-s*u*c),sp.Rational(N,u*a+s*w*c)]

def guard(p,level,kind,profile):
    required={'b','p','q','a','h','c','k','var'}|({'t'} if kind=='product' else set())
    if set(p)!=required:raise ValueError('Exact parameter keys required: '+str(sorted(required)))
    if p['var'] not in ('x','y','d','b','q','m','n','a'):raise ValueError('Supported variable letters only')
    if any(type(p[x]) is not int for x in required-{'var'}):raise ValueError('Integer coefficients required')
    b,u,w,a,h,c,k=(p[x] for x in ('b','p','q','a','h','c','k'))
    if not (2<=b<=6 and 2<=u<=5 and 2<=w<=5 and u!=w and max(b**u,b**w)<=1296):raise ValueError('Two different nonunit powers, familiar bases <=1296 required')
    if level=='easy':
        if kind!='one_shift' or a!=1 or c!=1 or abs(u-w)!=1 or (h==0)==(k==0) or not 1<=max(abs(h),abs(k))<=8:raise ValueError('Easy: adjacent powers, unit outer coefficients, exactly one small nonzero shift')
    elif level=='moderate':
        if kind=='two_shifts':
            if a!=1 or c!=1 or not (-10<=h<=-1 and 1<=k<=10):raise ValueError('Moderate two shifts: unit outer coefficients, opposite nonzero shifts <=10')
        elif kind=='coefficient':
            if not (1<=a<=4 and 1<=c<=4 and (a==1)!=(c==1) and (h==0)!=(k==0) and 1<=max(abs(h),abs(k))<=8):raise ValueError('Moderate coefficient: one nonunit outer coefficient and one nonzero shift <=8')
        else:raise ValueError('Moderate family')
    elif level=='hard':
        if kind=='reciprocal':
            if not (2<=abs(a)<=6 and 2<=abs(c)<=6 and 1<=abs(h)<=8 and 1<=abs(k)<=8 and max(abs(u*a),abs(w*c))<=24):raise ValueError('Hard reciprocal: two nonunit affine exponents, nonzero shifts, products <=24')
        elif kind=='product':
            if not (a==1 and h==0 and 2<=c<=4 and 1<=abs(k)<=4 and 2<=p['t']<=6):raise ValueError('Hard product: simple first exponent, nonunit shifted second exponent and rhs power 2..6')
        else:raise ValueError('Hard family')
    else:raise ValueError('Unknown level')
    D=u*a-(-1 if kind=='reciprocal' else 1)*w*c
    if level=='moderate' and D==1:raise ValueError('Moderate collection must retain a nontrivial isolation/sign stage')
    if kind=='reciprocal' and abs(D)<=1:raise ValueError('Reciprocal collection must retain division after two affine distributions')
    try:bank=values(p,kind,profile)
    except (ZeroDivisionError,TypeError) as e:raise ValueError('Complete bank has undefined operation') from e
    if not answer(p,kind).is_finite:raise ValueError('No unique solution')
    if bank and (len(bank)!=5 or any(not x.is_finite for x in bank) or len(set(bank))!=5):raise ValueError('Reject entire colliding or undefined bank')
    if bank and sum(x==answer(p,kind) for x in bank)!=1:raise ValueError('Exactly one correct value required')
    return bank

def equation(p,kind,legacy=False):
    b,u,w=p['b'],p['p'],p['q'];v=p['var'];L=lin(p['a'],p['h'],v);R=lin(p['c'],p['k'],v)
    if legacy:return f'{b**u}^{{{L}}} = {b**w}^{{{R}}}'
    if kind=='reciprocal':return '{'+str(b**u)+'}^{'+L+r'}={(\frac{1}{'+str(b**w)+'})}^{'+R+'}'
    if kind=='product':return '{'+str(b**u)+'}^{'+L+r'}\cdot {'+str(b**w)+'}^{'+R+'}='+str(b**p['t'])
    return '{'+str(b**u)+'}^{'+L+'}={'+str(b**w)+'}^{'+R+'}'

def prompt(sid,p,raw=False):
    level,kind,_=SPECS[sid];v=p['var'];E=equation(p,kind,sid in ('q-66788','q-66893'))
    if sid in ('q-100459','q-66895'):return f'If ${E}$ then ${v}=$'
    if sid=='q-3362':return f'If ${E},$ then ${v}=$'
    if sid in ('q-110544','q-66892','q-3090'):return f'Solve for ${v}$ where ${E}.$'
    if sid=='q-66788':
        # Legacy original has spaces in its outer exponent; full component slot.
        E=f"{p['b']**p['p']}^{{{lin(p['a'],0,v)} {'+' if p['h']>0 else '-'} {abs(p['h'])}}} = {p['b']**p['q']}^{{{lin(p['c'],p['k'],v)}}}"
        return f'Solve for ${v}$ where ${E}$.'
    if sid=='q-66893':E=f"{p['b']**p['p']}^{{{v} - {abs(p['h'])}}} = {p['b']**p['q']}^{{{v} + {p['k']}}}"
    if sid=='q-66893':return f'Find the value of ${v}$ that satisfies the equation ${E}$.'
    return f'Find the value of ${v}$ that satisfies the equation ${E}.$'

def solution(sid,p):
    level,kind,_=SPECS[sid];b,u,w,a,h,c,k=(p[x] for x in ('b','p','q','a','h','c','k'));v=p['var']
    L=lin(a,h,v);R=lin(c,k,v);U=mul(u,a,h,v);W=mul(w,c,k,v)
    powb=lambda e:'{'+str(b)+'}^{'+e+'}'
    nested=lambda n,e:'{({'+str(b)+'}^{'+str(n)+'})}^{'+e+'}'
    opening='To solve this equation, we need both exponential terms to have a common base. To do this, we rewrite the equation using '
    block=lambda x:'\n\n$$\n'+x+'\n$$'
    aligned=lambda x:r'\begin{aligned}'+x+r'\end{aligned}'
    if kind=='product':
        intro=f'${b**u}={{{b}}}^{{{u}}}$, ${b**w}={{{b}}}^{{{w}}}$ and ${b**p["t"]}={{{b}}}^{{{p["t"]}}},$ as follows:'
        first=nested(u,L)+r'\cdot '+nested(w,R)+'='+powb(str(p['t']))
        combined=U+'+'+W
        second=aligned(powb(U)+r'\cdot '+powb(W)+' & ='+powb(str(p['t']))+r' \\ '+powb(combined)+' & ='+powb(str(p['t'])))
        rule='Then, we apply the power rule and the product rule of exponents. This gives:'
        collectA=u*a+w*c;collectN=p['t']-u*h-w*k
        rows=[combined+' & ='+str(p['t']),lin(u*a,u*h,v)+('+' if w*c>0 else '')+lin(w*c,w*k,v)+' & ='+str(p['t']),lin(collectA,0,v)+' & ='+str(collectN),v+' & ='+tex(answer(p,kind))]
    else:
        comma='' if sid in ('q-100462','q-100468') else ','
        intro=f'${b**u}={{{b}}}^{{{u}}}$ and ${b**w}={{{b}}}^{{{w}}}{comma}$ as follows:'
        first=nested(u,L)+'='+ (r'{(\frac{1}{{'+str(b)+'}^{'+str(w)+'}})}^{'+R+'}' if kind=='reciprocal' else nested(w,R))
        if sid in ('q-66895','q-3090'):first+=r'\,'
        amp=' & ' if sid in ('q-66895','q-3090') else ''
        second=aligned(powb(U)+amp+'='+ (r'\frac{1}{{'+str(b)+'}^{'+W+'}}' if kind=='reciprocal' else powb(W)))
        rule='Then, we apply the power rule of exponents. This gives:'
        if kind=='reciprocal':rule='Then, we apply the power rule and the '+('power of quotient rule' if sid=='q-3362' else 'quotient rule')+' of exponents. This gives:'
        s=-1 if kind=='reciprocal' else 1
        collectA=u*a-s*w*c;collectN=s*w*k-u*h
        rows=[U+' & ='+ ('-'+W if s==-1 else W),lin(u*a,u*h,v)+' & ='+lin(s*w*c,s*w*k,v)]
        if level!='easy':
            if sid=='q-3362' and collectA<0:collectA=-collectA;collectN=-collectN
            rows.append(lin(collectA,0,v)+' & ='+str(collectN))
        rows.append(v+' & ='+tex(answer(p,kind)))
    # Shared original prose and every math stage are preserved.
    base_end=',' if sid=='q-110544' else ''
    base_tail=')' if sid=='q-110544' else ')'
    common=f'Now, since both sides of the equation share the same base $({b})'+base_end+'$'+('' if sid=='q-110544' else ',')+f' we equate the exponents and solve for ${v}:$'
    out=opening+intro+block(first)+'\n\n'+rule+block(second)
    if kind=='reciprocal':out+='\n\nNext, we rewrite the right-hand side using a negative exponent:'+block(aligned(powb(U)+'='+powb('-'+W)))
    out+='\n\n'+common+block(aligned(r' \\ '.join(rows)))
    return out

def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def identity(p,kind):
    # Common-power normalization avoids counting alternative rewrite bases, variable aliases,
    # shared coefficient scaling, layouts or complete banks as new assessed equations.
    v=sp.Symbol('x');b=p['b'];u=p['p'];w=p['q'];A=p['a'];H=p['h'];C=p['c'];K=p['k']
    factors=sp.factorint(b);prime=min(factors);e=factors[prime]
    if len(factors)!=1:prime=b;e=1
    if kind=='product':coeff=u*A+w*C;constant=u*H+w*K-p['t']
    else:s=-1 if kind=='reciprocal' else 1;coeff=u*A-s*w*C;constant=u*H-s*w*K
    # Assessed exponential task includes both base rewrites and outer affine components.
    import math
    nums=[A,H,C,K]+([p['t']] if kind=='product' else [])
    common=math.gcd(*nums)
    normalized=[n//common for n in nums]
    sides=sorted([(e*u,normalized[0],normalized[1]),(e*w,normalized[2],normalized[3])])
    payload=[prime,sides,normalized[4:] if kind=='product' else [],kind]
    return hashlib.sha256(json.dumps(payload).encode()).hexdigest()

def sample(rng,level,kind):
    b=rng.choice([2,3,4,5,6]);u=rng.randint(2,5);w=rng.randint(2,5)
    p=dict(b=b,p=u,q=w,a=1,h=0,c=1,k=rng.choice([i for i in range(-8,9) if i]),var=rng.choice(['x','y','n','d']))
    if kind=='one_shift':
        if rng.randrange(2):p['h'],p['k']=p['k'],0
    elif kind=='two_shifts':p.update(h=-rng.randint(1,10),k=rng.randint(1,10))
    elif kind=='coefficient':
        if rng.randrange(2):p['a']=rng.randint(2,4)
        else:p['c']=rng.randint(2,4)
        if rng.randrange(2):p['h'],p['k']=p['k'],0
    elif kind=='reciprocal':p.update(a=rng.choice([-1,1])*rng.randint(2,6),c=rng.choice([-1,1])*rng.randint(2,6),h=rng.choice([-1,1])*rng.randint(1,8),k=rng.choice([-1,1])*rng.randint(1,8))
    elif kind=='product':p.update(c=rng.randint(2,4),k=rng.choice([-1,1])*rng.randint(1,4),t=rng.randint(2,6))
    return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    rng=random.Random(seed)
    if template is None:template=rng.choice([s for s,(l,_,_) in SPECS.items() if l==level and s not in ('q-66788','q-66893')])
    if template not in SPECS or SPECS[template][0]!=level:raise ValueError('Template/level mismatch')
    kind=SPECS[template][1];raw=bool(profile and profile.startswith('observed:'))
    if raw and profile!='observed:'+template:raise ValueError('Observed bank belongs to its original template')
    if not raw and profile not in (None,'authored-method'):raise ValueError('Unknown profile')
    profile=profile or 'authored-method'
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Observed normal response is radio')
    if parameters is None:
        for _ in range(20000):
            p=sample(rng,level,kind)
            try:
                bank=guard(p,level,kind,profile)
                if template=='q-66788' and not (p['a']==1 and p['h']!=0 and p['k']==0):continue
                break
            except ValueError:continue
        else:raise ValueError('No eligible whole bank sampled')
    else:
        p=dict(parameters);bank=guard(p,level,kind,profile)
        if template=='q-66788' and not (p['a']==1 and p['h']!=0 and p['k']==0):raise ValueError('Legacy source requires left shift and right scaled exponent')
    original=ORIGINALS[template]
    problem=prompt(template,p,raw)
    worked=solution(template,p)
    q={':question/problem':problem}
    if not raw or ':question/difficulty' in original:q[':question/difficulty']=':question.difficulty/'+level
    if not raw or ':question/worked-solution' in original:q[':question/worked-solution']=worked
    if not raw or ':question/answer-fields' in original:
        fields=[]
        # raw fieldless questions intentionally omit fields instead of fabricating fidelity.
        if bank:
            content={'version':VERSION,'prompt':problem,'solution':q.get(':question/worked-solution'),'difficulty':q.get(':question/difficulty'),'bank':sorted(map(tex,bank)),'raw_missing_correct':raw and ':answer-field/correct' not in original[':question/answer-fields'][0]}
            key=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
            f={':answer-field/id':uid(key+'/selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio'}
            choices=[{':answer/id':uid(key+'/selection/'+tex(x)),':answer/type':':answer.type/math',':answer/value':tex(x)} for x in bank]
            if not raw or ':answer-field/correct' in original[':question/answer-fields'][0]:f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a,x in zip(choices,bank) if x==answer(p,kind))]
            rng.shuffle(choices);f[':answer-field/choices']=choices;fields.append(f)
        q[':question/answer-fields']=fields
    content={k:v for k,v in q.items()}
    # Owned IDs above are independent of order; question content hash uses sorted bank.
    canonical=json.loads(json.dumps(content))
    for f in canonical.get(':question/answer-fields',[]):f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    key=hashlib.sha256(json.dumps([VERSION,canonical],sort_keys=True).encode()).hexdigest()
    q[':question/id']=uid(key)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,'template':template,'kind':kind,'profile':profile,'parameters':p,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'domain':{'variable':'real scalar','common_base':'integer 2..6','rewriting_powers':'different integers 2..5','displayed_base_max':1296,'answer':'unique exact rational; all required divisions defined'},'origin':('original source replay' if p==SPECS[template][2] else 'generated historical-bank evidence') if raw else 'generated variant with authored method bank','source':{'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage']},'mathematical_fingerprint':identity(p,kind),'content_fingerprint':key,'evidence_only':raw,'eligible_for_learning':not raw,'bank_origin':('opaque observed proportional continuation' if bank else 'no original field/bank') if raw else 'authored complete operation bank','bank_recipes':(['source-value/reference-correct times new-correct']*len(bank) if raw else (['correct','omit left rewriting factor','omit right rewriting factor','omit both shift distribution factors','subtract rather than add outer exponents'] if kind=='product' else ['correct','ignore reciprocal sign','omit shift distribution factors','reverse transferred constant sign','subtract variable coefficients'] if kind=='reciprocal' else ['correct','reverse transferred constant sign','omit shift distribution factors','exchange the two rewriting factors','add variable coefficients'])),'field_repairs':[] if raw else (['authored radio field and correct ref'] if ':question/answer-fields' not in original else ['inferred mathematically verified correct ref'] if ':answer-field/correct' not in original[':question/answer-fields'][0] else [])}}

# Easy: two adjacent base powers, one nonzero shift; three linear rows.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: two shifted unit exponents or one scaled exponent and one shift;
# two base rewrites, power-rule distribution, four linear rows, exact rational value.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: source-observed reciprocal conversion or source-observed product rule;
# no logarithms, polynomial substitutions, or rewriting-only-one-base tasks.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];g=r['generation'];level=q.get(':question/difficulty','unrated raw evidence').split('/')[-1]
    s=f"### {level} — {g['origin']} — {g['profile']}\n\n"+q[':question/problem']+'\n\n'
    if ':question/answer-fields' not in q:s+='[Original answer fields absent.]\n'
    for f in q.get(':question/answer-fields',[]):
        correct=f.get(':answer-field/correct',[None,None])[1]
        if correct is None:s+='[Original correct designation absent.]\n'
        for a in f[':answer-field/choices']:s+=('- [correct] ' if a[':answer/id']==correct else '- ')+ '$'+a[':answer/value']+'$\n'
    return s+'\n'+q.get(':question/worked-solution','[Source worked solution absent]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
