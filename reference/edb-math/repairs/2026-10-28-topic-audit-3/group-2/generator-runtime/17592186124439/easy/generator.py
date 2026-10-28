#!/usr/bin/env python3
"""Seeded coordinate-slice tangent vectors. No services or writable runtime data."""
from __future__ import annotations
import argparse, functools, hashlib, itertools, json, random, re, uuid
from batch_policy import failures as bank_cue_failures
from pathlib import Path
import sympy as sp
from math_format import normalize_prose, normalize_tex, validate_generated_record

HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source-replay.json').read_text())
X,Y=sp.symbols('x y',real=True)
KP={'db_id':17592186124439,'id':'b0325887-ce25-5d6f-bf27-d85541e1dbe0','title':'Finding the Tangent Vector to a Curve at a Point'}
VERSION='slice-tangent-3'
# name, fixed coordinate, symbolic derivative, source point, eligible evaluation pairs
SPECS=[
 ('linear_x','y','6*(x-1)',(2,-3,3),[(a,b) for a in [-1,0,1,2,3] for b in [-2,1,3]]),
 ('factored_y','x','x**2*(2*x*y-1)',(1,-1,2),[(a,b) for a in [-1,1] for b in [-2,-1,0,1,2]]),
 ('exp_cos_x','y','exp(y-1)+2*x*cos(y-1)',(2,1,4),[(a,1) for a in [-2,-1,0,1,2]]),
 ('polynomial_y','x','x**2*y+2*x-y',(-2,2,3),[(a,b) for a in [-2,-1,1,2] for b in [-2,-1,0,1,2]]),
 ('log_polynomial_x','y','x**2+y**2-log(x+y)',(0,1,7),[(a,1-a) for a in [-1,0,1,2]]),
 ('exp_cos_y','x','x*exp(x*y)-2*cos(y)',(1,0,-1),[(a,0) for a in [-2,-1,0,1,2,3]]),
 ('affine_x','y','2*(x+y)-2',(1,1,1),[(a,b) for a in [-2,-1,0,1,2] for b in [-1,0,1,2]]),
 ('radical_y','x','(y-x)/sqrt(x*(y+x))',(-2,-6,1),[(a,b) for a,b in [(-2,-6),(-2,-4),(-1,-3),(1,3),(2,4),(2,6),(-2,1),(2,-1)]]),
 ('exp_log_x','y','3*exp(x+y)-log(Abs(x*y))',(-1,1,-1),[(-1,1),(1,-1)]),
 ('quotient_y','x','x*(y-x)/(2*x*(y+1))',(-1,0,sp.Rational(1,2)),[(a,b) for a in [-2,-1,1,2] for b in [0,1,2]]),
 ('trig_difference_y','x','2*sin(x*y)-cos(pi*y/2)',(sp.pi/2,1,0),[(a,b) for a in [sp.pi/2,-sp.pi/2] for b in [-1,0,1,2]]),
 ('trig_product_y','x','sin(x)*cos(y)/2',(-sp.pi/2,0,2),[(a,b) for a in [sp.pi/2,-sp.pi/2] for b in [0,sp.pi]]),
 ('trig_product_x','y','sqrt(2)*sin(2*y)*cos(y)',(1,sp.pi/4,0),[(a,b) for a in [-1,1,2] for b in [sp.pi/4,-sp.pi/4,3*sp.pi/4]]),
 ('log_cube_y','x','3*log(y+1)-(x+y)**3',(1,0,-1),[(a,0) for a in [-2,-1,0,1,2]]),
 ('radical_x','y','sqrt(y**2-x**2)/(2*x-y)',(4,5,-2),[(a,b) for a,b in [(4,5),(-4,5),(3,5),(-3,5),(4,-5),(-4,-5)]]),
 ('trig_sum_x','y','(y+1)*cos(pi*x)+2*x*cos(pi*y)*sin(pi*x)',(sp.Rational(1,2),0,1),[(a,0) for a in [sp.Rational(1,2),-sp.Rational(1,2),sp.Rational(3,2),1,0]]),
 ('log_reciprocal_y','x','x+2*x*log(x*y)+1/y',(2,sp.Rational(1,2),1),[(a,1/sp.Integer(a)) for a in [-2,-1,1,2]])]
