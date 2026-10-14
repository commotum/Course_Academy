#!/usr/bin/env python3
"""Tangent periodicity; frozen math basis 1356. No database writes.

Public source_<MA id> profiles are parameterized, evidence-only recipes. They
retain source omissions and complete banks. Their opaque scalars do not claim
recovered author intent. Normal defaults use complete method-derived banks.
Easy: integer given value, one periodicity substitution. Moderate: observed
radical direct / integer additive / integral-product scale or affine templates.
Hard: authored rational affine arithmetic, both operands nonintegral
rationals and nonintegral product. No negative x, angle addition or oddness.
Explicit inputs receive the same workload guards as sampled inputs.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186176050
KP_UUID='eed0c7c3-0bb5-56eb-a9ca-9ec4dc7b3efe'
TITLE='Utilizing the Periodicity Property of the Tangent Function'
VERSION='tangent-periodicity-v1'
DIR=Path(__file__).with_suffix('')
SOURCE=json.loads((DIR/'source.json').read_text())
PROVENANCE={k:SOURCE[k] for k in ('database','basis','lineage')}
V,A,B,N,AN,AD=sp.symbols('v a b n anum aden')
# Whole observed banks, in captured order. Entries are scalar operation/mask pairs.
# Opaque entries are ONLY eligible in explicitly requested evidence profiles.
SPECS={
 'q-29382':dict(level='moderate',template='affine_legacy',p=dict(v='2',a='2',b='-1',n=-4),ops=[V-N*sp.pi,B,-N*sp.pi,A*V+B,A*V-B]),
 'q-66218':dict(level='easy',template='direct_legacy',p=dict(v='4',a='1',b='0',n=7),ops=[1/V,sp.Integer(1),V,-V,-1/V]),
 'q-103307':dict(level='moderate',template='affine',p=dict(v='1/3',a='12',b='-6',n=5),ops=[A*V+B,A*V,-(A*V+B),A*V*sp.pi+A*V+B,-B]),
 'q-103312':dict(level='moderate',template='scale',p=dict(v='16',a='3/4',b='0',n=-9),ops=[V/AD,A*V,A*V+N/AN*sp.pi,A*V+sp.pi,A*V+AN]),
 'q-66594':dict(level='moderate',template='direct',p=dict(v='sqrt(3)',a='1',b='0',n=-5),ops=[V+2*sp.pi,sp.Integer(-1),-V,V,V/2]),
 'q-70998':dict(level='moderate',template='add',p=dict(v='3',a='1',b='2',n=5),ops=[V+B-N*sp.pi,N*sp.pi,B,-V+B,V+B]),
 'q-71002':dict(level='moderate',template='direct',p=dict(v='sqrt(2)',a='1',b='0',n=-11),ops=[-V,-V**2,V**2,V+N*sp.pi,V]),
}
TEMPLATES={'easy':('direct_legacy',),'moderate':('direct','add','scale','affine','affine_legacy'),'hard':('rational_affine',)}

def tex(x): return sp.latex(sp.sympify(x)).replace('- ', '-')
def scalar(x):
    e=sp.sympify(x)
    if e.free_symbols or e.is_real is not True or e.is_finite is not True: raise ValueError('finite real scalar required')
    return e

def shift(n,unicode=False,spaced=False):
    pi='π' if unicode else r'\pi '
    sign='+' if n>0 else '-'
    pad=' ' if spaced else ''
    return 'x'+pad+sign+pad+str(abs(n))+pi

def bterm(b,space=False):
    if b==0:return ''
    sep=' ' if space else ''
    return sep+('+' if b>0 else '-')+sep+tex(abs(b))

def target(p,fn=r'\tan ',unicode=False,spaced=False):
    a,b,n=p['a'],p['b'],p['n']
    head='' if a==1 else (r'\left('+tex(a)+r'\right)' if a<0 else tex(a))
    return head+fn+'('+shift(n,unicode,spaced)+')'+bterm(b,spaced)

def cleanparams(parameters):
    if set(parameters)!=set(('v','a','b','n')): raise ValueError('parameters require exactly v,a,b,n')
    p={k:scalar(parameters[k]) for k in ('v','a','b')}
    n=sp.sympify(parameters['n'])
    if not n.is_Integer or not 1<=abs(n)<=12:raise ValueError('shift is a nonzero integer of magnitude <=12')
    p['n']=int(n)
    if p['v']==0 or abs(p['v'])>16:raise ValueError('nonzero given tangent value of magnitude <=16')
    return p

def check_scope(level,t,p,raw=False):
    v,a,b=p['v'],p['a'],p['b']
    if raw:
        if t.startswith('direct') and (a!=1 or b!=0):raise ValueError('direct template requires a=1,b=0')
        if t=='scale' and b!=0:raise ValueError('scale template requires b=0')
        if t=='add' and a!=1:raise ValueError('add template requires a=1')
        return
    if t not in TEMPLATES[level]:raise ValueError('template is unavailable at difficulty')
    if level=='easy':
        if not v.is_Integer or not 2<=abs(v)<=16 or a!=1 or b!=0:raise ValueError('easy integer direct workload')
    elif level=='moderate':
        if t=='direct':
            if v not in [s*sp.sqrt(k) for s in (-1,1) for k in (2,3,5,6,7)] or a!=1 or b!=0:raise ValueError('moderate direct uses a familiar quadratic radical')
        elif t=='add':
            if not v.is_Integer or not 2<=abs(v)<=9 or a!=1 or not b.is_Integer or not 1<=abs(b)<=6:raise ValueError('moderate additive bounds')
        elif t=='scale':
            if not v.is_Integer or not a.is_Rational or a.is_Integer or not 2<=sp.denom(a)<=4 or not 1<=abs(sp.numer(a))<=3 or not (a*v).is_Integer or a*v==0 or b!=0:raise ValueError('moderate scaling has fractional coefficient and integral product')
        else:
            if not v.is_Rational or not a.is_Integer or not 2<=abs(a)<=12 or not 1<=sp.denom(v)<=4 or abs(sp.numer(v))>8 or not (a*v).is_Integer or abs(a*v)>24 or not b.is_Integer or not 1<=abs(b)<=6:raise ValueError('moderate affine has integer coefficient, integral product and integer offset')
    else:
        if not all(z.is_Rational and not z.is_Integer and 2<=sp.denom(z)<=4 and 1<=abs(sp.numer(z))<=6 for z in (a,v)) or (a*v).is_Integer or not b.is_Integer or not 1<=abs(b)<=5:raise ValueError('hard rational affine workload')

# Source-shaped prose and ordered stages. Source profiles reproduce exact prose,
# token styles and omitted attributes; normal presentation uses standard LaTeX.
def render(p,t,source=None):
    v,a,b,n=p['v'],p['a'],p['b'],p['n']; vv=tex(v); av=tex(a*v); ans=tex(a*v+b)
    legacy=t.endswith('_legacy'); fn=r'\tan ' if legacy else 'tan⁡'
    arg=shift(n,legacy,legacy); expression=target(p,fn,legacy,legacy)
    comma='value of $x$' if legacy else ('value of $x,$' if t in ('affine','scale') else '$x$')
    if legacy:
        prompt=f'If $\\tan x = {vv}$, for some {comma}, find the value of ${expression}$.'
    else:
        prompt=f'If $tan⁡x={vv},$ for some {comma}'+('' if t in ('affine','scale') else ',')+f' find the value of ${expression}.$'
    if legacy: return prompt,None
    anyword='any integer' if t in ('affine','scale','rational_affine') else 'integer'
    into='into the above' if t in ('affine','scale','rational_affine') else 'into the right-hand-side of the above'
    nt=tex(n) if n>0 else '('+tex(n)+')'
    solution=f'The period of $y=tan⁡x$ is $\\pi .$ Therefore, for {anyword} $n{',' if anyword=='any integer' else ''}$ we have\n\n$$\ntan⁡x=tan⁡(x+n\\pi ).\n$$\n\nSubstituting $n={n}$ {into} gives\n\n$$\n\\begin{{aligned}}tan⁡x=tan⁡(x+{nt}\\cdot \\pi )=tan⁡({arg}).\\end{{aligned}}\n$$\n\n'
    if t in ('direct','add'):
        solution+=f'Therefore, if $tan⁡x={vv},$ we get that $tan⁡({arg})={vv}.$'
        if t=='add': solution+=f'\n\nFinally, then\n\n$$\n{expression}=({vv}){bterm(b)}={ans}.\n$$'
    else:
        solution+=f'Since $tan⁡x={vv},$ we get that $tan⁡({arg})={vv}.$ Therefore\n\n$$\n{expression}={tex(a)}({vv}){bterm(b)}'
        if b!=0: solution+='='+av+bterm(b)
        solution+='='+ans+'.\n$$'
    return prompt,solution

def authored_render(p,t):
    # Keep the family's observed stage chain, while standardizing Unicode tan.
    if t in ('direct_legacy','affine_legacy'):
        style='direct' if t=='direct_legacy' else 'affine'
        prompt,solution=render(p,style)
        return prompt.replace('tan⁡',r'\tan '),solution.replace('tan⁡',r'\tan ')
    prompt,solution=render(p,t)
    return prompt.replace('tan⁡',r'\tan '),solution.replace('tan⁡',r'\tan ')

def values(p,t,profile):
    v,a,b,n=p['v'],p['a'],p['b'],p['n']
    if profile.startswith('source_'):
        sid=profile[7:];spec=SPECS[sid]
        subs={V:v,A:a,B:b,N:n,AN:sp.numer(a),AD:sp.denom(a)}
        out=[]
        for e in spec['ops']:
            out.append(sp.simplify(e.subs(subs)))
        return out
    if t.startswith('direct'):
        return [v,1/v,-v,-1/v,v+n*sp.pi]
    if t=='add':return [v+b,v,b,-v+b,v+n*sp.pi+b]
    if t=='scale':return [a*v,v,v/a,-a*v,a*(v+n*sp.pi)]
    return [a*v+b,a*v,a*v-b,a+b*v,a*(v+n*sp.pi)+b]

def source_bank_tex(sid,p,vals):
    v,a,b,n=p['v'],p['a'],p['b'],p['n']; av=a*v
    if sid=='q-29382':return [tex(v)+' + '+str(-n)+'π',tex(b),str(-n)+'π',tex(av+b),tex(av-b)]
    if sid=='q-103307':return [tex(av+b),tex(av),tex(-(av+b)),tex(av)+r'\pi '+bterm(av+b),tex(-b)]
    if sid=='q-103312':return [tex(vals[0]),tex(av),tex(av)+('+' if n>0 else '-')+tex(abs(n/sp.numer(a)))+r'\pi ',tex(av)+r'+\pi ',tex(vals[4])]
    if sid=='q-66594':return [tex(v)+r'+2\pi ', '-1',tex(-v),tex(v),tex(v/2)]
    if sid=='q-70998':return [tex(v+b)+('+' if n<0 else '-')+str(abs(n))+r'\pi ',tex(n)+r'\pi ',tex(b),tex(-v+b),tex(v+b)]
    if sid=='q-71002':return [tex(-v),tex(-v**2),tex(v**2),tex(v)+('+' if n>0 else '-')+str(abs(n))+r'\pi ',tex(v)]
    return [tex(z) for z in vals]

def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def canonical(p):return {k:sp.sstr(z) for k,z in p.items()}
def fingerprint(level,t,p):
    # Shift magnitude is incidental to the same integer-period operation.
    return hashlib.sha256(json.dumps(dict(level=level,information='given_tangent',v=sp.sstr(p['v']),a=sp.sstr(p['a']),b=sp.sstr(p['b'])),sort_keys=True).encode()).hexdigest()

def sample(level,t,rng):
    n=rng.choice([i for i in range(-12,13) if i])
    if level=='easy':return dict(v=rng.choice([i for i in range(-16,17) if abs(i)>=2]),a=1,b=0,n=n)
    if level=='hard':
        rats=sorted(set(sp.Rational(i,j) for i in range(-6,7) if i for j in (2,3,4) if not sp.Rational(i,j).is_Integer),key=float)
        return dict(v=rng.choice(rats),a=rng.choice(rats),b=rng.choice([i for i in range(-5,6) if i]),n=n)
    if t=='direct':return dict(v=rng.choice((-1,1))*sp.sqrt(rng.choice((2,3,5,6,7))),a=1,b=0,n=n)
    if t=='add':return dict(v=rng.choice([i for i in range(-9,10) if abs(i)>=2]),a=1,b=rng.choice([i for i in range(-6,7) if i]),n=n)
    if t=='scale':
        a=rng.choice([sp.Rational(i,j) for i in (-3,-2,-1,1,2,3) for j in (2,3,4) if not sp.Rational(i,j).is_Integer])
        return dict(v=rng.choice((-1,1))*sp.denom(a)*rng.randint(1,4),a=a,b=0,n=n)
    d=rng.choice((1,2,3,4));a=rng.choice((-1,1))*d*rng.randint(2,min(4,12//d));v=sp.Rational(rng.choice((-1,1))*rng.randint(1,8),d)
    return dict(v=v,a=a,b=rng.choice([i for i in range(-6,7) if i]),n=n)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in TEMPLATES:raise ValueError('difficulty easy|moderate|hard required')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio fields supported')
    raw=bool(profile and profile.startswith('source_'))
    if raw:
        sid=profile[7:]
        if sid not in SPECS:raise ValueError('unknown source profile')
        spec=SPECS[sid];t=spec['template']
        if level!=spec['level'] or template not in (None,t):raise ValueError('source replay level/template mismatch')
        parameters=parameters if parameters is not None else spec['p']
    else:
        if profile not in (None,'authored_method'):raise ValueError('unknown bank profile')
        profile='authored_method';rng=random.Random(seed);t=template or rng.choice(TEMPLATES[level])
    rng=random.Random(seed)
    for attempt in range(2000):
        try:
            p=cleanparams(parameters if parameters is not None else sample(level,t,rng));check_scope(level,t,p,raw)
        except ValueError:
            if parameters is not None:raise
            continue
        vs=values(p,t,profile)
        if len(vs)!=5 or any(sp.simplify(x-y)==0 for i,x in enumerate(vs) for y in vs[i+1:]):
            if parameters is not None:raise ValueError('whole bank collision')
            continue
        correct=sp.simplify(p['a']*p['v']+p['b'])
        ci=[i for i,x in enumerate(vs) if sp.simplify(x-correct)==0]
        if len(ci)!=1:raise ValueError('bank lacks unique correct value')
        break
    else:raise ValueError('no eligible complete bank')
    prompt,solution=render(p,t,sid) if raw else authored_render(p,t)
    texts=source_bank_tex(sid,p,vs) if raw else [tex(x) for x in vs]
    original=next(q for q in SOURCE['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==sid) if raw else None
    # Identity uses learner content, key presence and difficulty, never seed/order/profile alias.
    payload=dict(version=VERSION,prompt=prompt,solution=solution,bank=sorted(texts),level=None if raw and ':question/difficulty' not in original else level,correct_present=not raw or ':answer-field/correct' in original[':question/answer-fields'][0])
    identity=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    qid=uid(identity);fid=uid(qid+':selection')
    choices=[{':answer/id':uid(fid+':'+s),':answer/type':':answer.type/math',':answer/value':s} for s in texts]
    correct_id=choices[ci[0]][':answer/id'];rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    if not raw or ':answer-field/correct' in original[':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',correct_id]
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw or ':question/difficulty' in original:question[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:question[':question/worked-solution']=solution
    return dict(knowledge_point=dict(db_id=KP_ID,id=KP_UUID,title=TITLE),question=question,generation=dict(version=VERSION,seed=seed,parameters=canonical(p),template=t,profile=profile,source=PROVENANCE,source_id=sid if raw else None,origin='observed_evidence' if raw else 'authored_extension',evidence_only=raw,eligible_for_learning=not raw,domain='x is any real angle at which tangent is defined; integer shifts preserve that domain',mathematical_fingerprint=fingerprint(level,t,p),content_identity=identity,independently_inferred_correct_value=tex(correct),recipes='complete observed bank; opaque entries retained' if raw else 'complete method-derived bank',runtime=dict(python=sys.version.split()[0],sympy=sp.__version__)))

# EASY — authored completion of the canonical example and unrated direct source.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — observed four mathematical workloads / source rhetorical variants.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored rational affine evaluation, no new trigonometric property.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    lines=[q[':question/problem'],'']+[f'{c}. ${a[":answer/value"]}$' for c,a in zip('ABCDE',f[':answer-field/choices'])]
    lines+=['',q.get(':question/worked-solution','[Worked solution absent in raw source.]')]
    return '\n'.join(lines)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    levels=TEMPLATES if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
