"""Inverse integration: explicit normalization work and diagnostic answer banks."""
import math
import random
import sympy as s

X,U=s.symbols('x u',real=True)
VERSION='inverse-substitution-quality-4'
KPS={17592186064218:'sine',17592186064219:'tangent',17592186064250:'secant',17592186064220:'definite'}

def tex(v):
    return s.latex(v).replace(r'\log',r'\ln').replace(r'\operatorname{asin}',r'\arcsin').replace(r'\operatorname{atan}',r'\arctan').replace(r'\operatorname{asec}',r'\operatorname{arcsec}')

def primitive(fn,z):
    return {'sine':s.asin,'tangent':s.atan,'secant':s.asec}[fn](z)

def endpoint_pair(fn,band,profile):
    half=s.Rational(1,2);rt2=s.sqrt(2)/2;rt3=s.sqrt(3)/3
    if band=='easy':
        p=half if fn=='sine'else s.Integer(1)
        return (0,p)if profile%2==0 else(-p,0)
    if band=='moderate':
        return ((0,half),(0,rt2),(-half,half),(half,rt2))[profile]if fn=='sine'else ((0,1),(0,rt3),(-1,1),(rt3,1))[profile]
    return ((0,rt2),(-rt2,0),(-rt2,rt2),(half,rt2))[profile]if fn=='sine'else ((0,rt3),(-s.sqrt(3),0),(-rt3,rt3),(rt3,s.sqrt(3)))[profile]

