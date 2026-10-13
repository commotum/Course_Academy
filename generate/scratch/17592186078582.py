#!/usr/bin/env python3
"""Identify inhibited decay: source-faithful, parameterized radio generators.

Math capture basis 1356; see sibling evidence directory for seven original
banks, four-stage extraction, native grading, and the unrated-source repair.
Easy recognizes factored linear form; moderate factors expanded linear form;
hard also checks the initial value is above the equilibrium. No solving ODEs,
application modeling, new branches, plots, EDB transactions, or answer lookups.
All complete banks have explicit mathematical operation recipes. Formatting
profiles preserve observed TeX and source wording without returning payloads.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import uuid
from decimal import Decimal
from pathlib import Path
import sympy as sp

KP_ID = 17592186078582
KP_UUID = '0709c667-bc10-5bd5-a383-3fd6ca332361'
TITLE = 'Identifying Inhibited Decay Equations and Initial Value Problems'
VERSION = '1.0.0'
SOURCE = {'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES = {'factored':'easy','expanded':'moderate','ivp':'hard'}
# A profile is a WHOLE observed bank plus its notation. q-105893 contributes a
# spacing/power variant of expanded, not a new mathematical skill or label.
BANK_PROFILES = {
    'factored_signs': {'template':'factored','sources':['q-105898'], 'recipes':['wrong_shift','quadratic_reversed','reversed_difference','quadratic_wrong_shift','correct']},
    'factored_powers': {'template':'factored','sources':['q-106647'], 'recipes':['quadratic_wrong_shift_negative','cubic','reversed_difference','correct','square_difference']},
    'expanded': {'template':'expanded','sources':['q-106651','q-106654'],'recipes':['square','quadratic','square_reversed','correct','positive_slope']},
    'expanded_spaced': {'template':'expanded','sources':['q-105893'],'recipes':['quadratic','square_reversed','square','positive_slope','correct']},
    'ivp_integer': {'template':'ivp','sources':['q-105890'],'recipes':['below','correct','quadratic_below','quadratic_positive','positive_slope']},
    'ivp_decimal_grouped': {'template':'ivp','sources':['q-15591'],'recipes':['quadratic_below','correct','quadratic_positive','positive_slope','below']},
}
OBSERVED_PARAMETERS = {
    'factored_signs':[{'a':'20','k':'80'}], 'factored_powers':[{'a':'9','k':'5'}],
    'expanded':[{'a':'8','k':'22'},{'a':'30','k':'28'}], 'expanded_spaced':[{'a':'40','k':'20'}],
    'ivp_integer':[{'a':'500','k':'2','below':'400','above':'600'}],
    'ivp_decimal_grouped':[{'a':'1500','k':'0.002','below':'1000','above':'3000'}],
}
Y=sp.Symbol('y',real=True)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def number(value, grouped=False):
    r=sp.Rational(str(value))
    if r.q == 1:
        return format(int(r),',').replace(',',r'\,') if grouped else str(r)
    # Source coefficients are terminating decimals. Reject unsupported rationals.
    den=int(r.q)
    for prime in (2,5):
        while den%prime == 0: den//=prime
    if den != 1: raise ValueError('Use exact terminating decimal coefficients')
    return format(Decimal(int(r.p))/Decimal(int(r.q)),'f').rstrip('0').rstrip('.')

def checked_parameters(template,p):
    expected={'a','k','below','above'} if template=='ivp' else {'a','k'}
    if set(p)!=expected: raise ValueError(f'Parameters must have exactly {sorted(expected)}')
    vals={key:sp.Rational(str(value)) for key,value in p.items()}
    if vals['k']<=0 or vals['a']<=0 or vals['a'].q!=1: raise ValueError('Require positive k and positive integer a')
    number(vals['k'])
    if template!='ivp' and vals['k'].q!=1: raise ValueError('Equation profiles use positive integer k')
    if template=='ivp' and not (0<vals['below']<vals['a']<vals['above']): raise ValueError('Require 0 < below < a < above')
    if template=='ivp' and any(vals[x].q!=1 for x in ('below','above')): raise ValueError('Initial values must be integers')
    return vals

def sample(template,rng,profile):
    if template=='ivp':
        a=rng.choice([20,40,75,100,250,500,750,1000,1500,2000])
        return {'a':a,'k':rng.choice(['0.001','0.002','0.005','0.01','0.025','0.1','0.25','0.5','1','2','5']),
                'below':a-rng.choice([1,2,3,4])*max(1,a//5),'above':a+rng.choice([1,2,3,4])*max(1,a//2)}
    return {'a':rng.randint(2,100),'k':rng.randint(2,80)}

def bank_math(template,p,recipes):
    """Exact complete objects: (ODE RHS, initial value or None).

    Linear negative slope AND root a is the definition being assessed. For IVPs
    the initial value must exceed that root. Extra y/y² factors change the model.
    """
    a,k=p['a'],p['k']; c=k*a
    if template=='factored':
        mapping={'correct':-k*(Y-a),'wrong_shift':k*(Y+a),'quadratic_reversed':-k*Y*(a-Y),
                 'reversed_difference':-k*(a-Y),'quadratic_wrong_shift':k*Y*(Y+a),
                 'quadratic_wrong_shift_negative':-k*Y*(Y+a),'cubic':-k*Y**2*(Y-a),'square_difference':-k*(Y**2-a)}
        return [(mapping[r],None) for r in recipes]
    if template=='expanded':
        mapping={'correct':c-k*Y,'square':c-k*Y**2,'quadratic':c*Y-k*Y**2,'square_reversed':k*Y**2-c,'positive_slope':c+k*Y}
        return [(mapping[r],None) for r in recipes]
    mapping={'correct':(-k*(Y-a),p['above']),'below':(-k*(Y-a),p['below']),
             'quadratic_below':(-k*Y*(Y-a),p['below']),'quadratic_positive':(k*Y*(Y-a),p['above']),
             'positive_slope':(k*(Y-a),p['above'])}
    return [mapping[r] for r in recipes]

def qualifies(rhs,initial,a):
    poly=sp.Poly(sp.expand(rhs),Y)
    return poly.degree()==1 and poly.coeff_monomial(Y)<0 and sp.simplify(rhs.subs(Y,a))==0 and (initial is None or initial>a)

def render_bank(template,p,profile):
    """Render recipes independently of source numbers; all values derive from p."""
    grouped=profile=='ivp_decimal_grouped'
    a,k=number(p['a'],grouped),number(p['k'])
    c=number(p['a']*p['k'])
    eq=r'\frac{dy}{dt}'
    power=r'y^{2}' if profile=='expanded_spaced' else r'{y}^{2}'
    if template=='factored':
        mapping={'correct':f'-{k}(y-{a})','wrong_shift':f'{k}(y+{a})','quadratic_reversed':f'-{k}y({a}-y)',
                 'reversed_difference':f'-{k}({a}-y)','quadratic_wrong_shift':f'{k}y(y+{a})',
                 'quadratic_wrong_shift_negative':f'-{k}y(y+{a})','cubic':f'-{k}{{y}}^{{2}}(y-{a})','square_difference':f'-{k}({{y}}^{{2}}-{a})'}
    elif template=='expanded':
        gap=' ' if profile=='expanded_spaced' else ''
        mapping={'correct':f'{c}{gap}-{gap}{k}y','square':f'{c}{gap}-{gap}{k}{power}',
                 'quadratic':f'{c}y{gap}-{gap}{k}{power}','square_reversed':f'{k}{power}{gap}-{gap}{c}',
                 'positive_slope':f'{c}{gap}+{gap}{k}y'}
        eq+=gap
    else:
        high,low=number(p['above'],grouped),number(p['below'],grouped)
        mapping={'correct':f'-{k}(y-{a}),\\,y(0)={high}','below':f'-{k}(y-{a}),\\,y(0)={low}',
                 'quadratic_below':f'-{k}y(y-{a}),\\,y(0)={low}','quadratic_positive':f'{k}y(y-{a}),\\,y(0)={high}',
                 'positive_slope':f'{k}(y-{a}),\\,y(0)={high}'}
    equals='= ' if profile=='expanded_spaced' else '='
    return [eq+equals+mapping[r] for r in BANK_PROFILES[profile]['recipes']]

def block(s): return '$$\n'+s+'\n$$'

def prompt(template,p,profile):
    if template=='ivp': return 'Which of the following initial value problems is an inhibited decay problem?'
    a=number(p['a'])
    if profile=='expanded_spaced': return f'Given that $y > {a}$ and $t > 0$, which of the following is an inhibited decay equation?'
    return f'Given that $y>{a}$ and $t>0,$ which of the following is an inhibited decay equation?'

def solution(template,p,profile):
    a,k=number(p['a'],profile=='ivp_decimal_grouped'),number(p['k'])
    factored=rf'\frac{{dy}}{{dt}}=-{k}(y-{a})'
    if template=='ivp':
        high,low=number(p['above'],profile=='ivp_decimal_grouped'),number(p['below'],profile=='ivp_decimal_grouped')
        return ('An inhibited decay initial value problem has the form\n\n'+block(r'\frac{dy}{dt}=-k(y-a),\,y(0)={y}_{0}')+
            '\n\nwhere $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$\n\nFrom the given options, the only inhibited decay problem is\n\n'+
            block(factored+rf',\,y(0)={high}.')+f'\n\nIn this case, $k={k},a={a},$ and ${{y}}_{{0}}={high}.$ Notice that ${{y}}_{{0}}>a,$ which is required for inhibited decay. \n\n'+
            'The other options do not represent inhibited decay. In particular, the initial value problem\n\n'+block(factored+rf',\,y(0)={low},')+
            f'\n\ndoes *not* represent inhibited decay model because ${{y}}_{{0}}={low}<a={a}.$')
    correct=factored if template=='factored' else rf'\frac{{dy}}{{dt}}={number(p["a"]*p["k"])}-{k}y'
    out='An inhibited decay equation has the form\n\n'+block(r'\frac{dy}{dt}=-k(y-a),')+'\n\nwhere $k>0$ is a constant of proportionality, and $y>a$ for all $t>0.$\n\nFrom the given options, the only inhibited decay equation is\n\n'+block(correct+'.')
    if template=='expanded': out+="\n\nTo see this, let's factor the right-hand side of the equation. This gives,\n\n"+block(factored+'.')
    return out+f'\n\nIn this case, the constant of proportionality is $k={k},$ and $a={a}.$ Note that for inhibited decay, we must have $y>{a}$ for all $t>0.$'

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in TEMPLATES.values(): raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only observed radio field is supported')
    if profile is not None and profile not in BANK_PROFILES: raise ValueError('Unknown bank profile')
    template=template or (BANK_PROFILES[profile]['template'] if profile else next(k for k,v in TEMPLATES.items() if v==level))
    if TEMPLATES.get(template)!=level: raise ValueError('Template is not available at this difficulty')
    profiles=[name for name,spec in BANK_PROFILES.items() if spec['template']==template]
    if profile and profile not in profiles: raise ValueError('Incompatible profile')
    rng=random.Random(seed)
    # Explicit parameters preserve profile selection independently of seed.
    normalized=checked_parameters(template,parameters) if parameters is not None else None
    picker=random.Random(json.dumps({key:number(value) for key,value in normalized.items()},sort_keys=True)) if normalized is not None else rng
    profile=profile or picker.choice(profiles)
    p=normalized if normalized is not None else checked_parameters(template,sample(template,rng,profile))
    recipes=BANK_PROFILES[profile]['recipes']
    maths=bank_math(template,p,recipes)
    if len(maths)!=5 or any(sp.Poly(r1-r2,Y).is_zero and i1==i2 for j,(r1,i1) in enumerate(maths) for r2,i2 in maths[:j]): raise ValueError('Reject entire duplicate bank')
    corrects=[i for i,(rhs,initial) in enumerate(maths) if qualifies(rhs,initial,p['a'])]
    if len(corrects)!=1 or recipes[corrects[0]]!='correct': raise ValueError('Ambiguous/invalid bank')
    values=render_bank(template,p,profile)
    problem,worked=prompt(template,p,profile),solution(template,p,profile)
    serial={key:number(value) for key,value in p.items()}
    param_key=digest({'template':template,'parameters':serial,'domain':'t>0,y>a'})
    content_key=digest({'parameter_fingerprint':param_key,'prompt':problem,'solution':worked,'bank':sorted(values)})
    qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{KP_UUID}/{VERSION}/{content_key}')
    fid=uuid.uuid5(qid,'selection')
    answers=[{':answer/id':str(uuid.uuid5(fid,'math:'+value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct_id=answers[corrects[0]][':answer/id']
    recipe_map={ans[':answer/id']:recipe for ans,recipe in zip(answers,recipes)}
    rng.shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
        'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':worked,
            ':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},
        'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':serial,'bank_profile':profile,'bank_origin':'observed',
            'parameter_fingerprint':param_key,'content_fingerprint':content_key,'answer_shape':'complete_ode_and_initial_value' if template=='ivp' else 'complete_ode',
            'source_analysis':{**SOURCE,'question_ids':BANK_PROFILES[profile]['sources']},'domain':'t>0; y>a; k>0','plot_rating':'none','plot_assets':{},
            'recipes':recipe_map,'parameter_extension':serial not in OBSERVED_PARAMETERS[profile],'authored_extension':profile=='expanded_spaced',
            'difficulty_origin':'authored supported assignment for unrated source' if profile=='expanded_spaced' else 'observed',
            'solution_template_origin':'authored reconstruction from the two rated expanded sources' if profile=='expanded_spaced' else 'observed',
            'sampling_policy':'positive integer equilibrium; equation integer rates; IVP exact terminating rates and 0<below<a<above'}}

# EASY: already-factored recognition; no additional algebra branches.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: recognize by factoring a negative linear coefficient.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: check the same model and initial inequality, without solving it.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
    q,g=record['question'],record['generation']; f=q[':question/answer-fields'][0]
    out=[f"## {q[':question/difficulty'].split('/')[-1]} — {g['bank_profile']}",q[':question/problem'],'']
    for a in f[':answer-field/choices']:
        mark=' ✓' if a[':answer/id']==f[':answer-field/correct'][1] else ''
        out.append('- $'+a[':answer/value']+'$'+mark)
    return '\n\n'.join(out)+ '\n\n'+q[':question/worked-solution']

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    parser.add_argument('--seed',type=int,default=0); parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['markdown','json'],default='markdown')
    parser.add_argument('--template',choices=list(TEMPLATES)); parser.add_argument('--profile',choices=list(BANK_PROFILES))
    args=parser.parse_args()
    if args.count<1 or args.difficulty=='all' and (args.template or args.profile): parser.error('Use positive count and one difficulty with template/profile')
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (list(TEMPLATES.values()) if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
