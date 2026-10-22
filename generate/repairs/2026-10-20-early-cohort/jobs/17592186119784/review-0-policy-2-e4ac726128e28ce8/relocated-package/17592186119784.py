#!/usr/bin/env python3
"""Three-statement matrix recognition with full-statement checkboxes; frozen mathematical source snapshot basis 1356.

Easy (authored): fixed 3x3 A; upper/lower/diagonal statements, no operations.
Moderate (observed): three statements on A and its transpose; each source
recipe retains its original 3x3/4x4 dimension and operation workload. Complete source radio banks remain available only through evidence replay.
Hard (observed): three statements on A and one transpose sum/difference.
The unrated q-42115 has a separately inferred hard normal presentation.
Source-replay is parameterized, evidence-only, preserves raw missing attributes
and raw solution referent errors. Normal source-profile variants minimally
correct those errors. Numerical magnitudes/signs and diagonal values do not
inflate structural task counts. No database access or plots are needed.
"""
from __future__ import annotations
import argparse, copy, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186119784
KP_UUID=SOURCE['record'][':knowledge-point/id']
TITLE=SOURCE['record'][':knowledge-point/title']
VERSION='matrix-statements-radio-v2'
NS=uuid.UUID(KP_UUID)
LEVELS=('easy','moderate','hard')
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
MATRIX_RE=r'\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\1\}'
ROMANS=('I','II','III')


def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(NS, VERSION+':'+x))
def enum(x): return x.get(':db/ident') if isinstance(x,dict) else x
def read_matrix(text):
    match=re.search(MATRIX_RE,text,re.S)
    if not match: raise ValueError('Missing matrix')
    return sp.Matrix([[int(c.strip()) for c in row.split('&')] for row in match[2].split(r'\\')])
def matrix_body(m): return r' \\ '.join(' & '.join(str(v) for v in m.row(i)) for i in range(m.rows))
def matrix_tex(m): return r'[\begin{aligned}'+matrix_body(m)+r'\end{aligned}]'
def statements(text):
    out=[]
    for expr,kind in re.findall(r'\$(.*?)\$ is (upper triangular|lower triangular|diagonal)',text):
        clean=re.sub(r'[{}\s]','',expr)
        name=next(c for c in clean if c.isalpha())
        clean=clean.replace(name,'A')
        op={'A':'identity','A^T':'transpose','A^T+A':'sum','A+A^T':'sum','A^T-A':'transpose-minus','A-A^T':'minus-transpose'}.get(clean)
        if op is None: raise ValueError('Unsupported complete matrix expression: '+expr)
        out.append((expr,op,kind))
    if len(out)!=3: raise ValueError('Exactly three statements required')
    return out

def transform(m,op):
    if op=='identity': return m
    if op=='transpose': return m.T
    if op=='sum': return m+m.T
    if op=='transpose-minus': return m.T-m
    if op=='minus-transpose': return m-m.T
    raise ValueError('Unsupported operation')
def inspected(n,kind):
    return [(i,j) for i in range(n) for j in range(n) if (i>j if kind=='upper triangular' else i<j if kind=='lower triangular' else i!=j)]
def truth(m,op,kind):
    b=transform(m,op)
    return all(b[i,j]==0 for i,j in inspected(m.rows,kind))
def subset(value):
    if value=='None': return ()
    return tuple(re.findall(r'\b(?:III|II|I)\b',value))
def subset_value(keys):
    if not keys: return 'None'
    if len(keys)==3: return 'I, II, and III'
    return ' and '.join(keys)+' only'
def correct_value(m,ss): return subset_value(tuple(k for k,(_,op,kind) in zip(ROMANS,ss) if truth(m,op,kind)))
def source_level(sid): return enum(QS[sid].get(':question/difficulty'))
def level(sid): return (source_level(sid) or ':question.difficulty/hard').split('/')[-1]

