#!/usr/bin/env python3
"""Seeded scalar-function multiple rule practice. No services or runtime assets."""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import uuid
from pathlib import Path
import sympy as s
from algebra import T, KP_ID, KP_UUID, TITLE, QUESTIONS, SOURCE, parse, tex, vector, vector_read, read_prompt, equal, vequal
from math_format import normalize_prose, normalize_tex, validate_prose, validate_tex

VERSION='scalar-vector-3'
LEVELS=('easy','moderate','hard')
FAMILIES={'easy':('polynomial','logarithm'), 'moderate':('exponential','trigonometric'), 'hard':('nested_log',)}


def final_form(x):
    # Expand only distributive products; do not let a CAS choose trig identities.
    return s.expand_mul(x)


def vec(v):
    return normalize_tex(vector(v))


def display(text):
    return '\n\n$$\n'+text+'\n$$\n\n'


def normalized_record(level,prompt,solution,bank,correct,rng,metadata):
    prompt=normalize_prose(prompt.strip());solution=normalize_prose(solution.strip())
    bank=[normalize_tex(x) for x in bank]
    validate_prose(prompt);validate_prose(solution)
    for value in bank:validate_tex(value)
    identity=json.dumps([VERSION,level,prompt,solution,sorted(bank),bank[correct]],ensure_ascii=False)
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in bank]
    key=answers[correct][':answer/id'];rng.shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{
        ':question/id':qid,':question/difficulty':':question.difficulty/'+level,
        ':question/problem':prompt,':question/worked-solution':solution,
        ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',key]}]},
        'generation':{'version':VERSION,**metadata}}


def replay(qid,seed=0):
    """Replay eligible complete source banks only; no source is modified."""
    q=QUESTIONS[qid];u,v=read_prompt(q[':question/problem'])
    f=q[':question/answer-fields'][0];bank=[a[':answer/value'] for a in f[':answer-field/choices']]
    key=f[':answer-field/correct'][':answer/value'];correct=bank.index(key)
    level=q[':question/difficulty'][':db/ident'].split('/')[-1]
    sol=q[':question/worked-solution']
    # Source double-angle results require an explicit transition, not a silent CAS rewrite.
    if qid in ('q-70688','q-128473'):
        sol+='\n\nUse the identities $2\\sin t\\cos t=\\sin(2t)$ and $\\cos^2t-\\sin^2t=\\cos(2t)$ when collecting the trigonometric components.'
    return normalized_record(level,q[':question/problem'],sol,bank,correct,random.Random(seed),{
        'seed':seed,'template':'source_'+qid,'profile':'observed_'+qid,'source_ids':[q[':question/id']],
        'provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_replay':True})


def sample_instance(level,rng,family=None,parameters=None):
    family=family or rng.choice(FAMILIES[level])
    if family not in FAMILIES[level]:raise ValueError('family not in difficulty')
    # Roles/cases first, then small compatible numbers.
    profile=rng.choice(('signs','multiplicity'))
    branch=rng.choice(('cancel','survive'))
    perm=list(range(3));rng.shuffle(perm)
    sign=lambda:rng.choice((-2,-1,1,2))
    if parameters is None:
        p={'a':sign(),'b':rng.choice((-2,-1,0,1,2)),'n':rng.choice((1,2,3)),
           'k':rng.choice((-2,-1,1,2)),'coefficients':[sign() for _ in range(3)],'permutation':perm,
           'branch':branch,'profile':profile,'p':rng.choice((1,2)),'trig':rng.choice(('sin','cos')),
           'omit':rng.choice(('A','B'))}
    else:p=dict(parameters)
    a,b,n,k=p['a'],p['b'],p['n'],p['k'];c=p['coefficients']
    if family=='polynomial':
        u=a*T+b;v=[c[0]*T,c[1]*T**rng.choice((2,3)) if parameters is None else c[1]*T**n,c[2]]
        # Persist every sampled role parameter.
        p['n']=int(s.degree(v[1],T))
    elif family=='logarithm':
        n=max(2,n);p['n']=n
        u=a*s.log(T);v=[c[0]*T,c[1]*T**n,c[2]*T**(n+1)]
    elif family=='exponential':
        u=s.exp(k*T);rate=-k if p['branch']=='cancel' else k
        v=[c[0]*s.exp(rate*T),c[1]*T**n,c[2]]
    elif family=='trigonometric':
        fn=s.sin if p['trig']=='sin' else s.cos
        u=a*fn(T);v=[c[0]*s.sin(T),c[1]*s.cos(T),c[2]*s.exp(T)]
    else:
        power=p['p'];u=a*T**power*s.log(T)
        reciprocal=power if p['branch']=='cancel' else (2 if power==1 else 1)
        v=[c[0]*T**n,c[1]*s.exp(T),c[2]/T**reciprocal]
    v=[v[i] for i in p['permutation']]
    return family,p,u,v


