"""Local, unregistered exponential-product draft at immutable math basis 2275.

Easy: observed quadratic monomial substitutions, including direct differential;
the incomplete cubic q-73800 has a separately authored easy completion.
Moderate: observed positive rational cubic exponent, nonunit differential ratio.
Hard: authored negative quartic exponent, from canonical e-14403 (not an
observed difficulty): same substitution, signed rational scale, general base.

Raw observed banks are parameterized public evidence profiles. Their expression
transport does not establish historical error intent. Normal complete banks
derive actual chain-factor/logarithm operations and preserve each family's
source prose and ordered mathematical stages. Nothing imports live capture code.
"""
import argparse
import copy
from functools import lru_cache
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import re
import sys
import uuid
import sympy as sp

HERE=Path(__file__).with_suffix('')
def private_module(name,filename):
    spec=importlib.util.spec_from_file_location(name,HERE/filename)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
fmt=private_module('kp84350_frozen_format','frozen_math_format.py')
parser=private_module('kp84350_frozen_parser','frozen_parser.py')
KP_ID=17592186184350
KP_UUID='e8720b44-317d-590e-a251-bfcec97e0513'
TITLE='Integrating Products Containing Other Exponential Functions'
VERSION='other-base-products-private-v2'
NS=uuid.UUID('08d191cb-adcb-5a86-af24-ab0dc27b3e6c')
x=parser.x
BASES=tuple(range(2,13))
LEVELS=('easy','moderate','hard')
DATA={
 'q-31420':dict(base=8,level='easy',a=3,n=2,shift=0,d=1,prefactor=1),
 'q-31419':dict(base=4,level='easy',a=1,n=2,shift=-7,d=1,prefactor=1),
 'q-31426':dict(base=5,level='easy',a=1,n=2,shift=0,d=3,prefactor=1),
 'q-73665':dict(base=4,level='easy',a=4,n=2,shift=-3,d=1,prefactor=4),
 'q-73801':dict(base=6,level='easy',a=1,n=2,shift=1,d=1,prefactor=2),
 'q-73802':dict(base=7,level='easy',a=1,n=2,shift=-7,d=1,prefactor=1),
 'q-211989':dict(base=4,level='moderate',a=1,n=3,shift=0,d=5,prefactor=1),
 'q-73800':dict(base=3,level='easy',a=1,n=3,shift=-5,d=1,prefactor=3),
 'negative-quartic':dict(base=3,level='hard',a=-1,n=4,shift=1,d=1,prefactor=1),
}
DOMAINS={
 'q-31420':{'base':BASES,'a':tuple(range(2,6))},
 'q-31419':{'base':BASES,'shift':tuple(range(-9,0))},
 'q-31426':{'base':BASES,'d':tuple(range(3,10))},
 'q-73665':{'base':BASES,'a':tuple(range(2,6)),'shift':tuple(range(-6,0))},
 'q-73801':{'base':BASES,'shift':tuple(range(1,10))},
 'q-73802':{'base':BASES,'shift':tuple(range(-9,0))},
 'q-211989':{'base':BASES,'d':(2,4,5,7,8)},
 'q-73800':{'base':BASES,'shift':tuple(range(-9,0))},
 'negative-quartic':{'base':BASES,'a':(-1,-2,-3),'shift':tuple(range(-5,0))+tuple(range(1,6))},
}

@lru_cache(maxsize=1)
def capture():return json.loads((HERE/'source.json').read_text())
def sources():return {q[':question/math-academy-id']:q for q in capture()['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
def sha(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(NS,value))
def latex(expr):return sp.latex(expr).replace(r'\log',r'\ln')
def scalar(text):return parser.scalar(text.replace(r'\dfrac',r'\frac'))
def base_transport(text,old,new):
    text=text.replace('{'+str(old)+'}^','{'+str(new)+'}^')
    text=re.sub(r'(\\operatorname\{ln\}⁡)'+str(old)+r'(?!\d)',lambda m:m[1]+str(new),text)
    text=re.sub(r'(\\ln )'+str(old)+r'(?!\d)',lambda m:m[1]+str(new),text)
    # q-73800 alone has naked bases; the prefactor 3x² stays fixed.
    text=text.replace(str(old)+'^{x^{3} - 5}',str(new)+'^{x^{3} - 5}')
    return text

def parameters_for(template,raw,parameters,rng):
    domain={'base':BASES} if raw else DOMAINS[template]
    defaults={key:DATA[template][key] for key in domain}
    if parameters is None:
        return {key:rng.choice(values) for key,values in domain.items()}
    if type(parameters) is not dict or set(parameters)!=set(domain):
        raise ValueError('Explicit parameters require exactly '+','.join(domain))
    if any(type(value) is not int or value not in domain[key] for key,value in parameters.items()):
        raise ValueError('Parameters outside the explicit finite workload domain')
    return dict(parameters)

def complete_parameters(template,parameters):
    result=dict(DATA[template]);result.update(parameters)
    if template=='q-73665':result['prefactor']=result['a']
    return result

def mathematical_data(p):
    U=sp.Rational(p['a'],p['d'])*x**p['n']+p['shift']
    P=sp.Integer(p['prefactor'])*x**(p['n']-1)
    R=sp.Rational(p['prefactor']*p['d'],p['a']*p['n'])
    E=sp.Pow(sp.Integer(p['base']),U,evaluate=False)
    F=R*E/sp.log(p['base'])
    return U,P,R,E,F

def atomic_slots(text,replacements):
    """Replace complete mathematical components simultaneously, longest first."""
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)))
    return pattern.sub(lambda m:replacements[m[0]],text)

