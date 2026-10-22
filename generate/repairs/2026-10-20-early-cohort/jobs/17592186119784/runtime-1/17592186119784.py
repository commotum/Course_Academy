#!/usr/bin/env python3
"""Offline matrix-statement checkboxes from supplied source basis 5452.

Choose strict-region/cancellation roles before values; derive proofs and keys.
Replay preserves all current checkbox banks and original difficulty attributes.
The prior authored easy family is retained; unrated q-42115 defaults to hard.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP_ID=17592186119784
KP_UUID=SOURCE['record'][':knowledge-point/id']
TITLE=SOURCE['record'][':knowledge-point/title']
NS=uuid.UUID(KP_UUID)
LEVELS=('easy','moderate','hard')
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
MATRIX_RE=r'\\begin\{(aligned|bmatrix)\}(.*?)\\end\{\1\}'


def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def enum(x): return x.get(':db/ident') if isinstance(x,dict) else x
def read_matrix(text):
    match=re.search(MATRIX_RE,text,re.S)
    if not match: raise ValueError('Missing matrix')
    return sp.Matrix([[int(c.strip()) for c in row.split('&')] for row in match[2].split(r'\\')])
def matrix_body(m): return r' \\ '.join(' & '.join(str(v) for v in m.row(i)) for i in range(m.rows))
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
def source_level(sid): return enum(QS[sid].get(':question/difficulty'))
def level(sid): return (source_level(sid) or ':question.difficulty/hard').split('/')[-1]

def source_statements(q):
    ss=[statements_from_key(f[':answer-field/key']) for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above']
    # Stable ordinary presentation order; replay retains the captured order.
    return sorted(ss,key=lambda s: (s[1]!='identity',s[2]!='upper triangular'))

def statements_from_key(key):
    # Reuse the expression parser without inventing extra operations.
    return statements('\n'.join([key]*3))[0]

TEMPLATES={sid:{'level':level(sid),'source_matrix':[[int(v) for v in row] for row in read_matrix(q[':question/problem']).tolist()],'statements':source_statements(q)} for sid,q in QS.items()}
TEMPLATES['direct-properties']={'level':'easy','source_matrix':[[1,0,0],[2,3,0],[0,0,4]],'statements':[('A','identity','upper triangular'),('A','identity','lower triangular'),('A','identity','diagonal')]}


def positions(n): return [(i,j) for i in range(n) for j in range(n) if i!=j]
def math_fingerprint(m,ss):
    # Only matrices actually assessed contribute. Numeric diagonal values and
    # nonzero magnitudes/signs are incidental to these triangular properties.
    data={'dimension':m.rows,'matrix_support':[int(m[i,j]!=0) for i,j in positions(m.rows)],
          'statements':sorted((op,kind,tuple(int(transform(m,op)[i,j]!=0) for i,j in positions(m.rows))) for _,op,kind in ss)}
    return digest(data)

CHECKBOX_VERSION='matrix-statements-checkbox-v4'

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

def supports(sid):
    return ['diagonal','upper','lower','neither'] + (['cancellation'] if TEMPLATES[sid]['level']=='hard' else [])

def sample(sid,rng,support=None):
    case=support or rng.choice(supports(sid))
    if case not in supports(sid): raise ValueError('Unsupported decision case')
    n=len(TEMPLATES[sid]['source_matrix']);m=sp.zeros(n)
    for i in range(n): m[i,i]=rng.randint(-8,8)
    nz=lambda:rng.choice([v for v in range(-8,9) if v])
    for side in ('upper','lower'):
        if case in (side,'neither'):
            cells=[(i,j) for i,j in positions(n) if (i<j)==(side=='upper')]
            for i,j in rng.sample(cells,rng.randint(1,len(cells))):m[i,j]=nz()
    if case=='neither':
        # A shared pair guarantees failure of both sum and difference cancellation.
        i,j=rng.choice([(i,j) for i in range(n) for j in range(i+1,n)])
        m[i,j]=nz();m[j,i]=rng.choice([v for v in range(-8,9) if v and v not in (m[i,j],-m[i,j])])
    if case=='cancellation':
        op=next(op for _,op,_ in TEMPLATES[sid]['statements'] if op not in ('identity','transpose'))
        cells=[(i,j) for i in range(n) for j in range(i+1,n)]
        for i,j in rng.sample(cells,rng.randint(1,len(cells))):
            m[i,j]=nz();m[j,i]=-m[i,j] if op=='sum' else m[i,j]
    return {'matrix':[[int(v) for v in row] for row in m.tolist()]}

def validate_parameters(sid,p):
    if set(p)!={'matrix'}:raise ValueError('Only the complete matrix parameter is supported')
    a=p['matrix'];n=len(TEMPLATES[sid]['source_matrix'])
    if not isinstance(a,list) or len(a)!=n or any(not isinstance(r,list) or len(r)!=n for r in a):raise ValueError('Fixed template dimension required')
    if any(type(v) is not int or abs(v)>8 for row in a for v in row):raise ValueError('Integer entries in -8..8 required')
    return sp.Matrix(a)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Unknown difficulty')
    if field_type not in (None,'checkbox',':answer-field.type/checkbox'):raise ValueError('Checkbox fields required')
    if profile not in (None,'source-bank','authored-property-bank','source-replay'):raise ValueError('Unknown profile')
    rng=random.Random(seed);candidates=[sid for sid,t in TEMPLATES.items() if t['level']==level]
    sid=template or rng.choice(candidates)
    if sid not in candidates:raise ValueError('Wrong template difficulty')
    raw=profile=='source-replay'
    if raw and sid=='direct-properties':raise ValueError('Authored easy has no source replay')
    p=copy.deepcopy(parameters) if parameters is not None else ({'matrix':copy.deepcopy(TEMPLATES[sid]['source_matrix'])} if raw else sample(sid,rng))
    m=validate_parameters(sid,p);ss=TEMPLATES[sid]['statements']
    if raw and p['matrix']!=TEMPLATES[sid]['source_matrix']:raise ValueError('Replay requires original parameters')
    name=re.search(r'[A-E]',ss[0][0])[0]
    q={':question/difficulty':':question.difficulty/'+level,
       ':question/problem':'Consider the matrix\n\n$$\n'+name+r'=\begin{bmatrix}'+matrix_body(m)+r'\end{bmatrix}'+'\n$$\n\nWhich of the following statements are true?\n\nSelect all that apply.',
       ':question/worked-solution':checkbox_solution(m,ss)}
    objects=[(f'${expr}$ is {kind}.',truth(m,op,kind)) for expr,op,kind in ss]
    objects.append(('None of the above',not any(v for _,v in objects)))
    if raw:
        source=QS[sid]
        q={k:copy.deepcopy(source[k]) for k in (':question/problem',':question/worked-solution',':question/difficulty') if k in source}
        if ':question/difficulty' in q:q[':question/difficulty']=enum(q[':question/difficulty'])
        objects=[(f[':answer-field/key'],f[':answer-field/correct'][':answer/value']=='true') for f in source[':question/answer-fields']]
    fingerprint=digest({**q,'objects':objects})
    new_id=lambda label:str(uuid.uuid5(NS,CHECKBOX_VERSION+':'+label))
    qid=new_id(fingerprint);q[':question/id']=qid;fields=[]
    for key,correct in objects:
        fid=new_id(qid+':field:'+key)
        order=next((f[':answer-field/choices'] for f in QS[sid][':question/answer-fields'] if raw and f[':answer-field/key']==key),None) if raw else None
        values=[a[':answer/value'] for a in order] if order else ['false','true']
        answers=[{':answer/id':new_id(fid+':'+value),':answer/type':':answer.type/text',':answer/value':value} for value in values]
        correct_id=next(a[':answer/id'] for a in answers if a[':answer/value']==str(correct).lower())
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]})
    q[':question/answer-fields']=fields
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
      'generation':{'version':CHECKBOX_VERSION,'seed':seed,'template':sid,'profile':profile or 'source-bank','parameters':p,'level':level,
        'source_ids':[] if sid=='direct-properties' else [QS[sid][':question/id']],
        'source':{k:SOURCE[k] for k in ('database','basis','lineage')},
        'math_fingerprint':math_fingerprint(m,ss),'content_fingerprint':fingerprint,
        'eligible_for_learning':not raw,'evidence_only':raw,'python':sys.version.split()[0],'sympy':sp.__version__}}

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
