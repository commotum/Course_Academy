#!/usr/bin/env python3
"""Seeded partial-chain-rule practice. No database or filesystem writes."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import random
import re
import uuid
import sympy as S
from math_format import normalize_prose, normalize_tex, validate_generated_record

X,Y=S.symbols('x y',real=True)
KP={'db_id':17592186192790,'id':'14cc6590-c2fd-5395-9481-0e5c0d9b8b8b','title':'Applying the Chain Rule'}
NS=uuid.UUID('85764336-1fd0-4202-9549-2bac6687770c')
FAMILIES={'easy':['log_poly','exp_log','cos_radical','power','tan_log','log_minus'],
          'moderate':['exp_poly','poly_cos','cos_square','affine_power','arctan','sqrt_sum','norm'],
          'hard':['log_exp_poly']}
SOURCES={
 'log_poly':['6cc4635c-e2d0-54e1-a8b8-18c5b785e7cf','8bdc87f1-f622-5252-80a6-1d3652c87043'],
 'exp_log':['424001c9-342e-51ae-ba3f-40228db99e48'],
 'cos_radical':['0833bc78-75ed-516b-b7f3-7df11e162117'],
 'power':['9932dc44-faa7-51c4-b14b-b1d882efadd1'],
 'tan_log':['4560fcbf-c2fb-5e9f-b888-53c870445e63'],
 'log_minus':['b72fd759-0cb1-5717-8778-6af4e6d7337a'],
 'exp_poly':['52ec8ecc-7425-5715-9001-87fc8bd443a4','684028b0-fca2-5e81-bf94-98e01d24397f','39e13e50-9616-558b-a2da-0689d5cb4c25'],
 'poly_cos':['2942efcf-e503-5d5c-b252-e682ffa52f18'],
 'cos_square':['0d55bb11-970c-5f1f-831a-44fb97e659c5'],
 'affine_power':['6c44dfc3-39f6-598a-be48-62e051abdda4'],
 'arctan':['fe49ff44-a8f4-5323-af29-4e99b3a5291b'],
 'sqrt_sum':['738ade6c-0972-56b4-b1bb-9f8fdeb237e7'],
 'norm':['dfe77a47-89cf-58c9-a7e4-db0e7d6a133d'],
 'log_exp_poly':['17c05b7d-1ccb-5232-b562-f1c6a1350d59']}

def tex(z):
    return normalize_tex(S.latex(z,ln_notation=True,inv_trig_style='full'))

def uid(value):return str(uuid.uuid5(NS,value))
def eq(a,b):
    z=S.expand(a-b)
    return z==0 or S.cancel(z)==0

def evaluate(z,point):
    if point is None:return z
    value=S.simplify(z.subs({X:point[0],Y:point[1]}, simultaneous=True))
    # SymPy may turn exponential quotients into hyperbolic functions. This KP
    # teaches log/exp chain factors, so keep their evaluated values in that form.
    if value.has(S.tanh,S.coth,S.sinh,S.cosh,S.sech,S.csch):
        value=S.cancel(value.rewrite(S.exp))
    return value

def trig(fun,u):return fun(u,evaluate=False)

def make_instance(family,rng,overrides=None):
    # Choose derivative role and signed inner geometry before coefficients/points.
    p={'query':rng.choice([0,1]),'swap':rng.choice([False,True]),'a':rng.choice([-2,-1,1,2]),
       'b':rng.choice([1,2,3]),'c':rng.choice([-2,-1,1,2]),'n':rng.choice([2,3]),
       'shape':rng.choice(['product','sum'])}
    if family in ['power','affine_power','log_exp_poly']:p['query']=0
    if family=='cos_radical':p['b']=rng.choice([-2,-1,0,1,2])
    if family=='tan_log':p['c']=rng.choice([-2,-1,0,1,2])
    if overrides:p.update(overrides)
    t,v=(Y,X) if p['swap'] else (X,Y)
    a,b,c,n=map(S.Integer,[p['a'],p['b'],p['c'],p['n']])
    point=None;term=S.Integer(0)
    if family=='log_poly':
        u=b*t+a*t**n*v if p['shape']=='product' else b*v+a*t**n
        outer=S.log(u,evaluate=False);od=1/u;bad=[1/S.log(u),u]
        domain=f'${tex(u)}>0$'
    elif family=='exp_log':
        u=a*t**n*v;term=-c*v*S.log(t)
        outer=S.exp(u);od=S.exp(u);bad=[S.exp(u)/u,u*S.exp(u)]
        domain=f'${tex(t)}>0$'
    elif family=='cos_radical':
        u=a*t*v+b;root=S.sqrt(u)
        outer=trig(S.cos,root);od=-trig(S.sin,root)/(2*root)
        bad=[trig(S.cos,root)/(2*root),-trig(S.sin,root)/root]
        domain=f'${tex(u)}>0$'
    elif family in ['power','affine_power']:
        u=(a*t+b) if family=='affine_power' else (t+b)
        k=(n*v+1) if family=='affine_power' else v**n
        outer=S.Pow(u,k,evaluate=False);od=k*S.Pow(u,k-1,evaluate=False)
        bad=[S.Pow(u,k)*S.log(u),S.Pow(u,k-1)]
        domain=f'${tex(u)}>0$'
        if family=='affine_power':
            # Positive small bases, integer exponents; controlled evaluation.
            base_value=rng.choice([1,2])
            vv=rng.choice([0,1,2] if base_value==1 else [0,1])
            tv=(S.Integer(base_value)-b)/a
            point=(vv,tv) if p['swap'] else (tv,vv)
    elif family=='tan_log':
        u=a*t+b*v+c
        lu=S.log(u,evaluate=False);outer=trig(S.tan,lu)
        od=trig(S.sec,lu)**2/u
        bad=[trig(S.sec,lu)**2/S.log(u),trig(S.sec,u)**2/u]
        domain=f'${tex(u)}>0$ and $\\cos(\\ln({tex(u)}))\\ne0$'
    elif family=='log_minus':
        u=a*t*v;term=-c*t*v
        outer=S.log(u,evaluate=False);od=1/u;bad=[1/S.log(u),u]
        domain=f'${tex(u)}>0$'
    elif family=='exp_poly':
        u=a*t*v;term=c*t**3*v**2 if n==3 else (c*t*v**2 if p['shape']=='product' else c*t**2*v)
        outer=S.exp(u);od=S.exp(u);bad=[S.exp(u)/u,u*S.exp(u)]
        tv,vv=rng.choice([(-1,1),(1,0),(1,1),(2,0),(0,1),(1,-1)])
        point=(vv,tv) if p['swap'] else (tv,vv);domain='all real $x,y$'
    elif family=='poly_cos':
        u=a*t*v;term=c*t**2*v**2
        outer=-trig(S.cos,u);od=trig(S.sin,u)
        bad=[trig(S.cos,u),-trig(S.sin,u)]
        vv=rng.choice([-2,-1,1,2]);angle=rng.choice([-S.pi/2,0,S.pi/2,S.pi])
        tv=angle/(a*vv);point=(vv,tv) if p['swap'] else (tv,vv);domain='all real $x,y$'
    elif family=='cos_square':
        u=b*v+a*t**2;outer=trig(S.cos,u)**2
        od=-2*trig(S.cos,u)*trig(S.sin,u)
        bad=[2*trig(S.cos,u)*trig(S.sin,u),-2*trig(S.sin,u)]
        # Choose the familiar argument first, preserving zero AND nonzero values.
        tv=rng.choice([-1,1,2]);angle=rng.choice([-S.pi,-S.pi/4,S.pi/4,S.pi/2])
        vv=(angle-a*tv**2)/b
        point=(vv,tv) if p['swap'] else (tv,vv);domain='all real $x,y$'
    elif family=='arctan':
        u=a*t*v**n;outer=trig(S.atan,u);od=1/(1+u**2)
        bad=[1/(1+u),1/(1+u**2)**2]
        tv=rng.choice([-1,0,1]);vv=rng.choice([-2,-1,1,2])
        point=(vv,tv) if p['swap'] else (tv,vv);domain='all real $x,y$'
    elif family=='sqrt_sum':
        u=a*v+t;term=c*v**2*S.sqrt(t)
        outer=S.sqrt(u);od=1/(2*S.sqrt(u));bad=[1/S.sqrt(u),S.sqrt(u)/2]
        # Both radicals have small perfect-square arguments at the point.
        tv=rng.choice([1,4]);rad=rng.choice([1,4,9]);vv=(rad-tv)/a
        point=(vv,tv) if p['swap'] else (tv,vv)
        domain=f'${tex(t)}>0$ and ${tex(u)}>0$'
    elif family=='norm':
        u=b*t**2+v**2;outer=S.sqrt(u);od=1/(2*S.sqrt(u))
        bad=[1/S.sqrt(u),S.sqrt(u)/2]
        tv=rng.choice([-1,1]);radius=S.Integer(rng.choice([2,3]))
        vv=rng.choice([-1,1])*S.sqrt(radius**2-b*tv**2)
        point=(vv,tv) if p['swap'] else (tv,vv);domain='all real $(x,y)\\ne(0,0)$'
    elif family=='log_exp_poly':
        u=a*t*v if p['shape']=='product' else a*t**2+v
        term=c*t**2*v
        outer=S.log(1+S.exp(u),evaluate=False);od=S.exp(u)/(1+S.exp(u))
        bad=[1/(1+S.exp(u)),S.exp(u)]
        tv,vv=rng.choice([(-1,1),(1,2),(2,1),(0,1),(1,0),(-1,-2)])
        point=(vv,tv) if p['swap'] else (tv,vv);domain='all real $x,y$'
    else:raise ValueError(family)
    if overrides and 'point' in overrides:point=tuple(S.sympify(x) for x in overrides['point'])
    return {'family':family,'params':p,'t':t,'v':v,'u':u,'outer':outer,'od':od,
            'bad':bad,'term':term,'expr':outer+term,'point':point,'domain':domain}

def derive(inst,z):
    u,term=inst['u'],inst['term'];di=S.diff(u,z)
    # All polynomial inner derivatives use ordinary power/sum rules.
    dt=S.diff(term,z)
    chain=inst['od']*di
    result=chain+dt
    return {'variable':z,'di':di,'dt':dt,'chain':chain,'symbolic':result,
            'value':evaluate(result,inst['point'])}

def error_candidates(inst,d):
    z=d['variable'];other=Y if z==X else X
    di,dt,od=d['di'],d['dt'],inst['od'];u=inst['u']
    # Every candidate is an identifiable operation error, not a value offset.
    return {
        'omit_inner':od+dt,
        'other_inner':od*S.diff(u,other)+dt,
        'other_partial':(S.diff(inst['expr'],other) if inst['family'] in ['power','affine_power'] else derive(inst,other)['symbolic']),
        'inner_not_differentiated':od*u+dt,
        'inner_sign':-od*di+dt,
        'double_inner':od*(2*di)+dt,
        'half_inner':od*(di/2)+dt,
        'wrong_outer_1':inst['bad'][0]*di+dt,
        'wrong_outer_2':inst['bad'][1]*di+dt,
        'omit_other_term':od*di,
        'other_term_sign':od*di-dt,
        'other_term_undifferentiated':od*di+inst['term'],
        'omit_chain_term':dt,
        'derivative_of_inner_only':di+dt,
        'premature_substitution':S.Integer(0),
        'square_omit_cosine':-2*trig(S.sin,u)*di,
        'square_omit_sine':-2*trig(S.cos,u)*di,
        'square_forget_power':-trig(S.sin,u)*di,
        'square_forget_trig_factors':2*di,
        'square_forget_trig_factors_negative':-2*di,
        'square_cosine_not_differentiated':trig(S.cos,u)*di,
        'function_value_instead_of_partial':inst['expr'],
        'square_forget_power_and_inner':-trig(S.sin,u),
    }

# Profiles describe complete classes of eligible errors, selected before parameters.
PROFILES={
 'chain':['omit_inner','other_inner','inner_not_differentiated','inner_sign','double_inner','half_inner','wrong_outer_1','wrong_outer_2','derivative_of_inner_only'],
 'mixed':['omit_inner','other_partial','wrong_outer_1','wrong_outer_2','omit_other_term','other_term_sign','other_term_undifferentiated','omit_chain_term','double_inner','half_inner','premature_substitution'],
}

def bank(inst,d,rng,profile):
    correct=d['value'];available=[];candidates=error_candidates(inst,d)
    names=PROFILES[profile]+(['derivative_of_inner_only','square_omit_cosine','square_omit_sine','square_forget_power','square_forget_trig_factors','square_forget_trig_factors_negative','square_cosine_not_differentiated','function_value_instead_of_partial','square_forget_power_and_inner'] if inst['family']=='cos_square' else [])
    for name in names:
        val=evaluate(candidates[name],inst['point'])
        if val.has(S.zoo,S.nan,S.oo,-S.oo) or val.is_real is False:continue
        if eq(val,correct):continue
        if any(eq(val,v) for _,v in available):continue
        available.append((name,val))
    if len(available)<4:raise ValueError('bank collision')
    if inst['family']=='cos_square' and correct==0:
        # Include a genuine evaluation/compound-chain error that is not another
        # member of the symmetric {+/-inner', +/-2inner'} error family.
        distinct=[x for x in available if x[0] in ['function_value_instead_of_partial','square_forget_power_and_inner']]
        if not distinct:raise ValueError('No distinct zero-outcome error profile')
        anchor=rng.choice(distinct)
        chosen=[anchor]+rng.sample([x for x in available if x!=anchor],3)+[('correct',correct)]
    else:chosen=rng.sample(available,4)+[('correct',correct)]
    # A unique sign pair must not reveal the correct magnitude. If the sampled
    # bank has that cue, use a complete profile with TWO plausible sign pairs.
    pairs=[(i,j) for i in range(5) for j in range(i)
           if not eq(chosen[i][1],0) and eq(chosen[i][1],-chosen[j][1])]
    ci=next(i for i,(name,_) in enumerate(chosen) if name=='correct')
    if len(pairs)==1 and ci in pairs[0]:
        ni=next(i for i in pairs[0] if i!=ci)
        negative=chosen[ni]
        eligible=[(name,val) for name,val in available
                  if not eq(val,0) and not eq(val,correct) and not eq(val,-correct)]
        if not eligible:raise ValueError('No distinct paired-error profile')
        name,error=rng.choice(eligible)
        rest=[(n,v) for n,v in available if not any(eq(v,z) for z in [correct,-correct,error,-error])]
        if not rest:raise ValueError('Paired-error profile collision')
        chosen=[('correct',correct),negative,(name,error),('sign_after_'+name,-error),rng.choice(rest)]
    rng.shuffle(chosen)
    return chosen

def derivation(inst,d):
    z=d['variable'];other=Y if z==X else X;u=tex(inst['u']);od=tex(inst['od'])
    family=inst['family']
    U=S.Symbol('u',positive=True)
    if family in ['log_poly','log_minus']:odu=1/U
    elif family in ['exp_log','exp_poly']:odu=S.exp(U)
    elif family=='cos_radical':odu=-trig(S.sin,S.sqrt(U))/(2*S.sqrt(U))
    elif family in ['power','affine_power']:odu=inst['outer'].exp*U**(inst['outer'].exp-1)
    elif family=='tan_log':odu=trig(S.sec,S.log(U))**2/U
    elif family=='poly_cos':odu=trig(S.sin,U)
    elif family=='cos_square':odu=-2*trig(S.sin,U)*trig(S.cos,U)
    elif family=='arctan':odu=1/(1+U**2)
    elif family in ['sqrt_sum','norm']:odu=1/(2*S.sqrt(U))
    elif family=='log_exp_poly':odu=S.exp(U)/(1+S.exp(U))
    lines=[f'u&={u}',f'\\frac{{\\partial u}}{{\\partial {z}}}&={tex(d["di"])}']
    family=inst['family']
    if family=='cos_radical':
        lines += [f'\\frac{{\\partial}}{{\\partial {z}}}\\cos(\\sqrt{{u}})&=-\\sin(\\sqrt{{u}})\\cdot\\frac{{1}}{{2\\sqrt{{u}}}}\\cdot\\frac{{\\partial u}}{{\\partial {z}}}']
    elif family=='tan_log':
        lines += [f'\\frac{{\\partial}}{{\\partial {z}}}\\tan(\\ln u)&=\\sec^2(\\ln u)\\cdot\\frac{{1}}{{u}}\\cdot\\frac{{\\partial u}}{{\\partial {z}}}']
    elif family=='cos_square':
        lines += [f'\\frac{{\\partial}}{{\\partial {z}}}\\cos^2(u)&=2\\cos(u)\\cdot(-\\sin(u))\\cdot\\frac{{\\partial u}}{{\\partial {z}}}']
    elif family=='log_exp_poly':
        lines += [f'\\frac{{\\partial}}{{\\partial {z}}}\\ln(1+e^u)&=\\frac{{1}}{{1+e^u}}\\cdot e^u\\cdot\\frac{{\\partial u}}{{\\partial {z}}}']
    elif family in ['power','affine_power']:
        k=inst['outer'].exp
        lines += [f'\\frac{{\\partial}}{{\\partial {z}}}u^{{{tex(k)}}}&=\\left({tex(k)}\\right)\\,u^{{{tex(k-1)}}}\\cdot\\frac{{\\partial u}}{{\\partial {z}}}']
    else:
        lines += [f'\\frac{{\\partial}}{{\\partial {z}}}\\left({tex(inst["outer"].subs(inst["u"],U))}\\right)&=\\left({tex(odu)}\\right)\\cdot\\frac{{\\partial u}}{{\\partial {z}}}']
    if inst['term']!=0:
        lines += [f'\\frac{{\\partial}}{{\\partial {z}}}\\left({tex(inst["term"])}\\right)&={tex(d["dt"])}']
    symbolic_product=f'\\left({tex(odu)}\\right)\\cdot\\left({tex(d["di"])}\\right)'
    if d['dt']!=0:symbolic_product+=f'+\\left({tex(d["dt"])}\\right)'
    lines += [f'f_{z}(x,y)&={symbolic_product}',f'&={tex(d["symbolic"])}']
    text=f'Treat ${other}$ as constant and differentiate with respect to ${z}$. Apply the chain rule, and the sum and constant multiple rules where needed.\n\n$$\n\\begin{{aligned}}\n'+('\\\\\n'.join(lines))+'\n\\end{aligned}\n$$'
    if inst['point'] is not None:
        pt=','.join(tex(q) for q in inst['point'])
        def substitute_tex(value):
            return re.sub(r'(?<![A-Za-z\\])[xy](?![A-Za-z])', lambda m:r'\left('+tex(inst['point'][0 if m[0]=='x' else 1])+r'\right)',value)
        uv=evaluate(inst['u'],inst['point'])
        # Evaluate the inner input once instead of repeating a long coordinate expression.
        od_at=re.sub(r'(?<![A-Za-z\\])u(?![A-Za-z])',lambda m:r'u_0',substitute_tex(tex(odu)))
        eval_product=f'\\left({od_at}\\right)\\cdot\\left({tex(evaluate(d["di"],inst["point"]))}\\right)'
        if d['dt']!=0:eval_product+=f'+\\left({tex(evaluate(d["dt"],inst["point"]))}\\right)'
        eval_numeric=f'\\left({tex(odu.subs({U:uv,X:inst["point"][0],Y:inst["point"][1]},simultaneous=True))}\\right)\\cdot\\left({tex(evaluate(d["di"],inst["point"]))}\\right)'
        if d['dt']!=0:eval_numeric+=f'+\\left({tex(evaluate(d["dt"],inst["point"]))}\\right)'
        text+=f'\n\nSubstitute $x={tex(inst["point"][0])}$ and $y={tex(inst["point"][1])}$ after differentiating. The inner input is\n\n$$\nu_0={substitute_tex(tex(inst["u"]))}={tex(uv)}.\n$$\n\nUsing this value in the chain factors gives\n\n$$\n\\begin{{aligned}}\nf_{z}({pt})&={eval_product}\\\\\n&={eval_numeric}\\\\\n&={tex(d["value"])}.\n\\end{{aligned}}\n$$'
    return text

def record(inst,difficulty,rng,profile='mixed'):
    zs=[X,Y] if difficulty=='hard' else [inst['t'] if inst['params']['query']==0 else inst['v']]
    ds=[derive(inst,z) for z in zs]
    banks=[bank(inst,d,rng,profile) for d in ds]
    point=inst['point'];pt=','.join(tex(v) for v in point) if point is not None else 'x,y'
    function=tex(inst['expr'])
    if difficulty=='hard':
        prompt=f'For the function\n\n$$\nf(x,y)={function},\n$$\n\nevaluate both partial derivatives at $({pt})$.\n\n$f_x({pt})=$\n\n{{{{field-1}}}}\n\n$f_y({pt})=$\n\n{{{{field-2}}}}'
    elif point is None:prompt=f'Find $f_{zs[0]}(x,y)$ for $f(x,y)={function}$.'
    else:prompt=f'For the function $f(x,y)={function}$, evaluate $f_{zs[0]}({pt})$.'
    prompt=normalize_prose(prompt)
    solution=normalize_prose('\n\n'.join(derivation(inst,d) for d in ds)+f'\n\nThese derivatives apply for {inst["domain"]}.')
    # Normalize all public content BEFORE deriving content-based identities.
    content={'problem':prompt,'solution':solution,'difficulty':difficulty,'banks':[[tex(v) for _,v in b] for b in banks]}
    ident=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    fields=[]
    for i,b in enumerate(banks):
        choices=[{':answer/id':uid(f'{ident}/field/{i}/{tex(v)}'),':answer/type':':answer.type/math',':answer/value':tex(v)} for name,v in b]
        correct=next(a[':answer/id'] for a,(name,_) in zip(choices,b) if name=='correct')
        fields.append({':answer-field/id':uid(f'{ident}/field/{i}'),':answer-field/key':f'field-{i+1}' if difficulty=='hard' else 'selection',
                       ':answer-field/type':':answer-field.type/select' if difficulty=='hard' else ':answer-field.type/radio',
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]})
    rec={'knowledge_point':KP.copy(),'question':{':question/id':uid(ident),':question/problem':prompt,':question/worked-solution':solution,
            ':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields},
         'generation':{'generator':'partial-chain-v1','family':inst['family'],'profile':profile,'parameters':inst['params'],
            'source_question_ids':SOURCES[inst['family']],
            'point':None if point is None else [str(q) for q in point],
            'errors':[[name for name,_ in b] for b in banks]}}
    return validate_generated_record(rec)

def generate(difficulty,count,seed):
    if difficulty=='unclassified':difficulty='moderate'
    if difficulty not in FAMILIES:raise ValueError('unsupported difficulty')
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);out=[];seen=set();schedule=[];active=FAMILIES[difficulty].copy()
    while len(out)<count:
        index=len(out)
        if not schedule:
            if not active:raise RuntimeError('Requested count exceeds the available distinct semantic instances')
            schedule=active.copy();rng.shuffle(schedule)
        family=schedule.pop();profile=rng.choice(list(PROFILES))
        for attempt in range(300):
            inst=make_instance(family,rng)
            try:r=record(inst,difficulty,rng,profile)
            except ValueError:continue
            semantic=r['question'][':question/problem']
            if semantic in seen:continue
            seen.add(semantic);r['generation'].update({'seed':seed,'index':index,'attempt':attempt})
            out.append(r);break
        else:
            # A finite subfamily must not prevent the rest of the pool filling a batch.
            active.remove(family);schedule=[f for f in schedule if f!=family]
    return out

def replay_source(question_id):
    questions=json.loads(Path(__file__).with_name('source-cases.json').read_text())
    q=copy.deepcopy(next(q for q in questions if q[':question/id']==question_id))
    # New question and field-owned choice identities; no imported IDs are changed.
    old=q[':question/id'];q[':question/id']=uid('replay/'+old)
    for fi,f in enumerate(q[':question/answer-fields']):
        old_correct=f[':answer-field/correct'][1]
        f[':answer-field/id']=uid(f'replay/{old}/{fi}')
        for a in f[':answer-field/choices']:
            aid=a[':answer/id'];a[':answer/id']=uid(f'replay/{old}/{fi}/{aid}')
            if aid==old_correct:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
    return validate_generated_record({'knowledge_point':KP.copy(),'question':q,'generation':{'source_question_ids':[old],'source_replay':True}})

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',default='moderate',choices=['easy','moderate','hard','unclassified'])
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json')
    ap.add_argument('--replay-source')
    args=ap.parse_args()
    values=[replay_source(args.replay_source)] if args.replay_source else generate(args.difficulty,args.count,args.seed)
    print(json.dumps(values,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
