#!/usr/bin/env python3
"""Two dependent linear equations -> complete affine family. No DB or plots.

Observed public raw profiles omit ratings, worked solutions and answer keys.
The five-option historical bank is an opaque replay pattern, not a default.
Normal banks are whole method-derived banks, chosen before any parameters.
Exact integers/rationals only. Runtime uses the project .venv Python/SymPy.
Easy isolates an integral affine expression (unit reduced y coefficient);
moderate divides exactly one term into a noninteger fraction; hard divides BOTH
terms into noninteger fractions with reduced denominators 3..6. These missing
level labels are authored, anchored to e-14014, q-208832 and the lesson route.
No counts-only assessment, nonlinear equations, third variable or later KP.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
import sympy as sp
KP_ID=17592186073778
KP_UUID='50351666-c691-510f-863c-168c61f9980b'
TITLE='Finding the General Solution to a System With Infinitely Many Intersection Points'
VERSION='dependent-general-family-1'
LEVELS=('easy','moderate','hard')
TEMPLATES=('radio_family','blank_coordinate')
PROFILES=('method','raw_25524','raw_208832')
X=sp.Symbol('x')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,x))
def tex(v):return sp.latex(sp.Rational(v))
def poly(terms):
    out=''
    for coeff,var in terms:
        coeff=sp.Rational(coeff)
        if not coeff:continue
        term=('' if abs(coeff)==1 and var else tex(abs(coeff)))+var
        out+=('-' if coeff<0 else '')+term if not out else (' - ' if coeff<0 else ' + ')+term
    return out or '0'
def lhs(a,b):return poly(((a,'x'),(b,'y')))
def aff(m,k,var='x',constant_first=False):return poly(((k,''),(m,var))) if constant_first else poly(((m,var),(k,'')))
def aligned(rows):return '$$\n'+r'\begin{aligned}'+'\n'+' \\\\\n'.join(rows)+'\n'+r'\end{aligned}'+'\n$$'
def rows(p):
    a,b,c,r=(sp.Rational(p[k]) for k in ('a','b','c','r'))
    return [(a,b,c),(r*a,r*b,r*c)]
def parameters(p):
    if set(p)-{'a','b','c','r','variable'} or not all(k in p for k in ('a','b','c','r')):raise ValueError('Require a,b,c,r; optional variable x/t/u')
    out={k:str(sp.Rational(p[k])) for k in ('a','b','c','r')}
    out['variable']=p.get('variable','x')
    if out['variable'] not in ('x','t','u'):raise ValueError('Unknown parameter alias')
    return out

def guard(level,p,raw=False):
    a,b,c,r=(sp.Rational(p[k]) for k in ('a','b','c','r'))
    if not all((a,b,c,r)) or not all(v.q==1 for row in rows(p) for v in row):raise ValueError('Nonzero coefficients/constant and integral displayed equations required')
    if max(abs(v) for row in rows(p) for v in row[:2])>24 or max(abs(row[2]) for row in rows(p))>36:raise ValueError('Displayed coefficient <=24 and constant <=36')
    if abs(r) not in (sp.Rational(1,4),sp.Rational(1,3),sp.Rational(1,2),1,2,3,4):raise ValueError('Source-grounded row multiplier')
    m,k=-a/b,c/b
    # Apply level claims to the reduced mathematical object, never hidden GCFs.
    if level=='easy':
        if m.q!=1 or k.q!=1 or not 2<=abs(m)<=6 or not 1<=abs(k)<=8:raise ValueError('Easy integral slope2..6/intercept1..8')
    elif level=='moderate':
        if (m.q>1)+(k.q>1)!=1 or max(m.q,k.q)>4 or max(abs(m),abs(k))>8:raise ValueError('Moderate exactly one fractional term, denominator2..4, magnitude<=8')
    elif level=='hard':
        if not(3<=m.q<=6 and 3<=k.q<=6 and max(abs(m),abs(k))<=8):raise ValueError('Hard both fractional terms, reduced denominators3..6, magnitude<=8')
    else:raise ValueError('Unknown difficulty')
    return m,k

def prompt(p,template,raw=False):
    eq=[lhs(a,b)+' ='+('' if c<0 else ' ')+tex(c) for a,b,c in rows(p)]
    var=p['variable']
    if template=='radio_family':return f'Find all points of intersection of the lines ${eq[0]}$ and ${eq[1]}$.'
    start=f'Describe the points that lie on the intersection of the lines ${eq[0]}$ and ${eq[1]}$. Express your answer in terms of ${var}$ only.'
    return start+('' if raw else '\n\n')+f'The intersection points are $({var}$,\n'+'{{field-1}}'+f'\n$)$, where ${var}$ is any number.'

def solution(p):
    (a,b,c),(d,e,f)=rows(p);r=d/a;var=p['variable'];m,k=-a/b,c/b
    eq=[lhs(a,b)+' = '+tex(c),lhs(d,e)+' = '+tex(f)]
    out='The points of intersection of the lines correspond to the solutions of the following system:\n\n$$\n'+r'\{'+ '; '.join(eq)+'\n$$\n\n'
    out+=f'We will solve the system using elimination. Notice that if we multiply the first equation by ${tex(-r)}$, then we will get a ${poly(((-d,"x"),))}$ term that can cancel with the ${poly(((d,"x"),))}$ term in the second equation:\n\n'
    out+='$$\n'+r'\{'+eq[0]+r' \mid \mid \cdot ('+tex(-r)+'); '+eq[1]+'\n$$\n\n'
    out+='When we add the two equations, it turns out that both variables cancel, and we obtain a true statement:\n\n'
    sumtex=tex(-r*c)+(' + ' if f>=0 else ' - ')+tex(abs(f))
    out+=aligned([lhs(-d,-e)+' &= '+tex(-f),lhs(d,e)+' &= '+tex(f),'0 &= ('+sumtex+')','0 &= 0'])
    out+='\n\nBecause we obtained a true statement, we conclude that there are infinitely many solutions to the system. Therefore, the lines have infinitely many intersection points.\n\n'
    out+='We want to find an expression that represents every solution to the system. Any value of $x$ can be chosen, and we can find the corresponding $y$-coordinate for each $x$-coordinate by solving one of the lines for $y$, as follows:\n\n'
    numerator=poly(((c,''),(-a,'x')))
    out+=aligned([lhs(a,b)+' &= '+tex(c),poly(((b,'y'),))+' &= '+numerator,'y &= '+r'\frac{'+numerator+'}{'+tex(b)+'}','y &= '+aff(m,k,constant_first=True)])
    if var!='x':out+=f'\n\nLet ${var}=x$ be the free coordinate.'
    out+='\n\nTherefore, the points of intersection are\n\n$$\n'+r'\left('+var+','+aff(m,k,var,True)+r' \right)'+'\n$$\n\n'+f'where ${var}$ is any number.'
    return out

def bank(p,profile):
    a,b,c,r=(sp.Rational(p[k]) for k in ('a','b','c','r'));m,k=-a/b,c/b;v=p['variable']
    if profile=='raw_25524':
        # Exact structural historical pattern; interpretations deliberately opaque.
        return [f'({v}, '+aff(k,-m,v)+')',f'({v}, '+aff(1,k,v)+')',f'({v}, '+aff(m,k,v)+')',f'({v}, '+aff(1,m,v)+')',f'({v}, '+aff(m,-k,v)+')'],['swap_slope_intercept_negate','unit_slope','correct','unit_slope_swap_intercept','negate_intercept']
    return [f'({v}, '+aff(mm,kk,v)+')' for mm,kk in [(m,k),(-m,k),(m,-k),(-b/a,c/a),(0,k)]],['correct','move_x_without_sign_change','negate_constant','isolate_x_but_use_as_y','drop_x_term']

def canonical_family(pair):
    """Affine image signature, invariant to nonzero parameter rescale and shift."""
    xx,yy=map(sp.expand,pair);symbols=xx.free_symbols|yy.free_symbols
    if len(symbols)>1:raise ValueError('One free parameter required')
    z=next(iter(symbols),X)
    dx,dy=sp.diff(xx,z),sp.diff(yy,z)
    if dx.has(z) or dy.has(z) or (dx==0 and dy==0):return ('point',str(xx),str(yy)) if not symbols else ('non_affine',str(xx),str(yy))
    normal=sp.Matrix([dy,-dx,-dy*xx.subs(z,0)+dx*yy.subs(z,0)])
    pivot=next(v for v in normal if v!=0)
    return tuple(str(sp.simplify(v/pivot)) for v in normal)

def fingerprint(p,template=None):
    a,b,c,_=(sp.Rational(p[k]) for k in ('a','b','c','r'))
    return digest({'line':tuple(str(v/a) for v in (a,b,c)),'assessed':'complete_general_family'})

def sample(level,rng,profile):
    for _ in range(10000):
        if level=='easy':b=rng.choice([-1,1]);a=rng.choice([-6,-5,-4,-3,-2,2,3,4,5,6]);c=rng.choice([i for i in range(-8,9) if i])
        else:
            b=rng.choice([-1,1])*rng.randint(2,4 if level=='moderate' else 6)
            a=rng.choice([i for i in range(-12,13) if i]);c=rng.choice([i for i in range(-12,13) if i])
        r=rng.choice([-4,-3,-2,2,3,4]);p=parameters(dict(a=a,b=b,c=c,r=r,variable=rng.choice(['x','t','u'])))
        try:guard(level,p);eligible_bank(p,profile)
        except ValueError:continue
        return p
    raise ValueError('No eligible whole instance in bounded sampler')

def eligible_bank(p,profile):
    vals,recipes=bank(p,profile)
    if profile.startswith('raw_'):return vals,recipes
    a,b,c,r=(sp.Rational(p[k]) for k in ('a','b','c','r'));m,k=-a/b,c/b
    objects=[(X,mm*X+kk) for mm,kk in [(m,k),(-m,k),(m,-k),(-b/a,c/a),(0,k)]]
    signatures=[canonical_family(v) for v in objects]
    if len(set(signatures))!=5:raise ValueError('Whole bank has equivalent affine families')
    target=canonical_family((X,m*X+k))
    if signatures.count(target)!=1:raise ValueError('Whole bank ambiguous')
    return vals,recipes

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unknown difficulty')
    profile=profile or 'method'
    if profile not in PROFILES:raise ValueError('Unknown complete profile')
    rng=random.Random(seed);raw=profile.startswith('raw_')
    expected='radio_family' if profile=='raw_25524' else 'blank_coordinate' if raw else None
    if raw and template not in (None,expected):raise ValueError('Raw profile fixes source layout')
    template=template or expected or rng.choice(TEMPLATES) # family/bank before params
    if template not in TEMPLATES:raise ValueError('Unknown template')
    kind='radio' if template=='radio_family' else 'blank'
    if field_type not in (None,kind,':answer-field.type/'+kind):raise ValueError('Field type must match layout')
    p=globals()['parameters'](parameters) if parameters is not None else sample(level,rng,profile)
    m,k=guard(level,p,raw)
    vals,recipes=eligible_bank(p,profile)
    problem=prompt(p,template,raw);worked=None if raw else solution(p)
    values=vals if kind=='radio' else ([] if raw else [aff(m,k,p['variable'])])
    content=digest({'version':VERSION,'prompt':problem,'solution':worked,'values':sorted(values),'kind':kind,'difficulty':None if raw else level,'correct_present':not raw})
    qid=ident(content);fid=ident(qid+':'+kind);key='selection' if kind=='radio' else 'field-1'
    answers=[{':answer/id':ident(fid+':'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind}
    if kind=='radio' or not raw:f[':answer-field/choices']=answers
    q={':question/id':qid,':question/problem':problem,':question/answer-fields':[f]}
    if not raw:
        f[':answer-field/correct']=[':answer/id',answers[0][':answer/id']]
        q[':question/difficulty']=':question.difficulty/'+level;q[':question/worked-solution']=worked
        if kind=='radio':rng.shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'parameter_fingerprint':fingerprint(p),'content_fingerprint':content,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'source':SOURCE,'source_ids':['q-25524' if template=='radio_family' else 'q-208832'],'method_reference':'e-14014; tutorial17592186075062','raw_evidence':raw,'eligible_for_learning':not raw,'authored_extension':not raw,'authored_level':level,'inferred_correct_value':f'({p["variable"]}, '+aff(m,k,p['variable'])+')' if kind=='radio' else aff(m,k,p['variable']),'recipes':recipes if kind=='radio' else [],'domain':'All real free-coordinate values; two nonzero dependent linear equations only','plot_rating':'none','plot_assets':{}}}

# EASY: integral affine family; exactly the same isolation sequence in every task.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: exactly one noninteger divided term; canonical e-14014 workload.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: both noninteger divided terms (reduced denominator3..6); q-208832 workload.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    out=q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f.get(':answer-field/choices',[]))
    if ':question/worked-solution' in q:out+='\n\n'+q[':question/worked-solution']
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile',choices=PROFILES);ap.add_argument('--field-type',choices=('blank','radio'));args=ap.parse_args()
    if args.count<1:ap.error('Positive count required')
    try:records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    except ValueError as exc:ap.error(str(exc))
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
