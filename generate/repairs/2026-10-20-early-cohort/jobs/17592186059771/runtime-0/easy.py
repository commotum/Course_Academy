"""Easy one-operation coefficient matrices; all source banks stay complete."""
import copy
from fractions import Fraction
import hashlib
import json
import math
import random
import uuid
from math_format import checked_math_content, matrix_tex, normalize_prose, normalize_tex

VERSION = 'easy-row-operations-1.2.0'
KP_UUID = 'eb1afe82-86ba-5a15-9037-74717692ecb2'
FACTORS = (Fraction(2),Fraction(3),Fraction(-2),Fraction(-3),Fraction(1,2),Fraction(1,3),Fraction(-1,2),Fraction(-1,3))
CASES = {
 'q-10250': {'matrix':[[0,8,1],[3,3,6],[4,-1,3]],'rows':[0,1]},
 'q-10244': {'matrix':[[7,4,-1],[1,5,-3],[0,5,-2]],'rows':[0,1]},
 'q-130006': {'matrix':[[2,2,7],[7,-1,3],[6,9,-3]],'target':2,'anchor':0,'factor':[1,3]},
}
PROFILES = ('q-10250', 'swap-complete', 'scale-arithmetic')
REPLAY_ONLY = ('q-10244', 'q-130006')

def is_scaling(profile):return profile in ('q-130006', 'scale-arithmetic')

def tex(v):
    v=Fraction(v)
    if v.denominator==1:return str(v.numerator)
    return ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'

def matrix(m):return matrix_tex([[tex(x) if not isinstance(x,str) else x for x in r] for r in m])

def swap(m,x,y):
    n=copy.deepcopy(m);n[x],n[y]=n[y],n[x];return n

def scale(m,t,k):
    n=copy.deepcopy(m);n[t]=[k*v for v in m[t]];return n

def bank(p,profile):
    m=p['matrix']
    if not is_scaling(profile):
        x,y=p['rows'];z=3-x-y
        def perm(order):
            n=copy.deepcopy(m)
            for dest,src in zip((x,y,z),order):n[dest]=m[src][:]
            return n
        good=swap(m,x,y)
        if profile=='swap-complete':
            permutations=[(1,0,2),(2,1,0),(0,2,1),(1,2,0),(2,0,1)]
            candidates=[[m[i][:] for i in order] for order in permutations]
            return [good]+[b for b in candidates if b!=good]
        if profile=='q-10250':return [good,perm((y,z,x)),copy.deepcopy(m),perm((z,x,y)),perm((z,y,x))]
        copied=copy.deepcopy(m);copied[y]=m[x][:]
        cols=copy.deepcopy(m)
        for row in cols:row[x],row[y]=row[y],row[x]
        return [good,copied,swap(m,y,z),cols,perm((z,x,y))]
    t=p['target'];k=Fraction(*p['factor'])
    if profile=='scale-arithmetic':
        # Every candidate can be the key. Entry constraints apply to the entire
        # bank, so neither row structure nor integrality marks the correct one.
        candidates=sorted(Fraction(*v) for v in p['candidate_factors'])
        return [scale(m,t,v) for v in [k]+[v for v in candidates if v!=k]]
    a=p['anchor'];others=[r for r in range(3) if r!=t]
    good=scale(m,t,k)
    return [good,scale(m,others[0],k),scale(m,others[1],k),swap(good,t,a),scale(m,t,1/k)]

def validate(p,profile):
    m=p['matrix']
    if profile in REPLAY_ONLY and p!=CASES[profile]:raise ValueError(profile+' is exact source replay only; use a production profile')
    if len(m)!=3 or any(len(r)!=3 for r in m) or any(type(x)!=int or not -9<=x<=9 for r in m for x in r):raise ValueError('Bounded integer 3x3 matrix required')
    if len({tuple(r) for r in m})!=3:raise ValueError('Distinct rows required')
    if is_scaling(profile):
        if p['target'] not in range(3):raise ValueError('Eligible target required')
        k=Fraction(*p['factor'])
        if k not in FACTORS or any((k*v).denominator!=1 for v in m[p['target']]):raise ValueError('Eligible factor and integral correct row required')
        if profile=='scale-arithmetic':
            candidates=[Fraction(*v) for v in p['candidate_factors']]
            if len(candidates)!=5 or len(set(candidates))!=5 or k not in candidates or not set(candidates)<=set(FACTORS):raise ValueError('Five eligible factors including requested factor required')
            if any((v*x).denominator!=1 for v in candidates for x in m[p['target']]):raise ValueError('All five candidate outcomes must be integral')
    elif len(p['rows'])!=2 or len(set(p['rows']))!=2 or any(r not in range(3) for r in p['rows']):raise ValueError('Two distinct rows required')
    if len({matrix(b) for b in bank(p,profile)})!=5:raise ValueError('Colliding complete bank')

