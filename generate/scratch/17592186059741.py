"""Easy scalar recovery: source-shaped matrices, complete radio banks and blanks."""
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import matrix_tex, normalize_prose, normalize_tex, checked_math_content
KP_ID=17592186059741
KP_UUID='2da3580a-6a1a-5e38-bcab-bd35f1ea5a6e'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'scalar-generator-v1'))
VERSION='1.0.0'
SUPPORTED_LEVELS=('easy',)
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
CASES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions'] if q.get(':question/math-academy-id') in ('q-981','q-320536','q-320551','q-320563','q-69670')}
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
k=sp.Symbol('k')
def parse(s):
    s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s).replace(' ','')
    s=re.sub(r'(\d|\))(?=k)',r'\1*',s)
    return sp.sympify(s,locals={'k':k},rational=True)
def matrices(s):return [sp.Matrix([[parse(c) for c in row.split('&')] for row in body.split(r'\\')]) for body in MAT.findall(s)]
def tex(x):return normalize_tex(sp.latex(x))
def mat(a):return matrix_tex([[tex(a[i,j]) for j in range(a.cols)] for i in range(a.rows)])
DEFAULTS={}
for sid,q in CASES.items():
    b,a=matrices(q[':question/problem']);ratio=next(y/x for x,y in zip(a,b) if x)
    pos={'q-981':[0,0],'q-320536':[1,0],'q-320551':[2,0],'q-320563':[0,2],'q-69670':[0,0]}[sid]
    DEFAULTS[sid]={'matrix':[[str(a[i,j]) for j in range(a.cols)] for i in range(a.rows)],'scalar':str(ratio),'target':pos}
def fingerprint(q):
    ms=matrices(q[':question/problem'])
    if len(ms)!=2:return hashlib.sha256(q[':question/problem'].encode()).hexdigest()
    b,a=ms;pivot=next(x for x in a if x)
    # Uniform matrix scaling, names, target wording, banks and seeds add no novelty.
    return hashlib.sha256(json.dumps([a.shape,[str(x/pivot) for x in a],[str(x/pivot) for x in b]]).encode()).hexdigest()
@checked_math_content
def generate(difficulty='easy',seed=0,template=None,parameters=None):
    if difficulty!='easy':raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed);sid=template or rng.choice(list(CASES));q=CASES[sid]
    if parameters is None:
        old=sp.Matrix(DEFAULTS[sid]['matrix']);den=rng.randint(2,6) if sid=='q-320563' else 1
        a=old.applyfunc(lambda x:sp.sign(x)*rng.randint(1,12)*den if x else 0)
        ratio=sp.Rational(1,den) if den>1 else sp.Integer(rng.randint(5,9) if sid=='q-981' else -rng.randint(6,9) if sid=='q-69670' else rng.randint(2,9))
        target=rng.choice([[i,j] for i in range(a.rows) for j in range(a.cols) if a[i,j]])
        parameters={'matrix':[[str(a[i,j]) for j in range(a.cols)] for i in range(a.rows)],'scalar':str(ratio),'target':target}
    a=sp.Matrix(parameters['matrix']);ratio=sp.Rational(parameters['scalar']);i,j=parameters['target'];old=sp.Matrix(DEFAULTS[sid]['matrix'])
    assert a.shape==old.shape and ratio and a[i,j]
    assert all(x.is_Integer and sp.sign(x)==sp.sign(y) for x,y in zip(a,old))
    b=ratio*a;ak=k*a
    assert all(x.is_Integer for x in b)
    # Keep the source's complete wording and solution stages, replacing dependent slots.
    it=iter([mat(b),mat(a)]);problem=MAT.sub(lambda _:next(it),q[':question/problem'])
    sol=q[':question/worked-solution'];it=iter([mat(a),mat(ak),mat(ak),mat(b)])
    sol=MAT.sub(lambda _:next(it),sol)
    original=sp.Matrix(DEFAULTS[sid]['matrix']);oi,oj=DEFAULTS[sid]['target']
    if [i,j]==[oi,oj]:
        target_text=sol.split("Let's choose ")[1].split(', $')[0]
    else:target_text=f'the elements in row ${i+1}$ and column ${j+1}$'
    start=sol.index("Let's choose ");end=sol.index('Equating these elements',start)
    sol=sol[:start]+f"Let's choose {target_text}, ${tex(a[i,j]*k)}$ and ${tex(b[i,j])}.$ "+sol[end:]
    eq_start=sol.index('\\begin{aligned}',sol.index('Equating these elements'));eq_end=sol.index('\\end{aligned}',eq_start)+len('\\end{aligned}')
    sol=sol[:eq_start]+r'\begin{aligned}'+tex(a[i,j]*k)+' & ='+tex(b[i,j])+r' \\ k & ='+tex(ratio)+r'.\end{aligned}'+sol[eq_end:]
    problem=normalize_prose(problem);sol=normalize_prose(sol)
    f=q[':question/answer-fields'][0];radio=f[':answer-field/type'][':db/ident'].endswith('/radio')
    values=([ratio-3,ratio,ratio-1,ratio-4,ratio-2] if sid=='q-981' else [ratio+5,0,ratio,ratio+4,ratio+1]) if radio else [ratio]
    assert len(set(values))==len(values)
    answers=[('k='+tex(v)) if radio else tex(v) for v in values];correct=('k='+tex(ratio)) if radio else tex(ratio)
    identity=json.dumps([sid,problem,sol,sorted(answers)],sort_keys=True)
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),f[':answer-field/key']))
    bank=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in answers]
    out={':question/id':qid,':question/problem':problem,':question/worked-solution':sol,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':bank,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in bank if a[':answer/value']==correct)]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']},'question':out,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':sid,'profile':sid if radio else None,'seed':seed,'parameters':parameters,'domain':'signed integer entries; source zero/sign pattern; nonzero target; nonzero integer or reciprocal scalar; integral result','sympy':sp.__version__,'mathematical_fingerprint':fingerprint(out),'source_basis':json.loads((HERE/'reference/source-basis.json').read_text())['basis']}}
def batch(difficulty,count,seed):
    result=[];seen=set()
    for n in range(max(100,count*20)):
        r=generate(difficulty,seed+n,list(CASES)[n%len(CASES)]);fp=fingerprint(r['question'])
        if fp not in seen:result.append(r);seen.add(fp)
        if len(result)==count:return result
    raise ValueError('Bounded sampler exhausted')
def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+json.dumps(q[':question/answer-fields'],indent=2)+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n'.join(map(markdown,rs)))