NAMES=[s[0] for s in SPECS]

def tex(x):return sp.latex(sp.sympify(x)).replace(r'\log',r'\ln')
def vec(v):return r'\langle '+','.join(tex(x) for x in v)+r'\rangle'
def block(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def split_terms(rhs):
    """Split only top-level additive terms; keep operator arguments intact."""
    depth=0;parts=[];start=0
    for i,c in enumerate(rhs):
        if c in '({[':depth+=1
        elif c in ')}]':depth-=1
        elif c in '+-' and depth==0 and i>start:
            parts.append(rhs[start:i]);start=i
    parts.append(rhs[start:]);return parts

def equation_rows(lhs,rhs,limit=120):
    parts=split_terms(rhs)
    negative_group=rhs.startswith(r'-\left(') and rhs.endswith(r'\right)')
    if negative_group:
        inner=rhs[len(r'-\left('):-len(r'\right)')]
        inner_parts=split_terms(inner)
        if len(rhs)>limit and len(inner_parts)>1:
            rows=[lhs+r' & =-\Bigl('+inner_parts[0]]+['& '+part for part in inner_parts[1:]]
            rows[-1]+=r'\Bigr)'
            return rows
    if len(rhs)<=limit or len(parts)==1:return [lhs+' & ='+rhs]
    return [lhs+' & ='+parts[0]]+['& '+part for part in parts[1:]]

def expression(s):return sp.sympify(s,locals={'x':X,'y':Y},evaluate=False)
def parallel(a,b):return any(sp.simplify(t)!=0 for t in a) and all(sp.simplify(t)==0 for t in sp.Matrix(a).cross(sp.Matrix(b)))
def axis_vector(m,plane):return (sp.Integer(1),sp.Integer(0),m) if plane=='y' else (sp.Integer(0),sp.Integer(1),m)
def identity(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))

