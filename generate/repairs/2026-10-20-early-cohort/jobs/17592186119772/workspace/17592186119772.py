#!/usr/bin/env python3
"""Identifying a Triangular Matrix; local draft, math basis1356, no DB operations.

Easy: one complete matrix among five, eight observed complete banks (2/3-square).
Moderate: subset of three labeled matrices, four checkbox banks and one text bank.
Hard: authored subset of five 4-square matrices; same zero-support test only.
Normal subset tasks use whole-matrix checkbox fields. Easy retains its single-matrix radio choice. Raw profiles raw:q-N replay all current complete source banks.
Source masks replace complete matrices and actual nonzero witnesses, not literals.
Normal generation derives source solution stages from current matrix membership.

Finite support catalogs are sampled without a claimed infinite numeric diversity.
Diagonal entries, nonzero signs/magnitudes, labels and option order are incidental
and excluded from semantic task fingerprints. Different complete displayed banks
remain distinct content identities. No renderer is needed for native TeX arrays.
See the adjacent evidence folder for exact domains, source repairs and validation.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from functools import lru_cache
import hashlib
import itertools
import math
import json
from pathlib import Path
import random
import re
import sys
import uuid
import sympy as sp

KP_ID=17592186119772
KP_UUID='b55b50a0-034f-57c0-8a61-883cfb0412dc'
TITLE='Identifying a Triangular Matrix'
VERSION='triangular-identification-role-v4'
ROOT=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((ROOT/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions']}
MATRIX_RE=re.compile(r'([A-E])\s*=\s*(?:\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]|\\begin\{bmatrix\}(.*?)\\end\{bmatrix\})',re.S)
WITNESS_RE=re.compile(r'\{([a-e])\}_\{([1-4])([1-4])\} & =(-?\d+)\\ne 0')
LEVELS=('easy','moderate','hard')
TEMPLATES={'easy':'single_matrix','moderate':'three_matrix_subset','hard':'five_matrix_subset'}


def parse_matrices(text):
    """Read displayed integer arrays, independent of generation metadata."""
    result={}
    for m in MATRIX_RE.finditer(text):
        body=m[2] if m[2] is not None else m[3]
        matrix=[[int(x.strip()) if re.fullmatch(r'-?\d+',x.strip()) else float(x.strip()) for x in row.split('&')] for row in body.split(r'\\')]
        if m[1] in result and result[m[1]]!=matrix:
            raise ValueError('Inconsistent repeated displayed matrix')
        result[m[1]]=matrix
    return result


def matrix_tex(label, matrix):
    return label+r'=[\begin{aligned}'+r' \\ '.join(' & '.join(str(x) for x in row) for row in matrix)+r'\end{aligned}]'


def coordinates(n, above):
    return [(i,j) for i in range(n) for j in range(n) if (i<j if above else i>j)]


def forbidden(matrix, criterion):
    return [(i,j) for i,j in coordinates(len(matrix),criterion=='lower') if matrix[i][j]!=0]


def qualifies(matrix, criterion):
    return len(matrix)>0 and all(len(r)==len(matrix) for r in matrix) and not forbidden(matrix,criterion)


def subset(value):
    return tuple(re.findall(r'\$([A-E])\$',value))


def subset_tex(labels):
    labels=sorted(labels)
    if len(labels)==1:return '$'+labels[0]+'$ only'
    if len(labels)==2:return '$'+labels[0]+'$ and $'+labels[1]+'$ only'
    return ', '.join('$'+x+'$' for x in labels[:-1])+', and $'+labels[-1]+'$ only'


@lru_cache(None)
def recipe(source_id):
    q=SOURCES[source_id]
    level=q[':question/difficulty'][':db/ident'].rsplit('/',1)[1]
    criterion='upper' if 'upper triangular' in q[':question/problem'] else 'lower'
    fields=q[':question/answer-fields']
    matrices=parse_matrices(q[':question/problem']+'\n'+q[':question/worked-solution']+'\n'+'\n'.join(f.get(':answer-field/key','') for f in fields))
    if level=='easy':
        matrices={}
        for a in fields[-1][':answer-field/choices']:
            matrices.update(parse_matrices(a[':answer/value']))
    preferred={m[1].upper():(int(m[2])-1,int(m[3])-1) for m in WITNESS_RE.finditer(q[':question/worked-solution'])}
    def mask(text):
        text=MATRIX_RE.sub(lambda m:'@@matrix:'+m[1]+'@@',text)
        text=WITNESS_RE.sub(lambda m:'@@witness:'+m[1].upper()+'@@',text)
        return text
    counts={}
    for label,mat in matrices.items():
        counts[label]=[sum(mat[i][j]!=0 for i,j in coordinates(len(mat),criterion=='lower')),
                       sum(mat[i][j]!=0 for i,j in coordinates(len(mat),criterion=='upper'))]
    return {'source_id':source_id,'level':level,'criterion':criterion,'matrices':matrices,
            'preferred':preferred,'counts':counts,'problem_mask':mask(q[':question/problem']),
            'solution_mask':mask(q[':question/worked-solution']),
            'field_type':enum(fields[0][':answer-field/type'])}


def uid(text):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+text))
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def support(matrix):
    return (len(matrix),tuple((i,j) for i,row in enumerate(matrix) for j,v in enumerate(row) if i!=j and v!=0))


def witnesses(matrices,criterion,preferred=None):
    result={}
    for label,mat in matrices.items():
        bad=forbidden(mat,criterion)
        if bad:
            p=(preferred or {}).get(label)
            result[label]=p if p in bad else bad[0]
    return result


def task_fingerprint(level,p,bank,witness):
    """Canonical assessed objects, retaining repeated support-pattern objects.

    Whole-matrix choices are the input objects at easy; given matrices are the
    input objects for subsets. Text answer subsets and chosen proof witnesses
    cannot create new mathematics. They remain in full content identity.
    """
    objects=sorted(support(matrix) for matrix in p['matrices'].values())
    return digest([level,p['criterion'],objects])


def validate_parameters(level,p,r=None,hard_profile=None):
    if set(p)!={'criterion','matrices'}:raise ValueError('parameters need exactly criterion and matrices')
    criterion=p['criterion']; matrices=p['matrices']
    if criterion not in ('upper','lower'):raise ValueError('criterion upper|lower')
    labels='ABCDE' if level in ('easy','hard') else 'ABC'
    if set(matrices)!=set(labels):raise ValueError('incorrect matrix labels/count')
    for label,mat in matrices.items():
        n=len(mat)
        if n not in ((4,) if level=='hard' else (2,3,4) if level=='moderate' else (2,3)):
            raise ValueError('level dimension bound')
        if any(len(row)!=n for row in mat):raise ValueError('square matrices only')
        if any(type(v) not in (int,float) or not math.isfinite(v) or abs(v)>11 for row in mat for v in row):
            raise ValueError('finite numeric entries in [-11,11]')
        if r and n!=len(r['matrices'][label]):raise ValueError('source-profile dimension')
        # Membership is a mathematical role, never the source label's counts.
    objects=[json.dumps(x) for x in matrices.values()]
    if len(set(objects))!=len(objects):raise ValueError('duplicate complete matrices')
    good=tuple(label for label in labels if qualifies(matrices[label],criterion))
    if level=='easy' and len(good)!=1:raise ValueError('exactly one qualifying easy choice required')
    if level=='moderate' and len(good) not in (1,2):raise ValueError('source subset workload')
    if level=='hard':
        if len(good)!=(2 if hard_profile=='hard_two' else 3):raise ValueError('hard qualifying count')
        counts=[(sum(mat[i][j]!=0 for i,j in coordinates(4,criterion=='upper')),len(forbidden(mat,criterion)))
                for mat in matrices.values()]
        expected=[(0,0)]+[(3,0)]*(len(good)-1)+[(3,1)]*(5-len(good))
        if sorted(counts)!=sorted(expected):raise ValueError('hard workload support counts')
    return good


def source_bank(r):
    f=SOURCES[r['source_id']][':question/answer-fields'][-1]
    return [subset(a[':answer/value']) for a in f[':answer-field/choices']] if r['field_type']==':answer-field.type/radio' and r['level']=='moderate' else []


def hard_bank(profile):
    # Whole fixed profile chosen before parameters. Errors omit a qualifying
    # matrix or include a foil by overlooking its forbidden-side nonzero.
    if profile=='hard_two':return [('A','B'),('A',),('A','C'),('A','B','D'),('A','B','E')]
    if profile=='hard_three':return [('A','B','C'),('A','B'),('B','C'),('A','B','C','D'),('A','C','E')]
    raise ValueError('unknown hard bank')


def candidate_support(rng,level,r=None,profile=None):
    # Decide membership first, independently of labeled dimensions and values.
    criterion=rng.choice(('upper','lower'))
    labels='ABCDE' if level in ('easy','hard') else 'ABC'
    count=1 if level=='easy' else rng.choice((1,2)) if level=='moderate' else 2 if profile=='hard_two' else 3
    good=set(rng.sample(list(labels),count))
    diagonal=rng.choice(sorted(good)) if level=='hard' else None
    matrices={}
    max_bad=max(c[0] for c in r['counts'].values()) if r else 1
    max_allowed=max(c[1] for c in r['counts'].values()) if r else 3
    for label in labels:
        n=4 if level=='hard' else len(r['matrices'][label])
        capacity=n*(n-1)//2
        bad_count=0 if label in good else rng.randint(1,min(max_bad,capacity))
        allowed_count=rng.randint(0,min(max_allowed,capacity)) if r else 0 if label==diagonal else 3
        mat=[[0]*n for _ in range(n)]
        for side,count in ((criterion=='lower',bad_count),(criterion=='upper',allowed_count)):
            for i,j in rng.sample(coordinates(n,side),count):mat[i][j]=1
        for i in range(n):mat[i][i]=rng.randint(-11,11)
        matrices[label]=mat
    return {'criterion':criterion,'matrices':matrices}


@lru_cache(None)
def catalog(profile):
    """Finite explicit support catalog; no numeric-sign/diagonal count inflation.

    Deterministic 256 candidate support assignments per observed complete profile,
    384 per authored hard profile, deduplicated under whole assessed-bank identity.
    This finite catalog is the default sampling domain, not an estimate of every
    mathematically possible bank. Explicit input accepts the documented full bounds.
    """
    r=recipe(profile) if profile.startswith('q-') else None
    level=r['level'] if r else 'hard';bank=source_bank(r) if r else hard_bank(profile)
    result={}
    for k in range(256 if r else 384):
        p=candidate_support(random.Random(profile+':'+str(k)),level,r,profile)
        try:validate_parameters(level,p,r,profile)
        except ValueError:continue
        witness=witnesses(p['matrices'],p['criterion'],r['preferred'] if r else None)
        fingerprint=task_fingerprint(level,p,bank,witness)
        result.setdefault(fingerprint,p)
    return tuple(result.values())


def fill_values(base,rng,decimals=False):
    p=deepcopy(base)
    for mat in p['matrices'].values():
        for i,row in enumerate(mat):
            for j,value in enumerate(row):
                row[j]=rng.randint(-11,11) if i==j else rng.choice([x for x in range(-11,12) if x]) if value else 0
    if decimals:
        for mat in p['matrices'].values():
            for row in mat:
                for j,value in enumerate(row):
                    if value and rng.randrange(3)==0:row[j]=rng.choice((-987,-89,-65,65,89,987))/100
    return p


def render_mask(mask,p,r,witness):
    def matrix(m):return matrix_tex(m[1],p['matrices'][m[1]])
    text=re.sub(r'@@matrix:([A-E])@@',matrix,mask)
    def proof(m):
        label=m[1];i,j=witness[label]
        return '{'+label.lower()+'}_{'+str(i+1)+str(j+1)+'} & ='+str(p['matrices'][label][i][j])+r'\ne 0'
    text=re.sub(r'@@witness:([A-E])@@',proof,text)
    if p['criterion']!=r['criterion']:
        text=text.replace(r['criterion']+' triangular','@@criterion@@ triangular')
        text=text.replace('below','@@side@@') if r['criterion']=='upper' else text.replace('above','@@side@@')
        text=text.replace('@@criterion@@',p['criterion']).replace('@@side@@','below' if p['criterion']=='upper' else 'above')
    return text


def hard_solution(p,good,witness):
    criterion=p['criterion'];side='below' if criterion=='upper' else 'above'
    good_prose=', '.join('$'+x+'$' for x in good[:-1])+' and $'+good[-1]+'$'
    bad=[x for x in p['matrices'] if x not in good]
    bad_prose=' and '.join('$'+x+'$' for x in bad)
    rows=[]
    for label in bad:
        i,j=witness[label]
        rows.append('{'+label.lower()+'}_{'+str(i+1)+str(j+1)+'} & ='+str(p['matrices'][label][i][j])+r'\ne 0')
    return ('The matrices '+good_prose+' are '+criterion+' triangular matrices since all the entries '+side+' the main diagonal are zeros.\n\n'
            'The matrices '+bad_prose+' are *not* '+criterion+' triangular matrices since they each have a non-zero element '+side+' the main diagonal: \n\n$$\n'+
            r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$')


def enum(value):return value[':db/ident'] if isinstance(value,dict) else value


def present(label,mat):
    return label+r'=\begin{bmatrix}'+r' \\ '.join(' & '.join(str(v) for v in row) for row in mat)+r'\end{bmatrix}'


def prose_labels(labels):
    labels=['$'+x+'$' for x in sorted(labels)]
    return labels[0] if len(labels)==1 else ' and '.join(labels) if len(labels)==2 else ', '.join(labels[:-1])+', and '+labels[-1]


def concrete_solution(level,p,good,witness):
    criterion=p['criterion'];side='below' if criterion=='upper' else 'above'
    matrices=p['matrices'];bad=[x for x in sorted(matrices) if x not in good]
    if level=='easy':
        label=good[0]
        foils='\n\n'.join('$$\n'+present(x,matrices[x])+'\n$$' for x in bad)
        return ("Notice that $"+label+"$ is a matrix for which all entries *"+side+"* the diagonal are $0$'s:\n\n$$\n"+
                present(label,matrices[label])+"\n$$\n\nHence, it is "+('an ' if criterion=='upper' else 'a ')+criterion+
                " triangular matrix. \n\nBy contrast, matrices "+prose_labels(bad)+" each have at least one non-zero entry "+side+
                " the diagonal:\n\n"+foils+"\n\nSo, they are not "+criterion+" triangular matrices.")
    good_start=('The matrix ' if len(good)==1 else 'The matrices ')+prose_labels(good)
    bad_start=('The matrix ' if len(bad)==1 else 'The matrices ')+prose_labels(bad)
    rows=[]
    for label in bad:
        i,j=witness[label]
        rows.append('{'+label.lower()+'}_{'+str(i+1)+str(j+1)+'} & ='+str(matrices[label][i][j])+r'\ne 0')
    return (good_start+(' is '+('an ' if criterion=='upper' else 'a ') if len(good)==1 else ' are ')+criterion+
            ' triangular '+('matrix' if len(good)==1 else 'matrices')+' since all the entries '+side+' the main diagonal are zeros.\n\n'+
            bad_start+(' is *not* '+('an ' if criterion=='upper' else 'a ') if len(bad)==1 else ' are *not* ')+criterion+
            ' triangular '+('matrix' if len(bad)==1 else 'matrices')+' since '+('it has' if len(bad)==1 else 'they each have')+
            ' a non-zero element '+side+' the main diagonal: \n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$')


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('difficulty easy|moderate|hard')
    if template not in (None,TEMPLATES[level]):raise ValueError('unknown template for level')
    rng=random.Random(seed)
    available=[sid for sid in SOURCES if recipe(sid)['level']==level] if level!='hard' else ['hard_two','hard_three']
    profile=profile or rng.choice(available)
    raw=profile.startswith('raw:');base_profile=profile[4:] if raw else profile
    if base_profile not in available:raise ValueError('profile/level mismatch')
    r=recipe(base_profile) if level!='hard' else None
    expected=r['field_type'] if r else ':answer-field.type/checkbox'
    if field_type not in (None,expected,expected.rsplit('/',1)[1]):raise ValueError('source response contract requires '+expected)
    if parameters is not None:p=deepcopy(parameters)
    elif raw:p={'criterion':r['criterion'],'matrices':deepcopy(r['matrices'])}
    else:
        for attempt in range(100):
            p=fill_values(candidate_support(rng,level,r,base_profile),rng,base_profile=='q-42111')
            try:
                validate_parameters(level,p,r,base_profile);break
            except ValueError:continue
        else:raise ValueError('no valid whole instance in 100 attempts')
    good=validate_parameters(level,p,r,base_profile)
    witness=witnesses(p['matrices'],p['criterion'],r['preferred'] if r else None)
    source_anchor=bool(r) and p=={'criterion':r['criterion'],'matrices':r['matrices']}
    criterion=p['criterion']
    if source_anchor:
        prompt=SOURCES[base_profile][':question/problem']
        solution=SOURCES[base_profile][':question/worked-solution']
    else:
        prompt='Which of the following is '+('an ' if criterion=='upper' else 'a ')+criterion+' triangular matrix?' if level=='easy' else 'Which of the following matrices are '+criterion+' triangular matrices?'
        if expected==':answer-field.type/checkbox':prompt+='\n\nSelect all that apply.'
        elif level!='easy':prompt+='\n\n'+'\n\n'.join('$$\n'+present(x,mat)+'\n$$' for x,mat in sorted(p['matrices'].items()))
        solution=concrete_solution(level,p,good,witness)
    # Source anchors keep exact text; served multi-matrix displays are split for UI width.
    if not raw:
        def split_display(match):
            found=list(MATRIX_RE.finditer(match[1]))
            if len(found)<2:return match[0]
            return '\n\n'.join('$$\n'+present(m[1],p['matrices'][m[1]])+'\n$$' for m in found)
        prompt=re.sub(r'\$\$(.*?)\$\$',split_display,prompt,flags=re.S)
        solution=re.sub(r'\$\$(.*?)\$\$',split_display,solution,flags=re.S)
        if level=='moderate' and expected==':answer-field.type/radio':
            prompt=prompt.split('\n\n')[0]+'\n\n'+'\n\n'.join('$$\n'+present(x,mat)+'\n$$' for x,mat in sorted(p['matrices'].items()))
    specifications=[]
    if expected==':answer-field.type/checkbox':
        order=[next(iter(parse_matrices(f[':answer-field/key']))) for f in SOURCES[base_profile][':question/answer-fields']] if source_anchor else sorted(p['matrices'])
        if not raw:rng.shuffle(order)
        for label in order:
            key=next(f[':answer-field/key'] for f in SOURCES[base_profile][':question/answer-fields'] if label in parse_matrices(f[':answer-field/key'])) if source_anchor else '$'+present(label,p['matrices'][label])+'$'
            specifications.append((key,[('false',':answer.type/text'),('true',':answer.type/text')],str(label in good).lower()))
    elif level=='easy':
        original=SOURCES[base_profile][':question/answer-fields'][0]
        values=[(a[':answer/value'],enum(a[':answer/type'])) for a in original[':answer-field/choices']] if source_anchor else [(present(label,mat),':answer.type/math') for label,mat in sorted(p['matrices'].items())]
        correct=next(v for v,t in values if next(iter(parse_matrices(v)))==good[0])
        specifications=[(original.get(':answer-field/key','selection'),values,correct)]
    else:
        if source_anchor:
            f=SOURCES[base_profile][':question/answer-fields'][0]
            values=[(a[':answer/value'],enum(a[':answer/type'])) for a in f[':answer-field/choices']]
        else:
            # Complete source-shaped bank: two singletons and all three pairs.
            omitted=rng.choice([x for x in 'ABC' if good!=(x,)])
            bank=[(x,) for x in 'ABC' if x!=omitted]+list(itertools.combinations('ABC',2))
            values=[(subset_tex(labels),':answer.type/text') for labels in bank]
        correct=next(v for v,t in values if tuple(subset(v))==good)
        specifications=[('selection',values,correct)]
    fingerprint=task_fingerprint(level,p,[],witness)
    identity=digest([VERSION,level,prompt,solution,specifications])
    question={':question/id':uid(identity),':question/problem':prompt,':question/worked-solution':solution,
              ':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[]}
    if raw:question[':question/math-academy-id']=base_profile
    for index,(key,values,correct) in enumerate(specifications):
        fid=uid(identity+':field:'+str(index));answers=[]
        for value,kind in values:answers.append({':answer/id':uid(fid+':'+kind+':'+value),':answer/type':kind,':answer/value':value})
        cid=next(a[':answer/id'] for a in answers if a[':answer/value']==correct)
        rng.shuffle(answers)
        question[':question/answer-fields'].append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':expected,
                                                    ':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
            'generation':{'version':VERSION,'seed':seed,'template':TEMPLATES[level],'profile':profile,'parameters':p,
                          'mathematical_fingerprint':fingerprint,'content_identity':identity,
                          'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'source_ids':[base_profile] if r else [],
                          'authored_extension':not bool(r),'support_extension':not source_anchor,'evidence_only':raw,
                          'eligible_for_learning':not raw,'response_layout':expected.rsplit('/',1)[1],
                          'witnesses':{k:[i+1,j+1,p['matrices'][k][i][j]] for k,(i,j) in witness.items()},
                          'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':'none'}}


# EASY: observed one-matrix selection with five entire matrix options. Qualification and support assignments vary at fixed labeled sizes, n=2/3, no algebra.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE: three complete matrix checkbox options, one or two true.
# Profile-specific dimensions preserve workload; response types follow current source.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD: authored five 4x4 matrices, inclusive diagonal + two/three correct subset.
# Each foil differs through one forbidden-side entry; no operations/statements.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)


def markdown(record):
    q=record['question'];out=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        if f[':answer-field/type']==':answer-field.type/checkbox':
            out+=['\n- [ ] '+f[':answer-field/key']]
            continue
        out+=['\n'+f.get(':answer-field/key','(unkeyed legacy field)')+':']
        for a in f[':answer-field/choices']:
            value=a[':answer/value'];out+=['- '+('$'+value+'$' if a[':answer/type']==':answer.type/math' else value)]
    out+=['\nWorked solution:\n\n'+q.get(':question/worked-solution','')]
    return '\n'.join(out)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all')
    parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=('markdown','json'),default='markdown')
    parser.add_argument('--template');parser.add_argument('--profile')
    args=parser.parse_args()
    if args.count<1:parser.error('count must be positive')
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))


# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
