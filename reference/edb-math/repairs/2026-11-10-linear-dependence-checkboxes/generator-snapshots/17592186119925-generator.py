#!/usr/bin/env python3
"""Seeded, relocatable linear-dependence practice. No I/O except CLI stdout."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import matrix_tex, system_tex, normalize_prose, validate_generated_record

KP = 17592186119925
VERSION = 'row-reduction-3'
EQ = r'x_1\mathbf{a}_1+x_2\mathbf{a}_2+x_3\mathbf{a}_3=\mathbf{0}'
NAMESPACE = uuid.UUID('866fb065-482e-448a-9823-a7f95f1f1c04')
CONCEPTS = ('independent','dependent','trivial','infinite','free','pivot')

def uid(s): return str(uuid.uuid5(NAMESPACE,s))
def tex(x):
    x=F(x)
    if x.denominator==1:return str(x.numerator)
    return ('-' if x<0 else '')+r'\frac{'+str(abs(x.numerator))+'}{'+str(x.denominator)+'}'
def display(s): return '\n\n$$\n'+s+'\n$$\n\n'
def aug(A):return matrix_tex([[tex(x) for x in row]+['0'] for row in A],augmented=True)
def lin(coeffs, variables):
    out=''
    for a,v in zip(coeffs,variables):
        a=F(a)
        if not a:continue
        t=('' if abs(a)==1 else tex(abs(a)))+v
        out+=('-' if a<0 else '+' if out else '')+t
    return out or '0'

def eliminate(A):
    M=[[F(x) for x in r] for r in A];states=[[r[:] for r in M]];ops=[];piv=[];row=0
    for col in range(3):
        k=next((k for k in range(row,3) if M[k][col]),None)
        if k is None:continue
        if k!=row:
            M[k],M[row]=M[row],M[k]
            ops.append({'kind':'swap','i':row,'j':k})
            states.append([r[:] for r in M])
        for i in range(row+1,3):
            if M[i][col]:
                q=-M[i][col]/M[row][col]
                M[i]=[a+q*b for a,b in zip(M[i],M[row])]
                ops.append({'kind':'add','i':i,'j':row,'factor':str(q)})
                states.append([r[:] for r in M])
        piv.append(col);row+=1
        if row==3:break
    return states,ops,piv

def optex(o):
    i,j=o['i']+1,o['j']+1
    if o['kind']=='swap':return f'R_{i}'+r'\leftrightarrow '+f'R_{j}'
    q=F(o['factor']);return f'R_{i}'+r'\leftarrow '+lin([1,q],[f'R_{i}',f'R_{j}'])

def statement(c):
    return {'independent':r'The vectors $\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3$ are linearly independent.',
    'dependent':r'The vectors $\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3$ are linearly dependent.',
    'trivial':'The equation $'+EQ+'$ has only the solution $x_1=x_2=x_3=0$.',
    'infinite':'The equation $'+EQ+'$ has infinitely many solutions with coefficients not all zero.',
    'free':r'At least one of $x_1,x_2,x_3$ is a free variable in row echelon form.',
    'pivot':'Every column of the coefficient matrix contains a pivot in row echelon form.'}[c]

def truth(c,piv):
    independent=len(piv)==3
    return {'independent':independent,'dependent':not independent,'trivial':independent,
      'infinite':not independent,'free':not independent,'pivot':independent}[c]

def subset_text(sub):
    names=['I','II','III'];return 'None of the statements are true' if not sub else ' and '.join(names[i] for i in sub)+' only'

def raw_field(key,values,correct,kind):
    return {':answer-field/key':normalize_prose(key),':answer-field/type':':answer-field.type/'+kind,
      ':answer-field/choices':[{':answer/type':':answer.type/text',':answer/value':normalize_prose(v)} for v in values], '_correct':normalize_prose(correct)}

def finalize(problem,solution,fields,band,generation):
    q={':question/problem':normalize_prose(problem),':question/worked-solution':normalize_prose(solution),
       ':question/difficulty':':question.difficulty/'+band,':question/answer-fields':fields}
    ident=hashlib.sha256(json.dumps(q,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    q[':question/id']=uid(ident)
    for i,f in enumerate(fields):
        f[':answer-field/id']=uid(ident+f':field:{i}')
        correct=f.pop('_correct')
        for a in f[':answer-field/choices']:
            a[':answer/id']=uid(ident+f':answer:{i}:'+a[':answer/value'])
        a=next(a for a in f[':answer-field/choices'] if a[':answer/value']==correct)
        f[':answer-field/correct']=[':answer/id',a[':answer/id']]
    return validate_generated_record({'knowledge_point':KP,'question':q,'generation':{'version':VERSION,**generation}})

def solution(A,states,ops,piv):
    variables=['x_1','x_2','x_3']
    s='Place the three vectors in the columns of the coefficient matrix. The homogeneous equation $'+EQ+'$ corresponds to'+display(system_tex([lin(r,variables)+'=0' for r in A]))
    s+='Append the zero right-hand side and use the following row operations in order.'+display('M='+aug(A))
    for o,M in zip(ops,states[1:]):
        s+='Apply $'+optex(o)+'$:'+display(aug(M))
    s+='The pivot columns are $'+','.join(str(c+1) for c in piv)+'$.'
    if len(piv)==3:
        s+=' Back substitution, beginning with the last row, gives'
        lines=[]
        for row,col in reversed(list(enumerate(piv))):
            lines.append(lin(states[-1][row],variables)+r'&=0\quad\Longrightarrow\quad x_'+str(col+1)+'=0')
        s+=display(r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}')
        s+='Thus $x_1=x_2=x_3=0$ is the only solution. The vectors are **linearly independent**; there is no nontrivial solution and no free variable.'
    else:
        f=next(c for c in range(3) if c not in piv)
        v=[F(0)]*3;v[f]=F(1);lines=[f'x_{f+1}'+r'&=t']
        for row,col in reversed(list(enumerate(piv))):
            v[col]=-sum(states[-1][row][k]*v[k] for k in range(col+1,3))/states[-1][row][col]
            lines.append(lin(states[-1][row],variables)+r'&=0\quad\Longrightarrow\quad x_'+str(col+1)+'='+lin([v[col]],['t']))
        s+=f' The variable $x_{f+1}$ is free. Set $x_{f+1}=t$ and back-substitute:'
        s+=display(r'\begin{aligned}'+r' \\ '.join(lines)+r'\end{aligned}')
        s+='Hence'+display('(x_1,x_2,x_3)=('+','.join(lin([a],['t']) for a in v)+r'),\qquad t\in\mathbb{R}.')
        s+='For every $t\\ne0$, the coefficients are not all zero. Therefore there are infinitely many nontrivial solutions, and the vectors are **linearly dependent**. A zero final row imposes no additional constraint.'
    return s

def make(A,band,concepts=('independent','dependent','trivial'),shape='checkbox',rng=None,challenge='direct',source=None,answer_position=None):
    rng=rng or random.Random(0)
    states,ops,piv=eliminate(A)
    p='Consider the following vectors:'+display(r',\qquad '.join(r'\mathbf{a}_'+str(c+1)+'='+matrix_tex([[str(A[r][c])] for r in range(3)]) for c in range(3))+'.')
    if band=='easy':
        p+='For real $x_1,x_2,x_3$, form the equation $'+EQ+'$. Its augmented matrix is'+display('M='+aug(A))
        p+='Carry out these operations in the order shown: '+ '; then '.join('$'+optex(o)+'$' for o in ops)+'. Use the resulting pivots and free variables to decide which statements are true.'
    elif band=='moderate':p+='For real $x_1,x_2,x_3$, use row reduction to analyze $'+EQ+'$. Which statements are true?'
    else:p+='Assume that $x_1,x_2,x_3$ are real numbers. Use row reduction to decide which statements are true.'
    s=solution(A,states,ops,piv)
    truths=[truth(c,piv) for c in concepts]
    labels=[statement(c) for c in concepts]
    if shape=='checkbox':
        p+='\n\nSelect all that apply.'
        fields=[raw_field(t,['false','true'],str(b).lower(),'checkbox') for t,b in zip(labels,truths)]
        fields.append(raw_field('None of the above',['false','true'],str(not any(truths)).lower(),'checkbox'))
        rng.shuffle(fields)
        s+='\n\n'+ ' '.join(t+(' This is true.' if b else ' This is false.') for t,b in zip(labels,truths))
        s+=' “None of the above” is '+('false.' if any(truths) else 'true because all the listed statements are false.')
    else:
        p+='\n\n'+'\n\n'.join(n+'. '+t for n,t in zip(['I','II','III'],labels))
        p+='\n\nChoose the correct combination.'
        # Construct the bank from both possible ranks, independent of actual rank.
        free=next((c for c in range(3) if c not in piv),2)
        possible={tuple(i for i,c in enumerate(concepts) if truth(c,p)) for p in ([0,1,2],[c for c in range(3) if c!=free])}
        possible.add(())
        extras=[x for n in range(4) for x in itertools.combinations(range(3),n) if x not in possible]
        rng.shuffle(extras)
        bank=sorted(possible)+extras[:5-len(possible)];rng.shuffle(bank)
        actual=tuple(i for i,t in enumerate(truths) if t)
        if answer_position is not None:
            bank.remove(actual);bank.insert(answer_position,actual)
        fields=[raw_field('selection',[subset_text(x) for x in bank],subset_text(actual),'radio')]
        s+='\n\n'+ ' '.join(n+' is '+('true' if b else 'false')+'.' for n,b in zip(['I','II','III'],truths))+' Choose “'+subset_text(actual)+'”.'
    return finalize(p,s,fields,band,{'matrix':A,'concepts':list(concepts),'target':'homogeneous solution classification','shape':shape,'challenge':challenge,
      'source_ids':source or [17592186119499], 'pivots':[c+1 for c in piv],
      'operations':ops,'states':[[[str(x) for x in row] for row in M] for M in states]})

def sample_matrix(rng,rank,band,challenge=None):
    b=rng.choice([-2,-1,1,2]);d=rng.choice([-2,-1,1,2]);c=rng.choice([x for x in [-2,-1,1,2] if x!=b*d])
    z=0 if rank==2 else rng.choice([-2,-1,1,2]);m=rng.choice([-2,-1,1,2]);n=rng.choice([-2,-1,1,2]);k=rng.choice([-2,-1,1,2])
    E=[[1,b,c],[0,1,d],[0,0,z]]
    add=lambda a,b,q:[x+q*y for x,y in zip(a,b)]
    if band=='hard':
        challenge=challenge or rng.choice(['initial-exchange','interior-exchange'])
        if challenge=='interior-exchange':
            A=[E[0],add(E[2],E[0],m),add(E[1],E[0],n)]
        else:
            A=[E[1],E[0],add(add(E[2],E[0],n),E[1],k)]
            challenge='initial-exchange'
    else:
        challenge='direct'
        A=[E[0],add(E[1],E[0],m),add(add(E[2],E[0],n),E[1],k)]
    return A,challenge

def generate(band,count,seed):
    rng=random.Random(seed);schedule=[];records=[];seen=set();i=0
    placement=random.Random(str(seed)+':answer-positions');positions=[];radio_index=0;previous_radio_position=None
    profiles=random.Random(str(seed)+':profiles');previous_checkbox=None
    while len(records)<count:
        if i%4==0:
            schedule=list(itertools.product([2,3],['checkbox','radio']));rng.shuffle(schedule)
            checkbox_profile=profiles.sample(CONCEPTS,3)
            radio_profile=profiles.sample(CONCEPTS[:4],3)
        rank,shape=schedule[i%4];i+=1
        local=random.Random(rng.getrandbits(128))
        A,challenge=sample_matrix(local,rank,band)
        concepts=checkbox_profile if shape=='checkbox' else radio_profile
        position=None
        if shape=='radio':
            if radio_index%5==0:
                positions=list(range(5));placement.shuffle(positions)
                if positions[0]==previous_radio_position:
                    positions[0],positions[1]=positions[1],positions[0]
            position=positions[radio_index%5];radio_index+=1
            previous_radio_position=position
        rec=make(A,band,concepts,shape,local,challenge,answer_position=position)
        if shape=='checkbox':
            def selected_positions(r):
                return tuple(i for i,f in enumerate(r['question'][':question/answer-fields'])
                    if any(a[':answer/value']=='true' and a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices']))
            while selected_positions(rec)==previous_checkbox:
                rec=make(A,band,concepts,shape,local,challenge)
            previous_checkbox=selected_positions(rec)
        if rec['question'][':question/id'] in seen:continue
        seen.add(rec['question'][':question/id'])
        rec['generation'].update({'seed':seed,'ordinal':len(records),'difficulty':band})
        records.append(rec)
    return records

def replay_source(case):
    A=case['matrix'];states,ops,piv=eliminate(A)
    fields=[]
    for f in case['bank']:
        fields.append(raw_field(f['key'],f['choices'],f['correct'],f['type'].split('/')[-1]))
    p=case['problem']
    # Correct captured column-vector layout, not the mathematical content.
    if r'[\begin{aligned}' in p:
        import re
        p=re.sub(r'\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',lambda m:r'\begin{bmatrix}'+m[1]+r'\end{bmatrix}',p,flags=re.S)
    return finalize(p,solution(A,states,ops,piv),fields,case['difficulty'],{'source_ids':[case['source_id']], 'source_replay':True,'matrix':A,'shape':case['bank'][0]['type'].split('/')[-1],'pivots':[x+1 for x in piv],'operations':ops,'states':[[[str(x) for x in row] for row in M] for M in states]})

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,required=True)
    parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args()
    if args.count<0:parser.error('count must be nonnegative')
    print(json.dumps(generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
