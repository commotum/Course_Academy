"""Seeded single-row addition practice, scoped to KP 17592186059771.

Moderate: observed q-10248 and q-20239 banks. Easy/hard are classified in
the package but are outside this job's implemented sampler; no fabricated bands.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import random
import uuid
try:
    import sympy as sp
except ModuleNotFoundError:
    # The application's worker uses system Python; reuse the project's dependencies.
    import sys
    root = Path(__file__).resolve().parents[2]
    sites = list((root/'.venv/lib').glob('python*/site-packages'))
    if not sites: raise
    sys.path.insert(0,str(sites[0]))
    import sympy as sp

KP_ID = 17592186059771
KP_UUID = 'eb1afe82-86ba-5a15-9037-74717692ecb2'
TITLE = 'Applying Row Operations To a Coefficients Matrix'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = 'row-addition-1.0.0'
HERE = Path(__file__).with_suffix('')
SOURCES = {q[':question/math-academy-id']: q for q in json.loads((HERE/'source.json').read_text())[':knowledge-point/questions']}
CASES = {
    'q-10248': {'matrix': [[-1,2,4],[8,3,1],[3,-1,9]], 'target':2, 'source':0, 'k':3, 'name':'M'},
    'q-20239': {'matrix': [[1,2,1],[3,-1,1],[2,3,2]], 'target':1, 'source':0, 'k':-3, 'name':'X'},
}

def matrix(rows):
    return r'\begin{bmatrix}' + r' \\ '.join(' & '.join(map(str,row)) for row in rows) + r'\end{bmatrix}'

def answer_matrix(m,t,s,k):
    a=sp.Matrix(m); a[t,:]=a[t,:]+k*a[s,:]
    return [list(a.row(i)) for i in range(3)]

def bank(p,profile):
    m,t,s,k = p['matrix'],p['target'],p['source'],p['k']
    other=3-t-s
    good=answer_matrix(m,t,s,k)
    if profile=='q-10248':
        negswap=copy.deepcopy(m); negswap[s]=[-x for x in m[t]]; negswap[t]=m[s][:]
        swap=copy.deepcopy(m); swap[s],swap[t]=swap[t],swap[s]
        partial=copy.deepcopy(m); partial[t][0]=good[t][0]
        return [good,copy.deepcopy(m),swap,negswap,partial]
    if profile=='q-20239':
        swapsolved=copy.deepcopy(good); swapsolved[s],swapsolved[t]=swapsolved[t],swapsolved[s]
        # Observed expression pattern; cognitive interpretation is underdetermined.
        altered=[-m[s][0],k,-m[s][2]]
        misplaced=copy.deepcopy(m); misplaced[other]=altered
        moved=copy.deepcopy(m); moved[s]=altered; moved[t]=m[s][:]; moved[other]=m[t][:]
        column=copy.deepcopy(m)
        for i in range(3): column[i][1]=m[i][1]+k*m[i][0]
        return [good,swapsolved,misplaced,moved,column]
    raise ValueError('Unknown complete source bank profile')

def validate_parameters(p,profile):
    m,t,s,k=p['matrix'],p['target'],p['source'],p['k']
    if len(m)!=3 or any(len(r)!=3 for r in m) or any(type(x)!=int or not -9<=x<=9 for r in m for x in r):
        raise ValueError('Expected bounded 3 by 3 integer matrix')
    if t not in range(3) or s not in range(3) or t==s or type(k)!=int or not 2<=abs(k)<=5:
        raise ValueError('Distinct row roles and multiplier magnitude 2 through 5 required')
    if (profile=='q-10248' and (k<0 or m[s][0]!=-1)) or (profile=='q-20239' and (k>0 or m[s][0]!=1)):
        raise ValueError('Observed signed profile condition')
    if m[t][0]!=-k*m[s][0]:raise ValueError('First target entry must cancel')
    if p['name'] not in ('M','X'):raise ValueError('Observed matrix notation required')
    if len({matrix(x) for x in bank(p,profile)})!=5:raise ValueError('Colliding choices')

def operation(p):
    t,s,k=p['target']+1,p['source']+1,p['k']
    return '${R}_{'+str(t)+'}:={R}_{'+str(t)+'}'+('+' if k>0 else '-')+str(abs(k))+'{R}_{'+str(s)+'}$'

def render(p):
    m,t,s,k,n=p['matrix'],p['target'],p['source'],p['k'],p['name']
    good=answer_matrix(m,t,s,k)
    ordinal=['first','second','third']
    expanded=copy.deepcopy(m)
    expanded[t]=[str(m[t][j])+'+('+str(k)+')('+str(m[s][j])+')' for j in range(3)]
    op=operation(p)
    prompt='Consider the matrix $'+n+',$ given by\n\n$$\n'+n+'='+matrix(m)+'.\n$$\n\nWhat matrix results from carrying out the row operation '+op+' on $'+n+'?$'
    solution='The operation '+op+' means that we need to add $'+str(k)+'$ times the '+ordinal[s]+' row to the '+ordinal[t]+' row.\n\nApplying this row operation, we obtain the following:\n\n$$\n'+r'\begin{aligned}'+n+' & ='+matrix(m)+r'\,'+op[1:-1]+r' \\  & \sim'+matrix(expanded)+r' \\  & \sim'+matrix(good)+r'\end{aligned}'+'\n$$'
    return prompt,solution

def fingerprint(p):
    # Assessed row arithmetic: ignore unchanged rows, row permutation, notation,
    # seed, bank profile and option order when deciding fresh inventory.
    return hashlib.sha256(json.dumps([p['matrix'][p['source']],p['matrix'][p['target']],p['k']],separators=(',',':')).encode()).hexdigest()

def generate(difficulty='moderate',seed=0,profile=None,parameters=None):
    if difficulty!='moderate':raise ValueError('This validated package implements only the requested moderate band; other bands remain pending')
    rng=random.Random(seed); profile=profile or rng.choice(sorted(CASES))
    if profile not in CASES:raise ValueError('Unknown profile')
    if parameters is not None:
        p=copy.deepcopy(parameters);validate_parameters(p,profile)
    else:
        for _ in range(500):
            s,t=rng.sample(range(3),2);k=rng.randint(2,5)*(1 if profile=='q-10248' else -1)
            m=[[rng.randint(-9,9) for _ in range(3)] for _ in range(3)]
            m[s][0]=-1 if profile=='q-10248' else 1;m[t][0]=-k*m[s][0]
            p={'matrix':m,'target':t,'source':s,'k':k,'name':CASES[profile]['name']}
            try:validate_parameters(p,profile);break
            except ValueError:continue
        else:raise ValueError('Bounded sampling exhausted')
    prompt,solution=render(p);values=[matrix(b) for b in bank(p,profile)]
    fp=fingerprint(p)
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),prompt+'|'+profile+'|'+VERSION));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=choices[0][':answer/id'];rng.shuffle(choices)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':'single-row-addition','profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':fp,'source_question':profile,'source_basis':2366,'sympy_version':sp.__version__,'domain':'3x3 signed integer matrix; first target entry cancels; distinct source/target rows; |k|=2..5','choice_recipes':['correct','unchanged','swap','negate-target-and-swap','first-cell-only'] if profile=='q-10248' else ['correct','swap-solved-rows','altered-source-to-unused-row','move-altered-source-and-cycle','column-addition']}}

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n\n'.join('$'+a[':answer/value']+'$'+(' [correct]' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='moderate');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--profile',choices=sorted(CASES));args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[];seen=set()
    for offset in range(args.count*100):
        r=generate(args.difficulty,args.seed+offset,args.profile);fp=r['generation']['mathematical_fingerprint']
        if fp not in seen:records.append(r);seen.add(fp)
        if len(records)==args.count:break
    if len(records)<args.count:raise SystemExit('finite-limit: bounded search cannot fulfill count')
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
