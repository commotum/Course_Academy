#!/usr/bin/env python3
"""Seeded implicit tangent slopes. Runtime is independent of the repository."""
import argparse
import hashlib
import json
import random
from pathlib import Path
from uuid import UUID, uuid5
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

x,y,D=s.symbols('x y D', real=True)
NS=UUID('49a022e8-f8df-4b62-8862-3d399ecb56a2')
KP={'db_id':17592186054846,'id':'2311a895-587e-5609-8a9f-9963b8cae372','title':'Finding the Slope of the Tangent Line to a Curve Given in Implicit Form at a Point'}
SUPPORT={
 'powers':['f4792eb7-cef8-5807-bfe2-869a28aaef03','c28848f1-0f0e-5f71-af80-24cc5f2fd9a4'],
 'quadratic':['421782a5-f8ee-574b-bd35-7a68ca94b6ef','8a6eb51f-6232-5a08-acf1-136f0d14a4d9'],
 'product':['a60708d4-334c-5573-85a8-fee34ba1a832','9c578341-fd5b-5ea9-b094-029b8faa3d2a','45bf2a7e-b636-5c97-90c2-25563ca38da6','178ea495-c20f-5cdc-a1d6-8971b012cd62'],
 'radical':['e593c2e1-263c-5294-9a7c-b566ea68ae19','85cec444-2f0a-598c-bff4-89c6e3584a08','0a97764f-f130-5df7-bef4-c5372f6f59c9','be11712d-8184-5176-b182-3e96ce7e8e3b'],
 'trig':['ffb47def-243e-5613-87da-6b6ae8fdf163','c73f48a1-5f73-5fca-87a5-5adf2b36d0e9'],
 'nested':['2fb02dfe-1197-5eea-8e09-14662f8ce8e4','703b0ae9-246b-57d0-a0af-5bee4dbafe4a','af328f52-53a1-5cc1-a542-6cad8eea4c44']}

def tex(v):
    return normalize_tex(s.latex(v).replace('D',r'\frac{dy}{dx}'))

def aligned(rows,left=False):
    if left: rows=['&'+row.replace('&','') for row in rows]
    return '$$\n'+r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}'+'\n$$'

def ident(payload): return str(uuid5(NS,payload))

def term(c,p,q):
    """A polynomial monomial and its hand-authored total derivative components."""
    f=c*x**p*y**q
    u=c*p*x**(p-1)*y**q if p else s.S.Zero
    v=c*q*x**p*y**(q-1) if q else s.S.Zero
    return f,u,v

def construct(family,params):
    """Return terms and explicit rule inputs, without asking a CAS to differentiate."""
    p=params
    if family=='powers':
        terms=[term(p['a'],p['p'],0),term(p['b'],0,p['q'])]
        notes='Apply the power rule and the chain rule, treating $y$ as a function of $x$.'
    elif family=='quadratic':
        terms=[term(p['a'],2,0),term(p['b'],1,1),term(p['c'],0,2)]
        notes='Treat $y$ as a function of $x$. Use the product rule on $xy$ and the chain rule on powers of $y$.'
    elif family=='product':
        terms=[term(p['a'],p['p'],p['q']),term(p['b'],p['r'],0),term(p['c'],0,p['t'])]
        notes='Treat $y$ as a function of $x$. Use the product rule on the mixed power term and the chain rule on powers of $y$.'
    elif family=='radical':
        h,j=p['h'],p['j']
        terms=[(s.sqrt(x+h),1/(2*s.sqrt(x+h)),s.S.Zero),(p['b']*s.sqrt(y+j),s.S.Zero,p['b']/(2*s.sqrt(y+j)))]
        notes='Treat $y$ as a function of $x$. Differentiate the square roots using the power and chain rules.'
    elif family=='trig':
        if p['orientation']=='ycosx':
            terms=[(p['a']*y*s.cos(x),-p['a']*y*s.sin(x),p['a']*s.cos(x)),term(p['b'],1,0)]
            notes=r'Treat $y$ as a function of $x$. Use the product rule on the cosine product; the derivative of $\cos(x)$ is $-\sin(x)$.'
        else:
            terms=[(p['a']*x*s.sin(y),p['a']*s.sin(y),p['a']*x*s.cos(y)),term(p['b'],0,1)]
            notes=r'Treat $y$ as a function of $x$. Use the product rule on the sine product and the chain rule on $\sin(y)$.'
    else:
        k,a,b=p['k'],p['a'],p['b'];E=s.exp(k*x*y)
        if p['orientation']=='x':
            terms=[(a*x*E,a*E+a*k*x*y*E,a*k*x*x*E),term(b,0,2)]
            outer=s.Add(a*E,a*x*E*(k*y+k*x*D),2*b*y*D,evaluate=False)
        else:
            terms=[(a*y*E,a*k*y*y*E,a*E+a*k*x*y*E),term(b,2,0)]
            outer=s.Add(a*E*D,a*y*E*(k*y+k*x*D),2*b*x,evaluate=False)
        inner=k*x*y
        notes=('Treat $y$ as a function of $x$. The outer product and the exponential chain rule both matter. First differentiate the exponential input:\n\n'+
               aligned([r'\frac{d}{dx}\left('+tex(inner)+r'\right)&='+tex(k*y+k*x*D),
                        r'\frac{d}{dx}\left('+tex(E)+r'\right)&='+tex(E*(k*y+k*x*D))]))
        return terms,notes,outer
    # Keep derivative contributions as separate products before collecting.
    components=[]
    for _,u,v in terms:
        if u!=0: components.append(u)
        if v!=0: components.append(v*D)
    return terms,notes,s.Add(*components,evaluate=False)

