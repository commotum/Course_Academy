#!/usr/bin/env python3
"""Integrating secant squared, local unregistered draft at immutable basis2275.

Easy: a single sec² primitive with a signed integer/reduced fraction coefficient.
Moderate: observed two-term direct primitives, with optional source distribution.
Hard: authored three-term direct primitives with that SAME distribution/sum rule;
no substitution, identities, changed trig arguments, definite integrals or branches.
Raw profiles preserve missing fields, difficulty, keys and solutions publicly.
"""
import argparse,copy,hashlib,itertools,json,random,re,sys,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.question_capture.math_format import normalize_prose,normalize_tex,validate_generated_record
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
KP_ID=17592186064180
KP_UUID='caf358b8-31fb-5587-8663-f414317c42be'
TITLE='Integrating Secant Squared'
VERSION='2.0.0-draft'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCE_BASIS=SOURCE['basis'];LINEAGE=SOURCE['lineage']
SOURCE_PROFILES=json.loads((HERE/'source-profiles.json').read_text())
SUPPORTED_LEVELS=('easy','moderate','hard')
DEFAULTS={'easy':('q-113936','q-113937','fraction','single-positive'),
          'moderate':('q-113944','q-2164','q-49122','sine-sum','secant-difference','reverse-product'),
          'hard':('three-term-plus','three-term-minus')}
TEMPLATES={k:{'difficulty':v,'provenance':'observed source family or explicitly authored completion'} for v,ks in DEFAULTS.items() for k in ks}
SUPPORTED_PROFILES=tuple(TEMPLATES)

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def expression(text):
    """Small exact source-notation reader, accepting raw/source and standard TeX."""
    text=re.sub(r'\\operatorname\{(sin|cos|sec|csc|tan|cot)\}',r'\1',text)
    text=text.replace('⁡','').replace(r'\theta','theta').replace('θ','theta')
    text=re.sub(r'\\(sin|cos|sec|csc|tan|cot)',r'\1',text)
    text=re.sub(r'\{(sin|cos|sec|csc|tan|cot)\}\^\{(\d+)\}',r'\1**\2',text)
    text=re.sub(r'(sin|cos|sec|csc|tan|cot)\^\{(\d+)\}',r'\1**\2',text)
    text=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',text)
    text=re.sub(r'(sin|cos|sec|csc|tan|cot)\{(theta|x|y|t|z)\}',r'\1(\2)',text)
    text=re.sub(r'(sin|cos|sec|csc|tan|cot)\^(\d+)',r'\1**\2',text)
    text=text.replace(r'\,','').replace(r'\left','').replace(r'\right','').strip().lstrip('}').rstrip('.,')
    text=re.sub(r'(sin|cos|sec|csc|tan|cot)(?:\*\*(\d+))?\s*(theta|x|y|t|z)',lambda m:m[1]+'('+m[3]+')'+('**'+m[2] if m[2] else ''),text)
    local={n:sp.Symbol(n,real=True) for n in ('x','y','z','t','theta','C')}
    local.update({n:getattr(sp,n) for n in ('sin','cos','sec','csc','tan','cot')})
    return parse_expr(text,local_dict=local,transformations=standard_transformations+(implicit_multiplication_application,))

def reduced(expression):
    """Exact trig rational reduction modulo sin(v)^2+cos(v)^2=1.

    All accepted expressions are rational combinations of six trig functions
    at a fixed variable. Poles are excluded by the recorded instance domain.
    """
    substitutions, circles = {}, []
    args = sorted({f.args[0] for f in expression.atoms(sp.Function)}, key=str)
    for v in args:
        sine, cosine = sp.Symbol('_sin_' + str(v)), sp.Symbol('_cos_' + str(v))
        substitutions.update({sp.sin(v): sine, sp.cos(v): cosine,
            sp.tan(v): sine/cosine, sp.cot(v): cosine/sine,
            sp.sec(v): 1/cosine, sp.csc(v): 1/sine})
        circles.append((sine, cosine))
    numerator, _ = sp.fraction(sp.cancel(expression.xreplace(substitutions)))
    for sine, cosine in circles:
        if numerator != 0:
            numerator = sp.rem(numerator, sine**2+cosine**2-1, sine)
    return sp.expand(numerator)

