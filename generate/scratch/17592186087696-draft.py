#!/usr/bin/env python3
"""Local square-recognition draft; immutable math basis2275, no EDB access.

Observed: three independent checkbox decisions and one five-subset radio bank.
Authored moderate/hard retain exactly three decisions and vary only
row/column bookkeeping roles. Their labels are conservative design
claims, not recovered MA levels. Entries never determine square membership.
All public replay uses parameterized recipes; raw incomplete evidence is
ineligible for learning. See the private extraction and validation reports.
"""
import argparse, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_format import matrix_tex,normalize_prose,validate_prose,validate_generated_record,FORMAT_VERSION
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186087696
KP_UUID='3ca13445-0218-5950-967e-a68bcfec32c7'
TITLE='Identifying a Square Matrix'
VERSION='square-recognition-draft-v2'
NS=uuid.UUID(KP_UUID)
SUPPORTED_LEVELS=('easy','moderate','hard')
SUPPORTED_TEMPLATES=('three-checkbox','three-radio')
SOURCE_SHAPES=tuple(itertools.product(range(1,6),repeat=2))
SHAPES=tuple(itertools.product(range(1,9),repeat=2))
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
RADIO_SUBSETS=((0,2),(),(0,1),(1,),(0,))

def parse_matrices(prompt):
    out=[]
    for m in re.finditer(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',prompt,re.S):
        rows=[[x.strip() for x in row.split('&')] for row in m[2].split(r'\\')]
        shape(rows);out.append((m[1],rows))
    if not out:raise ValueError('no labeled matrices')
    return out

def shape(matrix):
    if not isinstance(matrix,list) or not matrix or not isinstance(matrix[0],list) or not matrix[0] or any(not isinstance(row,list) or len(row)!=len(matrix[0]) for row in matrix):raise ValueError('nonrectangular matrix')
    return len(matrix),len(matrix[0])

def parameters_of(q):
    pairs=parse_matrices(q[':question/problem'])
    return {'labels':[l for l,m in pairs],'matrices':[m for l,m in pairs],
            'trailing_space':q[':question/problem'].split('$$')[1].strip().endswith(r'\,') if '$$' in q[':question/problem'] else False,
            'none_instruction':'If none apply' in q[':question/problem'],
            'legacy_plural':'It has $1$ rows' in q.get(':question/worked-solution','')}
SOURCE_PARAMS={sid:parameters_of(q) for sid,q in QS.items()}

def uid(value):return str(uuid.uuid5(NS,json.dumps(value,sort_keys=True,separators=(',',':'))))
def task_fingerprint(p):
    # Multiplicity, row/column orientation and number of assessments matter;
    # letters, order, entries, profile and level aliases do not.
    return hashlib.sha256(json.dumps(['square-membership',sorted(shape(m) for m in p['matrices'])]).encode()).hexdigest()
def subset_text(indices,labels):
    names=['$'+labels[i]+'$' for i in indices]
    if not names:return 'None'
    if len(names)==1:return names[0]+' only'
    return ' and '.join(names)+' only'

def solution_of(p):
    steps=[];chosen=[]
    for label,m in zip(p['labels'],p['matrices']):
        r,c=shape(m);square=r==c
        rows='row' if r==1 and not p.get('legacy_plural',False) else 'rows'
        cols='column' if c==1 and not p.get('legacy_plural',False) else 'columns'
        if square:
            chosen.append(label);reason='is a square matrix since it has the same number of rows and columns.';end='so it is a'
        else:reason='is *not* a square matrix since the numbers of rows and columns are not the same.';end="so it's a"
        steps.append(f'- ${label}$ {reason} It has ${r}$ {rows} and ${c}$ {cols}, {end} ${r}\\times {c}$ matrix.')
    if len(chosen)==len(p['labels']) and len(chosen)>2:conclusion=', '.join('$'+l+'$' for l in chosen[:-1])+', and $'+chosen[-1]+'$ are square matrices.'
    elif len(chosen)>1:conclusion='only '+', '.join('$'+l+'$' for l in chosen[:-1])+' and $'+chosen[-1]+'$ are square matrices.'
    elif len(chosen)==1:conclusion='only $'+chosen[0]+'$ is a square matrix.'
    else:conclusion='none of these matrices are square matrices.'
    return normalize_prose('\n\n'.join(steps)+'\n\nTherefore, '+conclusion)

def prompt_of(p,template):
    pieces=[label+(' = ' if template=='three-radio' else '=')+matrix_tex(matrix) for label,matrix in zip(p['labels'],p['matrices'])]
    if template=='three-radio':return normalize_prose('Which of the following are square matrices?\n$'+', '.join(pieces)+'$')
    prompt='Which of the following are square matrices?\n\n$$\n'+r',\,'.join(pieces)+(r'\,' if p.get('trailing_space',False) else '')+'\n$$\n\nSelect all that apply.'
    if p.get('none_instruction',True):prompt+=' If none apply, leave all boxes unchecked.'
    return normalize_prose(prompt)

def validate_parameters(p,level,template,profile):
    n=3
    if set(p)-{'labels','matrices','trailing_space','none_instruction','legacy_plural'}:raise ValueError('unexpected parameters')
    if len(p['labels'])!=n or len(set(p['labels']))!=n or any(not isinstance(l,str) or not re.fullmatch('[A-Z]',l) for l in p['labels']):raise ValueError('distinct capital labels required')
    if len(p['matrices'])!=n:raise ValueError('incorrect assessment count')
    dims=[]
    for m in p['matrices']:
        dims.append(shape(m))
        if dims[-1] not in SHAPES:raise ValueError('shape outside 1..8 domain')
        if (profile=='observed-checkbox' or template=='three-radio') and dims[-1] not in SOURCE_SHAPES:raise ValueError('source-family shape outside1..5')
        for row in m:
            for x in row:
                if not isinstance(x,str) or not re.fullmatch(r'-?(?:\d+(?:\.\d+)?|\\sqrt\{[1-9]\d*\})',x):raise ValueError('unsupported entry')
                if r'\sqrt' not in x and abs(sp.Rational(x))>10:raise ValueError('entry magnitude beyond observed workload')
                if r'\sqrt' in x and int(re.search(r'\{(\d+)\}',x)[1])>100:raise ValueError('radical entry magnitude beyond observed workload')
    for key in ('trailing_space','none_instruction','legacy_plural'):
        if key in p and not isinstance(p[key],bool):raise ValueError('boolean presentation flag required')
    if template=='three-radio':
        chosen=tuple(i for i,(r,c) in enumerate(dims) if r==c)
        if chosen not in RADIO_SUBSETS:raise ValueError('whole radio bank lacks correct subset')
    if template=='three-checkbox' and profile=='boolean-membership':
        if level=='easy' and (any(max(d)>3 for d in dims) or not any(r==1 for r,c in dims)):raise ValueError('authored easy requires a single row and dimensions at most3')
        if level=='moderate' and (any(min(d)<2 or max(d)>6 for d in dims) or sum(r==c for r,c in dims)!=1 or not any(r!=c and (c,r) in dims for r,c in dims)):raise ValueError('moderate requires one square and a transpose rectangle pair')
        if level=='hard':
            if len({r for r,c in dims})!=1 or not 2<=dims[0][0]<=7 or sorted(c for r,c in dims)[1]!=dims[0][0] or len({c for r,c in dims})!=3:raise ValueError('hard requires shared row count and columns below/equal/above it')

def sample(rng,template,level):
    if template=='three-radio':
        selected=rng.choice(RADIO_SUBSETS);dims=[rng.choice([s for s in SOURCE_SHAPES if (s[0]==s[1])==(i in selected)]) for i in range(3)]
    elif level=='easy':
        dims=[(1,rng.randint(1,3))]+[(rng.randint(1,3),rng.randint(1,3)) for _ in range(2)];rng.shuffle(dims)
    elif level=='moderate':
        r,c=rng.sample(range(2,7),2);dims=[(rng.randint(2,6),)*2,(r,c),(c,r)];rng.shuffle(dims)
    else:
        n=rng.randint(2,7);dims=[(n,rng.randint(1,n-1)),(n,n),(n,rng.randint(n+1,8))];rng.shuffle(dims)
    return {'labels':list('ABCDE'[:len(dims)]),'matrices':[[[str(rng.randint(-5,5)) for _ in range(c)] for _ in range(r)] for r,c in dims],'trailing_space':False,'none_instruction':True,'legacy_plural':False}

# EASY: observed three decisions, both historical field contracts served.
# MODERATE: three decisions, one square and mutually transposed rectangles.
# HARD: three decisions, shared row count and below/equal/above column roles.
def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty')
    rng=random.Random(seed)
    if template is None:
        template=('three-radio' if field_type=='radio' else 'three-checkbox' if field_type=='checkbox' else rng.choice(('three-checkbox','three-radio'))) if level=='easy' else 'three-checkbox'
    if template not in SUPPORTED_TEMPLATES:raise ValueError('unsupported template')
    if template=='three-radio' and level!='easy':raise ValueError('radio observed at authored easy only')
    kind='radio' if template=='three-radio' else 'checkbox'
    if field_type not in (None,kind):raise ValueError('field type mismatch')
    default_profile='authored-subset-bank' if kind=='radio' else 'boolean-membership'
    profile=profile or default_profile
    if profile not in ((default_profile,'observed-radio-raw','completed-observed-radio') if kind=='radio' else (default_profile,'observed-checkbox')):raise ValueError('unsupported complete bank')
    if profile=='observed-checkbox' and level!='easy':raise ValueError('observed checkbox difficulty is easy')
    raw=profile=='observed-radio-raw'
    p=json.loads(json.dumps(parameters)) if parameters is not None else sample(rng,template,level)
    validate_parameters(p,level,template,profile)
    prompt=prompt_of(p,template);solution=solution_of(p)
    if kind=='checkbox':
        specs=[(l,[(v,':answer.type/text') for v in ('false','true')],'true' if shape(m)[0]==shape(m)[1] else 'false') for l,m in zip(p['labels'],p['matrices'])]
    else:
        chosen=tuple(i for i,m in enumerate(p['matrices']) if shape(m)[0]==shape(m)[1]);values=[subset_text(s,p['labels']) for s in RADIO_SUBSETS]
        if len(set(values))!=5:raise ValueError('ambiguous entire subset bank')
        specs=[('selection',[(v,':answer.type/text') for v in values],subset_text(chosen,p['labels']))]
    # Identity depends on displayed content, omissions and full unordered field bank.
    identity=[VERSION,prompt,None if raw else solution,None if raw else level,sorted((key,typ,sorted(bank),None if raw else correct) for key,bank,correct in specs for typ in [kind])]
    qid=uid(identity);fields=[]
    for key,bank,correct in specs:
        fid=uid([qid,key]);answers=[{':answer/id':uid([fid,value,typ]),':answer/type':typ,':answer/value':value} for value,typ in bank]
        rng.shuffle(answers)
        field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
        if not raw:field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]
        fields.append(field)
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':fields}
    if not raw:q.update({':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level})
    record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'level':level,'template':template,'profile':profile,'seed':seed,'parameters':p,'eligible_for_learning':not raw,'evidence_only':raw,'mathematical_fingerprint':task_fingerprint(p),'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_references':['q-7826'] if kind=='radio' else [s for s in QS if s!='q-7826'],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'domains':{'visual_dimension_ceiling':5 if template=='three-radio' or profile=='observed-checkbox' else {'easy':3,'moderate':6,'hard':8}[level],'sample_entries':[-5,5]},'authorship':'observed backbone; authored level bookkeeping constraints' if level!='easy' else 'observed shape-recognition backbone','math_format':FORMAT_VERSION}}
    if raw:validate_prose(prompt)
    else:validate_generated_record(record)
    return record

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+q.get(':question/worked-solution','[Raw evidence: no source worked solution or key.]')+'\n\n'+ '\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in q[':question/answer-fields'])
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',default='easy',choices=(*SUPPORTED_LEVELS,'all'));ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    if a.count<1:ap.error('count must be positive')
    levels=SUPPORTED_LEVELS if a.difficulty=='all' else (a.difficulty,)
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in levels for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
