#!/usr/bin/env python3
"""Relocatable, database-free product-rule tangent slopes; see instructional-account.md."""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186096619-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
from math_format import normalize_prose, normalize_tex, checked_math_content
X=s.Symbol('x',real=True)
HERE=Path(__file__).resolve().parent
RAW=json.loads((HERE/'source.json').read_text())
KP=RAW['material']['kp']; QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
VERSION='product-slope-3-format-audit-9122-v1'
ID=17592186096619
TEMPLATES={
 'q-48391':('moderate','exp_linear','radio',dict(a=2,b=1,t='0')),
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
 'q-166073':('moderate','named_exp_sin','blank',dict(a='1/2',b=-4,t='pi')),
 'q-319824':('moderate','linear_log','blank',dict(a=2,b=1,t='1')),
 'q-167316':('moderate','named_x_trig','blank',dict(a=2,b=3,t='0')),
 'q-167769':('moderate','named_x_trig','blank',dict(a=2,b=3,t='0')),
}

def expr(v):
 return s.sympify(v,locals={'pi':s.pi,'E':s.E,'x':X,'sin':s.sin,'cos':s.cos,'tan':s.tan,'exp':s.exp,'log':s.log})
def tex(v):
 v=s.sympify(v).replace(s.sinh,lambda z:(s.exp(z)-s.exp(-z))/2).replace(s.cosh,lambda z:(s.exp(z)+s.exp(-z))/2)
 return normalize_tex(s.latex(v,fold_short_frac=False).replace(r'\log',r'\ln'))
def group(v):return '('+tex(v)+')'
def mul(a,b):return group(a)+r'\cdot '+group(b)
def sum_display(left,right,always=False):
 if always or len(left+right)>60:
  return r'\begin{aligned}&'+left+r' \\ &{}+'+right+r'\end{aligned}'
 return left+'+'+right
def add(a,b):return sum_display(mul(*a),mul(*b))
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
 elif family=='named_x_trig':u=X;v=a*s.sin(X)+b*s.cos(X)
 else:raise ValueError('Unknown family')
 return u,v

def normalize_parameters(p):
 return {k:(v if k=='trig' else expr(v)) for k,v in p.items()}
def guard(p,family,level,observed):
 if level=='easy' and (family!='exp_linear' or p['t']!=0 or p['a'] not in (-4,-3,-2,-1,1,2,3,4) or p['b'] not in range(-3,4)):
  raise ValueError('Easy requires a small exponential-linear product evaluated at zero')
 expected=set(TEMPLATES[observed][3])
 if set(p)!=expected:raise ValueError('Unexpected parameter keys')
 for k,v in p.items():
  if v.is_real is not True or v.is_finite is not True:raise ValueError('Finite real parameters required')
  if k!='t' and not (family=='named_exp_sin' and k=='a') and v.is_integer is not True:raise ValueError('Integer coefficients required')
 if p['a']==0 or abs(p['a'])>9:raise ValueError('Nonzero leading coefficient with magnitude <=9')
 if any(abs(p[k])>9 for k in ('b','c') if k in p):raise ValueError('Small coefficients required')
 if family in ('named_x_trig','named_exp_sin') and p['b']==0:raise ValueError('Nonzero named-function coefficients')
 if 'n' in p and p['n']!=TEMPLATES[observed][3]['n']:raise ValueError('Preserve source polynomial degree')
 t=p['t']
 if family in ('power_sin','power_tan','named_exp_sin','linear_cos','exp_sin','named_x_trig'):
  allowed=(s.pi,2*s.pi,s.pi/4,3*s.pi/4) if family=='power_tan' else (0,s.pi/2,s.pi,3*s.pi/2,s.pi/4,3*s.pi/4)
  if t not in allowed:raise ValueError('Familiar trigonometric angle required')
 elif family=='linear_log':
  if t not in (1,s.E,s.E**2):raise ValueError('Positive familiar logarithm point')
 elif t not in (-1,0,1,2):raise ValueError('Small integer point required')
 if family=='shift_log' and (p['k'] not in (1,2,3,4,5) or p['k']*t+p['d'] not in (1,2)):raise ValueError('Log argument at point must be 1 or 2')
 u,v=math_parts(p,family)
 if any(z.has(s.zoo,s.nan,s.oo,-s.oo) for z in (u.subs(X,t),v.subs(X,t),s.diff(u,X).subs(X,t),s.diff(v,X).subs(X,t))):raise ValueError('Undefined function or slope')

