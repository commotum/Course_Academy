"""Relocatable easy row operations and retained moderate row addition.

Moderate practice uses the authored arithmetic bank; its legacy banks are replay only.
Easy practice uses a retained swap bank, a full-swap bank and a scaling bank.
"""
import argparse
import copy
import hashlib
import json
import random
import uuid
from pathlib import Path
from math_format import checked_math_content, matrix_tex, normalize_prose, normalize_tex

KP_ID = 17592186059771
KP_UUID = 'eb1afe82-86ba-5a15-9037-74717692ecb2'
TITLE = 'Applying Row Operations To a Coefficients Matrix'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
VERSION = 'row-addition-2.2.0'
MULTIPLIERS = (-5,-4,-3,-2,2,3,4,5)
CANONICAL = {'matrix': [[1,2,3],[4,2,-1],[7,12,13]], 'target':1, 'source':0, 'k':-4, 'name':'A'}
CASES = {
    'q-10243': {'matrix':[[0,3,4],[0,1,2],[0,5,6]],'target':2,'source':1,'k':-5,'name':'G'},
    'q-10248': {'matrix': [[-1,2,4],[8,3,1],[3,-1,9]], 'target':2, 'source':0, 'k':3, 'name':'M'},
    'q-20239': {'matrix': [[1,2,1],[3,-1,1],[2,3,2]], 'target':1, 'source':0, 'k':-3, 'name':'X'},
}

def matrix(rows):
    return matrix_tex(rows)

def answer_matrix(m,t,s,k):
    result=copy.deepcopy(m)
    result[t]=[m[t][j]+k*m[s][j] for j in range(3)]
    return result


def bank(p,profile):
    m,t,s,k = p['matrix'],p['target'],p['source'],p['k']
    other=3-t-s
    good=answer_matrix(m,t,s,k)
    if profile=='q-10243':
        observed=json.loads(Path(__file__).with_name('source_banks.json').read_text())[profile]['bank']
        return [good]+[b for b in observed if b!=good]
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
    if profile=='arithmetic':
        # The bank is exchangeable in the requested multiplier. No nuisance
        # perturbation is attached to the key; every candidate can be the key.
        coefficients=[k]+[v for v in p['candidate_multipliers'] if v!=k]
        rows=[[m[t][j]+v*m[s][j] for j in range(3)] for v in coefficients]
        results=[]
        for row in rows:
            # Share legitimate simplifications across the full bank: a zero
            # or unchanged coordinate must not reveal the key by inspection.
            row=[good[t][j] if good[t][j]==0 or m[s][j]==0 else row[j] for j in range(3)]
            item=copy.deepcopy(m);item[t]=row;results.append(item)
        return results
    raise ValueError('Unknown complete source bank profile')

def validate_parameters(p,profile):
    m,t,s,k=p['matrix'],p['target'],p['source'],p['k']
    if len(m)!=3 or any(len(r)!=3 for r in m) or any(type(x)!=int or not -9<=x<=9 for r in m for x in r):
        raise ValueError('Expected bounded 3 by 3 integer matrix')
    if t not in range(3) or s not in range(3) or t==s or type(k)!=int or not 2<=abs(k)<=5:
        raise ValueError('Distinct row roles and multiplier magnitude 2 through 5 required')
    if profile in CASES and p != CASES[profile]:
        raise ValueError('Legacy banks are restricted to exact source replay')
    if profile=='arithmetic':
        if not any(m[s]):raise ValueError('Nonzero donor required')
        c=p.get('cancellation_column')
        if c not in (None,0,1,2):raise ValueError('Invalid cancellation case')
        if [j for j,x in enumerate(answer_matrix(m,t,s,k)[t]) if x==0] != ([] if c is None else [c]):
            raise ValueError('Cancellation metadata does not match arithmetic')
        coefficients=p.get('candidate_multipliers',[])
        if len(coefficients)!=5 or len(set(coefficients))!=5 or k not in coefficients or any(type(v)!=int or v not in MULTIPLIERS for v in coefficients):
            raise ValueError('Five distinct eligible multipliers including the requested multiplier required')
        good=answer_matrix(m,t,s,k)[t]
        candidates=[b[t] for b in bank(p,profile)]
        for j in range(3):
            column=[row[j] for row in candidates]
            if good[j]==0 or m[s][j]==0:
                if any(v!=good[j] for v in column):raise ValueError('Shared simplification required')
            elif len(set(column))!=5 or any(v==0 or v==m[t][j] for v in column):
                raise ValueError('Bank leaks zero, unchanged-cell, or consensus cue')
    if p['name'] not in ('M','X','G'):raise ValueError('Observed matrix notation required')
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
    solution='The operation '+op+' means that we need to add $'+str(k)+'$ times the '+ordinal[s]+' row to the '+ordinal[t]+' row.\n\nApplying this row operation, we obtain the following:\n\n$$\n'+r'\begin{aligned}'+n+' & ='+matrix(m)+r'\,'+op[1:-1]+r' \\  & \sim'+r'{\small '+matrix(expanded)+r'} \\  & \sim'+matrix(good)+r'\end{aligned}'+'\n$$'
    return prompt,solution

