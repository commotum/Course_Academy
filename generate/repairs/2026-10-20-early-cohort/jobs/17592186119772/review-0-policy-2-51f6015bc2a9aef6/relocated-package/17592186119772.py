#!/usr/bin/env python3
"""Identifying a Triangular Matrix; local draft, math basis1356, no DB operations.

Easy: one complete matrix among five, six observed complete banks (2/3-square).
Moderate: subset of three labeled matrices, two observed complete text banks.
Hard: authored subset of five 4-square matrices; same zero-support test only.
Normal subset tasks use whole-matrix checkbox fields. Easy retains its single-matrix radio choice. Raw profiles raw:q-N preserve duplicate/missing refs.
Source masks replace complete matrices and actual nonzero witnesses, not literals.
Normal source-profile generation retains the original solution stage/prose masks.

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
VERSION='triangular-identification-2'
ROOT=Path(__file__).with_suffix('')
SNAPSHOT=json.loads((ROOT/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SNAPSHOT['record'][':knowledge-point/questions']}
MATRIX_RE=re.compile(r'([A-E])=\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',re.S)
WITNESS_RE=re.compile(r'\{([a-e])\}_\{([1-4])([1-4])\} & =(-?\d+)\\ne 0')
LEVELS=('easy','moderate','hard')
TEMPLATES={'easy':'single_matrix','moderate':'three_matrix_subset','hard':'five_matrix_subset'}


def parse_matrices(text):
    """Read displayed integer arrays, independent of generation metadata."""
    result={}
    for m in MATRIX_RE.finditer(text):
        matrix=[[int(x.strip()) for x in row.split('&')] for row in m[2].split(r'\\')]
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
    matrices=parse_matrices(q[':question/problem']+'\n'+q[':question/worked-solution'])
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
            'solution_mask':mask(q[':question/worked-solution'])}


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
        if any(type(v) is not int or abs(v)>11 for row in mat for v in row):raise ValueError('integer entries in [-11,11]')
        if r:
            if n!=len(r['matrices'][label]):raise ValueError('source-profile dimension')
            observed=r['counts'][label]
            got=[sum(mat[i][j]!=0 for i,j in coordinates(n,criterion=='lower')),
                 sum(mat[i][j]!=0 for i,j in coordinates(n,criterion=='upper'))]
            if got!=observed:raise ValueError('complete profile support counts must be preserved')
    objects=[json.dumps(x) for x in matrices.values()]
    if len(set(objects))!=len(objects):raise ValueError('duplicate complete matrices')
    good=tuple(label for label in labels if qualifies(matrices[label],criterion))
    if level=='easy' and len(good)!=1:raise ValueError('exactly one qualifying easy choice required')
    if level=='moderate' and len(good) not in (1,2):raise ValueError('source subset workload')
    if level=='hard':
        expected=('A','B') if hard_profile=='hard_two' else ('A','B','C')
        if good!=expected:raise ValueError('hard profile qualifying subset')
        # One diagonal matrix demonstrates inclusive membership; the others have
        # 3 allowed nonzeros. Every foil has 3 allowed + one forbidden nonzero.
        for label,mat in matrices.items():
            allowed=sum(mat[i][j]!=0 for i,j in coordinates(4,criterion=='upper'))
            bad=len(forbidden(mat,criterion))
            counts=(allowed,bad)
            expect=(0,0) if label=='A' else (3,0) if label in good else (3,1)
            if counts!=expect:raise ValueError('hard fixed workload support counts')
    return good


def source_bank(r):
    f=SOURCES[r['source_id']][':question/answer-fields'][-1]
    return [subset(a[':answer/value']) for a in f[':answer-field/choices']] if r['level']=='moderate' else []


def hard_bank(profile):
    # Whole fixed profile chosen before parameters. Errors omit a qualifying
    # matrix or include a foil by overlooking its forbidden-side nonzero.
    if profile=='hard_two':return [('A','B'),('A',),('A','C'),('A','B','D'),('A','B','E')]
    if profile=='hard_three':return [('A','B','C'),('A','B'),('B','C'),('A','B','C','D'),('A','C','E')]
    raise ValueError('unknown hard bank')


def candidate_support(rng,level,r=None,profile=None):
    criterion=rng.choice(('upper','lower'))
    matrices={}
    labels='ABCDE' if level in ('easy','hard') else 'ABC'
    good=('A','B') if profile=='hard_two' else ('A','B','C')
    for label in labels:
        n=4 if level=='hard' else len(r['matrices'][label])
        mat=[[0]*n for _ in range(n)]
        bad_count,allowed_count=r['counts'][label] if r else (0,0) if label=='A' else (0,3) if label in good else (1,3)
        for side,count in ((criterion=='lower',bad_count),(criterion=='upper',allowed_count)):
            for i,j in rng.sample(coordinates(n,side),count):mat[i][j]=1
        # Distinct diagonal entries are presentation only; support catalog stores
        # representative values so duplicate same-support foils aren't identical.
        for i in range(n):mat[i][i]=labels.index(label)+1
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


def fill_values(base,rng):
    p=deepcopy(base)
    for mat in p['matrices'].values():
        for i,row in enumerate(mat):
            for j,value in enumerate(row):
                row[j]=rng.randint(-11,11) if i==j else rng.choice([x for x in range(-11,12) if x]) if value else 0
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


def _generate_radio_evidence(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('difficulty easy|moderate|hard')
    if template not in (None,TEMPLATES[level]):raise ValueError('unknown template for level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('original radio layout required')
    rng=random.Random(seed)
    available=[sid for sid in SOURCES if recipe(sid)['level']==level] if level!='hard' else ['hard_two','hard_three']
    profile=profile or rng.choice(available)
    raw=profile.startswith('raw:');base_profile=profile[4:] if raw else profile
    if base_profile not in available:raise ValueError('profile/level mismatch')
    r=recipe(base_profile) if level!='hard' else None
    if raw and parameters is None:
        # No source payload return: this is only the parameter sampler's anchor.
        parameters={'criterion':r['criterion'],'matrices':deepcopy(r['matrices'])}
    if parameters is not None:
        p=deepcopy(parameters)
    else:
        # Profile selected first; reject the complete numerical instance on a
        # collision. Never replace an individual foil from a fallback pool.
        for attempt in range(100):
            p=fill_values(rng.choice(catalog(base_profile)),rng)
            try:
                validate_parameters(level,p,r,base_profile)
                break
            except ValueError:
                continue
        else:
            raise ValueError('no valid whole instance in 100 attempts')
    good=validate_parameters(level,p,r,base_profile)
    witness=witnesses(p['matrices'],p['criterion'],r['preferred'] if r else None)
    if r:
        prompt=render_mask(r['problem_mask'],p,r,witness)
        solution=render_mask(r['solution_mask'],p,r,witness)
        original_fields=SOURCES[base_profile][':question/answer-fields']
        chosen_fields=original_fields if raw else original_fields[-1:]
        fields=[]
        for f in chosen_fields:
            values=[]
            for a in f[':answer-field/choices']:
                value=matrix_tex(a[':answer/value'][0],p['matrices'][a[':answer/value'][0]]) if level=='easy' else a[':answer/value']
                values.append((value,enum(a[':answer/type'])))
            correct=matrix_tex(good[0],p['matrices'][good[0]]) if level=='easy' else next(v for v,t in values if tuple(subset(v))==good)
            fields.append({'values':values,'key':f.get(':answer-field/key'),'key_present':':answer-field/key' in f,
                           'correct':correct,'correct_present':':answer-field/correct' in f})
    else:
        prompt='Which of the following matrices are '+p['criterion']+' triangular matrices?\n\n$'+r',\,'.join(matrix_tex(label,m) for label,m in p['matrices'].items())+'.$'
        solution=hard_solution(p,good,witness)
        bank=hard_bank(base_profile)
        values=[(subset_tex(s),':answer.type/text') for s in bank]
        fields=[{'values':values,'key':'selection','key_present':True,'correct':subset_tex(good),'correct_present':True}]
    if not raw:
        # The conditional upper/lower mask also changes the English article.
        prompt=prompt.replace('a upper triangular','an upper triangular').replace('an lower triangular','a lower triangular')
        solution=solution.replace('a upper triangular','an upper triangular').replace('an lower triangular','a lower triangular')
    for f in fields:
        if len(f['values'])!=5 or len({v for v,t in f['values']})!=5:raise ValueError('complete five-choice bank collision')
        if sum(v==f['correct'] for v,t in f['values'])!=1:raise ValueError('ambiguous bank')
    bank=source_bank(r) if r else hard_bank(base_profile)
    fingerprint=task_fingerprint(level,p,bank,witness)
    # Content identity is actual displayed content + layout + all owned banks;
    # profile aliases/seed/unused source metadata cannot inflate question identity.
    identity=digest([VERSION,level,prompt,solution,fields])
    question={':question/id':uid(identity),':question/problem':prompt,':question/worked-solution':solution,
              ':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[]}
    if raw:
        original=SOURCES[base_profile]
        if ':question/difficulty' not in original:question.pop(':question/difficulty')
        if ':question/math-academy-id' in original:question[':question/math-academy-id']=original[':question/math-academy-id']
    for i,f in enumerate(fields):
        field_id=uid(identity+':field:'+str(i))
        answers=[{':answer/id':uid(field_id+':answer:'+v+':'+t),':answer/type':t,':answer/value':v} for v,t in f['values']]
        correct_id=next(a[':answer/id'] for a in answers if a[':answer/value']==f['correct'])
        rng.shuffle(answers)
        output={':answer-field/id':field_id,':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
        if f['key_present']:output[':answer-field/key']=f['key']
        if f['correct_present']:output[':answer-field/correct']=[':answer/id',correct_id]
        question[':question/answer-fields'].append(output)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
            'generation':{'version':VERSION,'seed':seed,'template':TEMPLATES[level],'profile':profile,'parameters':p,
                          'mathematical_fingerprint':fingerprint,'content_identity':identity,
                          'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},
                          'source_ids':[base_profile] if r else [],'authored_extension':not bool(r),
                          'support_extension':bool(r) and (p['criterion']!=r['criterion'] or any(
                              support(p['matrices'][label])!=support(mat) for label,mat in r['matrices'].items())),
                          'evidence_only':raw,
                          'eligible_for_learning':not raw,'witnesses':{k:[i+1,j+1,p['matrices'][k][i][j]] for k,(i,j) in witness.items()},
                          'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':'none'}}



CHECKBOX_VERSION='triangular-identification-checkbox-v3'

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    raw=bool(profile and profile.startswith('raw:'))
    expected='radio' if raw or level=='easy' else 'checkbox'
    if field_type not in (None,expected,':answer-field.type/'+expected):
        raise ValueError('This presentation requires '+expected+' fields')
    record=_generate_radio_evidence(level,seed,template,None,parameters,profile)
    if raw:return record
    record['generation']['version']=CHECKBOX_VERSION
    p=record['generation']['parameters'];matrices=p['matrices'];criterion=p['criterion']
    good={label for label,mat in matrices.items() if qualifies(mat,criterion)}
    if not good:raise ValueError('Normal checkbox questions must have at least one correct selection')
    q=record['question']
    # Keep matrix names for the worked explanation, but place each whole matrix
    # beside its control. Original source layouts remain evidence-only.
    def present(label,mat):
        return label+r'=\begin{bmatrix}'+r' \\ '.join(' & '.join(str(v) for v in row) for row in mat)+r'\end{bmatrix}'
    def normalized(text):
        def display(match):
            body=match[1];matches=list(MATRIX_RE.finditer(body))
            if len(matches)>1:
                remainder=MATRIX_RE.sub('',body)
                if re.sub(r'\\[,;! ]|[,.;\s]','',remainder):
                    raise ValueError('Unexpected prose in a multi-matrix display')
                return '\n\n'.join('$$\n'+present(m[1],matrices[m[1]])+'\n$$' for m in matches)
            return match[0]
        text=re.sub(r'\$\$(.*?)\$\$',display,text,flags=re.S)
        return MATRIX_RE.sub(lambda m:present(m[1],matrices[m[1]]),text)
    q[':question/problem']=normalized(q[':question/problem'])
    q[':question/worked-solution']=normalized(q[':question/worked-solution'])
    new_id=lambda label:str(uuid.uuid5(uuid.UUID(KP_UUID),CHECKBOX_VERSION+':'+label))
    if level=='easy':
        field=q[':question/answer-fields'][0]
        correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
        correct_value=normalized(correct[':answer/value'])
        for answer in field[':answer-field/choices']:answer[':answer/value']=normalized(answer[':answer/value'])
        payload={k:v for k,v in q.items() if k not in (':question/id',':question/answer-fields')}
        payload['radio_bank']=sorted((a[':answer/type'],a[':answer/value']) for a in field[':answer-field/choices'])
        payload['field_key']=field[':answer-field/key'];payload['correct_value']=correct_value
        fingerprint=digest(payload);qid=new_id(fingerprint);fid=new_id(qid+':field:'+field[':answer-field/key'])
        q[':question/id']=qid;field[':answer-field/id']=fid
        for answer in field[':answer-field/choices']:answer[':answer/id']=new_id(fid+':'+answer[':answer/type']+':'+answer[':answer/value'])
        field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in field[':answer-field/choices'] if a[':answer/value']==correct_value)]
        record['generation'].update(content_identity=fingerprint,response_layout='whole-matrix-radio')
        return record
    q[':question/problem']='Which of the following matrices are '+criterion+' triangular matrices?\n\nSelect all that apply.'
    objects=[('$'+present(label,mat)+'$',label in good) for label,mat in sorted(matrices.items())]
    payload={k:v for k,v in q.items() if k not in (':question/id',':question/answer-fields')}
    payload['checkbox_objects']=objects
    fingerprint=digest(payload)
    new_id=lambda label:str(uuid.uuid5(uuid.UUID(KP_UUID),CHECKBOX_VERSION+':'+label))
    qid=new_id(fingerprint);q[':question/id']=qid;fields=[]
    for key,correct in objects:
        fid=new_id(qid+':field:'+key)
        answers=[{':answer/id':new_id(fid+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[int(correct)][':answer/id']]})
    q[':question/answer-fields']=fields
    record['generation']['content_identity']=fingerprint
    record['generation']['response_layout']='whole-matrix-checkboxes'
    return record

# EASY: observed one-matrix selection with five entire matrix options. Each wrong
# object retains its source's forbidden/allowed support counts, n=2/3, no algebra.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE: three complete matrix checkbox options, one or two true.
# Profile-specific dimensions/counts preserve workload, including a diagonal case.
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
