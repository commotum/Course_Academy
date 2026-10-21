#!/usr/bin/env python3
"""One-pivot singular 3x3 systems. Runtime uses only the Python standard library."""
import argparse
from copy import deepcopy
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import matrix_tex, system_tex, normalize_prose, normalize_tex, checked_math_content

KP = {'db/id':17592186096746, 'id':'aa91091b-5368-5d80-b87d-08b3524177f3', 'title':'Finding the Reduced Row Echelon Form of a Singular 3x3 System With One Pivot'}
VERSION='1.0.0'
SIGNS=list(itertools.product((-1,1),repeat=3))

def uid(*parts):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(parts,sort_keys=True)))

def tex_number(n):
    n=F(n)
    if n.denominator==1:return str(n.numerator)
    return ('-' if n<0 else '')+r'\frac{'+str(abs(n.numerator))+'}{'+str(n.denominator)+'}'

def linear(terms):
    out=''
    for value,var in terms:
        value=F(value)
        if not value:continue
        term=('' if abs(value)==1 and var else tex_number(abs(value)))+var
        out+=('-' if value<0 else '+' if out else '')+term
    return out or '0'

def eq(row):
    return linear(zip(row[:3],('x','y','z')))+'='+tex_number(row[3])

def mat(rows,augmented=True):
    return matrix_tex([[tex_number(x) for x in row] for row in rows],augmented=augmented)

def display(t):return '\n\n$$\n'+t+'\n$$\n\n'

def poly(d=0,y=0,z=0):return (F(d),F(y),F(z))
Y=poly(y=1); Z=poly(z=1)

def vector(entries):
    return matrix_tex([[linear(zip(p,('', 'y','z')))] for p in entries])+r',\,y,z\in(-\infty,\infty)'

def rankrow(b,c,d):return [[1,b,c,d],[0]*4,[0]*4]

def identity(a,b,c):return [[1,0,0,a],[0,1,0,b],[0,0,1,c]]

def easy_source_bank(p):
    b,c,d=p['b'],p['c'],p['d']; s=p['scales']; r=rankrow(b,c,d)
    def two(top,row):return [top,row,[0]*4]
    rr=r[0]
    banks={
    'q-74536':([identity(d,0,0),two([1,b,0,d],[0,0,1,0]),r,two(rr,[0,0,0,1]),two([1,0,c,d],[0,1,0,0])],2),
    'q-74606':([two(rr,[0,0,1,0]),two([1,-b,c,0],[0,1,0,0]),rankrow(b,c,0),identity(d,b,-s[1]),r],4),
    'q-74608':([two([1,b,c,0],[0,0,0,d]),two([1,b,2*c,d],[0,1,0,0]),two(rr,[0,0,1,0]),identity(d,-b,-2*c),r],4),
    'q-74612':([two(rr,[0,0,1,0]),[rr,[0,0,0,s[1]*d],[0,0,0,s[2]*d]],identity(d,s[1]*d,s[2]*d),rankrow(b,c,0),r],4),
    'q-131647':([r,rankrow(-b,-c,-d),two([1,0,c,d],[0,1,0,-b]),rankrow(-b,-c,d),identity(d,-b,-s[0])],0),
    'q-74610':([identity(d,b,c),rankrow(b,c,0),two([1,b,c,b],[0,0,0,F(b,2)]),two(rr,[0,0,1,0]),r],4),
    'q-131648':([[[1,0,0,d],[0,1,1,-F(d,2)],[0,0,1,-c]],rankrow(-b,-c,d),rankrow(-b,-c,-d),r,two([1,0,c,d],[0,1,1,-F(d,2)])],3),
    'q-131638':([rankrow(-b,-c,-d),identity(d,-d,-c),rankrow(-b,-c,d),two([1,0,c,d],[0,1,0,-d]),r],4),
    }
    return banks[p['profile']]

