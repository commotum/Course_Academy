"""Source-faithful, bounded vector coefficient question generator.

Three backbones: c*a1+s*a2=b; a1-s*a2=b; c*a1+s*a2=0
with component consistency checking. Each source bank is a separate profile.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from vector_notation import vector_prose, plain_vector_prose
KP_ID=17592186119805
KP_UUID='33586620-e110-5a37-874f-a92103c5e9fb'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'linear-combination-coefficient-generator-v1'))
VERSION='1.2.0-notation-v1'
SOURCE=json.loads(Path(__file__).with_name('source-data.json').read_text())
PROFILES={q[':question/math-academy-id']:q for q in SOURCE['questions'] if q.get(':question/difficulty')}
LEVELS={level:tuple(sid for sid,q in PROFILES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+level)) for level in ('easy','moderate')}
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def vectors(text):return [list(map(int,re.split(r'\\\\',m))) for m in MAT.findall(text)]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def tex(x):return sp.latex(sp.Rational(x))
def vec(v):return r'\begin{bmatrix}'+r' \\ '.join(map(str,v))+r'\end{bmatrix}'
def original(sid):
    q=PROFILES[sid];a,u,*b=vectors(q[':question/problem']);letter=re.search(r'Find \$([a-z])',q[':question/problem'])[1]
    c=int(re.search(r'if \$(\d+)',q[':question/problem'])[1]) if sid!='q-34241' else 1
    s=int(q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']) if q[':question/difficulty'][':db/ident'].endswith('/easy') else None
    return {'a':a,'u':u,'c':c,'s':s,'letter':letter}
CASES={sid:original(sid) for sid in PROFILES}
# Hard is an authored composition of observed isolation and consistency methods.
LEVELS['hard']=tuple('hard:'+sid for sid in LEVELS['moderate'])
for sid in LEVELS['hard']:
    PROFILES[sid]=PROFILES[sid[5:]]
    CASES[sid]=CASES[sid[5:]]
def scalar(value):
    value=str(value).replace('\\\\frac','\\frac').replace(' ', '')
    m=re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}',value)
    return (-1 if m[1] else 1)*sp.Rational(int(m[2]),int(m[3])) if m else sp.Rational(value)

def source_bank(sid):
    return [a[':answer/value'] if a[':answer/value']=='No solution' else tex(scalar(a[':answer/value'])) for a in PROFILES[sid][':question/answer-fields'][0][':answer-field/choices']]

def values(sid,p,correct=None):
    if 'bank' in p:
        return [v if v=='No solution' else tex(scalar(v)) for v in p['bank']]
    bank=source_bank(sid)
    if correct is not None and correct not in bank:
        # Explicit non-source parameter paths retain five choices and the text option.
        index=next(i for i,v in enumerate(bank) if v!='No solution')
        bank[index]=correct
    return bank

def data(sid,p):
    a=sp.Matrix(p['a']);u=sp.Matrix(p['u']);c=p['c'];s=p['s'];moderate=sid in LEVELS['moderate'];minus=p.get('minus',sid=='q-34241')
    if not (len(a)==len(u) and (2<=len(a)<=4 if sid.startswith('hard:') else len(a)==len(CASES[sid]['a'])) and any(u)):
        raise ValueError('Equal source dimensions and a nonzero unknown vector required')
    if not (type(c) is int and c>0 and all(type(x)is int for x in p['a']+p['u']) and re.fullmatch('[a-z]',p['letter'])):
        raise ValueError('Integer vector entries, positive coefficient and scalar label required')
    if minus and not sid.startswith('hard:') and c!=1:
        raise ValueError('Subtraction profile displays a1 - scalar*a2, so c must equal 1')
    if moderate:
        b=sp.zeros(len(a),1)
    else:
        if s is None:raise ValueError('Explicit-target profile requires a scalar')
        s=scalar(s);b=sp.Matrix(p['b']) if 'b' in p else c*a+(-s if minus else s)*u
        if any(x.q!=1 for x in b):raise ValueError('Keep integer displayed vector entries')
    r=c*a-b if minus else b-c*a
    pivot=next(i for i,x in enumerate(u) if x)
    t=sp.Rational(r[pivot],u[pivot])
    correct=tex(t) if t*u==r else 'No solution'
    bank=values(sid,p,correct)
    if not (len(bank)==5 and len(set(bank))==5 and bank.count(correct)==1):
        raise ValueError('Five distinct choices with exactly one mathematically correct choice required')
    return a,u,b,r,t,correct,bank

def render(sid,p):
    a,u,b,r,t,correct,bank=data(sid,p);c=p['c'];letter=p['letter'];minus=p.get('minus',sid=='q-34241');moderate=sid in LEVELS['moderate']
    av,uv,bv,rv=map(lambda m:vec(list(m)),(a,u,b,r))
    eq=((str(c) if c!=1 else '')+r'{a}_{1}-'+letter+r'{a}_{2}=b') if minus else str(c)+r'{a}_{1}+'+letter+r'{a}_{2}='+('0' if moderate else 'b')
    problem=f'Find ${letter}$, if ${eq}$ and\n\n$$\n'+r'{a}_{1}='+av+r',\,{a}_{2}='+uv+('' if moderate else r',\,b='+bv)+'.\n$$'
    first=((str(c) if c!=1 else '')+av+'-'+letter+uv) if minus else str(c)+av+'+'+letter+uv
    difference=((str(c) if c!=1 else '')+av+'-'+bv) if minus else bv+'-'+str(c)+av
    sol=f'Using the properties of addition/subtraction and scalar multiplication of vectors to isolate the ${letter}$ term, we get\n\n$$\n'+r'\begin{aligned}'+eq.replace('=',' & =')+r' \\ '+first+' & ='+bv+r' \\ '+letter+uv+' & ='+difference+r' \\ '+letter+uv+' & ='+rv+r'.\end{aligned}'+'\n$$\n\n'
    if correct=='No solution':
        pivot=next(i for i,x in enumerate(u) if x)
        component=('first','second','third','fourth')[pivot]
        sol+='Equating the '+component+' components, we get\n\n$$\n'+str(u[pivot])+letter+'='+str(r[pivot])+r'\,⟹\,'+letter+'='+tex(t)+'.\n$$\n\nBut then\n\n$$\n'+r'\begin{aligned}'+tex(t)+uv+'='+vec(list(t*u))+r'\ne '+rv+r'.\end{aligned}'+'\n$$\n\nTherefore, there is no $'+letter+'$ such that $'+eq+'.$'
    else:
        sol+='From the final equation above, we can tell that $'+letter+'='+correct+'.$'
        if moderate or sid.startswith('hard:'):sol+=' This value satisfies every component.'
    return vector_prose(problem),vector_prose(sol),correct,bank

def fingerprint(q):
    text=plain_vector_prose(q[':question/problem']);a,u,*bs=vectors(text)
    minus=bool(re.search(r'\{a\}_\{1\}-[a-z]',text))
    match=re.search(r'if \$(\d+)',text);c=int(match[1]) if match else 1
    b=bs[0] if bs else [0]*len(a)
    # Ignore letters, bank, seeds, identities, coordinate ordering and common scaling.
    rows=sorted(zip(a,u,b));flat=[x for row in rows for x in row];pivot=next((x for x in flat if x),1)
    normalized=sorted(tuple(str(sp.Rational(x,pivot)) for x in row) for row in rows)
    return digest([c,-1 if minus else 1,normalized])

def generate(difficulty='easy',seed=0,profile=None,parameters=None):
    if difficulty not in LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed);sid=profile or rng.choice(LEVELS[difficulty]);assert sid in LEVELS[difficulty]
    p=parameters if parameters is not None else sample_parameters(sid,rng)
    problem,solution,correct,bank=render(sid,p)
    # Same mathematical task/profile always has the same field-owned identities.
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),json.dumps([VERSION,sid,p,bank],sort_keys=True)))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/text' if value=='No solution' else ':answer.type/math',':answer/value':value} for value in bank]
    f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]}
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[f]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Solving for One Coefficient in a Linear Combination'},'question':q,'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'parameters':p,'template':('signed-consistency-minus' if p.get('minus') else 'signed-consistency-plus') if difficulty=='hard' else 'homogeneous-coefficient' if difficulty=='moderate' else 'subtract' if sid=='q-34241' else 'unique-coefficient','bank_profile':sid,'bank_policy':'independent-role-extension' if 'bank' in p else 'source-replay-or-explicit','source_question_id':PROFILES[sid][':question/id'],'source_basis':SOURCE['basis'],'dependencies':{'sympy':sp.__version__},'assets':[],'parameter_fingerprint':fingerprint(q)}}

def sample_parameters(sid,rng):
    # Bank geometry is fixed before assigning correctness. Every numeric role is eligible.
    direction=rng.choice((-1,1));shift=rng.choice((-1,0,1))
    bank=[v if v=='No solution' else tex(direction*scalar(v)+shift) for v in source_bank(sid)]
    moderate=sid in LEVELS['moderate']
    if sid.startswith('hard:'):
        # Choose correctness independently of bank geometry, sign and zero-row position.
        numeric=[v for v in bank if v!='No solution']
        chosen=rng.choice(bank);s=scalar(rng.choice(numeric) if chosen=='No solution' else chosen)
        n=rng.choice((3,4));c=rng.choice((2,3));minus=rng.choice((False,True))
        a=[rng.randint(-3,3) for _ in range(n)]
        u=[rng.choice((-3,-2,-1,1,2,3)) for _ in range(n)]
        # A zero coefficient row plus at least two informative rows requires
        # interpreting constraints, not just extending an easy dot calculation.
        u[rng.randrange(n)]=0
        b=[int(c*x+(-s if minus else s)*y) for x,y in zip(a,u)]
        if chosen=='No solution':b[rng.randrange(n)]+=rng.choice((-1,1))
        if not any(b):a[0]+=1;b[0]+=c
        rng.shuffle(bank)
        return {'a':a,'u':u,'b':b,'c':c,'s':str(s),'minus':minus,'letter':rng.choice('h j k l m q t'.split()),'bank':bank}
    eligible=bank if moderate else [v for v in bank if v!='No solution']
    chosen=rng.choice(eligible)
    s=scalar(rng.choice([v for v in bank if v!='No solution']) if chosen=='No solution' else chosen)
    n=len(CASES[sid]['a']);c=1 if sid=='q-34241' else rng.randint(1,3 if moderate else 5)
    if moderate:
        # Integer vectors with bounded multipliers, then an optional contradictory row.
        multipliers=[rng.choice((-2,-1,1,2) if abs(s.p)<=6 else (-1,1)) for _ in range(n)]
        u=[int(c*s.q*m) for m in multipliers]
        a=[int(-s.p*m) for m in multipliers]
        # Keep at least one informative component, allowing any coordinate to
        # supply it. Contradictions may also occur in a zero unknown component.
        zeros=rng.sample(range(n),rng.randrange(n))
        for i in zeros:a[i]=0;u[i]=0
        if chosen=='No solution':
            nonzero=sum(x!=0 for x in u)
            mismatch=rng.choice(zeros) if nonzero==1 else rng.randrange(n)
            a[mismatch]+=rng.choice((-1,1))
    else:
        a=[rng.randint(-4,4) for _ in range(n)]
        u=[rng.randint(-4,4) for _ in range(n)]
        if sum(x!=0 for x in u)<2:u[rng.randrange(n)]=rng.choice((-3,-2,2,3))
        if not any(u):u[0]=1
    rng.shuffle(bank)
    return {'a':a,'u':u,'c':c,'s':None if moderate else str(s),'letter':rng.choice('h j k l m q t'.split()),'bank':bank}

def domain(sid):
    """Small reproducible normal-sampling witness set, not a finite sampling restriction."""
    return [sample_parameters(sid,random.Random(seed)) for seed in range(24)]

def batch(difficulty,count,seed=0):
    if difficulty not in LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    if count<0:raise ValueError('Count must be nonnegative')
    rng=random.Random(seed);records=[];seen=set()
    for _ in range(max(100,count*20)):
        if len(records)==count:break
        sid=rng.choice(LEVELS[difficulty]);p=sample_parameters(sid,rng)
        r=generate(difficulty,seed,sid,p);fp=r['generation']['parameter_fingerprint']
        if fp not in seen:seen.add(fp);records.append(r)
    if len(records)!=count:raise ValueError('Could not fill unique batch')
    return records
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='easy');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--output',type=Path);ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args()
    records=batch(args.difficulty,args.count,args.seed);text=json.dumps(records,indent=2)+'\n'
    if args.format=='markdown':text='\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text)
