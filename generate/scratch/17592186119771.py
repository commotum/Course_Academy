#!/usr/bin/env python3
"""Best description of a square triangular matrix, math snapshot basis 1356.

Easy: observed strict upper/lower 2x2 and 3x3. Moderate: observed nonidentity
3x3 diagonal. Hard: authored 4x4 versions of these same three families; the
extra entries enlarge the same zero-region scan, without matrix operations.
All normal profiles use the complete five-label radio bank and state the
most-specific-description criterion. Raw source profiles retain both legacy
fields and missing attributes; they are evidence-only and publicly replayable.

Meaningful catalog: strict triangular entries use only off-diagonal support;
diagonal tasks retain unit/nonunit diagonal positions for the identity check. Magnitudes, signs, names, layouts,
profiles and choice order do not inflate task counts. Normal sampling chooses
an unordered eligible structural pattern, then harmless bounded integer values.
No EDB clients, transactions, renderer, installs, or registration.
"""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, random, re, sys, uuid
from functools import lru_cache
from pathlib import Path
import sympy as sp

KP_ID=17592186119771
KP_UUID='1cca9b7c-358a-5f62-9a53-a696df0dd0ff'
TITLE='Describing a Triangular Matrix'
VERSION='triangular-description-2.0'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate','hard')
LABELS=('Identity matrix','Diagonal matrix','Upper triangular matrix','Lower triangular matrix','Other')
FAMILIES={'lower':'Lower triangular matrix','upper':'Upper triangular matrix','diagonal':'Diagonal matrix'}
CRITERION='Choose the most specific listed description: identity before diagonal, and diagonal before upper or lower triangular. Choose Other only if none of these descriptions applies.'
DOMAIN={'entries':'integers -9..9 (bool excluded)', 'easy':'strict upper/lower, square size 2 or 3',
 'moderate':'nonidentity diagonal, square size 3, including zero diagonal entries and the zero matrix',
 'hard':'authored strict upper/lower or nonidentity diagonal, square size 4',
 'fingerprint':'dimension and off-diagonal support for strict triangular; unit/nonunit diagonal mask for diagonal; fixed region-scan demand. Strict diagonal entries and all magnitudes/signs/labels/layouts/profiles/orders are incidental',
 'criterion':'Identity > Diagonal > the unique strict Upper/Lower > Other; zero square matrix is Diagonal in the available bank'}


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
    if any(type(v)!=int or abs(v)>9 for row in matrix for v in row): raise ValueError('Bounded integer entries required')
    if parameters['letter'] not in ('A','C') or parameters['layout'] not in ('aligned','bmatrix'): raise ValueError('Unknown letter/layout')
    return {'matrix':[list(row) for row in matrix],'letter':parameters['letter'],'layout':parameters['layout']}

def level_guard(level,p,template):
    n=len(p['matrix']); actual=family(p['matrix'])
    if template!=actual: raise ValueError('Requested family differs from the actual matrix')
    if level=='easy' and not (n in (2,3) and actual in ('lower','upper')): raise ValueError('Easy workload bounds')
    if level=='moderate' and not (n==3 and actual=='diagonal'): raise ValueError('Moderate workload bounds')
    if level=='hard' and not n==4: raise ValueError('Hard workload bounds: 4x4 only')