def instance(kp,band,fn,rng,profile=0):
    a=s.Integer(rng.randint(2,5));n=s.Integer(rng.randint(1,4));A=s.Integer(1);B=a*a
    definite=KPS[kp]=='definite';lo=hi=None;notes=[];facts=[]
    if fn=='secant':
        if band=='easy':n=a*rng.randint(1,min(3,12//int(a)))
        inner=a*X;du=a
        body=n/((s.Abs(X)if band=='hard'else s.Abs(a*X))*s.sqrt(a*a*X*X-1))
        body_tex=r'\frac{'+tex(n)+'}{'+('|x|'if band=='hard'else '|'+tex(a*X)+'|')+r'\sqrt{'+tex(a*a*X*X-1)+'}}'
        factor=n if band=='hard'else n/a
        trans=1/(s.Abs(U)*s.sqrt(U*U-1));prim=s.asec(U)
        if band=='hard':notes.append('Because $'+tex(a)+'>0$, $|u|='+tex(a)+r'|x|$, so $|x|=|u|/'+tex(a)+'$.')
        challenge='integer_differential_match'if band=='easy'else'visible_linear_scaling'if band=='moderate'else'absolute_value_normalization'
        pref=n*a if band=='hard'else n
    else:
        if band!='easy':A=a*a;B=s.Integer(1)
        if band=='hard':
            if definite:A=s.Integer(rng.choice((2,8)if fn=='sine'else(3,12)))
            else:
                b=s.Integer(rng.choice([v for v in(2,3,4,5)if math.gcd(v,int(a))==1]))
                B=b*b
        # Small cancellable displays remain easy after reduction. They are
        # never promoted merely because both printed coefficients exceed one.
        if band=='easy'and not definite and a==2:
            display=s.Integer(rng.choice((1,2)))if fn=='sine'else s.Integer(rng.choice((1,2,4)if n<=2 else(1,2)))
            if fn=='sine':A*=display**2;B*=display**2;n*=display
            else:A*=display;B*=display;n*=display
        inner=s.sqrt(B/A)*X;du=s.diff(inner,X)
        trans=1/s.sqrt(1-U*U)if fn=='sine'else 1/(1+U*U)
        prim=primitive(fn,U);body=n/(s.sqrt(A-B*X*X)if fn=='sine'else A+B*X*X);body_tex=tex(body)
        factor=n/s.sqrt(B)if fn=='sine'else n/s.sqrt(A*B)
        pref=n/s.sqrt(A)if fn=='sine'else n/A
        if A!=1:
            lhs=r'\sqrt{'+tex(A-B*X*X)+'}'if fn=='sine'else tex(A+B*X*X)
            rhs=tex(s.sqrt(A))+r'\sqrt{1-('+tex(inner)+')^2}'if fn=='sine'else tex(A)+r'\left(1+('+tex(inner)+r')^2\right)'
            notes.append('Normalize the denominator:\n\n$$\n'+lhs+'='+rhs+'.\n$$')
        if definite:
            p,q=map(s.sympify,endpoint_pair(fn,band,profile));lo,hi=(s.simplify(v/du)for v in(p,q))
            facts=[tex((s.asin if fn=='sine'else s.atan)(v,evaluate=False))+'='+tex(primitive(fn,v))for v in(p,q)]
        challenge='direct_standard_form'if band=='easy'else'constant_normalization'if band=='moderate'else'familiar_radical_normalization'if definite else'combined_coprime_normalization'
    notes.append('The differential is $\\mathrm{d}x='+tex(1/du)+r'\,\mathrm{d}u$. The outside factor is $'+tex(pref)+r'\cdot '+tex(1/du)+'='+tex(factor)+'$.')
    factor=s.simplify(factor)
    params={'A':str(A),'B':str(B),'numerator':str(n),'scale':str(du)}
    if definite:params.update(normalized_lower=str(p),normalized_upper=str(q),endpoint_profile=profile)
    return dict(body=body,body_tex=body_tex,inner=inner,du=du,factor=factor,trans=trans,prim=prim,primitive=factor*prim.subs(U,inner),lo=lo,hi=hi,notes=notes,facts=facts,params=params,challenge=challenge)

def answer_bank(m,fn,fingerprint,render):
    rng=random.Random('inverse-diagnostic-bank-v1:'+fingerprint)
    r,z=m['factor'],m['inner'];candidates=[];seen=set()
    definite=m['lo']is not None
    if definite:
        u0,u1=(s.simplify(z.subs(X,v))for v in(m['lo'],m['hi']))
        f0,f1=(primitive(fn,v)for v in(u0,u1));correct=s.simplify(r*(f1-f0))
        pref=s.simplify(r*m['du'])
        for c,label in ((pref,'omit_dx_factor'),(pref*m['du'],'multiply_by_inner_derivative'),(r/m['du'],'divide_by_inner_derivative_twice'),(r/2,'extra_factor_two'),(2*r,'lose_factor_two')):
            candidates.append((s.simplify(c*(f1-f0)),label,'factor'))
        for angle in(s.pi/6,s.pi/4,s.pi/3,s.pi/2):
            candidates.append((s.simplify(r*angle),'wrong_special_angle','endpoint'))
        candidates.extend([(s.simplify(r*f1),'omit_lower_endpoint','endpoint'),(s.simplify(-r*f0),'omit_upper_endpoint','endpoint'),(s.simplify(r*(f1+f0)),'add_endpoint_values','endpoint')])
        token=lambda v:str(s.simplify(v))
        good=lambda v:bool(v>0)
    else:
        correct=r*primitive(fn,z);A=s.Integer(m['params']['A']);n=s.Integer(m['params']['numerator'])
        pref=s.simplify(r*m['du']);a=m['du']
        factors=[(pref,'omit_dx_factor'),(pref*a,'multiply_by_inner_derivative'),(-r,'wrong_sign'),(r/2,'extra_factor_two'),(2*r,'lose_factor_two'),(n,'omit_denominator_normalization')]
        candidates=[((s.simplify(c),z),label,'factor')for c,label in factors]
        for arg,label in ((X,'omit_inner_scale'),(X/a,'invert_inner_scale'),(2*z,'double_inner_scale'),(z/2,'half_inner_scale')):
            for c,clabel in ((r,''),(r/2,'_extra_half'),(2*r,'_extra_double')):
                candidates.append(((s.simplify(c),s.simplify(arg)),label+clabel,'argument'))
        token=lambda v:(str(s.simplify(v[0])),str(s.simplify(v[1])))
        good=lambda v:True
        correct_pair=(r,z);seen.add(token(correct_pair))
    if definite:seen.add(token(correct))
    rng.shuffle(candidates);pools={'factor':[],'endpoint'if definite else'argument':[]}
    for value,label,kind in candidates:
        t=token(value)
        if t in seen or not good(value):continue
        seen.add(t);expr=value if definite else value[0]*primitive(fn,value[1])
        pools[kind].append((expr,label))
    other='endpoint'if definite else'argument';nf=rng.choice((1,2,3));nf=min(nf,len(pools['factor']));no=4-nf
    if no>len(pools[other]):no=len(pools[other]);nf=4-no
    if not no or nf>len(pools['factor']):raise ValueError('Insufficient distinct diagnostic choices')
    bank=[(correct,'correct')]+pools['factor'][:nf]+pools[other][:no]
    if definite:m['bank_correct_rank']=sum(bool(v<correct)for v,label in bank)
    rng.shuffle(bank)
    return [(render(v)+(''if definite else'+C'),label)for v,label in bank]
