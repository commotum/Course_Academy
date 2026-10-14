#!/usr/bin/env python3
"""Identifying vector scalar relations from one equal-square grid (steps 3–7).

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), plus three level entrypoints. Source snapshot: math basis 1356.
Source practice is unrated and lacks solutions/correct refs. Public raw-a/raw-b
profiles faithfully preserve those omissions, are evidence-only, and parameterize
both statements and plotted geometry. Completed source-shaped profiles add an
independently inferred key and an authored solution. No literal payload replay.

Easy: three signed unit relations in the opposite-multiple mask, axis/45-degree directions. Moderate: three
relations including a factor 2 or 1/2, integer endpoints and oblique directions.
Hard: identical operation with factor 3/2 or 2/3, integer-grid 3:2 lengths.
These are authored workload bounds, not recovered source difficulty labels.
Positive/negative multipliers are both parallel in the actual lesson. The zero
vector is parallel to every vector there; zero arrows are excluded because this
KP assesses arrow direction and magnitude rather than that later convention.
Translations do not change a vector. Only requested vectors enter task dedupe.

Five-choice banks are complete profiles, chosen before parameters. The observed
subset catalogs are preserved verbatim. Unit reciprocal questions have a labeled
authored bank of the true subset plus four complete selection-error operations:
toggle I, toggle II, toggle III, toggle I and III. Reject a whole instance when
an observed catalog does not contain its true subset. No random wrong values.
Raw source figures are reused only at independently raster-verified geometry;
changed geometry always calls the fixed Matplotlib renderer. Stable content UUIDs
include actual presentation, bank, solution and level, excluding choice order;
canonical mathematical fingerprints exclude banks, translations and unused arrows.
No EDB writes, registration, shared edits, installations, or image models.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, random, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().with_suffix('')
KP_ID=17592186096700
KP_UUID='dc5bab6c-1ce7-58b5-a59d-cff2ce35ecca'
TITLE='Identifying Parallel Vectors From a Diagram'
VERSION='parallel-diagram-2'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
RUNTIME='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
TEMPLATES=('opposite_multiple','reciprocal_multiple')
CATALOG_A=('I only','II and III only','I and III only','I and II only','III only')
CATALOG_B=('I only','II and III only','III only','II only','I and III only')
PROFILES={'raw-a':(TEMPLATES[0],'raw'),'raw-b':(TEMPLATES[1],'raw'),
          'observed-a-completed':(TEMPLATES[0],'completed'),
          'observed-b-completed':(TEMPLATES[1],'completed'),
          'authored-selection-flips':(None,'authored')}
ROMAN=('I','II','III')
SOURCE_CASES=json.loads((HERE/'source-cases.json').read_text())
ASSET_REFS={x['source_id']:q[':question/problem'].split('![](',1)[1].split(')',1)[0]
 for x,q in zip(SOURCE_CASES,json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions'])}

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'))
def digest(value):return hashlib.sha256(canonical(value).encode()).hexdigest()
def file_hash(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def owned(parent,value):return str(uuid.uuid5(uuid.UUID(parent),canonical(value)))
def rat(value):
    if isinstance(value,float):raise ValueError('Use exact integer/rational strings, not floats')
    r=sp.Rational(value)
    if abs(r)>12:raise ValueError('Parameter outside supported plot workload')
    return r

def tex_factor(k):
    k=sp.Rational(k)
    if k==1:return ''
    if k==-1:return '-'
    if k.q==1:return str(k)
    sign='-' if k<0 else ''
    return sign+r'\frac{'+str(abs(k.p))+'}{'+str(k.q)+'}'

def statement_tex(lhs,k,rhs,template,index):
    # Complete statement slots; source whitespace is deliberately retained.
    f=tex_factor(k)
    if template==TEMPLATES[0]:
        return lhs+(' ='+f+rhs if index<2 else ' = '+f+rhs)
    return lhs+(' ='+f+rhs if index<2 else ' = '+f+rhs)

def subset_text(indices):
    names=[ROMAN[i] for i in sorted(indices)]
    if not names:return 'None of the statements'
    if len(names)==3:return 'I, II and III'
    return ' and '.join(names)+' only'

def parse_subset(text):
    if text=='None of the statements':return frozenset()
    if text=='I, II and III':return frozenset(range(3))
    if not text.endswith(' only'):raise ValueError('Unknown subset text')
    return frozenset(ROMAN.index(x) for x in text[:-5].split(' and '))

def normalize_parameters(level,template,p,raw=False):
    if not isinstance(p,dict) or set(p)-{'u','v','k','s','t','tails'}:raise ValueError('Unknown parameters')
    if not {'u','v','k','s','t'}<=set(p):raise ValueError('Missing parameters')
    q={x:[rat(v) for v in p[x]] for x in ('u','v')}
    if any(len(q[x])!=2 or all(v==0 for v in q[x]) for x in q):raise ValueError('Nonzero 2D vectors required')
    q.update(k=rat(p['k']),s=p['s'],t=p['t'])
    if type(q['s']) is not int or type(q['t']) is not int or q['s'] not in (-1,1) or q['t'] not in (-1,1):raise ValueError('s/t must be signs')
    if q['u'][0]*q['v'][1]==q['u'][1]*q['v'][0]:raise ValueError('Distinct direction families required')
    if raw:
        if q['k']!=2 or max(abs(x) for x in q['u'])>3 or max(abs(x) for x in q['v'])>5:raise ValueError('Raw profile geometry bounds')
    elif level=='easy':
        if q['k']!=1:raise ValueError('Easy requires signed unit relations')
        for vector in (q['u'],q['v']):
            if any(x.q!=1 or abs(x)>2 for x in vector) or (all(vector) and abs(vector[0])!=abs(vector[1])):raise ValueError('Easy axis/45-degree bounds')
    elif level=='moderate':
        if q['k']!=2:raise ValueError('Moderate requires factor two')
        if any(x.q!=1 or abs(x)>3 for x in q['u']) or any(x.q!=1 or abs(x)>5 for x in q['v']):raise ValueError('Moderate integer endpoint bounds')
        if not all(q['u']) or abs(q['u'][0])==abs(q['u'][1]):raise ValueError('Moderate requires oblique unequal components')
    elif level=='hard':
        if q['k'] not in (sp.Rational(3,2),sp.Rational(2,3)):raise ValueError('Hard requires 3:2 or 2:3 ratios')
        if any(x.q!=1 or abs(x)>6 for x in q['u']+q['v']) or any((q['k']*x).q!=1 for x in q['u']):raise ValueError('Hard integer-grid 3:2 bounds')
        if not all(q['u']) or abs(q['u'][0])==abs(q['u'][1]):raise ValueError('Hard requires oblique unequal components')
    else:raise ValueError('Unknown level')
    if max(abs(q['k']*x) for x in q['u'])>6:raise ValueError('Scaled displacement exceeds six squares')
    if 'tails' in p:
        if set(p['tails'])!=set('abcde'):raise ValueError('Five vector tails required')
        q['tails']={x:[sp.Rational(v) for v in p['tails'][x]] for x in 'abcde'}
        if any(isinstance(v,float) or abs(sp.Rational(v))>48 or sp.Rational(v).q!=1 for tail in p['tails'].values() for v in tail):raise ValueError('Tail coordinates must be bounded integer grid points')
        if any(len(t)!=2 for t in q['tails'].values()):raise ValueError('Invalid tail')
    return q

def primitive(v):
    den=sp.ilcm(*[x.q for x in v]); ints=[int(x*den) for x in v]
    g=math.gcd(*ints)
    return [x//g for x in ints]

def vectors_and_statements(template,p):
    u,v,k,s,t=p['u'],p['v'],p['k'],p['s'],p['t']
    scale=lambda v,c:[sp.Rational(c)*x for x in v]
    if template==TEMPLATES[0]:
        vs=dict(a=scale(u,k),b=scale(u,s*k),c=v,d=scale(v,t),e=u)
        st=[('b',-k,'e'),('c',sp.Rational(-1),'d'),('b',k,'e')]
    else:
        vs=dict(a=scale(u,k),b=v,c=scale(u,s),d=scale(v,t),e=[sp.Integer(-4),sp.Integer(0)])
        st=[('a',sp.Rational(-1),'c'),('c',-1/k,'a'),('b',sp.Rational(1),'d')]
    return vs,st

def truth_set(vs,st):
    return frozenset(i for i,(a,k,b) in enumerate(st) if all(vs[a][j]==k*vs[b][j] for j in (0,1)))

def bank_values(profile,true):
    if profile.endswith('a') or profile=='observed-a-completed':values=list(CATALOG_A)
    elif profile.endswith('b') or profile=='observed-b-completed':values=list(CATALOG_B)
    else:
        values=[subset_text(true^frozenset(toggle)) for toggle in ((),(0,),(1,),(2,),(0,2))]
    sets=[parse_subset(x) for x in values]
    if len(sets)!=5 or len(set(sets))!=5 or sets.count(true)!=1:raise ValueError('Whole bank rejected: response ambiguity or missing correct subset')
    return values

def plot_geometry(vs,p):
    centers={'a':[5,4],'b':[14,4],'c':[23,4],'d':[5,13],'e':[14,13]}
    tails=p.get('tails',{x:[sp.floor(sp.Rational(centers[x][i])-vs[x][i]/2) for i in (0,1)] for x in vs})
    return {x:{'tail':[str(y) for y in tails[x]],'tip':[str(tails[x][i]+vs[x][i]) for i in (0,1)]} for x in 'abcde'}

def serialize_parameters(p):
    return {k:({a:[str(v) for v in b] for a,b in val.items()} if k=='tails' else [str(x) for x in val] if k in ('u','v') else str(val) if k=='k' else val) for k,val in p.items()}

def match_original(template,p):
    for c in SOURCE_CASES:
        if c['template']==template and serialize_parameters(p)==serialize_parameters(normalize_parameters('moderate',template,c['parameters'],True)):return c
    return None

def render_plots(geometry,force=False):
    """Fixed runtime/renderer; isolated inputs, atomic assets, verified cache sidecars."""
    config={'geometry':geometry,'renderer_sha256':file_hash(HERE/'render_plot.py'),'dependency_lock_sha256':file_hash(HERE/'dependency-lock.json'),'runtime_sha256':file_hash(RUNTIME)}
    key=digest(config);target=HERE/'plots'/f'{key}.png';side=target.with_suffix('.json')
    if not force and target.exists() and side.exists():
        meta=json.loads(side.read_text())
        if meta.get('config')==config and meta.get('png_sha256')==file_hash(target):return str(target),meta
    target.parent.mkdir(exist_ok=True)
    fd,name=tempfile.mkstemp(prefix='.render-',suffix='.json',dir=target.parent)
    try:
        with os.fdopen(fd,'w') as f:json.dump({'config':config,'output':str(target)},f)
        result=subprocess.run([RUNTIME,str(HERE/'render_plot.py'),name],capture_output=True,text=True)
        if result.returncode:raise RuntimeError('Renderer failed: '+result.stderr)
    finally:Path(name).unlink(missing_ok=True)
    return str(target),json.loads(side.read_text())

def solution(template,vs,st,true):
    lines=[]
    for i,(a,k,b) in enumerate(st):
        expr=statement_tex(a,k,b,template,i).replace(' ','')
        direction='the same direction' if sum(vs[a][j]*vs[b][j] for j in (0,1))>0 else 'opposite directions'
        norm=lambda v:sp.sqrt(sum(x*x for x in v))
        ratio=sp.simplify(norm(vs[a])/norm(vs[b])); ratio_tex=sp.latex(ratio)
        if i in true:
            wording=f'Indeed, vectors ${b}$ and ${a}$ are parallel and have {direction}. Also, the magnitude of ${a}$ is ${ratio_tex}$ times the magnitude of ${b}$. So, ${expr}$.'
        elif ratio!=abs(k):
            wording=f'The magnitude of ${a}$ is ${ratio_tex}$ times the magnitude of ${b}$. So, ${expr.replace("=",r"\neq")}$.'
        else:
            wording=f'The vectors ${a}$ and ${b}$ have {direction}. So, ${expr.replace("=",r"\neq")}$.'
        lines.append(f'- Statement {ROMAN[i]} is {"true" if i in true else "false"}. '+wording)
    phrase=subset_text(true)
    if not true:conclusion='Therefore, none of the statements are true.'
    elif len(true)==3:conclusion='Therefore, all three statements are true.'
    elif len(true)==1:conclusion=f'Therefore, only statement {ROMAN[next(iter(true))]} is true.'
    else:conclusion='Therefore, only statements '+' and '.join(ROMAN[i] for i in sorted(true))+' are true.'
    return '\n'.join(lines)+'\n\n'+conclusion

# Easy: equality/opposite direction only; opposite-multiple mask, three statements.
# Moderate: factor two/reciprocal, whole-grid oblique displacements, both masks.
# Hard: 3:2/2:3 comparison, same direction/length operation, both masks.
def sample(level,template,rng):
    if level=='easy':
        ds=[(1,0),(0,1),(1,1),(1,-1),(-1,0),(0,-1),(-1,-1),(-1,1)]
        k=sp.Integer(1);u=rng.choice(ds);u=[2*x for x in u];v=[2*x for x in rng.choice(ds)]
    else:
        dirs=[(1,2),(2,1),(1,-2),(2,-1),(-1,2),(-2,1),(-1,-2),(-2,-1),(2,3),(3,2),(2,-3),(3,-2),(-2,3),(-3,2),(-2,-3),(-3,-2)]
        if level=='moderate':k=sp.Integer(2);u=list(rng.choice(dirs))
        else:
            k=rng.choice((sp.Rational(3,2),sp.Rational(2,3)));d=rng.choice(dirs[:8]);u=[(2 if k==sp.Rational(3,2) else 3)*x for x in d]
        v=list(rng.choice(dirs+[(2,5),(5,2),(-3,-5),(3,5),(0,3),(3,0)]))
    return {'u':u,'v':v,'k':str(k),'s':rng.choice((-1,1)),'t':rng.choice((-1,1))}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio supported')
    if profile is not None and profile not in PROFILES:raise ValueError('Unknown profile')
    rng=random.Random(seed)
    if template is None:template=(PROFILES[profile][0] if profile and PROFILES[profile][0] else rng.choice(TEMPLATES[:1] if level=='easy' else TEMPLATES))
    if template not in TEMPLATES:raise ValueError('Unknown template')
    if level=='easy' and template==TEMPLATES[1] and not (profile and PROFILES[profile][1]=='raw'):raise ValueError('Unit reciprocal mask duplicates a relation; easy supports opposite_multiple')
    if profile is None:profile='authored-selection-flips' if level=='easy' and template==TEMPLATES[1] else ('observed-a-completed' if template==TEMPLATES[0] else 'observed-b-completed')
    if PROFILES[profile][0] not in (None,template):raise ValueError('Profile incompatible with template')
    raw=PROFILES[profile][1]=='raw'
    if raw and parameters is None:raise ValueError('Raw evidence requires explicit parameters')
    for _ in range(2000):
        try:
            p=normalize_parameters(level,template,parameters if parameters is not None else sample(level,template,rng),raw)
            vs,st=vectors_and_statements(template,p);true=truth_set(vs,st);values=bank_values(profile,true)
            geometry=plot_geometry(vs,p)
            break
        except ValueError:
            if parameters is not None:raise
    else:raise RuntimeError('No complete eligible instance')
    original=match_original(template,p)
    if original:
        asset=ASSET_REFS[original['source_id']]
        plot_meta={'role':'prompt','source_asset':str(Path('/media/jake/SSD/EDB/math')/asset),'png_sha256':file_hash(Path('/media/jake/SSD/EDB/math')/asset),'geometry':geometry,'independent_raster_evidence':'original-geometry.json'}
    else:
        asset,plot_meta=render_plots(geometry)
    statements=[statement_tex(*x,template,i) for i,x in enumerate(st)]
    prompt='![]('+asset+')\n\nConsider the diagram that is shown above. Which of the following statements are true?\n\n'+'\n'.join(f'{i+1}. ${v}$' for i,v in enumerate(statements))
    worked=None if raw else solution(template,vs,st,true)
    semantic={'template':template,'statements':statements,'requested_vectors':{x:[str(v) for v in vs[x]] for x in sorted(set(a for a,k,b in st)|set(b for a,k,b in st))}}
    # Common magnitude scaling is incidental; direction and ratios are assessed.
    requested=semantic['requested_vectors'];reference=next(iter(requested));scale=max(abs(sp.Rational(x)) for x in requested[reference])
    fingerprint=digest({'template':template,'k':str(p['k']),'s':p['s'],'t':p['t'],'u_direction':primitive(p['u']),'v_direction':primitive(p['v']),'grid':'equal-square unlabeled'})
    content={'version':VERSION,'level':None if raw else level,'prompt':prompt,'worked':worked,'bank':sorted(values),'field':'radio/selection','correct':None if raw else subset_text(true)}
    qid=owned(KP_UUID,content);fid=owned(qid,'selection')
    answers=[{':answer/id':owned(fid,v),':answer/type':':answer.type/text',':answer/value':v} for v in values]
    correct_id=owned(fid,subset_text(true));rng.shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
    if not raw:q.update({':question/difficulty':':question.difficulty/'+level,':question/worked-solution':worked});field[':answer-field/correct']=[':answer/id',correct_id]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':SOURCE,'seed':seed,'template':template,'bank_profile':profile,'parameters':serialize_parameters(p),'mathematical_fingerprint':fingerprint,'content_fingerprint':digest(content),'difficulty_status':'source unrated; authored assignment '+level,'source_ids':[c['source_id'] for c in SOURCE_CASES if c['template']==template],'evidence_only':raw,'eligible_for_learning':not raw,'correct_inference':subset_text(true),'geometry':geometry,'plot':plot_meta,'bank_recipes':(['toggle I','toggle II','toggle III','toggle I and III'] if profile=='authored-selection-flips' else 'complete observed subset catalog; selection omission/addition errors, original author intent unknown'),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate_easy(seed=0,**kw):
    """Authored unit/sign diagram recognition, no within-level progression."""
    return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):
    """Authored factor-two/reciprocal diagram recognition."""
    return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):
    """Authored 3:2/2:3 magnitude comparison grounded in lesson's 1.5 multiplier."""
    return generate('hard',seed,**kw)

def markdown(r):
    q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
    lines=['## '+('Parameterized raw evidence profile' if g['evidence_only'] else 'Generated authored '+q[':question/difficulty'].split('/')[-1]),'Template: '+g['template']+'; profile: '+g['bank_profile'],q[':question/problem']]
    lines+=['\nChoices:']+[f'- {a[":answer/value"]}'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices']]
    if ':question/worked-solution' in q:lines+=['\nWorked solution:',q[':question/worked-solution']]
    else:lines+=['\nOriginal correct ref, difficulty and worked solution absent. Independent inference: '+g['correct_inference']+'. Evidence only.']
    return '\n\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=TEMPLATES);ap.add_argument('--profile',choices=list(PROFILES));ap.add_argument('--parameters',help='Exact JSON parameters')
    args=ap.parse_args()
    if args.count<1:ap.error('count must be positive')
    params=json.loads(args.parameters) if args.parameters else None
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,parameters=params,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
