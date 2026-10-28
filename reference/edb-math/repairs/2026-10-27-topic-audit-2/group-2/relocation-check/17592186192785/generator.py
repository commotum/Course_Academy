#!/usr/bin/env python3
"""Seeded first partial derivatives with product-rule practice."""
import argparse
import json
from pathlib import Path
import random
import uuid
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

class SamplingError(ValueError):pass

KP = {'db_id':17592186192785,'id':'e960f6d1-5006-5ddc-ada2-59b46924bf73','title':'Applying the Product Rule'}
x,y=s.symbols('x y', real=True)
EASY=['cos_power','trig_sum','exp_power','log_power','tan_power','cos_mixed','sin_constant']
MODERATE=['exp_sub','log_rad','radical','trig_eval','tan_eval','exp_cos']
HARD=['group_exp_log','group_log','group_radical']
SOURCES=dict(zip(EASY+MODERATE+HARD,[
'7c4ebeea-f58f-5eb8-93aa-37b6d0eeb259','3444068d-2f79-5306-813a-47bbdab330c5','a1fee486-b1a7-59bd-ae9a-400ceeb58414','aaa7facc-73c8-58b5-b03f-ad80dd8597f5','67e10996-e62d-5489-9a64-73c5e56228d3','b7285b21-99ee-5b47-b1b3-ef79da9b3c2c','33a806e4-8348-5f3d-a738-c2a4c7316b98',
'd20c624a-1709-5495-88ea-45d0df97ea34','fd55c472-88b5-5201-8165-4111e38766b9','3f9cc492-b3ba-556f-a019-182cbc410bcf','e7a86e6a-207f-552d-b9da-b1e5c673da4e','39e99179-93fc-5477-adbb-fdfcbcd0de54','079e858b-c02c-58b3-bb61-a7e782e9db9f',
'477db031-06da-516b-adcf-00a254df15d0','477db031-06da-516b-adcf-00a254df15d0','477db031-06da-516b-adcf-00a254df15d0']))

def tex(a):
    # No trig expansion, argument reversal, or log expansion is authorized.
    return normalize_tex(s.latex(a,fold_short_frac=False,ln_notation=True))

def display(*rows):
    return '$$\n\\begin{aligned}\n'+('\\\\\n'.join(rows))+'\n\\end{aligned}\n$$'

