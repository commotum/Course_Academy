#!/usr/bin/env python3
"""Seeded finite closed-interval conversion; source basis 4471.
Adapted from the supplied 17592186059829-draft.py. Easy forward and moderate
reverse integer templates preserve complete source banks. No assets or DB writes.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, uuid, re, sys, copy, importlib.util
from pathlib import Path
from functools import lru_cache
import sympy as sp

KP_ID=17592186059829
KP_UUID='2f519fa9-de89-5b00-aa02-312cf8e32cba'
TITLE='Converting Between Intervals and Inequalities: Closed Intervals'
VERSION='closed-intervals-workspace-v4'
GENERATOR_ID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:question-generator:'+KP_UUID))
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source.json').read_text())
CURRENT_SOURCE={'record': SOURCE['material']['kp']}
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
    if level not in ('easy','moderate'): raise ValueError('unsupported difficulty; use easy or moderate')
    return tuple(str(i) for i in range(-12,13))

def eligible(level,a,b):
    return bool(sp.sympify(a)<sp.sympify(b))

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
    s=s.replace('$','').replace('∈',r'\in').strip().rstrip('.?')
    if r'\in ' in s: s=s.split(r'\in ',1)[1]
    if ' or ' in s:
        l,r=s.split(' or ')
        inclusive=r'\le' in l
        a=number(re.split(r'\\le|<',l)[1]); b=number(re.split(r'\\ge|>',r)[1])
        return sp.Union(sp.Interval(-sp.oo,a,right_open=not inclusive),sp.Interval(b,sp.oo,left_open=not inclusive))
    if s.startswith(('(','[')):
        l,r=s[1:-1].split(',')
        return sp.Interval(number(l),number(r),left_open=s[0]=='(',right_open=s[-1]==')')
    parts=re.split(r'(\\le|\\ge|<|>)',s)
    if len(parts)!=5 or parts[2].strip() not in VARIABLES: raise ValueError('not a complete inequality: '+s)
    if parts[1] in (r'\ge','>'):
        return sp.Interval(number(parts[4]),number(parts[0]),left_open=parts[3]=='>',right_open=parts[1]=='>')
    return sp.Interval(number(parts[0]),number(parts[4]),left_open=parts[1]=='<',right_open=parts[3]=='<')

def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def legacy_generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
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
    if profile=='observed_inequality':
        # Repair the missing solution with the complete same-direction source's
        # plain sequence; avoid adding low-contrast colors to the authored repair.
        exemplar=next(q for q in CURRENT_SOURCE['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id')=='q-154728')
        captured_solution=exemplar[':question/worked-solution'].replace('-7','@@LEFT@@').replace('0','@@RIGHT@@').replace('@@LEFT@@',a).replace('@@RIGHT@@',b)
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


VARIABLES=('x','y','t')
ORIENTATIONS=('ascending','descending')
_fmt_spec=importlib.util.spec_from_file_location('closed_interval_math_format',HERE/'math_format.py')
_fmt=importlib.util.module_from_spec(_fmt_spec);_fmt_spec.loader.exec_module(_fmt)

def strict_int(value,name,minimum=None):
    if type(value) is not int or (minimum is not None and value<minimum):
        raise ValueError(name+' must be an integer'+(' >= '+str(minimum) if minimum is not None else ''))
    return value

def transform_math(text,variable,orientation):
    # Reverse each complete chained inequality only, preserving colored relation
    # wrappers and concrete solution stage order. Outside-union profiles retain
    # their observed left/right ray presentation.
    text=re.sub(r'(?<![A-Za-z])x(?![A-Za-z])',variable,text)
    if orientation=='descending':
        # Split at math delimiters to prevent consuming prose around equations.
        pieces=re.split(r'(\$\$.*?\$\$|\$[^$]*\$)',text,flags=re.S)
        for i,p in enumerate(pieces):
            if not p.startswith('$'):continue
            delim='$$' if p.startswith('$$') else '$';body=p[len(delim):-len(delim)]
            body=reverse_chain(body,variable)
            pieces[i]=delim+body+delim
        text=''.join(pieces)
    return text

def reverse_chain(body,variable):
    # Locate full relation tokens including their source color group and spacing.
    rel=r'(?:\s|\\,)*(?:\{\\color\{(?:blue|red)\}\{)?(?:\\le|<)(?:\}\})?(?:\s|\\,)*'
    m=re.fullmatch(r'(.*?)('+rel+r')'+variable+r'('+rel+r')(.*?)',body,re.S)
    if not m:return body
    flip=lambda s:s.replace(r'\le',r'\ge').replace('<','>')
    return m.group(4)+flip(m.group(3))+variable+flip(m.group(2))+m.group(1)

@_fmt.checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,variable=None,orientation=None):
    if level not in ('easy','moderate'): raise ValueError('hard is unsupported by supplied source evidence')
    expected='inequality_to_interval' if level=='easy' else 'interval_to_inequality'
    allowed=('captured_interval',) if level=='easy' else ('captured_inequality','observed_inequality')
    if template not in (None,expected): raise ValueError('template unsupported at this source difficulty')
    if profile is not None and profile not in allowed: raise ValueError('profile unsupported at this source difficulty')
    profile=profile or random.Random('profile:'+str(seed)).choice(allowed)
    template=expected
    strict_int(seed,'seed')
    if profile is not None and profile.startswith('raw_'): raise ValueError('raw incomplete sources are evidence only; use replay_source')
    rng=random.Random('notation:'+str(seed))
    # A whole bank is selected before the endpoint instance. Distinct original
    # reverse banks remain whole profiles (strict versus inclusive outside rays).
    variable=variable if variable is not None else rng.choice(VARIABLES)
    orientation=orientation if orientation is not None else rng.choice(ORIENTATIONS)
    if variable not in VARIABLES or orientation not in ORIENTATIONS:raise ValueError('unknown variable/orientation')
    r=legacy_generate(level,int(digest({'stream':'instance','seed':seed}),16),template,field_type,parameters,profile)
    r['generation']['seed']=seed
    q=r['question']; f=q[':question/answer-fields'][0]
    old_correct=f[':answer-field/correct'][1]
    q[':question/problem']=_fmt.normalize_prose(transform_math(q[':question/problem'],variable,orientation))
    q[':question/worked-solution']=_fmt.normalize_prose(transform_math(q[':question/worked-solution'],variable,orientation))
    for a in f[':answer-field/choices']:
        if a[':answer/type']==':answer.type/math':
            a[':answer/value']=_fmt.normalize_tex(reverse_chain(re.sub(r'(?<![A-Za-z])x(?![A-Za-z])',variable,a[':answer/value']),variable) if orientation=='descending' else re.sub(r'(?<![A-Za-z])x(?![A-Za-z])',variable,a[':answer/value']))
        else:a[':answer/value']=_fmt.normalize_prose(transform_math(a[':answer/value'],variable,orientation))
    # Preserve existing v2 normal identities whenever the display is unchanged.
    if True: # All content identities follow normalization.
        content=digest({'version':VERSION,'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'difficulty':q[':question/difficulty'],'bank':sorted((a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])})
        qid=uid(content);fid=uid(qid+':selection');q[':question/id']=qid;f[':answer-field/id']=fid
        for a in f[':answer-field/choices']:
            is_correct=a[':answer/id']==old_correct
            a[':answer/id']=uid(fid+a[':answer/type']+a[':answer/value'])
            if is_correct:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
        r['generation']['content_fingerprint']=content
    r['generation'].update({'variable':variable,'orientation':orientation,'draft_revision':VERSION,'basis':SOURCE['basis'],'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],
        'level_origin':('observed source rating; integer endpoint/notation extension' if profile.startswith('captured_') else 'authored moderate rating for repaired unrated reverse bank'),
        'source_error_policy':'q-59295 raw record ineligible: no rating, key or solution; separately supported keyed repair; q-154728 punctuation normalized'})
    assert len(set(displayed_set(a[':answer/value']) for a in f[':answer-field/choices']))==5
    return r

def normalize_raw(q):
    # Preserve all original UUIDs and values. Strip only database projection
    # metadata and resolve enum/lookup representations for the learner fixture.
    q=copy.deepcopy(q)
    q.pop(':db/id',None)
    for k in [':question/difficulty']:
        if isinstance(q.get(k),dict):q[k]=q[k][':db/ident']
    for f in q.get(':question/answer-fields',[]):
        f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
        if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        for a in f[':answer-field/choices']:
            a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident']
    return q

def replay_source(source_id):
    raw=next(q for q in SOURCE['material']['kp'][':knowledge-point/questions'] if q[':question/math-academy-id']==source_id)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':normalize_raw(raw),
      'generation':{'source_id':source_id,'raw_evidence':True,'basis':SOURCE['basis'],'eligible':source_id!='q-59295'}}

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None,**kwargs):return generate('easy',seed,template,field_type,parameters,profile,**kwargs)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None,**kwargs):return generate('moderate',seed,template,field_type,parameters,profile,**kwargs)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None,**kwargs):return generate('hard',seed,template,field_type,parameters,profile,**kwargs)

def capacity(level,template=None,profile=None):
    if level not in ('easy','moderate'): raise ValueError('unsupported difficulty')
    expected='inequality_to_interval' if level=='easy' else 'interval_to_inequality'
    allowed=('captured_interval',) if level=='easy' else ('captured_inequality','observed_inequality')
    if template not in (None,expected) or profile not in (None,*allowed):raise ValueError('unsupported template/profile')
    return len(parameter_catalog(level))

def generate_batch(level,seed=0,count=1,template=None,profile=None,variable=None,orientation=None,_excluded=None):
    strict_int(seed,'seed');strict_int(count,'count',1)
    cap=capacity(level,template,profile)
    if count>cap:raise ValueError('count exceeds finite mathematical capacity '+str(cap))
    result=[];seen=set(_excluded or ());attempt=0
    while len(result)<count:
        r=generate(level,seed+attempt,template,parameters=None,profile=profile,variable=variable,orientation=orientation);attempt+=1
        fp=r['generation']['mathematical_fingerprint']
        if fp not in seen:seen.add(fp);result.append(r)
        if attempt>max(1000,count*100):raise ValueError('batch sampling exhausted; request a smaller batch')
    return result

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0];lines=[q[':question/problem'],'']
    for a in f[':answer-field/choices']:
        v=a[':answer/value'];lines.append('- '+(v if a[':answer/type'].endswith('/text') else '$'+v+'$'))
    answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    return '\n'.join(lines+['','Correct: $'+answer+'$','',q[':question/worked-solution']])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=('easy','moderate','hard'),default='easy')
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile',choices=tuple(p for p in PROFILES if not p.startswith('raw_')))
    ap.add_argument('--variable',choices=VARIABLES);ap.add_argument('--orientation',choices=ORIENTATIONS)
    ap.add_argument('--format',choices=('markdown','json'),default='json');args=ap.parse_args()
    levels=(args.difficulty,)
    try:
        rs=[];seen=set()
        for level in levels:
            batch=generate_batch(level,args.seed,args.count,args.template,args.profile,args.variable,args.orientation,seen)
            rs.extend(batch);seen.update(r['generation']['mathematical_fingerprint'] for r in batch)
    except ValueError as ex:ap.error(str(ex))
    print(json.dumps(rs,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
if __name__=='__main__':main()
