#!/usr/bin/env python3
"""Seeded complete Green's theorem practice; no service or database access."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import uuid
import sympy as s
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP=17592186133883
KPID='11d3f9e1-dad0-51d4-86a9-e0c49465cc3c'
VERSION='greens-complete-v3'
x,y=s.symbols('x y', real=True)
FAMILIES={'easy':['rectangle'],'moderate':['triangle','legacy-wedge'],'hard':['lens','quadratic-wedge']}
PROFILES={
 'signed-partials':['reverse','add','negative-add','omit-P'],
 'derivatives':['reverse','add','omit-P','omit-Q'],
 'integration':['reverse','inner-power','outer-power','box'],
 'mixed':['add','omit-Q','outer-power','box'],
 'component-signs':['omit-P','omit-Q','add','negative-add'],
 'orientation-signs':['zero','reverse','omit-P','negative-omit-P'],
 'closed-curve':['zero','reverse','add','omit-P'],
}

def tex(e): return normalize_tex(s.latex(s.sympify(e)))
def uid(text): return str(uuid.uuid5(uuid.UUID(KPID),VERSION+':'+text))
def display(text): return '$$\n'+text+'\n$$'
def aligned(rows): return display(r'\begin{aligned}'+'\n'+('\\\\\n'.join(rows))+'\n'+r'\end{aligned}')
def ident(e): return e.get(':db/ident') if isinstance(e,dict) else e

def instance(family,p):
    """Only mathematical data; no bank/solution/diagram-specific resampling."""
    a,b=p['a'],p['b'];h=p['h'];k=p['k'];n=p.get('n',1)
    extra=n*x**2+1;extraQ=n*y**2+1
    if family=='rectangle':
        lo,hi=s.Integer(p['left']),s.Integer(p['left']+k)
        low,up=s.Integer(p['bottom']),s.Integer(p['bottom']+h)
        P=a*y+extra;Q=b*x+extraQ;inner,outer=y,x
        vertices=[(lo,low),(hi,low),(hi,up),(lo,up)]
        description='the rectangle $'+tex(lo)+r'\le x\le '+tex(hi)+'$, $'+tex(low)+r'\le y\le '+tex(up)+'$'
        setup='The supplied rectangular bounds give independent limits.'
        source=['17592186701053','q-109149']
    elif family=='triangle':
        lo,hi=s.Integer(0),s.Integer(k);low,up=s.Rational(h,k)*x,s.Integer(h)
        P=a*x*y+extra;Q=b*x**2+extraQ;inner,outer=y,x
        vertices=[(0,0),(k,h),(0,h)]
        description='the triangle with vertices '+', '.join('$'+tex(s.Tuple(*v))+'$' for v in vertices)
        setup='The sloping side is $y='+tex(low)+'$. Vertical slices start there and end at $y='+tex(up)+'$.'
        source=['17592186701052','e-9072']
    elif family=='legacy-wedge':
        lo,hi=s.Integer(0),s.Integer(k);low,up=-s.Rational(h,k)*x,s.Rational(h,k)*x
        P=-a*x*y+extra;Q=b*x**2+extraQ;inner,outer=y,x
        vertices=[(0,0),(k,-h),(k,h)]
        description='the triangle with vertices '+', '.join('$'+tex(s.Tuple(*v))+'$' for v in vertices)
        setup='The two sloping sides are $y='+tex(low)+'$ and $y='+tex(up)+'$. Use vertical slices.'
        source=['q-41475']
    elif family=='lens':
        lo,hi=s.Integer(0),s.Integer(k);low,up=x**2,k*x
        P=a*x*y+p['c']*y**2+extra;Q=b*x**2+extraQ;inner,outer=y,x
        vertices=None
        description='the region enclosed by $y=x^2$ and $y='+tex(k*x)+'$'
        setup='The intersections satisfy $x^2='+tex(k*x)+'$, hence $x(x-'+str(k)+')=0$. Thus $x=0$ or $x='+str(k)+'$. Between them the parabola is below the line.'
        source=['17592186701041','q-109115','q-109166']
    elif family=='quadratic-wedge':
        lo,hi=s.Integer(0),s.Integer(h);low,up=-s.Rational(k,h)*y,s.Rational(k,h)*y
        P=-a*x**2*y+extra;Q=b*x*y**2+extraQ;inner,outer=x,y
        vertices=[(0,0),(k,h),(-k,h)]
        description='the triangle with vertices '+', '.join('$'+tex(s.Tuple(*v))+'$' for v in vertices)
        setup='The sloping sides are $x='+tex(low)+'$ and $x='+tex(up)+'$. Horizontal slices run between them.'
        source=['q-109147']
    else: raise ValueError(family)
    py=s.diff(P,y);qx=s.diff(Q,x);curl=s.expand(qx-py)
    primitive=s.integrate(curl,inner)
    inside=s.expand(primitive.subs(inner,up)-primitive.subs(inner,low))
    outside=s.integrate(inside,outer)
    answer=s.simplify(outside.subs(outer,hi)-outside.subs(outer,lo))
    return dict(family=family,parameters=p,P=P,Q=Q,py=py,qx=qx,curl=curl,inner=inner,outer=outer,
        low=low,up=up,lo=lo,hi=hi,primitive=primitive,inside=inside,outside=outside,answer=answer,
        description=description,setup=setup,vertices=vertices,sources=source)

def integral(d,e):
    return s.simplify(s.integrate(e,(d['inner'],d['low'],d['up']),(d['outer'],d['lo'],d['hi'])))

def wrong_primitive(expr,var):
    # A concrete power-rule error: add the power but omit division by it.
    return s.expand(sum(coef*var**(power[0]+1) for power,coef in s.Poly(expr,var).terms()))

def error_values(d):
    inner,outer=d['inner'],d['outer']
    bad=wrong_primitive(d['curl'],inner)
    bad_inner=s.expand(bad.subs(inner,d['up'])-bad.subs(inner,d['low']))
    outerbad=wrong_primitive(d['inside'],outer)
    # Integral over the enclosing rectangle, incorrectly ignoring sloped sides.
    pts=([d['low'].subs(outer,t) for t in [d['lo'],d['hi']]]+
         [d['up'].subs(outer,t) for t in [d['lo'],d['hi']]])
    box=s.integrate(d['curl'],(inner,min(pts),max(pts)),(outer,d['lo'],d['hi']))
    return {'zero':s.Integer(0),'negative-omit-P':-integral(d,d['qx']),'reverse':-d['answer'],'add':integral(d,d['qx']+d['py']),
            'negative-add':-integral(d,d['qx']+d['py']),
            'omit-P':integral(d,d['qx']),'omit-Q':integral(d,-d['py']),
            'inner-power':s.integrate(bad_inner,(outer,d['lo'],d['hi'])),
            'outer-power':outerbad.subs(outer,d['hi'])-outerbad.subs(outer,d['lo']),
            'box':box}

def draw(d,output):
    os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-greens-mpl')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    path=Path(output);path.mkdir(parents=True,exist_ok=True)
    key=hashlib.sha256(json.dumps([d['family'],d['parameters']['h'],d['parameters']['k'],
        d['parameters'].get('left'),d['parameters'].get('bottom')]).encode()).hexdigest()[:20]
    filename='region-'+key+'.png'
    if (path/filename).exists(): return filename
    ts=[float(d['lo'])+(float(d['hi'])-float(d['lo']))*i/160 for i in range(161)]
    lower=[float(d['low'].subs(d['outer'],float(t))) for t in ts]
    upper=[float(d['up'].subs(d['outer'],float(t))) for t in ts]
    if d['inner']==y:
        points=list(zip(ts,lower))+list(zip(ts[::-1],upper[::-1]))
    else:
        # Up side from bottom to top, low side back to bottom is CCW.
        points=list(zip(upper,ts))+list(zip(lower[::-1],ts[::-1]))
    points.append(points[0]);xx,yy=zip(*points)
    fig,ax=plt.subplots(figsize=(4.5,3.5),layout='constrained')
    ax.fill(xx,yy,color='#e0edff');ax.plot(xx,yy,color='#1f5687',lw=2)
    for f in [.16,.63]:
        i=int((len(points)-2)*f);j=min(i+9,len(points)-1)
        ax.annotate('',xy=points[j],xytext=points[i],arrowprops=dict(arrowstyle='->',color='#1f5687',lw=2))
    ax.axhline(0,color='#777',lw=.7);ax.axvline(0,color='#777',lw=.7)
    ax.set_xlabel('x');ax.set_ylabel('y',rotation=0);ax.set_aspect('equal',adjustable='box');ax.margins(.18)
    from matplotlib.ticker import MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(integer=True));ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.text(.96,.94,'D',transform=ax.transAxes,ha='right',va='top');ax.spines[['top','right']].set_visible(False)
    fig.savefig(path/filename,dpi=130);plt.close(fig)
    return filename

def render(d,difficulty,profile,seed=0,assets=None,bank_override=None):
    errors=error_values(d)
    values=[d['answer']]+[s.simplify(errors[n]) for n in PROFILES[profile]] if bank_override is None else bank_override
    if len(set(values))!=5 or sum(v==d['answer'] for v in values)!=1: raise ValueError('Bank collision')
    paired=[v for v in values if v!=0 and -v in values]
    if bank_override is None and len(paired)==2 and d['answer'] in paired:
        raise ValueError('Unique opposite pair reveals correct candidate')
    P,Q=tex(d['P']),tex(d['Q']);inner,outer=tex(d['inner']),tex(d['outer'])
    line=r'\oint_C \left('+P+r'\right)\,dx+\left('+Q+r'\right)\,dy'
    vector=d['family'] in ['lens','quadratic-wedge']
    prompt="Use Green's theorem to evaluate\n\n"+display(r'\oint_C\mathbf F\cdot d\mathbf r' if vector else line)+'\n\n'
    if vector: prompt+='where $\\mathbf F(x,y)=\\langle '+P+', '+Q+'\\rangle$ and $C$ is the boundary of '+d['description']+', traversed counterclockwise.'
    else: prompt+='where $C$ is the boundary of '+d['description']+', traversed counterclockwise.'
    solution=('The curve $C$ is a positively oriented, piecewise-smooth, simple closed curve. '
      'The components have continuous first partial derivatives on an open region containing $D$, so\n\n'+
      display(r'\oint_C P\,dx+Q\,dy=\iint_D(Q_x-P_y)\,dA.')+'\n\n')
    if vector: solution+='The vector form has $P='+P+'$ and $Q='+Q+'$.\n\n'
    else: solution+='Here $P='+P+'$ and $Q='+Q+'$.\n\n'
    solution+=aligned([r'P_y&='+tex(d['py'])+',',r'Q_x&='+tex(d['qx'])+',',r'Q_x-P_y&='+tex(d['curl'])+'.'])+'\n\n'+d['setup']+'\n\n'
    solution+=display('D=\\{(x,y):'+tex(d['lo'])+'\\le '+outer+'\\le '+tex(d['hi'])+',\\ '+tex(d['low'])+'\\le '+inner+'\\le '+tex(d['up'])+'\\}.')+'\n\n'
    if assets is not None: solution+='The shaded region and counterclockwise boundary are shown below.\n\n![]('+draw(d,assets)+')\n\n'
    rows=[r'\oint_C P\,dx+Q\,dy&=\int_{'+tex(d['lo'])+'}^{'+tex(d['hi'])+'}\\int_{'+tex(d['low'])+'}^{'+tex(d['up'])+'}\\left('+tex(d['curl'])+'\\right)\\,d'+inner+'\\,d'+outer,
      r'&=\int_{'+tex(d['lo'])+'}^{'+tex(d['hi'])+'}\\left['+tex(d['primitive'])+'\\right]_{'+tex(d['low'])+'}^{'+tex(d['up'])+'}\\,d'+outer,
      r'&=\int_{'+tex(d['lo'])+'}^{'+tex(d['hi'])+'}\\left('+tex(d['inside'])+'\\right)\\,d'+outer,
      r'&=\left['+tex(d['outside'])+'\\right]_{'+tex(d['lo'])+'}^{'+tex(d['hi'])+'}',
      '&='+tex(d['outside'].subs(d['outer'],d['hi']))+'-\\left('+tex(d['outside'].subs(d['outer'],d['lo']))+'\\right)',
      '&='+tex(d['answer'])+'.']
    solution+=aligned(rows)
    prompt,solution=normalize_prose(prompt),normalize_prose(solution)
    identity=json.dumps([difficulty,prompt,solution,sorted(tex(v) for v in values)])
    qid=uid(identity);fid=uid(qid+':selection')
    choices=[{':answer/id':uid(fid+':'+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in values]
    key=choices[values.index(d['answer'])][':answer/id'];random.Random(seed).shuffle(choices)
    r={'knowledge_point':{'db_id':KP,'id':KPID,'title':"Evaluating Line Integrals Using Green's Theorem"},
       'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
       ':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',key]}]},
       'generation':{'version':VERSION,'template':d['family'],'bank_profile':profile,'seed':seed,'parameters':d['parameters'],'source_ids':d['sources'],'source_basis':7398,'derivation':{'P':str(d['P']),'Q':str(d['Q']),'curl':str(d['curl']),'bounds':[str(d[t]) for t in ['inner','low','up','outer','lo','hi']],'answer':str(d['answer'])}}}
    return validate_generated_record(r)

def sample(difficulty,seed,count,assets=None):
    if difficulty=='unclassified': difficulty='easy'
    rng=random.Random(seed);records=[];seen=set();attempts=0
    # A complete batch must retain multiple decision cases within each visible
    # family. Rejection uses genuine error banks, never manufactured options.
    families=FAMILIES[difficulty]
    quotas={f:count//len(families) for f in families}
    for f in rng.sample(families,count%len(families)): quotas[f]+=1
    bank_cases={f:[] for f in families}
    while len(records)<count:
        attempts+=1
        if attempts>count*500+500: raise RuntimeError('Could not construct requested distinct batch')
        family=rng.choice([f for f in families if quotas[f]>0]);case=rng.choice(['positive','negative','cancel'])
        profile=rng.choice(list(PROFILES))
        p={'a':rng.choice([-3,-2,-1,1,2,3]),'b':rng.choice([-3,-2,-1,1,2,3]),'h':rng.randint(1,3),'k':rng.randint(1,3),'n':rng.choice([-1,1,2]),'left':rng.randint(-2,1),'bottom':rng.randint(-1,1),'c':rng.choice([-2,-1,1,2])}
        if family=='lens':
            # Cancellation coefficients also occur in noncancelling instances.
            p['a']=rng.choice([-4,-3,-2,-1,1,2,3,4])
            p['c']=rng.choice([-5,-2,-1,1,2,5])
        # Choose meaningful derivative sign/cancellation cases before remaining values.
        if case=='cancel':
            if family=='rectangle': p['b']=p['a']
            elif family=='triangle': p['a']=2*p['b']
            elif family=='legacy-wedge': p['a']=-2*p['b']
            elif family=='quadratic-wedge': p['h']=p['k'];p['b']=rng.choice([-1,1]);p['a']=-3*p['b']
            else:
                # For k=1, the two region moments have ratio 5:4.
                # 8x-10y integrates to zero without making the curl zero.
                sign=rng.choice([-1,1]);p['k']=1;p['c']=5*sign
                p['b']=rng.choice([2,3])*sign;p['a']=2*p['b']-8*sign
        d=instance(family,p)
        if case=='positive' and d['answer']<=0: continue
        if case=='negative' and d['answer']>=0: continue
        if case=='cancel' and d['answer']!=0: continue
        # Zero answers cannot use reversal profiles; a complete alternate error profile.
        try: r=render(d,difficulty,profile,rng.getrandbits(64),None)
        except ValueError: continue
        signature=json.dumps([family,str(d['py']),str(d['qx']),[str(d[t]) for t in ['low','up','lo','hi']]],sort_keys=True)
        if signature in seen: continue
        field=r['question'][':question/answer-fields'][0]
        errors=error_values(d)
        ordered=[s.simplify(v) for v in [d['answer']]+[errors[n] for n in PROFILES[profile]]]
        rank=sorted(ordered).index(d['answer'])
        magnitude_rank=sorted(ordered,key=lambda v:(abs(v),v)).index(d['answer'])
        position=next(i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1])
        previous=bank_cases[family]
        # Numeric magnitude is also visible without doing Green's theorem.
        # The first two banks must defeat every fixed absolute-value rank.
        if len(previous)==1 and (rank==previous[0][0] or position==previous[0][1] or magnitude_rank==previous[0][2]): continue
        if assets is not None:r=render(d,difficulty,profile,r['generation']['seed'],assets)
        seen.add(signature);r['generation']['selected_case']=case;records.append(r)
        quotas[family]-=1;bank_cases[family].append((rank,position,magnitude_rank))
    return records

def replay_sources():
    qs=json.loads((Path(__file__).with_name('source-replays.json')).read_text());records=[]
    for q in qs:
        q=copy.deepcopy(q)
        for key in [':question/problem',':question/worked-solution']: q[key]=normalize_prose(q[key])
        q[':question/difficulty']=ident(q.get(':question/difficulty',':question.difficulty/hard'))
        fields=q.get(':question/answer-fields',[])
        for f in fields:
            f.pop(':db/id',None);f[':answer-field/type']=ident(f[':answer-field/type'])
            correct=f[':answer-field/correct'];key=correct[':answer/id']
            f[':answer-field/correct']=[':answer/id',key]
            for a in f[':answer-field/choices']:
                a.pop(':db/id',None);a[':answer/type']=ident(a[':answer/type']);a[':answer/value']=normalize_tex(a[':answer/value'])
        q.pop(':db/id',None)
        r={'knowledge_point':{'db_id':KP,'id':KPID,'title':"Evaluating Line Integrals Using Green's Theorem"},'question':q,'generation':{'version':VERSION,'source_ids':[q.get(':question/math-academy-id',q[':question/id'])],'source_replay':True}}
        records.append(validate_generated_record(r))
    return records

# Preserve original explicit construction without the repository-relative interpreter/import fallback.
def generate(difficulty='hard',seed=0,parameters=None,**kwargs):
    if parameters is None:return sample(difficulty,seed,1,kwargs.get('output_dir'))[0]
    a=parameters['a'];p={'a':a,'b':0,'h':1,'k':2,'n':6}
    d=instance('legacy-wedge',p);d['P']=6*x*x-a*x*y+11;d['Q']=y*y+1
    return render(d,difficulty,'derivatives',seed,kwargs.get('output_dir'),[-d['answer']/4,d['answer'],-d['answer'],-d['answer']/2,d['answer']/2])

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='easy')
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json')
    ap.add_argument('--replay-source',action='store_true')
    args=ap.parse_args()
    if args.count<1:ap.error('--count must be positive')
    if args.replay_source:rs=replay_sources()
    else:
        output=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
        if not output:ap.error('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR must be set to a generated asset directory')
        rs=sample(args.difficulty,args.seed,args.count,output)
    print(json.dumps(rs,indent=2,ensure_ascii=False))
