#!/usr/bin/env python3
"""Direct circulation over closed space curves, frozen math basis 1356.

API: generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), and generate_easy/moderate/hard with the same optional arguments.
Normal profiles are authored complete method-error banks. `raw:q-N` profiles
are public, parameterized, evidence-only original banks with original omissions.
Their only parameter is force_scale (nonzero integer -4..4); the complete force,
force-dependent calculation stages and every opaque bank value scale together.
Normal parameters are primitive positive axis scales a,b; easy also sign +/-1.
CLI: --difficulty easy|moderate|hard|all --seed N --count N
     --format markdown|json [--template NAME] [--profile PROFILE].
No database reads/writes, registration, renderer, or engine modifications.
"""
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import re
import sys
import uuid
import sympy as sp

DB_ID = 17592186133926
VERSION = 'circulation-1356-v1'
HERE = Path(__file__).with_suffix('')
SOURCE = json.loads((HERE/'source.json').read_text())
KP = SOURCE['record']
ORIGINALS = {q[':question/math-academy-id']: q for q in KP[':knowledge-point/questions']}
t,x,y,z = sp.symbols('t x y z', real=True)
NS = uuid.UUID('74196b81-0e52-5d10-a099-ccd849d03a98')
TEMPLATES = {
 'xy_rotation': ('easy', ['q-161925','q-162229']),
 'xy_rotation_z': ('easy', ['q-162230']),
 'yz_rotation': ('easy', ['q-162237','q-162228']),
 'xy_symmetric': ('moderate', ['q-162220']),
 'polynomial_sine': ('moderate', ['q-162235']),
 'polynomial_loop': ('hard', ['q-162238']),
}
SOURCE_TEMPLATE = {s:k for k,(_,ss) in TEMPLATES.items() for s in ss}

def tex(e):
    return sp.latex(e).replace(r'\log',r'\ln')

def uid(value):
    return str(uuid.uuid5(NS, str(value)))

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def grp(s):
    return r'\left('+s+r'\right)'

def vec(items):
    # Every component is retained, including zero contributions.
    return '+'.join(grp(tex(e))+r'\,'+u for e,u in zip(items,('i','j','k')))

def block(s):
    return '\n\n$$\n'+s+'\n$$'

def aligned(lhs, rows):
    return block(r'\begin{aligned}'+lhs+' & ='+r' \\ & ='.join(rows)+r'\end{aligned}')

def enum(e):
    return e[':db/ident'] if isinstance(e,dict) else e

def parse_scalar(s):
    # Source answer scalars are rational multiples of pi, or rational numbers.
    s=s.strip().replace('π','pi').replace(r'\pi','pi').replace(' ','')
    s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
    s=re.sub(r'(\d)(pi)',r'\1*\2',s)
    return sp.sympify(s,locals={'pi':sp.pi})

def scalar_scale(raw,c):
    # Identity coefficient is elided by this same expression mask, never by
    # returning the original question object. Changed values are exact scalars.
    return raw if c==1 else tex(c*parse_scalar(raw))

def scale_rhs(rhs,c):
    if c==1:
        return rhs
    # Terminal punctuation belongs outside a complete mathematical component.
    suffix=''
    while rhs and rhs[-1] in '., ':
        suffix=rhs[-1]+suffix;rhs=rhs[:-1]
    return str(c)+grp(rhs)+suffix

def scale_aligned(raw,c,skip_first=False):
    """Mask EACH full RHS independently; formal F(r) rows remain symbolic.

    Complete vector, product, integrand, primitive and endpoint arithmetic
    expressions are distinct slots, retaining every original stage and prose.
    Raw mathematical errors intentionally remain in these evidence masks.
    """
    content=raw.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
    rows=content.split(r'\\')
    out=[]
    for n,row in enumerate(rows):
        if '& =' not in row:
            raise ValueError('Unexpected source aligned shape')
        lhs,rhs=row.split('& =',1)
        out.append(lhs+'& ='+(rhs if skip_first and n==0 else scale_rhs(rhs,c)))
    return raw.replace(content,r'\\'.join(out))

