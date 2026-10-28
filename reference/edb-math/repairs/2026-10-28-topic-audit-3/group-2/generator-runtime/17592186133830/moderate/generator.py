#!/usr/bin/env python3
"""Relocatable scalar line integral generator; no services or database writes."""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record
VERSION='scalar-ds-v3'
KP_ID=17592186133830
KP={'db_id':KP_ID,'id':'481a6b6e-05a2-5003-9ac7-b4876ffa4ffa','title':'Evaluating the Line Integral of a Scalar Function'}
T=sp.Symbol('t', real=True)
X,Y=sp.symbols('x y', real=True)
FAMILIES={'easy':('sum','reciprocal','product'),'moderate':('circle_cos','circle_sin','cubic','fractional'),'hard':('involute','mixed_fractional')}
SOURCE_IDS={'product':'8bf6a863-9b9f-5877-84bc-3e11d71261c9','sum':'72644873-b2ba-57a8-bd4c-d5dc5e8e5941','reciprocal':'a7a51cb6-cac0-57a7-bccc-fcb3f00d4af4','circle_cos':'2907fc18-ef26-5825-bc1f-b4cb4bdbf7cb','circle_sin':'5649582e-ddb6-5db4-a7c3-699a007eaafe','cubic':'a6c30ef5-4b00-5501-a5b6-18892cf4af06','fractional':'b920de5e-825e-5dcf-9aac-175e4a51e8a1','involute':'38682a53-16b6-5629-9f8b-b56796ac3444','mixed_fractional':'b920de5e-825e-5dcf-9aac-175e4a51e8a1'}
def L(e): return sp.latex(sp.sympify(e),ln_notation=True).replace(r'\log',r'\ln')
def G(e): return '('+L(e)+')'
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+s))
def digest(o): return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def eq(a,b): return sp.simplify(sp.trigsimp(a-b))==0



def math_data(f,p):
    c=p['c'];lo,hi=p['lower'],p['upper']
    if f in ('sum','reciprocal'):
        a,b=p['a'],p['b'];x,y=a*T,a*T+b;v=abs(a)*sp.sqrt(2);F=c*(X+Y) if f=='sum' else c/(Y-X)
    elif f=='product':
        a,b=p['a'],p['b'];x,y=a*T,b*T;v=sp.sqrt(a*a+b*b);F=c*X*Y
    elif f.startswith('circle'):
        R,o=p['R'],p['orientation'];x,y=R*sp.cos(T),o*R*sp.sin(T);v=R;F=c*(2*X**2-R**2) if f=='circle_cos' else c*Y**2
    elif f=='cubic':
        a,b=p['a'],p['b'];x,y=a*T**2,b*T**2;v=2*sp.sqrt(a*a+b*b)*T;F=c*(X**3-p['k']*Y**3)
    elif f in ('fractional','mixed_fractional'):
        s=p['s'];x,y=sp.Rational(4,3)*s*T**sp.Rational(3,2),s*(T*T/2-T);v=s*(T+1);F=c*X+(p.get('d',0))*Y
    else:
        A=p['A'];x,y=A*(sp.cos(T)+T*sp.sin(T)),A*(sp.sin(T)-T*sp.cos(T));v=A*T;F=c*(X**2+Y**2)+p['d']
    sub=sp.expand(F.subs({X:x,Y:y}));sub=sp.trigsimp(sub)
    if f=='circle_cos':sub=c*p['R']**2*sp.cos(2*T)
    if f=='involute':sub=c*p['A']**2*(1+T*T)+p['d']
    I=sp.expand(sub*v);primitive=sp.integrate(I,T);value=sp.simplify(primitive.subs(T,hi)-primitive.subs(T,lo))
    return x,y,F,v,sub,I,primitive,value




def source_parameters(f,c):
    # Independently derived source mathematical components, not answer lookups.
    base={
        'product':dict(a=3,b=4,c=c,lower=0,upper=1),
        'sum':dict(a=1,b=1,c=c,lower=0,upper=1),
        'reciprocal':dict(a=1,b=-4,c=c,lower=0,upper=4),
        'circle_cos':dict(R=4,c=c,orientation=1,lower=0,upper=sp.pi/4),
        'circle_sin':dict(R=2,c=c,orientation=1,lower=0,upper=sp.pi/4),
        'cubic':dict(a=4,b=3,c=c,k=2,lower=0,upper=1),
        'fractional':dict(s=1,c=3*c,lower=0,upper=1),
        'involute':dict(A=3,c=c,d=0,lower=0,upper=2*sp.pi)}
    return {k:sp.sympify(v) for k,v in base[f].items()}


