#!/usr/bin/env python3
"""Scalar line integral CONSTRUCTION on 2D segments; local draft, no EDB writes.

Five source families, five complete public observed evidence banks and five
separate complete method-derived default banks. Source wrapper is math2275.
Moderate/hard rational-coordinate workloads are authored, never observed labels.
Full solutions retain family-specific source notation, prose and stage masks.
All choices are compared as real definite values, including incorrect pairs.
Use .venv/bin/python; see sibling evidence/README.md for validation.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from dataclasses import dataclass
from functools import lru_cache
import sympy as s

KP_ID=17592186179724
KP_UUID='189f51d6-494f-515a-bf77-59496421b093'
TITLE='Constructing a Line Integral Along a Segment in the Cartesian Plane'
VERSION='segment-construction-1'
SOURCE={'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
X,Y,T=s.symbols('x y t', real=True)
FAMILIES=('quadratic','log','cos','linear','exp')
SOURCE_IDS=dict(zip(FAMILIES,('q-123127','q-123269','q-123268','q-123279','q-123283')))
FUNCTIONS={'quadratic':X**2-Y,'log':s.log(X+Y),'cos':1+X-s.cos(Y),'linear':2*X+Y,'exp':s.exp(X+Y)}
FUNCTION_TEX={'quadratic':r'{x}^{2}-y','log':r'\operatorname{ln}⁡(x+y)','cos':r'1+x-\operatorname{cos}⁡y','linear':'2x+y','exp':r'{e}^{x+y}'}
PROFILES={f'{f}_observed':{'family':f,'origin':'observed empirical evidence','eligible_for_learning':False} for f in FAMILIES}
PROFILES.update({f'{f}_method':{'family':f,'origin':'authored method bank','eligible_for_learning':True} for f in FAMILIES})

class SampleRejected(ValueError): pass

def tex(a):
    return s.latex(s.sympify(a),order='lex').replace('t^{2}','{t}^{2}').replace('x^{2}','{x}^{2}').replace(r' \sqrt',r'\sqrt')

def poly(a,var=T,constant_first=False):
    a=s.expand(a)
    if a==0:return '0'
    terms=[]
    p=s.Poly(a,var)
    for (power,),coef in p.terms():
        body=(('' if abs(coef)==1 else tex(abs(coef)))+('t' if power==1 else '{t}^{'+str(power)+'}')) if power else tex(abs(coef))
        terms.append(('-' if coef<0 else '+')+body)
    if constant_first:terms.reverse()
    return ''.join(terms).lstrip('+')

def affine(a,d,constant_first=False):return poly(a+d*T,constant_first=constant_first)
def group(z):return '('+z+')'
def vector(a,b,coordinate=False):
    parts=[]
    for val,name in ((a,'i'),(b,'j')):
        val=s.sympify(val)
        if val==0:continue
        if val.is_number:
            sign='-' if val<0 else '+'
            body=name if abs(val)==1 else tex(abs(val))+r'\,'+name
        else:
            z=str(val) if isinstance(val,str) else tex(val)
            body=(group(z) if '+' in z or '-' in z[1:] else z)+r'\,'+name
            sign='+'
        parts.append(sign+body)
    return ''.join(parts).lstrip('+') or '0'

def coord_vector(xt,yt):
    out=''
    for z,name in ((xt,'i'),(yt,'j')):
        if z=='0':continue
        if z in ('1','-1'):part=('-' if z=='-1' else '')+name
        else:part=(group(z) if '+' in z or '-' in z[1:] else z)+r'\,'+name
        out+=('+' if out and not part.startswith('-') else '')+part
    return out or '0'

def compound(z):return '+' in z or '-' in z[1:]
def function_arg(z):return group(z) if compound(z) or z.startswith('-') or r'\frac' in z else z
def poswrap(z):return group(z) if compound(z) else z
def signed_square(z):return group(tex(z))+'^{2}' if z<0 else '{'+tex(z)+'}^{2}'
def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'

def exprtex(expr,family):
    if family in ('linear','quadratic'):return poly(expr)
    if family=='log':return r'\operatorname{ln}⁡'+group(poly(expr.args[0],constant_first=True)) if expr.func==s.log else tex(expr)
    if family=='exp':return '{e}^{'+(poly(expr.args[0]) if expr.func==s.exp else '0')+'}'
    # Preserve source cos notation, never allow CAS to introduce other functions.
    if not expr.atoms(s.cos):return poly(expr)
    other=s.expand(expr+s.cos(next(iter(expr.atoms(s.cos))).args[0]))
    arg=next(iter(expr.atoms(s.cos))).args[0]
    z=poly(arg)
    return poly(other)+r'-\operatorname{cos}⁡'+function_arg(z)

@dataclass(frozen=True)
class Integral:
    factor:s.Expr
    integrand:s.Expr
    family:str
    def latex(self):
        p='' if self.factor==1 else tex(self.factor)
        inner=exprtex(self.integrand,self.family)
        inner=group(inner) if self.family in ('linear','quadratic','cos') else inner
        return p+r'{\int }_{0}^{1}'+inner+(r'\,' if self.family in ('log','exp') else '')+r'\text{d}t'
    def value(self):return definite(self.factor,self.integrand)

@lru_cache(maxsize=12000)
def definite(factor, integrand):
    # Exact definite objects. Used only in author validation, never learner solutions.
    total=0
    for term in s.Add.make_args(s.expand(integrand)):
        coef,body=term.as_independent(T,as_Add=False)
        if body.func in (s.log,s.exp,s.cos):
            arg=body.args[0];slope=s.diff(arg,T);offset=arg.subs(T,0)
            if slope==0:part=body
            elif body.func==s.exp:part=(s.exp(offset+slope)-s.exp(offset))/slope
            elif body.func==s.cos:part=(s.sin(offset+slope)-s.sin(offset))/slope
            else:
                primitive=lambda z:z*s.log(z)-z
                part=(primitive(offset+slope)-primitive(offset))/slope
            total+=coef*part
        else:
            total+=coef*s.integrate(body,(T,0,1))
    return s.expand(factor*total)

def equal_values(a,b):
    d=s.expand(a-b)
    if d==0:return True
    if d.is_algebraic:d=s.simplify(d)
    if d==0:return True
    # Distinct finite exact transcendental expressions: evaluate at 70 digits;
    # unresolved near-zero comparisons reject rather than certify a unique bank.
    v=s.N(d,70)
    if v.is_real is not True or not v.is_finite:raise SampleRejected('non-real/undefined definite value')
    if abs(v)<s.Float('1e-50',70):
        if s.simplify(d)==0:return True
        raise SampleRejected('unresolved definite-value equivalence')
    return False

def parameters_checked(level,family,parameters,observed=False):
    if set(parameters)!=set(('ax','ay','bx','by')):raise ValueError('exactly ax,ay,bx,by required')
    p={k:s.Rational(str(v)) for k,v in parameters.items()}
    if any(abs(v)>6 for v in p.values()):raise ValueError('coordinate magnitude ceiling 6')
    dx,dy=p['bx']-p['ax'],p['by']-p['ay']
    if dx==dy==0:raise ValueError('zero-length segment')
    if abs(dx)>6 or abs(dy)>6:raise ValueError('displacement magnitude ceiling 6')
    denoms=[int(v.q) for v in p.values()]
    if level=='easy' and any(d!=1 for d in denoms):raise ValueError('easy integer coordinates')
    if level=='moderate' and (denoms.count(2)!=1 or any(d not in (1,2) for d in denoms) or dx==0 or dy==0):raise ValueError('moderate exactly one half-coordinate, both components change')
    if level=='hard' and (denoms.count(2)!=1 or denoms.count(3)!=1 or any(d not in (1,2,3) for d in denoms) or dx==0 or dy==0):raise ValueError('hard exactly one half and one third coordinate, both components change')
    if family=='exp' and (p['ax']!=0 or p['ay']!=0):raise ValueError('exponential origin mask keeps initial endpoint zero')
    if family in ('exp','log') and dx+dy==0:raise ValueError('nonconstant exponent/log argument required')
    if family=='linear' and 2*dx+dy==0:raise ValueError('nonconstant affine pullback required')
    if family=='log' and min(p['ax']+p['ay'],p['bx']+p['by'])<=0:raise ValueError('log argument must remain positive on entire segment')
    return p

def components(family,p):
    ax,ay,bx,by=[p[k] for k in ('ax','ay','bx','by')]
    dx,dy=bx-ax,by-ay
    xt,yt=ax+dx*T,ay+dy*T
    pull=s.expand(FUNCTIONS[family].subs({X:xt,Y:yt},simultaneous=True))
    speed=s.sqrt(dx**2+dy**2)
    return ax,ay,bx,by,dx,dy,xt,yt,pull,speed

def bank(family,p,profile):
    ax,ay,bx,by,dx,dy,xt,yt,pull,L=components(family,p)
    correct=Integral(L,pull,family) # computed before wrong members
    if profile.endswith('_method'):
        choices=[correct,Integral(1,pull,family),Integral(L**2,pull,family),
                 Integral(L,s.expand(FUNCTIONS[family].subs({X:ax,Y:yt},simultaneous=True)),family),
                 Integral(L,s.expand(FUNCTIONS[family].subs({X:xt,Y:ay},simultaneous=True)),family)]
    elif family=='quadratic':
        wrong=T**2+yt
        choices=[correct,Integral(L,wrong,family),Integral(abs(ay),T**2-yt,family),Integral(L**2,pull,family),Integral(s.sqrt(2),wrong,family)]
    elif family=='log':
        w1=s.log(ay-ax+dx*T);w2=s.log(yt+2*dx*T);wrongL=s.sqrt(dx**2+(dy+dx)**2)
        choices=[correct,Integral(1,w1,family),Integral(1,w2,family),Integral(wrongL,w2,family),Integral(wrongL,pull,family)]
    elif family=='cos':
        w1=dy*T+ax-s.cos(dx*T);w2=dx**2*T-s.cos(dy*T)
        choices=[correct,Integral(L,w1,family),Integral(L,w2,family),Integral(L**2,w1,family),Integral(L**2,pull,family)]
    elif family=='linear':
        # Underidentified evidence: a three-equal-component norm built from
        # the coordinate difference, not a fitted multiplier of the answer.
        # This deliberately has no eligibility for ordinary learner output.
        alteredL=s.sqrt(3*(dx-dy)**2)
        w1=2*dx*T+ax;w2=(2*dx-dy)*T+2*bx+by
        choices=[correct,Integral(alteredL,pull,family),Integral(L**2,w1,family),Integral(L,w2,family),Integral(alteredL,w2,family)]
    else:
        alteredL=s.sqrt((dx+1)**2+dy**2)
        w1=s.exp((-dx+dy)*T);w2=s.exp(-dx*T)
        choices=[correct,Integral(alteredL,w1,family),Integral(2*abs(dx)+abs(dy),w2,family),Integral(alteredL,pull,family),Integral(L,w1,family)]
    # Whole-bank domain and equivalence rejection, never replace one wrong choice.
    for item in choices:
        if s.sympify(item.factor).is_real is not True or item.factor<=0:raise SampleRejected('nonpositive/non-real prefactor')
        for lg in item.integrand.atoms(s.log):
            arg=lg.args[0]
            if min(arg.subs(T,0),arg.subs(T,1))<=0:raise SampleRejected('bank log argument not positive')
    values=[c.value() for c in choices]
    for i,a in enumerate(values):
        for b in values[:i]:
            if equal_values(a,b):raise SampleRejected('definite-value bank collision')
    return choices

def solution(family,p):
    ax,ay,bx,by,dx,dy,xt,yt,pull,L=components(family,p)
    start='('+tex(ax)+','+tex(ay)+')';end='('+tex(bx)+','+tex(by)+')'
    a,b,d=vector(ax,ay),vector(bx,by),vector(dx,dy)
    # Source family order: positive y-offset first for quadratic/linear, t first
    # in cos, constants first in log, pure t in exponential.
    tx=affine(ax,dx, family=='log');ty=affine(ay,dy,family in ('quadratic','linear','log'))
    finalvec=coord_vector(tx,ty)
    rows=[r'r(t) & =a+t\,(b-a)']
    if family=='exp':rows += [r' & =0+t\,(b-0)',r' & =t(b)',r' & =t('+b+')',r' & ='+finalvec]
    else:
        rows += [r' & ='+poswrap(a)+r'+t['+(group(b) if compound(b) else b)+'-'+poswrap(a)+']']
        if d=='-i':rows += [r' & ='+poswrap(a)+r'-t\,i']
        else:rows += [r' & ='+poswrap(a)+r'+t('+d+')']
        rows += [r' & ='+finalvec]
    derivative=[r'{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j',
                r' & =\frac{\text{d}}{\text{d}t}('+tx+r')i+\frac{\text{d}}{\text{d}t}('+ty+')j',
                r' & ='+d,r'‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}',
                r' & =\sqrt{'+signed_square(dx)+'+'+signed_square(dy)+'}']
    if family=='exp':derivative.append(r' & =\sqrt{'+tex(dx**2+dy**2)+'}')
    derivative.append(r' & ='+tex(L))
    inner=exprtex(pull,family)
    if family=='quadratic':sub=group(tx)+'^{2}-'+group(ty)
    elif family=='log':sub=r'\operatorname{ln}⁡'+group((group(tx) if compound(tx) else tx)+'+'+ty)
    elif family=='cos':sub='1+'+group(tx)+r'-\operatorname{cos}⁡'+function_arg(ty)
    elif family=='linear':sub='2'+group(tx)+'+'+group(ty)
    else:sub='{e}^{'+tx+('+' if not ty.startswith('-') else '')+ty+'}'
    inside=group(inner) if family in ('quadratic','linear','cos') else inner
    integ=[r'{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t',
           r' & ={\int }_{0}^{1}'+inside+r'\cdot '+tex(L)+r'\cdot \text{d}t',
           r' & ='+Integral(L,pull,family).latex()+'.']
    return ('We will use the formula\n\n$$\n'+r'{\int }_{C}f(x,y)\,\text{d}s={\int }_{{t}_{a}}^{{t}_{b}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t,'+'\n$$\n\n \n\nwhere $C$ is the line segment from $'+start+'$ to $'+end+'.$ \n\nThe position vectors of the endpoints of our line segment are $a='+a+'$ and $b='+b+'.$ So, the parametrization of the line segment is given by\n\n'+aligned(rows)+'\n\nwhere $0\\le t\\le 1.$ Thus, we have that $x='+tx+'$ and $y='+ty+'$ along the segment.\n\nComputing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:\n\n'+aligned(derivative)+'\n\nNow, since $f(x,y)='+FUNCTION_TEX[family]+'$, we obtain\n\n'+aligned(['f(r(t)) & ='+sub,r' & ='+inner+'.'])+'\n\nTherefore, we can write the integral as\n\n'+aligned(integ))

def sample(level,family,rng):
    vals=[s.Integer(i) for i in range(-4,5)]
    p=dict(zip(('ax','ay','bx','by'),rng.choices(vals,k=4)))
    if family=='log':p=dict(zip(p,rng.choices([s.Integer(i) for i in range(1,5)],k=4)))
    if family=='exp':p['ax']=p['ay']=s.Integer(0)
    slots=['bx','by'] if family=='exp' else list(p)
    if level=='moderate':p[rng.choice(slots)]+=s.Rational(1,2)
    if level=='hard':
        half,third=rng.sample(slots,2);p[half]+=s.Rational(1,2);p[third]+=s.Rational(1,3)
    return {k:str(v) for k,v in p.items()}

def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def task_fingerprint(pull,L):
    a=s.srepr(s.expand(L*pull));b=s.srepr(s.expand((L*pull).subs(T,1-T)))
    return digest(min(a,b))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
    rng=random.Random(seed)
    family=template or (PROFILES[profile]['family'] if profile else rng.choice(FAMILIES))
    if family not in FAMILIES:raise ValueError('unknown template')
    profile=profile or family+'_method'
    if profile not in PROFILES or PROFILES[profile]['family']!=family:raise ValueError('profile-family mismatch')
    for attempt in range(500):
        try:
            p=parameters_checked(level,family,parameters if parameters is not None else sample(level,family,rng),profile.endswith('_observed'))
            choices=bank(family,p,profile)
            break
        except (SampleRejected,ValueError):
            if parameters is not None:raise
    else:raise SampleRejected('no eligible entire bank in 500 attempts')
    sol=solution(family,p)
    prompt='Which of the following is equivalent to the line integral of the function $f(x,y)='+FUNCTION_TEX[family]+',$ traversed along the line segment from $('+tex(p['ax'])+','+tex(p['ay'])+')$ to $('+tex(p['bx'])+','+tex(p['by'])+')?$'
    L=components(family,p)[-1];pull=components(family,p)[-2]
    fp=task_fingerprint(pull,L)
    values=[c.latex() for c in choices]
    content=digest({'version':VERSION,'level':level,'prompt':prompt,'solution':sol,'values':sorted(values)})
    qid=uuid.uuid5(uuid.UUID(KP_UUID),content);fid=uuid.uuid5(qid,'selection')
    answers=[{':answer/id':str(uuid.uuid5(fid,'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=answers[0][':answer/id'];rng.shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
            'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},
            'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':s.__version__,'seed':seed,'template':family,'parameters':{k:str(v) for k,v in p.items()},'bank_profile':profile,'bank_origin':PROFILES[profile]['origin'],'eligible_for_learning':PROFILES[profile]['eligible_for_learning'],'authored_extension':not profile.endswith('_observed') or level!='easy','source_analysis':{**SOURCE,'question_ids':[SOURCE_IDS[family]]},'parameter_fingerprint':fp,'mathematical_task_fingerprint':fp,'content_fingerprint':content,'plot_rating':'none','plot_assets':{},'domain':'0 <= t <= 1; nonzero speed; every logarithm argument positive on the whole interval'}}

# Difficulty sections share the SAME construction and family-specific stages.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];field=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in field[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=FAMILIES);ap.add_argument('--profile',choices=PROFILES)
    args=ap.parse_args();records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
