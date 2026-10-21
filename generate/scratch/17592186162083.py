#!/usr/bin/env python3
"""Arc-length invariance: five source-faithful checkbox templates.

Each source solution is parameterized as a whole. New instances retain curve
families, statement roles, response fields, and the original solution stages.
Curve geometry, rather than seed, integral value, or speed, defines distinctness.
"""
import argparse, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
D=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((D/'source.json').read_text());KP=SNAPSHOT['record']
KP_ID=17592186162083;KP_UUID=KP[':knowledge-point/id'];VERSION='1.0.0'
NS=uuid.UUID(KP_UUID);GENERATOR_UUID=str(uuid.uuid5(NS,'arc-length-invariance-generator'))
LEVELS={'moderate':('q-122814','q-122815','q-122816'),'hard':('q-122851','q-122868')}
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions'] if q.get(':question/difficulty')}
CASES={'q-122814':dict(a=1,b=3,T=2,k=4),'q-122815':dict(R=1,d=2,n=1,k=1),'q-122816':dict(c=1,T=4,k=3),'q-122851':dict(h=1,L=1,a=3,b=2),'q-122868':dict(A=2,B=2,T=2,s=2)}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def tex(x):return sp.latex(sp.sympify(x)).replace(' ','')
def coef(x):return '' if x==1 else tex(x)
def replace(text,mapping):
    # Simultaneous longest-first replacements prevent cascading numeric edits.
    return re.sub('|'.join(re.escape(s) for s in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m[0]],text)
def render(profile,p):
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
    else:
        A,B,T,s=(p[z] for z in ('A','B','T','s'))
        m={r'⟨2t,\,2\sqrt{t}⟩':'⟨'+coef(A)+'t,\\,'+coef(B)+r'\sqrt{t}⟩',r'⟨4u,\,2\sqrt{2u}⟩':'⟨'+coef(A*s)+'u,\\,'+coef(B)+r'\sqrt{'+coef(s)+'u}⟩',r'0\le t\le 2':r'0\le t\le '+str(T),r'0\le u\le 1':r'0\le u\le '+tex(sp.Rational(T,s)),r'\text{d}s=2k':r'\text{d}s='+coef(s)+'k',r'y=\sqrt{2x}':r'y=\sqrt{'+coef(sp.Rational(B*B,A))+'x}',r'0\le x\le 4':r'0\le x\le '+str(A*T)}
    return replace(old[':question/problem'],m),replace(old[':question/worked-solution'],m)
def candidates(profile):
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
def generate(level,seed=0,profile=None,parameters=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty: '+level)
    rng=random.Random(seed);profile=profile or rng.choice(LEVELS[level]);assert profile in LEVELS[level]
    p=dict(parameters) if parameters is not None else rng.choice(list(candidates(profile)))
    assert set(p)==set(CASES[profile]) and all(isinstance(z,int) for z in p.values())
    assert all(z>0 for z in p.values())
    if profile=='q-122814':assert p['T']>1
    if profile=='q-122815':assert p['d']*p['n']>1
    if profile=='q-122816':assert p['T'] in (4,9,16)
    if profile=='q-122851':assert p['a']!=p['b']
    if profile=='q-122868':assert p['s']>1
    prompt,solution=render(profile,p)
    # Identity excludes seed. Geometry exclusion additionally ignores equivalent
    # speed changes and supplied integral values, so these cannot fill reserves.
    qid=str(uuid.uuid5(NS,digest([VERSION,level,profile,p])));fields=[]
    for old in SOURCES[profile][':question/answer-fields']:
        key=old[':answer-field/key'];fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+key));choices=[]
        for value in ('false','true'):
            aid=str(uuid.uuid5(uuid.UUID(fid),value));choices.append({':answer/id':aid,':answer/type':':answer.type/text',':answer/value':value})
        cv=old[':answer-field/correct'][':answer/value'];cid=next(a[':answer/id'] for a in choices if a[':answer/value']==cv)
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',cid]})
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':profile,'bank_profile':profile,'seed':seed,'parameters':p,'source_basis':SNAPSHOT['basis'],'source_question':SOURCES[profile][':db/id'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'assets':[]}}
def batch(level,count,seed=0):
    if level not in LEVELS:raise ValueError('Unsupported difficulty: '+level)
    pool=[(profile,p) for profile in LEVELS[level] for p in candidates(profile)];random.Random(seed).shuffle(pool)
    if count>len(pool):raise ValueError('Bounded variant limit')
    return [generate(level,seed,profile,p) for profile,p in pool[:count]]
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');a=ap.parse_args()
    records=batch(a.difficulty,a.count,a.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))
