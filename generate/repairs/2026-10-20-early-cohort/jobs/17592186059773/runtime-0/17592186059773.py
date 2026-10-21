"""Moderate row-operation identification; bounded source-bank-preserving variants.

Numeric slots change one nonzero supplied entry by -3..3 without changing sign.
Target rows vary by a simultaneous permutation of matrices and complete banks.
Row relabeling, seeds and bank order alone are excluded from mathematical novelty.
"""
import argparse, hashlib, itertools, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186059773
KP_UUID='691b9107-a935-5965-b3ac-0f3a193ce9bd'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'row-operation-generator-v1'))
SUPPORTED_LEVELS=('moderate',)
VERSION='1.0.0'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions'] if q.get(':question/difficulty') and q.get(':question/worked-solution') and q[':question/answer-fields'][0].get(':answer-field/correct')}
DEFAULTS={sid:[sid,0,0,0,[0,1,2]] for sid in CASES}
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def matrices(text):
    return [sp.Matrix([[sp.Rational(c.strip()) for c in row.split('&')] for row in m.split(r'\\')]) for m in MAT.findall(text)]

def latex(m):
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(str(m[i,j]) for j in range(3)) for i in range(3))+r'\end{bmatrix}'

def operation(text):
    """Read source row expressions, including the two non-elementary distractors."""
    text=re.sub(r'\{R\}_\{([123])\}|R_\{([123])\}',lambda m:'r'+(m[1] or m[2]),text)
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text)
    text=text.replace(r'\cdot','*').replace(' ','')
    if '↔' in text:
        a,b=text.split('↔');return ('swap',int(a[1:])-1,int(b[1:])-1)
    lhs,rhs=text.split(':=');i=int(lhs[1:])-1
    rhs=re.sub(r'(\d|\))(?=r)',r'\1*',rhs)
    rs=sp.symbols('r1 r2 r3');expr=sp.sympify(rhs,locals=dict(zip(('r1','r2','r3'),rs)))
    assert sp.expand(expr).subs(dict.fromkeys(rs,0))==0
    cs=tuple(sp.expand(expr).coeff(r) for r in rs)
    assert sp.expand(expr)==sum(c*r for c,r in zip(cs,rs))
    return ('replace',i,cs)

def apply(m,op):
    result=m.copy()
    if op[0]=='swap':result.row_swap(op[1],op[2])
    else:
        row=sp.zeros(1,3)
        for j,c in enumerate(op[2]):row+=c*m[j,:]
        result[op[1],:]=row
    return result

def permute_text(text,p):
    inverse={old:new for new,old in enumerate(p)}
    text=re.sub(r'(\{R\}_\{|R_\{)([123])(\})',lambda m:m[1]+str(inverse[int(m[2])-1]+1)+m[3],text)
    ordinal=('st','nd','rd')
    text=re.sub(r'\$([123])\$(?:st|nd|rd)',lambda m:'$'+str(inverse[int(m[1])-1]+1)+'$'+ordinal[inverse[int(m[1])-1]],text)
    return text

def fingerprint(q):
    ms=matrices(q[':question/problem'])
    if len(ms)!=2:return hashlib.sha256(q[':question/problem'].encode()).hexdigest()
    # Ignore matrix names, row labels, bank profile/order and uniform scaling.
    canonical=[]
    for p in itertools.permutations(range(3)):
        values=[x for m in ms for i in p for x in m[i,:]]
        pivot=next((x for x in values if x),sp.Integer(1))
        canonical.append(tuple(str(x/pivot) for x in values))
    return hashlib.sha256(json.dumps(min(canonical)).encode()).hexdigest()

def generate(difficulty='moderate',seed=0,template=None,parameters=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed)
    if parameters is None:
        template=template or rng.choice(list(CASES));parameters=rng.choice(domain(template))
    sid,i,j,delta,p=parameters
    assert sid in CASES and template in (None,sid) and sorted(p)==[0,1,2]
    source=CASES[sid];a,b=matrices(source[':question/problem']);f=source[':question/answer-fields'][0]
    correct=f[':answer-field/correct'][':answer/value'];op=operation(correct)
    if delta:
        assert i in range(3) and j in range(3) and delta in (-3,-2,-1,1,2,3)
        assert a[i,j] and (a[i,j]+delta)*a[i,j]>0
        a[i,j]+=delta
    b=apply(a,op)
    a=a[list(p),:];b=b[list(p),:]
    def render(text):
        counter=iter([a,b]);text=MAT.sub(lambda _:latex(next(counter)),text)
        return permute_text(text,p)
    # Exact original layout retained on source replay.
    replay=delta==0 and p==[0,1,2]
    problem=source[':question/problem'] if replay else render(source[':question/problem'])
    solution=source[':question/worked-solution'] if replay else render(source[':question/worked-solution'])
    vals=[permute_text(c[':answer/value'],p) for c in f[':answer-field/choices']]
    correct=permute_text(correct,p)
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),json.dumps([parameters,vals],sort_keys=True)))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(c[':answer/id'] for c in answers if c[':answer/value']==correct)]}
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID},'question':q,'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'parameters':parameters,'template':sid,'bank_profile':sid,'source_question_id':source[':question/id'],'source_basis':2368,'dependencies':{'sympy':sp.__version__},'assets':[],'mathematical_fingerprint':fingerprint(q)}}

def domain(sid):
    a,_=matrices(CASES[sid][':question/problem'])
    return [[sid,i,j,d,list(p)] for i in range(3) for j in range(3) for d in (-3,-2,-1,1,2,3) if a[i,j] and (a[i,j]+d)*a[i,j]>0 for p in itertools.permutations(range(3))]

def batch(difficulty,count,seed=0):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    params=[x for sid in CASES for x in domain(sid)];random.Random(seed).shuffle(params)
    seen=set();result=[]
    for p in params:
        rec=generate(difficulty,seed,parameters=p);fp=fingerprint(rec['question'])
        if fp in seen:continue
        seen.add(fp);result.append(rec)
        if len(result)==count:return result
    if count:raise ValueError('Finite variant limit reached: '+str(len(result)))
    return []

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='moderate');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=59773);args=parser.parse_args()
    print(json.dumps({'instances':batch(args.difficulty,args.count,args.seed)},indent=2))
