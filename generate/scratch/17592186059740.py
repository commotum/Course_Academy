#!/usr/bin/env python3
"""Exact entrywise scalar multiplication; local draft, math basis2275.

Seven original public replay profiles preserve complete banks, missing fields,
source solutions and original field order. They build the same parameterized
recipes as other calls: no captured payload is read at runtime. raw_986's opaque
compound error is evidence-only; raw_979/raw_986 have no rating/key/solution;
raw_320075 preserves an erroneous introductory coefficient3. Normal generation
minimally repairs that prose and authors missing keys/solutions/ratings.

Default sampling covers all observed prompt/field families at easy, using their
eligible whole banks or an explicitly authored operation bank. Moderate/hard
are authored design claims: six nonzero signed entrywise products, half-integer
results at moderate, reduced noninteger rational times nonunit rational with exactly three
cancellation products at hard. Neither solves for a scalar nor combines matrices.
No plots, EDB client, registration or transactions. Stop after guide step7.

CLI: .venv/bin/python generate/scratch/17592186059740.py --difficulty all --seed 42
API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), generate_easy/moderate/hard with the same optional arguments.
Stable content UUID excludes seed/option order; mathematical fingerprint excludes
names/banks/layout and, for scalar0, irrelevant original entries. Operand values
remain substantive for nonzero multiplication: their cancellation/signed products
are the assessed arithmetic, even when another factorization yields the same result.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import sys
import uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186059740
KP_UUID='c4cc58a6-ebb8-544d-93a1-de6cbd5b180e'
TITLE='Multiplying a Matrix by a Scalar'
VERSION='scalar-matrix-v1'
SOURCE={'database':'math','basis':2275,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'what_2x2':'radio','named_3x2':'radio','named_2x3':'radio','entries_2x2':'blank','direct':'radio'}
# Complete profiles selected BEFORE parameter sampling. Raw profiles are public
# immutable evidence modes, never normal defaults. All formulas depend on k,A.
PROFILES={
 'raw_979':('what_2x2','bank979',True,False,False,None),
 'raw_986':('named_3x2','bank986',True,False,False,None),
 'raw_125885':('named_2x3','bankzero',True,True,True,None),
 'raw_980':('direct','bank980',True,True,True,None),
 'raw_320045':('entries_2x2','blank',True,True,True,None),
 'raw_320075':('entries_2x2','blank',True,True,True,3),
 'raw_320082':('entries_2x2','blank',True,True,True,None),
 'observed_979':('what_2x2','bank979',False,True,True,None),
 'observed_zero':('named_2x3','bankzero',False,True,True,None),
 'observed_980':('direct','bank980',False,True,True,None),
 'entries':('entries_2x2','blank',False,True,True,None),
 'method_what':('what_2x2','method',False,True,True,None),
 'method_named_3x2':('named_3x2','method',False,True,True,None),
 'method_named_2x3':('named_2x3','method',False,True,True,None),
 'method_direct':('direct','method',False,True,True,None),
}
ORDERS={'raw_320045':[4,1,2,3],'raw_320075':[1,4,2,3],'raw_320082':[3,4,1,2]}
RAW_PARAMS={
 'raw_979':{'k':5,'matrix':[[1,0],[2,6]],'name':'A'},
 'raw_986':{'k':6,'matrix':[[-1,2],[1,0],['1/3',4]],'name':'D'},
 'raw_125885':{'k':0,'matrix':[[1,-1,-3],[-5,0,2]],'name':'W'},
 'raw_980':{'k':3,'matrix':[[4,-5],[-2,'1/3']],'name':'A'},
 'raw_320045':{'k':3,'matrix':[[2,1],[4,3]],'name':'A'},
 'raw_320075':{'k':-7,'matrix':[[5,4],[-6,2]],'name':'A'},
 'raw_320082':{'k':2,'matrix':[[1,2],[-2,4]],'name':'C'},
}

def rational(value):
    if isinstance(value,bool) or isinstance(value,float):
        raise ValueError('Use exact integers or rational strings, not floats/bools.')
    x=sp.sympify(value)
    if not isinstance(x,sp.Rational):raise ValueError('Only exact rational scalars and entries are in scope.')
    return x

def tex(x):return sp.latex(rational(x))
def matrix_tex(rows):
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(tex(x) for x in row) for row in rows)+r'\end{bmatrix}'
def products_tex(k,A,group_scalar):
    factor=('('+tex(k)+')') if group_scalar and k<0 else tex(k)
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(factor+r'\cdot '+('('+tex(a)+')' if a<0 else tex(a)) for a in row) for row in A)+r'\end{bmatrix}'
def scale(k,A):return [[k*a for a in row] for row in A]
def changed(A, replacements):
    B=[row[:] for row in A]
    for (i,j),v in replacements.items():B[i][j]=v
    return B

def banks(k,A,kind):
    """Five values as one bank; no individually replacing a colliding choice."""
    C=scale(k,A)
    if kind=='bank979':
        return [('flip_lower_left',changed(C,{(1,0):-C[1][0]})),
                ('omit_lower_right',changed(C,{(1,1):A[1][1]})),('correct',C),
                ('zero_as_one',changed(C,{(0,1):k})),
                ('omit_lower_left',changed(C,{(1,0):A[1][0]}))]
    if kind=='bank986':
        # Underidentified source profile: this parameterized compound operation
        # reproduces every entry but does not claim recovered author intention.
        return [('flip_first_two_first_column',changed(C,{(0,0):-C[0][0],(1,0):-C[1][0]})),
                ('correct',C),('swap_second_column_first_two',changed(C,{(0,1):C[1][1],(1,1):C[0][1]})),
                ('opaque_last_row_sign_and_add',changed(C,{(2,0):-C[2][0],(2,1):k+A[2][1]})),
                ('flip_top_left',changed(C,{(0,0):-C[0][0]}))]
    if kind=='bankzero':
        return [('only_first_column',[[k*a if j==0 else a for j,a in enumerate(row)] for row in A]),
                ('correct',C),('only_top_left',changed(A,{(0,0):C[0][0]})),
                ('only_top_row',[C[0],A[1][:]]),('omit_all_scaling',A)]
    if kind=='bank980':
        ignored_denominator=k*A[1][1].p
        return [('omit_top_right',changed(C,{(0,1):A[0][1]})),
                ('ignore_denominator',changed(C,{(1,1):ignored_denominator})),
                ('lower_left_sign_and_ignore_denominator',changed(C,{(1,0):-C[1][0],(1,1):ignored_denominator})),
                ('omit_lower_left',changed(C,{(1,0):A[1][0]})),('correct',C)]
    if kind=='method':
        return [('correct',C),('omit_all_scaling',A),('reverse_scalar_sign',scale(-k,A)),
                ('omit_first_row',[A[0][:]]+C[1:]),
                ('omit_last_row',C[:-1]+[A[-1][:]])]
    raise ValueError('Unknown whole-bank recipe.')

def unique_bank(bank):
    vals=[tuple(tuple(row) for row in v) for _,v in bank]
    return len(vals)==len(set(vals))

def normalize(parameters,template):
    if set(parameters)-{'k','matrix','name'}:raise ValueError('Unexpected parameter slot.')
    k=rational(parameters['k']);A=[[rational(a) for a in row] for row in parameters['matrix']]
    if not A or not A[0] or any(len(row)!=len(A[0]) for row in A):raise ValueError('Rectangular matrix required.')
    shape=(len(A),len(A[0]))
    expected={'what_2x2':(2,2),'named_3x2':(3,2),'named_2x3':(2,3),'entries_2x2':(2,2)}
    if template in expected and shape!=expected[template]:raise ValueError('This family has a fixed source-shaped matrix size.')
    if template=='direct' and shape not in [(2,2),(2,3),(3,2)]:raise ValueError('Unsupported direct matrix size.')
    name=parameters.get('name','A')
    if name not in list('ACDMRW'):raise ValueError('Use one supported matrix name.')
    return k,A,name

def check_bounds(level,k,A,template,raw=False):
    if raw:
        if abs(k)>12 or any(abs(a)>12 or a.q>12 for row in A for a in row):raise ValueError('Evidence recipe exact-rational bounds exceeded.')
        return
    xs=sum(A,[]);shape=(len(A),len(A[0]))
    if level=='easy':
        if k.q!=1 or abs(k)>7 or (k!=0 and abs(k)<2):raise ValueError('Easy integer scalar0 or signed2..7 required.')
        if any(abs(a)>7 or a.q>7 for a in xs):raise ValueError('Easy entry bound7/denominator7.')
        if sum(a.q!=1 for a in xs)>1:raise ValueError('Easy permits at most one familiar unit fraction.')
        if any(a.q!=1 and abs(a.p)!=1 for a in xs):raise ValueError('Easy fraction is a signed unit fraction.')
        if k and shape!=(2,2) and sum(a!=0 for a in xs)>5 and abs(k)>6:raise ValueError('Six easy products use scalar magnitude2..6.')
    elif level=='moderate':
        if template=='entries_2x2' or shape not in [(2,3),(3,2)]:raise ValueError('Moderate has six products, radio source-shaped contract.')
        if abs(k)!=sp.Rational(1,2):raise ValueError('Moderate scalar is signed one half.')
        if any(a.q!=1 or not 1<=abs(a)<=9 for a in xs):raise ValueError('Moderate entries are six nonzero signed integers1..9.')
        if sum(abs(a)%2==1 for a in xs)!=3:raise ValueError('Moderate has exactly three half-integer and three integer products.')
        if not any(a<0 for a in xs) or not any(a>0 for a in xs):raise ValueError('Moderate requires both entry signs.')
    elif level=='hard':
        if template=='entries_2x2' or shape not in [(2,3),(3,2)]:raise ValueError('Hard has six products, radio source-shaped contract.')
        if abs(k) not in [sp.Rational(2,3),sp.Rational(3,4),sp.Rational(2,5),sp.Rational(3,5)]:raise ValueError('Hard scalar must be a nonunit reduced rational from the documented set.')
        if any(not 1<=abs(a.p)<=5 or not 2<=a.q<=5 or abs(a)>=4 for a in xs):raise ValueError('Hard entries use reduced signed fractions, numerator1..5/denominator2..5, magnitude below4.')
        if sum(bool(sp.gcd(abs(k.p*a.p),k.q*a.q)>1) for a in xs)!=3:raise ValueError('Hard has exactly three genuine cancellation products.')
        if sum((k*a).q>1 for a in xs)<4:raise ValueError('Hard retains at least four fractional results.')
        if not any(a<0 for a in xs) or not any(a>0 for a in xs):raise ValueError('Hard requires both entry signs.')
    else:raise ValueError('Difficulty must be easy/moderate/hard.')

def prompt(template,k,A,name,raw=False):
    K=tex(k);M=matrix_tex(A)
    if template=='what_2x2':return 'What is $'+K+M+'$?'
    if template=='named_3x2':return 'Calculate $'+K+name+'$, if\n$'+name+' = '+M+'$.'
    if template=='named_2x3':return 'Calculate $'+K+name+'$, if \n$'+name+'='+M+'.$'
    if template=='direct':return '$'+K+M+'=$'
    return ('Calculate $'+K+name+'$, where\n$'+name+'='+M+'.$\n\n| $'+K+name+r'=\,\,$ |  | {{field-1}} | {{field-2}} |  |'+'\n| --- | --- | --- | --- | --- |\n'+ ('|  | {{field-3}} | {{field-4}} |  |  |' if raw else '|  |  | {{field-3}} | {{field-4}} |  |'))

def solution(template,k,A,name,profile,prose_override):
    K=tex(k);M=matrix_tex(A);C=matrix_tex(scale(k,A))
    group=(k<0 and profile not in ['raw_979','raw_986','raw_125885','raw_980'])
    P=products_tex(k,A,group)
    if template=='direct':
        return ('We multiply each entry of the matrix by $'+K+'$, as follows:\n\n$$\n'+r'\begin{aligned}'+K+M+' & ='+P+r' \\  & ='+C+r'\end{aligned}'+'\n$$')
    prose=tex(prose_override) if prose_override is not None else K
    return ('We multiply each entry of $'+name+'$ by $'+prose+',$ as follows:\n\n$$\n'+r'\begin{aligned}'+K+name+' & ='+K+M+r' \\  & ='+P+r' \\  & ='+C+r'\end{aligned}'+'\n$$')

def defaults(level,field_type=None):
    if level=='easy':
        pairs=[('what_2x2','observed_979'),('named_3x2','method_named_3x2'),('named_2x3','observed_zero'),('entries_2x2','entries'),('direct','observed_980')]
    else:pairs=[('named_3x2','method_named_3x2'),('named_2x3','method_named_2x3'),('direct','method_direct')]
    return [(t,p) for t,p in pairs if not field_type or TEMPLATES[t]==field_type]

# EASY: observed signs/zeros/unit fractions already occur at this level.
def sample_easy(rng,template,profile):
    name=rng.choice(list('ACDMRW'))
    if profile=='observed_979':return {'k':rng.choice([-7,-6,-5,-4,-3,-2,2,3,4,5,6,7]),'matrix':[[rng.choice([1,2,3,4]),0],[rng.choice([-6,-4,-2,2,4,6]),rng.choice([-7,-5,-3,3,5,7])]],'name':name}
    if profile=='observed_zero':return {'k':0,'matrix':[[rng.choice([-5,-3,-1,1,3,5]) for _ in range(3)] for _ in range(2)],'name':name}
    if profile=='observed_980':return {'k':rng.choice([-6,-5,-4,-3,-2,2,3,4,5,6]),'matrix':[[rng.choice([-6,-4,2,4,6]),rng.choice([-5,-3,-1,1,3,5])],[rng.choice([-5,-3,-2,2,3,5]),str(sp.Rational(rng.choice([-1,1]),rng.choice([2,3,4,5,6])))]],'name':name}
    shape={'named_3x2':(3,2),'named_2x3':(2,3),'what_2x2':(2,2),'entries_2x2':(2,2)}.get(template,(2,2))
    return {'k':rng.choice([-6,-5,-4,-3,-2,2,3,4,5,6]),'matrix':[[rng.choice([-6,-4,-2,1,3,5]) for _ in range(shape[1])] for _ in range(shape[0])],'name':name}

# MODERATE: fixed six products, exactly3 odd integer inputs; signed half scalar.
def sample_moderate(rng,template,profile):
    xs=[rng.choice([-9,-7,-5,-3,-1,1,3,5,7,9]) for _ in range(3)]+[rng.choice([-8,-6,-4,-2,2,4,6,8]) for _ in range(3)]
    rng.shuffle(xs);shape=(3,2) if template=='named_3x2' or (template=='direct' and rng.choice([0,1])) else (2,3)
    return {'k':str(rng.choice([sp.Rational(1,2),sp.Rational(-1,2)])),'matrix':[xs[i:i+shape[1]] for i in range(0,6,shape[1])],'name':rng.choice(list('ACDMRW'))}

# HARD: fixed six reduced noninteger rational products, exactly3 cross-cancellations; no progression.
def sample_hard(rng,template,profile):
    k=rng.choice([s*sp.Rational(n,d) for s in [-1,1] for n,d in [(2,3),(3,4),(2,5),(3,5)]])
    domain=sorted({sp.Rational(s*n,d) for s in [-1,1] for n in range(1,6) for d in range(2,6) if sp.Rational(n,d).q>1 and sp.Rational(n,d)<4})
    cancel=[a for a in domain if sp.gcd(abs(k.p*a.p),k.q*a.q)>1];other=[a for a in domain if a not in cancel]
    xs=[rng.choice(cancel) for _ in range(3)]+[rng.choice(other) for _ in range(3)];rng.shuffle(xs)
    shape=(3,2) if template=='named_3x2' or (template=='direct' and rng.choice([0,1])) else (2,3)
    return {'k':str(k),'matrix':[[str(a) for a in xs[i:i+shape[1]]] for i in range(0,6,shape[1])],'name':rng.choice(list('ACDMRW'))}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ['easy','moderate','hard']:raise ValueError('Unknown level.')
    if field_type and field_type not in ['radio','blank']:raise ValueError('Unsupported field type.')
    rng=random.Random(seed)
    if profile:
        if profile not in PROFILES:raise ValueError('Unknown profile.')
        chosen=PROFILES[profile][0]
        if template and template!=chosen:raise ValueError('Profile does not belong to template.')
        template=chosen
    else:
        choices=[(t,p) for t,p in defaults(level,field_type) if not template or t==template]
        if not choices:raise ValueError('No eligible family/whole bank at this level.')
        template,profile=rng.choice(choices)
    if field_type and TEMPLATES[template]!=field_type:raise ValueError('Field contract mismatch.')
    _,bank_kind,raw,has_rating,has_solution,prose_override=PROFILES[profile]
    if raw and level!='easy':raise ValueError('Raw rated sources are easy; unrated raw replay uses easy only as routing metadata.')
    if profile in ['observed_979','observed_zero','observed_980','entries'] and level!='easy':raise ValueError('Observed easy bank profile cannot bypass authored level bounds.')
    if parameters is None and raw:parameters=RAW_PARAMS[profile]
    for _ in range(1000):
        p=parameters if parameters is not None else {'easy':sample_easy,'moderate':sample_moderate,'hard':sample_hard}[level](rng,template,profile)
        k,A,name=normalize(p,template)
        try:
            check_bounds(level,k,A,template,raw)
            if bank_kind=='bank979' and A[0][1]!=0:raise ValueError('Observed zero-as-one profile requires zero upper-right.')
            if bank_kind=='bankzero' and k!=0:raise ValueError('Zero source profile requires scalar0.')
            if bank_kind=='bank980' and A[1][1].q==1:raise ValueError('Denominator-error bank requires a fraction at lower-right.')
            bank=[] if bank_kind=='blank' else banks(k,A,bank_kind)
            if bank and not unique_bank(bank):raise ValueError('Reject complete colliding bank.')
        except ValueError:
            if parameters is not None:raise
            continue
        break
    else:raise ValueError('No eligible instance sampled.')
    P=prompt(template,k,A,name,raw);S=solution(template,k,A,name,profile,prose_override) if has_solution else None
    # Full presentation identity includes every matrix option and source omissions;
    # displayed order and cosmetics of absent names do not affect UUID.
    canonical_p={'k':str(k),'matrix':[[str(a) for a in row] for row in A],'name':name}
    bank_values=sorted(matrix_tex(v) for _,v in bank)
    content={'version':VERSION,'level':level if has_rating else None,'problem':P,'solution':S,'type':TEMPLATES[template],'bank':bank_values,'parameters':canonical_p,'profile':profile}
    digest=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    QID=str(uuid.uuid5(uuid.NAMESPACE_URL,'scalar-matrix:'+digest))
    question={':question/id':QID,':question/problem':P}
    if has_rating:question[':question/difficulty']=':question.difficulty/'+level
    if has_solution:question[':question/worked-solution']=S
    fields=[]
    def field(key,kind,values,correct_role):
        FID=str(uuid.uuid5(uuid.UUID(QID),'field:'+key));answers=[];correct=None
        for role,value in values:
            aid=str(uuid.uuid5(uuid.UUID(FID),value));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
            if role==correct_role:correct=aid
        f={':answer-field/id':FID,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
        if profile not in ['raw_979','raw_986']:f[':answer-field/correct']=[':answer/id',correct]
        return f
    if bank_kind=='blank':
        result=sum(scale(k,A),[])
        for i in ORDERS.get(profile,[1,2,3,4]):fields.append(field('field-'+str(i),'blank',[('correct',tex(result[i-1]))],'correct'))
    else:
        vals=[(r,matrix_tex(v)) for r,v in bank]
        rng.shuffle(vals);fields=[field('selection','radio',vals,'correct')]
    question[':question/answer-fields']=fields
    math_data={'operation':'entrywise scalar multiplication','shape':[len(A),len(A[0])],'k':str(k)}
    if k:math_data['matrix']=canonical_p['matrix']
    fingerprint=hashlib.sha256(json.dumps(math_data,sort_keys=True).encode()).hexdigest()
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':canonical_p,'difficulty':level,'difficulty_origin':'source omitted; authored routing only' if not has_rating else ('observed easy' if raw else ('source-grounded easy workload; authored assignment for unrated families' if level=='easy' else 'authored missing-level design')),'source':SOURCE,'source_ids':{'bank979':['q-979'],'bank986':['q-986'],'bankzero':['q-125885'],'bank980':['q-980'],'blank':['q-320045','q-320075','q-320082'],'method':['q-979','q-986','q-125885','q-980']}.get(bank_kind,[]),'recipes':[r for r,_ in bank],'eligible_for_learning':not raw,'evidence_only':raw,'source_error':'introductory coefficient3 contradicts supplied scalar' if profile=='raw_320075' else None,'interpretation_limit':'compound final-row intent underidentified' if bank_kind=='bank986' else None,'content_sha256':digest,'mathematical_fingerprint':fingerprint,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];g=record['generation']
    level=g['difficulty'] if ':question/difficulty' in q else 'unrated source (easy API routing)'
    out=[f"{level} · {g['template']} · {g['profile']}"+(' · INELIGIBLE RAW EVIDENCE' if g['evidence_only'] else ''),q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        out.append('Field '+f[':answer-field/key']+' ('+f[':answer-field/type']+')')
        correct=f.get(':answer-field/correct',[None,None])[1]
        out += [('* ' if a[':answer/id']==correct else '- ')+'$'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
    out.append(q.get(':question/worked-solution','[Source worked solution absent]'))
    return '\n\n'.join(out)

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template',choices=list(TEMPLATES));p.add_argument('--profile',choices=list(PROFILES));p.add_argument('--parameters',help='JSON with exact k,matrix,name');p.add_argument('--field-type',choices=['radio','blank']);a=p.parse_args()
    if a.count<1:p.error('count must be positive')
    levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
    rows=[generate(level,a.seed+i,template=a.template,profile=a.profile,field_type=a.field_type,parameters=json.loads(a.parameters) if a.parameters else None) for level in levels for i in range(a.count)]
    print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
if __name__=='__main__':main()
