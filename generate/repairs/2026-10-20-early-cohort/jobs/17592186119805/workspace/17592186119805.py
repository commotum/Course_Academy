"""Source-faithful, bounded vector coefficient question generator.

Three backbones: c*a1+s*a2=b; a1-s*a2=b; c*a1+s*a2=0
with incompatible component ratios. Each source bank is a separate profile.
"""
import argparse, hashlib, itertools, json, os, random, re, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    # The application invokes its own Python. Use this repository's installed
    # mathematical environment without changing the application or installing packages.
    if __name__ != '__main__':raise
    interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if not interpreter.is_file() or Path(sys.executable).absolute()==interpreter.absolute():raise
    os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186119805
KP_UUID='33586620-e110-5a37-874f-a92103c5e9fb'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'linear-combination-coefficient-generator-v1'))
VERSION='1.0.0'
LEVELS={'easy':('q-34249','q-105152','q-105154','q-34051','q-34241','q-34600'),'moderate':('q-34570','q-34602','q-73923')}
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'reference/source.json').read_text())
PROFILES={q[':question/math-academy-id']:q for q in SOURCE['rows'][0][0][':knowledge-point/questions'] if q.get(':question/difficulty')}
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
def values(sid,p):
    s=sp.Rational(p['s']) if p['s'] is not None else None;c=sp.Integer(p['c']);a=p['a'];u=p['u']
    t=-c*sp.Rational(a[0],u[0]) if sid in LEVELS['moderate'] else None
    z=-c*sp.Rational(a[1],u[1]) if sid in LEVELS['moderate'] else None
    banks={
      'q-34249':lambda:[-s,s,-s/2,0,'No solution'],
      'q-105152':lambda:[s,'No solution',s/2,-s/2,-s],
      'q-105154':lambda:[s+2,s,-s-2,-s,'No solution'],
      'q-34051':lambda:[s-1,s,c,-c,1],
      'q-34241':lambda:[0,s,-2*s,-s,2*s],
      'q-34600':lambda:[s-1,1,0,s,2*s],
      'q-34570':lambda:[-t,'No solution',1,t,z],
      'q-34602':lambda:[t,'No solution',t/2,-c,c/2],
      'q-73923':lambda:['No solution',-t,t/2,t,z]}
    return [v if isinstance(v,str) else tex(v) for v in banks[sid]()]
def data(sid,p):
    a=sp.Matrix(p['a']);u=sp.Matrix(p['u']);c=p['c'];s=p['s'];moderate=sid in LEVELS['moderate'];minus=sid=='q-34241'
    assert len(a)==len(CASES[sid]['a']) and len(a)==len(u) and any(u)
    assert c>0 and all(type(x)is int for x in p['a']+p['u']+[c]) and p['letter']==CASES[sid]['letter']
    if moderate:
        assert u[0] and u[1]
        b=sp.zeros(len(a),1);r=-c*a;t=sp.Rational(r[0],u[0]);assert t.q==1
        assert t*u!=r and sp.Rational(r[1],u[1])!=t
        correct='No solution'
    else:
        assert type(s)is int and s!=0
        b=c*a+(-s if minus else s)*u;r=s*u;t=s;correct=tex(s)
    bank=values(sid,p);assert len(bank)==5 and len(set(bank))==5 and bank.count(correct)==1
    return a,u,b,r,t,correct,bank

