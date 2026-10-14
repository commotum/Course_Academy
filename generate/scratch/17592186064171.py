#!/usr/bin/env python3
"""Constant multiples of e^x: basis2275 draft, steps3–7 only.

Observed families: signed integer, rational, symbolic pi^2 constants, all radio.
No linear substitution, variable coefficients, general bases, sums or plots.
Raw profiles preserve all source presence omissions and notation; they are
evidence-only. Normal profiles are complete method-derived banks, selected
before parameters, with whole-instance derivative-equivalence rejection.
The missing unrated source has an authored easy routing label only in metadata.
Bounds extend the observed number forms using constant-multiple prerequisites:
easy ±2..±12; moderate reduced positive proper fractions n<=9,d<=12;
hard m*pi^p, m=±1..±5,p=2..5. These are authored sampling bounds, not recovered
original generation policies. Every level keeps the same two solution rows.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186064171
KP_UUID='3f9548e6-28ef-5a97-ab04-dfb1b6e23c16'
TITLE='Integrating the Exponential Function'
VERSION='constant-exponential-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X=sp.Symbol('x', positive=True)
LEVELS=('easy','moderate','hard')
SOURCE_COEFFICIENTS={'q-31244':'3','q-31245':'-2','q-113853':'-4','q-71900':'1/2','q-71914':'-5','q-71918':'pi**2'}
SOURCE_LEVELS={sid:q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1] for sid,q in SOURCES.items()}
TEMPLATES={'integer_constant':'easy','rational_constant':'moderate','symbolic_constant':'hard','what_integral':'easy'}
DEFAULT_PROFILES={'easy':('method_exponent','method_reciprocal_sign','method_omit'), 'moderate':('method_rational',),'hard':('method_symbolic',)}

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,'constant-exponential:'+v))
def coefficient(p):
    if set(p)!={'c'}: raise ValueError('Parameters must contain only c')
    try: c=sp.sympify(p['c'],locals={'pi':sp.pi})
    except Exception as e: raise ValueError('Invalid exact coefficient') from e
    if c.free_symbols or c.is_real is not True: raise ValueError('c must be a real constant')
    return sp.simplify(c)
def domain(level):
    if level=='easy': return [sp.Integer(i) for i in range(-12,13) if abs(i)>=2]
    if level=='moderate': return sorted({sp.Rational(n,d) for n in range(1,10) for d in range(2,13) if n<d},key=float)
    return [m*sp.pi**p for p in range(2,6) for m in range(-5,6) if m]
def check_domain(level,c):
    if c not in domain(level): raise ValueError('Coefficient outside '+level+' authored bounds')
def tex(c):
    if c==sp.pi**2:return r'{\pi }^{2}'
    if c.is_Rational:
        if c.q==1:return str(c)
        return ('-' if c<0 else '')+r'\frac{'+str(abs(c.p))+'}{'+str(c.q)+'}'
    return sp.latex(c)
def product(c,exponent='x',style='aligned'):
    e=r'{e}^{'+exponent+'}' if style=='aligned' else 'e^{'+exponent+'}'
    return ('' if c==1 else ('-' if c==-1 else tex(c)))+e
def primitive(c,exponent='x',style='aligned'): return product(c,exponent,style)+'+C'

def bank(c,profile):
    """Correct primitive first, then the COMPLETE selected operation bank."""
    correct=c*sp.exp(X)
    if profile in ('raw:q-31244','raw:q-31245','method_exponent'):
        wrong=[c*sp.exp(-X),sp.exp(c*X),c*sp.exp(sp.log(X)),sp.exp(X)/c]
        labels=['reciprocate_exponential','move_constant_into_exponent','replace_x_by_ln_x','reciprocate_constant']
    elif profile in ('raw:q-113853','method_reciprocal_sign'):
        wrong=[sp.exp(X)/c,-c*sp.exp(-X),-sp.exp(X)/c,-c*sp.exp(X)]
        labels=['reciprocate_constant','reverse_sign_and_reciprocate_exponential','reverse_sign_and_reciprocate_constant','reverse_sign']
    elif profile=='raw:q-71914':
        wrong=[sp.exp(X)/c,sp.exp(X),-c*sp.exp(-c*X),sp.exp(c*X)]
        labels=['reciprocate_constant','omit_constant','observed_opposite_constant_and_exponent_opaque_intent','move_constant_into_exponent']
    elif profile=='method_omit':
        wrong=[sp.exp(X)/c,sp.exp(X),c*sp.exp(c*X),sp.exp(c*X)]
        labels=['reciprocate_constant','omit_constant','copy_constant_also_into_exponent','move_constant_into_exponent']
    elif profile in ('raw:q-71900','method_rational'):
        wrong=[c*sp.exp(X/c),sp.exp(X),c*sp.exp(c*X),sp.exp(X)/c]
        labels=['reciprocal_constant_into_exponent','omit_constant','copy_constant_into_exponent','reciprocate_constant']
    elif profile in ('raw:q-71918','method_symbolic'):
        # Treat the constant as a variable power, then substitute pi back.
        z=sp.Symbol('z'); variable_c=c.xreplace({sp.pi:z}); dc=sp.diff(variable_c,z).subs(z,sp.pi)
        wrong=[sp.exp(X)/dc,sp.exp(X)/c,dc*sp.exp(X),sp.exp(X)]
        labels=['reciprocal_derivative_of_constant_as_variable','reciprocate_constant','differentiate_constant_as_variable','omit_constant']
    else: raise ValueError('Unknown profile '+str(profile))
    result=[correct]+wrong
    derivatives=[sp.diff(a,X) for a in result]
    for i in range(len(result)):
        for j in range(i):
            if sp.simplify(derivatives[i]-derivatives[j])==0: raise ValueError('Whole bank rejected: equivalent primitives')
    return result,['correct']+labels

def raw_values(c,sid):
    """Parameterized observed expression masks, preserving exact source spelling."""
    s=tex(c); ex=r'{e}^{x}'
    if sid=='q-31244':
        return [''+s+'e^{x} + C',r'\frac{'+s+r'}{e^{x}} + C','e^{'+s+'x} + C',s+r'e^{\ln x} + C',r'\frac{e^{x}}{'+s+'} + C']
    if sid=='q-31245':
        reciprocal=('-' if c<0 else '')+r'\frac{{e}^{x}}{'+tex(abs(c))+'}+C'
        reciprocal_e=('-' if c<0 else '')+r'\frac{'+tex(abs(c))+r'}{{e}^{x}}+C'
        return [s+ex+'+C',reciprocal_e,'{e}^{'+s+'x}+C',s+r'{e}^{ln⁡x}+C',reciprocal]
    if sid=='q-113853':
        recip=lambda k: ('-' if k<0 else '')+r'\frac{{e}^{x}}{'+tex(abs(1/k))+'}+C'
        return [s+ex+'+C',recip(1/c),r'\frac{'+tex(-c)+r'}{{e}^{x}}+C',recip(-1/c),tex(-c)+ex+'+C']
    if sid=='q-71914':
        return [s+ex+'+C',tex(1/c)+ex+'+C',ex+'+C',tex(-c)+'{e}^{'+tex(-c)+'x}+C','{e}^{'+s+'x}+C']
    if sid=='q-71900':
        exponent= str(c.p)+'/'+str(c.q)+'x'
        return [s+ex+'+C',s+'{e}^{'+tex(1/c)+'x}+C',ex+'+C',s+'{e}^{'+exponent+'}+C',tex(1/c)+ex+'+C']
    if sid=='q-71918':
        z=sp.Symbol('z'); dc=sp.diff(c.xreplace({sp.pi:z}),z).subs(z,sp.pi)
        dtex=tex(dc).replace(' ', '').replace(r'\pi',r'\pi ')
        invc=r'\frac{1}{'+s+'}'; invdc=r'\frac{1}{'+dtex+'}'
        return [s+ex+'+C',invdc+ex+'+C',invc+ex+'+C',dtex+ex+'+C',ex+'+C']
    raise ValueError(sid)

def rendered_values(c,profile,expressions):
    if profile.startswith('raw:'):return raw_values(c,profile[4:])
    if profile=='method_exponent':return raw_values(c,'q-31245')
    if profile=='method_reciprocal_sign':return raw_values(c,'q-113853')
    if profile=='method_rational':return raw_values(c,'q-71900')
    if profile=='method_symbolic':return raw_values(c,'q-71918')
    return [sp.latex(a).replace(r'\log',r'\ln')+'+C' for a in expressions]
def prompt(c,template):
    if template=='what_integral':return 'What is $'+r'\displaystyle \int'+product(c,style='plain')+'dx$?'
    return r'$\int '+product(c)+r'\,\text{d}x=$'
def solution(c):
    s=tex(c)
    return ('Factoring out the constant $'+s+'$ and calculating the resulting integral, we get\n\n$$\n'+r'\begin{aligned}\int '+product(c)+r'\,\text{d}x & ='+s+r'\int {e}^{x}\,\text{d}x \\  & ='+primitive(c)+r'.\end{aligned}'+'\n$$')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unsupported level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields supported')
    rng=random.Random(seed)
    profile=profile or rng.choice(DEFAULT_PROFILES[level]) # before parameter selection
    raw=profile.startswith('raw:')
    sid=profile[4:] if raw else None
    if raw and (sid not in SOURCES or SOURCE_LEVELS[sid]!=level):raise ValueError('Source profile level mismatch')
    if not raw and profile not in DEFAULT_PROFILES[level]:raise ValueError('Profile level mismatch')
    if template is None:
        if raw:template='what_integral' if sid=='q-31244' else {'easy':'integer_constant','moderate':'rational_constant','hard':'symbolic_constant'}[level]
        else:template=rng.choice(('integer_constant','what_integral')) if level=='easy' else {'moderate':'rational_constant','hard':'symbolic_constant'}[level]
    if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('Template level mismatch')
    if raw and (template=='what_integral')!=(sid=='q-31244'):raise ValueError('Source template mismatch')
    c=coefficient(parameters) if parameters is not None else rng.choice(domain(level))
    check_domain(level,c)
    expressions,recipes=bank(c,profile)
    values=rendered_values(c,profile,expressions)
    q={':question/problem':prompt(c,template)}
    if sid!='q-31244':
        q[':question/difficulty']=':question.difficulty/'+level
        q[':question/worked-solution']=solution(c)
    task=digest({'integrand':sp.srepr(c*sp.exp(X)),'request':'indefinite_integral','field':'radio'})
    identity=digest({'version':VERSION,'level':level,**q,'bank':sorted(values),'correct':None if sid=='q-31244' else values[0]})
    qid=uid(identity);fid=uid(qid+':selection')
    answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if sid!='q-31244':field[':answer-field/correct']=[':answer/id',answers[0][':answer/id']]
    rng.shuffle(answers)
    q[':question/id']=qid;q[':question/answer-fields']=[field]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
        'version':VERSION,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':sp.__version__,
        'seed':seed,'level':level,'template':template,'field_type':'radio','profile':profile,'parameters':{'c':str(c)},'recipes':recipes,
        'mathematical_fingerprint':task,'content_fingerprint':identity,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},
        'source_ids':[sid] if raw else list(SOURCE_COEFFICIENTS),'evidence_only':raw,'eligible_for_learning':not raw,
        'authored_generalization':not raw,'plots':[],'domain':'real x; ln distractor interpreted on x>0; arbitrary C',
        'missing_correct_inferred_separately':sid=='q-31244'}}

# Easy: signed integer constants, keeping sign through constant factorization.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: reduced positive rational constants; same factorization workload.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: symbolic powers of pi remain constants; no variable differentiation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return '\n\n'.join([q[':question/problem']]+['- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']]+([q[':question/worked-solution']] if ':question/worked-solution' in q else []))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
