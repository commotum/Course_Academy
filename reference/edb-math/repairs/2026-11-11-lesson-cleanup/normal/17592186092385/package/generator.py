#!/usr/bin/env python3
"""Relocatable normal-intercept generator, evolved from 17592186092385-draft.
Exact derivative -> perpendicular slope -> point-slope line -> axis intersection.
"""
import argparse
import copy
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as s
import math_format as fmt

VERSION = 'normal-intercepts-7863-1'
KP_ID = 17592186092385
KP_UUID = '3ba61258-92a9-511e-891f-9e6adce2edb0'
X = s.Symbol('x', positive=True)
LEVELS = ('easy', 'moderate', 'hard')
FAMILIES = {'easy': ('quadratic', 'cubic'), 'moderate': ('sqrt', 'cubert', 'sqrtcube', 'fourth', 'reciprocal'), 'hard': ('sqrtlinear',)}
POWERS = {'quadratic': 2, 'cubic': 3, 'sqrt': s.Rational(1,2), 'cubert': s.Rational(2,3), 'sqrtcube': s.Rational(3,2), 'fourth': s.Rational(1,4), 'reciprocal': -1, 'sqrtlinear': s.Rational(1,2)}
PROVENANCE=json.loads(Path(__file__).with_name('source-provenance.json').read_text())
SUPPORT={k:v['source_refs'] for k,v in PROVENANCE['families'].items()}

def tex(e):
    return s.latex(s.sympify(e), order='lex').replace(r'\left', '').replace(r'\right', '')

def digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(text):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), text))

def display(rows):
    return '$$\n' + (r'\begin{aligned}'+'\n'+r' \\'.join(rows)+'\n'+r'\end{aligned}' if len(rows)>1 else rows[0]) + '\n$$'

def expression(family, a, b, c):
    return a*X**POWERS[family] + b*X + c

def curve_tex(family,a,b,c, power=False):
    r=POWERS[family]
    if power or family in ('quadratic','cubic'):
        return s.latex(expression(family,a,b,c), root_notation=False, order='lex')
    atom={'sqrt':r'\sqrt{x}', 'cubert':r'\sqrt[3]{x^{2}}', 'sqrtcube':r'\sqrt{x^{3}}', 'fourth':r'\sqrt[4]{x}', 'reciprocal':r'\frac{1}{x}', 'sqrtlinear':r'\sqrt{x}'}[family]
    lead = ('-' if a == -1 else '' if a == 1 else str(a)) + atom
    if family=='reciprocal': lead=(('-' if a<0 else '')+r'\frac{'+str(abs(a))+r'}{x}')
    if b: lead+=('+' if b>0 else '-')+('' if abs(b)==1 else str(abs(b)))+'x'
    if c: lead+=('+' if c>0 else '')+str(c)
    return lead

def finish(q, meta):
    q=copy.deepcopy(q)
    for name in (':question/problem', ':question/worked-solution'):
        q[name]=fmt.normalize_prose(q[name])
    # Strip database identities and compute owned identities only after normalization.
    q.pop(':db/id',None);q.pop(':question/math-academy-id',None);q.pop(':question/id',None)
    if isinstance(q[':question/difficulty'],dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
    canonical=[]
    for f in q[':question/answer-fields']:
        f.pop(':db/id',None)
        if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
        corr=f[':answer-field/correct'];cid=corr[':answer/id'] if isinstance(corr,dict) else corr[1]
        value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
        for a in f[':answer-field/choices']:
            a.pop(':db/id',None)
            if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
            a[':answer/value']=fmt.normalize_tex(a[':answer/value'])
            if ':answer/feedback' in a:a[':answer/feedback']=fmt.normalize_prose(a[':answer/feedback'])
        canonical.append([f[':answer-field/key'],f[':answer-field/type'],[a[':answer/value'] for a in f[':answer-field/choices']],fmt.normalize_tex(value)])
    identity=digest([VERSION,q[':question/problem'],q[':question/worked-solution'],q[':question/difficulty'],canonical])
    for f,desc in zip(q[':question/answer-fields'],canonical):
        f[':answer-field/id']=uid(identity+':field:'+f[':answer-field/key'])
        for a in f[':answer-field/choices']:
            a[':answer/id']=uid(f[':answer-field/id']+':answer:'+a[':answer/value'])
        correct=next(a for a in f[':answer-field/choices'] if a[':answer/value']==desc[3])
        f[':answer-field/correct']=[':answer/id',correct[':answer/id']]
    q[':question/id']=uid(identity)
    out={'question':q,'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Determining the Intercepts of a Normal Line'},'generation':dict(meta,version=VERSION,content_hash=identity,source_basis=7863)}
    fmt.validate_generated_record(out)
    return out

