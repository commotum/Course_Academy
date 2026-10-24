#!/usr/bin/env python3
"""Portable continuation of 17592186138429-draft, contextual intersections."""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186138429-source-policy.json'))
    raise SystemExit(0)

import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import sys
import uuid
sys.dont_write_bytecode = True
import sympy as sp
from math_format import normalize_prose, normalize_tex, checked_math_content

HERE = Path(__file__).resolve().parent
KP_ID = 17592186138429
KP_UUID = '4154d81b-c94a-57f7-80fa-0daa341505e6'
VERSION = 'word-graphs-portable-1'
SOURCE = json.loads((HERE / 'source.json').read_text())
QUESTIONS = SOURCE['material']['kp'][':knowledge-point/questions']
CANONICAL = SOURCE['material']['kp'][':knowledge-point/canonical-example']

# Constants below are retained from the supplied draft (see provenance).
PROMPTS={
 'cars':'The graph above shows the speed of cars $A$ and $B$ as a function of the distance that they traveled during a brake test. At which distance, in meters, did both cars reach the same speed?',
 'trucks':'Two trucks, Truck $A$ and Truck $B$, are carrying shipments between distribution centers. The graph above shows the distances (in miles) of Truck $A$ and Truck $B$ from one of the centers as a function of time (in hours). At what time are Truck $A$ and Truck $B$ the same distance from the center?',
 'pools':'The graph above shows the number of liters of water in pool $A$ and pool $B$ as a function of time, measured in days. How many days will it take for both pools to contain the same amount of water?'}

CONFIG={'cars':{'x_label':'Distance (m)','y_label':'Speed (km/h)','labels':['Car A','Car B']},'trucks':{'x_label':'Hours','y_label':'Miles','labels':['Truck A','Truck B']},'pools':{'x_label':'Days','y_label':'Liters','labels':['Pool A','Pool B']}}

SOURCE_PARAMETERS={
 'cars':{'a0':80,'a1':'-3/4','b0':40,'b1':'-1/4','xmax':100,'dx':10,'ymax':90,'dy':10,'ylabel_step':20,'xlabel_step':10},
 'trucks':{'a0':0,'a1':50,'b0':750,'b1':-75,'xmax':7,'dx':1,'ymax':900,'dy':100,'ylabel_step':200,'xlabel_step':1},
 'pools':{'a0':150,'a1':50,'b0':775,'b1':-75,'xmax':7,'dx':1,'ymax':900,'dy':100,'ylabel_step':200,'xlabel_step':1}}

ORIGINAL_ASSETS={
 'cars':'images/0d/0d5e3ef2393a00fc74c91ebc44f71d553e641d0e1bca21bf783252cbafcca84c.png',
 'trucks':'images/b9/b91b1093a485c671cb5e7566498a1e2b95452d9b92ea87e478696ff8c9ace0ff.png',
 'pools':'images/09/0915c99015922e27855d92ebb13756da634a8f10dd8fe3abbc016590f06e1077.png'}

PARAMS={
 'planes':dict(a0=4,a1='4/3',b0=0,b1='5/3',xmax=24,dx=3,ymax=36,dy=4,ylabel_step=4,xlabel_step=3),
 'tanks':dict(a0=25,a1='-5/2',b0=5,b1='5/2',xmax=7,dx=1,ymax=35,dy=5,ylabel_step=5,xlabel_step=1)}

WALKER_PARAMS=dict(a0=0,a1='300/11',b0=960,b1=-60,xmax=20,dx=1,ymax=1050,dy=50,ylabel_step=200,xlabel_step=2)

SOURCE_PARAMETERS.update(PARAMS)
SOURCE_PARAMETERS['walkers'] = WALKER_PARAMS
CONFIG.update({
    'planes': dict(x_label='Minutes', y_label='Feet (thousands)', labels=['Airplane A', 'Airplane B']),
    'tanks': dict(x_label='Minutes', y_label='Liters', labels=['Tank A', 'Tank B']),
    'walkers': dict(x_label='Time (minutes)', y_label='Distance (meters)', labels=['Sam', 'Mary'])})
SOURCE_IDS = dict(cars='q-45165', trucks='q-59886', planes='q-102519', tanks='q-237989', walkers='q-166758', pools='e-13130')
CONTEXTS = tuple(SOURCE_IDS)
WINDOWS = {
    'cars': (100,120,10,10,10,20), 'trucks': (12,1600,1,100,1,200),
    'pools': (12,1400,1,100,1,200), 'planes': (24,40,3,4,3,4),
    'tanks': (10,65,1,5,1,5), 'walkers': (20,1200,1,50,2,200)}
