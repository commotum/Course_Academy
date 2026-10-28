#!/usr/bin/env python3
"""Seeded scalar line-integral practice. No database or runtime asset writes."""
from __future__ import annotations
import argparse,copy,hashlib,json,random,sys,uuid
from pathlib import Path
import sympy as S
from math_format import normalize_prose,normalize_tex,validate_generated_record
KP_ID=17592186133827
KP_UUID='da23f1c0-678a-51c0-a2db-e12d756f9120'
TITLE='Evaluating the Line Integral of a Scalar Function Using a Substitution'
VERSION='scalar-substitution-4'
t=S.Symbol('t', real=True); u=S.Symbol('u', positive=True)
x,y,z=S.symbols('x y z',real=True)
LEVELS={'parabola_easy':'easy','ratio':'moderate','cubic':'moderate','cos_diagonal':'moderate','sine_line':'moderate','sin_cos':'moderate','space_ratio':'hard'}
SOURCE_IDS={'ratio':['a42a0c64-6afa-5778-a107-25576497d815'],'cubic':['c2dda2ab-f3d6-5a31-a33f-5b15f55a34c3'],'cos_diagonal':['5d73cf87-1a19-5cca-88b7-764818d04cb6'],'sine_line':['8ffd2389-f864-5810-9cd3-9a41b1f9dc53'],'sin_cos':['56e093a1-badc-5734-b16b-054c37904e43'],'space_ratio':['004b67de-a618-52fc-b8e0-1a45d41d2be5','b0411044-fc20-574c-a3d2-b78307b21dd1'],'parabola_easy':['c3fd95d9-ac39-5143-ab7b-7b87094db6e4']}
PROFILES=('differential','endpoints','primitive')
def tex(e):
    e=S.sympify(e)
    if e.is_number and e.is_positive and e.has(S.pi) and (e**2/S.pi).is_Rational:
        return normalize_tex(r'\sqrt{'+S.latex(S.simplify(e**2))+'}')
    return normalize_tex(S.latex(e,fold_short_frac=False).replace('\\log','\\ln'))
def block(rows): return '$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$'
def eq(e): return r' & ='+e
def mathematics(template,p):
    """Actual curve, substitution and endpoint data used by every display mask."""
    if template=='parabola_easy':
        r=(p['a']*t*t,t);f=p['k']*y; low=S.sqrt(p['lo']); high=S.sqrt(p['hi']); v=4*p['a']**2*t*t+1; W=S.Rational(p['k'],8*p['a']**2)
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
    dr=tuple(S.diff(c,t) for c in r); speed=S.sqrt(S.factor(S.expand(sum(c*c for c in dr))))
    if template=='cos_diagonal':speed=2*S.sqrt(p['a']**2+p['b']**2)*t
    if template=='sine_line':speed=S.sqrt(p['p']**2+p['q']**2)*S.cos(t)
    fr=S.cancel(f.subs(dict(zip((x,y,z),r)), simultaneous=True)) if template in ('ratio','space_ratio') else S.expand_mul(f.subs(dict(zip((x,y,z),r)), simultaneous=True)); integrand=fr*speed
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
    setup=['I'+eq(r'\int_C f\,\text{d}s'),eq(integral(m['low'],m['high'],r"f(r(t))\,\|r'(t)\|")),eq(integral(m['low'],m['high'],'('+tex(m['fr'])+')('+tex(m['speed'])+')'))]
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
    calc=['I'+eq(integral(A,B,tex(W)+r'\cdot '+('\\cos u' if template=='cos_diagonal' else r'u^2' if template=='sine_line' else r'u^{1/2}'),'u')),eq(primitive_mask+r'\big|_{'+tex(A)+'}^{'+tex(B)+'}'),eq(endpoint),eq(evaluated),eq('('+tex(m['upper'])+')-('+tex(m['lower'])+')'),eq(tex(m['answer']))]
    if template=='space_ratio':
        calc[0]='I'+eq(integral(A,B,r'\sqrt{u}\cdot '+tex(W),'u'))
        calc.insert(1,eq(tex(W)+integral(A,B,r'u^{1/2}','u')))
    notice=''
    if template=='cos_diagonal':notice='\n\nNotice that $|t|=t$ because $t\\geq0$ along the path of $C.$'
    if template=='sine_line':notice='\n\nNotice that $|\\cos t|=\\cos t$ because $\\cos t\\geq0$ along this interval.'
    if template=='sin_cos':notice='\n\nThe substitution decreases from $'+tex(A)+'$ to $'+tex(B)+'$; its differential includes the negative sign.'
    return ('To calculate the line integral, we will use the formula\n\n'+block([r"\int_C f\,\text{d}s=\int_a^b f(r(t))\,\|r'(t)\|\,\text{d}t."])+ '\n\nSince $r(t)='+curve+'$, then along the curve we have '+', '.join('$'+c+'='+tex(v)+'$' for c,v in zip(coords,m['r']))+'.\n\nComputing $r\'(t)$ and $\\|r\'(t)\\|,$ we get the following:\n\n'+block(derivative)+notice+'\n\nNow, since $f('+','.join(coords)+')='+f+'$, we obtain\n\n'+block(frrows)+'\n\nTherefore, we can write the integral as\n\n'+block(setup)+'\n\nWe can solve this using the substitution $u='+tex(m['v'])+'$, $\\text{d}u=('+tex(m['dv'])+')\\,\\text{d}t$ as follows:\n\n'+block(calc))


