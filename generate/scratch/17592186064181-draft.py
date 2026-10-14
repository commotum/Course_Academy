#!/usr/bin/env python3
"""Unregistered direct-primitive draft; exact raw replay preserves all source defects."""
import argparse,copy,hashlib,itertools,json,random,re,sys,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.question_capture.math_format import normalize_prose,normalize_tex,validate_generated_record
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
KP_ID=17592186064181
KP_UUID='9836abbe-e172-5c2f-8b19-145ef6d5c02d'
TITLE='Integrating Cosecant Squared'
VERSION='2.0.0-draft'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCE_BASIS=SOURCE['basis'];LINEAGE=SOURCE['lineage']
SOURCE_PROFILES=json.loads((HERE/'source-profiles.json').read_text())
SUPPORTED_LEVELS=('easy','moderate','hard')
DEFAULTS={'easy':('q-113947','q-71663','single-negative','fraction','blank'),
 'moderate':('q-49121','secant-difference','sine-difference','reverse-product'),
 'hard':('three-term',)}
TEMPLATES={k:{'difficulty':v} for v,ks in DEFAULTS.items() for k in ks}
SUPPORTED_PROFILES=tuple(TEMPLATES)

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def expression(text):
    """Small exact source-notation reader, accepting raw/source and standard TeX."""
    text=re.sub(r'\\operatorname\{(sin|cos|sec|csc|tan|cot)\}',r'\1',text)
    text=text.replace(r'\displaystyle','').replace('⁡','').replace(r'\theta','theta').replace('θ','theta')
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
    values.update({k+'coef':('' if v==1 else str(v)) for k,v in p.items()})
    if isinstance(mask,str):return re.sub(r'@(acoef|bcoef|ccoef|a|b|c|n|d)@',lambda m:values[m[1]],mask)
    if isinstance(mask,list):return [fill(v,p) for v in mask]
    if isinstance(mask,dict):return {k:fill(v,p) for k,v in mask.items()}
    return mask

def keys_for(name,raw=False):
    if raw or name in SOURCE_PROFILES:return set(SOURCE_PROFILES[name]['parameters'])
    if name=='fraction':return {'n','d'}
    if name in ('single-negative','blank','sine-difference'):return {'a'}
    if name=='three-term':return {'a','b','c'}
    return {'a','b'}
def validate_parameters(name,p,raw=False):
    if set(p)!=keys_for(name,raw) or any(type(v)is not int or not 1<=v<=9 for v in p.values()):raise ValueError('exact bounded positive integer slots 1..9 required')
    if name in ('q-113947','q-71663') and p['a']<2:raise ValueError('nonunit magnitude 2..9 required')
    if name in ('fraction','q-113948') and (min(p.values())<2 or p['n']==p['d'] or sp.gcd(p['n'],p['d'])!=1):raise ValueError('reduced noninteger fraction n,d in2..9 required')
    if raw and name=='q-49093' and p['a']==1:raise ValueError('raw bank collides when omitted coefficient becomes one')
    return dict(p)
def sample(name,rng,raw=False):
    while True:
        p={k:rng.randint(1,9) for k in sorted(keys_for(name,raw))}
        try:return validate_parameters(name,p,raw)
        except ValueError:pass

def field(values,correct=0,blank=False):
    return [{':answer-field/key':'field-1' if blank else 'selection',':answer-field/type':':answer-field.type/'+('blank' if blank else 'radio'),':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':v} for v in values],':answer-field/correct':values[correct]}]
def rows(rr):return '\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rr)+r'\end{aligned}'+'\n$$'
def primitive(e,x):
    table={sp.csc(x)**2:-sp.cot(x),sp.sec(x)*sp.tan(x):sp.sec(x),sp.csc(x)*sp.cot(x):-sp.csc(x),sp.sin(x):-sp.cos(x),sp.cos(x):sp.sin(x)}
    out=0
    for t in sp.Add.make_args(sp.expand(e)):
        c,f=t.as_coeff_Mul()
        if f not in table:raise ValueError('outside direct-primitive lesson method')
        out+=c*table[f]
    assert reduced(sp.diff(out,x)-e)==0
    return out

