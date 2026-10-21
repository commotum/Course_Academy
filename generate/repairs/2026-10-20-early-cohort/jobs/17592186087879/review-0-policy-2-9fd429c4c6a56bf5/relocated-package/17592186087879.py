#!/usr/bin/env python3
"""Integrating-factor IVPs, basis 1356. Steps 3–7 only; no database access.

Observed presentation templates use component masks for the initial value and
integration constant (cos/x² additionally supports forcing amplitude). Complete
observed banks are parameterized formulas, never answer lookups. Two ambiguous
legacy banks are explicitly evidence-only; normal banks are authored operations.
All levels use the same complete IF -> general solution -> initial-condition skill.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
KP=17592186087879
TITLE='Solving First-Order Initial Value Problems Using Integrating Factors'
VERSION='ivp-integrating-factors-2'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
CURRENT=json.loads((HERE/'current-source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in CURRENT['record'][':knowledge-point/questions']}
x=sp.Symbol('x',positive=True); C=sp.Symbol('C',real=True)
# Each observed presentation remains its own template, including unrated layouts.
OBS={
'q-334916':('moderate','constant',{'a':1,'b':1,'h':-3},4,5),
'q-335808':('hard','quadratic',{'d':2,'b':2,'h':1},4,5),
'q-335810':('moderate','nonstandard',{'b':1,'h':2},4,4),
'q-335811':('moderate','cosine',{'k':1,'h':0},4,5),
'q-335812':('moderate','sine',{'k':1,'h':1},4,5),
'q-335806':('moderate','cancellation',{'a':1,'b':1,'h':-2},4,5),
'q-335829':('moderate','constant',{'a':4,'b':2,'h':-1},4,5),
'q-339145':('hard','quadratic',{'d':6,'b':6,'h':5},4,5),
'q-335830':('moderate','trig_cancellation',{'a':-2,'h':4},4,5)}
AUTH={'easy_constant':('easy','constant'), 'moderate_nonstandard':('moderate','nonstandard'),
      'moderate_cancellation':('moderate','cancellation'), 'moderate_cosine':('moderate','cosine'),
      'moderate_sine':('moderate','sine'), 'hard_quadratic':('hard','quadratic'),
      'hard_cubic':('hard','cubic')}
TEMPLATES={**{k:(v[0],v[1]) for k,v in OBS.items()},**AUTH}

def tex(e):
    return sp.latex(sp.sympify(e),order='lex').replace(r'\log',r'\ln')

@lru_cache(maxsize=10000)
def eq(a,b):
    delta=sp.expand(a-b)
    if delta==0:return True
    if delta.is_zero is False:return False
    return sp.simplify(delta)==0

def model(f,p):
    h=sp.sympify(p['h'])
    if f=='constant':
        a,b=map(sp.sympify,(p['a'],p['b'])); P=a; Q=a*b; I=sp.exp(a*x); F=b*I; t=sp.S(0)
    elif f in ('quadratic','cubic'):
        d,b=map(sp.sympify,(p['d'],p['b'])); n=2 if f=='quadratic' else 3
        U=x**n/(n*d); P=x**(n-1)/d; Q=b*P; I=sp.exp(U); F=b*I; t=sp.S(0)
    elif f=='nonstandard':
        b=sp.sympify(p['b']); P=2/x; Q=4*b*x; I=x**2; F=b*x**4; t=sp.S(1)
    elif f=='cancellation':
        a,b=map(sp.sympify,(p['a'],p['b'])); P=a; Q=2*b*x*sp.exp(-a*x); I=sp.exp(a*x); F=b*x**2; t=sp.S(0)
    elif f=='trig_cancellation':
        a=sp.sympify(p['a']); P=a; Q=sp.exp(-a*x)*sp.sin(x); I=sp.exp(a*x); F=-sp.cos(x); t=sp.S(0)
    elif f=='cosine':
        k=sp.sympify(p['k']); P=2/x; Q=k*sp.cos(x)/x**2; I=x**2; F=k*sp.sin(x); t=sp.pi
    elif f=='sine':
        k=sp.sympify(p['k']); P=1/x; Q=k*sp.sin(x)/x; I=x; F=-k*sp.cos(x); t=sp.pi/2
    else: raise ValueError(f)
    const=sp.simplify(h*I.subs(x,t)-F.subs(x,t))
    y=sp.simplify((F+const)/I)
    return dict(P=P,Q=Q,I=I,F=F,t=t,h=h,c=const,y=y,g=(F+C)/I)

def check_parameters(level,template,p,profile):
    f=TEMPLATES[template][1]
    required={'constant':{'a','b','h'},'quadratic':{'d','b','h'},'cubic':{'d','b','h'},
              'nonstandard':{'b','h'},'cancellation':{'a','b','h'},'trig_cancellation':{'a','h'},'cosine':{'k','h'},'sine':{'k','h'}}[f]
    if set(p)!=required: raise ValueError('Parameter keys must be '+str(sorted(required)))
    for key,v in p.items():
        if not isinstance(v,int) or isinstance(v,bool): raise ValueError('Integer parameters required')
    if template in OBS:
        base=OBS[template][2]
        for key in required-{'h','k'}:
            if p[key]!=base[key]: raise ValueError('Observed masks keep this coefficient fixed; use authored template')
        if f=='cosine' and p['h']!=0: raise ValueError('Observed zero-constant stage sequence requires h=0')
        if 'k' in p and f!='cosine' and p['k']!=1: raise ValueError('Observed sine presentation fixes forcing amplitude')
        if not -8<=p['h']<=8 or 'k' in p and not 1<=p['k']<=5: raise ValueError('Observed parameter bounds')
    else:
        if not -6<=p['h']<=6: raise ValueError('Initial values must be -6..6')
        for key in required-{'h'}:
            if not 1<=p[key]<=6: raise ValueError('Coefficients must be 1..6')
        if f=='constant' and level=='easy' and p['a']!=1: raise ValueError('Easy fixes unit P')
        if f=='quadratic' and not 2<=p['d']<=6: raise ValueError('Hard quadratic requires fractional P')
        if f=='cubic' and not 1<=p['d']<=4: raise ValueError('Hard cubic bounds')
    if profile not in ('authored','observed'): raise ValueError('Unknown profile')
    if profile=='observed' and template not in OBS: raise ValueError('No observed bank')

def source_masks(qid,p,m):
    """Slot complete initial-condition and particular-constant components only.

    Source strings are immutable evidence. The source mask is the same recipe for
    original and changed values: there is no branch returning the original record.
    """
    q=QUESTIONS[qid]; original=OBS[qid][2]; old=model(OBS[qid][1],original)
    prompt=q[':question/problem']; solution=q.get(':question/worked-solution')
    init=re.compile(r'(y\([^\n]*?\)\s*=\s*)'+re.escape(str(original['h']))+r'(?!\d)')
    prompt=init.sub(lambda z:z.group(1)+str(p['h']),prompt)
    if solution is None: return prompt, authored_solution(OBS[qid][1],p,m)
    # Complete components with separate unevaluated substitution/evaluation masks.
    mapping={}
    if qid=='q-335810':
        mapping={'y(1)=2':'y(1)='+str(p['h']), '2 & =1+C':str(p['h'])+' & =1+C',
                 'C & =1':'C & ='+tex(m['c']),r'y={x}^{2}+\frac{1}{{x}^{2}}.':'y='+tex(m['y'])+'.'}
    elif qid=='q-335811':
        k=p['k']; prefix='' if k==1 else str(k)
        for name in ('sin','cos'):
            prompt=prompt.replace(r'\operatorname{'+name+'}⁡x',prefix+r'\operatorname{'+name+'}⁡x')
            solution=solution.replace(r'\operatorname{'+name+'}⁡',prefix+r'\operatorname{'+name+'}⁡')
    elif qid=='q-335812':
        mapping={'y(\\frac{\\pi }{2})=1':'y(\\frac{\\pi }{2})='+str(p['h']),
                 '1 & =\\frac{2C}{\\pi }':str(p['h'])+' & =\\frac{2C}{\\pi }',
                 r'C & =\frac{\pi }{2}':'C & ='+tex(m['c']),
                 r'-\operatorname{cos}⁡x+\frac{\pi }{2}':r'-\operatorname{cos}⁡x'+('+' if m['c']>=0 else '-')+tex(abs(m['c'])),
                 r'\frac{\pi }{2x}':tex(m['c']/x),
                 r'\frac{\pi -2\operatorname{cos}⁡x}{2x}':tex(m['y'])}
    elif qid=='q-335806':
        mapping={'y(0)=-2':'y(0)='+str(p['h']), '-2 & =(0+C)':str(p['h'])+' & =(0+C)',
                 'C & =-2':'C & ='+tex(m['c']),r'y=({x}^{2}-2){e}^{-x}.':'y='+tex(m['y'])+'.'}
    elif qid=='q-335829':
        mapping={'y(0)=-1':'y(0)='+str(p['h']), '-1 & =2+C(1)':str(p['h'])+' & =2+C(1)',
                 'C & =-3':'C & ='+tex(m['c']),r'y=2-3{e}^{-4x}.':'y='+tex(m['y'])+'.'}
    elif qid=='q-339145':
        mapping={'y(0)=5':'y(0)='+str(p['h']), '5 & =6+C':str(p['h'])+' & =6+C',
                 'C & =-1':'C & ='+tex(m['c']),r'y=6-{e}^{-{x}^{2}/12}.':'y='+tex(m['y'])+'.'}
    elif qid=='q-335808':
        mapping={'y(0)=1':'y(0)='+str(p['h']), '1 & =2+C':str(p['h'])+' & =2+C',
                 'C & =-1':'C & ='+tex(m['c']),r'y=2-{e}^{-{x}^{2}/4}.':'y='+tex(m['y'])+'.'}
    elif qid=='q-335830':
        mapping={'y(0)=4':'y(0)='+str(p['h']), '4 & =C-1':str(p['h'])+' & =C-1',
                 'C & =5':'C & ='+tex(m['c']),r'y={e}^{2x}(5-\operatorname{cos}⁡x).':'y='+tex(m['y'])+'.'}
    # Mask all exact complete components first; never mutate inserted components.
    masks={}
    for i,(a,b) in enumerate(sorted(mapping.items(),key=lambda it:-len(it[0]))):
        token='@@COMPONENT'+str(i)+'@@'; solution=solution.replace(a,token); masks[token]=b
    for a,b in masks.items(): solution=solution.replace(a,b)
    return prompt, solution

def aligned(rows): return '$$\n'+r'\begin{aligned}'+' \\\\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}'+'\n$$'

def authored_solution(f,p,m):
    P,Q,I,F,t,h,c,y=(m[k] for k in ('P','Q','I','F','t','h','c','y'))
    it,pt,qt,ft=map(tex,(I,P,Q,F)); derivative=r'\frac{\text{d}y}{\text{d}x}'
    out=''
    if f=='nonstandard':
        out='The first step is to write the equation in standard form,\n\n'+aligned([
            ('x'+derivative+'+2y',tex(4*p['b']*x**2)),
            (r'\frac{1}{x}\left(x'+derivative+'+2y\\right)',r'\frac{1}{x}\cdot '+tex(4*p['b']*x**2)),
            (derivative+'+'+pt+'y',qt)])+'\n\n'
    out+='This equation is in the standard form\n\n$$\n'+derivative+'+P(x)y=Q(x),\n$$\n\nwith $P(x)='+pt+'$ and $Q(x)='+qt+'.$\n\nWe compute an integrating factor using the definition:\n\n'
    integ=sp.integrate(P,x)
    rows=[('I(x)',r'e^{\int P(x)\,\text{d}x}'),('',r'e^{\int '+pt+r'\,\text{d}x}'),('',tex(sp.exp(integ)))]
    if f in ('nonstandard','cosine','sine'): rows.insert(2,('',r'e^{'+tex(integ)+'}'))
    out+=aligned(rows)+'\n\nMultiplying both sides of the equation in standard form by $I(x)='+it+'$ yields\n\n'
    prod=sp.simplify(I*Q)
    out+=aligned([(it+r'\cdot ('+derivative+'+'+pt+'y)',it+r'\cdot '+qt),
                  (it+derivative+'+'+tex(I*P)+'y',tex(prod)),
                  (r'\frac{\text{d}}{\text{d}x}(y'+it+')',tex(prod)+'.')])
    out+='\n\nNow, we integrate with respect to $x'
    if f in ('quadratic','cubic'): out+=',$ making use of the substitution $u='+tex(sp.log(I))
    out+=':$\n\n'
    rows=[(r'\int \frac{\text{d}}{\text{d}x}(y'+it+r')\,\text{d}x',r'\int '+tex(prod)+r'\,\text{d}x')]
    if f in ('quadratic','cubic'):
        rows.extend([('y'+it,r'\int '+tex(p['b'])+r'e^u\,\text{d}u'),('y'+it,tex(p['b'])+'e^u+C')])
    elif f=='constant':
        # Deliberately retain coefficient times primitive before collection.
        rows.append(('y'+it,tex(Q)+r'\left('+tex(1/P)+' '+it+r'\right)+C'))
    rows.extend([('y'+it,ft+'+C'),('y',tex(m['g']))]); out+=aligned(rows)
    out+='\n\nThis is the general solution. To find the value of $C$ corresponding to the specific solution, we apply the initial condition $y('+tex(t)+')='+tex(h)+'$ as follows:\n\n'
    # Explicit substitution before evaluating the arithmetic (no eager CAS).
    Ft='('+ft.replace('x','('+tex(t)+')')+')'; It='('+it.replace('x','('+tex(t)+')')+')'
    out+=aligned([('y('+tex(t)+')',r'\frac{'+Ft+'+C}{'+It+'}'),
                  (tex(h),r'\frac{'+tex(F.subs(x,t))+'+C}{'+tex(I.subs(x,t))+'}'),('C',tex(c))])
    out+='\n\nTherefore, the solution to the initial value problem is\n\n$$\ny='+tex(y)+'.\n$$'
    return out

def observed_banks(qid,p,m):
    h,c=m['h'],m['c']; e=sp.exp
    if qid=='q-334916': return [x,e(x),x**3,1/x],[1+c*e(x),1+c*e(-x),h*e(x),e(-x)+c,h*e(-x)]
    if qid=='q-335808': return [1/x,e(4*x),e(x*x/4),x**3],[e(2*x*x),2*x+h,2*x*x+h,2+c*e(-x*x/4),2+c*e(x*x)]
    if qid=='q-335810': return [2*x,e(2*x),e(x),x*x],[(h+1)*x*x-c/x**2,x*x+c/x**2,x+c/x**2,(h+1)*x-c/x**2]
    if qid=='q-335811':
        s=p['k']*sp.sin(x); return [e(x*x),e(2*x),x*x,2*x],[x*x*s,s/x,s/x**2,s/x**2,x*s]
    if qid=='q-335812': return [1/x,e(x),x,sp.log(x)],[(2*c+3*sp.cos(x))/(2*x),(2*c+4*sp.cos(x))/(2*x),(2*c-sp.cos(x))/(2*x),m['y'],m['y']]
    if qid=='q-335806': return [e(x),x,e(-x),x*x],[(x+h)*e(x),(x*x+h)*e(x),h*e(-x),(x+h)*e(-x),m['y']]
    if qid=='q-335829': return [e(2*x),4*x,e(4*x),e(8*x)],[m['y'],1+(h-1)*e(-4*x),4+(h-4)*e(4*x),h*e(4*x),h*e(-4*x)]
    if qid=='q-339145': return [e(12*x),1/x,x**6,e(x*x/12)],[6+c*e(x*x),6*x+h,e(6*x*x),6*x*x+h,m['y']]
    if qid=='q-335830': return [e(-2*x),-2*x,e(2*x),2*x],[e(-2*x)*(1+3*sp.cos(x)),2*e(-2*x)*(1+sp.cos(x)),m['y'],e(2*x)*(h-1+sp.cos(x)),h*e(2*x)*sp.cos(x)]
    raise ValueError(qid)

def authored_banks(f,p,m):
    I,F,c,y=m['I'],m['F'],m['c'],m['y']; P=m['P']
    # Entire banks chosen up front; all members must survive equivalence guards.
    if f in ('nonstandard','cosine','sine'): ib=[I,1/I,sp.exp(x),sp.log(x) if f=='sine' else P]
    else: ib=[I,1/I,sp.log(I),I**2]
    # Wrong sign of division, initial constant, omitted particular part,
    # omitted IF division, and dividing only the particular term.
    yb=[y,-y,F*I,F/x,F*x] if f=='cosine' and c==0 else [y,(F-c)/I,c/I,F+c,F/I+c]
    return ib,yb

def unique_bank(bank, factor=False):
    for i,a in enumerate(bank):
        if not a.is_finite and a.has(sp.zoo,sp.nan): return False
        for b in bank[:i]:
            if eq(a,b): return False
            if factor:
                ratio=sp.simplify(a/b)
                if not ratio.has(x) and ratio!=0: return False
    return True

def sample(f,level,r):
    h=r.randint(-6,6)
    if f=='constant': return {'a':1 if level=='easy' else r.randint(2,6),'b':r.randint(1,6),'h':h}
    if f in ('quadratic','cubic'): return {'d':r.randint(2,6) if f=='quadratic' else r.randint(1,4),'b':r.randint(1,6),'h':h}
    if f in ('cancellation','nonstandard'): return ({'a':r.randint(1,6),'b':r.randint(1,6),'h':h} if f=='cancellation' else {'b':r.randint(1,6),'h':h})
    return {'k':r.randint(1,6),'h':h}

def render_prompt(f,p,m):
    if f=='nonstandard': ode='x'+r'\frac{\text{d}y}{\text{d}x}+2y='+tex(4*p['b']*x**2)
    else: ode=r'\frac{\text{d}y}{\text{d}x}+\left('+tex(m['P'])+r'\right)y='+tex(m['Q'])
    if f in ('nonstandard','cosine','sine'): ode+=r',\quad x>0'
    return 'Consider the following initial value problem.\n\n$$\n'+ode+r',\quad y('+tex(m['t'])+')='+tex(m['h'])+'\n$$\n\nSelect the correct options below.\n\nAn integrating factor for this equation is $I(x)=$ {{field-1}}.\n\nThe solution to the initial value problem is $y(x)=$ {{field-2}}.'

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
    if field_type not in (None,'select',':answer-field.type/select'): raise ValueError('Only source select layout supported')
    r=random.Random(seed); template=template or r.choice([t for t,v in AUTH.items() if v[0]==level])
    if template not in TEMPLATES or TEMPLATES[template][0]!=level: raise ValueError('Template difficulty mismatch')
    profile=profile or 'authored'; f=TEMPLATES[template][1]
    for attempt in range(300):
        if parameters is not None: p=dict(parameters)
        elif template in OBS:
            p=dict(OBS[template][2]); p['h']=r.randint(-8,8)
            if f=='cosine': p['h']=0; p['k']=r.randint(1,5)
        else: p=sample(f,level,r)
        check_parameters(level,template,p,profile); m=model(f,p)
        ib,yb=observed_banks(template,p,m) if profile=='observed' else authored_banks(f,p,m)
        ambiguous=template in ('q-335811','q-335812','q-335830') and profile=='observed'
        # q-335830's wrong linear IF options differ only by a constant factor.
        # Preserve that redundant source bank for replay evidence only.
        valid=(unique_bank(ib,True) or template=='q-335830' and profile=='observed') and (unique_bank(yb) or ambiguous)
        if profile=='authored' and (m['c']==0 or m['h']==0) and not (template=='q-335811'): valid=False
        if valid: break
        if parameters is not None: raise ValueError('Whole bank rejected: equivalent or ambiguous options')
    else: raise ValueError('No eligible complete bank')
    if template in OBS: prompt,solution=source_masks(template,p,m)
    else: prompt,solution=render_prompt(f,p,m),authored_solution(f,p,m)
    # Display choices computed from mathematical recipes; normalize legacy double
    # TeX escapes / invisible function application rather than propagating them.
    banks=[[tex(e) for e in ib],[tex(e) for e in yb]]
    task=json.dumps([sp.srepr(m[k]) for k in ('P','Q','t','h')],sort_keys=True)
    fingerprint=hashlib.sha256(task.encode()).hexdigest()
    content=json.dumps({'version':VERSION,'problem':prompt,'solution':solution,'banks':[sorted(b) for b in banks]},sort_keys=True)
    contenthash=hashlib.sha256(content.encode()).hexdigest(); qid=str(uuid.uuid5(uuid.NAMESPACE_URL,contenthash))
    fields=[]
    corrects=[m['I'],m['y']]
    for fi,(bank,expressions,right) in enumerate(zip(banks,[ib,yb],corrects)):
        key='field-'+str(fi+1); fid=str(uuid.uuid5(uuid.UUID(qid),key)); answers=[]; correct=None
        # Occurrence index makes legacy equivalent duplicate records owned/unique.
        for i,(value,expr) in enumerate(zip(bank,expressions)):
            occurrence=bank[:i].count(value); aid=str(uuid.uuid5(uuid.UUID(fid),value+'#'+str(occurrence)))
            answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
            if correct is None and eq(expr,right): correct=aid
        if correct is None: raise ValueError('Correct value missing from complete bank')
        r.shuffle(answers)
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/select',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
    return {'knowledge_point':{'db_id':KP,'id':SOURCE['record'][':knowledge-point/id'],'title':TITLE},
            'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},
            'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'domain':'x>0' if f in ('nonstandard','cosine','sine') else 'real x','source':{k:CURRENT[k] for k in ('database','basis','lineage')},'source_refs':[template] if template in OBS else [],'authored_difficulty':template not in OBS or template=='q-334916','source_ambiguous_bank':ambiguous,'content_sha256':contenthash,'mathematical_fingerprint':fingerprint,'sympy_version':sp.__version__}}

def generate_easy(seed=0,**kw): return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw): return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw): return generate('hard',seed,**kw)
def markdown(record):
    q=record['question']; out=q[':question/problem']+'\n\n'
    for f in q[':question/answer-fields']:
        out+=f[':answer-field/key']+':\n'+''.join('- $'+a[':answer/value']+'$\n' for a in f[':answer-field/choices'])+'\n'
    return out+q[':question/worked-solution']
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    rows=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    print(json.dumps(rows,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(q) for q in rows))
