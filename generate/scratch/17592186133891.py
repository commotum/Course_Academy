#!/usr/bin/env python3
"""Source-shaped, bounded easy generators for constructing dx line integrals.

A positive integer multiplies the supplied scalar function, not the path.
This conservative same-method slot changes the integrand and dependent setup.
Every observed complete bank is replayable; ambiguous banks are evidence only.
Moderate and hard have no supported templates in this package.
"""
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('');ROOT=HERE.parents[2];sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT))
from math_reader import parse,integral,x,y,t
from scripts.question_capture.math_format import normalize_prose,normalize_tex,checked_math_content
KP_ID=17592186133891;VERSION='dx-line-integral-scalar-v1';SCALES=tuple(range(2,10))
CAPTURE=json.loads((HERE/'source.json').read_text());SOURCE=CAPTURE['record'];SOURCE_BY_ID={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
EXCLUDED={'q-124119':'unrated; correct answer and worked solution absent','q-124223':'four definite integrals equal zero','q-124226':'two wrong definite integrals equal zero','q-124246':'two wrong definite integrals equal zero'}
# Independent transcription of supplied functions and parametrizations.
MODELS={
'q-124230':(x-y,5*sp.cos(t),4*sp.sin(t),3*sp.pi/2,2*sp.pi),
'q-124223':(x*y**2,sp.cos(t),sp.sqrt(3)*sp.sin(t),sp.pi/2,3*sp.pi/2),
'q-124234':(x+y**2,3*t-1,t+1,sp.Integer(0),sp.Integer(1)),
'q-124226':(2*y,2*sp.cos(t),3*sp.sin(t),sp.Integer(0),sp.pi),
'q-124218':(y*sp.exp(x),2*sp.cos(t),2*sp.sin(t),sp.pi/2,sp.pi),
'q-124221':(x+y,4*sp.cos(t),4*sp.sin(t),sp.pi,2*sp.pi),
'q-124246':(x**2*y,2*t-2,3-3*t,sp.Integer(0),sp.Integer(1))}
TEMPLATES={mid:{'level':'easy','profile':'source-bank:'+mid,'source_db_id':SOURCE_BY_ID[mid][':db/id']} for mid in MODELS if mid not in EXCLUDED}

def scale(s,c):return s if c==1 else str(c)+r'\left('+s.strip().rstrip('.,')+r'\right)'
def problem(src,c):
    if c==1:return src
    m=re.search(r'(\{\\int \}_\{C\})(.*?)(\\,\\text\{d\}x)',src);assert m
    return src[:m.start(2)]+scale(m[2],c)+src[m.end(2):]
def solution(src,c):
    if c==1:return src
    # Scale the explicit f definition, each source substitution/collection row,
    # and each concrete integral row. Geometry and dx/dt rows remain exact.
    src=re.sub(r'(f\(x,y\)\s*=)([^$]+)',lambda m:m[1]+scale(m[2],c),src)
    def block(m):
        b=m[1]
        if b.startswith('f(r(t))'):
            rows=b.split(r'\\');out=[]
            for row in rows:
                lhs,rhs=row.split('& =',1);out.append(lhs+'& ='+scale(rhs,c))
            return r'\begin{aligned}'+r'\\'.join(out)+r'\end{aligned}'
        if b.startswith(r'{\int }_{C}'):
            rows=b.split(r'\\');out=[]
            for k,row in enumerate(rows):
                lhs,rhs=row.split('& =',1)
                if k:rhs=scale(rhs,c)
                out.append(lhs+'& ='+rhs)
            return r'\begin{aligned}'+r'\\'.join(out)+r'\end{aligned}'
        return m[0]
    return re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,src,flags=re.S)

@checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None):
    if level!='easy':raise ValueError('Unsupported band: '+level)
    rng=random.Random(seed);template=template or rng.choice(sorted(TEMPLATES));assert template in MODELS
    c=(parameters or {}).get('c',rng.choice(SCALES));assert isinstance(c,int) and (c==1 or c in SCALES)
    assert template in TEMPLATES or c==1,'Ambiguous source bank is replay only'
    assert profile is None or profile=='source-bank:'+template
    src=SOURCE_BY_ID[template];sf=src[':question/answer-fields'][0];f,X,Y,a,b=MODELS[template]
    F=c*f.subs({x:X,y:Y},simultaneous=True);correct=sp.simplify(F*sp.diff(X,t))
    ca=sf[':answer-field/correct'][':answer/id'];aa,bb,v=integral(sf[':answer-field/correct'][':answer/value']);assert (aa,bb)==(a,b) and sp.simplify(c*v-correct)==0
    obj=[VERSION,level,template,c,'source-bank:'+template]
    qid=str(uuid.uuid5(uuid.UUID(SOURCE[':knowledge-point/id']),json.dumps(obj,separators=(',',':'))));fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+sf[':answer-field/key']));choices=[];correct_id=None
    for opt in sf[':answer-field/choices']:
        aid=str(uuid.uuid5(uuid.UUID(fid),'source-option:'+opt[':answer/id']));choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':normalize_tex(scale(opt[':answer/value'],c))})
        if opt[':answer/id']==ca:correct_id=aid
    rng.shuffle(choices)
    q={':question/id':qid,':question/problem':normalize_prose(problem(src[':question/problem'],c)),':question/worked-solution':normalize_prose(solution(src[':question/worked-solution'],c)),':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':sf[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]}
    return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'generation':{'version':VERSION,'seed':seed,'parameters':{'c':c},'template':template,'bank_profile':'source-bank:'+template,'source_question':src[':question/id'],'source_db_id':src[':db/id'],'source_basis':CAPTURE['basis'],'source_lineage':CAPTURE['lineage'],'domain':'real path parameter on source closed interval; same path, orientation and supplied hint','sympy_version':sp.__version__,'python_version':sys.version.split()[0],'eligible_for_learning':c!=1 and template in TEMPLATES,'evidence_only':c==1,'mathematical_fingerprint':hashlib.sha256(json.dumps([str(F),str(X),str(Y),str(a),str(b)]).encode()).hexdigest()}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(*args,**kwargs):raise ValueError('moderate unsupported')
def generate_hard(*args,**kwargs):raise ValueError('hard unsupported')
def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True,choices=['easy','moderate','hard']);p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
    if a.difficulty!='easy':p.error('unsupported band: '+a.difficulty)
    candidates=[generate('easy',a.seed,mid,{'c':c}) for mid in sorted(TEMPLATES) for c in SCALES];random.Random(a.seed).shuffle(candidates)
    if not 0<=a.count<=len(candidates):p.error('finite variant limit: '+str(len(candidates)))
    print(json.dumps(candidates[:a.count],indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,candidates[:a.count])))
