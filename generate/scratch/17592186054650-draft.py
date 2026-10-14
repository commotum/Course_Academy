#!/usr/bin/env python3
"""Local, unregistered draft: parameterized six-entry non-square matrix addition.

Every historical bank is public evidence replay (source:<MA-id>), never a default.
Normal questions select a source-shaped family and a COMPLETE method bank before
sampling operands. Missing M/H levels are conservative authored workload claims;
see private template-extraction.md. Nothing reads or writes the live database.
"""
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import matrix_tex, normalize_prose, normalize_tex, validate_prose, validate_tex
HERE = Path(__file__).with_suffix('')
S = json.loads((HERE / 'source.json').read_text())
KP_ID = 17592186054650
KP_UUID = S['record'][':knowledge-point/id']
VERSION = '2.0.0-draft'
SOURCES = {q[':question/math-academy-id']: q for q in S['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
TEMPLATES = tuple(SOURCES)
LEVELS = ('easy', 'moderate', 'hard')
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
PROFILES = ('method-omission', 'method-sign')

def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def uid(parent, value):
    return str(uuid.uuid5(uuid.UUID(parent), str(value)))

def rows(body):
    return [[x.strip() for x in row.split('&')] for row in body.split(r'\\')]

def matrices(text):
    return [[[int(x) for x in row] for row in rows(body)] for body in MATRIX.findall(text)]

def flat(m):
    return [x for row in m for x in row]

def original(t):
    a, b = matrices(SOURCES[t][':question/problem'])
    return {'a': flat(a), 'b': flat(b)}

def shape(t):
    a, b = matrices(SOURCES[t][':question/problem'])
    return len(a), len(a[0])

def tex(values, nc):
    return matrix_tex([values[i:i + nc] for i in range(0, len(values), nc)])

def sums(p):
    return [int(x) for x in sp.Matrix(p['a']) + sp.Matrix(p['b'])]

# Historical bank recipes: exact full profiles, never infer arbitrary residuals
# as learner error mechanisms. Unknown source residual vectors are evidence-only.
def historical_bank(t, p):
    a, b = p['a'], p['b']; c = sums(p)
    def changed(updates):
        d = c.copy()
        for i, value in updates.items(): d[i] = value
        return d
    if t == 'q-103':
        return [changed({2:a[2]-b[2],5:-c[5]}),c,changed({3:-a[3]+b[3],5:-c[5]}),changed({0:-c[0],4:-a[4]+b[4]}),changed({1:-c[1],2:-c[2]})]
    if t == 'q-105':
        return [changed({0:-c[0],4:c[4]+12}),c,changed({4:c[4]+12,5:-c[5]}),changed({1:-c[1],4:c[4]+12}),changed({3:-c[3],4:c[4]+12})]
    if t == 'q-125722':
        return [c,changed({0:b[0],1:a[1]}),changed({2:a[4],5:c[2]}),changed({4:b[4]-a[4],5:b[5]-a[5]}),changed({2:a[3]})]
    if t == 'q-69622':
        return [[x+d for x,d in zip(c,delta)] for delta in ([-2,-1,-3,-4,-1,-10],[0,8,-6,1,0,-15],[0,0,-3,-11,0,-10],[4,0,-4,8,0,-11],[0,0,0,0,0,0])]
    if t == 'q-69635':
        return [changed({3:c[3]+6,4:-c[4],5:-c[5]}),changed({0:a[0]-b[0],2:-c[2],5:a[5]-b[5]}),c,changed({2:c[2]-10,3:c[3]+5,4:-c[4],5:-c[5]}),changed({2:-c[2],3:c[3]+28,5:-c[5]})]
    if t == 'q-106':
        return [changed({3:-c[3]}),c,changed({1:-c[1]}),changed({5:-a[4]+b[4]}),changed({1:-c[1],4:-c[4]})]
    if t == 'q-319601': return None
    raise ValueError('Unknown source family')

# Complete authored operation banks. Selection precedes operand sampling.
# Every wrong matrix is a real omission or sign reversal of displayed addends.
def method_bank(profile, p):
    a,b,c = p['a'],p['b'],sums(p)
    if profile == 'method-omission':
        return [c, a.copy(), b.copy(), [x-y for x,y in zip(a,b)], [y-x for x,y in zip(a,b)]]
    if profile == 'method-sign':
        return [c, [-x for x in c], [x-y for x,y in zip(a,b)], [y-x for x,y in zip(a,b)], [abs(x)+abs(y) for x,y in zip(a,b)]]
    raise ValueError('Unknown complete method bank')

def validate_parameters(p, level, evidence=False):
    if set(p) != {'a','b'} or any(not isinstance(p[k],list) or len(p[k]) != 6 for k in p):
        raise ValueError('Six corresponding entries in each operand required')
    if any(type(x) is not int for k in p for x in p[k]): raise ValueError('Integer entries required')
    a,b=p['a'],p['b']; opposite=sum(x*y<0 for x,y in zip(a,b))
    if evidence:
        if any(abs(x)>16 for x in a+b): raise ValueError('Historical evidence bound is 16')
        return
    if level == 'easy':
        if any(abs(x)>9 for x in a+b) or opposite>2: raise ValueError('Authored easy: magnitude <=9, at most two opposite-sign pairs')
    elif level == 'moderate':
        if any(x==0 or abs(x)>16 for x in a+b) or opposite!=3 or sum(x<0 and y<0 for x,y in zip(a,b))!=3:
            raise ValueError('Authored moderate: three negative-negative and three opposite-sign pairs, nonzero magnitude <=16')
    elif level == 'hard':
        if any(not 10<=abs(x)<=16 for x in a+b) or opposite!=6 or any(x+y==0 for x,y in zip(a,b)) or not (min(sums(p))<0<max(sums(p))):
            raise ValueError('Authored hard: six two-digit opposite-sign pairs, nonzero sums of both signs')
    else: raise ValueError('Unknown level')

def sample(rng, level):
    if level == 'easy':
        opposite=set(rng.sample(range(6),rng.randint(0,2)))
        a=[];b=[]
        for j in range(6):
            sign=rng.choice([-1,1]);a.append(sign*rng.randint(1,9));b.append((-sign if j in opposite else sign)*rng.randint(1,9))
    elif level == 'moderate':
        opposite=set(rng.sample(range(6),3));a=[];b=[]
        for j in range(6):
            sign=rng.choice([-1,1]) if j in opposite else -1
            a.append(sign*rng.randint(1,16));b.append((-sign if j in opposite else -1)*rng.randint(1,16))
    else:
        a=[rng.choice([-1,1])*rng.randint(10,16) for _ in range(6)]
        b=[(-1 if x>0 else 1)*rng.randint(10,16) for x in a]
    return {'a':a,'b':b}

def render_prompt(t,p,nc):
    replacements=iter([tex(p['a'],nc),tex(p['b'],nc)])
    return MATRIX.sub(lambda _:next(replacements),SOURCES[t][':question/problem'])

def render_solution(t,p,nc):
    a,b,c=p['a'],p['b'],sums(p)
    def first(x): return '('+str(x)+')' if t=='q-125722' and x<0 else str(x)
    entry_sums=[first(x)+'+'+('('+str(y)+')' if y<0 else str(y)) for x,y in zip(a,b)]
    replacements=[tex(a,nc),tex(b,nc),tex(entry_sums,nc),tex(c,nc)]
    source=SOURCES[t]
    if ':question/worked-solution' in source:
        # Source operative order is encoded by complete matrices: operand A,
        # operand B, six unevaluated component sums, six evaluated component sums.
        iterator=iter(replacements)
        return MATRIX.sub(lambda _:next(iterator),source[':question/worked-solution'])
    lhs=tex(a,nc)+'+'+tex(b,nc) if t=='q-103' else 'X+Y'
    initial=lhs+' & ='+tex(entry_sums,nc) if t=='q-103' else lhs+' & ='+tex(a,nc)+'+'+tex(b,nc)+r' \\  & ='+tex(entry_sums,nc)
    return 'We add the corresponding entries:\n\n$$\n'+r'\begin{aligned}'+initial+r' \\  & ='+tex(c,nc)+r'\end{aligned}'+'\n$$'

def canonical_profile(profile,t):
    if profile in (None,'method','authored-method'): return 'method-omission'
    if profile in PROFILES: return profile
    if profile in ('source','observed'): return 'source:'+t
    if profile in ('source-completed','observed-completed'): return 'source-completed:'+t
    if profile in ('source:'+t,'source-completed:'+t): return profile
    raise ValueError('Unknown profile or source/profile mismatch')

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS: raise ValueError('Difficulty must be easy, moderate or hard')
    rng=random.Random(seed)
    if template is None:
        families=[t for t in TEMPLATES if field_type is None or ('blank' if t=='q-319601' else 'radio')==field_type.removeprefix(':answer-field.type/')]
        if not families: raise ValueError('Unsupported field type')
        t=rng.choice(families)
    else:
        t=template
        if t not in SOURCES: raise ValueError('Unknown template')
    actual_type='blank' if t=='q-319601' else 'radio'
    if field_type is not None and field_type.removeprefix(':answer-field.type/')!=actual_type: raise ValueError('Field contract mismatch')
    # Default bank is chosen independently and BEFORE parameters.
    prof=canonical_profile(profile,t) if profile is not None else rng.choice(PROFILES)
    evidence=prof.startswith('source');raw=prof.startswith('source:')
    if evidence and level!='easy': raise ValueError('Historical originals only have easy or omitted difficulty')
    nr,nc=shape(t)
    if parameters is None and evidence: raise ValueError('Evidence replay requires explicit parameters')
    def bank_for(p): return historical_bank(t,p) if evidence else (None if actual_type=='blank' else method_bank(prof,p))
    if parameters is not None:
        p=copy.deepcopy(parameters);validate_parameters(p,level,evidence);values=bank_for(p)
        if values is not None and len({tuple(v) for v in values})!=5: raise ValueError('Whole bank collision')
    else:
        for _ in range(2000):
            p=sample(rng,level)
            try: validate_parameters(p,level)
            except ValueError: continue
            values=bank_for(p)
            if values is None or len({tuple(v) for v in values})==5: break
        else: raise ValueError('No eligible complete bank found')
    prompt=normalize_prose(render_prompt(t,p,nc));solution=normalize_prose(render_solution(t,p,nc));c=sums(p)
    source=SOURCES[t];field_specs=[]
    for sf in source[':question/answer-fields']:
        key=sf[':answer-field/key']
        strings=[normalize_tex(tex(v,nc)) for v in values] if actual_type=='radio' else [str(c[int(key.split('-')[1])-1])]
        correct=tex(c,nc) if actual_type=='radio' else strings[0]
        include_correct=not raw or ':answer-field/correct' in sf
        field_specs.append((key,strings,correct,include_correct))
    shown_difficulty=not raw or ':question/difficulty' in source
    shown_solution=not raw or ':question/worked-solution' in source
    # No template/profile/seed aliases in identity; complete displayed semantics.
    content={'version':VERSION,'problem':prompt,'difficulty':level if shown_difficulty else None,'solution':solution if shown_solution else None,
             'fields':sorted((key,actual_type,sorted(v),correct if inc else None) for key,v,correct,inc in field_specs)}
    ident=uid(KP_UUID,digest(content));fields=[]
    for key,strings,correct,include_correct in field_specs:
        fid=uid(ident,key)
        answers=[{':answer/id':uid(fid,v),':answer/type':':answer.type/math',':answer/value':v} for v in strings]
        if actual_type=='radio': rng.shuffle(answers)
        field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+actual_type,':answer-field/choices':answers}
        if include_correct: field[':answer-field/correct']=[':answer/id',uid(fid,correct)]
        fields.append(field)
    q={':question/id':ident,':question/problem':prompt,':question/answer-fields':fields}
    if shown_difficulty: q[':question/difficulty']=':question.difficulty/'+level
    if shown_solution: q[':question/worked-solution']=solution
    validate_prose(prompt)
    if shown_solution: validate_prose(solution)
    for f in fields:
        for answer in f[':answer-field/choices']: validate_tex(answer[':answer/value'])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},'question':q,
            'generation':{'version':VERSION,'seed':seed,'template':t,'profile':prof,'parameters':p,'source_id':source[':question/math-academy-id'],'source_db_id':source[':db/id'],'source_basis':S['basis'],'source_lineage':S['lineage'],
                          'authorship':'observed evidence replay' if raw else ('authored completion of historical evidence' if evidence else 'authored method-bank extension; source-shaped backbone'),
                          'evidence_only':evidence,'eligible_for_learning':not evidence,'raw_replay':raw,'difficulty_boundary':'observed easy/omitted' if evidence else 'authored, uncertain relative calibration',
                          'mathematical_fingerprint':digest({'shape':[nr,nc],'operands':sorted([p['a'],p['b']])}),'content_fingerprint':digest(content),'assets':[],
                          'dependency_versions':{'python':sys.version.split()[0],'sympy':sp.__version__},'math_format':'course-academy-tex-v1'}}

# EASY: six small integer additions; at most two opposite-sign pairs. Original
# labels are preserved separately even when original arithmetic exceeds this.
def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)

# MODERATE (authored): six signed additions, exactly three negative-negative and
# three opposed-sign pairs. Operand magnitude <=16; no zero operands.
def generate_moderate(seed=0,**kwargs): return generate('moderate',seed,**kwargs)

# HARD (authored): six two-digit opposed-sign additions, nonzero outcomes of both
# signs. No new matrix operation, target, operator, or extra solution stage.
def generate_hard(seed=0,**kwargs): return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];parts=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        parts.append(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']))
    if ':question/worked-solution' in q: parts.append(q[':question/worked-solution'])
    return '\n\n'.join(parts)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--template');parser.add_argument('--profile');parser.add_argument('--format',choices=('markdown','json'),default='json')
    args=parser.parse_args();levels=LEVELS if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