def semantic_object(matrix):
    n=len(matrix)
    kind=family(matrix)
    states=[['D' if i==j and kind!='diagonal' else '1' if i==j and v==1 else 'N' if i==j else '0' if v==0 else 'N' for j,v in enumerate(row)] for i,row in enumerate(matrix)]
    return {'n':n,'family':kind,'states':states,'scanned_region_entries':n*(n-1) if kind=='diagonal' else n*(n-1)//2}

def task_key(matrix): return digest(semantic_object(matrix))

@lru_cache(maxsize=None)
def catalog(level,template=None):
    """Enumerate finite meaningful patterns; do not count arbitrary integers."""
    if level not in SUPPORTED_LEVELS: raise ValueError('Unknown level')
    families=('lower','upper') if level=='easy' else ('diagonal',) if level=='moderate' else tuple(FAMILIES)
    if template is not None:
        if template not in families: raise ValueError('Template outside level')
        families=(template,)
    dimensions=(2,3) if level=='easy' else (3,) if level=='moderate' else (4,)
    result=[]
    for n in dimensions:
        for kind in families:
            cells=[(i,j) for i in range(n) for j in range(n) if (i>j if kind=='lower' else i<j)] if kind!='diagonal' else []
            for diag in itertools.product((0,1),repeat=n) if kind=='diagonal' else [(0,)*n]:
                for mask in range(1,1<<len(cells)) if cells else (0,):
                    if kind=='diagonal' and all(x==1 for x in diag): continue
                    matrix=[[0]*n for _ in range(n)]
                    for i,x in enumerate(diag): matrix[i][i]=x
                    for k,(i,j) in enumerate(cells): matrix[i][j]=2 if mask & (1<<k) else 0
                    result.append((kind,tuple(tuple(r) for r in matrix)))
    return tuple(result)

def sample_parameters(level,template,rng):
    kind,pattern=rng.choice(catalog(level,template))
    nonunit=tuple(v for v in range(-9,10) if v!=1)
    nonzero=tuple(v for v in range(-9,10) if v!=0)
    matrix=[[rng.randint(-9,9) if i==j and kind!='diagonal' else rng.choice(nonunit) if i==j and v==0 else rng.choice(nonzero) if v==2 else v for j,v in enumerate(row)] for i,row in enumerate(pattern)]
    layout='bmatrix' if level=='easy' and kind=='lower' and len(pattern)==3 and rng.choice((False,True)) else 'aligned'
    return kind,{'matrix':matrix,'letter':rng.choice(('A','C')),'layout':layout}

def render(p):
    body=r' \\ '.join(' & '.join(map(str,row)) for row in p['matrix'])
    if p['layout']=='bmatrix': return '$'+p['letter']+r' = \begin{bmatrix}'+body+r'\end{bmatrix}$'
    return '$$\n'+p['letter']+r'=[\begin{aligned}'+body+r'\end{aligned}]'+'\n$$'

def prompt(p,normal=True):
    prefix='How can we best describe the following matrix?'+(' \n\n' if p['layout']=='aligned' else '\n\n')
    return prefix+render(p)+('\n\n'+CRITERION if normal else '')

def solution(p,template):
    """The source region/prose, repeated matrix, then a concrete derived witness."""
    letter=p['letter']; region={'lower':'above','upper':'below','diagonal':'above and below'}[template]
    result=f"Notice that ${letter}$ is a matrix for which all entries {region} the diagonal are $0$'s:\n\n"+render(p)
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
    if source_id and source_levels(source_id)!=level: raise ValueError('Source profile/level mismatch')
    rng=random.Random(seed)
    if parameters is None:
        if source_id: raise ValueError('Source evidence profiles require explicit matrix parameters')
        template,p=sample_parameters(level,template,rng)
    else:
        p=validate_parameters(parameters)
        template=template or family(p['matrix'])
    p=validate_parameters(p);level_guard(level,p,template)
    if source_id:
        anchor=parse_matrix(SOURCES[source_id][':question/problem'])
        if (len(p['matrix']),p['layout'])!=(len(anchor['matrix']),anchor['layout']): raise ValueError('Source recipe dimension/layout mismatch')
        if template!=family(anchor['matrix']): raise ValueError('Source family mismatch')
    answer=FAMILIES[template]; problem=prompt(p,not raw); worked=solution(p,template)
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
        'source_id':source_id,'difficulty_origin':'authored 4x4 scan extension' if level=='hard' else 'authored easy inference for unrated q-13769' if source_id=='q-13769' else 'observed family rating; bounded structural extension',
        'evidence_only':raw,'eligible_for_learning':not raw,'plot_rating':'none',
        'repairs':[] if raw else ['explicit most-specific criterion']+(['single radio field confirmed by authoritative MA widget'] if source_id=='q-13759' else ['inferred correct ref and authored solution/rating'] if source_id=='q-13769' else []),
        'catalog_count':len(catalog(level))}}

# EASY: source-shaped 2x2/3x3 strict triangular, including sparse active regions.
def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)
# MODERATE: source-shaped 3x3 diagonal; zero diagonal entries explicitly permitted.
def generate_moderate(seed=0,**kwargs): return generate('moderate',seed,**kwargs)
# HARD: authored 4x4 same recognition method, bounded longer region scan.
def generate_hard(seed=0,**kwargs): return generate('hard',seed,**kwargs)

def batch(level,count,seed=0,**kwargs):
    if type(count)!=int or not 1<=count<=len(catalog(level,kwargs.get('template'))): raise ValueError('Count exceeds finite meaningful catalog')
    if kwargs.get('parameters') is not None and count!=1: raise ValueError('One explicit task cannot supply a distinct batch')
    result=[];seen=set()
    for offset in range(max(1000,30*count)):
        rec=generate(level,seed+offset,**kwargs);fp=rec['generation']['parameter_fingerprint']
        if fp not in seen: result.append(rec);seen.add(fp)
        if len(result)==count:return result
    raise ValueError('Finite sampler exhausted; '+str(len(result))+' distinct tasks found')

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