def instance(family,target,rng,overrides=None):
    t,o=(x,y) if target=='x' else (y,x)
    p={'n':rng.choice([2,3,4]),'m':rng.choice([2,3]),'k':rng.choice([2,3,4]),'sign':rng.choice([-1,1])}
    if overrides:p.update(overrides)
    n,m,k,sg=p['n'],p['m'],p['k'],p['sign']
    C=s.Integer(1);R=s.Integer(0);point=None;domain=''
    if family=='cos_power':
        U,V=t**n,s.cos(t);du,dv=n*t**(n-1),-s.sin(t);R=sg*t*o**m
    elif family=='trig_sum':
        U,V=t,s.cos(t);du,dv=s.Integer(1),-s.sin(t);R=sg*o**m*s.sin(t)
    elif family=='exp_power':
        C=o**m;U,V=t**n,s.exp(t**k);du,dv=n*t**(n-1),k*t**(k-1)*V
    elif family=='log_power':
        C=o**m;U,V=t,s.log(t**k);du,dv=s.Integer(1),k/t;domain=f'Assume ${tex(t)}>0$.'
    elif family=='tan_power':
        C=o**m;U,V=t,s.tan(t**k);du,dv=s.Integer(1),k*t**(k-1)*s.sec(t**k)**2;domain=f'Assume $\\cos({tex(t**k)})\\ne0$.'
    elif family=='cos_mixed':
        U,V=t**n,s.cos(t*o);du,dv=n*t**(n-1),-o*s.sin(t*o)
    elif family=='sin_constant':
        C=o;U,V=t**n,s.sin(t);du,dv=n*t**(n-1),s.cos(t);R=sg*o**m
    elif family=='exp_sub':
        U,V=t,s.exp(o*t);du,dv=s.Integer(1),o*V;R=sg*o**2*t**2
        point={t:rng.choice([-1,1,2]),o:rng.choice([-2,-1,1,2])}
    elif family=='log_rad':
        U,V=t,s.log(o*t);du,dv=s.Integer(1),1/t;R=sg*t*s.sqrt(o)
        ov=rng.choice([1,4,9]);point={t:s.Rational(1,ov),o:s.Integer(ov)};domain=f'Assume ${tex(o)}>0$ and ${tex(t)}>0$.'
    elif family=='radical':
        U,V=t,s.sqrt(o**2+t**2);du,dv=s.Integer(1),t/V
        tv,ov=rng.choice([(3,4),(4,3),(s.sqrt(5),2),(s.sqrt(3),1)])
        point={t:tv*rng.choice([-1,1]),o:s.Integer(ov)*rng.choice([-1,1])}
        domain='Assume $(x,y)\\ne(0,0)$.'
    elif family=='trig_eval':
        C=o;U,V=t,s.cos(t);du,dv=s.Integer(1),-s.sin(t);R=sg*s.sin(t)
        point={t:rng.choice([0,s.pi,-s.pi,s.pi/2,-s.pi/2]),o:rng.choice([-3,-2,2,3])}
    elif family=='tan_eval':
        # The old +/- pi/4, +/-1 points with an outer square all
        # produced the same value. Vary the product dependency and chain scale.
        degree=overrides['n'] if overrides and 'n' in overrides else rng.choice([1,2])
        p['n']=degree
        U,V=t**degree,s.tan(t*o**2);du,dv=degree*t**(degree-1),o**2*s.sec(t*o**2)**2
        other=s.Integer(rng.choice([-2,-1,1,2]));angle=rng.choice([-s.pi/4,s.pi/4])
        point={t:angle/other**2,o:other};domain=f'Assume $\\cos({tex(t*o**2)})\\ne0$.'
    elif family=='exp_cos':
        C=s.cos(o);U,V=t**2,s.exp(t);du,dv=2*t,V
        point={t:rng.choice([-2,-1,1,2]),o:rng.choice([0,s.pi,s.pi/3])}
    elif family=='group_exp_log':
        U,V=o+t**2,s.exp(o*t)+sg*s.log(t);du,dv=2*t,o*s.exp(o*t)+sg/t
        point={t:rng.choice([1,2]),o:rng.choice([-2,-1,1,2])};domain=f'Assume ${tex(t)}>0$.'
    elif family=='group_log':
        U,V=o+t**2,s.log(o*t)+sg*t;du,dv=2*t,1/t+sg
        point={t:rng.choice([1,2]),o:rng.choice([1,2])};domain=f'Assume ${tex(o*t)}>0$.'
    elif family=='group_radical':
        U,V=o+t**2,s.sqrt(o**2+t**2)+sg*t;du,dv=2*t,t/s.sqrt(o**2+t**2)+sg
        tv,ov=rng.choice([(3,4),(4,3),(s.sqrt(3),1)]);point={t:tv*rng.choice([-1,1]),o:s.Integer(ov)}
        domain='Assume $(x,y)\\ne(0,0)$.'
    else:raise ValueError(family)
    if overrides and 'point' in overrides: point=overrides['point']
    dr=s.diff(R,t)
    derivative=C*(du*V+U*dv)+dr
    function=C*U*V+R
    # Factor derivatives are specified above, not CAS-selected canonical answers.
    return dict(family=family,t=t,o=o,C=C,U=U,V=V,R=R,du=du,dv=dv,dr=dr,
                derivative=derivative,function=function,point=point,domain=domain,parameters=p)


def exact_value(a,point):
    # Preserve evaluated log/exp inputs; collecting coefficients does not need
    # log combination, exponential splitting, or trigonometric identities.
    return s.expand(a.subs(point),log=False,power_exp=False,power_base=False)

def evaluate(a,z):
    return exact_value(a,z['point']) if z['point'] is not None else a

def equivalent(a,b):
    if a==b:return True
    diff=a-b
    witness=diff.subs({x:s.Rational(7,10),y:s.Rational(6,5)})
    if witness.is_number and witness.is_real is not False:
        value=s.N(witness,35)
        if value.is_real and abs(value)>s.Rational(1,10**20):return False
    return s.simplify(s.expand_trig(diff).rewrite(s.cos))==0