# Each complete profile has four interpretable wrong differentiation/isolation paths.
PROFILES=[('sign-and-power',['sign','omit-x-power','signed-omit-x-power','variable-sign-omit-y-power']),
          ('sign-and-denominator',['sign','no-division','signed-no-division','variable-sign-reciprocal']),
          ('sign-and-reciprocal',['sign','reciprocal','negative-reciprocal','variable-sign-power-or-division']),
          ('sign-and-y-power',['sign','omit-y-power','signed-omit-y-power','variable-sign-no-division'])]

def bank(m,U,V,p,profile,error_sign):
    power=p.get('p',2);ypower=p.get('q',2)
    candidates={'sign':-m,'omit-x-power':m/power,'signed-omit-x-power':-m/power,
      'omit-y-power':m*ypower,'signed-omit-y-power':-m*ypower,
      'no-division':-U,'signed-no-division':U,
      'reciprocal':1/m if m!=0 else s.nan,'negative-reciprocal':-1/m if m!=0 else s.nan,
      'variable-sign-omit-y-power':error_sign*m*ypower,
      'variable-sign-reciprocal':error_sign/m if m!=0 else s.nan,
      'variable-sign-power-or-division':error_sign*(m/power if p.get('family')=='powers' else -U),
      'variable-sign-no-division':error_sign*(-U)}
    # Both the isolation mistake and that mistake combined with a sign error
    # are eligible complete misconception paths. Choose that assignment first.
    if p.get('family')!='powers' and profile[0] in ['sign-and-power','sign-and-y-power']: return None
    values=[m]+[s.simplify(candidates[n]) for n in profile[1]]
    for i,z in enumerate(values):
        if z.has(s.nan,s.zoo,s.oo,-s.oo) or any(s.simplify(z-w)==0 for w in values[:i]): return None
    return values

