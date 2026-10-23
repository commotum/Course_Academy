#!/usr/bin/env python3
"""Finite tangent slopes at a supplied parameter; math basis 4664, tutorial 1068 and target step 644788.

20 observed field/value templates, 13 observed complete radio profiles. All three
levels observed. Source scalar banks do not identify author intent: empirical
profiles retain complete parameterized expression patterns for replay, while
normal generation uses declared derivative scale/sign banks. No DB access.
Source real-domain errors in two reciprocal-root questions are repaired to t>0.
All displayed mathematics is independently parsed and checked by validate.py.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid, os
from math_format import checked_math_content, normalize_prose, normalize_tex
from pathlib import Path
import sympy as s
KP_ID=17592186083243
KP_UUID=''
TITLE='Calculating the Slope of the Tangent to a Parametric Curve at a Given Point'
VERSION='finite-parametric-slope-4'
HERE=Path(__file__).resolve().parent
SOURCE=json.loads((HERE/'source-data.json').read_text())
KP_UUID=SOURCE['record'][':knowledge-point/id']
T=s.Symbol('t',positive=True)
# A source ID here identifies a layout/provenance example, never a payload branch.
TEMPLATES={
 'double_sin_radio':('easy','radio','double_sin','q-102922',False),
 'double_cos_radio':('easy','radio','double_cos','q-15457',False),
 'poly5_radio':('easy','radio','poly5','q-102940',False),
 'trig_poly_radio':('easy','radio','trig_poly','q-102941',False),
 'cubic_radio':('easy','radio','cubic','q-6730',True),
 'cubic_blank':('easy','blank','cubic','q-348303',True),
 'linear_trig_radio':('easy','radio','linear_trig','q-15465',False),
 'poly4_radio':('easy','radio','poly4','q-15469',False),
 'harmonic_radio':('moderate','radio','harmonic','q-6808',True),
 'harmonic_blank':('moderate','blank','harmonic','q-348304',True),
 'ellipse_blank':('moderate','blank','ellipse','q-353350',True),
 'exp_log_blank':('moderate','blank','exp_log','q-353352',True),
 'exp_product_radio':('moderate','radio','exp_product','q-15470',False),
 'log_product_blank':('moderate','blank','log_product','q-353353',True),
 'sec_csc_radio':('hard','radio','sec_csc','q-15477',False),
 'exp_root_radio':('hard','radio','exp_root','q-20991',False),
 'exp_root_blank':('hard','blank','exp_root','q-348305',False),
 'reciprocal_exp_root_radio':('hard','radio','reciprocal_exp_root','q-15475',False),
 'reciprocal_exp_root_blank':('hard','blank','reciprocal_exp_root','q-363490',False),
 'nested_trig_radio':('hard','radio','nested_trig','q-15476',False),
}
# Fixed coefficients below are source expression-pattern hypotheses only. They
# are retained as explicit replay profiles and are NEVER default error banks.
BANK_PROFILES={ 'observed_'+v[3]:k for k,v in TEMPLATES.items() if v[1]=='radio'}
BANK_PROFILES.update({'authored_'+f:k for k,(l,kind,f,q,plot) in TEMPLATES.items() if kind=='radio'})
PARAMETERS={
 'q-353352':dict(a=2,b=2,u=0), 'q-15470':dict(a=1,b=1,c=1,u=0),
 'q-353353':dict(a=3,b=1,u=0), 'q-15477':dict(a=1,b=1,u='pi/4'),
 'q-102922':dict(a=1,b=1,u='pi/12'), 'q-15457':dict(a=1,b=1,u='pi/6'),
 'q-102940':dict(a=2,b=3,c=3,u=1), 'q-102941':dict(a=4,b=4,u='pi/4'),
 'q-6730':dict(a=1,b=1,u=2), 'q-348303':dict(a=2,b=1,u=2),
 'q-15465':dict(a=1,b=1,u='pi/2'), 'q-15469':dict(a=2,b=1,c=2,u=1),
 'q-6808':dict(a=4,b=3,n=2,u='pi/6'),
 'q-348304':dict(a=6,b=2,n=3,u='pi/4'),
 'q-353351':dict(a=3,b=4,n=2,u='pi/3'),
 'q-353350':dict(a=2,b=3,u='pi/4'),
 'q-20991':dict(a=2,b=2,u=5), 'q-348305':dict(a=3,b=3,u=4),
 'q-15475':dict(a=1,b=1,c=-1,u=2),
 'q-363490':dict(a=3,b=1,c=4,u=1), 'q-353363':dict(a=2,b=1,c=1,u=1),
 'q-15476':dict(a=1,b=1,u='log(pi/6)'),
}
SOURCE_TEMPLATE={v[3]:k for k,v in TEMPLATES.items()}
SOURCE_TEMPLATE.update({'q-353351':'harmonic_blank','q-353363':'reciprocal_exp_root_blank'})
SOURCE_ASSETS={}
for q in SOURCE['record'][':knowledge-point/questions']:
 import re
 refs=re.findall(r'!\[\]\((images/[^)]+)\)',q[':question/problem'])
 if refs: SOURCE_ASSETS[q[':question/math-academy-id']]=refs[0]

def expr(v): return s.sympify(v,locals={'pi':s.pi,'log':s.log})
def tex(v): return s.latex(v,fold_func_brackets=True,mul_symbol=None).replace(r'\log',r'\ln')
def block(v): return '\n\n$$\n'+v+'\n$$'
def aligned(values,lhs=r'\frac{dy}{dx}'):
 return r'\begin{aligned}'+lhs+' & ='+r' \\  & ='.join(values)+r'.\end{aligned}'
def frac(n,d): return r'\frac{'+n+'}{'+d+'}'
def bracket(v): return r'\left('+v+r'\right)'
def canon(v): return s.sstr(s.simplify(v))
def fingerprint(data): return hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def ident(payload): return str(uuid.uuid5(uuid.NAMESPACE_URL,'parametric-slope:'+payload))

def mathematics(f,p):
 a,b,u=[expr(p[k]) for k in ('a','b','u')];c=expr(p.get('c',0));n=expr(p.get('n',2))
 if f=='double_sin': x=a*s.sin(2*T);y=b*s.sin(T)**2;dx=2*a*s.cos(2*T);dy=b*s.sin(2*T);ratio=b*s.tan(2*T)/(2*a);domain=r'0\le t<2\pi'
 elif f=='double_cos': x=a*s.sin(2*T);y=b*s.cos(T)**2;dx=2*a*s.cos(2*T);dy=-b*s.sin(2*T);ratio=-b*s.tan(2*T)/(2*a);domain=r'0\le t<2\pi'
 elif f=='poly5': x=a*T**2+c;y=b*T**5+T**3;dx=2*a*T;dy=3*T**2*(s.Rational(5,3)*b*T**2+1);ratio=T*(5*b*T**2+3)/(2*a);domain=r'0\le t<\infty'
 elif f=='trig_poly': x=a*s.sin(T);y=b*T**2/s.pi;dx=a*s.cos(T);dy=2*b*T/s.pi;ratio=2*b*T*s.sec(T)/(a*s.pi);domain=r'0\le t<2\pi'
 elif f=='cubic': x=T**3+a*T**2;y=b*T**2;dx=3*T**2+2*a*T;dy=2*b*T;ratio=2*b/(3*T+2*a);domain=r'-\infty<t<\infty'
 elif f=='linear_trig': x=a*T+s.sin(T);y=b*T+s.cos(T);dx=a+s.cos(T);dy=b-s.sin(T);ratio=dy/dx;domain=r'0\le t<2\pi'
 elif f=='poly4': x=a*T**3+1;y=b*T**4+c*T**2;dx=3*a*T**2;dy=2*T*(2*b*T**2+c);ratio=2*(2*b*T**2+c)/(3*a*T);domain=r'0\le t<\infty'
 elif f=='harmonic': x=a*s.cos(T);y=b*s.sin(n*T);dx=-a*s.sin(T);dy=n*b*s.cos(n*T);ratio=-n*b*s.cos(n*T)/(a*s.sin(T));domain=r'0\le t<2\pi'
 elif f=='ellipse': x=a*s.sin(T);y=b*s.cos(T);dx=a*s.cos(T);dy=-b*s.sin(T);ratio=-b*s.tan(T)/a;domain=r'0\le t<2\pi'
 elif f=='exp_log': x=s.exp(a*T);y=s.log(T+b);dx=a*s.exp(a*T);dy=1/(T+b);ratio=1/(a*s.exp(a*T)*(T+b));domain=tex(-b)+r'<t<\infty'
 elif f=='exp_product': x=a*s.exp(T)-c*s.exp(-T);y=b*T*s.exp(T);dx=a*s.exp(T)+c*s.exp(-T);dy=b*(T+1)*s.exp(T);ratio=b*(T+1)/(a+c*s.exp(-2*T));domain=r'-\infty<t<\infty'
 elif f=='log_product': x=s.log(a*T+1);y=b*T*s.exp(T);dx=a/(a*T+1);dy=b*(T+1)*s.exp(T);ratio=b*(T+1)*(a*T+1)*s.exp(T)/a;domain=tex(-1/a)+r'<t<\infty'
 elif f=='sec_csc': x=a*s.sec(T)**2;y=b*s.csc(T)**3;dx=2*a*s.sec(T)**2*s.tan(T);dy=-3*b*s.csc(T)**3*s.cot(T);ratio=-3*b*s.csc(T)*s.cot(T)**4/(2*a);domain=r'0<t<\frac{\pi}{2}'
 elif f=='exp_root': x=1/(a*s.sqrt(T));y=s.exp(T)/(b*T);dx=-T**s.Rational(-3,2)/(2*a);dy=s.exp(T)*(T-1)/(b*T**2);ratio=-2*a*s.exp(T)*(T-1)/(b*s.sqrt(T));domain=r'0<t<\infty'
 elif f=='reciprocal_exp_root': x=s.exp(a/T);y=b/s.sqrt(T**2+c);dx=-a*s.exp(a/T)/T**2;dy=-b*T/(T**2+c)**s.Rational(3,2);ratio=b*T**3*s.exp(-a/T)/(a*(T**2+c)**s.Rational(3,2));domain=(tex(s.sqrt(-c))+r'<t<\infty') if c<0 else r'0<t<\infty'
 elif f=='nested_trig': x=a*s.sqrt(s.sin(s.exp(T)));y=b*s.cot(s.exp(T));dx=a*s.exp(T)*s.cos(s.exp(T))/(2*s.sqrt(s.sin(s.exp(T))));dy=-b*s.exp(T)*s.csc(s.exp(T))**2;ratio=-2*b/(a*s.sin(s.exp(T))**s.Rational(3,2)*s.cos(s.exp(T)));domain=r'-\infty<t<1'
 else: raise ValueError(f)
 if f in ('poly5','poly4'): dy=s.factor(dy);ratio=s.factor(ratio)
 return dict(x=x,y=y,dx=dx,dy=dy,ratio=ratio,m=s.simplify(ratio.subs(T,u)),u=u,domain=domain)

def validate_parameters(f,p):
 expected=set(PARAMETERS[next(q for q,k in SOURCE_TEMPLATE.items() if TEMPLATES[k][2]==f)])
 if set(p)!=expected: raise ValueError('Exact parameters required: '+str(expected))
 for k in expected-{'u','c'}:
  v=expr(p[k]);
  if not v.is_Integer or v<=0 or v>12: raise ValueError('positive integer coefficient required')
 if 'c' in p and (not expr(p['c']).is_Integer or abs(expr(p['c']))>12): raise ValueError('small integer c required')
 if f=='harmonic' and p['n'] not in (2,3): raise ValueError('observed harmonic frequencies 2 or 3')
 d=mathematics(f,p);u=d['u']
 if u.free_symbols or u.is_real is False: raise ValueError('real finite parameter required')
 common=[s.pi*k for k in (s.Rational(1,6),s.Rational(1,4),s.Rational(1,3),s.Rational(2,3),s.Rational(3,4),s.Rational(5,6),s.Rational(7,6),s.Rational(5,4),s.Rational(4,3),s.Rational(5,3),s.Rational(7,4),s.Rational(11,6))]
 allowed={'linear_trig':[s.pi/2,3*s.pi/2],'trig_poly':[s.pi/4,3*s.pi/4,5*s.pi/4,7*s.pi/4],'harmonic':common,'ellipse':common,'sec_csc':[s.pi/6,s.pi/4,s.pi/3],'double_sin':[s.pi*k for k in (s.Rational(1,12),s.Rational(1,6),s.Rational(1,3),s.Rational(5,12),s.Rational(7,12),s.Rational(2,3),s.Rational(5,6),s.Rational(11,12))],'double_cos':[s.pi*k for k in (s.Rational(1,12),s.Rational(1,6),s.Rational(1,3),s.Rational(5,12),s.Rational(7,12),s.Rational(2,3),s.Rational(5,6),s.Rational(11,12))]}
 if f in allowed and not any(s.simplify(u-v)==0 for v in allowed[f]):raise ValueError('evaluation angle outside same-workload policy')
 if f in ('exp_log','exp_product','log_product') and (not u.is_Integer or abs(u)>2):raise ValueError('small integer exponential parameter required')
 if f=='exp_log' and u+expr(p['b'])<=0:raise ValueError('logarithm domain')
 if f=='log_product' and expr(p['a'])*u+1<=0:raise ValueError('logarithm domain')
 if f=='sec_csc' and not 0<u<s.pi/2:raise ValueError('first quadrant required')
 if f=='nested_trig' and not any(s.simplify(s.exp(u)-v)==0 for v in (s.pi/6,5*s.pi/6)):raise ValueError('nested angle must preserve half-sine root workload')
 if f in ('poly5','poly4','cubic','exp_root','reciprocal_exp_root') and (not u.is_Integer or abs(u)>6):raise ValueError('small integer parameter required')
 if f in ('double_sin','double_cos','trig_poly','linear_trig','harmonic','ellipse') and not (0<=u<2*s.pi): raise ValueError('parameter outside interval')
 if f in ('poly5','poly4','exp_root','reciprocal_exp_root') and u<=0: raise ValueError('positive evaluation parameter required')
 if f=='reciprocal_exp_root' and u*u+expr(p['c'])<=0: raise ValueError('radical domain')
 if f=='nested_trig' and not (u<1 and s.sin(s.exp(u))>0): raise ValueError('nested real-domain violation')
 if d['dx'].subs(T,u)==0 or d['m'].has(s.zoo,s.oo,-s.oo,s.nan) or d['m'].is_real is False: raise ValueError('finite regular slope required')
 return d

def sample(f,rng):
 # Decide target evaluation/frequency first; then sample compatible coefficients.
 common=['pi/6','pi/4','pi/3','2*pi/3','3*pi/4','5*pi/6','7*pi/6','5*pi/4','4*pi/3','5*pi/3','7*pi/4','11*pi/6']
 cases={
  'double_sin':['pi/12','pi/6','pi/3','5*pi/12','7*pi/12','2*pi/3','5*pi/6','11*pi/12'],
  'double_cos':['pi/12','pi/6','pi/3','5*pi/12','7*pi/12','2*pi/3','5*pi/6','11*pi/12'],
  'trig_poly':['pi/4','3*pi/4','5*pi/4','7*pi/4'],
  'linear_trig':['pi/2','3*pi/2'], 'harmonic':common,'ellipse':common,
  'sec_csc':['pi/6','pi/4','pi/3'],'cubic':[-3,-2,-1,1,2,3],
  'exp_root':[1,2,3,4,5,6], 'exp_log':[0,1,2],
  'exp_product':[-2,-1,0,1,2], 'log_product':[0,1,2],
  'poly5':[1,2,3], 'poly4':[1,2,3], 'reciprocal_exp_root':[2,3,4],
  'nested_trig':['log(pi/6)','log(5*pi/6)']}
 u=rng.choice(cases[f]);n=rng.choice([2,3]) if f=='harmonic' else None
 a,b=rng.randint(1,6),rng.randint(1,6)
 p=dict(a=a,b=b,u=u)
 if f=='poly5':p['c']=rng.randint(-4,6)
 if f=='poly4':p['c']=rng.randint(1,5)
 if f=='exp_product':p['c']=rng.randint(1,6)
 if f=='reciprocal_exp_root':p['c']=rng.choice([-1,1,2,3,4])
 if f=='harmonic':p['n']=n
 return p

def sample_bank_factors(rng):
 # Select a complete bank and its eligible correct role before curve values.
 # Every palette member can be the key, so the bank's magnitude envelope does
 # not distinguish it. Small ratios express coefficient/sign arithmetic errors.
 magnitudes=sorted(rng.sample([1,2,3,4,6],4))
 negative=set(rng.sample(range(4),2))
 palette=[-v if i in negative else v for i,v in enumerate(magnitudes)]
 key_role=rng.randrange(4)
 return [str(s.Rational(v,palette[key_role])) for i,v in enumerate(palette) if i!=key_role]
HORIZONTAL_BANK_TARGETS={'exp_product':[-2,0,1,2], 'exp_root':[2,3,4,5,6]}

def bank(f,p,d,profile,bank_factors=None,bank_anchor_target=None,bank_partner=None):
 a,b,u=expr(p['a']),expr(p['b']),d['u'];m=d['m'];c=expr(p.get('c',0));n=expr(p.get('n',2))
 if profile.startswith('observed_'):
  if f=='exp_product':return [m/2,4*m/3,6*m,4*m,m],['half slope','four thirds slope','sixfold slope','fourfold slope','correct']
  if f=='sec_csc':return [m/3,-2*b/a,2*m/3,m,2*m/9],['omit cubic factor','alter trig factors','omit half factor','correct','alter cubic and half factors']
  if f=='double_sin': return [m,-3*m,6*m,-m,3*m],['correct','empirical -3m','empirical 6m','sign reversal','empirical 3m']
  if f=='double_cos': return [-2*m,-b/(2*a),m,2*m,b/(2*a)],['empirical -2m','omit tan','correct','omit half factor','omit tan and sign']
  if f=='poly5': return [(3*b*u**4+2*u**2)/(2*a),5*b*u**4/(2*a),(3*b*u**4+2*u**2)/a,m,3*u**2/a],['alter derivative powers','omit cubic derivative','compound scale error','correct','omit fifth derivative']
  if f=='trig_poly': return [m,4*m,2*m,2*b*u/(a*s.pi),8*b*u/(a*s.pi)],['correct','empirical 4m','omit factor cancellation','omit sec','omit sec and double']
  if f=='cubic': return [2*m,m,s.Rational(1,3*u),2*b/(3*u+2*a+2*b),2*b/(3*u)],['empirical double','correct','omit quadratic derivative and y factor','empirical denominator shift','omit quadratic derivative']
  if f=='linear_trig': return [s.sqrt(2)*b/a,b/(2*a),b/a,b/(s.sqrt(2)*a),m],['empirical sqrt2 scale','empirical half scale','linear coefficient ratio','empirical reciprocal sqrt2','correct']
  if f=='poly4': return [m/2,2*m,m,1/m,2/m],['omit y factor','extra y factor','correct','reciprocal','double reciprocal']
  if f=='harmonic': return [-b/((a-1)*s.sqrt(2)),-a/(n*b),-b/(n*(a-1)),-4*b/(a*s.sqrt(2)),m],['empirical sqrt2 scaled','coefficient reciprocal sign','alter coefficient/frequency','empirical scale sqrt2','correct']
  if f=='exp_root': return [2*a*s.exp(u)*(u-1)/(b*s.sqrt(u-2)),-a*u*s.exp(u-1)/(b*s.sqrt(u+1)),-a*(u-1)*s.exp(u)/(b*s.sqrt(u-3)),a*s.exp(u-2)/(b*s.sqrt(u)),m],['alter sign and radical','alter factors and exponential','alter factor and radical','alter factors exponent and sign','correct']
  if f=='reciprocal_exp_root':
   z=u*u+c;E=s.exp(2*a/u)
   return [m,s.sqrt(u**3*E/z**3),s.sqrt(z**2*E)/u**2,u**2/s.sqrt(z**2*E),s.sqrt(z**2/(u**3*E))],['correct','compound root/exponential error','alter power and exponent','alter powers','compound reciprocal-root error']
  if f=='nested_trig':
   v=s.exp(u);si,co=s.sin(v),s.cos(v);return [m,m/4,-b*s.sqrt(si)/(2*a*co),m*co**2,m*co**2/2],['correct','empirical quarter slope','empirical root/cosine expression','empirical cosine-squared factor','empirical half cosine-squared factor']
  raise ValueError(profile)
 # Authored full coefficient-palette bank: no first-valid recipe selection.
 # Wrong scales model omitted/extra derivative coefficients; their exact pattern
 # is an authored extension, not an inferred source author's intention.
 factors=bank_factors or ['1/2','2','-1']
 if f in HORIZONTAL_BANK_TARGETS:
  # Two coefficient roles at each exponential anchor. Even at a horizontal
  # target there are TWO nonzero choices with the correct exponential power.
  # Common scaling lets either nonhorizontal role be the correct response.
  if bank_anchor_target not in HORIZONTAL_BANK_TARGETS[f] or bank_partner not in range(3):raise ValueError('complete exponential bank profile required')
  anchor=mathematics(f,dict(p,u=bank_anchor_target))['m'] if m==0 else m
  omission=(-2*a*s.E/b if f=='exp_root' else s.sign(anchor)*b/(a+c*s.exp(2)))
  scales=[abs(expr(k)) for k in factors]
  other=[v for i,v in enumerate(scales) if i!=bank_partner]
  vals=[0,anchor,anchor*scales[bank_partner]]+[omission*v for v in other]
  v=bank_anchor_target if m==0 else u
  return vals,['correct' if m==0 else 'horizontal slope','correct' if m!=0 else 'substitute t='+str(v),'substitute t='+str(v)+'; derivative coefficient '+str(scales[bank_partner])]+['omit horizontal zero factor; coefficient/sign '+str(k) for k in other]
 base=m if m!=0 else b/a
 vals=[m,0]+[base*expr(k) for k in factors] if m!=0 else [0]+[base*expr(k) for k in ['1']+factors]
 return vals,['correct','horizontal slope' if m!=0 else 'omit trig cancellation']+['derivative scale/sign '+k for k in factors]

def source_curve_asset(f,p):
 for q,ref in SOURCE_ASSETS.items():
  if TEMPLATES[SOURCE_TEMPLATE[q]][2]!=f:continue
  if all(canon(expr(p[k]))==canon(expr(v)) for k,v in PARAMETERS[q].items() if k!='u'):
   return ref
 return None

def render_plots(template,p,d):
 if not TEMPLATES[template][4]:return {}
 f=TEMPLATES[template][2];asset=source_curve_asset(f,p)
 if asset:return {'prompt':asset,'origin':'unchanged-source-curve'}
 from plotter import render_curve
 out=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
 if not out:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required for new assets')
 root=Path(out).resolve();root.mkdir(parents=True,exist_ok=True)
 h=fingerprint({'family':f,'parameters':{k:v for k,v in p.items() if k!='u'},'renderer':'portable-1'})[:24]
 target=root/('curve-'+h+'.png')
 if not target.exists():render_curve(f,p,target)
 return {'prompt':str(target),'origin':'parameterized-matplotlib','curve_fingerprint':h}

def presentation(template,p,d,assets,source_wording=False):
 level,kind,f,src,plot=TEMPLATES[template];a,b,u=expr(p['a']),expr(p['b']),d['u'];c=expr(p.get('c',0));n=expr(p.get('n',2))
 ut=tex(u)
 prompt=('![]('+assets['prompt']+')\n\n' if assets else '')+'For the parametric curve '+block('x='+tex(d['x'])+r',\,y='+tex(d['y'])+r',\,'+d['domain']+',')+'\n\n'
 if kind=='blank': prompt+=('shown above, ' if plot else '')+'calculate the slope $m$ of the tangent to the curve at the point where $t='+ut+'.$ '+'Do not round the answer.'+'\n\n$m=$\n{{field-1}}'
 else: prompt+=('shown above, ' if plot else '')+'calculate the slope of the tangent to the curve at the point where $t='+ut+'.$'
 # Derivative blocks retain factorization, the source identity/quotient stages,
 # and nested chain factors. Each expression is computed from the prompt params.
 deriv=r"x'(t)="+tex(d['dx'])+r",\,y'(t)="+tex(d['dy'])+'.'
 if f in ('double_sin','double_cos'):
  raw=(2*b if f=='double_sin' else -2*b)*s.sin(T)*s.cos(T)
  deriv=r"x'(t)="+tex(d['dx'])+r",\,y'(t)="+tex(raw)+'='+tex(d['dy'])+'.'
 if f=='exp_root':
  uns=frac(tex(b*T*s.exp(T)-b*s.exp(T)),tex(b*b*T*T))
  deriv=r"x'(t)="+tex(d['dx'])+r",\,y'(t)="+uns+'='+tex(d['dy'])+'.'
 if f=='nested_trig':
  first=frac(tex(a),tex(2*s.sqrt(s.sin(s.exp(T)))))+r'\cdot '+tex(s.cos(s.exp(T)))+r'\cdot '+tex(s.exp(T))
  deriv=r"\begin{aligned}x'(t)&="+first+r"\\ &= "+tex(d['dx'])+r",\\ y'(t)&="+tex(d['dy'])+r'.\end{aligned}'
 ratio=[frac(bracket(tex(d['dy'])),bracket(tex(d['dx']))),tex(d['ratio'])]
 if f=='exp_root': ratio[0]=tex(d['dy'])+r'\cdot '+bracket(tex(1/d['dx']))
 if f=='sec_csc':
  coefficient=tex(-3*b/(2*a))
  ratio=[ratio[0],
   tex(-3*b*s.csc(T)**3*s.cot(T))+bracket(frac(tex(s.cos(T)**2*s.cot(T)),tex(2*a))),
   coefficient+r'\,'+tex(s.csc(T)**3*s.cot(T)**2*s.cos(T)**2),
   coefficient+bracket(frac('1',tex(s.sin(T)**3)))+bracket(frac(tex(s.cos(T)**2),tex(s.sin(T)**2)))+tex(s.cos(T)**2),
   tex(-3*b*s.cos(T)**4/(2*a*s.sin(T)**5)),tex(d['ratio'])]
 if f=='nested_trig': ratio.insert(1,frac(tex(-2*b*s.sqrt(s.sin(s.exp(T)))),tex(a*s.sin(s.exp(T))**2*s.cos(s.exp(T)))))
 # Keep the separate evaluation and simplification rows. Substitute into the
 # rendered ratio without letting symbolic substitution hide special angles.
 subtex=re.sub(r'(?<![A-Za-z])t(?![A-Za-z])',lambda _:bracket(ut),tex(d['ratio']))
 evaluation=[subtex]
 if f in ('double_sin','double_cos','trig_poly','harmonic','ellipse','linear_trig','nested_trig','sec_csc'):
  expanded=s.expand_trig(d['ratio']) if f=='linear_trig' else d['ratio']
  # A non-evaluating substitution gives a human-visible exact special-angle row.
  trig_atoms=list(expanded.atoms(s.sin,s.cos,s.tan,s.sec,s.cot,s.csc))
  evaltext=tex(expanded)
  for atom in sorted(trig_atoms,key=lambda z:len(tex(z)),reverse=True):
   val=s.simplify(atom.subs(T,u));evaltext=evaltext.replace(tex(atom),bracket(tex(val)))
  evaltext=re.sub(r'(?<![A-Za-z])t(?![A-Za-z])',lambda _:bracket(ut),evaltext)
  if f=='nested_trig':
   evaltext=frac(tex(-2*b),tex(a)+bracket(tex(s.sin(s.exp(u))))+r'^{3/2}'+bracket(tex(s.cos(s.exp(u)))))
  if f=='sec_csc':
   evaltext=frac(tex(-3*b)+r'\cdot '+bracket(tex(s.csc(u)))+r'\cdot '+bracket(tex(s.cot(u)))+r'^{4}',tex(2*a))
  evaluation.append(evaltext)
 else:
  # Unevaluated numerator/denominator powers preserve the pre-reduction row.
  numerator,denominator=s.fraction(d['ratio']);num=numerator.subs(T,u);den=denominator.subs(T,u)
  evaluation.append(frac(tex(num),tex(den)))
 evaluation.append(tex(d['m']))
 if kind=='blank': lhs='m='+r'\frac{dy}{dx}\,{|}_{t='+ut+'}'
 else: lhs=r'\frac{dy}{dx}'
 solution='We will use the formula'+block(r"\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.")+'\n\nDifferentiating $x$ and $y,$ we get'+block(deriv)+'\n\n \n\n'+('So, we have' if kind=='blank' else 'So we have')+block(aligned(ratio))+'\n\nTherefore, when $t='+ut+',$ the slope '+('$m$ ' if kind=='blank' else '')+'of the tangent to the curve is'+block(aligned(evaluation,lhs))
 return prompt,solution

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'): raise ValueError('unknown level')
 rng=random.Random(seed)
 eligible=[k for k,v in TEMPLATES.items() if v[0]==level and (field_type is None or v[1]==field_type.removeprefix(':answer-field.type/'))]
 if profile and profile!='observed':
  if profile not in BANK_PROFILES: raise ValueError('unknown bank profile')
  if template is None: template=BANK_PROFILES[profile]
 if template is None: template=rng.choice(eligible)
 if template not in eligible: raise ValueError('template/level/field mismatch')
 _,kind,f,src,_=TEMPLATES[template]
 source_wording=kind=='blank' and profile=='observed'
 if profile=='observed' and kind!='blank':raise ValueError('observed wording profile is only for blank templates')
 if kind=='blank' and profile not in (None,'observed'): raise ValueError('blank has no bank profile')
 if source_wording:profile=None
 if profile and BANK_PROFILES[profile]!=template: raise ValueError('bank profile/template mismatch')
 profile=profile or ('authored_'+f if kind=='radio' else None)
 bank_factors=sample_bank_factors(rng) if kind=='radio' and profile.startswith('authored_') else None
 bank_partner=rng.randrange(3) if bank_factors and f in HORIZONTAL_BANK_TARGETS else None
 bank_anchor_target=rng.choice(HORIZONTAL_BANK_TARGETS[f]) if bank_factors and f in HORIZONTAL_BANK_TARGETS else None
 rejections=[]
 for attempt in range(300):
  p=dict(parameters) if parameters is not None else sample(f,rng)
  try:
   d=validate_parameters(f,p)
   vals,recipes=bank(f,p,d,profile,bank_factors,bank_anchor_target,bank_partner) if kind=='radio' else ([d['m']],['correct'])
   vals=[s.simplify(v) for v in vals]
   if any(v.has(s.zoo,s.oo,-s.oo,s.nan) or v.is_real is False for v in vals): raise ValueError('nonreal or nonfinite bank')
   if any(s.simplify(a-b)==0 for i,a in enumerate(vals) for b in vals[i+1:]): raise ValueError('whole-bank collision')
   if sum(s.simplify(v-d['m'])==0 for v in vals)!=1: raise ValueError('ambiguous bank')
  except (ValueError,TypeError,ZeroDivisionError) as e:
   if parameters is not None: raise ValueError(str(e)) from e
   rejections.append(str(e))
   continue
  break
 else: raise ValueError('no valid complete bank sampled')
 assets=render_plots(template,p,d)
 prompt,solution=presentation(template,p,d,assets,source_wording)
 prompt,solution=normalize_prose(prompt),normalize_prose(solution)
 display=[normalize_tex(tex(v)) for v in vals]
 mathfp=fingerprint({'x':canon(d['x']),'y':canon(d['y']),'evaluation_parameter':canon(d['u']),'requested':'finite slope dy/dx','domain':d['domain']})
 content=fingerprint({'version':VERSION,'template':template,'parameters':mathfp,'prompt':prompt,'solution':solution,'bank':sorted(display),'profile':profile})
 qid=ident(content);fid=ident(qid+':field');answers=[];correct=None
 for value,v,recipe in zip(display,vals,recipes):
  aid=ident(fid+':'+value);answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
  if s.simplify(v-d['m'])==0: correct=aid
 rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/type':':answer-field.type/'+kind,':answer-field/key':'selection' if kind=='radio' else 'field-1',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'presentation_profile':'observed','profile_origin':'observed-expression-pattern' if profile and profile.startswith('observed_') else ('authored-operations' if profile else 'observed-blank'),'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[q for q,k in SOURCE_TEMPLATE.items() if k==template],'domain':d['domain'],'mathematical_fingerprint':mathfp,'parameter_fingerprint':mathfp,'content_fingerprint':content,'derivation':{k:canon(d[k]) for k in ('x','y','dx','dy','ratio','m')},'bank_factors':bank_factors,'bank_anchor_target':bank_anchor_target,'bank_partner':bank_partner,'sampling_rejections':rejections,'recipes':dict(zip(display,recipes)),'plots':assets,'sympy':s.__version__}}

# EASY: differentiate observed polynomials/basic trig and evaluate.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: scaled ellipse or frequency-two/three trig curves; exact angles.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: quotient/reciprocal exponential/root and nested chain rules, same slope.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+('\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']) if f[':answer-field/type'].endswith('/radio') else '')+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='moderate');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
