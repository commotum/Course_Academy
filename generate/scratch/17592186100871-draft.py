#!/usr/bin/env python3
"""Step 3–7 draft: count displayed matrix dimensions and apply the outer-dimension rule.

Easy (authored): forward displayed factors with the outer-dimension rule supplied,
all dimensions1–4, two dimension fragments.
Moderate (observed): forward products, each dimension 1–4, at least one3/4.
Hard (observed): product reverses the order in which factors are supplied, same
1–4 counting workload. No entry multiplication, symbolic dimensions or chains.
Historical bank profiles preserve their complete observed shape relationships.
"""
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).with_suffix('')
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import matrix_tex,normalize_tex,normalize_prose,checked_math_content,validate_generated_record
KP_ID=17592186100871
SNAPSHOT=json.loads((HERE/'source.json').read_text());KP=SNAPSHOT['record']
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions'] if ':question/math-academy-id' in q}
VERSION='matrix-product-dimensions-draft-v2'
SUPPORTED_LEVELS=('easy','moderate','hard')

def read(q):
    text=q[':question/problem'];items=[]
    for match in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S):
        rows=[[v.strip() for v in row.strip().split('&')] for row in match[2].split(r'\\')]
        items.append((match[1],rows))
    target=re.search(r'dimensions of \$([A-Z]{2})',text)[1]
    matrices=dict(items);a,b=target;left=matrices[a];right=matrices[b]
    assert len(left[0])==len(right)
    return items,target,(len(left),len(right),len(right[0]))
DEFAULTS={mid:dict(zip(('r','k','c'),read(q)[2])) for mid,q in SOURCES.items()}

def level_of(template):
    if template=='scaffolded-forward-blank':return 'easy'
    if template=='forward-blank':return 'moderate'
    if template=='reverse-blank':return 'hard'
    q=SOURCES[template]
    return q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1]

def field_kind(template):
    return 'blank' if template.endswith('blank') else (SOURCES[template][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1] if template in SOURCES else 'radio')

def recipes(profile,r,k,c):
    if profile=='source-bank:q-129489':return [('inner-right',(k,c)),('transpose',(c,r)),('right-square',(c,c)),('correct',(r,c)),('undefined',None)]
    if profile in ('source-bank:q-129492','authored-outers'):return [('correct',(r,c)),('transpose',(c,r)),('undefined',None),('right-square',(c,c)),('left-square',(r,r))]
    return [('undefined',None),('left-inner',(r,k)),('inner-left',(k,r)),('inner-square',(k,k)),('correct',(r,c))]

def eligible(template,p,raw=False):
    if set(p)!={'r','k','c'} or any(type(v) is not int for v in p.values()):return False
    r,k,c=(p[x] for x in ('r','k','c'));lev=level_of(template)
    if any(not 1<=v<=4 for v in (r,k,c)):return False
    if raw:return True
    if lev=='easy':return True
    if max(r,k,c)<3:return False
    # Retain observed complete structural profiles; blanks permit outer-role slots.
    if template=='q-129492':return r==k and r!=c
    if template=='q-77475':return r==c==1
    if template in ('q-77476','q-22065'):return k==1 and r==c
    if template=='q-22067':return r==c and r!=k
    if template=='q-129489':return len({r,k,c})==3
    return True

def domain(template,profile=None):
    out=[]
    for r in range(1,5):
      for k in range(1,5):
       for c in range(1,5):
        p=dict(r=r,k=k,c=c)
        if not eligible(template,p):continue
        bank=recipes(profile or ('source-bank:'+template if template in SOURCES else 'authored-outers'),r,k,c)
        if field_kind(template)=='radio' and len({v for _,v in bank})!=len(bank):continue
        out.append(p)
    return out

def cells(rows,cols):return [[str((i*cols+j)%9-4) for j in range(cols)] for i in range(rows)]

