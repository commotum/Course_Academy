#!/usr/bin/env python3
"""Relocatable, seeded matrix-associativity practice; no database operations."""
import argparse
import copy
import hashlib
import json
import random
import re
import uuid
from pathlib import Path
from math_format import matrix_tex, matrix_operands, matrix_answer, normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id':17592186115227,'id':'8feeacff-b07d-5f98-a765-4d8571674a7a','title':'Calculating a Matrix Product Using the Associative Law'}
LEVELS = ('easy','moderate','hard')
PROFILES = {'easy':['scalar-AB','row-AB','scalar-BC','row-BC'], 'moderate':['outer-AB','rect-BC','outer-BC','rect-AB'], 'hard':['diagonal-AB','diagonal-BC']}
SOURCES = {'scalar':'34cd5f5a-f82e-5ae5-899e-5e1bd32cf8b9','row':'7d60a4e0-4fdb-56f1-b62d-65e7bbd5fd84','outer':'25db1a97-9ec4-5a92-aa5c-6915402afa8c','rect':'ccf609af-63ab-558e-b2d1-560aae618250','diagonal':'4de9405f-1520-54e1-92d3-e7ba15edacd2; tutorial 31c195bb-9066-55bf-ae02-9de81da2b7bb'}

def mul(a,b):
    assert len(a[0]) == len(b)
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def transpose(a): return [list(row) for row in zip(*a)]
def reverse_transpose(p): return {k:transpose(p[l]) for k,l in zip('ABC','CBA')}
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(namespace,label): return str(uuid.uuid5(uuid.UUID(namespace),label))
def display(tex): return '\n\n$$\n'+tex+'\n$$\n\n'
def dot_entries(a,b):
    return [[ '+'.join('('+str(a[i][k])+r')\cdot('+str(b[k][j])+')' for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def calculation(label,a,b):
    # Full numeric matrices, with one illustrative row-column calculation.
    short=label.split('=')[0]
    result=mul(a,b)
    illustration=display(r'\begin{aligned}('+short+r')_{1,1} &='+dot_entries(a,b)[0][0]+r' \\ &='+str(result[0][0])+r'\end{aligned}')
    prefix=(short+' &='+label.split('=',1)[1]+r' \\ &=' if '=' in label else short+' &=')
    return 'For example, the first entry is'+illustration+'The complete product is'+display(r'\begin{aligned}'+prefix+matrix_tex(a)+r'\cdot '+matrix_tex(b)+r' \\ &='+matrix_tex(result)+r'\end{aligned}')

def make_record(band,p,side,profile,seed=0,source=None,radio_bank=None,source_correct=None):
    A,B,C=[p[k] for k in 'ABC'];AB=mul(A,B);BC=mul(B,C);result=mul(AB,C)
    prompt='Calculate $ABC$, where\n\n'+matrix_operands([k+'='+matrix_tex(p[k]) for k in 'ABC'])
    solution='The associative law changes the grouping while preserving factor order:'+display('ABC=(AB)C=A(BC).')
    if profile.startswith('diagonal'):
        solution+='All three factors are $3\\times3$, so intermediate dimensions do not distinguish the groupings. '
        solution+='Computing $'+side+'$ exposes cancellation. '+calculation(side,A,B) if side=='AB' else 'Computing $BC$ exposes cancellation. '+calculation('BC',B,C)
        solution+=('The diagonal intermediate multiplies the rows of $C$.' if side=='AB' else 'The diagonal intermediate multiplies the columns of $A$.')
    else:
        solution+='The intermediate $AB$ is $'+str(len(A))+r'\times'+str(len(B[0]))+'$; $BC$ is $'+str(len(B))+r'\times'+str(len(C[0]))+'$. '
        solution+='Compute $'+side+'$ first. '+ (calculation('AB',A,B) if side=='AB' else calculation('BC',B,C))
    solution+=' Now complete the product. '+ (calculation('ABC=(AB)C',AB,C) if side=='AB' else calculation('ABC=A(BC)',A,BC))
    if radio_bank is None:
        prompt+='\n\nEnter the entries of the product.\n\n'+matrix_answer('ABC', [['{{field-'+str(i*len(result[0])+j+1)+'}}' for j in range(len(result[0]))] for i in range(len(result))])
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    # Content identity includes the response contract and complete bank, after normalization.
    bank=[normalize_tex(v) for v in radio_bank] if radio_bank else [str(v) for row in result for v in row]
    qid=uid(KP['id'],digest({'prompt':prompt,'bank':bank}))
    fields=[]
    for i,values in enumerate([bank] if radio_bank is not None else [[v] for v in bank]):
        key='selection' if radio_bank is not None else 'field-'+str(i+1);fid=uid(qid,key)
        choices=[{':answer/id':uid(fid,str(j)+':'+v),':answer/type':':answer.type/math',':answer/value':v} for j,v in enumerate(values)]
        correct=source_correct if radio_bank is not None else 0
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('radio' if radio_bank is not None else 'blank'),':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[correct][':answer/id']]})
    r={'knowledge_point':KP.copy(),'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+band,':question/answer-fields':fields},'generation':{'version':'associative-matrices-2.0.0','seed':seed,'profile':profile,'grouping':side,'parameters':p,'source_question':source or SOURCES[profile.split('-')[0]],'source_basis':8210,'assets':{},'semantic_fingerprint':digest(p)}}
    return validate_generated_record(r)

def sample(rng,profile):
    family,side=profile.split('-')
    def matrix(m,n): return [[rng.randint(-3,3) for _ in range(n)] for _ in range(m)]
    if family=='diagonal':
        # U and V are an integral inverse pair. Conjugating varies cancellation
        # coordinates; independent diagonal assignments change surviving rows/columns.
        U=[[1,1,1],[1,2,2],[1,2,3]];V=[[2,-1,0],[-1,2,-1],[0,-1,1]]
        order=rng.sample(range(3),3);sign=[rng.choice([-1,1]) for _ in range(3)]
        T=[[int(order[i]==j)*sign[i] for j in range(3)] for i in range(3)]
        Ti=transpose(T);U=mul(mul(T,U),Ti);V=mul(mul(T,V),Ti)
        d=[rng.choice([-2,-1,1,2]) for _ in range(3)]
        if rng.randrange(4)==0:d[rng.randrange(3)]=0
        D=[[d[i] if i==j else 0 for j in range(3)] for i in range(3)]
        if side=='BC':p={'A':matrix(3,3),'B':U,'C':mul(V,D)}
        else:p={'A':mul(D,V),'B':U,'C':matrix(3,3)}
        return p
    dims={'scalar':[(1,2),(2,1),(1,3)],'row':[(1,2),(2,2),(2,2)],'outer':[(2,3),(3,1),(1,2)],'rect':[(3,2),(2,3),(3,1)]}[family]
    p={k:matrix(m,n) for k,(m,n) in zip('ABC',dims)}
    if side!=('BC' if family=='rect' else 'AB'):p=reverse_transpose(p)
    return p

def generate(band,seed=0,profile=None,parameters=None):
    if band not in LEVELS:raise ValueError('Unknown difficulty')
    rng=random.Random(seed);profile=profile or rng.choice(PROFILES[band])
    if profile not in PROFILES[band]:raise ValueError('Profile does not belong to this band')
    p=copy.deepcopy(parameters) if parameters is not None else sample(rng,profile)
    return make_record(band,p,profile.split('-')[1],profile,seed)

def fresh(band,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);out=[];seen=set()
    while len(out)<count:
        profiles=PROFILES[band].copy();rng.shuffle(profiles)
        for profile in profiles:
            for _ in range(100):
                r=generate(band,rng.getrandbits(64),profile);fp=r['generation']['semantic_fingerprint']
                # Entirely zero factors eliminate the assessed operation. Internal
                # cancellation and zero result entries remain valid and eligible.
                if fp not in seen and all(any(v for row in m for v in row) for m in r['generation']['parameters'].values()):break
            else:raise RuntimeError('Unable to construct a fresh nonvacuous product')
            out.append(r);seen.add(fp)
            if len(out)==count:break
    return out

def source_replay(name):
    q=next(q for q in json.loads(Path(__file__).with_name('source-cases.json').read_text()) if q[':question/math-academy-id']==name)
    bodies=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)
    p={k:[[int(c.strip()) for c in row.split('&')] for row in re.split(r'\\\\',body)] for k,body in zip('ABC',bodies)}
    side='AB' if 'product $AB$' in q[':question/worked-solution'] else 'BC'
    f=q[':question/answer-fields'][0];radio=f[':answer-field/type'][':db/ident'].endswith('/radio')
    values=[a[':answer/value'] for a in f[':answer-field/choices']] if radio else None
    correct=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id']) if radio else None
    return make_record(q[':question/difficulty'][':db/ident'].split('/')[-1],p,side,'source-replay',source=q[':question/id'],radio_bank=values,source_correct=correct)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=LEVELS,required=True);parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json');parser.add_argument('--source-case')
    a=parser.parse_args();records=[source_replay(a.source_case)] if a.source_case else fresh(a.difficulty,a.count,a.seed)
    print(json.dumps(records,indent=2))
if __name__=='__main__':main()