def source_solution(template,p):
    """Operative source masks, including q-73665's outer scalar stages and
    q-73801's omitted redundant extraction row. No generic CAS stage chain.
    """
    source=sources()[template]
    b=p['base'];text=base_transport(source[':question/worked-solution'],DATA[template]['base'],b)
    problem=base_transport(source[':question/problem'],DATA[template]['base'],b)
    replacements={}
    if template=='q-31420':
        a=p['a'];replacements={'3{x}^{2}':str(a)+'{x}^{2}','6x':str(2*a)+'x',r'\frac{1}{6}':r'\frac{1}{'+str(2*a)+'}',r'6\operatorname{ln}':str(2*a)+r'\operatorname{ln}'}
    elif template in ('q-31419','q-73802'):
        replacements={'{x}^{2}-7':'{x}^{2}'+str(p['shift'])}
    elif template in ('q-31426','q-211989'):
        n=p['n'];d=p['d'];old=DATA[template]['d'];power='{x}^{'+str(n)+'}'
        replacements={power+'/'+str(old):power+'/'+str(d),r'\frac{'+power+'}{'+str(old)+'}':r'\frac{'+power+'}{'+str(d)+'}',r'\frac{'+str(n)+'}{'+str(old)+'}':r'\frac{'+str(n)+'}{'+str(d)+'}',r'\frac{'+str(old)+'}{'+str(n)+'}':r'\frac{'+str(d)+'}{'+str(n)+'}',r'\frac{'+str(old)+r'\cdot ':r'\frac{'+str(d)+r'\cdot '}
    elif template=='q-73665':
        a=p['a'];s=p['shift'];replacements={'4{x}^{2}-3':str(a)+'{x}^{2}'+str(s),'8x':str(2*a)+'x',r'\frac{1}{8}':r'\frac{1}{'+str(2*a)+'}','4x':str(a)+'x','=4\\int':'='+str(a)+r'\int'}
    elif template=='q-73801':replacements={'{x}^{2}+1':'{x}^{2}+'+str(p['shift'])}
    return atomic_slots(problem,replacements),atomic_slots(text,replacements)

def authored_solution(p):
    """Same source introduction, formal derivative/differential, reordering,
    substitution, scalar extraction, exponential primitive, back substitution.
    Used only for missing q-73800 and canonical-grounded negative quartic.
    """
    U,P,R,E,F=mathematical_data(p);u=latex(U);power=r'{'+str(p['base'])+r'}^{'+u+'}';upower=r'{'+str(p['base'])+r'}^{u}'
    pref=latex(P);ratio=latex(R);prime=latex(sp.diff(U,x));lb=r'\ln '+str(p['base'])
    grouped=r'\left('+ratio+r'\right)' if R<0 else ratio
    integrand=pref+r'\,'+power
    prompt=r'Calculate the integral $\int '+integrand+r'\,\text{d}x.$'
    rows=[r'\int '+integrand+r'\,\text{d}x & =\int '+power+r'\cdot '+pref+r'\,\text{d}x',
          r'& =\int '+upower+r'\cdot '+grouped+r'\,\text{d}u']
    if R!=1:rows.append(r'& ='+grouped+r'\int '+upower+r'\,\text{d}u')
    rows.extend([r'& ='+grouped+r'\cdot\frac{'+upower+'}{'+lb+r'}+C',r'& ='+latex(F)+r'+C.'])
    solution="Let's introduce the new variable $u="+u+".$ Differentiating gives\n\n$$\n"+r'\frac{\text{d}u}{\text{d}x}='+prime+r'\,⟹\,'+grouped+r'\text{d}u='+pref+r'\,\text{d}x.'+'\n$$\n\nTherefore,\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
    return prompt,solution

