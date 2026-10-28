#!/usr/bin/env python3
"""Supplied-solution IVP constant recognition (math basis 1356).

No ODE solving is assessed. Source masks, including ordered stage omissions,
are documented in the private evidence folder. Observed opaque banks are public
parameterized evidence profiles, never sampled as normal learner defaults.
Easy: supplied power/exponential/trig/reciprocal/log families as observed.
Moderate (authored): same exponential substitution with a nonzero rational input.
Hard (authored): same reciprocal/log affine constant isolation at nonzero input.
Each level is independent, with no solving techniques or instructional progression.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186100951
KP_UUID='82a9b23c-4c79-56cd-9761-79d0ee22646d'
TITLE='Identifying Solutions to Initial Value Problems'
VERSION='ivp-constant-v3'
ROOT=Path(__file__).resolve().parent
X,Y,A=sp.symbols('x y A', real=True)
# id: family, coefficient, initial x, initial y, original field
SPECS={
'q-141055':('exp',2,1,3,'radio'), 'q-141117':('recip',-1,1,4,'radio'),
'q-141107':('power',4,-1,-1,'radio'), 'q-141108':('exp',-1,0,1,'radio'),
'q-141109':('exp',-2,0,2,'radio'), 'q-141111':('cos',2,sp.pi/8,sp.sqrt(2),'radio'),
'q-141114':('power',1,-1,3,'radio'), 'q-347839':('sin',3,sp.pi/6,1,'blank'),
'q-352649':('cos',2,sp.pi/8,sp.sqrt(2),'blank'), 'q-352654':('exp',3,2,5,'blank'),
'q-352655':('exp',-4,1,2,'blank'), 'q-352656':('exp',1,-1,4,'blank'),
'q-352660':('invpower',4,2,sp.Rational(3,4),'blank'), 'q-352661':('recip',-1,0,3,'blank'),
'q-352663':('power',3,2,4,'blank'), 'q-141112':('invpower',1,-2,-1,'radio'),
'q-141113':('invpower',2,2,-1,'radio'), 'q-141115':('log',1,1,1,'radio'),
'q-141116':('recip',1,0,sp.Rational(1,2),'radio')}
TEMPLATES={q:{'level':'easy','family':s[0],'kind':s[4],'source':q} for q,s in SPECS.items()}
TEMPLATES.update({'exponential_nonzero':{'level':'moderate','family':'exp','kind':'blank','source':None},
'reciprocal_nonzero':{'level':'hard','family':'recip','kind':'blank','source':None},
'logarithmic_nonzero':{'level':'hard','family':'log','kind':'blank','source':None}})
# Finite reduced number-form catalogs are shared by random and explicit easy inputs.
# The rational numerator bound is applied after reduction, independently of magnitude.
EASY_RATIONAL_VALUES=tuple(sorted({sp.Rational(n,d) for n in range(-8,9) if n for d in range(1,5)}))
EASY_TRIG_VALUES=tuple(v for base in (sp.Integer(1),sp.Integer(2),sp.Integer(3),sp.sqrt(2),sp.sqrt(3),sp.sqrt(2)/2,sp.sqrt(3)/2) for v in (base,-base))
MASKS=json.loads((ROOT/'masks.json').read_text())
def exact(v):
    return sp.sympify(v,locals={'pi':sp.pi,'sqrt':sp.sqrt,'E':sp.E})
def tex(v):
    v=exact(v)
    if v==sp.pi/8:return r'\frac{\pi }{8}'
    if v==sp.pi/6:return r'\frac{\pi }{6}'
    if v==sp.pi/4:return r'\frac{\pi }{4}'
    if v==sp.pi/2:return r'\frac{\pi }{2}'
    return sp.latex(v).replace(r'\log',r'\ln').replace(r'\left', '').replace(r'\right','')
def coeff(k,var):
    return var if k==1 else '-'+var if k==-1 else tex(k)+var

def math_object(f,k,u,b):
    if f=='power': fun=A*X**k; rhs=k*Y/X; a=b/u**k
    elif f=='invpower':fun=A/X**k;rhs=-k*Y/X;a=b*u**k
    elif f=='exp':fun=A*sp.exp(k*X);rhs=k*Y;a=b*sp.exp(-k*u)
    elif f=='sin':fun=A*sp.sin(k*X);rhs=k*Y*sp.cot(k*X);a=b/sp.sin(k*u)
    elif f=='cos':fun=A*sp.cos(k*X);rhs=-k*Y*sp.tan(k*X);a=b/sp.cos(k*u)
    elif f=='recip':fun=1/(A+k*X);rhs=-k*Y**2;a=1/b-k*u
    elif f=='log':fun=sp.log(A+X);rhs=sp.exp(-Y);a=sp.exp(b)-u
    return fun,rhs,sp.simplify(a)

def validate_parameters(level,f,p,observed=False):
    if set(p)!={'k','u','b'}:raise ValueError('parameters must have exactly k, u, b')
    k,u,b=(exact(p[z]) for z in ('k','u','b'))
    if not all(z.is_real is True and not z.free_symbols for z in (k,u,b)):raise ValueError('finite real exact parameters required')
    if k not in range(-4,5) or k==0 or abs(b)>8 or b==0:raise ValueError('coefficient/initial value outside finite workload bounds')
    if level=='easy':
        catalog=EASY_TRIG_VALUES if f in ('sin','cos') else EASY_RATIONAL_VALUES
        if b not in catalog:raise ValueError('easy initial output outside the finite reduced number-form catalog')
    if f in ('power','invpower') and (k<1 or u==0 or not u.is_Integer or abs(u)>3):raise ValueError('power requires n=1..4 and nonzero integer input |u|<=3')
    if f=='exp' and (not u.is_Rational or abs(u)>3 or u.q>2):raise ValueError('exponential input must be integer or half-integer |u|<=3')
    if f in ('sin','cos') and k*u not in (sp.pi/6,sp.pi/4,sp.pi/3,sp.pi/2,2*sp.pi/3,3*sp.pi/4):raise ValueError('familiar evaluation angle required')
    if f=='sin' and sp.sin(k*u)==0 or f=='cos' and sp.cos(k*u)==0:raise ValueError('nonzero function factor required')
    if f=='recip' and (k not in (-1,1) or not u.is_Rational or abs(u)>3 or u.q>2 or not b.is_Rational or b.q>4):raise ValueError('reciprocal bounds')
    if f=='log' and (k!=1 or not u.is_Rational or abs(u)>3 or u.q>2 or not b.is_Integer or abs(b)>3):raise ValueError('log bounds')
    if level=='moderate' and (f!='exp' or u==0 or u.q!=2 or abs(k*u)>6 or not b.is_Rational or b.q>3):raise ValueError('moderate requires a nonzero half-integer input, |ku|<=6, rational b denominator<=3')
    if level=='hard' and (f not in ('recip','log') or u==0):raise ValueError('hard requires affine constant isolation at nonzero input')
    if level=='hard' and f=='recip' and (b.q==1 or abs(b)>3):raise ValueError('hard reciprocal requires noninteger rational b, |b|<=3')
    return {'k':k,'u':u,'b':b}

def components(qid,f,p,normal=False):
    k,u,b=(p[z] for z in ('k','u','b'));fun,rhs,a=math_object(f,k,u,b)
    legacy=qid in ('q-141055','q-141117'); spaces=qid in ('q-347839','q-352649')
    tr=lambda name:r'\operatorname{'+name+'}\u2061'.replace('\\u2061','\u2061')
    power=lambda var:var if k==1 else '{'+var+'}^{'+tex(k)+'}'
    exp=lambda e:'{e}^{'+e+'}'
    if f=='power':form='A'+power('x');ode=r'\frac{'+coeff(k,'y')+'}{x}'
    elif f=='invpower':form=r'\frac{A}{'+power('x')+'}';ode='-'+r'\frac{'+coeff(k,'y')+'}{x}'
    elif f=='exp':form='A'+('e' if legacy else '{e}')+'^{'+coeff(k,'x')+'}';ode=coeff(k,'y')
    elif f in ('sin','cos'):
        arg=coeff(k,'x'); par=qid!='q-141111';form='A'+tr(f)+('('+arg+')' if par else arg)
        name='cot' if f=='sin' else 'tan'; ode=coeff(k if f=='sin' else -k,'y')+tr(name)+('('+arg+')' if par else arg)
    elif f=='recip':
        sign='+' if k==1 else '-';inner='A'+sign+'x';form=r'\frac{1}{'+inner+'}';ode=('' if k==-1 else '-')+r'{y}^{2}'
        if legacy:form=r'\frac{1}{A - x}';ode=r'y^{2}'
    elif f=='log':form=tr('ln')+'(A+x)';ode=r'{e}^{-y}'
    condition='y'+(r'\,' if spaces else '')+'('+tex(u)+')='+tex(b)
    given='y='+form
    if legacy:
        given='y = '+form
        prompt_eq=r'\frac{dy}{dx} = '+ode+', y('+tex(u)+') = '+tex(b)
    else:prompt_eq=r'\frac{\text{d}y}{\text{d}x}='+ode+r',\,'+condition+'.'
    av=tex(a);bt=tex(b);ut=tex(u)
    if qid=='q-352654':av=r'\frac{'+bt+'}{{e}^{'+tex(k*u)+'}}'
    if qid in ('q-352655','q-352656'):
        ep=-k*u; av=bt+('e' if ep==1 else '{e}^{'+tex(ep)+'}')
    if qid=='q-141115':
        et='e' if b==1 else '{e}^{'+tex(b)+'}'
        av=et+('-'+tex(u) if u>0 else '+'+tex(-u) if u<0 else '')
    rows=[('y',form)]
    if f=='power':
        rows += [(bt,'A('+ut+')'+('^{'+tex(k)+'}' if k!=1 else '')),(bt,coeff(u,'A') if k==1 else 'A('+tex(u**k)+')'),('A',av)]
    elif f=='invpower':
        den=('('+ut+')' if qid=='q-141112' else '{'+ut+'}^{'+tex(k)+'}')
        rows += [(bt,r'\frac{A}{'+den+'}')]
        if k!=1:rows.append((bt,r'\frac{A}{'+tex(u**k)+'}'))
        rows.append(('A',av))
    elif f=='exp':
        sub=('-'+ut if k==-1 else ut if k==1 else tex(k)+( '('+ut+')' if qid=='q-141109' else r'\cdot '+('('+ut+')' if u<0 else ut)))
        rows.append((bt,'A'+exp(sub)))
        if qid=='q-141108':rows.append((bt,'A('+tex(sp.exp(k*u))+')'))
        else:
            rows.append((bt,'A'+exp(tex(k*u))))
            if qid=='q-141109':rows.append((bt,'A('+tex(sp.exp(k*u))+')'))
            else:rows.append((av,'A'))
        rows.append(('A',av))
    elif f in ('sin','cos'):
        t=k*u;val=(sp.sin(t) if f=='sin' else sp.cos(t));tf=tr(f)
        sub=(f+r'\,' if not normal and qid in ('q-347839','q-352649') else tf)+'('+tex(k)+r'\cdot '+ut+')'
        rows += [(bt,'A'+sub),(bt,'A'+(f+r'\,' if not normal and qid=='q-347839' else tf)+'('+tex(t)+')'),(bt,'A'+(r'\cdot '+tex(val) if qid=='q-352649' else '('+tex(val)+')')),('A',av)]
    elif f=='recip':
        si='+' if k==1 else '-'; ui='('+ut+')' if u<0 else ut
        rows += [(bt,r'\frac{1}{A'+si+ui+'}')]
        if u==0:rows.append((bt,r'\frac{1}{A}'))
        else:rows.append((r'\frac{1}{'+bt+'}','A'+si+ui))
        rows.append(('A',av))
    elif f=='log':
        ui='('+ut+')' if u<0 else ut; tf=tr('ln'); e=sp.exp(b)
        rows += [(bt,tf+'(A+'+ui+')'),(exp(bt),exp(tf+'(A+'+ui+')')),(tex(e),'A+'+ui),('A',av)]
    stages=r'\begin{aligned}'+r' \\ '.join(l+' & ='+r for l,r in rows)+r'.\end{aligned}'
    final='y='+tex(fun.subs(A,a))
    if qid=='q-141107':final='y=('+av+')'+power('x')+'='+coeff(a,power('x'))
    if qid=='q-141108':final='y='+av+exp(coeff(k,'x'))+'='+coeff(a,exp(coeff(k,'x')))
    if qid=='q-141109':final='y='+av+exp(coeff(k,'x'))
    if qid=='q-141114':final='y='+coeff(a,'x')
    if qid=='q-141111':final='y='+av+tr('cos')+coeff(k,'x')
    if qid=='q-141113':final='y='+('-' if a<0 else '')+r'\frac{'+tex(abs(a))+'}{'+power('x')+'}'
    if qid=='q-141115':final='y='+tr('ln')+'('+av+'+x)'
    if qid=='q-141116':final=r'y=\frac{1}{'+av+('+' if k==1 else '-')+'x}'
    return {'prompt_equation':prompt_eq,'given':given,'condition':condition,'condition_period':condition+'.','stages':stages,'final':final+'.'},a

def fill(mask,parts):
    for k,v in parts.items():mask=mask.replace('@@'+k+'@@',v)
    if '@@' in mask:raise ValueError('unfilled source slot')
    return mask

def bank(qid,p,a):
    k,u,b=(p[z] for z in ('k','u','b'))
    # Opaque source banks use a documented proportional A profile. This is a
    # parameterized value pattern, NOT a recovered diagnostic error model.
    opaque={'q-141107':(4,-1,2,-2,1),'q-141108':(0,-2,2,-1,1),'q-141109':(2,1,sp.Rational(-1,2),0,-1),
    'q-141114':(sp.Rational(1,3),1,sp.Rational(-1,3),2,-1),
    'q-141112':(sp.Rational(-1,3),1,sp.Rational(1,2),sp.Rational(3,4),sp.Rational(-1,2)),
    'q-141113':(sp.Rational(-1,8),sp.Rational(-1,2),1,-1,sp.Rational(1,16)),
    'q-141116':(sp.Rational(-1,4),sp.Rational(1,4),1,sp.Rational(1,2),sp.Rational(-1,2))}
    if qid in opaque:return [sp.simplify(c*a) for c in opaque[qid]]
    if qid=='q-141055':return [b*sp.exp(u),a,1/b,b*sp.exp(k*u),b]
    if qid=='q-141117':return [u-1/b,a,b,2*a,u]
    if qid=='q-141111':return [-sp.cos(k*u),-a,b,sp.cos(k*u),a]
    if qid=='q-141115':return [sp.exp(b)+u,2*sp.exp(b)-u,2*u,a,u]
    return [a]

def source_parameters(qid):
    _,k,u,b,_=SPECS[qid];return {z:str(v) for z,v in zip(('k','u','b'),(k,u,b))}

# Each authored bank is chosen from the displayed family's substitution operation,
# before sampling parameters. These complete banks are never mixed or patched.
AUTHORED_BANK_OPERATIONS={
 'power_nonunit':('correct divide by u^n','use one excess factor of u','use one fewer factor of u','invert initial y before dividing','omit input factor'),
 'power_unary':('correct divide by u','multiply by u instead of dividing','omit the input factor','invert the isolation ratio','invert b before dividing by u'),
 'invpower_nonunit':('correct multiply by u^n','use one excess factor of u','use one fewer factor of u','invert initial y before multiplying','omit input factor'),
 'invpower_unary':('correct multiply by u','divide by u instead of multiplying','omit the input factor','invert b before multiplying by u','invert the entire isolated product'),
 'exp':('correct divide by exp(k*u)','multiply by exp(k*u) instead of dividing','omit the exponential factor','invert the isolation ratio','invert b before dividing by exp(k*u)'),
 'sin':('correct divide by sin(k*u)','multiply by sin(k*u) instead of dividing','omit the trigonometric factor','evaluate cosine instead of sine','invert the isolation ratio'),
 'cos':('correct divide by cos(k*u)','multiply by cos(k*u) instead of dividing','omit the trigonometric factor','evaluate sine instead of cosine','invert the isolation ratio'),
 'recip':('correct invert b then subtract the input shift','add the input shift instead of subtracting','omit inversion of b','subtract the shift before inversion','negate the reciprocal before subtracting the shift'),
 'log':('correct exponentiate b then subtract the input','add the input instead of subtracting','omit exponentiation of b','subtract the input before exponentiating','negate the exponent before subtracting the input')}

def authored_bank_name(t):
    f=t['family']
    if f=='power':return 'power_unary' if t['source']=='q-141114' else 'power_nonunit'
    if f=='invpower':return 'invpower_unary' if t['source']=='q-141112' else 'invpower_nonunit'
    return f

def authored_bank(name,p):
    k,u,b=(p[z] for z in ('k','u','b'))
    if name=='power_nonunit':return [b/u**k,b/u**(k+1),b/u**(k-1),1/(b*u**k),b]
    if name=='power_unary':return [b/u,b*u,b,u/b,1/(b*u)]
    if name=='invpower_nonunit':return [b*u**k,b*u**(k+1),b*u**(k-1),u**k/b,b]
    if name=='invpower_unary':return [b*u,b/u,b,u/b,1/(b*u)]
    if name=='exp':
        factor=sp.exp(k*u);return [b/factor,b*factor,b,factor/b,1/(b*factor)]
    if name in ('sin','cos'):
        factor=(sp.sin(k*u) if name=='sin' else sp.cos(k*u));other=(sp.cos(k*u) if name=='sin' else sp.sin(k*u))
        return [b/factor,b*factor,b,b/other,factor/b]
    if name=='recip':return [1/b-k*u,1/b+k*u,b-k*u,1/(b-k*u),-1/b-k*u]
    if name=='log':return [sp.exp(b)-u,sp.exp(b)+u,b-u,sp.exp(b-u),sp.exp(-b)-u]
    raise ValueError('unknown authored complete bank')

def eligible_values(values,a):
    values=[sp.simplify(v) for v in values]
    return all(v.is_real is True and v.is_finite is True for v in values) and all(sp.simplify(v-w)!=0 for i,v in enumerate(values) for w in values[i+1:]) and sum(sp.simplify(v-a)==0 for v in values)==1

def sample(level,f,rng):
    if level=='moderate':return {'k':rng.choice([-4,-3,-2,2,3,4]),'u':rng.choice([sp.Rational(i,2) for i in [-3,-1,1,3]]),'b':rng.choice([sp.Rational(i,j) for j in [1,2,3] for i in [-5,-3,-1,1,3,5]])}
    if level=='hard':return {'k':rng.choice([-1,1]) if f=='recip' else 1,'u':rng.choice([-2,-1,sp.Rational(-1,2),sp.Rational(1,2),1,2]),'b':rng.choice([sp.Rational(i,j) for j in [2,3,4] for i in [-5,-3,-1,1,3,5] if abs(sp.Rational(i,j))<=3 and sp.Rational(i,j).q>1]) if f=='recip' else rng.choice([-2,-1,1,2])}
    if f in ('power','invpower'):
        # Initial-value magnitude is an error-relevant decision case: inversion
        # moves it across 1. Choose the regime before incidental values.
        magnitudes=rng.choice(((sp.Rational(1,2),sp.Rational(2,3),sp.Rational(3,4)),(sp.Rational(3,2),sp.Integer(2),sp.Integer(3))))
        b=rng.choice((-1,1))*rng.choice(magnitudes)
        return {'k':rng.choice([1,2,3,4]),'u':rng.choice([-2,-1,1,2]),'b':b}
    if f in ('sin','cos'):
        k=rng.choice([1,2,3,4]); t=rng.choice([sp.pi/6,sp.pi/4,sp.pi/3,2*sp.pi/3,3*sp.pi/4] if f=='cos' else [sp.pi/6,sp.pi/4,sp.pi/3,sp.pi/2,2*sp.pi/3,3*sp.pi/4]);return {'k':k,'u':t/k,'b':rng.choice(EASY_TRIG_VALUES)}
    return {'k':rng.choice([1,2,3,4]) if f in ('power','invpower') else rng.choice([-3,-2,-1,1,2,3]) if f=='exp' else rng.choice([-1,1]) if f=='recip' else 1,'u':rng.choice([-2,-1,1,2]) if f in ('power','invpower') else rng.choice([-2,-1,0,1,2]),'b':rng.choice([-3,-2,-1,1,2,3] if f=='log' else EASY_RATIONAL_VALUES)}

def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown level')
    rng=random.Random(seed)
    if profile:
        if profile.startswith('observed:') or profile.startswith('completed:'):template=profile.split(':')[1]
        elif profile!='authored':raise ValueError('unknown profile')
    pool=[t for t,v in TEMPLATES.items() if v['level']==level and (field_type is None or v['kind']==field_type)]
    if template is None:template=rng.choice(pool)
    if template not in pool:raise ValueError('template/field type outside level')
    t=TEMPLATES[template];f=t['family'];qid=t['source'];observed=bool(profile and profile.startswith('observed:'));completed=bool(profile and profile.startswith('completed:'))
    if (observed or completed) and not qid:raise ValueError('observed profile requires source template')
    bank_name=authored_bank_name(t) if t['kind']=='radio' and not (observed or completed) else None
    for attempt in range(200):
        sampled=parameters if parameters is not None else sample(level,f,rng)
        required_k={'q-141117':-1,'q-141114':1,'q-141112':1}
        if qid in required_k:
            if parameters is not None and exact(sampled['k'])!=required_k[qid]:raise ValueError('source layout coefficient constraint')
            sampled=dict(sampled,k=required_k[qid])
        p=validate_parameters(level,f,sampled,observed)
        if bank_name in ('power_nonunit','invpower_nonunit') and p['k']==1:
            if parameters is not None:raise ValueError('selected nonunit power bank requires exponent >=2')
            continue
        render_id=qid or ('q-352654' if f=='exp' else 'q-352661' if f=='recip' else 'q-141115')
        parts,a=components(render_id,f,p,normal=not observed)
        kind=t['kind']
        if observed or completed:
            problem=fill(MASKS[qid]['prompt'],parts)
            solution=fill(MASKS[qid]['solution'],parts) if MASKS[qid]['solution'] is not None else None
            values=bank(qid,p,a)
        else:
            problem='Consider the following initial value problem\n\n$$\n'+parts['prompt_equation']+'\n$$\n\nYou\'re given that $'+parts['given']+'$ is the solution to this initial value problem. What is the value of the constant $A?$'
            if kind=='blank':problem+='\n\n$A=${{field-1}}'
            solution="We're given that $"+parts['given']+"$ is the solution to the initial value problem. Therefore, it must satisfy the differential equation *and* the initial condition $"+parts['condition_period']+"$\n\nSubstituting the initial condition $"+parts['condition']+"$ into our solution and solving for $A,$ we get\n\n$$\n"+parts['stages']+'\n$$'
            values=[a] if kind=='blank' else authored_bank(bank_name,p)
        if completed and solution is None:solution="Substituting the initial condition $"+parts['condition']+"$ into the supplied solution, we get\n\n$$\n"+parts['stages']+'\n$$'
        values=[sp.simplify(v) for v in values]
        valid=eligible_values(values,a)
        if valid:break
        if parameters is not None:raise ValueError('whole choice bank rejected for equivalence or ambiguity')
    else:raise ValueError('no eligible instance')
    if not observed:solution=solution.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln')
    # Source sine/cosine typo is repaired structurally; source equation order stays fixed.
    key='selection' if kind=='radio' else 'field-1'
    vals=[tex(v).replace(' ','') if observed else tex(v) for v in values]
    if qid=='q-141115' and observed:vals=['{e}^{'+tex(p['b'])+'}'+('+' if p['u']>=0 else '-')+tex(abs(p['u'])),tex(2*sp.exp(p['b'])).replace(' ','')+('-' if p['u']>=0 else '+')+tex(abs(p['u'])),tex(2*p['u']),parts['stages'].split('A & =')[-1].split('.')[0],tex(p['u'])]
    if qid=='q-141115' and observed:
        vals=[v.replace('{e}^{1}','e') for v in vals]
    # Preserve the supplied exp answer-fragment convention for its original blank.
    if qid=='q-352654' and (observed or completed):vals=[tex(p['b'])+'/{e}^{'+tex(p['k']*p['u'])+'}']
    if qid=='q-352655' and (observed or completed):vals=[tex(p['b'])+'{e}^{'+tex(-p['k']*p['u'])+'}']
    if qid in ('q-352661','q-352663') and (observed or completed):vals=[str(a)]
    rawmissing=observed and qid in ('q-141055','q-141117')
    identity={'version':VERSION,'prompt':problem,'solution':solution,'kind':kind,'bank':sorted(vals),'difficulty':None if rawmissing else level,'correct_present':not rawmissing}
    h=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest();field_id=uid(h+'/'+key)
    answers=[{':answer/id':uid(field_id+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
    correct=answers[next(i for i,v in enumerate(values) if sp.simplify(v-a)==0)][':answer/id']
    if kind=='radio':rng.shuffle(answers)
    field={':answer-field/id':field_id,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
    if not rawmissing:field[':answer-field/correct']=[':answer/id',correct]
    question={':question/id':uid(h),':question/problem':problem,':question/answer-fields':[field]}
    if not rawmissing:question[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:question[':question/worked-solution']=solution
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'template':template,'seed':seed,'parameters':{z:str(v) for z,v in p.items()},'profile':profile or 'authored','authored_bank':bank_name,'bank_operations':AUTHORED_BANK_OPERATIONS[bank_name] if bank_name else None,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'authored_level':level!='easy','evidence_only':observed or completed,'eligible_for_learning':not (observed or completed),'content_hash':h,'mathematical_fingerprint':hashlib.sha256(sp.srepr(math_object(f,p['k'],p['u'],p['b'])[0]) .encode()+sp.srepr(p['u']).encode()+sp.srepr(p['b']).encode()).hexdigest(),'domain':('x != 0; use the half-line containing u' if f in ('power','invpower') else 'A+k*x != 0; use the interval containing u after substituting A' if f=='recip' else 'A+x > 0 after substituting A' if f=='log' else 'sin(k*x) != 0; use the interval containing u' if f=='sin' else 'cos(k*x) != 0; use the interval containing u' if f=='cos' else 'all real x'),'source_anomalies':(['missing difficulty, worked solution and correct ref'] if qid in ('q-141055','q-141117') else ['unmarked sin/cos operator in original substitution row'] if qid in ('q-347839','q-352649') else []),'repairs':['unmarked sin/cos operator in substitution row'] if qid in ('q-347839','q-352649') and completed else []}}

