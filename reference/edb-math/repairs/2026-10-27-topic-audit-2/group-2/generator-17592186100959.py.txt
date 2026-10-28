#!/usr/bin/env python3
"""Seeded, relocatable checkbox generator for verifying first-order ODE solutions."""
import copy
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as s
from math_format import normalize_prose, validate_generated_record
from generator_policy import nonempty_checkbox

VERSION='2.0.0'
KP={'db_id':17592186100959,'id':'80ed79a9-8e39-5c84-9c87-dec266060afc','title':'Identifying Solutions to First-Order Differential Equations'}
X=s.Symbol('x',positive=True)
Y=s.Symbol('y',real=True)
FAMILIES={'easy':['exp'],'moderate':['exp','power','sin','cos','affine','log'],'hard':['log']}
SOURCES={'exp':[17592186101158,17592186348206], 'power':[17592186272207,17592186272208,17592186272209,17592186348207], 'sin':[17592186272204], 'cos':[17592186272205], 'affine':[17592186101538], 'log':[17592186272206,17592186272210]}

def tex(v):
    return s.latex(v,ln_notation=True)

def coefficient(v):
    return '' if v==1 else '-' if v==-1 else tex(v)

def uid(v):
    return str(uuid.uuid5(uuid.NAMESPACE_URL,'ca-ode-v2:'+str(v)))

def norm(v):
    return normalize_prose(v)

def simple(v):
    return s.simplify(s.trigsimp(s.expand(v)))

def instance(level,family,p):
    """Operator inputs, candidate functions and ordered conversions are shared."""
    k=p.get('k',1); h=p.get('h',0); n=p.get('n',2); a=p.get('a',2); slope=p.get('p',1)
    if family=='exp': rhs=k*(Y-h)
    elif family=='power': rhs=k*(Y-h)/X
    elif family=='sin': rhs=k*(Y-h)*s.cot(k*X)
    elif family=='cos': rhs=-k*(Y-h)*s.tan(k*X)
    elif family=='affine': rhs=n*Y/X+(1-n)*a
    else: rhs=a*slope*s.exp(-Y/a)
    rhs_tex=(r'\frac{'+tex(a*slope)+r'}{e^{y/'+str(a)+r'}}') if family=='log' else tex(rhs)
    candidates=[]
    for c in p['candidates']:
        conversion=[]
        if family in ('exp','power','sin','cos'):
            A,b,d=c
            f=A*({'exp':lambda:s.exp(b*X),'power':lambda:X**b,'sin':lambda:s.sin(b*X),'cos':lambda:s.cos(b*X)}[family]())+d
            ft=tex(f)
        elif family=='affine':
            A,b,d=c;f=A*X**n+b*X+d;ft=tex(f)
        else:
            A,t,b,mode=c; z=t*X+b
            if mode=='direct':
                f=A*s.log(z);ft=coefficient(A)+r'\ln\left('+tex(z)+r'\right)'
                reduced=slope*a*z**(-s.Rational(A,a))
                conversion=[r'e^{\frac{'+ft+r'}{'+str(a)+r'}}='+tex(z**s.Rational(A,a))]
            elif mode=='square':
                f=s.Mul(s.Rational(A,2),s.log(s.Pow(z,2,evaluate=False),evaluate=False),evaluate=False)
                ft=coefficient(s.Rational(A,2))+r'\ln\left(\left('+tex(z)+r'\right)^2\right)'
                reduced=slope*a*z**(-s.Rational(A,a))
                conversion=[r'\sqrt{\left('+tex(z)+r'\right)^2}='+tex(z), r'e^{\frac{'+ft+r'}{'+str(a)+r'}}='+tex(z**s.Rational(A,a))]
            else:
                z=t**2*X**2+b
                f=s.Mul(s.Rational(A,2),s.log(z,evaluate=False),evaluate=False)
                ft=coefficient(s.Rational(A,2))+r'\ln\left('+tex(z)+r'\right)'
                reduced=slope*a*z**(-s.Rational(A,2*a))
                power=s.Pow(z,s.Rational(A,2*a),evaluate=False)
                conversion=[r'e^{\frac{'+ft+r'}{'+str(a)+r'}}='+tex(power)]
                if tex(power)!=tex(z**s.Rational(A,2*a)):
                    conversion.append(tex(power)+'='+tex(z**s.Rational(A,2*a)))
        derivative=s.diff(f,X)
        sub=rhs.subs(Y,f)
        if family=='log':result=reduced
        elif family=='sin' and b==k:result=A*k*s.cos(k*X)+(d-h)*k*s.cot(k*X)
        elif family=='cos' and b==k:result=-A*k*s.sin(k*X)-(d-h)*k*s.tan(k*X)
        else:result=simple(sub)
        residual=simple(derivative-result)
        ok=(residual==0)
        counterexample=None
        if not ok:
            for v in ([s.pi/(4*k)] if family in ('sin','cos') else [1,2,s.Rational(1,2),3,4]):
                val=simple(residual.subs(X,v))
                if val.is_finite and val.is_zero is False:
                    counterexample=(tex(v),tex(simple(derivative.subs(X,v))),tex(simple(result.subs(X,v))));break
            if counterexample is None: raise ValueError('No proved counterexample')
        candidates.append({'f':f,'tex':ft,'derivative':derivative,'sub':sub,'result':result,'truth':ok,'conversion':conversion,'counterexample':counterexample})
    if any(simple(candidates[i]['f']-candidates[j]['f'])==0 for i in range(3) for j in range(i)):
        raise ValueError('Equivalent function choices')
    return rhs,rhs_tex,candidates