def record(level,prompt,solution,values,correct,metadata):
    prompt,solution=map(normalize_prose,(prompt,solution)); values=list(map(normalize_tex,values))
    payload=json.dumps([level,prompt,solution,sorted(values),values[correct]],ensure_ascii=False,separators=(',',':'))
    digest=hashlib.sha256(payload.encode()).hexdigest();fid=identity(digest+'/selection')
    choices=[{':answer/id':identity(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    q={':question/id':identity(digest),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[correct][':answer/id']]}]}
    return validate_generated_record({'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,**metadata}})

def replay(i):
    s=SOURCE[i]
    return record('hard',s['prompt'],s['solution'],s['values'],s['correct'],{'template':NAMES[i],'source_id':s['source_id'],'source_key':s['source_key'],'source_replay':True})

ROLES=['sign','reciprocal','normal','double_vertical','half_vertical','point_x','point_y','point_z','horizontal','vertical','omit_term','flip_term','wrong_axis']

@functools.lru_cache(maxsize=1024)
def bank_catalog(m,plane,point,expr,subitems,hard=False):
    """Choose one complete authored four-error profile, then instantiate/validate it.

    Profiles are combinations, not the first four usable errors in a recipe list.
    A colliding profile is retried on this SAME instance, preserving cancellations.
    """
    subs=dict(subitems)
    target=axis_vector(m,plane);a,b,z=point
    terms=sp.Add.make_args(sp.expand(expr))
    first=terms[0].subs(subs)
    slopes={'sign':-m,'double_vertical':2*m,'half_vertical':m/2,
            'point_x':a,'point_y':b,'point_z':z,'horizontal':sp.Integer(0),
            'omit_term':sp.simplify(m-first),'flip_term':sp.simplify(m-2*first)}
    # Common evaluation slips are instantiated from this expression, including
    # boundary mistakes that remain distinct when sign/reciprocal errors collide.
    log_nodes=[node for node in sp.preorder_traversal(expr) if node.func==sp.log and sp.simplify(node.subs(subs))==0]
    power_nodes=[node for node in sp.preorder_traversal(expr) if node.is_Pow and node.exp.is_positive and sp.simplify(node.base.subs(subs))==0]
    if log_nodes:slopes['log_one_as_one']=expr.xreplace({node:sp.Integer(1) for node in log_nodes}).subs(subs)
    if power_nodes:slopes['zero_power_as_one']=expr.xreplace({node:sp.Integer(1) for node in power_nodes}).subs(subs)
    if hard:
        next_derivative=sp.diff(expr,X if plane=='y' else Y).subs(subs)
        slopes['differentiate_again']=next_derivative
        slopes['differentiate_again_sign']=-next_derivative
    candidates={k:axis_vector(sp.simplify(v),plane) for k,v in slopes.items()}
    if m!=0:
        candidates['reciprocal']=axis_vector(1/m,plane)
        candidates['normal']=axis_vector(-1/m,plane)
    candidates['vertical']=(sp.Integer(0),sp.Integer(0),sp.Integer(1))
    if not hard:candidates['wrong_axis']=axis_vector(m,'x' if plane=='y' else 'y')
    # Mathematically valid profiles are computed exhaustively. Random profile choice
    # precedes rendering; no question instance is discarded to make a bank easier.
    usable=[k for k,v in candidates.items() if not parallel(v,target) and all(sp.sympify(c).is_real is True and not sp.sympify(c).has(sp.zoo,sp.nan,sp.oo) for c in v)]
    collisions={frozenset((u,v)) for u,v in itertools.combinations(usable,2) if parallel(candidates[u],candidates[v])}
    profiles=[p for p in itertools.combinations(usable,4) if all(frozenset((u,v)) not in collisions for u,v in itertools.combinations(p,2))]
    if not profiles:raise ValueError('No complete distinct bank for this instance')
    return candidates,profiles

def build_bank(m,plane,point,expr,subs,rng,hard=False):
    candidates,profiles=bank_catalog(m,plane,point,expr,tuple(subs.items()),hard)
    target=axis_vector(m,plane)
    roles=rng.choice(profiles); vectors=[target]+[candidates[r] for r in roles]
    # One presentation algorithm for every option. Hard banks have no canonical
    # free-component promise; reverse directions remain fully valid.
    scales=[rng.choice([-3,-2,-1,1,2,3]) for _ in vectors] if hard else [sp.Integer(1)]*len(vectors)
    vectors=[tuple(sp.simplify(t*c) for t in v) for c,v in zip(scales,vectors)]
    tagged=list(zip(vectors,['correct',*roles]));rng.shuffle(tagged)
    return [v for v,r in tagged],next(i for i,(v,r) in enumerate(tagged) if r=='correct'),[r for v,r in tagged]

def make_instance(level,seed,family=None,overrides=None):
    rng=random.Random(seed);o=overrides or {}
    if level=='hard':
        i=NAMES.index(family) if family else rng.randrange(len(SPECS));name,plane,es,pt,pairs=SPECS[i]
        a,b=map(sp.sympify,o.get('xy',rng.choice(pairs)));z=sp.sympify(o.get('z',rng.choice([-4,-3,-2,2,3,4])))
        expr=expression(es);sign=o.get('sign',rng.choice([-1,1]));swap=o.get('swap',rng.choice([False,True]))
        # Preserve the source operator input in the printed formula.
        original=SOURCE[i]['prompt'];rhs=re.search(r'and that \$(.*?)\$, which',original,re.S).group(1).split('=',1)[1]
        rhs=rhs.replace(r'\operatorname{cos}⁡',r'\cos ').replace(r'\operatorname{sin}⁡',r'\sin ').replace(r'\operatorname{ln}⁡',r'\ln ')
        if sign==-1:expr=-expr;rhs=r'-\left('+rhs+r'\right)'
        if swap:
            expr=expr.xreplace({X:Y,Y:X});a,b=b,a;plane='x' if plane=='y' else 'y'
            rhs=re.sub(r'(?<![A-Za-z])([xy])(?![A-Za-z])',lambda m:'y' if m[1]=='x' else 'x',rhs)
        source_ids=[SOURCE[i]['source_id']]
    else:
        name='evaluated' if level=='easy' else 'affine'
        plane=o.get('plane',rng.choice(['x','y']));a,b=map(sp.sympify,o.get('xy',rng.sample([-3,-2,-1,1,2,3],2)));z=sp.sympify(o.get('z',rng.choice([-4,-3,3,4])))
        w=X if plane=='y' else Y
        if level=='easy':expr=sp.Integer(o.get('m',rng.choice([-4,-3,-2,-1,0,1,2,3,4])));rhs=tex(expr)
        else:
            c=o.get('c',rng.choice([-2,-1,1,2]));d=o.get('d',rng.choice([-2,-1,1,2]));e=o.get('e',rng.choice([-2,-1,0,1,2]));expr=c*X+d*Y+e;rhs=tex(expr)
        source_ids=[17592186707343 if level=='easy' else 17592186707325]
    point=(a,b,z);subs={X:a,Y:b};m=sp.simplify(expr.subs(subs))
    if m.is_real is not True or m.has(sp.oo,sp.zoo,sp.nan):raise ValueError('Invalid real slope')
    w='x' if plane=='y' else 'y';fixed=b if plane=='y' else a;w0=a if plane=='y' else b
    bank_rng=random.Random(o['bank_seed']) if 'bank_seed' in o else rng
    vectors,ci,roles=build_bank(m,plane,point,expr,subs,bank_rng,hard=level=='hard')
    pt=','.join(tex(t) for t in point);xy=','.join(tex(t) for t in point[:2]);pe=plane+'='+tex(fixed)
    prompt='The curve $C$ is the intersection of the surface $z=f(x,y)$ with the plane $'+pe+'$. The point $P('+pt+')$ lies on $C$.'
    if level=='easy':prompt+=' At this point, $f_'+w+'('+xy+')='+tex(m)+'$. The coordinate $'+plane+'$ is fixed along the slice.'
    else:prompt+=' The partial derivative is supplied:\n\n'+block(equation_rows('f_'+w+'(x,y)',rhs,90))
    prompt+='\n\nWhich of the following is a tangent vector to $C$ at $P$?'
    evaluation=re.sub(r'\\[A-Za-z]+|[xy]',lambda t:t[0] if t[0].startswith('\\') else r'\left('+tex(a if t[0]=='x' else b)+r'\right)',rhs)
    slope_rows=equation_rows('m=f_'+w+'('+xy+')',evaluation)
    if level!='easy':slope_rows.append('& ='+tex(m))
    v=axis_vector(m,plane);chosen=vectors[ci];factor=chosen[0] if plane=='y' else chosen[1]
    n1=(0,1,0) if plane=='y' else (1,0,0);n2=(-m,0,1) if plane=='y' else (0,-m,1);cross=tuple(sp.Matrix(n1).cross(sp.Matrix(n2)))
    normal_eq=tex(sp.expand(m*(X if plane=='y' else Y)-sp.Symbol('z')+z-m*w0))+'=0'
    solution='Holding $'+plane+'$ fixed means that $'+w+'$ varies, so the slice slope is $f_'+w+'('+xy+')$.\n\n'+block(slope_rows)
    # Keep a visible intermediate exact simplification for radical/quotient families.
    if level=='hard' and ('radical' in name or 'quotient' in name):solution+='\n\nThe displayed quotient is evaluated at the supplied point; its denominator is nonzero. Simplifying the numerator and denominator gives the exact slope above.'
    solution+='\n\nA change of $1$ in $'+w+'$ along the tangent gives a change of $'+tex(m)+'$ in $z$, with no change in $'+plane+'$. A tangent direction is $'+vec(v)+'$.\n\nThe tangent line through $P('+pt+')$ is\n\n$$\n'+r'\left\{\begin{aligned}'+plane+'&='+tex(fixed)+r' \\ z-('+tex(z)+')&=('+tex(m)+')('+w+'-('+tex(w0)+r'))\end{aligned}\right.'+'\n$$'
    solution+='\n\nThe second plane is equivalently $'+normal_eq+'$. Normal vectors are $\\mathbf n_1='+vec(n1)+'$ and $\\mathbf n_2='+vec(n2)+'$. Their cross product is\n\n'+block([r'\mathbf n_1\times\mathbf n_2 & =\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k \\ '+' & '.join(tex(t) for t in n1)+r' \\ '+' & '.join(tex(t) for t in n2)+r'\end{vmatrix}','& ='+vec(cross)])
    if plane=='x':solution+='\n\nNegating this cross product gives $'+vec(v)+'$.'
    solution+='\n\nAny nonzero scalar multiple is valid. The listed answer is\n\n'+block([tex(factor)+r'\left('+vec(v)+r'\right) & ='+vec(chosen)])+'\n\nIt has the required component ratio $v_z/v_'+w+'='+tex(m)+'$.'
    semantic={'plane':plane,'expr':str(expr),'xy':[str(a),str(b)]} if level!='easy' else {'plane':plane,'slope':str(m)}
    return record(level,prompt,solution,list(map(vec,vectors)),ci,{'template':name,'seed':seed,'parameters':{'plane':plane,'point':list(map(str,point)),'expression':str(expr),'slope':str(m)},'profile':roles,'bank_vectors':[list(map(str,v)) for v in vectors],'source_ids':source_ids,'semantic_identity':hashlib.sha256(json.dumps(semantic,sort_keys=True).encode()).hexdigest(),'authored_bank':True})

def batch(level,count,seed):
    """Deterministic family cycling avoids amplitude/height clones in finite batches."""
    rng=random.Random(seed);families=NAMES.copy();rng.shuffle(families);out=[];seen=set()
    for i in range(count):
        family=families[i%len(families)] if level=='hard' else None
        for attempt in range(100):
            r=make_instance(level,rng.getrandbits(63),family)
            semantic=r['generation']['semantic_identity']
            if semantic not in seen:break
        else:raise ValueError('Requested count exceeds practical unique sampling capacity')
        seen.add(semantic);out.append(r)
    # The finite delivered pool must not admit a universal bank-only cue in
    # a recognizable subgroup with at least two members. Retry whole authored
    # banks on the SAME mathematical instances; do not change seed or discard
    # cancellations, signs, points, or derivative families to balance a pool.
    for bank_attempt in range(4096):
        items=[]
        for r in out:
            q=r['question'];f=q[':question/answer-fields'][0]
            items.append({'vectors':[[float(sp.N(sp.sympify(v))) for v in row] for row in r['generation']['bank_vectors']],
                          'correct':next(i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==f[':answer-field/correct'][1]),
                          'template':r['generation']['template'],'plane':r['generation']['parameters']['plane']})
        failures=bank_cue_failures(items)
        if not failures:return out
        retry_indices={rng.choice(f['indices']) for f in failures}
        out=[make_instance(level,r['generation']['seed'],r['generation']['template'] if level=='hard' else None,
                           {'bank_seed':rng.getrandbits(63)}) if i in retry_indices else r for i,r in enumerate(out)]
    raise ValueError('Unable to construct a complete batch without the tested answer-bank cues')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='hard');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json'],default='json');p.add_argument('--source-replay',action='store_true');a=p.parse_args()
    if a.count<0:p.error('count must be nonnegative')
    rs=[replay(i) for i in range(len(SOURCE))] if a.source_replay else [r for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for r in batch(level,a.count,a.seed)]
    print(json.dumps(rs,ensure_ascii=False,indent=2))
