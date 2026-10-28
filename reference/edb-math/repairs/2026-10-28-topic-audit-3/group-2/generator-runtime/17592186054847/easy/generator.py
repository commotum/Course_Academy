#!/usr/bin/env python3
"""Seeded implicit-curve line-intercept practice. No database or runtime repo access."""
import argparse
import copy
import hashlib
import json
import random
import uuid
from fractions import Fraction as Q
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record

ROOT = Path(__file__).resolve().parent
X, Y = sp.symbols('x y')
KP = {'db_id': 17592186054847, 'id': 'dfdb93d1-d550-5939-8a47-99bd1d863a8c',
      'title': 'Determining an Intercept of a Tangent or Normal Line to a Curve Given in Implicit Form'}
FAMILIES = {'easy': ['diagonal'], 'moderate': ['diagonal', 'translated', 'parabola', 'product'],
            'hard': ['diagonal', 'hyperbola', 'translated', 'parabola', 'product', 'mixed']}
PROFILES = {
 'slope': ['sign', 'reciprocal', 'double', 'half'],
 'normal-confusion': ['normal', 'reciprocal', 'double', 'no-translation'],
 'line-algebra': ['sign', 'half', 'no-translation', 'intercept-sign'],
}

def tex(v):
    return sp.latex(sp.Rational(v.numerator, v.denominator)) if isinstance(v, Q) else sp.latex(v)

def display(rows):
    if len(rows) == 1: return '$$\n' + rows[0] + '\n$$'
    return '$$\n\\begin{aligned}\n' + ' \\\\\n'.join(rows) + '\n\\end{aligned}\n$$'

def signed_point(p): return r'\left(' + ','.join(tex(v) for v in p) + r'\right)'

def parts(coeff):
    a,b,c,d,e = coeff
    return a*X**2+b*X*Y+c*Y**2+d*X+e*Y, 2*a*X+b*Y+d, b*X+2*c*Y+e

def intercept(u,v,m,axis):
    return (u-v/m,Q(0)) if axis == 'x' else (Q(0),v-m*u)

def finalize(record):
    q = record['question']
    for key in [':question/problem', ':question/worked-solution']: q[key] = normalize_prose(q[key])
    for f in q[':question/answer-fields']:
        for a in f[':answer-field/choices']: a[':answer/value'] = normalize_tex(a[':answer/value'])
    # Normalize first; identities depend only on public content and field ownership.
    identity = json.dumps([q[':question/problem'], q[':question/worked-solution'], q[':question/difficulty'],
                          [[f[':answer-field/key'], f[':answer-field/type'], [a[':answer/value'] for a in f[':answer-field/choices']]] for f in q[':question/answer-fields']]], sort_keys=True)
    qid = uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy/kp54847/v1/' + identity)
    q[':question/id'] = str(qid)
    for f in q[':question/answer-fields']:
        correct_index = f.pop('_correct_index')
        fid = uuid.uuid5(qid, f[':answer-field/key'])
        f[':answer-field/id'] = str(fid)
        for i,a in enumerate(f[':answer-field/choices']): a[':answer/id'] = str(uuid.uuid5(fid,str(i)+':'+a[':answer/value']))
        f[':answer-field/correct'] = [':answer/id',f[':answer-field/choices'][correct_index][':answer/id']]
    return validate_generated_record(record)

def field(key,kind,values,index=0):
    return {':answer-field/key':key, ':answer-field/type':':answer-field.type/'+kind,
            ':answer-field/choices':[{':answer/type':':answer.type/math', ':answer/value':v} for v in values], '_correct_index':index}

