#!/usr/bin/env python3
"""Ordered fundamental vector product. Offline, relocatable, seeded generator."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import sys
import uuid
sys.dont_write_bytecode = True
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

HERE = Path(__file__).resolve().parent
u, v = s.symbols('u v', real=True)
VERSION = 'fundamental-vector-product-6'
KP = 17592186119887
FAMILIES = {'easy': ('graph-quadratic','graph-exponential','graph-bilinear','separated-powers','separated-trigonometric','tutorial-cylinder'),
            'moderate': ('dense-polynomial','mixed-trigonometric'),
            'hard': ('nested-sin','nested-cos','nested-exp')}
SOURCE_IDS = ['6e620e4a-e82b-57dd-8cd9-76c33846bfaf','dade4255-e1e8-5d68-9c25-815855912b22',
              '5d08c35d-51cc-50ea-bb44-1ebd28104462','9f52e90e-7be3-5f9c-9e1c-12885e700253']
EXEMPLARS = ['b1477a61-61fb-5696-8adb-07eac7985d37','14ac2d28-1473-5546-8e40-b139ab446b84','447fa655-bea9-56ad-a706-376817226e2d']

def tex(e):
    # Expand sums/products only. Never trigsimp, argument reversal or log conversion.
    return s.latex(s.expand(e)).replace(r'\left', '').replace(r'\right', '')
def vec(xs): return r'\begin{pmatrix}'+r'\\'.join(tex(x) for x in xs)+r'\end{pmatrix}'

def normalize_vector_layout(value):
    # Source angle-bracket vectors and authored vectors share the same 3x1 layout.
    value=normalize_tex(value)
    if value.startswith('⟨'):value=r'\langle '+value[1:-1]+r'\rangle'
    if value.startswith(r'\langle'):
        cells=value[len(r'\langle'):-len(r'\rangle')].replace(r'\,','').split(',')
        assert len(cells)==3
        return r'\begin{pmatrix}'+r'\\'.join(c.strip() for c in cells)+r'\end{pmatrix}'
    return value
def display(t): return '\n\n$$\n'+t+'\n$$\n'
def digest(z): return hashlib.sha256(json.dumps(z,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(z): return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+z))
def expanded(xs): return s.Matrix([s.expand(x) for x in xs])
def cross(A,B): return expanded([A[1]*B[2]-A[2]*B[1], A[2]*B[0]-A[0]*B[2], A[0]*B[1]-A[1]*B[0]])
def signature(xs): return tuple(s.srepr(s.expand(x)) for x in xs)

def base_instance(family, a=1,b=1,c=1,d=1):
    """Manual ordered derivative model, separately checked by differentiation."""
    if family == 'graph-quadratic':
        R=[u,v,c*u**2+d*v**2]; A=[1,0,2*c*u]; B=[0,1,2*d*v]
    elif family == 'graph-exponential':
        R=[u,v,c*u+d*s.exp(v)]; A=[1,0,c]; B=[0,1,d*s.exp(v)]
    elif family == 'graph-bilinear':
        R=[u,v,c*u*v]; A=[1,0,c*v]; B=[0,1,c*u]
    elif family == 'separated-powers':
        R=[u**2+1,v**3+1,c*u+d*v]; A=[2*u,0,c]; B=[0,3*v**2,d]
    elif family == 'separated-trigonometric':
        R=[a*s.sin(u),b*v**2,c*v*s.cos(u)]
        A=[a*s.cos(u),0,-c*v*s.sin(u)]; B=[0,2*b*v,c*s.cos(u)]
    elif family == 'tutorial-cylinder':
        R=[a*s.cos(u),b*s.sin(u),c*v]
        A=[-a*s.sin(u),b*s.cos(u),0]; B=[0,0,c]
    elif family == 'dense-polynomial':
        R=[a*u+b*v,c*u**2+d*v,u*v]; A=[a,2*c*u,v]; B=[b,d,u]
    elif family == 'mixed-trigonometric':
        R=[u,c*u*s.sin(v),d*v*s.cos(u)]
        A=[1,c*s.sin(v),-d*v*s.sin(u)]; B=[0,c*u*s.cos(v),d*s.cos(u)]
    elif family.startswith('nested-'):
        f={'nested-sin':s.sin,'nested-cos':s.cos,'nested-exp':s.exp}[family]
        g={'nested-sin':s.cos,'nested-cos':lambda x:-s.sin(x),'nested-exp':s.exp}[family]
        R=[a*u+b*v,u*v,c*u*f(u*v)]
        A=[a,v,c*f(u*v)+c*u*v*g(u*v)]; B=[b,u,c*u**2*g(u*v)]
    else: raise ValueError(family)
    return tuple(map(s.Matrix,(R,A,B)))

def transform(instance, permutation=(0,1,2), swap=False, signs=(1,1,1), translation=(0,0,0)):
    R,A,B=instance
    if swap:
        exchange={u:v,v:u}
        R,A,B=(M.xreplace(exchange) for M in (R,B,A))
    R=s.Matrix([signs[i]*R[j]+translation[i] for i,j in enumerate(permutation)])
    A=s.Matrix([signs[i]*A[j] for i,j in enumerate(permutation)])
    B=s.Matrix([signs[i]*B[j] for i,j in enumerate(permutation)])
    return R,A,B

def solution(R,A,B,N):
    text=r'The fundamental vector product is $\mathbf r_u\times\mathbf r_v$, in that order. Hold the other parameter constant in each partial derivative.'
    text+='\n\nDifferentiate the coordinates to obtain'+display(r'\begin{aligned}'+r'\\'.join(r'\frac{\partial}{\partial '+parameter+'}('+tex(R[i])+')&='+tex(T[i]) for parameter,T in (('u',A),('v',B)) for i in range(3))+r'\end{aligned}')
    text+='\nThe tangent vectors are'+display(r'\begin{aligned}\mathbf r_u&='+vec(A)+r',\\\mathbf r_v&='+vec(B)+r'.\end{aligned}')
    text+='\nForm the ordered determinant:'+display(r'\mathbf r_u\times\mathbf r_v=\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\'+' & '.join(tex(x) for x in A)+r'\\'+' & '.join(tex(x) for x in B)+r'\end{vmatrix}.')
    # Show each unsimplified subtraction, including outside middle-cofactor minus.
    for i,(j,k) in enumerate(((1,2),(0,2),(0,1))):
        first='('+tex(A[j])+')('+tex(B[k])+')'
        second='('+tex(A[k])+')('+tex(B[j])+')'
        # Continuation rows keep the two products visible on a narrow card.
        difference=first+r'\\&\quad -'+second
        if i==1:difference='-'+first+r'\\&\quad +'+second
        text+=display(r'\begin{aligned}(\mathbf r_u\times\mathbf r_v)_{'+str(i+1)+r'}&='+difference+r'\\&='+tex(N[i])+r'.\end{aligned}')
    text+='\nTherefore the fundamental vector product is'+display(vec(N)+'.')
    return text


def error_pool(A,B,N,R=None):
    """Concrete error vectors, including general cofactor and derivative mistakes."""
    groups={'cofactor':[], 'derivative':[]}
    seen={signature(N)}
    def add(group,label,M):
        M=expanded(M); sig=signature(M)
        # Three-term mixed-trig errors can exceed the actual UI choice card.
        # Keep compact, question-specific mistakes; never clip a component or
        # shrink just the key. Current supported keys are within this budget.
        if any(len(tex(x))>64 for x in M):return
        if sig not in seen and any(x!=0 for x in M):
            groups[group].append((label,M));seen.add(sig)
    for mask in itertools.product((-1,1),repeat=3):
        if mask!=(1,1,1): add('cofactor','reverse cofactor subtractions '+str(mask),s.Matrix([mask[i]*N[i] for i in range(3)]))
    for i in range(3):
        j,k=((1,2),(2,0),(0,1))[i]
        M=N.copy();M[i]=A[j]*B[k]+A[k]*B[j]
        add('cofactor','add instead of subtract in component '+str(i+1),M)
    add('derivative','report first tangent',A);add('derivative','report second tangent',B)
    for side,T in enumerate((A,B)):
        for i,z in enumerate(T):
            if z==0: continue
            mutations=[('lose dependency',s.S.Zero)]
            other=(B,A)[side]
            if other[i]!=0:mutations.append(('differentiate held-fixed parameter too',z+other[i]))
            if R is not None:mutations.append(('retain undifferentiated coordinate',R[i]))
            if isinstance(z,s.Add):
                mutations += [('omit derivative term '+str(n),z-term) for n,term in enumerate(z.args)]
            coefficient,rest=z.as_coeff_Mul()
            if abs(coefficient)>1: mutations.append(('omit power factor',s.sign(coefficient)*rest))
            for label,value in mutations:
                wrong=T.copy();wrong[i]=value
                M=cross(wrong,B) if side==0 else cross(A,wrong)
                add('derivative',label+' tangent '+str(side)+' coordinate '+str(i),M)
    return groups


def cue_safe(values):
    """Reject a unique keyed vector identified by component modes or pairing."""
    sigs=[signature(M) for M in values]
    lengths=[len(vec(M)) for M in values]
    if any(lengths[0]==extreme and lengths.count(extreme)==1 for extreme in (min(lengths),max(lengths))):return False
    for absolute in (False,True):
        cols=[]
        for i in range(3):
            column=[min(s.srepr(x[i]),s.srepr(-x[i])) if absolute else s.srepr(x[i]) for x in values]
            counts={z:column.count(z) for z in set(column)};m=max(counts.values())
            cols.append({j for j,z in enumerate(column) if counts[z]==m})
        intersection=set.intersection(*cols)
        if intersection=={0}:return False
    paired=[any(signature(-a)==sigs[j] for j in range(len(values))) for a in values]
    if paired[0] and sum(paired)==1:return False
    if not paired[0] and sum(not p for p in paired)==1:return False
    return True


def bank(A,B,N,rng,profile,R=None):
    groups=error_pool(A,B,N,R)
    # Each profile specifies a complete error mix before choosing the values.
    ccount,dcount={'mixed':(2,2),'derivatives':(1,3),'orientation':(3,1)}[profile]
    if len(groups['derivative'])<dcount: raise ValueError('insufficient derivative errors')
    for _ in range(200):
        chosen=rng.sample(groups['cofactor'],ccount)+rng.sample(groups['derivative'],dcount)
        values=[N]+[M for label,M in chosen]
        if cue_safe(values):return values,['ordered product']+[label for label,M in chosen]
    raise ValueError('No cue-safe complete bank')


def make_record(level,R,A,B,values,recipes,rng,metadata=None,prompt=None):
    N=cross(A,B)
    if prompt is None:
        prompt='Find the fundamental vector product of the surface generated by the vector-valued function'+display(r'\mathbf r(u,v)='+vec(R)+'.')
    problem=normalize_prose(prompt)
    worked=normalize_prose(solution(R,A,B,N))
    answer_values=[normalize_vector_layout(z if isinstance(z,str) else vec(z)) for z in values]
    # All identities are derived after presentation normalization.
    h=digest([level,problem,worked,sorted(answer_values),answer_values[0]])
    answers=[{':answer/id':uid(h+':answer:'+z),':answer/type':{':db/ident':':answer.type/math'},':answer/value':z} for z in answer_values]
    correct=answers[0][':answer/id'];rng.shuffle(answers)
    q={':question/id':uid(h),':question/problem':problem,':question/worked-solution':worked,
       ':question/difficulty':{':db/ident':':question.difficulty/'+level},
       ':question/answer-fields':[{':answer-field/id':uid(h+':field'),':answer-field/key':'selection',
           ':answer-field/type':{':db/ident':':answer-field.type/radio'},':answer-field/choices':answers,
           ':answer-field/correct':[':answer/id',correct]}]}
    record={'knowledge_point':KP,'question':q,'generation':dict(metadata or {},version=VERSION,
        semantic_fingerprint=digest([signature(A),signature(B)]),
        error_recipes=dict(zip(answer_values,recipes)),domain='all real u,v; zero products at singular parameters allowed',
        dependencies={'python':sys.version.split()[0],'sympy':s.__version__})}
    validate_generated_record(record)
    return record


def generate(level,seed=0,family=None,parameters=None):
    if level not in FAMILIES:raise ValueError('Unknown difficulty')
    rng=random.Random(seed);family=family or rng.choice(FAMILIES[level])
    if family not in FAMILIES[level]:raise ValueError('Family outside authored band')
    p=parameters or {'a':rng.choice((-1,1)),'b':rng.choice((-1,1)),
       'c':rng.choice((-2,-1,1,2)) if level=='easy' else rng.choice((-1,1)),
       'd':rng.choice((-2,-1,1,2)) if level=='easy' else rng.choice((-1,1)),
       'permutation':rng.choice(tuple(itertools.permutations(range(3)))),
       'swap':bool(rng.getrandbits(1)), 'signs':tuple(rng.choice((-1,1)) for _ in range(3)),
       'profile':rng.choice(('mixed','derivatives','orientation'))}
    R,A,B=transform(base_instance(family,**{k:p.get(k,1) for k in ('a','b','c','d')}),
                     p.get('permutation',(0,1,2)),p.get('swap',False),p.get('signs',(1,1,1)),p.get('translation',(0,0,0)))
    values,recipes=bank(A,B,cross(A,B),rng,p.get('profile','mixed'),R)
    return make_record(level,R,A,B,values,recipes,rng,{'seed':seed,'family':family,'profile':p.get('profile','mixed'),'parameters':p,
        'source_ids':(['f1b86df9-267c-5991-bc04-39d7b75cdf3a'] if family=='tutorial-cylinder' else
                      ['cf9a45d8-93e4-5a5c-8ad1-796e86ba6570'] if family=='separated-trigonometric' else
                      [SOURCE_IDS[3]] if family=='mixed-trigonometric' else
                      [SOURCE_IDS[2]] if family=='separated-powers' else
                      [SOURCE_IDS[1]] if family=='graph-exponential' else
                      [SOURCE_IDS[0]] if family=='graph-quadratic' else
                      [EXEMPLARS[0]] if family=='graph-bilinear' else
                      [EXEMPLARS[1]] if family=='dense-polynomial' else [EXEMPLARS[2]])})


def replay(index):
    source=json.loads((HERE/'source-replay.json').read_text())[index]
    family=('graph-quadratic','graph-exponential','separated-powers','mixed-trigonometric','separated-trigonometric')[index]
    params=({'c':1,'d':-1},{'c':1,'d':-1},{'c':2,'d':1},{'c':1,'d':1},{'a':1,'b':1,'c':4})[index]
    R,A,B=base_instance(family,**params)
    f=source[':question/answer-fields'][0];key=f[':answer-field/correct'][':answer/id']
    choices=sorted(f[':answer-field/choices'],key=lambda a:a[':answer/id']!=key)
    return make_record('easy',R,A,B,[a[':answer/value'] for a in choices],['source choice; error intent may be opaque']*5,
                       random.Random(index),{'family':'source-replay','source_ids':[source[':question/id']], 'original_difficulty':'easy'},source[':question/problem'])


def replay_exemplar(index):
    record=json.loads((HERE/'replay-exemplars.json').read_text())[index]
    source=record['question'];level=('easy','moderate','hard')[index]
    family=('graph-bilinear','dense-polynomial','nested-sin')[index]
    R,A,B=base_instance(family)
    f=source[':question/answer-fields'][0];key=f[':answer-field/correct'][1]
    choices=sorted(f[':answer-field/choices'],key=lambda a:a[':answer/id']!=key)
    return make_record(level,R,A,B,[a[':answer/value'] for a in choices],['source choice']*5,
                       random.Random(index),{'family':'source-replay','source_ids':[source[':question/id']]},source[':question/problem'])


def unique_bank_ranks(record):
    """Choice-only rank signatures at a fixed ordinary positive parameter point.

    Do not let every repeated visible family in a finite batch share one such
    answer-producing action. Ties are deliberately not unique decisions.
    """
    choices=record['question'][':question/answer-fields'][0][':answer-field/choices']
    key=record['question'][':question/answer-fields'][0][':answer-field/correct'][1]
    # Values are generated from the instance model; map the displayed choices
    # back to error vectors, without parsing arbitrary external TeX.
    p=record['generation']['parameters'];family=record['generation']['family']
    R,A,B=transform(base_instance(family,**{k:p.get(k,1) for k in ('a','b','c','d')}),
        p.get('permutation',(0,1,2)),p.get('swap',False),p.get('signs',(1,1,1)),p.get('translation',(0,0,0)))
    N=cross(A,B);groups=error_pool(A,B,N,R)
    vectors={normalize_vector_layout(vec(M)):M for group in groups.values() for _,M in group}
    vectors[normalize_vector_layout(vec(N))]=N
    ki=next(i for i,a in enumerate(choices) if a[':answer/id']==key)
    ranks=set()
    for component in range(3):
        values=[float(vectors[a[':answer/value']][component].subs({u:2,v:3}).evalf()) for a in choices]
        if values.count(values[ki])==1:
            ranks.add((component,sorted(values).index(values[ki])))
    return ranks


def place_key(record,position):
    field=record['question'][':question/answer-fields'][0]
    choices=field[':answer-field/choices'];key=field[':answer-field/correct'][1]
    current=next(i for i,a in enumerate(choices) if a[':answer/id']==key)
    choices[current],choices[position]=choices[position],choices[current]


def batch(level,count,seed):
    if count<0:raise ValueError('Negative count')
    rng=random.Random(seed);records=[];seen=set();cycle=[];attempts=0
    common_ranks={};positions=[];family_positions={}
    while len(records)<count:
        if not cycle:cycle=list(FAMILIES[level]);rng.shuffle(cycle)
        family=cycle[-1];attempts+=1
        if attempts>max(1000,count*100):raise ValueError('Unique supported semantic domain exhausted')
        itemseed=rng.getrandbits(64)
        try:record=generate(level,itemseed,family)
        except ValueError:continue
        fp=record['generation']['semantic_fingerprint']
        if fp in seen:continue
        ranks=unique_bank_ranks(record)
        # For the first repeated family, require a different bank action;
        # later members preserve the empty intersection already established.
        if family in common_ranks and common_ranks[family] & ranks:continue
        if not positions:
            positions=list(range(5));rng.shuffle(positions)
        used=family_positions.get(family,set())
        eligible=[pos for pos in positions if pos not in used]
        if not eligible:
            used=set();eligible=list(positions)
        position=eligible[-1];positions.remove(position);used.add(position)
        family_positions[family]=used
        place_key(record,position)
        common_ranks[family]=ranks if family not in common_ranks else common_ranks[family] & ranks
        records.append(record);seen.add(fp);cycle.pop()
    return records


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=('easy','moderate','hard','unclassified'),default='easy')
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=('json',),default='json')
    ap.add_argument('--replay-source',type=int,choices=range(5))
    ap.add_argument('--replay-exemplar',type=int,choices=range(3))
    args=ap.parse_args()
    records=[replay_exemplar(args.replay_exemplar)] if args.replay_exemplar is not None else [replay(args.replay_source)] if args.replay_source is not None else batch('easy' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(records,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
