#!/usr/bin/env python3
"""Product-rule tangent slopes. Local review records only; math basis 1356.

Observed profiles preserve complete banks as parameterized algebraic patterns;
opaque scalar-bank interpretations are explicitly unresolved, never defaults.
Source notation is normalized, with original prose and ordered stage counts.
Easy/hard are authored level claims. No tangent equations/quotient branches.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
X=s.Symbol('x',real=True)
HERE=Path(__file__).with_suffix('')
RAW=json.loads((HERE/'source.json').read_text())
KP=RAW['record']; QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
VERSION='product-slope-1'
ID=17592186096619
TEMPLATES={
 'q-48391':('easy','exp_linear','radio',dict(a=2,b=1,t='0')),
 'q-48901':('moderate','power_sin','radio',dict(a=8,n=3,t='pi/2')),
 'q-31226':('moderate','power_tan','blank',dict(a=3,n=2,t='pi')),
 'q-319825':('moderate','shift_log','blank',dict(a=1,b=-1,k=2,d=1,t='0')),
 'q-167326':('moderate','named_exp_sin','blank',dict(a='1/2',b=-4,t='pi')),
 'q-167780':('moderate','named_exp_sin','blank',dict(a='1/2',b=-4,t='pi')),
 'q-319806':('moderate','linear_cos','blank',dict(a=1,b=2,t='pi/2')),
 'q-319829':('moderate','shift_log','blank',dict(a=1,b=-1,k=4,d=-3,t='1')),
 'q-319842':('moderate','poly_exp','blank',dict(a=1,b=-4,c=7,n=2,t='0')),
 'q-48515':('moderate','linear_log','radio',dict(a=3,b=-2,t='1')),
 'q-48516':('moderate','exp_sin','radio',dict(a=1,t='pi')),
 'q-48517':('moderate','power_exp','radio',dict(a=1,b=-1,n=3,t='2')),
 'q-48993':('moderate','linear_log','radio',dict(a=1,b=0,t='E')),
 'easy_exp_linear':('easy','exp_linear','blank',None),
 'easy_linear_log':('easy','linear_log','blank',None),
 'hard_poly_trig':('hard','poly_trig','blank',None),
 'hard_poly_log':('hard','poly_log','blank',None),
}

def expr(v):
 return s.sympify(v,locals={'pi':s.pi,'E':s.E,'x':X,'sin':s.sin,'cos':s.cos,'tan':s.tan,'exp':s.exp,'log':s.log})
def tex(v):
 v=s.sympify(v).replace(s.sinh,lambda z:(s.exp(z)-s.exp(-z))/2).replace(s.cosh,lambda z:(s.exp(z)+s.exp(-z))/2)
 return s.latex(v,fold_short_frac=False).replace(r'\log',r'\ln')
def group(v):return '('+tex(v)+')'
def mul(a,b):return group(a)+r'\cdot '+group(b)
def add(a,b):return mul(*a)+'+'+mul(*b)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'product-slope:'+v))
def math_parts(p,family):
 a=p.get('a',s.Integer(1));b=p.get('b',s.Integer(0));n=p.get('n',s.Integer(2))
 if family=='exp_linear':u=a*s.exp(X);v=X+b
 elif family=='power_sin':u=a*X**n;v=s.sin(X)
 elif family=='power_tan':u=a*X**n;v=s.tan(X)
 elif family=='shift_log':u=a*X+b;v=s.log(p['k']*X+p['d'])
 elif family=='named_exp_sin':u=a*s.exp(X);v=b*s.sin(X)
 elif family=='linear_cos':u=a*X+b;v=s.cos(X)
 elif family=='linear_log':u=a*X+b;v=s.log(X)
 elif family=='exp_sin':u=a*s.exp(X);v=s.sin(X)
 elif family=='poly_exp':u=a*X**n+b*X+p['c'];v=s.exp(X)
 elif family=='power_exp':u=a*X**n+b;v=s.exp(X)
 elif family=='poly_trig':u=a*X**2+b*X+p['c'];v={'sin':s.sin,'cos':s.cos}[p['trig']](X)
 elif family=='poly_log':u=a*X**2+b*X+p['c'];v=s.log(X)
 else:raise ValueError('Unknown family')
 return u,v

def normalize_parameters(p):
 return {k:(v if k=='trig' else expr(v)) for k,v in p.items()}
def guard(p,family,level,observed):
 expected=set(TEMPLATES[observed][3]) if observed else {'exp_linear':{'a','b','t'},'linear_log':{'a','b','t'},'poly_trig':{'a','b','c','t','trig'},'poly_log':{'a','b','c','t'}}[family]
 if set(p)!=expected:raise ValueError('Parameter keys must be '+str(sorted(expected)))
 for k,v in p.items():
  if k not in ('t','trig') and (v.is_real is not True or v.is_finite is not True):raise ValueError('Finite real coefficients required')
  if k not in ('t','trig','a') and v.is_integer is not True:raise ValueError('Integer coefficients/exponents required')
 if family!='named_exp_sin' and p['a'].is_integer is not True:raise ValueError('Integer leading coefficient required')
 if p['a']==0 or abs(p['a'])>9:raise ValueError('Nonzero a with |a| <=9')
 if any(abs(p[k])>9 for k in ('b','c') if k in p):raise ValueError('Coefficient magnitude <=9')
 if family=='named_exp_sin' and p['b']==0:raise ValueError('Nonzero sine scale')
 if 'n' in p and p['n'] not in (2,3):raise ValueError('Degree 2 or 3')
 t=p['t']
 if family in ('power_sin','power_tan','named_exp_sin','linear_cos','exp_sin','poly_trig'):
  allowed=(s.pi/4,3*s.pi/4,5*s.pi/4,7*s.pi/4) if level=='hard' else (0,s.pi/2,s.pi,3*s.pi/2,2*s.pi)
  if family=='power_tan':allowed=(s.pi,2*s.pi,-s.pi,s.pi/4,3*s.pi/4)
  if t not in allowed:raise ValueError('Familiar trigonometric angle required')
 elif family in ('linear_log','poly_log'):
  if t not in (1,s.E,s.E**2):raise ValueError('Positive familiar logarithm point')
 elif t not in (-2,-1,0,1,2):raise ValueError('Small integer point required')
 if family=='shift_log':
  if p['k'] not in (1,2,3,4,5) or p['k']*t+p['d']!=1:raise ValueError('Positive unit log argument at point; small positive k')
 if level=='easy':
  if family=='linear_log' and (p['b']!=0 or t!=s.E):raise ValueError('Easy log uses a*x ln x at e')
  if family=='exp_linear' and (t!=0 or p['b'] not in (1,2,3,4)):raise ValueError('Easy exponential uses point zero and positive small shift')
 if level=='hard':
  if any(p[k]==0 or abs(p[k])>5 for k in ('a','b','c')):raise ValueError('Hard: nonzero coefficients |a,b,c|<=5')
  if family=='poly_log' and t not in (s.E,s.E**2):raise ValueError('Hard log has two nontrivial product contributions')
 u,v=math_parts(p,family)
 if any(z.has(s.zoo,s.nan,s.oo,-s.oo) for z in (u.subs(X,t),v.subs(X,t),s.diff(u,X).subs(X,t),s.diff(v,X).subs(X,t))):raise ValueError('Undefined function or slope at point')

def sample(r,family,level,template):
 a=r.choice([-4,-3,-2,-1,1,2,3,4]);t=r.choice([0,1,2]);b=r.choice([-3,-2,-1,1,2,3])
 if family=='exp_linear':return dict(a=a,b=r.randint(1,4),t=0)
 if family=='linear_log':return dict(a=a,b=0 if level=='easy' else b,t='E' if level=='easy' else r.choice(['1','E','E**2']))
 if family=='power_sin':return dict(a=a,n=3,t=r.choice(['pi/2','3*pi/2']))
 if family=='power_tan':return dict(a=a,n=2,t=r.choice(['pi','2*pi','pi/4']))
 if family=='shift_log':k=r.randint(1,5);return dict(a=1,b=b,k=k,d=1-k*t,t=t)
 if family=='named_exp_sin':return dict(a='1/2',b=2*b,t=r.choice(['pi','pi/2','3*pi/2']))
 if family=='linear_cos':return dict(a=1,b=b,t=r.choice(['pi/2','3*pi/2','pi']))
 if family=='exp_sin':return dict(a=a,t=r.choice(['pi','pi/2','3*pi/2']))
 if family=='power_exp':return dict(a=a,b=b,n=3,t=r.choice([1,2]))
 if family=='poly_exp':return dict(a=1,b=b,c=r.randint(1,8),n=2,t=t)
 if family in ('poly_trig','poly_log'):
  p=dict(a=a,b=b,c=r.choice([-4,-3,-2,-1,1,2,3,4]),t=r.choice(['pi/4','3*pi/4','5*pi/4','7*pi/4']) if family=='poly_trig' else r.choice(['E','E**2']))
  if family=='poly_trig':p['trig']=r.choice(['sin','cos'])
  return p
 raise ValueError(family)

# Source-specific complete banks: each is selected whole, never pooled.
# Opaque numerical banks are algebraic replay patterns, NOT recovered error intent.
def observed_bank(template,p,slope,u,v):
 a=p['a'];b=p.get('b',0);t=p['t'];n=p.get('n',2)
 if template=='q-48391':return [a,2*a,s.sqrt(abs(a))*s.E,0,a*s.E]
 if template=='q-48901':return [3*a*s.pi**2/8,-6*a*s.pi**2/8,-3*a*s.pi**2/8,0,6*a*s.pi**2/8]
 if template=='q-48515':return [s.log(a),a+b,a+b-s.log(-b),a-b+2*s.log(a-b),-2*(a+b+1)]
 if template=='q-48516':return [0,-slope,slope,-t*slope,t*slope]
 if template=='q-48517':return [n*s.E+(t**n+b-2),s.exp(t)+t,s.exp(t)+b,slope,2*t*s.E]
 if template=='q-48993':return [slope,(u*v).subs(X,t),-(u*v).subs(X,t),-slope,0]
 raise ValueError('No observed radio bank')
def authored_bank(p,slope,u,v,family):
 t=p['t'];du=s.diff(u,X);dv=s.diff(v,X)
 if family=='power_sin':return [slope,-slope,(u*v).subs(X,t),(p['n']*u*v).subs(X,t),(p['a']*X**(p['n']-1)*v).subs(X,t)]
 return [slope,-slope,(u*v).subs(X,t),(du+dv).subs(X,t),(du-dv).subs(X,t)]

def source_problem(template,u,v,t,raw=False):
 """Mask complete math spans before insertion; never substitute short tokens."""
 original=QUESTIONS[template][':question/problem']
 def replace(m):
  body=m.group(1)
  if body.startswith('y'):
   return '$'+('y=f(x)\\cdot h(x)' if template.startswith('q-167') else 'y='+mul(u,v))+(',' if body.endswith(',') else '')+'$'
  if body.startswith('x'):
   return '$x='+tex(t)+('.' if body.endswith('.') else '')+'$'
  return m.group(0)
 prompt=re.sub(r'\$([^$]*)\$',replace,original)
 if template.startswith('q-167') and not raw:
  prompt='Given $f(x)='+tex(u)+'$ and $h(x)='+tex(v)+'$, '+prompt[0].lower()+prompt[1:]
 if not QUESTIONS[template].get(':question/answer-fields'):prompt+='\n\nSlope $=$ {{field-1}}'
 return prompt

def block(rows,lhs):return '$$\n\\begin{aligned}'+lhs+' &='+r' \\ &='.join(rows)+r'\end{aligned}'+'\n$$'
def source_derivative(family,p,u,v,du,dv):
 """Source-family reduction masks keep rational sums and factored exponentials."""
 a=p['a']
 if family=='shift_log':return r'\frac{'+tex(p['k'])+group(u)+'}{'+tex(p['k']*X+p['d'])+'}+'+mul(a,v)
 if family=='linear_log':
  if p['b']==0:return tex(a)+'+'+mul(a,v)
  return r'\frac{'+tex(u)+'}{x}+'+mul(a,v)
 if family in ('exp_sin','named_exp_sin'):
  c=a*p.get('b',1);return tex(c*s.exp(X))+r'(\cos x+\sin x)'
 if family in ('poly_exp','power_exp'):return tex(s.exp(X))+group(s.expand(u+du))
 if family=='linear_cos':return '-'+group(u)+r'\sin x+'+tex(a)+r'\cos x'
 if family=='power_tan':return tex(u)+r'\sec^{2}x+'+tex(du)+r'\tan x'
 return tex(s.expand(u*dv+v*du))

def solution(template,p,u,v,observed):
 t=p['t'];du=s.diff(u,X);dv=s.diff(v,X);der=s.diff(u*v,X)
 family=TEMPLATES[template][1]
 un,vn=('f','h') if template.startswith('q-167') else ('u','v')
 primitive='We differentiate using the product rule. '+('Recall that' if un=='f' else 'Let')+' $'+un+'(x)='+tex(u)+'$ and $'+vn+'(x)='+tex(v)+'.$ '+('Then,' if un=='f' else 'Then, we have')
 if un=='f':
  operator=r'\frac{\mathrm d}{\mathrm dx}'
  primitive+='\n\n$$\n'+r'\begin{aligned}\frac{\mathrm df}{\mathrm dx} &='+operator+group(u)+'='+tex(du)+r' \\ \frac{\mathrm dh}{\mathrm dx} &='+operator+group(v)+'='+tex(dv)+r'.\end{aligned}'+'\n$$'
 else:primitive+='\n\n$$\n'+un+"'(x)="+tex(du)+r',\quad '+vn+"'(x)="+tex(dv)+'.\n$$'
 reduction=source_derivative(family,p,u,v,du,dv) if observed else tex(s.factor(der))
 rows=[un+vn+"'(x)+"+vn+un+"'(x)",add((u,dv),(v,du)),reduction+'.']
 if observed and template=='q-319829':rows=rows[:2];rows[-1]+='.'
 result=s.simplify(der.subs(X,t))
 sub=lambda z:tex(z).replace('x','('+tex(t)+')')
 substitution='('+sub(u)+')\\cdot ('+sub(dv)+')+('+sub(v)+')\\cdot ('+sub(du)+')'
 evaluated=add((u.subs(X,t),dv.subs(X,t)),(v.subs(X,t),du.subs(X,t)))
 symbolic=r'\left.'+reduction+r'\right|_{x='+tex(t)+'}'
 ev=[substitution,evaluated,tex(result)+'.']
 if observed:
  substitution=reduction.replace('x','('+tex(t)+')')
  if family in ('exp_sin','named_exp_sin'):
   evaluated=tex(p['a']*p.get('b',1)*s.exp(t))+'('+tex(s.cos(t))+'+'+tex(s.sin(t))+')'
  elif family=='shift_log':
   arg=p['k']*t+p['d'];evaluated=group(p['k']*u.subs(X,t)/arg)+'+'+tex(p['a'])+r'\ln('+tex(arg)+')'
  elif family=='linear_log':
   evaluated=tex(s.cancel(u/X).subs(X,t))+'+'+tex(p['a'])+r'\ln('+tex(t)+')'
  elif family=='poly_exp':
   reduced=s.Poly(s.expand(u+du),X);terms=[]
   for (power,),coefficient in reduced.terms():
    value=coefficient*t**power
    negative=value<0 or (value==0 and coefficient<0)
    terms.append(('-' if negative else '+' if terms else '')+tex(abs(value)))
   evaluated=tex(s.exp(t))+r'\cdot ('+''.join(terms)+')'
  if template in ('q-48515','q-48517'):ev=[symbolic,substitution,tex(result)+'.']
  elif template in ('q-48516','q-48993'):ev=[symbolic,evaluated,tex(result)+'.']
  elif template=='q-31226':ev=[symbolic,substitution,evaluated,tex(result)+'.']
  elif template in ('q-319829','q-319842'):ev=[symbolic if template=='q-319842' else substitution,evaluated+'='+tex(result)+'.']
  else:ev=[substitution,evaluated,tex(result)+'.']
 return primitive+'\n\nApplying the product rule gives\n\n'+block(rows,r'\frac{\mathrm dy}{\mathrm dx}')+'\n\nTo find the slope of the tangent line, we now substitute $x='+tex(t)+'$ into the formula and get\n\n'+block(ev,r'\left.\frac{\mathrm dy}{\mathrm dx}\right|_{x='+tex(t)+'}')+'\n\nTherefore, the slope of the tangent line is $'+tex(result)+'.$'

# EASY: authored small exponential-linear evaluation at 0 or a*x*ln(x) at e.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed product families and evaluation workloads; familiar angles.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored quadratic with all coefficients nonzero and both contributions.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unsupported level')
 r=random.Random(seed)
 eligible=[k for k,v in TEMPLATES.items() if v[0]==level and (not field_type or v[2]==field_type)]
 template=template or r.choice(eligible)
 if template not in eligible:raise ValueError('Template/field/level mismatch')
 _,family,kind,original=TEMPLATES[template]
 profile=profile or ('authored_operations' if kind=='radio' else 'blank')
 if profile not in ('authored_operations','blank','observed','observed_raw'):raise ValueError('Unknown profile')
 if kind=='radio' and profile=='blank' or kind=='blank' and profile=='authored_operations':raise ValueError('Profile incompatible with field')
 if original is None and profile.startswith('observed'):raise ValueError('No source for observed profile')
 for attempt in range(300):
  p=normalize_parameters(parameters if parameters is not None else sample(r,family,level,template))
  try:
   guard(p,family,level,template if original is not None else None)
   u,v=math_parts(p,family);t=p['t'];der=s.diff(u*v,X);slope=s.simplify(der.subs(X,t))
   if slope.is_real is not True or slope.has(s.oo,s.nan,s.zoo):raise ValueError('Finite real slope required')
   vals=[slope] if kind=='blank' else (observed_bank(template,p,slope,u,v) if profile.startswith('observed') else authored_bank(p,slope,u,v,family))
   vals=[s.simplify(z) for z in vals]
   if any(z.is_real is not True or z.has(s.zoo,s.nan,s.oo) for z in vals):raise ValueError('Nonreal option')
   if any(s.simplify(a-b)==0 for i,a in enumerate(vals) for b in vals[i+1:]):raise ValueError('Complete bank collision')
   if sum(s.simplify(z-slope)==0 for z in vals)!=1:raise ValueError('Bank lacks unique correct slope')
   if level=='hard' and any(s.simplify(z.subs(X,t))==0 for z in (u*s.diff(v,X),v*s.diff(u,X))):raise ValueError('Both hard contributions nonzero')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No eligible complete instance')
 observed=profile.startswith('observed')
 if original is not None:prompt=source_problem(template,u,v,t,profile=='observed_raw')
 else:prompt='If a curve $C$ is given by $y='+mul(u,v)+'$, calculate the slope of the tangent line to the curve at the point where $x='+tex(t)+'$.\n\nSlope $=$ {{field-1}}'
 worked=solution(template,p,u,v,observed)
 key='selection' if kind=='radio' else 'field-1'
 task=digest([s.srepr(s.expand(u*v)),s.srepr(t)])
 content=digest([VERSION,prompt,worked,kind,key,sorted(tex(z) for z in vals)])
 qid=uid(content);fid=uid(content+':'+key)
 choices=[{':answer/id':uid(fid+':'+tex(z)),':answer/type':':answer.type/math',':answer/value':tex(z)} for z in vals]
 correct=next(a[':answer/id'] for a,z in zip(choices,vals) if s.simplify(z-slope)==0)
 r.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':{k:str(z) for k,z in p.items()},'family':family,'source_ids':[template] if original is not None else [],'source':{k:RAW[k] for k in ('database','basis','lineage')},'task_fingerprint':task,'content_fingerprint':content,'authored_difficulty':level=='hard' or level=='easy','domain':'All displayed primitive functions and derivatives defined at the given point','plot_rating':'none','sympy_version':s.__version__}}

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');a=parser.parse_args()
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 records=[generate(level,a.seed+i,a.template,profile=a.profile) for level in levels for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(z) for z in records))
