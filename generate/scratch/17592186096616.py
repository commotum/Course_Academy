#!/usr/bin/env python3
"""Logarithmic tangent-slope generator; bounded easy templates only.

Positive real x; logarithm bases are integers >1. Termwise differentiation,
then evaluation, with no chain/product rule extension. See package evidence.
"""
import argparse, hashlib, json, random, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os,sys
    python=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if python.exists() and Path(sys.executable).resolve()!=python.resolve():
        os.execv(str(python),[str(python),str(Path(__file__).resolve()),*sys.argv[1:]])
    raise
KP_ID=17592186096616
KP_UUID='cef7fc21-23f4-5d6a-a208-9963ef23c784'
TITLE='Calculating the Slope of the Tangent Line of a Logarithmic Function at a Point'
VERSION='logarithmic-tangent-1'
HERE=Path(__file__).with_suffix('')
CASES=json.loads((HERE/'source-cases.json').read_text())
TEMPLATES={c['template']:'easy' for c in CASES}
SUPPORTED_LEVELS=('easy',)
X=sp.Symbol('x',positive=True)
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
GENERATOR_UUID=uid('question-generator')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(v):return sp.latex(v,ln_notation=True)
def case(template):return next(c for c in CASES if c['template']==template)
def bounds(template,p):
    expected=set(case(template)['parameters'])
    if set(p)!=expected or any(type(v)!=int for v in p.values()):raise ValueError('exact integer parameter keys required')
    for k,v in p.items():
        if k=='b':
            if template=='common_log_cubic_radio' and v!=10:raise ValueError('common log remains base 10')
            if template!='common_log_cubic_radio' and not 2<=v<=9:raise ValueError('base range 2..9')
        elif k=='t':
            if template in ('rational_ln_radio','two_logs_radio','ln_quadratic_linear_radio','log_quadratic_linear_blank') and v!=1:raise ValueError('observed input remains one')
            if not 1<=v<=4:raise ValueError('positive integer input range 1..4')
        elif not 1<=v<=12:raise ValueError('coefficient magnitude range 1..12')
    if template=='rational_ln_radio' and (sp.gcd(p['n'],p['d'])!=1 or p['n']==p['d']):raise ValueError('reduced nonunit fraction required')
def sample(template,rng):
    p=dict(case(template)['parameters'])
    for k in p:
        if k=='b':p[k]=10 if template=='common_log_cubic_radio' else rng.randint(2,9)
        elif k=='t':p[k]=1 if template in ('rational_ln_radio','two_logs_radio','ln_quadratic_linear_radio','log_quadratic_linear_blank') else rng.randint(1,4)
        else:p[k]=rng.randint(1,12)
    return p

def terms(template,p):
    """Each term keeps its source position, coefficient sign, and core."""
    a=p.get('a',1);c=p.get('c',1);k=p.get('k',1);b=p.get('b',2)
    logb=sp.log(X)/sp.log(b)
    if template=='rational_ln_radio':return [(-sp.Rational(p['n'],p['d']),sp.log(X))]
    if template=='two_logs_radio':return [(1,logb),(c,sp.log(X))]
    if template=='exp_base_log_fieldless':return [(a,sp.exp(X)),(-c,logb)]
    if template=='quadratic_ln_blank':return [(a,X**2),(c,sp.log(X))]
    if template=='ln_exp_base_blank':return [(a,sp.log(X)),(-c,sp.Integer(b)**X)]
    if template=='negative_exp_log_blank':return [(-a,sp.exp(X)),(c,logb)]
    if template=='log_exp_base_fieldless':return [(a,logb),(1,sp.Integer(b)**X)]
    if template=='linear_log_reciprocal_radio':return [(a,X),(-k,sp.Integer(1)),(c,logb)]
    if template=='ln_quadratic_linear_radio':return [(a,sp.log(X)),(c,X**2),(-k,X)]
    if template=='cubic_log_blank':return [(a,X**3),(-c,logb)]
    if template=='log_quadratic_linear_blank':return [(a,logb),(c,X**2),(-k,X)]
    if template=='exp_log_constant_blank':return [(a,sp.exp(X)),(-c,logb),(k,sp.Integer(1))]
    if template=='common_log_cubic_radio':return [(a,logb),(1,X**3),(-k,sp.Integer(1))]
    raise ValueError('unknown template')
