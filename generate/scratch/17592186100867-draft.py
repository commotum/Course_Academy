#!/usr/bin/env python3
"""Read-only 3x3 matrix-column generator, draft v2.

Observed profiles preserve source fields, omissions and source-shaped solutions.
Opaque banks are evidence-only covariant families, never learner defaults.
Authored levels keep the three ordered row dot products; see classification.md.
"""
import sys
sys.dont_write_bytecode = True
import argparse, copy, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).with_suffix('')
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import matrix_tex, normalize_prose, normalize_tex, validate_generated_record, validate_prose, validate_tex, environment, cells
KP = 17592186100867
CAP = json.loads((HERE/'source.json').read_text())
RECORD = CAP['record']; KP_UUID = RECORD[':knowledge-point/id']; TITLE = RECORD[':knowledge-point/title']
VERSION = 'matrix3-column-draft-2.0'; LEVELS = ('easy','moderate','hard'); SUPPORTED_LEVELS = LEVELS
SOURCES = {q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions'] if ':question/math-academy-id' in q}
GROUPS = {'named-radio':['q-70188','q-70190','q-77350','q-13557'], 'inline-radio':['q-127267','q-70191','q-77349','q-77351'], 'named-blank':['q-318606'], 'inline-blank':['q-318622'], 'what-radio':['q-13558']}
TEMPLATES = tuple(GROUPS)
OPAQUE = {'q-13557','q-77349','q-77351'}
PROFILES = {t:[q for q in qs if q not in OPAQUE] for t,qs in GROUPS.items()}
NAMES = ('A','B','L','P','N','Z'); VNAMES = ('x','y','z','v','n')
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
ATOM = re.compile(r'\(-?\d+\)|[+-]?\d+')
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def matrices(text): return [[[int(c.strip()) for c in row.split('&')] for row in body.split('\\\\')] for body in MATRIX.findall(text)]
def parameters_of(q):
    m = matrices(q[':question/problem']); names = re.search(r'Find \$([A-Z])([a-z])\$',q[':question/problem'])
    return {'A':m[0], 'v':[row[0] for row in m[1]], 'matrix_name':names[1] if names else 'A', 'vector_name':names[2] if names else 'x'}
parameters = parameters_of
def template_of(mid): return next(t for t,ids in GROUPS.items() if mid in ids)
def vector(v): return matrix_tex([[x] for x in v])
def dot(p): return tuple(int(x) for x in s.Matrix(p['A'])*s.Matrix(p['v']))
def fingerprint(p):
    # Ordered operands matter: this KP assesses pairing every row with the column.
    return digest({'A':p['A'],'v':p['v'],'method':'three-ordered-row-dot-products'})
def question_fingerprint(q): return fingerprint(parameters_of(q))
def control_guard(value):
    if isinstance(value,str) and any(ord(c)<32 and c not in '\n\t' for c in value): raise ValueError('C0 control character in learner content')
    if isinstance(value,dict):
        for x in value.values(): control_guard(x)
    if isinstance(value,list):
        for x in value: control_guard(x)
def guard(p,level=None,observed=False):
    if set(p)!={'A','v','matrix_name','vector_name'}: raise ValueError('Exact parameter keys required')
    if len(p['A'])!=3 or len(p['v'])!=3 or any(len(row)!=3 for row in p['A']): raise ValueError('3x3 matrix and length3 column required')
    vals=[x for row in p['A'] for x in row]+p['v']
    if any(type(x)is not int or abs(x)>(128 if observed else 8) for x in vals) or not any(p['v']): raise ValueError('Integer arithmetic bounds')
    if p['matrix_name'] not in NAMES or p['vector_name'] not in VNAMES: raise ValueError('Unsupported variable name')
    if observed:return
    A,v=p['A'],p['v']
    if level=='easy':
        if v.count(0)!=1 or any(abs(x)>3 for x in v) or any(not 1<=abs(x)<=4 for row in A for x in row): raise ValueError('Easy requires six active small products')
    elif level=='moderate':
        if any(x==0 for x in v) or not any(abs(x)==1 for x in v) or any(sum(abs(x)==1 for x in row)!=1 or any(x==0 for x in row) for row in A): raise ValueError('Moderate requires one unit coefficient per row and a unit vector entry')
    elif level=='hard':
        if any(abs(x)<2 for x in vals) or any(len({1 if a*b>0 else -1 for a,b in zip(row,v)})!=2 for row in A): raise ValueError('Hard requires nine nonunit products and mixed product signs per row')
    else:raise ValueError('Unknown difficulty')

def covariance(mid,p):
    base=parameters_of(SOURCES[mid]); ratios={s.Rational(x,b) for x,b in zip(p['v'],base['v']) if b}
    if len(ratios)!=1 or any(x!=0 for x,b in zip(p['v'],base['v']) if b==0): raise ValueError('Opaque evidence requires global vector scaling')
    k=ratios.pop();scales=[]
    if not k:raise ValueError('Nonzero scaling required')
    for row,old in zip(p['A'],base['A']):
        rr={s.Rational(x,b) for x,b in zip(row,old) if b}
        if len(rr)!=1 or any(x!=0 for x,b in zip(row,old) if not b):raise ValueError('Opaque evidence requires per-row matrix scaling')
        d=rr.pop()
        if not d:raise ValueError('Nonzero row scaling required')
        scales.append(d*k)
    return scales

def bank(profile,p):
    mid=profile.removeprefix('observed:');r,t,u=dot(p)
    banks={
      'q-127267':[(r,t,u),(r,t,-u),(r,-t,-u),(r,-t,u),(r,r,-u)],
      'q-70188':[(r,t,u),(r,-t,-u),(r,t,-u),(-r,-t,u),(r,-t,u)],
      'q-70191':[(r,t,u),(r,-t,u),(r,-t,-u),(-r,t,u),(r,t,-u)],
      'q-70190':[(r,t,u),(r,t,-u),(r,-t,u),(-r,t,u),(-r,-t,u)],
      'q-77350':[(r,t,u),(-r,-t,u),(r,u,t),(r,-t,u),(u,t,r)],
      'q-13558':[(r,t,u),(-r,-t,u),(-r,t,u),(r,-t,-u),(r,t,-u)]}
    if mid in banks:return banks[mid]
    if mid in OPAQUE:
        factors=covariance(mid,p)
        # Homogeneous output covariance is mathematically justified; error intent is unknown.
        return [tuple(int(f*x) for f,x in zip(factors,[row[0] for row in matrices(a[':answer/value'])[0]])) for a in SOURCES[mid][':question/answer-fields'][0][':answer-field/choices']]
    if profile=='authored-method':
        result=dot(p);A,v=p['A'],p['v']
        active=[j for j in range(3) if v[j]]
        omissions=[tuple(result[i]-A[i][j]*v[j] for i in range(3)) for j in active]
        extra=[tuple(-x for x in result)] if len(active)==2 else []
        return [result,*omissions,tuple(int(x) for x in s.Matrix(A).T*s.Matrix(v)),*extra]
    if mid in ('q-318606','q-318622'):return []
    raise ValueError('Unknown bank profile')

def spans(text):
    out=[];offset=0
    while True:
        m=re.search(r'\\begin\{bmatrix\}',text[offset:])
        if not m:return out
        start=offset+m.start();span=environment(text,start)
        if span is None:raise ValueError('Bad source environment')
        out.append((start,span[2],text[span[0]:span[1]]));offset=span[2]
def substitute_atoms(body,values,kind,old_products=None):
    matches=list((re.compile(r'\(-?\d+\)|-?\d+') if kind=='factor' else ATOM).finditer(body))
    if len(matches)!=len(values):raise ValueError(('Unexpected source numeric mask',kind,len(matches),len(values)))
    result=[];last=0
    for i,(m,n) in enumerate(zip(matches,values)):
        old=m[0];n=int(n);prefix=''
        if kind=='factor':
            # A negative first factor can stay bare only where source begins a row that way.
            bare_negative=old.startswith('-') and not old.startswith('(')
            value='('+str(n)+')' if old.startswith('(') or (n<0 and not bare_negative) else str(n)
        elif kind=='signed-products':
            # Compact three-term rows preserve the sign of a zero product too.
            j=i%3;negative=old_products[i]
            value=('-' if negative else ('+' if j else ''))+str(abs(n))
        elif kind=='grouped-products':
            value='('+str(n)+')' if old.startswith('(') or (n<0 and not old.startswith('-')) else str(n)
        else:value=str(n)
        result.extend([body[last:m.start()],value]);last=m.end()
    return ''.join(result)+body[last:]
def render(template,p,mid):
    source=SOURCES[mid];old=parameters_of(source);prompt=source[':question/problem'];ms=spans(prompt)
    for ix,(start,end,_) in reversed(list(enumerate(ms))):prompt=prompt[:start]+(matrix_tex(p['A']) if ix==0 else vector(p['v']))+prompt[end:]
    if template.startswith('named'):
        # Only complete named mathematical components are replaced.
        prompt=re.sub(r'\$'+old['matrix_name']+old['vector_name']+r'(?=[=$])',lambda _: '$'+p['matrix_name']+p['vector_name'],prompt)
        prompt=re.sub(r'\$'+old['matrix_name']+r'(?=\s*=)',lambda _: '$'+p['matrix_name'],prompt)
        prompt=re.sub(r'\$'+old['vector_name']+r'(?=\s*=)',lambda _: '$'+p['vector_name'],prompt)
    if ':question/worked-solution' not in source:return normalize_prose(prompt),None
    solution=source[':question/worked-solution'];st=spans(solution)
    products=[a*b for row in p['A'] for a,b in zip(row,p['v'])]
    factors=[x for row in p['A'] for a,b in zip(row,p['v']) for x in (a,b)]
    signs=[(a<0) != (b<0) for row in p['A'] for a,b in zip(row,p['v'])]
    bodies=[matrix_tex(p['A']),vector(p['v']),r'\begin{bmatrix}'+substitute_atoms(st[2][2],factors,'factor')+r'\end{bmatrix}',r'\begin{bmatrix}'+substitute_atoms(st[3][2],products,'grouped-products' if template.endswith('blank') else 'signed-products',signs)+r'\end{bmatrix}',vector(dot(p))]
    if len(st)!=5:raise ValueError('Expected operands, expanded products, evaluated terms, final column')
    for (start,end,_),body in reversed(list(zip(st,bodies))):solution=solution[:start]+body+solution[end:]
    if template.startswith('named'):solution=solution.replace(r'\begin{aligned}'+old['matrix_name']+old['vector_name'],r'\begin{aligned}'+p['matrix_name']+p['vector_name'])
    return normalize_prose(prompt),normalize_prose(solution)

def sample(level,rng):
    sign=lambda n:rng.choice((-1,1))*n
    if level=='easy':
        v=[sign(rng.randint(1,3)) for _ in range(3)];v[rng.randrange(3)]=0;A=[[sign(rng.randint(1,4)) for _ in range(3)] for _ in range(3)]
    elif level=='moderate':
        v=[sign(rng.randint(2,8)) for _ in range(3)];v[rng.randrange(3)]=sign(1);A=[]
        for _ in range(3):
            row=[sign(rng.randint(2,8)) for _ in range(3)];row[rng.randrange(3)]=sign(1);A.append(row)
    else:
        v=[sign(rng.randint(2,8)) for _ in range(3)];A=[]
        for _ in range(3):
            product_signs=rng.choice(([-1,1,1],[1,-1,1],[1,1,-1],[-1,-1,1],[-1,1,-1],[1,-1,-1]))
            A.append([t*(1 if b>0 else -1)*rng.randint(2,8) for t,b in zip(product_signs,v)])
    return {'A':A,'v':v,'matrix_name':rng.choice(NAMES),'vector_name':rng.choice(VNAMES)}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty')
    rng=random.Random(seed);observed=bool(profile and profile.startswith('observed:'))
    mid=profile.removeprefix('observed:') if observed else None
    template=template or (template_of(mid) if observed else rng.choice(TEMPLATES))
    if template not in TEMPLATES or (observed and mid not in GROUPS[template]):raise ValueError('Mismatched template/profile')
    typ='blank' if template.endswith('blank') else 'radio'
    if field_type and field_type.removeprefix(':answer-field.type/')!=typ:raise ValueError('Field contract fixed by template')
    if observed:
        selected=mid
    elif profile is None:
        selected=rng.choice(PROFILES[template])
        profile='authored-method' if not PROFILES[template] else selected
    else:
        if profile not in PROFILES[template] and profile!='authored-method':raise ValueError('Unsupported normal bank')
        selected=profile if profile in SOURCES else GROUPS[template][0]
    # Opaque source masks have standard dot-product stages, but never supply default opaque banks.
    for _ in range(2000):
        p=copy.deepcopy(parameters) if parameters is not None else sample(level,rng)
        guard(p,level,observed)
        entries=[] if typ=='blank' else bank(profile,p)
        if len(set(entries))==len(entries):break
        if parameters is not None:raise ValueError('Entire bank rejected: equivalent choices')
    else:raise ValueError('No eligible complete bank')
    prompt,solution=render(template,p,selected)
    source=SOURCES[selected]
    # Unrated source completion is authored and explicit; raw replay preserves omissions.
    if solution is None and not observed:
        solution=render('named-radio' if template.startswith('named') else 'inline-radio',p,'q-70188' if template.startswith('named') else 'q-70191')[1]
    q={':question/problem':prompt}
    if solution is not None:q[':question/worked-solution']=solution
    if not observed or ':question/difficulty' in source:q[':question/difficulty']=source[':question/difficulty'][':db/ident'] if observed else ':question.difficulty/'+level
    fields=[]
    specs=[(f[':answer-field/key'],f[':answer-field/type'][':db/ident']) for f in source[':question/answer-fields']]
    complete=[]
    for key,ft in specs:
        values=[str(dot(p)[int(key[-1])-1])] if typ=='blank' else [vector(x) for x in entries]
        correct_value=str(dot(p)[int(key[-1])-1]) if typ=='blank' else vector(dot(p))
        rawf=next(f for f in source[':question/answer-fields'] if f[':answer-field/key']==key)
        has_correct=not observed or ':answer-field/correct' in rawf
        if correct_value not in values:raise ValueError('Correct vector absent from bank')
        complete.append((key,ft,sorted(values),correct_value if has_correct else None))
    identity=digest({'version':VERSION,'question':q,'fields':sorted(complete),'math':fingerprint(p)})
    qid=uid('question:'+identity);q[':question/id']=qid
    for key,ft,values,correct in complete:
        fid=uid(qid+':field:'+key);choices=[{':answer/id':uid(fid+':answer:'+value),':answer/type':':answer.type/math',':answer/value':normalize_tex(value)} for value in values]
        rng.shuffle(choices);f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':ft,':answer-field/choices':choices}
        if correct is not None:f[':answer-field/correct']=[':answer/id',uid(fid+':answer:'+correct)]
        fields.append(f)
    q[':question/answer-fields']=fields
    r={'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_version':VERSION,'template':template,'bank_profile':profile,'parameters':p,'seed':seed,'source_basis':CAP['basis'],'lineage':CAP['lineage'],'source_references':[selected],'mathematical_fingerprint':fingerprint(p),'eligible_for_learning':not observed,'evidence_only':observed,'authored_level':not observed,'python_version':sys.version.split()[0],'sympy_version':s.__version__}}
    control_guard(q)
    # Shared normalizer applies before identity; validate omissions separately for raw profiles.
    if solution is not None:validate_generated_record(r)
    else:
        validate_prose(prompt)
        for f in fields:
            for a in f[':answer-field/choices']:validate_tex(a[':answer/value'])
    return r

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='moderate');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=('json','markdown'),default='json');args=ap.parse_args()
    out=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    if args.format=='json':print(json.dumps(out,indent=2))
    else:
        for r in out:
            q=r['question'];print(q[':question/problem']+'\n\n'+q.get(':question/worked-solution','')+'\n\n'+json.dumps(q[':question/answer-fields']))
