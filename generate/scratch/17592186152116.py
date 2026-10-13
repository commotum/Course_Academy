#!/usr/bin/env python3
"""LCM of two scalar-multiple polynomials; math basis 1356, no database writes.

Observed templates preserve source prose, banks and omissions through explicit
observed_<MA-id> profiles. derived_<MA-id> completes missing fields, with inferred
keys/levels/solutions explicitly recorded. Normal defaults use defensible complete
method banks. Hard is an authored content-extraction extension within the SAME
constant-factor method: two expanded signed multiples of one primitive nonmonic
quadratic; no independently differing factors, variables, or third input.

Convention: in Z[v], LCM has positive leading coefficient and integer content
lcm(|content(P)|, |content(Q)|); retain the common positive-leading primitive
polynomial. Equality is polynomial equality, NOT equality up to rational units.
This is precisely the canonical lesson's 4F,6F -> 12F rule. Native blank graders
are separately tested for expanded/factored equality and wrong scalar multiples.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP=17592186152116
VERSION='constant-factor-lcm-1.0.1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
RECORD=SOURCE['record']
TITLE=RECORD[':knowledge-point/title']
NAMESPACE=uuid.UUID(RECORD[':knowledge-point/id'])
QUESTIONS={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
OPENING=r'To find the least common multiple ($\text{LCM}$) of two polynomials that are made up of products of binomials, we find the least common multiple of the constants and the least common multiple of the variable part. Then, we multiply all of the results together.'
TEMPLATES={
 'factored_radio': {'levels':['easy','moderate'],'field':'radio','observed':True},
 'factored_blank': {'levels':['easy','moderate'],'field':'blank','observed':True},
 'expanded_content_radio': {'levels':['hard'],'field':'radio','observed':False},
 'expanded_content_blank': {'levels':['hard'],'field':'blank','observed':False},
}
# Lists preserve the source's exact arithmetic sequence, including ellipses.
PROFILES={
 'q-218482':dict(level='moderate',template='factored_blank',a=6,b=15,v='w',h=-8,n=1,spaced=True,blankspace=True,period_inside=False,missing=True),
 'q-76238':dict(level='easy',template='factored_radio',a=3,b=5,v='x',h=-1,n=1,spaced=True,period_inside=False,missing=True,bank='opaque_twice',ans_space=True),
 'q-111582':dict(level='easy',template='factored_radio',a=2,b=7,v='z',h=-4,n=2,period_inside=True,indices_a=[1,2,'…',6,7,8,'…'],indices_b=[1,2,3,'…'],period_final=True,bank='double_product',ans_space=False),
 'q-221994':dict(level='easy',template='factored_blank',a=4,b=9,v='y',h=-3,n=1,period_inside=False,indices_a=list(range(1,10))+['…'],indices_b=list(range(1,7))+['…'],period_final=True),
 'q-221998':dict(level='moderate',template='factored_blank',a=3,b=9,v='y',h=7,n=2,period_inside=False,indices_a=[1,2,3,4,'…'],indices_b=[1,2,3,'…'],period_final=False),
 'q-221999':dict(level='moderate',template='factored_blank',a=4,b=10,v='z',h=-1,n=2,period_inside=False,indices_a=[1,2,3,4,5,6,'…'],indices_b=[1,2,3,4,5,'…'],period_final=False),
 'q-76409':dict(level='moderate',template='factored_radio',a=10,b=15,v='y',h=1,n=1,period_inside=True,indices_a=[1,2,3,4,'…'],indices_b=[1,2,3,'…'],period_final=True,bank='product',ans_space=False),
}

def uid(s): return str(uuid.uuid5(NAMESPACE,s))
def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(expr): return sp.latex(sp.expand(expr)).replace(' ', '')
def linear(p,spaced=False):
    a=p.get('leading',1); h=p['h']; v=p['v']; core=(str(a) if a!=1 else '')+v
    gap=' ' if spaced else ''
    return '('+core+gap+('+' if h>0 else '-')+gap+str(abs(h))+')'
def part(p,spaced=False,n=None):
    if 'constant' in p:
        core='('+tex(p['leading']*sp.Symbol(p['v'])**2+p['h']*sp.Symbol(p['v'])+p['constant'])+')'
        return core+(f'^{{{n//2}}}' if n is not None and n!=2 else '')
    n=p['n'] if n is None else n
    return linear(p,spaced)+(f'^{{{n}}}' if n!=1 else '')
def times(c,F): return ('' if c==1 else '-' if c==-1 else str(c))+F

def parse_tex(s):
    """Independent parser for the actual displayed polynomial/numeric tokens."""
    s=s.replace(r'\cdot','*').replace(r'\,','').replace('−','-')
    s=re.sub(r'\^\{(-?\d+)\}',r'**\1',s).replace('^','**')
    return sp.expand(parse_expr(s, transformations=standard_transformations+(implicit_multiplication_application,)))

def algebra(p):
    v=sp.Symbol(p['v']); F=(p['leading']*v**2+p['h']*v+p['constant']) if 'constant' in p else (v+p['h'])**p['n']
    return F,p['a']*F,p['b']*F,math.lcm(abs(p['a']),abs(p['b']))*F

def validate_parameters(level,t,p,replay=False):
    required={'a','b','v','h','n'}|({'leading','constant'} if level=='hard' else set())
    if set(p)!=required: raise ValueError(f'Expected parameter keys {sorted(required)}')
    if p['v'] not in ('x','y','z','w','t'): raise ValueError('Unsupported variable')
    if any(type(p[k]) is not int for k in required-{'v'}): raise ValueError('Integer parameters required')
    a,b=p['a'],p['b']; h=p['h']; n=p['n']
    if not (1<=abs(h)<=9) or a==b or not a or not b: raise ValueError('Invalid binomial/content')
    # Identical difficulty guards apply to default and explicit source profiles.
    if level=='easy':
        if not(2<=a<=9 and 2<=b<=9 and n in (1,2) and math.gcd(a,b)==1 and math.lcm(a,b)<=72): raise ValueError('Easy requires small coprime contents')
    elif level=='moderate':
        if not(2<=a<=18 and 2<=b<=18 and n in (1,2) and math.gcd(a,b)>1 and math.lcm(a,b)<=120): raise ValueError('Moderate nontrivial content bounds')
        if n==1 and (a%b==0 or b%a==0): raise ValueError('Linear moderate requires nondividing shared content')
    elif level=='hard':
        leading=p['leading']
        if not(2<=leading<=4 and 1<=abs(p['constant'])<=9 and math.gcd(leading,math.gcd(abs(h),abs(p['constant'])))==1 and n==2): raise ValueError('Hard requires a primitive nonmonic three-term quadratic')
        if not(2<=abs(a)<=18 and 2<=abs(b)<=18 and min(a,b)<0 and math.gcd(abs(a),abs(b))>1 and a%b and b%a and math.lcm(abs(a),abs(b))<=120): raise ValueError('Hard signed nondividing content bounds')
    else: raise ValueError('Unknown difficulty')
    F,P,Q,L=algebra(p)
    if sp.Poly(F,sp.Symbol(p['v'])).content()!=1: raise ValueError('Nonprimitive common part')
    return F,P,Q,L

def source_solution(p,config):
    a,b=p['a'],p['b']; l=math.lcm(abs(a),abs(b)); F=part(p)
    def multiples(c,indices):
        vals=[]
        for pos,i in enumerate(indices):
            if i=='…': vals.append('…')
            else: vals.append(('' if config.get('irregular_list') and indices is ia and pos==5 else r'\,')+str(c*i))
        return ','.join(vals)
    ia=config.get('indices_a',list(range(1,l//a+2))+['…'])
    ib=config.get('indices_b',list(range(1,l//b+2))+['…'])
    # One captured source has missing thin spaces on 16 and after its ellipsis.
    ma=multiples(a,ia); mb=multiples(b,ib)
    finalperiod='.' if config.get('period_final',True) else ''
    return OPENING+f'\n\nSo first, we find $\\text{{LCM}}({a},{b}):$\n\n- Multiples of ${a}:$ ${ma}$\n\n- Multiples of ${b}:$ ${mb}$\n\nSo, $\\text{{LCM}}({a},{b})={l}.$\n\nSince the variable part is the same in the expressions, we have\n\n$$\n\\text{{LCM}}({F},\\,{F})={F}.\n$$\n\nFinally, we multiply all of our results together:\n\n$$\n\\text{{LCM}}({a}{F},\\,{b}{F})={l}\\cdot {F}={l}{F}{finalperiod}\n$$'

def build(level,t,p,profile):
    raw=bool(profile and profile.startswith('observed_'))
    source_id=None; config={}; replay=False
    if profile and profile.startswith(('observed_','derived_')):
        source_id=profile.split('_',1)[1]
        if source_id not in PROFILES: raise ValueError('Unknown source profile')
        config=PROFILES[source_id]; replay=True
        if config['level']!=level or config['template']!=t: raise ValueError('Profile level/template mismatch')
    elif profile not in (None,'method_bank','content_bank'):
        raise ValueError('Unknown profile')
    elif profile=='method_bank' and level=='hard' or profile=='content_bank' and level!='hard':
        raise ValueError('Bank profile has incompatible level')
    F,P,Q,L=validate_parameters(level,t,p,replay)
    if replay and p['n']!=config['n']:
        raise ValueError('Source profile must preserve advertised exponent shape')
    if replay and level=='moderate':
        if math.gcd(p['a'],p['b'])<=1 or (p['n']==1 and (p['a']%p['b']==0 or p['b']%p['a']==0)):
            raise ValueError('Source replay must retain moderate content workload')
    a,b=p['a'],p['b']; l=math.lcm(abs(a),abs(b)); n=p['n']; kind=TEMPLATES[t]['field']
    if replay and 'indices_a' in config:
        if l//a not in config['indices_a'] or l//b not in config['indices_b']:
            raise ValueError('Whole source profile lacks displayed common multiple')
    ansF=part(p,config.get('ans_space',False))
    answer=times(l,ansF)
    expanded=level=='hard'
    Ptext=tex(P) if expanded else times(a,part(p,config.get('spaced',False)))
    Qtext=tex(Q) if expanded else times(b,part(p,config.get('spaced',False)))
    if kind=='radio':
        prompt=f'Find the least common multiple of ${Ptext}$ and ${Qtext}'+('.$' if config.get('period_inside',True) else '$.')
        key='selection'
    else:
        prompt=f'The least common multiple of ${Ptext}$ and ${Qtext}$ is'+(' ' if config.get('blankspace',not replay) else '')+'{{field-1}}.'
        key='field-1'
    if not replay: prompt+=' Use the positive integer LCM of the contents and a primitive polynomial part with positive leading coefficient.'
    if expanded:
        primitive=tex(F); signedA=f'({a})' if a<0 else str(a); signedB=f'({b})' if b<0 else str(b)
        hard_opening=OPENING.replace('that are made up of products of binomials','that differ by a constant factor')
        solution=hard_opening+f'\n\nFirst, factor out the integer contents and identify the common primitive polynomial:\n\n$$\n{Ptext}={signedA}({primitive}),\\qquad {Qtext}={signedB}({primitive}).\n$$\n\nUse the positive contents ${abs(a)}$ and ${abs(b)}$.\n\n'+'So first,'+source_solution({**p,'a':abs(a),'b':abs(b)},{}).split('So first,',1)[1]
        # Formal LCM refers to the printed signed polynomials, then content decomposition.
        positive_pair=f'\\text{{LCM}}({abs(a)}{part(p)},\\,{abs(b)}{part(p)})='
        solution=solution.replace(positive_pair,f'\\text{{LCM}}({Ptext},\\,{Qtext})=')
    else: solution=source_solution(p,{**config,'irregular_list':source_id=='q-111582'})
    if raw and config.get('missing'): solution=None
    recipes=[]
    if kind=='blank': recipes=[('correct',answer)]
    elif replay:
        # Complete observed banks, parameterized; opaque doubled-content profile
        # is replay-only and does not claim a recovered error interpretation.
        bank=config['bank']; base=part(p,config.get('ans_space',False)); doubled=part(p,config.get('ans_space',False),2*n)
        if bank=='opaque_twice': recipes=[('opaque_2l_squared',times(2*l,doubled)),('opaque_2l',times(2*l,base)),('sum_contents',times(a+b,base)),('correct',answer),('duplicate_common_part',times(l,doubled))]
        elif bank=='double_product': recipes=[('sum_contents',times(a+b,base)),('correct',answer),('twice_product_squared',times(2*a*b,doubled)),('twice_product',times(2*a*b,base)),('duplicate_common_part',times(l,doubled))]
        else: recipes=[('duplicate_common_part',times(l,doubled)),('multiply_inputs',times(a*b,doubled)),('product_contents',times(a*b,base)),('correct',answer),('sum_contents',times(a+b,base))]
    elif expanded:
        recipes=[('correct',answer),('use_GCF',times(math.gcd(abs(a),abs(b)),ansF)),('product_contents',times(abs(a*b),ansF)),('lose_content',ansF),('duplicate_common_part',times(l,part(p,n=2*n)))]
    else:
        # Default complete bank uses operations from the assessed method.
        recipes=[('correct',answer),('sum_contents',times(a+b,ansF)),('duplicate_common_part',times(l,part(p,n=2*n))),('omit_common_part',str(l)),('use_GCF',times(math.gcd(a,b),ansF))]
    values=[parse_tex(v) for _,v in recipes]
    if any(sp.expand(x-y)==0 for i,x in enumerate(values) for y in values[i+1:]): raise ValueError('Whole bank collision')
    if any(sp.expand(v-L)==0 for (name,_),v in zip(recipes,values) if name!='correct'): raise ValueError('Wrong choice equals correct')
    if not raw or not config.get('missing'): assert sp.expand(parse_tex(answer)-L)==0
    core={'prompt':prompt,'solution':solution,'bank':sorted(v for _,v in recipes),'field_type':kind,'raw':raw and bool(config.get('missing'))}
    # Identity uses actual presentation; parameter spellings/profile aliases are excluded.
    if raw and source_id=='q-218482': core['bank']=[]
    identity=digest({'version':VERSION,**core}); qid=uid(identity); fid=uid(identity+'/field/'+key)
    answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for _,v in recipes]
    field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid+'/'+answer)]}
    if raw and config.get('missing'):
        del field[':answer-field/correct']
        if source_id=='q-218482': del field[':answer-field/choices']
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not (raw and config.get('missing')):
        question[':question/difficulty']=':question.difficulty/'+level
        question[':question/worked-solution']=solution
    fingerprint=digest(sorted([sp.srepr(sp.Poly(P,sp.Symbol(p['v'])).as_expr().subs(sp.Symbol(p['v']),sp.Symbol('X'))),sp.srepr(sp.Poly(Q,sp.Symbol(p['v'])).as_expr().subs(sp.Symbol(p['v']),sp.Symbol('X')))]))
    return {'knowledge_point':{'db_id':KP,'id':str(NAMESPACE),'title':TITLE},'question':question,'generation':{'version':VERSION,'template':t,'level':level,'parameters':p,'profile':profile or ('content_bank' if expanded else 'method_bank'),'source_id':source_id,'source':{k:v for k,v in SOURCE.items() if k!='record'},'authored_level':expanded or bool(config.get('missing')),'raw_source_omissions':raw and bool(config.get('missing')),'mathematical_fingerprint':fingerprint,'content_identity':identity,'recipes':dict(recipes),'convention':'positive integer content LCM times common positive-leading primitive part','plot_rating':'none'}}

# EASY: visible identical monic binomial, exponent 1 or 2; small COPRIME contents.
# MODERATE: visible identical monic part; nontrivial shared content/divisibility.
# HARD: authored; signed expanded SAME primitive nonmonic quadratic, recover content.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    rng=random.Random(seed)
    if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio','blank'): raise ValueError('Unsupported field type')
    if profile and profile.startswith(('observed_','derived_')):
        config=PROFILES.get(profile.split('_',1)[1])
        if not config: raise ValueError('Unknown profile')
        template=template or config['template']
        if level!=config['level']: raise ValueError('Incorrect source replay level')
    allowed=[t for t,c in TEMPLATES.items() if level in c['levels'] and (field_type is None or c['field']==field_type)]
    template=template or rng.choice(allowed)
    if template not in allowed: raise ValueError('Template/type/level mismatch')
    for _ in range(2000):
        p=dict(parameters) if parameters is not None else {'a':rng.randint(2,9 if level=='easy' else 18),'b':rng.randint(2,9 if level=='easy' else 18),'v':rng.choice(['x','y','z','w','t']),'h':rng.choice([i for i in range(-9,10) if i]),'n':rng.choice([1,2])}
        if level=='hard' and parameters is None:
            p.update(leading=rng.randint(2,4),constant=rng.choice([i for i in range(-9,10) if i]),n=2); p['a']*=rng.choice([-1,1]); p['b']*=-1
        try: result=build(level,template,p,profile)
        except ValueError:
            if parameters is not None: raise
            continue
        choices=result['question'][':question/answer-fields'][0].get(':answer-field/choices',[])
        if TEMPLATES[template]['field']=='radio': rng.shuffle(choices)
        result['generation']['seed']=seed
        return result
    raise ValueError('No eligible whole bank instance')
def generate_easy(seed=0,**kw): return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw): return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw): return generate('hard',seed,**kw)
def markdown(r):
    q=r['question']; out=q[':question/problem']
    for f in q[':question/answer-fields']:
        if f[':answer-field/type'].endswith('/radio'):
            out+='\n\n'+'\n'.join(f'- ${a[":answer/value"]}$' for a in f.get(':answer-field/choices',[]))
    return out+'\n\n'+q.get(':question/worked-solution','[Source has no captured worked solution.]')
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all'); ap.add_argument('--seed',type=int,default=0); ap.add_argument('--count',type=int,default=1); ap.add_argument('--format',choices=['markdown','json'],default='markdown'); ap.add_argument('--template'); ap.add_argument('--profile')
    args=ap.parse_args(); levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    results=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(results,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in results))