def raw_recipe(source_id,c):
    """Compile captured prose into force-scaled expression slots.

    At force_scale=1 all source bytes and presence of source attributes survive;
    at other values this is a genuine same-curve scaled-force calculation. The
    opaque bank extension is a pattern only, not inferred distractor intent.
    """
    raw=ORIGINALS[source_id]
    q={k:copy.deepcopy(v) for k,v in raw.items()
       if k not in (':db/id',':question/id',':question/answer-fields')}
    prompt=q[':question/problem']
    # Only the COMPLETE force RHS from the first inline formula is a slot.
    pattern=r'(F\(x,\s*y,\s*z\)\s*=\s*)([^$]+)'
    q[':question/problem']=re.sub(pattern,lambda m:m[1]+scale_rhs(m[2],c),prompt,count=1)
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution']
        counter=[0]
        def replace(m):
            i=counter[0];counter[0]+=1
            if i==0:return scale_aligned(m[0],c) # every field-substitution RHS
            if i==1:return m[0]                 # derivative independent of F
            if i==2:return scale_aligned(m[0],c) # complete dot-product RHSs
            if i==3:return scale_aligned(m[0],c,True) # formal first integral
            raise ValueError('Unexpected source stage')
        q[':question/worked-solution']=re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}',replace,sol,flags=re.S)
        assert counter[0]==4
    if ':question/difficulty' in q:q[':question/difficulty']=enum(q[':question/difficulty'])
    fraw=raw[':question/answer-fields'][0]
    choices=[{':answer/id':uid((source_id,c,a[':answer/id'])),':answer/type':enum(a[':answer/type']),
              ':answer/value':scalar_scale(a[':answer/value'],c)} for a in fraw[':answer-field/choices']]
    f={':answer-field/id':uid((source_id,c,'field')),':answer-field/key':fraw[':answer-field/key'],
       ':answer-field/type':enum(fraw[':answer-field/type']),':answer-field/choices':choices}
    if ':answer-field/correct' in fraw:
        i=next(i for i,a in enumerate(fraw[':answer-field/choices']) if a[':answer/id']==fraw[':answer-field/correct'][':answer/id'])
        f[':answer-field/correct']=[':answer/id',choices[i][':answer/id']]
    q[':question/answer-fields']=[f]
    return q

def domains(template):
    """Finite primitive scales exclude common scale aliases; no reparametrizing.

    Easy/moderate scales 1..4 (11 primitive pairs); hard 1..6 (23 pairs).
    These bounds apply identically to random and explicit calls. In hard, F is
    (a*y-b*x)i so the linear terms cancel exactly as in the unrated source;
    every variant retains three polynomial integrand/primitive terms.
    """
    maxaxis=6 if template=='polynomial_loop' else 4
    return [dict(a=a,b=b,**({'sign':s} if TEMPLATES[template][0]=='easy' else {}))
            for a,b in itertools.product(range(1,maxaxis+1),repeat=2)
            if math.gcd(a,b)==1
            for s in ((-1,1) if TEMPLATES[template][0]=='easy' else (1,))]

