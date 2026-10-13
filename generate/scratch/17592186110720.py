#!/usr/bin/env python3
"""One unknown parameter in ax=bx; exact local generator (steps 3–7 only).

Basis 1356 source fidelity: scale/shift radio templates, affine blank template.
Easy normal banks are authored complete mathematical-error banks; ambiguous
source recipe intentions remain available through explicit observed profiles.
Moderate keeps two integer-coefficient inverse operations. Authored hard keeps
exactly the same two operations with three reduced rational coefficients; it
never introduces an independent constant term in x or a second parameter.
See the adjacent evidence folder for workload guards, full-bank extraction,
linked lesson route, source replay and native in-memory grading checks.

Explicit parameters are {a,b,c,var}; rationals use integers or exact strings.
The displayed coefficient is a*var+b, and the opposite coefficient is c.
Seed controls parameter sampling and choice order, never content identity.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import random
import uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186110720
KP_UUID='c6cd2f04-e0d5-5df0-8e74-ea737501cdf8'
TITLE='Solving For an Unknown Parameter'
VERSION='unknown-parameter-1356-v2'
PACKAGE=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={
    'scale_radio':{'level':'easy','field':'radio','sources':['q-287970','q-288436','q-288440']},
    'shift_radio':{'level':'easy','field':'radio','sources':['q-287971']},
    'affine_blank':{'level':'moderate','field':'blank','sources':['q-287975']},
    'fraction_affine_blank':{'level':'hard','field':'blank','sources':[]},
}
# A complete bank is selected BEFORE sampling. No candidate pooling/replacement.
PROFILES={
    'authored_scale':('scale_radio',('reciprocal','reverse_sign','omit_division','multiply_instead_of_divide'),'authored'),
    'authored_shift':('shift_radio',('reverse_shift','divide_by_shift','invert_shift_ratio','omit_shift'),'authored'),
    'observed_ratio':('scale_radio',('reciprocal','negative_reciprocal','unit_constraint','zero_constraint'),'observed'),
    'observed_scale':('scale_radio',('unit_constraint','coefficient_as_answer','divide_coefficient_by_answer','omit_division'),'observed'),
    'observed_signed':('scale_radio',('reverse_sign','reciprocal','zero_constraint','negated_coefficient'),'observed'),
    'observed_shift':('shift_radio',('divide_by_shift','invert_shift_ratio','omit_shift','shift_magnitude_as_answer'),'observed'),
    'blank':(None,(),'observed-layout'),
}
CASES={
    'q-287970':('scale_radio','observed_ratio',{'a':2,'b':0,'c':3,'var':'p'}),
    'q-287971':('shift_radio','observed_shift',{'a':1,'b':-3,'c':4,'var':'p'}),
    'q-288436':('scale_radio','observed_scale',{'a':5,'b':0,'c':10,'var':'p'}),
    'q-288440':('scale_radio','observed_signed',{'a':-4,'b':0,'c':8,'var':'k'}),
    'q-287975':('affine_blank','blank',{'a':2,'b':-3,'c':5,'var':'p'}),
}
PROFILE_ALIASES={'ratio-unit':'observed_ratio','scale-bank':'observed_scale','signed-bank':'observed_signed','shift-bank':'observed_shift'}


def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def ident(obj):
    return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(obj)))

def rational(value):
    if isinstance(value,bool) or isinstance(value,float):
        raise ValueError('Use an integer or exact rational string, not bool/float')
    try: result=sp.Rational(value)
    except (TypeError,ValueError,ZeroDivisionError) as exc: raise ValueError('Invalid exact rational') from exc
    if not result.is_finite: raise ValueError('Finite rational required')
    return result

def tex(value):
    return sp.latex(rational(value)).replace('- ', '-')

def term(a,var):
    return var if a==1 else '-'+var if a==-1 else tex(a)+var

def linear(a,b,var):
    return term(a,var)+('+'+tex(b) if b>0 else tex(b) if b<0 else '')

def normalize(parameters):
    if isinstance(parameters,(tuple,list)):
        if len(parameters)!=3: raise ValueError('Expected [a,b,c]')
        parameters=dict(zip(('a','b','c'),parameters))
    if not isinstance(parameters,dict) or set(parameters)-{'a','b','c','var'} or not {'a','b','c'}<=set(parameters):
        raise ValueError('Parameters must contain exactly a,b,c and optional var')
    var=parameters.get('var','p')
    if var not in ('p','k','s','q'): raise ValueError('Unsupported parameter name')
    return {**{key:rational(parameters[key]) for key in ('a','b','c')},'var':var}


def workload(template,p,profile):
    """All explicit calls and all samplers use these REDUCED-object guards."""
    a,b,c=(p[k] for k in ('a','b','c'))
    if a==0: raise ValueError('The parameter must be determined uniquely')
    r=(c-b)/a
    if template=='scale_radio':
        if not (a.q==c.q==1 and 2<=abs(a)<=8 and b==0 and 2<=abs(c)<=16):
            raise ValueError('Easy scale: integer |a|=2..8, b=0, integer |c|=2..16')
        if profile in ('observed_ratio','observed_scale') and not (a>0 and c>0):
            raise ValueError('Positive observed profile requires positive a,c')
        if profile=='observed_signed' and not (a<0 and c>0):
            raise ValueError('Signed observed profile requires negative a and positive c')
    elif template=='shift_radio':
        if not (a==1 and b.q==c.q==1 and 2<=abs(b)<=8 and 2<=abs(c)<=12 and r!=0):
            raise ValueError('Easy shift: a=1, integer |b|=2..8, |c|=2..12, nonzero result')
        if profile=='observed_shift' and not (b<0 and c>0):
            raise ValueError('Observed shift profile requires b<0,c>0')
    elif template=='affine_blank':
        if not (a.q==b.q==c.q==1 and 2<=abs(a)<=8 and 1<=abs(b)<=9 and 1<=abs(c)<=24
                and 0<abs(r)<=12 and r.q<=4 and abs(c-b)<=48
                and math.gcd(int(a),int(b),int(c))==1):
            raise ValueError('Moderate: primitive integer coefficient triple, nonunit a, nonzero b,c, bounded rational result')
    elif template=='fraction_affine_blank':
        if not (all(2<=v.q<=5 and 1<=abs(v.p)<=12 and abs(v)<=4 for v in (a,b,c))
                and b.q!=c.q and 2<=(c-b).q<=10 and abs((c-b).p)<=24
                and 2<=r.q<=6 and 1<=abs(r.p)<=12):
            raise ValueError('Hard: three noninteger reduced coefficients, unequal offset/RHS denominators; bounded noninteger intermediate/result')
    else: raise ValueError('Unknown template')
    return r


def wrong_values(profile,a,b,c,r):
    operations={
        'reciprocal':lambda:1/r,'negative_reciprocal':lambda:-1/r,
        'reverse_sign':lambda:-r,'omit_division':lambda:c,
        'multiply_instead_of_divide':lambda:a*c,
        'reverse_shift':lambda:c+b,'divide_by_shift':lambda:c/(-b),
        'invert_shift_ratio':lambda:(-b)/c,'omit_shift':lambda:c,
        'unit_constraint':lambda:sp.Integer(1),'zero_constraint':lambda:sp.Integer(0),
        'coefficient_as_answer':lambda:a,'divide_coefficient_by_answer':lambda:a/r,
        'negated_coefficient':lambda:-a,'shift_magnitude_as_answer':lambda:-b,
    }
    return [sp.cancel(operations[label]()) for label in PROFILES[profile][1]]


def bank(template,profile,p):
    r=workload(template,p,profile) # Correct value derived before wrong operations.
    values=[r]+wrong_values(profile,p['a'],p['b'],p['c'],r)
    if any(not v.is_finite for v in values) or len(set(values))!=len(values):
        raise ValueError('Whole selected bank rejected: undefined or equivalent options')
    return values

# ---------------- Easy: one inverse operation (observed scale/shift layouts).
def sample_easy(template,profile,rng):
    if template=='scale_radio':
        signs=[1] if profile in ('observed_ratio','observed_scale') else [-1] if profile=='observed_signed' else [-1,1]
        return {'a':rng.choice(signs)*rng.randint(2,8),'b':0,
                'c':rng.choice([1] if profile.startswith('observed_') else [-1,1])*rng.randint(2,16),'var':rng.choice(('p','k','s','q'))}
    return {'a':1,'b':rng.choice([-1] if profile=='observed_shift' else [-1,1])*rng.randint(2,8),
            'c':rng.choice([1] if profile=='observed_shift' else [-1,1])*rng.randint(2,12),'var':rng.choice(('p','k','s','q'))}

# ---------------- Moderate: same coefficient equality; two inverse operations.
def sample_moderate(rng):
    return {'a':rng.choice((-1,1))*rng.randint(2,8),'b':rng.choice((-1,1))*rng.randint(1,9),
            'c':rng.choice((-1,1))*rng.randint(1,24),'var':rng.choice(('p','k','s','q'))}

# ---------------- Hard (authored): identical method with reduced rational inputs.
# Candidate lists contain REDUCED values once; unreduced aliases add no tasks.
HARD_COEFFICIENTS=tuple(sorted({sp.Rational(n,d) for n in range(-12,13) if n for d in range(2,6)
                              if 2<=sp.Rational(n,d).q<=5 and abs(sp.Rational(n,d))<=4}))
def sample_hard(rng):
    return {**{k:rng.choice(HARD_COEFFICIENTS) for k in ('a','b','c')},'var':rng.choice(('p','k','s','q'))}


def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    # Source-ID/profile aliases select recipes, never a literal source payload.
    if template in CASES:
        template,source_profile,_=CASES[template]
        profile=profile or source_profile
    profile=PROFILE_ALIASES.get(profile,profile)
    if template is None and profile in PROFILES and PROFILES[profile][0] is not None:
        template=PROFILES[profile][0]
    template=template or rng.choice([k for k,v in TEMPLATES.items() if v['level']==level])
    if template not in TEMPLATES or TEMPLATES[template]['level']!=level: raise ValueError('Template/difficulty mismatch')
    kind=TEMPLATES[template]['field']
    if field_type is not None and field_type.removeprefix(':answer-field.type/')!=kind:
        raise ValueError('Unsupported field type for this template')
    profile=profile or {'scale_radio':'authored_scale','shift_radio':'authored_shift'}.get(template,'blank')
    if profile not in PROFILES or (PROFILES[profile][0] not in (None,template)) or (kind=='blank')!=(profile=='blank'):
        raise ValueError('Ineligible profile')
    if parameters is None:
        for _ in range(2000):
            proposal=sample_easy(template,profile,rng) if level=='easy' else sample_moderate(rng) if level=='moderate' else sample_hard(rng)
            p=normalize(proposal)
            try: values=bank(template,profile,p)
            except ValueError: continue
            break
        else: raise ValueError('Bounded complete-bank search exhausted')
    else:
        p=normalize(parameters)
        values=bank(template,profile,p) # Never silently repair explicit inputs.
    a,b,c,var=(p[k] for k in ('a','b','c','var'))
    r=values[0]
    coeff=linear(a,b,var)
    lhs=('('+coeff+')' if b else coeff)+'x'
    prompt='Consider the equation\n\n$$\n'+lhs+'='+tex(c)+'x\n$$\n\nwhere $'+var+'$ is a constant. Given that this equation has infinitely many solutions, what is the value of $'+var+'?$'
    key='field-1' if kind=='blank' else 'selection'
    if kind=='blank': prompt+='\n\n$'+var+'=$\n{{field-1}}'
    ending=(r'\begin{aligned}'+term(a,var)+' & ='+tex(c-b)+r' \\ '+var+' & ='+tex(r)+r'.\end{aligned}'
            if template in ('affine_blank','fraction_affine_blank') else var+'='+tex(r)+'.')
    worked='Suppose we have an equation of the form\n\n$$\nax=bx\n$$\n\nwhere $a$ and $b$ are constants. If $a=b,$ then the equation has infinitely many solutions.\n\nNotice that this equation is in the form $ax=bx.$ In this case, \n\n$$\na='+coeff+r',\,b='+tex(c)+'.\n$$\n\nTherefore, the equation has infinitely many solutions if\n\n$$\n'+coeff+'='+tex(c)+'.\n$$\n\nSolving this for $'+var+',$ we get\n\n$$\n'+ending+'\n$$'
    # Content includes actual prompt, fixed solution and full unordered bank.
    # Profile aliases, source IDs, seed, option order and parameter spelling do not.
    fp=digest(['one-parameter-homogeneous-identity',str(b/a),str(c/a)])
    content={'version':VERSION,'problem':prompt,'solution':worked,'level':level,'field':kind,
             'key':key,'values':sorted(tex(v) for v in values),'correct':tex(r),'domain':'real'}
    qid=ident(content);fid=ident([qid,'field',key])
    choices=[{':answer/id':ident([fid,tex(v)]),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in values]
    correct=choices[0][':answer/id'];rng.shuffle(choices)
    field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
           ':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
            'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':worked,
                        ':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]},
            'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'profile_origin':PROFILES[profile][2],
                          'parameters':{k:str(v) if k!='var' else v for k,v in p.items()},'source':SOURCE,
                          'source_ids':TEMPLATES[template]['sources'],'authored_level':level=='hard',
                          'evidence_only':profile.startswith('observed_'),'eligible_for_learning':not profile.startswith('observed_'),
                          'domain':'x and parameter real','recipes':['correct']+list(PROFILES[profile][1]),
                          'mathematical_fingerprint':fp,'content_fingerprint':digest(content),'sympy':sp.__version__}}


def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    options='\n\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']) if f[':answer-field/type'].endswith('/radio') else ''
    return q[':question/problem']+ ('\n\n'+options if options else '')+'\n\nWorked solution:\n\n'+q[':question/worked-solution']

def batch(level,count,seed,template=None,profile=None):
    if count<1: raise ValueError('Positive count required')
    records=[];seen=set()
    for i in range(max(200,count*100)):
        rec=generate(level,seed+i,template=template,profile=profile)
        fp=rec['generation']['mathematical_fingerprint']
        if fp not in seen: records.append(rec);seen.add(fp)
        if len(records)==count: return records
    raise ValueError('Finite bounded mathematical variants exhausted')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='easy')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['json','markdown'],default='json')
    parser.add_argument('--template');parser.add_argument('--profile')
    args=parser.parse_args();records=[]
    for level in ('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,):
        records.extend(batch(level,args.count,args.seed,args.template,args.profile))
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
