#!/usr/bin/env python3
"""Scalar line integrals along explicit graphs; basis 1356 scratch review only.

All source prose/stages use extracted complete-component masks in templates.json.
Observed banks are numerical expression-pattern replay profiles with unresolved
wrong-option intent; authored normal banks use explicit assessed operations.
No lookup of source answers and no literal source-return branch exists.
API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None), with individually documented easy/moderate/hard entrypoints.
Run .venv/bin/python generate/scratch/17592186152158/validate.py.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
D=Path(__file__).with_suffix('')
MASKS=json.loads((D/'templates.json').read_text())
KP_ID=17592186152158
KP_UUID='2d261248-985f-505e-85cb-4597828f95b2'
TITLE='Computing a Line Integral of a Scalar Function Along a Curve Given in Explicit Cartesian Form'
VERSION='scalar-graph-integral-1'
X,Y=sp.symbols('x y',real=True)
T=sp.symbols('t',positive=True)
U=sp.symbols('u',positive=True)
TEMPLATES={'easy_linear':'easy',**{k:v['level'] for k,v in MASKS.items()}}
BANK_PROFILES={p+k for k in TEMPLATES for p in ('authored_','observed_') if p!='observed_' or k!='easy_linear'}
def tex(e):
 return sp.latex(sp.sympify(e)).replace(r'\log',r'\ln')
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s): return str(uuid.uuid5(uuid.UUID(KP_UUID),s))
def block(s): return '$$\n'+s+'\n$$'
def aligned(rows): return block(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')
def math_data(name,p):
 b=sp.Rational(p.get('b',1));n=p.get('n',1)
 if name=='easy_linear':
  m,c=p['m'],p['c'];g=m*X;f=c*X
 elif name=='line_product':g=2*X+1;f=X*(Y-1)
 elif name=='line_sum':g=X;f=X+Y
 elif name=='line_polynomial':g=3*X+2;f=X**2+Y
 elif name=='line_constant':g=X-4;f=1/(X-Y)
 elif name=='circle':g=sp.sqrt(4-X**2);f=2*X*Y
 elif name=='exponential':g=sp.exp(X);f=2*Y**2;b=sp.log(n)
 elif name=='parabola':g=X**2/4;f=Y/X;b=2*sp.sqrt(n*n-1)
 elif name=='reciprocal':g=1/X;f=4*Y**2/X**3;b=sp.root(n,4)
 else:raise ValueError(name)
 a=sp.Integer(1) if name=='reciprocal' else sp.Integer(0)
 ft=sp.simplify(f.subs({X:T,Y:g.subs(X,T)}, simultaneous=True))
 gt=g.subs(X,T);der=sp.diff(gt,T);speed=sp.sqrt(1+der**2)
 if name=='circle':speed=2/sp.sqrt(4-T*T)
 it=sp.simplify(ft*speed)
 if name=='exponential':F=sp.Rational(2,3)*(1+sp.exp(2*T))**sp.Rational(3,2)
 elif name=='parabola':F=(1+T*T/4)**sp.Rational(3,2)/3
 elif name=='reciprocal':F=-sp.Rational(2,3)*(1+T**-4)**sp.Rational(3,2)
 else:F=sp.integrate(it,T)
 result=sp.simplify(F.subs(T,b)-F.subs(T,a))
 return dict(g=g,f=f,a=a,b=b,gt=gt,ft=ft,der=der,speed=speed,it=it,F=F,result=result)

def check_parameters(name,p,profile):
 key='n' if name in ('exponential','parabola','reciprocal') else 'b'
 required={key,'m','c'} if name=='easy_linear' else {key}
 if set(p)!=required:raise ValueError('Parameters must be exactly '+str(sorted(required)))
 if key=='n':
  if type(p['n']) is not int or not 2<=p['n']<=12:raise ValueError('n must be an integer in 2..12')
 else:
  if not isinstance(p['b'],(int,str,sp.Rational)) or isinstance(p['b'],bool):raise ValueError('b must be exact rational, not float')
  try:b=sp.Rational(p['b'])
  except Exception:raise ValueError('b must be exact rational')
  if b<=0 or b>8:raise ValueError('b must lie in (0,8]')
  if name=='circle' and (b>2 or b.q>4):raise ValueError('circle b must be <=2 with denominator <=4')
  if name!='circle' and name!='easy_linear' and b.q>2:raise ValueError('linear b denominator <=2')
  if name=='easy_linear' and (b.q!=1 or b<2):raise ValueError('easy b must be integer 2..8')
  if name=='line_sum' and b<3 and profile.startswith('authored_'):raise ValueError('authored sum b >=3')
 if name=='easy_linear' and any(type(p[k]) is not int or not 1<=p[k]<=6 for k in ('m','c')):raise ValueError('easy m,c in 1..6')

def sample(name,rng):
 if name in ('exponential','parabola','reciprocal'):return {'n':rng.randint(2,12)}
 if name=='easy_linear':return {'m':rng.randint(1,6),'c':rng.randint(1,6),'b':rng.randint(2,8)}
 if name=='circle':return {'b':rng.choice([str(sp.Rational(i,j)) for j in (2,3,4) for i in range(1,2*j)])}
 return {'b':str(sp.Rational(rng.randint(6,16) if name=='line_sum' else rng.randint(1,16),2))}

def observed_values(name,p,d):
 """Complete source expression patterns; intent unidentifiable from one bank.

 These are explicit formulas in changed endpoints, NOT an inferred error model.
 Replay profiles preserve original complete banks; normal output uses authored.
 """
 b=d['b'];n=p.get('n',1);v=d['result']
 if name=='line_product':return [v,2*b**3/3,2*b**3*sp.sqrt(5),b**3*sp.sqrt(5)/3,5*b**3*sp.sqrt(2)/3]
 if name=='line_sum':return [v,sp.sqrt(2)/b,b*sp.sqrt(2),b*b,sp.sqrt(2)/b**2]
 if name=='line_polynomial':return [b*sp.sqrt(5)/6,3*b*sp.sqrt(5),13*b*sp.sqrt(10),b*sp.sqrt(10)/3,v]
 if name=='line_constant':return [b/4,v,b,3*b/4,b*sp.sqrt(2)/2]
 if name=='circle':return [3*b*b/32,b*b*sp.sqrt(2),b*b*sp.sqrt(2)/4,b*b/16,v]
 if name=='exponential':return [v/2,3*v/2,-2*sp.sqrt(2),(n*n+1)**sp.Rational(3,2)/2,v]
 if name=='parabola':return [v,sp.sqrt(n)/3,sp.Rational(n*n,3),n*sp.sqrt(n)/3,n**3/sp.Integer(3)]
 if name=='reciprocal':return [12*v,16*2**sp.Rational(3,2),v,24*v,16*(1+1/sp.Integer(n))**sp.Rational(3,2)]
 raise ValueError(name)

def authored_values(name,d):
 """Select this whole operation bank first and reject on any collision."""
 v=d['result'];a,b=d['a'],d['b'];ft=d['ft'];speed=d['speed']
 squared=sp.simplify(sp.integrate(ft*speed**2,(T,a,b)))
 omit=sp.simplify(sp.integrate(ft,(T,a,b)))
 if name=='line_constant':
  return [v,omit,2*omit,omit/sp.sqrt(2),sp.sqrt(17)*omit],['correct','omit_ds','square_speed','invert_speed','use_intercept_as_slope']
 if name in ('easy_linear','line_sum','line_polynomial','line_product'):
  derivative=sp.integrate(sp.diff(ft,T)*speed,(T,a,b))
  return [v,omit,squared,derivative,-v],['correct','omit_ds','square_metric_factor','differentiate_scalar_integrand','reverse_bounds']
 # The same graph density, with a squared metric, reversed limits, or omitted ds.
 return [v,omit,squared,-v,sp.simplify(d['ft'].subs(T,b)*(b-a))],['correct','omit_ds','square_metric_factor','reverse_bounds','omit_ds_and_endpoint_rectangle']

def render_source(name,p,d):
 m=MASKS[name];sol=m['solution'];b=d['b'];n=p.get('n',1)
 slots={'upper':tex(b),'answer':tex(d['result'])}
 if name=='line_sum':slots['endpoint']=r'\sqrt{2}('+tex(b)+'^{2}-0^{2})'
 if name=='circle':slots['endpoint']='2('+tex(b)+'^{2}-0^{2})'
 if name=='line_polynomial':slots['endpoint']=r'\sqrt{10}('+tex(b**3/3)+'+'+tex(3*b*b/2)+'+'+tex(2*b)+')'
 if name=='line_constant':slots['endpoint']=r'\frac{\sqrt{2}}{4}('+tex(b)+'-0)'
 if name=='exponential':slots.update(uupper=tex(n*n+1),powerupper='{'+tex(n*n+1)+'}^{3/2}',expanded=tex((n*n+1)**sp.Rational(3,2))+'-2\\sqrt{2}')
 if name=='parabola':slots.update(uupper=str(n*n),powerupper='{'+str(n*n)+'}^{3/2}',expanded=str(n**3)+'-1')
 if name=='reciprocal':slots.update(uupper=tex(1+1/sp.Integer(n)),powerupper=r'\sqrt{('+tex(1+1/sp.Integer(n))+')^{3}}',expanded=tex((1+1/sp.Integer(n))**sp.Rational(3,2))+'-2\\sqrt{2}')
 prompt=m['problem']
 if sol is None:return generic_render(d)
 for k,v in slots.items():prompt=prompt.replace('@'+k+'@',v);sol=sol.replace('@'+k+'@',v)
 if '@' in prompt+sol:raise ValueError('Unfilled template slot')
 return prompt,sol

def generic_render(d):
 f,g,a,b=[tex(d[k]) for k in ('f','g','a','b')]
 prompt=f'Evaluate the integral of the function $f(x,y)={f}$ along the line $y={g},$ $\\,{a}\\le x\\le {b}.$'
 sol='Notice that the given curve is of the form $y=y(x).$ Therefore, by setting $x=t,$ we have $y=y(t)='+tex(d['gt'])+'.$ This gives the following parametrization of the curve:\n\n'
 sol+=block(r'\mathbf r(t)=\langle t,'+tex(d['gt'])+r'\rangle,\qquad '+a+r'\le t\le '+b)
 sol+='\n\nComputing $\\mathbf r^{\\prime}(t)$ and $\\|\\mathbf r^{\\prime}(t)\\|,$ we get the following:\n\n'+aligned([
  r'\mathbf r^{\prime}(t)&=\frac{\mathrm dx}{\mathrm dt}\mathbf i+\frac{\mathrm dy}{\mathrm dt}\mathbf j',
  r'&=\frac{\mathrm d}{\mathrm dt}(t)\mathbf i+\frac{\mathrm d}{\mathrm dt}('+tex(d['gt'])+r')\mathbf j',
  r'&=\mathbf i+('+tex(d['der'])+r')\mathbf j',
  r'\|\mathbf r^{\prime}(t)\|&=\sqrt{(\frac{\mathrm dx}{\mathrm dt})^2+(\frac{\mathrm dy}{\mathrm dt})^2}',
  r'&=\sqrt{1^2+('+tex(d['der'])+')^2}',
  r'&='+tex(d['speed'])])
 sol+='\n\nNow, since $f(x,y)='+f+'$, we obtain\n\n'+aligned(['f(r(t))&='+tex(d['ft'])])
 power=3 if d['f'].has(Y) else 2
 coefficient=sp.simplify(d['F']/T**power)
 endpoint=tex(coefficient)+r'\left(('+b+')^{'+str(power)+'}-('+a+')^{'+str(power)+r'}\right)'
 evaluated=tex(coefficient)+r'\left('+tex(d['b']**power)+'-'+tex(d['a']**power)+r'\right)'
 sol+='\n\nTherefore, we can write the integral as\n\n'+aligned([
  r'\int_C f(x,y)\,\mathrm ds&=\int_{'+a+'}^{'+b+r'}f(r(t))\|\mathbf r^{\prime}(t)\|\,\mathrm dt',
  r'&=\int_{'+a+'}^{'+b+'}('+tex(d['ft'])+')('+tex(d['speed'])+r')\,\mathrm dt',
  r'&=\left['+tex(d['F'])+r'\right]_{'+a+'}^{'+b+'}',
  r'&='+endpoint,
  r'&='+evaluated,
  r'&='+tex(d['result'])+'.'])
 return prompt,sol

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'radio'):raise ValueError('Only observed radio fields supported')
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if profile:
  if profile not in BANK_PROFILES:raise ValueError('Unknown complete profile')
  implied=profile.split('_',1)[1]
  if template and template!=implied:raise ValueError('Profile/template mismatch')
  template=implied
 rng=random.Random(seed)
 names=[n for n,l in TEMPLATES.items() if l==level]
 name=template or rng.choice(names)
 if name not in names:raise ValueError('Wrong template level')
 profile=profile or 'authored_'+name
 for attempt in range(100):
  p=dict(parameters) if parameters is not None else sample(name,rng)
  check_parameters(name,p,profile);d=math_data(name,p)
  if profile.startswith('observed_'):vals=observed_values(name,p,d);recipes=['source_expression_pattern_'+str(i) for i in range(5)]
  else:vals,recipes=authored_values(name,d)
  vals=[sp.simplify(v) for v in vals]
  eligible=all(v.is_finite is not False and v.is_real is not False for v in vals) and all(sp.simplify(v-w)!=0 for i,v in enumerate(vals) for w in vals[i+1:])
  if not eligible:
   if parameters is not None:raise ValueError('Complete bank rejected: invalid/equivalent options')
   continue
  corrects=[i for i,v in enumerate(vals) if sp.simplify(v-d['result'])==0]
  if len(corrects)!=1:raise ValueError('Incorrect complete bank')
  prompt,solution=generic_render(d) if name=='easy_linear' else render_source(name,p,d)
  bank=[tex(v) for v in vals]
  task=digest([sp.srepr(d['g']),sp.srepr(d['f']),sp.srepr(d['a']),sp.srepr(d['b'])])
  content=digest([VERSION,prompt,solution,sorted(bank)])
  qid=uid(content);fid=uid(content+':selection')
  answers=[{':answer/id':uid(fid+':'+value),':answer/type':':answer.type/math',':answer/value':value} for value in bank]
  correct_id=answers[corrects[0]][':answer/id'];rng.shuffle(answers)
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':'observed_expression_pattern_unresolved_intent' if profile.startswith('observed_') else 'authored_operations','recipes':recipes,'parameter_fingerprint':task,'content_fingerprint':content,'source':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'source_ids':[MASKS[name]['source_id']] if name in MASKS else [],'authored_level':name in ('easy_linear','line_product'),'plot_rating':'none','plot_assets':{},'domain':'graph y=g(x); scalar ds; endpoint removable singularities interpreted by continuous extension/improper limit where needed','sympy_version':sp.__version__}}
 raise ValueError('Bounded whole-bank sampling exhausted')

# EASY: authored missing level, canonical constant-speed graph method.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Linear f=cx and y=mx, one power antiderivative, positive small coefficients."""
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed linear graphs, substitution then polynomial/constant integration.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Four unordered observed linear templates; line_product level is authored."""
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: observed nonlinear graphs and their cancellation/u-substitution evaluations.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Exponential, circular, parabola and reciprocal graph instances; no new branch."""
 return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return '\n\n'.join([q[':question/problem'],*['- $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']],'Worked solution:',q[':question/worked-solution']])
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['all','easy','moderate','hard'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=sorted(BANK_PROFILES));a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 rs=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
if __name__=='__main__':main()
