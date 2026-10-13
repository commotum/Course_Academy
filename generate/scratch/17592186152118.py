#!/usr/bin/env python3
"""LCM of exactly two factored multivariable polynomials (basis 1356).

Two independent monic linear factors, positive integer contents, no factorization
or third polynomial. All three levels retain the complete source solution route:
list numerical multiples, select each maximum exponent, form the variable LCM,
then multiply by the numerical LCM. Hard is an explicitly authored larger-content
and exponent workload, not an observed rating. See the accompanying extraction.

Profiles observed_q-* preserve raw missing keys, exact source banks, and source
punctuation. completed_q-* supplies the one missing key/level/solution. The public
API parameterizes those profiles; it never returns a literal copied source payload.
q-111597's 3/2-content and doubled-first-power recipes are observed expression
patterns with unresolved intent; they are not normal default banks. method_bank
is a complete authored bank of min powers, gcd content, summed powers, swapped
maximum powers and the correct answer. Whole instances are rejected on collision.

Integer polynomial convention follows the lesson: positive content lcm(a,b),
monic primitive factor powers. Equality up to rational scalar is NOT accepted.
No EDB writes or registration. JSON is local review data, not transaction data.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

KP=17592186152118
VERSION='two-multivariable-lcm-1.0.0'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
RECORD=SOURCE['record']
TITLE=RECORD[':knowledge-point/title']
NAMESPACE=uuid.UUID(RECORD[':knowledge-point/id'])
QUESTIONS={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
OPENING=r'To find the least common multiple ($\text{LCM}$) of two polynomials that are made up of products of binomials, we find the least common multiple of the constants and the least common multiple of each variable part. Then, we multiply all of the results together.'
KEYS=('a','b','v','w','h','k','p','q','r','s')
TEMPLATES={
 'factored_blank':{'levels':('easy','moderate','hard'),'field':'blank'},
 'factored_radio':{'levels':('easy','moderate','hard'),'field':'radio'},
}
PROFILES={
 'q-218516':dict(level='easy',template='factored_blank',a=4,b=5,v='u',w='v',h=0,k=-2,p=3,q=2,r=1,s=5),
 'q-76246':dict(level='moderate',template='factored_radio',a=4,b=10,v='x',w='y',h=3,k=-1,p=2,q=3,r=2,s=1,spaced=True,missing=True,bank='product_sum_swap'),
 'q-111597':dict(level='easy',template='factored_radio',a=4,b=7,v='z',w='w',h=2,k=-5,p=2,q=2,r=3,s=4,period_inside=True,period_final=True,bank='opaque_patterns'),
 'q-222107':dict(level='easy',template='factored_blank',a=3,b=5,v='x',w='y',h=-3,k=1,p=3,q=1,r=1,s=2),
 'q-222113':dict(level='moderate',template='factored_blank',a=9,b=15,v='y',w='z',h=-2,k=1,p=5,q=3,r=2,s=6),
 'q-222116':dict(level='moderate',template='factored_blank',a=12,b=20,v='z',w='w',h=0,k=-7,p=6,q=3,r=5,s=4),
}

def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(NAMESPACE,s))
def parse_tex(s):
    """Parse printed numerical/factored polynomial tokens, independently of metadata."""
    s=s.strip().rstrip('.').replace(r'\cdot','*').replace(r'\,','')
    s=re.sub(r'\^\{(\d+)\}',r'**\1',s).replace('^','**').replace('{','').replace('}','')
    return sp.expand(parse_expr(s,transformations=standard_transformations+(implicit_multiplication_application,)))
def base(v,h,spaced=False):
    if h==0:return v
    gap=' ' if spaced else ''
    return '('+v+gap+('+' if h>0 else '-')+gap+str(abs(h))+')'
def power(v,h,n,spaced=False):
    b=base(v,h,spaced)
    if n==1:return b
    if h==0:b='{'+b+'}'
    return b+'^{'+str(n)+'}'
def product(p,e,f,coefficient=1,spaced=False):
    if not isinstance(coefficient,int) and sp.Rational(coefficient).q!=1:
        raise ValueError('Nonintegral content in bank')
    c=int(coefficient)
    return (str(c) if c!=1 else '')+power(p['v'],p['h'],e,spaced)+power(p['w'],p['k'],f,spaced)
def algebra(p):
    v,w=sp.symbols(p['v']+' '+p['w']);F=v+p['h'];G=w+p['k']
    A=p['a']*F**p['p']*G**p['q'];B=p['b']*F**p['r']*G**p['s']
    L=math.lcm(p['a'],p['b'])*F**max(p['p'],p['r'])*G**max(p['q'],p['s'])
    return A,B,L

def validate_parameters(level,p):
    if set(p)!=set(KEYS):raise ValueError('Expected '+str(KEYS))
    if p['v'] not in 'xyzuvw' or p['w'] not in 'xyzuvw' or len(p['v'])!=1 or len(p['w'])!=1 or p['v']==p['w']:raise ValueError('Two distinct supported variables required')
    if any(type(p[k]) is not int for k in KEYS if k not in ('v','w')):raise ValueError('Integer parameters required')
    a,b=p['a'],p['b'];ex=[p[k] for k in ('p','q','r','s')];lo,hi=min(ex),max(ex);l=math.lcm(a,b)
    if not (abs(p['h'])<=9 and abs(p['k'])<=9 and (p['h'] or p['k'])):raise ValueError('At least one binomial, bounded integer shifts')
    if a==b or min(a,b)<2 or lo<1 or (p['p']==p['r'] and p['q']==p['s']):raise ValueError('Distinct contents and variable power parts required')
    if level=='easy':
        if not(max(a,b)<=9 and math.gcd(a,b)==1 and l<=60 and hi<=5):raise ValueError('Easy coprime small-content bounds')
    elif level=='moderate':
        if not(4<=min(a,b) and 9<=max(a,b)<=20 and math.gcd(a,b)>1 and a%b and b%a and l<=120 and 3<=hi<=6):raise ValueError('Moderate shared nondividing content4–20, one≥9, and 3–6 exponent bounds')
    elif level=='hard':
        if not(12<=min(a,b) and max(a,b)<=30 and math.gcd(a,b)>1 and a%b and b%a and 120<l<=180 and lo>=2 and 7<=hi<=9):raise ValueError('Authored hard shared-content, LCM 121–180 and 7–9 exponent bounds')
    else:raise ValueError('Unknown difficulty')
    return algebra(p)

def solution(p,config):
    a,b=p['a'],p['b'];l=math.lcm(a,b);E=max(p['p'],p['r']);F=max(p['q'],p['s'])
    A=product(p,p['p'],p['q']);B=product(p,p['r'],p['s'])
    def multiples(c):return ','.join(r'\,'+str(i*c) for i in range(1,l//c+2))+',…'
    x=base(p['v'],p['h']);y=base(p['w'],p['k'])
    xp=power(p['v'],p['h'],p['p']);xr=power(p['v'],p['h'],p['r'])
    yq=power(p['w'],p['k'],p['q']);ys=power(p['w'],p['k'],p['s'])
    xm=power(p['v'],p['h'],E);ym=power(p['w'],p['k'],F)
    period='.' if config.get('period_final',False) else ''
    return (OPENING+f'\n\nSo first, we find $\\text{{LCM}}({a},{b}):$'
      +f'\n\n- Multiples of ${a}:$ ${multiples(a)}$\n\n- Multiples of ${b}:$ ${multiples(b)}$'
      +f'\n\nSo, $\\text{{LCM}}({a},{b})={l}.$'
      +f'\n\nTo find the $\\text{{LCM}}$ of ${A}$ and ${B},$ we find the largest powers for ${x}$ and ${y}$ that appear in the expressions:'
      +f'\n\n- For ${xp}$ and ${xr},$ the largest power is ${E}.$'
      +f'\n\n- For ${yq}$ and ${ys},$ the largest power is ${F}.$'
      +f'\n\nNow, we raise ${x}$ and ${y}$ to the corresponding largest powers. Therefore,'
      +f'\n\n$$\n\\text{{LCM}}({A},\\,{B})={xm}\\cdot {ym}.\n$$'
      +'\n\nFinally, we multiply all of our results together:'
      +f'\n\n$$\n\\text{{LCM}}({a}{A},\\,{b}{B})={l}{xm}{ym}{period}\n$$')

def bank(p,profile,spaced):
    a,b=p['a'],p['b'];l=math.lcm(a,b);E=max(p['p'],p['r']);F=max(p['q'],p['s'])
    m=min(p['p'],p['r']);n=min(p['q'],p['s'])
    if profile=='product_sum_swap':
        nodes=[('sum_powers',l,p['p']+p['r'],p['q']+p['s']),('correct',l,E,F),('product_content',a*b,E,F),('product_and_sum',a*b,p['p']+p['r'],p['q']+p['s']),('swap_maxima',l,F,E)]
    elif profile=='opaque_patterns':
        if l%2:raise ValueError('Observed 3/2-content expression pattern requires even LCM')
        # Patterns reproduce full observed bank; no claim of recovered learner mistakes.
        nodes=[('observed_3half_min_max',3*l//2,m,F),('observed_double_first_sum_second',l,2*p['p'],p['q']+p['s']),('correct',l,E,F),('min_first_max_second',l,m,F),('observed_3half_min_maxplus1',3*l//2,m,F+1)]
    elif profile=='method_bank':
        nodes=[('correct',l,E,F),('minima',l,m,n),('gcd_content',math.gcd(a,b),E,F),('sum_powers',l,p['p']+p['r'],p['q']+p['s']),('swap_maxima',l,F,E)]
    else:raise ValueError('Unknown complete bank')
    rendered=[(label,product(p,e,f,c,spaced)) for label,c,e,f in nodes]
    vals=[parse_tex(s) for _,s in rendered]
    if any(sp.expand(x-y)==0 for i,x in enumerate(vals) for y in vals[i+1:]):raise ValueError('Whole bank rejected: equivalent choices')
    return rendered

def build(level,t,p,profile,seed):
    if t not in TEMPLATES or level not in TEMPLATES[t]['levels']:raise ValueError('Unknown/incompatible template')
    config={};sid=None;raw=False;replay=False
    if profile and profile.startswith(('observed_','completed_')):
        sid=profile.split('_',1)[1]
        if sid not in PROFILES:raise ValueError('Unknown source profile')
        config=PROFILES[sid];raw=profile.startswith('observed_');replay=True
        if level!=config['level'] or t!=config['template']:raise ValueError('Profile level/template mismatch')
    elif profile not in (None,'method_bank'):raise ValueError('Unknown profile')
    validate_parameters(level,p)
    kind=TEMPLATES[t]['field'];space=config.get('spaced',False)
    A=product(p,p['p'],p['q'],p['a'],space);B=product(p,p['r'],p['s'],p['b'],space)
    inside=config.get('period_inside',False)
    problem=(f'The least common multiple of the polynomials ${A}$ and ${B}$ is{{{{field-1}}}}.' if kind=='blank' else f'Find the least common multiple of the polynomials ${A}$ and ${B}'+('.$' if inside else '$.'))
    worked=solution(p,config if replay else {'period_final':True})
    selected=config.get('bank','method_bank') if replay else 'method_bank'
    values=bank(p,selected,space) if kind=='radio' else [('correct',product(p,max(p['p'],p['r']),max(p['q'],p['s']),math.lcm(p['a'],p['b'])))]
    omit=raw and config.get('missing',False)
    # Identity depends on actual complete learner content, not aliases, seed or order.
    identity=digest({'version':VERSION,'problem':problem,'solution':None if omit else worked,'difficulty':None if omit else level,'field':kind,'correct':None if omit else next(v for k,v in values if k=='correct'),'bank':sorted(v for _,v in values)})
    qid=uid(identity);fid=uid(qid+'/field/'+kind)
    choices=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for _,value in values]
    correct=next(a[':answer/id'] for a,(label,_) in zip(choices,values) if label=='correct')
    random.Random(seed).shuffle(choices)
    f={':answer-field/id':fid,':answer-field/key':'field-1' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices}
    if not omit:f[':answer-field/correct']=[':answer/id',correct]
    q={':question/id':qid,':question/problem':problem,':question/answer-fields':[f]}
    if not omit:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':worked})
    Aexpr,Bexpr,L=algebra(p);symbols=sp.symbols(p['v']+' '+p['w'])
    # Canonical fingerprint excludes banks/profile, input order and variable aliases.
    canonical=sp.symbols('V W')
    presentations=[]
    for order in (canonical,canonical[::-1]):
        mapping=dict(zip(symbols,order))
        presentations.append(sorted(sp.srepr(sp.expand(e.xreplace(mapping))) for e in (Aexpr,Bexpr)))
    fingerprint=digest(min(presentations))
    return {'knowledge_point':{'db_id':KP,'id':str(NAMESPACE),'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'level':level,'template':t,'profile':profile or 'method_bank','bank':selected if kind=='radio' else None,'parameters':p,'source':{k:v for k,v in SOURCE.items() if k!='record'},'source_ids':[sid] if sid else [],'authored_level':level=='hard' or bool(sid and config.get('missing')),'authored_field_layout':level in ('moderate','hard') and kind=='radio','authored_bank':kind=='radio' and not replay,'bank_interpretation_limit':selected=='opaque_patterns' and kind=='radio','authored_completion':bool(sid and config.get('missing') and not raw),'raw_missing_attributes':bool(omit),'recipes':[k for k,_ in values],'content_identity':identity,'mathematical_fingerprint':fingerprint,'domain':'Two independent monic linear factors in Z[v,w], positive integer contents; normalized positive LCM.','plot_rating':'none','sympy':sp.__version__}}

def sample(level,rng,profile):
    cfg=PROFILES.get(profile.split('_',1)[1]) if profile and profile.startswith(('observed_','completed_')) else None
    # Complete profile selected before parameters. Source-profile random calls vary
    # coefficients/shifts/powers within the same advertised workload.
    v,w=rng.sample(list('xyzuvw'),2);h=rng.randint(-9,9);k=rng.choice([i for i in range(-9,10) if i])
    if level=='easy':
        a,b=rng.sample(range(2,10),2); ex=[rng.randint(1,5) for _ in range(4)]
    elif level=='moderate':
        a,b=rng.sample(range(4,21),2);ex=[rng.randint(1,6) for _ in range(4)]
    elif level=='hard':
        a,b=rng.sample(range(12,31),2);ex=[rng.randint(2,9) for _ in range(4)]
    else:raise ValueError('Unknown difficulty')
    return dict(zip(KEYS,[a,b,v,w,h,k,*ex]))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    cfg=None
    if profile and profile.startswith(('observed_','completed_')):
        cfg=PROFILES.get(profile.split('_',1)[1])
        if cfg is None:raise ValueError('Unknown source profile')
        if level!=cfg['level']:raise ValueError('Profile level mismatch')
    if field_type and field_type not in ('blank','radio'):raise ValueError('Unsupported field')
    template=template or (cfg['template'] if cfg else 'factored_'+(field_type or random.Random(seed).choice(['blank','radio'])))
    if template not in TEMPLATES or (field_type and TEMPLATES[template]['field']!=field_type):raise ValueError('Template/field mismatch')
    if cfg and template!=cfg['template']:raise ValueError('Profile template mismatch')
    if profile not in (None,'method_bank') and not cfg:raise ValueError('Unknown profile')
    if parameters is not None:return build(level,template,dict(parameters),profile,seed)
    rng=random.Random(seed)
    for _ in range(20000):
        p=sample(level,rng,profile)
        try:return build(level,template,p,profile,seed)
        except ValueError:continue
    raise ValueError('No eligible whole instance sampled')

# EASY: observed powers 1–5, contents 3/4/5/7; normal coprime small contents.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: shared nondividing content4–20, one≥9, maximum exponent3–6;
# rated sources have maxima5–6; the unrated4/10 source supports the authored3 floor.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored same two-factor method, nondividing shared content, LCM 121–180,
# and maximum exponent 7–9. No additional factorization or third polynomial.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    lines=[q[':question/problem']]
    if f[':answer-field/type'].endswith('/radio'):
        lines += [f"- ${a[':answer/value']}$" for a in f[':answer-field/choices']]
    else:lines += ['Answer: $'+f[':answer-field/choices'][0][':answer/value']+'$']
    if ':question/worked-solution' in q:lines += [q[':question/worked-solution']]
    return '\n\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    parser.add_argument('--template',choices=list(TEMPLATES));parser.add_argument('--profile')
    args=parser.parse_args()
    if args.count<1:parser.error('--count must be positive')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