def align(rows):
    return '$$\n'+r'\begin{aligned}'+'\n'+(' \\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'

def display(tex): return '$$\n'+tex+'\n$$'
def dint(e,lo,hi): return r'\int_{'+L(lo)+'}^{'+L(hi)+'} '+e+r'\,\mathrm{d}t'
def vec(x,y): return r'\langle '+L(x)+', '+L(y)+r'\rangle'

def solution(f,p,data):
    x,y,F,v,sub,I,P,value=data;lo,hi=p['lower'],p['upper']
    rows=[r"\mathbf r'(t)&="+vec(sp.diff(x,T),sp.diff(y,T)),r"\|\mathbf r'(t)\|&=\sqrt{"+G(sp.diff(x,T))+'^2+'+G(sp.diff(y,T))+'^2}']
    notes=[];subrows=[]
    if f.startswith('circle'):
        rows.append(r'&=\sqrt{'+L(p['R']**2)+r'(\sin^2t+\cos^2t)}='+L(v))
        if f=='circle_cos':
            subrows=[r'f(\mathbf r(t))&='+G(p['c'])+r'\left(2'+G(x)+'^2-'+L(p['R']**2)+r'\right)',r'&='+G(p['c']*p['R']**2)+r'(2\cos^2t-1)',r'&='+L(sub)]
            notes.append(r'Use $2\cos^2t-1=\cos 2t$.')
        else:
            subrows=[r'f(\mathbf r(t))&='+G(p['c'])+G(y)+'^2',r'&='+L(p['c']*p['R']**2)+r'\sin^2t',r'&='+G(p['c']*p['R']**2/2)+r'(1-\cos 2t)']
            notes.append(r'Use $\sin^2t=(1-\cos 2t)/2$.')
    elif f=='involute':
        A=p['A'];c=p['c'];d=p['d']
        rows=[r"x'(t)&="+G(A)+r'(-\sin t+\sin t+t\cos t)='+L(sp.diff(x,T)),r"y'(t)&="+G(A)+r'(\cos t-\cos t+t\sin t)='+L(sp.diff(y,T)),r"\|\mathbf r'(t)\|&=\sqrt{"+L(A*A)+r't^2(\cos^2t+\sin^2t)}',r'&='+L(A)+r'|t|='+L(v)]
        notes.append(r'The product-rule terms cancel in each derivative. On the supplied interval, $t\geq0$, so $|t|=t$.')
        subrows=[r'x(t)^2+y(t)^2&='+L(A*A)+r'\bigl[(\cos t+t\sin t)^2',r'&\qquad +(\sin t-t\cos t)^2\bigr]',r'&='+L(A*A)+r'\bigl[\cos^2t+\sin^2t',r'&\qquad +t^2(\sin^2t+\cos^2t)\bigr]',r'&='+L(A*A)+r'(1+t^2)',r'f(\mathbf r(t))&='+G(c*A*A)+r'(1+t^2)+'+G(d),r'&='+L(sub)]
        notes.append(r'In the sum of squared coordinates, the two mixed terms cancel.')
    elif f in ('fractional','mixed_fractional'):
        rows.extend([r'&=\sqrt{'+L(p['s']**2)+r'\bigl(4t+(t-1)^2\bigr)}',r'&='+L(p['s'])+r'|t+1|='+L(v)])
        notes.append(r'Since $t\geq0$, the speed simplifies using $4t+(t-1)^2=(t+1)^2$ and $|t+1|=t+1$.')
        subrows=[r'f(\mathbf r(t))&='+G(p['c'])+G(x)+(('+'+G(p['d'])+G(y)) if f=='mixed_fractional' else ''),r'&='+L(sub)]
    elif f=='product':
        rows.append(r'&='+L(v))
        subrows=[r'f(\mathbf r(t))&='+G(p['c'])+G(x)+G(y),r'&='+L(sub)]
    elif f=='cubic':
        n=sp.sqrt(p['a']**2+p['b']**2)
        rows.extend([r'&='+L(2*n)+r'|t|='+L(v)])
        notes.append(r'On this interval $t\geq0$, so $|t|=t$.')
        subrows=[r'f(\mathbf r(t))&='+G(p['c'])+r'\left('+G(x)+'^3-'+G(p['k'])+G(y)+r'^3\right)',r'&='+L(sub)]
    else:
        rows.append(r'&='+L(v))
        if f=='sum': subrows=[r'f(\mathbf r(t))&='+G(p['c'])+r'\left('+G(x)+'+'+G(y)+r'\right)',r'&='+L(sub)]
        else: subrows=[r'f(\mathbf r(t))&=\frac{'+L(p['c'])+'}{'+G(y)+'-'+G(x)+'}',r'&=\frac{'+L(p['c'])+'}{'+L(p['b'])+'}='+L(sub)]
    # Family-owned primitive forms, never a separate CAS-rendered solution path.
    if f=='circle_sin': Pshown=G(p['c']*p['R']**3/2)+r'\left(t-\frac{\sin 2t}{2}\right)'
    elif f=='circle_cos': Pshown=G(p['c']*p['R']**3/2)+r'\sin 2t'
    else: Pshown=L(P)
    derivation=[r'\int_C f\,\mathrm{d}s&='+dint(G(sub)+r'\cdot '+G(v),lo,hi)]
    if f=='circle_sin': derivation.append(r'&='+G(p['c']*p['R']**3/2)+dint(r'1-\cos 2t',lo,hi))
    else: derivation.append(r'&='+dint(L(I),lo,hi))
    derivation += [r'&=\left['+Pshown+r'\right]_{'+L(lo)+'}^{'+L(hi)+'}',r'&='+G(sp.simplify(P.subs(T,hi)))+'-'+G(sp.simplify(P.subs(T,lo))),r'&='+L(value)]
    return ('Use the scalar line-integral formula\n\n'+display(r'\int_C f\,\mathrm{d}s=\int_a^b f(\mathbf r(t))\,\|\mathbf r\,\!\prime(t)\|\,\mathrm{d}t.')
        .replace(r'\mathbf r\,\!\prime(t)',r"\mathbf r'(t)")+'\n\nDifferentiate both coordinates and compute the speed:\n\n'+align(rows)+'\n\n'+' '.join(notes)+'\n\nSubstitute the coordinates into the density:\n\n'+align(subrows)+'\n\nMultiply by the speed and integrate, subtracting the lower endpoint:\n\n'+align(derivation))

# Each complete profile is selected before incidental values. Names describe
# concrete mathematical errors; banks never contain arbitrary offsets.
PROFILES={
 'measure':('omit_speed','speed_squared','density_a','component_speed'),
 'density':('omit_speed','speed_squared','density_a','density_b'),
 'evaluation':('speed_squared','density_b','density_a','power_error'),
 'orientation':('omit_speed','negate_omit_speed','wrong_sign','density_a'),
}

def error_values(f,p,data):
    x,y,F,v,sub,I,P,z=data;lo,hi=p['lower'],p['upper'];c=p['c']
    def D(e): return sp.simplify(sp.integrate(sp.expand(e),(T,lo,hi)))
    # For zero-speed endpoints sub/v has an integrable limit in these families.
    component=abs(p['a']) if f in ('sum','reciprocal','product') else (p['R']*sp.sin(T) if lo>=0 else sp.Abs(p['R']*sp.sin(T))) if f.startswith('circle') else 2*p['s']*sp.sqrt(T) if f in ('fractional','mixed_fractional') else p['A'] if f=='involute' else abs(p['a'])*2*T
    errors={'omit_speed':D(sub),'speed_squared':D(sub*v*v),'component_speed':D(sub*component),'wrong_sign':-z}
    if f=='sum':
        errors.update(constant_only=D(c*p['b']*v),offset_sign=D(c*(2*p['a']*T-p['b'])*v),density_a=D(c*2*p['a']*T*v),density_b=D(c*y*v),power_error=D(c*(2*p['a']*T+p['b'])*v)+D(c*2*p['a']*T*v))
        # power_error integrates the linear term as t^2 instead of t^2/2.
    elif f=='product':
        errors.update(density_a=D(c*x*v),density_b=D(c*y*v),power_error=sp.Rational(3,2)*z)
    elif f=='reciprocal':
        errors.update(density_a=D(c*p['b']*v),density_b=D(c/(2*p['b'])*v),power_error=D(c*v))
    elif f=='circle_cos':
        errors.update(density_a=D(c*2*x*x*v),density_b=D(c*(x*x-p['R']**2)*v),power_error=2*z,omit_double_angle=D(c*p['R']**3*sp.cos(T)),wrong_trig_primitive=2*D(c*p['R']**3*sp.sin(2*T)))
    elif f=='circle_sin':
        R=p['R'];Q=c*R**3*(T/2+sp.sin(2*T)/4);W=c*R**3*(T/2-sp.sin(2*T)/2)
        errors.update(density_a=D(c*y*v),density_b=sp.simplify(Q.subs(T,hi)-Q.subs(T,lo)),power_error=sp.simplify(W.subs(T,hi)-W.subs(T,lo)))
    elif f=='cubic':
        errors.update(density_a=D(c*(x**3-y**3)*v),density_b=D(c*(x**3+p['k']*y**3)*v),power_error=sp.Rational(8,7)*z)
    elif f=='fractional':
        s=p['s'];Q=sp.Rational(4,3)*c*s*s*(T**sp.Rational(7,2)/sp.Rational(5,2)+T**sp.Rational(5,2)/sp.Rational(3,2))
        errors.update(density_a=D(c*x*p['s']*T),density_b=D(c*x*p['s']),power_error=sp.simplify(Q.subs(T,hi)-Q.subs(T,lo)))
    elif f=='mixed_fractional':
        errors.update(density_a=D(c*x*v),density_b=D(p['d']*y*v),power_error=D(c*x*v-p['d']*y*v))
    else:
        A=p['A'];d=p['d']
        errors.update(density_a=D(c*A*A*(1+T*T)*v),density_b=D((c*A*A+d)*v),power_error=D((c*A*A+d)*v)+sp.Rational(4,3)*D(c*A*A*T*T*v))
    errors['negate_omit_speed']=-errors['omit_speed']
    return errors

def sample(f,r):
    signs=(-2,-1,1,2)
    if f in ('sum','reciprocal'):
        lo=r.choice((-1,0,1)); return dict(a=r.choice((-2,-1,1,2)),b=r.choice((-4,-3,-2,-1,1,2,3,4)),c=r.choice(signs),lower=lo,upper=lo+r.choice((1,2,3)))
    if f=='product':
        a,b=r.choice(((1,1),(3,4),(4,3)));lo=r.choice((-1,0,1))
        return dict(a=a*r.choice((-1,1)),b=b*r.choice((-1,1)),c=r.choice((-1,1)),lower=lo,upper=lo+1)
    if f.startswith('circle'):
        # Double-angle endpoints include one/two nonzero contributions and zero.
        bounds=((0,sp.pi/4),(sp.pi/4,sp.pi/2),(0,sp.pi/2),(-sp.pi/4,sp.pi/4),(sp.pi/6,sp.pi/3))
        lo,hi=r.choice(bounds)
        return dict(R=r.choice((2,3,4)),c=r.choice((-1,1)),orientation=r.choice((-1,1)),lower=lo,upper=hi)
    if f=='cubic':
        a,b=r.choice(((3,4),(4,3)));return dict(a=a*r.choice((-1,1)),b=b*r.choice((-1,1)),c=r.choice((-1,1)),k=r.choice((1,2)),lower=0,upper=1)
    if f in ('fractional','mixed_fractional'):
        lo,hi=r.choice(((0,1),(1,2))) if f=='fractional' else (0,1)
        p=dict(s=r.choice((1,2)),c=r.choice((-3,-1,1,3)),lower=lo,upper=hi)
        if f=='mixed_fractional':p['d']=r.choice((-2,-1,1,2))
        return p
    lo,hi=r.choice(((0,1),(1,2),(0,2)))
    A=r.choice((1,2,3)); c=r.choice((-1,1))
    return dict(A=A,c=c,d=r.choice((-c*A*A,-2,-1,0,1,2)),lower=lo,upper=hi)

def make(level,f,p,profile='density',seed=0,observed_bank=None):
    if f not in FAMILIES[level]:raise ValueError('family/level mismatch')
    p={k:sp.sympify(v) for k,v in p.items()}; data=math_data(f,p)
    x,y,F,v,sub,I,P,z=data;lo,hi=p['lower'],p['upper']
    if not lo<hi: raise ValueError('increasing interval required')
    if f not in ('sum','reciprocal','product') and not f.startswith('circle') and lo<0:raise ValueError('nonnegative interval required')
    if observed_bank is not None:
        bank=[('observed_'+str(i),normalize_tex(a)) for i,a in enumerate(observed_bank)]
        # Key comes from the derivation, never a presumed position.
    else:
        errors=error_values(f,p,data);selected=PROFILES[profile]
        if f=='circle_cos' and profile=='evaluation':
            # A mistaken sine/cosine primitive may give zero on symmetric
            # bounds even when the true double-angle integral is nonzero.
            selected=('speed_squared','density_b','density_a','wrong_trig_primitive')
        if f=='sum' and z==0:
            # Scale and orientation mistakes also vanish at cancellation.
            profile='cancellation_sum'; selected=('density_a','density_b','constant_only','offset_sign')
        if f=='involute' and p['d']==0:
            # Omitting an absent offset is not an error. Use the same complete
            # radial-density error bank at every scale, sign and interval.
            profile='radial'; selected=('omit_speed','speed_squared','density_b','power_error')
        if f=='circle_cos' and z==0:
            profile='cancellation'; selected=('density_a','density_b','omit_double_angle','wrong_trig_primitive')
        values=[('correct',z)]+[(name,errors[name]) for name in selected]
        if any(e.has(sp.oo,sp.zoo,sp.nan) or e.is_real is not True for _,e in values):raise ValueError('invalid bank')
        if any(eq(a[1],b[1]) for i,a in enumerate(values) for b in values[:i]):raise ValueError('bank collision')
        bank=[(name,normalize_tex(L(e))) for name,e in values]
    prompt='Evaluate the line integral\n\n'+display(r'\int_C '+G(F)+r'\,\mathrm{d}s,')+'\n\nwhere $C$ is parametrized by\n\n'+display(r'\mathbf r(t)='+vec(x,y)+'.')+'\n\nThe parameter interval is $'+L(lo)+r'\leq t\leq '+L(hi)+'$.'
    prompt=normalize_prose(prompt);sol=normalize_prose(solution(f,p,data))
    if observed_bank is not None and z.is_Rational:
        numeric=bank[0][1]
        try: numeric_value=sp.Rational(numeric)
        except (TypeError,ValueError): numeric_value=None
        if numeric_value==z and '.' in numeric:
            sol=sol.rsplit(r'\end{aligned}',1)[0].rstrip()+r' \\'+'\n&='+numeric+'\n'+r'\end{aligned}'+'\n$$'
    identity=digest({'version':VERSION,'prompt':prompt,'solution':sol,'bank':sorted(a for _,a in bank),'level':level})
    fid=uid(identity+':selection')
    answers=[{':answer/id':uid(fid+':'+tex),':answer/type':':answer.type/math',':answer/value':tex} for _,tex in bank]
    correct=answers[0]
    random.Random(seed).shuffle(answers)
    q={':question/id':uid(identity),':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct[':answer/id']]}]}
    r={'knowledge_point':KP,'question':q,'generation':{'version':VERSION,'template':f,'bank_profile':profile,'parameters':{k:str(a) for k,a in p.items()},'seed':seed,'source_ids':[SOURCE_IDS[f]],'source_basis':7399,'role':'evaluate_scalar_ds','displayed_final':L(z),'derivation':{'density':str(sub),'speed':str(v),'integrand':str(I),'primitive':str(P)},'recipes':dict(bank)}}
    return validate_generated_record(r)

def generate(level,seed=0,template=None,parameters=None,profile=None):
    r=random.Random(seed);f=template or r.choice(FAMILIES[level]);profile=profile or r.choice(tuple(PROFILES))
    for attempt in range(100):
        try:return make(level,f,parameters if parameters is not None else sample(f,r),profile,seed)
        except ValueError as ex:
            if parameters is not None or str(ex) not in ('bank collision','invalid bank'):raise
    raise RuntimeError('No distinct complete bank for '+f+'/'+profile)

def semantic_key(record):
    # Ignore density amplitude and the bank. Never deliver amplitude-only clones
    # of the same curve, density shape and interval within a finite batch.
    p=record['generation']['parameters'].copy();p.pop('c',None)
    if record['generation']['template']=='involute':p['d/c']=str(sp.sympify(p.pop('d'))/sp.sympify(record['generation']['parameters']['c']))
    return (record['generation']['template'],json.dumps(p,sort_keys=True))

def bank_signature(record):
    """Numerical ranks computed from exact constructed values, never rounding."""
    q=record['question'];field=q[':question/answer-fields'][0];cid=field[':answer-field/correct'][1]
    # Exact values are already available in the derivation/error construction.
    f=record['generation']['template'];p={k:sp.sympify(v) for k,v in record['generation']['parameters'].items()};data=math_data(f,p);z=data[-1];errors=error_values(f,p,data)
    names=tuple(record['generation']['recipes']);vals=[z if n=='correct' else errors[n] for n in names]
    rank=sum(bool(sp.N(a-z,30)<0) for a in vals)
    magnitude=sum(bool(sp.N(abs(a)-abs(z),30)<0) for a in vals)
    return rank,magnitude,z==0


def batch(level,count,seed):
    r=random.Random(seed);out=[];seen=set();schedule=[];byfamily={}
    for i in range(count):
        if not schedule:schedule=list(FAMILIES[level]);r.shuffle(schedule)
        f=schedule.pop();prior=byfamily.get(f,[])
        for attempt in range(200):
            rec=generate(level,r.getrandbits(63),template=f);key=semantic_key(rec)
            if key in seen:continue
            sig=bank_signature(rec)
            # A finite repeated-family bank must not teach a fixed numerical
            # rank or magnitude rank. Once a witness differs, no balance quota
            # applies. Two zero-result instances are also insufficient evidence
            # of the non-cancelling member of this same supported family.
            if prior and (all(x[0]==sig[0] for x in prior) or all(x[1]==sig[1] for x in prior) or (sig[2] and all(x[2] for x in prior))):continue
            break
        else:raise ValueError('Requested batch exceeds distinct supported instances')
        seen.add(key);out.append(rec);byfamily.setdefault(f,[]).append(sig)
    return out

def replay_sources():
    captured=json.loads(Path(__file__).with_name('replay-data.json').read_text())
    byid={q[':question/id']:q for q in captured['sources']}
    out=[]
    for f in ('sum','reciprocal','circle_cos','circle_sin','cubic'):
        q=byid[SOURCE_IDS[f]];level='easy' if f in FAMILIES['easy'] else 'moderate'
        old=q[':question/answer-fields'][0]; key=old[':answer-field/correct'][':answer/id']
        choices=sorted(old[':answer-field/choices'],key=lambda a:a[':answer/id']!=key)
        rec=make(level,f,source_parameters(f,1),'source_replay',0,observed_bank=[a[':answer/value'] for a in choices])
        rec['generation']['replay_source_id']=q[':question/id'];out.append(rec)
    return out

def replay_exemplars():
    qs=json.loads(Path(__file__).with_name('replay-data.json').read_text())['exemplars']
    out=[]
    for q,f,p in zip(qs,('sum','circle_sin','involute'),(dict(a=2,b=1,c=1,lower=0,upper=1),dict(R=2,c=1,orientation=1,lower=0,upper=sp.pi/2),dict(A=2,c=1,d=-2,lower=0,upper=1))):
        old=q[':question/answer-fields'][0];key=old[':answer-field/correct'][':answer/id']
        choices=sorted(old[':answer-field/choices'],key=lambda a:a[':answer/id']!=key)
        rec=make(q[':question/difficulty'][':db/ident'].split('/')[-1],f,p,'exemplar_replay',0,observed_bank=[a[':answer/value'] for a in choices])
        rec['generation']['replay_source_id']=q[':question/id'];out.append(rec)
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=('easy','moderate','hard','unclassified','all'),default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json',),default='json');args=ap.parse_args()
    if args.count<1:ap.error('count must be positive')
    levels=('easy','moderate','hard') if args.difficulty=='all' else ('easy' if args.difficulty=='unclassified' else args.difficulty,)
    print(json.dumps([rec for level in levels for rec in batch(level,args.count,args.seed)],indent=2,ensure_ascii=False))
if __name__=='__main__':main()
