#!/usr/bin/env python3
"""Seeded polar-information practice; standard output is a JSON record array."""
import argparse
import copy
import hashlib
import json
import random
from pathlib import Path
import sympy as s
from legacy import tex, parse, pair, uid
from math_format import normalize_prose, normalize_tex, validate_generated_record

HERE = Path(__file__).resolve().parent
VERSION = 'polar-transfer-3'
KP = {'db_id':17592186092219,'id':'ad049d53-af38-5917-b9d0-be965cadabcb','title':'Finding the Cartesian Coordinates of a Point Given Some Information About Another Point'}
AXES = tuple(map(s.Rational, ['0','1/2','1','3/2']))
RAYS = tuple(map(s.Rational, ['0','1/6','1/4','1/3','1/2','2/3','3/4','5/6','1','7/6','5/4','4/3','3/2','5/3','7/4','11/6']))
NONAXIS = tuple(a for a in RAYS if a not in AXES)
FAMILIES = {'easy':('axis_radius',),'moderate':('scale','square','axis_offset'),'hard':('angle',)}

def aligned(rows):
    return '$$\n'+r'\begin{aligned}'+'\n'+(' \\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'

def cart(radius, ray):
    return tuple(s.simplify(radius*f(ray*s.pi)) for f in (s.cos,s.sin))

def seal(problem, solution, level, fields, meta):
    problem, solution = map(normalize_prose,(problem,solution))
    values = [[normalize_tex(v) for v in values] for _,_,values,_ in fields]
    ident = hashlib.sha256(json.dumps([VERSION,level,problem,solution,values],sort_keys=True).encode()).hexdigest()
    q={':question/id':uid(ident), ':question/problem':problem, ':question/worked-solution':solution, ':question/difficulty':':question.difficulty/'+level, ':question/answer-fields':[]}
    for i,((key,kind,_,ci),vals) in enumerate(zip(fields,values)):
        fid=uid(ident+key)
        answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
        q[':question/answer-fields'].append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]})
    return validate_generated_record({'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,**meta}})

def instance(level, family, a, b, r, operand, *, delta=None):
    """One ordered learner derivation is shared by prompt, key and solution."""
    a,b,r,operand=map(s.sympify,(a,b,r,operand))
    angle=family in ('angle','axis_offset')
    if angle:
        delta=s.sympify(delta if delta is not None else b-a)
        assert s.simplify(s.Mod(a+delta-b,2))==0 and delta != 0
        R=operand
    else:
        R=r*r if family=='square' else r*operand
    assert r>0 and R>0
    A=cart(r,a);B=cart(R,b)
    polarA='('+ (tex(r)+r',\theta' if angle else 'r,'+tex(a*s.pi))+')'
    relation=(r'\theta'+('+' if delta>0 else '-')+tex(abs(delta)*s.pi)) if angle else tex(b*s.pi)
    radial=tex(R) if angle else r'r^{2}' if family=='square' else ('r' if operand==1 else tex(operand)+'r' if operand.is_Integer else r'\frac{r}{'+tex(1/operand)+'}')
    problem=f'The point $A$ has polar coordinates ${polarA}$ and Cartesian coordinates ${pair(A)}$. '
    if not angle:problem+='The radius $r$ is positive. '
    problem+=f'The point $B$ has polar coordinates $({radial},{relation})$. Determine the Cartesian coordinates of $B$.'
    if level=='easy':problem+='\n\nUse $x=R\\cos\\phi$ and $y=R\\sin\\phi$ for polar coordinates $(R,\\phi)$.'
    problem+='\n\nThe Cartesian coordinates of $B$ are $(${{field-1}}$,$ {{field-2}}$)$.'
    if not angle:
        if family=='axis_radius':
            first='The point $A$ lies on a coordinate axis. Its positive distance from the origin is $r='+tex(r)+'$.'
        else:
            first='First, recover the positive radius of $A$:\n\n'+aligned([r'r&=\sqrt{x_A^2+y_A^2}',r'&=\sqrt{('+tex(A[0])+r')^2+('+tex(A[1])+r')^2}',r'&=\sqrt{'+tex(s.simplify(sum(t*t for t in A)))+'}='+tex(r)])
        calculation='('+tex(r)+')^2' if family=='square' else tex(operand)+r'\cdot('+tex(r)+')'
        first+='\n\nApply the radial relationship:\n\n'+aligned([r'R_B&='+calculation+'='+tex(R)])
    elif a in AXES:
        names={s.Rational(0):'positive $x$-axis',s.Rational(1,2):'positive $y$-axis',s.Rational(1):'negative $x$-axis',s.Rational(3,2):'negative $y$-axis'}
        first='The point $A$ lies on the '+names[a]+', so we may take $\\theta='+tex(a*s.pi)+'$.'
    else:
        ref=s.atan(abs(A[1]/A[0]))
        quadrant=1 if A[0]>0 and A[1]>0 else 2 if A[0]<0 and A[1]>0 else 3 if A[0]<0 else 4
        correction={1:r'\alpha',2:r'\pi-\alpha',3:r'\pi+\alpha',4:r'2\pi-\alpha'}[quadrant]
        first='First, find the nonnegative reference angle of $A$:\n\n'+aligned([r'\alpha&=\arctan\left(\left|\frac{y_A}{x_A}\right|\right)',r'&=\arctan\left('+tex(abs(A[1]/A[0]))+r'\right)='+tex(ref)])
        first+='\n\nThe signs of the Cartesian coordinates place $A$ in quadrant '+str(quadrant)+'. Thus\n\n'+aligned([r'\theta&='+correction+'='+tex(a*s.pi)])
    if angle:
        raw=a+delta
        first+='\n\nApply the signed angular offset:\n\n'+aligned([r'\phi_B&='+tex(a*s.pi)+('+' if delta>0 else '-')+tex(abs(delta)*s.pi)+'='+tex(raw*s.pi)])
        if raw!=b:
            first+='\n\nSubtract or add a multiple of $2\\pi$ to use the coterminal angle $\\phi_B='+tex(b*s.pi)+'$.'
    first+='\n\nConsequently, the polar coordinates of $B$ are $('+tex(R)+','+tex(b*s.pi)+')$. Convert each component:\n\n'
    rows=[]
    for name,func,value in zip(('x_B','y_B'),('cos','sin'),B):
        trig=(s.cos if func=='cos' else s.sin)(b*s.pi)
        rows.append(name+'&='+tex(R)+'\\'+func+r'\left('+tex(b*s.pi)+r'\right)='+tex(R)+r'\left('+tex(trig)+r'\right)='+tex(value))
    solution=first+aligned(rows)+'\n\nTherefore, the Cartesian coordinates of $B$ are $'+pair(B)+'$.'
    p={'a':str(a),'b':str(b),'r':str(r),'operand':str(operand),'delta':str(delta) if angle else None}
    fields=[('field-1','blank',[tex(B[0])],0),('field-2','blank',[tex(B[1])],0)]
    return seal(problem,solution,level,fields,{'template':family,'parameters':p,'difficulty_claim':'authored progression grounded in imported moderate/hard cases','source_support':['60b828e5-8a1d-5f25-a3d7-f526a8ab5604' if not angle else '88ed896e-de35-51be-8b01-2f69db5ceea4']})

def draw(rng,level,family):
    # Answer-bearing method and rays chosen before incidental radius sizes.
    a=rng.choice(AXES if family in ('axis_radius','axis_offset') else NONAXIS)
    b=rng.choice(NONAXIS if level=='easy' else RAYS)
    if family in ('angle','axis_offset'):
        while b==a:b=rng.choice(RAYS)
        delta=b-a
        # Both signed representatives, including wrapping around the origin ray.
        if rng.randrange(2):delta += -2 if delta>0 else 2
        r=rng.choice((s.Integer(2),s.Integer(4),s.sqrt(2),s.Integer(6)))
        return instance(level,family,a,b,r,rng.choice((2,3,4,6)),delta=delta)
    r=rng.choice((s.Integer(2),s.Integer(4),s.Integer(6)) if level=='easy' else (s.Integer(2),s.Integer(4),s.Integer(6),2*s.sqrt(2),2*s.sqrt(3)))
    op=rng.choice((2,3)) if level=='easy' else rng.choice((s.Integer(2),s.Integer(3),s.Rational(1,2),s.Rational(1,3)))
    return instance(level,family,a,b,r,op)

def essential(record):
    m=record['generation'];p=m['parameters'];f=m['template']
    if f in ('angle','axis_offset'):return (f,p['a'],p['b'])
    return (f,p['r'],p['operand'] if f!='square' else 'square',p['b'])

def batch(level,count,seed):
    if level=='unclassified':level='moderate'
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);out=[];seen=set();deck=[]
    for i in range(count):
        if not deck:deck=list(FAMILIES[level]);rng.shuffle(deck)
        f=deck.pop()
        for attempt in range(10000):
            rec=draw(rng,level,f);key=essential(rec)
            if key not in seen:break
        else:raise ValueError('Requested count exceeds the supported distinct calculation pool')
        seen.add(key);rec['generation']['seed']=seed;rec['generation']['batch_index']=i;out.append(rec)
    return out

def replay(name):
    """Original complete bank and response shape, normalized before fresh IDs."""
    originals=json.loads((HERE/'source-cases.json').read_text())
    q=next(q for q in originals if q[':question/math-academy-id']==name or q[':question/id']==name)
    fields=[]
    for f in q[':question/answer-fields']:
        vals=[a[':answer/value'] for a in f[':answer-field/choices']]
        ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
        fields.append((f[':answer-field/key'],f[':answer-field/type'][':db/ident'].split('/')[-1],vals,ci))
    sol=q[':question/worked-solution']
    if name=='q-276838':sol=sol.replace('lies in the first quadrant','lies on the positive $x$-axis')
    # The old quadrant-IV source calls a negative arctangent a reference angle.
    # Keep the observed calculation but call it the principal arctangent.
    if name=='q-120504':sol=sol.replace('its reference angle','its principal arctangent')
    return seal(q[':question/problem'],sol,q[':question/difficulty'][':db/ident'].split('/')[-1],fields,{'template':'source_replay','source_question_id':q[':question/id'],'source_math_academy_id':q[':question/math-academy-id'],'replay_only':True})

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');p.add_argument('--source-case');a=p.parse_args()
    print(json.dumps([replay(a.source_case)] if a.source_case else batch(a.difficulty,a.count,a.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