def mathematical_data(template,p):
    a,b=p['a'],p['b'];sgn=p.get('sign',1)
    if template=='xy_rotation':
        r=[a*sp.cos(sp.pi*t),b*sp.sin(sp.pi*t),1-t*t]
        F=[-sgn*y,sgn*x,0];lo,hi=-1,1
    elif template=='xy_rotation_z':
        r=[a*sp.sin(t),b*sp.cos(t),t*t]
        F=[sgn*y,-sgn*x,z];lo,hi=-sp.pi,sp.pi
    elif template=='yz_rotation':
        r=[t*t-t,a*sp.cos(2*sp.pi*t),b*sp.sin(2*sp.pi*t)]
        F=[0,sgn*z,-sgn*y];lo,hi=0,1
    elif template=='xy_symmetric':
        r=[a*sp.sin(t),b*sp.cos(t),2*sp.sin(t)]
        F=[y,x,0];lo,hi=0,2*sp.pi
    elif template=='polynomial_sine':
        r=[a*(1-t*t),a*t*t,b*sp.sin(sp.pi*t)]
        F=[x+y,0,-z];lo,hi=-1,1
    elif template=='polynomial_loop':
        r=[a*(t*t-t),b*(t**3-t),sp.sin(2*sp.pi*t)]
        F=[a*y-b*x,0,0];lo,hi=0,1
    else:raise ValueError('Unknown template')
    F=list(map(sp.sympify,F));r=list(map(sp.sympify,r))
    Fr=[e.subs({x:r[0],y:r[1],z:r[2]},simultaneous=True) for e in F]
    dr=[sp.diff(e,t) for e in r]
    products=[f*d for f,d in zip(Fr,dr)]
    integrand=sp.expand_trig(sp.trigsimp(sum(products)))
    if template=='xy_symmetric': integrand=a*b*sp.cos(2*t)
    if template=='polynomial_sine': integrand=-2*a*a*t-sp.pi*b*b*sp.sin(2*sp.pi*t)/2
    primitive=sp.integrate(integrand,t)
    result=sp.simplify(primitive.subs(t,hi)-primitive.subs(t,lo))
    return {'r':r,'F':F,'Fr':Fr,'dr':dr,'products':products,'integrand':integrand,
            'primitive':primitive,'result':result,'lo':sp.sympify(lo),'hi':sp.sympify(hi)}

def banks(template,p,d):
    """One whole authored profile per family, chosen before its parameters.

    The two cancellation families have their own real-operation banks, never
    perturbations of zero. Polynomial loop errors omit the x-component of F,
    reverse orientation, omit the cubic y term, or omit the -a term of dx/dt. A collision
    rejects the WHOLE bank. No replacement pool is used.
    """
    G=d['result'];a,b=p['a'],p['b'];lo,hi=d['lo'],d['hi']
    if template.startswith('xy_rotation') or template=='yz_rotation':
        vals=[G,-G,G/2,0,2*G]
        recipes=['correct','reverse_orientation','omit_one_rotating_component',
                 'reverse_one_rotating_derivative_sign','traverse_interval_twice']
    elif template=='xy_symmetric':
        vals=[0,2*sp.pi*a*b,-2*sp.pi*a*b,sp.pi*a*b,-sp.pi*a*b]
        recipes=['correct','change_difference_to_sum','reverse_both_component_signs_after_sum',
                 'omit_negative_component','omit_positive_component']
    elif template=='polynomial_sine':
        vals=[0,2*a*a,-2*a*a,b*b,-b*b]
        recipes=['correct','add_instead_of_subtract_x_primitive_endpoints_and_reverse_sign',
                 'add_instead_of_subtract_x_primitive_endpoints',
                 'evaluate_z_primitive_at_two_peaks_add_and_reverse_sign',
                 'evaluate_z_primitive_at_two_peaks_and_add']
    else:
        F=d['Fr'][0]
        vals=[G,-G,0,sp.integrate((-a*b*t*t)*d['dr'][0],(t,lo,hi)),sp.integrate(F*(2*a*t),(t,lo,hi))]
        recipes=['correct','reverse_orientation','omit_y_from_field',
                 'omit_cubic_term_in_y_before_substitution','omit_constant_term_in_dx_dt']
    vals=list(map(sp.simplify,vals))
    if any(sp.simplify(a-b)==0 for a,b in itertools.combinations(vals,2)):
        raise ValueError('Whole bank is ambiguous')
    return vals,recipes

OPENING=('The circulation $Γ$ measures the total work done by a force $F$ in moving a particle '
         'along a *closed* curve $C.$\nIt is given by the formula')

