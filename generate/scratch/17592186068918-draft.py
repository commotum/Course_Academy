"""Private basis-2275 draft; never imported from the registered generator.

Observed masks retain complete source formal chains; m scales each actual integral
operand and every primitive, not a lookup of source answers. Historical banks are
bounded public evidence profiles. Normal banks describe real substitution errors.
"""
import argparse, hashlib, importlib.util, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().with_suffix('')
def frozen(name):
    spec=importlib.util.spec_from_file_location('quotient_draft_'+name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
fmt=frozen('math_format');printed=frozen('printed')
x=printed.x;u=printed.u
KP_ID=17592186068918;KP_UUID='fc24eade-1b3d-5672-88fd-0bb48b371509'
TITLE='Integrating Quotients Containing Trigonometric Functions Using Substitution'
VERSION='quotient-private-2275-v1'
SOURCE=json.loads((HERE/'source.json').read_text());QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
# Ordered source roles: substitution, factor, transformed integrand, primitive,
# original independent variable, bounds. No unobserved algebra branches.
DATA={
'q-49557':('easy',sp.sin(x),sp.Integer(2),1/u,sp.log(u),'y',None,None),
'q-10046':('moderate',1+sp.sec(x),sp.Integer(1),1/u,sp.log(u),'x',0,sp.pi/4),
'q-10045':('hard',1+sp.sin(x),sp.Integer(1),1/u,sp.log(u),'x',-1,1),
'q-113998':('hard',sp.csc(x)+2,sp.Integer(-2),1/u,sp.log(u),'x',None,None),
'q-350887':('hard',sp.sin(x)**2+3,sp.Integer(1),1/u,sp.log(u),'x',0,sp.pi/2),
'q-350901':('hard',8*sp.cos(x)**3+5,sp.Integer(-1),1/u,sp.log(u),'x',sp.pi/3,sp.pi/2),
'q-350904':('hard',sp.csc(x)+2,sp.Integer(-1),1/u,sp.log(u),'x',sp.pi/6,sp.pi/2),
'q-73674':('hard',sp.sin(x**2),sp.Rational(1,2),1/u,sp.log(u),'y',None,None),
'q-113997':('hard',sp.tan(x)+1,sp.Integer(1),1-1/u,u-sp.log(u),'x',None,None)}
LEVELS=('easy','moderate','hard')
def latex(e):return sp.latex(e).replace(r'\log',r'\ln')
def realtex(e):
    # Replace each logarithm as a complete component before CAS TeX output.
    logs=sorted(e.atoms(sp.log),key=str);names={z:sp.Symbol('LOGSLOT'+str(i)) for i,z in enumerate(logs)}
    out=latex(e.xreplace(names))
    for z,n in names.items():out=out.replace(latex(n),r'\ln|'+latex(z.args[0])+'|')
    return out

def scalar_scale(text,m):
    """Identity renderer and nonunit multiplier for a complete primitive component."""
    match=re.search(r'\+([CK])\s*$',text)
    core=text[:match.start()] if match else text
    suffix='+'+match[1] if match else ''
    return (core if m==1 else str(m)+r'\left('+core+r'\right)')+suffix

def operand_scale(text,m):
    """Place amplitude inside integral operands; preserve original bounds/order."""
    if m==1:prefix=''
    else:prefix=str(m)+r'\cdot '
    pattern=re.compile(r'(?:\{\\int\s*\}|\\int)')
    inserts=[]
    for token in pattern.finditer(text):
        end=token.end();i=end
        while i<len(text) and text[i].isspace():i+=1
        if text[i:i+1]=='_':
            if text[i+1]=='{':_,i=printed.group(text,i+1)
            else:i+=2
            if text[i:i+1]!='^':raise ValueError('Integral bound mask')
            if text[i+1]=='{':_,i=printed.group(text,i+1)
            else:i+=2
            end=i
        inserts.append(end)
    for end in reversed(inserts):text=text[:end]+prefix+text[end:]
    return text

def source_solution(t,m):
    """Source prose/formal derivatives unchanged; ordered algebra rows are slots."""
    old=QUESTIONS[t].get(':question/worked-solution')
    if old is None:return None
    def chain(z):
        rows=z[1].split('\\\\');result=[]
        for row in rows:
            if '&' not in row:raise ValueError('Unexpected source aligned row')
            left,right=row.split('&',1)
            left=operand_scale(left,m)
            eq=re.match(r'(\s*=\s*)(.*?)(\s*)$',right,re.S)
            body=eq[2]
            body=operand_scale(body,m) if r'\int' in body else scalar_scale(body,m)
            result.append(left+'&'+eq[1]+body+eq[3])
        return r'\begin{aligned}'+'\\\\'.join(result)+r'\end{aligned}'
    out=re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',chain,old,flags=re.S)
    if t=='q-113997':out=out.replace('$K=C+1.$','$K=C+'+str(m)+'.$')
    return out

def math_data(t,params):
    if t=='shifted-sine':
        k,a=params['k'],params['a'];inner=a+sp.sin(x);factor=sp.Integer(k);h=1/u;H=sp.log(u);lo=hi=None;var='x'
    else:
        _,inner,c,h,H,var,lo,hi=DATA[t];factor=c*params['m']
    f=factor*sp.diff(inner,x)*h.subs(u,inner)
    F=factor*H.subs(u,inner)
    answer=F if lo is None else F.subs(x,hi)-F.subs(x,lo)
    return f,F,answer,factor,inner,h,H,var,lo,hi

def integral(operand,var,lo=None,hi=None):
    limits='' if lo is None else '_{'+latex(lo)+'}^{'+latex(hi)+'}'
    return r'\int'+limits+' '+operand+r'\,\text{d}'+var

def authored_solution(t,params):
    f,F,a,c,g,h,H,var,lo,hi=math_data(t,params)
    v=lambda e:latex(e).replace('x',var)
    num=sp.cancel(c*sp.diff(g,x));I=integral(r'\frac{'+v(num)+'}{'+v(g)+'}',var,lo,hi)
    out='Let $u='+v(g)+'.$ Differentiating, we have\n\n$$\n'+r'\frac{\text{d}u}{\text{d}'+var+'}='+v(sp.diff(g,x))+r'\,⟹\,\text{d}u='+v(sp.diff(g,x))+r'\,\text{d}'+var+'.\n$$\n\n'
    if lo is not None:
        ul=sp.simplify(g.subs(x,lo));uh=sp.simplify(g.subs(x,hi))
        out+='Calculating the limits for $u$ gives\n\n| $'+var+'$ | $'+latex(lo)+'$ | $'+latex(hi)+'$ |\n| --- | --- | --- |\n| $u$ | $'+latex(ul)+'$ | $'+latex(uh)+'$ |\n\n'
    out+='Using the above, we can write the integral in terms of $u$ and evaluate:\n\n$$\n'+r'\begin{aligned}'+I+' &= '+integral(r'\frac{1}{'+v(g)+r'}\cdot ('+v(num)+')',var,lo,hi)
    if lo is None:
        out+=r' \\ &= \int \frac{1}{u}\cdot '+latex(c)+r'\,\text{d}u \\ &= '+latex(c)+r'\int \frac{1}{u}\,\text{d}u \\ &= '+realtex(c*sp.log(u))+'+C'+r' \\ &= '+realtex(F).replace('x',var)+'+C'
    else:
        lim='_{'+latex(ul)+'}^{'+latex(uh)+'}'
        out+=r' \\ &= \int'+lim+r'\frac{1}{u}\cdot '+latex(c)+r'\,\text{d}u \\ &= '+latex(c)+r'\ln|u|\big|'+lim+r' \\ &= '+latex(c)+r'\left(\ln('+latex(uh)+r')-\ln('+latex(ul)+r')\right)'+r' \\ &= '+scalar_scale(latex(sp.log(uh)-sp.log(ul)),int(c))
    return out+r'\end{aligned}'+'\n$$'

def source_bank(t,m):return [scalar_scale(z[':answer/value'],m) for z in QUESTIONS[t][':question/answer-fields'][0][':answer-field/choices']]

def method_bank(t,params):
    f,F,a,c,g,h,H,var,lo,hi=math_data(t,params)
    if lo is not None:
        L=sp.log(g.subs(x,lo));U=sp.log(g.subs(x,hi))
        if t in ('q-350887','q-350901','q-350904'):
            of=QUESTIONS[t][':question/answer-fields'][0]
            return [scalar_scale(of[':answer-field/correct'][':answer/value'],params['m'])]
        # Upper minus lower, reversed limits, addition, omitted lower, omitted upper.
        return [latex(z) for z in [a,-a,c*(U+L),c*U,-c*L]]
    if t=='q-113997':
        b=sp.tan(x);values=[c*(b-sp.log(b+1)),c*(b+sp.log(b+1)),c*sp.log(b+1),c*(b-sp.log(b)),c*(g*g/2-g)]
    elif t=='shifted-sine':
        # Omit denominator shift; reverse derivative sign; omit reciprocal integral;
        # apply squared-denominator primitive instead of the logarithm.
        values=[F,c*sp.log(sp.sin(x)),-F,c*g,-c/g]
    elif t=='q-49557':
        values=[F,c*sp.log(sp.cos(x)),-F,c*sp.sin(x),-c/sp.sin(x)]
    elif t=='q-113998':
        values=[F,-F,(c/2)*sp.log(g),c*sp.log(sp.csc(x)),-c/g]
    elif t=='q-73674':
        values=[F,2*F,-F,c*sp.log(sp.cos(x**2)),-c/g]
    else:raise ValueError(t)
    return [realtex(z).replace('x',var)+'+C' for z in values]

def profiles(t):return ('observed','method') if t in DATA else ('method',)
def domains(level,template=None,profile=None):
    """One finite public domain; samplers and explicit-input validation share it."""
    if level not in LEVELS:raise ValueError('Unsupported difficulty')
    if profile=='raw':profile='observed'
    ts=[t for t,v in DATA.items() if v[0]==level]+(['shifted-sine'] if level=='moderate' else [])
    if template is not None:
        if template not in ts:raise ValueError('Template does not belong to this level')
        ts=[template]
    for t in ts:
        choices=profiles(t) if profile is None else (profile,)
        for pr in choices:
            if pr not in profiles(t):raise ValueError('Unsupported complete bank profile')
            if t=='shifted-sine':
                for a in range(2,7):
                    for k in range(1,13):yield t,pr,{'k':k,'a':a}
            else:
                for m in range(1,13):yield t,pr,{'m':m}

def eligible(t,profile):return profile=='method'
def validate_params(level,t,profile,params):
    if not isinstance(params,dict) or any(type(v)is not int for v in params.values()):raise ValueError('Parameters require strict built-in int values; bool is invalid')
    if not any(t==tt and profile==pp and params==d for tt,pp,d in domains(level,t,profile)):raise ValueError('Parameters outside shared finite domain')

def math_fingerprint(f,lo,hi):
    return digest([sp.srepr(sp.cancel(sp.expand_trig(sp.trigsimp(f)).rewrite(sp.sin).expand(trig=True))),None if lo is None else sp.srepr(sp.sympify(lo)),None if hi is None else sp.srepr(sp.sympify(hi)),'antiderivative-mod-C' if lo is None else 'definite-scalar'])
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if type(seed)is not int:raise ValueError('Seed must be a strict built-in int')
    if profile=='raw':profile='observed'
    candidates=[z for z in domains(level,template,profile) if profile is not None or eligible(z[0],z[1])]
    if field_type is not None:
        field_type=field_type.rsplit('/',1)[-1]
        if field_type not in ('radio','blank'):raise ValueError('Unsupported field type')
        candidates=[z for z in candidates if ('blank' if z[0] in ('q-350887','q-350901','q-350904') else 'radio')==field_type]
    if not candidates:raise ValueError('No supported combination')
    if parameters is not None:
        if template is None:raise ValueError('Explicit parameters require a template')
        pr=profile or 'method';validate_params(level,template,pr,parameters)
        if (template,pr,parameters) not in candidates:raise ValueError('Field/profile mismatch')
        t,pr,params=template,pr,dict(parameters)
    else:
        rng=random.Random(seed);family=rng.choice(sorted({(z[0],z[1]) for z in candidates}));t,pr,params=rng.choice([z for z in candidates if z[:2]==family])
    f,F,a,c,g,h,H,var,lo,hi=math_data(t,params);raw=pr=='observed';old=QUESTIONS.get(t)
    blank=t in ('q-350887','q-350901','q-350904');ft='blank' if blank else 'radio';key='field-1' if blank else 'selection'
    if t=='shifted-sine':
        num=latex(params['k']*sp.cos(x));prompt='Calculate $'+integral(r'\frac{'+num+'}{'+latex(g)+'}','x')+'.$';solution=authored_solution(t,params)
    else:
        m=params['m'];prompt=operand_scale(old[':question/problem'],m);solution=source_solution(t,m)
        if not raw and solution is None:solution=authored_solution(t,params)
        if not raw:prompt=prompt.replace('Do not round the answer.','Give an exact answer.')
    values=source_bank(t,params['m']) if raw else method_bank(t,params)
    ci=None
    if raw and ':answer-field/correct' in old[':question/answer-fields'][0]:
        of=old[':question/answer-fields'][0];ci=next(i for i,z in enumerate(of[':answer-field/choices']) if z[':answer/id']==of[':answer-field/correct'][':answer/id'])
    elif not raw:ci=0
    if not raw:
        prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution);values=[fmt.normalize_tex(z) for z in values]
    # No opaque source bank is served as eligible learning content.
    identity=digest([VERSION,level if not(raw and ':question/difficulty' not in old) else None,prompt,solution,ft,key,sorted(values),None if ci is None else values[ci]])
    qid=uid('question:'+identity);fid=uid(qid+':field:'+key)
    answers=[{':answer/id':uid(fid+':answer:'+str(i)+':'+v),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
    field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers}
    if ci is not None:field[':answer-field/correct']=[':answer/id',answers[ci][':answer/id']]
    if ft=='radio':random.Random(seed).shuffle(answers)
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if solution is not None:question[':question/worked-solution']=solution
    if not raw or ':question/difficulty' in old:question[':question/difficulty']=':question.difficulty/'+level
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':pr,'parameters':params,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'source_question':t if old else None,'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':math_fingerprint(*printed.integral(prompt)),'content_fingerprint':identity,'domain':'Connected real intervals excluding every displayed denominator zero and trigonometric pole (including choices); real logarithms use absolute values. Definite limits lie in a common pole-free interval with strictly positive substitution.','recipe_policy':'Complete historical expression patterns; error intent unproven.' if raw else 'Complete method-derived substitution-operation bank.','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
    # Raw absence of solution/key/rating must survive public replay.
    if not raw:fmt.validate_generated_record(record)
    return record

# Easy: authored completion of direct sin quotient, k=2m (m1..12).
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: authored shifted sine k cos(x)/(a+sin(x)), a2..6, k1..12;
# also independently completed familiar-angle secant definite source (unrated).
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: original rated definite, nested square-argument, and u-constant rewrite masks.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def candidates(level):
    for t,p,d in domains(level):
        if eligible(t,p):yield t,d

def batch(level,count=1,seed=0,template=None,profile=None,field_type=None):
    if type(count)is not int or count<1:raise ValueError('Positive strict integer count required')
    pool=list(domains(level,template,profile))
    if field_type is not None:
        ft=field_type.rsplit('/',1)[-1]
        if ft not in ('radio','blank'):raise ValueError('Unsupported field type')
        pool=[z for z in pool if ('blank' if z[0] in ('q-350887','q-350901','q-350904') else 'radio')==ft]
    random.Random(seed).shuffle(pool);seen=set();records=[]
    for t,pr,params in pool:
        if profile is None and not eligible(t,pr):continue
        r=generate(level,seed,t,field_type,params,pr);fp=r['generation']['mathematical_fingerprint']
        if fp in seen:continue
        seen.add(fp);records.append(r)
        if len(records)==count:return records
    raise ValueError('Finite mathematical task limit: '+str(len(records)))
def markdown(r):
    q=r['question'];out=q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):
        ref=f.get(':answer-field/correct',[None,None])[1]
        out+='\n'.join('- $'+z[':answer/value']+'$'+(' (correct)' if z[':answer/id']==ref else '') for z in f[':answer-field/choices'])+'\n\n'
    return out+q.get(':question/worked-solution','[Source has no worked solution.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    levels=LEVELS if args.difficulty=='all' else (args.difficulty,)
    rs=[r for level in levels for r in batch(level,args.count,args.seed,args.template,args.profile)]
    print(json.dumps(rs,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(map(markdown,rs)))
