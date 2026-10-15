#!/usr/bin/env python3
"""Cosecant derivatives: eight source families, exact finite bounded parameterization.

Easy: source sums, no chain rule. Moderate: one product of csc(x) with a
linear/log/exponential factor. Hard: differentiate a sum then evaluate at a
familiar angle. Complete profiles are selected before their parameter domain.
Evidence profiles preserve missing fields/keys/solutions and the known formal
operand typo; they are explicitly ineligible. No database access or writes.
"""
from __future__ import annotations
import argparse,copy,hashlib,importlib.util,itertools,json,random,sys,uuid
from pathlib import Path
import sympy as sp
D=Path(__file__).with_suffix('')
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
FMT=load('csc_frozen_format',D/'frozen_math_format.py')
PARSER=load('csc_frozen_parser',D/'frozen_parser.py')
VERSION='csc-source-families-v1'
KP_ID=17592186115190
KP_UUID='bbb56f0a-ead0-5794-9e33-7fe0e1f87dc6'
TITLE='Differentiating Expressions Involving the Cosecant Function'
SOURCE=json.loads((D/'source.json').read_text())
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
MASKS=json.loads((D/'templates.json').read_text())
LEVELS={'q-1889':'easy','q-31283':'easy','q-104316':'moderate','q-313722':'moderate','q-105298':'hard','q-105299':'moderate','q-313723':'hard','q-340582':'moderate'}
ANCHORS={'q-1889':{'c':2},'q-31283':{'c':6},'q-104316':{'c':1},'q-313722':{'c':4},'q-105298':{'c':5},'q-105299':{'b':2},'q-313723':{'c':2},'q-340582':{'c':1}}
KINDS={'q-1889':'radio','q-31283':'radio','q-104316':'blank','q-313722':'blank','q-105298':'radio','q-105299':'radio','q-313723':'blank','q-340582':'blank'}
CORRECT_INDEX={'q-1889':0,'q-31283':4,'q-105298':4,'q-105299':2}
ANGLES=(sp.pi/6,sp.pi/4,sp.pi/3,2*sp.pi/3,3*sp.pi/4,5*sp.pi/6)
x=PARSER.x
SUM='We take the derivative of each term and then add them, as follows:'
PRODUCT='We calculate the derivative using the product rule, as follows:'
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(o):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(o)))
def tex(z):return sp.latex(z).replace(r'\log',r'\ln')
def equivalent(a,b):return sp.simplify(sp.trigsimp(sp.expand(a-b),method='fu'))==0

def parameters_domain(template,profile='observed'):
    """Full explicit finite domain, identical for sampler and explicit requests."""
    if template not in LEVELS:raise ValueError('unknown template')
    if profile not in ('observed','evidence','authored-evaluation'):raise ValueError('unknown profile')
    if profile=='authored-evaluation':
        if template!='q-105298':raise ValueError('authored-evaluation applies only to q-105298')
        return tuple({'c':c,'angle':str(a)} for c in range(1,25) for a in ANGLES)
    if template=='q-105299':return tuple({'b':b} for b in range(2,13))
    # c=1 in this historical hard bank merges 2c/pi and the correct 2/pi.
    return tuple({'c':c} for c in range(2 if template=='q-105298' else 1,25))

def validate_parameters(t,profile,p):
    if not isinstance(p,dict):raise ValueError('parameters must be a dictionary')
    allowed=parameters_domain(t,profile)
    if any(type(v) is not int for k,v in p.items() if k!='angle'):raise ValueError('integer parameter required; bool rejected')
    if 'angle' in p and type(p['angle']) is not str:raise ValueError('angle must be an exact domain string')
    if p not in allowed:raise ValueError('parameters outside the complete bounded same-method domain')
    return dict(p)

def instantiate(t,p):
    c=p.get('c',1);b=p.get('b',2)
    values={'c':str(c),'b':str(b),'twoc':str(2*c),'threec':str(3*c),'pc':tex(sp.Rational(3*c,16))}
    def sub(v):
        if isinstance(v,str):
            for k,z in values.items():v=v.replace('@'+k+'@',z)
            if '@' in v:raise ValueError('unexpanded slot')
            return v
        if isinstance(v,list):return [sub(a) for a in v]
        return {k:sub(z) for k,z in v.items()}
    m=sub(MASKS[t])
    # Whole mathematical factor slots; never replace a variable letter in prose.
    if t=='q-104316':
        scalar='' if c==1 else str(c)
        for k in (':question/problem',':question/worked-solution'):m[k]=m[k].replace('{e}^{x}',scalar+'{e}^{x}')
    if t=='q-340582' and c!=1:
        for k in (':question/problem',':question/worked-solution'):
            m[k]=m[k].replace('ln⁡(x)',str(c)+'ln⁡(x)').replace(r'\frac{1}{x}',r'\frac{'+str(c)+'}{x}').replace(r'\frac{csc⁡(x)}{x}',r'\frac{'+str(c)+'csc⁡(x)}{x}')
        m['choices']=[v.replace(r'\frac{\operatorname{csc}(x)}{x}',r'\frac{'+str(c)+r'\operatorname{csc}(x)}{x}').replace(r'\operatorname{ln}(x)',str(c)+r'\operatorname{ln}(x)') for v in m['choices']]
    return m

