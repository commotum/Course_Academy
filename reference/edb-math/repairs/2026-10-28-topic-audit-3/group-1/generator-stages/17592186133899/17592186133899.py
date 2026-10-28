#!/usr/bin/env python3
"""Circulation summation over two holes. Local drafts; no database writes.

Easy: integer circulations already positively oriented. Moderate: the six
observed reversed-orientation families, bounded integers. Hard: authored same
families with noninteger halves and thirds, requiring a common denominator.
Raw observed profiles retain source attribute presence and original prose;
their explicit operation recipes are evidence, not recovered author intent.
Three opaque historical values support only common-scaling evidence replay.
Normal defaults use complete sign-error or omission banks and source masks.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material, asset_output as _ca_asset_output
import argparse
import hashlib
import json
import random
import re
import sys
import uuid
from pathlib import Path
import sympy as sp

KP_ID = 17592186133899
KP_UUID = '56caab23-f54d-58ee-99db-99c651f78e5c'
TITLE = 'Calculating the Circulation of a Vector Field Over a Region Containing Holes'
VERSION='circulation-holes-1.1-format-audit-9837-v1'
HERE = Path(__file__).resolve().parent / str(KP_ID)
WRAPPER = json.loads((HERE / 'source.json').read_text())
SOURCE = WRAPPER['record']
QUESTIONS = {q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
ASSET_ROOT = Path(__file__).resolve().parent / 'source-assets'
NAMESPACE = uuid.UUID(KP_UUID)

# Fixed per-family orientation components, never inferred from a random image.
# +1 means the supplied traversal is already positive, -1 means reversed.
FAMILIES = {
    'positive': {'signs':(1,1,1),'sources':['q-126862','q-126863','q-126855','q-126861'],'level':'easy'},
    'positive_legacy': {'signs':(1,1,1),'sources':['q-126558'],'level':'easy'},
    'all_ccw': {'signs':(1,-1,-1),'sources':['q-126654'],'level':'moderate'},
    'inner3_reverse': {'signs':(1,1,-1),'sources':['q-126865'],'level':'moderate'},
    'all_reverse': {'signs':(-1,-1,-1),'sources':['q-126867'],'level':'moderate'},
    'outer_inner3_reverse': {'signs':(-1,1,-1),'sources':['q-126870'],'level':'moderate'},
    'outer_reverse': {'signs':(-1,1,1),'sources':['q-126868'],'level':'moderate'},
    'inner2_reverse': {'signs':(1,-1,1),'sources':['q-126864'],'level':'moderate'},
}
SOURCE_FAMILY = {q:f for f,s in FAMILIES.items() for q in s['sources']}

# COMPLETE observed bank recipes in source order. Signed triples are exact
# operation definitions, not claims that one scalar identifies author intent.
# Opaque response scale recipes are restricted to values = scale*anchor.
OBSERVED_RECIPES = {
    'q-126558': [('opaque_pi',None),(1,0,0),(1,1,1),(1,-1,-1),(0,0,0)],
    'q-126654': [(-1,1,1),(1,1,-1),(1,-1,-1),(-1,-1,0),(1,1,1)],
    'q-126862': [(1,1,-1),(1,-1,-1),(1,-1,1),(-1,-1,-1),(1,1,1)],
    'q-126863': [(1,1,-1),(1,-1,1),(-1,1,1),(1,1,1),(1,-1,-1)],
    'q-126865': [('opaque_minus_five',None),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)],
    'q-126867': [(0,1,-1),(1,-1,-1),(-1,-1,-1),(1,1,1),(1,-1,1)],
    'q-126870': [(1,1,-1),(-1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,-1)],
    'q-126868': [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,1,1)],
    'q-126864': [(1,-1,1),(1,1,-1),(1,1,1),(-1,1,-1),(1,-1,-1)],
    'q-126855': [(1,1,1),(1,1,-1),(1,-1,1),(0,-1,-1),('opaque_twelve',None)],
    'q-126861': [(1,-1,-1),(1,1,1),(1,-1,1),(0,-1,0),(1,1,-1)],
}
OPAQUE = {'q-126558': 2*sp.pi, 'q-126865':sp.Integer(-5), 'q-126855':sp.Integer(12)}
METHOD_PROFILES = ('method_signs','method_omissions')

class SampleRejected(ValueError):
    """The complete selected bank or declared workload is ineligible."""

def digest(data):
    return hashlib.sha256(json.dumps(_ca_material(data),sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def number(value):
    return sp.latex(sp.Rational(value))

def operand(value):
    tex=number(value)
    return '('+tex+')' if value < 0 else tex

def source_values(q):
    # Complete RHS slots of supplied circulation equations only.
    if q[':question/math-academy-id']=='q-126558':
        return tuple(map(sp.Integer,re.findall(r' dr =\s*(-?\d+)',q[':question/problem'])))
    return tuple(map(sp.Integer,re.findall(r'\\text\{d\}r=(-?\d+)',q[':question/problem'])))

ANCHORS = {q:source_values(record) for q,record in QUESTIONS.items()}

def full_asset(path):
    p=ASSET_ROOT/path
    if not p.is_file():
        raise FileNotFoundError(p)
    return str(p)

def replace_assets(text):
    return re.sub(r'!\[\]\((images/[^)]+)\)',lambda m:'![]('+full_asset(m.group(1))+')',text)

def raw_prompt(q,values):
    """Instantiate numeric RHS slots; preserve every other source byte."""
    it=iter(values)
    pattern=r'( dr =\s*)(-?\d+)' if q[':question/math-academy-id']=='q-126558' else r'(\\text\{d\}r=)(-?\d+)'
    return re.sub(pattern,lambda m:m.group(1)+number(next(it)),q[':question/problem'])

def symbolic_sum(signs):
    terms=[]
    for index,sgn in enumerate(signs,1):
        op='-' if sgn<0 else ('+' if index>1 else '')
        terms.append(op+r'{∮}_{{C}_{'+str(index)+r'}}F\cdot \text{d}r')
    return ''.join(terms)

def arithmetic_sum(values,signs):
    return ''.join(('-' if s<0 else ('+' if i else ''))+operand(v)
                   for i,(v,s) in enumerate(zip(values,signs)))

def render_solution(q,values,signs,hard=False):
    """Retain the family's original prose and exact operative row structure."""
    text=q[':question/worked-solution']
    start=text.index(r'\begin{aligned}')
    prefix=text[:start]
    suffix=text[text.index(r'\end{aligned}',start):]
    total=sum(v*s for v,s in zip(values,signs))
    common=''
    if hard:
        denominator=sp.ilcm(*[v.q for v in values])
        scaled=[sp.Integer(v*denominator) for v in values]
        common=r' \\  & ='+r'\frac{'+arithmetic_sum(scaled,signs)+'}{'+str(denominator)+'}'
    return prefix+r'\begin{aligned}{∮}_{∂D}F\cdot \text{d}r & ='+symbolic_sum(signs)+r' \\  & ='+arithmetic_sum(values,signs)+common+r' \\  & ='+number(total)+'.'+suffix

