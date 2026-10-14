#!/usr/bin/env python3
"""Basis2275 IVP draft. Registered baseline is immutable; no database operations.
Public profile raw/observed preserves exact captured bytes and omissions, evidence
only. Normal profiles preserve family-specific source stages and shared prose,
normalize all math before identities, and use method-derived complete banks.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import normalize_prose,normalize_tex,checked_math_content
KP=17592186087879
TITLE='Solving First-Order Initial Value Problems Using Integrating Factors'
VERSION='ivp-draft-basis2275-v1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
x=sp.Symbol('x',positive=True);C=sp.Symbol('C',real=True)
OBS={
'q-334916':('moderate','constant',{'a':1,'b':1,'h':-3},4,5),
'q-335808':('hard','quadratic',{'d':2,'b':2,'h':1},4,5),
'q-335810':('moderate','nonstandard',{'b':1,'h':2},4,4),
'q-335811':('moderate','cosine',{'k':1,'h':0},4,5),
'q-335812':('moderate','sine',{'k':1,'h':1},4,5),
'q-335806':('moderate','cancellation',{'a':1,'b':1,'h':-2},4,5),
'q-335829':('moderate','constant',{'a':4,'b':2,'h':-1},4,5),
'q-339145':('hard','quadratic',{'d':6,'b':6,'h':5},4,5),
'q-335830':('moderate','trig_cancellation',{'a':-2,'k':1,'h':4},4,5)}
AUTH={'easy_constant':('easy','constant'),'hard_cubic':('hard','cubic')}
TEMPLATES={**{k:v[:2] for k,v in OBS.items()},**AUTH}
REQUIRED={'constant':{'a','b','h'},'quadratic':{'d','b','h'},'cubic':{'d','b','h'},'nonstandard':{'b','h'},'cancellation':{'a','b','h'},'cosine':{'k','h'},'sine':{'k','h'},'trig_cancellation':{'a','k','h'}}
RAW_H={'q-334916':(-8,-1),'q-335808':(0,1),'q-335810':(2,8),'q-335811':(0,0),'q-335812':(1,8),'q-335806':(-8,-1),'q-335829':(-8,-1),'q-339145':(1,5),'q-335830':(4,8)}
ALIASES={'observed':'raw','method':'authored'}
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
        a=sp.sympify(p['a']); P=a; Q=p['k']*sp.exp(-a*x)*sp.sin(x); I=sp.exp(a*x); F=-p['k']*sp.cos(x); t=sp.S(0)
    elif f=='cosine':
        k=sp.sympify(p['k']); P=2/x; Q=k*sp.cos(x)/x**2; I=x**2; F=k*sp.sin(x); t=sp.pi
    elif f=='sine':
        k=sp.sympify(p['k']); P=1/x; Q=k*sp.sin(x)/x; I=x; F=-k*sp.cos(x); t=sp.pi/2
    else: raise ValueError(f)
    const=sp.simplify(h*I.subs(x,t)-F.subs(x,t))
    y=sp.simplify((F+const)/I)
    return dict(P=P,Q=Q,I=I,F=F,t=t,h=h,c=const,y=y,g=(F+C)/I)


def bounds(level,template,p,raw=False):
    f=TEMPLATES[template][1]
    if set(p)!=REQUIRED[f]:raise ValueError('Exact parameter keys required: '+str(sorted(REQUIRED[f])))
    if any(not isinstance(v,int) or isinstance(v,bool) for v in p.values()):raise ValueError('Integer parameters only')
    if raw:
        base=OBS[template][2]
        if any(p[k]!=base[k] for k in p if k not in {'h','k'}):raise ValueError('Raw coefficients keep captured pattern; normal profile has broader slots')
        lo,hi=RAW_H[template]
        if not lo<=p['h']<=hi:raise ValueError('Raw sign-pattern bounds')
        if template=='q-335830' and p['h']%2:raise ValueError('Raw historical half-value coefficient requires even h')
        if 'k' in p and not (1<=p['k']<=6 and (template=='q-335811' or p['k']==1)):raise ValueError('Raw forcing bounds')
        return
    if not -6<=p['h']<=6:raise ValueError('Initial values -6..6')
    if p['h']==0 and f!='cosine':raise ValueError('Nonzero initial-value workload')
    for key in p.keys()-{'h'}:
        if key=='a' and f=='trig_cancellation':
            if not -4<=p[key]<=-1:raise ValueError('Negative exponential coefficient -4..-1')
        elif not 1<=p[key]<=6:raise ValueError('Positive coefficient magnitude 1..6')
    if f=='constant' and level=='easy' and p['a']!=1:raise ValueError('Easy unit integrating exponent')
    if f=='constant' and level=='moderate' and p['a']<2:raise ValueError('Moderate coefficient scaling')
    if f=='quadratic' and p['d']<2:raise ValueError('Hard fractional coefficient')
    if f=='cubic' and p['d']>4:raise ValueError('Cubic coefficient arithmetic ceiling')
    if model(f,p)['c']==0 and f!='cosine':raise ValueError('Constant solution collapses the workload')

def sample(f,level,r):
    h=r.choice([*range(-6,0),*range(1,7)])
    if f=='constant':return {'a':1 if level=='easy' else r.randint(2,6),'b':r.randint(1,6),'h':h}
    if f in ('quadratic','cubic'):return {'d':r.randint(2,6) if f=='quadratic' else r.randint(1,4),'b':r.randint(1,6),'h':h}
    if f=='nonstandard':return {'b':r.randint(1,6),'h':h}
    if f=='cancellation':return {'a':r.randint(1,6),'b':r.randint(1,6),'h':h}
    if f=='trig_cancellation':return {'a':-r.randint(1,4),'k':r.randint(1,6),'h':h}
    return {'k':r.randint(1,6),'h':0 if f=='cosine' and r.randrange(4)==0 else h}

def coeff(v,unit=True):return '' if unit and v==1 else str(v)
def masked(text,mapping):
    pending={}
    for i,(a,b) in enumerate(sorted(mapping.items(),key=lambda t:-len(t[0]))):
        tag='@@SLOT'+str(i)+'@@';text=text.replace(a,tag);pending[tag]=b
    for a,b in pending.items():text=text.replace(a,b)
    return text

def raw_strings(qid,p):
    """Exact captured styles, numerical components bound to initial-value recipes.
    No source+offset perturbation. Historical sign patterns have explicit domains.
    """
    q=QUESTIONS[qid];h=p['h'];f=OBS[qid][1];m=model(f,p);c=int(m['c']) if m['c'].is_Integer else m['c']
    prompt=re.sub(r'(y\([^\n]*?\)\s*=\s*)'+re.escape(str(OBS[qid][2]['h']))+r'(?!\d)',lambda z:z.group(1)+str(h),q[':question/problem'])
    solution=q.get(':question/worked-solution');mapping={}
    if solution is not None:
        if qid=='q-335810':mapping={'y(1)=2':'y(1)='+str(h),'2 & =1+C':str(h)+' & =1+C','C & =1':'C & ='+str(c),r'y={x}^{2}+\frac{1}{{x}^{2}}.':r'y={x}^{2}+\frac{'+str(c)+r'}{{x}^{2}}.'}
        elif qid=='q-335806':mapping={'y(0)=-2':'y(0)='+str(h),'-2 & =(0+C)':str(h)+' & =(0+C)','C & =-2':'C & ='+str(h),r'y=({x}^{2}-2){e}^{-x}.':r'y=({x}^{2}-'+str(-h)+r'){e}^{-x}.'}
        elif qid in ('q-335829','q-335808','q-339145'):
            b=OBS[qid][2]['b'];oldh=OBS[qid][2]['h'];oldc=oldh-b
            exponent={'q-335829':'4x','q-335808':'{x}^{2}/4','q-339145':'{x}^{2}/12'}[qid]
            final=str(b)+'-'+coeff(-c)+r'{e}^{-'+exponent+'}'
            oldfinal=str(b)+'-'+coeff(-oldc)+r'{e}^{-'+exponent+'}'
            mapping={'y(0)='+str(oldh):'y(0)='+str(h),str(oldh)+' & ='+str(b)+'+C':str(h)+' & ='+str(b)+'+C','C & ='+str(oldc):'C & ='+str(c),'y='+oldfinal+'.':'y='+final+'.'}
        elif qid=='q-335812':
            cp=r'\frac{'+coeff(h)+r'\pi }{2}'; pp=coeff(h)+r'\pi '
            mapping={r'y(\frac{\pi }{2})=1':r'y(\frac{\pi }{2})='+str(h),r'1 & =\frac{2C}{\pi }':str(h)+r' & =\frac{2C}{\pi }',r'C & =\frac{\pi }{2}':'C & ='+cp,r'-\operatorname{cos}⁡x+\frac{\pi }{2}':r'-\operatorname{cos}⁡x+'+cp,r'\frac{\pi }{2x}':r'\frac{'+pp+r'}{2x}',r'\frac{\pi -2\operatorname{cos}⁡x}{2x}':r'\frac{'+pp+r'-2\operatorname{cos}⁡x}{2x}'}
        elif qid=='q-335830':mapping={'y(0)=4':'y(0)='+str(h),'4 & =C-1':str(h)+' & =C-1','C & =5':'C & ='+str(h+1),r'y={e}^{2x}(5-\operatorname{cos}⁡x).':r'y={e}^{2x}('+str(h+1)+r'-\operatorname{cos}⁡x).'}
        solution=masked(solution,mapping)
        if qid=='q-335811':
            for name in ('sin','cos'):
                a=r'\operatorname{'+name+'}⁡';solution=solution.replace(a,coeff(p['k'])+a);prompt=prompt.replace(a,coeff(p['k'])+a)
    values={}
    for field in q[':question/answer-fields']:
        vals=[]
        for a in field[':answer-field/choices']:
            v=a[':answer/value'];mp={}
            if field[':answer-field/key']=='field-2':
                if qid=='q-334916':mp={'4':str(1-h),'-3':'-'+str(-h),r'\frac{3}':r'\frac{'+str(-h)+'}'}
                elif qid=='q-335808':mp={'+1':'+'+str(h),'-{e}':'-'+coeff(2-h)+r'{e}'}
                elif qid=='q-335810':mp={'3x':str(h+1)+'x','3{x}':str(h+1)+'{x}',r'\frac{1}':r'\frac{'+str(h-1)+'}'}
                elif qid=='q-335811':mp={r'\operatorname{sin}':coeff(p['k'])+r'\operatorname{sin}'}
                elif qid=='q-335812':mp={r'\pi ':coeff(h)+r'\pi '}
                elif qid=='q-335806':mp={'-2':'-'+str(-h)}
                elif qid=='q-335829':
                    if v.startswith('2-'):mp={'-3':'-'+str(2-h)}
                    elif v.startswith('1-'):mp={'-2':'-'+str(1-h)}
                    elif v.startswith('4-'):mp={'-5':'-'+str(4-h)}
                    else:mp={'-{e}':'-'+coeff(-h)+r'{e}'}
                elif qid=='q-339145':mp={'-{e}':'-'+coeff(6-h)+r'{e}','+5':'+'+str(h)}
                elif qid=='q-335830':
                    if v.startswith('{e}^{-2x}'):mp={'(1+3':'('+str(h-3)+'+'+str(h-1)}
                    elif v.startswith('2{e}'):mp={'2{e}':str(h//2)+'{e}'}
                    elif '(5-' in v:mp={'(5-':'('+str(h+1)+'-'}
                    elif '(3+' in v:mp={'(3+':'('+str(h-1)+'+'}
                    elif v.startswith('4{e}'):mp={'4{e}':str(h)+'{e}'}
            vals.append(masked(v,mp))
        values[field[':answer-field/key']]=vals
    return prompt,solution,values

D=r'\frac{\text{d}y}{\text{d}x}'
DX=r'\frac{\text{d}}{\text{d}x}'
def chain(rows):return r'\begin{aligned}'+r' \\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}'
def addterm(a,term):return a+('+' if not term.startswith('-') else '')+term
def evaluated_at(expr,t):
    # Controlled symbol token substitution; protects command names such as \exp.
    return re.sub(r'(?<![A-Za-z])x(?![A-Za-z])',lambda _: '('+tex(t)+')',expr)

def normal_blocks(qid,p,m):
    f=TEMPLATES[qid][1];P,Q,I,F,t,h,c,y=[m[k] for k in ('P','Q','I','F','t','h','c','y')]
    pt,qt,it,ft=map(tex,(P,Q,I,F));ip=tex(sp.expand(I*P));prod=tex(sp.simplify(I*Q));yg='y'+it
    U=sp.integrate(P,x)
    ifrows=[('I(x)',r'e^{\int P(x)\,\text{d}x}'),('',r'e^{\int ('+pt+r')\,\text{d}x}')]
    if f in ('nonstandard','cosine'):
        ifrows.extend([('',r'e^{2\int (1/x)\,\text{d}x}'),('',r'e^{2\ln x}'),('',r'e^{\ln(x^2)}')])
    elif f=='sine':ifrows.append(('',r'e^{\ln x}'))
    ifrows.append(('',it))
    product=[(it+r'\cdot ('+addterm(D,pt+'y')+')',it+r'\cdot ('+qt+')'),(addterm(it+r'\cdot '+D,ip+r'\cdot y'),prod),(DX+'('+yg+')',prod+'.')]
    integral=[(r'\int '+DX+'('+yg+r')\,\text{d}x',r'\int '+prod+r'\,\text{d}x')]
    if f in ('quadratic','cubic'):integral.extend([(yg,r'\int '+tex(p['b'])+r'e^u\,\text{d}u'),(yg,tex(p['b'])+'e^u+C')])
    elif f=='constant':integral.append((yg,qt+r'\left('+tex(1/P)+r'\cdot '+it+r'\right)+C'))
    integral.extend([(yg,ft+'+C'),('y',tex(m['g']))])
    if f in ('constant','quadratic','cubic'):
        sub=tex(p['b'])+r'+Ce^{-'+evaluated_at(tex(U),t)+'}'; ev=tex(p['b'])+('+C(1)' if qid=='q-335829' else '+C')
    elif f=='nonstandard':sub=tex(p['b'])+'('+tex(t)+r')^2+\frac{C}{('+tex(t)+')^2}';ev=tex(p['b'])+'+C'
    elif f=='cosine':sub=r'\frac{'+tex(p['k'])+r'\sin('+tex(t)+r')+C}{('+tex(t)+r')^2}';ev=r'\frac{C}{'+tex(t**2)+'}'
    elif f=='sine':sub=r'\frac{-'+tex(p['k'])+r'\cos('+tex(t)+r')+C}{('+tex(t)+')}';ev=r'\frac{2C}{\pi}'
    elif f=='cancellation':sub='('+tex(p['b'])+'('+tex(t)+r')^2+C)e^{'+evaluated_at(tex(-P*x),t)+'}';ev=r'(0+C)\cdot 1'
    else:sub=r'e^{'+evaluated_at(tex(-P*x),t)+'}(C-'+tex(p['k'])+r'\cos('+tex(t)+'))';ev='C-'+tex(p['k'])
    initial=[('y('+tex(t)+')',sub),(tex(h),ev),('C',tex(c))]
    final='y='+tex(y)+'.'
    if f=='sine':
        # Keep numerator quotient -> separated terms -> common denominator.
        final=chain([('y',r'\frac{-'+tex(p['k'])+r'\cos x+('+tex(c)+r')}{x}'),('',addterm(tex(c/x),tex(-p['k']*sp.cos(x)/x))),('',r'\frac{'+tex(h*sp.pi)+r'-'+tex(2*p['k'])+r'\cos x}{2x}.')])
    standard=chain([('x'+D+'+2y',tex(4*p.get('b',1)*x**2)),(r'\frac{1}{x}(x'+D+r'+2y)',r'\frac{1}{x}\cdot '+tex(4*p.get('b',1)*x**2)),(D+r'+\frac{2}{x}y',qt+'.')])
    return dict(IF=chain(ifrows),product=chain(product),integral=chain(integral),initial=chain(initial),final=final,standard=standard)

MATH=re.compile(r'\$\$([\s\S]*?)\$\$|(?<!\$)\$(?!\$)([^$]*?)\$')
def normal_solution(qid,p,m):
    if qid not in OBS or qid=='q-334916':
        # Author only when no captured worked chain exists. Same canonical prose.
        base=QUESTIONS['q-335829'] if TEMPLATES[qid][1]=='constant' else QUESTIONS['q-339145']
    else:base=QUESTIONS[qid]
    blocks=normal_blocks(qid,p,m);t=m['t'];h=m['h']
    def render(match):
        s=match.group(1) if match.group(1) is not None else match.group(2);s=s.strip();v=s
        if not s:return match.group(0) # q335810's empty display is an observed omission.
        if r'\begin{aligned}' in s:
            if 'I(x) &' in s:v=blocks['IF']
            elif 'C &' in s:v=blocks['initial']
            elif r'\int' in s:v=blocks['integral']
            elif s.startswith(r'\begin{aligned}y '):v=blocks['final']
            elif 'P(x)=' in s:v=chain([('P(x)',tex(m['P'])+r',\,Q(x)='+tex(m['Q'])+'.')])
            elif 'x'+D+'+2y &' in s:v=blocks['standard']
            else:v=blocks['product']
        elif s.startswith('P(x)'):v='P(x)='+tex(m['P'])
        elif s.startswith('Q(x)'):v='Q(x)='+tex(m['Q'])+('.' if s.endswith('.') else '')
        elif s.startswith('I(x)='):v='I(x)='+tex(m['I'])
        elif s.startswith('y(') and '=' in s:v='y('+tex(t)+')='+tex(h)
        elif s.startswith('u='):v='u='+tex(sp.integrate(m['P'],x))+':'
        elif s.startswith('y='):v=blocks['final']
        return '$$\n'+v+'\n$$' if match.group(1) is not None else '$'+v+'$'
    result=MATH.sub(render,base[':question/worked-solution'])
    # Extra domain declaration is a marked normal-presentation refinement.
    if TEMPLATES[qid][1] in ('nonstandard','cosine','sine'):result='We work on the interval $x>0$ containing the initial point.\n\n'+result
    return normalize_prose(result)

def normal_prompt(qid,p,m):
    f=TEMPLATES[qid][1]
    ode=('x'+D+'+2y='+tex(4*p['b']*x**2) if f=='nonstandard' else addterm(D,tex(m['P'])+'y')+'='+tex(m['Q']))
    if f in ('nonstandard','cosine','sine'):ode+=r',\quad x>0'
    ode+=r',\quad y('+tex(m['t'])+')='+tex(m['h'])
    base=QUESTIONS[qid][':question/problem'] if qid in OBS else QUESTIONS['q-335829'][':question/problem']
    replaced=False
    def render(match):
        nonlocal replaced
        body=match.group(1) if match.group(1) is not None else match.group(2)
        if not replaced and ('dy' in body or D in body):
            replaced=True;return '$$\n'+ode+'\n$$' if match.group(1) is not None else '$'+ode+'$'
        return match.group(0)
    return normalize_prose(MATH.sub(render,base))

def method_banks(qid,p,m):
    f=TEMPLATES[qid][1];I,F,c,y=[m[k] for k in ('I','F','c','y')]
    if f in ('nonstandard','cosine'):ib=[I,1/I,sp.exp(x),m['P']]
    elif f=='sine':ib=[I,1/I,sp.exp(x),sp.log(x)]
    else:ib=[I,1/I,sp.integrate(m['P'],x),I**2]
    if f=='cosine' and c==0:yb=[y,-y,F*I,F/x,F*x];bank='method_zero_constant'
    else:yb=[y,(F-c)/I,c/I,F+c,F/I+c];bank='method_nonzero_constant'
    if qid=='q-335810':yb=yb[:4] # Preserves source four-option field contract.
    return ib,yb,bank

def unique(bank,factor=False):
    for i,a in enumerate(bank):
        if a.has(sp.nan,sp.zoo,sp.oo,-sp.oo):return False
        for b in bank[:i]:
            if eq(a,b):return False
            if factor and not sp.simplify(a/b).has(x):return False
    return True

def identity(question):
    stable=copy.deepcopy(question);stable.pop(':question/id',None)
    for f in stable[':question/answer-fields']:
        f.pop(':answer-field/id',None)
        ref=f.pop(':answer-field/correct',None)
        if ref:
            f['correct_occurrence']=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==ref[1])
        f[':answer-field/choices']=[{k:v for k,v in a.items() if k!=':answer/id'} for a in f[':answer-field/choices']]
        # Canonical sorted bank plus exact designated value; preserve duplicate ordinal.
        if ref:f['correct_value']=f[':answer-field/choices'][f.pop('correct_occurrence')][':answer/value']
        f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda a:a[':answer/value'])
    return hashlib.sha256(json.dumps([VERSION,stable],sort_keys=True).encode()).hexdigest()

def package(level,seed,template,p,profile,prompt,solution,values,correct_indices,bank):
    raw=profile=='raw';source=QUESTIONS.get(template);question={':question/problem':prompt,':question/answer-fields':[]}
    if solution is not None:question[':question/worked-solution']=solution
    if not raw or ':question/difficulty' in source:question[':question/difficulty']=':question.difficulty/'+level
    # Derive provisional owned IDs; final identities reflect actual content only.
    for i,key in enumerate([f[':answer-field/key'] for f in source[':question/answer-fields']] if raw else ('field-1','field-2')):
        answers=[{':answer/id':str(j),':answer/type':':answer.type/math',':answer/value':v} for j,v in enumerate(values[key])]
        field={':answer-field/key':key,':answer-field/type':':answer-field.type/select',':answer-field/choices':answers}
        if correct_indices[key] is not None:field[':answer-field/correct']=[':answer/id',str(correct_indices[key])]
        question[':question/answer-fields'].append(field)
    fingerprint=identity(question);qid=str(uuid.uuid5(uuid.NAMESPACE_URL,fingerprint));question[':question/id']=qid
    r=random.Random(seed)
    for f in question[':question/answer-fields']:
        fid=str(uuid.uuid5(uuid.UUID(qid),f[':answer-field/key']));f[':answer-field/id']=fid;ref=f.get(':answer-field/correct');old=ref[1] if ref else None
        for i,a in enumerate(f[':answer-field/choices']):
            a[':answer/id']=str(uuid.uuid5(uuid.UUID(fid),a[':answer/value']+'#'+str(i)))
            if str(i)==old:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
        r.shuffle(f[':answer-field/choices'])
    m=model(TEMPLATES[template][1],p);task=hashlib.sha256(json.dumps([sp.srepr(m[k]) for k in ('P','Q','t','h')]).encode()).hexdigest()
    return {'knowledge_point':{'db_id':KP,'id':SOURCE['record'][':knowledge-point/id'],'title':TITLE},'question':question,'generation':{'version':VERSION,'template':template,'profile':profile,'bank_profile':bank,'parameters':p,'seed':seed,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'evidence_only':raw,'eligible':not raw,'raw_omissions_preserved':raw,'source_refs':[template] if source else [],'domain':'x>0' if TEMPLATES[template][1] in ('nonstandard','cosine','sine') else 'real x','content_sha256':fingerprint,'mathematical_fingerprint':task,'python_version':sys.version.split()[0],'sympy_version':sp.__version__}}

@checked_math_content
def generate_normal(level,seed,template,p):
    m=model(TEMPLATES[template][1],p);ib,yb,bank=method_banks(template,p,m)
    if not unique(ib,True) or not unique(yb):raise ValueError('Whole complete bank rejected')
    values={key:[normalize_tex(tex(a)) for a in group] for key,group in zip(('field-1','field-2'),(ib,yb))}
    return package(level,seed,template,p,'authored',normal_prompt(template,p,m),normal_solution(template,p,m),values,{'field-1':0,'field-2':0},bank)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if field_type not in (None,'select',':answer-field.type/select'):raise ValueError('Only source select fields')
    profile=ALIASES.get(profile,profile) or 'authored'
    if profile not in ('raw','authored'):raise ValueError('Unknown profile')
    r=random.Random(seed)
    eligible=[t for t,v in TEMPLATES.items() if v[0]==level and (profile!='raw' or t in OBS)]
    if not eligible:raise ValueError('No observed raw source at this difficulty')
    if template is None:template=r.choice(eligible)
    if template not in eligible:raise ValueError('Template difficulty/profile mismatch')
    f=TEMPLATES[template][1]
    if profile=='raw':
        p=dict(parameters) if parameters is not None else dict(OBS[template][2]);bounds(level,template,p,True)
        prompt,solution,values=raw_strings(template,p);indices={}
        for field in QUESTIONS[template][':question/answer-fields']:
            right=field.get(':answer-field/correct');indices[field[':answer-field/key']]=next((i for i,a in enumerate(field[':answer-field/choices']) if right and a[':answer/id']==right[':answer/id']),None)
        return package(level,seed,template,p,profile,prompt,solution,values,indices,'captured_raw')
    for _ in range(200):
        p=dict(parameters) if parameters is not None else sample(f,level,r)
        try:bounds(level,template,p);return generate_normal(level,seed,template,p)
        except ValueError:
            if parameters is not None:raise
    raise ValueError('No eligible whole bank')

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(record):
    q=record['question'];text=q[':question/problem']+'\n\n'
    for f in q[':question/answer-fields']:text+=f[':answer-field/key']+':\n'+''.join('- `'+a[':answer/value']+'`\n' for a in f[':answer-field/choices'])+'\n'
    return text+q.get(':question/worked-solution','[No captured worked solution.]')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');n=a.parse_args();rows=[generate(l,n.seed+i,template=n.template,profile=n.profile) for l in (['easy','moderate','hard'] if n.difficulty=='all' else [n.difficulty]) for i in range(n.count)];print(json.dumps(rows,indent=2,ensure_ascii=False) if n.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