# Select an evaluation/role case before the incidental coefficients.
CASES={
 'exp_linear':('both','B_zero','cancel'),
 'power_sin':('B_only_positive','B_only_negative','A_only','both'),
 'power_tan':('A_only_pi','A_only_2pi','both_positive','both_negative'),
 'shift_log':('A_only','B_only','both','neither'),
 'named_exp_sin':('A_only','B_only','both','cancel'),
 'exp_sin':('A_only','B_only','both','cancel'),
 'linear_cos':('A_only_positive','A_only_negative','B_only','both'),
 'linear_log':('log_zero','log_one','log_two','neither'),
 'power_exp':('both','u_zero','du_zero'),
 'poly_exp':('both','u_zero','du_zero','cancel'),
 'named_x_trig':('outer_zero','half_turn','quarter_turn','both'),
}
def sample(r,family,level,template,case=None):
 case=case or r.choice(CASES[family]); a=r.choice([-4,-3,-2,-1,1,2,3,4]); b=r.choice([-3,-2,-1,1,2,3])
 if family=='exp_linear':
  if level=='easy':
   return dict(a=a,b=0 if case=='B_zero' else -1 if case=='cancel' else r.choice([-3,-2,1,2,3]),t=0)
  t=r.choice([-1,0,1,2]); b=-t if case=='B_zero' else -t-1 if case=='cancel' else r.choice([j for j in range(-3,4) if j not in (-t,-t-1)])
  return dict(a=a,b=b,t=t)
 if family=='linear_log':
  return dict(a=a,b=-a if case=='neither' else b,t={'log_zero':'1','log_one':'E','log_two':'E**2','neither':'1'}[case])
 if family=='power_sin':return dict(a=a,n=3,t={'B_only_positive':'pi/2','B_only_negative':'3*pi/2','A_only':'pi','both':'pi/4'}[case])
 if family=='power_tan':return dict(a=a,n=2,t={'A_only_pi':'pi','A_only_2pi':'2*pi','both_positive':'pi/4','both_negative':'3*pi/4'}[case])
 if family=='shift_log':
  t=r.choice([-1,0,1,2]); k=r.randint(1,5); arg=1 if case in ('A_only','neither') else 2
  b=-a*t if case in ('B_only','neither') else r.choice([j for j in range(-4,5) if j!=-a*t])
  return dict(a=a,b=b,k=k,d=arg-k*t,t=t)
 if family in ('named_exp_sin','exp_sin'):
  p=dict(a='1/2' if family=='named_exp_sin' else a,t={'A_only':'pi','B_only':'pi/2','both':'pi/4','cancel':'3*pi/4'}[case])
  if family=='named_exp_sin':p['b']=2*b
  return p
 if family=='linear_cos':return dict(a=a,b=b,t={'A_only_positive':'pi/2','A_only_negative':'3*pi/2','B_only':'pi','both':'pi/4'}[case])
 if family=='power_exp':
  t=0 if case=='du_zero' else r.choice([-1,1,2]); b=-a*t**3 if case=='u_zero' else b
  return dict(a=a,b=b,n=3,t=t)
 if family=='poly_exp':
  t=r.choice([-1,0,1,2]); c=r.randint(-4,7)
  if case=='u_zero':c=-a*t*t-b*t
  elif case=='du_zero':b=-2*a*t
  elif case=='cancel':c=-a*t*t-b*t-2*a*t-b
  return dict(a=a,b=b,c=c,n=2,t=t)
 if family=='named_x_trig':return dict(a=a,b=b,t={'outer_zero':'0','half_turn':'pi','quarter_turn':'pi/2','both':'pi/4'}[case])
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
def authored_bank(p,slope,u,v,family,r,level='moderate'):
 # Complete arithmetic-error profile: mis-scale a product-rule contribution.
 # Keep the same mathematical basis in correct and incorrect scalar choices.
 ut,vt,du,dv=[s.simplify(z.subs(X,p['t'])) for z in (u,v,s.diff(u,X),s.diff(v,X))]
 if level=='easy':
  # Five consecutive integer multiples of the nonzero A contribution.
  # Placing the key uniformly within a nearby bank avoids making it the
  # only small-magnitude answer among large contribution-offset errors.
  rank=r.randrange(5);sensitivity=s.simplify(ut*dv)
  offsets=list(range(-rank,5-rank))
  return [slope+delta*sensitivity for delta in offsets],{'evaluation':'A','offsets':list(map(str,offsets)),'sensitivity':str(sensitivity)}
 eligible=[(key,z) for key,z in (('A',s.simplify(ut*dv)),('B',s.simplify(vt*du))) if z!=0]
 if not eligible:
  eligible=[(key,z) for key,z in zip(('u(t)','v(t)','du(t)','dv(t)'),(dv,du,vt,ut)) if z!=0]
 if not eligible:raise ValueError('No sensitive product-rule factor')
 key,sensitivity=r.choice(eligible)
 # Choose the key's ordering role first. Sampling an arbitrary four deltas
 # would usually put the correct answer in the middle of the numeric bank.
 below=r.randrange(5)
 positive=[s.Rational(1,4),s.Rational(1,2),s.Rational(3,4),s.Integer(1),s.Integer(2),s.Integer(3),s.Integer(4)]
 offsets=r.sample([-z for z in positive],below)+r.sample(positive,4-below)
 vals=[slope]+[slope+delta*sensitivity for delta in offsets]
 return vals,{'evaluation':key,'offsets':['0']+[str(z) for z in offsets],'sensitivity':str(sensitivity)}

