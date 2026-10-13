#!/usr/bin/env python3
"""Termwise differentiation of a^x, basis 1356. Local review records only.

All exponents are the independent variable x: no chain/product rule.
Observed parameterized masks preserve original complete components/stages;
raw_source profiles expose anomalies, never used by normal sampling.
Easy: formula + linear/quadratic/constant terms. Moderate: same derivative
then evaluate at zero. Hard (authored): two non-e bases and a quadratic,
evaluate at ±1 or ±2. No instructional progression within a level.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
# The inventory worker uses system Python; use the repository dependency environment.
try:
    import sympy as sp
except ModuleNotFoundError:
    import os, sys
    python = Path(__file__).resolve().parents[2] / '.venv/bin/python'
    if python.is_file() and Path(sys.executable).resolve() != python.resolve():
        os.execv(str(python), [str(python), str(Path(__file__).resolve()), *sys.argv[1:]])
    raise

KP_ID=17592186096612
KP_UUID='14e68965-6c39-5947-ac05-eee99e685063'
TITLE='Differentiating an Exponential Function with a Base Other Than e'
VERSION='base-other-than-e-1'
X=sp.Symbol('x',real=True)
ROOT=Path(__file__).with_suffix('')
# Compiled masks, not source payload selection. Slots represent full constants,
# derived coefficients and complete logarithms, leaving powers and prose fixed.
MASKS=json.loads((ROOT/'masks.json').read_text())
TEMPLATES={k:v['level'] for k,v in MASKS.items()}
TEMPLATES['two_bases_rate']='hard'

def tex(e):
    return sp.latex(e,ln_notation=True)

def uid(s):return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def apply(s,vals):
    return re.sub(r'@@([A-Za-z0-9_]+)@@',lambda m:str(vals[m[1]]),s)

def guards(template,p):
    if template=='two_bases_rate':
        required={'b','h','a','c','q','k','t'}
    else:required=set(MASKS[template]['parameters'])
    if set(p)!=required or any(type(v)!=int for v in p.values()):raise ValueError('exact integer parameter keys required: '+str(sorted(required)))
    for key in ('b','h'):
        if key in p and not 2<=p[key]<=9:raise ValueError('base must be an integer 2..9')
    for key in ('a','c','q','l'):
        if key in p and not 1<=p[key]<=12:raise ValueError('positive coefficient magnitude must be 1..12')
    if 'k' in p and not 1<=p['k']<=20:raise ValueError('constant magnitude 1..20')
    if template=='two_bases_rate':
        if p['b']==p['h'] or p['t'] not in (-2,-1,1,2):raise ValueError('hard uses two different bases and nonzero small integer input')
        if any(p[k]>4 for k in ('a','c','q')) or p['b']>6 or p['h']>6 or p['k']>9:raise ValueError('hard workload bounds exceeded')

def sample(template,rng):
    if template=='two_bases_rate':
        b,h=rng.sample(range(2,7),2)
        return dict(b=b,h=h,a=rng.randint(1,4),c=rng.randint(1,4),q=rng.randint(1,4),k=rng.randint(1,9),t=rng.choice([-2,-1,1,2]))
    p={key:rng.randint(2,9) if key=='b' else rng.randint(1,12) if key!='k' else rng.randint(1,20) for key in MASKS[template]['parameters']}
    return p

def values(p):
    v=dict(p)
    if 'q' in p:v.update(q2=2*p['q'],q3=3*p['q'])
    if 'c' in p:v.update(c1=p['c']+1)
    return v

def hard(p):
    b,h,a,c,q,k,t=(p[z] for z in ('b','h','a','c','q','k','t'))
    E=lambda b:r'{'+str(b)+r'}^{x}'
    f=f'{a}\\cdot {E(b)}+{c}\\cdot {E(h)}-{q}x^2+{k}'
    d=f'{a}\\ln({b})\\cdot {E(b)}+{c}\\ln({h})\\cdot {E(h)}-{2*q}x'
    ans=a*sp.Integer(b)**t*sp.log(b)+c*sp.Integer(h)**t*sp.log(h)-2*q*t
    rows=[r"f'(x)&=\frac{\text{d}}{\text{d}x}("+f+')',
      r'&='+f'{a}'+r'\frac{\text{d}}{\text{d}x}('+E(b)+')+'+f'{c}'+r'\frac{\text{d}}{\text{d}x}('+E(h)+')-'+f'{q}'+r'\frac{\text{d}}{\text{d}x}(x^2)+\frac{\text{d}}{\text{d}x}('+str(k)+')',
      '&='+f'{a}({E(b)}\\ln({b}))+{c}({E(h)}\\ln({h}))-{q}(2x)+0', '&='+d+'.']
    evalrows=[r"f'("+str(t)+')&='+d.replace('^{x}','^{('+str(t)+')}').replace('x',f'({t})'),
      '&='+f'{a}({tex(sp.Integer(b)**t)})\\ln({b})+{c}({tex(sp.Integer(h)**t)})\\ln({h})-({2*q})({t})', '&='+tex(ans)+'.']
    sol='Applying the formula, we get\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\nTherefore, the instantaneous rate of change at $x='+str(t)+'$ is\n\n$$\n\\begin{aligned}'+r' \\ '.join(evalrows)+r'\end{aligned}'+'\n$$'
    prompt='Given that $f(x)='+f+'$, find the instantaneous rate of change at $x='+str(t)+'.$\n\n{{field-1}}'
    return prompt,sol,[tex(ans)],0,'blank','field-1'


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown level')
    rng=random.Random(seed)
    if template is None:
        eligible=[k for k,v in TEMPLATES.items() if v==level and (field_type is None or ('blank' if k=='two_bases_rate' else MASKS[k]['field_type'])==field_type)]
        if not eligible:raise ValueError('unsupported field type')
        template=rng.choice(eligible)
    if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('template/level mismatch')
    if profile is not None and profile.startswith('q-'):
        if template=='two_bases_rate' or profile!=MASKS[template]['source_id']:raise ValueError('source bank/template mismatch')
        profile='observed'
    if profile not in (None,'observed','raw_source','normal'):raise ValueError('unsupported bank profile')
    if template=='two_bases_rate' and profile in ('observed','raw_source'):raise ValueError('hard has no observed profile')
    explicit=parameters is not None
    for attempt in range(200):
        p=dict(parameters) if explicit else sample(template,rng)
        guards(template,p)
        if template=='two_bases_rate':prompt,solution,bank,correct,kind,key=hard(p)
        else:
            m=MASKS[template];v=values(p)
            prompt,solution=apply(m['prompt'],v),apply(m['solution'],v)
            bank=[apply(s,v) for s in m['bank']]; correct=m['correct_index'];kind=m['field_type'];key=m['key']
            if profile not in ('observed','raw_source'):
                # Source dy/dx operators and stale unevaluated alias are explicit repairs.
                solution=solution.replace(r'\frac{\text{d}y}{\text{d}x}',r'\frac{\text{d}}{\text{d}x}')
                if template=='cubic_rate_blank':bank=bank[:1]
                solution=solution.replace('ln⁡',r'\ln ')
                bank=[s.replace('ln⁡',r'\ln ') for s in bank]
        if field_type is not None and kind!=field_type:raise ValueError('template field mismatch')
        if kind=='radio':
            parsed=[read_math(s.split('=',1)[-1]) for s in bank]
            if any(equiv(x,y) for i,x in enumerate(parsed) for y in parsed[i+1:]):
                if explicit:raise ValueError('ambiguous complete bank')
                continue
        break
    else:raise ValueError('unable to sample eligible whole bank')
    # Only real displayed content participates in presentation identity.
    signature=digest([VERSION,prompt,solution,kind,key,sorted(bank),bank[correct]])
    qid=uid(signature);fid=uid(signature+'/'+key)
    answers=[{':answer/id':uid(fid+'/'+s),':answer/type':':answer.type/math',':answer/value':s} for s in bank]
    correct_id=answers[correct][':answer/id']
    if kind=='radio':rng.shuffle(answers)
    question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]}
    printed=read_prompt(prompt)
    target=sp.diff(printed,X)
    t=read_input(prompt)
    if t is not None:target=target.subs(X,t)
    mathfinger=digest([sp.srepr(sp.diff(printed,X)),str(t)])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile or 'normal','parameters':p,'mathematical_fingerprint':mathfinger,'content_fingerprint':signature,'origin':'authored' if template=='two_bases_rate' else 'observed parameterized template','source_ids':[] if template=='two_bases_rate' else [MASKS[template]['source_id']],'solution_origin':'authored' if template=='two_bases_rate' or not MASKS[template]['solution_observed'] else 'observed','source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'sympy_version':sp.__version__,'domain':'x real; bases integers >1','plot_rating':'none'}}

# Shared printed-math reader: independent QA reads learner text, never parameters.
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def group(s,start):
    assert s[start]=='{'
    n=1;j=start+1
    while n:
        if s[j]=='{':n+=1
        elif s[j]=='}':n-=1
        j+=1
    return s[start+1:j-1],j

def read_math(s):
    s=s.replace(r'\,','').strip().rstrip('.,').replace('−','-').replace('⁡','')
    s=s.replace(r'\frac{\text{d}y}{\text{d}x}','D').replace(r'\frac{\text{d}}{\text{d}x}','D')
    s=s.replace(r'\operatorname{ln}',r'\ln').replace('ln',r'LOG')
    s=s.replace(r'\LOG','LOG')
    # TeX bare log argument is exactly one integer or x in observed templates.
    s=re.sub(r'LOG\s*(\d+|x)(?![A-Za-z])',r'log(\1)',s).replace('LOG','log')
    while r'\frac' in s:
        i=s.index(r'\frac');a,j=group(s,i+5);b,k=group(s,j);s=s[:i]+'(('+a+')/('+b+'))'+s[k:]
    s=s.replace(r'\cdot','*').replace(r'\,','').replace(r'\left','').replace(r'\right','')
    s=s.replace('{','(').replace('}',')').replace('^','**')
    s=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',s)
    return parse_expr(s,local_dict={'x':X,'E':sp.E,'log':sp.log,'D':lambda f:sp.diff(f,X)},transformations=TRANS)

def read_prompt(prompt):
    m=re.search(r'f\(x\)\s*=([^$]+)\$',prompt)
    if not m:raise ValueError('printed function missing')
    return read_math(m[1].rstrip(', '))
def read_input(prompt):
    m=re.search(r'(?:at|tangent at) \$x=(-?\d+)',prompt)
    return int(m[1]) if m else None

def equiv(a,b):
    d=sp.simplify(a-b)
    return d==0 or d.equals(0) is True

# Easy observed templates: scalar exponential; exponential + e^x; polynomial;
# linear and reversed-constant blank. Positive coefficient magnitudes 1..12,
# integer bases 2..9, constant magnitudes 1..20, fixed source degree/signs.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate observed templates: evaluation at zero after e^x or cubic terms.
# Zero remains fixed, preserving the captured easy exponent-evaluation workload.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard authored extension: two independent base-log terms + quadratic slope,
# evaluated at a nonzero familiar integer. Guards apply to explicit replay too.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        for r in records:
            q=r['question'];print(q[':question/problem']);f=q[':question/answer-fields'][0]
            if f[':answer-field/type'].endswith('radio'):
                for a in f[':answer-field/choices']:print('- $'+a[':answer/value']+'$')
            print('\n'+q[':question/worked-solution']+'\n')
if __name__=='__main__':main()