def substitution(family,p,ft):
    wrap=r'\left('+ft+r'\right)'
    if family=='log':return r'\frac{'+str(p['a']*p.get('p',1))+r'}{e^{\frac{'+ft+'}{'+str(p['a'])+r'}}}'
    # The RHS operator is printed with its candidate input intact.
    k=p.get('k',1);h=p.get('h',0)
    centered=wrap if not h else r'\left('+ft+('+' if h<0 else '-')+tex(abs(h))+r'\right)'
    if family=='exp':return tex(k)+r'\cdot '+centered
    if family=='power':return r'\frac{'+tex(k)+r'\cdot '+centered+r'}{x}'
    if family=='sin':return tex(k)+r'\cdot '+centered+r'\cot\left('+tex(k*X)+r'\right)'
    if family=='cos':return tex(-k)+r'\cdot '+centered+r'\tan\left('+tex(k*X)+r'\right)'
    return r'\frac{'+str(p['n'])+r'\cdot '+wrap+r'}{x}'+('+' if (1-p['n'])*p['a']>=0 else '')+str((1-p['n'])*p['a'])

def make_record(level,family,p,seed=0,include_none=True):
    rhs,rt,cs=instance(level,family,p)
    domain=r'x\in\mathbb{R}' if family=='exp' else r'0<x<\frac{\pi}{'+str(p['k'])+'}' if family=='sin' else r'0<x<\frac{\pi}{'+str(2*p['k'])+'}' if family=='cos' else 'x>0'
    prompt='Consider the differential equation\n\n$$\ny\'='+rt+r',\qquad '+domain+'.\n$$\n\n'
    if level=='easy':
        prompt+='The derivatives of the proposed functions are provided:\n\n'+'\n'.join('- For $y='+c['tex']+"$, $y'="+tex(c['derivative'])+'$.' for c in cs)+'\n\nSubstitute each function and its derivative into the equation. '
    prompt+='Which functions are solutions throughout the stated interval? Select all that apply.'
    solution="A function is a **solution** if its derivative equals the differential equation's right-hand side at every point of the stated interval. Differentiate each candidate and substitute it for $y$.\n\n"
    if family in ('sin','cos'):
        z=tex(p['k']*X)
        solution+='Use $'+(r'\cot('+z+r')=\frac{\cos('+z+r')}{\sin('+z+')}' if family=='sin' else r'\tan('+z+r')=\frac{\sin('+z+r')}{\cos('+z+')}')+'$ on the stated interval.\n\n'
    for c in cs:
        solution+='For $y='+c['tex']+'$:\n\n'
        if c['conversion']:
            solution+='The logarithm arguments are positive because $x>0$. Using the exponential and logarithm identities gives\n\n$$\n'+r'\begin{aligned}'+r'\\'.join(z.replace('=', '&=',1) for z in c['conversion'])+r'\end{aligned}'+'\n$$\n\n'
        solution+='$$\n'+r'\begin{aligned}'+"y'&="+tex(c['derivative'])+r'\\'+r'\text{RHS}&='+substitution(family,p,c['tex'])+r'\\'+'&='+tex(c['result'])+r'.\end{aligned}'+'\n$$\n\n'
        if c['truth']:solution+='The two expressions agree throughout the interval, so this function **is a solution**.\n\n'
        else:
            v,left,right=c['counterexample']
            solution+='At $x='+v+"$, $y'="+left+'$ whereas $'+r'\text{RHS}='+right+'$. Thus they are not identical, so this function **is not a solution**.\n\n'
    flags=[c['truth'] for c in cs]
    keys=['$y='+c['tex']+'$' for c in cs]
    if include_none:
        flags.append(not any(flags));keys.append('None of the above')
        solution+=('None of the proposed functions is a solution; select **None of the above**.' if not any(flags[:3]) else 'Select the functions verified above; do not select **None of the above**.')
    prompt=norm(prompt);solution=norm(solution);keys=[norm(k) for k in keys]
    content=json.dumps([level,prompt,solution,keys,flags],sort_keys=True)
    qid=uid(hashlib.sha256(content.encode()).hexdigest());fields=[]
    for i,(key,flag) in enumerate(zip(keys,flags)):
        fid=uid(qid+'/'+str(i))
        choices=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in ['false','true']]
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+'/'+str(flag).lower())]})
    record={'knowledge_point':KP,'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':family,'parameters':p,'source_question_ids':SOURCES[family],'domain':domain,'origin':'authored same-method extension'}}
    return validate_generated_record(record)

