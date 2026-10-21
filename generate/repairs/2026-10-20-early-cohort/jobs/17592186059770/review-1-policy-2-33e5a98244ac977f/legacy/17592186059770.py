#!/usr/bin/env python3
"""Source-backed moderate matrix questions; no database operations.

Two complete profiles: coefficient q-1070 and augmented q-1073. Numeric
slots preserve supplied equation order, missing-variable patterns and ordered
rearrangement/reading/augmentation stages. Easy/hard source families are
classified but not implemented by this requested moderate replenishment package;
their observed levels are not claimed mathematically unsupported or filled.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186059770
KP_UUID='14d047c8-f032-5ff3-aced-65d40bfeeaad'
TITLE='Finding the Augmented Matrix of a Linear System With Variables Other Than x, y, z'
VERSION='other-variables-matrices-1.0'
SUPPORTED_LEVELS=('moderate',)
SOURCE=json.loads(Path(__file__).with_suffix('').joinpath('source.json').read_text())
SOURCE={k:SOURCE[k] for k in ('database','basis','lineage')}
TEMPLATES={'coefficient':'q-1070','augmented':'q-1073'}
SOURCE_PARAMETERS={'coefficient':{'a':4,'b':2,'c':3,'d':-11,'e':12},'augmented':{'k':4,'l':11,'m':3,'r':-1}}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def tex(x):return sp.latex(sp.Rational(x))
def term(x,name,first=False,explicit=False):
    x=sp.Rational(x)
    sign='-' if x<0 else ('' if first else '+')
    return sign+('' if abs(x)==1 and not explicit else tex(abs(x)))+name

def linear(values,names):return ''.join(term(x,n,first=i==0,explicit=True) for i,(x,n) in enumerate(zip(values,names,strict=True)))
def matrix(rows,augmented=False):
    body=r' \\ '.join(' & '.join(tex(x) for x in row) for row in rows)
    if augmented:return r'\left[\begin{array}{'+'c'*(len(rows[0])-1)+'|c}'+body+r'\end{array}\right]'
    return r'\begin{bmatrix}'+body+r'\end{bmatrix}'
def system(equations):return r'\left\{\begin{aligned}'+r' \\ '.join(lhs+' &='+rhs for lhs,rhs in equations)+r'\end{aligned}\right.'
def normalize_parameters(template,p):
    assert set(p)==set(SOURCE_PARAMETERS[template]),'Parameter keys mismatch'
    p={k:int(v) for k,v in p.items() if not isinstance(v,bool) and sp.Rational(v).q==1}
    assert set(p)==set(SOURCE_PARAMETERS[template]),'Exact integers required'
    if template=='coefficient':
        assert all(1<=p[k]<=15 for k in ('a','b','c','e')) and -15<=p['d']<=-1
        assert p['a']!=p['b'],'Swapped-column distractor must differ'
    else:assert all(2<=p[k]<=15 for k in ('k','l','m')) and -15<=p['r']<=-1
    return p

def components(template,p):
    if template=='coefficient':
        a,b,c,d,e=(p[k] for k in ('a','b','c','d','e'));names=[r'{x}_{1}',r'{x}_{2}',r'{x}_{3}']
        equations=[(term(b,names[1],True)+term(a,names[0]),term(c,names[2],True)),(term(d,names[2],True),tex(e))]
        A=[[a,b,-c],[0,0,d]];rhs=[0,e]
        banks=[('correct',A,False),('append_constants',[[a,b,-c,0],[0,0,d,e]],False),('appearance_order_and_keep_rhs_sign_with_constants',[[b,a,c,0],[0,0,d,e]],False),('keep_rhs_sign',[[a,b,c],[0,0,d]],False),('appearance_order_and_keep_rhs_sign',[[b,a,c],[0,0,d]],False)]
        kind='coefficient'
    else:
        k,l,m,r=(p[x] for x in ('k','l','m','r'));names=['a','b','c']
        equations=[('a-c',term(k,'b',True)),(term(m,'c',True)+term(-l,'a'),tex(r))]
        A=[[1,-k,-1],[-l,0,m]];rhs=[0,r];C=[row+[v] for row,v in zip(A,rhs,strict=True)]
        banks=[('correct',C,True),('treat_b_coefficient_as_constant',[[1,0,-1,k],[-l,0,m,r]],True),('omit_b_column_and_use_second_row_appearance_order',[[1,-1,k],[m,-l,r]],True),('reverse_second_constant',[[1,-k,-1,0],[-l,0,m,-r]],True),('appearance_order_and_negate_c_second_row',[[1,-1,0,k],[-m,-l,0,r]],True)]
        kind='augmented'
    organized=[(linear(row,names),tex(v)) for row,v in zip(A,rhs,strict=True)]
    prompt='What is the '+kind+' matrix for the following system of linear equations?\n\n$$\n'+system(equations)+'\n$$'
    solution='First, we organize the system so that the variables are ordered $'+','.join(names)+'$ on the left-hand side, the constants are on the right-hand side, and every variable has a coefficient:\n\n$$\n'+system(organized)+'\n$$\n\nThe coefficient matrix consists of the coefficients of the variables:\n\n$$\n'+matrix(A)+'\n$$'
    if kind=='augmented':solution+='\n\nThe augmented matrix is the coefficient matrix augmented with the column that represents the right-hand sides of the equations:\n\n$$\n'+matrix([row+[v] for row,v in zip(A,rhs,strict=True)],True)+'\n$$'
    return prompt,solution,banks,A,rhs

def mathematical_fingerprint(template,A,rhs):
    # Exclude common scaling aliases, variable naming, bank/order and UUID changes.
    rows=[]
    for row,v in zip(A,rhs,strict=True):
        augmented=[sp.Rational(x) for x in (row if template=='coefficient' else row+[v])]
        pivot=next(x for x in augmented if x)
        rows.append([str(x/pivot) for x in augmented])
    return digest({'requested_matrix':template,'equations':rows})

def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Level observed but not implemented in this moderate-only package; shortage remains explicit')
    if field_type not in (None,'radio'):raise ValueError('Only source radio fields supported')
    rng=random.Random(seed);template=template or rng.choice(tuple(TEMPLATES))
    if template not in TEMPLATES:raise ValueError('Unknown template')
    profile=profile or TEMPLATES[template]
    if profile!=TEMPLATES[template]:raise ValueError('Template/profile mismatch')
    if parameters is None:
        if template=='coefficient':
            a,b=rng.sample(range(2,16),2);p={'a':a,'b':b,'c':rng.randint(2,15),'d':-rng.randint(2,15),'e':rng.randint(1,15)}
        else:p={'k':rng.randint(2,15),'l':rng.randint(2,15),'m':rng.randint(2,15),'r':-rng.randint(1,15)}
    else:p=parameters
    p=normalize_parameters(template,p);prompt,solution,banks,A,rhs=components(template,p)
    values=[matrix(rows,aug) for recipe,rows,aug in banks]
    assert len(set(values))==5
    content=digest({'template':template,'prompt':prompt,'bank':sorted(values),'correct':values[0]})
    qid=uid('question:'+content);fid=uid(qid+':selection')
    answers=[{':answer/id':uid(fid+':'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=answers[0][':answer/id'];rng.shuffle(answers)
    q={':question/id':qid,':question/problem':prompt,':question/difficulty':':question.difficulty/'+level,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'source':SOURCE,'source_references':[profile],'eligible_for_learning':True,'evidence_only':False,'mathematical_fingerprint':mathematical_fingerprint(template,A,rhs),'content_identity':content,'recipes':[{'recipe':recipe,'matrix':rows,'augmented_notation':aug} for recipe,rows,aug in banks],'plot_rating':'none','domains':'positive integer magnitude 1..15; fixed observed sign roles, zero structure and equation order','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='moderate');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='json');parser.add_argument('--template',choices=TEMPLATES);parser.add_argument('--parameters');parser.add_argument('--profile',choices=list(TEMPLATES.values()))
    args=parser.parse_args()
    if args.count<1:parser.error('Count must be positive')
    level='moderate' if args.difficulty=='all' else args.difficulty
    try:records=[generate(level,args.seed+i,args.template,json.loads(args.parameters) if args.parameters else None,args.profile) for i in range(args.count)]
    except ValueError as e:parser.error(str(e))
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