def domain(family):
    import itertools as I
    signs=(-3,-1,1,2,3,6)
    if family=='parabola_easy':return [dict(a=a,k=k,lo=lo,hi=hi) for a,k,(lo,hi) in I.product((1,2),signs,((0,1),(0,2),(1,2),(1,3)))]
    if family=='ratio':return [dict(a=a,h=h,k=k,ma=ma,mb=mb) for a,h,k,(ma,mb) in I.product((1,2),(-1,0,1),signs,((3,5),(3,7),(5,7)))]
    if family=='cubic':return [dict(s=1,b=b,n=n) for b,n in I.product((1,3,5),(1,2))]
    if family=='cos_diagonal':return [dict(a=a,b=b,k=k,angle=angle) for a,b,k,angle in I.product((1,2,3),(-3,-2,-1),(-2,-1,1,2),(2,3,6))]
    if family=='sine_line':return [dict(p=p,q=-q,d=d,angle=angle) for (p,q),d,angle in I.product(((4,3),(3,4),(5,12),(12,5)),(3,5,6),(2,6))]
    if family=='sin_cos':return [dict(s=s,z=z,k=k) for s,z,k in I.product((1,2),(1,2),signs)]
    if family=='space_ratio':return [dict(a=1,b=b,c=c,k=k,lo=lo,hi=hi) for (b,c),k,(lo,hi) in I.product(((1,1),(1,2),(2,1)),signs,((1,2),(1,3),(2,3)))]
    raise ValueError('unknown family')