def normal_notation(s):
    # Normalize legacy invisible function-application glyphs to proper commands.
    import re
    s=re.sub(r'(?<!\\)(csc|cot|cos|sin|ln)(?:⁡|(?=\\,))',lambda m:'\\'+m[1]+' ',s)
    s=s.replace(r'\begin{aligned}\begin{aligned}',r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}',r'\end{aligned}')
    return s

def aligned(name,rows):
    return '$$\n'+r'\begin{aligned}'+name+' & ='+rows[0]+''.join(r' \\  & ='+z for z in rows[1:])+r'\end{aligned}'+'\n$$'

def authored_evaluation(p):
    """Hard extension: same derivative/substitute/evaluate/collect sequence."""
    c=p['c'];a=sp.sympify(p['angle']);aT=tex(a);C=sp.csc(x)*sp.cot(x)
    f=sp.log(x)-c*sp.csc(x);der=1/x+c*C;answer=sp.simplify(der.subs(x,a))
    prompt=f"Find $f'({aT})$ if $f(x)=\\ln x-{c}\\csc x$."
    rows=[r'\frac{\text{d}}{\text{d}x}(\ln x-'+str(c)+r'\csc x)',r'\frac{1}{x}-'+str(c)+r'(-\csc x\cot x)',r'\frac{1}{x}+'+str(c)+r'\csc x\cot x']
    sol=SUM+'\n\n'+aligned("f'(x)",rows)
    sol+='\n\nThen, we substitute $x='+aT+'$ in the derivative and get\n\n'
    rows=[r'\frac{1}{('+aT+')}+'+str(c)+r'\csc('+aT+r')\cot('+aT+')',tex(1/a)+'+'+str(c)+r'\cdot ('+tex(sp.csc(a))+r')\cdot ('+tex(sp.cot(a))+')',tex(answer)+'.']
    sol+=aligned("f'("+aT+')',rows)
    # Complete method-derived bank selected before sampling: correct, opposite csc
    # sign, omit csc term, omit log term, confuse csc derivative with cot derivative.
    vals=[answer,1/a-c*sp.csc(a)*sp.cot(a),1/a,c*sp.csc(a)*sp.cot(a),1/a+c*sp.csc(a)**2]
    return {':question/problem':prompt,':question/worked-solution':sol,'choices':[tex(sp.simplify(z)) for z in vals]},0