def generate(level, family, a, b, c, point, axis, seed=0, supplied_point=None):
    if level not in LEVELS or family not in POWERS or axis not in ('x','y'):raise ValueError('Unknown level, family or axis')
    # Explicit instances also permit complete source replay and matched-band comparisons.
    if not all(type(v) is int for v in (a,b,c,point)) or a==0:raise ValueError('Integer parameters required')
    if family not in ('quadratic','cubic') and point<=0:raise ValueError('Positive power/root point required')
    f=expression(family,a,b,c);px=s.Integer(point);yp=s.simplify(f.subs(X,px));d=s.diff(f,X);m=s.simplify(d.subs(X,px))
    if m==0 or not m.is_finite or yp.is_real is not True:raise ValueError('Nonzero finite slope required')
    if (axis=='x' and yp==0) or (axis=='y' and px==0):raise ValueError('Given point already lies on the requested axis')
    n=-1/m; intercept=s.simplify(yp-n*px)
    value=s.simplify(-intercept/n) if axis=='x' else intercept
    xy=(value,s.Integer(0)) if axis=='x' else (s.Integer(0),value)
    supplied=(level!='hard') if supplied_point is None else supplied_point
    curve=curve_tex(family,a,b,c)
    point_text='the point $('+tex(px)+','+tex(yp)+')$' if supplied else 'the point with $x$-coordinate $'+tex(px)+'$'
    problem='Find where the normal line to the curve $y='+curve+'$ at '+point_text+' intersects the $'+axis+'$-axis.\n\nThe intersection is $(${{field-1}}$,$ {{field-2}}$)$. Give exact values.'
    steps=[]
    if not supplied:
        steps.append('First find the point on the curve.\n\n'+display(['f('+tex(px)+')='+curve.replace('x','('+tex(px)+')')+'='+tex(yp)+'.'])+'\n\nThe normal passes through $('+tex(px)+','+tex(yp)+')$.')
    if family in ('quadratic','cubic'):
        rows=["f'(x)="+tex(d)+'.']
        intro='Differentiate the polynomial.'
    else:
        rows=['f(x)&='+curve_tex(family,a,b,c,power=True)+',',"f'(x)&="+s.latex(d,root_notation=False,order='lex')+'='+tex(d)+'.']
        intro='Rewrite the radical or reciprocal using powers, then differentiate.'
    steps.append(intro+'\n\n'+display(rows))
    steps.append('Evaluate the tangent slope and take its negative reciprocal to find the normal slope.\n\n'+display(["m_t=f'("+tex(px)+')&='+tex(d).replace('x','('+tex(px)+')')+'='+tex(m)+',',r'm_n=-\frac{1}{m_t}&=-\frac{1}{('+tex(m)+')}='+tex(n)+'.']))
    steps.append('Use point-slope form through $('+tex(px)+','+tex(yp)+')$.\n\n'+display(['y-('+tex(yp)+')&='+tex(n)+'(x-('+tex(px)+')),','y&='+tex(n*X+intercept)+'.']))
    if axis=='x':
        rows=['0&='+tex(n)+'x+('+tex(intercept)+'),','x&='+tex(value)+'.']
        fixed='y'
    else:
        rows=['y&='+tex(n)+r'\cdot 0+('+tex(intercept)+'),','y&='+tex(value)+'.']
        fixed='x'
    final='('+tex(xy[0])+','+tex(xy[1])+')'
    steps.append('At the $'+axis+'$-axis, $'+fixed+'=0$.\n\n'+display(rows)+'\n\nThe intersection is $'+final+'$.')
    fields=[]
    for i,v in enumerate(xy,1):
        aid='temporary-'+str(i)
        fields.append({':answer-field/key':'field-'+str(i),':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex(v)}],':answer-field/correct':[':answer/id',aid]})
    q={':question/problem':problem,':question/worked-solution':'\n\n'.join(steps),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
    meta={'seed':seed,'template':family,'parameters':{'a':a,'b':b,'c':c,'point':point,'axis':axis},'supplied_point':supplied,'source_references':SUPPORT[family],'source_inference':PROVENANCE['families'][family]['reason'],'domain':'real x' if family in ('quadratic','cubic') else 'x>0','displayed_final':final,'solution_stages':['point' if not supplied else 'supplied point','power rewrite' if family not in ('quadratic','cubic') else 'polynomial derivative','tangent slope','negative reciprocal','point-slope','axis intersection'],'response_contract':'two exact coordinate fragments'}
    return finish(q,meta)

def sample(level,family,axis,rng,seed):
    while True:
        a=rng.choice((-3,-2,-1,1,2,3))
        if level=='hard':
            a=rng.choice((-4,-2,2,4));b=rng.choice((-3,-2,-1,1,2,3));c=rng.randint(-2,2);p=rng.choice((1,4))
        elif level=='easy':
            a=rng.choice((-2,-1,1,2)) if family=='quadratic' else rng.choice((-1,1))
            b=rng.randint(-2,2) if family=='quadratic' else 0;c=rng.randint(-3,3);p=rng.randint(-2,2)
        else:
            b=0;c=rng.randint(-3,3)
            p=rng.choice({'sqrt':(1,4,9),'cubert':(1,8),'sqrtcube':(1,4),'fourth':(1,16),'reciprocal':(1,2)}[family])
        try:return generate(level,family,a,b,c,p,axis,seed)
        except ValueError:continue

def batch(level,count,seed):
    if level not in LEVELS or count<0:raise ValueError('Invalid level/count')
    rng=random.Random(seed);families=list(FAMILIES[level]);rng.shuffle(families)
    first=rng.randrange(2);out=[];seen=set()
    for i in range(count):
        family=families[i%len(families)];axis=('x','y')[(i%len(families)+i//len(families)+first)%2]
        for attempt in range(10000):
            r=sample(level,family,axis,rng,seed)
            p=r['generation']['parameters'];fp=digest([family,p])
            if fp not in seen:seen.add(fp);out.append(r);break
        else:raise ValueError('Requested batch exceeds practical distinct capacity')
    return out

def source_replay():
    data=json.loads(Path(__file__).with_name('source-replay.json').read_text())
    return [finish(q,{'source_references':[q[':question/math-academy-id']], 'template':'source replay','seed':0,'replay':True}) for q in data['questions'] if q[':db/id'] not in PROVENANCE['retired_source_entities']]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'unclassified','all'),default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay-sources',action='store_true');args=ap.parse_args()
    level='moderate' if args.difficulty=='unclassified' else args.difficulty
    if args.count<0:ap.error('Count must be nonnegative')
    rows=source_replay() if args.replay_sources else [r for lev in (LEVELS if level=='all' else (level,)) for r in batch(lev,args.count,args.seed)]
    print(json.dumps(rows,indent=2))

if __name__=='__main__':main()
