"""Seeded distributive matrix products. No database, services, or runtime assets.
Parser and ordered factoring stages adapted from the supplied legacy entrypoint.
Fresh entry tasks avoid answer-bank cues; source banks are replayable separately.
"""
import argparse
import hashlib
import json
import random
import re
import uuid
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from math_format import matrix_answer, matrix_operands, matrix_tex, normalize_prose, normalize_tex, validate_generated_record
from matrix_product_prompt_policy import validate_delivery_batch
KP = {'db_id':17592186115226,'id':'a7ad52ce-d408-5390-b91f-c855274f39ea','title':'Calculating a Matrix Product Using the Distributive Law'}
NS = uuid.uuid5(uuid.UUID(KP['id']), 'distributive-entry-generator-v2')
RX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
PROFILES = {'easy':['scalar:0','scalar:1','scalar:-1','scalar:2'],
            'moderate':['scalar:2','scalar:-2','scalar:3','scalar:-3','sparse_combined','sparse_common'],
            'hard':['two_term']}
def scalar(text):
    text = normalize_tex(text)
    text = re.sub(r'\\text\{.*?\}', '',text)
    text = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',text)
    text = re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',text)
    return s.simplify(parse_expr(text,transformations=standard_transformations+(implicit_multiplication_application,)))
def matrices(text):
    return [s.Matrix([[scalar(x) for x in row.split('&')] for row in m[1].split(r'\\')]) for m in RX.finditer(normalize_prose(text))]
def tex(M): return matrix_tex([[s.latex(x) for x in row] for row in M.tolist()])
def display(text): return '\n\n$$\n'+text+'\n$$\n\n'
def parts(expr,env):
    a,op,b=re.fullmatch(r'([ABC]{2})([+-])([ABC]{2})',expr).groups()
    sign=1 if op=='+' else -1
    if a[0]==b[0]: common,u,v,side=a[0],a[1],b[1],'left'
    elif a[1]==b[1]:common,u,v,side=a[1],a[0],b[0],'right'
    else:raise ValueError('No shared matrix factor')
    inner=u+op+v
    fact=common+'('+inner+')' if side=='left' else '('+inner+')'+common
    D=env[u]+sign*env[v];F=env[common]
    R=F*D if side=='left' else D*F
    return common,inner,fact,side,D,F,R

def record(level,expr,env,targets,seed=0,profile='replay',choices=None,source_ids=None):
    common,inner,fact,side,D,F,R=parts(expr,env)
    problem='Calculate $'+expr+'$, where\n\n'+matrix_operands([name+'='+tex(env[name]) for name in 'ABC'],stacked=True)
    if choices is None:
        inverse={tuple(p):'field-'+str(i+1) for i,p in enumerate(targets)}
        rows=[['{{'+inverse[i,j]+'}}' if (i,j) in inverse else s.latex(R[i,j]) for j in range(3)] for i in range(3)]
        problem+='\n\nFill in the missing entries.\n\n'+matrix_answer(expr,rows)
    else:problem+='\n\nChoose the resulting matrix.'
    solution='Keep the common factor $'+common+'$ on the '+side+' and preserve the order of the '+('subtraction' if '-' in expr else 'addition')+':'+display(expr+'='+fact+'.')
    solution+='Combine corresponding entries first:'+display(inner+'='+tex(D)+'.')
    scalar_identity=all(D[i,j]==(D[0,0] if i==j else 0) for i in range(3) for j in range(3))
    if scalar_identity:
        k=D[0,0]
        if k==0:solution+='The combined matrix is zero, so the entire product is zero.'
        else:
            solution+='The combined matrix is $'+s.latex(k)+'I_3$. Multiply every entry of $'+common+'$ by $'+s.latex(k)+'$.'
    else:
        solution+='Use row-by-column multiplication on the shorter product $'+fact+'$.'
        # Explicitly instantiate each requested dot product; no CAS rewrite sets the pedagogy.
        lines=[]
        L,Q=(F,D) if side=='left' else (D,F)
        for i,j in targets:
            terms=[(L[i,k],Q[k,j]) for k in range(3) if L[i,k]!=0 and Q[k,j]!=0]
            calc='+'.join('('+s.latex(a)+')('+s.latex(b)+')' for a,b in terms) or '0'
            lines.append('('+expr+')_{'+str(i+1)+str(j+1)+'}&='+calc+'='+s.latex(R[i,j]))
        if lines:solution+=display(r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}')
    solution+=display(expr+'='+tex(R)+'.')
    # Normalize before content identities, as required by the shared publisher.
    problem,solution=normalize_prose(problem),normalize_prose(solution)
    values=[tex(M) for M in choices] if choices is not None else [s.latex(R[tuple(p)]) for p in targets]
    identity=json.dumps([level,problem,solution,values],sort_keys=True)
    qid=str(uuid.uuid5(NS,hashlib.sha256(identity.encode()).hexdigest()))
    fields=[]
    groups=[('selection',values)] if choices is not None else [('field-'+str(i+1),[v]) for i,v in enumerate(values)]
    for key,group in groups:
        fid=str(uuid.uuid5(uuid.UUID(qid),key))
        answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(i)+v)),':answer/type':':answer.type/math',':answer/value':normalize_tex(v)} for i,v in enumerate(group)]
        correct=choices.index(R) if choices is not None else 0
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if choices is not None else 'blank'),':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]})
    out={'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},
         'generation':{'version':3,'seed':seed,'profile':profile,'expression':expr,'side':side,'targets':[list(p) for p in targets],'matrices':{n:[[str(x) for x in row] for row in M.tolist()] for n,M in env.items()},'intermediate':[[str(x) for x in row] for row in D.tolist()],'source_ids':source_ids or []}}
    validate_delivery_batch([out],KP['db_id'])
    validate_generated_record(out)
    return out

