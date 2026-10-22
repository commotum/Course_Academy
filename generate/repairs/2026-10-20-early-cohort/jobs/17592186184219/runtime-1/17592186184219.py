#!/usr/bin/env python3
"""Seeded easy rank-nullity substitution, preserving complete observed banks.
CLI: .venv/bin/python generate/scratch/17592186184219.py --difficulty easy --count 5
Moderate/hard have no justified same-method source workloads.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
SNAPSHOT=json.loads((Path(__file__).parent/'runtime-source.json').read_text());KP=SNAPSHOT['record'];KP_ID=17592186184219
NAMESPACE=uuid.UUID(KP[':knowledge-point/id']);GENERATOR_UUID=str(uuid.uuid5(NAMESPACE,'question-generator'))
VERSION='rank-nullity-substitution-v2';SUPPORTED_LEVELS=('easy',)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(NAMESPACE,x))
def parse(q):
    text=q[':question/problem'];m,n=map(int,re.search(r'\$(\d+)\s*\\times\s*(\d+)',text).groups())
    k=int(re.search(r'\)\)?=(\d+)',text).group(1))
    return {'m':m,'n':n,'k':k,'target':'rank' if 'dim(Null' in text else 'nullity'}
ORIGINAL={s:parse(q) for s,q in SOURCES.items()}
# Keep whole observed bank shapes, but do not fix which offered value is correct.
PROFILES={s:sorted(int(a[':answer/value'])-(ORIGINAL[s]['n']-ORIGINAL[s]['k']) for a in q[':question/answer-fields'][0][':answer-field/choices']) for s,q in SOURCES.items()}
SHAPES={s:[o-min(offsets) for o in offsets] for s,offsets in PROFILES.items()}

def valid(p,profile=None):
    if set(p)!={'m','n','k','target'} or any(type(p[x]) is not int for x in ('m','n','k')):return False
    m,n,k=p['m'],p['n'],p['k']
    if not(2<=m<=12 and 2<=n<=12 and 0<=k<=n and p['target'] in ('rank','nullity')):return False
    rank=k if p['target']=='nullity' else n-k
    return 0<=rank<=min(m,n)

def render(p,profile):
    m,n,k,t=(p[x] for x in ('m','n','k','target'));c=n-k
    given=r'\text{dim(Null(}A))' if t=='rank' else r'\text{rank}(A)'
    problem=f'Consider a ${m}\\times {n}$ matrix $A.$ If ${given}={k}'+(',$ then $' if t=='rank' else '$ then $')+r'\text{'+t+r'}(A)=$'
    intro='According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then \n\n$$\n'+r'\text{rank}(A)+\text{nullity}(A)=n.'+'\n$$\n\n'+f'For the given matrix, we have $n={n}.$ Therefore,\n\n$$\n'
    lhs=(r'\text{rank}(A)+'+str(k)) if t=='rank' else (str(k)+r'+\text{nullity}(A)')
    solution=intro+r'\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ '+lhs+f' & ={n}'+r' \\ \text{'+t+r'}(A) & ='+f'{n}-{k}'+r' \\  & ='+f'{c}.'+r'\end{aligned}'+'\n$$'
    if profile=='q-141220':solution=solution.replace(r' & =n \\',f' & ={n}'+r' \\')
    return problem,solution,c

def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None,bank_role=None):
    if level!='easy':raise ValueError('unsupported level: no validated moderate/hard source workload')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio required')
    r=random.Random(seed)
    if template in SOURCES:
        profile=profile or template;template=ORIGINAL[template]['target']
    template=template or (parameters['target'] if parameters else r.choice(('rank','nullity')))
    if template not in ('rank','nullity'):raise ValueError('unsupported target')
    eligible=[s for s in SOURCES if ORIGINAL[s]['target']==template]
    profile=profile or r.choice(eligible)
    if profile not in eligible:raise ValueError('profile/target mismatch')
    if bank_role is not None and (type(bank_role) is not int or not 0<=bank_role<5):
        raise ValueError('bank_role must be an integer from 0 through 4')
    shape=SHAPES[profile]
    replay=False
    if parameters is None:
        # Decide the answer-bearing role before any prompt dimensions. No rejection
        # step depends on that role: all five bank values are feasible targets.
        role=r.randrange(5) if bank_role is None else bank_role
        start=r.randint(0,12-shape[-1])
        values=[start+x for x in shape]
        c=values[role]
        n=r.randint(max(2,values[-1]),12)
        lower=max(2,values[-1] if template=='rank' else n-values[0])
        m=r.randint(lower,12)
        p={'m':m,'n':n,'k':n-c,'target':template}
    else:
        p=dict(parameters)
        if p.get('target')!=template or not valid(p):raise ValueError('parameter constraint')
        c=p['n']-p['k']
        replay=p==ORIGINAL[profile] and bank_role is None
        if replay:
            values=[c+o for o in PROFILES[profile]]
            role=values.index(c)
        else:
            roles=[i for i,x in enumerate(shape) if c>=x]
            role=r.choice(roles) if bank_role is None else bank_role
            if role not in roles:raise ValueError('bank role gives negative choices')
            values=[c-shape[role]+x for x in shape]
    if p['target']!=template or not valid(p):raise ValueError('parameter constraint')
    problem,solution,c=render(p,profile)
    uid=ident(digest({'version':VERSION,'problem':problem,'solution':solution,'values':values}));fid=ident(uid+'/selection')
    choices=[{':answer/id':ident(fid+'/'+str(v)),':answer/type':':answer.type/math',':answer/value':str(v)} for v in values]
    r.shuffle(choices)
    q={':question/id':uid,':question/difficulty':':question.difficulty/easy',':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==str(c))]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'level':level,'seed':seed,'template':template,'profile':profile,'bank_role':role,'source_replay':replay,'parameters':p,'correct_value':str(c),'source_question_ids':[profile],'source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'mathematical_fingerprint':digest([template,p['n'],p['k']]),'dependencies':{'python':sys.version.split()[0]},'domain':'real matrices; rank <= min(rows,columns)','plots':'none'}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def markdown(r):return r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n\nChoices: '+', '.join(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
def main():
    a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--template');a.add_argument('--profile');a.add_argument('--bank-role',type=int);a.add_argument('--format',choices=['json','markdown'],default='json');v=a.parse_args()
    out=[generate(v.difficulty,v.seed+i,template=v.template,profile=v.profile,bank_role=v.bank_role) for i in range(v.count)]
    print(json.dumps(out,indent=2) if v.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
if __name__=='__main__':main()
