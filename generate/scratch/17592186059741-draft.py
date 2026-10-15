"""Scalar recovery; local draft, no registration or EDB access.

Raw profiles parameterize all original MA records, retaining documented omissions
and erroneous source signs as ineligible evidence. Normal records repair these
and use complete method-derived banks. See the private extraction document.
"""
import argparse, copy, functools, hashlib, json, random, re, sys, uuid
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import matrix_tex,normalize_prose,normalize_tex,checked_math_content,validate_generated_record
HERE=Path(__file__).with_suffix(''); VERSION='2.0.0'
SOURCE=json.loads((HERE/'source.json').read_text()); KP=SOURCE['record']
CASES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate','hard'); NS=uuid.UUID(KP[':knowledge-point/id'])
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S); K=sp.Symbol('k')
def parse(s):
    s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s).replace(' ','').rstrip('.')
    s=re.sub(r'(\d|\))(?=k)',r'\1*',s)
    return sp.sympify(s,locals={'k':K},rational=True)
def matrices(s):return [sp.Matrix([[parse(c) for c in row.split('&')] for row in body.split(r'\\')]) for body in MAT.findall(s)]
def tex(v):return normalize_tex(sp.latex(v).replace(" ",""))
def mat(a):return matrix_tex([[tex(a[i,j]) for j in range(a.cols)] for i in range(a.rows)])
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
POSITIONS={'q-11442':[0,0],'q-981':[0,0],'q-139431':[0,2],'q-320536':[1,0],'q-320551':[2,0],'q-320563':[0,2],'q-69670':[0,0]}
DEFAULTS={}
for sid,q in CASES.items():
    ms=matrices(q[':question/problem']); b=ms[0]
    a=ms[1] if len(ms)>1 else matrices(q[':question/worked-solution'])[0]
    scalar=next(y/x for x,y in zip(a,b) if x)
    DEFAULTS[sid]={'matrix':[[str(x) for x in row] for row in a.tolist()],'scalar':str(scalar),'target':POSITIONS[sid]}
def validate_parameters(p,sid,level,raw):
    if not isinstance(p,dict) or set(p)!={'matrix','scalar','target'}:raise ValueError('matrix/scalar/target required')
    a=sp.Matrix(p['matrix']); c=sp.Rational(p['scalar']); target=p['target']; old=sp.Matrix(DEFAULTS[sid]['matrix'])
    if a.shape!=old.shape or not c or any(x.is_Integer is not True or abs(x)>144 or sp.sign(x)!=sp.sign(y) for x,y in zip(a,old)):raise ValueError('source matrix shape/sign/zero pattern and integer bounds required')
    if not isinstance(target,list) or len(target)!=2 or any(type(x)!=int for x in target):raise ValueError('integer target pair required')
    i,j=target
    if not(0<=i<a.rows and 0<=j<a.cols) or a[i,j]==0:raise ValueError('nonzero corresponding target required')
    if any(x.is_Integer is not True or abs(x)>864 for x in c*a):raise ValueError('integral product entries bounded by 864 required')
    if sid=='q-139431' and (a!=old or c<=0 or c.q!=1 or c>9):raise ValueError('payoff context uses supplied fixed P and positive integer bet multiplier')
    if not raw:
        if level=='easy' and (c.q!=1 or not 2<=abs(c)<=9):raise ValueError('easy integer magnitude 2..9')
        if level=='moderate' and (abs(c.p)!=1 or not 2<=c.q<=6):raise ValueError('moderate signed reciprocal 1/2..1/6')
        if level=='hard' and (not 2<=abs(c.p)<=5 or not 2<=c.q<=6):raise ValueError('hard reduced nonunit rational numerator 2..5 denominator 2..6')
    return a,c,i,j
