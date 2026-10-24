"""Topic478: scaffolded substitution, with controlled prerequisite work.

Easy asks for a supplied substitution's transformed integral. Moderate asks for
the whole calculation. Hard changes one target condition, keeping arithmetic
small. Primitive formulas and endpoint values are supplied for full calculations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import uuid

import sympy as s
from trig_format import normalize_prose, normalize_tex

X,U=s.symbols('x u',real=True)
R,PI=s.Rational,s.pi
VERSION='4.0.0-scaffolded-substitution'
TRIG=('sin','cos','sec2','csc2','sec_tan','csc_cot')
RECIP=TRIG[2:]
LINEAR=('indef_sin','indef_cos','def_sin','def_cos')
RECIP_CASES=tuple(prefix+fn for prefix in ('indef_','def_')for fn in RECIP)
CASES={
    17592186068915:{level:LINEAR for level in ('easy','moderate','hard')},
    17592186068916:{'easy':RECIP,'moderate':RECIP_CASES,'hard':RECIP_CASES},
    17592186068917:{'easy':TRIG,'moderate':TRIG,
                   'hard':tuple('reciprocal_'+fn for fn in TRIG)+('sqrt_sin','sqrt_cos')},
    17592186068918:{'easy':('sin','cos','tan','sec'),
                   'moderate':('sin','cos','tan','sec','csc','cot','sin2','cos3'),
                   'hard':('rearranged_tan','rearranged_sec','nested_sin','nested_tan','def_sin2','def_cos3')},
}


def tex(z):return normalize_tex(s.latex(z))


def times(a,body):
    a=s.sympify(a)
    return body if a==1 else '-'+body if a==-1 else tex(a)+r'\left('+body+r'\right)'


def fun(name,z):return getattr(s,name)(z,evaluate=False)


def g(fn,z):
    if fn.endswith('2'):return fun(fn[:-1],z)**2
    if fn=='sec_tan':return fun('sec',z)*fun('tan',z)
    if fn=='csc_cot':return fun('csc',z)*fun('cot',z)
    return fun(fn,z)


def h(fn,z):
    pf,sign={'sin':('cos',-1),'cos':('sin',1),'sec2':('tan',1),
             'csc2':('cot',-1),'sec_tan':('sec',1),'csc_cot':('csc',-1)}[fn]
    return sign*fun(pf,z)


def derivative(fn,z):
    return {'sin':lambda:fun('cos',z),'cos':lambda:-fun('sin',z),
            'tan':lambda:fun('sec',z)**2,'sec':lambda:fun('sec',z)*fun('tan',z),
            'csc':lambda:-fun('csc',z)*fun('cot',z),'cot':lambda:-fun('csc',z)**2}[fn]()


def integral(body,var='x',lo=None,hi=None):
    limits='' if lo is None else '_{'+tex(lo)+'}^{'+tex(hi)+'}'
    return r'\int'+limits+' '+body+r'\,\mathrm{d}'+var


def logabs(z):return r'\ln\left|'+tex(z)+r'\right|'


def task_key(body,lo=None,hi=None):
    return hashlib.sha256(json.dumps([s.srepr(s.trigsimp(body)),
        None if lo is None else s.srepr(s.simplify(lo)),
        None if hi is None else s.srepr(s.simplify(hi))]).encode()).hexdigest()


def endpoint_pair(fn,rng):
    if fn in ('sin','cos'):
        pairs=((0,PI/2),(PI/2,PI),(0,PI),(PI,3*PI/2),(3*PI/2,2*PI))
        # Skip cancellations that make the integral zero.
        return rng.choice([pair for pair in pairs if s.simplify(h(fn,pair[1])-h(fn,pair[0]))!=0])
    return rng.choice({
        'sec2':((0,PI/4),(-PI/4,0),(-PI/4,PI/4)),
        'csc2':((PI/4,PI/2),(PI/2,3*PI/4),(PI/4,3*PI/4)),
        'sec_tan':((0,PI/3),(-PI/3,0)),
        'csc_cot':((PI/6,PI/2),(PI/2,5*PI/6)),
    }[fn])


def trig_instance(kp,level,case,rng):
    linear=kp==17592186068915
    definite=case.startswith('def_')
    fn=case.removeprefix('indef_').removeprefix('def_')
    a=s.Integer(rng.choice((2,3,4)))
    A=s.Integer(rng.randint(1,3 if level=='easy' else 4))
    if level=='easy' and A*a>8:A=s.Integer(1)
    b=s.Integer(0)
    if level=='moderate' and not definite:b=s.Integer(rng.randint(0,3))
    if level=='hard':
        a=-a
        if not definite:b=s.Integer(rng.randint(1,3))
    lo=hi=None
    if definite:
        u0,u1=endpoint_pair(fn,rng)
        if level=='hard':
            u0,u1=u1,u0
            b=u0 # start x at zero; preserve familiar transformed angles
        lo,hi=s.simplify((u0-b)/a),s.simplify((u1-b)/a)
    inner=a*X+b;r=s.cancel(A/a)
    return dict(kind=fn,inner=inner,du=a,body=A*g(fn,inner),factor=r,
        transformed=g(fn,U),primitive_u=r*h(fn,U),primitive=r*h(fn,inner),
        lo=lo,hi=hi,scale=a,amplitude=A,
        parameters={'slope':str(a),'shift':str(b),'amplitude':str(A)},
        challenge='supplied_substitution' if level=='easy' else 'positive_affine' if level=='moderate' else 'negative_inner_derivative',
        source_questions=['q-10061','q-10064','q-350039','q-350040'] if linear else ['q-10143','q-2203','q-13663','q-350053','q-350055','q-13524'])


def product_instance(level,case,rng):
    A=s.Integer(rng.randint(1,3));b=s.Integer(rng.randint(0,2))
    if level=='hard':
        role,fn=case.split('_',1)
        if role=='reciprocal':
            inner=1/(X+b);du=-1/(X+b)**2;outer=A/(X+b)**2;r=-A
        else:
            inner=s.sqrt(X+b);du=1/(2*s.sqrt(X+b));outer=A/s.sqrt(X+b);r=2*A
        params={'inner_role':role,'shift':str(b),'amplitude':str(A)}
        challenge='recognize_'+role
    else:
        fn=case;n=rng.choice((2,3))
        if level=='easy':b=s.Integer(0)
        inner=X**n+b;du=n*X**(n-1);outer=A*X**(n-1);r=R(A,n)
        params={'inner_role':'power','power':n,'shift':str(b),'amplitude':str(A)}
        challenge='supplied_substitution' if level=='easy' else 'recognize_power'
    return dict(kind=fn,inner=inner,du=du,body=outer*g(fn,inner),factor=r,
        transformed=g(fn,U),primitive_u=r*h(fn,U),primitive=r*h(fn,inner),lo=None,hi=None,
        scale=s.cancel(outer/r).as_coeff_Mul()[0],amplitude=A,parameters=params,challenge=challenge,
        source_questions=['q-13461','q-13474','q-13464','q-13471','q-13467','q-13470','q-2377','q-3038'])


def quotient_instance(level,case,rng):
    definite=case.startswith('def_');nested=case.startswith('nested_');rearranged=case.startswith('rearranged_')
    name=case.split('_',1)[1] if definite or nested or rearranged else case
    fn=name.rstrip('23');power=3 if name.endswith('3') else 2 if name.endswith('2') else 1
    d=s.Integer(rng.randint(1,3));c=s.Integer(rng.choice((1,2))) if level=='easy' else s.Integer(1)
    A=s.Integer(rng.randint(1,3));theta=X**2 if nested else X
    t=fun(fn,theta);inner=d+c*t**power
    du=c*power*t**(power-1)*derivative(fn,theta)*s.diff(theta,X)
    # Keep the displayed numerator small; the derivative's sign is the only
    # sign adjustment. No frequency, fractional amplitude or extra phase.
    sign=-1 if fn in ('cos','csc','cot') else 1
    scale=c*power*(2 if nested else 1)*sign
    r=s.cancel(A/scale)
    numerator=s.cancel(r*scale)*t**(power-1)*(derivative(fn,theta)/sign)*(X if nested else 1)
    transformed=1/U
    if rearranged:
        # u=d+t, and t/u=(u-d)/u. Leave all other components simple.
        c=s.Integer(1);power=1;inner=d+t;du=derivative(fn,theta)
        r=A;scale=s.Integer(1);numerator=A*t*derivative(fn,theta)
        transformed=1-d/U
    body=numerator/inner
    lo=hi=None
    if definite:
        # Both primitive endpoint arguments are small integers; trig recall is
        # supplied in the prompt rather than used to manufacture a hard item.
        lo=s.Integer(0);hi=PI/2
    primitive_u=r*(U-d*s.log(U)) if rearranged else r*s.log(U)
    return dict(kind=name,inner=inner,du=du,body=body,body_tex=r'\frac{'+tex(numerator)+'}{'+tex(inner)+'}',
        factor=r,transformed=transformed,primitive_u=primitive_u,primitive=primitive_u.subs(U,inner),
        lo=lo,hi=hi,scale=scale,amplitude=A,log=True,rearranged=rearranged,d=d,theta=theta,trig_fn=fn,
        parameters={'offset':str(d),'denominator_scale':str(c),'amplitude':str(A),'power':power,'inner_role':'quadratic' if nested else 'identity'},
        challenge='supplied_substitution' if level=='easy' else 'recognize_denominator' if level=='moderate' else 'definite_evaluation' if definite else 'rational_rearrangement' if rearranged else 'nested_inner',
        source_questions=['q-49557','q-113998','q-350887','q-350901','q-350908','q-350892','q-73679','q-113987','q-73674','q-114004','q-113997','q-113992'])


def primitive_tex(m,z):
    r=m['factor']
    if not m.get('log'):return tex(r*h(m['kind'],z))
    if m.get('rearranged'):return times(r,tex(z)+'-'+times(m['d'],logabs(z)))
    return times(r,logabs(z))


def easy_bank(m,rng):
    r=m['factor'];lo,hi=m['lo'],m['hi']
    u0,u1=(None,None) if lo is None else tuple(s.simplify(m['inner'].subs(X,v))for v in (lo,hi))
    def value(c,l,h):
        if l is None:return c # same nonconstant transformed integrand, different coefficient
        return s.simplify(c*(hfun(h)-hfun(l)))
    hfun=lambda z:h(m['kind'],z)
    correct_value=value(r,u0,u1)
    options=[(r,u0,u1,'correct')]
    if lo is not None:
        A=m['amplitude'];a=m['scale']
        candidates=[(A,u0,u1,'omit reciprocal derivative'),(A*a,u0,u1,'multiply by derivative'),
                    (r,lo,hi,'keep original bounds'),(r,u1,u0,'reverse only bounds')]
    else:
        A=m['amplitude'];a=m['scale']
        candidates=[(A,None,None,'omit reciprocal derivative'),(A*a,None,None,'multiply by derivative'),
                    (r/a,None,None,'divide twice'),(-r,None,None,'reverse factor sign'),
                    (r/2,None,None,'extra half'),(2*r,None,None,'extra double'),
                    (-A,None,None,'omit factor and reverse sign'),(-2*r,None,None,'double and reverse sign')]
        rng.shuffle(candidates)
    values=[correct_value]
    for c,l,h_,label in candidates:
        c=s.cancel(c)
        if c==0 or abs(c)>8 or c.q>8:continue
        v=value(c,l,h_)
        if any(s.simplify(s.trigsimp(v-old))==0 for old in values):continue
        options.append((c,l,h_,label));values.append(v)
        if len(options)==5:break
    if len(options)!=5:raise ValueError('Ambiguous or incomplete authored transformed-integral bank')
    rng.shuffle(options)
    return [(times(c,integral(tex(m['transformed']),'u',l,h_)),label)for c,l,h_,label in options]


def render(kp,level,case,m,seed,evidence,rng):
    inner,du,r,lo,hi=(m[k]for k in ('inner','du','factor','lo','hi'))
    definite=lo is not None;easy=level=='easy'
    body=m.get('body_tex',tex(m['body']));original=integral(body,lo=lo,hi=hi)
    u0,u1=(None,None)if not definite else tuple(s.simplify(inner.subs(X,v))for v in(lo,hi))
    target=times(r,integral(tex(m['transformed']),'u',u0,u1))
    if easy:
        problem='Use the substitution $u='+tex(inner)+'$. Which integral is obtained?\n\n$$\n'+original+'\n$$'
    else:
        problem=('Evaluate exactly.'if definite else 'Find an antiderivative.')+'\n\n$$\n'+original+'\n$$\n\n'
        formula=logabs(U)if m.get('log')else tex(h(m['kind'],U))
        problem+='You may use $'+integral('1/u'if m.get('log')else tex(g(m['kind'],U)),'u')+'='+formula+'+C$.'
        if definite:
            if m.get('log'):
                # Values of the original trig function suffice to find the new
                # bounds; no unrelated exact-value recall is left implicit.
                fn=m['trig_fn']
                facts=[tex(fun(fn,v))+'='+tex(s.simplify(getattr(s,fn)(v)))for v in(lo,hi)]
            else:
                pf={'sin':'cos','cos':'sin','sec2':'tan','csc2':'cot','sec_tan':'sec','csc_cot':'csc'}[m['kind']]
                facts=[tex(fun(pf,v))+'='+tex(s.simplify(getattr(s,pf)(v)))for v in(u0,u1)]
            problem+='\n\nEndpoint values: $'+r',\quad '.join(facts)+'$.'
        problem+='\n\n{{answer}}'+(''if definite else ' $+C$')
    sol='Let $u='+tex(inner)+'$. Then\n\n$$\n'+r'\frac{\mathrm{d}u}{\mathrm{d}x}='+tex(du)+'.\n$$\n\n'
    if definite:
        sol+='Transform both bounds:\n\n$$\n'+r'\begin{aligned}x='+tex(lo)+r'&\Longrightarrow u='+tex(u0)+r'\\x='+tex(hi)+r'&\Longrightarrow u='+tex(u1)+r'\end{aligned}'+'\n$$\n\n'
        if u0>u1:sol+='The new bounds decrease. Keep this order when evaluating the antiderivative.\n\n'
    if m.get('rearranged'):
        sol+='Since $'+tex(fun(m['trig_fn'],m['theta']))+'=u-'+tex(m['d'])+'$, rewrite the remaining factor:\n\n$$\n'+r'\frac{u-'+tex(m['d'])+r'}{u}=1-\frac{'+tex(m['d'])+'}{u}.\n$$\n\n'
    sol+='Including the differential factor gives\n\n$$\n'+r'\begin{aligned}&'+original+r'\\&='+target+r'.\end{aligned}'+'\n$$\n\n'
    if easy:
        sol+='The transformed integral is\n\n$$\n'+target+'.\n$$'
        key=target;answer=None;bank=easy_bank(m,rng)
    elif not definite:
        pu=primitive_tex(m,U);key=primitive_tex(m,inner)
        sol+='Integrate with respect to $u$:\n\n$$\n'+target+'='+pu+'+C.\n$$\n\nSubstitute back:\n\n$$\n'+key+'+C.\n$$'
        answer=m['primitive'];bank=[(key,'correct')]
    elif m.get('log'):
        assert u0>0 and u1>0
        # Keep the difference of logs. No hidden power/quotient simplification.
        key=times(r,r'\ln\left('+tex(u1)+r'\right)-\ln\left('+tex(u0)+r'\right)')
        sol+='Both transformed bounds are positive. Evaluating gives\n\n$$\n'+times(r,r'\left[\ln u\right]_{'+tex(u0)+'}^{'+tex(u1)+'}')+'='+key+'.\n$$\n\nThe answer is\n\n$$\n'+key+'.\n$$'
        answer=r*(s.log(u1)-s.log(u0));bank=[(key,'correct')]
    else:
        first,last=(s.simplify(m['primitive_u'].subs(U,v))for v in(u0,u1))
        answer=s.simplify(last-first);key=tex(answer)
        sol+='Integrate and evaluate:\n\n$$\n'+r'\left['+primitive_tex(m,U)+r'\right]_{'+tex(u0)+'}^{'+tex(u1)+'}='+r'\left('+tex(last)+r'\right)-\left('+tex(first)+r'\right).'+'\n$$\n\nThe answer is\n\n$$\n'+key+'.\n$$'
        bank=[(key,'correct')]
    fp=task_key(m['body'],lo,hi)
    uid=lambda role:str(uuid.uuid5(uuid.UUID(evidence['kp']['id']),VERSION+':'+fp+':'+('transform'if easy else 'evaluate')+':'+role))
    answers=[{':answer/id':uid('answer:'+text),':answer/type':':answer.type/math',':answer/value':normalize_tex(text)}for text,_ in bank]
    correct=next(a[':answer/id']for a,(_,label)in zip(answers,bank)if label=='correct')
    question={':question/id':uid('question'),':question/problem':normalize_prose(problem),
              ':question/worked-solution':normalize_prose(sol),':question/difficulty':':question.difficulty/'+level,
              ':question/answer-fields':[{':answer-field/id':uid('field'),':answer-field/key':'answer',
                  ':answer-field/type':':answer-field.type/radio'if easy else ':answer-field.type/blank',
                  ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    model={k:str(v)if v is not None else None for k,v in dict(integrand=m['body'],substitution=inner,
        derivative=du,factor=r,transformed=m['transformed'],primitive=m['primitive'],
        lower=lo,upper=hi,result=answer).items()}
    return {'knowledge_point':evidence['kp'],'question':question,'generation':{
        'version':VERSION,'seed':seed,'template':case,'family':case,'challenge':m['challenge'],
        'parameters':m['parameters'],'mathematical_fingerprint':fp,'model':model,
        'batch_contract':'trig-scaffolding-v4','source_questions':m['source_questions'],
        'source_basis':evidence['basis'],'band_origin':evidence['band_origin'][level],
        'operation':'transform'if easy else 'evaluate','provided_substitution':easy,
        'provided_primitive':not easy,'provided_endpoint_values':definite and not easy,
        'bank_profile':'authored transformed-integral bank; no imported-bank replay claim'if easy else 'exact fragment with external C for antiderivatives',
        'bank_recipes':[label for _,label in bank],'dependencies':{'sympy':s.__version__},
        'domain':'Connected real intervals where the displayed integrand is defined; all definite intervals avoid poles.'}}


def draw(kp,level,case,seed,evidence,index,attempt):
    rng=random.Random(f'{seed}:{kp}:{level}:{case}:{index}:{attempt}')
    m=trig_instance(kp,level,case,rng)if kp in(17592186068915,17592186068916)else product_instance(level,case,rng)if kp==17592186068917 else quotient_instance(level,case,rng)
    return render(kp,level,case,m,seed,evidence,rng)


def generate(kp,level,seed=0,template=None,*,evidence,index=0,attempt=0):
    if kp not in CASES or level not in CASES[kp]:raise ValueError('Unsupported KP or difficulty')
    cases=CASES[kp][level]
    if template is not None and template not in cases:raise ValueError('Unsupported template for this band')
    case=template or random.Random(f'{seed}:{kp}:{level}:one').choice(cases)
    excluded=set(evidence['excluded_tasks'])
    for offset in range(attempt,attempt+200):
        try:record=draw(kp,level,case,seed,evidence,index,offset)
        except ValueError:continue
        meta=record['generation']
        if meta['mathematical_fingerprint']in excluded:continue
        if meta['model']['lower']is not None and not meta['provided_substitution']and s.simplify(s.sympify(meta['model']['result']))==0:continue
        return record
    raise ValueError('No eligible bounded variant; no duplicate padding')


def batch(kp,level,count=8,seed=0,*,evidence,template=None):
    if type(count)is not int or not 1<=count<=100:raise ValueError('Count must be 1 through 100')
    if kp not in CASES or level not in CASES[kp]:raise ValueError('Unsupported KP or difficulty')
    order=list(CASES[kp][level]);random.Random(f'{seed}:{kp}:{level}:order').shuffle(order)
    seen=set();shapes=set();rows=[]
    for index in range(count):
        case=template or order[index%len(order)]
        for attempt in range(200):
            r=generate(kp,level,seed,case,evidence=evidence,index=index,attempt=attempt)
            m=r['generation'];shape=(case,m['model']['substitution'],m['model']['lower'],m['model']['upper'])
            if m['mathematical_fingerprint']in seen or shape in shapes:continue
            rows.append(r);seen.add(m['mathematical_fingerprint']);shapes.add(shape);break
        else:raise ValueError('Finite capacity reached; no amplitude-only padding')
    return rows


def cli(kp,folder):
    p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True,choices=('easy','moderate','hard'))
    p.add_argument('--count',type=int,default=8);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--template');p.add_argument('--format',choices=('json','markdown'),default='json');a=p.parse_args()
    evidence=json.loads((Path(folder)/'source-evidence.json').read_text())
    rows=batch(kp,a.difficulty,a.count,a.seed,evidence=evidence,template=a.template)
    if a.format=='json':print(json.dumps(rows,indent=2))
    else:
        print('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+
            '\n'.join('$'+v[':answer/value']+'$'for v in r['question'][':question/answer-fields'][0][':answer-field/choices'])+
            '\n\n'+r['question'][':question/worked-solution']for r in rows))
