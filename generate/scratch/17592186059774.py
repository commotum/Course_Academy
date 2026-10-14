"""Hard row-operation identification; bounded source-bank-preserving variants.

Numeric slots change an assessed-column entry by -3..3 without changing sign.
The target entry follows its exact elimination relation.
Target rows and columns vary by simultaneous permutation of matrices, targets and banks.
Row relabeling, seeds and bank order alone are excluded from mathematical novelty.
"""
from functools import lru_cache
import argparse, hashlib, itertools, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186059774
KP_UUID='0464b51e-8568-521e-96a5-a65c04569c2a'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'row-operation-generator-v1'))
SUPPORTED_LEVELS=('hard',)
VERSION='1.0.0'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions'] if q.get(':question/difficulty') and q.get(':question/worked-solution') and q[':question/answer-fields'][0].get(':answer-field/correct')}
DEFAULTS={sid:[sid,0,0,0,[0,1,2],[0,1,2]] for sid in CASES}
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def matrices(text):
    return [sp.Matrix([[sp.Rational(re.sub(r"\\frac\{(-?\d+)\}\{(\d+)\}",r"\1/\2",c.replace(r"\,", "").strip())) for c in row.split('&')] for row in m.split(r'\\')]) for m in MAT.findall(text)]

def latex(m):
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(sp.latex(m[i,j]) for j in range(3)) for i in range(3))+r'\end{bmatrix}'

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

def target(text):
    m=re.search(r'a\}_\{([123])([123])\}',text)
    if m is None:m=re.search(r'a_\{([123])([123])\}',text)
    return int(m[1])-1,int(m[2])-1

def fingerprint(q):
    a=matrices(q[':question/problem'])[0];i,j=target(q[':question/problem'])
    # Target column alone is assessed. Ignore row/column names, option order,
    # other matrix columns, and a common nonzero scaling of target entries.
    canonical=[]
    for p in itertools.permutations(range(3)):
        vals=[a[k,j] for k in p];pivot=next((x for x in vals if x),sp.Integer(1))
        canonical.append((p.index(i),tuple(str(x/pivot) for x in vals)))
    return hashlib.sha256(json.dumps(min(canonical)).encode()).hexdigest()

def generate(difficulty='hard',seed=0,template=None,parameters=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed)
    if parameters is None:
        template=template or rng.choice(list(CASES));parameters=rng.choice(domain(template))
    sid,i,j,delta,p,cols=parameters
    assert sid in CASES and template in (None,sid) and sorted(p)==[0,1,2]
    source=CASES[sid];a=matrices(source[':question/problem'])[0];f=source[':question/answer-fields'][0];ti,tj=target(source[':question/problem'])
    correct=f[':answer-field/correct'][':answer/value'];op=operation(correct)
    if delta:
        assert i in range(3) and j in range(3) and delta in (-3,-2,-1,1,2,3)
        assert a[i,j] and (a[i,j]+delta)*a[i,j]>0
        a[i,j]+=delta
        if j==tj:
            coeffs=op[2];other=next(k for k in range(3) if k!=ti and coeffs[k])
            a[ti,tj]=-coeffs[other]*a[other,tj]
    b=apply(a,op)
    a=a[list(p),list(cols)];b=b[list(p),list(cols)]
    def render(text):
        counter=iter([a,b]);text=MAT.sub(lambda _:latex(next(counter)),text)
        text=permute_text(text,p)
        invr={old:new+1 for new,old in enumerate(p)};invc={old:new+1 for new,old in enumerate(cols)}
        return re.sub(r'(a\}_\{|a_\{)([123])([123])(\})',lambda m:m[1]+str(invr[int(m[2])-1])+str(invc[int(m[3])-1])+m[4],text)
    # Exact original layout retained on source replay.
    replay=delta==0 and p==[0,1,2] and cols==[0,1,2]
    problem=source[':question/problem'] if replay else render(source[':question/problem'])
    solution=source[':question/worked-solution'] if replay and sid!='q-130301' else render(source[':question/worked-solution'])
    vals=[permute_text(c[':answer/value'],p) for c in f[':answer-field/choices']]
    correct=permute_text(correct,p)
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),json.dumps([parameters,vals],sort_keys=True)))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(c[':answer/id'] for c in answers if c[':answer/value']==correct)]}
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/hard',':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID},'question':q,'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'parameters':parameters,'template':sid,'bank_profile':sid,'source_question_id':source[':question/id'],'source_basis':2369,'dependencies':{'sympy':sp.__version__},'assets':[],'mathematical_fingerprint':fingerprint(q)}}

@lru_cache(None)
def domain(sid):
    a=matrices(CASES[sid][':question/problem'])[0];ti,tj=target(CASES[sid][':question/problem'])
    # Vary a non-target entry in the assessed column. If it is the source
    # row, adjust the target coherently to retain the complete bank coefficient.
    # Reject ambiguity against the entire original bank.
    result=[]
    for i in range(3):
        if i==ti:continue
        for d in (-3,-2,-1,1,2,3):
            if not a[i,tj] or (a[i,tj]+d)*a[i,tj]<=0:continue
            par=[sid,i,tj,d,[0,1,2],[0,1,2]]
            rec=generate('hard',parameters=par);q=rec['question'];m=matrices(q[':question/problem'])[0];r,c=target(q[':question/problem'])
            f=q[':question/answer-fields'][0]
            good=[x[':answer/id'] for x in f[':answer-field/choices'] if apply(m,operation(x[':answer/value']))[r,c]==0]
            if good==[f[':answer-field/correct'][1]] and all(x.is_Integer for x in m):
                result.extend([sid,i,tj,d,list(p),list(cols)] for p in itertools.permutations(range(3)) for cols in itertools.permutations(range(3)))
    return result

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
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='hard');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=59774);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
    records=batch(args.difficulty,args.count,args.seed)
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))
