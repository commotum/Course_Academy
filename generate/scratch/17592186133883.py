#!/usr/bin/env python3
"""Source-bounded hard Green's theorem generator; never writes to EDB.

q-41475 backbone: vector field -> differential form -> partials -> type-I
triangle -> double integral -> inner antiderivative -> cubic antiderivative.
The xy coefficient varies. Geometry is a deliberately narrower sampling policy,
not a claim that the observed vertices are essential to this method.
"""
import argparse
import json
import os
from pathlib import Path
import random
import sys
import uuid
try:
    import sympy as sp
except ModuleNotFoundError:
    interpreter = Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__ == '__main__' and interpreter.exists() and Path(sys.executable).resolve() != interpreter.resolve():
        os.execv(str(interpreter), [str(interpreter), str(Path(__file__).resolve()), *sys.argv[1:]])
    raise

KP_ID = 17592186133883
KP_UUID = '11d3f9e1-dad0-51d4-86a9-e0c49465cc3c'
TITLE = "Evaluating Line Integrals Using Green's Theorem"
VERSION = 'greens-evaluate-triangle-v1'
DOMAIN = list(range(1, 13))
IMAGE = 'images/00/007634ca34871f05cde9d44a58fcf24b1e5fd3b8c337c68f2025fb8724eef819.png'
x, y = sp.symbols('x y', real=True)
THEOREM = ("Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, "
    "and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial "
    "derivatives on an open region containing $D$, then Green's theorem states that\n\n"
    "$$\n"+r'\oint_C P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA.'+'\n$$')

def tex(value):
    return sp.latex(sp.sympify(value))

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), VERSION+':'+value))

def mathematics(a):
    if type(a) is not int or a not in DOMAIN:
        raise ValueError('Expected integer 1<=a<=12')
    P, Q = 6*x**2-a*x*y+11, y**2+1
    py, qx = sp.diff(P,y), sp.diff(Q,x)
    curl = sp.expand(qx-py)
    inner = sp.integrate(curl,(y,-x/2,x/2))
    answer = sp.integrate(inner,(x,0,2))
    # Complete observed bank. Ratios retain the observed mathematical patterns;
    # cognitive interpretations of these errors are unresolved, not invented.
    bank = [-answer/4, answer, -answer, -answer/2, answer/2]
    return P,Q,py,qx,curl,inner,answer,bank

def generate(difficulty='hard', seed=0, parameters=None, **kwargs):
    if difficulty != 'hard':
        raise ValueError('Unsupported difficulty: only hard has source evidence')
    if kwargs.get('template','triangle-linear-curl') != 'triangle-linear-curl':
        raise ValueError('Unsupported template')
    if parameters is None:
        a = random.Random(seed).choice(DOMAIN)
    else:
        if set(parameters) != {'a'}:
            raise ValueError('Expected a parameter')
        a = parameters['a']
    P,Q,py,qx,curl,inner,answer,bank = mathematics(a)
    key = str(a)
    qid, fid = uid('q:'+key), uid('q:'+key+':selection')
    choices = [{':answer/id':uid(fid+':'+sp.srepr(value)), ':answer/type':':answer.type/math',
                ':answer/value':tex(value)} for value in bank]
    field = {':answer-field/id':fid, ':answer-field/key':'selection',
             ':answer-field/type':':answer-field.type/radio', ':answer-field/choices':choices,
             ':answer-field/correct':[':answer/id',choices[1][':answer/id']]}
    integral = r'\oint_C \left('+tex(P)+r'\right)\,dx+\left('+tex(Q)+r'\right)\,dy'
    prompt = ("Use Green's theorem to evaluate $"+r'\oint_C F\cdot dr'+',$ where '
        '$F(x,y)='+r'\langle '+tex(P)+','+tex(Q)+r'\rangle'+
        '$ and $C$ is the boundary of the triangle with vertices at $(0,0),$ '
        '$(2,-1)$ and $(2,1),$ traversed counterclockwise.')
    solution = (THEOREM+'\n\nThe region $D$ and the curve $C$ for this case are shown below.\n\n'
        '![]('+IMAGE+')\n\nFirst, notice that we can rewrite our integral as follows:\n\n$$\n'
        +r'\oint_C F\cdot dr='+integral+'\n$$\n\n'
        'We have that $P(x,y)='+tex(P)+'$ and $Q(x,y)='+tex(Q)+'.$ Therefore,\n\n$$\n'
        +r'\begin{aligned}\frac{\partial P}{\partial y}&='+tex(py)+r',\\'
        +r'\frac{\partial Q}{\partial x}&='+tex(qx)+r'.\end{aligned}'+'\n$$\n\n'
        'We can express the region $D$ as a type I region as follows:\n\n$$\n'
        +r'D=\{(x,y):0\le x\le2,\,-x/2\le y\le x/2\}.'+'\n$$\n\n'
        "Therefore, applying Green's theorem, we get\n\n$$\n"
        +r'\begin{aligned}'+integral+r'&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\'
        +r'&=\iint_D\left(('+tex(qx)+')-('+tex(py)+r')\right)\,dA\\'
        +r'&=\iint_D '+tex(curl)+r'\,dA\\'
        +r'&=\int_0^2\int_{-x/2}^{x/2} '+tex(curl)+r'\,dy\,dx\\'
        +r'&=\int_0^2 '+tex(curl)+r'[y]_{-x/2}^{x/2}\,dx\\'
        +r'&=\int_0^2 '+tex(curl)+r'(x)\,dx\\'
        +r'&=\int_0^2 '+tex(inner)+r'\,dx\\'
        +r'&=\left['+tex(sp.integrate(inner,x))+r'\right]_0^2\\'
        +r'&='+tex(answer)+r'.\end{aligned}'+'\n$$')
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
        'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
            ':question/difficulty':':question.difficulty/hard',':question/answer-fields':[field]},
        'generation':{'version':VERSION,'template':'triangle-linear-curl','bank_profile':'q-41475-complete',
            'seed':seed,'parameters':{'a':a},'domain':'a integer, 1<=a<=12',
            'source_ids':['q-41475'],'source_basis':2602,
            'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','assets':[IMAGE],
            'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+
        (' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '')
        for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',default='hard',choices=['easy','moderate','hard'])
    p.add_argument('--count',type=int,default=1)
    p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json','markdown'],default='json')
    args=p.parse_args()
    if args.difficulty!='hard':p.error('unsupported difficulty: only hard is validated')
    if not 1<=args.count<=len(DOMAIN):p.error('finite domain: count must be 1..12')
    records=[generate(args.difficulty,args.seed,{'a':a}) for a in random.Random(args.seed).sample(DOMAIN,args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
