#!/usr/bin/env python3
"""Arc-length invariance: seven source-faithful templates and authored easy calibration.

Each source solution is parameterized as a whole. New instances retain curve
families, statement roles, response fields, and the original solution stages.
Curve geometry, rather than seed, integral value, or speed, defines distinctness.
"""
import argparse, hashlib, importlib.util, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
D=Path(__file__).with_suffix('')
ROOT=Path(__file__).resolve().parents[2]
_format_spec=importlib.util.spec_from_file_location('arc_math_format',ROOT/'scripts/question_capture/math_format.py')
FORMAT=importlib.util.module_from_spec(_format_spec);_format_spec.loader.exec_module(FORMAT)
SNAPSHOT=json.loads((D/'source.json').read_text());KP=SNAPSHOT['record']
KP_ID=17592186162083;KP_UUID=KP[':knowledge-point/id'];VERSION='2.0.0-draft'
NS=uuid.UUID(KP_UUID)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
CASES={'q-122814':dict(a=1,b=3,T=2,k=4),'q-122815':dict(R=1,d=2,n=1,k=1),'q-122816':dict(c=1,T=4,k=3),'q-122851':dict(h=1,L=1,a=3,b=2),'q-122868':dict(A=2,B=2,T=2,s=2)}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def tex(x):return sp.latex(sp.sympify(x)).replace(' ','')
def coef(x):return '' if x==1 else tex(x)
def replace(text,mapping):
    # Simultaneous longest-first replacements prevent cascading numeric edits.
    return re.sub('|'.join(re.escape(s) for s in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m[0]],text)
def render_rated(profile,p):
    old=SOURCES[profile];m={}
    if profile=='q-122814':
        a,b,T,k=(p[z] for z in ('a','b','T','k'));s=T
        m={r'{t}^{4}-3{t}^{2}':coef(a)+r'{t}^{4}-'+coef(b)+r'{t}^{2}',r'16{u}^{4}-12{u}^{2}':coef(a*s**4)+r'{u}^{4}-'+coef(b*s**2)+r'{u}^{2}',r'2u':coef(s)+'u',r'0\le t\le 2':r'0\le t\le '+tex(T),r'{y}^{4}-3{y}^{2}':coef(a)+r'{y}^{4}-'+coef(b)+r'{y}^{2}',r'0\le y\le 2':r'0\le y\le '+tex(T),r'\text{d}s=-4':r'\text{d}s='+tex(-k),r'\text{d}s=4':r'\text{d}s='+tex(k),r'\text{d}s=8':r'\text{d}s='+tex(s*k)}
    elif profile=='q-122815':
        R,d,n,k=(p[z] for z in ('R','d','n','k'))
        arg=r'\frac{u}{'+str(d)+'}'
        m={r'\operatorname{cos}⁡(\frac{u}{2})':coef(R)+r'\operatorname{cos}⁡('+arg+')',r'\operatorname{sin}⁡(\frac{u}{2})':coef(R)+r'\operatorname{sin}⁡('+arg+')',r'\operatorname{cos}⁡t':coef(R)+r'\operatorname{cos}⁡'+coef(n)+'t',r'\operatorname{sin}⁡t':coef(R)+r'\operatorname{sin}⁡'+coef(n)+'t',r'0\le u\le 2\pi':r'0\le u\le '+coef(d)+r'\pi',r'0\le t\le \pi':r'0\le t\le '+tex(sp.pi/n),r'radius $1$':'radius $'+str(R)+'$',r'\text{d}s=-1':r'\text{d}s='+tex(-k),r'\text{d}s=1':r'\text{d}s='+tex(k),r'\text{d}s=2':r'\text{d}s='+tex(d*n*k)}
    elif profile=='q-122816':
        c,T,k=(p[z] for z in ('c','T','k'));s=T
        m={r'⟨t,\,{t}^{3/2}⟩':'⟨t,\\,'+coef(c)+r'{t}^{3/2}⟩',r'⟨4u,\,8{u}^{3/2}⟩':'⟨'+coef(s)+'u,\\,'+coef(c*sp.Integer(s)**sp.Rational(3,2))+r'{u}^{3/2}⟩',r'0\le t\le 4':r'0\le t\le '+str(T),r'y={x}^{3/2}':'y='+coef(c)+r'{x}^{3/2}',r'0\le x\le 4':r'0\le x\le '+str(T),r'\text{d}s=-3':r'\text{d}s='+tex(-k),r'\text{d}s=3':r'\text{d}s='+tex(k),r'\text{d}s=12':r'\text{d}s='+tex(T*k)}
    elif profile=='q-122851':
        h,L,a,b=(p[z] for z in ('h','L','a','b'));k=sp.Symbol('k')
        m={r'⟨\sqrt{9{t}^{2}+1},\,3t⟩':'⟨\\sqrt{'+coef(a*a)+r'{t}^{2}+'+str(h)+'},\\,'+coef(a)+'t⟩',r'⟨\sqrt{4{u}^{2}+1},\,2u⟩':'⟨\\sqrt{'+coef(b*b)+r'{u}^{2}+'+str(h)+'},\\,'+coef(b)+'u⟩',r'0\le t\le \frac{1}{3}':r'0\le t\le '+tex(sp.Rational(L,a)),r'0\le u\le \frac{1}{2}':r'0\le u\le '+tex(sp.Rational(L,b)),r'\frac{2k}{3}':tex(sp.Rational(b,a)*k),r'x=\sqrt{{y}^{2}+1}':r'x=\sqrt{{y}^{2}+'+str(h)+'}',r'0\le y\le 1':r'0\le y\le '+str(L)}
    elif profile=='q-122868':
        A,B,T,s=(p[z] for z in ('A','B','T','s'))
        m={r'⟨2t,\,2\sqrt{t}⟩':'⟨'+coef(A)+'t,\\,'+coef(B)+r'\sqrt{t}⟩',r'⟨4u,\,2\sqrt{2u}⟩':'⟨'+coef(A*s)+'u,\\,'+coef(B)+r'\sqrt{'+coef(s)+'u}⟩',r'0\le t\le 2':r'0\le t\le '+str(T),r'0\le u\le 1':r'0\le u\le '+tex(sp.Rational(T,s)),r'\text{d}s=2k':r'\text{d}s='+coef(s)+'k',r'y=\sqrt{2x}':r'y=\sqrt{'+coef(sp.Rational(B*B,A))+'x}',r'0\le x\le 4':r'0\le x\le '+str(A*T)}
    return replace(old[':question/problem'],m),replace(old.get(':question/worked-solution',''),m)
