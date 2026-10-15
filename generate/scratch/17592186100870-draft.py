"""Draft matrix-product dimension generator; basis2275, no database operations.

Easy: two numeric dimensions in product order. Moderate: reverse the stated order.
Hard (authored): reverse the stated order with three whole symbolic dimensions.
Every family performs the same inner-dimension comparison and outer-dimension
selection, with no multiplication of entries or equations to solve. Raw profiles
preserve omissions/errors as ineligible evidence; defaults complete/repair them.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import uuid
import functools
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import checked_math_content, normalize_prose, normalize_tex

HERE = Path(__file__).with_suffix('')
SNAPSHOT = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186100870
KP_UUID = SNAPSHOT['record'][':knowledge-point/id']
VERSION = '2.0.0-draft'
SOURCES = {q[':question/math-academy-id']: q for q in SNAPSHOT['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS = ('easy', 'moderate', 'hard')
DEFAULTS = {
 'q-42379':dict(m=5,n=3,p=5), 'q-42380':dict(m=3,n=6,p=2),
 'q-129461':dict(m=2,n=4,p=6), 'q-129486':dict(m=2,n=8,p=7),
 'q-320315':dict(m=4,n=3,p=7), 'q-320344':dict(m=10,n=5,p=7),
 'q-70702':dict(m=2,n=4,p=5), 'q-70705':dict(m=5,n=2,p=3),
 'q-77473':dict(m=3,n=7,p=5), 'q-129480':dict(m=5,n=7,p=1),
 'q-70703':dict(m=4,n=3,p=6)}
# Entire observed banks, in captured order. '5'/'3' preserve opaque constants,
# never asserted to recover their historical misconception.
BANKS = {
 'q-42379':['m,n','m,p','n,m','undefined','n,n'],
 'q-42380':['m,n','p,m','m,p','p,n','n,p'],
 'q-129461':['p,m','m,5','undefined','n,m','m,p'],
 'q-129486':['m,p','m,n','undefined','n,p','p,m'],
 'q-70702':['n,3','3,p','m,p','p,m','undefined'],
 'q-70705':['m,m','n,n','p,m','m,p','undefined'],
 'q-77473':['m,p','p,p','undefined','m,m','p,m'],
 'q-129480':['m,p','p,m','m,m','undefined','n,m'],
 'q-70703':['n,p','undefined','p,m','m,p','n,n']}
AUTHORED_BANK = ['m,p','p,m','m,n','n,p','undefined']
DIM_RE = re.compile(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)')

def level_of(template):
    if template.startswith('symbolic-'): return 'hard'
    q = SOURCES[template]
    return q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]

def labels_of(template):
    text = SOURCES[template][':question/problem']
    labels = re.findall(r'\$([A-Z])\$ is a', text)
    target = re.search(r'\$([A-Z]{2})\??\$',text)[1]
    return labels, target

def kind_of(template):
    if template.startswith('symbolic-'): return template.split('-')[1]
    return SOURCES[template][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]

def valid_parameters(level, template, parameters):
    p = dict(parameters)
    if set(p) != {'m','n','p'}: raise ValueError('Expected exactly m,n,p')
    if level == 'hard':
        for key, variable in zip(('m','n','p'),('r','s','t')):
            if not isinstance(p[key],str) or not re.fullmatch(variable+r'\+[1-6]',p[key]):
                raise ValueError('Hard dimensions must be r+a, s+b, t+c with a,b,c in 1..6')
    else:
        if any(type(v) is not int or not 1 <= v <= 10 for v in p.values()):
            raise ValueError('Numeric dimensions are integers in 1..10')
        # All three values distinct preserves whole five-option source banks.
        if len(set(p.values())) != 3 and not (template=='q-42379' and p['m']==p['p'] and p['m']!=p['n']):
            raise ValueError('Numeric dimensions must be distinct, except q-42379 square output')
    return p

def dims_text(a,b,op=r'\times ',spaced=False):
    def component(x):
        return r'\left('+str(x)+r'\right)' if isinstance(x,str) and '+' in x else str(x)
    return component(a)+(' ' if spaced else '')+op+component(b)

def prompt_for(template,p,raw):
    old=SOURCES[template][':question/problem']; labels,target=labels_of(template)
    a,b=target
    shapes={a:(p['m'],p['n']),b:(p['n'],p['p'])}
    # Replace entire dimension components in factor order, never small tokens.
    i=iter(labels)
    def dim(match):
        label=next(i); x,y=shapes[label]
        old=match[0];op=r'\cdot ' if raw and r'\cdot' in old else r'\times '
        return dims_text(x,y,op,' ' in old[:old.index('\\')])
    return DIM_RE.sub(dim,old)

def solution_for(template,p,raw):
    source=SOURCES[template]; old=source.get(':question/worked-solution')
    if old is None: return None if raw else formal_solution(*labels_of(template)[1],p)
    # Distinct observed values make these slots unambiguous; protect field keys.
    values={str(v):str(p[k]) for k,v in DEFAULTS[template].items()}
    text=re.sub(r'\d+',lambda m:values.get(m[0],m[0]),old)
    if template=='q-70702' and not raw:
        text=text.replace('{R}','{@}').replace('{S}','{R}').replace('{@}','{S}')
    if not raw and p['n']==1:
        text=text.replace('There are $1$ columns','There is $1$ column').replace('$1$ rows in','$1$ row in')
    return text

def formal_solution(a,b,p):
    m,n,k=(p[x] for x in ('m','n','p'))
    outer=dims_text(m,k)
    def component(x):return r'\left('+str(x)+r'\right)' if isinstance(x,str) else str(x)
    opening=(f'There is $1$ column in ${a}$ and $1$ row in ${b}.$ ' if n==1 else f'There are ${n}$ columns in ${a}$ and ${n}$ rows in ${b}.$ ')
    return (opening+
      f'Since the number of columns in ${a}$ equals the number of rows in ${b},$ '
      f'the matrices ${a}$ and ${b}$ are conformable for multiplication, and ${a}{b}$ is a ${outer}$ matrix:\n\n$$\n'
      +f'{{{a}}}_{{{component(m)}\\times '+r'\boxed{\text{'+str(n)+r'}}}{\times }_{✓}'
      +f'{{{b}}}_{{'+r'\boxed{\text{'+str(n)+r'}}\times '+component(k)+'}='
      +f'{{{a}{b}}}_{{{outer}}}\n$$')

def bank_values(template,p,profile,raw):
    recipes=AUTHORED_BANK if profile=='method-derived' else BANKS[template]
    op=r'\cdot ' if raw and template in ('q-42379','q-42380') else r'\times '
    values=[]
    for recipe in recipes:
        if recipe=='undefined': values.append((':answer.type/text','The product is undefined'));continue
        x,y=recipe.split(',');a=p.get(x,x);b=p.get(y,y)
        # Exact source spacing is presentation evidence, not a distinct task.
        spaced=raw and template in ('q-42379','q-42380')
        values.append((':answer.type/math',dims_text(a,b,op,spaced)))
    if len(set(v[1].replace(' ','') for v in values))!=len(values):
        raise ValueError('bank_collision: reject whole profile')
    return values

def semantic_dimensions(parameters):
    return [str(parameters[k]) for k in ('m','n','p')]

def task_key(rec):
    # Order and supplied information matter; letter aliases/banks/layout do not.
    p=rec['generation']['parameters']
    return json.dumps([rec['generation']['ordering'],semantic_dimensions(p)],separators=(',',':'))

def checked_public(generator):
    """Shared checker requires a solution key; raw absent evidence uses a shadow.

    Empty shadow solution validates no invented content and never reaches output.
    All present source strings and every served normal record use the same checker.
    """
    @functools.wraps(generator)
    def checked(*args,**kwargs):
        rec=generator(*args,**kwargs)
        if ':question/worked-solution' not in rec['question']:
            shadow=copy.deepcopy(rec);shadow['question'][':question/worked-solution']=''
            checked_math_content(lambda:shadow)()
            rec['generation']['math_format']=shadow['generation']['math_format']
            return rec
        return checked_math_content(lambda:rec)()
    return checked

@checked_public
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,bank_profile=None):
    if level not in SUPPORTED_LEVELS: raise ValueError('Unknown level')
    if bank_profile is not None:
        if profile is not None and profile!=bank_profile: raise ValueError('Conflicting profiles')
        profile=bank_profile
    field_type=(field_type or '').split('/')[-1] or None
    rng=random.Random(seed)
    eligible=([t for t in SOURCES if level_of(t)==level] if level!='hard' else ['symbolic-radio','symbolic-blank'])
    eligible=[t for t in eligible if field_type in (None,kind_of(t))]
    if template is None:
        if not eligible: raise ValueError('Unsupported field type')
        template=rng.choice(eligible)
    if template not in eligible: raise ValueError('Template/level/field type mismatch')
    raw=bool(profile and profile.startswith('raw-'))
    if raw and profile!='raw-'+template: raise ValueError('Raw profile/template mismatch')
    normal_profile=('method-derived' if template.startswith('symbolic-') or template in ('q-129461','q-70702') else 'observed-'+template)
    profile=profile or normal_profile
    if profile not in (normal_profile,'raw-'+template): raise ValueError('Unsupported complete bank profile')
    if parameters is None:
        candidates=(list(itertools.product(range(1,7),repeat=3)) if level=='hard' else list(itertools.permutations(range(1,11),3)))
        rng.shuffle(candidates)
        for triple in candidates:
            p=dict(zip(('m','n','p'),(f'{v}+{n}' for v,n in zip(('r','s','t'),triple)))) if level=='hard' else dict(zip(('m','n','p'),triple))
            try:
                if kind_of(template)=='radio': bank_values(template,p,profile,raw)
            except ValueError: continue
            break
        else: raise ValueError('No eligible whole bank')
    else:p=valid_parameters(level,template,parameters)
    if template.startswith('symbolic-'):
        labels=['X','Y'];target='YX';a,b=target
        problem=(f'Suppose $X$ is a ${dims_text(p["n"],p["p"])}$ matrix and $Y$ is a ${dims_text(p["m"],p["n"])}$ matrix. '
                 'The symbols $r$, $s$, and $t$ denote positive integers. ')
        problem+=(f'What are the dimensions of ${target}$?' if kind_of(template)=='radio' else f'The dimensions of ${target}$ are{{{{field-1}}}}$\\times $\n{{{{field-2}}}}.')
        solution=formal_solution(a,b,p); source={}
    else:
        source=SOURCES[template];labels,target=labels_of(template);a,b=target
        problem=prompt_for(template,p,raw);solution=solution_for(template,p,raw)
    q={':question/problem':normalize_prose(problem)}
    if solution is not None:q[':question/worked-solution']=normalize_prose(solution)
    if not raw or ':question/difficulty' in source:q[':question/difficulty']=':question.difficulty/'+level
    fields=[]
    oldfields=source.get(':question/answer-fields',[])
    if kind_of(template)=='blank':
        for key in ('field-1','field-2'):
            fields.append({'key':key,'type':':answer-field.type/blank','values':[(':answer.type/math',str(p['m' if key=='field-1' else 'p']))], 'correct':0})
    else:
        values=bank_values(template,p,profile,raw)
        correct_value=dims_text(p['m'],p['p'],r'\cdot ' if raw and template in ('q-42379','q-42380') else r'\times ',raw and template in ('q-42379','q-42380'))
        correct=next(i for i,v in enumerate(values) if v[1]==correct_value)
        if raw and ':answer-field/correct' not in oldfields[0]:correct=None
        fields=[{'key':'selection','type':':answer-field.type/radio','values':values,'correct':correct}]
    for f in fields:f['values']=[(t,normalize_tex(v) if t==':answer.type/math' else v) for t,v in f['values']]
    content={'version':VERSION,'question':q,'fields':fields}
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps(content,sort_keys=True)))
    output=[]
    for f in fields:
        fid=str(uuid.uuid5(uuid.UUID(qid),f['key'])); choices=[]
        for t,v in f['values']:
            aid=str(uuid.uuid5(uuid.UUID(fid),t+'|'+v));choices.append({':answer/id':aid,':answer/type':t,':answer/value':v})
        field={':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':f['type'],':answer-field/choices':choices}
        if f['correct'] is not None:field[':answer-field/correct']=[':answer/id',choices[f['correct']][':answer/id']]
        if f['type'].endswith('/radio'):rng.shuffle(choices)
        output.append(field)
    q[':question/id']=qid;q[':question/answer-fields']=output
    ordering='forward' if labels==list(target) else 'reverse'
    rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SNAPSHOT['record'][':knowledge-point/title']},'question':q,
      'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'bank_profile':profile,'parameters':p,'ordering':ordering,
       'source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'raw_evidence':raw,'eligible_for_learning':not raw,
       'authored_completion':template in ('q-42379','q-42380') and not raw,'authored_level':level=='hard',
       'python_version':sys.version.split()[0],'sympy_version':sp.__version__}}
    rec['generation']['mathematical_fingerprint']=hashlib.sha256(task_key(rec).encode()).hexdigest()
    return rec

# Easy: observed forward numeric statements; unrated originals assigned authored easy.
def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)

# Moderate: observed reversed numeric statements; no increase in arithmetic.
def generate_moderate(seed=0,**kwargs): return generate('moderate',seed,**kwargs)

# Hard: authored symbolic whole dimensions; the same ordered matching/selection.
def generate_hard(seed=0,**kwargs): return generate('hard',seed,**kwargs)

def markdown(rec):
    q=rec['question'];g=rec['generation']
    rows=[f'Level: {q.get(":question/difficulty","unrated")} | Template: {g["template"]} | Profile: {g["profile"]}',q[':question/problem']]
    for field in q.get(':question/answer-fields',[]):
        rows.append(field[':answer-field/key']+' ('+field[':answer-field/type']+')')
        for a in field[':answer-field/choices']:
            mark=' [correct]' if field.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''
            value='$'+a[':answer/value']+'$' if a[':answer/type'].endswith('/math') else a[':answer/value']
            rows.append('- '+value+mark)
        if ':answer-field/correct' not in field: rows.append('Correct designation absent in raw source.')
    rows.append(q.get(':question/worked-solution','Worked solution absent in raw source.'))
    return '\n\n'.join(rows)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),required=True)
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2)
    ap.add_argument('--format',choices=('json','markdown'),default='json')
    ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    if args.count<0:ap.error('count must be nonnegative')
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (SUPPORTED_LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