def banks(family,p,m,profile,flavor="mixed"):
    """A complete, preselected error model. Never fill collisions ad hoc."""
    ans=m['answer']; A=m['A'];B=m['B'];W=m['W']
    if family=='cos_diagonal':
        a,b,k=p['a'],p['b'],p['k'];L=S.sqrt(a*a+b*b)
        errors={
            'omit differential factor':2*a*ans,
            'repeat differential factor':ans/(2*a),
            'sum signed derivative components':ans*(a+b)/L,
            'use squared norm prefactor':ans*L,
            'omit y derivative from speed':ans*a/L,
            'omit x derivative from speed':ans*abs(b)/L,
            'use cosine primitive':W*(S.cos(B)-S.cos(A)),
            'omit norm square root':ans*L**2,
            'invert speed prefactor':ans/(4*L**2),
            'repeat differential factor twice':ans/(2*a)**2,
            'multiply differential factor twice':ans*(2*a)**2,
        }
        names={
            'differential':['omit differential factor','repeat differential factor','sum signed derivative components','use squared norm prefactor'],
            'primitive':['repeat differential factor','use squared norm prefactor','invert speed prefactor','repeat differential factor twice'],
            'endpoints':['omit differential factor','use squared norm prefactor','omit norm square root','omit y derivative from speed'],
        }[profile]
    elif family=='sine_line':
        L=S.sqrt(p['p']**2+p['q']**2)
        errors={
            'omit speed prefactor':ans/L,
            'square speed prefactor':ans*L,
            'omit power reciprocal':3*ans,
            'repeat power reciprocal':ans/3,
            'omit scalar squared-coordinate sum':ans/L**2,
            'omit y squared in scalar':ans*p['p']**2/L**2,
            'use square primitive':W*(B**2-A**2)/2,
            'use speed prefactor squared twice':ans*L**2,
        }
        names={
            'differential':['omit speed prefactor','square speed prefactor','omit power reciprocal','repeat power reciprocal'],
            'primitive':['omit speed prefactor','omit scalar squared-coordinate sum','repeat power reciprocal','omit y squared in scalar'],
            'endpoints':['square speed prefactor','omit power reciprocal','use square primitive','use speed prefactor squared twice'],
        }[profile]
    else:
        D={'parabola_easy':8*p.get('a',1)**2,'ratio':8*p.get('a',1)**2,'cubic':4,'sin_cos':2*p.get('s',1)**2,'space_ratio':2*(p.get('b',0)**2+p.get('c',0)**2)}[family]
        # Independent mistakes in primitive, differential, speed and bounds.
        errors={
            'omit differential magnitude':ans*D,
            'repeat differential magnitude':ans/D,
            'omit power reciprocal':ans*S.Rational(3,2),
            'repeat power reciprocal':ans*S.Rational(2,3),
            'use square-root primitive':2*W*(S.sqrt(B)-S.sqrt(A)),
            'omit one endpoint contribution':-m['lower'] if family=='sin_cos' else m['upper'],
            'add endpoint contributions':m['upper']+m['lower'],
            'omit speed':S.integrate(m['fr'],(t,m['low'],m['high'])),
        }
        names={
            'differential':['omit differential magnitude','repeat differential magnitude','omit power reciprocal','repeat power reciprocal'],
            'endpoints':['omit one endpoint contribution','add endpoint contributions','omit differential magnitude','use square-root primitive'],
            'primitive':['repeat differential magnitude','repeat power reciprocal','use square-root primitive','omit speed'],
        }[profile]
    # Complete variants retain the same visible mathematical bank shape while
    # changing whether differential/normalization errors over- or under-scale.
    if family=='cos_diagonal':
        if profile=='differential' and flavor=='over':names=['omit differential factor','multiply differential factor twice','sum signed derivative components','use squared norm prefactor']
        if profile=='differential' and flavor=='under':names=['repeat differential factor twice','repeat differential factor','sum signed derivative components','use squared norm prefactor']
        if profile=='primitive' and flavor=='over':names=['repeat differential factor','use squared norm prefactor','multiply differential factor twice','omit differential factor']
        if profile=='endpoints' and flavor=='over':names=['omit differential factor','use squared norm prefactor','repeat differential factor','multiply differential factor twice']
        if profile=='endpoints' and flavor=='under':names=['repeat differential factor','use squared norm prefactor','repeat differential factor twice','omit y derivative from speed']
    elif family=='sine_line':
        if profile=='differential' and flavor=='over':names=['omit speed prefactor','square speed prefactor','omit power reciprocal','use speed prefactor squared twice']
        if profile=='differential' and flavor=='under':names=['omit speed prefactor','omit scalar squared-coordinate sum','omit y squared in scalar','repeat power reciprocal']
        if profile=='primitive' and flavor=='over':names=['square speed prefactor','omit scalar squared-coordinate sum','repeat power reciprocal','omit y squared in scalar']
        if profile=='endpoints' and flavor=='under':names=['square speed prefactor','omit power reciprocal','use square primitive','omit scalar squared-coordinate sum']
    else:
        errors['multiply differential magnitude twice']=ans*D**2
        errors['repeat differential magnitude twice']=ans/D**2
        errors['divide primitive by three again']=ans/3
        if profile=='differential' and flavor=='over':names=['omit differential magnitude','repeat differential magnitude','omit power reciprocal','multiply differential magnitude twice']
        if profile=='differential' and flavor=='under':names=['repeat differential magnitude','repeat power reciprocal','repeat differential magnitude twice','divide primitive by three again']
        if profile=='primitive' and flavor=='over':names=['omit differential magnitude','repeat power reciprocal','use square-root primitive','omit speed']
        if profile=='endpoints' and flavor=='under':names=['omit one endpoint contribution','add endpoint contributions','repeat differential magnitude','use square-root primitive']
    return [('correct',ans)]+[(n,S.simplify(errors[n])) for n in names]

