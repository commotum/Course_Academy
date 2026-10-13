#!/usr/bin/env python3
"""Cotangent horizontal stretch / vertical shift, frozen basis 1356.

Steps 3–7 only. Observed scalar banks are explicit opaque scaling-ray replay
profiles, never normal defaults. Their numeric reproduction is not an inferred
error model. Normal defaults choose a complete method-derived bank BEFORE
parameters and reject the whole instance on any collision. See private evidence.

Easy (authored): identify B alone from familiar rational period labels, no final
combination; the integer midpoint height is incidental to this response.
Moderate (observed family): read B and D, evaluate B+kD; one rational scale may
be present. Hard (authored): both scales fractional, quarter/fifth labels and
signed D, same period/midpoint method, no phase shift or amplitude assessment.
The grid increment and requested expression are mathematical task features.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
from functools import lru_cache

KP_ID=17592186184148
KP_UUID='dac9c72b-c23f-56fa-b939-6e3b56d3a13b'
TITLE='Identifying the Horizontal Stretch and Vertical Shift of a Transformed Cotangent Curve'
VERSION='cot-stretch-shift-1'
HERE=Path(__file__).with_suffix('')
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
RAW=json.loads((HERE/'source.json').read_text())['record']
CASES=json.loads((HERE/'source-cases.json').read_text())
OBS={c['bank_profile']:(c,q) for c,q in zip(CASES,RAW[':knowledge-point/questions'])}
MATH=re.compile(r'\$\$[\s\S]*?\$\$|\$[^$]*\$')
NAMESPACE=uuid.UUID(KP_UUID)

def tex(v):
    v=sp.Rational(v)
    sign='-' if v<0 else '';v=abs(v)
    return sign+(str(v.p) if v.q==1 else r'\frac{'+str(v.p)+'}{'+str(v.q)+'}')

def period_tex(b):
    t=1/b
    n=(str(t.p) if t.p!=1 else '')+r'\pi '
    return n.strip() if t.q==1 else r'\frac{'+n+'}{'+str(t.q)+'}'

def argument_tex(b):
    return (str(b.p)+'x' if b.p!=1 else 'x') if b.q==1 else r'\frac{'+(str(b.p) if b.p!=1 else '')+'x}{'+str(b.q)+'}'

def expression(k):
    return 'B' if k==0 else 'B'+('+' if k>0 else '-')+('' if abs(k)==1 else str(abs(k)))+'D'

def final_curve(b,d):
    return r'y=\operatorname{cot}⁡('+argument_tex(b)+')'+('+' if d>0 else '-')+tex(abs(d))+'.'

def arithmetic(b,d,k,style='normal'):
    ex=expression(k);bs=tex(b);ds=tex(d);ans=tex(b+k*d)
    if k==0:return 'B='+bs+'.'
    if abs(k)==2:
        first=bs+('+' if k>0 else '-')+str(abs(k))+r'\cdot ('+ds+')'
        term=k*d
        second=bs+('+' if term>=0 else '-')+tex(abs(term))
        return ex+'='+first+'='+second+'='+ans+'.'
    if k==1:
        first=bs+'+'+('('+ds+')' if d<0 else ds)
        return ex+'='+first+'='+ans+'.'
    first=('('+bs+')' if style=='minus_group' else bs)+'-'+('('+ds+')' if d<0 else ds)
    extra=('='+bs+'+'+tex(-d)) if d<0 else ''
    return ex+'='+first+extra+'='+ans+'.'

def source_solution(q,b,d,k):
    """Complete math-token slots only; untouched interstitial prose/layout.

    All eleven source math tokens are accounted for. Period subtraction and
    redundant arithmetic omissions follow each observed source's own mask.
    """
    old=q[':question/worked-solution']; tokens=MATH.findall(old)
    assert len(tokens)==11
    sid=q[':question/math-academy-id'];t=period_tex(b)
    if sid=='q-141999':row='$'+t+'.$'
    else:row='$$\nT='+t+('-0='+t if sid in ('q-117798','q-117800','q-117799') else '')+'.\n$$'
    replacements={1:row,5:'$$\n'+t+r'=\frac{\pi }{B}\,⟹\,B=\frac{\pi }{('+t+')}='+tex(b)+'.\n$$',7:'$'+tex(abs(d))+'$',8:'$D='+tex(d)+'.$',9:'$'+arithmetic(b,d,k,'minus_group' if sid=='q-65550' else 'normal')+'$',10:'$$\n'+final_curve(b,d)+'\n$$'}
    index=iter(range(len(tokens)))
    text=MATH.sub(lambda m:replacements.get(next(index),m.group()),old)
    # Direction is prose, not a short math replacement.
    text=re.sub(r'units? (up|down)',lambda m:('unit' if abs(d)==1 else 'units')+' '+('up' if d>0 else 'down'),text)
    # Source q-143669 uses singular "unit" for a fraction; retain that layout.
    if sid=='q-143669':text=text.replace('units down','unit down').replace('units up','unit up')
    return text

def default_solution(b,d,k):
    t=period_tex(b)
    return ('The period $T$ of the function is\n\n$$\nT='+t+'.\n$$\n\n'
            'The formula for the period $T$ of the function $y=A\\operatorname{cot}⁡(Bx+C)+D$ is given by \n\n$$\nT=\\frac{\\pi }{B}.\n$$\n\n'
            'Applying the formula of the period, we get\n\n$$\n'+t+r'=\frac{\pi }{B}\,⟹\,B=\frac{\pi }{('+t+')}='+tex(b)+'.\n$$\n\n'
            'The parameter $D$ represents the vertical shift of the cotangent function. We see that the function has been translated by $'+tex(abs(d))+'$ '+('unit' if abs(d)==1 else 'units')+' '+('up' if d>0 else 'down')+'. Hence, $D='+tex(d)+'.$\n\n'
            'Therefore, $'+arithmetic(b,d,k)+'$\n\nFinally, the equation of the curve is\n\n$$\n'+final_curve(b,d)+'\n$$')

def parse_source_scalar(v):
    # The frozen banks contain only signed integers and rational fractions.
    m=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',v)
    return sp.Rational((-1 if m[1] else 1)*int(m[2]),int(m[3])) if m else sp.Rational(v)

def bank(profile,b,d,k):
    correct=b+k*d
    if profile in OBS:
        c,q=OBS[profile];b0=sp.Rational(c['parameters']['B']);d0=sp.Rational(c['parameters']['D'])
        scale=correct/(b0+k*d0)
        return [[parse_source_scalar(a[':answer/value'])*scale for a in f[':answer-field/choices']] for f in q[':question/answer-fields']]
    if profile=='method_sign_period':
        # correct; read 1/B instead of B; reverse D; double period -> B/2;
        # halve period -> 2B. Fixed complete five-option bank.
        return [[correct,1/b+k*d,b-k*d,b/2+k*d,2*b+k*d]]
    if profile=='method_midpoint_offset':
        # correct; mistake cot(pi/4)=1 height for D; cot(3pi/4)=-1;
        # omit D; replace B by horizontal stretch 1/B.
        return [[correct,b+k*(d+1),b+k*(d-1),b,1/b+k*d]]
    if profile=='easy_period':return [[b,1/b,2*b,b/2,2/b]]
    raise ValueError('Unknown bank profile: '+str(profile))

def valid_bank(values):
    return all(len(v)==5 and len(set(v))==5 for v in values)

@lru_cache(None)
def domain(level):
    # Reduced rationals only: common scaling never adds a task.
    bs=sorted({sp.Rational(n,q) for q in (1,2,4,5) for n in range(1,21) if sp.Rational(1,2)<=sp.Rational(n,q)<=8})
    if level=='easy':return [(b,sp.Rational(d),0) for b in bs for d in range(1,5)]
    ds=sorted({sp.Rational(n,q) for q in (1,2,4,5) for n in range(-25,26) if n and abs(sp.Rational(n,q))<=5})
    if level=='moderate':return [(b,d,k) for b in bs for d in ds for k in (-2,-1,1,2) if b.q<=2 or d.q<=2]
    return [(b,d,k) for b in bs for d in ds for k in (-2,-1,1,2) if b.q in (4,5) and d.q in (4,5)]

@lru_cache(None)
def eligible_domain(level,profile):
    return tuple(p for p in domain(level) if valid_bank(bank(profile,*p)))

def validate_parameters(level,p,observed):
    if set(p)!={'B','D','k'}:raise ValueError('Parameters must contain B,D,k exactly')
    b=sp.Rational(p['B']);d=sp.Rational(p['D']);k=int(p['k'])
    if k!=p['k'] and str(k)!=str(p['k']):raise ValueError('k must be integral')
    if observed:
        if not (0<b<=8 and 0<abs(d)<=5 and b.q in (1,2,4,5) and d.q in (1,2,4,5)):raise ValueError('Observed-family bounds')
    elif (b,d,k) not in domain(level):raise ValueError('Parameters outside authored '+level+' workload bounds')
    return b,d,k

def render_plots(instance,output_dir=HERE/'plots'):
    """Matplotlib renderer uses unique inputs and atomic PNG/sidecar writes."""
    output_dir=Path(output_dir);output_dir.mkdir(exist_ok=True,parents=True)
    key=hashlib.sha256(json.dumps(instance,sort_keys=True).encode()).hexdigest()[:24]
    path=output_dir/(key+'.png');side=path.with_suffix('.json')
    if not (path.exists() and side.exists()):
        fd,temp=tempfile.mkstemp(prefix='render-input-',suffix='.json',dir=output_dir)
        try:
            with os.fdopen(fd,'w') as f:json.dump({'instance':instance,'path':str(path)},f)
            subprocess.run([sys.executable,str(HERE/'render.py'),temp],check=True,capture_output=True,text=True)
        finally:Path(temp).unlink(missing_ok=True)
    return {'prompt':str(path),'geometry':json.loads(side.read_text())}

def _uid(value):return str(uuid.uuid5(NAMESPACE,value))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    observed=profile in OBS
    if profile is not None and not observed and profile not in ('method_sign_period','method_midpoint_offset','easy_period'):raise ValueError('Unknown profile')
    template=('B_only' if level=='easy' else 'linear_combination') if template is None else template
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio shape supported')
    if template not in ('B_only','linear_combination'):raise ValueError('Unknown template')
    if observed:
        if level!='moderate' or template!='linear_combination':raise ValueError('Observed profiles require moderate linear_combination')
        c,sourceq=OBS[profile]
        parameters=c['parameters'] if parameters is None else parameters
    else:
        if (level=='easy')!=(template=='B_only'):raise ValueError('Template incompatible with difficulty')
        profile=profile or ('easy_period' if level=='easy' else rng.choice(('method_sign_period','method_midpoint_offset')))
        if (level=='easy')!=(profile=='easy_period'):raise ValueError('Bank incompatible with workload')
    if parameters is not None:
        b,d,k=validate_parameters(level,parameters,observed)
        if observed and k!=c['parameters']['k']:raise ValueError('Observed requested expression is fixed')
        values=bank(profile,b,d,k)
        if not valid_bank(values):raise ValueError('Whole-bank collision')
    else:
        eligible=eligible_domain(level,profile)
        b,d,k=rng.choice(eligible);values=bank(profile,b,d,k)
    p={'B':str(b),'D':str(d),'k':k}
    geometry={'B':str(b),'D':str(d),'x_mid_pi':str(1/(2*b)),'x_asymptote_pi':str(1/b),'y_increment':str(sp.Rational(1,d.q))}
    assets=render_plots(geometry)
    if observed:
        # Reuse exact source raster only for equal complete geometry. It is also
        # independently rendered and compared during QA, never answer lookup.
        original=c['parameters'];same=(b==sp.Rational(original['B']) and d==sp.Rational(original['D']))
        prompt=sourceq[':question/problem']
        if not same:prompt=re.sub(r'!\[\]\([^)]+\)','![]('+assets['prompt']+')',prompt,count=1)
        solution=source_solution(sourceq,b,d,k)
    else:
        prompt='![]('+assets['prompt']+')\n\nThe graph above shows the function $y=\\operatorname{cot}⁡(Bx)+D,$ where $B$ and $D$ are constants. What is $'+expression(k)+'?$'
        solution=default_solution(b,d,k)
    # Complete displayed bank, prompt, solution, level and renderer geometry.
    identity=json.dumps({'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'banks':[[tex(x) for x in sorted(v)] for v in values],'geometry':geometry},sort_keys=True)
    fingerprint=hashlib.sha256(json.dumps({'B':str(b),'D':str(d) if k else None,'k':k,'grid':geometry['y_increment'] if k else None,'assessed':'period_and_shift' if k else 'period'},sort_keys=True).encode()).hexdigest()
    qid=_uid(identity);fields=[]
    for i,v in enumerate(values):
        fid=_uid(qid+'/field/'+str(i));choices=[{':answer/id':_uid(fid+'/'+tex(x)),':answer/type':':answer.type/math',':answer/value':tex(x)} for x in v]
        rng.shuffle(choices)
        f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
        rawfield=sourceq[':question/answer-fields'][i] if observed else None
        if rawfield is None or ':answer-field/correct' in rawfield:f[':answer-field/correct']=[':answer/id',_uid(fid+'/'+tex(b+k*d))]
        fields.append(f)
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'provenance':PROVENANCE,'python':sys.version.split()[0],'sympy':sp.__version__,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'parameter_fingerprint':fingerprint,'content_identity':hashlib.sha256(identity.encode()).hexdigest(),'source_id':c['source_id'] if observed else None,'authored_extension':not observed,'eligible_for_learning':not observed,'evidence_only':observed,'plots':assets,'answer':tex(b+k*d),'scope':'A=1; C=0; B positive; cotangent decreasing branch; no endpoints'}}

# Easy: authored single-period reconstruction; integer height is incidental.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed method with unordered signed/rational B+kD variations.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: authored simultaneous quarter/fifth reading, same operation sequence.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];g=r['generation'];preview=re.sub(r'\]\((images/[^)]+)\)',lambda m:'](/media/jake/SSD/EDB/math/'+m[1]+')',q[':question/problem']);parts=['### '+q[':question/difficulty'].split('/')[-1]+' / '+g['bank_profile'],preview]
    for i,f in enumerate(q[':question/answer-fields']):parts.append('Field '+str(i+1)+' (radio)\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']))
    parts.extend(['Worked solution',q[':question/worked-solution'],'Review metadata: '+json.dumps({'parameters':g['parameters'],'template':g['template'],'profile':g['bank_profile'],'eligible':g['eligible_for_learning']}),'Rendered prompt: '+g['plots']['prompt']])
    return '\n\n'.join(parts)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    rs=[generate(level,a.seed+i,template=a.template,profile=a.profile) for level in (('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
    print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
