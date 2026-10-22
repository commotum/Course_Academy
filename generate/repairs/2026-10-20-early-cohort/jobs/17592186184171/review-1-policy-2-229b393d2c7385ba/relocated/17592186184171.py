#!/usr/bin/env python3
"""Rank/nullity from column-space bases or parametrized null spaces.

Seeded, relocatable, database-free generator; easy and moderate only.
Source replay and translated bank shapes are documented in instructional-account.md.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
from math_format import checked_math_content, matrix_tex, normalize_prose, normalize_tex
SNAPSHOT=json.loads(Path(__file__).with_name('source-data.json').read_text())
KP=SNAPSHOT['record']; KP_ID=17592186184171
NAMESPACE=uuid.UUID(KP[':knowledge-point/id'])
GENERATOR_UUID=str(uuid.uuid5(NAMESPACE,'question-generator'))
VERSION='rank-nullity-description-v2'
SUPPORTED_LEVELS=('easy','moderate')
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
ORIGINAL={
 'q-35305':{'m':3,'n':5,'k':3},'q-35433':{'m':3,'n':6,'k':3},
 'q-141230':{'m':5,'n':7,'k':4},'q-142487':{'m':6,'n':8,'k':5},
 'q-142485':{'m':4,'n':5,'k':2},'q-141232':{'m':6,'n':10,'k':4},
 'q-35306':{'matrix':[[2,0],[1,0],[0,1],[1,1]],'indices':[2,3]},
 'q-142486':{'matrix':[[1,0,0],[-1,1,0],[0,0,1],[1,0,-1]],'indices':[1,2,3]},
 'q-35434':{'matrix':[[1,2,0],[0,1,-1],[-3,0,1],[1,1,1]],'indices':[1,2,3]},
 'q-79352':{'matrix':[[1,0,0],[0,1,0],[0,0,1],[0,0,0]],'indices':[1,2,3]},
 'q-139982':{'matrix':[[1,0,0],[0,-1,0],[0,1,1],[0,1,0]],'indices':[1,2,3]},
 'q-141229':{'m':4,'n':5,'k':3},
 'q-142489':{'matrix':[[1,0],[0,0],[1,1],[0,0],[0,0]],'indices':[1,2]},
 'q-79350':{'matrix':[[-1,1,0],[0,1,-1],[1,0,1],[0,0,0],[0,0,0]],'indices':[1,2,3]},
 'q-79351':{'matrix':[[1,1],[1,-1],[0,0],[1,0],[0,0]],'indices':[1,2]}}
SOURCE_PROFILE={'q-35305':'small','q-35433':'small','q-141230':'small','q-142487':'offset-minus1','q-142485':'offset-minus2','q-141232':'dimensions','q-35306':'one-through5','q-142486':'zero-through4','q-35434':'one-through5','q-79352':'zero-through4','q-139982':'zero-through4','q-141229':'one-through5','q-142489':'one-through5','q-79350':'zero-through4','q-79351':'zero-through4'}
PROFILES={'easy':('small','offset-minus1','offset-minus2','dimensions','one-through5'),'moderate':('zero-through4','one-through5')}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(NAMESPACE,x))
# Source shapes are translated without tying any numeric position to correctness.
SHAPES={'small':(0,1,2,3,4),'offset-minus1':(0,1,2,3,4),
        'offset-minus2':(0,2,3,4,5),'dimensions':(0,1,2,3,5),
        'one-through5':(0,1,2,3,4)}

def bank(profile,p,correct=None,anchor=0,scale=1):
    if profile=='zero-through4':return list(range(5))
    return [anchor+scale*x for x in SHAPES[profile]]

def eligible_values(m,n,values):
    return [v for v in values if 1<=n-v<=min(m,n-1)]

def bank_candidates(p,profile,correct=None):
    out=[]
    for scale in ((1,2) if profile=='dimensions' else (1,)):
        for anchor in range(p['n']):
            values=bank(profile,p,anchor=anchor,scale=scale)
            eligible=eligible_values(p['m'],p['n'],values)
            if len(eligible)>=2 and (correct is None or correct in eligible):
                out.append((anchor,scale,values,eligible))
    return out

def valid(level,p,profile):
    if level=='easy':
        if set(p)!={'m','n','k'} or any(type(x)is not int for x in p.values()):return False
        return 2<=p['m']<=7 and 4<=p['n']<=12 and 1<=p['k']<=min(p['m'],p['n']-1)
    if set(p)!={'matrix','indices'}:return False
    m=p['matrix'];ind=p['indices']
    if len(m) not in (4,5) or ind not in ([1,2],[2,3],[1,2,3]):return False
    if any(len(row)!=len(ind) or any(type(v)is not int or abs(v)>3 for v in row) for row in m):return False
    return sp.Matrix(m).rank()==len(ind)

def sample(level,r,profile):
    if level=='easy':
        m=r.randint(2,7);n=r.randint(4,12)
        # Bank comes before the qualifying role. At least two values can qualify
        # with these exact dimensions, so neither shape nor endpoints fix the key.
        p={'m':m,'n':n}
        anchor,scale,values,eligible=r.choice(bank_candidates(p,profile))
        p['k']=n-r.choice(eligible)
        return p,anchor,scale,values
    n=r.choice((4,5));k=r.choice((2,3))
    indices=r.choice([[1,2],[2,3]]) if k==2 else [1,2,3]
    for _ in range(10000):
        p={'matrix':[[r.randint(-3,3) if r.random()<.65 else 0 for _ in indices] for _ in range(n)],'indices':indices}
        if valid(level,p,profile):
            return p,None,None,list(range(5)) if profile=='zero-through4' else list(range(1,6))
    raise ValueError('bounded sampler could not satisfy selected profile')

def expr(coefficients,indices):
    parts=[]
    for c,i in zip(coefficients,indices):
        if not c:continue
        term=('' if abs(c)==1 else str(abs(c)))+f'{{x}}_{{{i}}}'
        parts.append(('-' if c<0 else '+' if parts else '')+term)
    return ''.join(parts) or '0'

def render(level,p,template):
    intro='According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then \n\n$$\n'+r'\text{rank}(A)+\text{nullity}(A)=n.'+'\n$$\n\n'
    if level=='easy':
        m,n,k=p['m'],p['n'],p['k'];answer=n-k
        basis=','.join(f'{{b}}_{{{i}}}' for i in range(1,k+1))
        problem=f'Let $A$ be a ${m}\\times {n}$ matrix. If $B=\\{{{basis}\\}}$ is a basis of $\\text{{Col}}(A)$, find $\\text{{dim(Null}}(A)).$'
        solution=intro+f'For the given matrix, we have $n={n},$ and since $B$ is formed by ${k}$ {"vector" if k==1 else "vectors"}, $\\text{{rank}}(A)={k}.$ Therefore,\n\n$$\n'+r'\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ '+f'{k}+'+r'\text{nullity}(A) & ='+f'{n}'+r' \\ \text{nullity}(A) & ='+f'{n}-{k}'+r' \\ \text{dim(Null}(A)) & ='+f'{answer}.'+r'\end{aligned}'+'\n$$'
    else:
        C=sp.Matrix(p['matrix']);n=C.rows;k=C.cols;answer=n-k
        indices=p['indices'];vector=matrix_tex([[expr(row,indices)] for row in p['matrix']]);variables=','.join(f'{{x}}_{{{i}}}' for i in indices)
        space=r'\text{Null}(A)=\{'+vector+r'\,|\,\,'+variables+r'\in R\}'
        problem=('Find $'+r'\text{rank}(A)'+'$ given that\n\n$$\n'+space+'.\n$$') if template=='null-space-display' else 'Find $'+r'\text{rank}(A)'+'$ given that $'+space+'.$'
        expanded='+'.join(f'{{x}}_{{{indices[j]}}}'+matrix_tex([[C[i,j]] for i in range(n)]) for j in range(k))
        solution=intro+f'For the given matrix, we have $n={n},$ since this is the number of components in each of the vectors of the null space. \n\nAlso, since \n\n$$\n'+r'\text{Null}(A)=\{'+expanded+r'\,|\,\,'+variables+r'\in R\}'+'\n$$\n\n'+f'we conclude that $\\text{{nullity}}(A)={k}.$\n\nTherefore,\n\n$$\n'+r'\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ \text{rank}(A)+'+f'{k} & ={n}'+r' \\ \text{rank}(A) & ='+f'{n}-{k}'+r' \\  & ='+f'{answer}.'+r'\end{aligned}'+'\n$$'
    return normalize_prose(problem),normalize_prose(solution),answer

@checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None,bank_anchor=None,bank_scale=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty; hard has no validated source workload')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio required')
    r=random.Random(seed)
    if template in SOURCES:
        source=template
        if SOURCES[source][':question/difficulty'][':db/ident'].split('/')[-1]!=level:raise ValueError('source/level mismatch')
        template='column-basis' if level=='easy' else 'null-space-display' if source in ('q-35434','q-79350') else 'null-space-inline'
        profile=profile or SOURCE_PROFILE[source]
    else:source=None
    template=template or ('column-basis' if level=='easy' else r.choice(['null-space-inline','null-space-display']))
    if template not in (['column-basis'] if level=='easy' else ['null-space-inline','null-space-display']):raise ValueError('template/level mismatch')
    profile=profile or r.choice(PROFILES[level])
    if profile not in PROFILES[level]:raise ValueError('profile/level mismatch')
    if source and parameters is None:parameters=ORIGINAL[source]
    if parameters is None:
        p,anchor,scale,values=sample(level,r,profile)
        if bank_anchor is not None or bank_scale is not None:raise ValueError('bank translation requires explicit parameters')
    else:
        p=json.loads(json.dumps(parameters));anchor=None;scale=None
        if not valid(level,p,profile):raise ValueError('parameter/profile constraint')
        if source and p==ORIGINAL[source] and profile==SOURCE_PROFILE[source]:
            values=[int(a[':answer/value']) for a in SOURCES[source][':question/answer-fields'][0][':answer-field/choices']]
        elif level=='moderate':
            values=list(range(5)) if profile=='zero-through4' else list(range(1,6))
        else:
            candidates=bank_candidates(p,profile,p['n']-p['k'])
            if bank_anchor is not None:candidates=[c for c in candidates if c[0]==bank_anchor]
            if bank_scale is not None:candidates=[c for c in candidates if c[1]==bank_scale]
            if not candidates:raise ValueError('no compatible bank translation')
            anchor,scale,values,_=r.choice(candidates)
    if not valid(level,p,profile):raise ValueError('parameter/profile constraint')
    problem,solution,answer=render(level,p,template)
    values=sorted(values);content={'level':level,'problem':problem,'solution':solution,'values':values,'correct':answer}
    uid=ident(digest(content));fid=ident(uid+'/selection')
    choices=[{':answer/id':ident(fid+'/'+str(x)),':answer/type':':answer.type/math',':answer/value':normalize_tex(str(x))} for x in values]
    correct=next(a[':answer/id'] for a in choices if int(a[':answer/value'])==answer)
    q={':question/id':uid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    task=['easy',p['n'],p['k']] if level=='easy' else ['moderate',[[str(x) for x in row] for row in sp.Matrix(p['matrix']).T.rref()[0].tolist()]]
    return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'bank_anchor':anchor,'bank_scale':scale,'source_replay':source,'bank_recipe':'exact source bank' if source and p==ORIGINAL[source] and profile==SOURCE_PROFILE[source] else 'translated source shape; qualifying value independently assigned' if level=='easy' else 'observed consecutive bank','correct_value':str(answer),'mathematical_fingerprint':digest(task),'content_fingerprint':digest(content),'source_question_ids':[s for s in SOURCES if SOURCE_PROFILE[s]==profile], 'source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':'none','domain':'real vector spaces; full column rank parameter coefficient matrix'}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def markdown(rec):return rec['question'][':question/problem']+'\n\n'+rec['question'][':question/worked-solution']
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--template');parser.add_argument('--profile');a=parser.parse_args()
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
