#!/usr/bin/env python3
"""Seeded, relocatable polar double-integral generator. No database operations."""
from __future__ import annotations
import argparse, copy, hashlib, json, os, random, uuid
from functools import lru_cache
from pathlib import Path
import sympy as S
from audit_presentation import problem as _ca_problem
from math_format import normalize_prose, normalize_tex, validate_generated_record
HERE=Path(__file__).resolve().parent
VERSION='polar-double-v3-display-audit-9837-v1'
KP={'db_id':17592186129200,'id':'5b97f75d-c784-5f3a-984d-f9a5fdf21d61','title':'Evaluating a Double Integral by Converting To Polar Coordinates'}
x,y=S.symbols('x y',real=True);r=S.Symbol('r',nonnegative=True);t=S.Symbol('theta',real=True)
pi=S.pi
FAMILIES={'easy':['odd','square','radial','exponential'],'moderate':['affine','rational','radial','radical'],'hard':['radical','ratio']}
SOURCES={'odd':['q-161050'],'square':['q-161052'],'radial':['q-161054'],'exponential':['q-161053'],'affine':['q-38140','q-83520'],'rational':['q-83970'],'radical':['q-83968'],'ratio':['q-161055']}
# Closed coordinate-aligned sectors; strings are Cartesian restrictions visible before feedback.
SECTORS=[(0,pi/2,r'x\ge0,\ y\ge0'),(pi/2,pi,r'x\le0,\ y\ge0'),(pi,3*pi/2,r'x\le0,\ y\le0'),(-pi/2,0,r'x\ge0,\ y\le0'),(0,pi,r'y\ge0'),(-pi/2,pi/2,r'x\ge0'),(pi,2*pi,r'y\le0'),(pi/2,3*pi/2,r'x\le0')]
def tex(a):return normalize_tex(S.latex(S.sympify(a)).replace(r'\log',r'\ln'))
def digest(a):return hashlib.sha256(json.dumps(a,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(a):return str(uuid.uuid5(uuid.NAMESPACE_URL,a))
def same(a,b):return S.simplify(S.trigsimp(a-b))==0
def safe_scalar(expr):
    # Algebraic simplification must not move coefficients into logarithm/exponential arguments.
    protected={node:S.Dummy() for node in S.sympify(expr).atoms(S.log,S.exp)}
    return S.factor_terms(S.cancel(S.sympify(expr).xreplace(protected))).xreplace({v:k for k,v in protected.items()})


def model(p):
    R=S.Integer(p['R']);c=S.Integer(p.get('c',1));f=p['family'];axis=p.get('axis','y')
    if p['geometry']=='disk':lo,hi,restriction=0,2*pi,'';up=R
    elif p['geometry']=='sector':lo,hi,restriction=SECTORS[p['sector']];up=R
    else:
        # Four center orientations, reflected halves or full shifted disk.
        sign=p['sign']; side=p['side']
        if axis=='y':
            lo,hi=(0,pi) if sign==1 else (-pi,0)
            if side=='positive':lo,hi=(0,pi/2) if sign==1 else (-pi/2,0)
            elif side=='negative':lo,hi=(pi/2,pi) if sign==1 else (-pi,-pi/2)
            up=sign*R*S.sin(t);perp='x'
        else:
            lo,hi=(-pi/2,pi/2) if sign==1 else (pi/2,3*pi/2)
            if side=='positive':lo,hi=(0,pi/2) if sign==1 else (pi/2,pi)
            elif side=='negative':lo,hi=(-pi/2,0) if sign==1 else (pi,3*pi/2)
            up=sign*R*S.cos(t);perp='y'
        restriction='' if side=='whole' else perp+(r'\ge0' if side=='positive' else r'\le0')
    trig=S.sin(t) if p.get('component','y')=='y' else S.cos(t)
    coord=y if p.get('component','y')=='y' else x
    if f=='odd':
        fn=c*(x*x*y if p['component']=='y' else x*y*y)
        h=S.cos(t)**2*S.sin(t) if p['component']=='y' else S.sin(t)**2*S.cos(t)
        density=c*r**4*h;radial=c*r**5*h/5
    elif f=='square':fn=c*coord**2;density=c*r**3*trig**2;radial=c*r**4*trig**2/4
    elif f=='radial':fn=c*(x*x+y*y);density=c*r**3;radial=c*r**4/4
    elif f=='exponential':fn=c*S.exp(x*x+y*y);density=c*r*S.exp(r*r);radial=c*S.exp(r*r)/2
    elif f=='affine':
        a,b=S.Integer(p['a']),S.Integer(p['b']);fn=a*x+b*y;density=r*r*(a*S.cos(t)+b*S.sin(t));radial=r**3*(a*S.cos(t)+b*S.sin(t))/3
    elif f=='rational':fn=c/(x*x+y*y+1);density=c*r/(r*r+1);radial=c*S.log(r*r+1)/2
    elif f=='radical':fn=c*coord*S.sqrt(x*x+y*y);density=c*r**3*trig;radial=c*r**4*trig/4
    else:
        coord,denom=(x,y) if axis=='y' else (y,x)
        trign,trigd=(S.cos(t),S.sin(t)) if axis=='y' else (S.sin(t),S.cos(t))
        fn=c*coord/denom;density=c*r*trign/trigd;radial=c*r*r*trign/(2*trigd)
    angular=safe_scalar(radial.subs(r,up)-radial.subs(r,0))
    # Construct familiar angular primitives, never a CAS-rendered alternative identity.
    if f=='odd':P=-c*R**5*S.cos(t)**3/15 if p['component']=='y' else c*R**5*S.sin(t)**3/15
    elif f=='square':P=c*R**4/8*(t+ (1 if p['component']=='x' else -1)*S.sin(2*t)/2)
    elif f=='radial':P=c*R**4*t/4
    elif f=='exponential':P=c*(S.exp(R*R)-1)*t/2
    elif f=='affine':P=R**3*(p['a']*S.sin(t)-p['b']*S.cos(t))/3
    elif f=='rational':P=c*S.log(R*R+1)*t/2
    elif f=='radical' and p['geometry']!='shift':P=c*R**4/4*(S.sin(t) if p['component']=='x' else -S.cos(t))
    elif f=='radical':P=c*R**4/20*(S.sin(t)**5 if axis=='y' else -S.cos(t)**5)
    else:P=c*R**2/4*(S.sin(t)**2 if axis=='y' else -S.cos(t)**2)
    ans=safe_scalar(P.subs(t,hi)-P.subs(t,lo))
    return dict(fn=fn,density=density,radial=radial,angular=angular,primitive=P,answer=ans,lo=lo,hi=hi,up=up,restriction=restriction)

def sample(level,rng,family=None):
    f=family or rng.choice(FAMILIES[level]);p={'family':f,'geometry':'disk' if level=='easy' else 'shift' if level=='hard' else 'sector','R':rng.choice([1,2,3]),'c':rng.choice([-3,-2,-1,1,2,3])}
    if f=='exponential':p['R']=rng.choice([2,3])
    if f in ('odd','square'):p['component']=rng.choice(['x','y'])
    if level=='moderate':p['sector']=rng.randrange(8) if f in ('affine','radial') else rng.randrange(4)
    if f=='affine':p.update(a=rng.choice([-3,-2,-1,1,2,3]),b=rng.choice([-3,-2,-1,1,2,3]));p.pop('c')
    if f=='radical':p['component']=rng.choice(['x','y'])
    if level=='hard':
        p.update(axis=rng.choice(['x','y']),sign=rng.choice([-1,1]),side=rng.choice(['positive','negative','whole']))
        if f=='radical':p['component']='x' if p['axis']=='y' else 'y'
    return p

def errors(p,m):
    """Actual mathematical mistakes, with no arbitrary additive fallback."""
    A=m['answer'];R=S.Integer(p['R']);c=S.Integer(p.get('c',1));f=p['family'];lo,hi=m['lo'],m['hi'];P=m['primitive']
    if A==0:
        if f=='odd':
            v=c*R**5/15
            return {'first quadrant only':v,('upper half only' if p['component']=='y' else 'right half only'):2*v,'absolute angular factor':4*v,'third quadrant only':-v,('reverse upper half' if p['component']=='y' else 'reverse right half'):-2*v,'omit radial divisor and restrict quadrant':5*v}
        if f=='affine':
            vx=S.simplify(R**3*p['a']/3*(S.sin(hi)-S.sin(lo)));vy=S.simplify(-R**3*p['b']/3*(S.cos(hi)-S.cos(lo)))
            return {'omit y term':vx,'omit x term':vy,'reverse y sign':2*vx,'reverse x sign':2*vy,'omit divisor and omit y':3*vx,'omit divisor and omit x':3*vy}
        # Whole shifted disk: one signed half instead of the full angular interval.
        q=dict(p,side='positive');v=model(q)['answer']
        return {'positive half only':v,'negative half only':-v,'halve positive-half result':v/2,'omit radial divisor on positive half':v*(4 if f=='radical' else 2),'omit angular substitution divisor on negative half':-v*(5 if f=='radical' else 2),'double negative-half result':-2*v}
    e={'reverse bound subtraction':-A,'use radial upper bound divided by two':A/2**(4 if f in ('square','radial','radical') else 2 if f=='ratio' else 3)}
    # Wrong radial upper limit for nonhomogeneous integrands is evaluated exactly.
    if f=='exponential':
        e['use radial upper bound divided by two']=c*(hi-lo)*(S.exp(R*R/4)-1)/2
        e.update({'omit lower radial endpoint':c*(hi-lo)*S.exp(R*R)/2,'use R instead of R squared':c*(hi-lo)*(S.exp(R)-1)/2,'lose radial substitution factor':2*A,'double angular extent':2*A,'halve angular extent':A/2})
    elif f=='rational':
        e['use radial upper bound divided by two']=c*(hi-lo)*S.log(R*R/4+1)/2
        e.update({'omit angular integration':c*S.log(R*R+1)/2,'lose radial substitution factor':2*A,'omit logarithm':c*(hi-lo)*R*R/2,'double angular extent':2*A,'halve angular extent':A/2})
    elif f=='affine':
        e.update({'omit Jacobian':S.Rational(3,2)*A/R,'omit radial divisor':3*A,'full disk instead of sector':S.Integer(0),'omit x term':S.simplify(-R**3*p['b']/3*(S.cos(hi)-S.cos(lo))),'omit y term':S.simplify(R**3*p['a']/3*(S.sin(hi)-S.sin(lo)))})
    elif f in ('square','radial'):
        e.update({'omit Jacobian':4*A/(3*R),'omit radial divisor':4*A,'odd symmetry applied to even function':S.Integer(0),'halve radius and omit radial divisor':A/4,'halve angular extent':A/2,'double angular extent':2*A})
    elif f=='radical':
        e['omit radial divisor']=4*A
        if p['geometry']=='shift':
            e['omit angular substitution divisor']=5*A
            Q=c*p['sign']*R**3/12*(S.sin(t)**4 if p['axis']=='y' else -S.cos(t)**4)
            e['omit Jacobian']=S.simplify(Q.subs(t,hi)-Q.subs(t,lo))
            e['use full shifted disk']=S.Integer(0)
            e['double boundary coefficient']=16*A
            e['use constant radial bound']=c*R**4/4*(S.sin(hi)-S.sin(lo) if p['component']=='x' else -S.cos(hi)+S.cos(lo))
        else:e['omit Jacobian']=4*A/(3*R);e['full disk instead of sector']=S.Integer(0);e['double angular extent']=2*A
    else:e.update({'omit radial divisor':2*A,'omit Jacobian':c*p['sign']*R*(S.sin(hi)-S.sin(lo) if p['axis']=='y' else -S.cos(hi)+S.cos(lo)),'symmetry over whole shifted disk':S.Integer(0),'omit angular substitution divisor':2*A,'double boundary coefficient':4*A})
    # Reversing subtraction after a genuine earlier error is also a genuine compound error.
    # It prevents a sign pair from identifying the correct magnitude in the bank alone.
    for name,value in list(e.items()):
        if value!=0 and not same(value,A) and not same(value,-A):
            e[name+'; reverse subtraction']=-value
    return {k:safe_scalar(v) for k,v in e.items()}

def bank(p,m,rng):
    # A complete endpoint-error profile puts the common argument/coefficient cues on
    # an incorrect radial endpoint, rather than preserving them on the key.
    if p['family'] in ('rational','exponential') and rng.randrange(3)==0:
        R=S.Integer(p['R']);c=S.Integer(p['c']);angle=m['hi']-m['lo']
        endpoint=lambda z: S.log(z*z+1) if p['family']=='rational' else S.exp(z*z)-1
        v=c*angle*endpoint(R/2)/2;w=c*angle*endpoint(2*R)/2
        vs=[m['answer'],v,2*v,-v,w]
        if all(not same(a,b) for i,a in enumerate(vs) for b in vs[i+1:]):
            return [safe_scalar(z) for z in vs],['correct','halve radial bound','halve radial bound; omit substitution factor','halve radial bound; reverse subtraction','double radial bound']
        raise ValueError('Endpoint profile has colliding alternatives')
    candidates=errors(p,m);names=list(candidates)
    paired=m['answer']!=0 and rng.choice([False,True])
    for _ in range(200):
        if paired:
            bases=[n for n in names if n+'; reverse subtraction' in candidates]
            n=rng.choice(bases)
            remainder=[z for z in names if z not in (n,n+'; reverse subtraction') and not same(candidates[z],-m['answer'])]
            profile=[n,n+'; reverse subtraction']+rng.sample(remainder,2)
        else:profile=rng.sample(names,4)
        vs=[m['answer']]+[candidates[n] for n in profile]
        if all(not same(a,b) for i,a in enumerate(vs) for b in vs[i+1:]):return vs,['correct']+profile
    raise ValueError('No distinct plausible complete error profile')

@lru_cache(maxsize=256)
def plot_cached(serial,output):
    # Cache is local to a process; content-addressed files survive deterministic replay.
    p=json.loads(serial);m=model(p);out=Path(output)/('region-'+digest(p)[:20]+'.png')
    if out.exists():return str(out)
    os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-polar-mpl')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    R=p['R'];angles=np.linspace(float(m['lo']),float(m['hi']),601)
    rad=R if p['geometry']!='shift' else p['sign']*R*(np.sin(angles) if p['axis']=='y' else np.cos(angles))
    xx=rad*np.cos(angles);yy=rad*np.sin(angles)
    fig,ax=plt.subplots(figsize=(4.8,4.5));lim=R*1.3
    ax.fill(np.r_[0,xx,0],np.r_[0,yy,0],color='#dbeaf5',ec='#2673a8',lw=1.7)
    for end,start in [((lim,0),(-lim,0)),((0,lim),(0,-lim))]:ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','color':'#444'})
    ax.text(lim,.04*R,'$x$');ax.text(.04*R,lim,'$y$');ax.text(-.08*R,-.13*R,'$0$')
    mid=(float(m['lo'])+float(m['hi']))/2;rm=R*.4
    if p['geometry']=='shift':rm=R*.45
    ax.text(rm*np.cos(mid),rm*np.sin(mid),'$D$',ha='center',va='center',color='#154f78')
    if p['geometry']=='shift':eq=tex(x*x+y*y)+'='+tex(p['sign']*R*(x if p['axis']=='x' else y))
    else:eq=tex(x*x+y*y)+'='+tex(R*R)
    ax.set_title('$'+eq+'$',fontsize=13,pad=14)
    for v in (-R,R):ax.text(v,-.12*R,'$'+str(v)+'$',ha='center');ax.text(-.1*R,v,'$'+str(v)+'$',ha='right')
    ax.set(xlim=(-lim*1.08,lim*1.08),ylim=(-lim*1.08,lim*1.08),aspect='equal');ax.axis('off');fig.tight_layout();out.parent.mkdir(parents=True,exist_ok=True);fig.savefig(out,dpi=140,facecolor='white');plt.close(fig)
    return str(out)

def diagram(p,output_dir):return plot_cached(json.dumps(p,sort_keys=True),str(Path(output_dir).resolve()))
def aligned(rows):return '$$\n'+r'\begin{aligned}'+(' \\\\\n'.join(rows))+r'\end{aligned}'+'\n$$'

def worked(p,m,img):
    f=p['family'];lo,hi,up=[tex(m[k]) for k in ('lo','hi','up')];P=tex(m['primitive']);G=tex(m['angular']);A=tex(m['answer'])
    out='Use $x=r\\cos\\theta$, $y=r\\sin\\theta$ and $dA=r\\,dr\\,d\\theta$, with $r\\ge0$.\n\n'
    if p['geometry']=='shift':
        axis=p['axis'];sR=tex(p['sign']*p['R']);trig=r'\sin\theta' if axis=='y' else r'\cos\theta'
        out+=aligned([r'x^2+y^2&='+sR+axis,r'r^2&='+sR+'r'+trig,r'r&='+up+r'\quad(r>0)'])
        out+='\nThe selected part of the circle gives the angular interval below; the origin is included at the radial lower bound.\n\n'
    else:out+='The Cartesian restrictions give the following polar region.\n\n'
    out+='![]('+img+')\n\n'
    out+=aligned([r'0\le r&\le '+up,lo+r'\le\theta&\le '+hi])
    if f in ('radial','rational','exponential','radical'):
        out+='\nHere $x^2+y^2=r^2(\\cos^2\\theta+\\sin^2\\theta)=r^2$.'
    if f=='radical':out+=' Since $r\\ge0$, $\\sqrt{x^2+y^2}=r$.'
    if f=='square':out+='\nUse $'+(r'\sin^2\theta=\frac{1-\cos(2\theta)}{2}' if p['component']=='y' else r'\cos^2\theta=\frac{1+\cos(2\theta)}{2}')+'$ for the angular integral.'
    if f=='exponential':out+='\nFor the radial primitive, set $u=r^2$, so $du=2r\\,dr$.'
    if f=='rational':out+='\nFor the radial primitive, set $u=r^2+1$, so $du=2r\\,dr$; its logarithm is defined since $r^2+1>0$.'
    if f=='radical' and p['geometry']=='shift':out+='\nFor the angular primitive use $u='+ (r'\sin\theta$, $du=\cos\theta\,d\theta$.' if p['axis']=='y' else r'\cos\theta$, $du=-\sin\theta\,d\theta$.')
    if f=='ratio':out+='\nThe denominator vanishes only at boundary endpoints. Interpret angular endpoints as one-sided limits. Radial evaluation cancels the apparent singularity, leaving the continuous angular expression below, so the improper integral converges.'
    radial=tex(m['radial']);density=tex(m['density']);fn=tex(m['fn'])
    outer=lambda body:r'\int_{'+lo+'}^{'+hi+'}'+body+r'\,d\theta'
    inner=r'\int_0^{'+up+'}'+density+r'\,dr'
    out+='\n\n'+aligned([r'\iint_D '+fn+r'\,dA&='+outer(inner),r'&='+outer(r'\left['+radial+r'\right]_0^{'+up+'}'),r'&='+outer(r'\left('+G+r'\right)'),r'&=\left['+P+r'\right]_{'+lo+'}^{'+hi+'}',r'&=\left('+tex(m['primitive'].subs(t,m['hi']))+r'\right)-\left('+tex(m['primitive'].subs(t,m['lo']))+r'\right)',r'&='+A])
    return out

def finalize(question,meta,rng):
    q=copy.deepcopy(question)
    for k in (':question/problem',':question/worked-solution'):q[k]=normalize_prose(q[k])
    q[':question/problem']=_ca_problem(q[':question/problem'])
    field=q[':question/answer-fields'][0]
    for a in field[':answer-field/choices']:a[':answer/value']=normalize_tex(a[':answer/value'])
    # IDs follow normalization, and exclude machine-specific output-directory paths.
    core=[q[':question/problem'],q[':question/worked-solution'],sorted(a[':answer/value'] for a in field[':answer-field/choices'])]
    import re
    core=[re.sub(r'!\[\]\([^)]*/(region-[0-9a-f]+\.png)\)',r'![](\1)',v) if isinstance(v,str) else v for v in core]
    key=digest([VERSION,core]);qid=uid(key);fid=uid(key+'/selection');oldcorrect=field[':answer-field/correct'][1]
    correct=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==oldcorrect)
    q[':question/id']=qid;field[':answer-field/id']=fid
    for a in field[':answer-field/choices']:a[':answer/id']=uid(fid+'/'+a[':answer/value'])
    field[':answer-field/correct']=[':answer/id',uid(fid+'/'+correct)];rng.shuffle(field[':answer-field/choices'])
    meta.update(version=VERSION,content_hash=key)
    record={'knowledge_point':KP,'question':q,'generation':meta}
    return validate_generated_record(record)

def generate(level,seed=0,family=None,parameters=None,output_dir=None):
    if level not in FAMILIES:raise ValueError('Unknown difficulty')
    output_dir=output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not output_dir:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR for generated assets')
    rng=random.Random(seed)
    for attempt in range(200):
        p=dict(parameters) if parameters is not None else sample(level,rng,family)
        if p['family'] not in FAMILIES[level]:raise ValueError('Family outside difficulty')
        m=model(p)
        try:vs,ops=bank(p,m,rng);break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('Unable to construct a valid bank')
    img=diagram(p,output_dir)
    region=('the disk $x^2+y^2\\le '+tex(p['R']**2)+'$' if p['geometry']=='disk' else 'the portion of the disk $x^2+y^2\\le '+tex(p['R']**2)+'$ where $'+m['restriction']+'$')
    if p['geometry']=='shift':
        region='the '+('whole disk' if p['side']=='whole' else 'part of the disk where $'+m['restriction']+'$')+' bounded by $x^2+y^2='+tex(p['sign']*p['R']*(x if p['axis']=='x' else y))+'$, shown below'
    prompt='Evaluate $\\iint_D '+tex(m['fn'])+'\\,dA$, where $D$ is '+region+'.'
    if p['geometry']=='shift':prompt+='\n\n![]('+img+')'
    choices=[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':tex(v)} for i,v in enumerate(vs)]
    q={':question/problem':prompt,':question/worked-solution':worked(p,m,img),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/type':':answer-field.type/radio',':answer-field/key':'selection',':answer-field/choices':choices,':answer-field/correct':[':answer/id','0']}]}
    return finalize(q,{'seed':seed,'family':p['family'],'parameters':p,'bank_profile':ops[1:],'choice_errors':{tex(v):op for v,op in zip(vs,ops)},'source_ids':SOURCES[p['family']],'authored_extension':True,'derivation':{k:tex(v) for k,v in m.items() if k!='restriction'},'attempts':attempt+1},rng)

REPLAY_PARAMETERS={
'q-38140':('moderate',dict(family='affine',geometry='sector',R=2,a=2,b=1,sector=4)),
'q-83968':('hard',dict(family='radical',geometry='shift',R=1,c=1,axis='y',component='x',sign=-1,side='positive')),
'q-161050':('easy',dict(family='odd',geometry='disk',R=1,c=15,component='y')),
'q-161052':('easy',dict(family='square',geometry='disk',R=3,c=4,component='y')),
'q-161053':('easy',dict(family='exponential',geometry='disk',R=2,c=1)),
'q-161054':('easy',dict(family='radial',geometry='disk',R=3,c=2)),
'q-161055':('hard',dict(family='ratio',geometry='shift',R=2,c=1,axis='y',sign=1,side='positive')),
'q-83970':('moderate',dict(family='rational',geometry='sector',R=1,c=2,sector=2)),
'q-83520':('moderate',dict(family='affine',geometry='sector',R=2,a=1,b=-1,sector=0))}

def replay(source_id,output_dir):
    q=copy.deepcopy(next(q for q in json.loads((HERE/'source-replays.json').read_text()) if q[':question/math-academy-id']==source_id))
    level,p=REPLAY_PARAMETERS[source_id];m=model(p);img=diagram(p,output_dir)
    # Preserve original prompt and complete bank; rebuild the derivation from the same parameters.
    # This removes two documented transcription slips without changing imported records.
    def clean(z):
        if isinstance(z,dict):return {k:clean(v) for k,v in z.items() if k!=':db/id'}
        if isinstance(z,list):return [clean(a) for a in z]
        return z
    q=clean(q);field=q[':question/answer-fields'][0]
    for a in field[':answer-field/choices']:a[':answer/type']=':answer.type/math'
    field[':answer-field/type']=':answer-field.type/radio'
    if isinstance(field[':answer-field/correct'],dict):field[':answer-field/correct']=[':answer/id',field[':answer-field/correct'][':answer/id']]
    q.pop(':question/math-academy-id',None);q[':question/difficulty']=':question.difficulty/'+level;q[':question/worked-solution']=worked(p,m,img)
    source_key=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
    q[':question/worked-solution']=q[':question/worked-solution'].replace('&='+tex(m['answer'])+r'\end{aligned}', '&='+normalize_tex(source_key)+r'\end{aligned}')
    return finalize(q,{'source_ids':[source_id],'family':p['family'],'parameters':p,'bank_profile':'source-replay','authored_extension':False,'derivation':{k:tex(v) for k,v in m.items() if k!='restriction'}},random.Random(0))

def batch(level,count,seed,output_dir):
    capacity={'easy':102,'moderate':1224,'hard':432}[level]
    if count>capacity:raise ValueError('Requested count exceeds distinct supported semantic instances: '+str(capacity))
    rng=random.Random(seed);families=list(FAMILIES[level]);result=[];seen=set();bank_signatures={}
    # A shuffled cycle chooses the mathematical family before values. No seed-specific rule.
    while len(result)<count:
        rng.shuffle(families)
        for f in families:
            record=generate(level,rng.randrange(2**63),f,output_dir=output_dir)
            semantic=digest(record['generation']['parameters'])
            if semantic in seen:continue
            # In a small delivered pool, repeated nonzero instances must not all
            # reward a fixed bank position or numerical/magnitude rank. Repair
            # the bank for the SAME mathematical instance, not the seed or key.
            # Zero from symmetry is an intended mathematical decision.
            def signature(rec):
                field=rec['question'][':question/answer-fields'][0]
                correct=tex(model(rec['generation']['parameters'])['answer'])
                key_index=next(i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/value']==correct)
                instance=model(rec['generation']['parameters'])
                candidates={tex(v):v for v in [instance['answer']]+list(errors(rec['generation']['parameters'],instance).values())}
                # Endpoint profiles add exact radial-bound errors beyond errors().
                if rec['generation']['family'] in ('rational','exponential'):
                    pp=rec['generation']['parameters'];R=S.Integer(pp['R']);c=S.Integer(pp['c']);angle=instance['hi']-instance['lo']
                    endpoint=lambda z:S.log(z*z+1) if pp['family']=='rational' else S.exp(z*z)-1
                    for v in [c*angle*endpoint(R/2)/2,c*angle*endpoint(R/2),-c*angle*endpoint(R/2)/2,c*angle*endpoint(2*R)/2]:candidates[tex(safe_scalar(v))]=v
                values=[candidates[a[':answer/value']] for a in field[':answer-field/choices']]
                A=instance['answer']
                return (key_index,sum(bool(S.N(v)<S.N(A)) for v in values),sum(bool(S.N(abs(v))<S.N(abs(A))) for v in values))
            A=model(record['generation']['parameters'])['answer']
            history=bank_signatures.setdefault(f,[])
            if A!=0 and history:
                for retry in range(200):
                    sig=signature(record)
                    if all(len({prior[j] for prior in history}|{sig[j]})>1 for j in range(3)):break
                    record=generate(level,rng.randrange(2**63),parameters=record['generation']['parameters'],output_dir=output_dir)
                else:raise ValueError('Cannot diversify a repeated nonzero bank profile')
            if A!=0:history.append(signature(record))
            seen.add(semantic);result.append(record)
            if len(result)==count:break
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay');args=ap.parse_args()
    if args.count<1:ap.error('--count must be positive')
    out=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not out:ap.error('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required')
    records=[replay(args.replay,out)] if args.replay else batch('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed,out)
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
