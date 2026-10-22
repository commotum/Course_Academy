#!/usr/bin/env python3
"""Recognize triangular structure from its complete zero regions.

Normal difficulty permits source-observed 2x2 and 3x3 easy, 3x3 moderate,
and authored 4x4 hard. Every nonempty permitted-side support is eligible
for a non-diagonal triangular matrix. Diagonal contrasts remain
a minority independently of difficulty. Raw source replay preserves original
ratings, fields and prose, is exact-parameter-only, and is evidence-only.

The finite catalog counts dimension and off-diagonal support. Changing
diagonal values, signs, labels or layout never creates another task. Easy has
eighteen structural cases; do not inflate that limit with cosmetic changes.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
import itertools
from functools import lru_cache
from pathlib import Path
import sympy as sp

KP_ID=17592186119771
KP_UUID='1cca9b7c-358a-5f62-9a53-a696df0dd0ff'
TITLE='Describing a Triangular Matrix'
VERSION='triangular-description-3.3-batch-cue-counterexamples'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate','hard')
LABELS=('Identity matrix','Diagonal matrix','Upper triangular matrix','Lower triangular matrix','Other')
FAMILIES={'lower':'Lower triangular matrix','upper':'Upper triangular matrix','diagonal':'Diagonal matrix'}
CRITERION='Choose the most specific listed description: identity before diagonal, and diagonal before upper or lower triangular. Choose Other only if none of these descriptions applies.'
SIZES={'easy':(2,3),'moderate':(3,),'hard':(4,)}
FAMILY_WEIGHTS={'lower':2,'upper':2,'diagonal':1}
DOMAIN={'entries':'integers -10..10 (bool excluded); diagonal entries may be zero',
 'easy':'2x2 or 3x3 upper, lower, or nonidentity diagonal; eighteen finite structural cases',
 'moderate':'3x3; every nonempty permitted-side support is eligible for upper/lower',
 'hard':'4x4; every nonempty permitted-side support is eligible for upper/lower',
 'families':'Independent draws: 40% lower, 40% upper, 20% diagonal. Finite batches balance upper/lower and prefer one diagonal contrast when supply permits; deduplication changes those proportions.',
 'fingerprint':'dimension, family and off-diagonal support only; diagonal unit positions, values, signs, labels, layouts and choice order are incidental',
 'criterion':'Identity > Diagonal > non-diagonal Upper/Lower > Other; normal generation excludes identity and Other'}
DOMAIN['batch_selection']='Prefer cross-family contrasts at each represented size; independently draw incidental entries/letters/orders, rejecting batches with perfect sign/letter cues within a mixed-size group. Explicit tasks, single-family requests and forced finite remainders retain their full support.'


def digest(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(key): return str(uuid.uuid5(uuid.UUID(KP_UUID),key))
def parse_matrix(text):
    """Read actual printed TeX, independently of generation parameters."""
    matches=list(re.finditer(r'([AC])\s*=\s*\[?\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\2\}',text,re.S))
    if len(matches)!=1: raise ValueError('Exactly one complete displayed matrix required')
    m=matches[0]
    rows=[[int(v.strip()) for v in row.split('&')] for row in m[3].split(r'\\')]
    return {'matrix':rows,'letter':m[1],'layout':m[2]}

def classify(matrix):
    M=sp.Matrix(matrix)
    if M==sp.eye(M.rows): return LABELS[0]
    if M.is_diagonal(): return LABELS[1]
    if M.is_upper: return LABELS[2]
    if M.is_lower: return LABELS[3]
    return LABELS[4]

def family(matrix):
    result=classify(matrix)
    if result not in FAMILIES.values(): raise ValueError('Normal family excludes identity and Other')
    return next(k for k,v in FAMILIES.items() if v==result)

def validate_parameters(parameters):
    if not isinstance(parameters,dict) or set(parameters)!={'matrix','letter','layout'}: raise ValueError('Expected matrix, letter, layout')
    matrix=parameters['matrix']
    if not isinstance(matrix,(list,tuple)) or len(matrix) not in (2,3,4): raise ValueError('Square size 2, 3 or 4 required')
    n=len(matrix)
    if any(not isinstance(row,(list,tuple)) or len(row)!=n for row in matrix): raise ValueError('Nonsquare matrix')
    if any(type(v)!=int or abs(v)>10 for row in matrix for v in row): raise ValueError('Bounded integer entries required')
    if parameters['letter'] not in ('A','C') or parameters['layout'] not in ('aligned','bmatrix'): raise ValueError('Unknown letter/layout')
    return {'matrix':[list(row) for row in matrix],'letter':parameters['letter'],'layout':parameters['layout']}

def level_guard(level,p,template):
    n=len(p['matrix']); actual=family(p['matrix'])
    if template!=actual: raise ValueError('Requested family differs from the actual matrix')
    if n not in SIZES[level]: raise ValueError(f'{level} requires a square size in {SIZES[level]}')
    # family() already distinguishes nonempty one-sided supports from diagonal.
    # The lesson permits zero at every other position on the allowed side.

def semantic_object(matrix):
    n=len(matrix)
    kind=family(matrix)
    states=[['D' if i==j else '0' if v==0 else 'N' for j,v in enumerate(row)] for i,row in enumerate(matrix)]
    return {'n':n,'family':kind,'states':states,'scanned_region_entries':n*(n-1) if kind=='diagonal' else n*(n-1)//2}

def task_key(matrix): return digest(semantic_object(matrix))

@lru_cache(maxsize=None)
def catalog(level,template=None):
    """Enumerate finite meaningful patterns; do not count arbitrary integers."""
    if level not in SUPPORTED_LEVELS: raise ValueError('Unknown level')
    families=tuple(FAMILIES)
    if template is not None:
        if template not in families: raise ValueError('Template outside level')
        families=(template,)
    dimensions=SIZES[level]
    result=[]
    for n in dimensions:
        for kind in families:
            cells=[(i,j) for i in range(n) for j in range(n) if (i>j if kind=='lower' else i<j)] if kind!='diagonal' else []
            for mask in range(1,1<<len(cells)) if cells else (0,):
                matrix=[[0]*n for _ in range(n)]
                for i in range(n): matrix[i][i]=2
                for k,(i,j) in enumerate(cells): matrix[i][j]=2 if mask & (1<<k) else 0
                result.append((kind,tuple(tuple(r) for r in matrix)))
    return tuple(result)

def sample_parameters(level,template,rng):
    if template is None:
        template=rng.choices(tuple(FAMILY_WEIGHTS),tuple(FAMILY_WEIGHTS.values()))[0]
    kind,pattern=rng.choice(catalog(level,template))
    return kind,fill_pattern(kind,pattern,rng)

def fill_pattern(kind,pattern,rng):
    nonzero=tuple(v for v in range(-10,11) if v!=0)
    matrix=[[rng.randint(-10,10) if i==j else rng.choice(nonzero) if v else 0
             for j,v in enumerate(row)] for i,row in enumerate(pattern)]
    while kind=='diagonal' and all(matrix[i][i]==1 for i in range(len(matrix))):
        for i in range(len(matrix)): matrix[i][i]=rng.randint(-10,10)
    return {'matrix':matrix,'letter':rng.choice(('A','C')),'layout':'bmatrix'}

def render(p,display=False):
    body=r' \\ '.join(' & '.join(map(str,row)) for row in p['matrix'])
    if display: return '$$\n'+p['letter']+r' = \begin{bmatrix}'+body+r'\end{bmatrix}'+'\n$$'
    if p['layout']=='bmatrix': return '$'+p['letter']+r' = \begin{bmatrix}'+body+r'\end{bmatrix}$'
    return '$$\n'+p['letter']+r'=[\begin{aligned}'+body+r'\end{aligned}]'+'\n$$'

def prompt(p,normal=True):
    prefix='How can we best describe the following matrix?'+(' \n\n' if p['layout']=='aligned' else '\n\n')
    return prefix+render(p,display=normal)+('\n\n'+CRITERION if normal else '')

def solution(p,template,normal=True):
    """The source region/prose, repeated matrix, then a concrete derived witness."""
    letter=p['letter']; region={'lower':'above','upper':'below','diagonal':'above and below'}[template]
    result=f"Notice that ${letter}$ is a matrix for which all entries {region} the diagonal are $0$'s:\n\n"+render(p,display=normal)
    result+=f'\n\nTherefore, it is {"an" if template=="upper" else "a"} {FAMILIES[template].lower()}.'
    if template!='diagonal':
        cells=[(i,j) for i,row in enumerate(p['matrix']) for j,v in enumerate(row) if v and (i>j if template=='lower' else i<j)]
        i,j=cells[0]; opposite='upper' if template=='lower' else 'lower'; value=p['matrix'][i][j]
        result+=f'\n\nIt is not {"an" if opposite=="upper" else "a"} {opposite} triangular matrix or a diagonal matrix since there is a non-zero element {"below" if template=="lower" else "above"} the diagonal: ${{{letter.lower()}}}_{{{i+1}{j+1}}}={value}'+r'\ne 0.$'
    return result

def enum(value): return value[':db/ident'] if isinstance(value,dict) else value

def source_levels(source_id):
    q=SOURCES[source_id]
    return enum(q.get(':question/difficulty',':question.difficulty/easy')).split('/')[-1]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in SUPPORTED_LEVELS: raise ValueError('Unknown level')
    if type(seed)!=int: raise ValueError('Seed must be an integer')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only observed radio shape is supported')
    if profile is not None and not isinstance(profile,str): raise ValueError('Profile must be a string')
    profile='five-labels' if profile is None else profile
    raw=profile.startswith('raw:'); source_id=profile.split(':',1)[1] if raw or profile.startswith('source:') else None
    if profile!='five-labels' and source_id not in SOURCES: raise ValueError('Unknown complete bank profile')
    if raw and source_levels(source_id)!=level: raise ValueError('Raw source profile/level mismatch')
    rng=random.Random(seed)
    if parameters is None:
        if source_id: raise ValueError('Source evidence profiles require explicit matrix parameters')
        template,p=sample_parameters(level,template,rng)
    else:
        p=validate_parameters(parameters)
        template=template or family(p['matrix'])
    p=validate_parameters(p)
    if source_id:
        anchor=parse_matrix(SOURCES[source_id][':question/problem'])
        if raw and p!=anchor: raise ValueError('Raw evidence replay requires the exact source parameters')
        if len(p['matrix'])!=len(anchor['matrix']): raise ValueError('Source recipe dimension mismatch')
        if template!=family(anchor['matrix']): raise ValueError('Source family mismatch')
    if not raw:
        level_guard(level,p,template)
        p['layout']='bmatrix'
    answer=FAMILIES[template]; problem=prompt(p,not raw); worked=solution(p,template,not raw)
    q={':question/problem':problem}
    if raw:
        original=SOURCES[source_id]
        for key,value in original.items():
            if key not in (':question/problem',':question/worked-solution',':question/answer-fields',':question/id'):
                q[key]=enum(value) if key==':question/difficulty' else copy.deepcopy(value)
        if ':question/worked-solution' in original: q[':question/worked-solution']=worked
    else:
        q[':question/difficulty']=':question.difficulty/'+level
        q[':question/worked-solution']=worked
    if raw:
        bank_spec=[{'values':[a[':answer/value'] for a in f[':answer-field/choices']], 'correct_present':':answer-field/correct' in f,'key':f.get(':answer-field/key')} for f in SOURCES[source_id][':question/answer-fields']]
    else: bank_spec=[{'values':sorted(LABELS),'correct_present':True,'key':'selection'}]
    content=digest({'version':VERSION,'problem':problem,'solution':q.get(':question/worked-solution'),'solution_present':':question/worked-solution' in q,'difficulty':q.get(':question/difficulty'),'banks':[dict(b,values=sorted(b['values'])) for b in bank_spec]})
    qid=uid('question:'+content);q[':question/id']=qid
    fields=[]
    original_fields=SOURCES[source_id][':question/answer-fields'] if raw else [None]
    for index,original in enumerate(original_fields):
        fid=uid(qid+':field:'+str(index))
        f={k:copy.deepcopy(v) for k,v in original.items() if k not in (':answer-field/choices',':answer-field/correct',':answer-field/id',':answer-field/type')} if original else {':answer-field/key':'selection'}
        f[':answer-field/id']=fid;f[':answer-field/type']=':answer-field.type/radio'
        original_choices=original[':answer-field/choices'] if original else [{':answer/value':value} for value in LABELS]
        choices=[]
        for a in original_choices:
            item={k:copy.deepcopy(v) for k,v in a.items() if k not in (':answer/id',':answer/type')}
            item[':answer/id']=uid(fid+':answer:'+item[':answer/value']);item[':answer/type']=':answer.type/text';choices.append(item)
        if not raw or ':answer-field/correct' in original:
            f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==answer)]
        random.Random(seed+index).shuffle(choices);f[':answer-field/choices']=choices;fields.append(f)
    q[':question/answer-fields']=fields
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
        'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':template,'parameters':p,
        'bank_profile':profile,'recipes':list(LABELS),'parameter_fingerprint':task_key(p['matrix']),'content_fingerprint':content,
        'domain':DOMAIN,'source_database':SOURCE['database'],'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],
        'source_id':source_id,'difficulty_origin':'original captured rating or absence' if raw else 'source-observed 2x2/3x3 easy; 3x3 moderate; authored 4x4 hard scan workload',
        'evidence_only':raw,'eligible_for_learning':not raw,'plot_rating':'none',
        'repairs':[] if raw else ['explicit most-specific criterion']+(['single radio field confirmed by authoritative MA widget'] if source_id=='q-13759' else ['inferred correct ref and authored solution/rating'] if source_id=='q-13769' else []),
        'catalog_count':len(catalog(level))}}

# EASY: source-observed 2x2 and 3x3, eighteen structural cases.
def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)
# MODERATE: 3x3, all three families and every permitted-side support.
def generate_moderate(seed=0,**kwargs): return generate('moderate',seed,**kwargs)
# HARD: authored 4x4 same recognition method, bounded longer region scan.
def generate_hard(seed=0,**kwargs): return generate('hard',seed,**kwargs)

def select_patterns(available,chosen,rng):
    """Allocate sizes before supports, avoiding preventable size-only answers.

    Easy has two dimensions and at most one 2x2 task per family, so this
    enumeration is small. A forced finite remainder is retained in full.
    """
    dimensions=sorted({len(p) for pool in available.values() for p in pool})
    counts={kind:chosen.count(kind) for kind in FAMILIES}
    pools={(kind,n):[p for p in available[kind] if len(p)==n]
           for kind in FAMILIES for n in dimensions}
    allocations=[]
    for kind in FAMILIES:
        allocations.append([allocation for allocation in itertools.product(
            *(range(min(counts[kind],len(pools[kind,n]))+1) for n in dimensions))
            if sum(allocation)==counts[kind]])
    plans=list(itertools.product(*allocations))
    def score(plan):
        # No arbitrary proportion: penalize a size that alone reveals its key.
        return sum(sum(row[j]>0 for row in plan)==1 for j in range(len(dimensions)))
    best=min(map(score,plans));plan=rng.choice([p for p in plans if score(p)==best])
    selected=[]
    for kind,allocation in zip(FAMILIES,plan):
        for n,count in zip(dimensions,allocation):
            selected.extend((kind,p) for p in rng.sample(pools[kind,n],count))
    rng.shuffle(selected)
    return selected

def batch_has_counterexamples(records):
    """Check joint incidental cues within every mixed-size practice group.

    Conditioning selection on counterexamples does not assign a sign to a
    family or remove any accepted parameter value. This is a batch property.
    """
    groups={}
    positions=set()
    size_positions={}
    orientation_order={}
    for r in records:
        p=r['generation']['parameters'];m=p['matrix'];kind=r['generation']['template']
        cue=((m[0][0]>0)-(m[0][0]<0),p['letter'])
        groups.setdefault(len(m),[]).append((kind,cue))
        f=r['question'][':question/answer-fields'][0]
        position=next(i for i,a in enumerate(f[':answer-field/choices'])
                      if a[':answer/id']==f[':answer-field/correct'][1])
        positions.add(position)
        size_positions.setdefault(len(m),set()).add(position)
        if kind in ('upper','lower'):
            first=next(a[':answer/value'] for a in f[':answer-field/choices']
                       if a[':answer/value'] in (FAMILIES['upper'],FAMILIES['lower']))
            orientation_order.setdefault(len(m),[]).append(first==FAMILIES[kind])
    for n,group in groups.items():
        kinds={kind for kind,cue in group}
        if len(kinds)<2: continue  # Forced remainder or explicit family.
        if len(size_positions[n])<2: return False
        if {'upper','lower'}<=kinds and len(set(orientation_order[n]))<2: return False
        contrast=[(kind,cue) for kind,cue in group if kind in ('upper','lower')]
        if not {'upper','lower'}<=kinds: contrast=group
        if not any(k1!=k2 and c1==c2 for k1,c1 in contrast for k2,c2 in contrast):
            return False
    return len({r['generation']['template'] for r in records})<2 or len(positions)>1

def batch(level,count,seed=0,exclude_fingerprints=(),**kwargs):
    """Choose unique structures before incidental numbers and answer order.

    Family proportions cannot stay 40/40/20 in a finite catalog with only one
    diagonal structure. Prefer one diagonal in batches of 3+, balance upper
    and lower as supply permits, and report exhaustion instead of duplicates.
    Callers may supply existing structural fingerprints before quota selection.
    """
    if type(count)!=int or count<1: raise ValueError('Positive integer count required')
    if type(seed)!=int: raise ValueError('Seed must be an integer')
    excluded=set(exclude_fingerprints)
    if kwargs.get('parameters') is not None or kwargs.get('profile','five-labels') not in (None,'five-labels'):
        if count!=1: raise ValueError('One explicit/source task cannot supply a distinct batch')
        rec=generate(level,seed,**kwargs)
        if rec['generation']['parameter_fingerprint'] in excluded: raise ValueError('Explicit structural task was excluded')
        return [rec]
    available={kind:[] for kind in FAMILIES}
    for kind,pattern in catalog(level,kwargs.get('template')):
        if task_key(pattern) not in excluded: available[kind].append(pattern)
    total=sum(map(len,available.values()))
    if count>total:
        raise ValueError(f'{level} has only {total} available structural tasks ({len(catalog(level))} total); requested {count}. Numeric changes do not create fresh tasks.')
    rng=random.Random(seed)
    if count==1:
        kinds=[kind for kind in available if available[kind]]
        chosen=[rng.choices(kinds,[FAMILY_WEIGHTS[k] for k in kinds])[0]]
    elif kwargs.get('template'):
        chosen=[kwargs['template']]*count
    else:
        plans=[(lower,count-lower-diagonal,diagonal)
               for diagonal in range(min(len(available['diagonal']),count)+1)
               for lower in range(min(count,len(available['lower']))+1)
               if 0<=count-lower-diagonal<=len(available['upper'])]
        if not plans: raise ValueError('Remaining structural supply cannot provide the requested batch')
        desired_diagonal=int(count>=3 and bool(available['diagonal']))
        score=lambda p:(abs(p[2]-desired_diagonal),abs(p[0]-p[1]))
        best=min(map(score,plans));plan=rng.choice([p for p in plans if score(p)==best])
        chosen=[kind for kind,n in zip(FAMILIES,plan) for _ in range(n)]
        rng.shuffle(chosen)
    selected=select_patterns(available,chosen,rng)
    for attempt in range(4096):
        result=[]
        for kind,pattern in selected:
            p=fill_pattern(kind,pattern,rng)
            args={**kwargs,'template':kind,'parameters':p}
            record=generate(level,rng.getrandbits(64),**args)
            record['generation']['batch_seed']=seed
            record['generation']['batch_selection_attempt']=attempt
            result.append(record)
        if batch_has_counterexamples(result): return result
    raise ValueError('Could not construct incidental-cue counterexamples for this batch')

def markdown(record):
    q=record['question'];pieces=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        ref=f.get(':answer-field/correct',[':answer/id',None])[1]
        pieces.append('\n'.join(('- [x] ' if a[':answer/id']==ref else '- [ ] ')+a[':answer/value'] for a in f[':answer-field/choices']))
    if ':question/worked-solution' in q:pieces.append(q[':question/worked-solution'])
    return '\n\n'.join(pieces)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='json');parser.add_argument('--template',choices=tuple(FAMILIES));parser.add_argument('--profile');parser.add_argument('--parameters',type=json.loads)
    args=parser.parse_args();levels=SUPPORTED_LEVELS if args.difficulty=='all' else (args.difficulty,)
    records=[r for level in levels for r in batch(level,args.count,args.seed,template=args.template,profile=args.profile,parameters=args.parameters)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__': main()