# Complete authored profiles. Eligibility is determined at the actual evaluation point.
PROFILES=[['double_left','double_right','keep_power','omit_right'],
          ['omit_left','omit_right','subtract_left','keep_power'],
          ['omit_left','subtract_left','multiply_derivatives','double_right'],
          ['omit_right','subtract_right','wrong_variable','double_left'],
          ['omit_left','omit_right','subtract_right','keep_power'],
          ['multiply_derivatives','wrong_variable','double_right','keep_power'],
          ['omit_left','double_right','power_multiplier','keep_power'],
          ['omit_right','subtract_left','double_left','keep_power'],
          ['wrong_variable','keep_function','negate_remainder','keep_remainder'],
          ['wrong_variable','keep_function','negate_remainder','chain_omit'],
          ['omit_remainder','negate_remainder','chain_omit','wrong_variable'],
          ['omit_left','omit_right','subtract_right','double_left'],
          ['multiply_derivatives','wrong_variable','double_right','subtract_left'],
          ['omit_left','double_right','power_multiplier','wrong_variable'],
          ['omit_right','subtract_left','double_left','multiply_derivatives'],
          ['omit_right','subtract_right','double_right','wrong_variable']]

def bank(z,rng):
    C,U,V,du,dv,dr=[z[k] for k in ['C','U','V','du','dv','dr']]
    a,b=C*du*V,C*U*dv
    f,t,o=z['family'],z['t'],z['o']
    no_chain=dv
    if f=='exp_power':no_chain=dv/(z['parameters']['k']*t**(z['parameters']['k']-1))
    elif f=='log_power':no_chain=1/t**z['parameters']['k']
    elif f=='tan_power':no_chain=dv/(z['parameters']['k']*t**(z['parameters']['k']-1))
    elif f=='radical':no_chain=dv/(2*t)
    elif f in ['cos_mixed','exp_sub','log_rad']:no_chain=dv/o
    elif f=='tan_eval':no_chain=dv/o**2
    elif f=='group_exp_log':no_chain=s.exp(o*t)+z['parameters']['sign']/t
    elif f=='group_log':no_chain=1/(o*t)+z['parameters']['sign']
    elif f=='group_radical':no_chain=1/(2*s.sqrt(o**2+t**2))+z['parameters']['sign']
    degree=s.degree(U,t) if U.is_polynomial(t) else 1
    errors={'omit_left':b+dr,'omit_right':a+dr,'subtract_right':a-b+dr,
            'subtract_left':-a+b+dr,'double_left':2*a+b+dr,'double_right':a+2*b+dr,
            'multiply_derivatives':C*du*dv+dr,'wrong_variable':s.diff(z['function'],z['o']),
            'power_multiplier':C*(du/degree*V+U*dv)+dr,
            'keep_power':C*(t*du*V+U*dv)+dr,
            'keep_function':z['function'],'negate_remainder':a+b-dr,
            'keep_remainder':a+b+z['R'],'omit_remainder':a+b,
            'chain_omit':a+C*U*no_chain+dr}
    key=evaluate(z['derivative'],z)
    normalized_key=key.xreplace({z['t']:x,z['o']:y}) if z['point'] is None else key
    if z.get('previous_family_key') is not None and equivalent(normalized_key,z['previous_family_key']):
        raise SamplingError('Repeated answer within the same visible family')
    z['selected_family_key']=normalized_key
    if 'profile_order' in z:
        order=z['profile_order'];offset=z['profile_offset']%len(order)
        profiles=[PROFILES[i] for i in order[offset:]+order[:offset]]
    else:
        profiles=list(PROFILES);rng.shuffle(profiles)
    if f == 'log_rad':
        # At inactive coordinate 4 with a negative radical term, the wrong-
        # variable value and doubled-right value coincide at zero. This complete
        # profile keeps distinct, interpretable errors and same-sign integers.
        profiles.append(['omit_right','subtract_right','keep_function','wrong_variable'])
    for profile in profiles:
        vals=[key]+[evaluate(errors[k],z) for k in profile]
        if any(v.has(s.zoo,s.nan,s.oo,-s.oo,s.I) for v in vals):continue
        # Numerical points make comparison cheap; symbolic profiles require exact equivalence checks.
        if any(equivalent(vals[i],vals[j]) for i in range(5) for j in range(i)):continue
        # At the log/radical normalization points the exact result is an
        # integer. Keep a plausible same-sign integer error alongside a nonzero
        # integer key so its numerical form cannot identify it from the bank.
        # Zero cancellations remain eligible; all alternatives are still drawn
        # from the complete authored derivative-error profiles above.
        if f == 'log_rad' and key.is_Integer and key != 0:
            if sum(v.is_Integer and bool(v * key > 0) for v in vals) < 2:
                continue
        # A repeated visible family must not be answerable by a fixed bank rank.
        # Symbolic banks are compared at one declared legal reference point;
        # numerical banks need no prompt information for this strategy.
        numbers=[s.N(v.subs({x:s.Rational(7,10),y:s.Rational(6,5)}),30) for v in vals]
        if any(abs(numbers[i]-numbers[j])<s.Rational(1,10**20) for i in range(5) for j in range(i)):continue
        rank=sum(int(bool(number<numbers[0])) for number in numbers[1:])
        if rank==z.get('previous_bank_rank'):continue
        z['selected_bank_rank']=rank
        choices=list(zip(['correct']+profile,vals));rng.shuffle(choices)
        # Retain randomized order without a repeated literal-position answer action.
        position=next(i for i,(role,_) in enumerate(choices) if role=='correct')
        if position==z.get('previous_bank_position'):
            alternate=rng.choice([i for i in range(5) if i!=position])
            choices[position],choices[alternate]=choices[alternate],choices[position]
            position=alternate
        z['selected_bank_position']=position
        return key,choices,profile
    raise SamplingError('No distinct complete error profile')


