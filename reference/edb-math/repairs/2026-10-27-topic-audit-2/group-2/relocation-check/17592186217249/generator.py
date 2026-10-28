#!/usr/bin/env python3
"""Seeded, relocatable integrating-factor generator. No services or assets."""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import random
import uuid
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

X, Y = s.symbols('x y', positive=True)
KP = {'db_id': 17592186217249, 'id': '161b35e2-52bf-5f27-9fc3-bfe34eeb7935',
      'title': 'Finding an Integrating Factor for an Inexact Equation: Condition on Y Satisfied'}
SOURCES = {'easy': [17592186217763, 17592186311863], 'moderate': [17592186311873], 'hard': ['ec002adb-9111-59ec-9edd-86ddca0c8fc6']}
RATIO = r'\frac{1}{P}\left(\frac{\partial P}{\partial y}-\frac{\partial Q}{\partial x}\right)'
FORMULA = r'\exp\left(-\int h(y)\,\mathrm{d}y\right)'

def tex(e):
    return normalize_tex(s.latex(e, mul_symbol=None).replace(r'\log',r'\ln'))

def display(t):
    return '\n\n$$\n' + t + '\n$$\n\n'

def aligned(rows):
    return display(r'\begin{aligned}' + r' \\ '.join(rows) + r'\end{aligned}')

def differential(p,q):
    return r'\left(' + tex(p) + r'\right)\,\mathrm{d}x+\left(' + tex(q) + r'\right)\,\mathrm{d}y=0'

def differential_choice(p,q):
    return (r'\begin{aligned}&\left('+tex(p)+r'\right)\,\mathrm{d}x'
            +r'\\ &{}+\left('+tex(q)+r'\right)\,\mathrm{d}y=0\end{aligned}')

def eq_with_factor(factor, equation, q_terms=None):
    left,right=equation.removesuffix('=0').split(r'\,\mathrm{d}x+',1)
    tail=(r'\\ &\quad {}+'+right if q_terms is None else ''.join(
        r'\\ &\quad {}+\left('+tex(term)+r'\right)\,\mathrm{d}y' for term in q_terms))
    return (r'\begin{aligned}&\left(' + tex(factor) + r'\right)\, ['
            + r'\\ &\quad '+left+r'\,\mathrm{d}x'+tail+r']=0\end{aligned}')

def unique_bank(correct, candidates, count):
    out = [correct]
    for value in candidates:
        if all(s.simplify(value-v) != 0 for v in out):
            out.append(value)
        if len(out) == count:
            return out
    raise ValueError('Insufficient distinct distractors')

def make_instance(difficulty, params):
    n,a = params['n'],params['a']
    if difficulty == 'easy':
        b = params['b']
        if n == 2 and b == 2*a:
            raise ValueError('Already exact; integrating-factor operation absent')
        p,q = a*Y**n,b*X*Y
        h = n/Y - s.Rational(b,a)*Y**(1-n)
        if n == 2:
            k = s.Rational(b,a)-2
            anti = -k*s.log(Y)
            factor = Y**k
            factors = unique_bank(factor, [Y**(-k),Y**(k+1),Y**(k-1),Y**(k+2)],3)
        else:
            t = -s.Rational(b,a*(n-2))*Y**(2-n)
            anti = n*s.log(Y)-t
            factor = Y**(-n)*s.exp(t)
            factors = [factor,Y**(-n+1)*s.exp(t),Y**(-n)*s.exp(-t)]
    elif difficulty == 'moderate':
        c,d = params['c'],params['d']
        f = a*Y**n+d
        p,q = X*f,c*Y**(n-1)
        h = a*n*Y**(n-1)/f
        anti = s.log(f)
        factor = 1/f
        factors = [factor,f,s.exp(-f),s.exp(-a*n*Y)]
    else:
        raise ValueError('Unsupported difficulty: '+difficulty)
    return dict(p=p,q=q,py=s.diff(p,Y),qx=s.diff(q,X),h=s.factor(h),anti=anti,
                factor=factor,factors=factors,equation=differential(p,q))