TARGETS = {
    'cars': (list(range(30,81,10)), [20,30,40,50]),
    'trucks': (list(range(3,10)), list(range(100,701,100))),
    'pools': (list(range(3,10)), list(range(200,701,100))),
    'planes': ([6,9,12,15,18], [12,16,20,24,28]),
    'tanks': (list(range(2,8)), [15,20,25,30]),
    'walkers': (list(range(5,15)), [200,300,400,500,600])}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def normalize(p):
    if set(p) != set(SOURCE_PARAMETERS['cars']):
        raise ValueError('Exact parameter keys required')
    q = {k: sp.Rational(v) for k,v in p.items()}
    return {k: int(v) if v.q == 1 else str(v) for k,v in q.items()}

def derive(p):
    a0,a1,b0,b1 = [sp.Rational(p[k]) for k in ('a0','a1','b0','b1')]
    if a1 == b1: raise ValueError('Unique intersection required')
    t = (b0-a0)/(a1-b1)
    return t, a0+a1*t

def source_question(name, source_id=None):
    sid = source_id or SOURCE_IDS[name]
    if sid != SOURCE_IDS[name] and not (name=='walkers' and sid=='q-135288'):
        raise ValueError('Source ID must belong to the selected context')
    return CANONICAL if sid == 'e-13130' else next(q for q in QUESTIONS if q[':question/math-academy-id'] == sid)

def guard(name, p):
    if name not in CONTEXTS: raise ValueError('Unknown template')
    r = {k: sp.Rational(v) for k,v in p.items()}
    t,y = derive(p)
    if t.q != 1 or y.q != 1 or not 0<t<r['xmax'] or not 0<y<r['ymax']:
        raise ValueError('Visible positive integer grid intersection required')
    for k in ('xmax','ymax','dx','dy','xlabel_step','ylabel_step'):
        if r[k] <= 0 or r[k].q != 1: raise ValueError('Positive integer grids required')
    if t % r['dx'] or y % r['dy']:
        raise ValueError('Intersection must be on the grid')
    if r['xmax']%r['dx'] or r['ymax']%r['dy'] or r['xlabel_step']%r['dx'] or r['ylabel_step']%r['dy']:
        raise ValueError('Integral grid layout required')
    if any(not 0<=r[k+'0']<r['ymax'] for k in ('a','b')):
        raise ValueError('Visible nonnegative initial values required')
    if name=='cars' and not r['a1']<r['b1']<0: raise ValueError('Both cars brake')
    if name=='trucks' and not (r['a0']==0 and r['a1']>0>r['b1']): raise ValueError('Truck directions')
    if name=='pools' and not (r['a0']>0 and r['a1']>0>r['b1']): raise ValueError('Pool directions')
    if name=='planes' and not (r['a0']>0 and r['b0']==0 and 0<r['a1']<r['b1']): raise ValueError('Plane ascent')
    if name=='tanks' and not (r['a0']>r['b0'] and r['a1']==-r['b1']<0): raise ValueError('Conserved transfer')
    if name=='walkers' and not (r['a0']==0 and r['a1']>0>r['b1']): raise ValueError('Opposite walks')
    return t,y

def sample(name, rng, target=None):
    """Choose the answer-bearing grid slot first, then compatible geometry.

    Rejection is local to geometry, never to the chosen target or bank rank.
    """
    ts,ys = TARGETS[name]
    t = target[0] if target else rng.choice(ts)
    if t not in ts: raise ValueError('Unsupported target')
    preferred_y = target[1] if target else None
    if preferred_y is not None and preferred_y not in ys: raise ValueError('Unsupported target')
    attempts = 0
    while attempts < 100:
        attempts += 1
        y = preferred_y if preferred_y is not None else rng.choice(ys)
        if name=='cars':
            a1,b1 = rng.choice([(sp.Rational(-1,2),sp.Rational(-1,4)),(sp.Rational(-3,4),sp.Rational(-1,4)),(-1,sp.Rational(-1,2))])
            a0,b0 = y-a1*t,y-b1*t
        elif name in ('trucks','pools','walkers'):
            a0 = 0 if name!='pools' else rng.choice([50,100,150])
            a1 = sp.Rational(y-a0,t)
            b1 = -rng.choice([25,50,75])
            b0 = y-b1*t
        elif name=='planes':
            a0,b0 = rng.choice([4,8]),0
            a1,b1 = sp.Rational(y-a0,t),sp.Rational(y,t)
        else:
            a1,b1 = -sp.Rational(5,2),sp.Rational(5,2)
            a0,b0 = y-a1*t,y-b1*t
        xmax,ymax,dx,dy,xlabel_step,ylabel_step = WINDOWS[name]
        p = normalize(dict(a0=a0,a1=a1,b0=b0,b1=b1,xmax=xmax,ymax=ymax,dx=dx,dy=dy,xlabel_step=xlabel_step,ylabel_step=ylabel_step))
        try: guard(name,p)
        except ValueError: continue
        return p, attempts
    raise ValueError('No compatible geometry for selected target')