def render(p,profile):
    m=p['matrix'];ordinals=['first','second','third'];good=bank(p,profile)[0]
    if not is_scaling(profile):
        x,y=p['rows'];op=r'{R}_{'+str(x+1)+r'}\leftrightarrow{R}_{'+str(y+1)+'}'
        text='The operation $'+op+'$ means that we need to swap the '+ordinals[x]+' and '+ordinals[y]+' rows.'
        stages=matrix(good)
        transition='Applying this row operation, we obtain the following:'
    else:
        t=p['target'];k=Fraction(*p['factor']);f=tex(k)
        op=r'{R}_{'+str(t+1)+r'}:='+f+r'{R}_{'+str(t+1)+'}'
        text='The operation $'+op+'$ means that we need to multiply the '+ordinals[t]+' row of the matrix by $'+f+'.$'
        transition='Multiplying the '+ordinals[t]+' row by $'+f+'$, we obtain the following:'
        expanded=copy.deepcopy(m);expanded[t]=[f+r'\cdot ('+str(v)+')' for v in m[t]]
        stages=matrix(expanded)+r' \\ & \sim '+matrix(good)
    prompt='Consider the matrix $A,$ given by\n\n$$\nA='+matrix(m)+'.\n$$\n\nWhat matrix results from carrying out the row operation $'+op+'$ on $A?$'
    solution=text+'\n\n'+transition+'\n\n$$\n'+r'\begin{aligned}A & ='+matrix(m)+r'\quad '+op+r' \\ & \sim '+stages+r'\end{aligned}'+'\n$$'
    return prompt,solution

@checked_math_content
def generate(seed=0,profile=None,parameters=None):
    rng=random.Random(seed);profile=profile or rng.choice(PROFILES)
    if profile not in (*CASES,*PROFILES):raise ValueError('Unknown easy profile')
    if profile in REPLAY_ONLY and parameters is None:parameters=CASES[profile]
    if parameters is not None:
        p=copy.deepcopy(parameters);validate(p,profile);attempts=1
    else:
        # Select the assessed roles and operation before drawing compatible data.
        if profile=='scale-arithmetic':
            t=rng.randrange(3);candidates=sorted(rng.sample(FACTORS,5));k=rng.choice(candidates)
            p={'target':t,'factor':[k.numerator,k.denominator],
               'candidate_factors':[[v.numerator,v.denominator] for v in candidates]}
            divisor=math.lcm(*(v.denominator for v in candidates))
            bound=9//divisor
        else:p={'rows':rng.sample(range(3),2)}
        for attempts in range(1,501):
            m=[[rng.randint(-9,9) for _ in range(3)] for _ in range(3)]
            if profile=='scale-arithmetic':
                m[t]=[divisor*rng.randint(-bound,bound) for _ in range(3)]
            p['matrix']=m
            try:validate(p,profile);break
            except ValueError:continue
        else:raise ValueError('Bounded sampling exhausted')
    prompt,solution=map(normalize_prose,render(p,profile));values=[normalize_tex(matrix(b)) for b in bank(p,profile)]
    # Includes the mathematical task; excludes seed, option order and profile.
    task=[p['matrix'],['scale',p['target'],p['factor']] if is_scaling(profile) else ['swap',sorted(p['rows'])]]
    fp=hashlib.sha256(json.dumps(task,separators=(',',':')).encode()).hexdigest()
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+prompt+profile+json.dumps(sorted(values))));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=choices[0][':answer/id']
    # Decouple display order from role sampling and rejection draw counts.
    random.Random(hashlib.sha256((qid+':order:'+str(seed)).encode()).digest()).shuffle(choices)
    recipes=(['requested-factor']+['alternative-factor']*4 if profile=='scale-arithmetic' else (['correct','scale-other-row-1','scale-other-row-2','scale-then-swap-anchor','reciprocal'] if profile=='q-130006' else (['correct','cycle-yzx','unchanged','cycle-zxy','swap-xz'] if profile=='q-10250' else (['correct','alternative-swap','alternative-swap','cycle-123','cycle-132'] if profile=='swap-complete' else ['correct','copy-x-to-y','swap-yz','swap-columns-xy','cycle-zxy']))))
    source='q-130006' if is_scaling(profile) else (['q-10250','q-10244'] if profile=='swap-complete' else profile)
    return {'knowledge_point':{'db_id':17592186059771,'id':KP_UUID,'title':'Applying Row Operations To a Coefficients Matrix'},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':'single-row-scale' if is_scaling(profile) else 'single-row-swap','profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':fp,'source_question':source,'source_basis':4567,'sampling_attempts':attempts,'source_difficulty':'easy','replay_only':profile in REPLAY_ONLY,'choice_recipes':recipes}}