def integrand(problem):
    m=re.search(r'\\int\s*(.*?)(?:\\text\{d\}|\\textrm\{?d\}?|d[xyztzθ])',problem)
    if not m:raise ValueError('unreadable printed integrand')
    return expression(m[1])
def fingerprint_text(problem):
    e=integrand(problem);x=sp.Symbol('x',real=True)
    return digest(sp.srepr(sp.expand(e.subs({v:x for v in e.free_symbols}))))
def tex(e):
    pieces=[]
    for term in sp.Add.make_args(sp.expand(e)):
        coefficient,rest=term.as_coeff_Mul()
        sign='-' if coefficient<0 else '+'
        coefficient=abs(coefficient)
        c='' if coefficient==1 and rest!=1 else sp.latex(coefficient)
        f=sp.latex(rest).replace(r'\left','').replace(r'\right','') if rest!=1 else ''
        f=re.sub(r'(\\(?:sin|cos|sec|csc|tan|cot))(\^\{\d+\})?\{\((x|y|z|t|theta)\s*\)\}',lambda m:m[1]+(m[2] or '')+' '+m[3],f)
        pieces.append(sign+c+f)
    return ''.join(pieces).lstrip('+') or '0'

def fill(mask,p):
    values={k:str(v) for k,v in p.items()}
    if 'a' in p:values['half']=str(sp.Rational(p['a'],2))
    if 'b' in p:values['coef']='' if p['b']==1 else str(p['b'])
    if isinstance(mask,str):return re.sub(r'@(a|b|n|d|half|coef)@',lambda m:values[m[1]],mask)
    if isinstance(mask,list):return [fill(v,p) for v in mask]
    if isinstance(mask,dict):return {k:fill(v,p) for k,v in mask.items()}
    return mask

def validate_parameters(template,p,raw=False):
    if raw:keys=set(SOURCE_PROFILES[template]['parameters'])
    elif template in SOURCE_PROFILES:keys=set(SOURCE_PROFILES[template]['parameters'])
    elif template=='fraction':keys={'n','d'}
    elif template=='single-positive':keys={'a'}
    elif template in ('sine-sum','secant-difference','reverse-product'):keys={'a','b'}
    else:keys={'a','b','c'}
    if set(p)!=keys or any(type(v)is not int or not 1<=v<=9 for v in p.values()):raise ValueError('exact positive integer slots 1..9 required')
    if template in ('q-113936','q-113937','single-positive') and p['a']<2:raise ValueError('nonunit coefficient required')
    if keys=={'n','d'} and (min(p.values())<2 or p['n']==p['d'] or sp.gcd(p['n'],p['d'])!=1):raise ValueError('reduced noninteger fraction with numerator/denominator 2..9 required')
    if raw and template=='q-49118' and p['a']%2:raise ValueError('raw half-scale bank requires even coefficient')
    if template in ('reverse-product','sine-sum','secant-difference') and (p['a']<2 or p['b']<2):raise ValueError('two nonunit scaled terms required')
    return dict(p)

def sample(template,rng,raw=False):
    keys=SOURCE_PROFILES[template]['parameters'] if raw or template in SOURCE_PROFILES else ({'n':0,'d':0} if template=='fraction' else {'a':0} if template=='single-positive' else {'a':0,'b':0} if template in ('sine-sum','secant-difference','reverse-product') else {'a':0,'b':0,'c':0})
    while True:
        p={k:rng.randint(1,9) for k in keys}
        try:return validate_parameters(template,p,raw)
        except ValueError:pass

