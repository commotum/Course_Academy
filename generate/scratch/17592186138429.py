#!/usr/bin/env python3
"""Word Problems — graph-intersection contextual reading, math basis 1356.

Two unrated practice sources have full five-choice banks but no correct refs or
worked solutions. Correct refs are independently derived; solutions are authored
from e-13130's intersection → annotated graph → point → contextual x sequence.
All level assignments are authored, not recovered labels. See adjacent evidence.
Observed scalar bank interpretations remain unknown; explicit ratio profiles are
replay expressions only. Normal banks are complete authored adjacent-grid-line
misreadings, never a first-valid distractor pool. Stop at generator/plot step 7.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, subprocess, tempfile, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186138429
KP_UUID='4154d81b-c94a-57f7-80fa-0daa341505e6'
VERSION='word-graphs-5'
HERE=Path(__file__).resolve().parent/str(KP_ID)
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
TEMPLATES={'trucks':'easy','pools':'moderate','cars':'hard'}
PROMPTS={
 'cars':'The graph above shows the speed of cars $A$ and $B$ as a function of the distance that they traveled during a brake test. At which distance, in meters, did both cars reach the same speed?',
 'trucks':'Two trucks, Truck $A$ and Truck $B$, are carrying shipments between distribution centers. The graph above shows the distances (in miles) of Truck $A$ and Truck $B$ from one of the centers as a function of time (in hours). At what time are Truck $A$ and Truck $B$ the same distance from the center?',
 'pools':'The graph above shows the number of liters of water in pool $A$ and pool $B$ as a function of time, measured in days. How many days will it take for both pools to contain the same amount of water?'}
CONFIG={'cars':{'x_label':'Distance (m)','y_label':'Speed (km/h)','labels':['Car A','Car B']},'trucks':{'x_label':'Hours','y_label':'Miles','labels':['Truck A','Truck B']},'pools':{'x_label':'Days','y_label':'Liters','labels':['Pool A','Pool B']}}
PROFILES={'adjacent_grid':'authored','observed_car_ratios':'observed expression profile; intent unknown','observed_truck_ratios':'observed expression profile; intent unknown'}
SOURCE_PARAMETERS={
 'cars':{'a0':80,'a1':'-3/4','b0':40,'b1':'-1/4','xmax':100,'dx':10,'ymax':90,'dy':10,'ylabel_step':20,'xlabel_step':10},
 'trucks':{'a0':0,'a1':50,'b0':750,'b1':-75,'xmax':7,'dx':1,'ymax':900,'dy':100,'ylabel_step':200,'xlabel_step':1},
 'pools':{'a0':150,'a1':50,'b0':775,'b1':-75,'xmax':7,'dx':1,'ymax':900,'dy':100,'ylabel_step':200,'xlabel_step':1}}
ORIGINAL_ASSETS={
 'cars':'images/0d/0d5e3ef2393a00fc74c91ebc44f71d553e641d0e1bca21bf783252cbafcca84c.png',
 'trucks':'images/b9/b91b1093a485c671cb5e7566498a1e2b95452d9b92ea87e478696ff8c9ace0ff.png',
 'pools':'images/09/0915c99015922e27855d92ebb13756da634a8f10dd8fe3abbc016590f06e1077.png'}

def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def normalize(p):
    if set(p)!=set(SOURCE_PARAMETERS['cars']): raise ValueError('Exact parameter keys required')
    try: q={k:sp.Rational(v) for k,v in p.items()}
    except (TypeError,ValueError) as e: raise ValueError('Rational parameters required') from e
    return {k:int(v) if v.q==1 else str(v) for k,v in q.items()}
def derive(p):
    a0,a1,b0,b1=[sp.Rational(p[k]) for k in ('a0','a1','b0','b1')]
    if a1==b1: raise ValueError('Unique intersection required')
    t=(b0-a0)/(a1-b1); y=a0+a1*t
    return t,y

def guard(name,p,profile):
    r={k:sp.Rational(v) for k,v in p.items()}; t,y=derive(p)
    if any(r[k]<=0 for k in ('xmax','dx','ymax','dy','ylabel_step','xlabel_step')): raise ValueError('Positive scales required')
    if any(r[k].q!=1 for k in ('a0','b0','xmax','dx','ymax','dy','ylabel_step','xlabel_step')): raise ValueError('Integer contextual scales/intercepts required')
    if t.q!=1 or y.q!=1 or not 0<t<r['xmax'] or not 0<y<r['ymax']: raise ValueError('Positive integer intersection on graph required')
    if t%r['dx'] or y%r['dy']: raise ValueError('Intersection must lie on grid')
    if any(v<0 or v>=r['ymax'] for v in (r['a0'],r['b0'])): raise ValueError('Visible nonnegative initial values required')
    if any(not 0<=r[k+'0']+r[k+'1']*r['xmax']<r['ymax'] for k in ('a','b')): raise ValueError('Entire contextual segments must be nonnegative and visible')
    if r['xlabel_step']%r['dx'] or r['ylabel_step']%r['dy'] or r['xmax']%r['dx'] or r['ymax']%r['dy']: raise ValueError('Integral grids required')
    if name=='trucks':
        if not r['a0']==0 or r['a1'] not in (25,50,75,100) or r['b1'] not in (-25,-50,-75,-100) or r['dx']!=1 or r['dy']!=100 or not 3<=t<=9: raise ValueError('Easy truck scope: integer hours, 25–100 mile/hour slopes')
    elif name=='pools':
        if not 50<=r['a0']<=200 or r['a1'] not in (25,50,75) or r['b1'] not in (-50,-75,-100) or r['dx']!=1 or r['dy']!=100 or not 3<=t<=9: raise ValueError('Moderate pool scope: integer days, nonzero starting amount')
    else:
        if not r['a1']<r['b1']<0 or r['a1'] not in (sp.Rational(-1,2),sp.Rational(-3,4),-1) or r['b1'] not in (sp.Rational(-1,4),sp.Rational(-1,2)) or r['dx']!=10 or r['dy']!=10 or not 30<=t<=100: raise ValueError('Hard car scope: ten-meter grid, two decreasing speeds')
    if profile=='observed_car_ratios' and name!='cars' or profile=='observed_truck_ratios' and name!='trucks': raise ValueError('Profile belongs to another context')
    original=p==normalize(SOURCE_PARAMETERS[name])
    if not original and profile=='adjacent_grid':
        expected={'trucks':1,'pools':2,'cars':20}[name]
        if r['xlabel_step']!=expected: raise ValueError('Authored horizontal-label workload violated')
        if name!='trucks' and t%r['xlabel_step']!=r['dx']: raise ValueError('Authored intersection must be between numbered horizontal ticks')
    vals=bank(p,profile)
    if len(set(vals))!=5 or any(v.q!=1 or not 0<v<=r['xmax'] for v in vals): raise ValueError('Whole bank rejected: noninteger, impossible, or equivalent option')
    return t,y

def bank(p,profile):
    t,y=derive(p); dx=sp.Rational(p['dx'])
    if profile=='adjacent_grid': return [t,t-2*dx,t-dx,t+dx,t+2*dx]
    if profile=='observed_car_ratios': return [t/2,3*t/8,3*t/16,t,t/4]
    if profile=='observed_truck_ratios': return [t/2,t,5*t/6,t/3,2*t/3]
    raise ValueError('Unknown complete profile')

def sample(name,rng):
    for _ in range(1000):
        if name=='cars':
            t=rng.choice(range(30,100,20)); y=rng.choice(range(30,81,10)); a1=rng.choice(['-1/2','-3/4','-1']); b1=rng.choice(['-1/4','-1/2']); a0=y-sp.Rational(a1)*t;b0=y-sp.Rational(b1)*t
            xmax=t+30;dx=10;dy=10;yl=20
        else:
            t=rng.choice([3,5,7,9]) if name=='pools' else rng.randint(3,9); a1=rng.choice([25,50,75] if name=='pools' else [25,50,75,100]);b1=rng.choice([-50,-75,-100] if name=='pools' else [-25,-50,-75,-100]);a0=rng.choice([50,100,150,200]) if name=='pools' else 0
            y=a0+a1*t; b0=y-b1*t;xmax=t+3;dx=1;dy=100;yl=200
        top=max(a0,b0,a0+sp.Rational(a1)*xmax,b0+sp.Rational(b1)*xmax)
        ymax=(math.floor(top/dy)+2)*dy
        p=normalize(dict(a0=a0,a1=a1,b0=b0,b1=b1,xmax=xmax,dx=dx,ymax=ymax,dy=dy,ylabel_step=yl,xlabel_step={'cars':20,'pools':2,'trucks':1}[name]))
        try: guard(name,p,'adjacent_grid')
        except ValueError: continue
        return p
    raise ValueError('No eligible complete instance')

def render_plots(name,p):
    """One immutable geometry per call; unique inputs and atomic PNG+sidecar writes."""
    original=normalize(SOURCE_PARAMETERS[name])==p
    spec={'template':name,'parameters':p,'labels':CONFIG[name], 'intersection':[str(v) for v in derive(p)]}
    result={}
    for role in ('prompt','solution'):
        if original and role=='prompt':
            path=HERE/ORIGINAL_ASSETS[name]
            if not path.exists(): raise ValueError('Missing captured source asset')
            result[role]={'path':str(path),'reference':ORIGINAL_ASSETS[name],'geometry':spec,'renderer':'captured PNG'}
            continue
        data={**spec,'annotated':role=='solution'}
        filename='images/generated/'+digest(data)+'.png'; path=HERE/filename; side=path.with_suffix('.json')
        revision='wordgraphs5' if name in ('planes','tanks') else 'wordgraphs4'
        if not path.exists() or not side.exists() or json.loads(side.read_text()).get('renderer_revision')!=revision:
            path.parent.mkdir(parents=True,exist_ok=True)
            with tempfile.NamedTemporaryFile(mode='w',suffix='.json',dir=HERE,delete=False) as f:
                json.dump({'spec':data,'output':str(path)},f); tmp=Path(f.name)
            try: subprocess.run([str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),str(HERE/'render.py'),str(tmp)],check=True,capture_output=True,text=True)
            finally: tmp.unlink(missing_ok=True)
        result[role]={'path':str(path),'reference':filename,'sidecar':str(side),'geometry':spec,'renderer':'Matplotlib'}
    return result

def solution(name,p,assets):
    t,y=derive(p); graph='![]('+assets['solution']['reference']+')'
    if name=='pools': return 'The pools have the same amount of water when the two graphs intersect.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y})$. So, both pools have the same amount (${y}\\,\\textrm{{L}}$) of water at $t={t}$ days.'
    if name=='cars': return 'The cars have the same speed when the two graphs intersect.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y})$. So, both cars have the same speed (${y}\\,\\textrm{{km/h}}$) at a distance of ${t}$ meters.'
    return 'The trucks are the same distance from the center when the two graphs intersect.\n\n'+graph+f'\n\nIn this case, we have the point $({t},{y})$. So, both trucks are the same distance (${y}\\,\\textrm{{miles}}$) from the center at $t={t}$ hours.'

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if template in ('planes','tanks'):
        from importlib.util import spec_from_file_location, module_from_spec
        spec=spec_from_file_location('wordgraphs_extra',HERE/'extensions.py'); extra=module_from_spec(spec);spec.loader.exec_module(extra)
        return extra.generate(globals(),level,seed,template,field_type,parameters,profile)
    if level not in ('easy','moderate','hard'): raise ValueError('Unknown level')
    name=template or next(k for k,v in TEMPLATES.items() if v==level)
    if name not in TEMPLATES or TEMPLATES[name]!=level: raise ValueError('Template/level mismatch')
    if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only observed radio layout supported')
    profile=profile or 'adjacent_grid'
    if profile not in PROFILES: raise ValueError('Unknown complete profile')
    rng=random.Random(seed)
    if parameters is not None: p=normalize(parameters)
    elif profile!='adjacent_grid': p=normalize(SOURCE_PARAMETERS[name])
    else: p=sample(name,rng)
    t,y=guard(name,p,profile); vals=bank(p,profile); assets=render_plots(name,p)
    prompt='![]('+assets['prompt']['reference']+')\n\n'+PROMPTS[name]
    worked=solution(name,p,assets)
    values=[str(v)+('h' if name=='trucks' else '') for v in vals]
    content=digest({'version':VERSION,'prompt':prompt,'solution':worked,'bank':sorted(values)})
    qid=uuid.uuid5(uuid.NAMESPACE_URL,KP_UUID+'/'+content);fid=uuid.uuid5(qid,'selection')
    choices=[{':answer/id':str(uuid.uuid5(fid,'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    correct=str(uuid.uuid5(fid,'math:'+str(t)+('h' if name=='trucks' else '')))
    rng.shuffle(choices)
    fingerprint=digest({'context':name,'lines':[[p['a0'],p['a1']],[p['b0'],p['b1']]],'response':'horizontal coordinate','horizontal_grid':[p['dx'],p['xlabel_step']]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Word Problems'},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':PROFILES[profile],'level_origin':'authored; both practice sources unrated','solution_origin':'authored canonical-method adaptation' if name!='pools' else 'canonical-example parameterization','source_analysis':SOURCE,'parameter_fingerprint':fingerprint,'content_fingerprint':content,'domain':'Positive integer contextual horizontal-coordinate choices; nonnegative visible contextual lines','plot_rating':'moderate','plot_assets':assets,'recipe_operations':(['correct horizontal intersection','two gridlines left','one gridline left','one gridline right','two gridlines right'] if profile=='adjacent_grid' else 'Observed complete ratio-expression profile; wrong intent unknown'),'sympy_version':sp.__version__}}

# EASY — authored integer-hour trucks; one x-coordinate read, five radio choices.
# 3–9 h intersection on directly numbered unit-hour ticks; 25–100 mile/hour
# linear rates, 100-mile vertical grid. Source placement is authored, unrated.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Read directly numbered integer-hour ticks, t=3–9; preserve literal h."""
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE — authored canonical pools context; positive initial volume in both
# pools, odd 3–9 integer days between numbered two-day ticks, unit-day minor
# grid, 100-liter vertical grid. Same contextual horizontal-coordinate reading.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Read odd 3–9 days between numbered two-day ticks, unit-day minor grid."""
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD — authored car context: 30/50/70/90 m between numbered twenty-meter
# ticks with ten-meter minor grid, 10 km/h vertical grid. This familiar nonunit
# scale is the added reading workload; no algebra or graph crowding. Slopes are
# A in {-1/2,-3/4,-1}, B in {-1/4,-1/2}, A<B<0, with visible positive speed.
# Unrated source (80 m, numbered ten-meter ticks) receives a fidelity-only hard
# placement and does not establish the authored default workload or rating.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Read 30/50/70/90 m between twenty-meter ticks, ten-meter minor grid."""
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q=r['question']; f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join(f'- ${a[":answer/value"]}$' for a in f[':answer-field/choices'])+'\n\n**Worked solution**\n\n'+q[':question/worked-solution']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile'); args=ap.parse_args()
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
