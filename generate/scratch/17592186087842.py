#!/usr/bin/env python3
"""Vertical asymptotes, basis 1356. Read-only/local review records only.

Observed templates are positive root dilations of every captured prompt, complete
bank and worked-solution component. This is an explicit evidence transformation,
not a claim to recover undocumented source distractor intent. All observed radio
profiles are evidence_only and are excluded from default learning generation.
Defaults use bounded same-method objects with an independently authored five-member
operation bank. No cancellation or complex-root branch belongs to this KP.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
X=sp.Symbol('x',real=True)
KP_ID=17592186087842
KP_UUID='60c99086-75e7-5d91-b425-4e1b6f582bcc'
TITLE='Calculating the Vertical Asymptotes of a Rational Function'
VERSION='vertical-asymptotes-v1'
HERE=Path(__file__).with_suffix('')
CASES=json.loads((HERE/'source-cases.json').read_text())
OBS={c['template']:c for c in CASES}
OPENING='To find the vertical asymptotes of a rational function, we factor the numerator and denominator and cancel any common factors. Then, we set the denominator equal to zero and solve for $x.$'
NO_COMMON='There are no common factors in the numerator and denominator, so we set the denominator equal to zero and solve for $x:$'
DEFAULTS={'easy':['quadratic','repeated','factored_three','leading'], 'moderate':['numerator_quadratic'], 'hard':['sum']}

def tex(v): return sp.latex(sp.sympify(v))
def frac(n,d): return r'\frac{'+n+'}{'+d+'}'
def polynomial(v): return tex(sp.expand(v))
def linear(a,b): return polynomial(a*X+b)
def factor(root): return '('+linear(1,-root)+')'
def identifier(label): return str(uuid.uuid5(uuid.UUID(KP_UUID),label))
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def group(s,start):
    assert s[start]=='{', (s,start)
    depth=1
    for j in range(start+1,len(s)):
        depth+=(s[j]=='{')-(s[j]=='}')
        if depth==0:return s[start+1:j],j+1
    raise ValueError('unbalanced TeX group')

def parse_math(s):
    """Independent small TeX reader for displayed rational polynomial expressions."""
    s=s.replace(r'\dfrac',r'\frac').replace(r'\,','').replace(r'\left','').replace(r'\right','')
    while r'\frac' in s:
        i=s.index(r'\frac');a,j=group(s,i+5);b,k=group(s,j)
        s=s[:i]+'(('+str(parse_math(a))+')/('+str(parse_math(b))+'))'+s[k:]
    s=re.sub(r'\^\{([^{}]+)\}',r'**(\1)',s)
    s=re.sub(r'\^(\d)',r'**\1',s).replace('{','(').replace('}',')').replace('−','-')
    s=s.strip().rstrip('.,')
    if re.search(r'[^\dx()+*/.\-\s]',s):raise ValueError('unsupported displayed expression: '+s)
    return parse_expr(s,local_dict={'x':X},transformations=standard_transformations+(implicit_multiplication_application,))

def printed_function(problem):
    m=re.search(r'([fgh])\(x\)\s*=\s*([^$]+)',problem)
    if not m:raise ValueError('printed function missing')
    return parse_math(m.group(2)),m.group(1)

def poles(expr):
    n,d=sp.fraction(sp.cancel(expr))
    roots=sp.polys.polytools.ground_roots(d,X)
    if sum(roots.values())!=sp.degree(d,X):raise ValueError('nonrational/complex root out of scope')
    return tuple(sorted(roots))

# Source math-mask transformations. Constants are components of expressions; no
# source payload branch or correct-answer lookup is used. Positive dilation sends
# every root r to scale*r. Each polynomial P of degree d becomes scale^d*P(x/scale).
# Applying that independently to numerator/denominator only changes a nonzero
# overall scalar and preserves all poles, factorability and noncancellation.
def dilate_leaf(s,k):
    mon=re.compile(r'(?<![A-Za-z])(?P<c>\d*)(?P<x>\{x\}|x)(?P<e>\^\{\d+\}|\^\d+)?')
    hits=list(mon.finditer(s))
    if not hits:return s
    degree=max(int(re.sub(r'\D','',m.group('e'))) if m.group('e') else 1 for m in hits)
    repl=[];protected=[]
    for m in hits:
        e=int(re.sub(r'\D','',m.group('e'))) if m.group('e') else 1
        c=int(m.group('c') or 1)*k**(degree-e)
        coeff=str(c) if c!=1 or m.group('c') else ''
        repl.append((m.start(),m.end(),coeff+m.group('x')+(m.group('e') or '')))
        protected.append((m.start(),m.end()))
    for m in re.finditer(r'\d+',s):
        if not any(a<=m.start()<b for a,b in protected):repl.append((m.start(),m.end(),str(int(m.group())*k**degree)))
    for a,b,v in sorted(repl,reverse=True):s=s[:a]+v+s[b:]
    return s

def dilate_expression(s,k):
    # Fractions and factored parentheses are complete components, masked before
    # coefficient changes; function arguments and TeX syntax are never slots.
    save={}
    def mask(v):
        key='§'+chr(65+len(save))+'§';save[key]=v;return key
    while r'\frac' in s or r'\dfrac' in s:
        m=re.search(r'\\(?:d)?frac',s);a,j=group(s,m.end());b,end=group(s,j)
        v=m.group()+ '{'+dilate_expression(a,k)+'}{'+dilate_expression(b,k)+'}'
        s=s[:m.start()]+mask(v)+s[end:]
    while '(' in s:
        m=re.search(r'\([^()]*\)',s)
        if not m:raise ValueError('parentheses')
        s=s[:m.start()]+mask('('+dilate_expression(m.group()[1:-1],k)+')')+s[m.end():]
    s=dilate_leaf(s,k)
    for key,v in save.items():s=s.replace(key,v)
    return s

ROOT=re.compile(r'(x\s*=\s*)(-?\s*\\frac\{\d+\}\{\d+\}|-?\d+)')
def dilate_text(text,k,name):
    def component(m):
        body=m.group(2);saved={}
        def save(v):key='¤'+chr(65+len(saved))+'¤';saved[key]=v;return key
        def root(m):
            raw=m.group(2);val=parse_math(raw)*k
            rendered=raw if val==parse_math(raw) else tex(val)
            return m.group(1)+save(rendered)
        body=ROOT.sub(root,body)
        body=re.sub(r'f\(x\)',lambda _:save(name+'(x)'),body)
        # aligned row boundaries and equal signs isolate polynomial components.
        parts=re.split(r'(\\\\|=|&|\\begin\{aligned\}|\\end\{aligned\})',body)
        body=''.join(v if v in ('=', '&',r'\\',r'\begin{aligned}',r'\end{aligned}') else dilate_expression(v,k) for v in parts)
        for key,v in saved.items():body=body.replace(key,v)
        return m.group(1)+body+m.group(3)
    return re.sub(r'(\$\$?)(.*?)(\1)',component,text,flags=re.S)

def source_values(value,k):
    if 'x' in value:
        return ROOT.sub(lambda m:m.group(1)+(m.group(2) if k==1 else tex(parse_math(m.group(2))*k)),value)
    if 'asymptote' in value:return value
    return tex(parse_math(value)*k)

def rootset(value):
    if 'asymptote' in value:return ()
    return tuple(sorted(set(parse_math(m.group(2)) for m in ROOT.finditer(value))))

def validate_scope(n,d,level):
    n,d=sp.fraction(sp.cancel(n/d))
    # Bounds apply to reduced primitive objects, never inflated raw spellings.
    pn,pd=sp.Poly(n,X),sp.Poly(d,X)
    pn=pn.primitive()[1];pd=pd.primitive()[1]
    bound={'easy':40,'moderate':80,'hard':60}[level]
    if max(abs(c) for c in list(pn.all_coeffs())+list(pd.all_coeffs()))>bound:raise ValueError('primitive coefficient bounds')
    rs=poles(n/d)
    if not 2<=len(rs)<=3 or any(abs(r)>12 for r in rs):raise ValueError('root bounds')
    return rs

def build_fields(layout,rs,bank,identity,rng):
    fs=[]
    if layout=='blank':
        for i,r in enumerate(rs):
            fid=identifier(identity+'/field-'+str(i+1));aid=identifier(fid+'/'+tex(r))
            fs.append({':answer-field/id':fid,':answer-field/key':'field-'+str(i+1),':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex(r)}],':answer-field/correct':[':answer/id',aid]})
    else:
        fid=identifier(identity+'/selection');answers=[];correct=None
        for typ,v in bank:
            aid=identifier(fid+'/'+typ+'/'+v);answers.append({':answer/id':aid,':answer/type':typ,':answer/value':v})
            if rootset(v)==rs:correct=aid
        assert correct is not None
        rng.shuffle(answers)
        fs=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]
    return fs

def answer_bank(rs,n,profile):
    """Complete authored operation bank selected before parameter sampling."""
    nr=tuple(sorted(sp.polys.polytools.ground_roots(n,X)))
    if profile=='method_omission_sign':sets=[rs,rs[:-1],rs[1:],tuple(-r for r in rs),tuple(sorted(set(rs+(sp.Integer(0),))))]
    elif profile=='method_numerator':sets=[rs,(rs[0],),(rs[-1],),(),nr]
    else:raise ValueError('unsupported complete default bank')
    sets=[tuple(sorted(set(v))) for v in sets]
    if len(set(sets))!=5:raise ValueError('whole-bank collision')
    return [(':answer.type/text','No vertical asymptotes') if not v else (':answer.type/text','$x='+tex(v[0])+'$ only') if len(v)==1 else (':answer.type/math',r',\,'.join('x='+tex(r) for r in v)) for v in sets]

def finish(level,template,p,profile,problem,solution,layout,bank,rs,seed,origin,flags,field_order=None):
    sig={'version':VERSION,'prompt':problem,'solution':solution,'layout':layout,'bank':sorted(bank),'roots':[str(r) for r in rs]}
    identity=digest(sig);fields=build_fields(layout,rs,bank,identity,random.Random(seed))
    if field_order:fields.sort(key=lambda f:field_order.index(f[':answer-field/key']))
    expr,name=printed_function(problem)
    task=digest({'poles':[str(r) for r in rs],'denominator':sp.srepr(sp.Poly(sp.fraction(sp.cancel(expr))[1],X).monic()),'numerator':sp.srepr(sp.Poly(sp.fraction(sp.cancel(expr))[0],X).monic())})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':identifier(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':p,'content_fingerprint':identity,'mathematical_fingerprint':task,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'origin':origin,**flags}}

def observed(level,seed,template,parameters,profile):
    c=OBS[template]
    if level!=c['level']:raise ValueError('source level/supported authored assignment')
    raw_profile=profile==c['bank_profile']+'_raw'
    if profile not in (c['bank_profile'],c['bank_profile']+'_raw'):raise ValueError('source banks cannot be mixed')
    p=dict(parameters or {'scale':random.Random(seed).choice([1,3] if template=='observed_39790' else [1,2]),'function':'f'})
    if set(p)-{'scale','function'}:raise ValueError('unexpected parameters')
    k=p.get('scale',1);name=p.get('function','f')
    if type(k)!=int or not 1<=k<=3 or name not in ('f','g','h'):raise ValueError('source dilation bounds/name')
    if template=='observed_39790' and k%2==0:raise ValueError('primitive rational root workload requires odd dilation')
    q=c['raw_source'];problem=dilate_text(q[':question/problem'],k,name)
    expr,_=printed_function(problem);rs=poles(expr)
    if any(abs(r)>24 for r in rs):raise ValueError('evidence dilation root bounds')
    fields=q.get(':question/answer-fields',[]);layout='radio' if fields and fields[0][':answer-field/type'][':db/ident'].endswith('/radio') else 'blank'
    bank=[]
    if layout=='radio':
        bank=[(a[':answer/type'][':db/ident'],source_values(a[':answer/value'],k)) for a in fields[0][':answer-field/choices']]
        sets=[rootset(v) for _,v in bank]
        if len(set(sets))!=len(sets) or sets.count(rs)!=1:raise ValueError('whole source bank ambiguity')
    if c['missing_fields']:
        problem+='\n\nIn ascending order: '+ ' and '.join('$x=$ {{field-'+str(i+1)+'}}' for i in range(len(rs)))+'.'
    solution=dilate_text(q.get(':question/worked-solution',''),k,name)
    if not solution:
        if c['source_id']=='q-39796':
            # Authored completion of missing source solution, in the source's
            # actual 2-x / 2+x orientation; four distinct sum stages.
            base=OPENING+'\n\nAdding both fractions and then factoring the numerator and denominator, we get\n\n$$\n'+r'\begin{aligned}f(x) & =\frac{2}{2-x}+\frac{3}{2+x} \\ & =\frac{2(2+x)+3(2-x)}{(2-x)(2+x)} \\ & =\frac{4+2x+6-3x}{(2-x)(2+x)} \\ & =\frac{10-x}{(2-x)(2+x)}.\end{aligned}'+'\n$$\n\n'+NO_COMMON+'\n\n$$\n(2-x)(2+x)=0\n$$\n\n'+conclusion((sp.Integer(-2),sp.Integer(2)),False)
            solution=dilate_text(base,k,name)
        else:solution=authored_solution(expr,name,rs,layout=='blank')
    order=[f[':answer-field/key'] for f in fields] if layout=='blank' and fields else None
    result=finish(level,template,p,profile,problem,solution,layout,bank,rs,seed,'observed-dilation',{'evidence_only':layout=='radio','eligible_for_learning':layout!='radio','missing_original_correct':c['missing_correct'],'authored_level_assignment':c['authored_level'],'authored_solution':c['missing_solution'],'presentation_repair':c['missing_fields']},order)
    if raw_profile:
        # Explicit evidence profile keeps absence as absence, through the same
        # mathematical component transformation. No copied-payload return path.
        rawq=result['question'];rawq[':question/problem']=dilate_text(q[':question/problem'],k,name)
        if c['missing_solution']:rawq.pop(':question/worked-solution')
        if c['authored_level']:rawq.pop(':question/difficulty')
        if c['missing_fields']:rawq.pop(':question/answer-fields')
        else:
            original_by_key={f[':answer-field/key']:f for f in fields}
            for f in rawq[':question/answer-fields']:
                if ':answer-field/correct' not in original_by_key[f[':answer-field/key']]:f.pop(':answer-field/correct')
        signature={key:value for key,value in rawq.items() if key not in (':question/id',':question/answer-fields')}
        signature['version']=VERSION
        signature['fields']=[{'key':f[':answer-field/key'],'type':f[':answer-field/type'],'bank':sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices']),'has_correct':':answer-field/correct' in f} for f in rawq.get(':question/answer-fields',[])]
        identity=digest(signature);rawq[':question/id']=identifier(identity)
        for f in rawq.get(':question/answer-fields',[]):
            f[':answer-field/id']=identifier(identity+'/'+f[':answer-field/key']);old_correct=f.get(':answer-field/correct',[None,None])[1]
            for a in f[':answer-field/choices']:
                old_id=a[':answer/id'];a[':answer/id']=identifier(f[':answer-field/id']+'/'+a[':answer/type']+'/'+a[':answer/value'])
                if old_id==old_correct:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
        result['generation'].update(content_fingerprint=identity,evidence_only=True,eligible_for_learning=False,raw_source_replay=True,authored_solution=False,authored_level_assignment=False,presentation_repair=False)
    return result

def conclusion(rs,blank):
    pairs=['$x='+tex(r)+'$' for r in rs]
    join=', '.join(pairs[:-1])+(' and '+pairs[-1])
    count={2:'two',3:'three'}[len(rs)]
    return 'This gives the '+count+' solutions '+join+'. \n\nTherefore, '+('in ascending order, ' if blank else '')+'the equations of the vertical asymptotes are '+join+'.'

def authored_solution(expr,name,rs,blank):
    n,d=sp.fraction(sp.together(expr));nf=tex(sp.factor(n));df=''.join(factor(r) for r in rs)
    # Keep multiplicities and leading coefficients in the factored function.
    exactdf=tex(sp.factor(d))
    return OPENING+'\n\nFactoring the numerator and denominator, we get\n\n$$\n'+name+'(x)='+frac(nf,exactdf)+'.\n$$\n\n'+NO_COMMON+'\n\n$$\n'+df+'=0\n$$\n\n'+conclusion(rs,blank)

def object_for(template,p):
    if template=='quadratic':
        r,t,c=p['r'],p['t'],p['c'];n=sp.Integer(c);d=(X-r)*(X-t)
    elif template=='repeated':
        r,t,u=p['r'],p['t'],p['u'];n=X-u;d=(X-r)**2*(X-t)
    elif template=='factored_three':
        r,t,v,u=p['r'],p['t'],p['v'],p['u'];n=X-u;d=(X-r)*(X-t)*(X-v)
    elif template=='leading':
        a,b,t,u=p['a'],p['b'],p['t'],p['u'];n=X-u;d=(a*X+b)*(X-t)
    elif template=='numerator_quadratic':
        r,t,a,b,c=p['r'],p['t'],p['a'],p['b'],p['c'];n=c*X*(a*X+b);d=(X-r)*(X-t)
    elif template=='sum':
        r,t,a,b=p['r'],p['t'],p['a'],p['b'];n=a*(X-t)+b*(X-r);d=(X-r)*(X-t)
    else:raise ValueError('template')
    return sp.expand(n),sp.expand(d)

def sample(template,rng):
    rs=rng.sample([v for v in range(-7,8) if v!=0],3)
    r,t=sorted(rs[:2]);p={'function':rng.choice(['f','g','h'])}
    if template=='quadratic':p.update(r=r,t=t,c=rng.choice([1,2,3,4]))
    elif template=='repeated':p.update(r=r,t=t,u=rng.randint(-6,6))
    elif template=='factored_three':p.update(r=r,t=t,v=rs[2],u=rng.randint(-5,5))
    elif template=='leading':p.update(a=rng.randint(2,4),b=rng.choice([i for i in range(-7,8) if i]),t=t,u=rng.randint(-5,5))
    elif template=='numerator_quadratic':p.update(r=r,t=t,a=rng.randint(1,3),b=rng.choice([i for i in range(-8,9) if i]),c=rng.randint(1,4))
    elif template=='sum':p.update(r=r,t=t,a=rng.randint(1,4),b=rng.randint(1,4))
    return p

def check_parameters(template,p,level):
    required={'quadratic':{'r','t','c'},'repeated':{'r','t','u'},'factored_three':{'r','t','v','u'},'leading':{'a','b','t','u'},'numerator_quadratic':{'r','t','a','b','c'},'sum':{'r','t','a','b'}}[template]
    if set(p)!=required|{'function'} or p['function'] not in ('f','g','h'):raise ValueError('parameter keys/name')
    if any(type(p[k])!=int for k in required):raise ValueError('integer primitive components required')
    if any(abs(p[k])>8 for k in required if k in ('r','t','v','u','b')):raise ValueError('component bounds')
    if 'r' in p and p['r']>=p['t']:raise ValueError('ordered distinct root inputs')
    if template=='leading' and (not 2<=p['a']<=4 or p['b']==0 or math.gcd(p['a'],abs(p['b']))!=1):raise ValueError('primitive nonunit rational-root factor required')
    if template=='numerator_quadratic' and (not 1<=p['a']<=3 or not 1<=p['c']<=4 or p['b']==0):raise ValueError('moderate numerator factor workload')
    if template=='sum' and (not 1<=p['a']<=4 or not 1<=p['b']<=4 or p['r']==0 or p['t']==0):raise ValueError('hard two nonzero numerator fractions/nonzero constants required')
    if template=='quadratic' and not 1<=p['c']<=4:raise ValueError('numerator scale')
    n,d=object_for(template,p)
    if sp.degree(sp.gcd(n,d),X)>0:raise ValueError('common-factor branch excluded')
    rs=validate_scope(n,d,level)
    if template=='factored_three' and len(rs)!=3:raise ValueError('three distinct factors required')
    return n,d,rs

def default(level,seed,template,parameters,profile,field_type):
    rng=random.Random(seed)
    # Complete bank selected before parameters, never from a first-valid pool.
    layout=field_type or rng.choice(['blank','radio'])
    if layout not in ('blank','radio'):raise ValueError('field type')
    profile=profile or ('method_numerator' if template=='numerator_quadratic' else 'method_omission_sign')
    if profile not in ('method_numerator','method_omission_sign'):raise ValueError('profile')
    for _ in range(1000):
        p=dict(parameters) if parameters is not None else sample(template,rng)
        try:
            n,d,rs=check_parameters(template,p,level)
            bank=answer_bank(rs,n,profile) if layout=='radio' else []
            break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('no whole eligible instance found')
    name=p['function'];expr=n/d
    if template=='sum':formula=frac(str(p['a']),linear(1,-p['r']))+'+'+frac(str(p['b']),linear(1,-p['t']))
    elif template=='factored_three':formula=frac(polynomial(n),factor(p['r'])+factor(p['t'])+factor(p['v']))
    else:formula=frac(polynomial(n),polynomial(d))
    if layout=='blank':problem='In **ascending order**, the vertical asymptotes of $'+name+'(x)='+formula+'$ are\n\n'+' and '.join('$x=$\n{{field-'+str(i+1)+'}}' for i in range(len(rs)))+'.'
    else:problem='Determine the vertical asymptotes of $'+name+'(x)='+formula+'.$'
    solution=authored_solution(expr,name,rs,layout=='blank')
    if template=='factored_three':
        solution=OPENING+'\n\n'+NO_COMMON+'\n\n$$\n'+''.join(factor(r) for r in rs)+'=0\n$$\n\n'+conclusion(rs,layout=='blank')
    if template=='sum':
        r,t,a,b=(p[k] for k in ('r','t','a','b'))
        df=factor(r)+factor(t)
        # Structural masks preserve the common denominator, distribution and
        # collection separately. Signs are rendered as polynomial terms.
        common=str(a)+factor(t)+'+'+str(b)+factor(r)
        first=polynomial(a*X)+('+' if -a*t>=0 else '-')+str(abs(a*t))
        second=polynomial(b*X)+('+' if -b*r>=0 else '-')+str(abs(b*r))
        distributed=first+'+'+second
        rows=[formula,frac(common,df),frac(distributed,df),frac(polynomial(n),df)]
        pre=OPENING+'\n\nAdding both fractions and then factoring the numerator and denominator, we get\n\n$$\n'+r'\begin{aligned}'+name+'(x) & ='+(r' \\  & ='.join(rows))+r'.\end{aligned}'+'\n$$\n\n'
        solution=pre+NO_COMMON+'\n\n$$\n'+df+'=0\n$$\n\n'+conclusion(rs,layout=='blank')
    return finish(level,template,p,profile,problem,solution,layout,bank,rs,seed,'authored-default',{'evidence_only':False,'eligible_for_learning':True})

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in DEFAULTS:raise ValueError('difficulty')
    if template is None and profile and profile.removesuffix('_raw') in OBS:template=profile.removesuffix('_raw')
    template=template or random.Random(seed).choice(DEFAULTS[level])
    if template in OBS:
        if field_type is not None:raise ValueError('observed layout is fixed')
        return observed(level,seed,template,parameters,profile or template)
    if template not in DEFAULTS[level]:raise ValueError('template/level scope')
    return default(level,seed,template,parameters,profile,field_type)

# EASY: denominator factorization, repeated root or supplied linear factors.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: numerator GCF/linear factor plus denominator quadratic; no cancellation.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: exactly two proper fractions, combine/distribute/collect, then solve poles.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];out=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        if f[':answer-field/type'].endswith('/radio'):out+=['- '+a[':answer/value'] for a in f[':answer-field/choices']]
    out+=['\nWorked solution:\n',q.get(':question/worked-solution','[Source worked solution not supplied.]')]
    return '\n'.join(out)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type',choices=['blank','radio']);a=ap.parse_args()
    levels=list(DEFAULTS) if a.difficulty=='all' else [a.difficulty]
    records=[generate(l,a.seed+i,a.template,a.field_type,profile=a.profile) for l in levels for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