def rows_tex(rows):return '\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def direct_solution(I,terms,primitives,distributed=None):
    recalls=[r'\int '+t+r'\,\text{d}x &= '+f+'+C.' for t,f in [(r'{sec}^{2}x',r'\tan x'),(r'\sec x\tan x',r'\sec x'),(r'\csc x\cot x',r'-\csc x')] if any(fn in I for fn in ([r'{sec}^{2}',r'\sec x('] if t==r'{sec}^{2}x' else [r'\tan x'] if t==r'\sec x\tan x' else [r'\csc']))]
    integral=lambda t:r'\int '+t+r'\,\text{d}x'
    rr=[integral(I)+' &= '+integral(distributed)] if distributed else []
    split='+' .join(integral(t) for t in terms)
    rr.append(('' if rr else integral(I))+' &= '+split)
    factor_terms=[]
    for t in terms:
        coefficient,function=expression(t).as_coeff_Mul()
        factor_terms.append(str(coefficient)+r'\int '+tex(function)+r'\,\text{d}x')
    rr.append(' &= '+'+'.join(factor_terms))
    value=sp.expand(sum(expression(p) for p in primitives))
    rr.append(' &= '+tex(value)+r'+C.')
    return 'Recall that\n'+rows_tex(recalls)+'\n\nTherefore, we have\n'+rows_tex(rr)