def record(z,difficulty,rng):
    key,values,profile=bank(z,rng)
    t,o=z['t'],z['o'];U,V,du,dv,C,dr=[z[k] for k in ['U','V','du','dv','C','dr']]
    function=z['function'];derivative=z['derivative'];pt=z['point']
    if pt is None:
        prompt=f'Find $\\dfrac{{\\partial f}}{{\\partial {t}}}$ for $f(x,y)={tex(function)}$.'
    else:
        prompt=f'For $f(x,y)={tex(function)}$, evaluate $f_{t}({tex(pt[x])},{tex(pt[y])})$.'
    if z['domain']:prompt+=' '+z['domain']
    solution=f'Differentiate with respect to ${t}$, treating ${o}$ as constant. Write $f=Cuv+r$, where\n\n'
    solution+=display('C&='+tex(C)+',\\quad r='+tex(z['R']), 'u&='+tex(U)+',\\quad v='+tex(V))
    solution+='\n\nUsing the power, sum, and chain rules on the active factors gives\n\n'
    solution+=display(f'u_{t}&='+tex(du),f'v_{t}&='+tex(dv),f'r_{t}&='+tex(dr))
    # Keep inner inputs intact and make the product-rule stage explicit before any evaluation.
    solution+='\n\nApply both terms of the product rule:\n\n'
    product_rows=[f'f_{t}&=C(u_{t}v+uv_{t})+r_{t}']
    if difficulty!='hard':
        product_rows.append('&='+tex(C)+r'\left[\left('+tex(du)+r'\right)\left('+tex(V)+r'\right)+\left('+tex(U)+r'\right)\left('+tex(dv)+r'\right)\right]+\left('+tex(dr)+r'\right)')
    if difficulty=='hard':
        product_rows.append('&='+tex(C*du*V))
        product_rows.append(r'&\quad +\left('+tex(C*U*dv+dr)+r'\right)')
    else:
        product_rows.append('&='+tex(derivative))
    solution+=display(*product_rows)
    if pt is None and tex(derivative)!=tex(key):
        solution+='\n\nCollect like terms and factor common factors:\n\n'+display(f'f_{t}&='+tex(key))
    if pt is not None:
        # Simultaneous substitution in unevaluated component products shows both endpoint contributions.
        entries=[C,du,V,U,dv,dr]
        substituted=[exact_value(a,pt) for a in entries]
        cs,ds,vs,us,ws,rs=map(tex,substituted)
        solution+=f'\n\nNow substitute $x={tex(pt[x])}$ and $y={tex(pt[y])}$ and combine the exact values:\n\n'
        terms=r'\left('+ds+r'\right)\left('+vs+r'\right)+\left('+us+r'\right)\left('+ws+r'\right)'
        if substituted[0]!=1:terms=cs+r'\left['+terms+r'\right]'
        if substituted[-1]!=0:terms+=r'+\left('+rs+r'\right)'
        solution+=display(f'f_{t}({tex(pt[x])},{tex(pt[y])})&='+terms,'&='+tex(key))
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    canonical=tex(key)
    identity=json.dumps([difficulty,prompt,solution,sorted(tex(v) for _,v in values)],sort_keys=True)
    qid=uuid.uuid5(uuid.UUID(KP['id']),identity);fid=uuid.uuid5(qid,'selection')
    choices=[{':answer/id':str(uuid.uuid5(fid,tex(v))),':answer/type':':answer.type/math',':answer/value':tex(v)} for _,v in values]
    correct=next(a for a in choices if a[':answer/value']==canonical)
    q={':question/id':str(qid),':question/problem':prompt,':question/worked-solution':solution,
       ':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[
       {':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
        ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct[':answer/id']]}]}
    generation={'version':1,'family':z['family'],'target':str(t),'source_question_ids':[SOURCES[z['family']]],
                'authored_bank_profile':profile,'parameters':{k:str(v) for k,v in z['parameters'].items()},
                'domain':z['domain'],'point':{str(k):str(v) for k,v in pt.items()} if pt else None,
                'derivation':{'constant':str(C),'left':str(U),'right':str(V),'remainder':str(z['R']),
                              'left_derivative':str(du),'right_derivative':str(dv),'final':canonical},
                'choice_errors':{a[':answer/id']:role for a,(role,_) in zip(choices,values)}}
    return validate_generated_record({'knowledge_point':KP,'question':q,'generation':generation})