def moderate_source_bank(p):
    b,c,d=p['b'],p['c'],p['d']; s=p['scales']; k=poly(d,-b,-c)
    def v(a,y=Y,z=Z):return (a,y,z)
    banks={
    'q-131651':([v(poly(-d,-b,-c)),v(poly(-d,b,c)),v(poly(d,b,-c)),v(k),None],3),
    'q-74613':([v(k),v(poly(d,b,c),poly(y=b)),v(poly(-d,b,1),Y,poly(z=s[2])),v(poly(d,-b,c)),v(poly(-d,b,1))],0),
    'q-74615':([v(k),v(k,poly(d,-b),poly(d,0,-c)),v(poly(d,b,c),Y,poly(d,0,c)),v(k,poly(d,-b)),v(poly(d,b,c))],0),
    'q-131650':([v(poly(d+1,-b-1,-c+1)),None,v(poly(-d,-b,c)),v(k),v(poly(-d,b,c))],3),
    'q-74616':([v(poly(d,b,c),Y,poly(s[2]*d,0,-1)),v(k,poly(s[1]*d,-1)),v(k),v(poly(d,b,-c)),v(k,poly(s[1]*d,-1),poly(s[2]*d,0,-1))],2),
    'q-131649':([v(poly(-d,-b,c)),None,v(poly(-d,b,c)),v(k),v(poly(d+1,-b,-c))],3),
    'q-74534':([v(poly(d,0,-c),poly(d,0,-b)),v(k),None,v(poly(d,-1,2)),v(poly(d,0,-c),poly(z=-b))],1),
    }
    return banks[p['profile']]

def operation_trace(p):
    b,c,d=p['b'],p['c'],p['d']
    a=[[F(t)*v for v in (1,b,c,d)] for t in p['scales']]
    trace=[{'matrix':deepcopy(a),'operation':None}]
    def add(op):trace.append({'matrix':deepcopy(a),'operation':op})
    if p['plan'].startswith('swap'):
        j=int(p['plan'][-1])-1
        a[0],a[j]=a[j],a[0]; add(r'R_1\leftrightarrow R_'+str(j+1))
    if a[0][0]!=1:
        factor=1/a[0][0]; a[0]=[factor*x for x in a[0]]
        add(r'R_1:='+('('+tex_number(factor)+')')+r'R_1')
    for j in (1,2):
        factor=-a[j][0]; a[j]=[x+factor*y for x,y in zip(a[j],a[0])]
        add('R_'+str(j+1)+':=R_'+str(j+1)+'+('+tex_number(factor)+')R_1')
    return trace

def solution(p):
    b,c,d=p['b'],p['c'],p['d']; trace=operation_trace(p)
    out='The augmented matrix for this system is'+display('M='+mat(trace[0]['matrix'])+'.')
    out+='Transforming $M$ to reduced row echelon form, we have'
    # Put the operation above the resulting matrix so extrema fit the study pane.
    for state in trace[1:]:
        out+=display(state['operation'])
        out+=display(r'M\sim '+mat(state['matrix'])+'.')
    if p['difficulty']=='easy':return out
    out+='The corresponding system is now'+display(system_tex([eq([1,b,c,d]),'0x+0y+0z=0','0x+0y+0z=0'])+'.')
    out+='Since any numbers $x,y,z$ form a solution of the final two equations, we can remove these equations from the system.\n\n'
    out+='The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x$, and we have two free variables, $y$ and $z$. That means we need to find $x$ in terms of $y$ and $z$.'
    isolated=linear(zip((d,-b,-c),('','y','z')))
    out+='\n\nTherefore, the general solution is'+display(system_tex(['x='+isolated,'y=y','z=z'])+',')
    out+='where $y$ and $z$ (the free variables) are arbitrary numbers.\n\nIn vector form, the solution can be written as'+display(matrix_tex([['x'],['y'],['z']])+'='+vector((poly(d,-b,-c),Y,Z))+'.')
    return out