def build(level, coeff, point, axis, family, rng=None, profile='slope', name='P', line=None, correct_position=None, bank_guards=(), bank_actions=None):
    """Render one ordered rational derivation; explicit arguments support counterfactuals."""
    rng = rng or random.Random(0)
    u,v = map(Q,point)
    poly,fx,fy = parts(coeff)
    sub = {X:sp.Rational(u.numerator,u.denominator),Y:sp.Rational(v.numerator,v.denominator)}
    k = poly.subs(sub)
    gx,gy = Q(int(fx.subs(sub))),Q(int(fy.subs(sub)))
    if not gx or not gy: raise ValueError('Fresh practice requires finite nonzero tangent and normal slopes')
    tangent = -gx/gy
    line = line or ('normal' if level == 'hard' else 'tangent')
    m = -1/tangent if line == 'normal' else tangent
    p = intercept(u,v,m,axis)
    pt = signed_point((u,v))
    equation = tex(poly)+'='+tex(k)
    yp = r'\frac{dy}{dx}'
    differentiated = tex(fx) + r'+\left(' + tex(fy) + r'\right)' + yp + '=0'
    derivative = r'-\frac{' + tex(fx) + '}{' + tex(fy) + '}'
    problem = f'The curve has equation ${equation}$. The **{line}** line at ${pt}$ meets the ${axis}$-axis at ${name}$. Find the coordinates of ${name}$.'
    if level == 'easy':
        problem += r'\n\nUse $y-y_0=m(x-x_0)$ with the given point. On the $' + axis + r'$-axis, $' + ('y' if axis=='x' else 'x') + '=0$.'
        problem = problem.replace(r'\n','\n')
    if level != 'easy': problem += '\n\nGive exact values.\n\n$'+name+'=(${{field-1}}$,$ {{field-2}}$)$.'
    intro = 'Treat $y$ as a function of $x$.'
    if coeff[1]: intro += r' The product rule gives $\frac{d}{dx}(xy)=y+x\frac{dy}{dx}$.'
    intro += ' Differentiate implicitly and collect the derivative terms:'
    solution = intro + '\n\n' + display([differentiated.replace('=','&=',1),
        r'\left(' + tex(fy) + r'\right)' + yp + '&=-\\left(' + tex(fx) + r'\right)',
        yp + '&=' + derivative])
    solution += '\n\nEvaluate the tangent slope at the given point:\n\n' + display([r'm_{\mathrm{t}}=-\frac{' + tex(gx) + '}{' + tex(gy) + '}=' + tex(tangent)])
    if line == 'normal':
        solution += '\n\nThe normal slope is the negative reciprocal:\n\n' + display([r'm=-\frac{1}{m_{\mathrm{t}}}=-\frac{1}{'+tex(tangent)+'}='+tex(m)])
    else: solution += '\n\nThe tangent line uses $m='+tex(m)+'$.'
    solution += '\n\nUse the given point and this slope:\n\n' + display([
        'y-\\left('+tex(v)+r'\right)&='+tex(m)+r'\left(x-\left('+tex(u)+r'\right)\right)',
        'y&='+tex(m)+r'\left(x-\left('+tex(u)+r'\right)\right)+\left('+tex(v)+r'\right)'])
    if axis == 'y':
        rows = ['y&='+tex(m)+r'\left(0-\left('+tex(u)+r'\right)\right)+\left('+tex(v)+r'\right)', 'y&='+tex(p[1])]
        coord='x'
    else:
        rows = ['0&='+tex(m)+r'\left(x-\left('+tex(u)+r'\right)\right)+\left('+tex(v)+r'\right)',
                r'x-\left('+tex(u)+r'\right)&=-\frac{'+tex(v)+'}{'+tex(m)+'}', 'x&='+tex(p[0])]
        coord='y'
    solution += f'\n\nAt the ${axis}$-axis, ${coord}=0$. Substitute and simplify:\n\n' + display(rows)
    solution += '\n\nTherefore $'+name+'='+signed_point(p)+'$.'
    recipes=[]
    if level=='easy':
        errors={
          'sign': lambda:intercept(u,v,-m,axis),
          'normal': lambda:intercept(u,v,-1/m,axis),
          'reciprocal': lambda:intercept(u,v,1/m,axis),
          'double': lambda:intercept(u,v,2*m,axis),
          'half': lambda:intercept(u,v,m/2,axis),
          'no-translation': lambda:(-v/m,Q(0)) if axis=='x' else (Q(0),v),
          'intercept-sign': lambda:tuple(-z for z in p),
        }
        recipes=PROFILES[profile]
        candidates=[p]+[errors[r]() for r in recipes]
        if len(set(candidates))!=5: raise ValueError('Degenerate complete error profile')
        values=[z[0 if axis=='x' else 1] for z in candidates]
        value=values[0]
        actions={'rank:'+str(sorted(values).index(value))}
        # Only bank-visible numerical/format cues; no changes to mathematical answers.
        for cue,scores in [('min-abs',[abs(z) for z in values]),
                           ('max-abs',[-abs(z) for z in values]),
                           ('min-den',[z.denominator for z in values]),
                           ('max-den',[-z.denominator for z in values])]:
            winners=[i for i,z in enumerate(scores) if z==min(scores)]
            if winners==[0]:actions.add(cue)
        paired=[i for i,z in enumerate(values) if z!=0 and -z in values]
        if len(paired)==2 and 0 in paired:actions.add('opposite-positive' if value>0 else 'opposite-negative')
        if sum(z>0 for z in values)==1 and value>0:actions.add('unique-positive')
        if sum(z<0 for z in values)==1 and value<0:actions.add('unique-negative')
        if any(guard.get('common',set()) & actions for guard in bank_guards):
            raise ValueError('Bank cue would answer the entire visible subgroup')
        if bank_actions is not None:bank_actions.update(actions)
        indexed=list(enumerate(candidates));rng.shuffle(indexed)
        if correct_position is not None:
            current=next(i for i,(j,_) in enumerate(indexed) if j==0)
            indexed[current],indexed[correct_position]=indexed[correct_position],indexed[current]
        fields=[field('selection','radio',[signed_point(p1) for _,p1 in indexed],next(i for i,(j,_) in enumerate(indexed) if j==0))]
    else: fields=[field('field-1','blank',[tex(p[0])]),field('field-2','blank',[tex(p[1])])]
    return finalize({'knowledge_point':copy.deepcopy(KP), 'question':{':question/problem':problem,
        ':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level, ':question/answer-fields':fields},
        'generation':{'version':1,'family':family,'axis':axis,'line':line,'coefficients':list(coeff),'point':[int(u),int(v)],
        'constant':str(k),'profile':profile if level=='easy' else 'coordinate-blanks','error_recipes':recipes,
        'support':['4f8a0764-c99e-5be6-8b49-3ca28725caf9','cd630daa-4813-5ca8-b3d4-5fe35c4af4fa']}})

def sample_coeff(rng,family):
    a,c=rng.randint(1,4),rng.randint(1,4)
    if family=='diagonal': return a,0,c,0,0
    if family=='hyperbola': return a,0,-c,0,0
    if family=='translated': return a,0,c,rng.choice([-6,-4,-2,2,4,6]),rng.choice([-4,-2,0,2,4])
    if family=='parabola': return a,0,0,rng.choice([-4,-2,0,2,4]),rng.choice([-4,-2,2,4])
    if family=='product': return 0,1,0,rng.choice([-2,-1,0,1,2]),rng.choice([-2,-1,0,1,2])
    return rng.choice([0,1,2]),rng.choice([-2,-1,1,2]),rng.choice([-2,-1,0,1,2]),0,0

def generate(level,count,seed):
    rng=random.Random(seed);out=[];seen=set();families=[];offset=rng.randrange(2)
    # Independent shuffled decks avoid a constant answer action within an axis subgroup.
    positions={'x':[], 'y':[]}
    bank_history={}
    for index in range(count):
        if not families: families=list(FAMILIES[level]);rng.shuffle(families)
        family=families.pop();axis=['x','y'][(index+offset)%2]
        profile=rng.choice(list(PROFILES))
        correct_position=None
        if level=='easy':
            if not positions[axis]:
                positions[axis]=list(range(5));rng.shuffle(positions[axis])
            correct_position=positions[axis].pop()
        for attempt in range(1000):
            coeff=sample_coeff(rng,family)
            nonzero=[-4,-3,-2,-1,1,2,3,4]
            # A point on the other axis is valid (e-192 and q-14614).
            # Only a point already on the requested axis makes the intercept immediate.
            point=[rng.choice(nonzero+[0] if level!='easy' and axis=='x' else nonzero),
                   rng.choice(nonzero+[0] if level!='easy' and axis=='y' else nonzero)]
            if level=='easy':profile=rng.choice(list(PROFILES))
            groups=[axis,('circle' if coeff[0]==coeff[2] else 'ellipse')+'-'+axis] if level=='easy' else []
            guards=[bank_history.setdefault(group,{}) for group in groups]
            bank_actions=set()
            try:r=build(level,coeff,point,axis,family,rng,profile,correct_position=correct_position,bank_guards=guards,bank_actions=bank_actions)
            except (ValueError,ZeroDivisionError):continue
            poly,fx,fy=parts(coeff);sub={X:point[0],Y:point[1]};mt=Q(-int(fx.subs(sub)),int(fy.subs(sub)))
            m=-1/mt if level=='hard' else mt
            p=intercept(*map(Q,point),m,axis)
            if max(abs(m.numerator),m.denominator)>12 or any(abs(t)>30 or t.denominator>12 for t in p): continue
            key=json.dumps([str(poly),point,axis,r['generation']['line']])
            if key in seen:continue
            for guard in guards:
                guard['common']=guard.get('common',bank_actions) & bank_actions
            seen.add(key);r['generation'].update({'seed':seed,'index':index,'attempts':attempt+1});out.append(r);break
        else: raise RuntimeError('Could not construct the selected mathematical role/profile')
    return out

def replay():
    out=[]
    for source in json.loads((ROOT/'source-replay.json').read_text()):
        q=copy.deepcopy(source)
        sid=q.pop(':question/id');q.pop(':question/math-academy-id',None)
        q[':question/difficulty']=q[':question/difficulty'][':db/ident']
        for f in q[':question/answer-fields']:
            f[':answer-field/type']=f[':answer-field/type'][':db/ident']
            correct=f[':answer-field/correct'][':answer/id']
            f['_correct_index']=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==correct)
            f.pop(':answer-field/correct')
            for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
        out.append(finalize({'knowledge_point':copy.deepcopy(KP),'question':q,'generation':{'source_question_id':sid,'mode':'source-replay'}}))
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay-source',action='store_true')
    args=ap.parse_args()
    if args.count<0:ap.error('--count must be nonnegative')
    records=replay() if args.replay_source else generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