def generate(difficulty,count,seed):
    rng=random.Random(seed)
    families={'easy':EASY,'moderate':MODERATE,'hard':HARD}[difficulty]
    schedule=[(f,t) for f in families for t in ['x','y']];rng.shuffle(schedule)
    orders={f:list(range(len(PROFILES))) for f in families}
    for f in families:
        # Contrast the common missing-term/sign-error bank with a bank that
        # includes duplicated contributions before cycling further error profiles.
        core=[0,1];contrast=[2,3];rest=list(range(4,len(PROFILES)))
        rng.shuffle(core);rng.shuffle(contrast);rng.shuffle(rest)
        orders[f]=core+contrast+rest
    family_counts={f:0 for f in families}
    previous_ranks={f:None for f in families}
    previous_positions={f:None for f in families}
    previous_keys={f:None for f in families}
    results=[];seen=set();index=0;stalled=0
    while len(results)<count:
        family,target=schedule[index%len(schedule)];index+=1
        for _ in range(100):
            try:
                z=instance(family,target,rng)
                z.update(profile_order=orders[family],profile_offset=family_counts[family],previous_bank_rank=previous_ranks[family],previous_bank_position=previous_positions[family],previous_family_key=previous_keys[family])
                r=record(z,difficulty,rng)
            except SamplingError:continue
            # Option order and distractor profile alone are not new mathematical instances.
            if z['point'] is None:
                signature=('symbolic',s.srepr(z['function'].xreplace({z['t']:x,z['o']:y})))
            else:
                # Fixing the inactive variable is precisely the assessed partial
                # operation. Exclude relabelings and sign changes that leave this
                # active one-variable task and evaluation point identical.
                active=z['function'].subs(z['o'],z['point'][z['o']]).xreplace({z['t']:x})
                signature=('evaluated',s.srepr(active),str(z['point'][z['t']]))
            if signature in seen:continue
            seen.add(signature);r['generation']['seed']=seed;results.append(r);family_counts[family]+=1
            previous_ranks[family]=z['selected_bank_rank']
            previous_positions[family]=z['selected_bank_position']
            previous_keys[family]=z['selected_family_key'];stalled=0;break
        else:
            # A finite family may exhaust its eligible mathematical tasks or
            # bank contrasts before other supported families do. Continue the
            # deterministic schedule instead of failing a complete batch.
            stalled+=1
            if stalled>=len(schedule):
                raise RuntimeError('Requested count exceeds the eligible finite practice pool')
    return results


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json')
    args=ap.parse_args()
    if args.count<0:ap.error('count must be nonnegative')
    print(json.dumps(generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