def candidates_rated(profile):
    if profile=='q-122814':
        for a,b,T in itertools.product(range(1,4),range(1,7),range(2,7)):yield dict(a=a,b=b,T=T,k=(a+b+T)%8+1)
    elif profile=='q-122815':
        for R in range(1,9):yield dict(R=R,d=2+R%3,n=1+R%3,k=R+1)
    elif profile=='q-122816':
        for c,T in itertools.product(range(1,6),(4,9,16)):yield dict(c=c,T=T,k=c+T//4)
    elif profile=='q-122851':
        for h,L in itertools.product(range(1,10),range(1,6)):yield dict(h=h,L=L,a=2+(h%4),b=2+((h+1)%4))
    else:
        for A,B,T in itertools.product(range(2,7),range(2,7),range(2,6)):yield dict(A=A,B=B,T=T,s=2+(A+B+T)%4)

# Separate unrated historical radio templates. Raw profiles omit absent fields.
CASES.update({'q-122478':dict(c=1,T=1,s=2,k=2),'q-122571':dict(R=1,s=2)})
LEVELS={'easy':('q-122478',),'moderate':('q-122814','q-122815','q-122816','q-122571'),'hard':('q-122851','q-122868')}

def render(profile,p):
    if profile not in ('q-122478','q-122571'):return render_rated(profile,p)
    if profile=='q-122478':
        c,T,s,k=(p[z] for z in ('c','T','s','k'))
        m={r'⟨t, t^{2}⟩':'⟨t, '+coef(c)+r't^{2}⟩',r'⟨2u, 4u^{2}⟩':'⟨'+coef(s)+'u, '+coef(c*s*s)+r'u^{2}⟩',r'0 \le t \le 1':r'0 \le t \le '+tex(T),r'0 \le u \le \frac{1}{2}':r'0 \le u \le '+tex(sp.Rational(T,s)),r'ds =-2':r'ds ='+tex(-k),r'ds = 2':r'ds = '+tex(k),r'ds = 4':r'ds = '+tex(s*k)}
    else:
        R,s=(p[z] for z in ('R','s'))
        m={r'⟨\sin t, \cos t⟩':'⟨'+coef(R)+r'\sin t, '+coef(R)+r'\cos t⟩',r'⟨\sin 2θ, \cos 2θ⟩':'⟨'+coef(R)+r'\sin '+coef(s)+'θ, '+coef(R)+r'\cos '+coef(s)+'θ⟩',r'0 \le θ \le π':r'0 \le θ \le '+('π' if s==2 else tex(2*sp.pi/s)),r'\frac{1}{2}k':r'\frac{1}{'+str(s)+'}k'}
    return replace(SOURCES[profile][':question/problem'],m),''


def legacy_solution(profile,p):
    """Authored completion using the observed shared prose and operative stages."""
    exemplar=SOURCES['q-122814'][':question/worked-solution']
    if profile=='q-122478':
        c,T,k=p['c'],p['T'],p['k']
        sol=replace(exemplar,{'Statement I is false, while statement III is true.':'Statement I is false, while statement II is true.','Statement II is false.':'Statement III is false.',r'=4':r'='+tex(k),r'x={y}^{4}-3{y}^{2},\,0\le y\le 2.':r'y='+coef(c)+r'{x}^{2},\,0\le x\le '+tex(T)+'.','"III only."':'"II only."'})
        return sol
    # Full circle has the same invariant and orientation steps, with a locus argument.
    sol=SOURCES['q-122815'][':question/worked-solution']
    sol=replace(sol,{'Statement I is false.':'Statement II is true, while statement III is false.','Statement II is false, while statement III is true.':'Statement I is true.',r'=1.':r'=k.','a half-circle of radius $1$':'a circle of radius $'+tex(p['R'])+'$',r'between $0$ and $\pi .$':r'between $0$ and $2\pi .$','"III only."':'"I and II only."'})
    return sol


def candidates(profile):
    if profile=='q-122478':
        for c,T,s,k in itertools.product(range(1,7),range(1,5),range(2,6),(-7,-3,2,5)):
            yield dict(c=c,T=T,s=s,k=k)
    elif profile=='q-122571':
        for R,s in itertools.product(range(1,13),range(2,6)):yield dict(R=R,s=s)
    elif profile=='q-122815':
        for R,d,n,k in itertools.product(range(1,13),range(2,5),range(1,4),(-5,1,4)):
            yield dict(R=R,d=d,n=n,k=k)
    else:yield from candidates_rated(profile)


def guard(profile,p):
    if set(p)!=set(CASES[profile]) or not all(type(v) is int for v in p.values()):raise ValueError('Exact integer parameter slots required')
    bounds={'q-122478':dict(c=(1,6),T=(1,4),s=(2,5),k=(-9,9)),
      'q-122571':dict(R=(1,12),s=(2,5)),
      'q-122814':dict(a=(1,3),b=(1,6),T=(2,6),k=(-9,9)),
      'q-122815':dict(R=(1,12),d=(2,4),n=(1,3),k=(-9,9)),
      'q-122816':dict(c=(1,5),T=(4,16),k=(-9,9)),
      'q-122851':dict(h=(1,9),L=(1,5),a=(2,5),b=(2,5)),
      'q-122868':dict(A=(2,6),B=(2,6),T=(2,5),s=(2,5))}[profile]
    if any(not lo<=p[key]<=hi for key,(lo,hi) in bounds.items()):raise ValueError('Parameter outside family workload bounds')
    if 'k' in p and p['k']==0:raise ValueError('Numeric bank requires nonzero integral')
    if profile=='q-122816' and p['T'] not in (4,9,16):raise ValueError('Perfect-square endpoint required')
    if profile=='q-122851' and p['a']==p['b']:raise ValueError('Distinct speeds required')


def mathematical_fingerprint(profile,p):
    """Canonical curve and requested invariance relations, excluding speed/k magnitude."""
    z=sp.Symbol('z',nonnegative=True)
    if profile=='q-122478':v=[p['T']*z,p['c']*p['T']**2*z**2]
    elif profile=='q-122571':v=[p['R']*sp.sin(2*sp.pi*z),p['R']*sp.cos(2*sp.pi*z)]
    elif profile=='q-122814':v=[p['a']*p['T']**4*z**4-p['b']*p['T']**2*z**2,p['T']*z]
    elif profile=='q-122815':v=[p['R']*sp.cos(sp.pi*z),p['R']*sp.sin(sp.pi*z)]
    elif profile=='q-122816':v=[p['T']*z,p['c']*(p['T']*z)**sp.Rational(3,2)]
    elif profile=='q-122851':v=[sp.sqrt((p['L']*z)**2+p['h']),p['L']*z]
    else:v=[p['A']*p['T']*z,p['B']*sp.sqrt(p['T']*z)]
    roles={'q-122478':('reverse-negative','reverse-same','reparam-scaled'),'q-122571':('reverse-same','reparam-same','reparam-scaled'),'q-122814':('reverse-negative','reparam-scaled','reverse-same'),'q-122815':('reparam-scaled','reverse-negative','reverse-same'),'q-122816':('reverse-same','reverse-negative','reparam-scaled'),'q-122851':('reverse-negative','reparam-scaled','reparam-same'),'q-122868':('reparam-same','reparam-scaled','reverse-same')}
    return digest({'curve':[sp.srepr(sp.simplify(c)) for c in v],'relations':sorted(roles[profile])})


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty')
    raw=bool(profile and profile.startswith('raw:'))
    chosen=profile.removeprefix('raw:') if profile else template
    rng=random.Random(seed)
    chosen=chosen or rng.choice(LEVELS[level]) # Complete Boolean/radio bank selected before parameters.
    if chosen not in SOURCES or (template is not None and template!=chosen):raise ValueError('Unknown or incompatible template/profile')
    supported=chosen in LEVELS[level] or (chosen=='q-122571' and level=='moderate')
    if not supported:raise ValueError('Template outside difficulty scope')
    p=dict(parameters) if parameters is not None else rng.choice(list(candidates(chosen)))
    guard(chosen,p)
    source=SOURCES[chosen];prompt,solution=render(chosen,p)
    if not raw and chosen in ('q-122478','q-122571'):
        solution=legacy_solution(chosen,p)
        if chosen=='q-122571':
            prompt=prompt.replace(r'\begin{bmatrix}',r'\begin{aligned}').replace(r'\end{bmatrix}',r'\end{aligned}').replace('|=',' &=')
    typ=source[':question/answer-fields'][0][':answer-field/type'][':db/ident']
    if field_type and field_type not in (typ,typ.split('/')[-1]):raise ValueError('Field type conflicts with source contract')
    q={':question/problem':prompt}
    if ':question/worked-solution' in source or not raw:q[':question/worked-solution']=solution
    if ':question/difficulty' in source or not raw:q[':question/difficulty']=':question.difficulty/'+level
    field_specs=[]
    for old in source.get(':question/answer-fields',[]):
        f={':answer-field/key':old[':answer-field/key'],':answer-field/type':old[':answer-field/type'][':db/ident'],':answer-field/choices':[ {':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value'],**({':answer/feedback':a[':answer/feedback']} if ':answer/feedback' in a else {})} for a in old[':answer-field/choices']]}
        if ':answer-field/correct' in old:f['correct_value']=old[':answer-field/correct'][':answer/value']
        elif not raw:f['correct_value']='II only' if chosen=='q-122478' else 'I and II only'
        field_specs.append(f)
    if not raw:
        for key in (':question/problem',':question/worked-solution'):q[key]=FORMAT.normalize_prose(q[key])
    identity=digest({'version':VERSION,'question':q,'fields':[{**f,':answer-field/choices':sorted(f[':answer-field/choices'],key=lambda a:json.dumps(a,sort_keys=True))} for f in field_specs]})
    qid=str(uuid.uuid5(NS,identity));q[':question/id']=qid;fields=[]
    for f in field_specs:
        fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+f[':answer-field/key']));f[':answer-field/id']=fid
        for a in f[':answer-field/choices']:a[':answer/id']=str(uuid.uuid5(uuid.UUID(fid),digest(a)))
        if 'correct_value' in f:
            cv=f.pop('correct_value');f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==cv)]
        rng.shuffle(f[':answer-field/choices']);fields.append(f)
    if ':question/answer-fields' in source:q[':question/answer-fields']=fields
    result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':chosen,'bank_profile':('raw:' if raw else '')+chosen,'seed':seed,'parameters':p,'source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'source_question':source[':db/id'],'source_math_academy_id':chosen,'evidence_only':raw,'eligible_for_learning':not raw,'authored_completion':not raw and chosen in ('q-122478','q-122571'),'mathematical_fingerprint':mathematical_fingerprint(chosen,p),'content_fingerprint':identity,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'assets':[]}}
    if not raw:FORMAT.validate_generated_record(result)
    return result

# Difficulty entry points. Easy is an authored calibration, not a recovered label.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def batch(level,count,seed=0,template=None,profile=None):
    chosen=profile.removeprefix('raw:') if profile else template
    pool=[(family,p) for family in ([chosen] if chosen else LEVELS[level]) for p in candidates(family)]
    random.Random(seed).shuffle(pool);out=[];seen=set()
    for family,p in pool:
        r=generate(level,seed,template=family,profile=profile,parameters=p)
        fp=r['generation']['mathematical_fingerprint']
        if fp not in seen:out.append(r);seen.add(fp)
        if len(out)==count:return out
    raise ValueError('Requested count exceeds finite meaningful bank')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    records=[r for level in (LEVELS if a.difficulty=='all' else [a.difficulty]) for r in batch(level,a.count,a.seed,a.template,a.profile)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'].get(':question/worked-solution','') for r in records))
