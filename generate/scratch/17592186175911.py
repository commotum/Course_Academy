#!/usr/bin/env python3
"""Bounded two-point parallel-line generator; no database writes.

Sources at basis 1946 are unrated and have no keys/solutions. Local difficulty
and derived answers are authored. One RHS blank, no choice profiles or plots.
Canonical solution sequence: two-point slope, equal slopes, point-slope, expand.
Novelty is the resulting whole line (exact slope/intercept), never seed/order.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, os, random, re, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ImportError:
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__=='__main__': os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
    raise

KP_ID=17592186175911
KP_UUID='fded3d63-be68-5e3e-b633-58d282d16ef2'
TITLE='Finding the Equation of a Line Passing Through Two Points'
VERSION='parallel-two-points-rhs-1'
HERE=Path(__file__).resolve().with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SOURCE_PARAMETERS={'q-214094':dict(u=1,v=3,a=2,b=-1,c=4,d=3),
                   'q-216200':dict(u=0,v=2,a=2,b=1,c=3,d=-1)}
x=sp.Symbol('x',real=True)

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def tex(v): return sp.latex(sp.expand(v)).replace('- ','-')
def fingerprint(q):
    pairs=[tuple(map(int,p)) for p in re.findall(r'\((-?\d+),\s*(-?\d+)\)',q[':question/problem'])]
    if len(pairs)!=3: raise ValueError('Unrecognized existing prompt; review required')
    (u,v),(a,b),(c,d)=pairs
    if c==a: raise ValueError('Vertical reference not supported')
    m=sp.Rational(d-b,c-a)
    return digest([str(m),str(v-m*u)])

def allowed(level,p):
    if set(p)!=set('uvabcd') or any(type(v) is not int or abs(v)>12 for v in p.values()): return False
    if p['c']<=p['a']: return False
    m=sp.Rational(p['d']-p['b'],p['c']-p['a'])
    if not m or abs(m)>3 or m.q>3: return False
    return (p['u']==0 and m.q==1) if level=='easy' else (p['u']!=0) if level=='moderate' else False

def candidates(level):
    slopes=(-3,-2,-1,1,2,3) if level=='easy' else ('-2','-1','1','2','-1/2','1/2','-1/3','1/3','-2/3','2/3') if level=='moderate' else None
    if slopes is None: raise ValueError('Unsupported hard: no within-scope validated template')
    seen=set()
    for m,u,v in itertools.product(slopes,(0,) if level=='easy' else (-3,-2,-1,1,2,3),(-4,-3,-2,-1,1,2,3,4)):
        m=sp.Rational(m); a,b=2,1 if level=='easy' else -1
        dx=1 if level=='easy' else (m.q if m.q>1 else 2)
        p=dict(u=u,v=v,a=a,b=b,c=a+dx,d=int(b+m*dx))
        fp=digest([str(m),str(v-m*u)])
        if fp not in seen and allowed(level,p): seen.add(fp);yield p

def generate(level,seed=0,template=None,parameters=None,replay=False):
    if template not in (None,'parallel-two-points-rhs'): raise ValueError('Unknown template')
    p=dict(parameters or random.Random(seed).choice(list(candidates(level))))
    if not allowed(level,p): raise ValueError('Outside bounded workload/domain')
    u,v,a,b,c,d=[p[k] for k in 'uvabcd']; m=sp.Rational(d-b,c-a); intercept=v-m*u
    sid='q-216200' if level=='easy' else 'q-214094'
    if replay:
        if p!=SOURCE_PARAMETERS[sid]: raise ValueError('Replay requires source parameters')
        old={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
        prompt=old[sid][':question/problem']
    else:
        prompt=f'Find the equation of the line that passes through the point $({u}, {v})$ and is parallel to the line passing through the points $({a}, {b})$ and $({c}, {d})$.$y =$\n{{{{field-1}}}}'
    fp=fingerprint({':question/problem':prompt});qid=str(uuid.uuid5(uuid.UUID(KP_UUID),VERSION+':'+fp))
    fid=str(uuid.uuid5(uuid.UUID(qid),'field-1'));value=tex(m*x+intercept);aid=str(uuid.uuid5(uuid.UUID(fid),'value:'+value))
    sol=(f"Since parallel lines have equal slopes, both lines should have the same slope.\n\nFirst, let's find the slope of the line passing through the points $({a},{b})$ and $({c},{d})$:\n\n$$\n"
         f'\\begin{{aligned}}\nm &= \\frac{{y_{{2}} - y_{{1}}}}{{x_{{2}} - x_{{1}}}} \\\\\n&= \\frac{{{d} - ({b})}}{{{c} - ({a})}} \\\\\n&= {tex(m)}\n\\end{{aligned}}\n$$\n\n'
         f'Therefore, we wish to find a line that has a slope of\n\n$$\n{tex(m)}\n$$\n\nand passes through the point $({u},{v})$. To find the equation of this line, we use the point-slope form:\n\n$$\n'
         f'\\begin{{aligned}}\ny - y_{{1}} &= m(x - x_{{1}}) \\\\\ny - ({v}) &= {tex(m)}(x - ({u})) \\\\\ny - ({v}) &= {tex(m*(x-u))} \\\\\ny &= {value}\n\\end{{aligned}}\n$$')
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
      'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,
      ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'field-1',':answer-field/type':':answer-field.type/blank',':answer-field/correct':[':answer/id',aid],':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value}]}]},
      'generation':{'version':VERSION,'seed':seed,'template':'parallel-two-points-rhs','parameters':p,'replay':replay,'source_question':sid,'source_basis':1946,'source_lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','bank_profile':None,'mathematical_fingerprint':fp,'domain':'real x,y; bounded integer coordinates; nonzero slope; distinct x coordinates','difficulty_origin':'authored: easy integer slope and target on y-axis; moderate nonzero target x with integer or fractional slope','answer_origin':'derived; source keys absent','solution_origin':'authored canonical-example move sequence','dependencies':{'sympy':sp.__version__}}}

def batch(level,count,seed):
    pool=list(candidates(level));random.Random(seed).shuffle(pool)
    if type(count) is not int or not 1<=count<=len(pool): raise ValueError(f'Finite capacity {len(pool)}; requested {count}')
    return [generate(level,seed,parameters=p) for p in pool[:count]]
def markdown(r): return r['question'][':question/problem']+'\n\nAnswer: $'+r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+'$\n\n'+r['question'][':question/worked-solution']
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=('json','markdown'),default='json');args=a.parse_args();r=batch(args.difficulty,args.count,args.seed);print(json.dumps(r,indent=2) if args.format=='json' else '\n\n'.join(map(markdown,r)))
