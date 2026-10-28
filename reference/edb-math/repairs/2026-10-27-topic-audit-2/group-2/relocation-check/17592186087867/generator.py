#!/usr/bin/env python3
"""Seeded first-order linear ODE classification; no database or filesystem output."""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
import sympy as sp
from source_replay import read_equation, D as DERIVATIVE, D2 as SECOND
from math_format import normalize_prose, normalize_tex, validate_generated_record
from source_replay import KP_ID, KP_UUID, TITLE, TEMPLATES, generate as legacy_generate

VERSION='ode-classification-2'

class DuplicateBank(ValueError):
    pass

def bank_signatures(options):
    signatures=[]
    for o in options:
        residual=read_equation(o['equation'])
        if residual.has(SECOND):
            normalized=sp.cancel(residual/sp.diff(residual,SECOND))
        elif sp.diff(residual,DERIVATIVE,2)==0:
            normalized=sp.cancel(residual/sp.diff(residual,DERIVATIVE))
        else:
            normalized=residual
        signatures.append(sp.srepr(sp.expand(normalized)))
    return signatures

D=r'\frac{\text{d}y}{\text{d}x}'
D2=r'\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}'
FUNCS=('x','2x','3x',r'x^{2}',r'\sin(x)',r'\cos(x)',r'e^{x}',r'\ln(x)','2','3')
LINEAR=((1,0),(0,1),(1,1))
NONLINEAR=((2,0),(1,2),(-1,0),(0,-1),(2,1))
EASY_ERRORS=('quadratic','reciprocal','sqrt','sin','logxy','exp','second','square')
MEDIUM_ERRORS=('quadratic','reciprocal','sqrt','sin','logxy','exp')
SOURCES={
'easy':['q-8349','q-103551','q-103554','q-79753'],
'moderate':['q-103560','q-103557','q-103559','q-79752'],
'hard':['q-8352','q-79754','q-103567','q-79750']}

def mul(a,b):
    if a=='1': return b
    if b=='1': return a
    return '('+a+')'+b

def yp(n):
    if n==0:return '1'
    if n==1:return 'y'
    if n>1:return 'y^{'+str(n)+'}'
    return r'\frac{1}{'+yp(-n)+'}'

def powerterm(a,n):
    if n<0:return r'\frac{'+a+'}{'+yp(-n)+'}'
    return mul(a,yp(n))

def phi(kind):
    return {'quadratic':r'y^{2}','reciprocal':r'\frac{1}{y}',
            'sqrt':r'\sqrt{y}','sin':r'\sin(y)','logxy':r'\ln(xy)','exp':r'e^{y}'}[kind]

def aligned(rows):
    return '$$\n'+r'\begin{aligned}'+r' \\ '.join(s.replace('=', '&=',1) for s in rows)+r'\end{aligned}'+'\n$$'

def make_option(p,q,u=1,v=0,kind='powers',frame='direct',b='1'):
    """Ordered operator inputs. TeX is composed without CAS rewriting."""
    if kind in ('second','square'):
        deriv=D2 if kind=='second' else r'\left('+D+r'\right)^{2}'
        equation=deriv+'+'+mul(p,'y')+'='+q
        reason='It contains a second derivative, so it is not first order.' if kind=='second' else 'The first derivative is squared, so the equation is not linear in the derivative.'
        return {'equation':equation,'linear':False,'rows':[equation],'reason':reason,'kind':kind}
    is_power=kind=='powers'
    left=powerterm(p,u) if is_power else mul(p,phi(kind))
    right=powerterm(q,v)
    normal=D+'+'+left+'='+right
    rows=[]
    if frame=='direct': equation=normal
    elif frame=='xscale':
        equation=mul(b,D)+'+'+mul(b,'('+left+')')+'='+mul(b,'('+right+')')
    elif frame=='reciprocal':
        # Divide every term of the normalized equation by y.
        equation=r'\frac{1}{y}'+D+'+'+powerterm(p,u-1)+'='+powerterm(q,v-1)
    elif frame=='product':
        equation='y'+D+'+'+powerterm(p,u+1)+'='+powerterm(q,v+1)
    elif frame=='quotient':
        equation=r'\frac{1}{y}'+D+'='+r'\frac{'+right+'-'+left+'}{y}'
    else:raise ValueError(frame)
    rows.append(equation)
    if equation!=normal:rows.append(normal)
    linear=is_power and u in (0,1) and v in (0,1)
    if linear:
        if (u,v)==(1,0): std=normal; P=p;Q=q
        elif (u,v)==(0,1):P='-('+q+')';Q='-('+p+')';std=D+'-('+q+')y=-('+p+')'
        elif (u,v)==(1,1):P='('+p+')-('+q+')';Q='0';std=D+'+('+p+'-'+q+')y=0'
        else:raise ValueError((u,v))
        if rows[-1]!=std:rows.append(std)
        reason='This is standard form with $P(x)='+P+'$ and $Q(x)='+Q+'$, both depending only on $x$. It is a first-order linear ODE.'
    else:
        flow=D+'='+right+'-('+left+')'
        if rows[-1]!=flow:rows.append(flow)
        what= ('a quadratic term' if 2 in (u,v) else 'a reciprocal term') if is_power else {
            'quadratic':'a quadratic term','reciprocal':'a reciprocal term','sqrt':'a square root of $y$',
            'sin':'a sine of $y$','logxy':'a logarithm depending on $y$','exp':'an exponential of $y$'}[kind]
        reason='After collecting terms, '+what+' remains. The right-hand side is not of the form $Q(x)-P(x)y$, so this is not a first-order linear ODE.'
    return {'equation':equation,'linear':linear,'rows':rows,'reason':reason,'kind':kind,'powers':[u,v] if is_power else None,'frame':frame}