def legacy_solution_asset():
    """Only new diagram: legacy all-positive geometry lacks a solution raster.

    Original 360x304 raster: origin(169.5,163), outer radius108, two tangent
    circular holes radius27 centered NE/SW. New arrows are outer CCW/inner CW;
    boundaries stay orange because all stated traversals are positive.
    """
    target=_ca_asset_output(HERE/'plots'/'legacy-positive.png')
    side=target.with_suffix('.json')
    if target.is_file() and side.is_file(): return str(target)
    import os
    cache=_ca_asset_output(HERE/'plots'/'matplotlib-cache');cache.mkdir(parents=True,exist_ok=True)
    os.environ.setdefault('MPLCONFIGDIR',str(cache))
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.patches import Circle,FancyArrowPatch
    import numpy as np
    import os,tempfile
    target.parent.mkdir(exist_ok=True)
    fig=Figure(figsize=(3.6,3.04),dpi=160,facecolor='white')
    FigureCanvasAgg(fig)
    ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(-1.57,1.76),ylim=(-1.30,1.51),aspect='equal');ax.axis('off')
    ax.add_patch(Circle((0,0),1,facecolor='#d6e7f5',edgecolor='#f0a000',lw=1))
    centers=((.25,.25),(-.25,-.25))
    for center in centers: ax.add_patch(Circle(center,.25,facecolor='white',edgecolor='#f0a000',lw=1))
    for start,end in [((-1.57,0),(1.57,0)),((0,-1.3),(0,1.3))]:
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=8,color='black',lw=.9))
    for center,radius,direction,angles in [((0,0),1,1,[.76,2.4,3.95,5.55]),(centers[0],.25,-1,[.9,3.,5.1]),(centers[1],.25,-1,[.9,3.,5.1])]:
        for angle in angles:
            a=angle-direction*.07;b=angle+direction*.07
            p=(center[0]+radius*np.cos(a),center[1]+radius*np.sin(a));q=(center[0]+radius*np.cos(b),center[1]+radius*np.sin(b))
            ax.add_patch(FancyArrowPatch(p,q,arrowstyle='->',mutation_scale=8,color='black',lw=.7))
    for label,x,y,color in [('x',1.72,-.03,'black'),('y',0,1.43,'black'),('C_1',.80,.82,'black'),('C_2',.52,.52,'black'),('C_3',-.62,-.51,'black'),('D',-.57,.55,'#287eb9')]:
        ax.text(x,y,'$'+label+'$',fontsize=10,ha='center',va='center',color=color)
    # Unique temporary files and atomic publication, including the sidecar.
    fd,temp=tempfile.mkstemp(suffix='.png',dir=target.parent);os.close(fd)
    try: fig.savefig(temp,dpi=160);os.replace(temp,target)
    finally:
        if os.path.exists(temp):os.unlink(temp)
    spec={'renderer':'Matplotlib','version':matplotlib.__version__,'outer':{'shape':'circle','center':[0,0],'radius':1,'direction':'CCW','color':'orange'},'holes':[{'label':'C2','shape':'circle','center':[.25,.25],'radius':.25,'direction':'CW','color':'orange'},{'label':'C3','shape':'circle','center':[-.25,-.25],'radius':.25,'direction':'CW','color':'orange'}],'source':'q-126558','unchanged_geometry':True}
    fd,temp=tempfile.mkstemp(suffix='.json',dir=target.parent);os.close(fd)
    try:Path(temp).write_text(json.dumps(spec,indent=2));os.replace(temp,side)
    finally:
        if os.path.exists(temp):os.unlink(temp)
    return str(target)

