#!/usr/bin/env python3
"""Separable IVPs, captured math basis 1356; local review data only.

Twenty observed Markdown/stage templates are coordinate-translation recipes,
not source samplers: u=x-h translates the ODE, primitive, initial abscissa,
complete source bank, and domain together. h is any exact rational. Observed
banks are explicitly empirical shapes; no claim about original distractor intent.
Default radio banks instead use the documented method operations below. Three
coefficient/initial-value extensions retain the observed skill at each level.
JSON records use field-owned stable UUIDs. No EDB clients or database writes.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid, importlib.util
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
KP=CAPTURE['record']; KP_ID=KP[':db/id']; KP_UUID=KP[':knowledge-point/id']
VERSION='separable-ivp-3'
_parser_spec=importlib.util.spec_from_file_location('ivp_display_parser',ROOT/'parse_math.py')
DISPLAY=importlib.util.module_from_spec(_parser_spec);_parser_spec.loader.exec_module(DISPLAY)
X,Y,T,C=sp.symbols('x y t C',real=True)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# Exact independent inputs: ODE RHS, initial x, initial y, y-primitive,
# x-primitive. No particular answers or original correct IDs are stored here. The primitives differentiate to
# the separated integrands; initial values fix the additive constant.
MATH={
'q-4019':(2*X/Y**2,2,sp.real_root(13,3),Y**3/3,X**2),
'q-8310':(Y**2/X,1,2,-1/Y,sp.log(X)),
'q-104055':(1/sp.sin(Y),0,sp.pi/2,-sp.cos(Y),X),
'q-14310':(Y**2+1,sp.pi/2,1,sp.atan(Y),X),
'q-14312':(Y*sp.exp(-X),0,sp.exp(-1),sp.log(Y),-sp.exp(-X)),
'q-14313':(X**2/Y**2,1,2,Y**3/3,X**3/3),
'q-347853':(-2*Y**2,0,2,-1/Y,-2*X),
'q-355525':(sp.sin(4*X)/sp.cos(3*Y),sp.pi/8,0,sp.sin(3*Y)/3,-sp.cos(4*X)/4),
'q-355528':(4*X*sp.sqrt(Y),1,9,2*sp.sqrt(Y),2*X**2),
'q-355544':(sp.sec(7*X)**2/sp.sec(4*Y)**2,0,0,sp.tan(4*Y)/4,sp.tan(7*X)/7),
'q-355562':(X*Y,0,1,sp.log(Y),X**2/2),
'q-355578':(Y/X**2,1,sp.E,sp.log(Y),-1/X),
'q-355579':(Y/sp.sqrt(X),1,sp.exp(2),sp.log(Y),2*sp.sqrt(X)),
'q-50220':(-Y**2,1,1,-1/Y,-X),
'q-50566':(X/Y,-3,1,Y**2/2,X**2/2),
'q-8308':(Y,0,1,sp.log(Y),X),
'q-8309':(sp.sin(3*X)/sp.cos(2*Y),0,0,sp.sin(2*Y)/2,-sp.cos(3*X)/3),
'q-14309':(Y**2/(X**2+1),1,1,-1/Y,sp.atan(X)),
'q-50219':(-X*Y/sp.log(Y),0,sp.E,sp.log(Y)**2/2,-X**2/2),
}
# Complete authored operations. Each list has exactly four wrong expressions;
# retain one complete bank and reject any instance with an equivalent member.
# The explicit formulas express missed integral multipliers/signs/constants,
# incorrect integration, or incorrect inversion, rather than random perturbation.
def authored_wrong(s,u):
 return {
 'q-4019':[u**2+1,u**2/3+1,3*u**2-1,3*u**2+13],
 'q-8310':[2/(1+2*sp.log(u)),2/(1-sp.log(u)),2/(2-2*sp.log(u)),2*(1-2*sp.log(u))],
 'q-104055':[u,u+1,-u+sp.pi/2,-2*u],
 'q-14310':[sp.tan(u+sp.pi/4),sp.cot(u-sp.pi/4),sp.tan(u-sp.pi/2),u-sp.pi/4],
 'q-14312':[sp.exp(sp.exp(-u)),sp.exp(-u),sp.exp(-sp.exp(u)),sp.exp(-sp.exp(-u)-1)],
 'q-14313':[3*u**2+7,u**3+8,u**3-7,u**3/3+7],
 'q-50220':[1/(2-u),1/(u+1),1/(2*u-1),u],
 'q-50566':[-sp.sqrt(u**2-8),sp.sqrt(2*u**2-17),sp.sqrt(u**2+8),sp.sqrt(u**2+1)],
 'q-8308':[sp.exp(-u),1,sp.exp(2*u),u+1],
 'q-8309':[1-sp.cos(3*u),6*(1-sp.cos(3*u)),2*(1+sp.cos(3*u)),2*sp.cos(3*u)],
 'q-14309':[4/(sp.pi+4+4*sp.atan(u)),4/(sp.pi+4-2*sp.atan(u)),4/(4-4*sp.atan(u)),(sp.pi+4-4*sp.atan(u))/4],
 'q-50219':[1+u**2,1-2*u**2,(1-u)**2,sp.E-u**2],
 }[s]

OPERATION_RECIPES={
'q-4019':['omit_y_integral_multiplier','divide_instead_of_clear_y_denominator','reverse_initial_constant_sign','omit_initial_x_primitive'],
'q-8310':['reverse_reciprocal_integral_sign','omit_initial_amplitude_x_multiplier','initial_y_as_denominator_constant','multiply_instead_of_invert_denominator'],
'q-104055':['lose_sine_primitive_minus','lose_minus_and_use_initial_sine_constant','initial_y_as_constant','double_x_primitive'],
'q-14310':['reverse_initial_constant_sign','cot_instead_of_tan_inverse','omit_initial_arctangent_value','omit_inverse_tangent'],
'q-14312':['reverse_exponential_primitive_sign','report_coefficient_instead_of_exponentiating_primitive','reverse_primitive_exponent_input','omit_initial_primitive_in_constant'],
'q-14313':['omit_x_power_increment_and_clear_y_denominator','omit_initial_x_primitive','reverse_initial_constant_sign','omit_clearing_y_integral_denominator'],
'q-50220':['reverse_x_integral_sign_and_fit_initial','initial_y_as_constant','double_x_primitive_and_fit_initial','omit_reciprocal_inversion'],
'q-50566':['negative_square_root_branch','omit_x_integral_half_and_fit_initial','reverse_initial_constant_sign','omit_initial_x_primitive'],
'q-8308':['reverse_constant_primitive_sign','omit_x_primitive','double_x_primitive','add_instead_of_exponentiate_primitive'],
'q-8309':['omit_y_chain_multiplier','omit_x_chain_denominator','reverse_cosine_primitive_sign','omit_initial_cosine_subtraction'],
'q-14309':['reverse_arctangent_primitive_sign','halve_arctangent_coefficient','omit_initial_arctangent_in_constant','invert_particular_solution'],
'q-50219':['reverse_x_primitive_sign','double_x_primitive','integrate_both_separated_factors_as_constants_then_square','initial_y_instead_of_log_squared_constant'],
'exponential_rate':['reverse_exponential_rate','divide_instead_of_multiply_rate','add_instead_of_exponentiate_primitive','omit_initial_amplitude'],
'reciprocal_initial':['reverse_x_primitive_sign','omit_initial_amplitude_x_multiplier','initial_y_instead_of_reciprocal_constant','omit_reciprocal_inversion'],
 'trig_frequencies':['omit_y_chain_numerator','replace_y_chain_factor_with_x_frequency','reverse_cosine_primitive_sign','omit_initial_cosine_subtraction'],
}

def derive_particular(s,gy,fx,x0,y0):
 """Compute the integration constant from independent initial data, then
 invert exactly the template's separated primitive on its prescribed branch.
 No particular-answer slot or original choice designation is consulted.
 """
 constant=sp.simplify(gy.subs(Y,y0)-fx.subs(X,x0));integrated=sp.simplify(fx+constant)
 if s in ('q-4019','q-14313'):lhs,rhs=Y**3,3*integrated
 elif s in ('q-8310','q-347853','q-50220','q-14309'):lhs,rhs=Y,-1/integrated
 elif s=='q-104055':lhs,rhs=sp.cos(Y),-integrated
 elif s=='q-14310':lhs,rhs=Y,sp.tan(integrated)
 elif s in ('q-14312','q-355562','q-355578','q-355579','q-8308'):lhs,rhs=Y,sp.exp(integrated)
 elif s=='q-355525':lhs,rhs=sp.sin(3*Y),3*integrated
 elif s=='q-355528':lhs,rhs=Y,(integrated/2)**2
 elif s=='q-355544':lhs,rhs=sp.tan(4*Y),4*integrated
 elif s=='q-50566':lhs,rhs=Y,sp.sqrt(2*integrated)
 elif s=='q-8309':lhs,rhs=3*sp.sin(2*Y),6*integrated
 elif s=='q-50219':lhs,rhs=sp.log(Y)**2,2*integrated
 else:raise ValueError('unsupported primitive inversion')
 return lhs,sp.simplify(rhs),constant

TEMPLATES={s.replace('q-','source_'):{'level':q[':question/difficulty'][':db/ident'].split('/')[-1],
 'kind':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1], 'source':s,'origin':'observed'} for s,q in SOURCES.items()}
for name,level in [('exponential_rate','easy'),('reciprocal_initial','moderate'),('trig_frequencies','hard')]:
 TEMPLATES[name]={'level':level,'kind':'radio','source':{'easy':'q-8308','moderate':'q-50220','hard':'q-8309'}[level],'origin':'authored-coefficient-extension'}


def tex(e):return sp.latex(sp.sympify(e),order='lex')
def rational(v):
 e=sp.sympify(v)
 if not e.is_Rational:raise ValueError('translation/coefficients must be exact rational numbers')
 return e

def translated_math(content,h):
 """Translate only free x occurrences; preserve dx, y(x) labels and prose.