def render(sid,p):
    a,u,b,r,t,correct,bank=data(sid,p);c=p['c'];letter=p['letter'];minus=sid=='q-34241';moderate=sid in LEVELS['moderate']
    av,uv,bv,rv=map(lambda m:vec(list(m)),(a,u,b,r))
    eq=(r'{a}_{1}-'+letter+r'{a}_{2}=b') if minus else str(c)+r'{a}_{1}+'+letter+r'{a}_{2}='+('0' if moderate else 'b')
    problem=f'Find ${letter}$, if ${eq}$ and\n\n$$\n'+r'{a}_{1}='+av+r',\,{a}_{2}='+uv+('' if moderate else r',\,b='+bv)+'.\n$$'
    first=(av+'-'+letter+uv) if minus else str(c)+av+'+'+letter+uv
    difference=(av+'-'+bv) if minus else bv+'-'+str(c)+av
    sol=f'Using the properties of addition/subtraction and scalar multiplication of vectors to isolate the ${letter}$ term, we get\n\n$$\n'+r'\begin{aligned}'+eq.replace('=',' & =')+r' \\ '+first+' & ='+bv+r' \\ '+letter+uv+' & ='+difference+r' \\ '+letter+uv+' & ='+rv+r'.\end{aligned}'+'\n$$\n\n'
    if moderate:
        sol+='Equating the first components, we get\n\n$$\n'+str(u[0])+letter+'='+str(r[0])+r'\,⟹\,'+letter+'='+tex(t)+'.\n$$\n\nBut then\n\n$$\n'+r'\begin{aligned}'+tex(t)+uv+'='+vec(list(t*u))+r'\ne '+rv+r'.\end{aligned}'+'\n$$\n\nTherefore, there is no $'+letter+'$ such that $'+eq+'.$'
    else:sol+='From the final equation above, we can tell that $'+letter+'='+correct+'.$'
    return problem,sol,correct,bank

def fingerprint(q):
    text=q[':question/problem'];a,u,*bs=vectors(text)
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
    p=parameters if parameters is not None else rng.choice(domain(sid))
    problem,solution,correct,bank=render(sid,p)
    # Same mathematical task/profile always has the same field-owned identities.
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),json.dumps([sid,p,bank],sort_keys=True)))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/text' if value=='No solution' else ':answer.type/math',':answer/value':value} for value in bank]
    f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]}
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[f]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Solving for One Coefficient in a Linear Combination'},'question':q,'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'parameters':p,'template':'inconsistent-zero' if difficulty=='moderate' else 'subtract' if sid=='q-34241' else 'unique-coefficient','bank_profile':sid,'source_question_id':PROFILES[sid][':question/id'],'source_basis':SOURCE['basis'],'dependencies':{'sympy':sp.__version__},'assets':[],'parameter_fingerprint':fingerprint(q)}}

_CACHE={}
def domain(sid):
    if sid in _CACHE:return _CACHE[sid]
    base=CASES[sid];out=[];seen=set()
    # Conservative finite policy: one coordinate changes, coefficient changes by at most one,
    # and easy solutions change by at most one. All source cases remain replayable.
    for which,index,delta,c,ss in itertools.product(('a','u'),range(len(base['a'])),(-2,-1,0,1,2),range(max(1,base['c']-1),base['c']+2),[None] if base['s'] is None else range(base['s']-1,base['s']+2)):
        if sid=='q-34241' and c!=1:continue
        p=json.loads(json.dumps(base));p[which][index]+=delta;p['c']=c;p['s']=ss
        if p['u'][index]==0 and which=='u' and base['u'][index]!=0:continue
        try:data(sid,p)
        except (AssertionError,ZeroDivisionError,TypeError):continue
        key=json.dumps(p,sort_keys=True)
        if key not in seen:seen.add(key);out.append(p)
    _CACHE[sid]=out;return out

def batch(difficulty,count,seed=0):
    if difficulty not in LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    cases=[(sid,p) for sid in LEVELS[difficulty] for p in domain(sid)];random.Random(seed).shuffle(cases)
    records=[];seen=set()
    for sid,p in cases:
        r=generate(difficulty,seed,sid,p);fp=r['generation']['parameter_fingerprint']
        if fp not in seen:seen.add(fp);records.append(r)
        if len(records)>=count:break
    return records if count else []
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='moderate');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--output',type=Path);ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args()
    records=batch(args.difficulty,args.count,args.seed);text=json.dumps(records,indent=2)+'\n'
    if args.format=='markdown':text='\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text)