TEMPLATES={sid:{'level':level(sid),'source_matrix':[[int(v) for v in row] for row in read_matrix(q[':question/problem']).tolist()],'statements':statements(q[':question/problem'])} for sid,q in QS.items()}
TEMPLATES['direct-properties']={'level':'easy','source_matrix':[[1,0,0],[2,3,0],[0,0,4]],'statements':[('A','identity','upper triangular'),('A','identity','lower triangular'),('A','identity','diagonal')]}
EASY_BANK=('None','I only','II only','I and II only','I, II, and III')


def positions(n): return [(i,j) for i in range(n) for j in range(n) if i!=j]
def supports(sid):
    if sid=='direct-properties':
        pp=positions(3)
        return [list(c) for k in range(len(pp)+1) for c in itertools.combinations(pp,k) if not (any(i>j for i,j in c) and any(i<j for i,j in c))]
    old=sp.Matrix(TEMPLATES[sid]['source_matrix']);n=old.rows
    lo=any(old[i,j]!=0 for i in range(n) for j in range(i))
    up=any(old[i,j]!=0 for i in range(n) for j in range(i+1,n))
    if not lo and not up: return [[]]
    pp=[(i,j) for i in range(n) for j in range(n) if i<j] if lo and up else [(i,j) for i in range(n) for j in range(n) if (i>j if lo else i<j)]
    return [list(c) for k in range(1,len(pp)+1) for c in itertools.combinations(pp,k)]

def sample(sid,rng,support=None):
    old=sp.Matrix(TEMPLATES[sid]['source_matrix']);n=old.rows
    if support is None:
        catalog=supports(sid)
        if sid=='direct-properties':
            # Sample the three nonempty semantic truth classes equally, then choose a
            # concrete support. Do not make None dominate because its region
            # contains many more structural masks. The complete bank is fixed.
            groups={}
            for candidate in catalog:
                category=(any(i>j for i,j in candidate),any(i<j for i,j in candidate))
                groups.setdefault(category,[]).append(candidate)
            support=rng.choice(rng.choice(list(groups.values())))
        else: support=rng.choice(catalog)
    m=sp.zeros(n)
    for i in range(n): m[i,i]=rng.randint(-8,8)
    skew=sid!='direct-properties' and any(old[i,j]!=0 for i in range(n) for j in range(i)) and any(old[i,j]!=0 for i in range(n) for j in range(i+1,n))
    for i,j in support:
        m[i,j]=rng.choice([v for v in range(-8,9) if v])
        if skew: m[j,i]=-m[i,j]
    return {'matrix':[[int(v) for v in row] for row in m.tolist()]}

def validate_parameters(sid,p):
    if set(p)!={'matrix'}: raise ValueError('Only the complete matrix parameter is supported')
    a=p['matrix'];n=len(TEMPLATES[sid]['source_matrix'])
    if not isinstance(a,list) or len(a)!=n or any(not isinstance(r,list) or len(r)!=n for r in a): raise ValueError('Fixed template dimension required')
    if any(type(v) is not int or abs(v)>8 for row in a for v in row): raise ValueError('Integer entries in -8..8 required')
    m=sp.Matrix(a)
    if sid=='direct-properties': return m
    old=sp.Matrix(TEMPLATES[sid]['source_matrix']);ss=TEMPLATES[sid]['statements']
    # The complete source bank and shared proof prose require this eligibility
    # class. Guard explicit parameters just as strictly as sampled parameters.
    if [truth(m,op,k) for _,op,k in ss]!=[truth(old,op,k) for _,op,k in ss]: raise ValueError('Complete source-bank truth profile required')
    lo=any(old[i,j]!=0 for i in range(n) for j in range(i));up=any(old[i,j]!=0 for i in range(n) for j in range(i+1,n))
    if not lo and any(m[i,j]!=0 for i in range(n) for j in range(i)): raise ValueError('Source lower zero region required')
    if not up and any(m[i,j]!=0 for i in range(n) for j in range(i+1,n)): raise ValueError('Source upper zero region required')
    if lo and up and any(m[i,j]!=-m[j,i] for i in range(n) for j in range(i+1,n)): raise ValueError('Source off-diagonal cancellation relation required')
    return m