def replay_canonical():
    """The source is a worked example, not a question with an authored bank."""
    original=json.loads(Path(__file__).with_name('canonical.json').read_text())
    question={key:normalize_prose(original[key]) for key in (':question/problem', ':question/worked-solution')}
    question.update({':question/id':original[':question/id'], ':question/answer-fields':[]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
            'question':question,
            'generation':{'version':VERSION,'template':'single-row-addition','profile':'e-4693',
                          'parameters':copy.deepcopy(CANONICAL),'source_question':'e-4693',
                          'source_basis':4144,'source_difficulty':None,'replay_only':True}}

def fingerprint(p):
    # Assessed row arithmetic: ignore unchanged rows, row permutation, notation,
    # seed, bank profile and option order when deciding fresh inventory.
    return hashlib.sha256(json.dumps([p['matrix'][p['source']],p['matrix'][p['target']],p['k']],separators=(',',':')).encode()).hexdigest()

@checked_math_content
def generate(difficulty='easy',seed=0,profile=None,parameters=None):
    if difficulty=='hard':
        if profile is not None:raise ValueError('Hard normal generation has one authored arithmetic profile; source banks use hard.replay')
        from hard import generate as generate_hard
        return generate_hard(seed,parameters)
    if difficulty=='easy':
        from easy import generate as generate_easy
        return generate_easy(seed,profile,parameters)
    if difficulty!='moderate':raise ValueError('Supported difficulties: easy, moderate and hard')
    rng=random.Random(seed); profile=profile or 'arithmetic'
    if profile=='e-4693' or parameters==CANONICAL:
        if parameters is not None and parameters!=CANONICAL:raise ValueError('Canonical replay requires original parameters')
        return replay_canonical()
    if profile not in (*CASES,'arithmetic'):raise ValueError('Unknown profile')
    attempts=1
    if parameters is not None:
        p=copy.deepcopy(parameters);validate_parameters(p,profile)
    elif profile in CASES:
        p=copy.deepcopy(CASES[profile]);validate_parameters(p,profile)
    else:
        # Decide the assessed roles and case before drawing compatible entries.
        s,t=rng.sample(range(3),2)
        coefficients=sorted(rng.sample(MULTIPLIERS,5))
        k=rng.choice(coefficients)
        cancel=rng.choice([None,0,1,2])
        name=rng.choice(['M','X'])
        for attempts in range(1,501):
            m=[[rng.randint(-9,9) for _ in range(3)] for _ in range(3)]
            if cancel is not None:
                m[s][cancel]=rng.choice([-1,1]);m[t][cancel]=-k*m[s][cancel]
            zero_columns=[j for j,v in enumerate(answer_matrix(m,t,s,k)[t]) if v==0]
            if zero_columns != ([] if cancel is None else [cancel]):continue
            p={'matrix':m,'target':t,'source':s,'k':k,'name':name,
               'candidate_multipliers':coefficients,
               'cancellation_column':cancel}
            try:validate_parameters(p,profile);break
            except ValueError:continue
        else:raise ValueError('Bounded sampling exhausted')
    prompt,solution=map(normalize_prose,render(p));values=[normalize_tex(matrix(b)) for b in bank(p,profile)]
    fp=fingerprint(p)
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),prompt+'|'+profile+'|'+VERSION+'|'+json.dumps(sorted(values),separators=(',',':'))));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=choices[0][':answer/id'];rng.shuffle(choices)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':'single-row-addition','profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':fp,'source_question':profile if profile in CASES else ['q-10248','q-20239','e-4693'],'source_basis':5358 if profile=='q-10243' else 4144,'sampling_attempts':attempts,'domain':'3x3 signed integer matrix; distinct source/target rows; |k|=2..5; cancellation optional','replay_only':profile in CASES,'choice_recipes':(['correct']+['exact-source-distractor; interpretation unresolved']*4) if profile=='q-10243' else ['correct','unchanged','swap','negate-target-and-swap','first-cell-only'] if profile=='q-10248' else (['correct','swap-solved-rows','altered-source-to-unused-row','move-altered-source-and-cycle','column-addition'] if profile=='q-20239' else ['requested-multiplier']+['alternative-multiplier']*4)}}

def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n\n'.join('$'+a[':answer/value']+'$'+(' [correct]' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='easy');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--profile',choices=[*sorted(CASES),'arithmetic','q-10250','q-10244','q-10251','q-130006','scale-arithmetic','swap-complete']);args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[];seen=set()
    for offset in range(args.count*100):
        r=generate(args.difficulty,args.seed+offset,args.profile);fp=r['generation']['mathematical_fingerprint']
        if fp not in seen:records.append(r);seen.add(fp)
        if len(records)==args.count:break
    if len(records)<args.count:raise SystemExit('finite-limit: bounded search cannot fulfill count')
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
