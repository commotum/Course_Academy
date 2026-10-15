#!/usr/bin/env python3
"""Rank/nullity from column-space bases or parametrized null spaces.

Observed easy/moderate workloads only. No hard sampler. See the sibling package
for source replay, complete bank profiles, bounded domains and validation.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, sys, uuid
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
try:
    import sympy as sp
except ModuleNotFoundError as error:
    # The application invokes registered CLIs with /usr/bin/python3; use the
    # project's installed mathematical runtime without changing the application.
    runtime=REPO/'.venv/bin/python'
    if error.name!='sympy' or __name__!='__main__' or not runtime.is_file() or Path(sys.executable).resolve()==runtime.resolve():
        raise
    os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
sys.path.insert(0,str(REPO/'scripts/question_capture'))
from math_format import checked_math_content, matrix_tex, normalize_prose, normalize_tex
PACKAGE=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((PACKAGE/'reference/source.json').read_text())
KP=SNAPSHOT['record']; KP_ID=17592186184171
NAMESPACE=uuid.UUID(KP[':knowledge-point/id'])
GENERATOR_UUID=str(uuid.uuid5(NAMESPACE,'question-generator'))
VERSION='rank-nullity-description-v1'
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
 'q-139982':{'matrix':[[1,0,0],[0,-1,0],[0,1,1],[0,1,0]],'indices':[1,2,3]}}
SOURCE_PROFILE={'q-35305':'small','q-35433':'small','q-141230':'small','q-142487':'offset-minus1','q-142485':'offset-minus2','q-141232':'dimensions','q-35306':'one-through5','q-142486':'zero-through4','q-35434':'one-through5','q-79352':'zero-through4','q-139982':'zero-through4'}
PROFILES={'easy':('small','offset-minus1','offset-minus2','dimensions'),'moderate':('zero-through4','one-through5')}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(x):return str(uuid.uuid5(NAMESPACE,x))
def bank(profile,p,correct):
    if profile in ('small','zero-through4'):return list(range(5))
    if profile=='one-through5':return list(range(1,6))
    if profile=='offset-minus1':return [correct+i for i in (-1,0,1,2,3)]
    if profile=='offset-minus2':return [correct+i for i in (-2,0,1,2,3)]
    if profile=='dimensions':return [0,p['n']-2*p['k'],p['k'],correct,p['n']]
    raise ValueError('unsupported bank profile')

def valid(level,p,profile):
    if level=='easy':
        if set(p)!={'m','n','k'} or any(type(x)is not int for x in p.values()):return False
        if not(2<=p['m']<=7 and 4<=p['n']<=12 and 1<=p['k']<=min(p['m'],p['n']-1)):return False
        correct=p['n']-p['k']
    else:
        if set(p)!={'matrix','indices'}:return False
        m=p['matrix'];ind=p['indices']
        if len(m)!=4 or len(ind) not in (2,3) or ind not in ([2,3],[1,2,3]):return False
        if any(len(row)!=len(ind) or any(type(v)is not int or abs(v)>3 for v in row) for row in m):return False
        if sp.Matrix(m).rank()!=len(ind):return False
        correct=4-len(ind)
    values=bank(profile,p,correct)
    return len(set(values))==5 and min(values)>=0 and correct in values

def sample(level,r,profile):
    for _ in range(10000):
        if level=='easy':
            m=r.randint(2,7);n=r.randint(4,12);p={'m':m,'n':n,'k':r.randint(1,min(m,n-1))}
        else:
            indices=r.choice([[2,3],[1,2,3]])
            p={'matrix':[[r.randint(-3,3) if r.random()<.65 else 0 for _ in indices] for _ in range(4)],'indices':indices}
        if valid(level,p,profile):return p
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
        solution=intro+f'For the given matrix, we have $n={n},$ and since $B$ is formed by ${k}$ vectors, $\\text{{rank}}(A)={k}.$ Therefore,\n\n$$\n'+r'\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ '+f'{k}+'+r'\text{nullity}(A) & ='+f'{n}'+r' \\ \text{nullity}(A) & ='+f'{n}-{k}'+r' \\ \text{dim(Null}(A)) & ='+f'{answer}.'+r'\end{aligned}'+'\n$$'
    else:
        C=sp.Matrix(p['matrix']);n=C.rows;k=C.cols;answer=n-k
        indices=p['indices'];vector=matrix_tex([[expr(row,indices)] for row in p['matrix']]);variables=','.join(f'{{x}}_{{{i}}}' for i in indices)
        space=r'\text{Null}(A)=\{'+vector+r'\,|\,\,'+variables+r'\in R\}'
        problem=('Find $'+r'\text{rank}(A)'+'$ given that\n\n$$\n'+space+'.\n$$') if template=='null-space-display' else 'Find $'+r'\text{rank}(A)'+'$ given that $'+space+'.$'
        expanded='+'.join(f'{{x}}_{{{indices[j]}}}'+matrix_tex([[C[i,j]] for i in range(n)]) for j in range(k))
        solution=intro+f'For the given matrix, we have $n={n},$ since this is the number of components in each of the vectors of the null space. \n\nAlso, since \n\n$$\n'+r'\text{Null}(A)=\{'+expanded+r'\,|\,\,'+variables+r'\in R\}'+'\n$$\n\n'+f'we conclude that $\\text{{nullity}}(A)={k}.$\n\nTherefore,\n\n$$\n'+r'\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ \text{rank}(A)+'+f'{k} & ={n}'+r' \\ \text{rank}(A) & ='+f'{n}-{k}'+r' \\  & ='+f'{answer}.'+r'\end{aligned}'+'\n$$'
    return normalize_prose(problem),normalize_prose(solution),answer

@checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty; hard has no validated source workload')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio required')
    r=random.Random(seed)
    if template in SOURCES:
        source=template
        template='column-basis' if level=='easy' else 'null-space-display' if source=='q-35434' else 'null-space-inline'
        profile=profile or SOURCE_PROFILE[source]
    else:source=None
    template=template or ('column-basis' if level=='easy' else r.choice(['null-space-inline','null-space-display']))
    if template not in (['column-basis'] if level=='easy' else ['null-space-inline','null-space-display']):raise ValueError('template/level mismatch')
    profile=profile or r.choice(PROFILES[level])
    if profile not in PROFILES[level]:raise ValueError('profile/level mismatch')
    p=json.loads(json.dumps(parameters)) if parameters is not None else sample(level,r,profile)
    if not valid(level,p,profile):raise ValueError('parameter/profile constraint')
    problem,solution,answer=render(level,p,template)
    values=sorted(bank(profile,p,answer));content={'level':level,'problem':problem,'solution':solution,'values':values,'correct':answer}
    uid=ident(digest(content));fid=ident(uid+'/selection')
    choices=[{':answer/id':ident(fid+'/'+str(x)),':answer/type':':answer.type/math',':answer/value':normalize_tex(str(x))} for x in values]
    correct=next(a[':answer/id'] for a in choices if int(a[':answer/value'])==answer)
    q={':question/id':uid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    task=['easy',p['n'],p['k']] if level=='easy' else ['moderate',[[str(x) for x in row] for row in sp.Matrix(p['matrix']).T.rref()[0].tolist()]]
    return {'knowledge_point':{'db_id':KP_ID,'id':str(NAMESPACE),'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'correct_value':str(answer),'mathematical_fingerprint':digest(task),'content_fingerprint':digest(content),'source_question_ids':[s for s in SOURCES if SOURCE_PROFILE[s]==profile], 'source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':'none','domain':'real vector spaces; full column rank parameter coefficient matrix'}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def markdown(rec):return rec['question'][':question/problem']+'\n\n'+rec['question'][':question/worked-solution']
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--template');parser.add_argument('--profile');a=parser.parse_args()
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