def replace_matrices(text,matrices):
    matches=list(re.finditer(MATRIX_RE,text,re.S))
    if len(matches)!=len(matrices): raise ValueError('Exact source matrix-stage count required')
    for match,m in reversed(list(zip(matches,matrices))): text=text[:match.start(2)]+matrix_body(m)+text[match.end(2):]
    return text

def authored_solution(m,ss):
    parts=["Let's analyze each statement in turn."]
    for key,(expr,op,kind) in zip(ROMANS,ss):
        b=transform(m,op);good=truth(m,op,kind)
        side='below' if kind=='upper triangular' else 'above' if kind=='lower triangular' else 'off'
        why=f'all the entries {side} the main diagonal are zeros' if good else f'${expr}$ has non-zero entries {side} the main diagonal'
        parts.append(f'- Statement {key} is {str(good).lower()}, since {why}:\n\n$$\n{expr}={matrix_tex(b)}\n$$')
    parts.append('Therefore, the correct answer is "'+correct_value(m,ss)+'".')
    return '\n\n'.join(parts)

def render_solution(sid,m,raw):
    source=QS[sid];ss=TEMPLATES[sid]['statements']
    if ':question/worked-solution' not in source: return None if raw else authored_solution(m,ss)
    out=replace_matrices(source[':question/worked-solution'],[transform(m,op) for _,op,_ in ss])
    if not raw:
        if sid=='q-126477': out=out.replace('since $A$ has','since $B$ has')
        if sid=='q-126484': out=out.replace('Statement III is false, since $B$ has non-zero entries below the main diagonal:', 'Statement III is false, since ${B}^{T}$ has non-zero entries above the main diagonal:')
    return out

def math_fingerprint(m,ss):
    # Only matrices actually assessed contribute. Numeric diagonal values and
    # nonzero magnitudes/signs are incidental to these triangular properties.
    data={'dimension':m.rows,'matrix_support':[int(m[i,j]!=0) for i,j in positions(m.rows)],
          'statements':sorted((op,kind,tuple(int(transform(m,op)[i,j]!=0) for i,j in positions(m.rows))) for _,op,kind in ss)}
    return digest(data)

def local_answer(a):
    return {k:(enum(v) if k==':answer/type' else v) for k,v in a.items() if k!=':db/id'}

