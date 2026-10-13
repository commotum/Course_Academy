#!/usr/bin/env python3
"""LCM of two single-variable polynomials: frozen local generator, steps 3–7.

Math database basis 1356; source and evidence alongside this script. No EDB writes.
Two scalar contents multiply unequal powers of ONE common monic binomial. Compute
positive integer lcm(a,b), retain max(n,m). This is the lesson's Z[v] convention:
NOT monic normalization over Q[v], and NOT equality modulo arbitrary scalars.

Observed profiles preserve exact source prompt, bank and solution arithmetic
sequence. Missing originals retain omissions under observed_<id>; derived_<id>
adds independently computed answers, solutions and explicitly authored labels.
No replay returns a captured payload: all values pass through polynomial recipes.
Default E/M/H vary the same operation and use complete defensible five-choice
banks. Moderate is authored (no observed label): shared integer content, at least
one 9..18 content, max exponent 4..5; unequal powers remain visible. Hard follows
observed 8/20,10/15 contents and max powers 6..9, without new factors/variables.

API generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None)
and individual difficulty entrypoints. Source profiles parameterize list positions
and punctuation; an invalid whole bank or list rejects the entire instance.
Identity follows actual prompt, solution and complete bank, independent of seed
or shuffle. Mathematical identity excludes variable aliases and answer banks.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186152117
VERSION='single-variable-lcm-1.0.0'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
RECORD=SOURCE['record']; TITLE=RECORD[':knowledge-point/title']
NS=uuid.UUID(RECORD[':knowledge-point/id'])
OPENING=r'To find the least common multiple ($\text{LCM}$) of two polynomials that are made up of products of binomials, we find the least common multiple of the constants and the least common multiple of the variable part. Then, we multiply all of the results together.'
TEMPLATES={'power_blank':{'field':'blank','levels':['easy','moderate','hard']},'power_radio':{'field':'radio','levels':['easy','moderate','hard']}}
# Captured multiple-list positions are arithmetic recipes (c*k), not literal lists.
PROFILES={
 'q-222016':dict(level='moderate',template='power_blank',a=9,b=3,n=4,m=2,v='y',h=7,spaced=True,blankspace=True,missing=True),
 'q-76460':dict(level='easy',template='power_radio',a=2,b=3,n=2,m=1,v='y',h=-4,spaced=True,ans_space=True,period_inside=False,missing=True,bank='retain_inputs'),
 'q-218483':dict(level='easy',template='power_blank',a=7,b=2,n=2,m=5,v='z',h=3,indices_a=[1,2,4],indices_b=[1,2,3,4,5,6,7,12],comma=False,period_part=True,period_final=True),
 'q-222013':dict(level='easy',template='power_blank',a=5,b=8,n=3,m=4,v='x',h=-1,indices_a=list(range(1,9)),indices_b=list(range(1,8)),comma=False,period_part=True,period_final=False),
 'q-222021':dict(level='hard',template='power_blank',a=15,b=10,n=3,m=6,v='w',h=3,indices_a=[1,2,3,4],indices_b=[1,2,3,4],comma=True,period_part=False,period_final=False),
 'q-222022':dict(level='hard',template='power_blank',a=8,b=20,n=9,m=7,v='y',h=-2,indices_a=[1,2,3,4,5],indices_b=[1,2,3,4],comma=True,period_part=True,period_final=False),
 'q-76457':dict(level='hard',template='power_radio',a=10,b=15,n=6,m=4,v='y',h=1,indices_a=[1,2,3,4],indices_b=[1,2,3],comma=True,period_part=True,period_final=True,period_inside=True,bank='product_power'),
}
BANK_PROFILES={'method_bank':{'origin':'authored','recipes':['correct','minimum_power','sum_powers','GCF_content','omit_binomial']},'retain_inputs':{'origin':'observed','source_id':'q-76460','recipes':['correct','sum_powers','first_content_max_power','second_content_max_power','second_input']},'product_power':{'origin':'observed','source_id':'q-76457','recipes':['correct','sum_powers','product_contents_sum_powers','twice_max_power','product_contents_max_power']}}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NS,x))
def parse_tex(s):
    """Read actual displayed polynomial; source notation needs only elementary tokens."""
    s=s.replace(r'\cdot','*').replace(r'\,','').replace('−','-')
    s=re.sub(r'\^\{(\d+)\}',r'**\1',s).replace('^','**')
    return sp.expand(parse_expr(s,transformations=standard_transformations+(implicit_multiplication_application,)))
def base(p,spaced=False):
    gap=' ' if spaced else ''
    return '('+p['v']+gap+('+' if p['h']>0 else '-')+gap+str(abs(p['h']))+')'
def power(p,n,spaced=False):return base(p,spaced)+(f'^{{{n}}}' if n!=1 else '')
def polynomial(p,c,n,spaced=False):return ('' if c==1 else str(c))+power(p,n,spaced)
def algebra(p):
    F=sp.Symbol(p['v'])+p['h'];a,b,n,m=(p[k] for k in ('a','b','n','m'))
    return a*F**n,b*F**m,math.lcm(a,b)*F**max(n,m)
def validate_parameters(level,p,replay=False):
    if set(p)!={'a','b','n','m','v','h'}:raise ValueError('Expected exactly a,b,n,m,v,h')
    if p['v'] not in ('x','y','z','w','t'):raise ValueError('Unsupported variable')
    if any(type(p[k]) is not int for k in ('a','b','n','m','h')):raise ValueError('Integer parameters required')
    a,b,n,m,h=(p[k] for k in ('a','b','n','m','h'))
    if not (2<=a<=24 and 2<=b<=24 and a!=b and 1<=abs(h)<=9 and 1<=n<=9 and 1<=m<=9 and n!=m):raise ValueError('Single-binomial scope')
    if replay:
        # Still enforce the original level workload, not a broad replay bypass.
        if level=='easy' and not (a<=9 and b<=9 and math.gcd(a,b)==1 and 2<=max(n,m)<=5):raise ValueError('Observed easy bounds')
        if level=='moderate' and not (a<=18 and b<=18 and math.gcd(a,b)>1 and max(a,b)>=9 and 4<=max(n,m)<=5 and min(n,m)>=2):raise ValueError('Authored moderate bounds')
        if level=='hard' and not (a>=8 and b>=8 and math.gcd(a,b)>1 and a%b and b%a and 6<=max(n,m)<=9 and min(n,m)>=3):raise ValueError('Observed hard bounds')
    else:
        validate_parameters(level,p,True)
    if math.lcm(a,b)>120:raise ValueError('Integer LCM arithmetic exceeds source-like workload')
    return algebra(p)
def multiples(c,indices):return ','.join(r'\,'+str(c*k) for k in indices)+',…'
def solution(p,cfg):
    a,b,n,m=(p[k] for k in ('a','b','n','m'));l=math.lcm(a,b);N=max(n,m)
    f,g,k=power(p,n),power(p,m),power(p,N)
    ia=cfg.get('indices_a',list(range(1,l//a+2)));ib=cfg.get('indices_b',list(range(1,l//b+2)))
    comma=',' if cfg.get('comma',True) else ''
    endpart='.' if cfg.get('period_part',True) else '';endfinal='.' if cfg.get('period_final',True) else ''
    return OPENING+f'\n\nSo first, we find $\\text{{LCM}}({a},{b}):$\n\n- Multiples of ${a}:$ ${multiples(a,ia)}$\n\n- Multiples of ${b}:$ ${multiples(b,ib)}$\n\nSo, $\\text{{LCM}}({a},{b})={l}.$\n\nTo find the $\\text{{LCM}}$ of ${f}$ and ${g}{comma}$ we raise ${base(p)}$ to the largest power that appears in the expressions, which is ${N}.$ Therefore,\n\n$$\n\\text{{LCM}}({f},\\,{g})={k}{endpart}\n$$\n\nFinally, we multiply all of our results together:\n\n$$\n\\text{{LCM}}({a}{f},\\,{b}{g})={l}\\cdot {k}={l}{k}{endfinal}\n$$'
def build(level,template,p,profile):
    cfg={};sid=None;raw=False
    if profile and profile.startswith(('observed_','derived_')):
        sid=profile.split('_',1)[1]
        if sid not in PROFILES:raise ValueError('Unknown source profile')
        cfg=PROFILES[sid]
        if level!=cfg['level'] or template!=cfg['template']:raise ValueError('Source level/template mismatch')
        raw=profile.startswith('observed_') and cfg.get('missing',False)
    elif profile not in (None,'method_bank','retain_inputs','product_power'):raise ValueError('Unknown profile')
    if profile=='retain_inputs' and level!='easy' or profile=='product_power' and level!='hard':raise ValueError('Wrong bank workload')
    P,Q,L=validate_parameters(level,p,bool(sid))
    a,b,n,m=(p[k] for k in ('a','b','n','m'));l=math.lcm(a,b);N=max(n,m)
    if sid and 'indices_a' in cfg and (l//a not in cfg['indices_a'] or l//b not in cfg['indices_b']):raise ValueError('Whole profile lacks displayed common multiple')
    kind=TEMPLATES[template]['field'];bank=cfg.get('bank',profile if profile in BANK_PROFILES else 'method_bank')
    ans_space=cfg.get('ans_space',False);answer=polynomial(p,l,N,ans_space)
    if kind=='blank':recipes=[('correct',answer)]
    elif bank=='retain_inputs':recipes=[('correct',answer),('sum_powers',polynomial(p,l,n+m,ans_space)),('first_content_max_power',polynomial(p,a,N,ans_space)),('second_content_max_power',polynomial(p,b,N,ans_space)),('second_input',polynomial(p,b,m,ans_space))]
    elif bank=='product_power':recipes=[('correct',answer),('sum_powers',polynomial(p,l,n+m)),('product_contents_sum_powers',polynomial(p,a*b,n+m)),('twice_max_power',polynomial(p,l,2*N)),('product_contents_max_power',polynomial(p,a*b,N))]
    else:recipes=[('correct',answer),('minimum_power',polynomial(p,l,min(n,m))),('sum_powers',polynomial(p,l,n+m)),('GCF_content',polynomial(p,math.gcd(a,b),N)),('omit_binomial',str(l))]
    vals=[parse_tex(value) for _,value in recipes]
    if any(sp.expand(x-y)==0 for i,x in enumerate(vals) for y in vals[i+1:]):raise ValueError('Reject complete bank: equivalent options')
    if sp.expand(vals[0]-L)!=0:raise ValueError('Incorrect derived answer')
    spaced=cfg.get('spaced',False);pt=polynomial(p,a,n,spaced);qt=polynomial(p,b,m,spaced)
    if kind=='blank':prompt=f'The least common multiple of ${pt}$ and ${qt}$ is'+(' ' if cfg.get('blankspace',not sid) else '')+'{{field-1}}.';key='field-1'
    else:prompt=f'Find the least common multiple of ${pt}$ and ${qt}'+('.$' if cfg.get('period_inside',True) else '$.');key='selection'
    sol=None if raw else solution(p,cfg)
    bankvals=[] if raw and kind=='blank' else sorted(v for _,v in recipes)
    ident=digest({'version':VERSION,'prompt':prompt,'solution':sol,'bank':bankvals,'field_type':kind})
    qid=uid(ident);fid=uid(ident+'/'+key)
    answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for _,v in recipes]
    field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[0][':answer/id']]}
    if raw:
        del field[':answer-field/correct']
        if kind=='blank':del field[':answer-field/choices']
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':sol})
    v=sp.Symbol(p['v']);x=sp.Symbol('X');task=digest(sorted(sp.srepr(sp.expand(o).subs(v,x)) for o in (P,Q)))
    return {'knowledge_point':{'db_id':KP_ID,'id':str(NS),'title':TITLE},'question':q,'generation':{'version':VERSION,'level':level,'template':template,'seed':None,'parameters':p,'profile':profile or 'method_bank','bank_profile':bank if kind=='radio' else None,'source_id':sid,'source':{k:v for k,v in SOURCE.items() if k!='record'},'source_omissions':bool(raw),'authored_level':level=='moderate' or bool(cfg.get('missing')),'authored_completion':bool(sid and cfg.get('missing') and not raw),'mathematical_fingerprint':task,'content_identity':ident,'recipes':dict(recipes),'convention':'positive integer content LCM times maximum power of common monic binomial','plot_rating':'none'}}

# EASY: observed positive coprime contents 2..9, max exponent 2..5.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: authored same method; shared content, 9..18 larger content, powers2..5.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: observed nondividing shared contents8..24, max power6..9, min3..8.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    if field_type not in (None,'radio','blank'):raise ValueError('Unknown field type')
    rng=random.Random(seed)
    if profile and profile.startswith(('observed_','derived_')):
        cfg=PROFILES.get(profile.split('_',1)[1])
        if not cfg:raise ValueError('Unknown profile')
        template=template or cfg['template']
        if parameters is None:parameters={k:cfg[k] for k in ('a','b','n','m','v','h')}
    if profile in ('retain_inputs','product_power'):
        if template not in (None,'power_radio') or field_type not in (None,'radio'):
            raise ValueError('A complete radio bank requires the radio layout')
        template='power_radio'
    allowed=[t for t,c in TEMPLATES.items() if level in c['levels'] and (field_type is None or c['field']==field_type)]
    template=template or rng.choice(allowed)
    if template not in allowed:raise ValueError('Template/field mismatch')
    if parameters is None:
        for _ in range(10000):
            bound=(2,9) if level=='easy' else (2,18) if level=='moderate' else (8,24)
            exps=(1,5) if level=='easy' else (2,5) if level=='moderate' else (3,9)
            p={'a':rng.randint(*bound),'b':rng.randint(*bound),'n':rng.randint(*exps),'m':rng.randint(*exps),'v':rng.choice(['x','y','z','w']),'h':rng.choice([i for i in range(-9,10) if i])}
            try:record=build(level,template,p,profile)
            except ValueError:continue
            break
        else:raise ValueError('No eligible whole instance')
    else:record=build(level,template,dict(parameters),profile)
    record['generation']['seed']=seed
    f=record['question'][':question/answer-fields'][0]
    if f[':answer-field/type'].endswith('/radio'):rng.shuffle(f[':answer-field/choices'])
    return record

def markdown(r):
    q,g=r['question'],r['generation'];f=q[':question/answer-fields'][0]
    lines=[f"### {g['level'].title()} — {g['template']} ({g['profile']})",'',q[':question/problem'],'']
    for a in f.get(':answer-field/choices',[]):lines.append('- $'+a[':answer/value']+'$'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
    lines+=['','**Worked solution**','',q.get(':question/worked-solution','[Absent in raw source; see labeled authored completion.]')]
    return '\n'.join(lines)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template',choices=TEMPLATES);parser.add_argument('--profile');parser.add_argument('--field-type',choices=['blank','radio'])
    a=parser.parse_args()
    if a.count<1:parser.error('Positive count required')
    levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
    try:records=[generate(level,a.seed+i,a.template,a.field_type,profile=a.profile) for level in levels for i in range(a.count)]
    except ValueError as exc:parser.error(str(exc))
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