def bank(p, rng, start=None):
    """A complete five-tick bank; the correct sorted rank is not fixed."""
    t,_ = derive(p)
    dx = p['dx']
    starts = [s for s in range(dx,p['xmax']-4*dx+1,dx) if s<=t<=s+4*dx]
    if start is None: start = rng.choice(starts)
    if start not in starts: raise ValueError('Bank must contain intersection')
    return list(map(sp.Rational,range(start,start+5*dx,dx)))

def render_plots(name,p,output_dir=None):
    from plot import render
    directory = output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not directory: raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required')
    directory = Path(directory).resolve()
    if directory == HERE or HERE in directory.parents:
        # Evidence directories are outside the declared runtime package; the
        # runner normally supplies a separate asset directory. Never silently
        # default to writing beside this file.
        if directory == HERE: raise ValueError('Use an explicit asset subdirectory or external directory')
    directory.mkdir(parents=True,exist_ok=True)
    spec = dict(template=name,parameters=p,labels=CONFIG[name],intersection=list(map(str,derive(p))))
    assets = {}
    for role in ('prompt','solution'):
        revision = VERSION + ('-physical-endpoints-2' if name in ('tanks','walkers') else '')
        data = {**spec,'annotated':role=='solution','renderer_revision':revision}
        filename = 'images/generated/'+digest(data)+'.png'
        path = directory/filename
        if not path.exists(): render(data,path)
        # The runner reserves relative images/... paths for published assets.
        # These bytes are unpublished and live in the caller's output directory.
        assets[role] = dict(reference=str(path),relative_reference=filename,geometry=data)
    return assets

def solution(name,p,assets):
    t,y=derive(p); graph='![]('+assets['solution']['reference']+')'
    if name=='pools': return 'The pools have the same amount of water when the two graphs intersect.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y})$. So, both pools have the same amount (${y}\\,\\textrm{{L}}$) of water at $t={t}$ days.'
    if name=='cars': return 'The cars have the same speed when the two graphs intersect.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y})$. So, both cars have the same speed (${y}\\,\\textrm{{km/h}}$) at a distance of ${t}$ meters.'
    if name=='trucks': return 'The trucks are the same distance from the center when the two graphs intersect.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y})$. So, both trucks are the same distance (${y}\\,\\textrm{{miles}}$) from the center at $t={t}$ hours.'
    if name=='planes': return 'Here, we need to find the point of intersection of the two graphs.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y}).$ So, it takes ${t}$ minutes for both planes to get to the same altitude (of ${int(y)*1000:,}\\,\\text{{ft}}$).'
    if name=='tanks': return 'The tanks contain the same amount when the two graphs intersect.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y}).$ So, the tanks contain the same amount (${y}\\,\\text{{L}}$) of water after $t={t}$ minutes.'
    return 'Mary and Sam meet when they are at the same distance from home. At this moment, their graphs intersect.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y}).$ So, Mary and Sam met ${t}$ minutes since they started moving at a distance of ${y}\\,\\text{{m}}$ away from their home.'