def finish(problem,solution,banks,corrects,difficulty,params,refs,profile,rng):
    # Normalize all learner prose BEFORE deriving content identities.
    problem,solution = normalize_prose(problem),normalize_prose(solution)
    values = [[normalize_tex(v) for v in bank] for bank in banks]
    corrects = [normalize_tex(v) for v in corrects]
    payload = json.dumps([problem,solution,values,corrects,difficulty],sort_keys=True)
    identity = str(uuid.uuid5(uuid.NAMESPACE_URL,hashlib.sha256(payload.encode()).hexdigest()))
    fields=[]
    for i,(bank,keyed) in enumerate(zip(values,corrects),1):
        fid = str(uuid.uuid5(uuid.UUID(identity),'field-'+str(i)))
        choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
        rng.shuffle(choices)
        fields.append({':answer-field/id':fid,':answer-field/key':'field-'+str(i),':answer-field/type':':answer-field.type/select',
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(c[':answer/id'] for c in choices if c[':answer/value']==keyed)]})
    record={'knowledge_point':KP,'question':{':question/id':identity,':question/difficulty':':question.difficulty/'+difficulty,
            ':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},
            'generation':{'generator_version':'2.0.1','template':difficulty,'parameters':params,'source_question_ids':refs,
                          'bank_profile':profile,'domain':'y>0' if difficulty=='easy' else 'x>0,y>0'}}
    return validate_generated_record(record)

def generate_instance(difficulty,params,rng=None,power_profiles=None,avoid_mixed_ranks=(),avoid_moderate_ranks=()):
    rng = rng or random.Random(0)
    if difficulty=='hard':return generate_hard(params,rng)
    z=make_instance(difficulty,params)
    p,q,py,qx,h,anti,I = [z[k] for k in ['p','q','py','qx','h','anti','factor']]
    n,a=params['n'],params['a']
    if difficulty=='easy' and n==2:
        k=s.Rational(params['b'],a)-2
        offsets=(power_profiles[0] if power_profiles else rng.choice([[-2,-1,1],[-1,1,2],[-3,-2,-1],[1,2,3]]))
        z['factors']=[Y**k]+[Y**(k+j) for j in offsets]
        profile='power-exponent-'+','.join(map(str,offsets))
    elif difficulty=='easy':
        coefficient=-s.Rational(params['b'],a*(n-2))
        alternatives=rng.sample([-coefficient,2*coefficient,coefficient/2],3)
        for other in alternatives:
            z['factors']=[Y**r*s.exp(c*Y**(2-n)) for r in [-3,-4] for c in [coefficient,other]]
            key_value=float(I.subs(Y,2))
            rank=sum(float(v.subs(Y,2))<key_value for v in z['factors'])
            if rank not in avoid_mixed_ranks:break
        else:raise ValueError('No mixed error profile avoids the repeated batch rank')
        profile='power-exponential-grid-rank-'+str(rank)
    else:
        pairs=[(aa,dd) for aa in range(1,5) for dd in range(1,5) if aa!=a and dd!=params['d']
               and len({s.Rational(A,D) for A,D in [(a,params['d']),(a,dd),(aa,params['d']),(aa,dd)]})==4]
        # At y=2 reciprocal rank reverses denominator order. Vary complete
        # coefficient grids across the batch and each repeated exponent group;
        # shuffling positions alone cannot remove a fixed numerical-rank cue.
        def grid_rank(pair):
            aa,dd=pair
            return sum(A*2**n+D > a*2**n+params['d']
                       for A in [a,aa] for D in [params['d'],dd])
        pairs=[pair for pair in pairs if grid_rank(pair) not in avoid_moderate_ranks]
        if not pairs:raise ValueError('No moderate error profile avoids the repeated batch rank')
        other_a,other_d=rng.choice(pairs)
        moderate_rank=grid_rank((other_a,other_d))
        z['factors']=[1/(aa*Y**n+dd) for aa in [a,other_a] for dd in [params['d'],other_d]]
        profile='reciprocal-coefficient-grid-rank-'+str(moderate_rank)
    banks = [[RATIO,RATIO.replace('{P}', '{Q}'),RATIO.replace('-','+'),RATIO.replace('{P}','{Q}').replace('-','+')],
             [FORMULA,r'\exp(h(y))',r'\exp(-h(y))',r'\exp\left(\int h(y)\,\mathrm{d}y\right)']]
    corrects=[RATIO,FORMULA]
    problem='Find an integrating factor to convert the following differential equation into an **exact equation**. Select the correct options in the reasoning below.'
    if difficulty=='easy':
        problem += display(z['equation']+r',\qquad y>0')
    else:
        problem += display(tex(q)+r'\frac{\mathrm{d}y}{\mathrm{d}x}=-\left('+tex(p)+r'\right),\qquad x>0,\ y>0')
    problem += 'For an equation of the form'+display(r'P(x,y)\,\mathrm{d}x+Q(x,y)\,\mathrm{d}y=0')
    problem += 'if'+display('{{field-1}}=h(y)')+'where $h(y)$ is independent of $x$, an integrating factor is'+display('I(y)={{field-2}}')
    problem += r'Here $\exp(y)$ denotes $e^y$.'+'\n\n'
    if difficulty=='moderate':
        bank=[differential_choice(p,q),differential_choice(q,p),differential_choice(p,-q),differential_choice(p/X,X*q)]
        banks.append(bank);corrects.append(bank[0])
        problem += 'First rewrite the equation in differential form:'+display('{{field-3}}')
    if difficulty=='easy':problem += 'Denote'+display('P(x,y)='+tex(p)+r',\qquad Q(x,y)='+tex(q))
    else:problem += r'Let $P$ and $Q$ be the coefficients of $\mathrm{d}x$ and $\mathrm{d}y$ in that form.'+'\n\n'
    idx=len(banks)+1
    for derivative,variable,input_,value,candidates in [
        (r'\frac{\partial P}{\partial y}',Y,p,py,[p, Y, X, py/a, py+Y]),
        (r'\frac{\partial Q}{\partial x}',X,q,qx,[-qx,s.diff(q,Y),Y,X,q,qx+1])]:
        if variable==Y:
            coeff=a*n;other_coeff=rng.choice([v for v in [2,3,4,6,8,9,12,16] if v!=coeff])
            other_power=rng.choice([v for v in [1,2,3] if v!=n-1])
            bank=[c*Y**k*(X if difficulty=='moderate' else 1) for c in [coeff,other_coeff] for k in [n-1,other_power]]
        elif difficulty=='easy':
            other_magnitude=rng.choice([v for v in [1,2,3] if v!=abs(params['b'])])
            bank=[sgn*c*Y for sgn in [-1,1] for c in [abs(params['b']),other_magnitude]]
        else:bank=unique_bank(value,candidates,4)
        banks.append([tex(v) for v in bank]);corrects.append(tex(value))
        problem += ('Compute the partial derivatives:' if idx==(4 if difficulty=='moderate' else 3) else '')+display(derivative+'={{field-'+str(idx)+'}}');idx+=1
    if difficulty=='easy' and n==2:
        coefficient=s.simplify(h*Y)
        shifts=(power_profiles[1] if power_profiles else rng.choice([[-2,-1,1],[-1,1,2],[-3,-2,-1],[1,2,3]]))
        bank=[h]+[(coefficient+j)/Y for j in shifts]
    elif difficulty=='easy':
        other_n=rng.choice([v for v in [2,3,4] if v!=n])
        bank=[nn/Y+sgn*s.Rational(params['b'],a)*Y**(1-n) for nn in [n,other_n] for sgn in [-1,1]]
    else:
        # Each denominator comes from one complete reciprocal grid. Different
        # coefficient ratios ensure neither duplicate ratios nor constant multiples.
        bank=[s.cancel(-s.diff(mu,Y)/mu) for mu in z['factors']]
    banks.append([tex(s.factor(v)) for v in bank]);corrects.append(tex(h))
    problem+='For this equation,'+display(RATIO+'={{field-'+str(idx)+'}}');idx+=1
    problem+='This depends on $y$ only, so'+display('I(y)={{field-'+str(idx)+'}}');idx+=1
    banks.append([tex(v) for v in z['factors']]);corrects.append(tex(I))
    problem+='Multiplying gives the exact equation'+display('{{field-'+str(idx)+'}}')
    banks.append([eq_with_factor(v,z['equation']) for v in z['factors']]);corrects.append(eq_with_factor(I,z['equation']))
    solution='For an equation in differential form, the condition is'+display(RATIO+'=h(y)')+'with $h(y)$ independent of $x$. Then'+display('I(y)='+FORMULA)
    if difficulty=='moderate':
        solution+=r'Multiplying the derivative equation by $\mathrm{d}x$ and moving its right side to the left gives'+display(z['equation'])
    solution+='Set'+display('P(x,y)='+tex(p)+r',\qquad Q(x,y)='+tex(q))
    solution+='Compute the partial derivatives:'+aligned([
        r'\frac{\partial P}{\partial y}&=\frac{\partial}{\partial y}\left('+tex(p)+r'\right)='+tex(py),
        r'\frac{\partial Q}{\partial x}&=\frac{\partial}{\partial x}\left('+tex(q)+r'\right)='+tex(qx)])
    solution+='Therefore,'+aligned([RATIO+r'&=\frac{1}{'+tex(p)+r'}\left[\left('+tex(py)+r'\right)-\left('+tex(qx)+r'\right)\right]',r'&='+tex(h)])
    if difficulty=='easy' and n>2:solution+='Separating the powers gives'+display('h(y)='+tex(s.expand(h)))
    solution+='The ratio depends on $y$ only. On the stated domain,'
    rows=[r'I(y)&=\exp\left(-\int\left('+tex(s.expand(h))+r'\right)\,\mathrm{d}y\right)',
          r'&=\exp\left(-\left('+tex(anti)+r'\right)\right)']
    if difficulty=='easy' and n>2:
        t=-s.Rational(params['b'],a*(n-2))*Y**(2-n)
        rows.append(r'&=\exp\left(-'+str(n)+r'\ln y\right)\exp\left('+tex(t)+r'\right)')
    rows.append(r'&='+tex(I));solution+=aligned(rows)
    solution+='We choose the arbitrary nonzero constant multiplier to be $1$. Here $y>0$ permits the logarithm and exponential conversion. Multiplying the original equation by this factor gives'+display(eq_with_factor(I,z['equation']))
    return finish(problem,solution,banks,corrects,difficulty,params,([17592186217002]+SOURCES[difficulty] if difficulty=='easy' and n==2 else SOURCES[difficulty]),profile,rng)

def hard_instance(params):
    u,v,t=params['u'],params['v'],params['t']
    if u not in [-1,1] or v not in [1,2] or t not in [1,2]:raise ValueError('Outside hard domain')
    p=2*Y*(X+t*Y)
    q=(1-v)*X**2+2*t*(2-v)*X*Y-u*X**2*Y-2*u*t*X*Y**2
    h=u+v/Y
    return dict(p=p,q=q,py=s.diff(p,Y),qx=s.diff(q,X),h=h,anti=u*Y+v*s.log(Y),factor=Y**(-v)*s.exp(-u*Y))

def generate_hard(params,rng):
    z=hard_instance(params)
    p,q,py,qx,h,anti,I=[z[k] for k in ['p','q','py','qx','h','anti','factor']]
    ratios=[u+v/Y for u in [-1,1] for v in [1,2]]
    factors=[Y**(-v)*s.exp(-u*Y) for u in [-1,1] for v in [1,2]]
    equation=differential(p,s.factor(q))
    q_terms=s.Add.make_args(s.expand(q))
    problem='Find an integrating factor depending only on $y$ for'+display(r'\left('+tex(q)+r'\right)\frac{\mathrm{d}y}{\mathrm{d}x}=-\left('+tex(p)+r'\right)')
    problem+='Work on the domain $x>0$, $y>0$.\n\n'
    problem+=r'Rewrite as $P\,\mathrm{d}x+Q\,\mathrm{d}y=0$, with $P='+tex(p)+r'$. Compute the ratio and simplify before choosing:'+display(r'\frac{P_y-Q_x}{P}={{field-1}}')
    problem+='Use this ratio to choose an integrating factor:'+display('I(y)={{field-2}}')
    problem+='Choose the **exact equation** obtained by multiplying the original differential equation by that factor:'+display('{{field-3}}')
    solution=r'Move the right side to the left and multiply by $\mathrm{d}x$:'+display(equation)
    solution+='The coefficients and their partial derivatives are'+aligned(['P&='+tex(p),'Q&='+tex(q),'P_y&='+tex(py),'Q_x&='+tex(qx)])
    solution+='Subtract, factor, and cancel:'+aligned(['P_y-Q_x&='+tex(s.expand(py-qx)),r'&='+tex(s.factor(py-qx)),r'\frac{P_y-Q_x}{P}&=\frac{'+tex(s.factor(py-qx))+'}{'+tex(p)+'}',r'&='+tex(h)])
    solution+='The domain makes the canceled factors nonzero. This ratio depends on $y$ only. Apply the negative-integral formula:'+aligned(['I(y)&='+FORMULA,r'&=\exp\left(-\int\left('+tex(s.expand(h))+r'\right)\,\mathrm{d}y\right)',r'&=\exp\left(-\left('+tex(anti)+r'\right)\right)',r'&=\exp\left('+tex(-params['u']*Y)+r'\right)\exp\left(-'+str(params['v'])+r'\ln y\right)',r'&='+tex(I)])
    solution+=r'Since $y>0$, the logarithm conversion is valid. Choose the arbitrary nonzero multiplier as $1$. The multiplied equation, distributing $Q\,\mathrm{d}y$ across rows, is'+display(eq_with_factor(I,equation,q_terms))
    solution+='Its cross-partials agree:'+display(r'\frac{\partial(IP)}{\partial y}=\frac{\partial(IQ)}{\partial x}='+tex(s.factor(s.diff(I*p,Y))))
    return finish(problem,solution,[[tex(v) for v in ratios],[tex(v) for v in factors],[eq_with_factor(v,equation,q_terms) for v in factors]],
                  [tex(h),tex(I),eq_with_factor(I,equation,q_terms)],'hard',params,SOURCES['hard'],'linear-log-grid',rng)

def source_replay(entity_id):
    if entity_id in [17592186681040,17592186681060,17592186681093]:
        src=next(q for q in json.loads(Path(__file__).with_name('replay-exemplars.json').read_text()) if q[':db/id']==entity_id)
        difficulty=src[':question/difficulty'][':db/ident'].split('/')[-1]
        params={17592186681040:dict(n=3,a=1,b=2),17592186681060:dict(n=2,a=1,c=1,d=1),17592186681093:dict(u=1,v=1,t=1)}[entity_id]
        fs=sorted(src[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
        return finish(src[':question/problem'],src[':question/worked-solution'],[[a[':answer/value'] for a in f[':answer-field/choices']] for f in fs],
                      [f[':answer-field/correct'][':answer/value'] for f in fs],difficulty,params,[entity_id],'source-replay-published',random.Random(0))
    data=json.loads(Path(__file__).with_name('replay-data.json').read_text())
    source=next(q for q in data if q[':db/id']==entity_id)
    difficulty=source[':question/difficulty'][':db/ident'].split('/')[-1]
    params={17592186217763:dict(n=3,a=1,b=1),17592186311863:dict(n=3,a=2,b=-1),17592186311873:dict(n=3,a=1,c=1,d=1)}[entity_id]
    base=generate_instance(difficulty,params)
    banks=[];correct=[]
    for f in sorted(source[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
        bank=[c[':answer/value'] for c in f[':answer-field/choices']]
        if entity_id==17592186311873 and f[':answer-field/key']=='field-3':
            # Source options 1 and 4 are identical equations; retain archive,
            # replace just the second with an actual incorrect sign choice.
            bank[3]=differential(X*(Y**3+1),-Y**2)
        banks.append(bank);correct.append(f[':answer-field/correct'][':answer/value'])
    return finish(base['question'][':question/problem'],base['question'][':question/worked-solution'],banks,correct,difficulty,params,[entity_id],'source-replay-corrected' if difficulty=='moderate' else 'source-replay',random.Random(0))

def spread_positions(records,rng):
    # Per recognizable response shape, cycle independently shuffled positions for each
    # field. A two-item subgroup must not accidentally deliver a fixed-position key.
    cycles={}
    for r in records:
        p=r['generation']['parameters'];d=r['generation']['template']
        group=(d,p.get('n','linear-log'))
        for i,f in enumerate(r['question'][':question/answer-fields']):
            choices=f[':answer-field/choices'];key=f[':answer-field/correct'][1]
            slot=(group,i,len(choices));cycle=cycles.setdefault(slot,[])
            if not cycle:cycle.extend(rng.sample(range(len(choices)),len(choices)))
            target=cycle.pop()
            selected=next(j for j,c in enumerate(choices) if c[':answer/id']==key)
            choices[target],choices[selected]=choices[selected],choices[target]
    return records

def generate(difficulty,count,seed):
    if difficulty=='unclassified':difficulty='easy'
    if difficulty not in SOURCES:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed)
    if difficulty=='hard':
        catalog=[dict(u=u,v=v,t=t) for u,v,t in itertools.product([-1,1],[1,2],[1,2])]
        rng.shuffle(catalog)
        if count>len(catalog):raise ValueError('Finite semantic catalog exhausted')
        records=[generate_instance('hard',p,rng) for p in catalog[:count]]
        for i,r in enumerate(records):r['generation'].update(seed=seed,batch_index=i)
        return spread_positions(records,rng)
    # A shuffled cycle covers reasoning branches before incidental magnitudes.
    roles=list(itertools.product([2,3,4],[-1,1])) if difficulty=='easy' else [(n,1) for n in [2,3,4]]
    records=[];seen=set();cycle=[];factor_profiles=[];ratio_profiles=[];mixed_ranks={};moderate_ranks={}
    while len(records)<count:
        if not cycle:cycle=roles.copy();rng.shuffle(cycle)
        n,sign=cycle.pop()
        params={'n':n,'a':rng.randint(1,4)}
        if difficulty=='easy':params['b']=sign*rng.randint(1,3)
        else:params.update(c=rng.randint(1,4),d=rng.randint(1,4))
        marker=tuple(sorted(params.items()))
        if marker in seen or (difficulty=='easy' and n==2 and params['b']==2*params['a']):continue
        profiles=None
        if difficulty=='easy' and n==2:
            # Each profile puts the key at a different exponent rank. Cycle
            # independently for the factor and ratio; random independent draws
            # can make an entire delivered power subgroup answerable by rank.
            choices=[[-2,-1,1],[-1,1,2],[-3,-2,-1],[1,2,3]]
            if not factor_profiles:factor_profiles=rng.sample(choices,len(choices))
            if not ratio_profiles:ratio_profiles=rng.sample(choices,len(choices))
            profiles=(factor_profiles.pop(),ratio_profiles.pop())
        avoid=set()
        if difficulty=='easy' and n>2:
            for group in ['mixed',n]:
                history=mixed_ranks.get(group,[])
                if history and len(set(history))==1:avoid.add(history[0])
        moderate_avoid=set()
        if difficulty=='moderate':
            for group in ['moderate',n]:
                history=moderate_ranks.get(group,[])
                if history and len(set(history))==1:moderate_avoid.add(history[0])
        try:
            r=generate_instance(difficulty,params,rng,power_profiles=profiles,
                                avoid_mixed_ranks=avoid,avoid_moderate_ranks=moderate_avoid)
        except ValueError as error:
            if difficulty=='moderate' and str(error)=='No moderate error profile avoids the repeated batch rank':
                # Do not retire this valid assignment: once the subgroup has
                # varied ranks, it is eligible again, including full catalogs.
                continue
            raise
        seen.add(marker)
        if difficulty=='moderate':
            rank=int(r['generation']['bank_profile'].rsplit('-',1)[1])
            for group in ['moderate',n]:moderate_ranks.setdefault(group,[]).append(rank)
        if difficulty=='easy' and n>2:
            rank=int(r['generation']['bank_profile'].rsplit('-',1)[1])
            for group in ['mixed',n]:mixed_ranks.setdefault(group,[]).append(rank)
        r['generation'].update(seed=seed,batch_index=len(records));records.append(r)
        # Finite semantic catalog, never fake extra instances by shuffling.
        if len(seen)==(71 if difficulty=='easy' else 192) and len(records)<count:raise ValueError('Finite semantic catalog exhausted')
    return spread_positions(records,rng)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='easy');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');args=ap.parse_args()
    if args.count<0:ap.error('count must be nonnegative')
    # Easy: 72 parameter assignments minus b=2a for (a,b)=(1,2), n=2.
    cap=71 if args.difficulty in ['easy','unclassified'] else 8 if args.difficulty=='hard' else 192
    if args.count>cap:ap.error('Requested count exceeds finite supported catalog')
    print(json.dumps(generate(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
