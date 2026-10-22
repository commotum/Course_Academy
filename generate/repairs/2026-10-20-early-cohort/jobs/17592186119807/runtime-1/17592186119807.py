#!/usr/bin/env python3
"""Moderate vector systems with source replay and independent consistency roles.

No database access. See instructional-account.md for the conservative target
residual and choice-bank extensions. New solutions retain each source method.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import re
import sys
import uuid
import sympy as sp
from math_format import checked_math_content, matrix_tex, system_tex, normalize_prose, normalize_tex
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source-data.json').read_text())
KP_ID=17592186119807
KP_UUID=SOURCE['record'][':knowledge-point/id']
GENERATOR_UUID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:generator:'+str(KP_ID)))
VERSION='two-coefficients-2'
SUPPORTED_LEVELS=('moderate',)
CASES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
X=('{x}_{1}','{x}_{2}')
# eliminated variable, equation rows, multipliers, substitution row, check row.
# Direct and immediate-contradiction cases have distinct ordered backbones.
PLANS={
 'q-34054':('direct',1,2,1,0),
 'q-34242':('eliminate',1,1,2,1,-1,2,0),
 'q-34568':('eliminate',0,0,1,3,1,0,2),
 'q-105166':('eliminate',0,0,1,2,1,1,2),
 'q-105167':('eliminate',0,0,1,1,1,1,2),
 'q-73951':('eliminate',1,1,2,1,1,2,0),
 'q-73952':('eliminate',0,0,1,1,1,0,2),
 'q-73954':('eliminate',0,0,1,3,2,1,2),
 'q-73981':('eliminate',1,0,2,1,-1,2,1),
 'q-105163':('eliminate',1,0,1,-2,1,0,2),
 'q-105165':('direct',1,1,0,2),
 'q-105164':('direct',0,1,0,2),
 'q-73957':('eliminate',0,0,1,1,2,1,2),
 'q-73950':('eliminate',1,1,2,1,1,1,0),
}
def scalar(text):
    text=re.sub(r'\s+','',text)
    match=re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}',text)
    return (-1 if match[1] else 1)*sp.Rational(match[2],match[3]) if match else sp.Rational(text)
def vectors(text):
    return [sp.ImmutableMatrix([scalar(v) for v in m[1].split(r'\\')]) for m in MATRIX.finditer(text)]
def tex(v):
    return matrix_tex([[sp.latex(z)] for z in v]) if isinstance(v,sp.MatrixBase) else sp.latex(v)
def domain(sid):return (-2,-1,0,1,2)
def template_id(sid):return '-'.join(map(str,PLANS[sid]))
def fingerprint(q):
    a,c,b=vectors(q[':question/problem'])[:3]
    # Normalize each complete equation, ignoring names, bank, order and seed.
    rows=[]
    for row in zip(a,c,b):
        pivot=next((v for v in row if v),sp.Integer(1))
        rows.append(tuple(str(sp.Rational(v,pivot)) for v in row))
    return hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest()
def term(coef,symbol):
    if coef==0:return ''
    return ('-' if coef==-1 else '' if coef==1 else tex(coef))+symbol
def linear(a,c,symbols=X):
    terms=[term(a,symbols[0]),term(c,symbols[1])]
    return ''.join(('+' if i and t and not t.startswith('-') and terms[0] else '')+t for i,t in enumerate(terms)) or '0'
def display(s):return '$$\n'+s+'\n$$'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def data(sid,t,residual=None):
    a,c,b0=vectors(CASES[sid][':question/problem'])
    plan=PLANS[sid]; rows=(plan[2],plan[3])
    x=sp.ImmutableMatrix([[a[i],c[i]] for i in rows]).inv()*sp.ImmutableMatrix([b0[i] for i in rows])
    x+=sp.ImmutableMatrix([t,2*t])
    b=sp.MutableDenseMatrix(a*x[0]+c*x[1]);check=plan[-1]
    if residual is None:residual=b0[check]-(a[check]*(x[0]-t)+c[check]*(x[1]-2*t))
    b[check]+=residual;lhs=a[check]*x[0]+c[check]*x[1]
    return a,c,sp.ImmutableMatrix(b),x,lhs,lhs==b[check]
def render_solution(sid,a,c,b,x,lhs,consistent):
    old=CASES[sid];plan=PLANS[sid];names=('a','b') if '{a}_{1}' in old[':question/problem'] else ('c','d')
    n,y=names;u='{'+n+'}_{1}';w='{'+n+'}_{2}'
    result='If $'+X[0]+u+'+'+X[1]+w+'='+y+'$, then we have\n\n'
    result+=display(aligned([X[0]+tex(a)+'+'+X[1]+tex(c)+' &='+tex(b),
        matrix_tex([[term(v,X[0]) or '0'] for v in a])+'+'+matrix_tex([[term(v,X[1]) or '0'] for v in c])+' &='+tex(b),
        matrix_tex([[linear(ai,ci)] for ai,ci in zip(a,c)])+' &='+tex(b)]))
    result+='\n\nEquating the corresponding components, we get the following system:\n\n'+display(system_tex([linear(ai,ci)+'='+tex(bi) for ai,ci,bi in zip(a,c,b)]))
    ordinals=('first','second','third')
    if a[0]==c[0]==0 and b[0]!=0:return result+'\n\nThe first equation is a false statement. Hence, the system has no solution.'
    if plan[0]=='direct':
        _,known,row,sub,check=plan
        result+='\n\nFrom the '+ordinals[row]+' equation we get $'+X[known]+'='+tex(x[known])+'$.'
    else:
        _,elim,i,j,m,n,sub,check=plan;known=1-elim
        coef=m*(a[i] if known==0 else c[i])+n*(a[j] if known==0 else c[j]);rhs=m*b[i]+n*b[j]
        if m==n==1:sentence='Adding the '+ordinals[i]+' and the '+ordinals[j]+' equations we get'
        elif n==1:sentence='Multiplying the '+ordinals[i]+' equation by $'+str(m)+'$ and adding the result to the '+ordinals[j]+' equation, we get'
        elif m==1:sentence='Multiplying the '+ordinals[j]+' equation by $'+str(n)+'$ and adding the result to the '+ordinals[i]+' equation, we get'
        else:sentence='Multiplying the '+ordinals[i]+' equation by $'+str(m)+'$, the '+ordinals[j]+' equation by $'+str(n)+'$, and adding the resulting equations, we obtain'
        result+='\n\n'+sentence+'\n\n'
        rows=[term(coef,X[known])+' &='+tex(rhs)]
        if coef!=1:rows.append(X[known]+' &='+tex(x[known]))
        result+=display(aligned(rows))
    unknown=1-known;coefs=(a[sub],c[sub]);remainder=b[sub]-coefs[known]*x[known]
    symbols=list(X);symbols[known]='('+tex(x[known])+')'
    result+='\n\nSubstituting $'+X[known]+'='+tex(x[known])+'$ into the '+ordinals[sub]+' equation, we get\n\n'
    result+=display(aligned([linear(a[sub],c[sub])+' &='+tex(b[sub]),linear(a[sub],c[sub],symbols)+' &='+tex(b[sub]),term(coefs[unknown],X[unknown])+' &='+tex(remainder),X[unknown]+' &='+tex(x[unknown])]))
    result+='\n\nFinally, we substitute $'+X[0]+'='+tex(x[0])+'$ and $'+X[1]+'='+tex(x[1])+'$ into the '+ordinals[check]+' equation to get\n\n'
    result+=display(aligned([linear(a[check],c[check])+' &='+tex(b[check]),linear(a[check],c[check],['('+tex(z)+')' for z in x])+' &='+tex(b[check]),tex(lhs)+' &='+tex(b[check])]))
    result+='\n\nwhich gives a '+('true' if consistent else 'false')+' statement.'
    if not consistent:return result+'\n\nSo, the system has no solution.'
    result+='\n\nSo the solution of the system is $'+X[0]+'='+tex(x[0])+'$ and $'+X[1]+'='+tex(x[1])+'$, which means\n\n'+display(linear(x[0],x[1],(u,w))+'='+y+'.')
    return result+'\n\nConsequently,\n\n'+display(X[0]+'+'+X[1]+'=('+tex(x[0])+')+('+tex(x[1])+')='+tex(sum(x))+'.')
@checked_math_content
def generate(level,seed=0,profile=None,parameters=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
    rng=random.Random(seed);sid=profile or rng.choice(sorted(CASES))
    if sid not in CASES:raise ValueError('Unknown profile')
    replay=parameters=={'translation':0}
    if parameters is not None and set(parameters) not in ({'translation'},{'translation','residual','rank','gaps'}):
        raise ValueError('Expected translation or translation/residual/rank/gaps')
    # Select answer-bearing branch and bank rank before incidental values/order.
    residual=rng.choice((-1,0,1));rank=rng.randint(1,4)
    t=rng.choice(domain(sid))
    gaps=[rng.randint(1,5) for _ in range(3)]
    if parameters is not None:
        t=parameters['translation']
        if 'residual' in parameters:
            residual=parameters['residual'];rank=parameters['rank'];gaps=parameters['gaps']
    if type(t) is not int or t not in domain(sid):raise ValueError('Translation outside bounded domain')
    if type(rank) is not int or rank not in range(1,5):raise ValueError('Rank outside 1..4')
    if type(gaps) is not list or len(gaps)!=3 or any(type(z) is not int or not 1<=z<=5 for z in gaps):raise ValueError('Three positive gaps 1..5 required')
    try:
        if isinstance(residual,bool):raise ValueError('Boolean residual')
        residual=sp.Rational(residual)
        if abs(residual)>20 or residual.q>2:raise ValueError('Residual outside small integer/half-integer domain')
    except (TypeError,ValueError,ZeroDivisionError) as e:raise ValueError('Invalid residual') from e
    old=CASES[sid];a,c,b,x,lhs,consistent=data(sid,t,None if replay else residual)
    correct=tex(sum(x)) if consistent else 'No solution'
    problem=old[':question/problem'];ms=list(MATRIX.finditer(problem));m=ms[2];problem=problem[:m.start()]+tex(b)+problem[m.end():]
    if replay:
        solution=old[':question/worked-solution']
        if sid=='q-105163':
            solution=solution.replace(r'-\frac{33}{2} & =-8',r'-\frac{39}{2} & =-11')
        bank=[(str(o[':answer/type'][':db/ident']),o[':answer/value']) for o in old[':question/answer-fields'][0][':answer-field/choices']]
        params={'translation':0};policy='exact complete source bank; documented arithmetic correction in q-105163'
    else:
        solution=render_solution(sid,a,c,b,x,lhs,consistent)
        offsets=[0]
        for gap in gaps:offsets.append(offsets[-1]+gap)
        values=[sum(x)+z-offsets[rank-1] for z in offsets]
        bank=[(':answer.type/math',tex(z)) for z in values]+[(':answer.type/text','No solution')]
        params={'translation':t,'residual':str(b[PLANS[sid][-1]]-lhs),'rank':rank,'gaps':gaps}
        policy='authored extension: four numeric candidates with independent gaps and rank, plus No solution in both branches'
    problem=normalize_prose(problem);solution=normalize_prose(solution)
    content=hashlib.sha256(json.dumps([VERSION,problem,solution,sorted(bank)]).encode()).hexdigest()
    uid=lambda key:str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP_ID)+':'+content+':'+key))
    choices=[{':answer/id':uid('selection:'+kind+':'+value),':answer/type':kind,':answer/value':normalize_tex(value) if kind==':answer.type/math' else value} for kind,value in bank]
    cid=next(o[':answer/id'] for o in choices if o[':answer/value']==correct);random.Random(str(seed)+':choices').shuffle(choices)
    field={':answer-field/id':uid('selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]}
    q={':question/id':uid('question'),':question/difficulty':':question.difficulty/moderate',':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template_id(sid),'bank_profile':sid,'source_id':sid,'parameters':params,'mathematical_fingerprint':fingerprint(q),'content_fingerprint':content,'correct_value':correct,'candidate_coefficients':list(map(str,x)),'consistent':bool(consistent),'assets':[],'source':{'basis':SOURCE['basis'],'lineage':SOURCE['lineage']},'dependencies':{'sympy':sp.__version__},'domain':'integer translation -2..2; residual abs<=20, denominator 1 or 2; numeric rank 1..4; three gaps 1..5','bank_policy':policy}}
def catalog():
    # Small decision-coverage catalog; option banks are not counted as new systems.
    records=[]
    for sid in sorted(CASES):
        records.append(generate('moderate',0,sid,{'translation':0}))
        for residual in (0,1):
            for rank in range(1,5):
                records.append(generate('moderate',rank,sid,{'translation':0,'residual':residual,'rank':rank,'gaps':[1,2,3]}))
    return records
def batch(level,count,seed=0):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
    if type(count) is not int or not 0<=count<=10000:raise ValueError('Count outside 0..10000')
    rng=random.Random(seed);records=[];seen=set()
    for _ in range(max(100,count*30)):
        if len(records)==count:return records
        rec=generate(level,rng.randrange(2**63))
        fp=rec['generation']['mathematical_fingerprint']
        if fp not in seen:seen.add(fp);records.append(rec)
    raise ValueError('Requested count exceeds available semantic systems')
def markdown(rec):
    q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join(o[':answer/value'] for o in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='moderate');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');args=p.parse_args()
    records=batch(args.difficulty,args.count,args.seed);print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,records)))
