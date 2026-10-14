#!/usr/bin/env python3
"""Local basis2275 draft: constant/linear logarithmic integration; no database IO.
Historical complete banks are parameterized evidence profiles. Normal defaults use
explicit complete method-derived banks, chosen before parameters. Missing levels
are authored arithmetic bands, not recovered Math Academy difficulty claims.
"""
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064206
KP_UUID='fc4294d6-3d60-5c9e-a862-863e1d129049'
TITLE='Integrating a Linear Rational Function'
VERSION='linear-rational-draft-v2'
PACKAGE=Path(__file__).with_suffix('')
SOURCE=json.loads((PACKAGE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
PROFILES=json.loads((PACKAGE/'contract.json').read_text())['profiles']
PARAMETERS={'q-15707':[2,1,1],'q-49450':[1,1,-1],'q-49452':[1,-3,2],'q-49453':[3,1,4],'q-49454':[1,1,3],'q-49511':[2,3,5]}
x=sp.Symbol('x',real=True)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(v):return sp.latex(sp.Rational(v)).replace('- ', '-')
def coefficient(v):return '' if v==1 else '-' if v==-1 else tex(v)
def linear(a,b,order='slope-first'):
    ax=coefficient(a)+'x'
    bt=('+' if b>0 else '-')+tex(abs(b))
    return (tex(b)+('+' if a>0 else '')+ax) if order=='offset-first' else ax+bt

def log(c,d,style='source'):return coefficient(c)+(r'\operatorname{ln}⁡|' if style=='source' else r'\ln|')+d+'|+C'
def fingerprint(p):
    c,a,b=p
    return digest(['constant-over-linear',str(sp.cancel(c/(a*x+b)))])
def parse_parameters(parameters):
    if isinstance(parameters,dict):parameters=[parameters[k] for k in ('n','a','b')]
    if not isinstance(parameters,(list,tuple)) or len(parameters)!=3:raise ValueError('parameters must be [n,a,b] or n/a/b mapping')
    try:p=tuple(sp.Rational(v) for v in parameters)
    except Exception as e:raise ValueError('exact rational coefficients required') from e
    if any(v==0 for v in p):raise ValueError('nonzero numerator, slope and shift required')
    return p

def allowed(level,sid,p,observed=False):
    c,a,b=p
    if observed:
        if sid in ('q-15707','q-49453'):return a==1 and c.q==1 and 2<=c<=12 and b.q==1 and 1<=b<=15
        if sid=='q-49450':return c==a==1 and b.q==1 and -15<=b<=-1
        if sid=='q-49454':return c==a==1 and b.q==1 and 2<=b<=15
        if sid=='q-49452':return c==1 and a.q==b.q==1 and -12<=a<=-2 and 1<=b<=15
        if sid=='q-49511':return c.q==a.q==b.q==1 and 2<=c<=12 and 2<=a<=12 and 1<=b<=15
        return False
    if level=='easy':return sid!='q-49511' and allowed(level,sid,p,True)
    if sid not in ('canonical','q-49511'):return False
    if level=='moderate':return c.q==a.q==b.q==1 and 2<=abs(c)<=12 and 2<=abs(a)<=12 and 1<=abs(b)<=15 and c>0
    if level=='hard':return c.q>=2 and a.q>=2 and 1<=abs(c.p)<=12 and 2<=c.q<=12 and 2<=abs(a.p)<=12 and 2<=a.q<=12 and abs(a)!=1 and b.q==1 and 1<=abs(b)<=15 and 0<c<1
    return False

def bank(sid,profile,p):
    c,a,b=p; d=linear(a,b,'offset-first' if sid=='q-49452' else 'slope-first')
    if profile=='original':
        if sid in ('q-15707','q-49453'):return [log(z,d) for z in (c,1/c,-c,-1/c,1)]
        if sid=='q-49452':return [log(z,d) for z in (1/a,-1/a,a,-a,-1)]
        if sid=='q-49450':return [log(1,d),log(-1,d),log(1,'x'),log(-1,'x'),log(-1,linear(a,-b))]
        if sid=='q-49454':return [log(1,d),log(1/b,d),log(b,d),log(1,'x'),log(b,'x')]
        if sid=='q-49511':
            spaced=tex(a)+'x '+('+' if b>0 else '-')+' '+tex(abs(b))
            return [coefficient(z)+r'\ln \mid '+spaced+r' \mid + C' for z in (c*a,-c/a,c/a,c,-c)]
    if profile=='method':
        if sid in ('q-15707','q-49453'):return [log(z,d) for z in (c,1/c,-c,-1/c,1)]
        if sid=='q-49452':return [log(z,d) for z in (1/a,-1/a,a,-a,-1)]
        if sid in ('q-49450','q-49454'):return [log(1,d),log(-1,d),log(1,'x'),log(-1,'x'),log(1,linear(a,-b))]
        if sid in ('canonical','q-49511'):return [log(z,d) for z in (c/a,-c/a,c,c*a,1/a)]
    raise ValueError('unsupported complete bank profile')

def bank_signature(v):
    # Actual response criterion: primitives modulo C on each common real interval.
    import re
    normalized=v.replace(r'\ln \mid ',r'\ln|').replace(r' \mid + C','|+C')
    m=re.fullmatch(r'(.*?)(?:\\operatorname\{ln\}⁡|\\ln)\|([^|]+)\|\+C',normalized)
    if not m:raise ValueError('unsupported logarithmic primitive')
    ct=m[1];ct='1' if not ct else '-1' if ct=='-' else ct
    ct=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',ct)
    dt=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1/\2)',m[2])
    dt=re.sub(r'(\d|\))x',r'\1*x',dt)
    c=sp.sympify(ct);d=sp.sympify(dt,locals={'x':x});poly=sp.Poly(d,x)
    if poly.degree()!=1:raise ValueError('log argument must be nonconstant real linear')
    return sp.cancel(c*sp.diff(d,x)/d),sp.solve(d,x)[0]
def validate_bank(values,p):
    sig=[bank_signature(v) for v in values]
    for i in range(len(sig)):
        for j in range(i):
            if sp.cancel(sig[i][0]-sig[j][0])==0:raise ValueError('whole-bank equivalence collision modulo C on common domain')
    correct=[i for i,(derivative,pole) in enumerate(sig) if sp.cancel(derivative-p[0]/(p[1]*x+p[2]))==0 and pole==-p[2]/p[1]]
    if len(correct)!=1:raise ValueError('exactly one primitive valid outside prompt pole required')
    return correct[0]

def render_source(sid,p):
    c,a,b=p;t=PROFILES[sid];d=linear(a,b,'offset-first' if sid=='q-49452' else 'slope-first')
    def fill(s):
        for key,value in {'@@D@@':d,'@@N@@':tex(c),'@@INV@@':tex(1/a),'@@A@@':tex(a)}.items():s=s.replace(key,value)
        return s
    return fill(t['prompt']),fill(t['solution'])

def render_canonical(p):
    c,a,b=p;d=linear(a,b);inv=tex(1/a);factor=tex(c/a);num=tex(c)
    prompt='Calculate $'+r'\int \frac{'+num+'}{'+d+r'}\,\text{d}x.$'
    sol='First, let $u='+d+'.$ Then differentiating with respect to $x$ gives\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+tex(a)+r'\,⟹\,\text{d}x='+inv+r'\text{d}u.'+'\n$$\n\nWe can now rewrite the integral in terms of $u,$ solve it, and write the final answer in terms of $x$ as follows:\n\n$$\n'
    rows=[r'\int \frac{'+num+'}{'+d+r'}\,\text{d}x & ='+num+r'\int \frac{1}{'+d+r'}\,\text{d}x',num+r'\int \frac{1}{u}\cdot ('+inv+r'\,\text{d}u)',factor+r'\int \frac{1}{u}\,\text{d}u',log(c/a,'u'),log(c/a,d)]
    return prompt,sol+r'\begin{aligned}'+r' \\  & ='.join(rows)+r'\end{aligned}'+'\n$$'

# EASY: observed arithmetic families; MODERATE/HARD: authored coefficient bands.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio layout supported')
    rng=random.Random(seed);sid=template or rng.choice([sid for sid in PARAMETERS if sid!='q-49511'] if level=='easy' else ['canonical','q-49511'] if level=='moderate' else ['canonical'])
    profile=profile or 'method'
    if profile not in ('original','method','completed'):raise ValueError('unknown profile')
    observed=profile=='original'
    if observed and sid not in PARAMETERS:raise ValueError('original requires source template')
    if sid not in PARAMETERS and sid!='canonical':raise ValueError('unknown template')
    if level=='easy' and not observed and sid in ('canonical','q-49511'):raise ValueError('nonunit numerator and slope completion belongs to authored moderate')
    if observed and level!='easy':raise ValueError('source banks have only easy/unrated evidence')
    if profile=='completed' and sid!='q-49511':raise ValueError('completed is only inferred missing source')
    bp='method' if profile=='completed' else profile
    for attempt in range(1000):
        if parameters is not None:p=parse_parameters(parameters)
        elif level=='hard':p=(sp.Rational(rng.randint(1,11),rng.randint(2,12)),sp.Rational(rng.choice([-1,1])*rng.randint(2,12),rng.randint(2,12)),sp.Integer(rng.choice([-1,1])*rng.randint(1,15)))
        elif level=='moderate':p=tuple(map(sp.Integer,[rng.randint(2,12),rng.choice([-1,1])*rng.randint(2,12),rng.choice([-1,1])*rng.randint(1,15)]))
        elif sid in ('q-15707','q-49453'):p=tuple(map(sp.Integer,[rng.randint(2,12),1,rng.randint(1,15)]))
        elif sid=='q-49450':p=tuple(map(sp.Integer,[1,1,-rng.randint(1,15)]))
        elif sid=='q-49454':p=tuple(map(sp.Integer,[1,1,rng.randint(2,15)]))
        elif sid=='q-49452':p=tuple(map(sp.Integer,[1,-rng.randint(2,12),rng.randint(1,15)]))
        else:p=tuple(map(sp.Integer,[rng.randint(2,12),rng.randint(2,12),rng.randint(1,15)]))
        if not allowed(level,sid,p,observed):
            if parameters is not None:raise ValueError('outside declared difficulty/template bounds')
            continue
        values=bank(sid,bp,p)
        try:ci=validate_bank(values,p)
        except ValueError:
            if parameters is not None:raise
            continue
        break
    else:raise ValueError('eligible complete-bank sampler exhausted')
    if sid in PROFILES:prompt,solution=render_source(sid,p)
    elif sid=='q-49511':
        c,a,b=p;prompt=r'Calculate $\displaystyle \int\frac{'+tex(c)+'}{'+tex(a)+'x '+('+' if b>0 else '-')+' '+tex(abs(b))+'}dx$.'
        solution=None if observed else render_canonical(p)[1]
    else:prompt,solution=render_canonical(p)
    raw_missing=sid=='q-49511' and observed
    payload=[VERSION,level,prompt,solution,sorted(values),{'difficulty_present':not raw_missing,'correct_present':not raw_missing}]
    qid=ident(['question',payload]);fid=ident([qid,'field','selection'])
    choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=choices[ci][':answer/id'];rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    if not raw_missing:field[':answer-field/correct']=[':answer/id',correct]
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw_missing:q.update({':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':profile,'bank_profile':bp,'parameters':[str(v) for v in p],'mathematical_fingerprint':fingerprint(p),'domain':{'real':True,'excluded_pole':str(-p[2]/p[1]),'primitive_convention':'one arbitrary constant on each connected interval outside the pole'},'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'source_ids':[sid] if sid in SOURCES else ['e-449'],'evidence_only':observed,'eligible_for_learning':not observed,'difficulty_evidence':'observed easy' if observed and not raw_missing else 'unrated source, omissions retained' if raw_missing else 'authored arithmetic band','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}
def generate_easy(seed=0,**kwargs):
    """Observed monic-numerator scaling or unit-numerator signed-Jacobian workload."""
    return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):
    """Authored: both numerator and integer slope nonunit; form/reduce c/a."""
    return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):
    """Authored: rational numerator and rational nonunit slope; same five stages."""
    return generate('hard',seed,**kwargs)
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+ ('\n\n'+q[':question/worked-solution'] if ':question/worked-solution' in q else '')
def batch(level,count,seed,template=None,profile=None):
    if count<1:raise ValueError('count must be positive')
    out=[];seen=set()
    for offset in range(max(2000,count*100)):
        rec=generate(level,seed+offset,template=template,profile=profile);fp=rec['generation']['mathematical_fingerprint']
        if fp not in seen:seen.add(fp);out.append(rec)
        if len(out)==count:return out
    raise ValueError('unique task capacity exhausted')
if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');cli.add_argument('--count',type=int,default=1);cli.add_argument('--seed',type=int,default=0);cli.add_argument('--format',choices=['json','markdown'],default='json');cli.add_argument('--template');cli.add_argument('--profile');args=cli.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[r for level in levels for r in batch(level,args.count,args.seed,args.template,args.profile)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