def normal_bank(template,p):
    """Complete bank chosen from actual derivative/log operations, never a pool.
    Direct R=1 families use their real monomial derivative coefficient n;
    all other families invert or omit the nonunit differential ratio.
    """
    U,P,R,E,F=mathematical_data(p);L=sp.log(p['base'])
    if R==1:
        exprs=[F,E,E*L,E/(p['n']*L),p['n']*E/L]
        recipes=['correct','omit logarithm divisor','multiply by logarithm','retain monomial derivative coefficient','apply prefactor twice']
    else:
        exprs=[F,R*E,R*E*L,E/(R*L),E/L]
        recipes=['correct','omit logarithm divisor','multiply by logarithm','invert differential ratio','omit differential ratio']
    return [latex(v)+'+C' for v in exprs],recipes,0

def mathematical_fingerprint(prompt):
    match=re.search(r'\{?(\d+)\}?\^\{',prompt)
    if not match:raise ValueError('Missing numeric exponential base')
    base=int(match[1]);start=match.end();pos=start;depth=1
    while depth:
        depth+=(prompt[pos]=='{')-(prompt[pos]=='}');pos+=1
    U=scalar(prompt[start:pos-1]);J=displayed_integrand(prompt)
    P=sp.cancel(J/sp.Integer(base)**U)
    return task_fingerprint(base,U,P)

def task_fingerprint(base,U,P):
    """Prime-base exponential normalization merges b=4,d=6 with b=2,d=3,
    and excludes bank/profile/seed/spelling from assessed-task counts."""
    shift=U.subs(x,0);variable=sp.expand(U-shift)
    multiplier=sp.cancel(P*sp.Integer(base)**shift)
    exponents=[(int(prime),sp.srepr(sp.expand(power*variable))) for prime,power in sorted(sp.factorint(base).items())]
    return sha({'multiplier':sp.srepr(multiplier),'prime_exponents':exponents})

def displayed_integrand(prompt):
    match=re.search(r'\\int\s*(.*?)\s*(?:\\,)?(?:\\text\{d\}|dx|\\textrm\{d\})',prompt,re.S)
    if not match:raise ValueError('No displayed integral')
    raw=match[1].strip()
    if raw.endswith(r'\,'):raw=raw[:-2]
    return scalar(raw)

