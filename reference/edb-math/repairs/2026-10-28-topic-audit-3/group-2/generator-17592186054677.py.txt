#!/usr/bin/env python3
"""Seeded implicit-product differentiation. No IO except CLI output and replay fixtures."""
import argparse
from collections import Counter
import math
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION='1.0.4'
x,y,z=s.symbols('x y z',real=True)
KP={'db_id':17592186054677,'id':'619182bf-107d-5217-a306-ec4f7c1109eb','title':'Finding the Derivative of a Function Given in Implicit Form Using the Product Rule'}
ANCHORS={'easy':['5da798c0-eff7-5dba-adf8-d976d10d73c3','af328f52-53a1-5cc1-a542-6cad8eea4c44'], 'sin':['cf25af3d-9878-567e-91a7-d51ce920ad85','454b7cf5-7862-57c7-a910-8dbc0dac1fcc'], 'cos':['56e6a335-1c6d-5f20-b447-7c7858535bf5'], 'log':['3f5ae45c-0d29-593f-abd0-85c3a45aaf13'], 'exp':['7f4c216f-b191-5d84-8924-850e05c75712','f3116e79-f97e-5cc4-bde9-874a3e1f4d65'], 'hard':['8e608f41-f7b0-5fa0-8ef4-bed7e273d142']}
# Complete profiles, chosen before parameters; pairs refer to numerator/denominator errors.
PROFILES={
 'transpose-grid':[(0,0),(1,0),(0,1),(1,1),(2,2)],
 'factor-grid':[(0,0),(1,0),(0,2),(1,2),(2,1)],
 'omission-grid':[(0,0),(2,0),(0,1),(2,1),(1,2)],
 'power-grid':[(0,0),(2,0),(0,2),(2,2),(1,1)]}



def tex(expr):
    return normalize_tex(s.latex(expr,ln_notation=True))


def factor(kind,q):
    # Explicit instructional derivative rules. CAS differentiation is validation only.
    return {'one':(s.Integer(1),s.Integer(0)), 'power':(y**q,q*y**(q-1)),
            'sin':(s.sin(y),s.cos(y)), 'cos':(s.cos(y),-s.sin(y)),
            'log':(s.log(y),1/y),'exp':(s.exp(y),s.exp(y))}[kind]


def term(t):
    c,p,k,q=t;g,dg=factor(k,q)
    return c*x**p*g


def derivative_parts(ts):
    a=[];b=[]
    for c,p,k,q in ts:
        g,dg=factor(k,q)
        a.append(c*p*x**(p-1)*g if p else s.Integer(0))
        b.append(c*x**p*dg)
    return sum(a,s.Integer(0)),sum(b,s.Integer(0))


def quotient(n,d):
    # Keep exactly the collection form shown in feedback, not a CAS normal form.
    return normalize_tex(r'\frac{'+tex(n)+'}{'+tex(d)+'}')


def algebra(spec):
    L,R=spec['left'],spec['right']
    a,b=derivative_parts(L);c,d=derivative_parts(R)
    return a,b,c,d,c-a,b-d


def bank(spec,profile, return_expressions=False, return_parts=False):
    a,b,c,d,n,den=algebra(spec)
    # Numerator errors: wrong transposition; omit the left product's independent term.
    ns=[n,c+a,c] if c!=0 else [n,a,s.Integer(0)]
    # Denominator errors: omit a derivative contribution; wrong derivative of a factor.
    mixed=spec['left'][0]; co,p,k,q=mixed;g,dg=factor(k,q)
    mixed_b=co*x**p*dg
    omission=den-mixed_b
    if omission==0: omission=den/(p+1)  # replay-only single-product shape
    wrong_factor=den-mixed_b+co*x**p*(g if k!='exp' else s.Integer(1))
    if s.expand(wrong_factor-den)==0:
        wrong_factor=den-mixed_b+co*x**p*(dg/(q if q>1 else 2))
    if len(spec['left'])>1:
        pure_b=derivative_parts([spec['left'][1]])[1]
        wrong_factor=den-pure_b+pure_b*y  # power rule: fail to reduce the y exponent
    ds=[den,omission,wrong_factor]
    if d!=0:
        ds[2]=b+d  # failure to transpose the opposing derivative term
    values=[]; expressions=[];parts=[]
    for cell in PROFILES[profile]:
        if cell=='missing-chain':
            # Genuine missing-y' error: move that term to the independent side.
            role=spec.get('chain_error_role','mixed')
            bt=mixed_b if role=='mixed' else derivative_parts([spec['left'][1]])[1]
            nn,dd=n-bt,den-bt
        else:
            i,j=cell;nn,dd=ns[i],ds[j]
        if dd==0:raise ValueError('zero distractor denominator')
        expr=nn/dd
        if any(s.cancel(expr-old)==0 for old in expressions):raise ValueError('equivalent choices')
        values.append(quotient(nn,dd));expressions.append(expr);parts.append((nn,dd))
    return parts if return_parts else expressions if return_expressions else values