def solution(items,target,dims,source=None,raw=False):
    a,b=target;r,k,c=dims;shapes={a:(r,k),b:(k,c)}
    # Four complete stages, retaining source prose and original white-space masks.
    first,second=(x[0] for x in items)
    firstrow=3 if source=='q-22067' and raw else shapes[first][0]
    opening=f'We notice that ${first}$ is a ${firstrow}\\times {shapes[first][1]}$ matrix and ${second}$ is a ${shapes[second][0]}\\times {shapes[second][1]}$ matrix. \n\n'
    count=('There is $1$ column' if k==1 else f'There are ${k}$ columns')+f' in ${a}$ and ${k}$ '+('row' if k==1 else 'rows')+f' in ${b}.$ Since the number of columns in ${a}$ equals the number of rows in ${b},$ the matrices ${a}$ and ${b}$ are conformable for multiplication. \n\n'
    trailing=' ' if source in ('q-129492','q-320389') else ''
    final=f'The product ${target}$ has dimensions ${r}\\times {c}:$'+trailing+'\n\n$$\n'
    diagram=rf'{{{a}}}_{{{r}\times \boxed{{\text{{{k}}}}}}}{{\times }}_{{✓}}{{{b}}}_{{\boxed{{\text{{{k}}}}}\times {c}}}={{{target}}}_{{{r}\times {c}}}'
    return opening+count+final+diagram+'\n$$'

