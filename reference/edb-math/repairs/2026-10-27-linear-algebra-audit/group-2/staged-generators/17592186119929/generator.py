#!/usr/bin/env python3
"""Seeded triangular determinant practice. No database, network or output assets."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import random
import re
import sympy as sp
import uuid
from math_format import matrix_tex, matrix_operands, normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id': 17592186119929, 'id': 'e84e45ca-c250-5e65-a04e-4714a485f38e', 'title': 'Finding the Determinant of a Triangular Matrix'}
VERSION = '1.1.0'
SUPPORT = {'rule': '46e747f7-564e-5827-b2a4-c7fb0456d174 properties II and III', 'matrix_operations': '205d32a2-ac26-5eaf-896a-c6182a70eff7', 'hard_exemplar': 'e943bc0b-58ab-5d24-9b76-ad39a0da742b'}
NS = uuid.UUID('eb8c35fc-e736-467d-80da-739965b89557')

def uid(s):
    return str(uuid.uuid5(NS, s))

def display(s):
    return '$$\n' + s + '\n$$'

def par(x):
    return '('+str(x)+')' if str(x).startswith('-') else str(x)

def product_line(m):
    return r'\cdot'.join(par(m[i][i]) for i in range(len(m)))

def exact(value):
    if isinstance(value, str):
        value = value.replace(' ', '')
        value = re.sub(r'\\sqrt\{(\d+)\}', r'*sqrt(\1)', value)
        value = value.lstrip('*').replace('-*', '-')
    return sp.sympify(value)

def value_tex(value):
    return sp.latex(sp.simplify(value)) if isinstance(value, sp.Basic) else str(value)

def diagonal(m):
    return [exact(m[i][i]) for i in range(len(m))]

def determinant(m):
    return math.prod(diagonal(m))

def transpose(m):
    return [list(r) for r in zip(*m)]

def combine(a,b,sign):
    return [[x+sign*y for x,y in zip(r,s)] for r,s in zip(a,b)]

def operand(name,t):
    return name + ('^T' if t else '')

def detexpr(name,t):
    return r'\det('+operand(name,t)+')'

def finalize(level,problem,solution,values,key,generation):
    # Normalize first: content ownership is based on served content, never a seed.
    problem,solution=map(normalize_prose,(problem,solution))
    values=[normalize_tex(value_tex(v)) for v in values]
    content=json.dumps([level,problem,solution,values,value_tex(key)],sort_keys=True)
    identity=hashlib.sha256(content.encode()).hexdigest()
    choices=[{':answer/id':uid(identity+'/answer/'+str(i)),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
    correct=next(c[':answer/id'] for c in choices if c[':answer/value']==normalize_tex(value_tex(key)))
    q={':question/id':uid(identity),':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':uid(identity+'/field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    return validate_generated_record({'knowledge_point':KP,'question':q,'generation':{'version':VERSION,**generation}})

def error_candidates(inst,a,b,target,key):
    """All values are outcomes of specific mistakes on this exact instance."""
    candidates=[]
    def add(name,value):
        if value != key and value not in [v for _,v in candidates]: candidates.append((name,value))
    add('lost overall sign',-key)
    add('uses a structural zero in the product',0)
    add('adds target diagonal entries',sum(diagonal(target)))
    anti=[target[i][-i-1] for i in range(len(target))]
    # A structural zero annihilates the product, even when other cells are TeX.
    add('multiplies anti-diagonal entries',0 if 0 in anti else math.prod(anti))
    for i in range(len(target)):
        add('omits diagonal factor '+str(i+1),math.prod(v for j,v in enumerate(diagonal(target)) if i!=j))
        add('uses diagonal entry '+str(i+1)+' alone',exact(target[i][i]))
        if inst['kind']!='combine':
            add('repeats diagonal factor '+str(i+1),key*exact(target[i][i]))
    add('adds diagonal magnitudes',sum(abs(v) for v in diagonal(target)))
    if inst['kind']=='identity':
        n=len(a);s=a[0][0]
        add('uses scalar only',s)
        add('uses dimension times scalar',n*s)
        add('uses one too few scalar factors',s**(n-1))
        add('uses one too many scalar factors',s**(n+1))
    if b is not None:
        x,y=determinant(a),determinant(b)
        if inst['kind']=='combine' and inst.get('reverse'):x,y=y,x
        add('uses first determinant only',x)
        add('uses second determinant only',y)
        add('multiplies determinants',x*y)
        if inst['kind']=='combine':
            add('reverses subtraction',-key)
            add('uses opposite outer operation',x-inst['sign']*y)
            add('loses second determinant sign',x+inst['sign']*abs(y))
        else:
            add('distributes determinant over matrix operation',x+inst['sign']*y)
            add('takes determinant after opposite matrix operation',determinant(combine(a,b,-inst['sign'])))
            for i in range(len(target)):
                d=diagonal(target);d[i]=a[i][i]
                add('omits second diagonal contribution '+str(i+1),math.prod(d))
    return candidates

def build(inst,rng,bank=None):
    level=inst['level'];kind=inst['kind'];a=inst['a'];b=inst.get('b');name=inst.get('name','T')
    if kind in ('triangular','identity'):
        target=a;key=determinant(a);expr=detexpr(name,False)
        if kind=='identity':
            s=a[0][0];n=len(a)
            problem=f'Given that ${name}={s}I$, where $I$ is the ${n}\\times {n}$ identity matrix, find ${expr}$.'
            solution='First write the scalar multiple of the identity matrix:\n\n'+display(name+'='+matrix_tex(a)+'.')+'\n\n'
        else:
            problem='Find the determinant of the matrix\n\n'+display(name+'='+matrix_tex(a)+'.')
            solution=''
        direction=inst.get('orientation','diagonal')
        description=direction+' triangular' if direction!='diagonal' else 'diagonal'
        solution+=f'The matrix ${name}$ is {description}. Its determinant is the product of the main diagonal entries:\n\n'+display(expr+'='+product_line(a)+'='+value_tex(key)+'.')
        stages=['identify triangular structure','locate diagonal','multiply diagonal entries']
        if kind=='identity':stages.insert(0,'expand scalar identity')
    else:
        ta,tb=inst['ta'],inst['tb'];sign=inst['sign'];op='+' if sign==1 else '-'
        left=transpose(a) if ta else a;right=transpose(b) if tb else b
        if kind=='combine':
            first,second=(('B',tb,b),('A',ta,a)) if inst.get('reverse') else (('A',ta,a),('B',tb,b))
            expr=detexpr(first[0],first[1])+op+detexpr(second[0],second[1])
            key=determinant(first[2])+sign*determinant(second[2]);target=a
            solution='Both matrices are triangular. Multiply their main diagonal entries:\n\n'+display(r'\begin{aligned}\det(A)&='+product_line(a)+'='+value_tex(determinant(a))+r',\\\det(B)&='+product_line(b)+'='+value_tex(determinant(b))+r'.\end{aligned}')
            solution+='\n\nTransposition preserves the determinant: $\\det(M^T)=\\det(M)$. Therefore,\n\n'+display(expr+'='+value_tex(determinant(first[2]))+op+par(determinant(second[2]))+'='+value_tex(key)+'.')
            stages=['identify both triangular matrices','multiply both diagonals','use transpose invariance','apply requested outer operation']
        else:
            inner=operand('A',ta)+op+operand('B',tb);expr=r'\det('+inner+')'
            target=combine(left,right,sign);key=determinant(target)
            solution='After transposition the operands have the same triangular direction. Combine corresponding entries before taking the determinant:\n\n'
            # Each operand is shown on its own row, then the combined matrix.
            solution+=display(r'\begin{aligned}'+operand('A',ta)+'&='+matrix_tex(left)+r',\\'+operand('B',tb)+'&='+matrix_tex(right)+r'.\end{aligned}')
            unevaluated=[[str(left[i][j])+op+par(right[i][j]) for j in range(len(a))] for i in range(len(a))]
            solution+='\n\n'+display(r'\begin{aligned}'+inner+'&='+matrix_tex(unevaluated)+r'\\&='+matrix_tex(target)+r'.\end{aligned}')
            solution+='\n\nThe resulting matrix is triangular, so multiply its main diagonal entries:\n\n'+display(expr+'='+product_line(target)+'='+value_tex(key)+'.')
            solution+='\n\nThe determinant rule applies to the combined matrix; determinants do not in general distribute over matrix addition or subtraction.'
            stages=['transpose specified operand','combine corresponding entries','recognize resulting triangular matrix','multiply resulting diagonal']
        problem='Consider the matrices $A$ and $B$ below. Find $'+expr+'$.\n\n'+matrix_operands(['A='+matrix_tex(a),'B='+matrix_tex(b)])
    errors=error_candidates(inst,a,b,target,key)
    if exact(key).has(sp.Pow) and not exact(key).is_Rational:
        # Keep several plausible radical outcomes, avoiding a uniquely radical key.
        errors=[(name,value) for name,value in errors if sp.simplify(value/key).is_Rational]
    if bank is None:
        if len(errors)<4:raise ValueError('Not enough distinct misconception outcomes')
        selected=rng.sample(errors,4)
        values=[key]+[v for _,v in selected];rng.shuffle(values)
    else:
        values=bank;selected=[]
    return finalize(level,problem,solution,values,key,{'template':kind,'instance':inst,'selected_errors':[{'recipe':n,'value':value_tex(v)} for n,v in selected], 'solution_path':{'target':expr,'final_expression':value_tex(key),'key':value_tex(key),'conversions':[],'shown_steps':stages,'support':SUPPORT}})

def triangular(rng,n,orientation,zero=False,identity=False):
    nonzero=[-3,-2,-1,1,2,3]
    d=[rng.choice(nonzero) for _ in range(n)]
    if identity:d=[rng.choice([-3,-2,2,3])]*n
    if zero:d[rng.randrange(n)]=0
    m=[[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        m[i][i]=d[i]
        for j in range(n):
            if (orientation=='upper' and i<j) or (orientation=='lower' and i>j):
                m[i][j]=rng.choice([-4,-2,-1,0,1,2,4,r'\sqrt{2}',r'\pi','0.5'])
    return m

def sample_instance(rng,level):
    if level=='easy':
        kind=rng.choice(['identity','triangular','triangular']);n=rng.choice([3,4]);o=rng.choice(['upper','lower']) if kind=='triangular' else 'diagonal'
        a=triangular(rng,n,o,zero=(kind!='identity' and rng.randrange(7)==0),identity=kind=='identity')
        if kind=='triangular' and rng.randrange(4)==0:
            i=rng.randrange(n)
            a[i][i]=r'\sqrt{'+str(rng.choice([2,3,5]))+'}'
        return {'level':level,'kind':kind,'orientation':o,'name':rng.choice(['T','D','E']), 'a':a}
    kind='combine' if level=='moderate' else 'matrix_combine'
    o=rng.choice(['upper','lower']);ta,tb=rng.choice([(True,False),(False,True),(True,True)]) if level=='moderate' else rng.choice([(True,False),(False,True)])
    # Hard uses integers off-diagonal so entrywise reconstruction stays routine.
    a=triangular(rng,3,o,zero=rng.randrange(9)==0);b=triangular(rng,3,o,zero=rng.randrange(9)==0)
    if kind=='matrix_combine':
        a=[[v if isinstance(v,int) else rng.choice([-2,1,3]) for v in row] for row in a]
        b=[[v if isinstance(v,int) else rng.choice([-2,1,3]) for v in row] for row in b]
        if ta:a=transpose(a)
        if tb:b=transpose(b)
    return {'level':level,'kind':kind,'orientation':o,'ta':ta,'tb':tb,'sign':rng.choice([-1,1]),'reverse':rng.choice([False,True]) if kind=='combine' else False,'a':a,'b':b}

def bank_cues(record):
    """Strategies using only the bank: used to reject a shared finite-batch cue."""
    f=record['question'][':question/answer-fields'][0]
    values=[exact(c[':answer/value']) for c in f[':answer-field/choices']]
    key=next(exact(c[':answer/value']) for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
    cues={'rank '+str(sorted(values).index(key)), 'position '+str(values.index(key))}
    for name,subset in [('unique positive',[v for v in values if v>0]),('unique negative',[v for v in values if v<0]),('minimum magnitude',[v for v in values if abs(v)==min(map(abs,values))]),('maximum magnitude',[v for v in values if abs(v)==max(map(abs,values))]),('positive opposite',[v for v in values if v>0 and -v in values]),('negative opposite',[v for v in values if v<0 and -v in values])]:
        if subset==[key]:cues.add(name)
    if key==0:cues.add('zero')
    return cues

def cue_groups(inst):
    kind=inst['kind']
    if kind=='identity':return [kind,kind+'/n='+str(len(inst['a']))]
    a=inst['a'];n=len(a)
    direction='upper' if all(a[i][j]==0 for i in range(n) for j in range(i)) else 'lower'
    return [kind,kind+'/'+direction]


def generate(level,count,seed):
    rng=random.Random(seed);result=[];seen=set();attempts=0;groups={};cue_rejections=0
    while len(result)<count:
        attempts+=1
        if attempts>count*200+200:raise RuntimeError('Unable to construct requested distinct batch')
        inst=sample_instance(rng,level)
        try:r=build(inst,rng)
        except ValueError as exc:
            if str(exc)=='Not enough distinct misconception outcomes':continue
            raise
        # Semantic identity excludes labels, order of choices and irrelevant entries.
        signature=json.dumps([inst['kind'],[value_tex(v) for v in diagonal(inst['a'])],[value_tex(v) for v in diagonal(inst['b'])] if 'b' in inst else None,inst.get('ta'),inst.get('tb'),inst.get('sign'),inst.get('reverse')])
        if signature in seen:continue
        cues=bank_cues(r);labels=cue_groups(inst)
        # Once a visible family has three items, no tested bank-only strategy
        # may answer every item. This is a batch rule, independent of seed.
        if any(label in groups and groups[label][0]>=2 and groups[label][1]&cues for label in labels):
            cue_rejections+=1
            continue
        for label in labels:
            n,shared=groups.get(label,(0,cues))
            groups[label]=(n+1,shared&cues)
        seen.add(signature);r['generation'].update({'seed':seed,'index':len(result),'attempt':attempts,'batch_cue_rejections':cue_rejections})
        result.append(r)
    return result

def replay_sources():
    result=[]
    for q in json.loads(Path(__file__).with_name('source-cases.json').read_text()):
        f=q[':question/answer-fields'][0];key=f[':answer-field/correct'][':answer/value']
        values=[c[':answer/value'] for c in f[':answer-field/choices']]
        level=q[':question/difficulty'][':db/ident'].split('/')[-1]
        result.append(finalize(level,q[':question/problem'],q[':question/worked-solution'],values,key,{'source_id':q[':question/id'],'template':'source_replay','source_replay':True}))
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='easy');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');p.add_argument('--replay-source',action='store_true');a=p.parse_args()
    if a.count<0:p.error('--count must be nonnegative')
    records=replay_sources() if a.replay_source else generate('easy' if a.difficulty=='unclassified' else a.difficulty,a.count,a.seed)
    print(json.dumps(records,ensure_ascii=False))
if __name__=='__main__':main()