def completed_legacy_solution(values):
    q=QUESTIONS['q-126862']
    text=render_solution(q,values,(1,1,1))
    return re.sub(r'!\[\]\([^)]+\)',lambda m:'![]('+legacy_solution_asset()+')',text)

def check_domain(level,family,values,raw):
    if len(values)!=3 or any(not v.is_Rational for v in values): raise SampleRejected('Three exact rational circulation operands required')
    if raw:
        if level!=FAMILIES[family]['level']:raise SampleRejected('Observed raw level mismatch')
        if any(abs(v)>20 for v in values):raise SampleRejected('Evidence replay magnitudes must be ≤20')
        return
    if any(v==0 or abs(v)>10 for v in values): raise SampleRejected('Nonzero operand magnitudes must be ≤10')
    if not (min(values)<0<max(values)):raise SampleRejected('Mixed operand signs required')
    if level=='easy':
        if family not in ('positive','positive_legacy') or any(v.q!=1 for v in values):raise SampleRejected('Easy needs positive traversals and integers')
    elif level=='moderate':
        if FAMILIES[family]['level']!='moderate' or any(v.q!=1 for v in values):raise SampleRejected('Moderate needs observed reversed traversals and integers')
    else:
        if FAMILIES[family]['level']!='moderate' or any(v.q not in (2,3) for v in values) or {v.q for v in values}!={2,3} or any(abs(v.p)>29 for v in values):
            raise SampleRejected('Hard requires noninteger halves and thirds with both denominators and numerator magnitude ≤29')

