#!/usr/bin/env python3
"""Finite closed intervals, both directions. Basis 1356; no database operations.

All three difficulty definitions are authored: source radios are unrated.
Easy reads ordered integer endpoints; moderate reads reduced rational endpoints;
hard reads signed exact surd endpoints. No solving, endpoint simplification,
ordering question, or open/half-open/unbounded correct-set branch is introduced.
Source raw profiles preserve missing rating, solution and correct designation.
Normal profiles add independently computed keys and canonical-example solutions.
Each profile selects its complete five-choice bank before building an instance.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, uuid
from pathlib import Path
from functools import lru_cache
import sympy as sp

KP_ID=17592186059829
KP_UUID='2f519fa9-de89-5b00-aa02-312cf8e32cba'
TITLE='Converting Between Intervals and Inequalities: Closed Intervals'
VERSION='closed-intervals-v2'
GENERATOR_ID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+KP_UUID))
HERE=Path(__file__).with_suffix('')
CURRENT_SOURCE=json.loads((HERE/'current-kp.json').read_text())
SOURCE=json.loads((HERE/'source.json').read_text())
TEMPLATES=('inequality_to_interval','interval_to_inequality')
PROFILES={
 'observed_interval':('inequality_to_interval',False),
 'raw_interval':('inequality_to_interval',True),
 'observed_inequality':('interval_to_inequality',False),
 'raw_inequality':('interval_to_inequality',True),
 'captured_interval':('inequality_to_interval',False),
 'captured_inequality':('interval_to_inequality',False),
}
SOURCE_IDS={'inequality_to_interval':'q-102200','interval_to_inequality':'q-59295'}

def canonical(v):
    return sp.sstr(sp.sympify(v))

@lru_cache(None)
def endpoint_catalog(level):
    if level=='easy': return tuple(str(i) for i in range(-12,13))
    if level=='moderate':
        values={sp.Rational(n,d) for d in (1,2,3,4,5) for n in range(-12,13) if abs(sp.Rational(n,d))<=8}
    elif level=='hard':
        values={sp.Rational(n,d) for d in (1,2,3) for n in range(-6,7)}
        values|={sgn*c*sp.sqrt(r) for sgn in (-1,1) for c in (1,2,3) for r in (2,3,5,7)}
    else: raise ValueError('difficulty must be easy, moderate, or hard')
    return tuple(canonical(v) for v in sorted(values,key=lambda v:float(v)))

def eligible(level,a,b):
    va,vb=sp.sympify(a),sp.sympify(b)
    if not bool(va<vb): return False
    if level=='moderate': return not (va.is_Integer and vb.is_Integer)
    if level=='hard':
        # Both noninteger, one irrational, at least one negative endpoint:
        # an exact signed-number reading demand, never a positive integer easy alias.
        return not va.is_Integer and not vb.is_Integer and (va.is_irrational or vb.is_irrational) and bool(va<0)
    return True

@lru_cache(None)
def parameter_catalog(level):
    return tuple({'a':a,'b':b} for a,b in itertools.combinations(endpoint_catalog(level),2) if eligible(level,a,b))

def guard(level,p,raw=False):
    if not isinstance(p,dict) or set(p)!={'a','b'}: raise ValueError('parameters require exactly a and b')
    catalog=endpoint_catalog('easy' if raw else level)
    for v in p.values():
        if not isinstance(v,str) or v not in catalog: raise ValueError('canonical endpoint strings required; aliases rejected')
    if raw:
        # Explicit evidence replay generalizes both recovered recipes across integers.
        if any(v not in endpoint_catalog('easy') for v in p.values()) or not bool(sp.sympify(p['a'])<sp.sympify(p['b'])):
            raise ValueError('raw evidence endpoints must be ordered integers in -12..12')
    elif any(v not in endpoint_catalog(level) for v in p.values()) or not eligible(level,p['a'],p['b']):
        raise ValueError('parameters outside authored '+level+' workload catalog')

def tex(v): return sp.latex(sp.sympify(v))
def spaced_negative(v): return '- '+v[1:] if v.startswith('-') else v

def prompt(template,a,b):
    if template=='inequality_to_interval':
        return 'The inequality $'+a+r' \le x \le '+b+'$ can be expressed in interval notation as'
    return 'Which inequality corresponds to the interval $x ∈ ['+spaced_negative(a)+', '+b+']$?'

def choices(template,a,b):
    if template=='inequality_to_interval':
        aa=spaced_negative(a)
        return [(':answer.type/math','['+aa+', '+b+')'),
                (':answer.type/math','('+a+', '+b+')'),
                (':answer.type/math','(- ∞, '+b+']'),
                (':answer.type/math','['+aa+', '+b+']'),
                (':answer.type/math','('+a+', '+b+']')]
    return [(':answer.type/math',a+r' \le x < '+b),
            (':answer.type/math',a+' < x < '+b),
            (':answer.type/math',a+r' < x \le '+b),
            (':answer.type/math',a+r' \le x \le '+b),
            (':answer.type/text','$x < '+spaced_negative(a)+'$ or $x > '+b+'$')]

NOTATION='- Parentheses ${\\color{red}{(}}\\phantom{0} \\phantom{0}{\\color{red}{)}}$ if the endpoints are *not* included.\n- Brackets ${\\color{blue}{[}}\\phantom{0} \\phantom{0}{\\color{blue}{]}}$ if the endpoints *are* included.'
def solution(template,a,b):
    if template=='inequality_to_interval':
        return ('Every inequality can be expressed as an interval. We use the following notations:\n\n'+NOTATION+
          '\n\nOur inequality contains only "or equal to" symbols. So, the endpoints $'+a+'$ and $'+b+'$ *are* included.\n\n$$\n'+a+r'\,\, {\color{blue}{\le}} \,\, x \,\, {\color{blue}{\le}} \,\, '+b+
          '\n$$\n\nTherefore, we can express our inequality in interval notation as follows:\n\n$$\n'+r'{\color{blue}{[}}'+a+','+b+r'{\color{blue}{]}}'+
          '\n$$\n\nMore formally, we can also write\n\n$$\nx'+r'\in ['+a+','+b+']\n$$')
    # Reverse direction follows the preceding open-interval canonical sequence;
    # only the closed endpoint inclusion, brackets and relations change.
    notation=NOTATION.replace(' if the endpoints',' to indicate that the endpoints')
    return ('Every interval can be expressed as an inequality. We use the following notations:\n\n'+notation+
      '\n\nOur interval contains only brackets. So, the endpoints are *included*.\n\n$$\nx'+r'\in {\color{blue}{[}}'+a+', '+b+r'{\color{blue}{]}}'+
      '\n$$\n\nTherefore, our interval can be expressed as the following inequality:\n\n$$\n'+a+r' \,\,{\color{blue}{\le}}\,\, x \,\,{\color{blue}{\le}}\,\, '+b+'\n$$')

# Parse actual displayed complete mathematical objects, independently of recipes.
def number(s):
    s=s.strip().replace(' ','').replace('−','-')
    if s in ('-∞',r'-\infty'): return -sp.oo
    if s in ('∞',r'\infty'): return sp.oo
    import re
    s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
    s=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',s)
    s=re.sub(r'(\d)(sqrt)',r'\1*\2',s)
    return sp.sympify(s)

def displayed_set(s):
    s=s.replace('$','').strip()
    if 'or' in s:
        l,r=s.split(' or ')
        inclusive=r'\le' in l
        a=number(l.split(r'\le' if inclusive else '<')[1]);b=number(r.split(r'\ge' if inclusive else '>')[1])
        return sp.Union(sp.Interval(-sp.oo,a,right_open=not inclusive),sp.Interval(b,sp.oo,left_open=not inclusive))
    if s.startswith(('(','[')):
        l,r=s[1:-1].split(',')
        return sp.Interval(number(l),number(r),left_open=s[0]=='(',right_open=s[-1]==')')
    import re
    parts=re.split(r'(\\le|<)',s)
    if len(parts)!=5 or parts[2].strip()!='x': raise ValueError('not a complete inequality: '+s)
    return sp.Interval(number(parts[0]),number(parts[4]),left_open=parts[1]=='<',right_open=parts[3]=='<')

def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'): raise ValueError('unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only radio supported')
    rng=random.Random(seed)
    if profile is not None:
        if profile not in PROFILES:raise ValueError('unknown bank profile')
        selected,raw=PROFILES[profile]
        if template is not None and template!=selected:raise ValueError('profile/template mismatch')
        template=selected
    else:
        template=template or rng.choice(TEMPLATES)
        profile='observed_interval' if template=='inequality_to_interval' else 'observed_inequality'
        raw=False
    if template not in TEMPLATES:raise ValueError('unknown template')
    if raw and level!='easy':raise ValueError('raw evidence uses easy replay without assigning an observed rating')
    captured=profile.startswith('captured_')
    if captured and level!=('easy' if profile=='captured_interval' else 'moderate'):
        raise ValueError('captured source profile requires its observed rating')
    sampling_level='easy' if captured else level
    p=dict(parameters) if parameters is not None else dict(rng.choice(parameter_catalog(sampling_level)))
    guard(sampling_level,p,raw)
    a,b=tex(p['a']),tex(p['b'])
    problem=prompt(template,a,b)
    bank=choices(template,a,b)
    captured_solution=None
    source_id=SOURCE_IDS[template]
    if captured:
        source_id='q-102200' if profile=='captured_interval' else 'q-154728'
        original=next(q for q in CURRENT_SOURCE['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id')==source_id)
        oa,ob=('-10','3') if profile=='captured_interval' else ('-7','0')
        def substitute(text):return text.replace(oa,'@@LEFT@@').replace(ob,'@@RIGHT@@').replace('@@LEFT@@',a).replace('@@RIGHT@@',b)
        problem=substitute(original[':question/problem'])
        # q-154728 includes its question mark inside math. Preserve source,
        # but put punctuation outside the generated math delimiter.
        if profile=='captured_inequality':problem=problem.replace(']?$',']$?')
        field=original[':question/answer-fields'][0]
        bank=[(z[':answer/type'][':db/ident'],substitute(z[':answer/value'])) for z in field[':answer-field/choices']]
        captured_solution=substitute(original[':question/worked-solution'])
    sets=[displayed_set(v) for _,v in bank]
    correct=sp.Interval(sp.sympify(p['a']),sp.sympify(p['b']))
    correct_indices=[i for i,s in enumerate(sets) if s==correct]
    if len(correct_indices)!=1 or len(set(sets))!=5:raise ValueError('reject entire ambiguous bank')
    q={':question/problem':problem}
    if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':captured_solution or solution(template,a,b)})
    fingerprint=digest({'direction':template,'a':sp.srepr(correct.start),'b':sp.srepr(correct.end),'endpoint_inclusion':'both'})
    content=digest({'version':VERSION,'prompt':problem,'solution':q.get(':question/worked-solution'),'difficulty':q.get(':question/difficulty'),'bank':sorted(bank)})
    qid=uid(content);fid=uid(qid+':selection')
    answers=[{':answer/id':uid(fid+typ+v),':answer/type':typ,':answer/value':v} for typ,v in bank]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if not raw:field[':answer-field/correct']=[':answer/id',answers[correct_indices[0]][':answer/id']]
    rng.shuffle(answers)
    q.update({':question/id':qid,':question/answer-fields':[field]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
      'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,
       'mathematical_fingerprint':fingerprint,'content_fingerprint':content,'level_origin':'observed current source rating' if captured else 'authored; historical originals unrated',
       'source_id':source_id,'raw_evidence':raw,'database':SOURCE['database'],'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],
       'correct_set':str(correct),'domain':'a < b, finite real closed endpoints; both directions, no solving','plot_rating':'none'}}

# EASY: integer endpoint reading; both directions are equal-level variants.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: at least one reduced noninteger rational; no arithmetic is requested.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: signed, noninteger endpoint forms, including an exact surd; same conversion.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    lines=[q[':question/problem'],'']
    for a in f[':answer-field/choices']:
        v=a[':answer/value']; lines.append('- '+(v if a[':answer/type'].endswith('/text') else '$'+v+'$'))
    if ':answer-field/correct' in f:
        v=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        lines+=['','Correct: $'+v+'$','',q[':question/worked-solution']]
    else:lines+=['','Raw evidence: source correct designation, rating and solution absent.']
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=('all','easy','moderate','hard'),default='all')
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile',choices=tuple(PROFILES))
    ap.add_argument('--format',choices=('markdown','json'),default='markdown')
    args=ap.parse_args()
    if args.count<1:ap.error('count must be positive')
    levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    rs=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(rs,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
if __name__=='__main__':main()