def unique_bank(bank):
    vals=[v for _,v in bank]
    # Also exclude an exact opposite pair: that pair can disclose the correct sign.
    return all(S.simplify(a-b)!=0 for i,a in enumerate(vals) for b in vals[i+1:]) and all(S.simplify(vals[0]+v)!=0 for v in vals[1:])

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def identity(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))

def structural_key(family,p):
    keys={'parabola_easy':('a','lo','hi'),'ratio':('a','ma','mb'),'cubic':('s','n'),'cos_diagonal':('a','b','angle'),'sine_line':('p','q','angle'),'sin_cos':('s',),'space_ratio':('a','lo','hi')}
    values=tuple(p[k] for k in keys[family])
    if family=='space_ratio':values+=(p['b']**2+p['c']**2,)
    if family=='sine_line':values=(p['p']**2+p['q']**2,p['angle'])
    return values

def generate(level,seed=0,template=None,parameters=None,profile=None,excluded_structures=(),bank_flavor=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    rng=random.Random(seed)
    supported=[f for f,l in LEVELS.items() if l==level]
    family=template or rng.choice(supported)
    if family not in supported:raise ValueError('family outside difficulty')
    profile=profile or rng.choice(PROFILES)
    if profile not in PROFILES:raise ValueError('unknown profile')
    flavor=bank_flavor or random.Random(str(seed)+':bank-flavor').choice(('mixed','over','under'))
    if flavor not in ('mixed','over','under'):raise ValueError('bank flavor')
    candidates=domain(family)
    if parameters is not None:candidates=[dict(parameters)]
    else:rng.shuffle(candidates)
    for p in candidates:
        if structural_key(family,p) in excluded_structures:continue
        actual=mathematics(family,p);bank=banks(family,p,actual,profile,flavor)
        if unique_bank(bank):break
    else:raise ValueError('No complete distinct bank for this instance/profile')
    coords=('x','y','z')[:len(actual['r'])]
    prompt=('Evaluate the line integral of $f('+','.join(coords)+')='+tex(actual['f'])+'$ along the curve\n\n$$\n'+r'\mathbf r(t)=\langle '+','.join(tex(v) for v in actual['r'])+r'\rangle,\qquad '+tex(actual['low'])+r'\le t\le '+tex(actual['high'])+'.\n$$\n\nGive the exact value.')
    if level=='easy':prompt+='\n\nUse the scalar line integral formula\n\n'+block([r"\int_C f\,\mathrm ds=\int_a^b f(\mathbf r(t))\|\mathbf r'(t)\|\,\mathrm dt."])
    worked=solution(family,p,actual)
    return make_record(level,prompt,worked,bank,rng,{
        'version':VERSION,'template':family,'profile':profile,'bank_flavor':flavor,'parameters':p,'seed':seed,
        'source_ids':SOURCE_IDS[family],
        'solution_components':{key:str(actual[key]) for key in ('speed','fr','integrand','v','dv','A','B','W','transformed','primitive','upper','lower','answer')},
        'bank_operations':[name for name,_ in bank],
        'choice_values':[str(v) for _,v in bank],
        'plot_rating':'none','eligible_for_learning':True,
    })

def make_record(level,prompt,worked,bank,rng,meta):
    prompt=normalize_prose(prompt);worked=normalize_prose(worked)
    vals=[tex(v) for _,v in bank]
    cid=digest([VERSION,level,prompt,worked,sorted(vals),vals[0]])
    fid=identity(cid+'/selection')
    answers=[{':answer/id':identity(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[0][':answer/id']]}
    random.Random(cid+':choices:'+str(meta.get('seed',0))).shuffle(answers)
    rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':identity(cid),':question/problem':prompt,':question/worked-solution':worked,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]},'generation':meta}
    return validate_generated_record(rec)

def replay_source(source_id):
    """Normalized historical replay only, never selected by normal sampling."""
    sources=json.loads(Path(__file__).with_name('replay.json').read_text())
    return copy.deepcopy(next(r for r in sources if r['generation']['source_ids']==[source_id]))

def generate_batch(level,count,seed):
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed);families=[f for f,l in LEVELS.items() if l==level]
    deck=[];profile_deck=[];records=[];seen=set();structures={f:set() for f in families}
    recipe_uses={};position_deck=[]
    for _ in range(count):
        if not deck:deck=families[:];rng.shuffle(deck)
        family=deck.pop()
        if not profile_deck:profile_deck=list(PROFILES);rng.shuffle(profile_deck)
        profile=profile_deck.pop()
        for attempt in range(100):
            item_seed=rng.getrandbits(63)
            # Cycle distinct complete error recipes, rather than flavor labels:
            # two flavor labels sometimes describe exactly the same bank model.
            # Selection consults error operations only, never the keyed rank.
            flavors=['mixed','over','under'];rng.shuffle(flavors)
            candidates=[]
            for flavor in flavors:
                try:
                    candidate=generate(level,item_seed,template=family,profile=profile,
                        excluded_structures=structures[family],bank_flavor=flavor)
                except ValueError:
                    continue
                recipe=tuple(candidate['generation']['bank_operations'])
                usage=recipe_uses.get((family,profile,recipe),0)
                candidates.append((usage,recipe,candidate))
            if not candidates:
                structures[family].clear()
                continue
            usage,recipe,rec=min(candidates,key=lambda candidate:candidate[0])
            q=rec['question'];signature=digest([q[':question/problem'],q[':question/worked-solution']])
            if signature not in seen:break
        else:raise RuntimeError('requested batch exhausts distinct semantic tasks')
        seen.add(signature);structures[family].add(structural_key(family,rec['generation']['parameters']))
        recipe_uses[(family,profile,recipe)]=usage+1
        # Seeded position deck prevents a short batch from collapsing to one
        # answer position, including within repeated visible bank shapes.
        if not position_deck:position_deck=list(range(5));rng.shuffle(position_deck)
        position=position_deck.pop()
        field=rec['question'][':question/answer-fields'][0]
        choices=field[':answer-field/choices'];correct_id=field[':answer-field/correct'][1]
        correct=next(a for a in choices if a[':answer/id']==correct_id)
        choices.remove(correct);choices.insert(position,correct)
        records.append(rec)
    return records

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified','all'],default='moderate')
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json','markdown'],default='json')
    args=ap.parse_args();level='moderate' if args.difficulty=='unclassified' else args.difficulty
    levels=('easy','moderate','hard') if level=='all' else (level,)
    records=[r for l in levels for r in generate_batch(l,args.count,args.seed)]
    if args.format=='json':print(json.dumps(records,indent=2,ensure_ascii=False))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']));print(q[':question/worked-solution'])
if __name__=='__main__':main()
