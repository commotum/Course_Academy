#!/usr/bin/env python3
"""Open bounded intervals ↔ strict compound inequalities, basis 1356.

Two unrated practice sources supply two complete five-option radio recipes.
Neither supplies a correct ref or solution. source_raw publicly reproduces those
missing attributes; original_bank supplies independently derived keys and authored
solutions, with the same prompt/bank. No TeX repair is needed: decoded strings
have no doubled slashes. Canonical prose/stages anchor the authored solutions.

All three difficulty policies are authored, not recovered labels. Easy: positive
integer endpoints 1..12. Moderate: signed integer endpoints -12..12, lower < 0.
Hard: two noninteger rational endpoints, reduced denominators 2..4, |value|≤6.
Every question requires exactly two excluded endpoints and no solving, union,
half-open or closed correct interval, number line, or unbounded correct interval.
The finite catalogs are documented in classification.md; variable aliases and
choice order do not increase mathematical task counts. Explicit parameters obey
exactly the same guards as sampling. No EDB writes or shared-file edits.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, uuid
from functools import lru_cache
from fractions import Fraction
import sympy as sp

KP_ID=17592186059826
KP_UUID='74f45f69-d8e7-5e79-a1ec-38d8912cbc19'
TITLE='Converting Between Intervals and Inequalities: Open Intervals'
VERSION='open-interval-v2'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
LEVELS=('easy',)
TEMPLATES=('inequality_to_interval','interval_to_inequality')
PROFILES=('original_bank','source_raw','signed_source','surd_source')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
OPENING=(r'Every interval can be expressed as an inequality. We use the following notations:'+'\n\n'
 r'- Parentheses ${\color{red}{(}}\phantom{0} \phantom{0}{\color{red}{)}}$ to indicate that the endpoints are *not* included.'+'\n'
 r'- Brackets ${\color{blue}{[}}\phantom{0} \phantom{0}{\color{blue}{]}}$ to indicate that the endpoints *are* included.')

@lru_cache(maxsize=3)
def catalog(level):
    if level!='easy': raise ValueError('unsupported level: current rated sources only establish easy')
    integers=[(str(a),str(b)) for a,b in itertools.combinations(range(-12,13),2)]
    radicals=[('-sqrt('+str(n)+')','sqrt('+str(n)+')') for n in range(2,31) if all(n%(p*p) for p in range(2,int(n**.5)+1))]
    return integers+radicals

def endpoint(v):
    if isinstance(v,bool) or not isinstance(v,(str,int,Fraction)): raise ValueError('endpoint must be exact rational')
    if isinstance(v,str) and v.lstrip('-').startswith('sqrt('):
        import re
        m=re.fullmatch(r'(-?)sqrt\((\d+)\)',v)
        if not m: raise ValueError('invalid exact radical')
        n=int(m[2])
        if n<2 or n>30 or any(n%(p*p)==0 for p in range(2,int(n**.5)+1)): raise ValueError('radicand must be squarefree in 2..30')
        return (-1 if m[1] else 1)*sp.sqrt(n)
    try: return Fraction(v)
    except (ValueError,ZeroDivisionError): raise ValueError('endpoint must be exact rational') from None

def tex(v):
    v=endpoint(str(v) if isinstance(v,sp.Expr) else v)
    if isinstance(v,sp.Expr): return sp.latex(v)
    if v.denominator==1: return str(v.numerator)
    sign='-' if v<0 else ''
    return sign+rf'\frac{{{abs(v.numerator)}}}{{{v.denominator}}}'

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(*parts): return str(uuid.uuid5(uuid.UUID(KP_UUID),'|'.join(parts)))

def solution(template,a,b,v):
    if template=='interval_to_inequality':
        return OPENING+'\n\nOur interval contains only parentheses. So, the endpoints are *not* included.\n\n$$\n'+v+rf'\in {{\color{{red}}{{(}}}}'+a+', '+b+r'{\color{red}{)}}'+'\n$$\n\nTherefore, our interval can be expressed as the following inequality:\n\n$$\n'+a+r' \,\,{\color{red}{<}}\,\, '+v+r' \,\,{\color{red}{<}}\,\, '+b+'\n$$'
    return ('Every inequality can be expressed as an interval. We use the following notations:\n\n'
      r'- Parentheses ${\color{red}{(}}\phantom{0} \phantom{0}{\color{red}{)}}$ if the endpoints are *not* included.'+'\n'
      r'- Brackets ${\color{blue}{[}}\phantom{0} \phantom{0}{\color{blue}{]}}$ if the endpoints *are* included.'+
      '\n\nOur inequality contains only strict inequality symbols. So, the endpoints $'+a+'$ and $'+b+'$ are *not* included.\n\n$$\n'+a+r'\,\, {\color{red}{<}} \,\, '+v+r' \,\, {\color{red}{<}} \,\, '+b+
      '\n$$\n\nTherefore, we can express our inequality in interval notation as follows:\n\n$$\n'+r'{\color{red}{(}}'+a+', '+b+r'{\color{red}{)}}'+'\n$$\n\nMore formally, we can also write\n\n$$\n'+v+r'\in ('+a+', '+b+')\n$$')

def source_solution(a,b,v):
    return ('Every inequality can be expressed as an interval. We use the following notations:\n\n'
      '- Parentheses $()$ if the endpoints are *not* included.\n\n'
      '- Brackets $[]$ if the endpoints *are* included.\n\n'
      'Our inequality contains only "less than" symbols. So, the endpoints $'+a+'$ and $'+b+'$ are *not* included. \n\n$$\n'
      +a+r'\,\,<\,\,'+v+r'\,\,<\,\,'+b+'\n$$\n\nTherefore, we can express our inequality in interval notation as follows:\n\n$$\n('
      +a+','+b+')\n$$\n\nMore formally, we can also write\n\n$$\n'+v+r'\in ('+a+','+b+').\n$$')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    rng=random.Random(seed)
    if level not in LEVELS: raise ValueError('unsupported level: current rated sources only establish easy')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('only radio is observed/supported')
    template=template or rng.choice(TEMPLATES)
    if template not in TEMPLATES: raise ValueError('unknown template')
    profile=profile or 'original_bank'
    if profile not in PROFILES: raise ValueError('unknown profile')
    if parameters is None:
        eligible=catalog(level)
        if profile=='signed_source': eligible=[(a,b) for a,b in eligible if 'sqrt' not in a and int(b)<0]
        if profile=='surd_source': eligible=[(a,b) for a,b in eligible if 'sqrt' in a]
        a,b=rng.choice(eligible); parameters={'a':a,'b':b,'variable':'x'}
    if set(parameters)-{'a','b','variable'} or not {'a','b'}<=set(parameters): raise ValueError('parameters require a,b and optional variable')
    a,b=endpoint(parameters['a']),endpoint(parameters['b']); v=parameters.get('variable','x')
    if v not in ('x','y','t','z'): raise ValueError('unsupported variable')
    if (str(a),str(b)) not in catalog(level): raise ValueError('parameters outside authored difficulty domain')
    p={'a':str(a),'b':str(b),'variable':v}; at,bt=tex(a),tex(b)
    if profile in ('signed_source','surd_source'):
        if template!='inequality_to_interval': raise ValueError('profile only applies to inequality-to-interval')
        if profile=='signed_source' and not (isinstance(a,Fraction) and isinstance(b,Fraction) and a<b<0): raise ValueError('signed bank requires two negative integer endpoints')
        if profile=='surd_source' and not (isinstance(a,sp.Expr) and a==-b): raise ValueError('surd source requires symmetric radicals')
    if template=='inequality_to_interval':
        prompt=f'The inequality ${at} < {v} < {bt}$ can be expressed in interval notation as'
        bank=[('open',f'({at}, {bt})','math'),('omit_lower',f'(- ∞, {bt})','math'),('both_closed',f'[{at}, {bt}]','math'),('right_closed',f'({at}, {bt}]','math'),('left_closed',f'[{at}, {bt})','math')]
    else:
        prompt=f'Which inequality corresponds to the interval ${v} ∈ ({at}, {bt})$?'
        bank=[('left_closed',rf'{at} \le {v} < {bt}','math'),('open',f'{at} < {v} < {bt}','math'),('right_closed',rf'{at} < {v} \le {bt}','math'),('outside',f'${v} < {at}$ or ${v} > {bt}$','text'),('both_closed',rf'{at} \le {v} \le {bt}','math')]
    sol=solution(template,at,bt,v)
    if profile in ('signed_source','surd_source'):
        prompt=f'The inequality ${at}<{v}<{bt}$ can be expressed in interval notation as'
        bank=[('open',f'({at},{bt})','math'),('both_closed',f'[{at},{bt}]','math'),('right_closed',f'({at},{bt}]','math'),('left_closed',f'[{at},{bt})','math')]
        if profile=='signed_source': bank.append(('reflect',f'({tex(str(-b))},{tex(str(-a))})','math'))
        else: bank.append(('omit_lower',rf'(-\infty ,{bt})','math'))
        sol=source_solution(at,bt,v)
    # Content identity uses actual displayed components; raw missing attributes differ.
    content=digest({'version':VERSION,'prompt':prompt,'solution':None if profile=='source_raw' else sol,'bank':sorted((val,typ) for _,val,typ in bank),'correct':None if profile=='source_raw' else next(val for rec,val,_ in bank if rec=='open')})
    qid=uid('question',content); fid=uid(qid,'selection')
    answers=[{':answer/id':uid(fid,typ,val),':answer/type':':answer.type/'+typ,':answer/value':val} for _,val,typ in bank]
    correct=answers[next(i for i,item in enumerate(bank) if item[0]=='open')][':answer/id']
    rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if profile!='source_raw':
        q[':question/difficulty']=':question.difficulty/'+level
        q[':question/worked-solution']=sol
        field[':answer-field/correct']=[':answer/id',correct]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':template,'profile':profile,'difficulty':level,'difficulty_status':'authored','parameters':p,'source':SOURCE,'source_ids':['q-102204' if template==TEMPLATES[0] else 'q-59294'],'recipes':[rec for rec,_,_ in bank],'mathematical_fingerprint':digest({'template':template,'a':str(a),'b':str(b)}),'content_fingerprint':content,'repairs':[] if profile=='source_raw' else ['missing correct ref independently derived','missing practice solution authored','missing difficulty authored'],'plots':'none'}}

# All observed rated banks are easy, including negative and surd endpoints.
def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)
# Moderate: signed integer endpoints, always with a negative lower endpoint.
def generate_moderate(seed=0,**kwargs): return generate('moderate',seed,**kwargs)
# Hard: noninteger reduced rational endpoints; still no arithmetic or solving.
def generate_hard(seed=0,**kwargs): return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question']; f=q[':question/answer-fields'][0]
    rows=[q[':question/problem'],'']
    for letter,a in zip('ABCDE',f[':answer-field/choices']): rows.append(f'{letter}. '+('$'+a[':answer/value']+'$' if a[':answer/type'].endswith('/math') else a[':answer/value']))
    if ':answer-field/correct' in f:
        rows+=['','Correct: '+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]),'',q[':question/worked-solution']]
    return '\n'.join(rows)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all'); parser.add_argument('--seed',type=int,default=0); parser.add_argument('--count',type=int,default=1); parser.add_argument('--format',choices=['markdown','json'],default='markdown'); parser.add_argument('--template',choices=TEMPLATES); parser.add_argument('--profile',choices=PROFILES)
    args=parser.parse_args()
    if args.count<1: parser.error('count must be positive')
    levels=list(LEVELS) if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
