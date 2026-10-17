#!/usr/bin/env python3
"""Bounded source-matrix target variants for one entry of a matrix product.

Only Easy is supported. Matrices remain unchanged; eligible target cells vary.
Radio banks preserve the observed incorrect integer constants verbatim (their
error interpretation is unresolved); only the canonical dot product changes.
Targets colliding with a fixed distractor are excluded. No new bank is inferred.
"""
import argparse,copy,hashlib,json,os,random,re,sys,uuid
from pathlib import Path
try:import sympy as sp
except ModuleNotFoundError:
    if __name__!='__main__':raise
    exe=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(exe),[str(exe),str(Path(__file__).resolve()),*sys.argv[1:]])
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE))
from math_reader import matrices,target,fingerprint
KP_ID=17592186100873
CAPTURE=json.loads((HERE/'source.json').read_text());SOURCE=CAPTURE['record'];VERSION='matrix-entry-targets-v1';SUPPORTED=('easy',)
SOURCE_BY_ID={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
EXCLUDED={mid:'Unrated; correct-answer link and worked solution absent. Original preserved.' for mid,q in SOURCE_BY_ID.items() if ':question/difficulty' not in q}
TEMPLATES={mid:{'level':'easy','field_type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1],'profile':'source-bank:'+mid} for mid,q in SOURCE_BY_ID.items() if mid not in EXCLUDED}
def domain(mid):
    q=SOURCE_BY_ID[mid];A,B=matrices(q);f=q[':question/answer-fields'][0];key=f[':answer-field/correct'][':answer/id']
    wrong={int(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']!=key}
    return [(i+1,j+1) for i in range(len(A)) for j in range(len(B[0])) if sum(a*row[j] for a,row in zip(A[i],B)) not in wrong]
def matrix(A):return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,r)) for r in A)+r'\end{bmatrix}'
def ordinal(i):return str(i)+{1:'st',2:'nd',3:'rd'}.get(i,'th')
def factor(n):return '('+str(n)+')' if n<0 else str(n)
def generate(level,seed=0,template=None,parameters=None,profile=None,replay=False):
    if level not in SUPPORTED:raise ValueError('Unsupported difficulty: '+level)
    rng=random.Random(seed);mid=template or rng.choice(sorted(TEMPLATES));t=TEMPLATES[mid];src=SOURCE_BY_ID[mid]
    assert profile in (None,t['profile'])
    letter,oi,oj=target(src);p=parameters or dict(zip(('row','column'),(oi+1,oj+1) if replay else rng.choice(domain(mid))))
    assert set(p)=={'row','column'} and all(type(x)is int for x in p.values());i,j=p['row'],p['column'];assert (i,j) in domain(mid)
    A,B=matrices(src);row=A[i-1];col=[r[j-1] for r in B];terms=[a*b for a,b in zip(row,col)];answer=int((sp.Matrix(A)*sp.Matrix(B))[i-1,j-1]);assert answer==sum(terms)
    old=r'{'+letter+'}_{'+str(oi+1)+str(oj+1)+'}';new=r'{'+letter+'}_{'+str(i)+str(j)+'}'
    problem=src[':question/problem'].replace(old,new)
    solution=src[':question/worked-solution'].replace(old,new)
    solution=solution.replace('$'+str(oi+1)+'$'+ordinal(oi+1)[-2:]+' row','$'+str(i)+'$'+ordinal(i)[-2:]+' row').replace('$'+str(oj+1)+'$'+ordinal(oj+1)[-2:]+' column','$'+str(j)+'$'+ordinal(j)[-2:]+' column')
    head=solution.split(r'\\  & =')[0]
    # Source-preserved first stage displays both complete matrices. Next stages:
    # selected row/column, dot product expansion, signed terms, final integer.
    dot=r'\cdot ' if r'\cdot' in src[':question/worked-solution'] else ''
    expansion='+'.join(factor(a)+dot+factor(b) if dot else factor(a)+'('+str(b)+')' for a,b in zip(row,col))
    signed=''.join(('+' if k and n>=0 else '')+str(n) for k,n in enumerate(terms))
    stages=[matrix([row])+matrix([[x] for x in col]),expansion,signed,str(answer)+'.']
    solution=head+r'\\  & ='+(r' \\  & ='.join(stages))+r'\end{aligned}'+'\n$$'
    if replay:
        assert (i,j)==(oi+1,oj+1);problem=src[':question/problem'];solution=src[':question/worked-solution']
    identity=json.dumps([VERSION,mid,i,j],separators=(',',':'));qid=str(uuid.uuid5(uuid.UUID(SOURCE[':knowledge-point/id']),identity));sf=src[':question/answer-fields'][0];fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+sf[':answer-field/key']));choices=[];correct=None
    for a in sf[':answer-field/choices']:
        is_key=a[':answer/id']==sf[':answer-field/correct'][':answer/id'];aid=str(uuid.uuid5(uuid.UUID(fid),'source-recipe:'+a[':answer/id']));val=str(answer) if is_key else a[':answer/value']
        choices.append({':answer/id':aid,':answer/type':a[':answer/type'][':db/ident'],':answer/value':val})
        if is_key:correct=aid
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':sf[':answer-field/key'],':answer-field/type':sf[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',correct],':answer-field/choices':choices}]}
    return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'generation':{'version':VERSION,'seed':seed,'template':mid,'parameters':p,'bank_profile':t['profile'],'source_question':src[':question/id'],'source_db_id':src[':db/id'],'source_basis':CAPTURE['basis'],'source_lineage':CAPTURE['lineage'],'eligible_for_learning':not replay,'evidence_only':replay,'sympy_version':sp.__version__,'python_version':sys.version.split()[0],'domains':'all eligible product cells in source matrices; fixed distractor collisions excluded','entry_policy':'fixed source matrices; only selected dot products create distinct tasks'}}
def candidates(level,seed=0):
    if level not in SUPPORTED:raise ValueError('Unsupported difficulty: '+level)
    out=[];used=set()
    for mid in sorted(TEMPLATES):
        for i,j in domain(mid):
            r=generate(level,seed,mid,{'row':i,'column':j});fp=fingerprint(r['question'])
            if fp not in used:used.add(fp);out.append(r)
    random.Random(seed).shuffle(out);return out
def easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\n'+json.dumps(q[':question/answer-fields'],indent=2)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True,choices=SUPPORTED);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=('json','markdown'),default='json');a=p.parse_args();rs=candidates(a.difficulty,a.seed)
    if not 0<=a.count<=len(rs):p.error('finite distinct task limit: '+str(len(rs)))
    print(json.dumps(rs[:a.count],indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs[:a.count])))
