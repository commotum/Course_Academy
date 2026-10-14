#!/usr/bin/env python3
"""Identify ONE root's qualitative multiplicity from a graph, math basis 1356.

Source sketches do not determine exact higher exponents. Rendered curves are
representatives of the three observed categories, never equations to recover.
Public raw profiles preserve missing attributes and source five-option banks.
Easy: one local root; authored moderate: two distinct integer roots; authored
hard: three half-integer roots, all three categories. No within-level progression.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid, os, tempfile
from pathlib import Path
import sympy as sp
import numpy as np
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186129253-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

KP_ID=17592186129253
KP_UUID='4d48e2a0-1a76-5eec-a98c-4a7eb16f70cb'
TITLE='Identifying Multiplicity of a Root Given a Graph'
VERSION='root-category-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X=sp.Symbol('x')
SUFFIXES={'simple':'is a simple root','even':'is a multiple root of even multiplicity','odd':'is a multiple root of odd multiplicity','not':'is not a root of $p(x)$','impossible':'is a simple root of even multiplicity'}
# Predicate semantics, including wrong/wrong pairs. The last is contradictory,
# a source-observed misconception, not a second spelling of another category.
SEMANTICS={'simple':frozenset([1]),'even':frozenset(range(2,30,2)),'odd':frozenset(range(3,30,2)),'not':frozenset([0]),'impossible':frozenset()}
SOURCE_DATA={
'q-140411':(3,1,-1), 'q-140414':(-2,2,1),
'q-141133':(-1,3,1), 'q-141137':(-5,3,-1),
'q-141142':(9,3,1), 'q-141144':(6,2,1), 'q-141140':(-3,1,1)}
TEMPLATES={'local-identification':'easy','two-root-identification':'moderate','three-root-identification':'hard'}
PROFILES=['observed-five']+['raw-'+s for s in QUESTIONS]+['completed-'+s for s in QUESTIONS]
DEFAULT_PARAMS={s:{'roots':[r],'multiplicities':[m],'orientation':o,'target':0} for s,(r,m,o) in SOURCE_DATA.items()}
# The shared instructional table/rules are a single stable source backbone.
BASE_SOLUTION=QUESTIONS['q-141133'][':question/worked-solution'].split('\n\nIn our case,')[0]
PROMPT='A part of the graph of a polynomial $p(x)$ is {shown} above. Which of the following statements is true?'

class SampleRejected(ValueError): pass

def stable(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(obj): return hashlib.sha256(stable(obj).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def category(m): return {1:'simple',2:'even',3:'odd'}[m]
def tex(v): return sp.latex(sp.Rational(str(v)))
def fraction(v):
    r=sp.Rational(str(v));return int(r) if r.q==1 else str(r)

def canonical_parameters(p):
    allowed={'roots','multiplicities','orientation','target'}
    if set(p)!=allowed: raise ValueError('Exactly roots, multiplicities, orientation, target are required; amplitude and aliases are unsupported')
    try:
        roots=[sp.Rational(str(v)) for v in p['roots']]
        ms=list(p['multiplicities']);o=p['orientation'];t=p['target']
    except Exception as e: raise ValueError('Invalid exact root parameters') from e
    if not isinstance(t,int) or isinstance(t,bool) or not 0<=t<len(roots): raise ValueError('Invalid target index')
    if o not in (-1,1) or isinstance(o,bool): raise ValueError('Orientation must be -1 or 1')
    if len(ms)!=len(roots) or any(type(m)!=int or m not in (1,2,3) for m in ms): raise ValueError('Representative multiplicities must be 1,2,3 only')
    # Normalize sorting and target by actual root, so reordering input is no task.
    target_root=roots[t]
    if len(set(roots))!=len(roots): raise ValueError('Roots must be distinct')
    pairs=sorted(zip(roots,ms));rs=[r for r,m in pairs]
    return {'roots':[fraction(r) for r in rs],'multiplicities':[m for r,m in pairs], 'orientation':int(o),'target':rs.index(target_root)}

def guard(level,p):
    rs=[sp.Rational(str(v)) for v in p['roots']];ms=p['multiplicities']
    if any(abs(r)>9 for r in rs): raise ValueError('Root magnitude bound is 9')
    if level=='easy':
        if len(rs)!=1 or any(r.q!=1 for r in rs): raise ValueError('Easy is exactly one integer root')
    elif level=='moderate':
        if len(rs)!=2 or any(r.q!=1 or abs(r)>6 for r in rs) or len(set(ms))!=2 or rs[1]-rs[0]<3:
            raise ValueError('Moderate needs two differently classified integer roots in [-6,6], separation >=3')
    elif level=='hard':
        if len(rs)!=3 or any(r.q!=2 or abs(r)>sp.Rational(13,2) for r in rs) or set(ms)!={1,2,3} or min(rs[1]-rs[0],rs[2]-rs[1])<3:
            raise ValueError('Hard needs three strict half-integer roots in [-13/2,13/2], all categories, separation >=3')
    else: raise ValueError('Unsupported difficulty')

def polynomial(p):
    rs=[sp.Rational(str(v)) for v in p['roots']]
    y=sp.Integer(p['orientation'])
    for r,m in zip(rs,p['multiplicities']): y*= (X-r)**m
    # Local simple-source representative has the same monotonic sigmoid cues.
    # Exact unseen source equations are expressly not asserted.
    if len(rs)==1 and p['multiplicities']==[1]:
        y*=1-(X-rs[0])**2/12
    return sp.expand(y)

def option(key,r,style='compact'):
    eq='x='+tex(r)
    if style=='q-140411': eq='x = '+tex(r)
    if style=='q-140414': eq='x ='+tex(r)
    return '$'+eq+'$ '+SUFFIXES[key]

def worked_solution(r,cat):
    rt=tex(r)
    if cat=='simple':
        tail='In our case, the graph is *not* tangent to the $x$-axis at $x='+rt+'.$ Therefore, $x='+rt+'$ is a *simple* root.'
    else:
        action='touches the $x$-axis and reverses direction' if cat=='even' else 'crosses the $x$-axis'
        tail='In our case, the graph is *tangent* to the $x$-axis at $x='+rt+'.$ So, $x='+rt+'$ is a *multiple* root. \n\nFurthermore, the graph '+action+' at $x='+rt+'.$ So, $x='+rt+'$ has *'+cat+'* multiplicity.\n\nTherefore, $x='+rt+'$ is a multiple root of '+cat+' multiplicity.'
    return BASE_SOLUTION+'\n\n'+tail

def atomic_json(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,delete=False,suffix='.json') as f:
        json.dump(value,f,indent=2);tmp=f.name
    os.replace(tmp,path)

def render_plot(p):
    """Overview + root-local panels for cluttered graphs, all the SAME function.

    Zero axes are at mathematical y=0. Per-panel vertical scale is chosen from
    the function's values in that panel, never changing its polynomial. Root
    locations have explicit readable ticks; no artificial tangent label gives
    away the category. Sidecar includes the actual plotted vertices/transform.
    """
    key=digest({'version':VERSION,'parameters':p})
    path=HERE/'plots'/f'{key}.png';side=path.with_suffix('.json')
    if path.exists() and side.exists(): return str(path),json.loads(side.read_text())
    path.parent.mkdir(parents=True,exist_ok=True)
    roots=[sp.Rational(str(r)) for r in p['roots']];poly=polynomial(p)
    fn=sp.lambdify(X,poly,'numpy');n=len(roots)
    fig=plt.figure(figsize=(7.2,3.1 if n==1 else 5.1),dpi=150)
    axes=[fig.add_subplot(111)] if n==1 else [fig.add_subplot(2,1,1),fig.add_subplot(2,1,2)]
    ranges=[(float(roots[0])-2,float(roots[-1])+2)]
    target=roots[p['target']]
    if n>1:ranges.append((float(target)-.85,float(target)+.85))
    panels=[]
    for i,(ax,(lo,hi)) in enumerate(zip(axes,ranges)):
        xs=np.unique(np.concatenate([np.linspace(lo,hi,2601),np.array([float(r) for r in roots if lo<=r<=hi])]))
        ys=fn(xs)
        scale=max(float(np.max(np.abs(ys))),1e-8)
        # Include an actual zero y-axis wherever 0 lies in the shown x-window.
        ax.axhline(0,color='black',lw=1,zorder=1)
        if lo<=0<=hi:ax.axvline(0,color='black',lw=.7,zorder=1)
        ax.plot(xs,ys,color='#e82420',lw=2.15,zorder=3)
        ax.set_xlim(lo,hi);ax.set_ylim(-scale*1.18,scale*1.18)
        ax.set_yticks([])
        ticks=[r for r in roots if lo<=r<=hi]
        if lo<=0<=hi and 0 not in ticks: ticks.append(sp.Integer(0))
        ticks=sorted(ticks)
        ax.set_xticks([float(r) for r in ticks],[f'${tex(r)}$' for r in ticks],fontsize=12)
        ax.spines['bottom'].set_position(('data',0))
        for pos in ['left','top','right']:ax.spines[pos].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='x',length=4,pad=6)
        ax.text(hi,0,'  $x$',ha='left',va='center',fontsize=12)
        ax.annotate('',xy=(hi,0),xytext=(hi-(hi-lo)*.045,0),arrowprops={'arrowstyle':'->','color':'black','lw':1})
        if n>1:ax.set_title('Graph' if i==0 else 'Enlarged view near $x='+tex(target)+'$',fontsize=11,pad=8)
        panels.append({'xlim':[lo,hi],'ylim':[-scale*1.18,scale*1.18],'ticks':[str(r) for r in ticks], 'vertices':[[float(x),float(y)] for x,y in zip(xs,ys)],'role':'overview' if i==0 else 'target-local'})
    fig.tight_layout(pad=1.6,h_pad=2)
    fig.canvas.draw()
    for ax,panel in zip(axes,panels):panel['axes_pixel_bounds']=list(map(float,ax.bbox.bounds));panel['zero_pixel_y']=float(ax.transData.transform((0,0))[1])
    with tempfile.NamedTemporaryFile(dir=path.parent,suffix='.png',delete=False) as f:tmp=f.name
    fig.savefig(tmp,facecolor='white');plt.close(fig);os.replace(tmp,path)
    meta={'renderer':'Matplotlib','version':matplotlib.__version__,'python':sys.version.split()[0], 'parameters':p,'polynomial':str(poly),'panels':panels,'png_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    atomic_json(side,meta)
    return str(path),meta

def sample(level,rng):
    if level=='easy':return {'roots':[rng.randint(-9,9)],'multiplicities':[rng.choice([1,2,3])],'orientation':rng.choice([-1,1]),'target':0}
    n=2 if level=='moderate' else 3
    pool=list(range(-6,7)) if level=='moderate' else [str(sp.Rational(k,2)) for k in range(-13,14,2)]
    for _ in range(100):
        roots=sorted(rng.sample(pool,n),key=lambda r:sp.Rational(str(r)))
        if min(sp.Rational(str(roots[i+1]))-sp.Rational(str(roots[i])) for i in range(n-1))<3:continue
        ms=rng.sample([1,2,3],n)
        return {'roots':roots,'multiplicities':ms,'orientation':rng.choice([-1,1]),'target':rng.randrange(n)}
    raise SampleRejected('No well-separated roots')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    if field_type not in (None,'radio'):raise ValueError('Only observed radio fields are supported')
    template=template or next(k for k,v in TEMPLATES.items() if v==level)
    if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('Template/level mismatch')
    # Select the WHOLE eligible bank before sampling parameters. Every bank is
    # the same observed five distinct predicates, with original notation style.
    profile=profile or 'observed-five'
    if profile not in PROFILES:raise ValueError('Unknown profile')
    source_id=profile.split('-',1)[1] if profile.startswith(('raw-','completed-')) else None
    if source_id and level!='easy':raise ValueError('Source profiles retain local easy workload')
    rng=random.Random(seed)
    if parameters is None and source_id:parameters=DEFAULT_PARAMS[source_id]
    p=canonical_parameters(parameters if parameters is not None else sample(level,rng));guard(level,p)
    if source_id and category(p['multiplicities'][0])!=category(SOURCE_DATA[source_id][1]):raise ValueError('Observed profile preserves its operative solution category')
    target=sp.Rational(str(p['roots'][p['target']]));cat=category(p['multiplicities'][p['target']])
    correct_value=option(cat,target,source_id)
    keys=[cat]+[k for k in SUFFIXES if k!=cat]
    # Source replay has exactly the original full bank; no repair or pool fill.
    vals=[option(k,target,source_id) for k in keys]
    if len({SEMANTICS[k] for k in keys})!=5:raise SampleRejected('Complete bank semantic collision')
    original=QUESTIONS.get(source_id,{})
    anchor=bool(source_id and p==canonical_parameters(DEFAULT_PARAMS[source_id]))
    asset_meta=None
    if anchor:asset=re.search(r'!\[\]\((.*?)\)',original[':question/problem']).group(1)
    else:asset,asset_meta=render_plot(p)
    shown='shown' if source_id in ('q-140414','q-141144') else 'given'
    prompt='![]('+asset+')\n\n'+PROMPT.format(shown=shown)
    solution=worked_solution(target,cat)
    raw=profile.startswith('raw-')
    presence={'difficulty':not raw or ':question/difficulty' in original,'solution':not raw or ':question/worked-solution' in original, 'correct':not raw or ':answer-field/correct' in original.get(':question/answer-fields',[{}])[0]}
    payload={'version':VERSION,'level':level if presence['difficulty'] else None,'prompt':prompt,'solution':solution if presence['solution'] else None,'bank':sorted(vals),'correct':correct_value if presence['correct'] else None}
    content=digest(payload);qid=uid(content);fid=uid(content+'/selection')
    answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/text',':answer/value':v} for v in vals]
    random.Random(seed).shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if presence['correct']:field[':answer-field/correct']=[':answer/id',uid(fid+'/'+correct_value)]
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if presence['difficulty']:q[':question/difficulty']=':question.difficulty/'+level
    if presence['solution']:q[':question/worked-solution']=solution
    # Assessed graphical geometry matters: root labels, category, orientation,
    # visible root configuration and information/workload. Positive scale is
    # absent; bank/profile/seed/notation and source IDs are excluded.
    task=digest({'parameters':p,'workload':len(p['roots'])})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'parameter_fingerprint':task,'mathematical_task_fingerprint':task,'content_fingerprint':content,'source_analysis':{'database':'math','basis':1356,'lineage':SOURCE['lineage'],'question_ids':[source_id] if source_id else list(QUESTIONS)},'authored_extension':level!='easy','evidence_only':raw,'eligible_for_learning':not raw,'inferred_completion':bool(source_id and not raw and not presence.get('raw',False) and ':question/difficulty' not in original),'plot_rating':'heavy','plot_assets':{'prompt':asset},'plot_data':asset_meta,'category':cat,'answer_predicates':{v:k for v,k in zip(vals,keys)},'renderer_version':matplotlib.__version__,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'source_anchor':anchor,'higher_exponent_claimed':False}}

# EASY — observed single-root categorical identification; integer target.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Observed simple/even-multiple/odd-multiple local graph workload."""
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE — authored two differently classified integer roots; one target.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Select the named root among two integer intercepts, classify locally."""
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD — authored three strict half-integer roots/all categories; one target.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    """Read a half-integer target among three intercepts, classify locally."""
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(rec):
    q=rec['question'];g=rec['generation'];f=q[':question/answer-fields'][0]
    content=q[':question/problem']
    # Review-only path resolution does not change public raw source strings.
    content=re.sub(r'!\[\]\(images/[^/]+/([^)]*)\)',lambda m:'![]('+str(HERE/'originals'/m.group(1))+')',content)
    lines=['## '+q.get(':question/difficulty','Unrated raw evidence').split('/')[-1],f"Template `{g['template']}`, profile `{g['bank_profile']}`; parameters `{stable(g['parameters'])}`.",'',content,'']
    for a in f[':answer-field/choices']:lines.append('- '+a[':answer/value'])
    if ':answer-field/correct' in f:
        lines+=['','Correct: '+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])]
    if ':question/worked-solution' in q:
        sol=re.sub(r'!\[\]\(images/[^/]+/([^)]*)\)',lambda m:'![]('+str(HERE/'originals'/m.group(1))+')',q[':question/worked-solution'])
        lines+=['','Worked solution','',sol]
    return '\n'.join(lines)

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template',choices=list(TEMPLATES));a.add_argument('--profile',choices=PROFILES);args=a.parse_args()
    if args.count<1:a.error('Count must be positive')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    if args.difficulty=='all' and (args.template or args.profile):a.error('Choose a specific level for explicit template/profile')
    records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