def normalize_and_check(prompt,solution,values,raw=False):
    strings=[prompt,*values]+([solution] if solution is not None else [])
    if any(any(ord(c)<32 and c not in '\n\t\r' for c in s) for s in strings):raise ValueError('Control character in learner content')
    if not raw:
        prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution);values=[fmt.normalize_tex(v) for v in values]
    fmt.validate_prose(prompt)
    if solution is not None:fmt.validate_prose(solution)
    for value in values:fmt.validate_tex(value)
    return prompt,solution,values

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS or type(seed) is not int:raise ValueError('Valid level and integer seed required')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Observed radio layout required')
    if template is not None and (type(template) is not str or template not in DATA):raise ValueError('Unknown template')
    rng=random.Random(seed)
    if template is None and type(profile) is str and profile.startswith('observed-'):
        template=profile[len('observed-'):]
        if template not in DATA:raise ValueError('Unknown observed profile')
    if template is None:template=rng.choice([t for t,p in DATA.items() if p['level']==level])
    if DATA[template]['level']!=level:raise ValueError('Template does not belong to requested level')
    if profile is None:profile='method-derived'
    if profile not in ('method-derived','observed','observed-'+template):raise ValueError('Unknown profile')
    raw=profile!='method-derived'
    if raw and template=='negative-quartic':raise ValueError('No observed hard practice bank')
    params=parameters_for(template,raw,parameters,rng);p=complete_parameters(template,params)
    original=sources().get(template);raw_incomplete=raw and template=='q-73800'
    if raw:
        oldbase=DATA[template]['base'];prompt=base_transport(original[':question/problem'],oldbase,p['base'])
        solution=base_transport(original[':question/worked-solution'],oldbase,p['base']) if ':question/worked-solution' in original else None
        field=original[':question/answer-fields'][0]
        values=[base_transport(a[':answer/value'],oldbase,p['base']) for a in field[':answer-field/choices']]
        ci=next((i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field.get(':answer-field/correct',{}).get(':answer/id')),None)
        recipes=['opaque historical expression transport; historical error operation not recovered']*5
    else:
        prompt,solution=authored_solution(p) if template in ('q-73800','negative-quartic') else source_solution(template,p)
        values,recipes,ci=normal_bank(template,p)
    prompt,solution,values=normalize_and_check(prompt,solution,values,raw)
    U,P,R,E,F=mathematical_data(p)
    if sp.expand(displayed_integrand(prompt)-P*E)!=0:raise ValueError('Rendered prompt differs from its mathematical recipe')
    if not raw_incomplete:assert_bank(values,ci,P*E)
    content={'version':VERSION,'level':None if raw_incomplete else level,'prompt':prompt,'solution':solution,'bank':sorted(values),'correct':values[ci] if ci is not None else None}
    qid=uid('question:'+sha(content));fid=uid(qid+':field:selection')
    answers=[{':answer/id':uid(fid+':answer:'+value),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct_id=answers[ci][':answer/id'] if ci is not None else None
    rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if correct_id is not None:field[':answer-field/correct']=[':answer/id',correct_id]
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw_incomplete:question[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:question[':question/worked-solution']=solution
    generation={'version':VERSION,'seed':seed,'template':template,'profile':('observed-'+template) if raw else profile,'parameters':params,'source_basis':capture()['basis'],'source_lineage':capture()['lineage'],'source_question':template if original else 'e-14403','evidence_only':raw,'eligible_for_learning':not raw,'authored_completion':not raw and template=='q-73800','authored_difficulty':not raw and template in ('negative-quartic','q-73800'),'domain':'All real x; integer base 2..12, finite template-specific integer coefficients. Every power base is positive; all bank choices are real on R.','parameter_domain':{k:list(v) for k,v in ({'base':BASES} if raw else DOMAINS[template]).items()},'recipes':recipes,'interpretation_limit':'Observed expression transport is not recovered historical error intent.' if raw else 'Authored complete bank from displayed substitution and exponential integration operations.','mathematical_fingerprint':mathematical_fingerprint(prompt),'content_fingerprint':sha(content),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'math_format':fmt.FORMAT_VERSION,'plots':'none'}
    result={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':generation}
    if set(result['knowledge_point'])!={'db_id','id','title'}:raise AssertionError('Invalid outer KP keys')
    if not raw:fmt.validate_generated_record(result)
    return result

@lru_cache(maxsize=32768)
def derivative_tex(value):return sp.diff(scalar(value),x)
@lru_cache(maxsize=65536)
def equal(a,b):
    if a==b:return True
    return sp.cancel(sp.expand_log(a-b,force=True))==0
def assert_bank(values,ci,integrand):
    derivatives=[derivative_tex(v) for v in values]
    if len(values)!=5 or sum(equal(v,integrand) for v in derivatives)!=1 or not equal(derivatives[ci],integrand):raise ValueError('Invalid complete bank key')
    for i,a in enumerate(derivatives):
        for b in derivatives[i+1:]:
            if equal(a,b):raise ValueError('Bank collision modulo additive integration constant')

# Easy: observed quadratic families; q-73800 completion remains authored.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: cubic exponent divided by 2,4,5,7,8; reduced nonunit rational ratio.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: canonical-grounded negative quartic; signed ratio, no new operation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def batch(level,count=5,seed=0,template=None,field_type=None,profile=None):
    if level not in LEVELS or type(count) is not int or count<1 or type(seed) is not int:raise ValueError('Valid level, positive count and integer seed required')
    if template is not None and (type(template) is not str or template not in DATA):raise ValueError('Unknown template')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Observed radio layout required')
    if template is None and type(profile) is str and profile.startswith('observed-'):
        template=profile[len('observed-'):]
        if template not in DATA:raise ValueError('Unknown observed profile')
    templates=[template] if template else [t for t,p in DATA.items() if p['level']==level]
    choices=[];seen=set()
    for family in templates:
        if DATA[family]['level']!=level:raise ValueError('Template does not belong to level')
        domain={'base':BASES} if profile is not None and profile!='method-derived' else DOMAINS[family]
        for values in itertools.product(*domain.values()):
            params=dict(zip(domain,values));p=complete_parameters(family,params);U,P,*_=mathematical_data(p);fp=task_fingerprint(p['base'],U,P)
            if fp not in seen:choices.append((family,params));seen.add(fp)
    if count>len(choices):raise ValueError('Requested batch exceeds finite meaningful task domain: '+str(len(choices)))
    random.Random(seed).shuffle(choices)
    return [generate(level,seed+i,family,field_type,params,profile) for i,(family,params) in enumerate(choices[:count])]

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0];correct=f.get(':answer-field/correct',[None,None])[1]
    return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value']+(' (correct)' if a[':answer/id']==correct else '') for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Raw source has no worked solution or correct designation.]')
if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');cli.add_argument('--seed',type=int,default=0);cli.add_argument('--count',type=int,default=2);cli.add_argument('--format',choices=('markdown','json'),default='json');cli.add_argument('--template');cli.add_argument('--profile')
    args=cli.parse_args();records=[]
    for level in LEVELS if args.difficulty=='all' else (args.difficulty,):records.extend(batch(level,args.count,args.seed,args.template,profile=args.profile))
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(map(markdown,records)))