def build_record(sid,m,p,seed,profile,difficulty):
    raw=profile=='source-replay';ss=TEMPLATES[sid]['statements'];cv=correct_value(m,ss)
    if sid=='direct-properties':
        problem='Consider the matrix \n$A='+matrix_tex(m)+'.$\nWhich of the following statements are true?\n\n'+ '\n'.join('- $'+e+'$ is '+k for e,_,k in ss)
        q={':question/problem':problem,':question/worked-solution':authored_solution(m,ss),':question/difficulty':':question.difficulty/easy'}
        oldfields=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/text',':answer/value':v} for v in EASY_BANK]}]
    else:
        source=QS[sid]
        # db IDs and MA provenance stay in source.json and generation metadata.
        q={k:copy.deepcopy(v) for k,v in source.items() if k not in (':db/id',':question/math-academy-id',':question/id',':question/answer-fields',':question/worked-solution')}
        q[':question/problem']=replace_matrices(source[':question/problem'],[m])
        if ':question/difficulty' in q: q[':question/difficulty']=enum(q[':question/difficulty'])
        if not raw: q[':question/difficulty']=':question.difficulty/'+difficulty
        sol=render_solution(sid,m,raw)
        if sol is not None: q[':question/worked-solution']=sol
        oldfields=source[':question/answer-fields']
    banks=[[local_answer(a) for a in f[':answer-field/choices']] for f in oldfields]
    # Ignore ordering, aliases, seed, and evidence-profile name in identity.
    canonical_banks=[sorted([{k:v for k,v in a.items() if k!=':answer/id'} for a in b],key=lambda a:a[':answer/value']) for b in banks]
    content={**q,'banks':canonical_banks,'field_attributes':[{k:enum(v) for k,v in f.items() if k not in (':db/id',':answer-field/id',':answer-field/choices',':answer-field/correct')} for f in oldfields], 'correct_present':[not raw or ':answer-field/correct' in f for f in oldfields]}
    qid=uid(digest(content));q[':question/id']=qid;fields=[]
    for f,bank in zip(oldfields,banks):
        if len(bank)!=5 or len({subset(a[':answer/value']) for a in bank})!=5: raise ValueError('Complete distinct five-option bank required')
        eligible=[a for a in bank if subset(a[':answer/value'])==subset(cv)]
        if len(eligible)!=1: raise ValueError('Whole bank lacks unique correct subset')
        nf={k:enum(v) for k,v in f.items() if k not in (':db/id',':answer-field/id',':answer-field/choices',':answer-field/correct')}
        fid=uid(qid+':field:'+nf[':answer-field/key']);nf[':answer-field/id']=fid
        for a in bank: a[':answer/id']=uid(fid+':answer:'+digest({k:v for k,v in a.items() if k!=':answer/id'}))
        correct=next(a for a in bank if subset(a[':answer/value'])==subset(cv))
        random.Random(seed).shuffle(bank);nf[':answer-field/choices']=bank
        if not raw or ':answer-field/correct' in f: nf[':answer-field/correct']=[':answer/id',correct[':answer/id']]
        fields.append(nf)
    q[':question/answer-fields']=fields
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':profile,'parameters':p,'level':difficulty,'source_ids':[] if sid=='direct-properties' else [sid],'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'authored':sid=='direct-properties' or (sid=='q-42115' and not raw),'inferred_correct_value':cv,'math_fingerprint':math_fingerprint(m,ss),'content_fingerprint':digest(content),'eligible_for_learning':not raw,'evidence_only':raw,'python':sys.version.split()[0],'sympy':sp.__version__}}


CHECKBOX_VERSION='matrix-statements-checkbox-v3'

def checkbox_solution(m,ss):
    parts=[]
    for expr,op,kind in ss:
        b=transform(m,op);good=truth(m,op,kind)
        side='below' if kind=='upper triangular' else 'above' if kind=='lower triangular' else 'off'
        if good:
            why='All entries '+side+' the main diagonal are zero.'
        else:
            i,j=next((i,j) for i,j in inspected(m.rows,kind) if b[i,j]!=0)
            why=f'The entry in row {i+1}, column {j+1} is ${b[i,j]}\\ne 0$, '+side+' the main diagonal.'
        parts.append(f'- ${expr}$ is {kind}: **{str(good).lower()}**. '+why+'\n\n$$\n'+expr+r'=\begin{bmatrix}'+matrix_body(b)+r'\end{bmatrix}'+'\n$$')
    return '\n\n'.join(parts)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    raw=profile=='source-replay';expected='radio' if raw else 'checkbox'
    if field_type not in (None,expected,':answer-field.type/'+expected):
        raise ValueError('This presentation requires '+expected+' fields')
    record=_generate_radio_evidence(level,seed,template,None,parameters,profile)
    if raw:return record
    meta=record['generation'];sid=meta['template'];ss=TEMPLATES[sid]['statements'];m=sp.Matrix(meta['parameters']['matrix'])
    verdicts=[truth(m,op,kind) for _,op,kind in ss]
    if not any(verdicts):raise ValueError('Normal checkbox questions must have at least one correct selection')
    q=record['question'];name=re.search(r'[A-E]',ss[0][0])[0]
    q[':question/problem']='Consider the matrix\n\n$$\n'+name+r'=\begin{bmatrix}'+matrix_body(m)+r'\end{bmatrix}'+'.\n$$\n\nWhich of the following statements are true?\n\nSelect all that apply.'
    q[':question/worked-solution']=checkbox_solution(m,ss)
    objects=[(f'${expr}$ is {kind}.',correct) for (expr,_,kind),correct in zip(ss,verdicts)]
    payload={k:v for k,v in q.items() if k not in (':question/id',':question/answer-fields')};payload['checkbox_objects']=objects
    fingerprint=digest(payload)
    new_id=lambda label:str(uuid.uuid5(NS,CHECKBOX_VERSION+':'+label))
    qid=new_id(fingerprint);q[':question/id']=qid;fields=[]
    for key,correct in objects:
        fid=new_id(qid+':field:'+key)
        answers=[{':answer/id':new_id(fid+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[int(correct)][':answer/id']]})
    q[':question/answer-fields']=fields
    meta.update(version=CHECKBOX_VERSION,content_fingerprint=fingerprint,response_layout='complete-statement-checkboxes')
    return record

