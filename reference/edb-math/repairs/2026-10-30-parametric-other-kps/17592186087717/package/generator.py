#!/usr/bin/env python3
"""Seeded exact parametric-table practice, with complete original-case replay.

Runtime is relocatable and read-only. No diagrams are generated for this KP.
The row/column roles are sampled before compatible function parameters.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import random
import re
import uuid
import sympy as sp
from algebra import scalar, T
from math_format import normalize_prose, normalize_tex, validate_generated_record

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT/'source_data.json').read_text())
KP = {'db_id':17592186087717, 'id':'bbf50e27-a8c3-52e7-be21-5d7ed61e5512',
      'title':'Filling a Table of Values for a Parametric Curve'}
NS = uuid.UUID(KP['id'])
VERSION = 'parametric-table-3'
BANDS = ('easy','moderate','hard')

def tex(v):
    return normalize_tex(sp.latex(sp.simplify(v)))

def uid(value):
    return str(uuid.uuid5(NS,value))

def clean(text):
    text=re.sub(r'\$\$(.*?)\$\$', lambda m: m[0] if m[1].strip() else '', text, flags=re.S)
    # Captured functions sometimes lost their backslash, or retain U+2061.
    text=text.replace('\u2061','')
    text=re.sub(r'(?<![A-Za-z\\])(sin|cos|tan)(?=\s|\\)',r'\\\1',text)
    return normalize_prose(text)

def record(level, problem, solution, fields, metadata):
    problem,solution=clean(problem),clean(solution)
    normalized=[(key,kind,[normalize_tex(v) for v in bank],normalize_tex(correct))
                for key,kind,bank,correct in fields]
    identity=json.dumps([VERSION,level,problem,solution,normalized],sort_keys=True)
    digest=hashlib.sha256(identity.encode()).hexdigest()
    fs=[]
    for key,kind,bank,correct in normalized:
        fid=uid(digest+':field:'+key)
        choices=[{':answer/id':uid(fid+':'+str(i)+':'+v), ':answer/type':':answer.type/math',
                  ':answer/value':v} for i,v in enumerate(bank)]
        indices=[i for i,v in enumerate(bank) if v==correct]
        if len(indices)!=1: raise ValueError('Answer must occur exactly once')
        fs.append({':answer-field/id':fid,':answer-field/key':key,
                   ':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,
                   ':answer-field/correct':[':answer/id',choices[indices[0]][':answer/id']]})
    return validate_generated_record({'knowledge_point':KP.copy(), 'question':{
        ':question/id':uid(digest), ':question/difficulty':':question.difficulty/'+level,
        ':question/problem':problem, ':question/worked-solution':solution,
        ':question/answer-fields':fs}, 'generation':{'version':VERSION,**metadata}})

REPAIRS={
 'q-326242':[('x(2)=','x(3)=')],
 'q-326250':[('y(0)=','y(5)=')],
 'q-326255':[('y(1)=','y(4)=')],
 'q-6832':[(r'into $y=\operatorname{sin}',r'into $x=\operatorname{sin}')],
 'q-6825':[('a=3(3)','c=3(3)')],
}

def enum(v): return v.get(':db/ident') if isinstance(v,dict) else v

def replay(source_id):
    """Replay an eligible complete source/exemplar, retaining its entire bank."""
    qs=DATA['questions']+DATA['exemplars']
    q=next((q for q in qs if source_id in (q.get(':question/math-academy-id'),q[':question/id'])),None)
    if q is None: raise ValueError('Not a complete replay case: '+source_id)
    solution=q[':question/worked-solution']
    for a,b in REPAIRS.get(source_id,[]):solution=solution.replace(a,b)
    fields=[]
    for f in q[':question/answer-fields']:
        fields.append((f[':answer-field/key'],enum(f[':answer-field/type']).split('/')[-1],
                       [a[':answer/value'] for a in f[':answer-field/choices']],
                       f[':answer-field/correct'][':answer/value']))
    level=enum(q[':question/difficulty']).split('/')[-1]
    return record(level,q[':question/problem'],solution,fields,
        {'template':'source-replay','source_question_ids':[q[':question/id']],
         'source_math_academy_id':q.get(':question/math-academy-id'),
         'source_basis':DATA['provenance'],'source_repairs':REPAIRS.get(source_id,[])})


def poly(coefficients):
    return sp.Add(*(sp.Rational(c)*T**i for i,c in enumerate(coefficients)))

def function(profile,rng,axis):
    """Compatible small coordinates; no common output-scaling-only sampler."""
    nz=lambda:rng.choice([-3,-2,-1,1,2,3])
    if profile=='guided':
        return poly([rng.randint(-3,3),nz()]) if axis=='linear' else poly([rng.randint(-2,2),0,rng.choice([-1,1])])
    if profile=='polynomial':
        return poly([rng.randint(-2,2),rng.choice([-2,-1,1,2]),0,rng.choice([-1,1])]) if axis=='special' else poly([rng.randint(-2,2),nz()])
    if profile=='quotient':
        return (T+rng.choice([-2,-1,1,2]))/(T+rng.choice([4,5])) if axis=='special' else poly([rng.randint(-2,2),rng.choice([-1,1]),1])
    if profile=='root':
        return rng.choice([-1,1])*sp.sqrt(T+rng.choice([3,4,5])) if axis=='special' else poly([rng.randint(-2,2),rng.choice([-1,1]),1])
    raise ValueError(profile)


def table(times, forms, targets, values, combination, completed=False):
    panels=[]
    for start in range(0,len(times),3):
        stop=min(start+3,len(times))
        rows=['| **$t$** | '+' | '.join('$'+str(t)+'$' for t in times[start:stop])+' |',
              '| --- | '+' | '.join('---' for t in times[start:stop])+' |']
        for axis in ('x','y'):
            cells=[]
            for i in range(start,stop):
                names=[name for name,loc in targets.items() if tuple(loc)==(axis,i)]
                cells.append(('$'+names[0]+'$' if combination else '{{'+names[0]+'}}')
                             if names and not completed else '$'+tex(values[axis][i])+'$')
            rows.append('| $'+axis+'$ | '+' | '.join(cells)+' |')
        panels.append('\n'.join(rows))
    return '\n\n'.join(panels)


def combination_tex(signs):
    return ''.join(('' if s==1 and i==0 else '+' if s==1 else '-')+name
                   for i,(name,s) in enumerate(zip('abc',signs)))


def render_instance(level,profile,times,forms,targets,signs=None,guidance=None,seed=None):
    """One ordered derivation owns formulas, prompt, table, fields and solution."""
    combo=signs is not None
    values={a:[sp.simplify(scalar(f).subs(T,t)) for t in times] for a,f in forms.items()}
    if any(v.is_finite is not True or v.is_real is not True for row in values.values() for v in row):
        raise ValueError('Invalid cell')
    if len(targets)!=3 or len(set(map(tuple,targets.values())))!=3:raise ValueError('Three distinct target cells required')
    solved={n:values[a][i] for n,(a,i) in targets.items()}
    p='Consider the curve with parametric equations\n\n$$\nx='+forms['x']+r',\qquad y='+forms['y']
    if profile!='trigonometric':p+=r',\qquad '+str(min(times))+r'\le t\le '+str(max(times))
    p+='.'+'\n$$\n\n'
    if combo:
        p+='Consider the following table of values. Angles are in radians.\n\n'
    else:p+='Fill in the three blanks in the table. Give exact values.\n\n'
    if guidance is None:guidance=level=='easy'
    if guidance:
        a,i=next((a,i) for a in ('x','y') for i in range(len(times)) if (a,i) not in map(tuple,targets.values()))
        substituted=re.sub(r'(?<![A-Za-z\\])t(?![A-Za-z])',r'\\left('+str(times[i])+r'\\right)',forms[a])
        p+='Use the value of $t$ at the top of each column in the formula for that row. For example, $'+a+'('+str(times[i])+')='+substituted+'='+tex(values[a][i])+'$.\n\n'
    p+=table(times,forms,targets,values,combo)
    if combo:p+='\n\nFind the exact value of $'+combination_tex(signs)+'$.\n\n{{result}}'
    sections=[];steps=[]
    for name,(axis,i) in targets.items():
        t=times[i];f=forms[axis];val=solved[name]
        label=name if combo else axis+'('+str(t)+')'
        substituted=re.sub(r'(?<![A-Za-z\\])t(?![A-Za-z])',r'\\left('+str(t)+r'\\right)',f)
        stages=[substituted]
        expr=scalar(f)
        if expr.func in (sp.sin,sp.cos,sp.tan):
            arg=expr.args[0].subs(T,t)
            stages.append('\\'+expr.func.__name__+r'\left('+tex(arg)+r'\right)')
        stages.append(tex(val))
        sections.append('The '+('$'+name+'$' if combo else 'missing')+' entry is in the $'+axis+'$-row under $t='+str(t)+'$. Substitute into $'+axis+'='+f+'$:\n\n$$\n'+r'\begin{aligned}'+label+' &='+(' \\\\ &='.join(stages))+r'\end{aligned}'+'\n$$')
        steps.append({'target':name,'axis':axis,'t':t,'operator_input':f,'stages':stages,'final':tex(val)})
    if combo:
        result=sp.simplify(sum(s*solved[n] for n,s in zip('abc',signs)))
        terms=''.join(('' if i==0 and s==1 else '+' if s==1 else '-')+r'\left('+tex(solved[n])+r'\right)' for i,(n,s) in enumerate(zip('abc',signs)))
        sections.append('Substitute the three entries with the signs in the requested expression:\n\n$$\n'+r'\begin{gathered}'+combination_tex(signs)+r' \\ ='+terms+r' \\ ='+tex(result)+r'\end{gathered}'+'\n$$')
        fields=[('result','blank',[tex(result)],tex(result))]
    else:
        result=None
        fields=[(n,'blank',[tex(v)],tex(v)) for n,v in solved.items()]
    sections.append('The completed table is\n\n'+table(times,forms,targets,values,combo,True))
    refs={'guided':['q-326242','q-123753'], 'polynomial':['q-326246','q-326247','q-326248'],
          'quotient':['q-326250','fca75a6f-ed74-5c52-b7db-81a5147488d0'], 'root':['q-326251'],
          'trigonometric':['q-6832','q-326255','q-326256','86dd7dd4-5849-554c-9e2d-91445aacb13c']}
    return record(level,p,'\n\n'.join(sections),fields,{
        'seed':seed,'template':profile,'source_question_ids':refs[profile],
        'parameters':{'times':times,'forms':forms,'targets':targets,'signs':signs,'guidance':guidance},
        'derivation':steps,'displayed_final':tex(result) if combo else {n:tex(v) for n,v in solved.items()},
        'plot_rating':'none','response_design':'exact-entry-combination' if combo else 'three-exact-cells'})


def sample(level,rng,seed=None,profile=None):
    if level not in BANDS:raise ValueError('Unknown band')
    profile=profile or ('guided' if level=='easy' else rng.choice(['polynomial','quotient','root']) if level=='moderate' else 'trigonometric')
    if (level=='easy' and profile!='guided') or (level=='moderate' and profile not in ('polynomial','quotient','root')) or (level=='hard' and profile!='trigonometric'):
        raise ValueError('Incompatible profile')
    times=sorted(rng.sample(range(-4,5),5)) if level=='hard' else [-2,-1,0,1,2]
    # Decide the requested row/column roles before function parameters.
    rows=rng.choice([['x','x','y'],['x','y','y']]);rng.shuffle(rows)
    cols=rng.sample(range(len(times)),3)
    names=list('abc') if level=='hard' else ['field-1','field-2','field-3']
    targets={n:(a,i) for n,a,i in zip(names,rows,cols)}
    signs=[rng.choice([-1,1]) for _ in 'abc'] if level=='hard' else None
    if level!='hard':
        special=rng.choice(['x','y'])
        forms={a:tex(function(profile,rng,('linear' if a==special else 'quadratic') if level=='easy' else ('special' if a==special else 'other'))) for a in ('x','y')}
        return render_instance(level,profile,times,forms,targets,seed=seed)
    # Exact familiar angles only; both sine/cosine and tangent are supported.
    for attempt in range(200):
        pair=rng.choice([('sin',4,'cos',6),('cos',4,'sin',6),('cos',4,'tan',3),('sin',4,'tan',3)])
        if rng.choice([False,True]):pair=pair[2:]+pair[:2]
        forms={a:'\\'+pair[j]+r'\left(\frac{\pi t}{'+str(pair[j+1])+r'}\right)' for a,j in [('x',0),('y',2)]}
        vals=[sp.simplify(scalar(forms[a]).subs(T,times[i])) for a,i in targets.values()]
        occupied=set(map(tuple,targets.values()))
        given={sp.simplify(scalar(forms[a]).subs(T,t)) for a in ('x','y') for i,t in enumerate(times) if (a,i) not in occupied}
        # Preserve exact evaluation at the exemplar's hard stage: no missing
        # value is already printed elsewhere in the table. Hidden equalities
        # and signed cancellation remain eligible.
        if sum(v.is_rational is False for v in vals)>=2 and not set(vals)&given:
            return render_instance(level,profile,times,forms,targets,signs,seed=seed)
        # Regenerate the decision assignment, not just amplitudes.
        times=sorted(rng.sample(range(-4,5),5));cols=rng.sample(range(5),3)
        targets={n:(a,i) for n,a,i in zip(names,rows,cols)}
    raise RuntimeError('No exact-angle role assignment found')


def generate_batch(difficulty,count,seed):
    difficulty='easy' if difficulty=='unclassified' else difficulty
    if difficulty not in BANDS or count<0:raise ValueError('Invalid request')
    rng=random.Random(seed);out=[];seen=set()
    # Whole-batch uniqueness is mathematical prompt uniqueness, not UUID/seed.
    for i in range(count):
        for attempt in range(1000):
            r=sample(difficulty,rng,seed)
            params=r['generation']['parameters']
            signs=params['signs'] or [1,1,1]
            roles=sorted((a,j,s) for (a,j),s in zip(params['targets'].values(),signs))
            # Field/letter renaming is not a new mathematical instance.
            signature=json.dumps([params['forms'],params['times'],roles],sort_keys=True)
            if signature not in seen:
                seen.add(signature);out.append(r);break
        else:raise ValueError('Requested batch exceeds supported diversity')
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=BANDS+('unclassified','all'),default='easy')
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay')
    a=ap.parse_args()
    rs=[replay(a.replay)] if a.replay else [r for band in (BANDS if a.difficulty=='all' else (a.difficulty,)) for r in generate_batch(band,a.count,a.seed)]
    print(json.dumps(rs,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
