#!/usr/bin/env python3
"""Scalar line integrals using substitution, math basis 1356.

Observed profiles raw:q-N are public, evidence-only homogeneous-integrand
extensions of each COMPLETE historical bank. Their error intent is opaque.
They preserve absent ratings/solutions/correct refs. Normal method banks retain
source-family stages, correct source notation defects, and add endpoint detail.
No DB or plot calls: all six practice sources are unillustrated.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as S

KP_ID=17592186133827
ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
KP=CAPTURE['record']; VERSION='scalar-substitution-2'
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
t=S.Symbol('t', positive=True); u=S.Symbol('u', positive=True)
x,y,z=S.symbols('x y z',real=True)
LEVELS={'parabola_easy':'easy','ratio':'moderate','cubic':'moderate','cos_diagonal':'moderate','sine_line':'moderate','sin_cos':'moderate','space_ratio':'hard'}
SOURCE_TEMPLATE={'q-76186':'ratio','q-167612':'cubic','q-76479':'cos_diagonal','q-76484':'sine_line','q-76187':'sin_cos','q-76496':'space_ratio'}
ANCHORS={'ratio':{'a':1,'h':1,'k':12,'ma':3,'mb':5},'cubic':{'s':1,'b':1,'n':1},'cos_diagonal':{'a':1,'b':-1,'k':1,'angle':2},'sine_line':{'p':4,'q':-3,'d':5,'angle':2},'sin_cos':{'s':1,'z':1,'k':4},'space_ratio':{'a':1,'b':1,'c':1,'k':1,'lo':1,'hi':2},'parabola_easy':{'k':1,'m':3}}
SOURCE_VALUES={
'q-76186':[S.Integer(56),-S.Integer(64),S.Integer(75),-S.Integer(16),S.Integer(98)],
'q-167612':[28*S.sqrt(2),14*(2*S.sqrt(2)-1),7*(2*S.sqrt(2)+1),7*(S.sqrt(2)-1),12*S.sqrt(2)-5],
'q-76479':[S.Integer(2),S.sqrt(2)-1,2-S.sqrt(2),2*S.sqrt(2),S.sqrt(2)],
'q-76484':[S.Rational(5,3),S.Rational(2,5),S.Rational(25,3),S.Rational(5,2),S.Rational(20,3)],
'q-76496':[(S.sqrt(5)+S.sqrt(3))/3,(S.sqrt(5)+3)/2,5*S.sqrt(5)-3*S.sqrt(3),S.sqrt(5)+S.sqrt(3),(5*S.sqrt(5)-3*S.sqrt(3))/6],
'q-76187':[S.Rational(3,2)*(S.sqrt(2)-1),3*S.sqrt(2)/4,(2*S.sqrt(2)+1)/2,3*S.sqrt(2)/2,S.Rational(4,3)*(2*S.sqrt(2)-1)]}

def tex(e): return S.latex(S.sympify(e),fold_short_frac=False).replace('\\log','\\ln')
def block(rows): return '$$\n\\begin{aligned}'+r' \\ '.join(rows)+ '\\end{aligned}\n$$'
def eq(e): return r' & ='+e

def scaled(mask,k):
    """Opaque homogeneous recipe: complete component times a scalar, not fit values."""
    return mask if k==1 else tex(k)+r'\left('+mask+r'\right)'

def raw_prompt(source,k):
    original=SOURCES[source][':question/problem']
    # Exact complete integrand slots, no replacement of individual letters.
    component={'q-76186':r'\frac{12x}{y-1}','q-167612':r'{x}^{3}+y','q-76479':r'\operatorname{cos}⁡x','q-76484':r'\frac{{x}^{2}+{y}^{2}}{5}', 'q-76496':r'\frac{y+z}{x}','q-76187':r'4yz\cos x'}[source]
    assert original.count(component)==1
    return original.replace(component,scaled(component,k))

def raw_solution(source,k):
    original=SOURCES[source].get(':question/worked-solution')
    if original is None:return None
    # Tokenize at complete display components, preserving original rows/prose.
    parts=original.split('$$')
    assert len(parts)==11
    fcomponent={'q-76186':r'\frac{12x}{y-1}','q-167612':r'{x}^{3}+y','q-76479':r'\operatorname{cos}⁡x','q-76484':r'\frac{{x}^{2}+{y}^{2}}{5}', 'q-76496':r'\frac{y+z}{x}'}[source]
    for i in range(0,len(parts),2):parts[i]=parts[i].replace(fcomponent,scaled(fcomponent,k))
    # Display 3: f(r(t)). All concrete RHS components scale together.
    # Display 4: first RHS refers to the actual f, later explicit integrals scale.
    # Display 5: complete scalar substitution chain, including its LHS scales.
    for display in (5,7,9):
        chunk=parts[display]; start=chunk.index('\\begin{aligned}')+len('\\begin{aligned}'); end=chunk.index('\\end{aligned}')
        rows=chunk[start:end].split(r'\\')
        for index,row in enumerate(rows):
            lhs,rhs=row.split('& =',1)
            if display==9 and index==0:lhs=scaled(lhs,k)
            if not(display==7 and index==0):
                # Preserve terminal punctuation outside the mathematical component.
                tail='.' if rhs.endswith('.') else ''
                core=rhs[:-1] if tail else rhs
                rhs='='.join(scaled(component,k) for component in core.split('='))+tail
            rows[index]=lhs+'& ='+rhs
        parts[display]=chunk[:start]+r'\\'.join(rows)+chunk[end:]
    return '$$'.join(parts)


def domain(template):
    """Finite, unordered same-workload domains. Explicit calls obey these too."""
    import itertools as I
    if template=='parabola_easy':return [dict(k=k,m=m) for k,m in I.product(range(1,13),(3,5,7))]
    if template=='ratio':return [dict(a=a,h=h,k=k,ma=ma,mb=mb) for a,h,k,(ma,mb) in I.product(range(1,4),(-2,-1,0,1,2),range(1,13),((3,5),(3,7),(5,7)))]
    if template=='cubic':return [dict(s=s,b=b,n=n) for s,b,n in I.product(range(1,4),range(1,6),(1,2,3))]
    if template=='cos_diagonal':return [dict(a=a,b=b,k=k,angle=angle) for a,b,k,angle in I.product(range(1,5),(-4,-3,-2,-1),range(1,7),(2,3,6))]
    if template=='sine_line':return [dict(p=p,q=-q,d=d,angle=angle) for (p,q),d,angle in I.product(((4,3),(3,4),(12,5),(5,12),(15,8),(8,15)),range(1,13),(2,6))]
    if template=='sin_cos':return [dict(s=s,z=z,k=k) for s,z,k in I.product(range(1,4),range(1,4),range(1,7))]
    if template=='space_ratio':return [dict(a=a,b=b,c=c,k=k,lo=lo,hi=hi) for a,b,c,k,(lo,hi) in I.product(range(1,4),range(1,4),range(1,4),range(1,7),((1,2),(1,3),(2,3),(2,4),(3,4)))]
    raise ValueError('unknown template')


def mathematics(template,p):
    """Actual curve, substitution and endpoint data used by every display mask."""
    if template=='parabola_easy':
        r=(t*t,t);f=p['k']*y; low=0; high=S.sqrt(S.Rational(p['m']**2-1,4)); v=4*t*t+1; W=S.Rational(p['k'],8)
    elif template=='ratio':
        a,h,k,ma,mb=[p[v] for v in ('a','h','k','ma','mb')]
        r=(a*t*t,t+h);f=k*x/(y-h);low=S.sqrt(S.Rational(ma*ma-1,4*a*a));high=S.sqrt(S.Rational(mb*mb-1,4*a*a));v=4*a*a*t*t+1;W=S.Rational(k,8*a)
    elif template=='cubic':
        s,b,n=[p[v] for v in ('s','b','n')];r=(3*s*t,s*t**3);f=x**3+b*y;low=0;high=S.root(n,4);v=1+t**4;W=S.Rational(3*s*(27*s**3+b*s),4)
    elif template=='cos_diagonal':
        a,b,k,ang=[p[v] for v in ('a','b','k','angle')];r=(a*t*t,b*t*t);f=k*S.cos(x);low=0;high=S.sqrt(S.pi/(ang*a));v=a*t*t;W=k*S.sqrt(a*a+b*b)/a
    elif template=='sine_line':
        p0,q,d,ang=[p[v] for v in ('p','q','d','angle')];r=(p0*S.sin(t),q*S.sin(t));f=(x*x+y*y)/d;low=0;high=S.pi/ang;v=S.sin(t);W=S.sqrt(p0*p0+q*q)**3/d
    elif template=='sin_cos':
        s,z0,k=[p[v] for v in ('s','z','k')];r=(t,s*S.sin(t),S.Integer(z0));f=k*y*z*S.cos(x);low=0;high=S.pi/2;v=1+s*s*S.cos(t)**2;W=-S.Rational(k*z0,2*s)
    else:
        a,b,c,k,lo,hi=[p[v] for v in ('a','b','c','k','lo','hi')];r=(a*t,b*t*t/2,c*t*t/2);f=k*(y+z)/x;low=S.sqrt(lo);high=S.sqrt(hi);v=a*a+(b*b+c*c)*t*t;W=S.Rational(k*(b+c),4*a*(b*b+c*c))
    dr=tuple(S.diff(c,t) for c in r); speed=S.sqrt(S.expand(sum(c*c for c in dr)))
    if template=='sine_line':speed=S.sqrt(p['p']**2+p['q']**2)*S.cos(t)
    fr=S.simplify(f.subs(dict(zip((x,y,z),r)), simultaneous=True)); integrand=S.simplify(fr*speed)
    A=S.simplify(v.subs(t,low));B=S.simplify(v.subs(t,high))
    transformed=W*(S.cos(u) if template=='cos_diagonal' else u**2 if template=='sine_line' else S.sqrt(u))
    primitive=W*S.sin(u) if template=='cos_diagonal' else W*u**3/3 if template=='sine_line' else 2*W*u**S.Rational(3,2)/3
    upper=S.simplify(primitive.subs(u,B));lower=S.simplify(primitive.subs(u,A));answer=S.simplify(upper-lower)
    return dict(r=r,f=f,low=S.sympify(low),high=high,dr=dr,speed=speed,fr=fr,integrand=integrand,v=v,dv=S.diff(v,t),W=W,A=A,B=B,transformed=transformed,primitive=primitive,upper=upper,lower=lower,answer=answer)


def integral(a,b,expression,var='t'):return r'{\int }_{'+tex(a)+'}^{'+tex(b)+'}'+expression+r'\,\text{d}'+var

def solution(template,p,m):
    """Shared formal -> component -> reduced masks, no eager endpoint collapse."""
    dims=len(m['r']); coords=('x','y','z')[:dims];basis=('i','j','k')[:dims]
    vector=lambda comps: '+'.join('('+tex(v)+r')\,'+b for v,b in zip(comps,basis))
    curve=vector(m['r']);f=tex(m['f']);formal='+'.join(r'\frac{\text{d}'+c+r'}{\text{d}t}\,'+b for c,b in zip(coords,basis))
    diffops='+'.join(r'\frac{\text{d}}{\text{d}t}('+tex(v)+r')\,'+b for v,b in zip(m['r'],basis))
    speedformal=r'\sqrt{'+ '+'.join(r'(\frac{\text{d}'+c+r'}{\text{d}t})^2' for c in coords)+'}'
    speedsquare=r'\sqrt{'+ '+'.join('('+tex(v)+')^2' for v in m['dr'])+'}'
    derivative=[r"r'(t)"+eq(formal),eq(diffops),eq(vector(m['dr'])),r"\|r'(t)\|"+eq(speedformal),eq(speedsquare)]
    rad=S.expand(sum(v*v for v in m['dr']))
    if template=='sine_line':
        derivative += [eq(r'\sqrt{'+str(p['p']**2)+r'\cos^2 t+'+str(p['q']**2)+r'\cos^2 t}')]
    derivative += [eq(r'\sqrt{'+tex(rad)+'}')]
    if template=='sine_line':derivative += [eq(tex(S.sqrt(p['p']**2+p['q']**2))+r'|\cos t|')]
    if template=='cos_diagonal':derivative += [eq(tex(2*S.sqrt(p['a']**2+p['b']**2))+r'|t|')]
    derivative += [eq(tex(m['speed']))]
    # Don't show a duplicate reduction if the radicand is already the final speed.
    if derivative[-1]==derivative[-2]:derivative.pop()
    subs={x:m['r'][0],y:m['r'][1]}
    if dims==3:subs[z]=m['r'][2]
    # Unevaluated masks preserve actual component substitution/expansion operations.
    if template=='ratio':
        sub=r'\frac{'+str(p['k'])+'('+tex(m['r'][0])+')}{('+tex(m['r'][1])+')-('+str(p['h'])+')}'
        middle=r'\frac{'+str(p['k']*p['a'])+r't^2}{t}'
    elif template=='cubic':
        sub='('+tex(m['r'][0])+')^3+('+str(p['b'])+')('+tex(m['r'][1])+')';middle=str((3*p['s'])**3)+r't^3+'+str(p['b']*p['s'])+r't^3'
    elif template=='sine_line':
        sub=r'\frac{('+tex(m['r'][0])+')^2+('+tex(m['r'][1])+')^2}{'+str(p['d'])+'}'
        middle=r'\frac{'+str(p['p']**2)+r'\sin^2 t+'+str(p['q']**2)+r'\sin^2 t}{'+str(p['d'])+'}'
    elif template=='space_ratio':
        sub=r'\frac{('+str(p['k'])+')[('+tex(m['r'][1])+')+('+tex(m['r'][2])+')]}{'+tex(m['r'][0])+'}'
        middle=r'\frac{('+tex(S.Rational(p['k']*(p['b']+p['c']),2))+r')t^2}{('+str(p['a'])+')t}'
    elif template=='sin_cos':sub='('+str(p['k'])+')('+tex(m['r'][1])+')('+str(p['z'])+r')\cos('+tex(m['r'][0])+')';middle=None
    elif template=='cos_diagonal':sub='('+str(p['k'])+r')\cos('+tex(m['r'][0])+')';middle=None
    else:sub='('+str(p['k'])+')('+tex(m['r'][1])+')';middle=None
    frrows=['f(r(t))'+eq(sub)]
    if middle:frrows += [eq(middle)]
    if sub!=tex(m['fr']):frrows +=[eq(tex(m['fr']))]
    if template=='cos_diagonal':frrows=['f(r(t))'+eq(tex(m['fr']))]
    setup=[r'\int_C f\,\text{d}s'+eq(integral(m['low'],m['high'],r"f(r(t))\,\|r'(t)\|")),eq(integral(m['low'],m['high'],'('+tex(m['fr'])+')('+tex(m['speed'])+')'))]
    if template in ('cubic','sine_line'):setup +=[eq(integral(m['low'],m['high'],tex(m['integrand'])))]
    # Ordered substitution, primitive, substitution endpoints, individual endpoint
    # evaluation and collected arithmetic. Explicit expressions retain operands.
    P=m['primitive']; W=m['W']; A=m['A'];B=m['B']
    if template=='cos_diagonal':endpoint=tex(W)+r'[\sin('+tex(B)+r')-\sin('+tex(A)+')]'
    elif template=='sine_line':endpoint=tex(W)+r'[\frac{('+tex(B)+r')^3}{3}-\frac{('+tex(A)+')^3}{3}]'
    else:endpoint=tex(S.Rational(2,3)*W)+r'[('+tex(B)+')^{3/2}-('+tex(A)+')^{3/2}]'
    if template=='cos_diagonal': evaluated=tex(W)+'[('+tex(S.sin(B))+')-('+tex(S.sin(A))+')]'
    elif template=='sine_line':evaluated=tex(W)+'[('+tex(B**3/3)+')-('+tex(A**3/3)+')]' 
    else:evaluated=tex(S.Rational(2,3)*W)+'[('+tex(S.simplify(B**S.Rational(3,2)))+')-('+tex(S.simplify(A**S.Rational(3,2)))+')]'
    primitive_mask=tex(W)+r'\sin u' if template=='cos_diagonal' else tex(W)+r'\cdot\frac{u^3}{3}' if template=='sine_line' else tex(W)+r'\cdot\frac{2}{3}u^{3/2}'
    calc=[integral(m['low'],m['high'],tex(m['integrand']))+eq(integral(A,B,tex(W)+r'\cdot '+('\\cos u' if template=='cos_diagonal' else r'u^2' if template=='sine_line' else r'u^{1/2}'),'u')),eq(primitive_mask+r'\big|_{'+tex(A)+'}^{'+tex(B)+'}'),eq(endpoint),eq(evaluated),eq('('+tex(m['upper'])+')-('+tex(m['lower'])+')'),eq(tex(m['answer']))]
    if template=='space_ratio':
        calc[0]=integral(m['low'],m['high'],tex(m['integrand']))+eq(integral(A,B,r'\sqrt{u}\cdot '+tex(W),'u'))
        calc.insert(1,eq(tex(W)+integral(A,B,r'u^{1/2}','u')))
    notice=''
    if template=='cos_diagonal':notice='\n\nNotice that $|t|=t$ because $t\\geq0$ along the path of $C.$'
    if template=='sine_line':notice='\n\nNotice that $|\\cos t|=\\cos t$ because $\\cos t\\geq0$ along this interval.'
    if template=='sin_cos':notice='\n\nThe substitution decreases from $'+tex(A)+'$ to $'+tex(B)+'$; its differential includes the negative sign.'
    return ('To calculate the line integral, we will use the formula\n\n'+block([r"\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t."])+ '\n\nSince $r(t)='+curve+'$, then along the curve we have '+', '.join('$'+c+'='+tex(v)+'$' for c,v in zip(coords,m['r']))+'.\n\nComputing $r\'(t)$ and $\\|r\'(t)\\|,$ we get the following:\n\n'+block(derivative)+notice+'\n\nNow, since $f('+','.join(coords)+')='+f+'$, we obtain\n\n'+block(frrows)+'\n\nTherefore, we can write the integral as\n\n'+block(setup)+'\n\nWe can solve this using the substitution $u='+tex(m['v'])+'$, $\\text{d}u=('+tex(m['dv'])+')\\,\\text{d}t$ as follows:\n\n'+block(calc))


def banks(template,p,m):
    """Complete authored operations, selected before parameters (one per family)."""
    ans=m['answer'];A=m['A'];B=m['B'];W=m['W']
    if template=='cos_diagonal':
        a,b,k=[p[v] for v in ('a','b','k')]
        return [('correct',ans),('omit differential 2a',2*a*ans),('cosine primitive instead of sine',W*(S.cos(B)-S.cos(A))),('retain old t bounds after u substitution',W*(S.sin(m['high'])-S.sin(m['low']))),('sum signed velocity components as speed',S.Rational(k*(a+b),a)*(S.sin(B)-S.sin(A)))]
    if template=='sine_line':
        L=S.sqrt(p['p']**2+p['q']**2);d=p['d'];bnd=m['high']
        # Actual speed-squared integral: L^4/d integral sin²t cos²t dt.
        speed_squared=L**4/d*(bnd/8-S.sin(4*bnd)/32)
        return [('correct',ans),('omit speed',ans/L),('use speed squared',speed_squared),('omit power reciprocal',W*(B**3-A**3)),('use square primitive',W*(B**2-A**2)/2)]
    if template=='sin_cos':
        # u reversed limits are preserved. Squared-speed integrand admits cos t substitution.
        s,z0,k=[p[v] for v in ('s','z','k')]
        sq=S.Rational(k*s*z0,1)*(S.Rational(1,2)+S.Rational(s*s,4))
        return [('correct',ans),('omit speed',S.Rational(k*s*z0,2)),('use speed squared',sq),('omit substitution differential',ans*(-2*s*s)),('use square-root primitive',2*W*(S.sqrt(B)-S.sqrt(A)))]
    derivativefactor={'parabola_easy':8,'ratio':8*p.get('a',1)**2,'cubic':4,'space_ratio':2*(p.get('b',0)**2+p.get('c',0)**2)}[template]
    omitted_ds=S.integrate(m['fr'],(t,m['low'],m['high']))
    return [('correct',ans),('omit substitution differential',ans*derivativefactor),('use square-root primitive',2*W*(S.sqrt(B)-S.sqrt(A))),('add endpoint primitive values',m['upper']+m['lower']),('omit speed',omitted_ds)]


def unique_bank(values):
    return all(S.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[i+1:])
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def identity(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio fields supported')
    rng=random.Random(seed)
    if profile and profile.startswith('raw:'):
        source=profile[4:]
        if source not in SOURCES:raise ValueError('unknown raw source')
        family=SOURCE_TEMPLATE[source]
        if template not in (None,family):raise ValueError('source template mismatch')
        if level!=LEVELS[family]:raise ValueError('source replay level route mismatch')
        p={'scale':rng.choice((1,2,3,4,5,6))} if parameters is None else dict(parameters)
        if set(p)!={'scale'} or type(p['scale']) is not int or p['scale'] not in range(1,7):raise ValueError('raw scale is integer 1..6')
        k=p['scale'];q=copy.deepcopy(SOURCES[source]);q.pop(':db/id',None);q.pop(':question/math-academy-id',None)
        q[':question/problem']=raw_prompt(source,k)
        if ':question/worked-solution' in q:q[':question/worked-solution']=raw_solution(source,k)
        if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
        vals=[scaled(a[':answer/value'],k) for a in q[':question/answer-fields'][0][':answer-field/choices']]
        correct_original=SOURCES[source][':question/answer-fields'][0].get(':answer-field/correct',{}).get(':answer/id')
        corridx=next((i for i,a in enumerate(SOURCES[source][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==correct_original),None)
        actual=mathematics(family,ANCHORS[family]);task=digest([[str(v) for v in actual['r']],str(actual['f']*k),str(actual['low']),str(actual['high'])]);evidence=True
        solutionmeta={};mathvalues=[v*k for v in SOURCE_VALUES[source]]
    else:
        supported=[f for f,l in LEVELS.items() if l==level]
        family=template or rng.choice(supported)
        if family not in supported:raise ValueError('template outside difficulty')
        if profile not in (None,'method'):raise ValueError('unknown bank profile')
        profile='method'
        candidates=domain(family)
        if parameters is not None:
            p=dict(parameters)
            if any(type(v) is not int for v in p.values()) or p not in candidates:raise ValueError('explicit parameters outside finite workload domain')
            actual=mathematics(family,p);bank=banks(family,p,actual)
            if not unique_bank([v for _,v in bank]):raise ValueError('whole-bank mathematical ambiguity')
        else:
            for _ in range(1000):
                p=rng.choice(candidates);actual=mathematics(family,p);bank=banks(family,p,actual)
                if unique_bank([v for _,v in bank]):break
            else:raise RuntimeError('domain has no eligible bank')
        vals=[tex(v) for _,v in bank];mathvalues=[v for _,v in bank];corridx=0
        coords=('x','y','z')[:len(actual['r'])]; curve=r'\langle '+','.join(tex(v) for v in actual['r'])+r'\rangle'
        prompt='Evaluate the line integral of the function $f('+','.join(coords)+')='+tex(actual['f'])+'$ along the curve parametrized by $r(t)='+curve+'$ for $t\\in ['+tex(actual['low'])+','+tex(actual['high'])+'].$'
        q={':question/problem':prompt,':question/worked-solution':solution(family,p,actual),':question/difficulty':':question.difficulty/'+level}
        task=digest([[str(v) for v in actual['r']],str(actual['f']),str(actual['low']),str(actual['high'])]);evidence=False
        solutionmeta={key:str(actual[key]) for key in ('speed','fr','integrand','v','dv','A','B','W','transformed','primitive','upper','lower','answer')}
    # Identity from actual learner content + full unordered bank, not profile aliases.
    cid=digest([VERSION,q[':question/problem'],q.get(':question/worked-solution'),q.get(':question/difficulty'),sorted(vals),('selection',':answer-field.type/radio'),None if corridx is None else vals[corridx]])
    q[':question/id']=identity(cid)
    fid=identity(cid+'/selection');answers=[{':answer/id':identity(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if corridx is not None:field[':answer-field/correct']=[':answer/id',answers[corridx][':answer/id']]
    rng.shuffle(answers);q[':question/answer-fields']=[field]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':family,'profile':profile,'parameters':p,'seed':seed,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_ids':[s for s,f in SOURCE_TEMPLATE.items() if f==family],'authored_level':family=='parabola_easy' or family=='sin_cos','evidence_only':evidence,'eligible_for_learning':not evidence,'mathematical_fingerprint':task,'content_fingerprint':cid,'solution_components':solutionmeta,'choice_values':[str(v) for v in mathvalues],'bank_operations':[] if evidence else [name for name,_ in bank],'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'plot_rating':'none'}}

# Easy: authored direct y substitution on a planar parabola, zero lower bound.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed planar algebraic/trig families; inferred unrated 3D sin/cos.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed 3D rational combination and nonzero radical endpoint subtraction.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2,ensure_ascii=False))
    else:
        for rec in records:
            print(rec['question'][':question/problem']);print('\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']));print('\n'+rec['question'].get(':question/worked-solution','[Source solution absent.]')+'\n')
if __name__=='__main__':main()