def parameters(level,family,mask,rng):
    """Truth roles precede compatible values. Full candidate banks are resampled."""
    p={}
    if family in ('exp','power','sin','cos'):
        p['k']=rng.choice([-1,1] if level=='easy' else [-3,-2,-1,1,2,3] if family in ('exp','power') else [1,2,3])
        p['h']=rng.choice([-1,0,0,1])
    elif family=='affine':p.update(n=rng.choice([2,3]),a=rng.choice([-2,-1,1,2]))
    else:p.update(a=rng.choice([1,2]),p=1 if level=='moderate' else rng.choice([1,2]))
    cs=[]
    for i in range(3):
        good=bool(mask&(1<<i))
        if family in ('exp','power','sin','cos'):
            A=rng.choice([-3,-2,-1,1,2,3]);b=p['k'];d=p['h']
            if not good:
                if family in ('sin','cos') or rng.randrange(2):d+=rng.choice([-2,-1,1,2])
                else:b=-b if level=='easy' else rng.choice([v for v in [-3,-2,-1,1,2,3] if v!=b])
            c=[A,b,d]
        elif family=='affine':
            A=rng.choice([-2,-1,0,1,2]);b=p['a'];d=0
            if not good:
                if rng.randrange(2):b+=rng.choice([-2,-1,1,2])
                else:d=rng.choice([-2,-1,1,2])
            c=[A,b,d]
        else:
            mode='direct' if level=='moderate' else rng.choice(['direct','square','quadratic'])
            A=p['a'];t=p['p'];b=0 if mode=='quadratic' else rng.choice([0,1,2,3])
            if not good:
                if mode=='quadratic':b=rng.choice([1,2,3])
                elif rng.randrange(2):A=rng.choice([v for v in [-2,-1,1,2,3,4] if v!=p['a']])
                else:t=3-p['p']
            c=[A,t,b,mode]
        cs.append(c)
    p['candidates']=cs
    return p

