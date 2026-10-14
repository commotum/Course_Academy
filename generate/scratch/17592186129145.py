#!/usr/bin/env python3
"""Graph → factored polynomial radio generator, frozen math basis 1356.

Observed families preserve their complete root/multiplicity banks and shared
solution stages. Affine horizontal maps and positive vertical scales are the
variable slots; exact anchors are ordinary parameter values, not source-payload
branches. Hard is authored: four roots including a simple, an even multiple and
an odd multiple root, using the same ordered graph-reading method.

Public replay profiles retain original factor typography. Decoded source math
contains single TeX command backslashes; JSON escaping needs no source repair.
No DB writes. See adjoining extraction and validation evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid, os, tempfile
from pathlib import Path
import sympy as sp
import numpy as np
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186129145-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

KP_ID=17592186129145
TITLE='Identifying the Factored Polynomial Shown in a Graph'
KP_UUID='4fc09a0f-34d3-5ca9-9964-6cb00498bfa7'
VERSION='graph-factored-polynomial-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X=sp.Symbol('x')

# Profile is selected as a WHOLE before parameters. Each factor is a complete
# mathematical slot, including distractor-only roots and extra factors.
DATA={
'q-38668':('easy',[-1,0,1],[1,1,1],'-1'),
'q-38671':('easy',[-3,-1,2],[1,2,1],'1'),
'q-38763':('easy',[-2,-1,2],[1,2,1],'1/4'),
'q-38765':('easy',[-1,1,2,3],[2,1,1,1],'1'),
'q-112595':('moderate',[-3,0,2],[1,2,4],'-1/10'),
'q-112596':('moderate',[-2,0,3],[1,3,1],'1/5'),
'q-38774':('easy',[-2,-1,2],[2,1,2],'1/10'),
'q-80348':('moderate',[-1,0,2],[1,3,3],'1'),
'q-80350':('moderate',[-1,2,5],[1,5,1],'1'),
'q-80352':('moderate',[-2,0,1],[3,1,3],'-1'),
'hard-mixed':('hard',[-4,-1,1,4],[1,2,3,1],'1/20'),
'hard-even-right':('hard',[-4,-2,1,3],[3,1,1,2],'1/20'),
'hard-odd-right':('hard',[-3,-1,2,4],[2,1,1,3],'-1/20'),
'hard-even-left':('hard',[-3,-2,1,4],[2,3,1,1],'-1/20'),
}
RAW_COLLISION_PROFILES={'q-38671','q-38774'}
for _base in RAW_COLLISION_PROFILES: DATA[_base+'-authored']=DATA[_base]

def normalize(t):
    return t.replace('\\\\frac','\\frac')

def parse_polynomial(value):
    """Independent strict parser of displayed factored polynomial math."""
    s=normalize(value).replace(' ','').split('=')[-1]
    s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
    s=s.replace('{','').replace('}','')
    if s.startswith('-') and not re.match(r'-\d',s): s='-1'+s[1:]
    tokens=re.findall(r'\(-?\d+/\d+\)|\(x[+-]\d+\)|x|\^\d+|[+-]?\d+',s)
    if ''.join(tokens)!=s: raise ValueError('Unsupported displayed polynomial: '+repr(value))
    out=sp.Integer(1);i=0
    while i<len(tokens):
        z=tokens[i];i+=1
        if z=='x': f=X
        elif z.startswith('(x'): f=sp.sympify(z[1:-1])
        elif z.startswith('('): f=sp.Rational(z[1:-1])
        elif z=='-1': f=sp.Integer(-1)
        else: f=sp.Rational(z)
        if i<len(tokens) and tokens[i].startswith('^'): f=f**int(tokens[i][1:]);i+=1
        out*=f
    return sp.Poly(sp.expand(out),X)

def factor_spec(value):
    p=parse_polynomial(value);c,f=sp.factor_list(p.as_expr(),X)
    roots=[]
    for z,m in f:
        if sp.degree(z,X)!=1: raise ValueError('Nonlinear factor')
        roots.append((sp.solve(z,X)[0],m))
    return str(c),sorted(roots)

def polynomial(c,roots,mults):
    return sp.Poly(sp.Rational(c)*sp.prod((X-r)**m for r,m in zip(roots,mults)),X)

def tex_factor(r,m):
    z='x' if r==0 else '(x'+('+'+str(-r) if r<0 else '-'+str(r))+')'
    return z if m==1 else z+'^{'+str(m)+'}'

def equation(c,roots,mults):
    c=sp.Rational(c)
    prefix='' if c==1 else '-' if c==-1 else sp.latex(c)
    # x first is the course convention, then ascending nonzero roots.
    order=sorted(range(len(roots)),key=lambda i:(roots[i]!=0,roots[i]))
    return 'y='+prefix+''.join(tex_factor(roots[i],mults[i]) for i in order)

def source_pattern(value,h,s,v):
    """Tokenize source factor slots; never replace fragments across prose."""
    value=normalize(value)
    c,rr=factor_spec(value)
    # Preserve source typography at every parameter set with complete factor masks.
    rhs=value.split('=')[1]
    # Coefficient and factor spelling are read once into full structural slots.
    factors=re.findall(r'\{?\(?x(?:\s*[+-]\s*\d+)?\)?(?:\{\))?\}?(?:\s*\^\{?\d+\}?)?',rhs)
    # Use the exact source equation only as a reusable typography mask.
    pat=r'(?:\{?\(x\s*([+-])\s*(\d+)(?:\{\))?\)?\}?(?:\^\{?(\d+)\}?)?|\{?x\}?(?:\^\{?(\d+)\}?)?)'
    matches=list(re.finditer(pat,rhs))
    if not matches: raise ValueError(value)
    first=matches[0].start();prefix=rhs[:first]
    coeff=sp.Rational(c)*sp.Rational(v)
    cp=prefix if sp.Rational(v)==1 else ('' if coeff==1 else '-' if coeff==-1 else sp.latex(coeff))
    pieces=[]
    for a in matches:
        sign,n,m,mx=a.groups();r=(-int(n) if sign=='+' else int(n)) if n else 0
        nr=s*r+h; mult=int(m or mx or 1)
        original=a.group()
        if nr==r: z=original
        else: z=tex_factor(nr,mult)
        pieces.append(z)
    return value.split('=')[0]+'='+cp+''.join(pieces)

def category(m): return 'simple' if m==1 else 'even' if m%2==0 else 'odd-multiple'

def authored_solution(roots,mults,ans):
    n={3:'three',4:'four'}[len(roots)]
    text='First, we notice that the function has precisely '+n+' distinct roots, '+', '.join('$x='+str(r)+'$' for r in roots[:-1])+', and $x='+str(roots[-1])+'.$\n\nBased on the graph, we can make the following conclusions about the multiplicities of the roots:'
    for r,m in zip(roots,mults):
        if m==1: sentence=f'Since the graph is *not* tangent to the $x$-axis at $x={r},$ this root is a simple root (the multiplicity equals $1$).'
        elif m%2==0: sentence=f'Since the graph just touches the $x$-axis and reverses direction at $x={r},$ this root has even multiplicity.'
        else: sentence=f'Since the graph passes through $x={r},$ this root has odd multiplicity, and since the graph is tangent to the $x$-axis at $x={r},$ the multiplicity must be greater than one.'
        text+='\n\n- '+sentence
    return text+'\n\nFrom the given options, the only possible equation is $'+ans+'.$'

def source_solution(sid,h,s,v,ans):
    q=QS[sid];text=q.get(':question/worked-solution')
    if not text: return authored_solution([s*r+h for r in DATA[sid][1]],DATA[sid][2],ans)
    # Complete x=value references, including several in one inline span.
    text=re.sub(r'x\s*=\s*(-?\d+)',lambda a:'x='+str(s*int(a.group(1))+h),text)
    # Preserve source final factor typography and operative stages.
    text=re.sub(r'\$y=.*?\$',lambda _: '$'+ans+'.$',text)
    return text

def bank(sid,h,s,v):
    level,roots,mults,c=DATA[sid]
    authored=sid.endswith('-authored');base=sid.removesuffix('-authored')
    roots=[s*r+h for r in roots];coeff=sp.Rational(c)*sp.Rational(v)
    correct=equation(coeff,roots,mults)
    fields=[] if authored else QS.get(base,{}).get(':question/answer-fields',[])
    if fields:
        choices=fields[0][':answer-field/choices']
        values=[source_pattern(a[':answer/value'],h,s,v) for a in choices]
        ci=next((i for i,a in enumerate(choices) if a[':answer/id']==fields[0].get(':answer-field/correct',{}).get(':answer/id')),None)
        if ci is None:
            ci=next(i for i,z in enumerate(values) if parse_polynomial(z)==polynomial(coeff,roots,mults))
        correct=values[ci]
    else:
        # Authored complete bank: sign inversion, flattening mistake, root shift,
        # and parity reversal. No individual fallback replacement is permitted.
        m1=list(mults);j=next(i for i,m in enumerate(m1) if m>1);m1[j]=1
        m2=list(mults);m2[j]+=1
        r2=list(roots);r2[0]-=s
        values=[correct,equation(-coeff,roots,mults),equation(coeff,roots,m1),equation(coeff,r2,mults),equation(coeff,roots,m2)];ci=0
    polys=[parse_polynomial(z) for z in values]
    if len(set(str(z.as_expr()) for z in polys))!=5: raise ValueError('Whole bank collision')
    # The graph only identifies simple/even/odd-multiple and leading sign; do
    # not imply it determines the precise even exponent or vertical magnitude.
    target=(tuple(zip(roots,map(category,mults))),sp.sign(coeff))
    compat=[];signatures=[]
    for z in values:
        cc,rr=factor_spec(z)
        signature=(tuple((int(r),category(m)) for r,m in rr),sp.sign(sp.Rational(cc)))
        signatures.append(signature);compat.append(signature==target)
    if sum(compat)!=1 or not compat[ci]: raise ValueError('Graph-compatible bank ambiguity')
    if len(set(signatures))!=len(signatures) and sid not in RAW_COLLISION_PROFILES: raise ValueError('Whole graphical bank collision')
    return roots,mults,coeff,values,ci

def render_plot(roots,mults,c):
    spec={'roots':roots,'multiplicities':mults,'coefficient':str(c),'renderer':matplotlib.__version__,'version':VERSION}
    key=hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()[:24]
    out=HERE/'plots';out.mkdir(exist_ok=True);dest=out/(key+'.png');side=out/(key+'.json')
    if dest.exists() and side.exists(): return str(dest.resolve()),json.loads(side.read_text())
    poly=polynomial(c,roots,mults);f=sp.lambdify(X,poly.as_expr(),'numpy')
    lo=min(min(roots)-.8,0-.7);hi=max(max(roots)+.8,0+.7)
    critical=sorted(float(sp.re(z)) for z in sp.nroots(sp.diff(poly.as_expr(),X),maxsteps=300) if abs(float(sp.im(z)))<1e-8) if False else []
    # Derivative factors remove repeated roots before numeric solving.
    d=sp.Poly(sp.diff(poly.as_expr(),X),X).sqf_part()
    critical=[float(sp.re(z)) for z in sp.nroots(d,maxsteps=300) if abs(float(sp.im(z)))<1e-8 and lo<float(sp.re(z))<hi]
    ys=[float(f(z)) for z in critical]+[0.0]
    ymin=min(ys);ymax=max(ys);span=max(ymax-ymin,1)
    ymin-=span*.22;ymax+=span*.22
    xx=np.sort(np.unique(np.concatenate([np.linspace(lo,hi,10001),np.array(roots),np.array(critical)])))
    yy=f(xx)
    fig,ax=plt.subplots(figsize=(6.8,5.4),dpi=150)
    fig.subplots_adjust(left=.06,right=.94,bottom=.1,top=.94)
    ax.set_xlim(lo,hi);ax.set_ylim(ymin,ymax)
    for k in ('left','bottom'): ax.spines[k].set_position(('data',0));ax.spines[k].set_linewidth(1.1)
    for k in ('right','top'): ax.spines[k].set_visible(False)
    ax.set_xticks([r for r in roots if r]);ax.set_yticks([])
    ax.tick_params(axis='x',labelsize=12,pad=6)
    ax.plot(xx,yy,color='#e51b23',linewidth=2.0,zorder=3)
    ax.annotate('',xy=(hi,0),xytext=(hi-.15,0),arrowprops={'arrowstyle':'->','color':'black'})
    ax.annotate('',xy=(0,ymax),xytext=(0,ymax-.06*(ymax-ymin)),arrowprops={'arrowstyle':'->','color':'black'})
    # Source root zero is unlabelled because it coincides with the vertical axis.
    fig.canvas.draw();points=[]
    for z in [(roots[i]+roots[i+1])/2 for i in range(len(roots)-1)]+critical:
        px,py=ax.transData.transform((z,float(f(z))));points.append({'x':z,'y':float(f(z)),'pixel':[float(px),float(fig.bbox.height-py)]})
    spec.update({'xlim':[lo,hi],'ylim':[ymin,ymax],'zero_pixel':list(map(float,ax.transData.transform((0,0)))),'width':int(fig.bbox.width),'height':int(fig.bbox.height),'raster_points':points,'critical':critical})
    fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.png',dir=out);os.close(fd)
    fig.savefig(tmp);plt.close(fig);os.replace(tmp,dest)
    fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.json',dir=out);os.close(fd);Path(tmp).write_text(json.dumps(spec,indent=2));os.replace(tmp,side)
    return str(dest.resolve()),spec

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('radio only')
    rng=random.Random(seed)
    eligible=[k for k,v in DATA.items() if v[0]==level and k not in RAW_COLLISION_PROFILES]
    replay=[k for k,v in DATA.items() if v[0]==level]
    sid=profile or template or rng.choice(eligible)
    if sid not in replay or template not in (None,sid,'graph-to-polynomial'): raise ValueError('profile/template level mismatch')
    if parameters is None: p={'h':rng.randint(-3,3),'s':rng.choice([1,2]) if level!='hard' else 1,'v':rng.choice(['1','2','1/2'])}
    else: p=dict(parameters)
    if set(p)!={'h','s','v'} or type(p['h'])!=int or type(p['s'])!=int or abs(p['h'])>3 or p['s'] not in ([1] if level=='hard' else [1,2]) or sp.Rational(p['v']) not in (sp.Rational(1,2),sp.Integer(1),sp.Integer(2)): raise ValueError('same-level parameter bounds')
    h,s,v=p['h'],p['s'],str(sp.Rational(p['v']));p['v']=v
    roots,mults,c,values,ci=bank(sid,h,s,v)
    imagepath,plot=render_plot(roots,mults,c)
    prompt='![]('+imagepath+')\n\nWhich of the following could be the equation of the polynomial curve shown above?'
    base=sid.removesuffix('-authored')
    solution=source_solution(base,h,s,v,values[ci]) if base in QS else authored_solution(roots,mults,values[ci])
    identity={'version':VERSION,'difficulty':level,'prompt':prompt,'solution':solution,'bank':sorted(values)}
    digest=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    qid=str(uuid.uuid5(uuid.NAMESPACE_URL,digest));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(parse_polynomial(z).as_expr()))),':answer/type':':answer.type/math',':answer/value':z} for z in values]
    correctid=answers[ci][':answer/id'];rng.shuffle(answers)
    mathkey={'roots':roots,'categories':list(map(category,mults)),'leading_sign':int(sp.sign(c)),'assessed_information':'unscaled graph local root behavior'}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]}]},'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid,'parameters':p,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[base] if base in QS else [],'raw_graphical_pair_collision':sid in RAW_COLLISION_PROFILES,'eligible_default':sid not in RAW_COLLISION_PROFILES,'authored_bank':sid.endswith('-authored') or sid in ('q-38763','q-38765') or level=='hard','authored_hard':level=='hard','authored_field':sid in ('q-38763','q-38765'),'inferred_missing_key':sid=='q-38668','math_fingerprint':hashlib.sha256(json.dumps(mathkey,sort_keys=True).encode()).hexdigest(),'math_task':mathkey,'plot':plot,'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