def source_problem(template,u,v,t,raw=False):
 original=QUESTIONS[template][':question/problem']
 family=TEMPLATES[template][1]
 def replace(m):
  body=m.group(1).strip()
  if body.startswith('y'):
   formula='y=f(x)\\cdot h(x)' if family=='named_exp_sin' else 'y=x\\cdot f(x)' if family=='named_x_trig' else 'y='+mul(u,v)
   return '$'+formula+(',' if body.endswith(',') else '')+'$'
  if body.startswith('x'):return '$x='+tex(t)+('.' if body.endswith('.') else '')+'$'
  return m.group(0)
 prompt=re.sub(r'\$([^$]*)\$',replace,original)
 if not raw and family in ('named_exp_sin','named_x_trig'):
  given='Given $f(x)='+tex(u)+'$ and $h(x)='+tex(v)+'$, ' if family=='named_exp_sin' else 'Given $f(x)='+tex(v)+'$, '
  prompt=given+prompt[0].lower()+prompt[1:]
 if not QUESTIONS[template].get(':question/answer-fields'):prompt+='\n\nSlope $=$ {{field-1}}'
 return normalize_prose(prompt)

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
 if family=='named_x_trig':return add((p['a']-p['b']*X,s.sin(X)),(p['b']+p['a']*X,s.cos(X)))
 return tex(s.factor(u*dv+v*du))

def solution(template,p,u,v,observed):
 t=p['t'];du=s.diff(u,X);dv=s.diff(v,X);der=s.diff(u*v,X)
 family=TEMPLATES[template][1]
 # Preserve the source's tangent derivative and direct product-rule step.
 # SymPy's default tan derivative adds an unrequested trig identity rewrite.
 if family=='power_tan':dv=s.sec(X)**2
 un,vn=('f','h') if family=='named_exp_sin' else ('u','v')
 primitive='We differentiate using the product rule. '+('Recall that' if un=='f' else 'Let')+' $'+un+'(x)='+tex(u)+'$ and $'+vn+'(x)='+tex(v)+'.$ '+('Then,' if un=='f' else 'Then, we have')
 if un=='f':
  operator=r'\frac{\mathrm d}{\mathrm dx}'
  primitive+='\n\n$$\n'+r'\begin{aligned}\frac{\mathrm df}{\mathrm dx} &='+operator+group(u)+'='+tex(du)+r' \\ \frac{\mathrm dh}{\mathrm dx} &='+operator+group(v)+'='+tex(dv)+r'.\end{aligned}'+'\n$$'
 else:primitive+='\n\n$$\n'+un+"'(x)="+tex(du)+r',\quad '+vn+"'(x)="+tex(dv)+'.\n$$'
 reduction=source_derivative(family,p,u,v,du,dv)
 rows=[un+vn+"'(x)+"+vn+un+"'(x)",add((u,dv),(v,du)),reduction+'.']
 if observed and template=='q-319829':rows=rows[:2];rows[-1]+='.'
 result=s.simplify(der.subs(X,t))
 sub=lambda z:tex(z).replace('x','('+tex(t)+')')
 substitution=sum_display('('+sub(u)+')\\cdot ('+sub(dv)+')','('+sub(v)+')\\cdot ('+sub(du)+')',always=True)
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

