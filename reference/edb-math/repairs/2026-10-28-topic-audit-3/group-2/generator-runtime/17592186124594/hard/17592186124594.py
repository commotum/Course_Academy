#!/usr/bin/env python3
"""Plane-polar derivatives, steps 3–7 only; math snapshot basis 1356.

Seven observed families, eight captured complete banks (one duplicate legacy
field). Every observed family is a linear coefficient template: a multiplies
the entire Cartesian function AND every term of the captured bank. This is a
transparent expression-pattern extension, not a claim to recover distractor
intent. Original a=1 is rendered by the same calculations. All observed choices
are retained. Correctness, original references, and source presentation repairs
are reported separately. No plots are present in these practice questions.

Moderate/hard are explicitly authored equal-level peer families. They apply
the same two-term Cartesian→polar chain rule, with bounded polynomial/log
workload. They never differentiate a polar-given function with respect to x/y.
The API rejects an entire ambiguous bank. Explicit invalid inputs never resample.
Question UUID hashes actual display, fixed solution and unordered complete bank;
mathematical fingerprints exclude banks, source profiles, names and seeds.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID = 17592186124594
KP_UUID = 'c2696e2e-7aa9-5831-9028-9adfe5889bbe'
TITLE = 'Calculating the Derivative of a Cartesian Function With Respect to Plane Polar Coordinates'
VERSION = 'plane-polar-derivatives-1'
ROOT = Path(__file__).with_suffix('')
CAPTURE = json.loads((ROOT/'source.json').read_text())
RAW = {q[':question/math-academy-id']: q for q in CAPTURE['record'][':knowledge-point/questions']}
X,Y = sp.symbols('x y', real=True)
R = sp.Symbol('r', positive=True)
T = sp.Symbol('theta', real=True)
C,S = sp.cos(T),sp.sin(T)
SOURCE_IDS = {'cross_theta':'q-37192','log_linear_r':'q-37196','cubic_r':'q-94999',
              'log_radial_r':'q-95109','x_square_r':'q-95112','y_square_theta':'q-95113',
              'radial_theta':'q-95116'}
TEMPLATES = {**{k:'easy' for k in SOURCE_IDS}, 'quadratic_r':'moderate',
             'quadratic_theta':'moderate','cubic_sum_theta':'hard','log_quadratic_theta':'hard'}
BASE = {'cross_theta':2*X*Y+Y**2,'log_linear_r':sp.log(X+Y),
        'cubic_r':X**2*Y,'log_radial_r':sp.log(X**2+Y**2),
        'x_square_r':X**2,'y_square_theta':Y**2,'radial_theta':(X**2+Y**2)/2}

def normalize(s):
    """Only notation: visible TeX trig commands replace imported application glyphs."""
    s=s.replace('\u2061','').replace('θ',r'\theta').replace('−','-')
    s=re.sub(r'\\operatorname\{(sin|cos|ln)\}',lambda m:'\\'+m[1],s)
    s=re.sub(r'\{(sin|cos)\}',lambda m:'\\'+m[1],s)
    return s

def tex(e):
    return sp.latex(e,order='lex',ln_notation=True).replace(r'\log',r'\ln')

def coeff(a):
    return '' if a==1 else tex(a)

def term(a,s):
    if a==0:return '0'
    return coeff(a)+s

def digest(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(v)))

def equivalent(a,b):
    # Exact rational trigonometric equivalence without costly phase-shift CAS
    # searches. All supported arguments are theta or 2 theta.
    u,v=sp.symbols('_sin _cos')
    difference=(sp.expand_trig(a)-sp.expand_trig(b)).subs({S:u,C:v})
    numerator=sp.fraction(sp.cancel(difference))[0]
    return sp.reduced(numerator,[u**2+v**2-1],u,v)[1]==0

def parse_math(s):
    """Small independent parser for the actual printed arithmetic/trig subset.

    Supports implicit products (including xy), nested fractions/powers, and
    trig/log expressions. It reads display strings, never generation metadata.
    Rejects unsupported commands rather than silently losing tokens.
    """
    s=normalize(s)
    s=re.sub(r'\\(?:left|right|,|!|;|quad)', '',s)
    s=s.replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
    toks=re.findall(r'\\[A-Za-z]+|\d+|[a-zA-Z]|[^\s]',s)
    i=0
    variables={'x':X,'y':Y,'r':R,'\\theta':T}
    def atom():
        nonlocal i
        if i>=len(toks):raise ValueError('incomplete '+s)
        tok=toks[i];i+=1
        if tok in ('{','('):
            v=expr(); close='}' if tok=='{' else ')'
            if i>=len(toks) or toks[i]!=close:raise ValueError('unbalanced '+s)
            i+=1
        elif tok==r'\frac':v=atom()/atom()
        elif tok in (r'\sin',r'\cos',r'\ln'):
            power=sp.Integer(1)
            if i<len(toks) and toks[i]=='^':i+=1;power=atom()
            # TeX's unparenthesized 2 theta argument is one implicit product.
            numeric_argument=i<len(toks) and toks[i].isdigit()
            arg=atom()
            while numeric_argument and i<len(toks) and toks[i] in ('r','x','y',r'\theta'):
                arg*=atom()
            v={r'\sin':sp.sin,r'\cos':sp.cos,r'\ln':sp.log}[tok](arg)**power
        elif tok in variables:v=variables[tok]
        elif tok.isdigit():v=sp.Integer(tok)
        elif tok in ('+','-'):v=atom()*(1 if tok=='+' else -1)
        else:raise ValueError('unsupported token '+tok+' in '+s)
        if i<len(toks) and toks[i]=='^':i+=1;v=v**atom()
        return v
    def product():
        nonlocal i
        v=atom()
        while i<len(toks) and toks[i] not in ('+','-','}',')'):
            if toks[i] in ('*','/'):
                op=toks[i];i+=1;w=atom();v=v*w if op=='*' else v/w
            else:v*=atom()
        return v
    def expr():
        nonlocal i
        v=product()
        while i<len(toks) and toks[i] in ('+','-'):
            op=toks[i];i+=1;w=product();v=v+w if op=='+' else v-w
        return v
    result=expr()
    if i!=len(toks):raise ValueError('unconsumed math '+s)
    return result

def _name_replace(s,old,new):
    # Function labels only. Never touch Cartesian variables, commands or tuples.
    s=s.replace('∂'+old,'∂'+new)
    s=re.sub(r'(?<![A-Za-z])'+old+r'(?=\(x\s*,\s*y\))',new,s)
    return s.replace('$'+old+'$','$'+new+'$')

def source_prose(family,name):
    q=RAW[SOURCE_IDS[family]]
    if ':question/worked-solution' not in q:
        # No recovered solution exists: explicitly authored, using the common
        # four-paragraph method of the owning KP, not called original fidelity.
        q=RAW['q-95109']
    text=normalize(q[':question/worked-solution'])
    old=re.search(r'function \$([a-z])\(',text)[1]
    # Minimal teaching-label corrections, raw evidence remains source.json.
    if family=='cubic_r':text=text.replace('∂g','∂h')
    if family in ('y_square_theta','radial_theta'):
        start=text.index('Writing the above'); end=text.index('Finally,',start)
        piece=text[start:end].replace('∂'+old+'}{∂y','∂'+old+'}{∂x',1)
        text=text[:start]+piece+text[end:]
    return _name_replace(text,old,name)

def aligned(rows):return '\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'

def derivative(name,v):return r'\frac{∂'+name+'}{∂'+('\\theta' if v=='theta' else v)+'}'

def calculation(f,variable):
    fx,fy=sp.diff(f,X),sp.diff(f,Y)
    px,py=[e.subs({X:R*C,Y:R*S},simultaneous=True) for e in (fx,fy)]
    ux,uy=(-R*S,R*C) if variable=='theta' else (C,S)
    # Keep course sin/cos arguments; generic trigsimp may invent phase-shift
    # radicals (sqrt(2) sin(theta+pi/4)), changing the advertised workload.
    answer=sp.cancel(sp.expand(px*ux+py*uy))
    return fx,fy,px,py,ux,uy,answer

def easy_components(family,a):
    """Explicit unevaluated source-stage masks: no CAS collapse of teaching rows."""
    c=lambda n:coeff(a*n)
    rr=r'{r}^{2}'; rrr=r'{r}^{3}'; co=r'\cos\theta '; si=r'\sin\theta '
    co2=r'\cos^{2}\theta ';si2=r'\sin^{2}\theta '
    sn2=r'\sin(2\theta)';cs2=r'\cos(2\theta)'
    if family=='cross_theta':
        formula=c(2)+'xy+'+c(1)+r'{y}^{2}'
        fx=c(2)+'y';fy=c(2)+'x+'+c(2)+'y'
        px=c(2)+'r'+si;py=c(2)+'r'+co+'+'+c(2)+'r'+si
        rows=['-'+px+r'\,r'+si+'+('+py+')r'+co,
              c(2)+rr+'('+co2+'-'+si2+')+'+c(1)+rr+sn2,
              c(2)+rr+cs2+'+'+c(1)+rr+sn2]
    elif family=='cubic_r':
        formula=c(1)+r'{x}^{2}y';fx=c(2)+'xy';fy=c(1)+r'{x}^{2}'
        px=c(2)+rr+co+si;py=c(1)+rr+co2
        rows=['('+px+')'+co+'+('+py+')'+si,
              c(2)+rr+co2+si+'+'+c(1)+rr+co2+si,c(3)+rr+co2+si]
    elif family=='log_radial_r':
        formula=c(1)+r'\ln({x}^{2}+{y}^{2})'
        den=r'{x}^{2}+{y}^{2}';pden=rr+co2+'+'+rr+si2
        fx=r'\frac{'+c(2)+'x}{'+den+'}';fy=r'\frac{'+c(2)+'y}{'+den+'}'
        px=r'\frac{'+c(2)+'r'+co+'}{'+pden+'}';py=r'\frac{'+c(2)+'r'+si+'}{'+pden+'}'
        rows=['('+px+')'+co+'+('+py+')'+si,
              r'\frac{'+c(2)+'r('+co2+'+'+si2+')}{'+rr+'('+co2+'+'+si2+')}',r'\frac{'+tex(2*a)+'}{r}']
    elif family=='log_linear_r':
        formula=c(1)+r'\ln(x+y)';fx=fy=r'\frac{'+tex(a)+'}{x+y}'
        px=py=r'\frac{'+tex(a)+'}{r'+co+'+r'+si+'}'
        rows=['('+px+')'+co+'+('+py+')'+si,
              r'\frac{'+c(1)+'('+co+'+'+si+')}{r('+co+'+'+si+')}',r'\frac{'+tex(a)+'}{r}']
    elif family=='x_square_r':
        formula=c(1)+r'{x}^{2}';fx=c(2)+'x';fy='0';px=c(2)+'r'+co;py='0'
        rows=['('+px+')'+co+r'+0\,('+si+')',c(2)+'r'+co2]
    elif family=='y_square_theta':
        formula=c(1)+r'{y}^{2}';fx='0';fy=c(2)+'y';px='0';py=c(2)+'r'+si
        rows=[r'0\,(-r'+si+')+('+py+r')\,r'+co,c(1)+rr+sn2]
    elif family=='radial_theta':
        formula=r'\frac{'+c(1)+r'{x}^{2}}{2}+\frac{'+c(1)+r'{y}^{2}}{2}'
        fx=c(1)+'x';fy=c(1)+'y';px=c(1)+'r'+co;py=c(1)+'r'+si
        rows=['-('+px+r')\,r'+si+'+('+py+r')\,r'+co,
              '-'+c(1)+rr+si+co+'+'+c(1)+rr+si+co,'0']
    else:raise ValueError(family)
    return formula,fx,fy,px,py,rows

def easy_solution(family,a,name):
    _,fx,fy,px,py,rows=easy_components(family,a)
    prototype=source_prose(family,name)
    blocks=re.findall(r'\$\$.*?\$\$',prototype,flags=re.S)
    assert len(blocks)==4
    # First chain-rule block is fixed, except derivative-variable change for
    # the uncaptured log-linear worked solution.
    chain=blocks[0]
    if family=='log_linear_r':chain=chain.replace('∂w','∂'+name)
    replacements=[chain,
      '$$\n'+r'\begin{aligned}'+derivative(name,'x')+'='+fx+r',\,'+derivative(name,'y')+'='+fy+r'\end{aligned}'+'\n$$',
      '$$\n'+r'\begin{aligned}'+derivative(name,'x')+' & ='+px+r', \\ '+derivative(name,'y')+' & ='+py+r'.\end{aligned}'+'\n$$',
      '$$\n'+r'\begin{aligned}'+derivative(name,'theta' if family.endswith('theta') else 'r')+' & ='+r' \\ & ='.join(rows)+r'\end{aligned}'+'\n$$']
    it=iter(replacements)
    return re.sub(r'\$\$.*?\$\$',lambda _:next(it),prototype,flags=re.S)

def easy_bank(family,a,legacy=False):
    """Full observed expression-pattern banks, with exact independent formulas."""
    banks={
      'cross_theta':[2*R**2*sp.cos(2*T)+R**2*sp.sin(2*T),3*R**2*sp.cos(2*T),
          2*R*sp.sin(2*T)+2*R*S**2,2*R*sp.cos(2*T)+R*sp.sin(2*T),R**2*(C+S)],
      'log_linear_r':[1/R,R,(C-S)/(C+S),1/(R*C+R*S),R**2*S],
      'cubic_r':[2*R**3*C*S**2,3*R**2*C,R**2*C**2,3*R**2*C**2*S,2*R**2*S**2],
      'log_radial_r':[2*C**2-1,R/2,2*R,2/R,R**2*C],
      'x_square_r':[2*R*C**2,2*R*S**2,2*R*sp.cos(2*T),R*C**2,R*sp.cos(2*T)],
      'y_square_theta':[R*C**2,R**2*(1-S**2),R*sp.sin(2*T),R**2*S**2,R**2*sp.sin(2*T)],
      'radial_theta':[1-R**2*sp.sin(2*T),R**2*sp.sin(2*T),0,R*S**2,R*C**2]}
    values=[sp.sympify(v)*a for v in banks[family]]
    fields=RAW[SOURCE_IDS[family]][':question/answer-fields']
    field=fields[0] if legacy else fields[-1]
    # Original complete bank is a presentation profile. A nonunit coefficient
    # scales each entire printed source expression, retaining nested structure.
    display=[normalize(x[':answer/value']) for x in field[':answer-field/choices']]
    # Captured q-37192 current bank is ordered in reverse of its legacy bank.
    if family=='cross_theta' and not legacy:values=list(reversed(values))
    if a!=1:display=[tex(a)+r'\left('+s+r'\right)' if v!=0 else '0' for s,v in zip(display,values)]
    return display,values

def authored_easy_bank(family,a):
    """Whole operation banks; explicit observed profiles preserve uncertain intent."""
    f=a*BASE[family];variable='theta' if family.endswith('theta') else 'r'
    fx,fy,px,py,ux,uy,answer=calculation(f,variable)
    if family=='cross_theta':
        values=[answer,-answer,answer/R,px*C+py*S,px*ux]
        recipes=['correct','negate','drop one r factor','differentiate with respect to r','omit y contribution']
    elif family=='log_linear_r':
        values=[answer,-answer,a/(R*(C+S)),a*(C-S)/(C+S),a*R]
        recipes=['correct','negate','omit coordinate derivatives','differentiate with respect to theta','invert radial derivative']
    elif family=='cubic_r':
        values=[answer,-answer,answer/R,py*uy,R*answer]
        recipes=['correct','negate','drop one r factor','omit x contribution','add one r factor']
    elif family=='log_radial_r':
        values=[answer,-answer,2*a*R,a/(2*R),sp.Integer(0)]
        recipes=['correct','negate','invert radial power','reciprocal quadratic factor','differentiate with respect to theta']
    elif family=='x_square_r':
        values=[answer,2*a*R*S**2,a*R*C**2,-2*a*R**2*C*S,2*a*R*C]
        recipes=['correct','swap coordinate trig factor','omit power-rule factor','differentiate with respect to theta','omit coordinate derivative']
    elif family=='y_square_theta':
        values=[answer,-answer,answer/R,2*a*R*S**2,2*a*R*S]
        recipes=['correct','negate','drop one r factor','differentiate with respect to r','omit coordinate derivative']
    else:
        values=[answer,px*ux,py*uy,-px*ux+py*uy,a*R]
        recipes=['correct','omit y contribution','omit x contribution','lose negative coordinate derivative','differentiate with respect to r']
    return [tex(sp.cancel(v)) for v in values],values,recipes

def _parameters(level,template,p):
    p=dict(p)
    if template in SOURCE_IDS:
        expected={'a','name'}
        p.setdefault('a',1);p.setdefault('name',re.search(r'\$([a-z])\(',RAW[SOURCE_IDS[template]][':question/problem'])[1])
        a=sp.Rational(str(p['a']))
        if a not in {sp.Rational(1,2),1,2,3,4,5,6}:raise ValueError('easy coefficient must be 1/2 or 1..6')
        p['a']=str(a)
    else:
        expected={'a','b','c','name'} if template.startswith(('quadratic','log_quadratic')) else {'a','b','name'}
        p.setdefault('name','f')
        for key in expected-{'name'}:
            if key not in p:raise ValueError('missing '+key)
            if isinstance(p[key],bool) or int(p[key])!=p[key] or not 1<=abs(int(p[key]))<=4:raise ValueError('bounded nonzero integer coefficients required')
            p[key]=int(p[key])
        if 'c' in p and p['a']==p['c']:raise ValueError('unequal square coefficients required')
        if template=='log_quadratic_theta' and not(p['a']>0 and p['c']>0 and 4*p['a']*p['c']>p['b']**2):raise ValueError('positive definite quadratic required')
    if set(p)!=expected:raise ValueError('unused or unknown parameters')
    if p['name'] not in ('f','g','h','w'):raise ValueError('unsupported named function')
    return p

def authored_function(template,p):
    if template=='cubic_sum_theta':return p['a']*X**2*Y+p['b']*X*Y**2
    q=p['a']*X**2+p['b']*X*Y+p['c']*Y**2
    return sp.log(q) if template=='log_quadratic_theta' else q

def authored_solution(f,variable,name):
    fx,fy,px,py,ux,uy,answer=calculation(f,variable)
    d=lambda v:derivative(name,v)
    rule=d('x')+r'\cdot '+derivative('x',variable)+'+'+d('y')+r'\cdot '+derivative('y',variable)
    weighted=('('+d('x')+')('+tex(ux)+')+('+d('y')+')('+tex(uy)+')')
    # These are explicit text components, not an Add that the CAS can collapse.
    substitute='('+tex(px)+')('+tex(ux)+')+('+tex(py)+')('+tex(uy)+')'
    distributed=tex(sp.expand(px*ux))+' + '+tex(sp.expand(py*uy))
    # Parenthesize each displayed summand to avoid a plus followed by minus.
    distributed='('+tex(sp.expand(px*ux))+')+('+tex(sp.expand(py*uy))+')'
    return ('Applying the multivariable chain rule for the function $'+name+'(x,y)$ with two independent variables $r$ and $\\theta,$ where $x=r\\cos\\theta$ and $y=r\\sin\\theta,$ we have'+
      aligned([d(variable)+' & ='+rule,' & ='+weighted])+ '\n\nFirst, we find the partial derivatives of $'+name+'$ with respect to $x$ and $y:$'+
      aligned([d('x')+'='+tex(fx)+r',\,'+d('y')+'='+tex(fy)])+
      '\n\nWriting the above results in terms of $r$ and $\\theta,$ we get'+
      aligned([d('x')+' & ='+tex(px)+',',d('y')+' & ='+tex(py)+'.'])+
      '\n\nFinally, substituting these into our chain rule formula, we get'+
      aligned([d(variable)+' & ='+substitute,' & ='+distributed,' & ='+tex(answer)]))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio layout is supported')
    rng=random.Random(seed)
    options=[k for k,v in TEMPLATES.items() if v==level]
    template=template or rng.choice(options)
    if template not in options:raise ValueError('template is outside difficulty scope')
    eligible=['authored','observed','legacy'] if template=='cross_theta' else (['authored','observed'] if level=='easy' else ['authored'])
    profile=profile or 'authored'
    if profile not in eligible:raise ValueError('profile not eligible')
    for _ in range(200):
        if parameters is None:
            p={'a':rng.choice(['1/2','1','2','3','4','5','6']),'name':rng.choice(['f','g','h','w'])} if level=='easy' else {
              'a':rng.choice([-4,-3,-2,-1,1,2,3,4]),'b':rng.choice([-4,-3,-2,-1,1,2,3,4]),'name':rng.choice(['f','g','h','w'])}
            if level!='easy' and template!='cubic_sum_theta':p['c']=rng.choice([-4,-3,-2,-1,1,2,3,4])
        else:p=parameters
        try:
            p=_parameters(level,template,p);name=p['name']
            variable='theta' if template.endswith('theta') else 'r'
            if level=='easy':
                a=sp.Rational(p['a']);f=a*BASE[template]
                formula=easy_components(template,a)[0]
                raw=normalize(RAW[SOURCE_IDS[template]][':question/problem'])
                old=re.search(r'\$([a-z])\(',raw)[1]
                # Complete formula slot only: never replace x/y throughout text.
                m=re.search(r'\$'+old+r'\(x\s*,\s*y\)\s*=\s*(.*?)\$',raw)
                tail=',' if m[1].rstrip().endswith(',') else ''
                original=m[1].rstrip().removesuffix(',')
                rendered=original if a==1 else formula
                problem=raw[:m.start(1)]+rendered+tail+raw[m.end(1):]
                problem=_name_replace(problem,old,name)
                solution=easy_solution(template,a,name)
                if profile=='authored':display,values,recipes=authored_easy_bank(template,a)
                else:
                    display,values=easy_bank(template,a,profile=='legacy')
                    recipes=['a times complete observed expression pattern']*5
            else:
                f=authored_function(template,p)
                problem='Given that $'+name+'(x,y)='+tex(f)+',$ find $'+derivative(name,variable)+',$ where $(x,y)$ are Cartesian coordinates and $(r,\\theta)$ are the corresponding plane polar coordinates.'
                solution=authored_solution(f,variable,name)
                fx,fy,px,py,ux,uy,answer=calculation(f,variable)
                values=[answer,-answer,answer/R,sp.expand(px*ux),sp.expand(py*uy)]
                display=[tex(v) for v in values]
                recipes=['correct','negate','drop one r factor','omit y contribution','omit x contribution']
            fx,fy,px,py,ux,uy,answer=calculation(f,variable)
            correct=[i for i,v in enumerate(values) if equivalent(v,answer)]
            if len(correct)!=1:raise ValueError('bank has missing or multiple correct options')
            for i,v in enumerate(values):
                if not equivalent(parse_math(display[i]),v):raise ValueError('printed option is not recipe value')
                if any(equivalent(v,w) for w in values[:i]):raise ValueError('ambiguous complete bank')
            break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('no valid whole-bank instance in 200 trials')
    bank=sorted(display)
    # Only meaningful mathematical f and derivative target enter this key.
    # Additive constants, including a common positive scale inside ln, do not
    # alter either assessed Cartesian partial. Canonicalize that redundancy.
    math_key=digest([sp.srepr(sp.cancel(fx)),sp.srepr(sp.cancel(fy)),variable])
    content_key=digest([VERSION,problem,solution,bank,'radio','selection'])
    qid=uid([content_key,'question']);fid=uid([content_key,'field','selection'])
    answers=[{':answer/id':uid([fid,s]),':answer/type':':answer.type/math',':answer/value':s} for s in display]
    correct_id=answers[correct[0]][':answer/id'];rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
           ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
    domain='r>0; theta real'
    if template=='log_linear_r':domain+='; r(cos(theta)+sin(theta))>0'
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,
              ':question/worked-solution':solution,':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
      'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,
       'mathematical_fingerprint':math_key,'content_fingerprint':content_key,'domain':domain,
       'source':{'database':CAPTURE['database'],'basis':CAPTURE['basis'],'lineage':CAPTURE['lineage']},
       'source_ids':[SOURCE_IDS[template]] if level=='easy' else [],
       'authored_difficulty':level!='easy' or template=='log_linear_r','plot_rating':'none',
       'bank_interpretation':'linear scaling of complete observed expression patterns; intent unresolved' if profile in ('observed','legacy') else 'authored operation bank',
       'recipes':recipes,
       'sympy_version':sp.__version__}}

# Easy: observed polynomial/log families with their original fixed stage counts.
def generate_easy(seed=0,**kw):
    """Apply the two-term chain rule to an observed simple Cartesian function.

    Original monomial, cross-term, radial/log cancellation families are peers;
    each keeps its captured two/three final rows and positive bounded scale.
    The unrated log-linear family has an explicitly authored easy assignment.
    """
    return generate('easy',seed,**kw)

# Moderate: both quadratic Cartesian partials contain two nonzero terms.
def generate_moderate(seed=0,**kw):
    """Author quadratic r/theta peers with four nonzero product contributions.

    Nonzero a,b,c and unequal square coefficients preserve the extra collection
    demand. Signed integer magnitudes stay 1..4; the method remains unchanged.
    """
    return generate('moderate',seed,**kw)

# Hard: four cubic angular products or a nonconstant angular log denominator.
def generate_hard(seed=0,**kw):
    """Author theta-derivative cubic-sum/log-quadratic peers in the same KP.

    Both use two two-term Cartesian partials; cubic powers or a common quotient
    increase simplification workload. Bounds and positive definiteness prevent
    degeneration into a source easy radial cancellation or a domain branch.
    """
    return generate('hard',seed,**kw)

def markdown(record):
    q=record['question'];out=q[':question/problem']+'\n\n'
    f=q[':question/answer-fields'][0]
    for i,a in enumerate(f[':answer-field/choices']):out+=chr(65+i)+'. $'+a[':answer/value']+'$\n\n'
    return out+'Worked solution:\n\n'+q[':question/worked-solution']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2)
    ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile')
    args=ap.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