def make(family,p,band,kind,rng,profile_index=None,error_sign=None):
    terms,notes,derivative=construct(family,p)
    lhs=s.Add(*(t[0] for t in terms)); U=s.Add(*(t[1] for t in terms)); V=s.Add(*(t[2] for t in terms))
    point={x:s.sympify(p['x0']),y:s.sympify(p['y0'])}
    C=s.simplify(lhs.subs(point));u=s.simplify(U.subs(point));v=s.simplify(V.subs(point))
    if v==0: raise ValueError('vertical or singular slope')
    m=s.simplify(-u/v)
    # Ratio form is the collected derivation; only endpoint arithmetic is simplified.
    ratio=r'-\frac{'+tex(U)+'}{'+tex(V)+'}'
    slope_eval=r'-\frac{'+tex(u)+'}{'+tex(v)+'}'
    a,b=tex(point[x]),tex(point[y]);equation=tex(lhs)+'='+tex(C)
    problem='Find the slope '+('$m$ ' if kind=='blank' else '')+'of the tangent at the point $('+a+','+b+')$ for the curve $'+equation+'$.'
    if band=='hard': problem+=' Give an exact answer.'
    if kind=='blank': problem+='\n\n$m=$\n{{field-1}}'
    solution=notes+'\n\nDifferentiate both sides with respect to $x$, then collect the derivative terms:\n\n'+aligned([
      r'\frac{d}{dx}\left('+tex(lhs)+r'\right)&=\frac{d}{dx}\left('+tex(C)+r'\right)',
      tex(derivative)+'&=0',
      r'\left('+tex(V)+r'\right)\frac{dy}{dx}&=-\left('+tex(U)+r'\right)',
      r'\frac{dy}{dx}&='+ratio],left=family=='nested')
    solution+='\n\nAt $('+a+','+b+')$, the coefficient of $\\dfrac{dy}{dx}$ is $'+tex(v)+'\\ne 0$. Substitute the point to obtain\n\n'+aligned([
       r'm&=\left.\frac{dy}{dx}\right|_{('+a+','+b+')}','&='+slope_eval,'&='+tex(m)+'.'])
    values=[m];profile='exact-slope'
    if kind=='radio':
        idx=profile_index if profile_index is not None else rng.randrange(len(PROFILES))
        error_sign=error_sign if error_sign is not None else rng.choice([-1,1])
        result=bank(m,u,v,dict(p,family=family),PROFILES[idx],error_sign)
        if result is None: raise ValueError('bank collision or inapplicable profile')
        values=result;profile=PROFILES[idx][0]
        rng.shuffle(values)
    problem=normalize_prose(problem);solution=normalize_prose(solution)
    texts=[tex(z) for z in values];key=tex(m)
    basis=json.dumps([band,problem,solution,sorted(texts),key],ensure_ascii=False)
    qid=ident(basis);fid=ident(qid+'/field')
    answers=[{':answer/id':ident(fid+'/'+z),':answer/type':':answer.type/math',':answer/value':z} for z in texts]
    field={':answer-field/id':fid,':answer-field/key':'selection' if kind=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==key)]}
    record={'knowledge_point':KP,'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+band,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':'1.0.0','family':family,'profile':profile,'error_sign':error_sign,'error_recipes':PROFILES[idx][1] if kind=='radio' else [],'parameters':p,'source_question_ids':SUPPORT[family],'domain':'Real local curve; coefficient of dy/dx at the supplied point is nonzero.','derivation':{'lhs':str(lhs),'constant':str(C),'U':str(U),'V':str(V),'point':[str(point[x]),str(point[y])],'slope':str(m),'displayed_final':key,'conversions':['Evaluate at the supplied point and simplify exact arithmetic.']}}}
    return validate_generated_record(record)

def sample_params(family,rng):
    small=[-3,-2,-1,1,2,3]
    if family=='powers': return dict(a=rng.choice([1,2,3,5]),b=rng.choice(small),p=rng.choice([2,3]),q=rng.choice([2,3,4]),x0=rng.choice(small),y0=rng.choice(small))
    if family=='quadratic': return dict(a=rng.choice(small),b=rng.choice([-2,-1,1,2]),c=rng.choice(small),x0=rng.randint(-2,2),y0=rng.randint(-2,2))
    if family=='product':
        style=rng.randrange(3)
        if style==0: return dict(a=1,p=rng.choice([2,3]),q=1,b=rng.choice([-3,-2,-1,0,1,2,3]),r=1,c=0,t=1,x0=rng.choice([-2,-1,1,2]),y0=rng.choice(small))
        if style==1: return dict(a=1,p=2,q=rng.choice([2,3]),b=rng.choice([-2,-1,1,2]),r=1,c=rng.choice([-4,-2,2,4]),t=1,x0=rng.choice([-1,0,1]),y0=rng.choice([-1,0,1]))
        return dict(a=1,p=2,q=2,b=rng.choice([-2,-1,1,2]),r=3,c=rng.choice([-2,-1,1,2]),t=3,x0=rng.choice([-1,1]),y0=rng.choice([-1,1]))
    if family=='radical':
        # Select root values first, then translations; equal roots stay eligible.
        u,v=rng.randint(1,4),rng.randint(1,4);h,j=rng.choice([0,0,-2,2,7]),rng.choice([0,0,-2,2,7])
        return dict(b=rng.choice([-1,1]),h=h,j=j,x0=u*u-h,y0=v*v-j)
    if family=='trig':
        orient=rng.choice(['ycosx','xsiny']);angle=rng.choice(['0','pi/6','-pi/6','pi/4','-pi/4','pi/3','-pi/3'])
        return dict(orientation=orient,a=1,b=rng.choice([0,0,-1,1]),x0=angle if orient=='ycosx' else rng.choice([-2,-1,1,2]),y0=angle if orient=='xsiny' else rng.choice([-2,-1,1,2]))
    return dict(orientation=rng.choice(['x','y']),a=rng.choice([-2,-1,1,2]),b=rng.choice([-2,-1,1,2]),k=rng.choice([-1,1]),x0=rng.choice([-1,1]),y0=rng.choice([-1,1]))

def semantic_key(record):
    """Same curve up to nonzero scalar at the same point is one practice instance."""
    d=record['generation']['derivation']
    F=s.expand(s.sympify(d['lhs'])-s.sympify(d['constant']))
    coefficients=F.as_coefficients_dict()
    pivot=coefficients[sorted(coefficients,key=s.srepr)[0]]
    return str(s.expand(F/pivot)),tuple(d['point'])


