#!/usr/bin/env python3
"""Seeded easy open-interval conversions, source basis 4466.

Retains the supplied draft's four complete source banks and solution masks.
Only easy is supported; see instructional-account.md for scope and evidence.
No assets are generated, no database is accessed, and runtime is relocatable.
Private _generate with raw_* profiles exists only for evidence replay.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, re, sys, uuid
from functools import lru_cache
import sympy as sp
from math_format import checked_math_content, normalize_prose, normalize_tex

KP_ID=17592186059826
KP_UUID='74f45f69-d8e7-5e79-a1ec-38d8912cbc19'
TITLE='Converting Between Intervals and Inequalities: Open Intervals'
VERSION='open-interval-4466-v3'
SOURCE={'database':'math','basis':4466,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES=('inequality_spaced','inequality_compact','interval_to_inequality')
BANKS={'spaced_ray':('inequality_spaced','q-102204'),'compact_reflection':('inequality_compact','q-1256'),'compact_ray':('inequality_compact','q-154704'),'membership':('interval_to_inequality','q-59294')}
PROFILES=tuple(BANKS)+tuple('raw_'+p for p in BANKS)
ROOT_RADICANDS=(2,3,5,6,7,10,11,13)
ORIGINAL_PARAMETERS={'spaced_ray':('3','7'),'membership':('3','4'),
                     'compact_reflection':('-3','-1'),'compact_ray':('-sqrt(2)','sqrt(2)')}

# Shared exact endpoint/identity helpers. Strings are restricted complete components.
def endpoint(value):
    if isinstance(value,bool) or not isinstance(value,(str,int,sp.Expr)): raise ValueError('use an exact rational or simple signed sqrt(n) endpoint')
    token=str(value).replace(' ','')
    if re.fullmatch(r'[+-]?\d+(?:/\d+)?',token):
        try: out=sp.Rational(token)
        except (ValueError,ZeroDivisionError,TypeError): raise ValueError('invalid rational endpoint') from None
    elif re.fullmatch(r'[+-]?sqrt\(\d+\)',token):
        sign=-1 if token.startswith('-') else 1
        out=sign*sp.sqrt(int(re.search(r'\d+',token)[0]))
    else: raise ValueError('unsupported endpoint component')
    if out.is_real is not True or out.is_finite is not True: raise ValueError('finite real endpoints required')
    return out

def tex(value):
    value=endpoint(value)
    return "-"+sp.latex(-value) if value.is_negative else sp.latex(value)

def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(*parts): return str(uuid.uuid5(uuid.UUID(KP_UUID),'|'.join(parts)))
def base_profile(profile): return profile.removeprefix('raw_')

@lru_cache(maxsize=16)
def catalog(level,profile):
    profile=base_profile(profile)
    if profile not in BANKS: raise ValueError('unknown bank')
    if level=='easy':
        integer_pairs=list(itertools.combinations(map(sp.Integer,range(-12,13)),2))
        if profile=='compact_ray': pairs=[(-sp.sqrt(n),sp.sqrt(n)) for n in ROOT_RADICANDS]
        elif profile=='compact_reflection': pairs=[(a,b) for a,b in integer_pairs if a+b!=0]
        else: pairs=integer_pairs
    else: raise ValueError('unknown difficulty')
    return tuple((str(a),str(b)) for a,b in pairs)

# Whole source-derived solution masks, retaining whitespace, prose, and row roles.
def inequality_solution(a,b,v):
    return ('Every inequality can be expressed as an interval. We use the following notations:\n\n'
      '- Parentheses $()$ if the endpoints are *not* included.\n\n'
      '- Brackets $[]$ if the endpoints *are* included.\n\n'
      'Our inequality contains only "less than" symbols. So, the endpoints $'+a+'$ and $'+b+'$ are *not* included. \n\n$$\n'+a+r'\,\,<\,\,'+v+r'\,\,<\,\,'+b+
      '\n$$\n\nTherefore, we can express our inequality in interval notation as follows:\n\n$$\n('+a+','+b+
      ')\n$$\n\nMore formally, we can also write\n\n$$\n'+v+r'\in ('+a+','+b+').\n$$')

def membership_solution(a,b,v):
    # Canonical e-10785 at basis 4466, including the two spaced color relation masks.
    return ('Every interval can be expressed as an inequality. We use the following notations:\n\n'
      r'- Parentheses ${\color{red}{(}}\phantom{0} \phantom{0}{\color{red}{)}}$ to indicate that the endpoints are *not* included.'+'\n\n'
      r'- Brackets ${\color{blue}{[}}\phantom{0} \phantom{0}{\color{blue}{]}}$ to indicate that the endpoints *are* included.'+
      '\n\nOur interval contains only parentheses. So, the endpoints are *not* included. \n\n$$\n'+v+r'\in {\color{red}{(}}'+a+', '+b+r'{\color{red}{)}}'+
      '\n$$\n\nTherefore, our interval can be expressed as the following inequality:\n\n$$\n'+a+r' \,\,{\color{red}{<      }}\,\,      '+v+r'  \,\,{\color{red}{<      }}\,\,      '+b+'\n$$')

# Exact complete observed banks; spelling/layout are separate from represented sets.
def build_bank(profile,a,b,v):
    p=base_profile(profile); at,bt=tex(a),tex(b)
    opened=sp.Interval.open(a,b)
    if p=='membership':
        return [('left_closed',rf'{at} \le {v} < {bt}','math',sp.Interval(a,b,right_open=True)),
                ('open',f'{at} < {v} < {bt}','math',opened),
                ('right_closed',rf'{at} < {v} \le {bt}','math',sp.Interval(a,b,left_open=True)),
                ('outside',f'${v} < {at}$ or ${v} > {bt}$','text',sp.Union(sp.Interval.open(-sp.oo,a),sp.Interval.open(b,sp.oo))),
                ('both_closed',rf'{at} \le {v} \le {bt}','math',sp.Interval(a,b))]
    join=', ' if p=='spaced_ray' else ','
    items=[('open','('+at+join+bt+')','math',opened),
           ('both_closed','['+at+join+bt+']','math',sp.Interval(a,b)),
           ('right_closed','('+at+join+bt+']','math',sp.Interval(a,b,left_open=True)),
           ('left_closed','['+at+join+bt+')','math',sp.Interval(a,b,right_open=True))]
    if p=='compact_reflection':
        items.append(('reflect','('+tex(-b)+','+tex(-a)+')','math',sp.Interval.open(-b,-a)))
    else:
        inf='- ∞, ' if p=='spaced_ray' else r'-\infty ,'
        items.append(('omit_lower','('+inf+bt+')','math',sp.Interval.open(-sp.oo,b)))
    return items

def _generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level != 'easy': raise ValueError('unsupported difficulty: only source-justified easy is supported')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('only the observed radio contract is supported')
    if template is not None and template not in TEMPLATES: raise ValueError('unknown template')
    if profile is not None and profile not in PROFILES: raise ValueError('unknown profile')
    rng=random.Random(seed)
    supplied_pair=None
    if parameters is not None:
        if not isinstance(parameters,dict) or set(parameters)-{'a','b','variable'} or not {'a','b'}<=set(parameters): raise ValueError('parameters require complete a,b and optional variable slots')
        supplied_pair=(str(endpoint(parameters['a'])),str(endpoint(parameters['b'])))
    # Choose a whole compatible bank before sampled endpoints. Supplied endpoints
    # may filter whole-bank eligibility; they are never changed or resampled.
    if profile is None:
        eligible=[p for p,(t,_) in BANKS.items() if (template is None or t==template) and (supplied_pair is None or supplied_pair in catalog(level,p))]
        if not eligible: raise ValueError('no complete eligible profile for the supplied endpoints/template')
        profile=rng.choice(eligible)
    p=base_profile(profile); required_template,source_id=BANKS[p]
    if template is not None and template!=required_template: raise ValueError('profile/template mismatch')
    template=required_template; raw=profile.startswith('raw_')
    pool=catalog(level,p)
    if parameters is None:
        a,b=rng.choice(pool); parameters={'a':a,'b':b,'variable':'x'}
    if not isinstance(parameters,dict) or set(parameters)-{'a','b','variable'} or not {'a','b'}<=set(parameters): raise ValueError('parameters require complete a,b and optional variable slots')
    a,b=endpoint(parameters['a']),endpoint(parameters['b']); v=parameters.get('variable','x')
    if v not in ('x','y','t','z'): raise ValueError('unsupported variable alias')
    if (str(a),str(b)) not in pool: raise ValueError('parameters outside level/profile domain; no silent resampling')
    at,bt=tex(a),tex(b)
    if template=='inequality_spaced': prompt=f'The inequality ${at} < {v} < {bt}$ can be expressed in interval notation as'
    elif template=='inequality_compact': prompt=f'The inequality ${at}<{v}<{bt}$ can be expressed in interval notation as'
    else: prompt=f'Which inequality corresponds to the interval ${v} ∈ ({at}, {bt})$?'
    prompt=normalize_prose(prompt)
    bank=[(recipe, normalize_tex(value) if typ=='math' else normalize_prose(value), typ, obj)
          for recipe,value,typ,obj in build_bank(p,a,b,v)]
    answer_set=sp.Interval.open(a,b)
    if len(bank)!=5 or sum(obj==answer_set for _,_,_,obj in bank)!=1 or any(lhs[3]==rhs[3] for lhs,rhs in itertools.combinations(bank,2)):
        raise ValueError('reject entire ambiguous/invalid complete bank')
    sol=membership_solution(at,bt,v) if template=='interval_to_inequality' else inequality_solution(at,bt,v)
    sol=normalize_prose(sol)
    omitted=raw and p in ('spaced_ray','membership')
    stored_level=None if omitted else ('easy' if raw else level)
    full_identity={'version':VERSION,'difficulty':stored_level,'prompt':prompt,'solution':None if omitted else sol,'bank':sorted((val,typ) for _,val,typ,_ in bank),'correct':None if omitted else next(val for recipe,val,_,_ in bank if recipe=='open')}
    content=digest(full_identity); qid=uid('question',content); fid=uid(qid,'selection')
    answers=[{':answer/id':uid(fid,typ,val),':answer/type':':answer.type/'+typ,':answer/value':val} for _,val,typ,_ in bank]
    correct=next(answer[':answer/id'] for answer in answers if answer[':answer/value']==full_identity['correct']) if not omitted else None
    rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not omitted:
        question[':question/difficulty']=':question.difficulty/'+stored_level
        question[':question/worked-solution']=sol
        field[':answer-field/correct']=[':answer/id',correct]
    direction='interval_to_inequality' if template=='interval_to_inequality' else 'inequality_to_interval'
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
      'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':template,'profile':profile,'bank_profile':profile,'parameters':{'a':str(a),'b':str(b),'variable':v},'difficulty':level,'difficulty_status':'omitted original' if omitted else ('observed easy' if raw or level=='easy' and p in ('compact_reflection','compact_ray') else 'authored policy'),
        'bank_origin':'observed complete structural recipes','authored_extension':not raw and (p in ('spaced_ray','membership') or (str(a),str(b))!=ORIGINAL_PARAMETERS[p]),'evidence_only':raw,'eligible_for_learning':not raw,'source':SOURCE,'source_ids':[source_id],'recipes':[recipe for recipe,_,_,_ in bank],
        'mathematical_fingerprint':digest({'direction':direction,'a':str(a),'b':str(b),'endpoint_reading_policy':level}),
        'parameter_fingerprint':digest({'direction':direction,'a':str(a),'b':str(b),'endpoint_reading_policy':level}),
        'content_fingerprint':content,'solution_origin':'canonical e-10785 mask' if direction=='interval_to_inequality' else 'q-1256/q-154704 shared operative mask',
        'repairs':[] if raw or p in ('compact_reflection','compact_ray') else ['missing correct ref independently derived','missing practice solution supplied from original/canonical mask','missing difficulty assigned by authored easy policy' if level=='easy' else 'missing difficulty assigned by authored '+level+' policy'],
        'domain':{'finite_ordered_endpoints':True,'both_endpoints_excluded':True,'catalog_size':len(pool)},'plots':'none'}}

@checked_math_content
def generate(level='easy',seed=0,**kwargs):
    """Public served record: complete fields only, validated canonical math."""
    if (kwargs.get('profile') or '').startswith('raw_'):
        raise ValueError('raw source evidence is not a served profile')
    return _generate(level,seed,**kwargs)

def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)

def markdown(record):
    q=record['question']; f=q[':question/answer-fields'][0]; rows=[q[':question/problem'],'']
    for letter,a in zip('ABCDE',f[':answer-field/choices']): rows.append(letter+'. '+('$'+a[':answer/value']+'$' if a[':answer/type'].endswith('/math') else a[':answer/value']))
    if ':answer-field/correct' in f: rows+=['','Correct: '+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])]
    if ':question/worked-solution' in q: rows+=['',q[':question/worked-solution']]
    return '\n'.join(rows)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=('easy',),default='easy'); parser.add_argument('--seed',type=int,default=0); parser.add_argument('--count',type=int,default=1); parser.add_argument('--format',choices=('markdown','json'),default='markdown'); parser.add_argument('--template',choices=TEMPLATES); parser.add_argument('--profile',choices=tuple(BANKS))
    args=parser.parse_args()
    if args.count<1: parser.error('count must be positive')
    levels=(args.difficulty,)
    try: records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    except ValueError as exc: parser.error(str(exc))
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
