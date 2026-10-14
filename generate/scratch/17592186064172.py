#!/usr/bin/env python3
"""General-base exponential integral; basis2275 local draft, steps3–7.

Easy: integer a>1. Moderate: constant c times integer a>1. Hard: reciprocal
integer a=1/b and ln(1/b)=-ln b. No exponent multiplier, substitution, sums,
definite limits or parts. All observed fields are five-option radio.
Raw whole-bank profiles retain exact notation, wording and attribute omissions;
they are parameterized evidence, not default recovered error algorithms.
Normal profiles retain the source solution stages with standard TeX ln.
Select complete bank/family BEFORE parameters. Reject the whole instance on any
pair of derivative-equivalent primitives (including two wrong options).
Explicit inputs receive the same guards as sampling. C is arbitrary.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186064172
KP_UUID='8bd8c6d8-0b11-5735-88a1-9b12e6315401'
TITLE='Integrating an Exponential Function With a General Base'
VERSION='general-base-integral-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X=sp.Symbol('x', positive=True)
LEVELS=('easy','moderate','hard')
BASES=tuple(range(2,21))
COEFFICIENTS=tuple(c for c in range(-12,13) if abs(c)>=2)
SOURCE_PARAMETERS={'q-31248':{'b':5,'c':4},'q-66139':{'b':3,'c':1},'q-113887':{'b':5,'c':1},'q-113890':{'b':9,'c':2},'q-113893':{'b':8,'c':1},'q-31249':{'b':2,'c':3}}
SOURCE_LEVELS={'q-31248':'moderate','q-66139':'easy','q-113887':'easy','q-113890':'moderate','q-113893':'hard','q-31249':'moderate'}
SOURCE_TEMPLATES={s:('what_integral' if s=='q-31248' else {'easy':'integer_base','moderate':'scalar_base','hard':'reciprocal_base'}[SOURCE_LEVELS[s]]) for s in SOURCES}
TEMPLATES={'integer_base':'easy','scalar_base':'moderate','what_integral':'moderate','reciprocal_base':'hard'}
# Each listed pair is an eligible full family+bank chosen before parameters.
DEFAULT_FAMILIES={'easy':(('integer_base','base_ln_power'),('integer_base','base_scaled_ln_x')),
                  'moderate':(('scalar_base','scalar_log_coefficient'),('scalar_base','scalar_reciprocal'),('what_integral','scalar_log_coefficient'),('what_integral','scalar_reciprocal')),
                  'hard':(('reciprocal_base','reciprocal_method'),)}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'general-base-integral:'+v))
def read_parameters(p):
    if set(p)!={'b','c'}:raise ValueError('Parameters must contain exactly integer b and c')
    result={}
    for k,v in p.items():
        try:a=sp.sympify(v)
        except Exception as exc:raise ValueError('Invalid exact integer parameter') from exc
        if a.is_Integer is not True:raise ValueError('b and c must be exact integers')
        result[k]=int(a)
    return result

def guard(level,b,c,profile):
    if b not in BASES:raise ValueError('Integer base/reciprocal denominator outside 2..20')
    if level=='moderate':
        if c not in COEFFICIENTS:raise ValueError('Moderate coefficient magnitude must be 2..12')
    elif c!=1:raise ValueError('Easy/hard require unit coefficient')
    if profile in ('raw:q-113890','raw:q-31249') and c<2:raise ValueError('Observed ln(coefficient) evidence requires positive coefficient')
    if profile=='raw:q-31248' and c<2:raise ValueError('Observed positive-scalar evidence requires positive coefficient')
    if profile=='scalar_log_coefficient' and abs(c)==b:raise ValueError('Whole bank rejected: ln coefficient equals ln base')

def exptex(b,reciprocal=False,exponent='x'):
    return '{'+(r'(\frac{1}{'+str(b)+'})' if reciprocal else str(b))+'}^{'+exponent+'}'
def ln(arg,raw):return ('ln\u2061' if raw else r'\ln ')+str(arg)
def frac(a,b):return r'\frac{'+a+'}{'+b+'}'
def integral(b,c,hard=False):return ('' if c==1 else str(c)+r'\cdot ')+exptex(b,hard)
def prompt(b,c,template):
    if template=='what_integral':return r'What is $\displaystyle \int'+str(c)+r' \cdot '+str(b)+r'^{x}dx$?'
    body=integral(b,c,template=='reciprocal_base')
    return (r'$\int '+body+r'\,\text{d}x=$' if template=='scalar_base' else r'Calculate $\int '+body+r'\,\text{d}x.$')

def solution(b,c,template,raw=False):
    L=lambda a:ln(a,raw)
    e=exptex(b,template=='reciprocal_base')
    common='To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:\n\n$$\n'
    if template in ('scalar_base','what_integral'):
        return ('First, we factor out the constant $'+str(c)+'.$ Then, we integrate the exponential function and get\n\n$$\n'+r'\begin{aligned}\int '+str(c)+r'\cdot '+e+r'\,\text{d}x & ='+str(c)+r'\int '+e+r'\,\text{d}x \\  & ='+str(c)+r'\cdot '+frac(e,L(b))+r'+C.\end{aligned}'+'\n$$')
    if template=='integer_base':return common+r'\begin{aligned}\int '+e+r'\,\text{d}x & ='+frac(e,L(b))+r'+C\end{aligned}'+'\n$$'
    rec=r'(\frac{1}{'+str(b)+'})'
    return (common+r'\begin{aligned}\int '+e+r'\,\text{d}x & ='+frac(e,L(rec))+r'+C\end{aligned}'+'\n$$\n\nUsing the laws of logarithms, we have that\n\n$$\n'+r'\begin{aligned}'+L(rec)+' & ='+L(1)+'-'+L(b)+r' \\  & =0-'+L(b)+r' \\  & =-'+L(b)+r'.\end{aligned}'+'\n$$\n\nSo, we can simplify our final answer as follows:\n\n$$\n'+r'\begin{aligned}'+frac(e,L(rec))+'+C=-'+frac(e,L(b))+r'+C\end{aligned}'+'\n$$')

def raw_values(b,c,sid):
    """All five masks per original complete bank; opaque intent remains evidence."""
    e=exptex(b);L=lambda a:ln(a,True);correct=(str(c)+r'\cdot ' if c!=1 else '')+frac(e,L(b))+'+C'
    if sid=='q-66139':return [frac(e,L(b))+'+C',L('('+e+')')+'+C',e+L(b)+'+C',e+'+C',frac(L('x'),L(b))+'+C']
    if sid=='q-113887':return [e+L(b)+'+C',e+'+C',frac(L('x'),L(b))+'+C',frac(e,L(b))+'+C',str(b)+L('x')+'+C']
    if sid=='q-113890':return [str(c)+r'\cdot '+e+'+C',frac(L(b),e)+'+C',frac(e,L(c))+'+C',frac(L(c),str(b)+L('x'))+'+C',correct]
    if sid=='q-113893':
        r=exptex(b,True)
        return [r+L(b)+'+C','-'+frac(r,L(b))+'+C',frac(L('x'),L(b))+'+C','-'+frac(L('x'),e)+'+C',frac(e,L(b))+'+C']
    if sid=='q-31249':return [str(b)+r'\cdot '+frac(exptex(c,exponent=L('x')),L(b))+'+C',frac(L('x'),L(b))+'+C',correct,str(c)+r'\cdot '+frac(exptex(c,exponent=str(b)+'x'),L(c))+'+C',frac(str(b),L('x'))+'+C']
    if sid=='q-31248':
        # The half coefficient and predecessor base are parameterized evidence
        # of the observed 2*4^x form; no historical error algorithm is claimed.
        half=sp.latex(sp.Rational(c,2))
        return [frac(str(b),r'\ln x')+' + C',frac(r'\ln x',r'\ln '+str(b))+' + C',half+r' \cdot '+frac(str(b-1)+'^{x}',r'\ln '+str(b))+' + C',str(c)+r' \cdot '+frac(str(b)+r'^{\ln x}',r'\ln '+str(b))+' + C',str(c)+r' \cdot '+frac(str(b)+'^{x}',r'\ln '+str(b))+' + C']
    raise ValueError(sid)

def bank(b,c,level,profile):
    """Correct first; compute exact full selected bank then reject all collisions."""
    a=sp.Rational(1,b) if level=='hard' else sp.Integer(b)
    correct=c*a**X/sp.log(a)
    opaque=False
    if profile=='base_ln_power' or profile=='raw:q-66139':wrong=[sp.log(b**X),b**X*sp.log(b),b**X,sp.log(X)/sp.log(b)];labels=['ln_of_exponential','multiply_ln_base','omit_ln_base','replace_exponential_by_ln_x']
    elif profile=='base_scaled_ln_x' or profile=='raw:q-113887':wrong=[b**X*sp.log(b),b**X,sp.log(X)/sp.log(b),b*sp.log(X)];labels=['multiply_ln_base','omit_ln_base','replace_exponential_by_ln_x','base_times_ln_x']
    elif profile=='raw:q-113890':wrong=[c*b**X,sp.log(b)/b**X,b**X/sp.log(c),sp.log(c)/(b*sp.log(X))];labels=['omit_ln_base','invert_exponential_quotient','omit_coefficient_and_log_coefficient','opaque_log_coefficient_over_base_ln_x'];opaque=True
    elif profile=='raw:q-31249':wrong=[b*c**sp.log(X)/sp.log(b),sp.log(X)/sp.log(b),c*c**(b*X)/sp.log(c),b/sp.log(X)];labels=['opaque_swap_coefficient_base_and_ln_exponent','replace_by_logarithm','opaque_swapped_base_and_exponent_coefficient','opaque_base_over_ln_x'];opaque=True
    elif profile=='raw:q-31248':wrong=[b/sp.log(X),sp.log(X)/sp.log(b),sp.Rational(c,2)*(b-1)**X/sp.log(b),c*b**sp.log(X)/sp.log(b)];labels=['opaque_base_over_ln_x','replace_by_logarithm','opaque_half_coefficient_predecessor_base','replace_x_by_ln_x'];opaque=True
    elif profile=='raw:q-113893':wrong=[a**X*sp.log(b),sp.log(X)/sp.log(b),-sp.log(X)/b**X,b**X/sp.log(b)];labels=['wrong_log_multiplier_sign','replace_exponential_by_ln_x','opaque_negative_ln_x_over_integer_exponential','invert_reciprocal_base'];opaque=True
    elif profile=='scalar_log_coefficient':wrong=[b**X/sp.log(b),c*b**X,c*b**X*sp.log(b),c*b**X/sp.log(abs(c))];labels=['omit_coefficient','omit_ln_base','multiply_ln_base','log_coefficient_instead_of_base']
    elif profile=='scalar_reciprocal':wrong=[b**X/sp.log(b),c*b**X,b**X/(c*sp.log(b)),c*b**(-X)/sp.log(b)];labels=['omit_coefficient','omit_ln_base','reciprocate_coefficient','reciprocate_base']
    elif profile=='reciprocal_method':wrong=[a**X/sp.log(b),a**X*sp.log(b),b**X/sp.log(b),a**X];labels=['omit_negative_log_sign','multiply_positive_ln_base','invert_reciprocal_base','omit_ln_reciprocal_base']
    else:raise ValueError('Unknown profile '+str(profile))
    expressions=[correct]+wrong
    derivatives=[sp.diff(v,X) for v in expressions]
    for i in range(5):
        if expressions[i].has(sp.nan,sp.zoo,sp.oo,-sp.oo):raise ValueError('Whole bank rejected: undefined option')
        for j in range(i):
            if sp.simplify(derivatives[i]-derivatives[j])==0:raise ValueError('Whole bank rejected: derivative-equivalent choices')
    return expressions,['correct']+labels,opaque

def normal_values(b,c,profile):
    # Retain familiar source syntax, never let SymPy rewrite b^x to hyperbolics.
    e=exptex(b);L=lambda a:ln(a,False);F=lambda n,d:frac(n,d)+'+C'
    correct=(str(c)+r'\cdot ' if c!=1 else '')+F(e,L(b))
    if profile in ('base_ln_power','base_scaled_ln_x'):
        return [v.replace('ln\u2061',r'\ln ') for v in raw_values(b,c,'q-66139' if profile=='base_ln_power' else 'q-113887')]
    if profile=='scalar_log_coefficient':return [correct,F(e,L(b)),str(c)+r'\cdot '+e+'+C',str(c)+r'\cdot '+e+L(b)+'+C',str(c)+r'\cdot '+F(e,L(abs(c)))]
    if profile=='scalar_reciprocal':return [correct,F(e,L(b)),str(c)+r'\cdot '+e+'+C',F(e,str(c)+L(b)),str(c)+r'\cdot '+F(exptex(b,exponent='-x'),L(b))]
    if profile=='reciprocal_method':
        r=exptex(b,True)
        return ['-'+F(r,L(b)),F(r,L(b)),r+L(b)+'+C',F(e,L(b)),r+'+C']
    raise ValueError(profile)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unsupported difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields supported')
    rng=random.Random(seed);raw=profile is not None and profile.startswith('raw:');sid=profile[4:] if raw else None
    if raw:
        if sid not in SOURCES or SOURCE_LEVELS[sid]!=level:raise ValueError('Source profile level mismatch')
        expected=SOURCE_TEMPLATES[sid]
        if template not in (None,expected):raise ValueError('Source profile template mismatch')
        template=expected
    else:
        eligible=[pair for pair in DEFAULT_FAMILIES[level] if (template is None or pair[0]==template) and (profile is None or pair[1]==profile)]
        if not eligible:raise ValueError('No eligible whole template/bank for this level')
        template,profile=rng.choice(eligible)
    # Selection precedes all parameter construction and rejection; no recipe pool.
    for attempt in range(1000):
        p=read_parameters(parameters) if parameters is not None else {'b':rng.choice(BASES),'c':rng.choice(COEFFICIENTS) if level=='moderate' else 1}
        b,c=p['b'],p['c']
        try:
            guard(level,b,c,profile);expressions,recipes,opaque=bank(b,c,level,profile)
        except ValueError:
            if parameters is not None:raise
            continue
        break
    else:raise ValueError('No unambiguous instance sampled for selected whole bank')
    values=raw_values(b,c,sid) if raw else normal_values(b,c,profile)
    # Read-only source profile uses presence policy, never returns copied payload.
    q={':question/problem':prompt(b,c,template)}
    if sid!='q-31248':
        q[':question/difficulty']=':question.difficulty/'+level
        q[':question/worked-solution']=solution(b,c,template,raw)
    elif not raw:raise AssertionError('Unreachable raw omission branch')
    if not raw:
        q[':question/difficulty']=':question.difficulty/'+level
        q[':question/worked-solution']=solution(b,c,template,False)
    a=sp.Rational(1,b) if level=='hard' else sp.Integer(b)
    task=digest({'integrand':sp.srepr(c*a**X),'request':'indefinite_integral','field':'radio'})
    correct_value=next(v for v in values if v==((str(c)+r'\cdot ' if c!=1 else '')+frac(exptex(b),ln(b,raw))+'+C')) if level!='hard' and sid!='q-31248' else ('-'+frac(exptex(b,True),ln(b,raw))+'+C' if level=='hard' else values[-1])
    identity=digest({'version':VERSION,'level':level,**q,'bank':sorted(values),'correct':None if sid=='q-31248' else correct_value})
    qid=uid(identity);fid=uid(qid+':selection')
    answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if sid!='q-31248':field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct_value)]
    rng.shuffle(answers);q[':question/id']=qid;q[':question/answer-fields']=[field]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
        'version':VERSION,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__,
        'seed':seed,'level':level,'template':template,'field_type':'radio','profile':profile,'parameters':p,'recipes':recipes,
        'mathematical_fingerprint':task,'content_fingerprint':identity,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},
        'source_ids':[sid] if raw else list(SOURCES),'evidence_only':raw,'eligible_for_learning':not raw,'opaque_historical_intent':opaque,
        'authored_generalization':not raw,'plots':[],'domain':'real x; logarithmic distractors compared on x>0; arbitrary additive C',
        'missing_correct_inferred_separately':sid=='q-31248','authored_level_assignment':sid=='q-31248'}}

# Easy: apply divide-by-ln(base) once, unit coefficient.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: factor a signed nonunit scalar, then the same base rule.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: reciprocal base, base rule and the source's three log-law rows.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return '\n\n'.join([q[':question/problem']]+['- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']]+([q[':question/worked-solution']] if ':question/worked-solution' in q else []))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    if args.count<1:ap.error('count must be positive')
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
