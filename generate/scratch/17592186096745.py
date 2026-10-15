"""Hard, two-pivot 3x3 RREF generator. See package/template-extraction.md.

Conservative RHS scaling is an explicit same-method generalization. It changes
the affine solution set, not identities or option order. No source is edited.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186096745
KP_UUID='b010a518-7aa3-5b53-9a6d-ef0779ff0dfa'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
VERSION='two-pivot-rref-rhs-v1'
HERE=Path(__file__).with_suffix('')
PROFILES=('q-131632','q-74617','q-74618','q-131636','q-74621')
SCALES=(-5,-4,-3,-2,-1,1,2,3,4,5)
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)

def sources():
    return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}

def parse_matrix(value):
    body=MATRIX.fullmatch(value.strip())
    if not body: raise ValueError('Expected complete matrix')
    return sp.Matrix([[sp.Rational(v.strip()) for v in row.split('&')] for row in body[1].split('\\\\')])

def matrix_tex(matrix):
    return r'\begin{bmatrix}'+' \\\\ '.join(' & '.join(sp.latex(v) for v in row) for row in matrix.tolist())+r'\end{bmatrix}'

def scale_matrix(value,k):
    m=parse_matrix(value)
    assert m.shape==(3,4)
    m[:,3]=m[:,3]*k
    return matrix_tex(m)

def scale_matrices(text,k):
    return MATRIX.sub(lambda m:scale_matrix(m[0],k),text)

def prompt_matrix(text):
    body=text.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
    variables=sp.symbols('x y z');rows=[]
    for row in body.split('\\\\'):
        lhs,rhs=row.replace('&','').split('=')
        lhs=re.sub(r'(\d)([xyz])',r'\1*\2',lhs)
        expr=sp.sympify(lhs,locals=dict(zip(('x','y','z'),variables)))
        rows.append([expr.coeff(v) for v in variables]+[sp.Rational(rhs.strip())])
    return sp.Matrix(rows)

def fingerprint(q):
    # Canonical row space of the augmented system: equivalent row scalings,
    # reorderings, option banks and seeds never create fresh mathematics.
    r=prompt_matrix(q[':question/problem']).rref()[0]
    return hashlib.sha256(str(r.tolist()).encode()).hexdigest()

def candidates(level):
    if level!='hard':raise ValueError('Unsupported difficulty: '+level)
    return [{'profile':p,'scale':k} for p in PROFILES for k in SCALES]

def generate(difficulty='hard',seed=0,template=None,parameters=None,replay=False):
    if difficulty!='hard': raise ValueError('Only hard is source-supported')
    rng=random.Random(seed);profile=template or rng.choice(PROFILES)
    if profile not in PROFILES:raise ValueError('Unsupported source profile')
    p=parameters or {'scale':rng.choice(SCALES)};k=p['scale']
    if type(k)!=int or k not in SCALES:raise ValueError('Scale outside validated bounded domain')
    source=sources()[profile];f=source[':question/answer-fields'][0]
    # Only equation RHS integers change. Matrix column 4 uses the same k.
    prompt=re.sub(r'&=\s*(-?\d+)',lambda m:'&='+str(int(m[1])*k),source[':question/problem'])
    solution=scale_matrices(source[':question/worked-solution'],k)
    identity=uuid.uuid5(uuid.UUID(GENERATOR_UUID),VERSION+'|'+profile+'|'+str(k))
    fid=uuid.uuid5(identity,'field:'+f[':answer-field/key'])
    answers=[];correct=None
    for a in f[':answer-field/choices']:
        typ=a[':answer/type'][':db/ident'];value=scale_matrix(a[':answer/value'],k) if typ==':answer.type/math' else a[':answer/value']
        aid=str(uuid.uuid5(fid,typ+'|'+value))
        answers.append({':answer/id':aid,':answer/type':typ,':answer/value':value})
        if a[':answer/id']==f[':answer-field/correct'][':answer/id']:correct=aid
    q={':question/id':str(identity),':question/problem':prompt,':question/worked-solution':solution,
       ':question/difficulty':':question.difficulty/hard',':question/answer-fields':[
           {':answer-field/id':str(fid),':answer-field/key':f[':answer-field/key'],':answer-field/type':':answer-field.type/radio',
            ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    return {'question':q,'knowledge_point':{'id':KP_ID,'title':json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/title']},
            'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':profile,'profile':profile,
                          'parameters':{'scale':k},'replay':replay,'source_question':source[':question/id'],
                          'source_db_id':source[':db/id'],'source_basis':json.loads((HERE/'source.json').read_text())['basis'],
                          'domain':{'scale':list(SCALES),'coefficient_matrix':'fixed per source profile','pivot_columns':[1,2]},
                          'choice_recipes':'Complete source-profile matrices; columns 1–3 fixed, column 4 multiplied by scale; text unchanged',
                          'mathematical_fingerprint':fingerprint(q),'dependencies':{'sympy':sp.__version__}}}

def batch(difficulty,count,seed=0):
    domain=candidates(difficulty);random.Random(seed).shuffle(domain)
    if count<0:raise ValueError('Negative count')
    if count==0:return []
    result=[];seen=set()
    for item in domain:
        r=generate(difficulty,seed,item['profile'],{'scale':item['scale']})
        fp=r['generation']['mathematical_fingerprint']
        if fp not in seen:result.append(r);seen.add(fp)
        if len(result)==count:return result
    raise ValueError(f'Finite domain has only {len(result)} distinct tasks; requested {count}')

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n\n'.join('$$'+a[':answer/value']+'$$' if a[':answer/type']==':answer.type/math' else a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='hard');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=('json','markdown'),default='json')
    args=parser.parse_args();records=batch(args.difficulty,args.count,args.seed)
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
