"""Independent Gaussian elimination with a zero second pivot; offline runtime."""
import sys
sys.dont_write_bytecode = True
import argparse
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random
import uuid
from math_format import matrix_tex, system_tex, normalize_prose, normalize_tex, checked_math_content

KP = 17592186096673
VERSION = '1.1.0'
BANDS = ('easy', 'moderate', 'hard')
FAMILIES = ('equations-solve', 'matrix-solve', 'equations-echelon', 'matrix-echelon')
REFS = ['e-4702', 'q-73396', 'q-73397', 'tutorial 3156 / 17592186097842']

def tex(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ('-' if x < 0 else '') + r'\frac{' + str(abs(x.numerator)) + '}{' + str(x.denominator) + '}'

def matrix(rows):
    return matrix_tex([[tex(v) for v in row] for row in rows], augmented=True)

def display(s):
    return '\n\n$$\n' + s + '\n$$\n\n'

def equation(row):
    terms = []
    for a, name in zip(row[:3], 'xyz'):
        a = F(a)
        if not a:
            continue
        body = ('' if abs(a) == 1 else tex(abs(a))) + name
        terms.append(('-' if a < 0 else ('+' if terms else '')) + body)
    return ''.join(terms) + ' &=' + tex(row[3])

def uid(value):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy:17592186096673:' + value))

def initial(first, tail, p, beta, gamma, q, s):
    u,v,w = tail
    return [[p*a for a in first],
            [beta*a + e for a,e in zip(first,[0,0,s,s*w])],
            [gamma*a + e for a,e in zip(first,[0,q,q*u,q*v])]]

def bank(rng,band,q,s):
    # Two last-coordinate values, each repeated, prevent z alone from selecting
    # a complete endpoint. Distinct (y,z) pairs ensure no row-equivalent options.
    extent=3 if band=='easy' else (4 if band=='moderate' else 5)
    wa,wb=rng.sample(range(-extent,extent+1),2)
    ws=[wa,wa,wa,wb,wb];rng.shuffle(ws)
    tails=[];solutions=set()
    for wn in ws:
        w=F(wn,s) if band=='hard' else F(wn)
        while True:
            if band=='easy':u,v=F(rng.randint(-1,1)),F(rng.randint(-3,3))
            elif band=='moderate':u,v=F(rng.randint(-2,2)),F(rng.randint(-5,5))
            else:u,v=F(rng.randint(-5,5),q),F(rng.randint(-5,5),q)
            yz=(v-u*w,w)
            if yz not in solutions:break
        solutions.add(yz);tails.append((u,v,w))
    return tails

def draw(rng, band, family=None):
    family = family or rng.choice(FAMILIES)
    if band == 'easy':
        p=q=s=1
        beta=rng.choice([-1,1]); gamma=rng.choice([-1,0,1])
        b=rng.choice([-2,-1,1,2]); c=rng.randint(-1,1); d=rng.randint(-3,3)
        tails=bank(rng,band,q,s)
    elif band == 'moderate':
        p,q,s=[rng.choice([-3,-2,-1,1,2,3]) for _ in range(3)]
        beta=rng.choice([-2,-1,1,2]); gamma=rng.randint(-2,2)
        b=rng.choice([-3,-2,-1,1,2,3]); c=rng.randint(-2,2); d=rng.randint(-5,5)
        tails=bank(rng,band,q,s)
    else:
        p,q,s=[rng.choice([-3,-2,2,3]) for _ in range(3)]
        beta=rng.choice([-3,-2,-1,1,2,3]); gamma=rng.randint(-2,2)
        b=rng.choice([-3,-2,-1,1,2,3]); c=rng.randint(-2,2); d=rng.randint(-5,5)
        tails=bank(rng,band,q,s)
    # Every candidate has the same generative status. The key is assigned AFTER
    # the bank exists; no outlier, modal coordinate or offset singles it out.
    key=rng.randrange(5)
    return {'band':band,'family':family,'first':[F(1),F(b),F(c),F(d)],
            'tails':tails,'key':key,'p':p,'q':q,'s':s,'beta':beta,'gamma':gamma}

@checked_math_content
def generate(instance):
    i=instance; first=i['first']; u,v,w=i['tails'][i['key']]
    p,q,s,beta,gamma=[i[k] for k in ('p','q','s','beta','gamma')]
    M=initial(first,(u,v,w),p,beta,gamma,q,s)
    eq=i['family'].startswith('equations'); solve=i['family'].endswith('solve')
    given=('Consider the system of linear equations'+display(system_tex([equation(r) for r in M]))) if eq else ('Consider the augmented matrix $M$ for the variables $x,y,z$ in that order.'+display(matrix(M)))
    prompt=given+'Use the standard method of Gaussian elimination to reduce the augmented matrix to row echelon form'+(', and then solve the linear system. Select the solution $(x,y,z)$.' if solve else '. Select the resulting augmented matrix.')
    current=copy.deepcopy(M)
    solution='The augmented matrix is'+display(matrix(M))
    def step(label):
        nonlocal solution
        solution+=label+display(matrix(current))
    if p!=1:
        current[0]=[a/p for a in current[0]]
        step('Normalize the first pivot with $R_1:='+tex(F(1,p))+r'R_1$.')
    for j,k in [(1,beta),(2,gamma)]:
        if k:
            current[j]=[a-k*b for a,b in zip(current[j],current[0])]
            step('$R_'+str(j+1)+':=R_'+str(j+1)+'+('+tex(-k)+r')R_1$.')
    solution+='The second pivot is zero, while the third row has a nonzero second entry. Exchange $R_2$ and $R_3$.'
    current[1],current[2]=current[2],current[1]
    solution+=display(matrix(current))
    for j in (1,2):
        pivot=current[j][j]
        if pivot!=1:
            current[j]=[a/pivot for a in current[j]]
            step('Normalize with $R_'+str(j+1)+':='+tex(1/pivot)+'R_'+str(j+1)+'$.')
    U=[first,[F(0),F(1),u,v],[F(0),F(0),F(1),w]]
    assert current==U
    solution+='Thus the row echelon matrix is'+display(matrix(U))
    if solve:
        y=v-u*w; x=first[3]-first[1]*y-first[2]*w
        solution+='Back substitute, starting with the last row:'+display(r'\begin{aligned}z &='+tex(w)+r' \\ y &='+tex(v)+'-('+tex(u)+')('+tex(w)+')'+r' \\ &='+tex(y)+r' \\ x &='+tex(first[3])+'-('+tex(first[1])+')('+tex(y)+')'+r' \\ &\quad -('+tex(first[2])+')('+tex(w)+')'+r' \\ &='+tex(x)+r'\end{aligned}')
        solution+='The solution $(x,y,z)$ is'+display(r'\left('+','.join(tex(a) for a in (x,y,w))+r'\right)')
    vals=[]
    for a,b,c in i['tails']:
        if solve:
            y=b-a*c; x=first[3]-first[1]*y-first[2]*c
            vals.append(r'\left('+','.join(tex(t) for t in (x,y,c))+r'\right)')
        else:
            vals.append(matrix([first,[0,1,a,b],[0,0,1,c]]))
    prompt=normalize_prose(prompt); solution=normalize_prose(solution)
    vals=[normalize_tex(val) for val in vals]
    signature=hashlib.sha256(json.dumps([prompt,solution,vals,i['key']],sort_keys=True).encode()).hexdigest()
    choices=[{':answer/id':uid(signature+':answer:'+value),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
    field={':answer-field/id':uid(signature+':field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[i['key']][':answer/id']]}
    return {'knowledge_point':KP,'question':{':question/id':uid(signature),':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+i['band'],':question/answer-fields':[field]},
            'metadata':{'generator_version':VERSION,'family':i['family'],'bank':'authored-exchangeable-v1','source_refs':REFS,'observed_difficulty':None,'authored_difficulty':i['band'],'seed':i.get('seed'),'parameters':{'first_row':[str(a) for a in first],'tail':[str(a) for a in (u,v,w)],'pivot_scales':[p,q,s],'first_column_multipliers':[beta,gamma]},'domain':'x,y,z real; p,q,s nonzero; nonsingular 3-by-3 coefficient matrix'}}

def sample(band,count,seed):
    rng=random.Random(seed); out=[]; seen=set()
    while len(out)<count:
        instance=draw(rng,band)
        instance['seed']=seed
        M=initial(instance['first'],instance['tails'][instance['key']],*[instance[k] for k in ('p','beta','gamma','q','s')])
        # Reject repeated main calculations, irrespective of endpoint/input form.
        signature=tuple(tuple(r) for r in M)
        if signature in seen:
            continue
        seen.add(signature); out.append(generate(instance))
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=(*BANDS,'unclassified'),default='moderate')
    p.add_argument('--count',type=int,default=5); p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json'],default='json')
    p.add_argument('--replay',help='Replay a complete retained eligible source bank by Math Academy ID')
    a=p.parse_args()
    if a.count<1: p.error('--count must be positive')
    if a.replay:
        sources=json.loads((Path(__file__).parent/'source-replay.json').read_text())
        if a.replay not in sources: p.error('Unknown source ID')
        records=[sources[a.replay]]
    else:
        records=sample('moderate' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
