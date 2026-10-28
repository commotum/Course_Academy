#!/usr/bin/env python3
"""Portable center-and-point circle generator.

Moderate: source solution stages with an authored five-option cross-product bank.
Original complete source banks and the unkeyed evidence bank remain available
through replay(), at original parameters; see instructional-account.md.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, random, re, sys, uuid
from math_format import normalize_prose, normalize_tex, checked_math_content
from renderer import render
from pathlib import Path
import sympy as sp

KP_ID=17592186087768
KP_UUID='3520d323-c6a4-5bce-bac1-1f4c02bd0068'
TITLE='Finding the Equation of a Circle Given the Center and a Point on the Circle'
VERSION='circle-center-point-portable-v3'
RENDER_VERSION='Matplotlib-v5-measured-label-placement'
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['material']['kp'][':knowledge-point/questions']}
PROVENANCE={k:SOURCE[k] for k in ('database','lineage','basis','source_sha256')}
x,y=sp.symbols('x y',real=True)
PROFILES={
 'bank-q-54215':['correct','reverse_both_radius','radius','reverse_x_point_y','point_y_reverse'],
 'bank-q-72616':['reverse_y','correct','radius','reverse_both','reverse_both_radius'],
 'bank-q-117096':['reverse_both_radius','reverse_y','correct','radius','reverse_both'],
 'bank-q-117099':['reverse_y','radius','correct','reverse_both_radius','reverse_both'],
 'bank-q-72617':['correct','reverse_x_radius','reverse_x','radius','reverse_x_double_root'],
 'bank-q-72619':['reverse_y','reverse_both','reverse_both_radius','radius','correct'],
 'bank-q-72621':['reverse_y_radius','correct','reverse_x','radius','reverse_x_radius'],
 'authored-easy':['correct','reverse_x','center_point','radius','omit_vertical_square'],
 'authored-hard':['correct','reverse_y','reverse_both','radius','reverse_both_radius'],
}
DEFAULT_MODERATE_PROFILES=tuple('bank-'+s for s,q in QUESTIONS.items() if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/moderate')
TEMPLATES={
 'integer_center_first': ['q-54215'],
 'radical_simplified': ['q-117096','q-117099'],
 'integer_signed': ['q-72617'],
 'radical_unsimplified': ['q-72619','q-72621'],
 'incomplete_radio': ['q-72616'],
 'authored_easy': [], 'authored_hard': [],
}
SOURCE_TEMPLATE={s:t for t,ss in TEMPLATES.items() for s in ss}

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def uid(value): return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(value)))
def tex(value): return sp.latex(sp.sympify(value)).replace(' \\sqrt',r'\sqrt')
def coord(v): return '('+tex(v)+')' if v<0 else tex(v)
def shift(v,c):
    if c==0:return v+'^{2}'
    return '('+v+('-' if c>0 else '+')+tex(abs(c))+')^{2}'
def equation(h,k,R): return shift('x',h)+'+'+shift('y',k)+'='+tex(R)
def residual(h,k,R):return sp.expand((x-h)**2+(y-k)**2-R)

def parse_parameters(p):
    if not isinstance(p,dict) or set(p)!={'h','k','u','v'}:raise ValueError('Require exactly h, k, u, v')
    out={}
    for key,val in p.items():
        if isinstance(val,bool) or isinstance(val,float):raise ValueError('Use exact integer/rational coordinates')
        try:q=sp.Rational(val)
        except (TypeError,ValueError):raise ValueError('Coordinates must be exact rationals')
        if not q.is_finite:raise ValueError('Nonfinite coordinates')
        out[key]=q
    return out

def source_parameters(source_id):
    text=QUESTIONS[source_id][':question/problem']
    m=re.search(r'C\(([-\d]+),\s*([-\d]+)\).*?X\(([-\d]+),\s*([-\d]+)\)',text,re.S)
    return dict(zip(('h','k','u','v'),map(sp.Rational,m.groups())))

def guard(level,p,profile):
    h,k,u,v=(p[key] for key in ('h','k','u','v'));dx=u-h;dy=v-k;R=dx**2+dy**2
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    if profile not in PROFILES:raise ValueError('Unknown complete profile')
    if dx==0 or dy==0 or R<=1:raise ValueError('Both nonzero distance components and R>1 required')
    if level=='easy':
        if profile!='authored-easy':raise ValueError('Easy requires its complete authored profile')
        if not all(q.q==1 for q in p.values()) or k!=0 or not 1<=abs(h)<=5 or sorted((abs(dx),abs(dy))) not in ([3,4],[6,8]):raise ValueError('Easy: k=0, nonzero integer h <=5, 3-4 or 6-8 offsets')
    elif level=='moderate':
        if profile.startswith('authored-'):raise ValueError('Moderate uses observed operation banks')
        if not all(q.q==1 for q in p.values()) or not (1<=abs(h)<=5 and 1<=abs(k)<=5 and 1<=abs(dx)<=8 and 1<=abs(dy)<=8 and R<=100):raise ValueError('Moderate: nonzero integer centers <=5; offsets <=8; R<=100')
        is_square=math.isqrt(int(R))**2==R
        if profile in ('bank-q-54215','bank-q-72617') and not is_square:raise ValueError('Integer-radius source masks require a perfect-square squared radius')
        if profile in ('bank-q-117096','bank-q-117099') and (is_square or not any(int(R)%(f*f)==0 for f in range(2,math.isqrt(int(R))+1))):raise ValueError('Simplified-radical source masks require nonsquare R with a nonunit square factor')
        if profile in ('bank-q-72619','bank-q-72621') and is_square:raise ValueError('Unsimplified-radical source masks require nonsquare R')
    else:
        if profile!='authored-hard':raise ValueError('Hard requires its complete authored profile')
        if not all(q.q==2 for q in (h,k,dx,dy)) or not (abs(h)<=sp.Rational(9,2) and abs(k)<=sp.Rational(9,2) and abs(dx)<=sp.Rational(9,2) and abs(dy)<=sp.Rational(9,2)) or R.q==1:raise ValueError('Hard: noninteger half-integer centers and offsets <=9/2; noninteger R')
    return R

def bank(p,profile):
    h,k,u,v=(p[key] for key in ('h','k','u','v'));R=(u-h)**2+(v-k)**2;r=sp.sqrt(R)
    operations={
      'correct':(h,k,R),'reverse_x':(-h,k,R),'reverse_y':(h,-k,R),'reverse_both':(-h,-k,R),
      'radius':(h,k,r),'reverse_x_radius':(-h,k,r),'reverse_y_radius':(h,-k,r),'reverse_both_radius':(-h,-k,r),
      'reverse_x_double_root':(-h,k,sp.sqrt(r)),
      'reverse_x_point_y':(-h,v,R),'point_y_reverse':(h,-v,R),
      'center_point':(u,v,R),'omit_vertical_square':(h,k,(u-h)**2),
    }
    result=[(label,operations[label]) for label in PROFILES[profile]]
    polys=[residual(*triple) for _,triple in result]
    # Every complete residual is monic in x^2. Equality therefore also detects
    # equation equivalence up to any nonzero scalar, without radical coercion.
    for i,P in enumerate(polys):
        for Q in polys[:i]:
            if sp.simplify(P-Q)==0:raise ValueError('Ambiguous complete bank; reject whole instance')
    return result

def radius_block(p,source_id=None):
    h,k,u,v=(p[key] for key in ('h','k','u','v'));R=(u-h)**2+(v-k)**2;r=sp.sqrt(R)
    if source_id=='q-54215':
        initial=r'\sqrt{{('+tex(h)+'-'+coord(u)+r')}^{2}+{('+tex(k)+'-'+coord(v)+r')}^{2}}'
        middle=r'\sqrt{{'+tex(abs(h-u))+r'}^{2}+{'+tex(abs(k-v))+r'}^{2}}'
        rows=[initial,middle,r'\sqrt{'+tex(R)+'}',tex(r)+'.']
    elif source_id in ('q-117096','q-117099'):
        initial=r'\sqrt{('+tex(u)+'-'+coord(h)+r')^{2}+('+tex(v)+'-'+coord(k)+r')^{2}}'
        middle=r'\sqrt{{'+tex(abs(u-h))+r'}^{2}+{'+tex(abs(v-k))+r'}^{2}}'
        rows=[initial,middle,tex(r)+'.']
    else:
        initial=r'\sqrt{{('+tex(u)+'-'+coord(h)+r')}^{2}+{('+tex(v)+'-'+coord(k)+r')}^{2}}'
        def square(a):return '('+tex(a)+')^{2}' if a<0 else '{'+tex(a)+'}^{2}'
        middle=r'\sqrt{'+square(u-h)+'+'+square(v-k)+'}'
        rows=[initial,middle,r'\sqrt{'+tex(R)+'}'+('.' if source_id in ('q-72619','q-72621') else '')]
        if source_id not in ('q-72619','q-72621'):rows.append(tex(r)+'.')
    return r'\begin{aligned}CX & ='+r' \\  & ='.join(rows)+r'\end{aligned}'

def equation_block(p,source_id=None):
    h,k,u,v=(p[key] for key in ('h','k','u','v'));R=(u-h)**2+(v-k)**2;r=sp.sqrt(R)
    raw='(x-'+coord(h)+')^{2}+(y-'+coord(k)+')^{2}'
    if source_id in ('q-72619','q-72621'):radius=r'(\sqrt{'+tex(R)+'})^{2}'
    elif source_id in ('q-117096','q-117099'):radius='{('+tex(r)+')}^{2}'
    elif source_id=='q-54215':radius='('+tex(r)+')^{2}'
    elif source_id=='q-72617':radius='{'+tex(r)+'}^{2}'
    else:radius='('+tex(r)+')^{2}'
    return r'\begin{aligned}(x-a)^{2}+(y-b)^{2} & ={r}^{2} \\ '+raw+' & ='+radius+r' \\ '+equation(h,k,R).replace('=',' & =')+r'\end{aligned}'

def solution(p,source_id=None):
    # Source sentences and structural masks are fixed; all mathematical rows
    # are recomputed. No source payload-return branch or answer lookup is used.
    return 'The general equation of a circle with radius $r$ centered at the point $(a,b)$ is\n\n$$\n(x-a)^{2}+(y-b)^{2}={r}^{2}.\n$$\n\nThe length of the radius is \n\n$$\n'+radius_block(p,source_id)+'\n$$\n\nSo, our circle is generated by the following equation:\n\n$$\n'+equation_block(p,source_id)+'\n$$'

def render_plots(p,source_id=None):
    geometry=[str(p[key]) for key in ('h','k','u','v')]
    if source_id and p==source_parameters(source_id):
        ref=re.search(r'!\[\]\((.*?)\)',QUESTIONS[source_id][':question/problem'])[1]
        return ref,{'renderer':'source-raster','coordinates':geometry,'role':'prompt'}
    root=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not root:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required for new figures')
    out=Path(root).resolve()/('circle-'+digest([RENDER_VERSION,geometry])+'.png')
    out.parent.mkdir(parents=True,exist_ok=True)
    h,k,u,v=(p[key] for key in ('h','k','u','v'));R=(u-h)**2+(v-k)**2
    data={'coordinates':geometry,'radius':str(float(sp.sqrt(R))),'labels':['C('+tex(h)+','+tex(k)+')','X('+tex(u)+','+tex(v)+')']}
    if not out.exists() or not out.with_suffix('.json').exists():render(data,out)
    side=json.loads(out.with_suffix('.json').read_text())
    if side['coordinates']!=geometry:raise AssertionError('Plot cache geometry mismatch')
    return str(out),{'path':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'role':'prompt',**side}

def sample(level,rng,profile):
    for _ in range(2000):
        if level=='easy':
            h=rng.choice([i for i in range(-5,6) if i]);k=0;d=rng.choice([(3,4),(4,3),(6,8),(8,6)])
            dx,dy=[rng.choice([-1,1])*a for a in d]
        elif level=='moderate':
            h,k=[rng.choice([i for i in range(-5,6) if i]) for _ in range(2)];dx,dy=[rng.choice([i for i in range(-8,9) if i]) for _ in range(2)]
        else:
            h,k,dx,dy=[sp.Rational(rng.choice([-9,-7,-5,-3,-1,1,3,5,7,9]),2) for _ in range(4)]
        p=parse_parameters({'h':h,'k':k,'u':h+dx,'v':k+dy})
        try:guard(level,p,profile);bank(p,profile);return p
        except ValueError:continue
    raise RuntimeError('Complete eligible bank sampling exhausted')

def replay(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields supported')
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    default_profile_choice=profile is None and template is None and level=='moderate'
    if profile is None:
        if template in TEMPLATES and TEMPLATES[template]:profile='bank-'+TEMPLATES[template][0]
        elif level=='moderate':profile=rng.choice(DEFAULT_MODERATE_PROFILES)
        else:profile={'easy':'authored-easy','hard':'authored-hard'}[level]
    if profile not in PROFILES:raise ValueError('Unknown complete profile')
    source_id=profile[5:] if profile.startswith('bank-') else None
    expected_template=SOURCE_TEMPLATE[source_id] if source_id else ('authored_easy' if level=='easy' else 'authored_hard')
    if template is not None and template!=expected_template:raise ValueError('Template/profile mismatch')
    template=expected_template
    p=parse_parameters(parameters) if parameters is not None else sample(level,rng,profile)
    R=guard(level,p,profile);options=bank(p,profile)
    image_ref,plot=render_plots(p,source_id)
    h,k,u,v=(p[key] for key in ('h','k','u','v'))
    space=' ' if source_id=='q-72616' else ''
    prompt='![]('+image_ref+')\n\nThe circle above is centered at $C('+tex(h)+','+space+tex(k)+')$ and the point $X('+tex(u)+','+space+tex(v)+')$ lies on the circumference. Find the equation of the circle.'
    fixed_solution=solution(p,source_id)
    # Preserve spelling of the spaced legacy bank using a formatting profile.
    def answer_text(triple):
        value=equation(*triple)
        if source_id=='q-72616':value=value.replace('+',' + ').replace('-',' - ').replace('=',' = ')
        return value
    values=[normalize_tex(answer_text(triple)) for _,triple in options]
    prompt=normalize_prose(prompt);fixed_solution=normalize_prose(fixed_solution)
    raw_incomplete=source_id=='q-72616'
    q={':question/problem':prompt}
    if not raw_incomplete:q[':question/difficulty']=':question.difficulty/'+level;q[':question/worked-solution']=fixed_solution
    identity=digest([VERSION,level if not raw_incomplete else None,prompt,q.get(':question/worked-solution'),sorted(values),'radio','selection',not raw_incomplete])
    qid=uid(['question',identity]);fid=uid([qid,'selection'])
    answers=[{':answer/id':uid([fid,value]),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    correct_index=PROFILES[profile].index('correct')
    if not raw_incomplete:field[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
    rng.shuffle(answers)
    q[':question/id']=qid;q[':question/answer-fields']=[field]
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
        'version':VERSION,'seed':seed,'difficulty':level,'difficulty_origin':'observed' if source_id and not raw_incomplete else 'authored level assignment' if raw_incomplete else 'authored extension',
        'template':template,'bank_profile':profile,'profile_selection':'seeded choice among all six rated source banks before parameter sampling' if default_profile_choice else 'explicit profile or template / fixed authored level profile','parameters':{key:str(value) for key,value in p.items()},
        'source':PROVENANCE,'source_ids':[source_id] if source_id else ['e-6150','q-54215','q-117096','q-72621'],
        'domains':{'center_and_point':'exact rational coordinates','radius_squared':str(R),'equal_workload_bounds':{'easy':'k=0; integer center <=5; nonzero 3-4 or 6-8 offsets','moderate':'nonzero integer centers <=5, offsets <=8, R<=100; integer masks require square R; simplified-radical masks require nonsquare R with a nonunit square factor; unsimplified-radical masks require nonsquare R','hard':'noninteger half-integer centers and offsets <=9/2; noninteger R'}[level]},
        'recipes':PROFILES[profile],'eligible_for_learning':not raw_incomplete,'evidence_only':raw_incomplete,
        'inferred_correct_value':equation(h,k,R) if raw_incomplete else None,
        'mathematical_fingerprint':digest(['center-and-point-distance-equation',*map(str,(h,k,u,v))]),
        'content_fingerprint':identity,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'renderer':plot.get('versions',{'renderer':'captured source raster'})},'plot':plot}}

def complete_incomplete(record):
    """Explicit authored repair, preserving raw public replay as evidence."""
    record=json.loads(json.dumps(record));g=record['generation'];q=record['question'];p=parse_parameters(g['parameters'])
    if g['bank_profile']!='bank-q-72616':raise ValueError('Only incomplete captured source may be completed')
    radius_squared=(p['u']-p['h'])**2+(p['v']-p['k'])**2
    # No original solution exists. Author the closest supported radius mask,
    # avoiding a repeated sqrt(R) row when the radius remains irrational.
    completion_mask='integer_signed' if math.isqrt(int(radius_squared))**2==radius_squared else 'radical_unsimplified'
    q[':question/difficulty']=':question.difficulty/moderate';q[':question/worked-solution']=solution(p,'q-72617' if completion_mask=='integer_signed' else 'q-72621')
    f=q[':question/answer-fields'][0]
    correct=next(a for a in f[':answer-field/choices'] if equation_equivalent(a[':answer/value'],g['inferred_correct_value']))
    f[':answer-field/correct']=[':answer/id',correct[':answer/id']]
    identity=digest([VERSION,'authored completion',q[':question/problem'],q[':question/worked-solution'],sorted(a[':answer/value'] for a in f[':answer-field/choices'])])
    q[':question/id']=uid(identity);f[':answer-field/id']=uid([q[':question/id'],'selection'])
    for a in f[':answer-field/choices']:a[':answer/id']=uid([f[':answer-field/id'],a[':answer/value']])
    f[':answer-field/correct']=[':answer/id',correct[':answer/id']]
    g.update({'content_fingerprint':identity,'eligible_for_learning':True,'evidence_only':False,'completion_solution_mask':completion_mask,'presentation_repair':'authored difficulty, independently inferred correct designation and authored solution'})
    return record

def parse_math(value):
    """Small exact parser for displayed circle arithmetic, independent of recipes.

    Supports only the public expression language (rational numbers, square roots,
    x/y/a/b/r, sums, products and powers). No external parser installation.
    """
    value=value.replace(r'\left','').replace(r'\right','').strip().rstrip('.')
    pattern=r'\\(?:sqrt|frac|dfrac)|[xyabr]|\d+|[\[\]{}()+\-*/^]'
    tokens=re.findall(pattern,value)
    if ''.join(tokens)!=re.sub(r'\s+','',value):raise ValueError('Unsupported displayed math: '+value)
    i=0
    def peek():return tokens[i] if i<len(tokens) else None
    def take():
        nonlocal i
        if i>=len(tokens):raise ValueError('Unexpected end of expression')
        t=tokens[i];i+=1;return t
    def atom():
        t=take()
        if t in ('(','{'):
            e=addition();close=')' if t=='(' else '}'
            if take()!=close:raise ValueError('Unbalanced displayed group')
            return e
        if t==r'\sqrt':
            index=sp.Integer(2)
            if peek()=='[':
                take();index=sp.Integer(take())
                if take()!=']':raise ValueError('Unbalanced root index')
            return atom()**(1/index)
        if t in (r'\frac',r'\dfrac'):return atom()/atom()
        if t.isdigit():return sp.Integer(t)
        if t in ('x','y','a','b','r'):return sp.Symbol(t,real=True)
        raise ValueError('Invalid expression atom '+t)
    def power():
        e=atom()
        if peek()=='^':take();e=e**unary()
        return e
    def unary():
        if peek()=='+':take();return unary()
        if peek()=='-':take();return -unary()
        return power()
    def multiplication():
        e=unary()
        while peek() not in (None,'+','-',')','}'):
            t=peek()
            if t=='*':take();e*=unary()
            elif t=='/':take();e/=unary()
            else:e*=unary()
        return e
    def addition():
        e=multiplication()
        while peek() in ('+','-'):
            t=take();n=multiplication();e=e+n if t=='+' else e-n
        return e
    result=addition()
    if i!=len(tokens):raise ValueError('Unused displayed tokens')
    return result

def equation_equivalent(a,b):
    def poly(s):
        lhs,rhs=s.split('=');return sp.expand(parse_math(lhs)-parse_math(rhs))
    P,Q=poly(a),poly(b)
    # EX handles all algebraic coefficients from the complete bank.
    P,Q=sp.Poly(P,*sorted(P.free_symbols|Q.free_symbols,key=str),domain='EX'),sp.Poly(Q,*sorted(P.free_symbols|Q.free_symbols,key=str),domain='EX')
    return all(sp.simplify(c)==0 for c in (P*Q.LC()-Q*P.LC()).all_coeffs()) if len(P.gens)==1 else sp.simplify(P.as_expr()*Q.LC()-Q.as_expr()*P.LC())==0


# Authored same-method bank extension. These are complete cross-product banks,
# not pools of options selected until enough happen to survive.
SIGN_CASES=('x','y','both')
OFFSET_PAIRS={R:tuple((dx,dy) for dx in range(-8,9) for dy in range(-8,9)
                     if dx and dy and dx*dx+dy*dy==R)
              for R in range(18,101)}
OFFSET_PAIRS={R:pairs for R,pairs in OFFSET_PAIRS.items() if pairs}
RADIUS_DOMAIN=tuple(OFFSET_PAIRS)

def arithmetic_bank(p,roles):
    h,k,u,v=(p[key] for key in ('h','k','u','v'));R=(u-h)**2+(v-k)**2
    radii=roles['radii']
    target=[c for c in range(3) if c!=roles['omit_column']][roles['target_side']]
    if (len(radii)!=3 or sorted(set(radii))!=radii or any(r not in RADIUS_DOMAIN for r in radii)
        or radii[target]!=R):raise ValueError('Radius candidates incompatible with target geometry')
    case=roles['wrong_center'];wrong=(-h if case in ('x','both') else h,-k if case in ('y','both') else k)
    if wrong==(h,k):raise ValueError('Sign case requires a distinct center')
    omitted=(roles['omit_group'],roles['omit_column'])
    out=[('correct' if (g,c)==(0,target) else f'group-{g}-radius-{c}',(*center,radii[c]))
         for g,center in enumerate(((h,k),wrong)) for c in range(3) if (g,c)!=omitted]
    assert len(out)==5
    return out

@checked_math_content
def generate(level='moderate',seed=0,parameters=None,roles=None,source_id=None):
    if level!='moderate':raise ValueError('Only source-supported moderate generation is available')
    if source_id:
        if source_id not in QUESTIONS:raise ValueError('Unknown source id')
        if source_id=='q-72616':raise ValueError('Unkeyed source is evidence-only; use replay()')
        return replay(level,seed,parameters=parameters or source_parameters(source_id),profile='bank-'+source_id)
    rng=random.Random(seed)
    if roles is None:
        roles={'omit_group':rng.randrange(2),'omit_column':rng.randrange(3),
               'target_side':rng.randrange(2),'wrong_center':rng.choice(SIGN_CASES)}
    roles=json.loads(json.dumps(roles))
    if set(roles)-{'radii'}!={'omit_group','omit_column','target_side','wrong_center'} or roles['omit_group'] not in (0,1) or roles['omit_column'] not in (0,1,2) or roles['target_side'] not in (0,1) or roles['wrong_center'] not in SIGN_CASES:raise ValueError('Invalid bank roles')
    if 'radii' not in roles:
        if parameters is not None:raise ValueError('Explicit geometry requires explicit candidate radii')
        roles['radii']=sorted(rng.sample(RADIUS_DOMAIN,3))
    rejections={};attempts=0
    for attempts in range(1,2001):
        if parameters is None:
            nonzero=[i for i in range(-5,6) if i]
            h,k=[rng.choice(nonzero) for _ in range(2)]
            target=[c for c in range(3) if c!=roles['omit_column']][roles['target_side']]
            dx,dy=rng.choice(OFFSET_PAIRS[roles['radii'][target]])
            p=parse_parameters(dict(h=h,k=k,u=h+dx,v=k+dy))
        else:p=parse_parameters(parameters)
        try:
            # Generic moderate guard, without the source-mask square constraints.
            R=guard(level,p,'bank-q-72616')
            options=arithmetic_bank(p,roles)
            image_ref,plot=render_plots(p)
            break
        except (ValueError,RuntimeError) as exc:
            if parameters is not None:raise
            reason=str(exc);rejections[reason]=rejections.get(reason,0)+1
    else:raise RuntimeError('Role-preserving sampler exhausted')
    h,k,u,v=(p[key] for key in ('h','k','u','v'))
    prompt=normalize_prose('![]('+image_ref+')\n\nThe circle above is centered at $C('+tex(h)+','+tex(k)+')$ and the point $X('+tex(u)+','+tex(v)+')$ lies on the circumference. Find the equation of the circle.')
    square=math.isqrt(int(R))**2==R
    if square:mask='q-72617'
    elif any(int(R)%(f*f)==0 for f in range(2,math.isqrt(int(R))+1)):mask='q-117096'
    else:mask='q-72621'
    worked=normalize_prose(solution(p,mask))
    values=[normalize_tex(equation(*triple)) for _,triple in options]
    # Image path is a delivery detail, not a question identity input.
    ident=digest([VERSION,level,[str(p[k]) for k in ('h','k','u','v')],worked,sorted(values)])
    qid=uid(['question',ident]);fid=uid([qid,'selection'])
    answers=[{':answer/id':uid([fid,value]),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=answers[[name for name,_ in options].index('correct')][':answer/id']
    rng.shuffle(answers)
    q={':question/id':qid,':question/problem':prompt,':question/difficulty':':question.difficulty/moderate',':question/worked-solution':worked,
       ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{
        'version':VERSION,'seed':seed,'difficulty':level,'difficulty_origin':'observed moderate; authored bank extension',
        'template':'center-point-equation','bank_profile':'authored-cross-product','roles':roles,
        'parameters':{key:str(value) for key,value in p.items()},'radius_squared':str(R),'solution_mask':mask,
        'source_ids':['e-6150','q-54215','q-117096','q-117099','q-72617','q-72619','q-72621'],
        'content_fingerprint':ident,'mathematical_fingerprint':digest([str(p[k]) for k in ('h','k','u','v')]),
        'sampling':{'attempts':attempts,'rejections':rejections},'plot':plot}}

def main():
    ap=argparse.ArgumentParser(description='Center and on-circle point: equation of a circle')
    ap.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate')
    ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--source-id')
    args=ap.parse_args()
    if args.count<1:ap.error('--count must be positive')
    try:records=[generate(args.difficulty,args.seed+i,source_id=args.source_id) for i in range(args.count)]
    except ValueError as exc:ap.error(str(exc))
    print(json.dumps(records,indent=2))

if __name__=='__main__':main()
