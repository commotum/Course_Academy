#!/usr/bin/env python3
"""Supplied potentials over parametric curves; local review records, steps 3–7.

Twelve observed families and their complete five-option banks are retained.
Observed bank formulas are homogeneous potential scalings, whose original error
intent is underdetermined; they are explicit replay profiles, never default banks.
Authored default banks use complete endpoint/input operations and reject the whole
instance on a collision. Hard is an authored, bounded canonical-example extension.
No EDB client, registration, writes, plots, or answer lookup table is used.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import re
import uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186133878
KP_UUID='7b643761-8eab-5bd3-a5f5-c85b6ba34a61'
TITLE='Applying the Fundamental Theorem of Line Integrals Over Parametric Curves'
VERSION='endpoint-potential-1'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x,y,z,t=sp.symbols('x y z t',real=True)
E=sp.E; P=sp.pi

# Each observed formula is a genuine variable-potential, variable-curve recipe.
# Exact original bank replay permits potential scale changes only. Authored
# banks permit the listed curve parameters; no opaque source distractor fitting.
TEMPLATES={
 'cubic':('easy','q-104616',{'c':3}),
 'cycloid':('easy','q-104623',{'d':1}),
 'sqrt_product':('easy','q-124002',{'n':2,'h':1}),
 'exponential':('easy','q-124003',{'k':2,'c':3}),
 'cos_linear':('easy','q-124005',{'c':2}),
 'quadratic':('easy','q-104624',{'c':2,'b':2,'h':1}),
 'zero_ellipse':('easy','q-104637',{'c':1,'d':2}),
 'trig3':('moderate','q-99008',{'c':1,'d':2}),
 'helix':('moderate','q-104640',{'c':1,'d':1}),
 'exp_sum':('moderate','q-124008',{'c':1,'d':1,'k':2}),
 'exp_product':('moderate','q-104638',{'b':2,'h':1,'k':1}),
 'monomial3':('moderate','q-104639',{'c':1,'d':1,'k':1}),
 'reciprocal_exp':('hard',None,{'a':1,'b':1,'h':1,'end':1}),
 'reciprocal_product':('hard',None,{'a':1,'b':1,'h':1,'end':1}),
}

# Complete observed banks as parameterized homogeneous component expressions.
# Their provenance/interpretation limits appear in extraction, not learner prose.
OBSERVED_BANKS={
 'cubic':[8,32,28,10,21],
 'cycloid':[P**2+2*P,P**2-1,P+2,0,2*P**2-4*P],
 'sqrt_product':[76,98,87,109,106],
 'exponential':[3*E+1,3+E,3*E,3*E**2,E**2-1],
 'cos_linear':[-3*P/4,P/4,-2*P,P/2,-3*P/2],
 'quadratic':[15,24,12,6,20],
 'zero_ellipse':[P**2-2,0,P*sp.exp(2*P),P**2*sp.exp(P**2),P**2/4],
 'trig3':[P+1,1-P/2,1-P,P/3,P**2],
 'helix':[0,P**2,2,2*P,P+1],
 'exp_sum':[E**2+3*E,3*E**2-2,E**2+2*E-3,E**2-2,3*E-3],
 'exp_product':[E,0,4,3*E**2,5*E**6],
 'monomial3':[0,1,36,8,64],
}
BOUNDS={
 'cubic':{'c':(1,4)},'cycloid':{'d':(1,3)},
 'sqrt_product':{'n':(1,3),'h':(-2,3)},
 'exponential':{'k':(1,3),'c':(1,4)},'cos_linear':{'c':(1,4)},
 'quadratic':{'c':(1,3),'b':(1,3),'h':(-2,3)},
 'zero_ellipse':{'c':(1,3),'d':(1,4)},
 'trig3':{'c':(1,3),'d':(2,2)},'helix':{'c':(1,3),'d':(1,3)},
 'exp_sum':{'c':(1,2),'d':(1,2),'k':(1,3)},
 'exp_product':{'b':(1,3),'h':(1,3),'k':(1,3)},
 'monomial3':{'c':(1,2),'d':(1,2),'k':(1,2)},
 'reciprocal_exp':{'a':(-3,3),'b':(-3,3),'h':(1,3),'end':(1,2)},
 'reciprocal_product':{'a':(-3,3),'b':(-3,3),'h':(1,3),'end':(1,2)},
}

class SampleRejected(ValueError):pass

def tex(v):return sp.latex(sp.sympify(v))
def simplify(v):
    value=sp.simplify(sp.expand(v))
    # SymPy sometimes rewrites equal exp(+u)/exp(-u) contributions as cosh/sinh.
    # The curriculum's canonical example uses ordinary exponentials; retain that
    # notation instead of introducing hyperbolic functions in learner content.
    value=value.replace(sp.cosh,lambda u:(sp.exp(u)+sp.exp(-u))/2)
    value=value.replace(sp.sinh,lambda u:(sp.exp(u)-sp.exp(-u))/2)
    return sp.expand(value)
def components(name,p):
    """Return unscaled potential, supplied curve, and oriented interval."""
    if name=='cubic':return x**3+y,(p['c']*t,t**3),0,1
    if name=='cycloid':return x*x*y-y*y*x,(t-sp.sin(t),p['d']*(1-sp.cos(t))),0,P
    if name=='sqrt_product':return x*x*y*y+x+y,(sp.sqrt(t),t+p['h']),0,p['n']**2
    if name=='exponential':return y*sp.exp(p['k']*x),(t,p['c']*t*t),0,1
    if name=='cos_linear':return y*sp.cos(x)+x,(t,p['c']*t),P/2,P
    if name=='quadratic':return y+x*x,(p['c']*t,t*t-p['h']),0,p['b']
    if name=='zero_ellipse':return y*x*x*sp.exp(x*y),(p['c']*sp.cos(t),p['d']*sp.sin(t)),0,P/2
    if name=='trig3':return x*sp.sin(y)+y*sp.cos(z),(p['c']*sp.sin(t),t,p['d']*t),0,P/2
    if name=='helix':return x*x*z+x*sp.sin(y),(p['c']*sp.cos(t),sp.sin(t),p['d']*t),0,2*P
    if name=='exp_sum':return sp.exp(x)+sp.exp(y)+sp.exp(z),(p['c']*t,p['d']*t*t,p['k']*t**3),0,1
    if name=='exp_product':return y*sp.exp(x*z),(t*t+p['h'],t*t-p['k'],t*(t-p['b'])),0,p['b']
    if name=='monomial3':return x*y**2*z**3,(p['c']*t**2,p['d']*t**4,p['k']*t**6),0,1
    if name=='reciprocal_exp':return p['a']*x*y*y+p['b']*y*z,(sp.exp(t),t+p['h'],sp.exp(-t)),0,p['end']
    if name=='reciprocal_product':return p['a']*x*y*y+p['b']*x*y*z,(sp.exp(t),t+p['h'],sp.exp(-t)),0,p['end']
    raise ValueError('unknown template')

def evaluate(f,point):return simplify(f.subs(dict(zip((x,y,z),point)),simultaneous=True))
def point_tex(point):return ','.join(tex(v) for v in point)
def inline_substitution(f,point):
    # Command tokens are protected; replace only complete variable tokens.
    replacement={str(v):r'\left('+tex(c)+r'\right)' for v,c in zip((x,y,z),point)}
    return re.sub(r'\\[A-Za-z]+|[xyz]',lambda m:replacement.get(m[0],m[0]),tex(f))

REPAIRS={
 'q-99008':('f(r(\\pi ))-f(r(0))','f(r(\\frac{\\pi }{2}))-f(r(0))'),
 'q-104637':('f((r(\\frac{\\pi }{2}))-f(r(0))','f(r(\\frac{\\pi }{2}))-f(r(0))'),
}

def source_solution(name,scale):
    """A reusable homogeneous scaling of all source substitution stages.

    The Markdown recipe retains full source sentence/stage sequence. Stage
    components are not returned as a source question: potential and answers are
    computed, and every numerical stage is multiplied by the potential scale.
    """
    sid=TEMPLATES[name][1]; sol=QS[sid][':question/worked-solution']
    if sid in REPAIRS:sol=sol.replace(*REPAIRS[sid])
    begin=sol.rfind(r'\begin{aligned}')
    prefix,body=sol[:begin],sol[begin:]
    rows=re.split(r'\\\\\s*&\s*=',body)
    # First row states theorem; second calls f at endpoint coordinates.
    # Remaining rows expand this potential and therefore all scale by lambda.
    if scale!=1:
        for i in range(2,len(rows)):
            tail=''
            rhs=rows[i]
            if i==len(rows)-1:
                rhs,tail=rhs.split(r'\end{aligned}',1)
                rhs=rhs.rstrip();assert rhs.endswith('.')
                rhs=rhs[:-1];tail=r'\end{aligned}'+tail
            rows[i]=tex(scale)+r'\left('+rhs.strip()+r'\right)'+('.' if tail else '')+tail
    return prefix+(' \\\\  & ='.join(rows))

def source_prompt(name,scale):
    q=QS[TEMPLATES[name][1]][':question/problem']
    # Slot is the entire potential expression, delimited within the first math
    # component, rather than a replacement across variable names/prose/tuples.
    start=q.index('=')+1; end=q.index('.$',start)
    base=q[start:end]
    value=base if scale==1 else tex(scale)+r'\left('+base+r'\right)'
    return q[:start]+value+q[end:]

def intermediate_stage(name,f,A,B,fa,fb,scale):
    """Retain the family's arithmetic simplification stage, before final sum.

    In particular cubic/quadratic keep their evaluated-power sums; trig3 keeps
    its product with cos(pi)=-1; helix keeps its vanished sine term. This is a
    displayed operation recipe, not an equality selected from the answer bank.
    """
    def scaled(stage):
        return stage if scale==1 else tex(scale)+r'\left('+stage+r'\right)'
    if name=='cubic':
        return scaled(r'\left('+tex(B[0]**3)+'+'+tex(B[1])+r'\right)-\left('+tex(fa/scale)+r'\right)')
    if name=='quadratic':
        return scaled(r'\left('+tex(B[1])+'+'+tex(B[0]**2)+r'\right)-\left('+tex(fa/scale)+r'\right)')
    if name=='trig3':
        return scaled(r'\left('+tex(B[0]*sp.sin(B[1]))+'+'+tex(B[1])+r'\cdot\left('+tex(sp.cos(B[2]))+r'\right)\right)-\left('+tex(fa/scale)+r'\right)')
    if name=='helix':
        return scaled(r'\left('+tex(B[0]**2*B[2])+r'+0\right)-\left('+tex(fa/scale)+r'\right)')
    if name=='exp_product':
        return scaled(tex(B[1])+'+'+tex(-A[1]))
    return r'\left('+tex(fb)+r'\right)-\left('+tex(fa)+r'\right)'

def generic_solution(f,curve,a,b,A,B,fa,fb,name,scale):
    sid=TEMPLATES[name][1]
    intro=(QS[sid][':question/worked-solution'].split('In our case,')[0] if sid else
      next(iter(QS.values()))[':question/worked-solution'].split('In our case,')[0])
    endpoint=(r'\begin{aligned}r('+tex(a)+') & =⟨'+point_tex(A)+r'⟩ \\ r('+tex(b)+') & =⟨'+point_tex(B)+r'⟩.\end{aligned}')
    rows=[r'f(r('+tex(b)+'))-f(r('+tex(a)+'))',
          'f('+point_tex(B)+')-f('+point_tex(A)+')',
          r'\left('+inline_substitution(f,B)+r'\right)-\left('+inline_substitution(f,A)+r'\right)']
    if name!='zero_ellipse':rows.append(intermediate_stage(name,f,A,B,fa,fb,scale))
    rows.append(tex(simplify(fb-fa)))
    block=r'\begin{aligned}{\int }_{C}∇f\cdot \text{d}r & ='+(' \\\\  & ='.join(rows))+r'.\end{aligned}'
    return (intro+'In our case, the position vectors of the endpoints of the curve are given by\n\n$$\n'+endpoint+
      '\n$$\n\nTherefore, the coordinates of the endpoints of the path defined by $C$ are $('+point_tex(A)+')$ and $('+point_tex(B)+
      ').$\n\nApplying the fundamental theorem for line integrals, we have\n\n$$\n'+block+'\n$$')

def authored_bank(name,f,curve,a,b,A,B,fa,fb):
    """Compute one complete five-option operation bank, no pooled replacements."""
    delta=simplify(fb-fa)
    if name=='zero_ellipse':
        c,d=B[1],A[0]
        values=[delta,evaluate(f,(b,c)),evaluate(f,(d,c)),evaluate(f,(c,d)),evaluate(f,(b/2,c))]
        recipes=['correct','use_upper_parameter_as_x','combine_nonzero_endpoint_coordinates',
                 'exchange_nonzero_endpoint_coordinates','halve_upper_parameter_for_x']
    elif name=='monomial3':
        values=[delta,-delta,evaluate(f,(B[0]+1,B[1],B[2])),
                simplify(B[0]*B[1]*B[2]-A[0]*A[1]*A[2]),sp.Integer(0)]
        # Account for the potential scale in the omitted-power operation.
        base=x*y**2*z**3
        scale=simplify(f/base)
        values[3]*=scale
        recipes=['correct','reverse_orientation','increase_final_x_by_one','omit_y_and_z_powers','use_initial_point_twice']
    elif name in ('trig3','helix'):
        # All source trig endpoints have fa=0; exact scalar coordinates avoid
        # introducing unfamiliar trigonometric values in the displayed bank.
        values=[delta,-delta,sp.Integer(0),simplify(2*delta),simplify(delta/2)]
        recipes=['correct','reverse_orientation','use_initial_point_twice','double_endpoint_contribution','halve_endpoint_contribution']
    elif name=='cycloid':
        scale=simplify(f/(x*x*y-y*y*x))
        first=scale*B[0]**2*B[1];second=scale*B[1]**2*B[0]
        values=[delta,-delta,simplify(first+second),simplify(first),sp.Integer(0)]
        recipes=['correct','reverse_orientation','add_second_potential_term','omit_second_potential_term','use_initial_point_twice']
    elif name=='cos_linear':
        values=[delta,-delta,fb,fa,sp.Integer(0)]
        recipes=['correct','reverse_orientation','omit_initial_value','use_initial_value_only','use_initial_point_twice']
    elif name=='exp_product':
        values=[delta,-delta,simplify(fb+fa),fb,sp.Integer(0)]
        recipes=['correct','reverse_orientation','add_endpoint_values','omit_initial_value','use_initial_point_twice']
    elif name=='sqrt_product':
        scale=simplify(f/(x*x*y*y+x+y))
        values=[delta,-delta,fb,simplify(scale*(B[0]**2*B[1]**2-A[0]**2*A[1]**2)),sp.Integer(0)]
        recipes=['correct','reverse_orientation','omit_initial_value','omit_linear_potential_terms','use_initial_point_twice']
    elif name=='quadratic':
        scale=simplify(f/(y+x*x))
        values=[delta,-delta,fb,simplify(scale*(B[1]+B[0]-A[1]-A[0])),sp.Integer(0)]
        recipes=['correct','reverse_orientation','omit_initial_value','omit_x_square','use_initial_point_twice']
    elif name=='cubic':
        scale=simplify(f/(x**3+y))
        values=[delta,-delta,simplify(scale*(B[0]+B[1]-A[0]-A[1])),
                simplify(scale*(B[0]**2+B[1]-A[0]**2-A[1])),sp.Integer(0)]
        recipes=['correct','reverse_orientation','omit_x_cube','replace_x_cube_with_square','use_initial_point_twice']
    elif name=='exponential':
        scale=simplify(f/(y*sp.exp(_exponential_coefficient(f)*x)))
        k=_exponential_coefficient(f)
        values=[delta,-delta,scale*B[1]*E,scale*(sp.exp(k*B[0])-1),sp.Integer(0)]
        recipes=['correct','reverse_orientation','replace_exponent_with_one','omit_y_factor_and_use_initial_exponential','use_initial_point_twice']
    elif name=='exp_sum':
        scale=simplify(f/(sp.exp(x)+sp.exp(y)+sp.exp(z)))
        values=[delta,-delta,fb,fb-scale,scale*(3*sp.exp(B[2])-3)]
        recipes=['correct','reverse_orientation','omit_initial_value','count_initial_exponentials_as_one','use_final_z_for_all_exponents']
    elif name.startswith('reciprocal'):
        values=[delta,-delta,simplify(fb+fa),fb,fa]
        recipes=['correct','reverse_orientation','add_endpoint_values','omit_initial_value','use_initial_value_only']
    else:
        raise ValueError('no authored complete bank for this family')
    values=[simplify(v) for v in values]
    for i,v in enumerate(values):
        if v.has(sp.zoo,sp.nan,sp.oo,-sp.oo):raise SampleRejected('invalid bank')
        for w in values[:i]:
            if simplify(v-w)==0:raise SampleRejected('whole bank contains equivalent options')
    return list(zip(recipes,values))

def _exponential_coefficient(f):
    exponent=next(iter(f.atoms(sp.exp))).args[0]
    return exponent.coeff(x)

def normalize_parameters(name,parameters,profile):
    base={'scale':1,**TEMPLATES[name][2]}
    if parameters is not None:
        unknown=set(parameters)-set(base)
        if unknown:raise ValueError('unknown parameters: '+str(sorted(unknown)))
        base.update(parameters)
    for key,v in base.items():
        if not isinstance(v,int) or isinstance(v,bool):raise ValueError('integer parameters required')
        low,high=(-4,4) if key=='scale' else BOUNDS[name][key]
        if not low<=v<=high:raise ValueError('parameter outside difficulty bounds: '+key)
        if (key in ('scale','a','b') and name.startswith('reciprocal')) or key=='scale':
            if not v:raise ValueError('zero defining coefficient')
    if name.startswith('reciprocal'):
        if any(not 1<=abs(base['scale']*base[k])<=3 for k in ('a','b')):
            raise ValueError('hard displayed coefficient magnitude must be 1..3')
    if profile=='observed_scale' and any(base[k]!=v for k,v in TEMPLATES[name][2].items()):
        raise ValueError('observed bank underdetermined beyond homogeneous potential scaling')
    return base

def sample_parameters(name,rng,profile):
    if profile=='observed_scale':return {'scale':rng.choice([-3,-2,-1,1,2,3]),**TEMPLATES[name][2]}
    p={'scale':1 if name.startswith('reciprocal') else rng.choice([-3,-2,-1,1,2,3])}
    for key,(lo,hi) in BOUNDS[name].items():
        p[key]=rng.randint(lo,hi)
        if key in ('a','b') and name.startswith('reciprocal'):
            p[key]=rng.choice([-3,-2,-1,1,2,3])
    return p

def _instance(level,seed,name,p,profile):
    base,curve,a,b=components(name,p);f=p['scale']*base
    A=tuple(simplify(v.subs(t,a)) for v in curve);B=tuple(simplify(v.subs(t,b)) for v in curve)
    fa,fb=evaluate(f,A),evaluate(f,B);answer=simplify(fb-fa)
    if profile=='observed_scale':
        options=[('observed_component_'+str(i),simplify(p['scale']*v)) for i,v in enumerate(OBSERVED_BANKS[name])]
        if sum(simplify(v-answer)==0 for _,v in options)!=1:raise SampleRejected('observed correct correspondence')
        options=[('correct' if simplify(v-answer)==0 else label,v) for label,v in options]
        prompt=source_prompt(name,p['scale']);sol=source_solution(name,p['scale'])
        option_tex=[tex(v) for _,v in options]
    else:
        options=authored_bank(name,f,curve,a,b,A,B,fa,fb);option_tex=[tex(v) for _,v in options]
        variables='x,y' if len(curve)==2 else 'x,y,z'
        prompt=('Let $f('+variables+')='+tex(f)+'.$ Given that $C$ is the path along the curve $r(t)=⟨'+point_tex(curve)+
           r'⟩$ for $t\in ['+tex(a)+','+tex(b)+r'],$ evaluate ${\int }_{C}∇f\cdot \text{d}r.$')
        sol=generic_solution(f,curve,a,b,A,B,fa,fb,name,p['scale'])
    mathematical={'potential':sp.srepr(f),'curve':[sp.srepr(v) for v in curve],'a':sp.srepr(sp.sympify(a)),'b':sp.srepr(sp.sympify(b))}
    fingerprint=hashlib.sha256(json.dumps(mathematical,sort_keys=True).encode()).hexdigest()
    content={'version':VERSION,'problem':prompt,'solution':sol,'bank':sorted(option_tex),'math':fingerprint}
    content_fingerprint=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    qid=uuid.uuid5(uuid.UUID(KP_UUID),content_fingerprint);fid=uuid.uuid5(qid,'selection')
    answers=[];recipe_map={}
    for (recipe,value),display in zip(options,option_tex):
        aid=str(uuid.uuid5(fid,'math:'+display));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':display})
        recipe_map[aid]={'operation':recipe,'expression':sp.srepr(value)}
        if recipe=='correct':correct=aid
    random.Random(seed).shuffle(answers)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
       'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,
        ':question/problem':prompt,':question/worked-solution':sol,
        ':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
         ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},
       'generation':{'version':VERSION,'sympy_version':sp.__version__,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,
         'bank_origin':'observed_homogeneous_replay' if profile=='observed_scale' else 'authored',
         'authored_extension':profile!='observed_scale','source_analysis':{k:SOURCE[k] for k in ('database','basis','lineage')},
         'source_ids':[TEMPLATES[name][1]] if TEMPLATES[name][1] else ['e-8759'],
         'mathematical_fingerprint':fingerprint,'parameter_fingerprint':fingerprint,'content_fingerprint':content_fingerprint,
         'mathematical_components':mathematical,'endpoint_values':[sp.srepr(fa),sp.srepr(fb)],
         'distractor_recipes':recipe_map,'plot_rating':'none','plot_assets':{},
         'domain':'real smooth supplied curve; sqrt endpoint uses one-sided continuous endpoint; all potentials globally smooth',
         'source_solution_repair':list(REPAIRS.get(TEMPLATES[name][1],()))}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('invalid difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio layout is supported')
    names=[k for k,v in TEMPLATES.items() if v[0]==level]
    if template is not None and template not in names:raise ValueError('template does not belong to level')
    rng=random.Random(seed);name=template or rng.choice(names);profile=profile or 'authored_endpoint_bank'
    if profile not in ('observed_scale','authored_endpoint_bank'):raise ValueError('unknown profile')
    if profile=='observed_scale' and TEMPLATES[name][1] is None:raise ValueError('hard has no observed bank')
    if parameters is not None:return _instance(level,seed,name,normalize_parameters(name,parameters,profile),profile)
    for _ in range(1000):
        p=normalize_parameters(name,sample_parameters(name,rng,profile),profile)
        try:return _instance(level,seed,name,p,profile)
        except SampleRejected:pass
    raise SampleRejected('no eligible complete bank')

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(record):
    q=record['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
    p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1)
    p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template');p.add_argument('--profile')
    args=p.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
