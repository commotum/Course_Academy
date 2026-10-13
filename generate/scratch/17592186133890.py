#!/usr/bin/env python3
"""Supplied-potential FTLI on Cartesian curves, immutable math basis 1356.

Twelve observed families preserve their distinct source arithmetic rows and all
five options. `observed` is a homogeneous coefficient replay: each captured
potential and each complete bank are multiplied by the same nonzero scale. This
is not a recovered distractor theory. Authored defaults use complete operations
and vary Cartesian curves, coefficients and endpoints at fixed workload.
No database clients, registrations, plots, or writes outside this KP are used.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186133890
KP_UUID='c4519f3b-0fb8-54fd-9e9e-fca3e599b80b'
TITLE='Applying the Fundamental Theorem of Line Integrals Over Cartesian Curves'
VERSION='cartesian-ftli-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X,Y,T=s.symbols('x y t', real=True)
# Source mathematical models; complete source banks are homogeneous replay masks.
MODELS={
'q-123879':(Y**2-X**2,T**2/4,T,0,2*s.sqrt(2)),
'q-39749':(X**2*Y,T,s.cos(T)+T**3-2,0,s.pi),
'q-104617':(s.sin(X)+s.cos(Y),T,2*T,0,s.pi),
'q-104625':(s.exp(X)*s.sin(s.pi*Y/2),T,T**3+1,1,2),
'q-104626':((X**3+Y**3)/3,T,2*T**2,-1,2),
'q-124027':(X*s.exp(Y+1),T,s.exp(T)+1,0,s.log(2)),
'q-124028':(Y*X**3,T,s.log(T),1,s.exp(2)),
'q-124029':(X*s.sin(Y),T**2,T,0,s.pi/2),
'q-124030':(X**2+s.exp(X*Y),2*s.sqrt(T),T,1,4),
'q-124032':(s.exp(Y)*s.sin(X),T/2,T,0,s.pi),
'q-124034':(s.cos(X)*s.cos(Y),s.pi*T**3/2,T,0,1),
'q-124035':(Y**2-X,s.cos(T),T,0,s.pi),
}
LEVELS={name:q[':question/difficulty'][':db/ident'].split('/')[-1] for name,q in QUESTIONS.items()}
LEVELS.update({'authored_direct':'easy','authored_inverse':'moderate','authored_mixed':'hard'})
DEFAULTS={'easy':'authored_direct','moderate':'authored_inverse','hard':'authored_mixed'}
THEOREM=QUESTIONS['q-104626'][':question/worked-solution'].split('We start by parametrizing')[0]

def tex(v):return s.latex(s.sympify(v))
def par(v):return r'\left('+tex(v)+r'\right)'
def block(v):return '$$\n'+v+'\n$$'
def scaled_raw(raw,k):
    return raw if k==1 else str(k)+r'\left('+raw+r'\right)'
def hash_data(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'cartesian-ftli:'+v))
def simplified(v):
    # Keep exp-form answers within source vocabulary; SymPy may introduce cosh.
    return s.expand(s.simplify(s.expand(v)).rewrite(s.exp))

def source_components(name,p):
    """Component masks, not a literal replay branch; same renderer for scale 1/2/etc."""
    q=QUESTIONS[name];k=p['scale'];base,xt,yt,a,b=MODELS[name];f=k*base
    prompt=q[':question/problem']
    match=re.search(r'Let \$f\(x,y\)=(.*?)\.\$',prompt)
    assert match,name
    prompt=prompt[:match.start(1)]+scaled_raw(match[1],k)+prompt[match.end(1):]
    sol=q[':question/worked-solution']
    if name=='q-39749':
        # Raw evidence remains unchanged. Both substitution entries use r(0)=(0,-1).
        sol=sol.replace(')-f(0,0)',')-f(0,-1)').replace(r'-{0}^{2}\cdot 0',r'-{0}^{2}\cdot (-1)')
    final_start=sol.rindex(r'\begin{aligned}')
    tail=sol[final_start:];rows=tail.split(r'\\')
    # First two rows are theorem and endpoint substitution. All subsequent rows
    # retain source arithmetic operations, including optional collection stages.
    for i in range(2,len(rows)):
        m=re.search(r'& =(.*?)(?=\.\\end\{aligned\}|$)',rows[i],re.S)
        assert m,(name,rows[i])
        rows[i]=rows[i][:m.start(1)]+scaled_raw(m[1],k)+rows[i][m.end(1):]
    sol=sol[:final_start]+r'\\'.join(rows)
    A=(simplified(xt.subs(T,a)),simplified(yt.subs(T,a)));B=(simplified(xt.subs(T,b)),simplified(yt.subs(T,b)))
    start=simplified(f.subs({X:A[0],Y:A[1]}));end=simplified(f.subs({X:B[0],Y:B[1]}));D=simplified(end-start)
    field=q[':question/answer-fields'][0]
    values=[scaled_raw(answer[':answer/value'],k) for answer in field[':answer-field/choices']]
    correct_raw=field[':answer-field/correct'][':answer/value']
    ci=next(i for i,a0 in enumerate(field[':answer-field/choices']) if a0[':answer/value']==correct_raw)
    return prompt,sol,values,ci,{'f':f,'xt':xt,'yt':yt,'a':s.sympify(a),'b':s.sympify(b),'A':A,'B':B,'start':start,'end':end,'D':D}

# Easy: direct Cartesian function, integer endpoints and one supplied cubic sum.
# Moderate: recover x from a principal square root, square endpoints, two terms.
# Hard: solve a line for y, two supplied mixed terms, nonzero endpoint values.
# These are independent fixed-workload choices, not a level-internal progression.
def authored_components(name,p):
    k,m,c,a,b=[s.Integer(p[z]) for z in ('k','m','c','a','b')]
    if name=='authored_direct':
        f=k*(X**3+Y**3)/3;xt=T;yt=m*T**2+c
        ftext=tex(k/3)+r'\left(x^{3}+y^{3}\right)';curve='y='+tex(m)+r'x^{2}'+('+'+tex(c) if c>=0 else tex(c));variable='x'
        def ev(x,y):return tex(k/3)+r'\left('+par(x)+r'^{3}+'+par(y)+r'^{3}\right)'
        def partial(x,y):return tex(k/3)+r'\left('+tex(x**3+y**3)+r'\right)'
    elif name=='authored_inverse':
        f=k*(X**2+s.exp(X*Y));xt=m*s.sqrt(T)+c;yt=T
        ftext=tex(k)+r'\left(x^{2}+e^{xy}\right)';curve=r'\frac{x-'+tex(c)+'}{'+tex(m)+r'}=\sqrt{y}';variable='y'
        def ev(x,y):return tex(k)+r'\left('+par(x)+r'^{2}+e^{'+tex(x)+r'\cdot '+tex(y)+r'}\right)'
        def partial(x,y):return tex(k)+r'\left('+tex(x*x)+r'+e^{'+tex(x*y)+r'}\right)'
    else:
        ell=s.Integer(p['ell']);n=s.Integer(p['n']);f=k*X**2*Y+ell*X*s.exp(Y);xt=T;yt=(c-m*T)/n
        ftext=tex(k)+r'x^{2}y+'+tex(ell)+r'xe^{y}';curve=tex(m)+'x+'+tex(n)+'y='+tex(c);variable='x'
        def ev(x,y):return tex(k)+r'\cdot '+par(x)+r'^{2}\cdot '+par(y)+'+'+tex(ell)+r'\cdot '+par(x)+r'\cdot e^{'+tex(y)+'}'
        def partial(x,y):return tex(k*x*x*y)+('+' if ell*x>=0 else '-')+tex(abs(ell*x))+r'\cdot e^{'+tex(y)+'}'
    A=(simplified(xt.subs(T,a)),simplified(yt.subs(T,a)));B=(simplified(xt.subs(T,b)),simplified(yt.subs(T,b)))
    start=simplified(f.subs({X:A[0],Y:A[1]}));end=simplified(f.subs({X:B[0],Y:B[1]}));D=simplified(end-start)
    interval='['+tex(a)+','+tex(b)+']'
    prompt='Let $f(x,y)='+ftext+'.$ Given that $C$ is the path along the curve $'+curve+'$ for $'+variable+r'\in '+interval+r',$ evaluate $\displaystyle\int_C\nabla f\cdot\mathrm{d}\mathbf r.$'
    sol=THEOREM+'We start by parametrizing the curve $C.$ A suitable parametrization is\n\n'+block('r(t)=⟨'+tex(xt)+','+tex(yt)+'⟩,\\,t\\in '+interval+'.')
    sol+='\n\nThen, the position vectors of the endpoints of the curve are given by\n\n'+block(r'\begin{aligned}r('+tex(a)+') & =⟨'+tex(A[0])+','+tex(A[1])+r'⟩, \\ r('+tex(b)+') & =⟨'+tex(B[0])+','+tex(B[1])+r'⟩.\end{aligned}')
    sol+='\n\nApplying the fundamental theorem for line integrals, we have\n\n'
    rows=['f(r('+tex(b)+'))-f(r('+tex(a)+'))','f('+tex(B[0])+','+tex(B[1])+')-f('+tex(A[0])+','+tex(A[1])+')',r'\left('+ev(*B)+r'\right)-\left('+ev(*A)+r'\right)',r'\left('+partial(*B)+r'\right)-\left('+partial(*A)+r'\right)',tex(D)]
    sol+=block(r'\begin{aligned}\int_C\nabla f\cdot\mathrm{d}\mathbf r & ='+rows[0]+''.join(r' \\ & ='+v for v in rows[1:])+r'.\end{aligned}')
    # Complete operation bank: reverse difference; omit the outer coefficient
    # (hard omits both supplied coefficients); apply the coefficient twice;
    # substitute the independent coordinate for the dependent coordinate.
    omitted=(X**3+Y**3)/3 if name=='authored_direct' else X**2+s.exp(X*Y) if name=='authored_inverse' else X**2*Y+X*s.exp(Y)
    omitD=simplified(omitted.subs({X:B[0],Y:B[1]})-omitted.subs({X:A[0],Y:A[1]}))
    wrongB=(B[0],B[0]) if variable=='x' else (B[1],B[1]);wrongA=(A[0],A[0]) if variable=='x' else (A[1],A[1])
    wrongD=simplified(f.subs({X:wrongB[0],Y:wrongB[1]})-f.subs({X:wrongA[0],Y:wrongA[1]}))
    bank=[D,-D,omitD,k*D,wrongD]
    if D==0 or any(simplified(bank[i]-bank[j])==0 for i in range(5) for j in range(i)):
        raise ValueError('Complete authored bank collision; reject whole instance')
    return prompt,sol,[tex(v) for v in bank],0,{'f':f,'xt':xt,'yt':yt,'a':a,'b':b,'A':A,'B':B,'start':start,'end':end,'D':D}

def validate_parameters(name,p):
    required={'scale'} if name in QUESTIONS else {'k','m','c','a','b'}|({'ell','n'} if name=='authored_mixed' else set())
    if set(p)!=required or any(type(v)!=int for v in p.values()):raise ValueError('Exact integer parameter keys required: '+str(sorted(required)))
    if name in QUESTIONS:
        if not 1<=abs(p['scale'])<=12:raise ValueError('Nonzero source coefficient magnitude at most 12')
        return
    if not (2<=p['k']<=6 and 1<=p['m']<=3 and -2<=p['c']<=6 and p['a']<p['b']):raise ValueError('Coefficient/domain bounds')
    if name=='authored_direct':
        if not (-2<=p['a']<=1 and 1<=p['b']<=3):raise ValueError('Easy endpoint bounds')
        if any(abs(p['m']*u*u+p['c'])>8 for u in (p['a'],p['b'])):raise ValueError('Easy dependent endpoints bounded by 8 to retain source cube workload')
    if name=='authored_inverse' and not (p['a'] in (1,4) and p['b'] in (4,9) and 0<=p['c']<=2 and p['m']<=2):raise ValueError('Moderate endpoints must be positive perfect squares, modest coefficients')
    if name=='authored_mixed':
        if not (1<=p['ell']<=4 and 1<=p['n']<=3 and p['a'] in (-2,-1,1) and p['b'] in (1,2,3)):raise ValueError('Hard fixed workload bounds')
        if any((p['c']-p['m']*u)%p['n'] for u in (p['a'],p['b'])):raise ValueError('Hard dependent endpoints must be integers')
        if any(p['c']-p['m']*u==0 for u in (p['a'],p['b'])):raise ValueError('Both hard endpoint y values must be nonzero')
        if any(abs((p['c']-p['m']*u)//p['n'])>4 for u in (p['a'],p['b'])):raise ValueError('Hard endpoint exponents bounded by 4')

def sample(name,rng):
    if name in QUESTIONS:return {'scale':rng.choice([i for i in range(-12,13) if i])}
    p={'k':rng.randint(2,6),'m':rng.randint(1,3),'c':rng.randint(-2,6),'a':rng.choice([-2,-1,0,1]),'b':rng.randint(1,3)}
    if name=='authored_inverse':p.update(m=rng.randint(1,2),c=rng.randint(0,2),a=rng.choice([1,4]),b=rng.choice([4,9]))
    if name=='authored_mixed':p.update(ell=rng.randint(1,4),n=rng.randint(1,3),a=rng.choice([-2,-1,1]))
    return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in DEFAULTS:raise ValueError('Unsupported difficulty')
    name=template or DEFAULTS[level]
    if name not in LEVELS or LEVELS[name]!=level:raise ValueError('Template/difficulty mismatch')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only source radio layout supported')
    expected='observed' if name in QUESTIONS else 'authored_operations'
    if profile not in (None,expected):raise ValueError('Profile/template mismatch')
    profile=expected;rng=random.Random(seed)
    for attempt in range(1000):
        p=dict(parameters) if parameters is not None else sample(name,rng)
        try:
            validate_parameters(name,p)
            prompt,sol,values,ci,data=(source_components if name in QUESTIONS else authored_components)(name,p)
            break
        except ValueError:
            if parameters is not None:raise
    else:raise RuntimeError('Sampler failed to find eligible complete bank')
    mathkey=hash_data({'f':s.srepr(data['f']),'xt':s.srepr(data['xt']),'yt':s.srepr(data['yt']),'a':str(data['a']),'b':str(data['b'])})
    content=hash_data({'version':VERSION,'prompt':prompt,'solution':sol,'values':sorted(values),'correct':values[ci],'field':'radio'})
    qid=uid(content);fid=uid(qid+':selection');ids=[uid(fid+':'+v) for v in values]
    answers=[{':answer/id':i,':answer/type':':answer.type/math',':answer/value':v} for i,v in zip(ids,values)]
    rng.shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',ids[ci]]}]},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':'observed homogeneous residual replay; interpretation underidentified' if name in QUESTIONS else 'authored complete method operations','parameter_fingerprint':mathkey,'mathematical_fingerprint':mathkey,'content_fingerprint':content,'source_analysis':{'database':'math','basis':1356,'lineage':SOURCE['lineage'],'question_ids':[QUESTIONS[name][':question/id']] if name in QUESTIONS else [],'method_reference_ids':['e-9502','q-104626','q-124030']},'authored_extension':name not in QUESTIONS,'plot_rating':'none','plot_assets':{},'source_repair':'q-39749 two zero-start substitution slots corrected to (0,-1)' if name=='q-39749' else None,'mathematics':{z:str(v) for z,v in data.items()}}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    if args.count<1:ap.error('count must be positive')
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (DEFAULTS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
