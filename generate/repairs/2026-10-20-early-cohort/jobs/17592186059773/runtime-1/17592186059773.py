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
VERSION='1.1.0'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions'] if q.get(':question/difficulty') and q.get(':question/worked-solution') and q[':question/answer-fields'][0].get(':answer-field/correct')}
DEFAULTS={sid:[sid,0,0,0,[0,1,2]] for sid in CASES}
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def matrices(text):
    def rational(c):
        c=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',c.strip())
        return sp.Rational(sp.sympify(c))
    return [sp.Matrix([[rational(c) for c in row.split('&')] for row in m.split(r'\\')]) for m in MAT.findall(text)]

def latex(m):
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(sp.latex(m[i,j]) for j in range(3)) for i in range(3))+r'\end{bmatrix}'

def operation(text):
    """Read source row expressions, including the two non-elementary distractors."""
    text=re.sub(r'\{R\}_\{([123])\}|R_\{([123])\}',lambda m:'r'+(m[1] or m[2]),text)
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text)
    text=text.replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(' ','')
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

class InvalidInstance(ValueError):
    pass

def eligible_keys(sid):
    """Only the three lesson-defined elementary forms can produce the target."""
    result=[]
    for k,choice in enumerate(CASES[sid][':question/answer-fields'][0][':answer-field/choices']):
        op=operation(choice[':answer/value'])
        if op[0]=='swap':
            result.append(k)
        else:
            i,cs=op[1:];others=[c for j,c in enumerate(cs) if j!=i and c]
            if (not others and cs[i] not in (0,1)) or (cs[i]==1 and len(others)==1):
                result.append(k)
    return result

def worked_solution(source,a,b,correct):
    changed=[i for i in range(3) if a[i,:]!=b[i,:]]
    unchanged=[i for i in range(3) if i not in changed]
    def rows(indices):
        return ' and '.join('$'+str(i+1)+'$'+('st','nd','rd')[i] for i in indices)
    first=('First, notice that the '+rows(unchanged)+(' row is' if len(unchanged)==1 else ' rows are')+
           ' the same in both matrices. The only '+('row that has changed is' if len(changed)==1 else 'rows that have changed are')+
           ' the '+rows(changed)+(' row.' if len(changed)==1 else ' rows.'))
    names=re.findall(r'matrix\s+\$(\w+)\$',source[':question/problem'])[:2]
    left,right=names
    return (first+'\n\nBy considering the given row operations that '+
            ('modify the '+rows(changed)+' row' if len(changed)==1 else 'change both the '+rows(changed)+' rows')+
            ', we notice that\n\n$$\n'+r'\begin{aligned}'+left+' & ='+latex(a)+' & '+correct+
            r' \\ & \sim'+latex(b)+r' \\ & ='+right+r'.\end{aligned}'+'\n$$\n\nTherefore, the required row operation is\n\n$$\n'+correct+'.\n$$')

def generate(difficulty='moderate',seed=0,template=None,parameters=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed)
    if parameters is None:
        template=template or rng.choice(list(CASES))
        key=rng.choice(eligible_keys(template))
        parameters=rng.choice(domain(template))+[key]
    if len(parameters) not in (5,6):raise ValueError('Expected five legacy parameters or six with selected key')
    sid,i,j,delta,p=parameters[:5]
    assert sid in CASES and template in (None,sid) and sorted(p)==[0,1,2]
    source=CASES[sid];a,b=matrices(source[':question/problem']);f=source[':question/answer-fields'][0]
    original=f[':answer-field/correct'][':answer/value']
    original_key=next(k for k,c in enumerate(f[':answer-field/choices']) if c[':answer/value']==original)
    key=parameters[5] if len(parameters)==6 else original_key
    if key not in eligible_keys(sid):raise ValueError('Selected operation is not elementary')
    correct=f[':answer-field/choices'][key][':answer/value'];op=operation(correct)
    if delta:
        assert i in range(3) and j in range(3) and delta in (-3,-2,-1,1,2,3)
        assert a[i,j] and (a[i,j]+delta)*a[i,j]>0
        a[i,j]+=delta
    b=apply(a,op)
    outcomes=[apply(a,operation(c[':answer/value'])) for c in f[':answer-field/choices']]
    if a==b or sum(out==b for out in outcomes)!=1 or len({tuple(out) for out in outcomes})!=len(outcomes):
        raise InvalidInstance('Ambiguous or duplicate operation outcomes')
    a=a[list(p),:];b=b[list(p),:]
    def render(text):
        counter=iter([a,b]);text=MAT.sub(lambda _:latex(next(counter)),text)
        return permute_text(text,p)
    # Exact original layout retained on source replay.
    replay=delta==0 and p==[0,1,2] and key==original_key
    problem=source[':question/problem'] if replay else render(source[':question/problem'])
    solution=(source[':question/worked-solution'] if replay else
              render(source[':question/worked-solution']) if key==original_key else
              worked_solution(source,a,b,permute_text(correct,p)))
    vals=[permute_text(c[':answer/value'],p) for c in f[':answer-field/choices']]
    correct=permute_text(correct,p)
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),json.dumps([parameters,vals],sort_keys=True)))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in vals]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(c[':answer/id'] for c in answers if c[':answer/value']==correct)]}
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID},'question':q,'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'parameters':parameters,'selected_key':key,'template':sid,'bank_profile':sid,'source_question_id':source[':question/id'],'source_basis':5359,'dependencies':{'sympy':sp.__version__},'assets':[],'mathematical_fingerprint':fingerprint(q)}}

def domain(sid):
    a,_=matrices(CASES[sid][':question/problem'])
    return [[sid,i,j,d,list(p)] for i in range(3) for j in range(3) for d in (-3,-2,-1,1,2,3) if a[i,j] and (a[i,j]+d)*a[i,j]>0 for p in itertools.permutations(range(3))]

def batch(difficulty,count,seed=0):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
    if count<0:raise ValueError('Count must be nonnegative')
    if count==0:return []
    rng=random.Random(seed)
    domains={sid:domain(sid) for sid in CASES}
    seen=set();result=[]
    for _ in range(max(100,count*100)):
        sid=rng.choice(list(CASES));key=rng.choice(eligible_keys(sid))
        p=rng.choice(domains[sid])+[key]
        try:rec=generate(difficulty,seed,parameters=p)
        except InvalidInstance:continue
        fp=rec['generation']['mathematical_fingerprint']
        if fp in seen:continue
        seen.add(fp);result.append(rec)
        if len(result)==count:return result
    if count:raise ValueError('Finite variant limit reached: '+str(len(result)))
    return []

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=SUPPORTED_LEVELS,default='moderate');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=59773);parser.add_argument('--format',choices=('json',),default='json');args=parser.parse_args()
    print(json.dumps({'instances':batch(args.difficulty,args.count,args.seed)},indent=2))