def sample(rng,sid,level):
    old=sp.Matrix(DEFAULTS[sid]['matrix'])
    c=sp.Integer(rng.choice([-1,1])*rng.randint(2,9)) if level=='easy' else sp.Rational(rng.choice([-1,1])*(1 if level=='moderate' else rng.randint(2,5)),rng.randint(2,6))
    if sid=='q-139431':c=sp.Integer(rng.randint(2,9));a=old
    else:a=old.applyfunc(lambda x:sp.sign(x)*rng.randint(1,12)*c.q if x else sp.Integer(0))
    target=rng.choice([[i,j] for i in range(a.rows) for j in range(a.cols) if a[i,j]])
    return {'matrix':[[str(x) for x in row] for row in a.tolist()],'scalar':str(c),'target':target}
def components(sid,a,c,i,j,raw):
    """Complete source masks: expand kM, equate matrices, choose cell, solve."""
    q=CASES[sid];old=sp.Matrix(DEFAULTS[sid]['matrix']);b=c*a; ak=K*a
    it=iter([mat(b),mat(a)]);problem=MAT.sub(lambda _:next(it),q[':question/problem'])
    if sid=='q-139431' and not raw:
        problem=re.sub(r'\n[ \t]+','\n',problem)
        problem=problem[:problem.index(r'$\,k=$')]+r'$k=$'+'\n{{field-1}}.'
        problem=problem.replace('This new matrix is obtained',f'The original payoff matrix is $P={mat(a)}$.\n\nThis new matrix is obtained')
    solution=q.get(':question/worked-solution')
    if solution is None and not raw:
        solution=CASES['q-69670'][':question/worked-solution'].replace('kS','kG').replace('$S$','$G$')
    if solution is not None:
        first=a.copy();firstk=ak.copy()
        if raw and sid=='q-320536':first[1,0]=-first[1,0];firstk[1,0]=-firstk[1,0]
        it=iter([mat(first),mat(firstk),mat(ak),mat(b)]); solution=MAT.sub(lambda _:next(it),solution)
        target_text=solution.split("Let's choose ")[1].split(', $')[0] if [i,j]==POSITIONS[sid] else f'the elements in row ${i+1}$ and column ${j+1}$'
        start=solution.index("Let's choose ");end=solution.index('Equating these elements',start)
        solution=solution[:start]+f"Let's choose {target_text}, ${tex(a[i,j]*K)}$ and ${tex(b[i,j])}.$ "+solution[end:]
        start=solution.index(r'\begin{aligned}',solution.index('Equating these elements'));end=solution.index(r'\end{aligned}',start)+len(r'\end{aligned}')
        solution=solution[:start]+r'\begin{aligned}'+tex(a[i,j]*K)+' & ='+tex(b[i,j])+r' \\ k & ='+tex(c)+r'.\end{aligned}'+solution[end:]
    return normalize_prose(problem),normalize_prose(solution) if solution is not None else None
def checked_optional_solution(fn):
    @functools.wraps(fn)
    def wrapped(*args,**kwargs):
        record=fn(*args,**kwargs); validation=copy.deepcopy(record)
        validation['question'].setdefault(':question/worked-solution','')
        validate_generated_record(validation)
        return record
    return wrapped
