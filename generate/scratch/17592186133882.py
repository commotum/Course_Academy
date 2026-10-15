#!/usr/bin/env python3
"""Bounded easy Green's theorem generator; no database writes.

Supported source family: q-109111. The triangle is fixed because the assessed
object is the scalar curl, not a variable integration region. Positive integer
a,b vary the two nonzero supplied terms; b != 2a retains a nonzero answer.
Other captured families remain classified evidence, outside this version.
"""
import argparse
import hashlib
import json
import random
import uuid
import os
import sys
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    # Inventory workers use /usr/bin/python3; use the repository's declared
    # dependencies without changing the worker or installing system packages.
    interpreter = Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__ == '__main__' and interpreter.exists() and Path(sys.executable).resolve()!=interpreter.resolve():
        os.execv(str(interpreter), [str(interpreter), str(Path(__file__).resolve()), *sys.argv[1:]])
    raise

KP_ID = 17592186133882
KP_UUID = 'bf385144-2f48-5874-8c0d-dec31d8fc6e3'
TITLE = "Expressing a Line Integral as a Double Integral Using Green's Theorem"
VERSION = 'greens-triangle-v1'
HERE = Path(__file__).with_suffix('')
IMAGE = 'images/0d/0dfe132146c4095954d6b628b055317c975fed6ec429b9ad48b68f4015d6c033.png'
x, y = sp.symbols('x y', real=True)
DOMAIN = [(a, b) for a in range(1, 6) for b in range(1, 10) if b != 2*a]
THEOREM = (
    "Let $C$ be a positively oriented, piecewise-smooth, simple closed curve in the plane, "
    "and let $D$ be the region bounded by $C.$ If $P$ and $Q$ have continuous first partial "
    "derivatives on an open region containing $D$, then Green's theorem states that\n\n"
    "$$\n\\oint_C P\\,dx+Q\\,dy=\\iint_D"
    "\\left(\\frac{\\partial Q}{\\partial x}-\\frac{\\partial P}{\\partial y}\\right)\\,dA.\n$$"
)

def tex(value):
    return sp.latex(sp.sympify(value))

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), VERSION+':'+value))

def mathematics(a, b):
    if type(a) is not int or type(b) is not int or (a, b) not in DOMAIN:
        raise ValueError('Expected integers 1<=a<=5, 1<=b<=9, b!=2a')
    P, Q = a*y**2, b*x*y
    py, qx = sp.diff(P, y), sp.diff(Q, x)
    answer = sp.expand(qx-py)
    # Complete source bank, in original mathematical order. Interpretations of
    # the final two errors are unresolved; retain their exact expression shapes.
    bank = [answer, b*x, -answer, a*(y-x), a*(x-y)]
    return P, Q, py, qx, answer, bank

def generate(difficulty='easy', seed=0, parameters=None, **kwargs):
    if difficulty != 'easy':
        raise ValueError('Unsupported difficulty: no classified source evidence beyond easy')
    if kwargs.get('template', 'triangle-polynomial') != 'triangle-polynomial':
        raise ValueError('Unsupported template')
    if parameters is None:
        a, b = random.Random(seed).choice(DOMAIN)
    else:
        if set(parameters) != {'a', 'b'}:
            raise ValueError('Expected a,b parameters')
        a, b = parameters['a'], parameters['b']
    P, Q, py, qx, answer, bank = mathematics(a, b)
    # Identities encode mathematical parameters and full bank, never the seed.
    key = f'{a}:{b}'
    qid, fid = uid('q:'+key), uid('q:'+key+':selection')
    choices = [{':answer/id': uid(fid+':'+sp.srepr(value)), ':answer/type': ':answer.type/math',
                ':answer/value': tex(value)} for value in bank]
    field = {':answer-field/id': fid, ':answer-field/key': 'selection',
             ':answer-field/type': ':answer-field.type/radio', ':answer-field/choices': choices,
             ':answer-field/correct': [':answer/id', choices[0][':answer/id']]}
    integral = r'\oint_C \left('+tex(P)+r'\right)\,dx+\left('+tex(Q)+r'\right)\,dy'
    prompt = (
        'Consider the triangle $C$ in the plane with vertices $(-1,0),(1,0)$ and $(0,1),$ '
        'and the region $D$ bounded by $C.$ According to Green\'s theorem,\n\n'
        '$$\n'+integral+r'=\iint_D f(x,y)\,dA.'+'\n$$\n\n'
        'The curve $C$ is traversed counterclockwise. Calculate the function $f(x,y).$'
    )
    solution = (THEOREM+'\n\nThe region $D$ and the curve $C$ for this case are shown below.\n\n'
        '![]('+IMAGE+')\n\n'
        'We have that $P(x,y)='+tex(P)+'$ and $Q(x,y)='+tex(Q)+'.$ Therefore,\n\n'
        '$$\n'+r'\begin{aligned}\frac{\partial P}{\partial y}&='+tex(py)+r',\\'
        +r'\frac{\partial Q}{\partial x}&='+tex(qx)+r'.\end{aligned}'+'\n$$\n\n'
        'Therefore, applying Green\'s theorem, we get\n\n$$\n'
        +r'\begin{aligned}'+integral+r'&=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)\,dA\\'
        +r'&=\iint_D\left(('+tex(qx)+')-('+tex(py)+r')\right)\,dA\\'
        +r'&=\iint_D\left('+tex(answer)+r'\right)\,dA.\end{aligned}'+'\n$$\n\n'
        'Hence, $f(x,y)='+tex(answer)+'.$')
    return {'knowledge_point': {'db_id': KP_ID, 'id': KP_UUID, 'title': TITLE},
            'question': {':question/id': qid, ':question/problem': prompt,
                         ':question/worked-solution': solution, ':question/difficulty': ':question.difficulty/easy',
                         ':question/answer-fields': [field]},
            'generation': {'version': VERSION, 'template': 'triangle-polynomial',
                           'bank_profile': 'q-109111-complete', 'seed': seed,
                           'parameters': {'a': a, 'b': b}, 'source_ids': ['q-109111'],
                           'source_basis': 2576, 'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1',
                           'domain': '1<=a<=5,1<=b<=9,b!=2a; integers',
                           'dependencies': {'sympy': sp.__version__}, 'assets': [IMAGE]}}

def markdown(record):
    q = record['question']; f = q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+
        (' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '')
        for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty', default='easy', choices=['easy', 'moderate', 'hard'])
    p.add_argument('--count', type=int, default=1)
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--format', choices=['json', 'markdown'], default='json')
    args = p.parse_args()
    if args.difficulty!='easy': p.error('unsupported difficulty: only easy is validated')
    if not 1<=args.count<=len(DOMAIN): p.error(f'finite domain: count must be 1..{len(DOMAIN)}')
    pairs = random.Random(args.seed).sample(DOMAIN, args.count)
    records = [generate('easy', args.seed, {'a': a, 'b': b}) for a,b in pairs]
    print(json.dumps(records, indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