def core_tex(core,p):
    if core==sp.log(X)/sp.log(p.get("b",2)):return r"\log_{"+str(p["b"])+"}x"
    return tex(core)

def join(parts):
    return ''.join(('+' if i and not s.startswith('-') else '')+s for i,s in enumerate(parts))
def signed(c,s):
    if s=='1':return tex(c)
    return ('-' if c<0 else '')+(tex(abs(c))+r'\cdot ' if abs(c)!=1 else '')+s
D=r'\frac{\text{d}}{\text{d}x}'
DY=r'\frac{\text{d}y}{\text{d}x}'
def rows_block(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def render(template,p):
    parts=terms(template,p);f=sum(c*core for c,core in parts);d=sp.diff(f,X)
    t=1/sp.log(p['b']) if template=='linear_log_reciprocal_radio' else sp.Integer(p['t'])
    ans=sp.expand(d.subs(X,t),log=False)
    # Explicit term order is preserved throughout splitting and evaluation.
    fs=join([signed(c,core_tex(core,p)) for c,core in parts])
    ds=join([tex(c*sp.diff(core,X)) for c,core in parts if core!=1])
    meta=case(template)
    if meta['field_type']=='radio' or 'fieldless' in template:
        problem='Given that $y='+fs+'$, find the slope of the tangent at $x='+tex(t)+'.$'
        if meta['field_type']=='blank':problem+='\n\n{{field-1}}'
    else:problem='Given the function $y='+fs+',$ the slope of the tangent line at $x='+tex(t)+'$ is{{field-1}}.'
    n=meta['d_stages']
    if n==1:rows=[DY+'&='+ds+r'\,.']
    else:
        first=DY+'&='+D+'('+fs+')'
        coef=join([('-' if c<0 else '')+D+'('+tex(abs(c))+')' if core==1 else signed(c,D+'('+core_tex(core,p)+')') for c,core in parts])
        calculate=join([('-0' if c<0 else '0') if core==1 else signed(c,'('+tex(sp.diff(core,X))+')') for c,core in parts])
        last='&='+ds+r'\,.'
        if n==3:rows=[first,'&='+calculate,last]
        elif n==4:rows=[first,'&='+coef,'&='+calculate,last]
        else:
            split=join([('-' if c<0 else '')+D+'('+signed(abs(c),core_tex(core,p))+')' for c,core in parts])
            rows=[first,'&='+split,'&='+coef,'&='+calculate,last]
    ev=join([tex(c*sp.diff(core,X)).replace('x','('+tex(t)+')') for c,core in parts if core!=1])
    reduced=join([tex(c*sp.diff(core,X).subs(X,t)) for c,core in parts if core!=1])
    evalrows=[DY+r'\big|_{x='+tex(t)+r'}&=\left('+ds+r'\right)\big|_{x='+tex(t)+'}']
    if meta['eval_stages']>=3:evalrows.append('&='+ev)
    if meta['eval_stages']==4:evalrows.append('&='+reduced)
    evalrows.append('&='+tex(ans)+r'\,.')
    solution=('To find the slope of the tangent at a given point, we have to find $'+DY+'$ at that point.\n\nTaking the derivative, we have\n\n'+rows_block(rows)+'\n\nTherefore, the slope of the tangent at $x='+tex(t)+'$ is\n\n'+rows_block(evalrows))
    return problem,solution,f,d,t,ans

def bank(template,p,ans):
    a=p.get('a',1);c=p.get('c',1);k=p.get('k',1);b=p.get('b',2);t=p.get('t',1)
    if template=='rational_ln_radio':
        r=sp.Rational(p['n'],p['d']);return [-1/r,sp.Integer(0),r,-r,1/r]
    if template=='two_logs_radio':return [1/sp.log(b),sp.log(b)+c,sp.Integer(0),c/sp.log(b),ans]
    if template=='linear_log_reciprocal_radio':return [a+1,a+c*sp.log(b),ans,c*sp.log(b)+a-k,a+c-k]
    if template=='ln_quadratic_linear_radio':return [ans,-a,-ans,a+2*c+k,-k]
    if template=='common_log_cubic_radio':return [a*t/sp.log(b)-t,ans,sp.Rational(a,t*t)/sp.log(b)+t,sp.Rational(a,t)/sp.log(b)-t*t,a/sp.log(b)+t*t]
    return [ans]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level!='easy':raise ValueError('Unsupported bounded package level: '+level+'; see capabilities.json')
    rng=random.Random(seed)
    eligible=[c['template'] for c in CASES if field_type is None or field_type==c['field_type']]
    template=template or rng.choice(eligible);meta=case(template)
    if field_type is not None and field_type!=meta['field_type']:raise ValueError('field/template mismatch')
    if profile not in (None,meta['source_id'],'observed','normal'):raise ValueError('complete profile/template mismatch')
    for _ in range(200):
        p=dict(parameters) if parameters is not None else sample(template,rng)
        try:bounds(template,p)
        except ValueError:
            if parameters is not None:raise
            continue
        problem,solution,f,d,t,ans=render(template,p);values=[sp.sympify(v) for v in bank(template,p,ans)]
        if any(sp.simplify(u-v)==0 for i,u in enumerate(values) for v in values[i+1:]):
            if parameters is not None:raise ValueError('complete profile collides')
            continue
        break
    else:raise ValueError('bounded bank sampler exhausted')
    correct=next(i for i,v in enumerate(values) if sp.simplify(v-ans)==0)
    strings=[tex(v) for v in values]
    if meta.get('aliases')==2:strings.append(tex(ans).replace(r'\ln',r'\operatorname{ln}'))
    identity=digest([template,p,strings,VERSION]);qid=uid('question/'+identity);fid=uid(qid+'/'+meta['key'])
    answers=[{':answer/id':uid(fid+'/'+s),':answer/type':':answer.type/math',':answer/value':s} for s in strings]
    cid=answers[correct][':answer/id'];rng.shuffle(answers)
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':meta['key'],':answer-field/type':':answer-field.type/'+meta['field_type'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]}
    repairs=[]
    if not meta['observed_level']:repairs+=['legacy easy classification; mathematically recovered correct ref; authored missing solution']
    if 'fieldless' in template:repairs+=['authored blank field for fieldless source; source preserved']
    if meta['source_id']=='q-70903':repairs+=['source solution prose says x=1, whereas prompt and calculation use x=3; normal solution uses actual input']
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':template,'profile':meta['source_id'],'source_ids':[meta['source_id']],'seed':seed,'parameters':p,'domain':'x>0; logarithm base>1','dependencies':{'sympy':sp.__version__},'mathematical_fingerprint':digest([sp.srepr(sp.simplify(d)),sp.srepr(t)]),'repairs':repairs,'fidelity':'same ordered term structure, field shape, complete observed bank mathematics, derivative/evaluation stage counts; standardized TeX components','plots':[]}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def batch(level,count,seed):
    records=[];seen=set()
    for i in range(max(100,count*100)):
        if len(records)>=count:break
        r=generate(level,seed+i,template=CASES[i%len(CASES)]['template']);fp=r['generation']['mathematical_fingerprint']
        if fp not in seen:records.append(r);seen.add(fp)
    if len(records)!=count:raise ValueError('bounded distinct sampler limit; requested count not filled')
    return records
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='easy');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');args=ap.parse_args()
    records=[generate(args.difficulty,args.seed+i,args.template) for i in range(args.count)] if args.template else batch(args.difficulty,args.count,args.seed)
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);print('\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']));print(q[':question/worked-solution'])
