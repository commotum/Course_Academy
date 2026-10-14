#!/usr/bin/env python3
"""Source-anchored moderate distributivity generator; no database writes.

q-13536: (A+B)-C-(B-C)=A. Fixed 2x2 layout and ordered cancellation
stages. One complete five-option source profile; a duplicate incomplete field
in the source is excluded explicitly. Easy/hard have no implemented generator.
"""
import argparse
import hashlib
import json
import random
import sys
import uuid
from pathlib import Path
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
VERSION = 'distributivity-moderate-1'
GENERATOR_ID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
SOURCE = {'database':'math','basis':2277,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','question':'q-13536'}
PROFILE = 'q-13536-complete'
RECIPES = ('B', 'A', 'zero', 'A00_minus_one_copy_A01_to_A10', 'C')
ORIGINAL = {'A':[[6,7],[4,5]], 'B':[[3,2],[2,3]], 'C':[[5,1],[6,8]]}

def matrix(m):
    return r'\begin{bmatrix}' + r' \\ '.join(' & '.join(map(str,row)) for row in m) + r'\end{bmatrix}'

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def mathematical_key(p):
    # Canceled matrices and distractor changes cannot inflate inventory.
    return digest(['(A+B)-C-(B-C)',p['A']])

def bank(p):
    a,b,c=(sp.Matrix(p[name]) for name in 'ABC')
    result=(a+b)-c-(b-c)
    assert result == a
    altered=sp.Matrix([[a[0,0]-1,a[0,1]],[a[0,1],a[1,1]]])
    objects=[b,result,sp.zeros(2),altered,c]
    if len({tuple(m) for m in objects}) != 5:
        raise ValueError('Entire source profile rejected: equivalent options')
    return [matrix(m.tolist()) for m in objects]

def generate(level='moderate',seed=0,parameters=None,profile=PROFILE):
    if level != 'moderate':
        raise ValueError('Bounded capability exception: only moderate is implemented; see capability.json')
    if profile != PROFILE:
        raise ValueError('Unsupported complete profile')
    rng=random.Random(seed)
    for attempt in range(1000):
        p=parameters or {name:[[rng.randint(0,9) for _ in range(2)] for _ in range(2)] for name in 'ABC'}
        if set(p) != set('ABC') or any(len(p[n])!=2 or any(len(row)!=2 for row in p[n]) for n in 'ABC'):
            raise ValueError('Required three 2x2 matrices')
        if any(type(x) is not int or not 0<=x<=9 for n in 'ABC' for row in p[n] for x in row):
            raise ValueError('Moderate sampling policy: integer entries from 0 through 9')
        try:
            values=bank(p)
            break
        except ValueError:
            if parameters is not None: raise
    else:
        raise ValueError('No valid whole source bank within bounded attempts')
    fingerprint=digest([VERSION,profile,p])
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_ID),fingerprint))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=answers[1][':answer/id']
    random.Random(seed ^ 0xCA00992).shuffle(answers)
    problem='Find $(A+B)-C-(B-C)$, if\n\n$$\n'+',\\,'.join(n+'='+matrix(p[n]) for n in 'ABC')+'.\n$$'
    solution='First, we simplify the expression by distributing the subtraction over the matrices in the parentheses:\n\n$$\n'+r'\begin{aligned}(A+B)-C-(B-C) & =A+B-C-B+C \\  & =A+\cancel{B}-\cancel{C}-\cancel{B}+\cancel{C} \\  & =A\end{aligned}'+'\n$$\n\nWe are left with a single matrix. So, the result is \n\n$$\n'+r'\begin{aligned}A & ='+matrix(p['A'])+r'\end{aligned}'+'\n$$'
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':'double-cancellation-single-matrix','bank_profile':profile,'recipes':list(RECIPES),'source':SOURCE,'seed':seed,'parameters':p,'parameter_fingerprint':fingerprint,'mathematical_key':mathematical_key(p),'domain':'three 2x2 matrices; integer entries 0..9; five distinct complete-bank matrices','runtime':{'sympy':sp.__version__},'source_field_exclusion':'legacy duplicate key selection without correct ref; source unchanged'}}

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
