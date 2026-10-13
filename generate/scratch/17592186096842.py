#!/usr/bin/env python3
"""Exact radical-chain generator; local review only, no database operations.

Nine source questions, all fields and banks retained. Eight observed source
solutions use parameterized instructional scaffolds; q-48846's absent solution,
level and correct ref are separately documented repairs. Source empirical banks
are explicit-only; default radios use whole operation-derived banks. See evidence
folder for parameter policies, mathematical and native grader checks.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid, re
from pathlib import Path
import sympy as sp
KP_ID=17592186096842
KP_UUID='2f0cdac9-57b2-5634-8d98-d6adf8a85204'
TITLE='Differentiating a Radical Function Using the Chain Rule'
VERSION='radical-chain-1'
ROOT=Path(__file__).with_suffix('')
X=sp.Symbol('x', real=True)
U=sp.Symbol('u', positive=True)
D=r'\frac{\text{d}y}{\text{d}x}'
DU=r'\frac{\text{d}y}{\text{d}u}'
UX=r'\frac{\text{d}u}{\text{d}x}'
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
# Each layout is independent, never an ordered progression within a level.
TEMPLATES={
 'reciprocal_radio':dict(level='moderate',field='radio',family='reciprocal',degree=1,source='q-48730',style='linear'),
 'sqrt_spaced_radio':dict(level='moderate',field='radio',family='sqrt',degree=1,source='q-48846',style='spaced',repair=True),
 'sqrt_constfirst_radio':dict(level='moderate',field='radio',family='sqrt',degree=1,source='q-107291',style='constfirst'),
 'slope_sqrt_radio':dict(level='easy',field='radio',family='sqrt',degree=1,source='q-107360',style='constfirst',slope=True),
 'reciprocal_blank':dict(level='moderate',field='blank',family='reciprocal',degree=1,source='q-342764',style='linear'),
 'reciprocal_blank_braced':dict(level='moderate',field='blank',family='reciprocal',degree=1,source='q-314194',style='linear',braced=True),
 'sqrt_quadratic_blank':dict(level='hard',field='blank',family='sqrt',degree=2,source='q-342680',style='quadratic'),
 'sqrt_linear_blank':dict(level='hard',field='blank',family='sqrt',degree=1,source='q-342683',style='linear'),
 'slope_reciprocal_blank':dict(level='easy',field='blank',family='reciprocal',degree=2,source='q-342802',style='quadratic',slope=True),
}
PROFILES={
 'source_reciprocal':('reciprocal_radio','observed empirical; coefficient -3 unresolved'),
 'source_spaced':('sqrt_spaced_radio','observed operation shapes'),
 'source_constfirst':('sqrt_constfirst_radio','observed operation shapes'),
 'source_slope':('slope_sqrt_radio','observed empirical; wrong scalar intent unresolved'),
 'authored_operations':(None,'authored full four-error bank'),
 'blank':(None,'observed single expression fragment'),
}

def tex(v):return sp.latex(sp.sympify(v)).replace(' ', '').replace(r'\left(', '(').replace(r'\right)', ')')
def poly(p,spec,var='x'):
    a,b,c=p['a'],p['b'],p.get('c',0)
    def term(co,n):
        if co==0:return ''
        sign='-' if co<0 else '+'
        co=abs(co)
        return sign+('' if co==1 and n else str(co))+(var if n==1 else ((var[:-1]+r'{)}^{2}' if var.startswith('(') else '{'+var+'}^{2}') if n==2 else ''))
    if spec['degree']==1:
        parts=[term(a,1),term(b,0)] if spec['style']!='constfirst' else [term(b,0),term(a,1)]
    else:parts=[term(a,2),term(b,1),term(c,0)]
    text=''.join(parts).lstrip('+')
    if spec['style']=='spaced':text=text.replace('+',' + ').replace('-',' - ').strip()
    return text

def model(spec,p):
    inner=p['a']*X**spec['degree']+p['b']*(X if spec['degree']==2 else 1)+p.get('c',0)
    exponent=sp.Rational(1,2) if spec['family']=='sqrt' else -sp.Rational(1,2)
    du=sp.diff(inner,X)
    derivative=exponent*inner**(exponent-1)*du
    answer=sp.simplify(derivative.subs(X,p['t'])) if spec.get('slope') else derivative
    return inner,du,exponent,derivative,answer

def frac(n,d):
    n=sp.sympify(n)
    if n==0:return '0'
    neg=n.could_extract_minus_sign()
    if n.is_Rational and n.q!=1:
        prefix=re.match(r'^([0-9]+)',d)
        d=str(n.q*(int(prefix.group(1)) if prefix else 1))+d[len(prefix.group(1)) if prefix else 0:]
        n=sp.Integer(n.p)
    return ('-' if neg else '')+r'\frac{'+tex(-n if neg else n)+'}{'+d+'}'

def derivative_tex(spec,p,at_u=False,simplified=True):
    inner,du,e,der,ans=model(spec,p)
    z='u' if at_u else poly(p,spec)
    z3=r'{u}^{3}' if at_u else '('+z+(r'{)}^{3}' if spec.get('braced') or spec['source'] in ('q-48730','q-342802') else r')^{3}')
    radical=r'\sqrt{'+(z if e>0 else z3)+'}'
    num=du if e>0 else -du
    if simplified:
        coeff=sp.Rational(1,2)
        # Cancel integer factor 2 in numerator, preserving source radical shape.
        g=sp.polys.polytools.terms_gcd(num)
        if all(co%2==0 for co in sp.Poly(num,X).all_coeffs()):num=sp.expand(num/2);den=radical
        else:den='2'+radical
    else:den='2'+radical
    return frac(num,den)

def aligned(rows):return r'\begin{aligned}'+r' \\  & ='.join([D+' & ='+rows[0]]+rows[1:])+r'.\end{aligned}'
def blocks(spec,p):
    """All displayed mathematical blocks are computed, including substitutions."""
    inner,du,e,der,ans=model(spec,p)
    z=poly(p,spec)
    function=r'\sqrt{'+z+'}' if e>0 else r'\frac{1}{\sqrt{'+z+'}}'
    outer=r'\sqrt{u}' if e>0 else r'\frac{1}{\sqrt{u}}={u}^{-1/2}'
    if spec['source']=='q-107291':outer=r'\sqrt{u}={u}^{1/2}'
    outer_deriv=DU+('='+r'\frac{1}{2}{u}^{-1/2}=\frac{1}{2\sqrt{u}}' if spec['source']=='q-107291' else '='+r'\frac{1}{2\sqrt{u}}') if e>0 else DU+r'=-\frac{1}{2}{u}^{-3/2}=-\frac{1}{2\sqrt{{u}^{3}}}'
    if spec['field']=='blank':outer_deriv+=','
    if spec.get('repair'):outer_deriv=DU+r'=\frac{1}{2\sqrt{u}},'
    outer_factor=r'\frac{1}{2\sqrt{u}}' if e>0 else r'-\frac{1}{2\sqrt{{u}^{3}}}'
    du_tex=tex(du)
    if spec['degree']==1:du_tex=str(p['a'])
    product_du='('+du_tex+')'
    if spec['field']=='blank' and spec['degree']==1:product_du=du_tex
    rows=[outer_factor+r'\cdot '+product_du]
    if spec['level']=='hard':rows.insert(0,DU+r'\cdot '+UX)
    if spec['family']=='reciprocal' and spec['field']=='blank' and not spec.get('slope'):
        rows+=[derivative_tex(spec,p,at_u=True),derivative_tex(spec,p)]
    elif spec['degree']==2 and spec['family']=='sqrt':
        num=sp.factor(du)
        rows += [frac(num,'2'+r'\sqrt{'+z+'}'),derivative_tex(spec,p)]
    elif spec.get('slope') and spec['family']=='reciprocal':
        rows += [derivative_tex(spec,p,simplified=False)]
    else:rows += [derivative_tex(spec,p)]
    multiplication=aligned(rows)
    evaluation=''
    if spec.get('slope'):
        t=p['t']; val=inner.subs(X,t); derivative_render=derivative_tex(spec,p,simplified=spec['family']=='sqrt')
        target=r'{'+D+r'|}_{x='+str(t)+'}'
        subst=poly(p,spec,'('+str(t)+')')
        if e>0:
            half=sp.Rational(p['a'],2)
            evrows=[r'{('+derivative_render+r')|}_{x='+str(t)+'}',frac(half,r'\sqrt{'+subst+'}'),tex(ans)+r'\,']
        else:
            # Keep the source's unreduced numerator for quadratic substitution.
            vdu=tex(du).replace('x','('+str(t)+')')
            first=r'{('+derivative_render+r')|}_{x='+str(t)+'}'
            second='-'+r'\frac{'+vdu+r'}{2\sqrt{('+subst+r'{)}^{3}}}'
            third=frac(-du.subs(X,t),'2'+r'\sqrt{{'+str(val)+r'}^{3}}')
            evrows=[first,second,third,tex(ans)]
        evaluation=r'\begin{aligned}'+target+' & ='+r' \\  & ='.join(evrows)+r'.\end{aligned}'
    return {'z':z,'function':function,'outer':outer,'chain':D+'='+DU+r'\cdot '+UX+'.','outer_deriv':outer_deriv,'inner_deriv':UX+'='+du_tex+'.','multiplication':multiplication,'evaluation':evaluation,'t':str(p.get('t',''))}

def render(scaffold,parts):
    for key,value in parts.items():scaffold=scaffold.replace('<<'+key+'>>',value)
    if '<<' in scaffold:raise ValueError('Unfilled template')
    return scaffold

def bank(spec,p,profile):
    inner,du,e,d,ans=model(spec,p)
    def assessed(v):return sp.simplify(v.subs(X,p['t'])) if spec.get('slope') else v
    answer_spec={**spec,'braced':False} if spec['source']=='q-314194' else spec
    out=[('correct',ans,tex(ans) if spec.get('slope') else derivative_tex(answer_spec,p))]
    if spec['field']=='blank':return out
    if profile=='source_reciprocal':
        values=[('empirical_minus_three_over_inner',-3/inner,frac(-3,poly(p,spec))),('omit_inner_and_wrong_exponent',1/(2*sp.sqrt(inner)),frac(1,'2'+r'\sqrt{'+poly(p,spec)+'}')),('keep_square_root_exponent',-du/(2*sp.sqrt(inner)),frac(-du,'2'+r'\sqrt{'+poly(p,spec)+'}')),('omit_inner_and_negative_sign',1/(2*inner**sp.Rational(3,2)),frac(1,'2'+r'\sqrt{('+poly(p,spec)+r'{)}^{3}}'))]
    elif profile=='source_spaced':
        reverse=p.copy();reverse['b']=-p['b']; revinner=p['a']*X-p['b'];revz=poly(reverse,spec)
        values=[('omit_half',du/sp.sqrt(inner),frac(du,r'\sqrt{'+poly(p,spec)+'}')),('reverse_constant_and_omit_inner',1/(2*sp.sqrt(revinner)),frac(1,'2'+r'\sqrt{'+revz+'}')),('reverse_constant',du/(2*sp.sqrt(revinner)),frac(du/2,r'\sqrt{'+revz+'}')),('omit_inner',1/(2*sp.sqrt(inner)),frac(1,'2'+r'\sqrt{'+poly(p,spec)+'}'))]
    elif profile=='source_constfirst':
        z=poly(p,spec)
        values=[('divide_by_inner_magnitude',-1/(2*du*sp.sqrt(inner)),frac(-1/du,'2'+r'\sqrt{'+z+'}')),('use_constant_as_divisor',du/(2*p['b']*sp.sqrt(inner)),frac(du/(2*p['b']),r'\sqrt{'+z+'}')),('omit_half_and_reverse_sign',-du/sp.sqrt(inner),frac(-du,r'\sqrt{'+z+'}')),('omit_inner_magnitude',sp.sign(du)/(2*sp.sqrt(inner)),frac(sp.sign(du),'2'+r'\sqrt{'+z+'}'))]
    elif profile=='source_slope':
        v=inner.subs(X,p['t']); root=sp.sqrt(v)
        # Empirical expression shapes, not a claim to recover cognitive errors.
        values=[('empirical_minus_five_over_root',-5/root,None),('empirical_one_over_root',1/root,None),('empirical_root_over_linear_coefficient',root/p['a'],None),('empirical_negative_half_coefficient',-sp.Rational(p['a'],2),None)]
    elif profile=='authored_operations':
        values=[('omit_inner_derivative',assessed(e*inner**(e-1)),None),('reverse_derivative_sign',-ans,None),('omit_half',2*ans,None),('do_not_lower_outer_power',assessed(e*inner**e*du),None)]
    else:raise ValueError('Unknown bank')
    for label,value,latex in values:out.append((label,sp.simplify(value),latex or tex(value)))
    for i,(_,value,_) in enumerate(out):
        if value.has(sp.zoo,sp.nan,sp.oo) or value.is_real is False:raise ValueError('Invalid whole bank')
        for _,other,_ in out[:i]:
            if sp.simplify(value-other)==0:raise ValueError('Ambiguous whole bank')
    return out

def check_parameters(spec,p):
    expected={'a','b'} | ({'c'} if spec['degree']==2 else set()) | ({'t'} if spec.get('slope') else set())
    if set(p)!=expected or any(type(v)!=int for v in p.values()):raise ValueError('Exact integer parameters required: '+str(sorted(expected)))
    if p['a']==0:raise ValueError('Nonconstant inner function required')
    if spec['degree']==2 and p['c']!=0:raise ValueError('Observed quadratic scope has two nonconstant terms and c=0')
    if spec['degree']==1 and abs(p['a'])==1 and spec['field']=='radio':raise ValueError('Radio coefficient magnitude >=2 avoids omitted-chain collision')
    inner,du,e,d,ans=model(spec,p)
    if spec.get('slope') and (inner.subs(X,p['t'])<=0 or du.subs(X,p['t'])==0):raise ValueError('Slope requires positive radicand and nonzero inner derivative')
    if spec.get('slope') and not sp.sqrt(inner.subs(X,p['t'])).is_Integer:raise ValueError('Easy slope requires a perfect-square radicand')
    if spec['family']=='sqrt' and spec['degree']==2 and p['a']<0 and sp.discriminant(inner,X)<=0:raise ValueError('No positive real domain')

SLOPE_QUADRATIC_PARAMETERS=tuple(
    dict(a=a,b=sign*b,c=0,t=sign*t)
    for a in range(1,7) for b in range(1,25) for t in range(1,5) for sign in (-1,1)
    if 2<=sp.sqrt(a*t*t+b*t)<=12 and sp.sqrt(a*t*t+b*t).is_Integer)

def sample(spec,rng):
    if spec.get('slope') and spec['degree']==1:
        a=rng.choice([-8,-7,-6,-5,-4,-3,-2,2,3,4,5,6,7,8]);t=rng.choice([-3,-2,-1,1,2,3]);r=rng.randint(2,9)
        return dict(a=a,b=r*r-a*t,t=t)
    if spec.get('slope'):
        return dict(rng.choice(SLOPE_QUADRATIC_PARAMETERS))
    return dict(a=rng.choice([-8,-7,-6,-5,-4,-3,-2,2,3,4,5,6,7,8]),b=rng.choice([i for i in range(-12,13) if i!=0]),**({'c':0} if spec['degree']==2 else {})) if spec['degree']==1 else dict(a=rng.randint(1,5),b=rng.choice([i for i in range(-12,13) if i!=0]),c=0)

# EASY: evaluated slopes; source evidence includes linear sqrt and quadratic
# reciprocal. These are alternatives, never a progression in this difficulty.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: radical or reciprocal radical with linear inner function.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: preserve both observed blank layouts, including the linear source.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    rng=random.Random(seed)
    if profile not in (None,'authored_operations','blank'):
        if profile not in PROFILES:raise ValueError('Unknown profile')
        required=PROFILES[profile][0]
        if template is not None and template!=required:raise ValueError('Ineligible source profile')
        template=required
    eligible=[k for k,v in TEMPLATES.items() if v['level']==level and (field_type is None or field_type in (v['field'],':answer-field.type/'+v['field']))]
    if template is None:
        if not eligible:raise ValueError('No eligible templates')
        template=rng.choice(eligible)
    if template not in eligible:raise ValueError('Template incompatible with level or field')
    spec=TEMPLATES[template];profile=profile or ('blank' if spec['field']=='blank' else 'authored_operations')
    if (spec['field']=='blank')!=(profile=='blank'):raise ValueError('Profile incompatible with field')
    for attempt in range(1000):
        p=dict(parameters) if parameters is not None else sample(spec,rng)
        try:check_parameters(spec,p); options=bank(spec,p,profile);break
        except ValueError:
            if parameters is not None:raise
    else:raise ValueError('No valid whole-bank instance')
    parts=blocks(spec,p)
    scaffold=json.loads((ROOT/'templates.json').read_text())[template]
    prompt=render(scaffold['prompt'],parts);solution=render(scaffold['solution'],parts)
    inner,du,e,d,ans=model(spec,p)
    domain=tex(inner)+'>0'
    mathematical_identity={'inner':str(sp.expand(inner)), 'outer_exponent':str(e), 'evaluation_point':p.get('t'), 'response_kind':'slope' if spec.get('slope') else 'derivative RHS', 'domain':str(sp.expand(inner))+'>0'}
    fingerprint=hashlib.sha256(json.dumps(mathematical_identity,sort_keys=True).encode()).hexdigest()
    display={'version':VERSION,'template':template,'parameters':p,'profile':profile,'domain':domain,'prompt':prompt,'solution':solution,'bank':sorted(v for _,_,v in options),'field':spec['field']}
    identity=hashlib.sha256(json.dumps(display,sort_keys=True).encode()).hexdigest()
    def uid(role):return str(uuid.uuid5(uuid.UUID(KP_UUID),identity+':'+role))
    answers=[{':answer/id':uid('answer:'+value),':answer/type':':answer.type/math',':answer/value':value} for _,_,value in options]
    correct=answers[0][':answer/id'];rng.shuffle(answers)
    field={':answer-field/id':uid('field'),':answer-field/key':'selection' if spec['field']=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+spec['field'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid('question'),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'generator_version':VERSION,'template':template,'seed':seed,'parameters':p,'bank_profile':profile,'bank_origin':PROFILES[profile][1],'source':SOURCE,'source_ids':[spec['source']],'source_repair':bool(spec.get('repair')),'domain':domain,'plot_rating':'none','parameter_fingerprint':fingerprint,'content_fingerprint':identity,'sympy_version':sp.__version__,'exact':{'inner':str(inner),'inner_derivative':str(du),'outer_exponent':str(e),'derivative':str(d),'answer':str(ans)},'recipes':{value:label for label,_,value in options}}}

def markdown(rec):
    q=rec['question'];field=q[':question/answer-fields'][0]
    s=q[':question/problem']+'\n\n'
    if field[':answer-field/type'].endswith('/radio'):
        s+='\n'.join('- $'+a[':answer/value']+'$' for a in field[':answer-field/choices'])+'\n\n'
    return s+q[':question/worked-solution']

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    records=[generate(level,a.seed+i,a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