def generate(level,seed=0,family=None,mask=None,parameters_override=None):
    if level not in FAMILIES:raise ValueError('Unknown difficulty')
    rng=random.Random(seed);family=family or rng.choice(FAMILIES[level])
    if family not in FAMILIES[level]:raise ValueError('Family outside difficulty')
    mask=rng.randrange(8) if mask is None else mask
    if not 0<=mask<=7:raise ValueError('Invalid mask')
    if parameters_override is not None:return make_record(level,family,parameters_override,seed)
    for _ in range(128):
        p=parameters(level,family,mask,rng)
        if level=='hard' and all(c[3]=='direct' for c in p['candidates']):continue
        try:r=make_record(level,family,p,seed)
        except ValueError:continue
        return r
    raise ValueError('Unable to construct distinct candidate bank')

generate=nonempty_checkbox(generate,none_label='None of the above')

def batch(level,count,seed):
    rng=random.Random(seed);families=[];masks=[];out=[];seen=set();attempt=0
    while len(out)<count:
        if not families:families=list(FAMILIES[level]);rng.shuffle(families)
        if not masks:masks=list(range(8));rng.shuffle(masks)
        family=families.pop();mask=masks.pop();subseed=rng.getrandbits(64)
        r=generate(level,subseed,family,mask)
        qid=r['question'][':question/id'];attempt+=1
        if qid not in seen:out.append(r);seen.add(qid)
        if attempt>count*100+128:raise ValueError('Batch capacity exceeded')
    return out

def replay_source(source_id):
    from mathparse import parse, X as RX, Y as RY
    row=next(r for r in json.loads(Path(__file__).with_name('source-replay.json').read_text()) if r['source_id']==source_id)
    q=copy.deepcopy(row['question']);rhs=parse(row['rhs']);computed=[]
    for f in q[':question/answer-fields']:
        key=f[':answer-field/key']
        if key.startswith('$'):
            function=parse(key[1:-1].split('=',1)[1])
            truth=s.simplify(s.trigsimp(s.diff(function,RX)-rhs.subs(RY,function)))==0
            computed.append(truth)
        else:truth=not any(computed) if len(computed)==3 else None
        # None can appear first in captured order; calculate after all functions.
    flags=[]
    for f in q[':question/answer-fields']:
        if f[':answer-field/key'].startswith('$'):flags.append(computed.pop(0))
        else:flags.append(None)
    none_value=not any(v for v in flags if v is not None)
    qid=uid('source:'+str(source_id)+':'+q[':question/problem']+q[':question/worked-solution'])
    q[':question/id']=qid
    for key in [':db/id',':question/math-academy-id']:q.pop(key,None)
    q[':question/difficulty']=':question.difficulty/moderate'
    for i,(field,flag) in enumerate(zip(q[':question/answer-fields'],flags)):
        fid=uid(qid+'/'+str(i));flag=none_value if flag is None else flag
        field.clear();field.update({':answer-field/id':fid,':answer-field/key':row['question'][':question/answer-fields'][i][':answer-field/key'],':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in ['false','true']],':answer-field/correct':[':answer/id',uid(fid+'/'+str(flag).lower())]})
    r={'knowledge_point':KP,'question':q,'generation':{'version':VERSION,'origin':'source replay with normalized presentation','source_question_ids':[source_id]}}
    return validate_generated_record(r)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');args=ap.parse_args()
    if args.count<1:ap.error('--count must be positive')
    print(json.dumps(batch('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