def choice_batch_shortcuts(records):
    """Return bank-only rules that answer every member of a repeated family.

    This guard uses whole batches, after numerical/bank collision resampling.
    Small one-off families cannot support this statistical claim. It is a
    conservative guard against observable finite-pool leaks, not a proof of
    absence of all shortcuts. No TeX parser is a runtime dependency.
    """
    groups={}
    for record in records:
        f=record['question'][':question/answer-fields'][0]
        if not f[':answer-field/type'].endswith('/radio'): continue
        g=record['generation']; d=g['derivation']; p=g['parameters']
        pt={x:s.sympify(d['point'][0]),y:s.sympify(d['point'][1])}
        u=s.sympify(d['U'],locals={'x':x,'y':y}).subs(pt)
        v=s.sympify(d['V'],locals={'x':x,'y':y}).subs(pt)
        m=s.sympify(d['slope'])
        profile=next(z for z in PROFILES if z[0]==g['profile'])
        generated=bank(m,u,v,dict(p,family=g['family']),profile,g['error_sign'])
        by_tex={tex(z):z for z in generated}
        values=[by_tex[a[':answer/value']] for a in f[':answer-field/choices']]
        correct=next(i for i,z in enumerate(values) if s.simplify(z-m)==0)
        signs=[int(s.sign(z)) for z in values]
        majority=max(set(signs),key=signs.count)
        paired=[i for i,z in enumerate(values) if any(i!=j and s.simplify(z+w)==0 for j,w in enumerate(values))]
        outcomes={}
        for subset,indices in [('all',list(range(len(values)))),('paired',paired),('unpaired',[i for i in range(len(values)) if i not in paired])]:
            for sign in ['any','positive','negative','majority','minority']:
                eligible=[i for i in indices if sign=='any' or sign=='positive' and signs[i]>0 or sign=='negative' and signs[i]<0 or sign=='majority' and signs[i]==majority or sign=='minority' and signs[i]!=majority]
                for metric,fn in [('value',lambda i:float(values[i])),('absolute',lambda i:abs(float(values[i]))),('position',lambda i:i)]:
                    for direction in ['min','max']:
                        ordered=sorted(eligible,key=fn,reverse=direction=='max')
                        pick=ordered[0] if ordered and (len(ordered)==1 or fn(ordered[0])!=fn(ordered[1])) else None
                        outcomes['/'.join([subset,sign,metric,direction])]=pick==correct
        order=sorted(range(len(values)),key=lambda i:float(values[i]))
        for i in range(len(values)):
            outcomes['rank/'+str(i)]=order[i]==correct
            outcomes['position/'+str(i)]=i==correct
        groups.setdefault(g['family'],[]).append(outcomes)
    return [(family,strategy) for family,rows in groups.items() if len(rows)>=4
            for strategy in rows[0] if all(row[strategy] for row in rows)]

def generate(band,count,seed):
    rng=random.Random(seed);out=[];seen=set();attempts=0
    families=['powers'] if band=='easy' else ['quadratic','product','radical','trig'] if band=='moderate' else ['nested']
    # Repeated shuffled family cycles preserve available method families in short batches.
    schedule=[]
    while True:
        if len(out)==count:
            if not choice_batch_shortcuts(out): break
            # Continue the same RNG stream; do not change the requested seed or
            # hand-pick a saved batch. Retry the entire short batch so its full
            # family/profile schedule remains eligible.
            out=[];seen=set();schedule=[]
        if not schedule:
            for family in rng.sample(families,len(families)):
                kind='radio' if band=='easy' else 'blank'
                if family in ['quadratic','product','trig'] and rng.randrange(2)==0: kind='radio'
                profile=rng.randrange(len(PROFILES)) if family=='powers' else rng.choice([1,2])
                schedule.append((family,kind,profile,rng.choice([-1,1])))
        family,kind,profile,error_sign=schedule[-1]
        p=sample_params(family,rng)
        try: record=make(family,p,band,kind,rng,profile,error_sign)
        except ValueError: record=None
        attempts+=1
        if attempts>max(2000,count*500): raise RuntimeError('Unable to construct requested unique batch')
        if record is None: continue
        fingerprint=semantic_key(record)
        if fingerprint in seen: continue
        seen.add(fingerprint);schedule.pop();out.append(record)
    for r in out: r['generation']['seed']=seed
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,required=True);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay-source',action='store_true')
    args=ap.parse_args()
    if args.count<0: ap.error('count must be nonnegative')
    if args.replay_source: records=json.loads((Path(__file__).parent/'source-replay.json').read_text())
    else: records=generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