def construct(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported level')
    rng=random.Random(seed)
    choices={'easy':['scaffolded-forward-blank'],'moderate':['q-129492','q-77475','q-77476','q-22065','q-320351','q-320389','forward-blank'],'hard':['q-22067','q-129489','q-275395','q-320371','reverse-blank']}[level]
    if template is None:
        if field_type:choices=[t for t in choices if field_kind(t)==field_type]
        if not choices:raise ValueError('Unsupported field type')
        template=rng.choice(choices)
    if template not in SOURCES and template not in ('scaffolded-forward-blank','forward-blank','reverse-blank'):raise ValueError('Unknown template')
    if level_of(template)!=level:raise ValueError('Template level mismatch')
    kind=field_kind(template)
    if field_type not in (None,kind):raise ValueError('Field type mismatch')
    raw=profile=='raw-'+template
    if raw and template not in SOURCES:raise ValueError('Raw profile needs source')
    bank_profile=('source-bank:'+template if template in SOURCES else 'authored-outers')
    if profile not in (None,bank_profile,'raw-'+template):raise ValueError('Unknown profile')
    p=copy.deepcopy(parameters) if parameters is not None else (dict(DEFAULTS[template]) if raw else rng.choice(domain(template,bank_profile)))
    if not eligible(template,p,raw):raise ValueError('Parameters violate level/shape workload')
    r,k,c=(p[x] for x in ('r','k','c'))
    # Exact independent shape operation, without computing learner matrix entries.
    assert (sp.zeros(r,k)*sp.zeros(k,c)).shape==(r,c)
    if template in SOURCES:
        src=SOURCES[template];olditems,target,_=read(src);a,b=target
    else:
        src=None;target='BA' if level=='hard' else 'AB';a,b=target;olditems=[('A',[]),('B',[])]
    shapes={a:(r,k),b:(k,c)}
    items=[(name,(entries if template in DEFAULTS and p==DEFAULTS[template] else cells(*shapes[name]))) for name,entries in olditems]
    if src:
        # Replace complete matrix components; no global scalar/text replacement.
        index=iter(items)
        def submatrix(m):
            name,entries=next(index);return m[0][:m[0].index(r'\begin')]+matrix_tex(entries,augmented=False)
        problem=re.sub(r'[A-Z]\s*=\s*\\begin\{bmatrix\}.*?\\end\{bmatrix\}',submatrix,src[':question/problem'],flags=re.S)
    else:
        problem='Let\n'+('\nand\n'.join('$'+name+'='+matrix_tex(entries,augmented=False)+'$' for name,entries in items))+'.\n'
        problem+=('What are the dimensions of $'+target+'$?' if kind=='radio' else 'Then, the dimensions of $'+target+r'$ are {{field-1}} $\times$ {{field-2}}.')
    if level=='easy':problem+='\n\nFor conformable factors, use the number of rows of the first factor and the number of columns of the second.'
    sol=solution(items,target,(r,k,c),template if src else None,raw)
    q={':question/problem':normalize_prose(problem)}
    if not raw or ':question/worked-solution' in src:q[':question/worked-solution']=normalize_prose(sol)
    if not raw or ':question/difficulty' in src:q[':question/difficulty']=':question.difficulty/'+level
    fields=[]
    sfields=src[':question/answer-fields'] if src else [{':answer-field/key':key} for key in (['selection'] if kind=='radio' else ['field-1','field-2'])]
    bank=recipes(bank_profile,r,k,c)
    if kind=='radio' and len({v for _,v in bank})!=len(bank):raise ValueError('bank_collision: reject whole bank')
    for sf in sfields:
        key=sf[':answer-field/key'];f={':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind}
        members=bank if kind=='radio' else [('correct',r if key=='field-1' else c)]
        values=[]
        for recipe,v in members:
            value='The product is undefined' if v is None else str(v[0])+r'\times '+str(v[1]) if isinstance(v,tuple) else str(v)
            # q22065's legacy choice spelling used a centered dot for dimensions.
            if raw and template=='q-22065':value=value.replace(r'\times ',r' \cdot ')
            values.append((recipe,{':answer/type':':answer.type/text' if v is None else ':answer.type/math',':answer/value':normalize_tex(value) if v is not None else value}))
        f['_members']=values
        f['_correct_present']=not raw or ':answer-field/correct' in sf
        fields.append(f)
    # Content IDs depend on normalized learner strings and complete unordered banks.
    signature={'version':VERSION,'level':q.get(':question/difficulty'),'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'fields':[{k:f[k] for k in (':answer-field/key',':answer-field/type')}|{'bank':sorted((a[':answer/type'],a[':answer/value'],recipe=='correct' and f['_correct_present']) for recipe,a in f['_members'])} for f in fields]}
    identity=json.dumps(signature,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    qid=str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),identity));q[':question/id']=qid
    for f in fields:
        fid=str(uuid.uuid5(uuid.UUID(qid),f[':answer-field/key']));f[':answer-field/id']=fid;answers=[]
        correct_present=f.pop('_correct_present')
        for recipe,ans in f.pop('_members'):
            aid=str(uuid.uuid5(uuid.UUID(fid),json.dumps(ans,sort_keys=True)));ans[':answer/id']=aid;answers.append(ans)
            if recipe=='correct' and correct_present:f[':answer-field/correct']=[':answer/id',aid]
        if kind=='radio':rng.shuffle(answers)
        f[':answer-field/choices']=answers
    q[':question/answer-fields']=fields
    # Label-free ordered supplied shapes + target roles, not entries or bank profile.
    math_task={'supplied_shapes':[shapes[name] for name,_ in items],'target_roles':[next(i for i,(n,_) in enumerate(items) if n==name) for name in target]}
    meta={'version':VERSION,'seed':seed,'template':template,'parameters':p,'profile':profile or bank_profile,'bank_profile':bank_profile,'evidence_only':raw,'eligible_for_learning':not raw,'source_basis':SNAPSHOT['basis'],'source_lineage':SNAPSHOT['lineage'],'source_question':template if src else None,'source_difficulty':'missing; authored moderate for completed record' if template=='q-22065' else 'observed' if src else 'authored','mathematical_fingerprint':hashlib.sha256(json.dumps(math_task,sort_keys=True).encode()).hexdigest(),'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'source_repairs':['first A dimension 3×2 corrected to4×2'] if template=='q-22067' and not raw else [],'matrix_roles':'ordinary coefficient matrices, augmented=False'}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':meta}

@checked_math_content
def completed(*args,**kwargs):return construct(*args,**kwargs)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if profile and profile.startswith('raw-'):
        record=construct(level,seed,template,field_type,parameters,profile)
        # Validate a temporary copy so absent source attributes remain absent.
        temp=copy.deepcopy(record);temp['question'].setdefault(':question/worked-solution','');validate_generated_record(temp)
        record['generation']['math_format']=temp['generation']['math_format'];return record
    return completed(level,seed,template,field_type,parameters,profile)

# Authored easy: source outer-dimension rule supplied; displayed dimensions1–4.
def generate_easy(**kwargs):return generate('easy',**kwargs)
# Observed moderate: forward product, including row/column-vector families.
def generate_moderate(**kwargs):return generate('moderate',**kwargs)
# Observed hard: reverse supplied factor order, same outer-dimension method.
def generate_hard(**kwargs):return generate('hard',**kwargs)

def markdown(rec):
    q=rec['question'];m=rec['generation'];out=[f"Difficulty: {q.get(':question/difficulty','missing source rating')} | Template: {m['template']} | Profile: {m['profile']}",q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        out.append(f"Field {f[':answer-field/key']} ({f[':answer-field/type']})")
        for a in f[':answer-field/choices']:out.append('- '+a[':answer/value']+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''))
        if ':answer-field/correct' not in f:out.append('Correct designation missing in source.')
    out.append(q.get(':question/worked-solution','Worked solution missing in source.'))
    return '\n\n'.join(out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=[*SUPPORTED_LEVELS,'all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');p.add_argument('--template');p.add_argument('--profile');args=p.parse_args()
    levels=SUPPORTED_LEVELS if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
