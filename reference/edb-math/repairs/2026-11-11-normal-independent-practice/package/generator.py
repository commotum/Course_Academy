"""Seeded normal-line practice. All runtime resources are local to this file."""
import argparse
import copy
import itertools
import json
import random
import uuid
from functools import lru_cache
from pathlib import Path
import sympy as s
import math_format as F

VERSION = '3.0.2'
KP = {'db_id':17592186092240,'id':'55a323ba-f2a7-5a49-abd4-a9812518ef8c',
      'title':'Determining the Equation of a Normal Line to a Curve at a Point'}
NS = uuid.UUID(KP['id'])
x, y = s.symbols('x y', real=True)
ROOT = Path(__file__).resolve().parent
LEVELS = ('easy','moderate','hard')

def tex(v):
    return s.latex(s.expand(v))

def aligned(rows):
    return '$$\n\\begin{aligned}\n' + '\\\\\n'.join(rows) + '\n\\end{aligned}\n$$'

def display(v):
    return '$$\n' + v + '\n$$'

def own_record(level, prompt, solution, specs, provenance):
    prompt, solution = F.normalize_prose(prompt), F.normalize_prose(solution)
    specs = [(key,kind,[F.normalize_tex(v) for v in vals],F.normalize_tex(correct))
             for key,kind,vals,correct in specs]
    payload = json.dumps([VERSION,level,prompt,solution,specs],sort_keys=True)
    qid = str(uuid.uuid5(NS,payload))
    fields = []
    for key,kind,values,correct in specs:
        fid = str(uuid.uuid5(uuid.UUID(qid),key))
        choices = [{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),
                    ':answer/type':':answer.type/math',':answer/value':value} for value in values]
        assert len(set(values)) == len(values) and correct in values
        fields.append({':answer-field/id':fid,':answer-field/key':key,
                       ':answer-field/type':':answer-field.type/'+kind,
                       ':answer-field/choices':choices,
                       ':answer-field/correct':[':answer/id',str(uuid.uuid5(uuid.UUID(fid),correct))]})
    return F.validate_generated_record({'knowledge_point':KP.copy(),'question':{
        ':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,
        ':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},
        'generation':{'version':VERSION,**provenance}})

def instance(family,a,b,c,point):
    a,b,c,point = map(s.Rational,(a,b,c,point))
    if family=='quadratic': expr=a*x**2+b*x+c
    elif family=='cubic': expr=a*x**3+b*x+c
    elif family=='sextic': expr=a*x**6/8-b*x**3/4+c
    elif family=='root-reciprocal': expr=a/s.sqrt(x)+b/x+c
    elif family=='reciprocal-powers': expr=a/x+b/x**2+c
    elif family=='cube-linear': expr=a*x**s.Rational(1,3)+b*x+c
    else: raise ValueError('Unknown family')
    derivative=s.diff(expr,x); ordinate=s.simplify(expr.subs(x,point)); tangent=s.simplify(derivative.subs(x,point))
    if tangent==0: raise ValueError('Zero tangent slope')
    normal=-1/tangent; intercept=s.simplify(ordinate-normal*point)
    return dict(family=family,expr=expr,derivative=derivative,point=point,ordinate=ordinate,
                tangent=tangent,normal=normal,intercept=intercept,
                parameters=dict(a=str(a),b=str(b),c=str(c),point=str(point)))

def build(level, data):
    if level not in LEVELS: raise ValueError('Unknown difficulty')
    e,d,p,h,m,n,b=(data[k] for k in ('expr','derivative','point','ordinate','tangent','normal','intercept'))
    prompt=rf'Find the equation of the normal line to the curve $y={tex(e)}$ at $\left({tex(p)},{tex(h)}\right)$.'
    if level=='moderate':
        prompt+='\n\nGive exact values of $a$ and $b$ in $x+ay=b$.\n\n$a=$ {{coefficient}}\n\n$b=$ {{constant}}'
        specs=[('coefficient','blank',[tex(m)],tex(m)),('constant','blank',[tex(p+m*h)],tex(p+m*h))]
    else:
        prompt+='\n\nGive exact values of $a$ and $b$ in $y=ax+b$.\n\n$a=$ {{slope}}\n\n$b=$ {{intercept}}'
        specs=[('slope','blank',[tex(n)],tex(n)),('intercept','blank',[tex(b)],tex(b))]
    solution=rf'Let $f(x)={tex(e)}$.'
    # Explicit power rewrite is a learner stage, not a CAS-normal-form side effect.
    if data['family'] in ('root-reciprocal','reciprocal-powers','cube-linear'):
        a0,b0,c0=map(s.Rational,(data['parameters'][k] for k in ('a','b','c')))
        powers={'root-reciprocal':(s.Rational(-1,2),-1),'reciprocal-powers':(-1,-2),
                'cube-linear':(s.Rational(1,3),1)}[data['family']]
        terms=[tex(a0)+rf'x^{{{tex(powers[0])}}}',tex(b0)+rf'x^{{{tex(powers[1])}}}',tex(c0)]
        solution+=' Rewrite with powers, then differentiate term by term:\n\n'+aligned([
            'f(x)&='+ '+'.join('('+t+')' for t in terms),
            "f'(x)&="+tex(d)])
    else:
        solution+=' Differentiate:\n\n'+display("f'(x)="+tex(d))
    substituted=tex(d).replace('x', r'\left('+tex(p)+r'\right)')
    solution+='\n\nEvaluate the tangent slope at the supplied abscissa:\n\n'+display(rf"m_t=f'\left({tex(p)}\right)={substituted}={tex(m)}")
    solution+='\n\nThe normal is perpendicular to the tangent, so\n\n'+display(rf'm_n=-\frac{{1}}{{m_t}}=-\frac{{1}}{{\left({tex(m)}\right)}}={tex(n)}.')
    rows=[rf'y-\left({tex(h)}\right)&={tex(n)}\left(x-\left({tex(p)}\right)\right)',
          rf'y&={tex(n*x)}+\left({tex(-n*p)}\right)+\left({tex(h)}\right)',
          'y&='+tex(n*x+b)]
    if level=='moderate':
        # Multiplication is written explicitly even for fractional tangent slopes.
        rows += [rf'\left({tex(m)}\right)y&=-x+\left({tex(p)}\right)+\left({tex(m*h)}\right)',
                 rf'x+\left({tex(m)}\right)y&={tex(p+m*h)}']
    solution+='\n\nUse the point in point-slope form and rearrange:\n\n'+aligned(rows)
    if level=='moderate': solution+=rf'\n\nThe coefficient is ${tex(m)}$ and the constant is ${tex(p+m*h)}$.'
    else: solution+=rf'\n\nThus $a={tex(n)}$ and $b={tex(b)}$.'
    solution=solution.replace('\\n\\n','\n\n')
    refs={'quadratic':['q-340942','q-342162'],'cubic':['q-342163','e-6080'],
          'sextic':['q-342168'],'root-reciprocal':['q-103546','3d7c9c49-19d3-52b0-87ac-8a31e56af5e6'],
          'reciprocal-powers':['q-340945','q-47398'],'cube-linear':['q-342190','q-342187']}[data['family']]
    return own_record(level,prompt,solution,specs,{'template':data['family'],'profile':'two-exact-coefficients',
        'parameters':data['parameters'],'source_references':refs,'domain':'x>0' if data['family'] in ('root-reciprocal','cube-linear') else 'x!=0' if data['family']=='reciprocal-powers' else 'real x',
        'displayed_final':tex(n*x+b) if level!='moderate' else [tex(m),tex(p+m*h)],
        'stages':['power rewrite']*(data['family'] in ('root-reciprocal','reciprocal-powers','cube-linear'))+['derivative','evaluation','negative reciprocal','point-slope','rearrangement']})

@lru_cache(None)
def catalog(level):
    if level=='easy': families=['quadratic']
    elif level=='moderate': families=['quadratic','cubic','sextic']
    elif level=='hard': families=['root-reciprocal','reciprocal-powers','cube-linear']
    else: raise ValueError('Unknown difficulty')
    cells={}
    for family in families:
        points=[-1,0,1,2] if family=='quadratic' else [-1,1,2] if family=='cubic' else [2] if family=='sextic' else [1,8] if family=='cube-linear' else [1,2] if family=='reciprocal-powers' else [1,4]
        av=[-1,1] if family=='sextic' else [-2,-1,1,2]; bv=[-8,-7,-4,4,7,8] if family=='sextic' else [-2,-1,0,1,2] if family=='quadratic' else [-2,-1,1,2]
        for a,b,c,p in itertools.product(av,bv,range(-2,3),points):
            try: z=instance(family,a,b,c,p)
            except ValueError: continue
            if any(abs(z[k].p)>160 or z[k].q>48 for k in ['ordinate','tangent','normal','intercept']): continue
            if family=='sextic' and abs(z['tangent'])>12: continue
            cell=(family,1 if z['tangent']>0 else -1)
            cells.setdefault(cell,[]).append((family,a,b,c,p))
    return cells

def generate_batch(level,count,seed):
    if count<1: raise ValueError('Positive count required')
    rng=random.Random(seed); cells={k:list(v) for k,v in catalog(level).items()}
    if count>sum(map(len,cells.values())): raise ValueError('Finite semantic capacity exceeded')
    for candidates in cells.values(): rng.shuffle(candidates)
    keys=list(cells);rng.shuffle(keys);out=[]
    while len(out)<count:
        for key in keys:
            if not cells[key]: continue
            data=instance(*cells[key].pop())
            out.append(build(level,data))
            if len(out)==count: break
    return out

def replay(source_id):
    questions=json.loads((ROOT/'source_replay.json').read_text())
    q=next((q for q in questions if q.get(':question/math-academy-id',q[':question/id'])==source_id),None)
    if q is None: raise ValueError('Unknown complete eligible source')
    specs=[]
    for f in q[':question/answer-fields']:
        kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
        clean=lambda v:v.replace('\\\\frac','\\frac')
        specs.append((f[':answer-field/key'],kind,[clean(a[':answer/value']) for a in f[':answer-field/choices']],clean(f[':answer-field/correct'][':answer/value'])))
    solution=q[':question/worked-solution']
    if source_id=='q-47398': solution=solution.replace("=-\\frac{4}{{x}^{2}}=-4", "=-\\frac{4}{{1}^{2}}=-4")
    return own_record('moderate',q[':question/problem'],solution,specs,{'template':'source-replay','profile':source_id,'source_references':[q[':question/id']], 'parameters':{'original':True}})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=LEVELS,required=True)
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--source-id')
    a=ap.parse_args()
    if a.source_id:
        if a.count!=1 or a.difficulty!='moderate': ap.error('Source replay uses count=1 and original moderate difficulty')
        records=[replay(a.source_id)]
    else: records=generate_batch(a.difficulty,a.count,a.seed)
    print(json.dumps(records,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