@checked_math_content
def generate(level='easy',seed=0,template=None,parameters=None,source_id=None,replay=False,bank_start=None,output_dir=None,target=None):
    if level!='easy': raise ValueError('Only source-justified easy band is supported')
    rng=random.Random(seed)
    name=template or rng.choice(CONTEXTS)
    if name not in CONTEXTS: raise ValueError('Unknown template')
    sq=source_question(name,source_id)
    if replay:
        p=normalize(SOURCE_PARAMETERS[name]); attempts=0
    elif parameters is not None:
        p=normalize(parameters); attempts=0
    else: p,attempts=sample(name,rng,target)
    t,y=guard(name,p)
    if not replay:
        if t not in TARGETS[name][0] or y not in TARGETS[name][1]:
            raise ValueError('Normal questions must use the declared target slots')
        if tuple(p[k] for k in ('xmax','ymax','dx','dy','xlabel_step','ylabel_step')) != WINDOWS[name]:
            raise ValueError('Normal questions must use the fixed context viewport')
    if replay:
        def asset(prose): return dict(reference=prose.split('![](')[1].split(')')[0])
        assets={'prompt':asset(sq[':question/problem'])}
        if ':question/worked-solution' in sq: assets['solution']=asset(sq[':question/worked-solution'])
        else: assets['solution']=render_plots(name,p,output_dir)['solution']
    else: assets=render_plots(name,p,output_dir)
    prompt='![]('+assets['prompt']['reference']+')'+sq[':question/problem'].split(')',1)[1]
    worked=solution(name,p,assets)
    if replay and ':question/worked-solution' in sq:
        worked=sq[':question/worked-solution']
        if sq[':question/math-academy-id']=='q-166758': worked=worked.replace('Mary and her brother','Mary and Sam')
    field_kind='blank' if name in ('tanks','walkers') else 'radio'
    if replay and name!='pools':
        specs=[]
        for f in sq[':question/answer-fields']:
            key=f[':answer-field/key'];values=[a[':answer/value'] for a in f[':answer-field/choices']]
            correct=f.get(':answer-field/correct',{}).get(':answer/value',str(t)+('h' if name=='trucks' else ''))
            specs.append((key,values,correct))
        profile='source-complete-bank' if field_kind=='radio' else 'source-blank'
    elif field_kind=='radio':
        vals=bank(p,rng,bank_start); suffix='h' if name=='trucks' else ''
        specs=[('selection',[str(v)+suffix for v in vals],str(t)+suffix)]
        profile='authored-variable-grid-window'
    else:
        specs=[('field-1',[str(t)],str(t))]
        if name=='walkers': specs.append(('field-2',[str(y)],str(y)))
        profile='source-blank'
    prompt,worked=normalize_prose(prompt),normalize_prose(worked)
    def logical_prose(text):
        for asset in assets.values():
            if 'relative_reference' in asset:
                text=text.replace(asset['reference'],asset['relative_reference'])
        return text
    content=digest(dict(prompt=logical_prose(prompt),solution=logical_prose(worked),fields=specs))
    qid=uuid.uuid5(uuid.NAMESPACE_URL,KP_UUID+'/'+content);fields=[]
    for key,values,correct in specs:
        fid=uuid.uuid5(qid,key)
        choices=[{':answer/id':str(uuid.uuid5(fid,'math:'+normalize_tex(v))),':answer/type':':answer.type/math',':answer/value':normalize_tex(v)} for v in values]
        rng.shuffle(choices)
        fields.append({':answer-field/id':str(fid),':answer-field/key':key,':answer-field/type':':answer-field.type/'+field_kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',str(uuid.uuid5(fid,'math:'+normalize_tex(correct)))]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Word Problems'},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/easy',':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'intersection':[str(t),str(y)],'bank_profile':profile,'source_reference':sq[':question/math-academy-id'],'source_difficulty':sq.get(':question/difficulty'),'source_basis':SOURCE['basis'],'replay':replay,'geometry_attempts':attempts,'plot_assets':assets,'parameter_fingerprint':digest(dict(template=name,parameters=p)),'sympy_version':sp.__version__}}

def batch(level='easy',count=5,seed=0,template=None,output_dir=None):
    if type(count) is not int or count<1 or count>100: raise ValueError('Count must be 1..100')
    result=[];seen=set()
    for i in range(count*50):
        r=generate(level,seed+i,template,output_dir=output_dir)
        key=r['generation']['parameter_fingerprint']
        if key in seen: continue
        seen.add(key);result.append(r)
        if len(result)==count:return result
    raise ValueError('Bounded semantic family exhausted')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--difficulty',default='easy',choices=['easy','moderate','hard'])
    ap.add_argument('--count',default=5,type=int)
    ap.add_argument('--seed',default=0,type=int)
    ap.add_argument('--format',default='json',choices=['json'])
    ap.add_argument('--template',choices=CONTEXTS)
    args=ap.parse_args()
    try: result=batch(args.difficulty,args.count,args.seed,args.template)
    except ValueError as exc:ap.error(str(exc))
    print(json.dumps(result,indent=2))


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186138429-source-policy.json'))

if __name__=='__main__':main()