@checked_optional_solution
def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
    if type(seed)!=int:raise TypeError('seed must be a built-in integer')
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
    rng=random.Random(seed)
    if profile is not None and profile!='method' and not profile.startswith('raw-'):raise ValueError('unknown profile')
    raw=bool(profile and profile.startswith('raw-'))
    if raw and level!='easy':raise ValueError('raw source replay uses observed easy level or retained unrated omission')
    sid=template or (profile[4:] if raw else rng.choice(list(CASES) if level=='easy' else [s for s in CASES if s!='q-139431']))
    if sid not in CASES or (raw and profile!='raw-'+sid):raise ValueError('unknown/incompatible template/profile')
    q=CASES[sid];f=q[':question/answer-fields'][0];ft=f[':answer-field/type'][':db/ident']
    if field_type is not None and field_type not in (ft,ft.split('/')[-1]):raise ValueError('source field type required')
    explicit=parameters is not None
    for attempt in range(1000):
        p=parameters if explicit else sample(rng,sid,level)
        try:
            a,c,i,j=validate_parameters(p,sid,level,raw); b=c*a
            # Correct value is computed before any wrong option. Complete profile fixed first.
            correct=c;radio=ft.endswith('/radio')
            if raw and radio:
                original=sp.Rational(DEFAULTS[sid]['scalar']);values=[c+(parse(z[':answer/value'].split('=')[-1])-original) if parse(z[':answer/value'].split('=')[-1])!=0 else sp.Integer(0) for z in f[':answer-field/choices']]
            elif radio:values=[correct,a[i,j]/b[i,j],b[i,j]*a[i,j],b[i,j]-a[i,j],b[i,j]+a[i,j]]
            else:values=[correct]
            if len(set(values))!=len(values):raise ValueError('complete bank collision')
            break
        except ValueError:
            if explicit:raise
    else:raise ValueError('sampler exhausted')
    problem,solution=components(sid,a,c,i,j,raw)
    fmt=(lambda v:'k = '+tex(v)) if sid=='q-11442' and raw else (lambda v:'k='+tex(v)) if radio else tex
    answers=[fmt(v) for v in values]; correct_value=fmt(correct)
    identity=digest([VERSION,level,problem,solution,sorted(answers),ft,raw])
    qid=str(uuid.uuid5(NS,identity));fid=str(uuid.uuid5(uuid.UUID(qid),f[':answer-field/key']))
    bank=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in answers]
    field={':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':ft,':answer-field/choices':bank}
    if not raw or ':answer-field/correct' in f:field[':answer-field/correct']=[':answer/id',next(x[':answer/id'] for x in bank if x[':answer/value']==correct_value)]
    rng.shuffle(bank)
    out={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
    if not raw or ':question/difficulty' in q:out[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:out[':question/worked-solution']=solution
    # Assessed task is scalar recovery from the supplied pair: target is only a solution choice.
    # Uniform matrix scaling changes no ratio; remove that incidental scaling.
    pivot=next(x for x in a if x)
    fingerprint=digest([a.shape,[str(x/pivot) for x in a],str(c),sid=='q-139431'])
    return {'knowledge_point':{'db_id':17592186059741,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':out,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':profile or 'method','parameters':p,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'mathematical_fingerprint':fingerprint,'python':sys.version.split()[0],'sympy':sp.__version__,'evidence_only':raw,'eligible_for_learning':not raw,'bank_recipes':('empirical scalar offsets; interpretation unresolved' if raw and radio else ['quotient','reciprocal quotient','product','difference','sum'] if radio else ['quotient']),'repairs':[] if raw else (['supply omitted P','remove captured indentation around blank'] if sid=='q-139431' else ['correct negative first matrix entry'] if sid=='q-320536' else ['infer correct value and author solution/difficulty'] if sid=='q-11442' else [])}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def batch(level='all',seed=0,count=1,**kw):
    if type(seed)!=int or type(count)!=int:raise TypeError('seed/count must be built-in integers')
    if count<1:raise ValueError('positive count required')
    levels=SUPPORTED_LEVELS if level=='all' else (level,);out=[]
    for lev in levels:
        seen=set()
        for n in range(count*1000):
            r=generate(lev,seed+n,**kw);fp=r['generation']['mathematical_fingerprint']
            if fp not in seen:seen.add(fp);out.append(r)
            if len(seen)==count:break
        else:raise ValueError('not enough distinct tasks')
    return out
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+json.dumps(q[':question/answer-fields'],indent=2)+'\n\n'+q.get(':question/worked-solution','[Source has no worked solution]')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=[*SUPPORTED_LEVELS,'all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template');p.add_argument('--profile');args=p.parse_args();rs=batch(args.difficulty,args.seed,args.count,template=args.template,profile=args.profile);print(json.dumps(rs,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,rs)))