def solution(d):
    """Shared fixed source prose; complete ordered mathematical component masks.

    Derivatives include the formal operator for every coordinate. Dot products
    retain zero terms. Primitive terms are evaluated individually at BOTH
    endpoints before collection, including zero-valued terms.
    """
    r,F,Fr,dr=[d[k] for k in ('r','F','Fr','dr')]
    lo,hi=d['lo'],d['hi']
    formal='+'.join(r'\frac{\mathrm d}{\mathrm dt}'+grp(tex(e))+r'\,'+u for e,u in zip(r,'ijk'))
    products='+'.join(grp(tex(f))+r'\cdot'+grp(tex(v)) for f,v in zip(Fr,dr))
    primitive_terms=sp.Add.make_args(sp.expand(d['primitive']))
    # Sort by polynomial power, with the trigonometric term last, to make the
    # individually evaluated arithmetic row stable and pedagogically visible.
    primitive_terms=sorted(primitive_terms,key=sp.default_sort_key)
    at_hi='+'.join(grp(tex(e.subs(t,hi))) for e in primitive_terms)
    at_lo='+'.join(grp(tex(e.subs(t,lo))) for e in primitive_terms)
    out=OPENING+block(r'Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.')
    out+='\n\nAlong the curve $C,$ we have'+block(',\\quad '.join(v+'='+tex(e) for v,e in zip('xyz',r))+'.')
    out+='\n\nSo,'+aligned('F(r(t))',[vec(F),vec(Fr)])
    out+='\n\nComputing $r^{\\prime}(t),$ we get'+aligned(r'r^{\prime}(t)',[formal,vec(dr)])
    out+='\n\nTherefore,'+aligned(r'F(r(t))\cdot r^{\prime}(t)',[
        grp(vec(Fr))+r'\cdot'+grp(vec(dr)),products,
        '+'.join(grp(tex(sp.expand(e))) for e in d['products']),tex(d['integrand'])])
    out+='\n\nFinally, we evaluate the integral as follows:'+aligned(r'Γ=\oint_C F\cdot\mathrm dr',[
        r'\int_{'+tex(lo)+'}^{'+tex(hi)+r'}F(r(t))\cdot r^{\prime}(t)\,\mathrm dt',
        r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}'+grp(tex(d['integrand']))+r'\,\mathrm dt',
        r'\left['+tex(d['primitive'])+r'\right]_{'+tex(lo)+'}^{'+tex(hi)+'}',
        '['+at_hi+']-['+at_lo+']',tex(d['result'])])
    return out

