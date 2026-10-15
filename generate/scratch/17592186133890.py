#!/usr/bin/env python3
"""Supplied-potential FTLI on Cartesian curves, immutable math basis 1356.

Twelve observed families preserve their distinct source arithmetic rows and all
five options. `observed` is a homogeneous coefficient replay: each captured
potential and each complete bank are multiplied by the same nonzero scale. This
is not a recovered distractor theory. Authored defaults use complete operations
and vary Cartesian curves, coefficients and endpoints at fixed workload.
Public generation supports observed easy/moderate families only. Hard is unsupported.
No database clients, registrations, plots, or writes outside this KP are used.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
KP_ID=17592186133890
KP_UUID='c4519f3b-0fb8-54fd-9e9e-fca3e599b80b'
TITLE='Applying the Fundamental Theorem of Line Integrals Over Cartesian Curves'
VERSION='cartesian-ftli-2-observed'
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
SUPPORTED_LEVELS=('easy','moderate')
DEFAULTS={'easy':'q-104626','moderate':'q-124030'}
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

def validate_parameters(name,p):
    required={'scale'}
    if set(p)!=required or any(type(v)!=int for v in p.values()):raise ValueError('Exact integer parameter keys required: '+str(sorted(required)))
    if name in QUESTIONS:
        if not 1<=abs(p['scale'])<=12:raise ValueError('Nonzero source coefficient magnitude at most 12')
        return

def sample(name,rng):
    if name in QUESTIONS:return {'scale':rng.choice([i for i in range(-12,13) if i])}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in DEFAULTS:raise ValueError('Unsupported difficulty: hard has no observed source family; see capabilities.json')
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
            prompt,sol,values,ci,data=source_components(name,p)
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
    if args.difficulty=='hard':ap.error('hard is unsupported; see capabilities.json')
    records=[]
    for level in (DEFAULTS if args.difficulty=='all' else [args.difficulty]):
        templates=[args.template] if args.template else [name for name in QUESTIONS if LEVELS[name]==level]
        candidates=[(name,k) for name in templates for k in range(-12,13) if k]
        random.Random(args.seed).shuffle(candidates);used=set();selected=[]
        for name,k in candidates:
            r=generate(level,args.seed,template=name,parameters={'scale':k},profile=args.profile)
            fp=r['generation']['mathematical_fingerprint']
            if fp in used:continue
            used.add(fp);selected.append(r)
            if len(selected)==args.count:break
        if len(selected)<args.count:ap.error(f'finite variant limit for {level}: {len(selected)} distinct questions')
        records.extend(selected)
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