def generate(difficulty='moderate',seed=0,profile=None):
    if difficulty not in PROFILES:raise ValueError('Unknown difficulty')
    rng=random.Random(seed);profile=profile or rng.choice(PROFILES[difficulty])
    if profile not in PROFILES[difficulty]:raise ValueError('Wrong profile for difficulty')
    # Choose mathematical roles before incidental values.
    side=rng.choice(['left','right']);sign=rng.choice([-1,1]);names=rng.sample(list('ABC'),3);common,u,v=names
    expr=common+u+('+' if sign==1 else '-')+common+v if side=='left' else u+common+('+' if sign==1 else '-')+v+common
    if profile.startswith('scalar:'):D=int(profile.split(':')[1])*s.eye(3)
    elif profile in ['sparse_combined','sparse_common']:
        D=s.zeros(3);D[rng.randrange(3),rng.randrange(3)]=rng.choice([-3,-2,-1,1,2,3])
    else:
        D=s.zeros(3);order=rng.sample(list(range(3)),3)
        for i in range(3):
            for j in [order[i],order[(i+1)%3]]:D[i,j]=rng.choice([-1,1])
    hard_anchor=(rng.randrange(3),rng.randrange(3)) if difficulty=='hard' else None
    F=s.Matrix(3,3,lambda i,j:rng.randint(-3,3))
    if hard_anchor is not None:
        # One requested cell must actually combine two nonzero products.
        # Signed equal contributions may still cancel: zero answers are valid.
        i,j=hard_anchor
        for k in range(3):
            if side=='left' and D[k,j]!=0 and F[i,k]==0:F[i,k]=rng.choice([-3,-2,-1,1,2,3])
            if side=='right' and D[i,k]!=0 and F[k,j]==0:F[k,j]=rng.choice([-3,-2,-1,1,2,3])
    if difficulty=='moderate':
        # Familiar radicals; exactly one radical per row keeps arithmetic controlled.
        for i in range(3):F[i,rng.randrange(3)]=rng.choice([-1,1])*s.sqrt(rng.choice([2,3,5]))
    if profile=='sparse_common':F,D=D,F
    U=s.Matrix(3,3,lambda i,j:rng.randint(-4,4));V=sign*(D-U)
    env={common:F,u:U,v:V}
    n=4 if difficulty=='hard' else 3
    coordinates=[(i,j) for i in range(3) for j in range(3)]
    if profile in ['sparse_combined','sparse_common']:
        # Assess routing as well as zero recognition: at least one requested cell
        # must lie in the structurally active output row/column. Values can cancel.
        L,Q=(F,D) if side=='left' else (D,F)
        active=[(i,j) for i,j in coordinates if any(L[i,k]!=0 and Q[k,j]!=0 for k in range(3))]
        anchor=rng.choice(active)
        targets=[anchor]+rng.sample([p for p in coordinates if p!=anchor],n-1)
        rng.shuffle(targets)
    elif hard_anchor is not None:
        targets=[hard_anchor]+rng.sample([p for p in coordinates if p!=hard_anchor],n-1)
        rng.shuffle(targets)
    else:targets=rng.sample(coordinates,n)
    return record(difficulty,expr,env,targets,seed,profile)

def batch(difficulty,count,seed):
    if count<0:raise ValueError('Count must be nonnegative')
    rng=random.Random(seed);out=[];seen=set();profiles=[]
    while len(out)<count:
        if not profiles:profiles=rng.sample(PROFILES[difficulty],len(PROFILES[difficulty]))
        profile=profiles.pop()
        for attempt in range(100):
            rec=generate(difficulty,rng.getrandbits(64),profile)
            qid=rec['question'][':question/id']
            if qid not in seen:break
        else:raise RuntimeError('Distinct instance sampling exhausted')
        out.append(rec);seen.add(qid)
    return out

def replay_source(q):
    expr=re.search(r'\$\s*([ABC]{2}\s*[+-]\s*[ABC]{2})',q[':question/problem'])[1].replace(' ','')
    env=dict(zip('ABC',matrices(q[':question/problem'])[:3]))
    level=q[':question/difficulty'][':db/ident'].split('/')[-1]
    fields=q[':question/answer-fields'];radio=fields[0][':answer-field/type'][':db/ident'].endswith('/radio')
    if radio:choices=[matrices('$'+normalize_tex(a[':answer/value'])+'$')[0] for a in fields[0][':answer-field/choices']];targets=[]
    else:
        choices=None;targets={}
        rows=[line for line in q[':question/problem'].splitlines() if line.startswith('|') and '---' not in line]
        for i,line in enumerate(rows):
            for j,cell in enumerate(line.split('|')[3:6]):
                if m:=re.search(r'\{\{field-(\d+)\}\}',cell):targets[int(m[1])]=(i,j)
        targets=[targets[i] for i in sorted(targets)]
    return record(level,expr,env,targets,profile='source-replay',choices=choices,source_ids=[q[':question/id']])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=list(PROFILES),default='moderate');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args();print(json.dumps(batch(args.difficulty,args.count,args.seed),indent=2))