def normal(template,p):
    x=sp.Symbol('x',real=True)
    if template in ('q-113936','q-113937','q-113944','q-2164','q-49122'):
        # Derive the canonical primitive before constructing the complete bank.
        prompt=fill(SOURCE_PROFILES[template]['record_mask'][':question/problem'],p)
        e=integrand(prompt);v=next(iter(e.free_symbols))
        table={sp.sec(v)**2:sp.tan(v),sp.sec(v)*sp.tan(v):sp.sec(v),sp.csc(v)*sp.cot(v):-sp.csc(v)}
        canonical=0
        for t in sp.Add.make_args(sp.expand(e)):
            coefficient,function=t.as_coeff_Mul()
            canonical+=coefficient*table[function]
        q=fill(SOURCE_PROFILES[template]['record_mask'],p)
        assert reduced(sp.diff(expression(q[':question/answer-fields'][0][':answer-field/correct'])-canonical,v))==0
        return q
    if template=='fraction':
        q=fill(SOURCE_PROFILES['q-113935']['record_mask'],p);a=-sp.Rational(p['n'],p['d']);values=[a*sp.tan(x),-a*sp.tan(x),a*sp.sec(x),a*sp.cot(x),a*sp.sec(x)**2];correct=0
    elif template=='single-positive':
        a=p['a'];I=f'{a}'+r'{sec}^{2}x';q={':question/problem':'$'+r'\int '+I+r'\,\text{d}x=$',':question/worked-solution':'Recall that\n\n$$\n'+r'\int {sec}^{2}x\,\text{d}x=\tan x+C'+'\n$$\n\nTherefore, we get\n'+rows_tex([r'\int '+I+r'\,\text{d}x &= '+str(a)+r'\int {sec}^{2}x\,\text{d}x',r' &= '+str(a)+r'\tan x+C.'])};values=[a*sp.tan(x),a*sp.cot(x),a*sp.sec(x)*sp.tan(x),a*sp.sec(x),a*sp.csc(x)];correct=0
    elif template=='sine-sum':
        a,b=p['a'],p['b'];I=f'({a}'+r'{sec}^{2}x-'+str(b)+r'\sin x)';F=a*sp.tan(x)+b*sp.cos(x);values=[F,a*sp.tan(x)-b*sp.cos(x),a*sp.sec(x)**2+b*sp.cos(x),a*sp.cot(x)+b*sp.cos(x),a*sp.tan(x)+b*sp.sin(x)];correct=0
        q={':question/problem':'$'+r'\int '+I+r'\,\text{d}x=$',':question/worked-solution':'Recall that\n'+rows_tex([r'\int \sin x\,\text{d}x &= -\cos x+C,',r'\int {sec}^{2}x\,\text{d}x &= \tan x+C.'])+'\n\nTherefore, we have\n'+rows_tex([r'\int '+I+r'\,\text{d}x &= \int '+str(a)+r'{sec}^{2}x\,\text{d}x-\int '+str(b)+r'\sin x\,\text{d}x',r' &= '+str(a)+r'\tan x-'+str(b)+r'(-\cos x)+C',r' &= '+str(a)+r'\tan x+'+str(b)+r'\cos x+C.'])}
    elif template=='secant-difference':
        a,b=p['a'],p['b'];I=f'({a}'+r'\sec x\tan x-'+str(b)+r'{sec}^{2}x)';F=a*sp.sec(x)-b*sp.tan(x);values=[F,-a*sp.sec(x)-b*sp.tan(x),a*sp.sec(x)+b*sp.tan(x),a*sp.sec(x)-b*sp.sec(x)**2,a*sp.sec(x)-b*sp.cot(x)];correct=0
        q={':question/problem':'$'+r'\int '+I+r'\,\text{d}x=$',':question/worked-solution':'Recall that\n'+rows_tex([r'\int \sec x\tan x\,\text{d}x &= \sec x+C,',r'\int {sec}^{2}x\,\text{d}x &= \tan x+C.'])+'\n\nTherefore, we have\n'+rows_tex([r'\int '+I+r'\,\text{d}x &= '+str(a)+r'\int \sec x\tan x\,\text{d}x-'+str(b)+r'\int {sec}^{2}x\,\text{d}x',r' &= '+str(a)+r'\sec x-'+str(b)+r'\tan x+C.'])}
    elif template=='reverse-product':
        a,b=p['a'],p['b'];I=r'\sec x('+str(b)+r'\tan x+'+str(a)+r'\sec x)';F=a*sp.tan(x)+b*sp.sec(x);values=[F,a*sp.tan(x)-b*sp.sec(x),-a*sp.tan(x)+b*sp.sec(x),a*sp.cot(x)+b*sp.sec(x),a*sp.tan(x)+b*sp.csc(x)];correct=0
        q={':question/problem':'What is $'+r'\int '+I+r'\,\text{d}x$?',':question/worked-solution':direct_solution(I,[str(b)+r'\sec x\tan x',str(a)+r'{sec}^{2}x'],[str(b)+r'\sec x',str(a)+r'\tan x'],f'({b}'+r'\sec x\tan x+'+str(a)+r'{sec}^{2}x)')}
    else:
        a,b,c=p['a'],p['b'],p['c'];sign=1 if template=='three-term-plus' else -1
        I=r'(\sec x('+str(a)+r'\sec x+'+str(b)+r'\tan x)'+('+' if sign==1 else '-')+str(c)+r'\csc x\cot x)';F=a*sp.tan(x)+b*sp.sec(x)-sign*c*sp.csc(x)
        values=[F,a*sp.tan(x)+b*sp.sec(x)+sign*c*sp.csc(x),-a*sp.tan(x)+b*sp.sec(x)-sign*c*sp.csc(x),a*sp.sec(x)**2+b*sp.sec(x)-sign*c*sp.csc(x),a*sp.tan(x)+b*sp.sec(x)-sign*c*sp.cot(x)];correct=0
        # Ordered masks keep expansion, splitting, constant extraction, substitution,
        # and sign collection as distinct displayed operations.
        s='+' if sign==1 else '-';expanded=f'({a}'+r'{sec}^{2}x+'+str(b)+r'\sec x\tan x'+s+str(c)+r'\csc x\cot x)'
        rr=[r'\int '+I+r'\,\text{d}x &= \int '+expanded+r'\,\text{d}x',r' &= \int '+str(a)+r'{sec}^{2}x\,\text{d}x+\int '+str(b)+r'\sec x\tan x\,\text{d}x'+s+r'\int '+str(c)+r'\csc x\cot x\,\text{d}x',r' &= '+str(a)+r'\int {sec}^{2}x\,\text{d}x+'+str(b)+r'\int \sec x\tan x\,\text{d}x'+s+str(c)+r'\int \csc x\cot x\,\text{d}x',r' &= '+str(a)+r'\tan x+'+str(b)+r'\sec x'+s+str(c)+r'(-\csc x)+C',r' &= '+tex(F)+r'+C.']
        recalls=[r'\int {sec}^{2}x\,\text{d}x &= \tan x+C,',r'\int \sec x\tan x\,\text{d}x &= \sec x+C,',r'\int \csc x\cot x\,\text{d}x &= -\csc x+C.']
        q={':question/problem':'Calculate $'+r'\int '+I+r'\,\text{d}x.$',':question/worked-solution':'Recall that\n'+rows_tex(recalls)+'\n\nTherefore, we have\n'+rows_tex(rr)}
    vals=[tex(v)+r'+C' for v in values]
    q[':question/answer-fields']=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':v} for v in vals],':answer-field/correct':vals[correct]}]
    return q

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio-only default contract')
    rng=random.Random(seed);raw=bool(profile and profile.startswith('raw:'))
    if raw:
        name=profile[4:]
        if name not in SOURCE_PROFILES or (template and template!=name) or SOURCE_PROFILES[name]['level']!=level:raise ValueError('raw profile/level mismatch')
    else:
        name=template or profile or rng.choice(DEFAULTS[level])
        if name not in DEFAULTS[level] or (profile and profile!=name):raise ValueError('template/profile/level mismatch')
    p=validate_parameters(name,parameters,raw) if parameters is not None else sample(name,rng,raw)
    q=fill(SOURCE_PROFILES[name]['record_mask'],p) if raw else normal(name,p)
    if not raw:
        q[':question/difficulty']=':question.difficulty/'+level
        for k in (':question/problem',':question/worked-solution'):q[k]=normalize_prose(q[k])
        for f in q[':question/answer-fields']:
            f[':answer-field/correct']=normalize_tex(f[':answer-field/correct'])
            for a in f[':answer-field/choices']:a[':answer/value']=normalize_tex(a[':answer/value'])
    # Content identity comes from actual owned fields, difficulty, prompt and solution;
    # raw/default profile aliases, unused parameters, seed and shuffles are excluded.
    bare=copy.deepcopy(q)
    for f in bare.get(':question/answer-fields',[]):f[':answer-field/choices']=sorted(f.get(':answer-field/choices',[]),key=lambda a:json.dumps(a,sort_keys=True))
    content=digest([VERSION,bare]);qid=uid('question:'+content);q[':question/id']=qid
    for i,f in enumerate(q.get(':question/answer-fields',[])):
        fid=uid(qid+':field:'+str(i)+':'+f[':answer-field/key']);f[':answer-field/id']=fid
        for a in f.get(':answer-field/choices',[]):a[':answer/id']=uid(fid+':answer:'+digest(a))
        if ':answer-field/correct' in f:
            correct=f[':answer-field/correct'];f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==correct)]
        rng.shuffle(f.get(':answer-field/choices',[]))
    if not raw:
        e=integrand(q[':question/problem']);x=next(iter(e.free_symbols));f=q[':question/answer-fields'][0]
        values=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
        for i,v in enumerate(values):
            is_correct=reduced(sp.diff(v,x)-e)==0
            if is_correct!=(f[':answer-field/choices'][i][':answer/id']==f[':answer-field/correct'][1]):raise ValueError('invalid complete bank')
            if any(reduced(sp.diff(v-prev,x))==0 for prev in values[:i]):raise ValueError('equivalent antiderivative families')
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':name,'bank_profile':profile or name,'parameters':p,'parameter_fingerprint':fingerprint_text(q[':question/problem']),'content_fingerprint':content,'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'domain':'Real connected intervals where every displayed trigonometric function is defined (exclude sin(x)=0 and/or cos(x)=0 poles); C arbitrary. Equality criterion: antiderivatives modulo additive constants on those intervals.','plot_rating':'none','evidence_only':raw,'eligible_for_learning':not raw,'authored':name not in ('q-113936','q-113937','q-113944','q-2164','q-49122'),'source_references':['source.json','source-profiles.json','topic.json','lesson.json']}}
    return record if raw else validate_generated_record(record)

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[]))+'\n\n'+q.get(':question/worked-solution','[Worked solution absent in raw evidence.]')
def batch(level,count=5,seed=0):
    records=[];seen=set()
    for i in range(count*100):
        r=generate(level,seed+i)
        if r['generation']['parameter_fingerprint'] not in seen:records.append(r);seen.add(r['generation']['parameter_fingerprint'])
        if len(records)==count:return records
    raise ValueError('requested batch exhausted bounded domain')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),required=True);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    if args.count<1:ap.error('count must be positive')
    rows=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
if __name__=='__main__':main()
