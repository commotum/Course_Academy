#!/usr/bin/env python3
"""Bounded scalar-curl generator: source-backed easy/moderate radio templates.

A positive integer constant scales both components, all intermediate solution
rows and each complete source bank. No seed, UUID or option shuffle changes the
mathematical identity. Hard and context-dependent blanks are unsupported here.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186133898-source-policy.json'))
    raise SystemExit(0)

import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('');sys.path.insert(0,str(HERE))
from math_reader import clean,parse,displayed,derivative_inputs,x,y
KP_ID=17592186133898
CAPTURE=json.loads((HERE/'source.json').read_text());SOURCE=CAPTURE['record']
SOURCE_BY_ID={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
EXCLUDED={'q-126427':'unrated; no correct link or solution', 'q-168118':'prompt omits supplied vector field', 'q-169202':'prompt omits supplied vector field'}
TEMPLATES={mid:{'level':q[':question/difficulty'][':db/ident'].split('/')[-1], 'profile':'source-bank:'+mid,'source_db_id':q[':db/id']} for mid,q in SOURCE_BY_ID.items() if mid not in EXCLUDED}
VERSION='scalar-curl-scale-v1'
SCALES=tuple(range(2,10))

def scale(s,c):return s if c==1 else str(c)+r'\left('+s.strip().rstrip('.,')+r'\right)'

def solution(src,c):
    s=src
    if c==1:return s
    def block(m):
        out=[]
        for row in m[1].split(r'\\'):
            if '& =' not in row:out.append(row);continue
            lhs,rhs=row.split('& =',1)
            ds=derivative_inputs(rhs)
            if ds:
                for _,arg,a,b in reversed(ds):rhs=rhs[:a]+scale(arg,c)+rhs[b:]
            else:rhs=scale(rhs,c)
            out.append(lhs+'& ='+rhs)
        return r'\begin{aligned}'+r'\\'.join(out)+r'\end{aligned}'
    return re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,s,flags=re.S)

def generate(level,seed=0,template=None,parameters=None,profile=None):
    if level not in ('easy','moderate'):raise ValueError('Unsupported band: '+level)
    rng=random.Random(seed);templates=sorted(mid for mid,t in TEMPLATES.items() if t['level']==level)
    template=template or rng.choice(templates);assert template in templates
    c=(parameters or {}).get('c',rng.choice(SCALES));assert c==1 or c in SCALES
    assert profile is None or profile==TEMPLATES[template]['profile']
    src=SOURCE_BY_ID[template];P,Q,pt=displayed(src);D=sp.simplify(sp.diff(c*Q,x)-sp.diff(c*P,y))
    ans=sp.simplify(D.subs(dict(zip((x,y),pt)),simultaneous=True)) if pt else D
    # Compute correct mathematics before authoring the source-bank recipes.
    sf=src[':question/answer-fields'][0];correct_src=sf[':answer-field/correct'][':answer/id']
    bank=[(a,c*parse(a[':answer/value'])) for a in sf[':answer-field/choices']]
    assert all((sp.simplify(v-ans)==0)==(a[':answer/id']==correct_src) for a,v in bank)
    assert all(sp.simplify(a[1]-b[1])!=0 for k,a in enumerate(bank) for b in bank[k+1:])
    problem=src[':question/problem']
    if c!=1:
        problem=re.sub(r'(F\(x,y\)\s*=)([^$]+)',lambda m:m[1]+scale(m[2],c),problem)
    identity=json.dumps([VERSION,template,c],separators=(',',':'));qid=str(uuid.uuid5(uuid.UUID(SOURCE[':knowledge-point/id']),identity));fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+sf[':answer-field/key']))
    choices=[];correct=None
    for a,val in bank:
        aid=str(uuid.uuid5(uuid.UUID(fid),'source-option:'+a[':answer/id']))
        # Fix captured escaped-backslash and function-application artifacts in new content only.
        choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':scale(clean(a[':answer/value']),c)})
        if a[':answer/id']==correct_src:correct=aid
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution(src[':question/worked-solution'],c),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':sf[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',correct],':answer-field/choices':choices}]}
    return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'generation':{'version':VERSION,'seed':seed,'parameters':{'c':c},'template':template,'bank_profile':TEMPLATES[template]['profile'],'source_question':src[':question/id'],'source_db_id':src[':db/id'],'source_basis':CAPTURE['basis'],'source_lineage':CAPTURE['lineage'],'domain':'source domain unchanged by positive scalar; log arguments positive at evaluation points; rational field excludes origin','sympy_version':sp.__version__,'python_version':sys.version.split()[0],'eligible_for_learning':c!=1,'evidence_only':c==1}}

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186133898-source-policy.json'))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard'],required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
    if a.difficulty=='hard':p.error('hard is unsupported; see capabilities.json')
    candidates=[generate(a.difficulty,a.seed,t,{'c':c}) for t in sorted(TEMPLATES) if TEMPLATES[t]['level']==a.difficulty for c in SCALES];random.Random(a.seed).shuffle(candidates)
    if a.count>len(candidates):p.error('finite limit: '+str(len(candidates)))
    if a.count<0:p.error('count must be nonnegative')
    out=candidates[:a.count];print(json.dumps(out,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