def uid(label):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/implicit-product/'+label))


def make(spec, difficulty, profile='transpose-grid', rng=None, source=None):
    rng=rng or random.Random(0)
    # A regular relation that reduces to y^q=constant assesses no product rule.
    # Reject the whole algebraic family, not a seed or a particular coefficient.
    if source is None and len(spec['left'])==2 and len(spec['right'])==1:
        co,p,k,q=spec['left'][0];b,_,pk,pq=spec['left'][1];c,r,rk,_=spec['right'][0]
        if k=='power' and rk=='one' and q==pq and p==r and co*spec['constant']==b*c:
            raise ValueError('constant regular branches eliminate the assessed operation')
    a,b,c,d,n,den=algebra(spec)
    L=sum(map(term,spec['left']),s.Integer(0)); R=sum(map(term,spec['right']),s.Integer(0))+spec['constant']
    condition=' This relation requires $y>0$.' if any(t[2]=='log' for t in spec['left']+spec['right']) else ''
    problem=normalize_prose(r'Calculate $\dfrac{\mathrm{d}y}{\mathrm{d}x}$ for $'+tex(L)+'='+tex(R)+'$.'+condition)
    # Derivative rows are assembled from explicit per-term operator inputs.
    rows=[]
    for t in spec['left']+spec['right']:
        if t[1] and t[2]!='one':
            aa,bb=derivative_parts([t])
            rows.append(r'\frac{\mathrm{d}}{\mathrm{d}x}\left('+tex(term(t))+r'\right)&='+tex(aa+bb*z).replace('z',"y'"))
    def equation_rows(lhs,rhs,split=False):
        # Break long hard-band right sides at actual additive terms. The
        # continuation retains its sign and equality alignment, never a code block.
        terms=s.Add.make_args(rhs) if split else (rhs,)
        terms=sorted(terms,key=s.default_sort_key)
        first_term=tex(terms[0]).replace('z',"y'")
        result=lhs+'&='+first_term
        for more in terms[1:]:
            negative=more.could_extract_minus_sign()
            result+=r'\\'+'\n'+r'&\quad '+('-' if negative else '+')+tex(-more if negative else more).replace('z',"y'")
        return result
    first=equation_rows(tex(a+b*z).replace('z',"y'"),c+d*z,difficulty=='hard')
    second=equation_rows(r'\left('+tex(den)+r'\right)y^{\prime}',n,difficulty=='hard')
    collector_separator=('\n'+r'\end{aligned}'+'\n$$\n\n$$\n'+r'\begin{aligned}'+'\n') if difficulty=='hard' else (r'\\'+'\n')
    key=quotient(n,den)
    solution=("Treat $y$ as a function of $x$ and write $y'=\\dfrac{\\mathrm{d}y}{\\mathrm{d}x}$. "
              'Use the **product rule** for each mixed product, including the chain-rule factor $y^{\\prime}$ when differentiating a function of $y$.\n\n'
              '$$\n'+r'\begin{aligned}'+'\n'+r'\\'.join(rows)+'\n'+r'\end{aligned}'+'\n$$\n\n'
              'Differentiate the equation, collect all terms containing $y^{\\prime}$, and factor:\n\n'
              '$$\n'+r'\begin{aligned}'+'\n'+first+collector_separator+second+'\n'+r'\end{aligned}'+'\n$$\n\n'
              'Divide by the coefficient of $y^{\\prime}$:\n\n$$\n'+r'\frac{\mathrm{d}y}{\mathrm{d}x}='+key+'\n$$\n\n'
              'This formula applies where $'+tex(den)+r'\ne0$.'+condition)
    solution=normalize_prose(solution)
    values=bank(spec,profile) if source is None else [normalize_tex(v.replace('\u2061','')) for v in source['bank']]
    key_index=0 if source is None else source['correct_index']
    if source:
        problem=normalize_prose(source['problem'].replace('\u2061',''))
        solution=normalize_prose(source['solution'].replace('\u2061',''))
    canonical=json.dumps([difficulty,problem,values,solution],sort_keys=True)
    h=hashlib.sha256(canonical.encode()).hexdigest()
    answers=[{':answer/id':uid(h+'/choice/'+str(i)),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
    correct=answers[key_index][':answer/id'];rng.shuffle(answers)
    field={':answer-field/id':uid(h+'/field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
    family='hard-'+spec['left'][0][2] if difficulty=='hard' else ('polynomial' if difficulty=='easy' else spec['left'][0][2])
    refs=[source['source_id']] if source else ANCHORS['hard' if difficulty=='hard' else 'easy' if difficulty=='easy' else spec['left'][0][2]]
    record={'knowledge_point':KP.copy(),'question':{':question/id':uid(h),':question/problem':problem,':question/difficulty':':question.difficulty/'+difficulty,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'generator_version':VERSION,'template':family,'bank_profile':profile if not source else 'source-replay','parameters':spec,'source_question_ids':refs,'displayed_final':key,'domain':'y>0 and derivative denominator nonzero' if 'log' in family else 'derivative denominator nonzero'}}
    return validate_generated_record(record)


def sample_spec(difficulty,family,rng):
    # Select roles/exponents/signs first; coefficients follow.
    p=rng.choice([1,2] if difficulty=='hard' else [1,2,3])
    q=rng.choice([1,2,3]) if difficulty=='easy' else 1
    pure_q=2 if difficulty=='hard' else rng.choice([1,2,3])
    sign=rng.choice([-1,1]);right_sign=rng.choice([-1,1])
    r=rng.choice([1,2] if difficulty=='hard' else [2,3])
    mixed_sign=rng.choice([-1,1]) if difficulty=='hard' else 1
    chain_role=rng.choice(['mixed','pure'])
    co=rng.choice([1,2,3]);b=sign*rng.choice([1,2,3]);c=rng.choice([1,2,3])
    kind='power' if difficulty=='easy' else family
    L=[(mixed_sign*co,p,kind,q),(b,0,'power',pure_q)]
    R=[(right_sign*c,r,'exp',1)] if difficulty=='hard' else [(c,r,'one',0)]
    return {'left':L,'right':R,'constant':rng.choice([-2,-1,0,1,2]),'chain_error_role':chain_role}


def bank_cues(record,spec,profile):
    """Test declared bank-only strategies; return those that select the key.

    Sampling two members of a visible family or repeated bank profile must
    break any shared strategy.
    Numerical ranks are diagnostic evaluations of the bank, never derivatives
    of the defining equation. They add no learner-facing prerequisite.
    """
    field=record['question'][':question/answer-fields'][0]
    choices=field[':answer-field/choices']
    key=next(i for i,a in enumerate(choices) if a[':answer/id']==field[':answer-field/correct'][1])
    texts=[a[':answer/value'] for a in choices]
    original=bank(spec,profile)
    lookup=dict(zip(original,bank(spec,profile,return_expressions=True)))
    values=[lookup[t] for t in texts]
    hits={'position-'+str(key+1)}
    lengths=list(map(len,texts))
    for name,score in [('shortest',min(lengths)),('longest',max(lengths))]:
        ids=[i for i,v in enumerate(lengths) if v==score]
        if ids==[key]:hits.add(name)
    # quotient() emits exactly two outer groups, whose texts are already known.
    # Use the displayed numerator and denominator for modal structure probes.
    def outer_group(t,start):
        depth=1;end=start+1
        while depth:
            depth+=(t[end]=='{')-(t[end]=='}');end+=1
        return t[start+1:end-1],end
    nums=[];dens=[]
    for text in texts:
        n,end=outer_group(text,5);d,end=outer_group(text,end)
        nums.append(n);dens.append(d)
    nc,dc=Counter(nums),Counter(dens)
    ids=[i for i in range(5) if nc[nums[i]]==max(nc.values()) and dc[dens[i]]==max(dc.values())]
    if ids==[key]:hits.add('modal-intersection')
    # A modal coefficient/argument cue can survive full-fraction tie checks.
    # Track each displayed numerator/denominator monomial, including absence.
    parts_lookup=dict(zip(original,bank(spec,profile,return_parts=True)))
    features=[]
    for text in texts:
        fs={}
        for side,part in zip(['n','d'],parts_lookup[text]):
            for summand in s.Add.make_args(s.expand(part)):
                coefficient,monomial=summand.as_coeff_Mul()
                fs[(side,str(monomial))]=coefficient
        features.append(fs)
    slots=set().union(*(set(fs) for fs in features));modes={}
    for slot in slots:
        frequencies=Counter(fs.get(slot,s.Integer(0)) for fs in features)
        modal=[v for v,n in frequencies.items() if n==max(frequencies.values())]
        if len(modal)==1:modes[slot]=modal[0]
    scores=[sum(fs.get(slot,s.Integer(0))==value for slot,value in modes.items()) for fs in features]
    if [i for i,score in enumerate(scores) if score==max(scores)]==[key]:hits.add('modal-coefficients')
    for j,(xx,yy) in enumerate([(s.Rational(7,5),s.Rational(3,5)),(-s.Rational(4,5),s.Rational(6,5))]):
        numbers=[complex(v.subs({x:xx,y:yy}).evalf()) for v in values]
        if any(abs(v.imag)>1e-9 or not math.isfinite(v.real) for v in numbers):continue
        order=sorted(range(5),key=lambda i:numbers[i].real)
        if any(abs(numbers[order[i]].real-numbers[order[i-1]].real)<1e-9 for i in range(1,5)):continue
        hits.add('rank-point-'+str(j)+'-'+str(order.index(key)+1))
    return hits


def generate(difficulty,count,seed):
    if difficulty=='unclassified':difficulty='moderate'
    rng=random.Random(seed);families=['power'] if difficulty=='easy' else ['sin','cos'] if difficulty=='hard' else ['sin','cos','log','exp']
    schedule=[];records=[];seen=set();rejections=0;family_cues={}
    for i in range(count):
        if not schedule:
            schedule=families.copy();rng.shuffle(schedule)
        family=schedule.pop()
        profile=rng.choice(list(PROFILES))
        for attempt in range(100):
            spec=sample_spec(difficulty,family,rng)
            try:rec=make(spec,difficulty,profile,rng)
            except ValueError:rejections+=1;continue
            # Semantic identity includes the actual relation, not seed or permutation.
            *_,numerator,denominator=algebra(spec)
            semantic=s.srepr(s.cancel(numerator/denominator))
            if semantic in seen:rejections+=1;continue
            cues=bank_cues(rec,spec,profile)
            groups=[family,family+'/'+profile]
            if any(family_cues.get(group,set()) & cues for group in groups):
                rejections+=1;continue
            for group in groups:
                previous=family_cues.get(group)
                family_cues[group]=cues if previous is None else previous & cues
            seen.add(semantic);break
        else:raise RuntimeError('Unable to construct distinct plausible answer bank')
        rec['generation'].update({'seed':seed,'index':i,'rejections_before_record':rejections})
        records.append(rec)
    return records


def replay_sources():
    fixtures=json.loads(Path(__file__).with_name('source-cases.json').read_text())
    return [make({k:f[k] for k in ['left','right','constant']},f['difficulty'],source=f) for f in fixtures]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json'],default='json');p.add_argument('--replay-source',action='store_true')
    a=p.parse_args()
    if a.count<0:p.error('--count must be nonnegative')
    records=replay_sources() if a.replay_source else generate(a.difficulty,a.count,a.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
