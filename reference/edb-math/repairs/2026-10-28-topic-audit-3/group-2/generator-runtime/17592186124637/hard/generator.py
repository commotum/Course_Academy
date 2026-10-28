#!/usr/bin/env python3
"""Seeded domain-diagram questions. Runtime writes only into the explicit output dir."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import random
import tempfile
import uuid

os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'course-academy-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from math_format import normalize_prose, validate_generated_record

NS = uuid.UUID('9e4fd256-a726-523c-84dc-f62d4e2711cc')
x, y = sp.symbols('x y', real=True)
FAMILIES = {
    'easy': ['polynomial', 'reciprocal_line', 'reciprocal_vertical', 'reciprocal_parabola', 'reciprocal_cubic', 'reciprocal_point'],
    'moderate': ['radical_line', 'radical_parabola', 'radical_circle', 'radical_wedge', 'radical_positive'],
    'hard': ['log_ellipse', 'reciprocal_log'],
}
SOURCES = {
    'polynomial': ['59f09d6c-7a4e-5350-aa9e-955b620390c4'],
    'reciprocal_line': ['036420cb-4253-5cbd-8d56-15a7f64df030'],
    'reciprocal_vertical': ['ddc33dd3-a1a1-567c-a9d1-d5d15d54e87f'],
    'reciprocal_parabola': ['e8d03db3-7c5a-5bd7-8cd4-aef29b72c104'],
    'reciprocal_cubic': ['56f9c6d4-908f-5999-9300-6cd67e4208c5'],
    'reciprocal_point': ['9419d3b0-0595-5357-8a67-2ff487c67499'],
    'radical_line': ['28327fac-a614-5756-91bd-3fcab54fcda2'],
    'radical_parabola': ['3f8af9ca-3fa0-5528-bb2b-5f736d2c06fe'],
    'radical_circle': ['76db17ba-163a-5fe3-9bd7-63e519e3eab2'],
    'radical_wedge': ['a90460ca-8a09-5a2d-bb95-26ae2a0e2a46', '2b882cc3-ef39-5506-bf91-1860550bd797'],
    'radical_positive': ['f90f5dc8-4e9d-5e87-800a-708d8b32cd8d'],
    'log_ellipse': ['aca8e51f-98b0-5cbe-9d48-2cf6165eb100'],
    'reciprocal_log': ['42cbeba7-685e-5782-9695-9671d16b7f80'],
}
OPS = {'neq': r'\ne ', 'gt': '>', 'ge': r'\ge ', 'lt': '<', 'le': r'\le '}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def uid(text):
    return str(uuid.uuid5(NS, text))


def expr(g):
    h, k, a, b = (g.get(n, 0 if n in ('h', 'k') else 1) for n in ('h', 'k', 'a', 'b'))
    u, v = x-h, y-k
    return {'line': v-a*x, 'vertical': u, 'parabola': v-a*u**2,
            'cubic': v-a*u**3, 'point': u**2+v**2,
            'circle': u**2+v**2-a**2, 'wedge': u**2-v**2,
            'ellipse': b*b*u**2+a*a*v**2-a*a*b*b,
            'positive': u**2+v**2+a, 'polynomial': a*x*x-b*y*y+k}[g['kind']]


def tex(e):
    return sp.latex(e, order='lex')


def sample_instance(family, rng, decision=None):
    decision=decision or {}
    # Assessed choices precede coefficient/shift sampling.
    bank_role=rng.randrange(5)
    corner=rng.randrange(4)
    log_scale=rng.choice([1,2])
    extra_mode=rng.choice(['gt','ge'])
    extra_sign=rng.choice([-1,1])
    corner=decision.get('corner',corner)
    log_scale=decision.get('log_scale',log_scale)
    kind = family.split('_')[-1]
    operator = ('polynomial' if family == 'polynomial' else 'reciprocal' if family.startswith('reciprocal_') and family != 'reciprocal_log'
                else 'reciprocal_log' if family == 'reciprocal_log' else 'log' if family.startswith('log_')
                else rng.choice(['sqrt', 'inv_sqrt']))
    sign = rng.choice([-1, 1]) if operator in ('sqrt', 'inv_sqrt', 'log', 'reciprocal_log') else 1
    if family == 'radical_positive': operator, sign = 'sqrt', 1
    if family == 'reciprocal_log': kind = 'line'
    operator=decision.get('operator',operator)
    sign=decision.get('sign',sign)
    g = dict(kind=kind, h=rng.randint(-2, 2), k=rng.randint(-2, 2), a=rng.choice([-2, -1, 1, 2]), b=1)
    if kind=='positive': g['a']=rng.randint(1,3)
    if kind=='circle':g.update(a=rng.randint(1,4),h=rng.randint(-1,1),k=rng.randint(-1,1))
    if kind == 'ellipse':
        g.update(h=rng.randint(-1, 1), k=rng.randint(-1, 1))
        g['a'], g['b'] = rng.sample([1, 2, 3], 2)
    if kind == 'wedge': g['h'] = g['k'] = 0  # familiar intersecting diagonals; side still varies
    if kind == 'polynomial': g['b'] = rng.randint(1, 3)
    if 'orientation' in decision:g['a']=decision['orientation']
    if kind in ('line','polynomial'): g['h']=0
    if kind=='vertical': g.update(h=rng.choice([-2,0,2])+corner%2,k=0,a=1,b=1)
    if kind=='point': g.update(h=rng.choice([-2,0,2])+corner%2,k=rng.choice([-2,0,2])+corner//2,a=1,b=1)
    return dict(family=family, geometry=g, operator=operator, sign=sign, numerator=rng.choice([1, 2, 3]), profile=rng.randrange(2),bank_role=bank_role,extra_mode=extra_mode,extra_sign=extra_sign,log_scale=log_scale)


def target_mode(i):
    op = i['operator']
    if op == 'polynomial' or i['geometry']['kind'] == 'positive': return 'all'
    return {'reciprocal': 'neq', 'sqrt': 'ge', 'inv_sqrt': 'gt', 'log': 'gt', 'reciprocal_log': 'log'}[op]


def region(g, mode, sign=1):
    return dict(geometry=copy.deepcopy(g), mode=mode, sign=sign)


def alter(g):
    q = dict(g)
    if g['kind'] == 'ellipse': q['a'], q['b'] = g['b'], g['a']
    elif g['kind'] in ('line', 'parabola', 'cubic'): q['a'] = -g['a']
    elif g['kind'] == 'wedge': q['kind'] = 'circle'; q['a'] = 2
    elif g['kind'] in ('point', 'vertical'): q['h'] = g['h'] + (1 if g['h']%2==0 else -1)
    elif g['kind'] == 'circle': q['a'] = g['a'] + (1 if g['a']%2 else -1)
    else: q['kind'] = 'circle'; q['a'] = 2
    return q


def bank_specs(i):
    g, s, mode = i['geometry'], i['sign'], target_mode(i)
    alt = alter(g)
    key = region(g, mode, s)
    if mode == 'all':
        # Whole-plane cases intentionally assess absence of restrictions.
        if g['kind'] == 'polynomial':
            base = dict(g, kind='wedge', h=0, k=0)
        else: base = dict(g, kind='circle', a=2)
        return [key, region(base, 'ge'), region(base, 'gt'), region(base, 'le'), region(base, 'neq')]
    if mode == 'neq' and g['kind']=='point':
        alt_y=dict(g,k=g['k']+(1 if g['k']%2==0 else -1))
        alt_both=dict(alt_y,h=alt['h'])
        return [key,region(alt,'neq'),region(alt_y,'neq'),region(alt_both,'neq'),region(g,'all')]
    if mode == 'neq':
        # The same unordered bank supports either zero locus as the correct answer.
        side='gt' if i['profile'] else 'lt'
        return [key, region(alt,'neq',s), region(g,side,s),region(alt,side,s),region(g,'all')]
    if mode == 'log':
        scale=i.get('log_scale',1)
        # Two identical positive half-planes with different excluded levels require
        # the logarithm-zero calculation. Neither line rank is always correct.
        key=dict(key,hole=scale)
        return [key,dict(region(g,'log',s),hole=3-scale),region(g,'gt',s),
                dict(region(g,'log',-s),hole=1),dict(region(alt,'log',s),hole=2)]
    if g['kind']=='wedge':
        # No partial wedge echoes the key. All four side/inclusion cases can be correct.
        return [key]+[region(g,m,t) for m in ['ge','gt'] for t in [-1,1] if (m,t)!=(mode,s)]+[region(g,'all')]
    # A whole five-image profile, with a variable answer-bearing role. Four side /
    # inclusion states of one locus and one state of the other locus. The key can
    # be any of the five displayed regions; no geometry majority fixes its role.
    # alter() is an involution over the served parameter domain.
    majority=g if i.get('bank_role',0)<4 else alt
    minority=alt if i.get('bank_role',0)<4 else g
    extra=(i.get('extra_mode','gt'),i.get('extra_sign',1)) if i.get('bank_role',0)<4 else (mode,s)
    specs=[region(majority,m,t) for m in ['ge','gt'] for t in [-1,1]]+[region(minority,*extra)]
    return [key]+[q for q in specs if q!=key]


def values(g, xx, yy):
    h,k,a,b=(g.get(n,0 if n in ('h','k') else 1) for n in ('h','k','a','b'))
    u,v=xx-h,yy-k
    kind=g['kind']
    if kind=='line': return v-a*xx
    if kind=='vertical': return u
    if kind=='parabola': return v-a*u*u
    if kind=='cubic': return v-a*u*u*u
    if kind in ('circle','point','positive'):
        return u*u+v*v+(-a*a if kind=='circle' else a if kind=='positive' else 0)
    if kind=='wedge': return u*u-v*v
    if kind=='ellipse': return b*b*u*u+a*a*v*v-a*a*b*b
    return a*xx*xx-b*yy*yy+k


def mask(spec, xx, yy):
    z = spec['sign']*values(spec['geometry'], xx, yy)
    mode = spec['mode']
    if mode == 'all': return np.ones(np.broadcast(xx,yy).shape, dtype=bool)
    if mode == 'neq': return np.abs(z)>1e-9
    if mode == 'gt': return (z>1e-9) & ((xx>=0) if spec.get('half')=='right' else (yy>=0) if spec.get('half')=='upper' else True)
    if mode == 'ge': return (z>=-1e-9) & ((xx>=0) if spec.get('half')=='right' else (yy>=0) if spec.get('half')=='upper' else True)
    if mode == 'lt': return z<-1e-9
    if mode == 'le': return z<=1e-9
    if mode=='beyond': return z>1+1e-9
    if mode=='strip': return (z>1e-9)&(z<1-1e-9)
    return (z>1e-9)&(np.abs(z-spec.get('hole',1))>1e-9)


def plot(spec, output):
    name = 'domain_'+hashlib.sha256(canonical(spec).encode()).hexdigest()[:24]+'.png'
    path=output/name
    if path.exists(): return name
    fig, ax=plt.subplots(figsize=(3.2,3.2),dpi=120)
    # Identical extent/style for every choice, irrespective of correctness.
    ax.set_position([.12,.12,.83,.83]); ax.set_xlim(-6,6); ax.set_ylim(-6,6); ax.set_aspect('equal')
    zgrid=np.linspace(-6,6,481); xx,yy=np.meshgrid(zgrid,zgrid)
    zz=spec['sign']*values(spec['geometry'],xx,yy)
    allowed=mask(spec,xx,yy)
    from matplotlib.colors import ListedColormap
    ax.pcolormesh(xx,yy,allowed,cmap=ListedColormap(['white','#c8deef']),vmin=0,vmax=1,shading='nearest',rasterized=True)
    for spine in ['right','top']: ax.spines[spine].set_visible(False)
    ax.spines['left'].set_position('zero'); ax.spines['bottom'].set_position('zero')
    for spine in ['left','bottom']:
        ax.spines[spine].set_color('#555555'); ax.spines[spine].set_linewidth(.65); ax.spines[spine].set_zorder(2)
    ticks=[-4,-2,2,4]
    ax.set_xticks(ticks); ax.set_yticks(ticks); ax.tick_params(labelsize=8,length=2,pad=2,colors='#444444')
    ax.text(5.7,-.6,'$x$',fontsize=11); ax.text(.25,5.5,'$y$',fontsize=11)
    mode=spec['mode']; kind=spec['geometry']['kind']
    if mode != 'all':
        if kind=='point' and mode=='neq':
            ax.plot(spec['geometry']['h'],spec['geometry']['k'],'o',mfc='white',mec='#246a9c',ms=6,mew=1.3,zorder=5)
        else:
            levels=[0, spec.get('hole',1)] if mode in ('log','strip') else [1] if mode=='beyond' else [0]
            style='solid' if mode in ('ge','le') else 'dashed'
            # A white under-stroke makes excluded loci visible in a shaded plane.
            if style=='dashed':
                ax.contour(xx,yy,zz,levels=sorted(levels),colors='white',linewidths=2.8,zorder=3)
            ax.contour(xx,yy,zz,levels=sorted(levels),colors='#246a9c',linewidths=1.35,linestyles=style,zorder=4)
    fig.savefig(path,facecolor='white',metadata={'Software':'Course Academy domain renderer v1'})
    plt.close(fig)
    return name


def solution(i, correct_image):
    g,op,s=i['geometry'],i['operator'],i['sign']
    q=expr(g); r=s*q; mode=target_mode(i); t=tex(r)
    scale=i.get('log_scale',1) if op=='reciprocal_log' else 1
    argument=tex(r/scale)
    if op=='polynomial':
        text='A polynomial is defined for every real pair $(x,y)$. No denominator, radical or logarithm restricts the inputs. Thus $D=\\mathbb{R}^2$: shade the **entire plane**.'
    elif g['kind']=='positive':
        text=(f'The radicand must be nonnegative. Both squared terms are nonnegative, so ${t}\\ge {g["a"]}>0$ for every real pair $(x,y)$. '
              'Therefore $D=\\mathbb{R}^2$: shade the **entire plane**.')
    else:
        rule={'reciprocal':'The denominator must be nonzero.', 'sqrt':'The radicand must be nonnegative.',
              'inv_sqrt':'The radicand must be nonnegative and the denominator must be nonzero. Together these require a strictly positive radicand.',
              'log':'The argument of the logarithm must be positive.',
              'reciprocal_log':'The logarithm needs a positive argument, and its value in the denominator must be nonzero.'}[op]
        if mode=='log':
            cond=t+r'>0,\quad '+t+r'\ne '+str(scale)
            domain_cond=r'\begin{aligned}'+t+r'&>0 \\ '+t+r'&\ne '+str(scale)+r'\end{aligned}'
            deriv=(r'\begin{aligned}'+argument+r'&>0 \\ \ln\!\left('+argument+r'\right)&\ne0 \\ '+argument+r'&\ne1'+(r' \\ '+t+r'&\ne '+str(scale) if scale!=1 else '')+r'\end{aligned}')
            detail=(r'Since $\ln(1)=0$ and the logarithm is one-to-one on positive inputs, its argument must differ from $1$. '
                    + (f'Multiplying both restrictions by the positive constant ${scale}$ gives ${cond}$. ' if scale!=1 else '')
                    + f'Shade the half-plane ${t}>0$ and remove the parallel line ${t}={scale}$. Both lines are **excluded**, so draw them dashed. Keep both portions of the positive half-plane separated by the removed line.')
        else:
            restriction=t+OPS[mode]+'0'; cond=restriction
            final=restriction
            kind=g['kind']
            if kind in ('line','parabola','cubic','vertical'):
                if kind=='vertical': left=x; right=g['h']; direction=1
                else: left=y; right=sp.solve(q,y)[0]; direction=s
                relation=mode
                if relation in ('gt','ge','lt','le') and direction<0: relation={'gt':'lt','ge':'le','lt':'gt','le':'ge'}[relation]
                final=tex(left)+OPS[relation]+tex(right)
                sense={'gt':'above' if kind!='vertical' else 'to the right of','ge':'above' if kind!='vertical' else 'to the right of',
                       'lt':'below' if kind!='vertical' else 'to the left of','le':'below' if kind!='vertical' else 'to the left of','neq':'on both sides of'}[relation]
                detail=f'Solving for ${tex(left)}$ gives ${final}$. Shade **{sense}** the boundary ${tex(left)}={tex(right)}$.'
            elif kind=='point':
                final=rf'(x,y)\ne({g["h"]},{g["k"]})'
                detail=f'A sum of two real squares is zero exactly when both squares are zero. Remove only the point $({g["h"]},{g["k"]})$, shown by a hollow circle; shade the rest of the plane.'
            elif kind in ('circle','ellipse'):
                u,v=x-g['h'],y-g['k']; a,b=g['a'],g['b']
                lhs=u*u+v*v if kind=='circle' else u*u/(a*a)+v*v/(b*b)
                rhs=a*a if kind=='circle' else 1
                relation=mode if s>0 else {'gt':'lt','ge':'le','lt':'gt','le':'ge'}[mode]
                final=tex(lhs)+OPS[relation]+str(rhs)
                side='outside' if relation in ('gt','ge') else 'inside'
                detail=(f'Rearrange'+(f' and divide by the positive constant ${a*a*b*b}$' if kind=='ellipse' else '')+f' to obtain ${final}$. '
                        f'The boundary is centered at $({g["h"]},{g["k"]})$'+(f' with horizontal and vertical semiaxes ${a}$ and ${b}$' if kind=='ellipse' else f' with radius ${a}$')+f'. Shade **{side}** it.')
            elif kind=='wedge':
                final=(r'y^2'+(r'\le ' if mode=='ge' else '<')+r'x^2') if s>0 else (r'x^2'+(r'\le ' if mode=='ge' else '<')+r'y^2')
                detail=('Comparing the squares gives $'+final+'$. Shade the **'+('left and right' if s>0 else 'upper and lower')+'** wedges between the diagonal lines $y=x$ and $y=-x$.')
            deriv=r'\begin{aligned}&'+restriction+r' \\ &\Longleftrightarrow '+final+r'\end{aligned}'
            cond=final
            if kind!='point': detail+=' The boundary is **'+('included** (solid).' if mode in ('ge','le') else 'excluded** (dashed).')
        text=rule+'\n\n$$\n'+deriv+'\n$$\n\n'+detail+'\n\nTherefore,\n\n$$\nD=\\left\\{(x,y)\\in\\mathbb{R}^2\\;:\\;'+(domain_cond if mode=='log' else cond)+r'\right\}.'+'\n$$'
    return text+'\n\n![]('+correct_image+')'


def make_record(i, difficulty, output, rng):
    specs=bank_specs(i); key_spec=specs[0]; rng.shuffle(specs)
    images=[plot(c,output) for c in specs]
    r=i['sign']*expr(i['geometry']); raw=tex(r); n=i['numerator'];op=i['operator']
    log_input=tex(r/i.get('log_scale',1))
    function={'polynomial': raw, 'reciprocal':rf'\frac{{{n}}}{{{raw}}}', 'sqrt':rf'\sqrt{{{raw}}}',
              'inv_sqrt':r'\frac{'+str(n)+r'}{\sqrt{'+raw+'}}', 'log':rf'\ln\!\left({raw}\right)',
              'reciprocal_log':rf'\frac{{{n}}}{{\ln\!\left({log_input}\right)}}'}[op]
    problem=normalize_prose('Which of the following shaded regions corresponds to the domain of the real-valued function $f(x,y)='+function+'$?')
    key_image=images[specs.index(key_spec)]
    worked=normalize_prose(solution(i,key_image))
    identity=uid(canonical([problem, sorted(images)]))
    choices=[{':answer/id':uid(identity+':'+v), ':answer/type':':answer.type/image', ':answer/value':v} for v in images]
    field={':answer-field/id':uid(identity+':selection'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
           ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[images.index(key_image)][':answer/id']]}
    record={'knowledge_point':{'db_id':17592186124637,'id':str(NS)},'question':{':question/id':identity,':question/problem':problem,
            ':question/worked-solution':worked,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[field]},
            'generation':{'version':1,'template':i['family'],'instance':i,'choice_regions':specs,'source_question_ids':SOURCES[i['family']]}}
    return validate_generated_record(record)


def generate(difficulty,count,seed,output):
    rng=random.Random(seed); records=[]; seen=set(); schedule=[]; misses=0; decisions={}; answer_positions=[]
    def draw_decision(family):
        if family not in decisions or not decisions[family]:
            if family.startswith('radical_') and family!='radical_positive':
                cases=[dict(operator=o,sign=t) for o in ['sqrt','inv_sqrt'] for t in [-1,1]]
            elif family=='log_ellipse': cases=[dict(sign=t) for t in [-1,1]]
            elif family=='reciprocal_log': cases=[dict(sign=t,log_scale=c) for t in [-1,1] for c in [1,2]]
            elif family in ('reciprocal_line','reciprocal_parabola','reciprocal_cubic'):cases=[dict(orientation=a) for a in [-2,-1,1,2]]
            elif family=='reciprocal_point':cases=[dict(corner=c) for c in range(4)]
            elif family=='reciprocal_vertical':cases=[dict(corner=c) for c in range(2)]
            else:cases=[{}]
            rng.shuffle(cases);decisions[family]=cases
        return decisions[family].pop()
    while len(records)<count:
        if not schedule: schedule=FAMILIES[difficulty][:];rng.shuffle(schedule)
        family=schedule.pop();i=sample_instance(family,rng,draw_decision(family))
        signature=canonical([i['family'], str(sp.expand(i['sign']*expr(i['geometry'])/(i.get('log_scale',1) if i['operator']=='reciprocal_log' else 1))), i['operator']])
        if signature in seen:
            misses+=1
            if misses>=1000: raise ValueError('The finite domain catalog cannot supply the requested number of distinct formulas; request a smaller batch.')
            continue
        misses=0
        record=make_record(i,difficulty,output,rng)
        # A finite delivered batch must not accidentally teach a fixed option.
        # Deal each answer position once per five accepted records; the schedule
        # advances only after semantic rejection/resampling has succeeded.
        if not answer_positions:
            answer_positions=list(range(5));rng.shuffle(answer_positions)
        desired=answer_positions.pop()
        field=record['question'][':question/answer-fields'][0]
        current=next(j for j,c in enumerate(field[':answer-field/choices'])
                     if c[':answer/id']==field[':answer-field/correct'][1])
        for sequence in [field[':answer-field/choices'],record['generation']['choice_regions']]:
            sequence[current],sequence[desired]=sequence[desired],sequence[current]
        seen.add(signature);records.append(record)
    for r in records:r['generation']['seed']=seed
    return records


def replay(source_id):
    records=json.loads(Path(__file__).with_name('source_cases.json').read_text())
    return next(r for r in records if r['question'][':question/id']==source_id)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json')
    p.add_argument('--source-id',help='Explicit unchanged-parameter source replay for fidelity checks')
    args=p.parse_args()
    if not 0<=args.count<=2000:p.error('count must be between 0 and 2000')
    out=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if args.source_id: records=[replay(args.source_id)]
    else:
        if not out:p.error('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required')
        output=Path(out).resolve()
        if output==Path(__file__).parent.resolve():p.error('output directory must differ from the package root')
        output.mkdir(parents=True,exist_ok=True)
        records=generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed,output)
    print(json.dumps(records,ensure_ascii=False))

if __name__=='__main__': main()