@checked_math_content
def build(p, bank=None, correct_index=None, source_replay=False):
    p=deepcopy(p); band=p['difficulty']
    rows=[[scale*v for v in (1,p['b'],p['c'],p['d'])] for scale in p['scales']]
    problem='Consider the following system of linear equations:'+display(system_tex([eq(row) for row in rows]))
    problem+='Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form'
    problem+=('.' if band=='easy' else ', and then solve the linear system.')
    if bank is None:
        bank,correct_index=(easy_source_bank(p) if band=='easy' else moderate_source_bank(p))
    values=[('No solution' if item is None else mat(item,False) if band=='easy' else vector(item)) for item in bank]
    problem=normalize_prose(problem); worked=normalize_prose(solution(p))
    values=[normalize_tex(v) if item is not None else v for v,item in zip(values,bank)]
    qid=uid(VERSION,band,problem,values)
    fid=uid(qid,'selection')
    answers=[{':answer/id':uid(fid,i,value),':answer/type':':answer.type/text' if item is None else ':answer.type/math',':answer/value':value} for i,(value,item) in enumerate(zip(values,bank))]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct_index][':answer/id']]}
    question={':question/id':qid,':question/problem':problem,':question/worked-solution':worked,':question/answer-fields':[field]}
    if band!='unclassified': question[':question/difficulty']=':question.difficulty/'+band
    return {'knowledge_point':KP,'question':question,'generation':{'generator_version':VERSION,'template':'rref' if band=='easy' else 'solve','profile':p['profile'],'parameters':p,'source_replay':source_replay,'source_references':[p['source_id']] if source_replay else ['8de46974-719c-5ac2-a43c-83d1c67c57b6','88a095c1-7277-5941-89d0-b1e503b7ab22' if band=='easy' else 'a5bda611-2864-532a-b9d9-e426378f7835']}}

def authored(p,sign_bank,correct_index):
    magnitudes=[abs(p[k]) for k in ('b','c','d')]
    triples=[[s*m for s,m in zip(signs,magnitudes)] for signs in sign_bank]
    p=deepcopy(p); p.update(zip(('b','c','d'),triples[correct_index]))
    bank=[rankrow(*v) if p['difficulty']=='easy' else (poly(v[2],-v[0],-v[1]),Y,Z) for v in triples]
    return build(p,bank,correct_index)

def sample_parameters(rng,difficulty):
    # Assignment of answer-bearing signs and bank member precedes numerical values.
    sign_bank=rng.sample(SIGNS,5); correct_index=rng.randrange(5)
    p=dict(profile='authored-sign-comparison',difficulty=difficulty,b=rng.randint(1,10),c=rng.randint(1,10),d=rng.randint(1,18))
    plan=rng.choice(('positive','negative','swap2','swap3'))
    scales=[rng.choice((-1,1))*rng.randint(2,10) for _ in range(3)]
    if plan in ('positive','negative'):
        scales[0]=(1 if plan=='positive' else -1)*rng.randint(1,10); p['plan']='normalize'
    else:
        scales[int(plan[-1])-1]=1; p['plan']=plan
    p['scales']=scales
    return p,sign_bank,correct_index

def generate(difficulty,count,seed):
    if difficulty=='unclassified':difficulty='easy'
    if difficulty not in ('easy','moderate'):raise ValueError('Supported bands: easy, moderate; hard has no source evidence')
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed); records=[]; seen=set(); attempts=0
    while len(records)<count:
        attempts+=1
        if attempts>max(100,100*count):raise RuntimeError('Unable to sample distinct prompts')
        p,bank,index=sample_parameters(rng,difficulty)
        record=authored(p,bank,index)
        # Dedupe mathematical prompt instances, independent of choice ordering and IDs.
        identity=tuple(record['generation']['parameters'][k] if k!='scales' else tuple(record['generation']['parameters'][k]) for k in ('b','c','d','scales'))
        if identity in seen:continue
        seen.add(identity)
        record['generation'].update(seed=seed,draw=attempts,rejections=attempts-len(records)-1,sign_bank=[list(s) for s in bank],correct_index=index)
        records.append(record)
    return records

def replay():
    parameters=json.loads(Path(__file__).with_name('source_parameters.json').read_text())
    return [build(p,source_replay=True) for p in parameters]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',default='easy',choices=['easy','moderate','hard','unclassified'])
    parser.add_argument('--count',type=int,default=5)
    parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    parser.add_argument('--replay-sources',action='store_true')
    a=parser.parse_args()
    try:records=replay() if a.replay_sources else generate(a.difficulty,a.count,a.seed)
    except ValueError as error:parser.error(str(error))
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