def bank_recipes(profile,source_id,values,signs):
    total=sum(v*s for v,s in zip(values,signs))
    if profile.startswith('observed:'):
        recipes=OBSERVED_RECIPES[source_id]
        scale=None
        if source_id in OPAQUE:
            ratios=[v/a for v,a in zip(values,ANCHORS[source_id])]
            if len(set(ratios))!=1 or ratios[0]<=0: raise SampleRejected('Opaque evidence banks require positive common scaling of all source operands')
            scale=ratios[0]
        results=[sum(v*s for v,s in zip(values,op)) if isinstance(op[0],int) else OPAQUE[source_id]*scale for op in recipes]
        # Preserve opaque source notation at the anchor without payload copying.
        tex=[('2π' if source_id=='q-126558' and i==0 and scale==1 else sp.latex(v)) for i,v in enumerate(results)]
    elif profile=='method_signs':
        recipes=[tuple(signs)]+[tuple(-s if j==i else s for j,s in enumerate(signs)) for i in range(3)]+[tuple(-s for s in signs)]
        results=[sum(v*s for v,s in zip(values,op)) for op in recipes];tex=[sp.latex(v) for v in results]
    elif profile=='method_omissions':
        recipes=[tuple(signs)]+[tuple(0 if j==i else s for j,s in enumerate(signs)) for i in range(3)]+[tuple(-s for s in signs)]
        results=[sum(v*s for v,s in zip(values,op)) for op in recipes];tex=[sp.latex(v) for v in results]
    else:raise ValueError('Unsupported complete bank profile: '+profile)
    if len(set(results))!=5 or results.count(total)!=1:raise SampleRejected('Complete selected bank collides')
    return results,tex,recipes,total

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unsupported difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('This KP supports radio only')
    rng=random.Random(seed)
    raw=bool(profile and profile.startswith('observed:'))
    source_id=profile.split(':',1)[1] if raw else None
    if raw and source_id not in QUESTIONS:raise ValueError('Unknown source profile')
    allowed=[f for f,s in FAMILIES.items() if s['level']==('moderate' if level=='hard' else level)]
    family=template or (SOURCE_FAMILY[source_id] if raw else rng.choice(allowed))
    if family not in FAMILIES or family not in allowed:raise ValueError('Unsupported template for level')
    if raw and SOURCE_FAMILY[source_id]!=family:raise ValueError('Profile/template mismatch')
    bank=profile or rng.choice(METHOD_PROFILES)
    if not raw and bank not in METHOD_PROFILES:raise ValueError('Unsupported bank profile')
    if parameters is not None:
        if set(parameters)-{'values','diagram'}:raise ValueError('Unknown parameters')
        if 'values' not in parameters:raise ValueError('Missing circulation values')
        values=tuple(sp.Rational(v) for v in parameters['values'])
        diagram=parameters.get('diagram',source_id or FAMILIES[family]['sources'][0])
        if raw and diagram!=source_id:raise ValueError('Raw source profile requires its own geometry')
        if diagram not in FAMILIES[family]['sources']:raise ValueError('Diagram is not in selected source family')
        check_domain(level,family,values,raw)
        result=bank_recipes(bank,source_id or diagram,values,FAMILIES[family]['signs'])
    else:
        diagram=source_id or rng.choice(FAMILIES[family]['sources'])
        for attempt in range(10000):
            if raw and source_id in OPAQUE:
                scale=sp.Rational(rng.choice([1,2,3]),2);values=tuple(v*scale for v in ANCHORS[source_id])
            elif level=='hard':
                domain=[sp.Rational(n,d) for d in (2,3) for n in range(-29,30) if n and sp.Rational(n,d).q==d and abs(sp.Rational(n,d))<=10]
                values=tuple(rng.choice(domain) for _ in range(3))
            else:values=tuple(sp.Integer(rng.choice([v for v in range(-10,11) if v])) for _ in range(3))
            try:
                check_domain(level,family,values,raw);result=bank_recipes(bank,source_id or diagram,values,FAMILIES[family]['signs']);break
            except SampleRejected:continue
        else:raise RuntimeError('No eligible complete bank sampled')
    vals,tex,recipes,total=result
    q=QUESTIONS[diagram];signs=FAMILIES[family]['signs']
    prompt=raw_prompt(q,values)
    solution=render_solution(q,values,signs,hard=not raw and level=='hard') if ':question/worked-solution' in q else (None if raw else completed_legacy_solution(values))
    if not raw:
        if family=='positive_legacy':
            for index in (1,2,3):
                prompt=prompt.replace('∮_(C_{'+str(index)+'})',r'{∮}_{{C}_{'+str(index)+'}}')
            prompt=prompt.replace('∮_(∂D)',r'{∮}_{∂D}').replace(' dr =',r' \text{d}r =')
        prompt=replace_assets(prompt)
        if solution is not None:solution=replace_assets(solution)
    if not raw:prompt=_ca_problem(prompt);solution=_ca_prose(solution);tex=_ca_values(tex)
    difficulty=q.get(':question/difficulty',{}).get(':db/ident') if raw else ':question.difficulty/'+level
    # Content identity uses actual presentation; option shuffle/profile alias do
    # not change identity. Mathematical identity excludes diagram and bank.
    identity=digest({'version':VERSION,'difficulty':difficulty,'prompt':prompt,'solution':solution,'bank':sorted(tex),'correct_present':not(raw and ':answer-field/correct' not in q[':question/answer-fields'][0])})
    qid=str(uuid.uuid5(NAMESPACE,identity));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'math:'+t)),':answer/type':':answer.type/math',':answer/value':t} for t in tex]
    correct_id=answers[vals.index(total)][':answer/id']
    random.Random(seed).shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    correct_present=not(raw and ':answer-field/correct' not in q[':question/answer-fields'][0])
    if correct_present:field[':answer-field/correct']=[':answer/id',correct_id]
    question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if difficulty:question[':question/difficulty']=difficulty
    if solution is not None:question[':question/worked-solution']=solution
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{
        'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'template':family,'bank_profile':bank,
        'parameters':{'values':[str(v) for v in values],'diagram':diagram},'parameter_fingerprint':digest({'outer':[str(values[0]),signs[0]],'holes':sorted([[str(v),s] for v,s in zip(values[1:],signs[1:])])}),
        'content_fingerprint':identity,'source_id':diagram,'source_provenance':{k:WRAPPER[k] for k in ('database','basis','lineage')},
        'recipes':[list(r) for r in recipes],'answer_math':[str(v) for v in vals],'total':str(total),'inferred_correct_answer_id':correct_id,
        'bank_origin':'observed replay operations, interpretation underdetermined' if raw else 'authored complete method bank',
        'evidence_only':raw,'eligible_for_learning':not raw,'authored_extension':level=='hard' or not raw,'difficulty_claim':'observed' if raw and difficulty else 'authored',
        'plot_rating':'none: unchanged source geometry, one missing solution diagram completed','plot_assets':re.findall(r'!\[\]\(([^)]+)\)',prompt+(solution or ''))}}

# EASY: already-positive outer CCW and two inner CW traversals; three mixed-sign
# nonzero bounded integer operands. Legacy missing fields are completed only in
# the authored normal presentation, never raw evidence replay.
def generate_easy(seed=0,**kwargs):return generate('easy',seed=seed,**kwargs)

# MODERATE: all six observed reversal arrangements, integer operand ceiling10.
# Each preserves its own reversal prose, symbolic signs and substitution row.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed=seed,**kwargs)

# HARD (AUTHORED): same six arrangements and three source stages plus an explicit common-denominator row; all operands are
# reduced noninteger halves/thirds, both denominators present, mixed signs and
# |value|≤10 / |numerator|≤29. No curl, geometry/area or integration demand.
def generate_hard(seed=0,**kwargs):return generate('hard',seed=seed,**kwargs)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    lines=[q[':question/problem'],'']+[f'- ${a[":answer/value"]}$' for a in f[':answer-field/choices']]
    if ':question/worked-solution' in q:lines+=['','Worked solution',q[':question/worked-solution']]
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
    parser.add_argument('--format',choices=['json','markdown'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile')
    args=parser.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))

if __name__=='__main__':main()
