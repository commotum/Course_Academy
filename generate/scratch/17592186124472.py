#!/usr/bin/env python3
"""Identifying invertible functions from four displayed graphs (steps 3–7).

Read-only source: math basis 1356, lineage in source.json. Raw captured ink
profiles are parameterized affine evidence, never normal practice. Their
unlabelled smooth geometry cannot establish exact polynomial equations.
Normal authored defaults use exact finite-domain functions and complete
five-choice subset banks recovered from sources. Scope: one horizontal-line
recognition on the whole shown domain, no interval selection/inverse algebra.

Easy: four familiar continuous shapes; no boundary-sensitive inference.
Moderate: four two-piece graphs; compare strictly separated or overlapping
ordinate interiors. Hard (authored absent level): four three-piece graphs;
interiors separated, equal endpoint ordinates require open/closed reasoning.
Every graph within a level has the same structural workload. Domains are
supplied visually, not chosen by the learner. Source profiles are explicit,
preserve missing attributes, and are excluded from default sampling.

CLI: .venv/bin/python generate/scratch/17592186124472.py --difficulty all
API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None); generate_easy/moderate/hard. Parameters never silently repaired.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, os, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
try:
    import sympy as sp
except ImportError:
    interpreter = Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__ == '__main__' and interpreter.exists() and str(interpreter) != sys.executable:
        os.execv(str(interpreter), [str(interpreter), str(Path(__file__).resolve()), *sys.argv[1:]])
    raise

KP=17592186124472
D=Path(__file__).resolve().with_suffix('')
REPO=Path(__file__).resolve().parents[2]
VERSION='invertible-graph-1.0'
SNAPSHOT=json.loads((D/'source.json').read_text())
R=SNAPSHOT['record']; TITLE=R[':knowledge-point/title']; UUID=R[':knowledge-point/id']
SOURCES={q[':question/math-academy-id']:q for q in R[':knowledge-point/questions']}
ROMANS=('I','II','III','IV');X=sp.Symbol('x',real=True)
EASY_TRUE=('linear','cubic','exponential','logarithm','reciprocal')
EASY_FALSE=('parabola','absolute','wave','bell','constant')
EASY_KINDS=EASY_TRUE+EASY_FALSE
OPENING="A function is invertible if and only if it's a one-to-one function. To determine which of the functions are one-to-one, we use the horizontal line test."

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp:'+str(KP)+':'+v))
def mask(v):return sum(1<<ROMANS.index(t) for t in re.findall(r'\b(?:IV|III|II|I)\b',v))
def answer_label(m):
    z=[r for i,r in enumerate(ROMANS) if m>>i&1]
    if not z:return 'None'
    if len(z)==1:return z[0]+' only'
    return ', '.join(z[:-1])+(' and '+z[-1])+' only'
BANKS={name:[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']] for name,q in SOURCES.items()}

def expression(s):
    if 'expression' in s:return sp.sympify(s['expression'],locals={'x':X})
    return sum(sp.Rational(v)*X**i for i,v in enumerate(s['coefficients']))

def endpoint(s,t):return sp.simplify(expression(s).subs(X,sp.Rational(t)))
def image_range(s):
    e=expression(s);a,b=sp.Rational(s['a']),sp.Rational(s['b']);fa,fb=endpoint(s,a),endpoint(s,b)
    if sp.diff(e,X)==0:return sp.FiniteSet(fa)
    roots=sp.solveset(sp.diff(e,X),X,domain=sp.Interval.open(a,b))
    values=[fa,fb]+[sp.simplify(e.subs(X,t)) for t in roots if roots.is_FiniteSet]
    lo=min(values,key=lambda z:float(z));hi=max(values,key=lambda z:float(z))
    def included(v):
        return (v==fa and s['left_closed']) or (v==fb and s['right_closed']) or any(v==e.subs(X,t) for t in roots if roots.is_FiniteSet)
    return sp.Interval(lo,hi,left_open=not included(lo),right_open=not included(hi))

def injectivity(g):
    """Exact analytic criterion on ALL actual domain pieces.
    Each piece must be injective; their images must be pairwise disjoint, except
    two adjoining domain pieces may share the SAME input/output point.
    """
    intervals=[]
    for s in g['segments']:
        e=expression(s);der=sp.diff(e,X)
        if der==0:return False
        a,b=sp.Rational(s['a']),sp.Rational(s['b'])
        # Signs at all critical subinterval midpoints; no floating grid surrogate.
        roots=sp.solveset(der,X,domain=sp.Interval.open(a,b))
        if not roots.is_FiniteSet:raise ValueError('unsupported derivative roots')
        points=[a]+sorted(list(roots),key=float)+[b]
        signs={sp.sign(der.subs(X,(u+v)/2)) for u,v in zip(points,points[1:])}
        if len(signs-{0})>1:return False
        intervals.append(image_range(s))
    for i in range(len(intervals)):
        for j in range(i):
            common=sp.Intersection(intervals[i],intervals[j])
            if common==sp.EmptySet:continue
            # Continuous split of |x| at x=0 counts the single input only once.
            si,sj=g['segments'][i],g['segments'][j]
            same=sp.Rational(si['a'])==sp.Rational(sj['b']) and endpoint(si,si['a'])==endpoint(sj,sj['b'])
            if same and common==sp.FiniteSet(endpoint(si,si['a'])):continue
            return False
    return True

def witness(g):
    if injectivity(g):return None
    intervals=[image_range(s) for s in g['segments']]
    for i in range(len(intervals)):
        for j in range(i):
            inter=sp.Intersection(intervals[i],intervals[j])
            if inter==sp.EmptySet:continue
            if isinstance(inter,sp.Interval):return float((2*inter.start+inter.end)/3)
            if inter.is_FiniteSet:return float(next(iter(inter)))
    s=g['segments'][0];r=image_range(s)
    return float(next(iter(r))) if r.is_FiniteSet else float((2*r.start+r.end)/3)

def illustrative_height(g):
    r=image_range(g['segments'][0])
    if r.is_FiniteSet:return float(next(iter(r)))
    y=(2*r.start+r.end)/3
    if y==0:y=(3*r.start+r.end)/4
    return float(y)

def seg(a,b,e,lc=True,rc=True):return {'a':a,'b':b,'expression':str(e),'left_closed':lc,'right_closed':rc}
def easy_graph(kind,orientation=1):
    if kind not in EASY_KINDS or type(orientation)!=int or orientation not in (-1,1):raise ValueError('easy bounds')
    formulas={'linear':X*sp.Rational(4,5),'cubic':X**3/20,'exponential':sp.exp(X/2)-1,'logarithm':sp.log(X),'reciprocal':1/X-sp.Rational(1,2),'parabola':X**2/4-2,'wave':2*sp.cos(2*X),'bell':3/(1+X**2)-sp.Rational(1,2),'constant':sp.Integer(2)}
    if kind=='absolute':ss=[seg(-4,0,-X/2-1),seg(0,4,X/2-1)]
    else:
        a,b=(-3,3) if kind=='exponential' else ((.25,4) if kind in ('logarithm','reciprocal') else (-4,4))
        ss=[seg(a,b,orientation*formulas[kind])]
    g={'level':'easy','family':kind,'segments':ss};g['witness']=witness(g);g['test_height']=illustrative_height(g);return g

def polynomial_segment(a,b,low,high,direction,kind,lc,rc):
    u=(X-sp.Rational(a))/sp.Rational(b-a)
    shape=u if kind=='linear' else u**2
    e=sp.Rational(low)+(sp.Rational(high)-sp.Rational(low))*(shape if direction==1 else 1-shape)
    p=sp.Poly(sp.expand(e),X)
    return {'a':a,'b':b,'coefficients':[str(p.nth(i)) for i in range(p.degree()+1)],'left_closed':lc,'right_closed':rc}

def piece_graph(level,wanted,p):
    n=2 if level=='moderate' else 3
    if set(p)!={'kinds','directions','range_order','closures','overlap'}:raise ValueError('piece parameters')
    if len(p['kinds'])!=n or any(z not in ('linear','quadratic') for z in p['kinds']):raise ValueError('piece kind bounds')
    if len(p['directions'])!=n or any(z not in (-1,1) for z in p['directions']):raise ValueError('directions')
    if sorted(p['range_order'])!=list(range(n)):raise ValueError('range_order')
    if len(p['closures'])!=n or any(len(z)!=2 or any(type(b)!=bool for b in z) for z in p['closures']):raise ValueError('closures')
    if type(p['overlap'])!=bool:raise ValueError('overlap bool')
    if level=='hard' and p['overlap']:raise ValueError('hard interiors must be disjoint')
    if level=='hard':
        order=p['range_order'];dirs=p['directions'];cl=p['closures']
        low_outer=order.index(0);high_outer=order.index(2)
        if not cl[low_outer][0 if dirs[low_outer]==1 else 1] or not cl[high_outer][1 if dirs[high_outer]==1 else 0]:raise ValueError('hard exterior endpoints must be included')
        for boundary in (0,1):
            i=order.index(boundary);j=order.index(boundary+1)
            count=cl[i][1 if dirs[i]==1 else 0]+cl[j][0 if dirs[j]==1 else 1]
            expected=1 if wanted or boundary==1 else 2
            if count!=expected:raise ValueError('hard exact endpoint-membership workload bounds')
    domains=[(-4,-1),(1,4)] if n==2 else [(-4,-2),(-1,1),(2,4)]
    ranges=[(-3,-1),(1,3)] if n==2 and not p['overlap'] else ([(-1,1),(-1,1)] if n==2 else [(-3,-1),(-1,1),(1,3)])
    ss=[polynomial_segment(a,b,*ranges[p['range_order'][i]],p['directions'][i],p['kinds'][i],*p['closures'][i]) for i,(a,b) in enumerate(domains)]
    g={'level':level,'family':'two-pieces' if n==2 else 'three-pieces','segments':ss}
    if injectivity(g)!=wanted:raise ValueError('requested bank mask disagrees with plotted domain')
    g['witness']=witness(g);g['test_height']=illustrative_height(g);return g

def sample_piece(level,wanted,rng):
    n=2 if level=='moderate' else 3
    order=list(range(n));rng.shuffle(order)
    dirs=[rng.choice([-1,1]) for _ in range(n)]
    closes=[[True,True] for _ in range(n)]
    if level=='hard':
        # Two shared output levels. Open at least one endpoint at each level for
        # injective graphs; for a failing graph keep one complete duplicate pair.
        for boundary in (0,1):
            i=order.index(boundary);j=order.index(boundary+1)
            ei=1 if dirs[i]==1 else 0;ej=0 if dirs[j]==1 else 1
            if wanted or boundary==1:
                q=rng.choice([(i,ei),(j,ej)]);closes[q[0]][q[1]]=False
    return {'kinds':[rng.choice(['linear','quadratic']) for _ in range(n)],'directions':dirs,'range_order':order,'closures':closes,'overlap':not wanted if level=='moderate' else False}

def asset(data):
    data=dict(data,renderer_version='1.3');key=digest(data);p=D/'assets'/f'{key}.png';side=p.with_suffix('.json')
    if p.exists() and side.exists():
        z=json.loads(side.read_text())
        if hashlib.sha256(p.read_bytes()).hexdigest()==z['sha256']:return str(p)
    fd,tmp=tempfile.mkstemp(prefix='render-',suffix='.json',dir=D/'assets');os.close(fd)
    try:
        Path(tmp).write_text(json.dumps(data));run=subprocess.run([sys.executable,str(D/'render.py'),tmp,str(p)],capture_output=True,text=True)
        if run.returncode:raise RuntimeError(run.stderr)
    finally:Path(tmp).unlink(missing_ok=True)
    return str(p)

def render_plots(graphs):
    # Convert exact rational coefficients only at the rendering boundary.
    gg=copy.deepcopy(graphs)
    return {role:asset({'mode':'normal','graphs':gg,'solution':role=='solution'}) for role in ('prompt','solution')}

def enum(v):return v[':db/ident'] if isinstance(v,dict) else v

def source_replay(name,seed,parameters):
    """Public raw recipe. Bank subset masks and ALL prose are permutable slots.
    Captured ink gets a positive affine map; no source answer lookup is performed.
    Raw absent correct refs/difficulty/solution remain absent.
    """
    q=SOURCES[name]
    p={'order':[0,1,2,3],'scale':[1,1]} if parameters is None else copy.deepcopy(parameters)
    if set(p)!={'order','scale'} or sorted(p['order'])!=[0,1,2,3] or len(p['scale'])!=2 or any(not .75<=v<=1 for v in p['scale']):raise ValueError('raw profile bounds')
    # Only affine raw transforms are currently supported. Label permutation is
    # disallowed until the source pixel labels can be independently regenerated.
    if p['order']!=[0,1,2,3]:raise ValueError('opaque labels cannot be permuted')
    assets={}
    def textfield(s):
        def sub(m):
            ref=m.group(1);full=D/'originals'/Path(ref).name
            if p['scale']==[1,1]:assets[ref]=str(full);return m.group(0)
            rendered=asset({'mode':'raw','asset':str(full),'scale':p['scale']});assets[ref]=rendered
            return '![]('+rendered+')'
        return re.sub(r'!\[\]\((images/[^)]+)\)',sub,s)
    problem=textfield(q[':question/problem'])
    sol=textfield(q[':question/worked-solution']) if ':question/worked-solution' in q else None
    values=BANKS[name]
    content=digest({'version':VERSION,'problem':problem,'solution':sol,'bank':sorted(values),'difficulty':q.get(':question/difficulty'),'presence':sorted(k for k in q if k.startswith(':question/'))})
    qq={':question/id':uid(content),':question/problem':problem,':question/math-academy-id':q[':question/math-academy-id']}
    if ':question/difficulty' in q:qq[':question/difficulty']=enum(q[':question/difficulty'])
    if sol is not None:qq[':question/worked-solution']=sol
    field_id=uid(content+':selection')
    choices=[{':answer/id':uid(field_id+':'+str(mask(v))),':answer/type':':answer.type/text',':answer/value':v} for v in values]
    f={':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
    srcf=q[':question/answer-fields'][0]
    if ':answer-field/correct' in srcf:
        correct_mask=mask(srcf[':answer-field/correct'][':answer/value'])
        f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in choices if mask(a[':answer/value'])==correct_mask)]
    random.Random(seed).shuffle(choices);qq[':question/answer-fields']=[f]
    return {'knowledge_point':{'db_id':KP,'id':UUID,'title':TITLE},'question':qq,'generation':{'version':VERSION,'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'source_id':name,'template':'captured-graph-bank','profile':'raw:'+name,'bank_profile':name,'parameters':p,'evidence_only':True,'eligible_for_learning':False,'opaque_geometry':True,'assets':assets,'mathematical_fingerprint':digest({'captured_bank':name}), 'identity':content,'python':sys.version.split()[0]}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
    if profile and profile.startswith('raw:'):
        name=profile[4:]
        if name not in SOURCES or template not in (None,'captured-graph-bank'):raise ValueError('source profile')
        return source_replay(name,seed,parameters)
    if template not in (None,level+'-graphs'):raise ValueError('level template')
    rng=random.Random(seed)
    bank_name=profile or rng.choice(sorted(BANKS))
    if bank_name not in BANKS:raise ValueError('complete bank profile')
    values=BANKS[bank_name];masks=[mask(v) for v in values]
    if len(masks)!=5 or len(set(masks))!=5:raise ValueError('invalid whole bank')
    if parameters is None:
        correct=rng.choice(masks)
        ps=[]
        for i in range(4):
            wanted=bool(correct>>i&1)
            if level=='easy':ps.append({'kind':rng.choice(EASY_TRUE if wanted else EASY_FALSE),'orientation':rng.choice([-1,1])})
            else:ps.append(sample_piece(level,wanted,rng))
        parameters={'correct_mask':correct,'graphs':ps}
    p=copy.deepcopy(parameters)
    if set(p)!={'correct_mask','graphs'} or type(p['correct_mask'])!=int or p['correct_mask'] not in masks or len(p['graphs'])!=4:raise ValueError('parameters/bank mismatch')
    graphs=[]
    for i,gp in enumerate(p['graphs']):
        wanted=bool(p['correct_mask']>>i&1)
        if level=='easy':
            if set(gp)!={'kind','orientation'}:raise ValueError('easy parameters')
            g=easy_graph(**gp)
            if injectivity(g)!=wanted:raise ValueError('easy graph mask mismatch')
        else:g=piece_graph(level,wanted,gp)
        graphs.append(g)
    computed=sum(1<<i for i,g in enumerate(graphs) if injectivity(g))
    if computed!=p['correct_mask'] or masks.count(computed)!=1:raise ValueError('whole-instance ambiguity')
    plots=render_plots(graphs)
    problem=f"![]({plots['prompt']})\n\nWhich of the graphs above correspond to an invertible function?\n\nEach graph shows its entire domain; an open circle excludes its endpoint."
    passes=[ROMANS[i] for i in range(4) if computed>>i&1];fails=[ROMANS[i] for i in range(4) if not computed>>i&1]
    solution=OPENING+'\n\n![]('+plots['solution']+')\n\nFrom the above, we see that:'
    if passes:solution+='\n\n- For graph'+('s ' if len(passes)>1 else ' ')+', '.join(passes)+", any horizontal line will intersect the curve at most once, no matter where we draw the line. Therefore, "+('these graphs show one-to-one functions. As a result, these functions are invertible.' if len(passes)>1 else 'this graph shows a one-to-one function. As a result, this function is invertible.')
    if fails:solution+='\n\n- For graph'+('s ' if len(fails)>1 else ' ')+', '.join(fails)+', some horizontal lines intersect the curve more than once. These are not one-to-one functions. As a result, they are not invertible.'
    solution+='\n\nTherefore, the correct answer is "'+next(v for v in values if mask(v)==computed)+'".'
    content=digest({'version':VERSION,'problem':problem,'solution':solution,'bank':sorted(values),'difficulty':level})
    fid=uid(content+':selection');choices=[{':answer/id':uid(fid+':'+str(mask(v))),':answer/type':':answer.type/text',':answer/value':v} for v in values]
    f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if mask(a[':answer/value'])==computed)]}
    rng.shuffle(choices)
    # Strip affine/coefficient aliases: fingerprint only structural recognition,
    # domains, image ordering/overlap and endpoint inclusion at shared levels.
    task=[]
    for i,g in enumerate(graphs):
        if level=='easy':task.append({'family':g['family']})
        elif level=='moderate':task.append({'kinds':p['graphs'][i]['kinds'],'directions':p['graphs'][i]['directions'],'range_order':p['graphs'][i]['range_order'],'overlap':p['graphs'][i]['overlap']})
        else:task.append(p['graphs'][i])
    return {'knowledge_point':{'db_id':KP,'id':UUID,'title':TITLE},'question':{':question/id':uid(content),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[f]},'generation':{'version':VERSION,'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'template':level+'-graphs','bank_profile':bank_name,'profile':bank_name,'parameters':p,'graphs':graphs,'assets':plots,'authored':True,'authored_difficulty':True,'evidence_only':False,'eligible_for_learning':True,'correct_mask':computed,'mathematical_fingerprint':digest({'level':level,'graphs':task}),'identity':content,'python':sys.version.split()[0],'sympy':sp.__version__}}

# The current database migrated the finite-subset response to four checkbox
# fields. Keep the historical radio profiles as ineligible source evidence;
# convert normal exact-domain instances without changing their mathematics.
legacy_generate = generate
CURRENT = json.loads((D/'current-source.json').read_text())
CURRENT_SOURCES = {q[':question/math-academy-id']:q for q in CURRENT[':knowledge-point/questions']}
CHECKBOX_VERSION = 'invertible-graph-checkbox-2.0'

def generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None):
    if profile and profile.startswith('current:'):
        name = profile[8:]
        if name not in CURRENT_SOURCES or parameters is not None:
            raise ValueError('current source replay accepts original parameters only')
        q = copy.deepcopy(CURRENT_SOURCES[name])
        return {'knowledge_point':{'db_id':KP,'id':UUID,'title':TITLE}, 'question':q,
                'generation':{'version':CHECKBOX_VERSION,'template':'current-source',
                    'source_id':name,'source_basis':2221,'evidence_only':True,
                    'eligible_for_learning':False,'assets':{}}}
    if profile and profile.startswith('raw:'):
        return legacy_generate(level, seed, template, field_type, parameters, profile)
    if field_type not in (None, 'checkbox', ':answer-field.type/checkbox'):
        raise ValueError('current production response uses four checkbox fields')
    r = legacy_generate(level, seed, template, None, parameters, profile)
    q, meta = r['question'], r['generation']
    q[':question/problem'] += '\n\nSelect all that apply.\n\nGraph positions: **I.** upper left; **II.** upper right; **III.** lower left; **IV.** lower right.'
    q[':question/worked-solution'] = q[':question/worked-solution'].split('\n\nTherefore, the correct answer is')[0]
    content = digest({'version':CHECKBOX_VERSION, 'problem':q[':question/problem'],
                      'solution':q[':question/worked-solution'],'difficulty':level,
                      'response':'four-boolean-checkboxes'})
    fields = []
    for i, label in enumerate(ROMANS):
        fid = uid(content+':checkbox:'+label)
        choices = [{':answer/id':uid(fid+':'+value), ':answer/type':':answer.type/text',
                    ':answer/value':value} for value in ('false','true')]
        value = 'true' if meta['correct_mask'] >> i & 1 else 'false'
        fields.append({':answer-field/id':fid, ':answer-field/key':label,
                       ':answer-field/type':':answer-field.type/checkbox',
                       ':answer-field/choices':choices,
                       ':answer-field/correct':[':answer/id',uid(fid+':'+value)]})
    q[':question/id'], q[':question/answer-fields'] = uid(content), fields
    # Panel-label permutations are incidental to the unordered recognition task.
    task = []
    for i, graph in enumerate(meta['graphs']):
        p = meta['parameters']['graphs'][i]
        task.append({'family':graph['family']} if level=='easy' else
                    {k:p[k] for k in ('kinds','directions','range_order','overlap')} if level=='moderate' else p)
    meta.update(version=CHECKBOX_VERSION, identity=content,
                mathematical_fingerprint=digest({'level':level,'graphs':sorted(task,key=lambda t:json.dumps(t,sort_keys=True))}),
                legacy_sampling_profile=meta['bank_profile'], bank_profile='checkbox-boolean',
                response_contract='four field-owned false/true banks', seed=seed)
    return r

# Easy: continuous shape recognition, one domain per graph.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: two independently monotone pieces, interior image overlap criterion.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard authored extension: three monotone pieces, endpoint membership criterion.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
    q=r['question'];out=q[':question/problem']+'\n\n'
    for f in q.get(':question/answer-fields',[]):
        out+='\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'
    return out+q.get(':question/worked-solution','[Original source omits the worked solution.]')

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--parameters',type=json.loads)
    a=ap.parse_args();levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
    if a.count<1:ap.error('count must be positive')
    rs=[generate(l,a.seed+i,template=a.template,profile=a.profile,parameters=a.parameters) for l in levels for i in range(a.count)]
    print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rs))