def make(level,seed=0,family=None,parameters=None,name='f'):
    if level not in LEVELS:raise ValueError('difficulty')
    rng=random.Random(seed)
    for attempt in range(120):
        family,p,u,v=sample_instance(level,rng,family,parameters)
        # Construct the ordered learner derivation first; never simplify trig arguments.
        up=s.diff(u,T);vp=[s.diff(x,T) for x in v]
        A=[up*x for x in v];B=[u*x for x in vp]
        result=[final_form(x+y) for x,y in zip(A,B)]
        # Sample a complete bank from meaningful contribution errors rather than
        # fixing an algebraic relationship that reveals the key from choices alone.
        pool=[('subtract_vector',1,-1),('subtract_scalar',-1,1),
              ('negate_both',-1,-1),('omit_vector',1,0),('omit_scalar',0,1),
              ('double_scalar',2,1),('double_vector',1,2),
              ('double_scalar_subtract',2,-1),('double_vector_subtract',-1,2),
              ('double_scalar_only',2,0),('double_vector_only',0,2)]
        candidates=[]
        for label,ca,cb in pool:
            value=[final_form(ca*x+cb*y) for x,y in zip(A,B)]
            if not vequal(value,result) and not any(vequal(value,z[1]) for z in candidates):
                candidates.append((label,value))
        # Numeric signatures only screen bank geometry; exact tests above establish
        # distinctness. No answer is inferred from these diagnostic values.
        def numeric(value):
            return tuple(float(s.N(x.subs(T,s.Rational(13,10)))) for x in value)
        def near(x,y):return all(abs(a-b)<1e-8*(1+abs(a)+abs(b)) for a,b in zip(x,y))
        target=numeric(result)
        for bank_attempt in range(160):
            selected=rng.sample(candidates,4)
            values=[result]+[z[1] for z in selected]
            points=[target]+[numeric(z[1]) for z in selected]
            midpoints=[]
            for i in range(5):
                for j in range(5):
                    for k in range(j):
                        if i not in (j,k) and near(tuple(2*x for x in points[i]),tuple(x+y for x,y in zip(points[j],points[k]))):
                            midpoints.append(i)
            if set(midpoints)=={0}:continue
            # Avoid a complete vector assembled uniquely from coordinate modes.
            modes=[]
            for cidx in range(3):
                counts=[sum(abs(x[cidx]-y[cidx])<1e-8 for y in points) for x in points]
                modes.append({i for i,nc in enumerate(counts) if nc==max(counts)})
            if set.intersection(*modes)=={0}:continue
            recipes=[('correct',result)]+selected
            break
        else:
            if parameters is not None:raise ValueError('cannot form bank without geometry shortcut')
            continue
        break
    else:raise ValueError('could not form distinct complete bank')
    domain='t>0' if family in ('logarithm','nested_log') else 'real t'
    f=r'\mathbf '+name
    prompt='Find $'+r'\big(u(t)'+f+r'(t)\big)^{\prime}'+ '$, where'
    prompt+=display('u(t)='+tex(u)+r',\qquad '+f+'(t)='+vec(v)+'.')
    if domain=='t>0':prompt+='Assume $t>0$.'
    sol='Use the scalar function multiple rule:'
    sol+=display(r'\big(u(t)'+f+r'(t)\big)^{\prime}=u^{\prime}(t)'+f+'(t)+u(t)'+f+r'^{\prime}(t).')
    sol+='Differentiate the scalar and each vector component.'
    if family=='nested_log':
        power=p['p'];a=p['a']
        sol+=' The scalar is itself a product:'
        upstep=tex(a*power*T**(power-1))+r'\ln t+\big('+tex(a*T**power)+r'\big)\frac{1}{t}'
        sol+=display(r'u^{\prime}(t)='+upstep+'='+tex(up)+'.')
    else:sol+=display(r'u^{\prime}(t)='+tex(up)+'.')
    sol+=display(f+r'^{\prime}(t)='+vec(vp)+'.')
    sol+='Substitute both contributions and add corresponding components:'
    sol+=display(r'\begin{aligned}\big(u(t)'+f+r'(t)\big)^{\prime}&=\big('+tex(up)+r'\big)'+vec(v)+r'\\&\quad+\big('+tex(u)+r'\big)'+vec(vp)+r'.\end{aligned}')
    # Separate each distributed coordinate; full-vector intermediate sums can exceed the UI width.
    sol+='Write $'+r'\mathbf h(t)=u(t)'+f+'(t)$'+'. For each component, the two terms are:'
    rows=[r'h_{'+str(i+1)+r'}^{\prime}(t)&=\big('+tex(A[i])+r'\big)\\&\quad+\big('+tex(B[i])+r'\big)\\&='+tex(result[i]) for i in range(3)]
    sol+=display(r'\begin{aligned}'+r'\\'.join(rows)+r'.\end{aligned}')
    if family=='exponential':
        sol+='Combine exponential factors with $e^{at}e^{bt}=e^{(a+b)t}$; opposite exponents give a constant product.'
    if family=='nested_log' and p['branch']=='cancel':
        sol+=r'In the reciprocal-power component, the logarithmic contributions cancel; the remaining term comes from differentiating $\ln t$.'
    sol+=' Therefore,'+display(r'\big(u(t)'+f+r'(t)\big)^{\prime}='+vec(result)+'.')
    # Work signature strips only amplitudes/permutations, not meaningful slopes or offsets.
    def shape(x):
        _,body=s.factor_terms(s.sympify(x)).as_coeff_Mul();return s.srepr(body)
    signature=json.dumps([shape(u),sorted(shape(x) for x in v)],sort_keys=True)
    return normalized_record(level,prompt,sol,[vec(x) for x in values],0,rng,{
        'seed':seed,'template':family,'profile':'sampled_contribution_errors','parameters':p,'domain':domain,
        'source_ids':{'polynomial':['caf13fa2-de78-52bc-ba1b-170f27934a7b','28487445-4637-5ffc-a325-dcbc682a33b5'],
                      'logarithm':['f31a5c94-f740-5b67-b455-a131169207f5'],
                      'exponential':['3b0680d9-f905-5e2d-ad7e-963cf0c87370','1c08c320-55ed-59e1-87a0-c92a722748de'],
                      'trigonometric':['9d92bf36-e24a-53bf-b359-cf412f728c8a','35965478-f53a-5fac-81aa-ae163d831cd1'],
                      'nested_log':['97c145f1-410d-5b44-8ef5-8d31acd301e1','6bb0eded-7277-5ab5-8c13-bfc480403b1a']}[family],
        'work_signature':hashlib.sha256(signature.encode()).hexdigest(),'recipes':[x[0] for x in recipes],
        'difficulty_status':'authored extension','plots':'none'})


def batch(level,count,seed):
    if count==0:return []
    rng=random.Random(seed);records=[];seen=set()
    for attempt in range(max(500,count*200)):
        r=make(level,rng.getrandbits(64))
        signature=r['generation']['work_signature']
        if signature in seen:continue
        seen.add(signature);records.append(r)
        if len(records)==count:return records
    if count==0:return []
    raise ValueError('requested batch exceeds supported distinct work instances')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=(*LEVELS,'unclassified','all'),default='easy')
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=('json',),default='json');ap.add_argument('--replay')
    args=ap.parse_args()
    if args.count<0:ap.error('count must be nonnegative')
    level='easy' if args.difficulty=='unclassified' else args.difficulty
    rs=[replay(args.replay,args.seed)] if args.replay else [r for l in (LEVELS if level=='all' else (level,)) for r in batch(l,args.count,args.seed)]
    print(json.dumps(rs,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