def normal(name,p):
    x=sp.Symbol('x',real=True)
    if name in ('q-113947','q-71663','q-49121'):return fill(SOURCE_PROFILES[name]['record_mask'],p)
    if name=='fraction':
        q=fill(SOURCE_PROFILES['q-113948']['record_mask'],p);a=sp.Rational(p['n'],p['d']);F=a*sp.cot(x);vals=[F,-F,a*sp.tan(x),a*sp.csc(x),a*sp.csc(x)**2]
    elif name=='single-negative':
        a=p['a'];mask=copy.deepcopy(SOURCE_PROFILES['q-71664']['record_mask'])
        # Source unit primitive bank generalizes by multiplying every complete value.
        I=r'-'+('' if a==1 else str(a))+r'{csc}^{2}y';y=sp.Symbol('y',real=True)
        q={':question/problem':'$'+r'\int '+I+r'\,\text{d}y=$',':question/worked-solution':'Recall that'+rows([r'\int {csc}^{2}y\,\text{d}y=-\cot y+C'])+'\n\nTherefore, we get'+rows([r'\int '+I+r'\,\text{d}y &= -'+('' if a==1 else str(a))+r'\int {csc}^{2}y\,\text{d}y',r' &= -'+('' if a==1 else str(a))+r'(-\cot y)+C',r' &= '+('' if a==1 else str(a))+r'\cot y+C.'])}
        vals=[a*sp.cot(y),a*sp.sec(y)*sp.tan(y),a*sp.tan(y),-a*sp.tan(y),-a*sp.cot(y)]
    elif name=='blank':
        a=p['a'];q=fill(SOURCE_PROFILES['q-143522']['record_mask'],p)
        q[':question/problem']='Given $v(t)='+str(a)+r'{csc}^{2}t$, calculate '+'$'+r'\int v(t)\,\text{d}t=${{field-1}} $+C$.'
        return q
    elif name=='secant-difference':
        q=fill(SOURCE_PROFILES['q-113952']['record_mask'],p);a,b=p['a'],p['b'];F=-a*sp.cot(x)-b*sp.sec(x);vals=[F,a*sp.cot(x)-b*sp.sec(x),-a*sp.cot(x)+b*sp.sec(x),-a*sp.tan(x)-b*sp.sec(x),-a*sp.cot(x)-b*sp.sec(x)*sp.tan(x)]
    elif name=='sine-difference':
        a=p['a'];q=fill(SOURCE_PROFILES['q-71666']['record_mask'],{'b':a});F=-sp.cos(x)+a*sp.cot(x)
        # Malformed source csc distractors are never repaired implicitly or served;
        # this complete authored bank uses defined component error operations.
        vals=[F,sp.cos(x)+a*sp.cot(x),-sp.cos(x)-a*sp.cot(x),-sp.sin(x)+a*sp.cot(x),-sp.cos(x)+a*sp.tan(x)]
    elif name=='reverse-product':
        a,b=p['a'],p['b'];I=r'\csc x('+str(a)+r'\csc x-'+str(b)+r'\cot x)';F=-a*sp.cot(x)+b*sp.csc(x)
        q={':question/problem':'What is $'+r'\int '+I+r'\,\text{d}x$?',':question/worked-solution':'Recall that'+rows([r'\int {csc}^{2}x\,\text{d}x=-\cot x+C,',r'\int \csc x\cot x\,\text{d}x=-\csc x+C.'])+'\n\nTherefore, we get'+rows([r'\int '+I+r'\,\text{d}x &= \int ('+str(a)+r'{csc}^{2}x-'+str(b)+r'\csc x\cot x)\,\text{d}x',r' &= \int '+str(a)+r'{csc}^{2}x\,\text{d}x-\int '+str(b)+r'\csc x\cot x\,\text{d}x',r' &= '+str(a)+r'\int {csc}^{2}x\,\text{d}x-'+str(b)+r'\int \csc x\cot x\,\text{d}x',r' &= '+str(a)+r'(-\cot x)-'+str(b)+r'(-\csc x)+C',r' &= '+tex(F)+r'+C.'])}
        vals=[F,a*sp.cot(x)+b*sp.csc(x),-a*sp.cot(x)-b*sp.csc(x),-a*sp.tan(x)+b*sp.csc(x),-a*sp.cot(x)+b*sp.cot(x)]
    elif name=='three-term':
        q=fill(SOURCE_PROFILES['q-113958']['record_mask'],p)
        # Supported by source prompt/main calculation, derivative and lesson formula.
        q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\int sin\,',r'\int sin x\,')
        a,b,c=p['a'],p['b'],p['c'];F=a*sp.sec(x)+b*sp.cot(x)-c*sp.cos(x)
        vals=[F,-a*sp.sec(x)+b*sp.cot(x)-c*sp.cos(x),a*sp.sec(x)-b*sp.cot(x)-c*sp.cos(x),a*sp.sec(x)+b*sp.cot(x)+c*sp.cos(x),-F]
    else:raise ValueError('unknown family')
    q[':question/answer-fields']=field([tex(v)+r'+C' for v in vals]);return q

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
    raw=bool(profile and profile.startswith('raw:'));rng=random.Random(seed)
    if raw:
        name=profile[4:]
        if name not in SOURCE_PROFILES or (template and template!=name) or SOURCE_PROFILES[name]['level']!=level:raise ValueError('raw profile/level mismatch')
    else:
        name=template or profile or rng.choice(DEFAULTS[level])
        if name not in DEFAULTS[level] or (profile and profile!=name):raise ValueError('template/profile/level mismatch')
    expected_type='blank' if name=='blank' or name in ('q-143522','q-167569') else 'radio'
    if field_type not in (None,expected_type,':answer-field.type/'+expected_type):raise ValueError('source-family field type required')
    p=validate_parameters(name,parameters,raw) if parameters is not None else sample(name,rng,raw)
    q=fill(SOURCE_PROFILES[name]['record_mask'],p) if raw else normal(name,p)
    if not raw:
        q[':question/difficulty']=':question.difficulty/'+level
        for k in (':question/problem',':question/worked-solution'):q[k]=normalize_prose(q[k])
        for f in q[':question/answer-fields']:
            f[':answer-field/correct']=normalize_tex(f[':answer-field/correct'])
            for a in f[':answer-field/choices']:a[':answer/value']=normalize_tex(a[':answer/value'])
    bare=copy.deepcopy(q)
    for f in bare.get(':question/answer-fields',[]):f[':answer-field/choices']=sorted(f.get(':answer-field/choices',[]),key=lambda a:json.dumps(a,sort_keys=True))
    content=digest([VERSION,bare]);qid=uid('question:'+content);q[':question/id']=qid
    for i,f in enumerate(q.get(':question/answer-fields',[])):
        fid=uid(qid+':field:'+str(i)+':'+f[':answer-field/key']);f[':answer-field/id']=fid
        for a in f.get(':answer-field/choices',[]):a[':answer/id']=uid(fid+':answer:'+digest(a))
        if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==f[':answer-field/correct'])]
        rng.shuffle(f.get(':answer-field/choices',[]))
    if not raw:
        e=integrand(q[':question/problem']) if name!='blank' else p['a']*sp.csc(sp.Symbol('t',real=True))**2
        x=next(iter(e.free_symbols));F=primitive(e,x);f=q[':question/answer-fields'][0];values=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
        for i,v in enumerate(values):
            if (reduced(sp.diff(v,x)-e)==0)!=(f[':answer-field/choices'][i][':answer/id']==f[':answer-field/correct'][1]):raise ValueError('invalid complete bank')
            if any(reduced(sp.diff(v-prev,x))==0 for prev in values[:i]):raise ValueError('equivalent antiderivatives collide')
        fp=digest(sp.srepr(sp.expand(e.subs(x,sp.Symbol('x',real=True)))))
    else:
        # Undefined v(t) raw prompt has no mathematical task until its absent
        # definition is supplied. Do not count unseen parameters as novelty.
        fp=digest(q[':question/problem']) if name in ('q-143522','q-167569') else fingerprint_text(q[':question/problem'])
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':name,'bank_profile':profile or name,'parameters':p,'parameter_fingerprint':fp,'content_fingerprint':content,'source_basis':SOURCE_BASIS,'lineage':LINEAGE,'domain':'Real connected intervals excluding sin(variable)=0 and every additional cos(variable)=0 pole appearing in the input or bank; C arbitrary. Primitive families are compared modulo additive constants.','plot_rating':'none','evidence_only':raw,'eligible_for_learning':not raw,'authored':name not in ('q-113947','q-71663','q-49121'),'source_references':['source.json','source-profiles.json','topic.json','lesson.json'],'completion':'Missing fields completed with derived radio banks; blank v(t) definition completed from solution; hard recall argument supplied from prompt and lesson. Raw source defects remain separate evidence.' if not raw and name not in ('q-113947','q-71663','q-49121') else None}}
    return record if raw else validate_generated_record(record)

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[]))+'\n\n'+q.get(':question/worked-solution','[Worked solution absent in raw evidence.]')
def batch(level,count=5,seed=0):
    rr=[];seen=set()
    for i in range(count*100):
        r=generate(level,seed+i)
        if r['generation']['parameter_fingerprint'] not in seen:rr.append(r);seen.add(r['generation']['parameter_fingerprint'])
        if len(rr)==count:return rr
    raise ValueError('bounded domain exhausted')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),required=True);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    if a.count<1:ap.error('positive count required')
    rr=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (SUPPORTED_LEVELS if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
    print(json.dumps(rr,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rr)))
if __name__=='__main__':main()
