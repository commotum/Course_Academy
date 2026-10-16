#!/usr/bin/env python3
"""Moderate matrix distributivity with varying grouping and surviving roles.

Six expression structures and six role assignments preserve the source's
distribution / two cancellations / one surviving matrix method. No DB writes.
"""
import argparse
import ast
import hashlib
import itertools
import json
import random
import sys
import uuid
from pathlib import Path
if Path(__file__).with_name('math_format.py').is_file():
    from math_format import matrix_operands
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.question_capture.math_format import matrix_operands
try:
    import sympy as sp
except ModuleNotFoundError:
    # The application invokes system Python; reuse installed repo dependencies.
    for packages in (Path(__file__).resolve().parents[2]/'.venv/lib').glob('python*/site-packages'):
        sys.path.insert(0,str(packages))
    import sympy as sp

KP_ID = 17592186100992
KP_UUID = '16e62b0e-adda-5d35-aeb9-961057dce8f0'
TITLE = 'Calculating the Sum or Difference of Three or More Matrices Using Distributivity'
VERSION = 'distributivity-moderate-3'
GENERATOR_ID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
SOURCE = {'database':'math','basis':2277,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','question':'q-13536'}
PROFILE = 'q-13536-complete'
RECIPES = ('B', 'A', 'zero', 'A00_minus_one_copy_A01_to_A10', 'C')
ORIGINAL = {'A':[[6,7],[4,5]], 'B':[[3,2],[2,3]], 'C':[[5,1],[6,8]]}
# X survives; Y and Z cancel. X can occur inside a subtracted group, at
# the beginning, in the middle, or at the end. Displayed matrices stay A/B/C.
TEMPLATES = (
    '(X+Y)-Z-(Y-Z)',
    '(Y-Z)-(Y-X)+Z',
    'Y-(Z-X)-(Y-Z)',
    '(Y+X)-(Z+Y)+Z',
    'Y-(Z+Y)+(Z+X)',
    '(Z+Y)-(Z-X)-Y',
)
ROLES = tuple(''.join(p) for p in itertools.permutations('ABC'))

def expression_for(template, roles):
    if type(template) is not int or not 0 <= template < len(TEMPLATES) or roles not in ROLES:
        raise ValueError('Unsupported expression structure or matrix roles')
    return TEMPLATES[template].translate(str.maketrans(dict(zip('XYZ', roles))))

def expanded_terms(expression):
    """Distribute signs in displayed order, without simplifying away the work."""
    def visit(node, sign=1):
        if isinstance(node, ast.Name) and node.id in 'ABC':
            return [(sign, node.id)]
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
            return visit(node.left, sign) + visit(node.right, -sign if isinstance(node.op, ast.Sub) else sign)
        raise ValueError('Expected only matrix addition, subtraction and parentheses')
    return visit(ast.parse(expression, mode='eval').body)

def render_terms(terms, survivor=None):
    return ''.join(('+' if sign == 1 and i else '-' if sign == -1 else '') +
                   (r'\cancel{' + name + '}' if survivor is not None and name != survivor else name)
                   for i, (sign, name) in enumerate(terms))

def matrix(m):
    return r'\begin{bmatrix}' + r' \\ '.join(' & '.join(map(str,row)) for row in m) + r'\end{bmatrix}'

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def mathematical_key(p, expression='(A+B)-C-(B-C)', survivor='A'):
    # Canceled matrices and distractor changes cannot inflate inventory.
    return digest([expression,p[survivor]])

def bank(p, expression='(A+B)-C-(B-C)', roles='ABC'):
    a,b,c=(sp.Matrix(p[name]) for name in roles)
    result=sum((sign*sp.Matrix(p[name]) for sign,name in expanded_terms(expression)), sp.zeros(2))
    assert result == a
    altered=sp.Matrix([[a[0,0]-1,a[0,1]],[a[0,1],a[1,1]]])
    objects=[b,result,sp.zeros(2),altered,c]
    if len({tuple(m) for m in objects}) != 5:
        raise ValueError('Entire source profile rejected: equivalent options')
    return [matrix(m.tolist()) for m in objects]

def generate(level='moderate',seed=0,parameters=None,profile=PROFILE,template=None,roles=None):
    if level != 'moderate':
        raise ValueError('Bounded capability exception: only moderate is implemented; see capability.json')
    if profile != PROFILE:
        raise ValueError('Unsupported complete profile')
    rng=random.Random(seed)
    template = rng.randrange(len(TEMPLATES)) if template is None else template
    roles = rng.choice(ROLES) if roles is None else roles
    expression = expression_for(template, roles)
    survivor = roles[0]
    for attempt in range(1000):
        p=parameters if parameters is not None else {name:[[rng.randint(0,9) for _ in range(2)] for _ in range(2)] for name in 'ABC'}
        if set(p) != set('ABC') or any(len(p[n])!=2 or any(len(row)!=2 for row in p[n]) for n in 'ABC'):
            raise ValueError('Required three 2x2 matrices')
        if any(type(x) is not int or not 0<=x<=9 for n in 'ABC' for row in p[n] for x in row):
            raise ValueError('Moderate sampling policy: integer entries from 0 through 9')
        try:
            values=bank(p, expression, roles)
            break
        except ValueError:
            if parameters is not None: raise
    else:
        raise ValueError('No valid whole source bank within bounded attempts')
    fingerprint=digest([VERSION,profile,expression,roles,p])
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_ID),fingerprint))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=answers[1][':answer/id']
    random.Random(seed ^ 0xCA00992).shuffle(answers)
    problem='Find $'+expression+'$, if\n\n'+matrix_operands(n+'='+matrix(p[n]) for n in 'ABC')
    terms=expanded_terms(expression)
    solution='First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:\n\n$$\n'+r'\begin{aligned}'+expression+' & ='+render_terms(terms)+r' \\  & ='+render_terms(terms,survivor)+r' \\  & ='+survivor+r'\end{aligned}'+'\n$$\n\nWe are left with a single matrix. So, the result is \n\n$$\n'+r'\begin{aligned}'+survivor+' & ='+matrix(p[survivor])+r'\end{aligned}'+'\n$$'
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':'double-cancellation-single-matrix','structure':template,'roles':roles,'expression':expression,'survivor':survivor,'bank_profile':profile,'recipes':[roles[1],survivor,'zero','altered-survivor',roles[2]],'source':SOURCE,'seed':seed,'parameters':p,'parameter_fingerprint':fingerprint,'mathematical_key':mathematical_key(p,expression,survivor),'domain':'three 2x2 matrices; integer entries 0..9; five distinct complete-bank matrices','runtime':{'sympy':sp.__version__},'source_field_exclusion':'legacy duplicate key selection without correct ref; source unchanged'}}

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='moderate');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
    if args.count<1: parser.error('count must be positive')
    records=[];used=set()
    for i in range(max(1000,args.count*100)):
        r=generate(args.difficulty,args.seed+i)
        key=r['generation']['mathematical_key']
        if key not in used: records.append(r);used.add(key)
        if len(records)==args.count: break
    if len(records)!=args.count: raise ValueError('Finite search limit; shortage remains explicit')
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))

if __name__=='__main__':main()