@checked_math_content
def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None,case=None):
 if level not in ('easy','moderate'):raise ValueError('Supported difficulties are easy and moderate')
 r=random.Random(seed)
 eligible=[k for k,v in TEMPLATES.items() if (level!='easy' or k=='q-48391') and (not field_type or v[2]==field_type)]
 if not eligible:raise ValueError('No template supports that difficulty and field type')
 template=template or r.choice(eligible)
 if template not in eligible:raise ValueError('Template/field mismatch')
 _,family,kind,original=TEMPLATES[template]
 profile=profile or ('evaluation_errors' if kind=='radio' else 'blank')
 if profile not in ('evaluation_errors','blank','observed'):raise ValueError('Unknown profile')
 if kind=='radio' and profile=='blank' or kind=='blank' and profile=='evaluation_errors':raise ValueError('Profile/field mismatch')
 if profile=='observed':
  if parameters is None:parameters=original
  if normalize_parameters(parameters)!=normalize_parameters(original):raise ValueError('Observed banks are source replay only')
 selected_case=case or r.choice(CASES[family])
 if selected_case not in CASES[family]:raise ValueError('Unknown decision case')
 for attempt in range(300):
  p=normalize_parameters(parameters if parameters is not None else sample(r,family,level,template,selected_case))
  try:
   guard(p,family,level,template)
   u,v=math_parts(p,family);t=p['t'];der=s.diff(u*v,X);slope=s.simplify(der.subs(X,t)); bank_meta={}
   if slope.is_real is not True or slope.has(s.oo,s.nan,s.zoo):raise ValueError('Finite real slope required')
   if kind=='blank':vals=[slope]
   elif profile.startswith('observed'):vals=observed_bank(template,p,slope,u,v)
   else:vals,bank_meta=authored_bank(p,slope,u,v,family,r,level)
   vals=[s.simplify(z) for z in vals]
   if any(z.is_real is not True or z.has(s.zoo,s.nan,s.oo) for z in vals):raise ValueError('Nonreal option')
   if any(s.simplify(a-b)==0 for i,a in enumerate(vals) for b in vals[i+1:]):raise ValueError('Complete bank collision')
   if sum(s.simplify(z-slope)==0 for z in vals)!=1:raise ValueError('Bank lacks unique correct slope')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No eligible complete instance')
 prompt=source_problem(template,u,v,t,profile=='observed_raw')
 worked=normalize_prose(solution(template,p,u,v,profile.startswith('observed')))
 key='selection' if kind=='radio' else 'field-1'
 task=digest([s.srepr(s.expand(u*v)),s.srepr(t)])
 content=digest([VERSION,prompt,worked,kind,key,sorted(tex(z) for z in vals)])
 qid=uid(content);fid=uid(content+':'+key)
 choices=[{':answer/id':uid(fid+':'+tex(z)),':answer/type':':answer.type/math',':answer/value':tex(z)} for z in vals]
 correct=next(a[':answer/id'] for a,z in zip(choices,vals) if s.simplify(z-slope)==0)
 r.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
 A=s.simplify((u*s.diff(v,X)).subs(X,t)); B=s.simplify((v*s.diff(u,X)).subs(X,t))
 return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':{k:str(z) for k,z in p.items()},'family':family,'source_ids':[template],'source':{k:RAW[k] for k in ('database','basis','lineage')},'original_difficulty':QUESTIONS[template].get(':question/difficulty'),'decision_case':selected_case if parameters is None else 'explicit_parameters','contributions':{'A':str(A),'B':str(B)},'bank':bank_meta,'rejections':attempt,'task_fingerprint':task,'domain':'Both factors and derivatives defined at the point','plot_rating':'none','sympy_version':s.__version__}}

def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186096619-source-policy.json'))

if __name__=='__main__':
 parser=argparse.ArgumentParser()
 parser.add_argument('--difficulty',choices=['easy','moderate','hard'],default='easy')
 parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1)
 parser.add_argument('--format',choices=['markdown','json'],default='json');parser.add_argument('--template');parser.add_argument('--profile')
 args=parser.parse_args()
 if args.count<1:parser.error('count must be positive')
 records=[generate(args.difficulty,args.seed+i,args.template,profile=args.profile) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(z) for z in records))