# Easy section: sum-rule masks; q1889's level and solution completion are authored.
# Moderate section: exactly one source product-rule application; no inner chain.
# Hard section: source derivative followed by familiar-angle substitution; no tangent.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if type(seed) is not int:raise ValueError('integer seed required')
    rng=random.Random(seed)
    eligible=[t for t,l in LEVELS.items() if l==level and (field_type is None or field_type==KINDS[t]) and (profile!='authored-evaluation' or t=='q-105298')]
    if template is None:
        if not eligible:raise ValueError('no matching family')
        template=rng.choice(eligible)
    if template not in eligible:raise ValueError('template/field_type incompatible with difficulty')
    t=template
    if profile is None:profile='authored-evaluation' if t=='q-105298' else 'observed'
    domain=parameters_domain(t,profile)
    p=validate_parameters(t,profile,parameters if parameters is not None else rng.choice(domain))
    m=instantiate(t,p);raw=profile=='evidence'
    ci=CORRECT_INDEX.get(t,0)
    if profile=='authored-evaluation':m,ci=authored_evaluation(p)
    if not raw:
        if t=='q-1889':
            c=p['c'];m[':question/worked-solution']=SUM+'\n\n'+aligned("f'(x)",[r'\frac{\text{d}}{\text{d}x}(\csc x+'+str(c)+r'\tan x-\cos x)',r'(-\csc x\cot x)+'+str(c)+r'\sec^2 x-(-\sin x)',str(c)+r'\sec^2 x-\csc x\cot x+\sin x'])
        if t=='q-104316':
            a='' if p['c']==1 else str(p['c'])
            m['choices']=[a+r'e^x\csc x(1-\cot x)'];m[':question/problem']+="\n\n$f'(x)=$\n{{field-1}}"
        if t=='q-313723':m[':question/worked-solution']=m[':question/worked-solution'].replace(r'\text{d}x}(-csc',r'\text{d}x}(csc')
        for k in (':question/problem',':question/worked-solution'):m[k]=normal_notation(m[k])
        m['choices']=[normal_notation(v) for v in m['choices']]
        for k in (':question/problem',':question/worked-solution'):m[k]=FMT.normalize_prose(m[k])
        m['choices']=[FMT.normalize_tex(v) for v in m['choices']]
    # Content identity ignores source alias, option order and seed; includes difficulty,
    # actual prompt, fixed solution and complete bank. Parameter spelling is immaterial.
    body={k:v for k,v in m.items() if k!='choices'}
    qid=uid([VERSION,level,body,sorted(m['choices']),KINDS[t]])
    q={':question/id':qid,**body}
    original=ORIGINALS[t]
    if not raw or ':question/difficulty' in original:q[':question/difficulty']=':question.difficulty/'+level
    if not raw or ':question/answer-fields' in original:
        key=original.get(':question/answer-fields',[{':answer-field/key':'field-1'}])[0][':answer-field/key']
        fid=uid([qid,key]);choices=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in m['choices']]
        f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+KINDS[t],':answer-field/choices':choices}
        if not raw or ':answer-field/correct' in original.get(':question/answer-fields',[{}])[0]:f[':answer-field/correct']=[':answer/id',choices[ci][':answer/id']]
        rng.shuffle(choices);q[':question/answer-fields']=[f]
    fun,at=read_given(q[':question/problem'])
    answer=sp.diff(fun,x) if at is None else sp.simplify(sp.diff(fun,x).subs(x,at))
    # A canonical assessed task excludes profiles/banks and incidental notation.
    task=digest(['differentiate-csc',sp.srepr(fun),sp.srepr(at),KINDS[t]])
    if t=='q-105298' and profile!='authored-evaluation':task=digest(['differentiate-log-minus-scaled-csc-evaluate',str(sp.pi/2)])
    constraints='Real x in a connected pole-free interval (k*pi,(k+1)*pi), integer k, sin(x) != 0.'
    if t=='q-1889':constraints='Real x in a connected component excluding sin(x)=0 and cos(x)=0; sin(x) != 0 and cos(x) != 0.'
    if t in ('q-340582','q-105298'):constraints+=' Require x > 0; intersect with the indicated interval.'
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':profile,'bank_profile':profile,'parameters':p,'source_basis':SOURCE['basis'],'source_question':t,'domain':constraints,'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_key':task,'parameter_fingerprint':task,'answer_math':str(answer),'authored_completion':t in ('q-1889','q-104316'),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
    if not raw:FMT.validate_generated_record(record)
    return record

def read_given(problem):
    import re
    m=re.search(r'\$([fgh])\(x\)\s*=\s*(.*?)\$',problem);assert m,problem
    fun=PARSER.scalar(m[2]);first=re.search(r"Find \$.*?\((.*?)\)\$",problem)
    # Read the requested derivative argument, including braced legacy prime labels.
    requested=first[1] if first else 'x'
    at=None if requested=='x' else PARSER.scalar(requested)
    return fun,at

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def batch(level,count,seed=0,template=None,profile=None):
    if type(count) is not int or count<1:raise ValueError('positive integer count required')
    rng=random.Random(seed);candidates=[]
    for t,l in LEVELS.items():
        if l!=level or template not in (None,t) or (profile=='authored-evaluation' and t!='q-105298'):continue
        pr=profile or ('authored-evaluation' if t=='q-105298' else 'observed')
        for p in parameters_domain(t,pr):candidates.append((t,pr,p))
    rng.shuffle(candidates);out=[];seen=set()
    for t,pr,p in candidates:
        r=generate(level,seed,template=t,profile=pr,parameters=p);key=r['generation']['mathematical_key']
        if key not in seen:out.append(r);seen.add(key)
        if len(out)==count:return out
    raise ValueError(f'finite-limit: requested {count}, only {len(out)} distinct mathematical tasks')
def markdown(r):
    q=r['question'];s=q[':question/problem']
    for f in q.get(':question/answer-fields',[]):
        s+='\n\n'+ '\n'.join('$'+a[':answer/value']+'$'+(' [correct]' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices'])
    return s+'\n\n'+q.get(':question/worked-solution','[Original worked solution absent]')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
    try:rows=[r for l in (('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)) for r in batch(l,a.count,a.seed,a.template,a.profile)]
    except ValueError as e:p.error(str(e))
    print(json.dumps(rows,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
