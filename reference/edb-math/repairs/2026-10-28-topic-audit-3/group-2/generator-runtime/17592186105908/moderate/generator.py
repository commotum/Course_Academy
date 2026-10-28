#!/usr/bin/env python3
"""Seeded coplanarity practice. Offline, relocatable, no database or assets.

Reuses scalar parsing and deterministic field-owned record assembly from the
supplied legacy generator, with the investigated instructional progression.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import sympy as sp
from legacy_parser import parse_math
from generator_policy import nonempty_checkbox
from math_format import normalize_prose, normalize_tex, validate_generated_record, cells, environment

KP={'db_id':17592186105908,'id':'26c84e5b-97a7-5116-a90c-e4f011e87cf0','title':'Determining Whether Three Vectors are Coplanar'}
VERSION='coplanarity-2'
X=sp.Symbol('k')
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source-cases.json').read_text())
PROFILES={
 'signed-cofactors':('flip0','flip1','flip2','reciprocal'),
 'minor-arithmetic':('add0','add1','add2','negate'),
 'mixed-operations':('drop0','add1','add2','omit-division'),
 'mixed-minors':('add0','drop1','add2','reciprocal'),
 'minor-and-omission':('add0','add1','add2','drop0'),
}

def tex(e):return normalize_tex(sp.latex(sp.sympify(e),fold_short_frac=False))
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP['id']),x))
def atom(e):return '('+tex(e)+')'
def determinant(m):return r'\begin{vmatrix}'+r'\\'.join('&'.join(tex(v) for v in row)for row in m.tolist())+r'\end{vmatrix}'
def display(rows):return '$$\n'+r'\begin{aligned}'+'\n'+r'\\'.join(rows)+'\n'+r'\end{aligned}'+'\n$$'

def expansion(m,stage):
    terms=[]
    for j in range(3):
        n=m.minor_submatrix(0,j)
        inside=(determinant(n) if stage=='minors' else
                '('+atom(n[0,0])+r'\cdot '+atom(n[1,1])+'-'+atom(n[0,1])+r'\cdot '+atom(n[1,0])+')' if stage=='products' else
                atom(n.det()))
        terms.append(atom(m[0,j])+r'\cdot '+inside)
    return ['&='+terms[0],r'&\quad -'+terms[1],r'&\quad +'+terms[2]]

def roots_and_form(m,v='k'):
    x=sp.Symbol(v);d=sp.expand(m.det());degree=sp.degree(d,x)
    if degree not in (1,2) or (degree==2 and d.coeff(x,1)!=0):raise ValueError('Outside linear / single-square scope')
    a=d.coeff(x,degree);b=d.subs(x,0);q=sp.cancel(-b/a)
    if degree==1:return d,degree,a,b,q,[tex(q)]
    if q<=0:raise ValueError('Two distinct real roots needed')
    # Preserve the shown square-root operation instead of silently rationalizing.
    root=tex(sp.sqrt(q)) if sp.sqrt(q).is_Rational else r'\sqrt{'+tex(q)+'}'
    return d,degree,a,b,q,['-'+root,root]

def assemble(level,seed,prompt,solution,specs,metadata):
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    normalized=[]
    for key,kind,values,ci,typ,label in specs:
        vals=[normalize_tex(s)if typ=='math' else normalize_prose(s) for s in values]
        normalized.append((key,kind,vals,ci,typ,normalize_prose(label) if label else None))
    identity=digest({'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'fields':normalized})
    fs=[]
    for key,kind,values,ci,typ,label in normalized:
        fid=uid(identity+':field:'+key)
        choices=[{':answer/id':uid(fid+':'+s),':answer/type':':answer.type/'+typ,':answer/value':s}for s in values]
        f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]}
        if label:f[':answer-field/label']=label
        if kind=='radio':random.Random(str(seed)+fid).shuffle(choices)
        fs.append(f)
    r={'knowledge_point':KP,'question':{':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fs},'generation':{'version':VERSION,'seed':seed,'source':SOURCE['source'],**metadata}}
    return validate_generated_record(r)

def solution(m,v='k'):
    d,degree,a,b,q,answers=roots_and_form(m,v);x=sp.Symbol(v)
    rows=[r'\mathbf{a}\cdot(\mathbf{b}\times\mathbf{c})&='+determinant(m)]
    for stage in ('minors','products','values'):rows+=expansion(m,stage)
    rows+=['&='+tex(d)]
    solving=[tex(d)+'&=0',tex(a*x**degree)+'&='+tex(-b),tex(x**degree)+'&='+tex(q)]
    if degree==2:solving+=[v+r'&=\pm '+answers[1]]
    final=' or '.join('$'+v+'='+s+'$' for s in answers)
    closing=('Both signs are necessary because both have square $'+tex(q)+'$. ' if degree==2 else '')
    return ('The vectors are coplanar if and only if their scalar triple product is zero. Expanding along the first row gives\n\n'+display(rows)+'\n\nSet the triple product equal to zero and solve:\n\n'+display(solving)+'\n\n'+closing+'Thus the vectors are coplanar exactly when '+final+'.')

def bank(m,profile):
    d,deg,a,b,q,answers=roots_and_form(m)
    if deg!=1:raise ValueError('Scalar bank requires linear equation')
    ts=[sp.expand((-1)**j*m[0,j]*m.minor_submatrix(0,j).det())for j in range(3)]
    values=[q];recipes=['correct']
    for recipe in PROFILES[profile]:
        if recipe=='reciprocal':value=1/q if q else sp.zoo
        elif recipe=='negate':value=-q
        elif recipe=='omit-division':value=-b
        else:
            j=int(recipe[-1]);n=m.minor_submatrix(0,j)
            if recipe.startswith('flip'):wrong=d-2*ts[j]
            elif recipe.startswith('drop'):wrong=d-ts[j]
            else:wrong=d-ts[j]+(-1)**j*m[0,j]*(n[0,0]*n[1,1]+n[0,1]*n[1,0])
            wrong=sp.expand(wrong)
            value=-wrong.subs(X,0)/wrong.coeff(X) if wrong.coeff(X) else sp.zoo
        value=sp.cancel(value)
        if not value.is_Rational or value in values or abs(value)>100:raise ValueError('Reject entire colliding/inapplicable bank')
        values.append(value);recipes.append(recipe)
    return list(map(tex,values)),recipes

def render_instance(m,level,seed=0,profile='signed-cofactors',source_ids=None):
    d,deg,a,b,q,answers=roots_and_form(m)
    if (level=='hard')!=(deg==2):raise ValueError('Difficulty/operation mismatch')
    vectors=[r'$\mathbf{'+name+r'}=\langle '+','.join(tex(m[i,j]) for j in range(3))+r'\rangle$'for i,name in enumerate('abc')]
    prompt=('Find all real values of $k$ for which the vectors 'if deg==2 else 'Find $k$ given that the vectors ')+vectors[0]+', '+vectors[1]+', and '+vectors[2]+' are coplanar.'
    if level=='easy':
        prompt+='\n\nThe first-row expansion of their scalar triple product is provided:\n\n'+display([r'\mathbf{a}\cdot(\mathbf{b}\times\mathbf{c})'+expansion(m,'products')[0]]+expansion(m,'products')[1:])+'\n\nSelect the value of $k$.'
        values,recipes=bank(m,profile);specs=[('selection','radio',values,0,'math',None)]
    else:
        recipes=[]
        if deg==2:prompt+='\n\n**In ascending order**, enter both exact values.\n\n$k=${{field-1}} and $k=${{field-2}}'
        else:prompt+='\n\n$k=${{field-1}}'
        specs=[('field-'+str(i+1),'blank',[ans],0,'math',None)for i,ans in enumerate(answers)]
    slots=[(i,j)for i in range(3)for j in range(3)if X in m[i,j].free_symbols]
    role='square'if deg==2 else 'single'if len(slots)==1 else 'same-row'if slots[0][0]==slots[1][0] else 'same-column'
    return assemble(level,seed,prompt,solution(m),specs,{'template':role,'profile':profile if level=='easy'else 'exact-entry','parameters':{'vectors':[[str(e)for e in row]for row in m.tolist()]},'source_question_ids':source_ids or (['85dbcbc6-7e0b-5364-ba3b-2e4b14e4021a','fe6d904a-8846-5cf7-a75e-99f480622386']if deg==2 else ['b990ba56-2404-5f20-a869-596a97b7f65e','ee4f8503-0b7f-5200-9b9f-9ac97e166c2a','65ad1da6-49b7-5494-8267-2eea67ec5389']),'recipes':recipes})

def generate(level,seed=0,case=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    # Answer-bearing roles and whole bank profile precede incidental coordinates.
    role=case or ('square'if level=='hard'else rng.choice(('single','same-row','same-column')))
    prof=profile or rng.choice(tuple(PROFILES))
    if (level=='hard')!=(role=='square'):raise ValueError('Wrong role for band')
    eligible=[(i,j) for i in range(3) for j in range(3) if not (level=='easy' and role=='single' and i==0 and 'drop'+str(j) in PROFILES[prof])]
    row,col=rng.choice(eligible)
    second=(row,(col+rng.choice((1,2)))%3)if role=='same-row'else ((row+rng.choice((1,2)))%3,col)
    square_sign=rng.choice((-1,1)) if level=='hard' else 1
    for attempt in range(10000):
        lim=3 if level=='easy'else 4
        m=sp.Matrix(3,3,[rng.randint(-lim,lim)for _ in range(9)])
        m[row,col]=square_sign*X**2 if role=='square'else X
        if role in ('same-row','same-column'):m[second]=X
        try:
            d,degree,a,b,q,answers=roots_and_form(m)
            # Coefficients constrain incidental arithmetic; do not reject cancellation.
            if abs(a)>60 or abs(b)>100:continue
            if level=='hard':
                if q.p>12 or q.q>6:continue
            elif abs(q)>12 or q.q>8:continue
            if level!='hard' and role!='single':
                # Ensure both printed parameter occurrences actually contribute.
                y=sp.Symbol('y');single=m.copy();single[row,col]=y
                if sp.diff(single.det(),y)==0:continue
                single=m.copy();single[second]=y
                if sp.diff(single.det(),y)==0:continue
            if any(all(e.subs(X,sp.sqrt(q)if degree==2 else q)==0 for e in m.row(i))for i in range(3)):continue
            r=render_instance(m,level,seed,prof);r['generation']['attempts']=attempt+1;return r
        except ValueError:continue
    raise RuntimeError(f'Unable to construct {level} {role} {prof} at {row},{col} seed={seed}')


def wrap_source_derivation(prose):
    """Reflow long captured equalities without changing any summand or stage."""
    prose=normalize_prose(prose)
    changes=[]
    for match in re.finditer(r'\\begin\{aligned\}',prose):
        span=environment(prose,match.start())
        if not span:continue
        # Only the outer equation alignment; vmatrix bodies are never reflowed.
        body=prose[span[0]:span[1]]
        rows=cells(body)
        if not rows or not any(len(row)==2 and row[1].lstrip().startswith('=') for row in rows):continue
        out=[]
        for row in rows:
            if len(row)!=2 or not row[1].lstrip().startswith('=') or len(row[1])<55:
                out.append(' & '.join(row));continue
            expr=row[1].lstrip()[1:];parts=[];start=0;i=0;depth=0
            while i<len(expr):
                if expr.startswith(r'\begin{',i):
                    env=environment(expr,i)
                    if env:i=env[2];continue
                if expr[i]=='\\':
                    command=re.match(r'\\[a-zA-Z]+|\\.',expr[i:]);i+=len(command[0])if command else 1;continue
                if expr[i] in '{([':depth+=1
                elif expr[i]in '})]':depth-=1
                elif depth==0 and expr[i]in '+-' and i>start:
                    parts.append(expr[start:i]);start=i
                i+=1
            parts.append(expr[start:]);out.append(row[0]+' &='+parts[0])
            out.extend(r'&\quad '+part for part in parts[1:])
        changes.append((span[0],span[1],r' \\ '.join(out)))
    for start,end,body in reversed(changes):prose=prose[:start]+body+prose[end:]
    return prose

@nonempty_checkbox
def replay_source(identity):
    q=next(q for q in SOURCE['questions']if identity in (q[':question/id'],q.get(':question/math-academy-id')))
    specs=[]
    for f in q[':question/answer-fields']:
        choices=f[':answer-field/choices'];ci=next(i for i,a in enumerate(choices)if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
        if q.get(':question/math-academy-id')=='q-18266':ci=next(i for i,a in enumerate(choices)if a[':answer/value']=='k=-3,k=3')
        ident=lambda x:x[':db/ident']if isinstance(x,dict)else x
        specs.append((f[':answer-field/key'],ident(f[':answer-field/type']).split('/')[-1],[a[':answer/value']for a in choices],ci,ident(choices[0][':answer/type']).split('/')[-1],f.get(':answer-field/label')))
    level=q[':question/difficulty'];level=(level[':db/ident'] if isinstance(level,dict) else level).split('/')[-1]
    worked=wrap_source_derivation(q[':question/worked-solution'])
    if q.get(':question/math-academy-id')=='q-280772':
        worked += '\n\nThe positive square root of a quotient is the quotient of the positive square roots, so $'+r'\sqrt{\frac{1}{10}}=\frac{\sqrt{1}}{\sqrt{10}}=\frac{1}{\sqrt{10}}'+ '$. The negative root has the corresponding minus sign. These are the two equivalent answer forms in the fields.'
    return assemble(level,0,q[':question/problem'],worked,specs,{'template':'source-replay','source_question_ids':[q[':question/id']],'source_key_corrected':q.get(':question/math-academy-id')=='q-18266'})

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all','unclassified'],default='moderate');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');p.add_argument('--replay-source');args=p.parse_args()
    if args.count<1:p.error('count must be positive')
    if args.replay_source:records=[replay_source(args.replay_source)]
    else:
        levels=['easy','moderate','hard']if args.difficulty=='all'else ['moderate'if args.difficulty=='unclassified'else args.difficulty]
        records=[]
        for level in levels:
            seen=set()
            for i in range(args.count):
                for retry in range(1000):
                    record=generate(level,args.seed+i+retry*1000003)
                    # Matrix semantic fingerprint ignores cosmetic identities and options.
                    fingerprint=digest(record['generation']['parameters'])
                    if fingerprint not in seen:break
                else:raise RuntimeError('Batch exhausted semantic instances')
                seen.add(fingerprint);records.append(record)
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
