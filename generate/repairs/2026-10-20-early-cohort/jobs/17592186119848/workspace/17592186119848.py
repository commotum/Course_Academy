#!/usr/bin/env python3
"""Bounded, source-faithful rank inspection generator; no database operations.

Easy: dimension exclusions followed by pivot inspection. Original profiles replay
exactly (apart from canonical math formatting and one documented spelling fix).
Authored variants change pivot ranks within the same shapes and field contract.
Moderate/hard remain unsupported pending evidence. See adjacent extraction.
"""
import argparse, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    if __name__ != '__main__': raise
    import os
    python=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    os.execv(str(python),[str(python),str(Path(__file__).resolve()),*sys.argv[1:]])
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import matrix_tex,normalize_prose,normalize_tex,checked_math_content
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186119848
KP_UUID=SOURCE['record'][':knowledge-point/id']
GENERATOR_UUID=str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:generator:'+str(KP_ID)))
VERSION='rank-inspection-pivots-1'
SUPPORTED_LEVELS=('easy',)
CASES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy' and q.get(':question/worked-solution')}
MATRIX=re.compile(r'([A-E])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def parse_matrices(text):
    return {m[1]:sp.ImmutableMatrix([[sp.Integer(v.strip()) for v in row.split('&')] for row in m[2].split(r'\\')]) for m in MATRIX.finditer(text)}
def target(q):return int(re.search(r'rank of \$(\d+)',q[':question/problem'])[1])
def matrices(q):
    result=parse_matrices(q[':question/problem'])
    for f in q.get(':question/answer-fields',[]):
        for a in f.get(':answer-field/choices',[]):result.update(parse_matrices(a[':answer/value']))
    return result
def kind(sid):
    old=CASES[sid];f=old[':question/answer-fields'][0]
    if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':return 'three-matrix-checkbox'
    return 'five-matrix-radio' if f[':answer-field/choices'][0][':answer/type'][':db/ident']==':answer.type/math' else 'three-matrix-subset-radio'
def eligible(sid):
    q=CASES[sid];r=target(q)
    return [label for label,m in sorted(matrices(q).items()) if min(m.shape)>=r]
def original_matches(sid):
    q=CASES[sid];r=target(q)
    return tuple(k for k,m in sorted(matrices(q).items()) if m.rank()==r)
def subset(value):return tuple(sorted(set(re.findall(r'\$([A-E])\$',value))))
def domain(sid):
    q=CASES[sid];typ=kind(sid);labels=eligible(sid)
    if typ=='five-matrix-radio':return [(label,) for label in labels]
    if typ=='three-matrix-checkbox':return sorted({original_matches(sid), ()})
    f=q[':question/answer-fields'][0]
    return sorted({subset(a[':answer/value']) for a in f[':answer-field/choices'] if set(subset(a[':answer/value']))<=set(labels)})
def rank_adjust(matrix,desired):
    """Change a visible pivot structure, keeping shape and integer entries.

    Reduce by retaining a maximal initial independent row subset of desired size;
    grow by filling empty rows with unused standard basis directions. All source
    eligible matrices are triangular or echelon up to zero-row position.
    """
    m=sp.MutableDenseMatrix(matrix)
    if desired<m.rank():
        keep=[]
        for i in range(m.rows):
            if len(keep)<desired and sp.Matrix([list(matrix.row(j)) for j in keep+[i]]).rank()>len(keep):keep.append(i)
        for i in range(m.rows):
            if i not in keep:
                for j in range(m.cols):m[i,j]=0
    while m.rank()<desired:
        zero=next(i for i in range(m.rows) if all(m[i,j]==0 for j in range(m.cols)))
        for j in [zero]+[j for j in range(m.cols) if j!=zero]:
            if j>=m.cols:continue
            candidate=m.copy();candidate[zero,j]=1
            if candidate.rank()>m.rank():m=candidate;break
        else:raise ValueError('No independent pivot')
    assert m.rank()==desired
    return sp.ImmutableMatrix(m)
def structure(q):
    # Ignore scalar rescaling, labels and choice order. Rank locations/zero masks
    # are the assessed information; this deliberately coalesces cosmetic variants.
    return [target(q),sorted((m.rows,m.cols,int(m.rank()),tuple(int(v!=0) for v in m)) for m in matrices(q).values())]
def fingerprint(q):return hashlib.sha256(json.dumps(structure(q),sort_keys=True).encode()).hexdigest()
def render_matrices(text,bank):
    return MATRIX.sub(lambda m:m[1]+'='+matrix_tex([list(bank[m[1]].row(i)) for i in range(bank[m[1]].rows)]),text)
def variant_solution(old,bank,r):
    labels=sorted(bank);excluded=[k for k in labels if min(bank[k].shape)<r];valid=[k for k in labels if k not in excluded]
    matches=[k for k in valid if bank[k].rank()==r]
    # Retain the source's ordered stages and shared instructional sentences.
    text=normalize_prose(old[':question/worked-solution']).replace('coumns','columns')
    head=text.split('Also, the matrix must have')[0]
    body=f'Also, the matrix must have ${r}$ pivot columns. '
    for k in valid:
        rank=int(bank[k].rank());word='exactly' if rank==r else 'only'
        body+=f'As we can see, the matrix ${k}$ has {word} ${rank}$ pivot columns. So, $'+r'\text{rank}('+k+')='+str(rank)+'.$ '
    if kind(old[':question/math-academy-id'])=='five-matrix-radio':end='the matrix $'+matches[0]+'.$'
    elif not matches:end='"None."'
    else:end='"'+' and '.join('$'+k+'$' for k in matches)+' only."'
    return head+body.rstrip()+'\n\nTherefore, the correct answer is '+end
@checked_math_content
def generate(level,seed=0,profile=None,parameters=None):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
    rng=random.Random(seed);sid=profile or rng.choice(sorted(CASES));old=CASES[sid]
    desired=tuple(parameters['matches']) if parameters is not None else rng.choice(domain(sid))
    if parameters is not None and set(parameters)!={'matches'}:raise ValueError('Exactly matches required')
    if desired not in domain(sid):raise ValueError('Unsupported match subset')
    r=target(old);bank=matrices(old);original=original_matches(sid)
    if desired!=original:
        # Only dimension-eligible candidates can change rank. Deficient candidates
        # retain their observed rank unless they need to become correct.
        for label in eligible(sid):
            rank=int(bank[label].rank())
            wanted=r if label in desired else r-1 if rank==r else rank
            bank[label]=rank_adjust(bank[label],wanted)
    problem=render_matrices(normalize_prose(old[':question/problem']),bank)
    solution=normalize_prose(old[':question/worked-solution']).replace('coumns','columns') if desired==original else variant_solution(old,bank,r)
    rawfields=[]
    for f in old[':question/answer-fields']:
        choices=[];typ=f[':answer-field/type'][':db/ident'];correct0=f[':answer-field/correct'][':answer/id']
        for a in f[':answer-field/choices']:
            val=normalize_tex(render_matrices(a[':answer/value'],bank)) if a[':answer/type'][':db/ident']==':answer.type/math' else normalize_prose(a[':answer/value'])
            if typ==':answer-field.type/checkbox':
                lab=f[':answer-field/key']
                correct=val==('true' if lab in desired else 'false')
            elif kind(sid)=='five-matrix-radio':correct=next(iter(parse_matrices(val))) in desired
            else:correct=subset(val)==desired
            choices.append((a[':answer/type'][':db/ident'],val,correct))
        assert sum(x[2] for x in choices)==1
        rawfields.append((f,choices))
    content=hashlib.sha256(json.dumps([VERSION,problem,solution,[(f[':answer-field/key'],sorted(v)) for f,v in rawfields]],sort_keys=True).encode()).hexdigest()
    uid=lambda key:str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP_ID)+':'+content+':'+key))
    fields=[]
    for f,rows in rawfields:
        key=f[':answer-field/key'];choices=[{':answer/id':uid(key+':'+typ+':'+val),':answer/type':typ,':answer/value':val} for typ,val,_ in rows]
        correct=next(a[':answer/id'] for a,row in zip(choices,rows) if row[2])
        field={':answer-field/id':uid('field:'+key),':answer-field/key':key,':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
        for extra in (':answer-field/label',):
            if extra in f:field[extra]=f[extra]
        fields.append(field)
    question={':question/id':uid('question'),':question/difficulty':':question.difficulty/easy',':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':kind(sid),'bank_profile':sid,'source_id':sid,'parameters':{'matches':list(desired)},'mathematical_fingerprint':fingerprint(question),'content_fingerprint':content,'assets':[],'source':{'basis':SOURCE['basis'],'lineage':SOURCE['lineage']},'dependencies':{'sympy':sp.__version__},'ranks':{k:int(m.rank()) for k,m in bank.items()},'extension':desired!=original}}
def catalog():
    result=[];seen=set()
    for sid in sorted(CASES):
        for matches in domain(sid):
            rec=generate('easy',0,sid,{'matches':list(matches)});fp=rec['generation']['mathematical_fingerprint']
            if fp not in seen:seen.add(fp);result.append(rec)
    return result
def batch(level,count,seed=0):
    if level not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+level)
    records=catalog();random.Random(seed).shuffle(records)
    if type(count) is not int or count<0 or count>len(records):raise ValueError('Finite variant limit: '+str(len(records)))
    return records[:count]
def markdown(rec):
    q=rec['question'];return q[':question/problem']+'\n\n'+'\n\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']) for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
    recs=batch(a.difficulty,a.count,a.seed);print(json.dumps(recs,indent=2) if a.format=='json' else '\n\n'.join(map(markdown,recs)))
