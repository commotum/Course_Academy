#!/usr/bin/env python3
"""Eliminate the FIRST variable by multiplying exactly ONE equation, then adding.
Two source-shaped select fields. Raw public profiles preserve missing attributes,
full banks and malformed source system braces as evidence only. Completed output
is authored, using the canonical four-stage calculation (never solving a system).
Difficulty bounds are authored design claims; originals are unrated.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186192654
KP_UUID='93dcc73c-ce2d-5fa3-b32b-9fc600fb269e'
TITLE='Eliminating the First Variable'
VERSION='one-transformation-first-v1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
ANCHORS={
'q-210858':dict(a1=1,b1=-1,c1=1,a2=-7,b2=5,c2=9,variables='xy'),
'q-210859':dict(a1=3,b1=4,c1=8,a2=1,b2=5,c2=10,variables='st')}
NS=uuid.UUID(KP_UUID)
def uid(x): return str(uuid.uuid5(NS,str(x)))
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def term(n,v,source=False):
    n=sp.Rational(n)
    if n==0:return '0'
    sign=('- ' if source else '-') if n<0 else ''
    return sign+('' if abs(n)==1 else sp.latex(abs(n)))+v

def lhs(a,b,x,y,source=False):
    return term(a,x,source)+(' + ' if b>0 else ' - ')+term(abs(b),y,source)
def eq(a,b,c,x,y,source=False):return lhs(a,b,x,y,source)+' = '+sp.latex(sp.Rational(c))
def parameters_check(p,level,raw=False):
    if set(p)!=set(ANCHORS['q-210858']):raise ValueError('Exactly a1,b1,c1,a2,b2,c2,variables required')
    if p['variables'] not in ('xy','st','ab','uv'):raise ValueError('Unsupported variable pair')
    if any(type(p[k]) is not int for k in p if k!='variables'):raise ValueError('Integer coefficients required')
    if any(p[k]==0 for k in ('a1','a2','b1','b2')):raise ValueError('Nonzero coefficients required')
    if p['a1']*p['b2']==p['a2']*p['b1']:raise ValueError('A unique, nondegenerate system is required')
    if raw:return
    lo,hi=(2,7) if level=='easy' else ((2,4) if level=='moderate' else (5,7))
    small=min(abs(p['a1']),abs(p['a2']));big=max(abs(p['a1']),abs(p['a2']))
    if (level=='easy' and small!=1) or (level!='easy' and not 2<=small<=4):raise ValueError('Level-specific smaller coefficient bound')
    if big%small or not lo<=big//small<=hi:raise ValueError('Level-specific integer ratio bound')
    if any(not 1<=abs(p[k])<=10 for k in ('b1','b2')) or any(abs(p[k])>12 for k in ('c1','c2')):raise ValueError('Remaining coefficient/constant bound')

def operation(p):
    # The smaller first-variable coefficient gets the one multiplication.
    row=0 if abs(p['a1'])<abs(p['a2']) else 1
    a=[p['a1'],p['a2']]; m=-sp.Rational(a[1-row],a[row])
    return row,m

def eligible(p,values):
    if len(set(values))!=4:raise ValueError('Whole bank has duplicate values')
    valid=[(row,v) for row in (0,1) for v in values if v*p[f'a{row+1}']+p[f'a{2-row}']==0]
    if len(valid)!=1:raise ValueError('Whole bank lacks a unique elimination combination')
    return valid[0]

def sample(level,rng):
    ratio=rng.randint(*( (2,7) if level=='easy' else ((2,4) if level=='moderate' else (5,7))))
    small=1 if level=='easy' else rng.randint(2,4)
    aa=[small,small*ratio]; rng.shuffle(aa)
    return dict(a1=aa[0]*rng.choice((-1,1)),a2=aa[1]*rng.choice((-1,1)),b1=rng.choice([-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10]),b2=rng.choice([-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10]),c1=rng.randint(-12,12),c2=rng.randint(-12,12),variables=rng.choice(('xy','st','ab','uv')))

def prompt(p,raw=False):
    x,y=p['variables']; equations=[eq(p[f'a{i}'],p[f'b{i}'],p[f'c{i}'],x,y,raw) for i in (1,2)]
    system=('$'+'{'+ '; '.join(equations)+'$') if raw else ('$\\{'+ '; '.join(equations)+'$')
    return 'Consider the following system of equations.\n'+system+'\nDescribe the steps needed to eliminate the variable $'+x+'$ from the system:\n\nTo eliminate $'+x+'$, multiply the\n{{field-1}}\nequation by\n{{field-2}},\nand add the equations.'

def solution(p,row,m):
    x,y=p['variables'];a=[p['a1'],p['a2']];b=[p['b1'],p['b2']];c=[p['c1'],p['c2']]
    names=['first','second'];ab=a.copy();bb=b.copy();cc=c.copy();ab[row]*=m;bb[row]*=m;cc[row]*=m
    equations=[eq(a[i],b[i],c[i],x,y) for i in (0,1)]
    equations[row]='('+equations[row]+r')\cdot ('+str(m)+')'
    # Keep the canonical's distributed equation rows, grouped addition, collection.
    grouped='('+term(bb[0],y)+(' + ' if bb[1]>=0 else ' - ')+term(abs(bb[1]),y)+')'
    rhs='('+str(cc[0])+(' + ' if cc[1]>=0 else ' - ')+str(abs(cc[1]))+')'
    rows=[lhs(ab[i],bb[i],x,y)+' &= '+str(cc[i]) for i in (0,1)]
    rows += [grouped+' &= '+rhs,term(bb[0]+bb[1],y)+' &= '+str(cc[0]+cc[1])]
    return (f'Notice that the coefficient of ${x}$ in the first equation is ${a[0]}$, while in the second equation it is ${a[1]}$.\n\n'
        f'If we multiply the {names[row]} equation by ${{\\color{{blue}}{m}}}$, then the coefficient of ${x}$ will turn into ${ab[row]}$, which will cancel with the coefficient of ${a[1-row]}$ in the {names[1-row]} equation.\n\n'
        '$$\n\\{'+ '; '.join(equations)+'\n$$\n\n'+f'Now, when we add the two equations, the variable ${x}$ will be eliminated:\n\n'
        '$$\n\\begin{aligned}\n'+ ' \\\\\n'.join(rows)+'\n\\end{aligned}\n$$\n\nTherefore, the correct answer is the following:\n\n'
        f'> *To eliminate ${x}$, multiply the $\\bbox[3pt,Gainsboro]{{\\color{{blue}}\\text{{{names[row]}}}}}$ equation by $\\bbox[3pt,Gainsboro]{{\\color{{blue}}{m}}}$, and add the equations*.')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Invalid level')
    if template not in (None,'one_transformation'):raise ValueError('Unknown template')
    if field_type not in (None,'select'):raise ValueError('Only two source select fields')
    profile=profile or 'authored-coefficient-confusion'
    raw=profile.startswith('raw-');source_id=profile.removeprefix('raw-') if raw else None
    if raw and source_id not in ORIGINALS:raise ValueError('Unknown raw profile')
    if not raw and profile!='authored-coefficient-confusion':raise ValueError('Unknown bank')
    rng=random.Random(seed)
    for attempt in range(1000):
        p=copy.deepcopy(parameters if parameters is not None else (ANCHORS[source_id] if raw else sample(level,rng)))
        try:
            parameters_check(p,level,raw);row,m=operation(p)
            other=1-row
            if raw:
                # Observed complete banks ±coefficient of first/second variable
                # in the nonunit row. Intent beyond these algebraic recipes unknown.
                k=p['a2'] if source_id=='q-210858' else p['a1']
                n=p['b2'] if source_id=='q-210858' else p['b1']
                values=[sp.Rational(n),-sp.Rational(k),sp.Rational(k),-sp.Rational(n)]
            else:
                n=sp.Rational(p[f'b{other+1}']);values=[m,-m,n,-n]
                eligible(p,values)
            break
        except ValueError:
            if parameters is not None or raw:raise
    else:raise ValueError('No eligible complete bank')
    q={':question/problem':prompt(p,raw)}
    if raw:
        original=ORIGINALS[source_id]
        q={k:copy.deepcopy(v) for k,v in original.items() if k!=':question/problem'}
        q[':question/problem']=prompt(p,True)
        scalars=next(f for f in q[':question/answer-fields'] if f[':answer-field/key']=='field-2')
        for answer,value in zip(scalars[':answer-field/choices'],values):answer[':answer/value']=str(value)
        # Local review records use enum idents rather than Pull enum entities.
        # The unchanged capture remains the authoritative full source object.
        for f in q[':question/answer-fields']:
            f[':answer-field/type']=f[':answer-field/type'][':db/ident']
            for answer in f[':answer-field/choices']:
                answer[':answer/type']=answer[':answer/type'][':db/ident']
    else:
        q[':question/difficulty']=':question.difficulty/'+level
        q[':question/worked-solution']=solution(p,row,m)
        q[':question/answer-fields']=[]
        for key,bank,correct,kind in [('field-1',['first','second'],['first','second'][row],'text'),('field-2',[str(v) for v in values],str(m),'math')]:
            field={':answer-field/key':key,':answer-field/type':':answer-field.type/select',':answer-field/choices':[ {':answer/type':':answer.type/'+kind,':answer/value':v} for v in bank]}
            field['_correct_value']=correct;q[':question/answer-fields'].append(field)
    # Full printed content plus level determines identity; order and seed do not.
    clean=copy.deepcopy(q)
    for f in clean[':question/answer-fields']:
        f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda z:z[':answer/value'])
    content=digest([VERSION,level if not raw else None,clean])
    if not raw or p!=ANCHORS[source_id]:
        q[':question/id']=uid(content)
        for f in q[':question/answer-fields']:
            f[':answer-field/id']=uid(content+f[':answer-field/key'])
            for a in f[':answer-field/choices']:a[':answer/id']=uid(content+f[':answer-field/key']+a[':answer/value'])
    if not raw:
        for f in q[':question/answer-fields']:
            correct=f.pop('_correct_value')
            f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==correct)]
            rng.shuffle(f[':answer-field/choices'])
    # b,c and variable names do not affect the assessed coefficient-ratio choice.
    # Keep absolute coefficient scale: the printed division is the calculation.
    # A global sign reversal leaves the requested operation unchanged.
    task=digest([abs(p['a1']),p['a2']*(1 if p['a1']>0 else -1)])
    return dict(knowledge_point=dict(db_id=KP_ID,id=KP_UUID,title=TITLE),question=q,generation=dict(version=VERSION,seed=seed,template='one_transformation',profile=profile,parameters=p,source={k:v for k,v in SOURCE.items() if k!='record'},mathematical_fingerprint=task,content_identity=content,evidence_only=raw,eligible_for_learning=not raw,authored_completion=not raw,difficulty_claim='authored; source originals unrated',python=sys.version.split()[0],sympy=sp.__version__))

# Easy: one unit first-variable coefficient; one signed integer multiplier 2–7.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: smaller nonunit coefficient 2–4; integer coefficient ratio 2–4.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: smaller nonunit coefficient 2–4; integer coefficient ratio 5–7.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
    q=r['question'];out=q[':question/problem']
    for f in q.get(':question/answer-fields',[]):
        out+='\n\n'+f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices'])
    return out+'\n\n'+q.get(':question/worked-solution','[Original omits worked solution and correct designations.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
