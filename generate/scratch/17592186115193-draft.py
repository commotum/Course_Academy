#!/usr/bin/env python3
"""Draft reciprocal-trigonometric tangent slopes; registered numeric pair immutable.

Easy sums, moderate original sum/product/quotient families, and a missing hard
family grounded in canonical e3648's trig/trig quotient. Frozen source masks
preserve every practice chain/bank; raw evidence retains missing attributes.
No database, registry or shared runtime mutations.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import argparse,copy,functools,hashlib,importlib.util,itertools,json,random,re,uuid
from pathlib import Path
import sympy as s
D=Path(__file__).with_suffix('')
def load(name,path):
    z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
F=load('slope_draft_frozen_format',D/'frozen_math_format.py')
P=load('slope_draft_frozen_parser',D/'frozen_parser.py');x=P.x
VERSION='reciprocal-trig-slopes-draft-v1'
KP_ID=17592186115193
KP_UUID='7995b377-1de4-5126-aa29-8cc30b4918f8'
TITLE='Finding the Slope of the Tangent at a Point of a Function Involving Reciprocal Trigonometric Functions'
SOURCE=json.loads((D/'source.json').read_text());ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
MASKS=json.loads((D/'templates.json').read_text())
LEVELS={t:q[':question/difficulty'][':db/ident'].rsplit('/',1)[1] for t,q in ORIGINALS.items()};LEVELS['canonical-quotient']='hard'
KINDS={t:('radio' if t in ('q-1886','q-1905','q-104442','q-1904','q-70874') else 'blank') for t in LEVELS}
ANCHORS={'q-1886':{'a':11},'q-1905':{'a':2},'q-104437':{'a':1},'q-340642':{'a':1},'q-104442':{'a':3},'q-1904':{'a':5},'q-340630':{'a':1},'q-340660':{'a':4},'q-70874':{'a':3}}
CORRECT_INDEX={'q-1886':1,'q-1905':3,'q-104442':3,'q-1904':4,'q-70874':1}
ANGLES=('pi/6','pi/4','pi/3')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(v):return s.latex(v).replace(r'\log',r'\ln')
def pi_fraction(a,den):
    c=s.Rational(a,den);n=int(c.p);d=int(c.q);num=('' if n==1 else str(n))+r'\pi '
    return num if d==1 else r'\frac{'+num+'}{'+str(d)+'}'
def default_profile(t):return 'authored-bank' if t=='q-1905' else 'authored-hard' if t=='canonical-quotient' else 'observed'
def profiles(t):return ('observed','authored-bank','evidence') if t=='q-1905' else ('authored-hard',) if t=='canonical-quotient' else ('observed','evidence')
def parameters_domain(t,profile=None):
    profile=profile or default_profile(t)
    if t not in LEVELS or profile not in profiles(t):raise ValueError('incompatible template/profile')
    if t=='canonical-quotient':return tuple({'a':a,'angle':p} for a in range(1,25) for p in ANGLES)
    return tuple({'a':a} for a in range(2 if t=='q-1886' else 1,25))
def strict_parameters(t,profile,p):
    if not isinstance(p,dict) or any(type(v) is not int for k,v in p.items() if k!='angle'):raise ValueError('strict integer coefficients required; bool rejected')
    if 'angle' in p and type(p['angle']) is not str:raise ValueError('exact angle domain string required')
    if p not in parameters_domain(t,profile):raise ValueError('parameters outside bounded same-level domain')
    return dict(p)

def normal_math(t):
    # Operate inside mathematical components only; adjacent xsec/cot tokens are
    # function factors, while operatorname braces are protected by conversion.
    t=re.sub(r'\\operatorname\{(sin|cos|tan|sec|csc|cot|ln)\}',lambda m:'\\'+m[1]+' ',t)
    t=re.sub(r'\{(sin|cos|tan|sec|csc|cot|ln)\}',lambda m:'\\'+m[1],t)
    t=re.sub(r'(?<!\\)(sin|cos|tan|sec|csc|cot|ln)(?:⁡|(?=x|\\,|\(|[0-9]))',lambda m:'\\'+m[1]+' ',t)
    return t.replace('⁡','')
def normal_prose(t):
    t=t.replace(r'\begin{aligned}\begin{aligned}',r'\begin{aligned}').replace(r'\end{aligned}\end{aligned}',r'\end{aligned}')
    def math(m):
        z=m[0];n=2 if z.startswith(('$$',r'\[',r'\(')) else 1
        return z[:n]+normal_math(z[n:-n])+z[-n:]
    return F.normalize_prose(F.MATH.sub(math,t))
def source_instance(t,p):
    a=p['a'];v={'a':str(a),'factor':'' if a==1 else str(a),'twice':str(2*a),'halfpi':pi_fraction(a,2),'qpart':tex(s.Rational(2*a,3)),'negqpart':tex(-s.Rational(2*a,3)),'correct':str(a-2) if t=='q-1905' else tex(2+s.Rational(2*a,3)),'plus':str(a+2),'difference':tex(2-s.Rational(2*a,3)),'negative':tex(-2-s.Rational(2*a,3))}
    def sub(z):
        if isinstance(z,str):
            for k,val in v.items():z=z.replace('@'+k+'@',val)
            if '@' in z:raise ValueError('unexpanded source mask')
            return z
        if isinstance(z,list):return [sub(k) for k in z]
        return {k:sub(val) for k,val in z.items()}
    return sub(MASKS[t])

def hard_instance(p):
    """Authored hard: canonical quotient, same four derivative/evaluation stages."""
    a=p['a'];at=s.sympify(p['angle']);A=tex(at)
    prompt='Find the slope $m$ of $y=f(x)$ at $x='+A+r'$ if $f(x)=\frac{-'+str(a)+r'\cot x}{\sin x}.$'+'\n\n$m=$\n{{field-1}}'
    # Same canonical numerator/denominator, formal quotient, substitution,
    # reciprocal identity reduction, familiar-angle evaluation and collection.
    s1=r'\frac{\text{d}}{\text{d}x}(\frac{-'+str(a)+r'\cot x}{\sin x})'
    s2=r'\frac{\frac{\text{d}}{\text{d}x}(-'+str(a)+r'\cot x)\cdot \sin x-(-'+str(a)+r'\cot x)\cdot \frac{\text{d}}{\text{d}x}(\sin x)}{[\sin x]^2}'
    s3=r'\frac{-'+str(a)+r'(-\csc^2 x)\cdot \sin x+'+str(a)+r'\cot x\cdot (\cos x)}{\sin^2 x}'
    s4=r'\frac{'+str(a)+r'\csc x+'+str(a)+r'\cot x\cos x}{\sin^2 x}'
    def aligned(label,rows):return '$$\n'+r'\begin{aligned}'+label+' & ='+rows[0]+''.join(r' \\  & ='+z for z in rows[1:])+r'\end{aligned}'+'\n$$'
    sol='First, we calculate the derivative using the quotient rule:\n\n'+aligned("f'(x)",[s1,s2,s3,s4])
    sol+='\n\nThen, we substitute $x='+A+'$ in the derivative and get\n\n'
    csc,cot,cos,sin=(fn(at) for fn in (s.csc,s.cot,s.cos,s.sin));num=s.simplify(a*csc+a*cot*cos);den=s.simplify(sin**2);answer=s.simplify(num/den)
    r1=r'\frac{'+str(a)+r'\csc('+A+')+'+str(a)+r'\cot('+A+r')\cos('+A+r')}{\sin^2('+A+')}'
    r2=r'\frac{'+str(a)+r'\cdot ('+tex(csc)+')+'+str(a)+r'\cdot ('+tex(cot)+r')\cdot ('+tex(cos)+r')}{('+tex(sin)+')^2}'
    r3=r'\frac{'+tex(num)+'}{('+tex(den)+')}'
    sol+=aligned("f'("+A+')',[r1,r2,r3,tex(answer)+'.'])
    return {':question/problem':prompt,':question/worked-solution':sol,'choices':[tex(answer)]}

# Easy: five observed sum families; fixed familiar source angles and term counts.
# Moderate: observed reciprocal sum, linear*cot, csc*cot and linear/sec quotient.
# Hard: authored canonical quotient at pi/6, pi/4, pi/3; both trig factors vary.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard') or type(seed) is not int:raise ValueError('difficulty and strict integer seed required')
    rng=random.Random(seed);eligible=[t for t,l in LEVELS.items() if l==level and (field_type is None or field_type==KINDS[t]) and (profile is None or profile in profiles(t))]
    if template is None:
        if not eligible:raise ValueError('no matching template/profile')
        template=rng.choice(eligible)
    if template not in eligible:raise ValueError('template/profile/field/difficulty mismatch')
    t=template;pr=profile or default_profile(t);p=strict_parameters(t,pr,parameters if parameters is not None else rng.choice(parameters_domain(t,pr)));raw=pr=='evidence'
    m=hard_instance(p) if t=='canonical-quotient' else source_instance(t,p);ci=CORRECT_INDEX.get(t,0)
    if t=='q-1905' and pr=='authored-bank':
        a=p['a'];m['choices']=[tex(z) for z in (a-2,a+2,a-s.sqrt(2),a-2*s.sqrt(2),a*s.pi/4-2)];ci=0
    if not raw:
        if t=='q-104437':
            m['choices']=[tex(p['a']*(1-s.pi/2))];m[':question/problem']+='\n\n$m=$\n{{field-1}}'
        for k in (':question/problem',':question/worked-solution'):m[k]=normal_prose(m[k])
        m['choices']=[F.normalize_tex(normal_math(v)) for v in m['choices']]
    body={k:v for k,v in m.items() if k!='choices'}
    qid=uid([VERSION,level,body,sorted(m['choices']),KINDS[t]]);q={':question/id':qid,**body,':question/difficulty':':question.difficulty/'+level}
    original=ORIGINALS.get(t,{})
    if not raw or ':question/answer-fields' in original:
        key=original.get(':question/answer-fields',[{':answer-field/key':'field-1'}])[0][':answer-field/key'];fid=uid([qid,key]);choices=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in m['choices']]
        f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+KINDS[t],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]};rng.shuffle(choices);q[':question/answer-fields']=[f]
    name,fun,at=read_given(q[':question/problem']);answer=s.simplify(s.diff(fun,x).subs(x,at))
    task=digest(['slope-at-point',s.srepr(fun),s.srepr(at)])
    opaque=t=='q-1905' and pr=='observed'
    domain='Real x on the connected pole-free component containing '+str(at)+'; '
    restrictions=[]
    if fun.has(s.sec,s.tan) or t=='q-340660':restrictions.append('cos(x) != 0')
    if fun.has(s.csc,s.cot) or t=='canonical-quotient':restrictions.append('sin(x) != 0')
    if t=='q-1886':restrictions.append('x != 0')
    if t=='q-70874':restrictions.append('x > 0')
    domain+=', '.join(restrictions)+'.'
    r={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':pr,'bank_profile':pr,'parameters':p,'source_basis':SOURCE['basis'],'source_question':'e-3648' if t=='canonical-quotient' else t,'domain':domain,'evidence_only':raw or opaque,'eligible_for_learning':not(raw or opaque),'raw_evidence':raw,'opaque_source_bank':opaque,'authored_completion':t=='q-104437','authored_extension':t=='canonical-quotient' or pr=='authored-bank','mathematical_key':task,'parameter_fingerprint':task,'answer_math':str(answer),'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}
    if not raw:F.validate_generated_record(r)
    return r

def read_given(prompt):
    m=re.search(r'\$([fgh])\(x\)\s*=\s*(.*?)\$',prompt);assert m,prompt
    at=re.search(r'\$x\s*=\s*(.*?)\$',prompt);assert at,prompt
    return m[1],P.scalar(m[2]),P.scalar(at[1])
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def batch(level,count,seed=0,template=None,profile=None):
    if type(count) is not int or count<1:raise ValueError('positive integer count required')
    if type(seed) is not int:raise ValueError('strict integer seed required')
    rng=random.Random(seed);candidates=[]
    for t,l in LEVELS.items():
        if l!=level or template not in (None,t) or profile is not None and profile not in profiles(t):continue
        pr=profile or default_profile(t)
        for p in parameters_domain(t,pr):candidates.append((t,pr,p))
    rng.shuffle(candidates);out=[];seen=set()
    for t,pr,p in candidates:
        r=generate(level,seed,template=t,profile=pr,parameters=p);key=r['generation']['mathematical_key']
        if key not in seen:out.append(r);seen.add(key)
        if len(out)==count:return out
    raise ValueError(f'finite-limit: requested {count}, only {len(out)} distinct tasks')
def markdown(r):
    q=r['question'];body=q[':question/problem']
    for f in q.get(':question/answer-fields',[]):body+='\n\n'+'\n'.join('$'+a[':answer/value']+'$'+(' [correct]' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])
    return body+'\n\n'+q.get(':question/worked-solution','[Source solution absent]')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='json');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
    try:rows=[r for l in (('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)) for r in batch(l,a.count,a.seed,a.template,a.profile)]
    except ValueError as e:p.error(str(e))
    print(json.dumps(rows,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
