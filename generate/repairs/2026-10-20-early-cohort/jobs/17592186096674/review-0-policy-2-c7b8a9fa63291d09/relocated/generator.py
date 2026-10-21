#!/usr/bin/env python3
"""Seeded, relocatable easy Gauss-Jordan questions, with exact source replay."""
import argparse
import hashlib
import json
import math
import random
import uuid
from pathlib import Path
import sympy as sp
from math_format import matrix_tex, system_tex, normalize_prose, normalize_tex, checked_math_content
DATA=json.loads(Path(__file__).with_name('source-data.json').read_text())
PROFILES={p['id']:p for p in DATA['profiles']}
MASKS=((1,1,1),(0,1,1),(1,0,1),(1,1,0)) # a12,a13,a23
COEFFS=tuple(range(-5,0))+tuple(range(1,6))
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(DATA['kp_uuid']),'question-generator'))
VERSION='2.0.0'

def bank_points(profile,translation,scale):
    bank=PROFILES[profile]['bank'];columns=[]
    for j in range(3):
        lo=min(v[j] for v in bank)
        g=math.gcd(*(v[j]-lo for v in bank)) or 1
        vals=[(v[j]-lo)//g for v in bank];center=max(vals)//2
        columns.append([(v-center)*scale+translation[j] for v in vals])
    return [list(v) for v in zip(*columns)]

def make_instance(seed=0,profile=None,parameters=None,replay=False):
    rng=random.Random(seed);profile=profile or rng.choice(sorted(PROFILES));p=PROFILES[profile]
    if replay:
        return {'profile':profile,'A':[r[:3] for r in p['matrix']],'b':[r[3] for r in p['matrix']],'bank':p['bank'],'role':p['correct_role'],'mode':'source-replay','parameters':{}}
    supplied=parameters or {}
    role=supplied.get('role',rng.randrange(5))
    mask=tuple(supplied.get('mask',rng.choice(MASKS)))
    if role not in range(5) or mask not in MASKS:raise ValueError('Unsupported role/mask')
    coeff=supplied.get('coefficients',[rng.choice(COEFFS) if active else 0 for active in mask])
    if len(coeff)!=3 or any((v not in COEFFS if active else v!=0) for active,v in zip(mask,coeff)):raise ValueError('Invalid coefficients')
    shift=supplied.get('translation',[rng.randint(-5,5) for _ in range(3)])
    scale=supplied.get('scale',rng.choice((1,2)))
    if len(shift)!=3 or any(not isinstance(v,int) or abs(v)>5 for v in shift) or scale not in (1,2):raise ValueError('Invalid bank parameters')
    a,c,d=coeff;A=[[1,a,c],[0,1,d],[0,0,1]]
    bank=bank_points(profile,shift,scale);v=bank[role]
    b=[sum(x*y for x,y in zip(row,v)) for row in A]
    return {'profile':profile,'A':A,'b':b,'bank':bank,'role':role,'mode':'authored-role-bank','parameters':{'role':role,'mask':list(mask),'coefficients':coeff,'translation':shift,'scale':scale}}

def lhs(row):
    out=''
    for a,var in zip(row,'xyz'):
        if not a:continue
        term=('' if abs(a)==1 else str(abs(a)))+var
        out+=('-' if a<0 else ('+' if out else ''))+term
    return out or '0'

def mat(rows):return matrix_tex(rows,augmented=True)
def solution(instance,shape):
    rows=[r+[v] for r,v in zip(instance['A'],instance['b'])]
    out='The augmented matrix for this system is\n\n$$\nM='+mat(rows)+'.\n$$\n\nNotice that the matrix $M$ is already in row echelon form.\n\nTransforming $M$ to reduced row echelon form, we have'
    for target,pivot,col in [(1,2,2),(0,2,2),(0,1,1)]:
        k=-rows[target][col]
        if not k:continue
        operation=f'R_{{{target+1}}}:=R_{{{target+1}}}'+('+' if k>0 else '-')+('' if abs(k)==1 else str(abs(k)))+f'R_{{{pivot+1}}}'
        rows[target]=[x+k*y for x,y in zip(rows[target],rows[pivot])]
        out+='\n\n$$\n'+operation+r',\qquad M\sim '+mat(rows)+'.\n$$'
    if shape!='rref':
        v=instance['bank'][instance['role']]
        out+='\n\nThe corresponding system is now\n\n$$\n'+system_tex([f'{var}={n}' for var,n in zip('xyz',v)])+'.\n$$\n\n'+f'So, we have the solution $x={v[0]}$, $y={v[1]}$, and $z={v[2]}$.'
        if shape=='vector':out+=' Or, in vector form, $'+value(v,'vector')+'$.'
    return normalize_prose(out)

def value(v,shape):
    if shape=='rref':return normalize_tex(r'M\sim '+mat([[1,0,0,v[0]],[0,1,0,v[1]],[0,0,1,v[2]]]))
    if shape=='vector':return normalize_tex(r'\langle '+','.join(map(str,v))+r'\rangle')
    return normalize_prose(f'$x={v[0]}$, $y={v[1]}$, and $z={v[2]}$')

@checked_math_content
def render(instance,seed=0,order=None):
    p=PROFILES[instance['profile']];shape=p['shape']
    augmented=sp.Matrix([r+[b] for r,b in zip(instance['A'],instance['b'])])
    reduced,_=augmented.rref()
    if list(reduced[:,3]) != instance['bank'][instance['role']]:raise ValueError('Inconsistent instance')
    prompt='Consider the following system of linear equations:\n\n$$\n'+system_tex([lhs(row)+'='+str(b) for row,b in zip(instance['A'],instance['b'])])+'\n$$\n\nUse the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form'+('.' if shape=='rref' else ', and then solve the linear system.')
    prompt=normalize_prose(prompt);sol=solution(instance,shape)
    values=[value(v,shape) for v in instance['bank']]
    identity=json.dumps([prompt,sorted(values)],sort_keys=True)
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/text' if shape=='text' else ':answer.type/math',':answer/value':v} for v in values]
    key=answers[instance['role']][':answer/id']
    if order is None:order=list(range(5));random.Random(seed).shuffle(order)
    if sorted(order)!=list(range(5)):raise ValueError('Invalid choice order')
    return {'knowledge_point':{'db_id':DATA['kp_id'],'id':DATA['kp_uuid'],'title':DATA['title']},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[answers[i] for i in order],':answer-field/correct':[':answer/id',key]}]},'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'template':shape,'source_profile':p['id'],'source_question_id':p['source_uuid'],'bank_profile':instance['mode']+':'+p['id'],'source_basis':DATA['basis'],'instance':instance,'semantic_hash':hashlib.sha256(identity.encode()).hexdigest(),'eligible_for_learning':True,'evidence_only':False}}

@checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None,replay=False):
    if difficulty!='easy':raise ValueError('Only easy has supported source evidence')
    return render(make_instance(seed,template,parameters,replay),seed)

def batch(difficulty,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);records=[];seen=set();attempts=0
    while len(records)<count:
        attempts+=1
        if attempts>count*10+10:raise RuntimeError('Unable to obtain unique items')
        r=generate(difficulty,rng.getrandbits(64));key=r['generation']['semantic_hash']
        if key in seen:continue
        seen.add(key);records.append(r)
    return records
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='easy');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args();print(json.dumps(batch(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