def normal_question(template,p):
    d=mathematical_data(template,p);vals,recipes=banks(template,p,d)
    prompt=('Calculate the circulation $Γ$ of the vector field $F(x,y,z)='+vec(d['F'])+
            '$ along the closed curve $C$ given by $r(t)='+vec(d['r'])+
            '$ for $t\\in ['+tex(d['lo'])+','+tex(d['hi'])+').$')
    q={':question/problem':prompt,':question/worked-solution':solution(d),
       ':question/difficulty':':question.difficulty/'+TEMPLATES[template][0]}
    return q,vals,recipes,d

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields supported')
    rng=random.Random(seed)
    if profile and profile.startswith('raw:'):
        sid=profile[4:]
        if sid not in ORIGINALS:raise ValueError('Unknown source profile')
        expected=SOURCE_TEMPLATE[sid]
        if template not in (None,expected) or level!=TEMPLATES[expected][0]:raise ValueError('Source profile template/level mismatch')
        template=expected;p={'force_scale':1} if parameters is None else dict(parameters)
        if set(p)!={'force_scale'} or type(p['force_scale']) is not int or not 1<=abs(p['force_scale'])<=4:raise ValueError('Raw force_scale must be a nonzero integer -4..4')
        q=raw_recipe(sid,p['force_scale'])
        provenance='original parameterized evidence' if p['force_scale']==1 else 'generated opaque evidence pattern'
        eligible=False;recipes=['opaque scalar scaling; intent unresolved']*5
        mathkey=[template,sid,p]
    else:
        if profile not in (None,'authored-method'):raise ValueError('Unknown profile')
        eligible_templates=[k for k,(l,_) in TEMPLATES.items() if l==level]
        if template is None:template=rng.choice(eligible_templates)
        if template not in eligible_templates:raise ValueError('Template/level mismatch')
        # Family + complete profile first; then select from its full finite domain.
        domain=domains(template)
        if parameters is None:p=rng.choice(domain)
        else:
            p=dict(parameters)
            if any(type(v) is not int for v in p.values()) or p not in domain:raise ValueError('Parameters outside primitive, level-specific domain')
        q,vals,recipes,d=normal_question(template,p)
        fingerprint=digest([template,[sp.srepr(e) for e in d['r']],[sp.srepr(e) for e in d['F']],str(d['lo']),str(d['hi'])])
        q[':question/answer-fields']=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
            ':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':tex(v)} for v in vals]}]
        provenance='authored same-method extension';eligible=True;profile='authored-method';sid=None;mathkey=fingerprint
    # Presentation identity includes actual difficulty, prompt, fixed solution,
    # attribute presence and entire displayed bank, but not seed/choice order.
    identity=digest([VERSION,q])
    q[':question/id']=uid(identity)
    field=q[':question/answer-fields'][0]
    oldcorrect=field.get(':answer-field/correct',[None,None])[1]
    correct_value=next((a[':answer/value'] for a in field[':answer-field/choices'] if a.get(':answer/id')==oldcorrect),None) if oldcorrect else None
    if eligible:correct_value=tex(vals[0])
    field[':answer-field/id']=uid((identity,'field'))
    for a in field[':answer-field/choices']:a[':answer/id']=uid((identity,'answer',a[':answer/value']))
    if correct_value is not None:field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in field[':answer-field/choices'] if a[':answer/value']==correct_value)]
    rng.shuffle(field[':answer-field/choices'])
    return {'knowledge_point':{'db_id':DB_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},
            'question':q,'generation':{'version':VERSION,'basis':1356,'lineage':SOURCE['lineage'],'seed':seed,
              'template':template,'bank_profile':profile,'parameters':p,'source_id':sid,'provenance':provenance,
              'source_references':[sid] if sid else TEMPLATES[template][1],
              'canonical_example':'e-12421','domain':'F is polynomial on R^3; closed limiting endpoints; one traversal',
              'actual_difficulty':q.get(':question/difficulty','unrated'),'eligible_for_learning':eligible,
              'evidence_only':not eligible,'error_recipes':recipes,'mathematical_fingerprint':digest(mathkey),
              'content_identity':identity,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# EASY: same two rotating products, optional conservative z contribution.
# Four source geometries collapse to three coordinate/operator families. Signs
# and primitive axis pairs 1..4 vary; one full turn only. 22 tasks per family.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE: both observed cancellation families, with a double-angle reduction
# or polynomial substitution plus sine-cosine product. Primitive pairs 1..4.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)

# HARD: authored rating of the unrated polynomial loop. Expand three nonzero
# polynomial terms and integrate/evaluate all three, same direct circulation
# formula. Primitive pairs 1..6; no Stokes theorem or surface task.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
    q,g=r['question'],r['generation'];f=q[':question/answer-fields'][0]
    lines=['### '+g['provenance']+' — '+g['actual_difficulty'].split('/')[-1],
           'Template: `'+g['template']+'`; profile: `'+g['bank_profile']+'`; eligible: '+str(g['eligible_for_learning']),
           '',q[':question/problem'],'']
    correct=f.get(':answer-field/correct',[None,None])[1]
    for i,a in enumerate(f[':answer-field/choices']):lines.append('- '+chr(65+i)+'. $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==correct else ''))
    if not correct:lines+=['','Original correct designation absent; inferred separately.']
    if ':question/worked-solution' in q:lines+=['','**Worked solution**','',q[':question/worked-solution']]
    else:lines+=['','Original worked solution absent.']
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all')
    ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1)
    ap.add_argument('--format',choices=('markdown','json'),default='markdown')
    ap.add_argument('--template',choices=tuple(TEMPLATES));ap.add_argument('--profile')
    args=ap.parse_args()
    if args.count<1:ap.error('--count must be positive')
    if args.difficulty=='all' and (args.template or args.profile):ap.error('Select specific difficulty for template/profile')
    levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
    try:rs=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
    except ValueError as e:ap.error(str(e))
    print(json.dumps(rs,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))

if __name__=='__main__':main()