At evaluations the displayed original numerical abscissa denotes u=x-h.
Initial-condition calls are changed to their new abscissa before substitution.
No source-value branch: the same substitution pipeline runs at h=0.
 """
 def part(m):
  s=m.group(0); delim='$$' if s.startswith('$$') else '$'; body=s[len(delim):-len(delim)]
  protected=[]
  def protect(m):protected.append(m.group(0));return f'@@{len(protected)-1}@@'
  body=re.sub(r'\\text\{d\}x|\\textrm\{d\}x|(?<![A-Za-z])dx(?![A-Za-z])|y\(x\)',protect,body)
  # These source values are the only y(initial-x) calls, not arbitrary functions.
  body=re.sub(r'y\(([^()]*)\)',lambda z:'y('+tex(sp.sympify({'0':'0','1':'1','2':'2','-3':'-3',r'\frac{\pi }{2}':'pi/2',r'\frac{\pi }{8}':'pi/8'}[z[1]])+h)+')' if z[1] in ('0','1','2','-3',r'\frac{\pi }{2}',r'\frac{\pi }{8}') else z[0],body)
  if body.strip() not in ('x,','x',r'x\mathbin{:}'):
   # Protect TeX commands so the x in \text is never interpreted as a variable.
   body=re.sub(r'\\(?:operatorname|text|textrm)\{[^{}]*\}|\\[A-Za-z]+',protect,body)
   variable='x' if h==0 else r'\left('+tex(X-h)+r'\right)'
   # Adjacent variables denote multiplication: xy contains a free x too.
   # TeX commands, their text/function names, dx and y(x) are protected above.
   body=re.sub(r'x',lambda _:variable,body)
  for i,saved in enumerate(protected):body=body.replace(f'@@{i}@@',saved)
  return delim+body+delim
 return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*?\$',part,content)


def source_build(s,p,profile):
 q=SOURCES[s];h=rational(p['h']);f=q[':question/answer-fields'][0]
 if s=='q-168078':
  ambient=rational(p.get('ambient',25));initial=ambient+3;amplitude=sp.simplify(initial-ambient)
  def render(text):return re.sub(r'(?<!\d)(25|28)(?!\d)',lambda m:tex(ambient if m[0]=='25' else initial),text)
  problem=render(q[':question/problem']);solution=render(q[':question/worked-solution'])
  # Standalone questions must supply the known previous-part equation.
  if profile!='observed':problem='The general solution of the differential equation is $T='+tex(ambient)+r'+Ke^{-0.03t}.$'+'\n\n'+problem
  return problem,solution,[(None,ambient+amplitude*sp.exp(-sp.Rational(3,100)*T),render(f[':answer-field/choices'][0][':answer/value']))],{'variable':'t','initial_x':'0','initial_y':str(initial),'ode':str(-sp.Rational(3,100)*(Y-ambient)),'lhs':str(Y),'rhs':str(ambient+amplitude*sp.exp(-sp.Rational(3,100)*T)),'domain':'time t; positive decay rate 0.03; initial time 0','h':str(h)}
 problem=translated_math(q[':question/problem'],h);solution=translated_math(q[':question/worked-solution'],h)
 ode,x0,y0,gy,original_fx=map(sp.sympify,MATH[s]);u=X-h;fx=original_fx.subs(X,u);ode=ode.subs(X,u)
 lhs,rhs,constant=derive_particular(s,gy,fx,x0+h,y0)
 def value(a):return translated_math('$'+a+'$',h)[1:-1]
 if f[':answer-field/type'][':db/ident'].endswith('/blank'):
  choices=[(None,rhs,value(f[':answer-field/choices'][0][':answer/value']))]
 elif profile=='observed':
  # Each observed whole equation is a shape recipe in u=x-h, including unusual
  # signs, powers, and constants. Interpretation is deliberately not promoted.
  choices=[(None,None,value(a[':answer/value'])) for a in f[':answer-field/choices']]
 else:
  choices=[(lhs,rhs,tex(lhs)+'='+tex(rhs))]+[(lhs,sp.sympify(w),tex(lhs)+'='+tex(w)) for w in authored_wrong(s,u)]
 restrictions={
 'q-4019':'y != 0; connected interval containing initial x, with (x-h)^2*3+1 != 0',
 'q-8310':'x-h > 0; 1-2*log(x-h) != 0; connected interval containing h+1',
 'q-104055':'local branch 0<y<pi; |x-h|<1, initial y=pi/2',
 'q-14310':'tan branch containing h+pi/2; -pi/4 < x-h < 3*pi/4',
 'q-14312':'positive y; x real',
 'q-14313':'y != 0; connected interval containing h+1, (x-h)^3+7 != 0',
 'q-347853':'4*(x-h)+1 != 0; connected interval x>h-1/4',
 'q-355525':'-pi/6 < y < pi/6; local interval containing h+pi/8',
 'q-355528':'y>0 and (x-h)^2+2>0; x real',
 'q-355544':'-pi/8<y<pi/8; cos(7*(x-h)) !=0; -pi/14<x-h<pi/14',
 'q-355562':'y>0; x real','q-355578':'x>h; initial x=h+1',
 'q-355579':'x>h; initial x=h+1',
 'q-50220':'x>h; initial x=h+1',
 'q-50566':'y>0; x-h < -sqrt(8), connected interval containing h-3',
 'q-8308':'y>0; x real',
 'q-8309':'-pi/4<y<pi/4; cos(3*(x-h))> -1/2; local component containing h',
 'q-14309':'denominator !=0; connected interval containing h+1',
 'q-50219':'y>1, |x-h|<1; branch containing initial y=e',
 }[s]
 return problem,solution,choices,{'variable':'x','initial_x':str(x0+h),'initial_y':str(y0),'ode':str(ode),'lhs':str(lhs),'rhs':str(rhs),'primitive_y':str(gy),'primitive_x':str(fx),'integration_constant':str(constant),'domain':restrictions,'h':str(h)}


def extension_build(template,p):
 h,a,b=map(rational,(p['h'],p['a'],p['b']));u=X-h
 if a<=0 or b<=0:raise ValueError('positive extension coefficients required')
 D=r'\frac{\text{d}y}{\text{d}x}';start='We first find the general solution and then apply the given initial condition to find the particular solution.\n\nSeparating variables and integrating both sides with respect to $x,$ we get\n\n'
 def aligned(rows):return '$$\n'+r'\begin{aligned}'+' \\\\ '.join(rows)+r'\end{aligned}'+'\n$$'
 if template=='exponential_rate':
  lhs=Y;rhs=b*sp.exp(a*u);ode=a*Y;x0=h;y0=b;gy=sp.log(Y);fx=a*u
  problem=f'Find the particular solution to the differential equation ${D}={tex(ode)}$ that satisfies $y({tex(x0)})={tex(y0)}.$'
  solution=start+aligned([D+' & ='+tex(ode),r'\frac{1}{y}'+D+' & ='+tex(a),r'\int\frac{1}{y}\,\text{d}y & =\int '+tex(a)+r'\,\text{d}x',r'\ln|y| & ='+tex(a*u)+'+C'])+'\n\nApplying the exponential function to both sides, we find the general solution:\n\n'+aligned(['y & ='+tex(sp.exp(a*u+C)),'y & =K'+tex(sp.exp(a*u))])+f'\n\nWe now apply the condition $y({tex(x0)})={tex(y0)}$ to find $K:$\n\n'+aligned([tex(y0)+' & =K e^0','K & ='+tex(b)])+'\n\nThus, the particular solution is\n\n$$\n'+tex(lhs)+'='+tex(rhs)+'.\n$$'
  wrong=[b*sp.exp(-a*u),b*sp.exp(u/a),b*a*u+b,sp.exp(a*u)]
  if a==1 or b==1:raise ValueError('authored rate bank requires a>1 and b>1 to keep all operations visible')
 elif template=='reciprocal_initial':
  lhs=Y;rhs=b/(1+a*b*u);ode=-a*Y**2;x0=h;y0=b;gy=-1/Y;fx=-a*u
  problem=f'Find the particular solution to the differential equation ${D}+{tex(a*Y**2)}=0$ that satisfies $y({tex(h)})={tex(b)}.$'
  solution=start+aligned([D+' & ='+tex(ode),r'-\frac{1}{y^2}\,\text{d}y & ='+tex(a)+r'\,\text{d}x',r'-\int\frac{1}{y^2}\,\text{d}y & =\int '+tex(a)+r'\,\text{d}x',r'\frac{1}{y} & ='+tex(a*u)+'+C','y & ='+r'\frac{1}{'+tex(a*u)+'+C}'])+'\n\nwhere $C$ is an arbitrary constant.\n\n'+f'We now apply the condition $y({tex(h)})={tex(b)}$ to find $C:$\n\n'+aligned([tex(b)+r' & =\frac{1}{C}','C & ='+tex(1/b)])+'\n\nThus, the particular solution is\n\n$$\n'+tex(lhs)+'='+tex(rhs)+'.\n$$'
  wrong=[b/(1-a*b*u),b/(1+a*u),1/(a*u+b),b*(1+a*b*u)]
  if b==1:raise ValueError('reciprocal bank requires b>1')
 else:
  lhs=b*sp.sin(a*Y);rhs=a*(1-sp.cos(b*u));ode=sp.sin(b*u)/sp.cos(a*Y);x0=h;y0=0;gy=sp.sin(a*Y)/a;fx=-sp.cos(b*u)/b
  problem=f'Find the particular solution to the differential equation ${D}={tex(ode)}$ that satisfies $y({tex(h)})=0.$ Assume that $-{tex(sp.pi/(2*a))}<y<{tex(sp.pi/(2*a))}.$'
  solution=start+aligned([D+' & ='+tex(ode),tex(sp.cos(a*Y))+D+' & ='+tex(sp.sin(b*u)),r'\int '+tex(sp.cos(a*Y))+r'\,\text{d}y & =\int '+tex(sp.sin(b*u))+r'\,\text{d}x',tex(gy)+' & ='+tex(fx)+'+C',tex(sp.sin(a*Y))+' & ='+tex(a*fx)+'+C_1'])+f'\n\nwhere $C_1={tex(a)}C.$\n\nWe now apply the condition $y({tex(h)})=0$ to find $C_1:$\n\n'+aligned(['0 & ='+tex(-a/b)+'+C_1','C_1 & ='+tex(a/b)])+'\n\nSo we get the particular solution in implicit form:\n\n$$\n'+tex(lhs)+'='+tex(rhs)+'.\n$$'
  wrong=[1-sp.cos(b*u),b*(1-sp.cos(b*u)),a*(1+sp.cos(b*u)),a*sp.cos(b*u)]
  if a==1 or a==b:raise ValueError('frequency bank requires a>1 and unequal a,b')
 constant=sp.simplify(gy.subs(Y,y0)-fx.subs(X,x0));integrated=sp.simplify(fx+constant)
 rhs=sp.exp(integrated) if template=='exponential_rate' else sp.cancel(-1/integrated) if template=='reciprocal_initial' else sp.expand(a*b*integrated)
 choices=[(lhs,rhs,tex(lhs)+'='+tex(rhs))]+[(lhs,w,tex(lhs)+'='+tex(w)) for w in wrong]
 return problem,solution,choices,{'variable':'x','initial_x':str(x0),'initial_y':str(y0),'ode':str(ode),'lhs':str(lhs),'rhs':str(rhs),'primitive_y':str(gy),'primitive_x':str(fx),'integration_constant':str(constant),'domain':('y>0; x real' if template=='exponential_rate' else f'x>{h-1/(a*b)}; y>0; connected interval containing initial x={h}' if template=='reciprocal_initial' else f'-pi/{2*a}<y<pi/{2*a}; abs({a}/{b}*(1-cos({b}*(x-({h})))))<1; connected interval containing x={h}; cos({a}*y)!=0'),'h':str(h)}


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown level')
 rng=random.Random(seed);eligible=[n for n,t in TEMPLATES.items() if t['level']==level and (field_type is None or t['kind']==field_type)]
 if template is None:
  if not eligible:raise ValueError('no matching field type')
  template=rng.choice(eligible)
 if template not in TEMPLATES or template not in eligible:raise ValueError('template/level/field mismatch')
 spec=TEMPLATES[template];s=spec['source'];profile=profile or ('blank' if spec['kind']=='blank' else 'authored')
 if profile not in ('observed','authored','blank'):raise ValueError('unknown profile')
 if spec['kind']=='blank' and profile not in ('observed','blank'):raise ValueError('blank has no choice bank')
 if spec['kind']=='radio' and profile not in ('observed','authored'):raise ValueError('radio requires a complete choice bank')
 if spec['origin']!='observed' and profile!='authored':raise ValueError('coefficient extension has authored bank only')
 p=dict(parameters) if parameters is not None else {'h':rng.randint(-6,6)}
 permitted={'h'} if spec['origin']=='observed' else {'h','a','b'}
 if s=='q-168078':permitted.add('ambient')
 if not set(p)<=permitted or 'h' not in p:raise ValueError('invalid or missing parameters')
 if spec['origin']!='observed':
  if parameters is None:p.update(a=rng.randint(2,5),b=rng.randint(2,5));p['b']=p['b']+1 if p['b']==p['a'] else p['b']
  if not {'a','b'}<=set(p):raise ValueError('extension needs h,a,b')
  problem,solution,choices,m=extension_build(template,p)
 else:
  if s=='q-168078' and parameters is None:p={'h':0,'ambient':rng.randint(15,35)}
  if s=='q-168078' and rational(p['h'])!=0:raise ValueError('cooling source uses ambient, not coordinate translation')
  if s=='q-168078':p.setdefault('ambient',25)
  problem,solution,choices,m=source_build(s,p,profile)
 if profile=='authored':
  # Authored members deliberately share one identical nonconstant LHS;
  # whole-equation equivalence therefore reduces to exact RHS equality.
  for i,(lhs,rhs,_) in enumerate(choices):
   for olhs,other,_ in choices[:i]:
    if lhs!=olhs:raise ValueError('authored bank changed its fixed LHS')
    difference=sp.simplify(rhs-other)
    if difference==0 or (difference.has(sp.sin,sp.cos,sp.tan,sp.cot) and sp.trigsimp(sp.expand_trig(difference))==0):raise ValueError('whole bank contains equivalent equations')
 key=SOURCES[s][':question/answer-fields'][0][':answer-field/key']
 
 normalized={k:str(rational(v)) for k,v in sorted(p.items())}
 # Deduplicate assessed mathematics across equivalent layouts and parameter
 # spellings. The initial condition selects the same connected real branch;
 # human-readable domain prose and template names are not semantic identities.
 semantic={'variable':m['variable'],'response':'particular_solution_relation',
           'branch':'connected real solution branch containing the initial value'}
 for part in ('ode','initial_x','initial_y','lhs','rhs'):
  semantic[part]=sp.srepr(sp.simplify(sp.sympify(m[part],locals={'x':X,'y':Y,'t':T})))
 fp=hashlib.sha256(json.dumps(semantic,sort_keys=True).encode()).hexdigest()
 identity=json.dumps({'version':VERSION,'fp':fp,'problem':problem,'solution':solution,'kind':spec['kind'],'bank':sorted(c[2] for c in choices)},sort_keys=True)
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),identity));fid=str(uuid.uuid5(uuid.UUID(qid),key))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for _,_,v in choices]
 target=(sp.sympify(m['lhs'],locals={'x':X,'y':Y,'t':T}) if spec['kind']=='radio' else None,sp.sympify(m['rhs'],locals={'x':X,'y':Y,'t':T}))
 matched=[i for i,a in enumerate(answers) if DISPLAY.equivalent(DISPLAY.relation(a[':answer/value']),target)]
 if len(matched)!=1:raise ValueError('derived particular relation must match one complete displayed answer')
 correct_index=matched[0]
 recipe_names=(['correct_separate_integrate_apply_initial_value']+OPERATION_RECIPES[template if spec['origin']!='observed' else s]) if profile=='authored' else ['observed_shape_in_translated_coordinate' if spec['kind']=='radio' else 'derived_rhs_fragment']*len(answers)
 answer_recipes={a[':answer/id']:{'recipe':recipe_names[i], 'displayed_expression':a[':answer/value'],'correct':i==correct_index} for i,a in enumerate(answers)}
 correct=answers[correct_index][':answer/id'];rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':KP[':knowledge-point/title']},
 'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+spec['kind'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},
 'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':normalized,'bank_profile':profile,'answer_recipes':answer_recipes,'origin':spec['origin'],'source_ids':[s],'provenance':{k:CAPTURE[k] for k in ('database','basis','lineage')},'parameter_fingerprint':fp,'mathematics':m,'plot_rating':'none','source_bank_interpretation':'empirical coordinate-translated complete bank; distractor intent underdetermined' if profile=='observed' else 'authored operation bank' if profile=='authored' else 'blank RHS fragment','dependencies':{'sympy':sp.__version__}}}

# All levels are independent unordered families, never a progression.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 return '\n'.join([f"### Generated {q[':question/difficulty'].split('/')[-1]} — {g['template']} ({g['bank_profile']})",'',q[':question/problem'],'']+[f"- ${a[':answer/value']}$" for a in f[':answer-field/choices']]+['','Correct: $'+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])+'$','','Worked solution:',q[':question/worked-solution'],'','Author domain: '+g['mathematics']['domain']])
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['all','easy','moderate','hard'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template',choices=list(TEMPLATES));p.add_argument('--profile',choices=['observed','authored','blank']);p.add_argument('--field-type',choices=['radio','blank']);a=p.parse_args()
 if a.count<1:p.error('count must be positive')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 if a.template:levels=[TEMPLATES[a.template]['level']] if a.difficulty=='all' else levels
 rs=[generate(l,a.seed+i,a.template,a.field_type,None,a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