def record(options,level,negative,seed,profile,parameters,origin='authored',source_ids=None):
    signatures=bank_signatures(options)
    if len(set(signatures))!=len(options):
        raise DuplicateBank('Equivalent equations in complete bank')
    selected=[i for i,o in enumerate(options) if o['linear'] != negative]
    if len(selected)!=1:raise ValueError('Bank must have exactly one requested classification')
    problem='Which of the following is '+('**NOT** ' if negative else '')+'a first-order linear ordinary differential equation?'
    problem+='\n\nClassify on local intervals where the expressions are defined and $x>0$.'
    if level=='hard' or origin=='source-replay':problem+=r' Assume $y\ne0$ whenever a factor of $y$ is canceled.'
    solution='A first-order linear ODE can be written as\n\n$$\n'+D+'+P(x)y=Q(x).\n$$\n\n'
    if level=='hard':solution+='Normalize the derivative coefficient on the stated nonzero domain, then collect the terms in $y$.\n\n'
    for o in options:
        solution+=aligned(o['rows'])+'\n\n'+o['reason']+'\n\n'
    solution+='Therefore select\n\n$$\n'+options[selected[0]]['equation']+'\n$$'
    problem=normalize_prose(problem);solution=normalize_prose(solution)
    values=[normalize_tex(o['equation']) for o in options]
    payload={'problem':problem,'solution':solution,'values':values,'difficulty':level}
    key=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
    qid=uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/'+KP_UUID+'/'+VERSION+'/'+key)
    fid=uuid.uuid5(qid,'selection')
    answers=[{':answer/id':str(uuid.uuid5(fid,v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{
        ':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,
        ':question/problem':problem,':question/worked-solution':solution,
        ':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
        ':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[selected[0]][':answer/id']]}]},
        'generation':{'version':VERSION,'seed':seed,'template':profile,'bank_profile':profile,'origin':origin,
        'parameters':parameters,'source_analysis':{'database':'math','basis_t':7095,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','question_ids':source_ids or SOURCES[level]},
        'derivation':options,'domain':'local common real domain; x>0; canceled y factors nonzero'}}
    return validate_generated_record(result)

def _generate_once(level,seed,case_index=None):
    rng=random.Random(seed)
    # Choose mathematical profile/target assignments before x-only data.
    if level=='easy':
        negative=False;frame='direct'
        specs=[('powers',1,0)]+[(k,1,0) for k in rng.sample(EASY_ERRORS,4)]
    elif level=='moderate':
        negative=True;frame='xscale'
        error=MEDIUM_ERRORS[(case_index if case_index is not None else rng.randrange(6))%6]
        specs=[(error,1,0)]+[('powers',*rng.choice(LINEAR)) for _ in range(4)]
    elif level=='hard':
        case=case_index if case_index is not None else rng.randrange(6)
        negative=bool(case%2);frame=('reciprocal','product','quotient')[(case//2)%3]
        specs=([('powers',*rng.choice(NONLINEAR))]+[('powers',*rng.choice(LINEAR)) for _ in range(4)] if negative else
               [('powers',*rng.choice(LINEAR))]+[('powers',*pat) for pat in rng.sample(NONLINEAR,4)])
    else:raise ValueError(level)
    rng.shuffle(specs)
    p=rng.choice(FUNCS);q=rng.choice([f for f in FUNCS if f!=p]);b=rng.choice(('2','3','x',r'x^{2}',r'\frac{1}{x}'))
    # Distinct function pairs prevent duplicate equations when affine patterns repeat.
    pairs=[(p,q)]
    while len(pairs)<5:
        pair=(rng.choice(FUNCS),rng.choice(FUNCS))
        if pair[0]!=pair[1] and pair not in pairs:pairs.append(pair)
    options=[make_option(pi,qi,u,v,kind,frame,b) for (kind,u,v),(pi,qi) in zip(specs,pairs)]
    return record(options,level,negative,seed,level+'-'+frame,{'pairs':pairs,'specs':specs,'frame':frame,'b':b})

def generate(level,seed,case_index=None):
    retry=random.Random(seed)
    realized=seed
    for attempt in range(100):
        try:
            result=_generate_once(level,realized,case_index)
            result['generation'].update({'seed':seed,'realized_seed':realized,'bank_attempts':attempt+1})
            return result
        except DuplicateBank:
            realized=retry.getrandbits(63)
    raise RuntimeError('Cannot construct a distinct complete bank')

def replay(name):
    """Source banks at original parameters; explanation corrected by actual reduction."""
    import sympy as sp
    from source_replay import read_equation,linear_flow,X,Y,D as deriv
    spec=TEMPLATES[name]
    latex=lambda value:sp.latex(value).replace(r'\operatorname{atan}',r'\arctan').replace(r'\atan',r'\arctan').replace(r'\log',r'\ln')
    options=[]
    # Preserve the complete original bank, not authored replacements.
    for v in spec['choices']:
        equation=v.replace('@@X@@','x');residual=read_equation(equation);flow=linear_flow(residual)
        rows=[equation]
        if flow is not None:
            P=sp.simplify(-sp.diff(flow,Y));Q=sp.simplify(flow.subs(Y,0))
            std=D+'+('+latex(P)+')y='+latex(Q)
            rows.append(std)
            reason='After normalization on the stated domain, $P(x)='+latex(P)+'$ and $Q(x)='+latex(Q)+'$ depend only on $x$. This is first-order linear.'
        else:
            # The original explanation remains useful for the sole target, but give
            # all options a precise classification instead of a power-of-log claim.
            coefficient=sp.diff(residual,deriv)
            if residual.has(__import__('source_replay').D2):reason='A second derivative is present, so it is not first order.'
            elif coefficient.has(deriv):reason='A squared derivative is present, so it is not linear.'
            else:
                normalized=sp.cancel(-(residual-coefficient*deriv)/coefficient)
                rows.append(D+'='+latex(normalized))
                reason='After normalization and collection, nonlinear dependence on $y$ remains, so this is not a first-order linear ODE.'
        options.append({'equation':equation,'linear':flow is not None,'rows':rows,'reason':reason,'kind':'source'})
    return record(options,spec['level'],'**NOT**' in spec['problem'],0,name,{'a':1,'h':0},'source-replay',[spec['source']])

def batch(level,count,seed):
    if count<1:raise ValueError('count must be positive')
    rng=random.Random(seed)
    # Stratify decision cases without attaching a case to a fixed seed or position.
    schedule=list(range(6));rng.shuffle(schedule)
    records=[];seen=set();i=0
    while len(records)<count:
        case=schedule[len(records)%6]
        r=generate(level,rng.getrandbits(63),case)
        i+=1
        identity=r['question'][':question/id']
        if identity not in seen:records.append(r);seen.add(identity)
        if i>count*30:raise RuntimeError('Cannot construct distinct requested batch')
    return records

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='moderate')
    p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=('json',),default='json');p.add_argument('--replay',choices=tuple(TEMPLATES))
    args=p.parse_args()
    if args.count<1:p.error('count must be positive')
    levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    records=[replay(args.replay)] if args.replay else [r for level in levels for r in batch(level,args.count,args.seed)]
    print(json.dumps(records,indent=2))
if __name__=='__main__':main()
