"""Easy parametric arc-length integral identification, version 1.

Conservative slot: integration endpoints only. Curves, derivative stages and
complete source-specific banks stay fixed. Nonplot profiles have bounded,
real-valued variants; illustrated profiles support source replay only. Seeds,
choice order and rigid translations do not establish novelty.
"""
import argparse, functools, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex

KP_ID=17592186092375
KP_UUID='4b03546f-6c79-53b9-b284-fb23ae4dba52'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'parametric-arc-integral-generator-v1'))
SUPPORTED_LEVELS=('easy',)
VERSION='1.0.0'
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source_cases.json').read_text())
CASES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/difficulty' in q and ':question/worked-solution' in q}
t=s.Symbol('t',real=True)
# Observed curves and intervals, retained exactly; no coefficient generalization.
CURVES={
'q-123005':(t**3-8,t**4+5*t,-2,3),
'q-123019':(3*t**2,5*t,0,1),
'q-123025':(3*t**3+5,t**2-5*t,-1,2),
'q-81377':(t-1,t**2+2,-1,2),
'q-81380':(t**3+1,3*t,-2,0),
'q-85724':(t**3-1,t**2-t,0,1),
'q-123020':(t**3-4,2*t,-2,0),
'q-15174':(t**3+t**2,t**3-t**2,0,1)}
PLOTTED={'q-123019','q-81380','q-123020'}

@functools.lru_cache(maxsize=None)
def recipe(value):
    """Read complete source integral, retaining outside multipliers and t factors."""
    z=value.replace('\\\\','\\')
    start=z.index(r'\sqrt{')+6
    depth=1;end=start
    while depth:
        if z[end]=='{':depth+=1
        elif z[end]=='}':depth-=1
        end+=1
    rad=z[start:end-1]
    rad=rad.replace('{t}','t').replace('{','(').replace('}',')')
    rad=re.sub(r'(\d|\))(?=t)',r'\1*',rad)
    rad=re.sub(r't(?=\()',r't*',rad)
    # Powers have become ^(n), and implicit products are simple polynomials.
    p=s.sympify(rad.replace('^','**'),locals={'t':t})
    factor=int(z[0]) if z[0].isdigit() else 1
    outside_t=bool(re.search(r'\}_\{[^}]+\}\^\{[^}]+\}t\\sqrt',z))
    # The imported notation has bounds as }_{a}^{b}t\\sqrt.
    outside_t=outside_t or bool(re.search(r'\^\{[^}]+\}t\\sqrt',z))
    return s.expand(p),s.Integer(factor)*(t if outside_t else 1)

def square(value):
    p,c=recipe(value);return s.expand(c*c*p)

def positive_on(p,a,b,strict=False):
    p=s.Poly(p,t)
    if p.is_zero:return not strict
    # Exact real-root isolation plus midpoint sign proves a fixed sign throughout.
    if p.count_roots(a,b):return False
    return p.eval(s.Rational(a+b,2))>0 and p.eval(a)>=0 and p.eval(b)>=0

def admissible(sid,a,b):
    q=CASES[sid];values=[square(x[':answer/value']) for x in q[':question/answer-fields'][0][':answer-field/choices']]
    if a>=b or sid=='q-15174' and a<0:return False
    if not all(positive_on(p,a,b) for p in values):return False
    for i,p in enumerate(values):
        for r in values[:i]:
            if not (positive_on(p-r,a,b,True) or positive_on(r-p,a,b,True)):return False
    return True

@functools.lru_cache(maxsize=None)
def domain(sid):
    if sid in PLOTTED:return []
    pairs=[(a,b) for a in range(2,9) for b in range(a+1,a+5)]
    if sid=='q-85724':pairs=[(a,b) for a in range(-8,-2) for b in range(a+1,min(a+5,0))]
    return [[sid,a,b] for a,b in pairs if admissible(sid,a,b)]

def change_bounds(text,old_a,old_b,a,b):
    # Only explicit integration bounds and the final prompt interval are slots.
    z=text.replace('_{'+str(old_a)+'}^{'+str(old_b)+'}','_{'+str(a)+'}^{'+str(b)+'}')
    z=z.replace('from $t='+str(old_a)+'$ to $t='+str(old_b)+'$', 'from $t='+str(a)+'$ to $t='+str(b)+'$')
    return z

def fingerprint(q):
    text=q[':question/problem']
    return hashlib.sha256(text.encode()).hexdigest()

def generate(difficulty='easy',seed=0,template=None,parameters=None):
    if difficulty!='easy':raise ValueError('Unsupported difficulty: '+difficulty)
    if parameters is None:
        rng=random.Random(seed);sid=template or rng.choice(sorted(set(CASES)-PLOTTED));parameters=rng.choice(domain(sid))
    sid,a,b=parameters;source=CASES[sid];x,y,oa,ob=CURVES[sid]
    replay=(a,b)==(oa,ob)
    if not replay and (sid in PLOTTED or not admissible(sid,a,b)):raise ValueError('Outside validated endpoint domain')
    if not replay and parameters not in domain(sid):raise ValueError('Outside bounded sampling policy')
    transform=lambda z:z if replay else change_bounds(z,oa,ob,a,b)
    problem=normalize_prose(transform(source[':question/problem']));solution=normalize_prose(transform(source[':question/worked-solution']))
    f=source[':question/answer-fields'][0];vals=[normalize_tex(transform(v[':answer/value'])) for v in f[':answer-field/choices']];correct=normalize_tex(transform(f[':answer-field/correct'][':answer/value']))
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),json.dumps([sid,a,b,vals])))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(v[':answer/id'] for v in answers if v[':answer/value']==correct)]}
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/easy',':question/answer-fields':[field]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'template':sid,'bank_profile':sid,'parameters':parameters,'source_question_id':source[':question/id'],'source_basis':SOURCE['basis'],'dependencies':{'sympy':s.__version__},'mathematical_fingerprint':fingerprint(q),'replay_only':replay}}

def batch(difficulty,count,seed=0):
    if difficulty!='easy':raise ValueError('Unsupported difficulty: '+difficulty)
    if count<0:raise ValueError('Negative count')
    params=[p for sid in CASES for p in domain(sid)];random.Random(seed).shuffle(params)
    if count>len(params):raise ValueError('Finite variant limit: '+str(len(params)))
    return [generate(difficulty,seed,parameters=p) for p in params[:count]]

def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n'.join(map(markdown,rs)))
