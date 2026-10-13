#!/usr/bin/env python3
"""Evaluate supplied polar repeated integrals; scratch only, no database writes.

math basis 1356. Easy/moderate capture fidelity is independent of authored
operation banks. Explicit source profiles are homogeneous scalar extensions of
whole observed banks: their numerical patterns are evidence, not recovered
error intent. Defaults use complete banks of actual omitted-factor, endpoint,
and sign operations. Hard is an authored canonical e-7346 extension: a partial
sine/cosine double-angle radial bound leaves a nonzero angular endpoint term.
No Cartesian conversion, plots, region inference, or new integration method.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
from functools import lru_cache
import sympy as sp

KP_ID=17592186129198
TITLE='Evaluating Repeated Integrals Expressed in Polar Coordinates'
KP_UUID='0bc5322f-ed04-53d2-8ce6-20ec58f73a5e'
VERSION='polar-repeated-v1'
EVIDENCE=Path(__file__).with_suffix('')
RAW=json.loads((EVIDENCE/'source.json').read_text())
SOURCE={k:RAW[k] for k in ('database','basis','lineage')}
QUESTIONS={q[':question/math-academy-id']:q for q in RAW['record'][':knowledge-point/questions']}
r,t=sp.symbols('r theta',real=True)
pi=sp.pi
# Bounds and integrands are supplied. Negative upper bounds in q-38133 are
# oriented integral limits, not a reason to reject the mathematical question.
SOURCE_DATA={
 'q-38031':(0,pi/2,0,sp.sin(t),2*r*sp.cos(t)),
 'q-38127':(pi/3,pi/2,1,2,r**2*sp.sin(t)),
 'q-161049':(0,pi/2,0,sp.cos(t),3*r*sp.cos(t)),
 'q-38133':(-pi/2,pi/2,0,2*sp.cos(2*t),r),
 'q-83511':(0,pi/2,1,3,r**3*sp.cos(t)*sp.sin(t)),
 'q-83957':(pi/6,3*pi/4,2,4,r*sp.cos(t)),
 'q-83958':(0,pi/2,1-sp.cos(t),1,r),
 'q-83514':(pi/4,pi/2,sp.csc(t),2,2*r),
 'q-161048':(0,pi,0,1,5*r**4*sp.sin(t)),
 'q-83966':(5*pi/3,2*pi,1,2*sp.cos(t),r*sp.sin(t)),
}
FAMILIES={'q-38031':'sine_bound_cosine','q-38127':'constant_sine',
 'q-161049':'cosine_bound_cosine','q-38133':'cosine_double_full',
 'q-83511':'constant_product','q-83957':'constant_cosine',
 'q-83958':'offset_cosine','q-83514':'cosecant_lower',
 'q-161048':'constant_sine','q-83966':'cosine_bound_sine'}
TEMPLATES={q:{'level':('easy' if q=='q-38127' else QUESTIONS[q][':question/difficulty'][':db/ident'].split('/')[-1]),
                  'family':FAMILIES[q],'source_id':q} for q in QUESTIONS}
for family in ('sine_double_partial','cosine_double_partial'):
 TEMPLATES[family]={'level':'hard','family':family,'source_id':'e-7346'}
BANK_PROFILES={**{q+'_observed':{'template':q,'origin':'observed','interpretation':'homogeneous scaling of complete captured scalar bank; error intent unresolved'} for q in QUESTIONS},
 **{q+'_operations':{'template':q,'origin':'authored','interpretation':'complete method-derived operation bank'} for q in TEMPLATES}}

def tex(x):
 return sp.latex(sp.sympify(x)).replace(r'\theta',r'\theta').replace(r'\operatorname{csc}',r'\csc').replace(r'\operatorname{cot}',r'\cot')
def exact(x): return sp.simplify(sp.sympify(x))
@lru_cache(maxsize=4096)
def integral(f,a,b,var=t): return sp.integrate(f,(var,a,b))
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def eq(x,y): return sp.simplify(x-y)==0

def scale_tex(s,c):
 """A linear-homogeneity slot applied to complete mathematical components.

 This is a recipe for arbitrary bounded scale, including scale 1; no literal
 source-record replay branch and no alteration of substrings such as prose,
 variable labels or arbitrary occurrences of a short number.
 """
 if c==1 or not s.strip():return s
 # Preserve leading/trailing whitespace and terminal punctuation.
 prefix=s[:len(s)-len(s.lstrip())];suffix=s[len(s.rstrip()):]
 core=s.strip();trail=''
 if core.endswith('.'):
  core,trail=core[:-1],'.'
 return prefix+tex(c)+r'\left('+core+r'\right)'+trail+suffix

def scale_prompt(s,c):
 def repl(m):
  v=m.group(1)
  ending='=' if v.rstrip().endswith('=') else ''
  if ending:v=v.rstrip()[:-1]
  return '$'+scale_tex(v,c)+ending+'$'
 return re.sub(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',repl,s,flags=re.S)

def scale_solution(s,c):
 # Only display equations are assessed components. Inline prose variables stay
 # fixed. Every side of every aligned equality scales together, preserving the
 # exact source stage sequence and common instructional wording.
 def block(m):
  v=m.group(1)
  if r'\begin{aligned}' not in v:return '$$'+scale_tex(v,c)+'$$'
  opening,body=v.split(r'\begin{aligned}',1)
  body,closing=body.split(r'\end{aligned}',1)
  parts=body.split('\\\\')
  rows=[]
  for row in parts:
   if '&' not in row:raise ValueError('Unexpected aligned layout')
   left,right=row.split('&',1)
   if not right.lstrip().startswith('='):raise ValueError('Expected equality')
   whitespace=right[:len(right)-len(right.lstrip())]
   rhs=right.lstrip()[1:]
   rows.append(scale_tex(left,c)+'&'+whitespace+'='+scale_tex(rhs,c))
  return '$$'+opening+r'\begin{aligned}'+'\\\\'.join(rows)+r'\end{aligned}'+closing+'$$'
 return re.sub(r'\$\$(.*?)\$\$',block,s,flags=re.S)

def validate_parameters(name,p,profile):
 family=TEMPLATES[name]['family'];level=TEMPLATES[name]['level']
 if BANK_PROFILES[profile]['origin']=='observed':
  if set(p)!={'scale'} or type(p['scale'])!=int or not 1<=p['scale']<=5:raise ValueError('Observed profile requires scale integer 1..5')
  return
 expected=({'c','a','b','n','alpha','beta'} if family.startswith('constant_') else
           {'c','A','alpha','beta'} if family in ('sine_bound_cosine','cosine_bound_cosine','cosine_bound_sine','offset_cosine','cosecant_lower') else
           {'c','A','k'} if family=='cosine_double_full' else {'c','A','beta'})
 if set(p)!=expected:raise ValueError(f'Expected parameters: {sorted(expected)}')
 for key in ('c','A'):
  if key in p and (type(p[key])!=int or not 1<=p[key]<=4):raise ValueError(key+' must be integer 1..4')
 if family.startswith('constant_'):
  if type(p['n'])!=int or not 1<=p['n']<=4:raise ValueError('power 1..4')
  if any(type(p[k])!=int for k in ('a','b')) or not 0<=p['a']<p['b']<=4:raise ValueError('0 <= a < b <= 4')
  if exact(p['alpha']) not in (0,pi/6,pi/4,pi/3) or exact(p['beta']) not in (pi/2,2*pi/3,3*pi/4,pi):raise ValueError('familiar fixed-angle endpoints required')
  if family=='constant_product' and (exact(p['alpha']) not in (0,pi/6,pi/4) or exact(p['beta'])!=pi/2):raise ValueError('product endpoints remain inside first quadrant')
 elif family=='cosine_double_full':
  if type(p['k'])!=int or p['k'] not in (1,2,3):raise ValueError('frequency 1..3')
 elif level=='hard':
  if exact(p['beta']) not in (pi/12,pi/8,pi/6):raise ValueError('hard requires nonzero familiar sin(4 beta) endpoint, beta in pi/12,pi/8,pi/6')
 else:
  domains={'sine_bound_cosine':((0,pi/6,pi/4),(pi/3,pi/2)),
   'cosine_bound_cosine':((0,pi/6,pi/4),(pi/3,pi/2)),
   'offset_cosine':((0,pi/6,pi/4),(pi/3,pi/2)),
   'cosecant_lower':((pi/6,pi/4,pi/3),(pi/2,2*pi/3,3*pi/4)),
   'cosine_bound_sine':((5*pi/3,7*pi/4),(11*pi/6,2*pi))}
  aa,bb=domains[family]
  if exact(p['alpha']) not in aa or exact(p['beta']) not in bb or exact(p['alpha'])>=exact(p['beta']):raise ValueError('Unsupported level-specific angular interval')
  if family=='cosecant_lower' and p['A']<2:raise ValueError('cosecant upper constant must be 2..4')

def sample(name,rng,profile):
 if BANK_PROFILES[profile]['origin']=='observed':return {'scale':rng.randint(1,5)}
 f=TEMPLATES[name]['family']
 p={'c':rng.randint(1,4)}
 if f.startswith('constant_'):
  a=rng.randrange(3);b=rng.randint(a+1,4)
  return dict(p,a=a,b=b,n=rng.randint(1,4),alpha=str(rng.choice((0,pi/6,pi/4) if f=='constant_product' else (0,pi/6,pi/4,pi/3))),beta=str(pi/2 if f=='constant_product' else rng.choice((pi/2,2*pi/3,3*pi/4,pi))))
 p['A']=rng.randint(1,4)
 if f=='cosine_double_full':return dict(p,k=rng.choice((1,2,3)))
 if TEMPLATES[name]['level']=='hard':return dict(p,beta=str(rng.choice((pi/12,pi/8,pi/6))))
 aa,bb=((5*pi/3,7*pi/4),(11*pi/6,2*pi)) if f=='cosine_bound_sine' else ((pi/6,pi/4,pi/3),(pi/2,2*pi/3,3*pi/4)) if f=='cosecant_lower' else ((0,pi/6,pi/4),(pi/3,pi/2))
 if f=='cosecant_lower':p['A']=rng.randint(2,4)
 return dict(p,alpha=str(rng.choice(aa)),beta=str(rng.choice(bb)))

def object_data(name,p,profile):
 if BANK_PROFILES[profile]['origin']=='observed':
  a,b,L,U,f=SOURCE_DATA[name]
  return tuple(map(sp.sympify,(a,b,L,U,p['scale']*f)))
 family=TEMPLATES[name]['family'];c=p['c']
 if family.startswith('constant_'):
  a,b=map(exact,(p['alpha'],p['beta']));L,U=p['a'],p['b'];n=p['n']
  g={'constant_sine':sp.sin(t),'constant_cosine':sp.cos(t),'constant_product':sp.cos(t)*sp.sin(t)}[family]
  return a,b,sp.Integer(L),sp.Integer(U),c*r**n*g
 A=p['A']
 if family=='cosine_double_full':return -pi/2,pi/2,sp.Integer(0),A*sp.cos(p['k']*t),c*r
 if TEMPLATES[name]['level']=='hard':
  g=sp.sin(2*t) if family=='sine_double_partial' else sp.cos(2*t)
  return sp.Integer(0),exact(p['beta']),sp.Integer(0),A*g,c*r
 a,b=map(exact,(p['alpha'],p['beta']))
 L,U,f={
  'sine_bound_cosine':(0,A*sp.sin(t),c*r*sp.cos(t)),
  'cosine_bound_cosine':(0,A*sp.cos(t),c*r*sp.cos(t)),
  'cosine_bound_sine':(1,A*sp.cos(t),c*r*sp.sin(t)),
  'offset_cosine':(A*(1-sp.cos(t)),A,c*r),
  'cosecant_lower':(sp.csc(t),A,c*r)}[family]
 return tuple(map(sp.sympify,(a,b,L,U,f)))

@lru_cache(maxsize=4096)
def math_data(a,b,L,U,f):
 radial=sp.integrate(f,r)
 upper=radial.subs(r,U);lower=radial.subs(r,L)
 reduced=sp.expand(upper-lower)
 angular=sp.integrate(reduced,t)
 answer=sp.simplify(angular.subs(t,b)-angular.subs(t,a))
 return radial,upper,lower,reduced,angular,answer

def I(f,a,b,var): return r'\int_{'+tex(a)+'}^{'+tex(b)+'} '+(f if isinstance(f,str) else tex(f))+r'\,\mathrm d '+tex(var)
def B(f,a,b): return r'\left['+(f if isinstance(f,str) else tex(f))+r'\right]_{'+tex(a)+'}^{'+tex(b)+'}'
def align(rows):return '$$\n'+r'\begin{aligned}'+ '\n' +(' \\\\\n'.join((rows[0]+' & = '+rows[1],*['& = '+v for v in rows[2:]])))+'\n'+r'\end{aligned}'+'\n$$'
def groups(s):return r'\left('+s+r'\right)'

def authored_solution(name,p,data):
 a,b,L,U,f=data;P,Phi,Plow,h,F,z=math_data(*data)
 c=f.expand().coeff(r,1) if sp.degree(f,r)==1 else None
 prompt='Evaluate $'+I(I(f,L,U,r),a,b,t)+'.$'
 # Structural masks retain each substitution and evaluated component before
 # simplifying. The two original shared prose sentences stay fixed.
 degree=sp.degree(f,r);radial_factor=sp.expand(f).coeff(r,degree)
 powerP=r'\frac{r^{'+str(degree+1)+'}}{'+str(degree+1)+'}'
 radial_rows=[I(I(f,L,U,r),a,b,t)]
 if radial_factor!=1:
  radial_rows.append(I(tex(radial_factor)+' '+I(r**degree,L,U,r),a,b,t))
 radial_prefix='' if radial_factor==1 else tex(radial_factor)+' '
 radial_rows.append(I(radial_prefix+B(powerP,L,U),a,b,t))
 substituted=r'\frac{'+groups(tex(U))+'^{'+str(degree+1)+'}-'+groups(tex(L))+'^{'+str(degree+1)+'}}{'+str(degree+1)+'}'
 radial_rows.append(I(radial_prefix+groups(substituted),a,b,t))
 radial_rows.append(I(h,a,b,t))
 solution='First, we integrate with respect to $r,$ treating $\\theta $ as a constant:\n\n'+align(radial_rows)
 family=TEMPLATES[name]['family']
 if family.startswith('constant_'):
  K=sp.Rational(p['c'],p['n']+1)*(p['b']**(p['n']+1)-p['a']**(p['n']+1))
  F=K*({'constant_sine':-sp.cos(t),'constant_cosine':sp.sin(t),'constant_product':sp.sin(t)**2/2}[family])
 elif family in ('sine_bound_cosine','cosine_bound_cosine','cosine_bound_sine','offset_cosine','cosecant_lower'):
  C=p['c'];A=p['A']
  F={'sine_bound_cosine':C*A**2*sp.sin(t)**3/6,
     'cosine_bound_cosine':C*A**2*sp.Rational(1,2)*(sp.sin(t)-sp.sin(t)**3/3),
     'cosine_bound_sine':C*sp.Rational(1,2)*(-A**2*sp.cos(t)**3/3+sp.cos(t)),
     'offset_cosine':C*A**2*(sp.sin(t)-t/4-sp.sin(2*t)/8),
     'cosecant_lower':C*sp.Rational(1,2)*(A**2*t+sp.cot(t))}[family]
  F=sp.expand(F)
 angular_rows=[I(h,a,b,t)]
 if family in ('cosine_double_full','sine_double_partial','cosine_double_partial'):
  k=p.get('k',2);sign='-' if family.startswith('sine') else '+'
  multiplier=sp.Rational(p['c']*p['A']**2,4)
  identity=(r'\sin^2' if sign=='-' else r'\cos^2')+groups(str(k)+r'\theta')+r'=\frac{1}{2}\left(1'+sign+r'\cos'+groups(str(2*k)+r'\theta')+r'\right)'
  double_formula=r'\cos(2x)=1-2\sin^2 x.' if sign=='-' else r'\cos(2x)=2\cos^2 x-1.'
  solution+='\n\nNext, we recall the double-angle formula\n\n$$\n'+double_formula+'\n$$\n\nSubstituting $x='+str(k)+r'\theta$ and rearranging, we get'+'\n\n$$\n'+identity+'.\n$$'
  reduced=multiplier*(1+(-1 if sign=='-' else 1)*sp.cos(2*k*t))
  angular_rows.append(I(tex(multiplier)+groups('1'+sign+r'\cos'+groups(str(2*k)+r'\theta')),a,b,t))
  # Show primitive inside coefficient, then substitute both components.
  inner=t+(-1 if sign=='-' else 1)*sp.sin(2*k*t)/(2*k)
  angular_rows.append(tex(multiplier)+B(tex(inner),a,b))
  def substitution(x):return tex(x)+sign+r'\frac{1}{'+str(2*k)+'}'+r'\sin'+groups(tex(2*k*x))
  angular_rows.append(tex(multiplier)+groups(groups(substitution(b))+'-'+groups(substitution(a))))
  def evaluated(x):return tex(x)+sign+tex(sp.Rational(1,2*k))+' '+groups(tex(sp.sin(2*k*x)))
  angular_rows.append(tex(multiplier)+groups(groups(evaluated(b))+'-'+groups(evaluated(a))))
  angular_rows.append(tex(multiplier)+groups(groups(tex(b-a))+sign+r'\frac{1}{'+str(2*k)+'}'+groups(tex(sp.sin(2*k*b)-sp.sin(2*k*a)))))
  angular_rows.append(tex(z))
  solution+='\n\nFinally, we can finish our integral by integrating with respect to $\\theta,$ as follows:\n\n'+align(angular_rows)
  return prompt,solution
 # Algebraic identity/reduction step, before the angular primitive.
 if family=='cosine_bound_cosine':
  K=sp.Rational(p['c']*p['A']**2,2)
  angular_rows.append(I(tex(K)+r'\cos\theta\left(1-\sin^2\theta\right)',a,b,t))
 elif family=='offset_cosine':
  K=sp.Rational(p['c']*p['A']**2,2)
  angular_rows.append(I(tex(K)+r'\left(2\cos\theta-\frac{1+\cos(2\theta)}{2}\right)',a,b,t))
 angular_rows.append(B(F,a,b))
 # Keep term-by-term endpoint substitution and evaluation; never print the
 # already-collected expression twice as purported intermediate arithmetic.
 terms=sp.Add.make_args(F)
 def substituted(x):return '+'.join(groups(tex(v).replace(r'\theta',groups(tex(x)))) for v in terms)
 def evaluated(x):return '+'.join(groups(tex(v.subs(t,x))) for v in terms)
 angular_rows.append(groups(substituted(b))+'-'+groups(substituted(a)))
 angular_rows.append(groups(evaluated(b))+'-'+groups(evaluated(a)))
 angular_rows.append(tex(z))
 solution+='\n\nNext, we integrate with respect to $\\theta :$ \n\n'+align(angular_rows)
 return prompt,solution

def observed_solution(name,c,data):
 q=QUESTIONS[name]
 prompt=scale_prompt(q[':question/problem'],c)
 if ':question/worked-solution' in q:return prompt,scale_solution(q[':question/worked-solution'],c)
 # Missing q-38127 solution is explicitly authored, never a source-match claim.
 p={'c':c,'a':1,'b':2,'n':2,'alpha':'pi/3','beta':'pi/2'}
 _,solution=authored_solution(name,p,data)
 return prompt,solution

# EASY — supplied constant radial bounds with sine/cosine or their product;
# cosine squared over a full interval. No region conversion or interpretation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — supplied trigonometric radial endpoints yield powers/products,
# subtraction of a squared offset, or a cosecant-squared angular primitive.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored e-7346 extension: squared double-angle bound and a partial
# familiar-angle interval with nonzero sine endpoint. Same method in both
# sine/cosine families; c,A<=4 and fixed double-angle argument 2 theta.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def authored_bank(data):
 a,b,L,U,f=data;P,hi,lo,h,F,z=math_data(*data)
 # One complete five-choice bank. Missing radial denominator, extra radial
 # factor (cosecant family: omit lower radial endpoint to avoid a new log
 # integration method), reversed orientation, and incorrect upper endpoint
 # weighting are actual operations on the supplied integral.
 # No pool replacement: any collision rejects the whole candidate.
 n=sp.degree(f,r)
 wrong1=(n+1)*z
 wrong2=integral(hi,a,b) if L.has(sp.csc(t)) else integral(integral(r*f,L,U,r),a,b)
 wrong3=-z
 endpoint=exact(F.subs(t,b))
 wrong4=exact(F.subs(t,b)/2-F.subs(t,a))
 # Halve the upper primitive endpoint only: a fixed endpoint-evaluation
 # operation. Collision with any required option rejects the entire instance.
 return [z,exact(wrong1),exact(wrong2),exact(wrong3),exact(wrong4)]

def source_values(name):
 # Captured whole-bank scalar patterns, not inferred author mistake formulas.
 # parse_scalar is shared by evidence tooling but correctness is independently
 # checked from printed integrals in validate.py.
 values={
 'q-38031':[sp.Rational(2,3),1,2,2*pi,sp.Rational(1,3)],
 'q-38127':[-sp.Rational(2,3),sp.Rational(7,6),pi/5,-pi,4],
 'q-161049':[2,sp.Rational(1,2),1,sp.Rational(3,2),3],
 'q-38133':[pi/4,pi,sp.sqrt(3)/2,2*pi,pi+4],
 'q-83511':[5,30,10,20,40],
 'q-83957':[6*(sp.sqrt(2)-1),3,3*sp.sqrt(2),sp.Rational(3,2)*(sp.sqrt(2)-1),3*(sp.sqrt(2)-1)],
 'q-83958':[(4-pi)/4,8-pi,(2-pi)/2,(8-pi)/8,1-pi],
 'q-83514':[pi-1,pi+1,pi-2,pi+2,pi],
 'q-161048':[0,1,5,2,4],
 'q-83966':[-sp.Rational(1,12),-sp.Rational(1,3),sp.Rational(1,12),sp.Rational(1,6),-sp.Rational(1,6)]}
 return list(map(sp.sympify,values[name]))

class SampleRejected(ValueError):pass

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only the observed radio layout is supported')
 if profile is not None:
  if profile not in BANK_PROFILES:raise ValueError('Unknown bank profile')
  owner=BANK_PROFILES[profile]['template']
  if template is not None and template!=owner:raise ValueError('Profile belongs to another template')
  template=owner
 eligible=[n for n,s in TEMPLATES.items() if s['level']==level]
 if template is not None and template not in eligible:raise ValueError('Template outside requested difficulty')
 rng=random.Random(seed);name=template or rng.choice(eligible)
 profile=profile or name+'_operations'
 for attempt in range(256):
  p=dict(parameters) if parameters is not None else sample(name,rng,profile)
  validate_parameters(name,p,profile)
  data=object_data(name,p,profile);answer=math_data(*data)[-1]
  observed=BANK_PROFILES[profile]['origin']=='observed'
  if observed:
   values=[p['scale']*v for v in source_values(name)]
   strings=[scale_tex(a[':answer/value'],p['scale']) for a in QUESTIONS[name][':question/answer-fields'][0][':answer-field/choices']]
   prompt,solution=observed_solution(name,p['scale'],data)
  else:
   values=authored_bank(data);strings=list(map(tex,values));prompt,solution=authored_solution(name,p,data)
  bad=any(not v.is_finite for v in values) or any(eq(x,y) for i,x in enumerate(values) for y in values[i+1:])
  keys=[i for i,v in enumerate(values) if eq(v,answer)]
  if bad or len(keys)!=1:
   if parameters is not None:raise SampleRejected('Whole bank invalid, equivalent, or ambiguous')
   continue
  # Profiles/parameter aliases cannot create identity differences without actual
  # displayed differences. Mathematical task excludes answer-bank/profile.
  fingerprint=digest([sp.srepr(x) for x in data])
  content=digest([VERSION,prompt,solution,sorted(strings),level])
  qid=uid(content);fid=uid(content+'selection')
  answers=[{':answer/id':uid(content+'selection'+s),':answer/type':':answer.type/math',':answer/value':s} for s in strings]
  correct=answers[keys[0]][':answer/id'];rng.shuffle(answers)
  q={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,
     ':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':BANK_PROFILES[profile]['origin'],'source':SOURCE,'source_ids':[TEMPLATES[name]['source_id']],'mathematical_fingerprint':fingerprint,'content_hash':content,'difficulty_origin':'authored' if level=='hard' or name=='q-38127' else 'observed','domains':'Supplied oriented repeated integral; finite trigonometric expressions on the given interval. No physical-region claim.','plot_rating':'none','sympy':sp.__version__}}
 raise SampleRejected('Bounded sampler exhausted complete eligible banks')

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0];g=rec['generation']
 text='### '+g['template']+' — '+q[':question/difficulty'].split('/')[-1]+'\n\n'+q[':question/problem']+'\n\n'
 for letter,a in zip('ABCDE',f[':answer-field/choices']):text+='- '+letter+'. $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '')+'\n'
 return text+'\n'+q[':question/worked-solution']+'\n'

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(BANK_PROFILES));ap.add_argument('--field-type',choices=['radio'])
 args=ap.parse_args()
 if args.count<1 or ((args.template or args.profile) and args.difficulty=='all'):ap.error('Use positive count and specific difficulty with template/profile')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 recs=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(recs,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,recs)))
if __name__=='__main__':main()
