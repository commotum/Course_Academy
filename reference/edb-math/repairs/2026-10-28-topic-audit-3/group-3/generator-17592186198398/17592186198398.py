#!/usr/bin/env python3
"""Evaluate triple integrals using supplied changes of variables (basis 1356).

Seven captured five-choice radio families; original banks are opaque evidence
profiles, never default practice. Public raw replay uses a variable integrand
coefficient and scales every actual ordered integration stage and whole bank.
Its retained defects/key omissions are explicitly ineligible for learners.
Normal moderate serves all seven families with complete method-derived banks.
Easy and hard are authored same-method workload domains, described below.
No EDB writes, plots, external resources, or engine modifications.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s

KP_ID=17592186198398
KP_UUID='832dc2b8-873f-56c6-bd87-5e886a586fb1'
TITLE='Evaluating a Triple Integral Using a Change of Variables'
VERSION='triple-change-evaluation-1-audit9837'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
RAW=json.loads((HERE/'raw-recipes.json').read_text())
x,y,z,u,v,w=s.symbols('x y z u v w',real=True)
XYZ=(x,y,z); UVW=(u,v,w)
FAMILIES=('power','vcosu','ucosv','sum','exp','zcosu','sinsin')
SOURCE_FAMILY=dict(zip((17592186198623,17592186198964,17592186374090,17592186374097,17592186374125,17592186374132,17592186374139),FAMILIES))
LEVELS=('easy','moderate','hard')

class SampleRejected(ValueError):pass

def tex(e):return s.latex(s.sympify(e),order='lex').replace(r'\log',r'\ln')
def block(a):return '$$\n'+a+'\n$$'
def aligned(rows):return block(r'\begin{aligned}'+r' \\ '.join(a+' & ='+b for a,b in rows)+r'\end{aligned}')
def group(a):return r'\left('+a+r'\right)'
def difftex(a,b):return group(tex(a))+'-'+group(tex(b))
def integral(bounds,expr,variables=UVW):
    return ''.join(r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}' for lo,hi in bounds)+group(expr)+''.join(r'\,\mathrm{d}'+str(t) for t in reversed(variables))
def stable(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(key):return str(uuid.uuid5(uuid.NAMESPACE_URL,TITLE+':'+key))
def numeric(p):return {k:s.sympify(q,locals={'pi':s.pi}) for k,q in p.items()}
def serialized(p):return {k:str(q) for k,q in p.items()}

# ---------------------------------------------------------------------------
# Exact mathematics shared by observed and authored domains.
# No square-root inverses: every map is globally bijective with constant nonzero
# determinant; the quadratic shear is inverted using the linear v coordinate.
# ---------------------------------------------------------------------------
def model(f,p):
    a,b,c,d,n=(p[k] for k in ('a','b','c','d','n'))
    if f=='power':
        trans=(a*x+b*y,y+d*z,c*z); invy=v-d*w/c
        inverse=((u-b*invy)/a,invy,w/c); density=u**n*v
    elif f in ('vcosu','ucosv','sinsin'):
        trans=(x*x+b*y,x+d*z,c*z); invx=v-d*w/c
        inverse=(invx,(u-invx**2)/b,w/c)
        density={'vcosu':v*s.cos(u),'ucosv':u*s.cos(v),'sinsin':s.sin(v)*s.sin(u)}[f]
    elif f=='sum':
        trans=(x-y/b,y/b,c*z); inverse=(u+v,b*v,w/c);density=u+w
    elif f=='exp':
        trans=(x+y*y,y+d*z,c*z); invy=v-d*w/c
        inverse=(u-invy**2,invy,w/c);density=v*s.exp(u)
    elif f=='zcosu':
        trans=(a*x+b*y,d*x+z,c*z); invx=(v-w/c)/d
        inverse=(invx,(u-a*invx)/b,w/c);density=w*w*s.cos(u)/c**2
    else:raise ValueError('Unknown family')
    matrix=s.Matrix(trans).jacobian(XYZ); determinant=s.factor(matrix.det())
    if determinant==0:raise ValueError('Singular transformation')
    j=1/s.Abs(determinant)
    bounds=((p['lu'],p['hu']),(p['lv'],p['hv']),(c*p['lz'],c*p['hz']))
    weighted=s.expand(density*j)
    value=s.integrate(weighted,(w,*bounds[2]),(v,*bounds[1]),(u,*bounds[0]))
    return dict(trans=trans,inverse=inverse,matrix=matrix,det=determinant,j=j,
                f=density,density=weighted,bounds=bounds,value=s.simplify(value))


def guard(level,f,p):
    required={'a','b','c','d','n','lu','hu','lv','hv','lz','hz'}
    if set(p)!=required:raise ValueError('Explicit parameters require exactly '+', '.join(sorted(required)))
    for key in ('a','b','d'):
        if p[key].is_Integer is not True or p[key]==0 or abs(p[key])>4:raise ValueError('Nonzero integer coefficients of magnitude <=4 required')
    if p['c'] not in (s.Rational(1,2),s.Rational(1,3),s.Rational(1,4),s.Integer(2),s.Integer(3),s.Integer(4)):raise ValueError('c must be 1/2,1/3,1/4,2,3,4')
    if p['n'].is_Integer is not True or not 1<=p['n']<=3:raise ValueError('n must be 1..3')
    for lo,hi in [('lu','hu'),('lv','hv'),('lz','hz')]:
        if (p[hi]-p[lo]).is_positive is not True or abs(p[lo])>2*s.pi or abs(p[hi])>4*s.pi:raise ValueError('Ordered finite familiar bounds required')
    if level=='easy':
        if f!='power' or p['n']!=1 or p['lu']!=0 or p['lv']!=0 or p['lz']!=0:raise ValueError('Easy: linear density uv, all lower bounds zero')
        if abs(p['a'])>3 or abs(p['b'])>2 or abs(p['d'])>2 or any(p[k] not in (1,2,3) for k in ('hu','hv','hz')):raise ValueError('Easy arithmetic bounds')
    elif level=='moderate':
        if all(p[k]!=0 for k in ('lu','lv','lz')):raise ValueError('Moderate requires a zero lower endpoint; hard endpoints are disjoint')
        if f=='power' and p['n']!=2:raise ValueError('Moderate polynomial exponent is 2')
        if f=='power' and any(p[k]!=0 for k in ('lu','lv','lz')):raise ValueError('Moderate power lower bounds zero')
    elif level=='hard':
        if not all(p[k].is_positive is True for k in ('lu','lv','lz')):raise ValueError('Hard: all three strictly positive lower endpoints')
        if f=='power' and p['n']!=2:raise ValueError('Hard retains source polynomial exponent 2')
    else:raise ValueError('Unknown difficulty')
    # Bound number forms control the arithmetic workload, including explicit calls.
    angles=(0,s.pi/6,s.pi/3,s.pi/2,s.pi,3*s.pi/2,2*s.pi)
    trigaxes={'vcosu':('lu','hu'),'ucosv':('lv','hv'),'zcosu':('lu','hu'),'sinsin':('lu','hu','lv','hv')}.get(f,())
    for key in ('lu','hu','lv','hv','lz','hz'):
        if key in trigaxes:
            if p[key] not in angles:raise ValueError('Trigonometric endpoints must be familiar sixth/third/half/full turns')
        elif p[key].is_Integer is not True or not -1<=p[key]<=6:raise ValueError('Nontrig bounds are integers -1..6')
    if f=='exp' and (p['hu']>3 or p['lu']>2):raise ValueError('Exponential endpoints <=3')
    if level=='hard':
        if f in ('vcosu','zcosu') and s.sin(p['lu'])==0:raise ValueError('Hard lower cosine primitive must be nonzero')
        if f=='ucosv' and s.sin(p['lv'])==0:raise ValueError('Hard lower cosine primitive must be nonzero')
        if f=='sinsin' and (s.cos(p['lu'])==0 or s.cos(p['lv'])==0):raise ValueError('Hard lower sine primitives must be nonzero')
    if f=='sum' and p['c']>=1:raise ValueError('Sum keeps inverse integer w scale')
    if f!='sum' and p['c']<1:raise ValueError('Other families keep integer w scale')
    if f in ('vcosu','ucosv','sinsin') and p['b']<=0:raise ValueError('Quadratic shear b positive')


def sample(level,f,rng):
    p=dict(a=rng.choice((-3,-2,2,3)),b=rng.choice((2,3,4)),c=rng.choice((2,3,4)),d=rng.choice((-2,-1,1,2)),n=2,
           lu=0,hu=rng.choice((1,2,3)),lv=0,hv=rng.choice((1,2,3)),lz=0,hz=rng.choice((1,2,3)))
    if f=='sum':p['c']=rng.choice((s.Rational(1,2),s.Rational(1,3),s.Rational(1,4)))
    if level=='easy':p.update(a=rng.choice((-3,-2,2,3)),b=rng.choice((-2,-1,1,2)),n=1)
    if f in ('vcosu','zcosu'):p.update(lu=s.pi/6,hu=rng.choice((s.pi/2,s.pi,2*s.pi)))
    if f=='ucosv':p.update(lv=0,hv=s.pi/2,lz=-1)
    if f=='sinsin':p.update(lu=s.pi/2,hu=s.pi,lv=s.pi,hv=2*s.pi)
    if level=='hard':
        p.update(lu=1,hu=rng.choice((2,3)),lv=1,hv=rng.choice((2,3,4)),lz=1,hz=rng.choice((2,3,4)))
        if f in ('vcosu','zcosu'):p.update(lu=s.pi/6,hu=rng.choice((s.pi/2,s.pi,2*s.pi)))
        if f=='ucosv':p.update(lv=s.pi/6,hv=rng.choice((s.pi/2,s.pi,2*s.pi)))
        if f=='sinsin':p.update(lu=rng.choice((s.pi/6,s.pi/3)),hu=s.pi,lv=s.pi,hv=2*s.pi)
    return numeric(p)


def bank(f,p,m):
    """Complete family bank chosen before parameters, never a distractor pool.

    All operations are genuine displayed-method changes; their intent is authored.
    The entire instance is rejected if any complete scalar integral values collide.
    """
    I,J=m['value'],m['j']; bounds=m['bounds'];density=m['density']
    integrate=lambda q:s.simplify(s.integrate(q,(w,*bounds[2]),(v,*bounds[1]),(u,*bounds[0])))
    wrong=[('omit_inverse_jacobian',integrate(m['f'])),('use_forward_jacobian',integrate(m['f']*s.Abs(m['det'])))]
    if f=='power':wrong += [('omit_power_primitive_denominator',(p['n']+1)*I),('omit_w_bound_scale',I/p['c']) if p['n']==1 else ('omit_v_primitive_denominator',2*I)]
    elif f=='vcosu':wrong += [('differentiate_cos_instead_of_integrate',integrate(J*v*(-s.sin(u)))),('omit_v_primitive_denominator',2*I)]
    elif f=='ucosv':wrong += [('omit_u_primitive_denominator',2*I),('differentiate_cos_instead_of_integrate',integrate(J*u*(-s.sin(v))))]
    elif f=='sum':wrong += [('omit_u_summand',integrate(J*w)),('omit_w_summand',integrate(J*u))]
    elif f=='exp':
        wrong += [('omit_lower_exponential_endpoint',s.simplify(J*s.exp(p['hu'])*(p['hv']**2-p['lv']**2)/2*(bounds[2][1]-bounds[2][0]))),('omit_v_primitive_denominator',2*I)]
    elif f=='zcosu':wrong += [('omit_z_inverse_scale_squared',integrate(J*w*w*s.cos(u))),('omit_w_primitive_denominator',3*I)]
    elif f=='sinsin':
        wrong += [('omit_w_bound_scale',s.simplify(I/p['c'])),('reverse_one_cosine_endpoint_difference',-I)]
    values=[I]+[a for _,a in wrong]
    if any(a.has(s.nan,s.zoo,s.oo,-s.oo) for a in values):raise SampleRejected('Invalid whole bank')
    if any(s.simplify(a-b)==0 for i,a in enumerate(values) for b in values[i+1:]):raise SampleRejected('Equivalent complete scalar options')
    return [('correct',I)]+wrong


def normal_prompt(f,p,m):
    trans=m['trans'];F=m['f'].subs(dict(zip(UVW,trans)),simultaneous=True)
    change=',\\quad '.join(str(t)+'='+tex(e) for t,e in zip(UVW,trans))
    region=r'R=\{(x,y,z):'+',\\quad '.join(tex(lo)+r'\le '+tex(e)+r'\le '+tex(hi) for e,(lo,hi) in zip((trans[0],trans[1],z),((p['lu'],p['hu']),(p['lv'],p['hv']),(p['lz'],p['hz']))))+r'\}.'
    prompt='Use the change of variables \n\n'+block(change)+'\n\nto evaluate the triple integral\n\n'+block(r'\iiint_R '+group(tex(F))+r'\,\mathrm{d}V,')+'\n\n \nwhere the region $R$ is given by\n\n'+block(region)
    return prompt,change,F


def normal_solution(f,p,m,change,F):
    """Source four-step prose, full Jacobian expansion and successive primitives.

    Authored arithmetic expansion adds individual evaluated primitive components
    at BOTH endpoints before collection. The source direct/separable sequence is
    preserved exactly in the public evidence profiles, including its omissions.
    """
    intro=RAW['17592186374125']['solution_prefix'].replace(RAW['17592186374125']['change'],change)
    # Everything before Step 1 is shared source prose and the same formal formula.
    bounds=m['bounds'];mat=m['matrix'];D=m['det'];J=m['j']
    domain=r'\Delta=\{(u,v,w):'+',\\quad '.join(tex(lo)+r'\le '+str(t)+r'\le '+tex(hi) for t,(lo,hi) in zip(UVW,bounds))+r'\}.'
    matrix=lambda cells:r'\begin{vmatrix}'+r' \\ '.join(' & '.join(row) for row in cells)+r'\end{vmatrix}'
    formal=matrix([[r'\frac{\partial '+str(t)+r'}{\partial '+str(q)+'}' for q in XYZ] for t in UVW])
    numericmat=matrix([[tex(mat[i,j]) for j in range(3)] for i in range(3)])
    rows=[(r'\frac{\partial(u,v,w)}{\partial(x,y,z)}',formal),('',numericmat)]
    # Third row is (0,0,c); keep cofactor, minor products and their subtraction.
    minor=matrix([[tex(mat[i,j]) for j in range(2)] for i in range(2)])
    rows += [('',group(tex(mat[2,2]))+r'(-1)^{3+3}'+minor),('',group(tex(mat[2,2]))+group(group(tex(mat[0,0]))+r'\cdot '+group(tex(mat[1,1]))+'-'+group(tex(mat[0,1]))+r'\cdot '+group(tex(mat[1,0])))),('',tex(D)+'.')]
    sol=intro+'**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$ \n\nOur domain in the $uvw$-space is\n\n'+block(domain)+'\n\n**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$\n\nThe Jacobian determinant corresponding to ${T}^{-1}$ is\n\n'+aligned(rows)
    sol+='\n\n**Step 3**: Compute the Jacobian determinant corresponding to $T:$\n\nThe Jacobian determinant corresponding to $T$ is\n\n'+block(r'\frac{\partial(x,y,z)}{\partial(u,v,w)}=\left(\frac{\partial(u,v,w)}{\partial(x,y,z)}\right)^{-1}='+tex(1/D)+'.')
    sol+='\n\nNote that $\\frac{∂(x,y,z)}{∂(u,v,w)}\\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$'
    sol+='\n\n**Step 4**: Perform the change of variables:\n\n'
    initial=[(r'\iiint_R '+group(tex(F))+r'\,\mathrm{d}V',r'\iiint_\Delta '+group(tex(m['f']))+r'\cdot \left|'+tex(1/D)+r'\right|\,\mathrm{d}u\mathrm{d}v\mathrm{d}w'),('',r'\iiint_\Delta '+group(tex(m['density']))+r'\,\mathrm{d}u\mathrm{d}v\mathrm{d}w'),('',integral(bounds,tex(m['density'])))]
    stages=[]; current=m['density'];arithmetic=initial
    for pos in (2,1,0):
        t=UVW[pos];lo,hi=bounds[pos]
        primitive=s.integrate(current,t);terms=s.Add.make_args(s.expand(primitive))
        substitution=[];evaluated=[];components=[]
        for term in terms:
            top=term.subs(t,hi);bottom=term.subs(t,lo)
            # Unevaluated substitution keeps exponent/endpoint structure visible.
            substitution.append(group(tex(term).replace(str(t),group(tex(hi))))+'-'+group(tex(term).replace(str(t),group(tex(lo)))))
            evaluated.append(difftex(top,bottom));components.append((top,bottom))
        endpoint=s.simplify(primitive.subs(t,hi)-primitive.subs(t,lo))
        wrap=lambda expr:integral(bounds[:pos],expr,UVW[:pos]) if pos else expr
        arithmetic += [('',wrap(r'\left['+tex(primitive)+r'\right]_{'+str(t)+'='+tex(lo)+'}^{'+str(t)+'='+tex(hi)+'}')),('',wrap('+'.join(substitution))),('',wrap('+'.join(evaluated))),('',wrap(tex(endpoint)))]
        stages.append(dict(variable=str(t),input=str(current),primitive=str(primitive),terms=[str(a) for a in terms],components=[[str(a),str(b)] for a,b in components],result=str(endpoint)))
        current=endpoint
    sol+=aligned(arithmetic)
    return sol,stages


def assemble(level,f,p,seed,profile,problem,solution,values,correct_index,raw_recipe=None,math=None,stages=None):
    keypresence=raw_recipe['question_keys'] if raw_recipe else None
    if raw_recipe is None:problem=normalize_prose(problem);solution=normalize_prose(solution);values=[(v,normalize_tex(t))for v,t in values]
    identity=stable(dict(version=VERSION,level=(level if not raw_recipe else raw_recipe.get('difficulty')),problem=problem,solution=solution,bank=sorted(q for _,q in values),correct=(values[correct_index][1] if correct_index is not None else None),keys=keypresence))
    qid=uid(identity);fid=uid(identity+':selection')
    answers=[{':answer/id':uid(fid+':'+q),':answer/type':':answer.type/math',':answer/value':q} for _,q in values]
    correct=answers[correct_index][':answer/id'] if correct_index is not None else None
    random.Random(seed).shuffle(answers)
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if correct is not None:field[':answer-field/correct']=[':answer/id',correct]
    question={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
    if not raw_recipe or ':question/difficulty' in keypresence:question[':question/difficulty']=':question.difficulty/'+level
    if solution is not None:question[':question/worked-solution']=solution
    if math:
        fingerprint=stable(dict(trans=[str(a) for a in math['trans']],integrand=str(math['f']),bounds=[[str(a) for a in b] for b in math['bounds']]))
    else:fingerprint=stable(dict(family=f,parameters=serialized(p)))
    generation=dict(version=VERSION,python_version=sys.version.split()[0],sympy_version=s.__version__,seed=seed,template=f,parameters=serialized(p),bank_profile=profile,bank_origin='opaque_observed' if raw_recipe else 'authored_method',source_basis=1356,source_lineage=SOURCE['lineage'],source_ids=([raw_recipe['source_id']] if raw_recipe else [str(k) for k,q in SOURCE_FAMILY.items() if q==f]),evidence_only=bool(raw_recipe),eligible_for_learning=not bool(raw_recipe),authored_level=level!='moderate',plot_rating='none',parameter_fingerprint=fingerprint,content_fingerprint=identity,recipes=[name for name,_ in values],domain='Globally bijective polynomial/linear shear; constant nonzero determinant; ordered bounded box.',stages=stages or [])
    if math:generation['math']={k:([[str(c) for c in row] for row in math[k]] if k=='bounds' else [str(a) for a in math[k]] if k in ('trans','inverse') else str(math[k])) for k in ('trans','inverse','det','j','f','density','bounds','value')}
    if raw_recipe:generation['raw_presence']={'question':keypresence,'field':raw_recipe['field_keys']};generation['raw_defects']=raw_recipe.get('defects',[])
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':generation}


def scale_fragment(text,k):
    """Formatting of an actual mathematical coefficient, not literal question replay."""
    return text if k==1 else group(tex(k))+r'\cdot '+group(text)


def replay(level,template,seed,parameters,profile):
    source_id=profile.removeprefix('raw-')
    if source_id not in RAW:raise ValueError('Unknown public raw evidence profile')
    r=RAW[source_id]
    if template is not None and template!=r['family']:raise ValueError('Profile/template mismatch')
    if level!='moderate':raise ValueError('Observed raw profiles use moderate routing; unrated records retain omission')
    p=numeric(parameters or {'scale':1})
    if set(p)!={'scale'} or p['scale'].is_Integer is not True or p['scale']==0 or abs(p['scale'])>6:raise ValueError('Raw replay scale must be a nonzero integer of magnitude <=6')
    k=p['scale'];integrand=scale_fragment(r['integrand'],k)
    problem=r['prompt_mask'].replace('{{integrand}}',integrand)
    solution=None
    if 'solution_mask' in r:
        solution=r['solution_mask'].replace('{{integrand}}',integrand)
        for i,stage in enumerate(r['arithmetic_nodes']):solution=solution.replace('{{stage_'+str(i)+'}}',scale_fragment(stage,k))
    values=[('opaque_observed_'+str(i),scale_fragment(q,k)) for i,q in enumerate(r['choice_atoms'])]
    return assemble(level,r['family'],p,seed,profile,problem,solution,values,r.get('correct_index'),raw_recipe=r)


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in LEVELS:raise ValueError('Difficulty must be easy, moderate, or hard')
    if field_type not in (None,'radio'):raise ValueError('This KP supports observed radio fields only')
    if profile and profile.startswith('raw-'):return replay(level,template,seed,parameters,profile)
    if profile not in (None,'method'):raise ValueError('Use method or an explicit raw-<source-id> evidence profile')
    eligible=('power',) if level=='easy' else FAMILIES
    rng=random.Random(seed);f=template or rng.choice(eligible)
    if f not in eligible:raise ValueError('Unsupported family at this level')
    # Family and complete bank are selected BEFORE any parameter sampling.
    for _ in range(128):
        p=numeric(parameters) if parameters is not None else sample(level,f,rng)
        guard(level,f,p);m=model(f,p)
        try:choices=bank(f,p,m)
        except SampleRejected:
            if parameters is not None:raise
            continue
        problem,change,F=normal_prompt(f,p,m);solution,stages=normal_solution(f,p,m,change,F)
        return assemble(level,f,p,seed,'method',problem,solution,[(name,tex(value)) for name,value in choices],0,math=m,stages=stages)
    raise SampleRejected('Whole-bank sampling exhausted')

# EASY — authored reduced workload: linear uv density; three zero endpoints,
# one product of two elementary primitives and one constant-length integral.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE — all seven source-shaped families; two density factors or a two-term
# sum, constant Jacobian, familiar trig/exponential endpoints, at least one zero.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD — authored ALL-THREE-ENDPOINT bookkeeping demand: every successive
# primitive has a nonzero lower endpoint, evaluated separately before collecting.
# Same source operations and arithmetic ceiling; no new integration method.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)


def markdown(r):
    q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
    lines=['## '+('Original evidence replay' if g['evidence_only'] else 'Generated variant')+' / '+g['template']+' / '+q.get(':question/difficulty','unrated evidence').split('/')[-1],'',q[':question/problem'],'']
    for i,a in enumerate(f[':answer-field/choices']):lines.append('- '+chr(65+i)+'. $'+a[':answer/value']+'$')
    lines+=['','Correct: '+(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) if ':answer-field/correct' in f else 'absent in raw source'),'',q.get(':question/worked-solution','Worked solution absent in raw source.')]
    return '\n'.join(lines)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template',choices=FAMILIES);parser.add_argument('--profile')
    a=parser.parse_args()
    if a.count<1:parser.error('count must be positive')
    records=[generate(level,a.seed+i,a.template,profile=a.profile) for level in (LEVELS if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