# EASY: authored same-workload direct property hierarchy, fixed 3x3.
# MODERATE: source-shaped matrix/transpose statements and full observed banks.
# HARD: source-shaped matrix/transpose sum or difference and full observed banks.
def _generate_radio_evidence(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS: raise ValueError('Unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only observed RADIO fields supported')
    raw=profile=='source-replay'
    candidates=[sid for sid,t in TEMPLATES.items() if t['level']==level]
    rng=random.Random(seed)
    sid=template or rng.choice(candidates)
    if sid not in candidates: raise ValueError('Wrong template difficulty')
    chosen=profile or ('authored-property-bank' if sid=='direct-properties' else 'source-bank')
    if chosen not in ('source-replay','source-bank','authored-property-bank'): raise ValueError('Unknown complete bank profile')
    if sid=='direct-properties' and chosen!='authored-property-bank': raise ValueError('Authored easy has no observed replay')
    if sid!='direct-properties' and chosen=='authored-property-bank': raise ValueError('Wrong bank family')
    p=copy.deepcopy(parameters) if parameters is not None else ({'matrix':copy.deepcopy(TEMPLATES[sid]['source_matrix'])} if raw else sample(sid,rng))
    m=validate_parameters(sid,p)
    return build_record(sid,m,p,seed,chosen,level)
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('hard',seed,template,field_type,parameters,profile)
def batch(level,count,seed=0):
    rng=random.Random(seed);candidates=[(sid,s) for sid,t in TEMPLATES.items() if t['level']==level for s in supports(sid)];rng.shuffle(candidates)
    out=[];seen=set()
    for sid,s in candidates:
        rec=generate(level,seed,sid,parameters=sample(sid,rng,s))
        fp=rec['generation']['math_fingerprint']
        if fp not in seen: out.append(rec);seen.add(fp)
        if len(out)>=count: break
    return out

def markdown(rec):
    q=rec['question'];parts=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):
        if f[':answer-field/type']==':answer-field.type/checkbox':parts+=['\n- [ ] '+f[':answer-field/key']]
        else:parts+=['\nChoices: '+ '; '.join(a[':answer/value'] for a in f[':answer-field/choices'])]
    if ':question/worked-solution' in q: parts+=['\n'+q[':question/worked-solution']]
    return '\n'.join(parts)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=('markdown','json'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ns=ap.parse_args()
    if ns.count<1: ap.error('count must be positive')
    records=[generate(l,ns.seed+i,ns.template,profile=ns.profile) for l in (LEVELS if ns.difficulty=='all' else [ns.difficulty]) for i in range(ns.count)]
    print(json.dumps(records,indent=2) if ns.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

# Every learner-facing checkbox question has a nonempty correct selection.
from generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__': main()
