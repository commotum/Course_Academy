#!/usr/bin/env python3
"""Portable, seeded two-variable substitution generator (captured basis 4610).

The retained source templates cover isolated/unit-variable algebra, known-variable
substitution, ordered differences and supplied affine contexts. Source profiles
are explicit replay modes; normal generation uses standalone prompts and an
identified authored five-choice bank. See instructional-account.md for scope.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186073752-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, json, random, uuid
import sys
sys.dont_write_bytecode=True
import sympy as sp
import re
from math_format import normalize_prose,normalize_tex,system_tex,checked_math_content

KP_ID=17592186073752
KP_UUID='5e79a91b-c479-53da-9f06-59c082fa4187'
TITLE='Solving a System of Linear Equations Using Substitution'
VERSION='substitution-4610-portable-v3'
TEMPLATES={
 'coefficient_b_first':('easy','blank'),
 'coefficient_a_first':('easy','blank'),
 'tuple_xy':('easy','blank'),
 'direct_pq':('moderate','radio'),
 'difference_ab':('moderate','radio'),
 'unit_pair':('hard','blank'),
 'preisolated_uv':('easy','blank'),
 'isolate_xy':('hard','blank'),
 'cake_context':('easy','blank'),
 'meeting_context':('easy','blank'),
 'known_ab':('moderate','radio'),
 'known_xy':('moderate','blank'),
 'isolate_uv':('hard','blank'),
}
PROFILES={'source_context_b':'coefficient_b_first','source_context_a':'coefficient_a_first',
          'source_tuple':'tuple_xy','source_4133':'difference_ab','source_5179':'direct_pq',
          'method_bank_ab':'difference_ab','method_bank_pq':'direct_pq',
 'source_181149':'preisolated_uv','source_181175':'isolate_xy','source_166843':'cake_context','source_166761':'meeting_context','source_52115':'known_ab','source_181154':'known_xy','source_171693':'isolate_uv'}
OPEN='We will isolate a variable in one of the equations and then substitute it into the other equation. '

def number(n,group=False):
 n=sp.Rational(n)
 if n.q != 1:
  return ('-' if n<0 else '')+r'\frac{'+str(abs(n.p))+'}{'+str(n.q)+'}'
 if group and abs(n)>=1000:
  return f'{int(n):,}'.replace(',',r'\,')
 return str(n)

def term(n,v):
 n=sp.Rational(n)
 if n==0:return '0'
 return ('-' if n==-1 else '' if n==1 else number(n))+v

def add(*parts):
 return ''.join(('+' if i and not str(t).startswith('-') else '')+str(t) for i,t in enumerate(parts))

def display(s):return '$$\n'+s+'\n$$'
def aligned(rows):return display(r'\begin{aligned}'+r' \\ '.join(l+' & ='+r for l,r in rows)+r'\end{aligned}')
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def fingerprint(s):return hashlib.sha256(json.dumps(s,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rational(p):
 return {k:sp.Rational(v) for k,v in p.items()}

def check_parameters(name,level,p,profile):
 if name in NEW_TEMPLATES:
  return check_new(name,p)
 expected={'C','k','m','n','R'} if name.startswith('coefficient') else {'A','B','C','S','T'} if name in ('difference_ab','unit_pair') else {'k','C','h'} if name=='tuple_xy' else {'k','C','n','R'}
 if set(p)!=expected:raise ValueError(f'Expected parameters {sorted(expected)}')
 if name.startswith('coefficient'):
  if any(v.q!=1 for v in p.values()) or not (1<=p['k']<=30 and 1<=p['m']<=100 and 1<=p['n']<=1000 and 1<=p['C']<=600):raise ValueError('Coefficient bounds')
  a=(p['R']-p['m']*p['C'])/(p['n']-p['m']*p['k']) if p['n']!=p['m']*p['k'] else sp.oo
  b=p['C']-p['k']*a
  if not (0<abs(p['n']-p['m']*p['k'])<=500 and a.is_Integer and -15<=a<=15 and 0<b<=1000 and p['R']>0):raise ValueError('Easy contextual integer workload')
 elif name=='tuple_xy':
  if any(v.q!=1 for v in p.values()) or not (1<=abs(p['k'])<=6 and abs(p['C'])<=80 and 1<=abs(p['h'])<=12) or p['k']==-1:raise ValueError('Tuple bounds')
  if ((p['C']-p['k']*p['h'])/(1+p['k'])).q!=1:raise ValueError('Easy tuple integer result')
 elif name=='direct_pq':
  if any(v.q!=1 for v in p.values()) or not (1<=p['k']<=6 and 1<=p['n']<=6 and abs(p['C'])<=60 and abs(p['R'])<=60):raise ValueError('Direct bounds')
  if (p['C']/p['k']).q!=1 or ((p['R']-p['C']/p['k'])/p['n']).q!=1:raise ValueError('Easy direct integer results')
 else:
  if any(v.q!=1 for v in p.values()) or not (1<=abs(p['A'])<=6 and 1<=abs(p['B'])<=6 and 1<=abs(p['S'])<=6 and 1<=abs(p['C'])<=80 and 1<=abs(p['T'])<=80):raise ValueError('Unit isolation bounds')
  if p['A']==p['B']*p['S']:raise ValueError('Singular system')
  x=(p['C']-p['B']*p['T'])/(p['A']-p['B']*p['S']);y=p['T']-p['S']*x
  if name=='unit_pair' and not (2<=x.q<=7 and 2<=y.q<=7 and abs(x)<=12 and abs(y)<=12):raise ValueError('Hard requires bounded noninteger pair')
  if name=='difference_ab' and (x.q!=1 or y.q!=1 or abs(x)>12 or abs(y)>12):raise ValueError('Moderate integer-result bounds')

def coefficient(name,p,profile):
 C,k,m,n,R=(p[v] for v in ('C','k','m','n','R'))
 a=(R-m*C)/(n-m*k);b=C-k*a
 f=lambda v:number(v,True)
 first=f(C)+'-'+term(k,'a')
 second=add(term(m,'b'),term(n,'a')) if name=='coefficient_b_first' else add(term(n,'a'),term(m,'b'))
 prompt='The coefficients $a$ and $b$ also satisfy the equation $'+second+'='+f(R)+'.$ Find the values of $a$ and $b.$\n\n$a\\,=$\n{{field-1}}\n\n$b\\,=$\n{{field-2}}'
 if profile not in ('source_context_b','source_context_a'):
  prompt='The coefficients $a$ and $b$ satisfy $b='+first+'.$\n\n'+prompt
 system=r'\{\begin{aligned}b='+first+r' \\ '+second+'='+f(R)+r'\end{aligned}'
 substitute=add(str(m)+'('+first+')',term(n,'a')) if name=='coefficient_b_first' else add(term(n,'a'),str(m)+'('+first+')')
 expanded=add(f(m*C),term(-m*k,'a'),term(n,'a')) if name=='coefficient_b_first' else add(term(n,'a'),f(m*C),term(-m*k,'a'))
 collected=add(f(m*C),term(n-m*k,'a')) if name=='coefficient_b_first' else add(term(n-m*k,'a'),f(m*C))
 rows=[(second,f(R)),(substitute,f(R)),(expanded,f(R)),(collected,f(R)),(term(n-m*k,'a'),f(R-m*C)),('a',f(a))]
 solution='We have the following system of linear equations:\n\n'+display(system)+'\n\n'+OPEN+'\n\nNotice that the first equation is already solved for $b:$\n\n'+display('b='+first)+'\n\nSo, we replace $b$ in the second equation and solve for $a:$\n\n'+aligned(rows)+'\n\nIf we now substitute $a='+f(a)+'$ into $b='+first+',$ we can then find the value of $b:$\n\n'+aligned([('b',f(C)+'-'+str(k)+'('+number(a)+')'),('b',f(b))])+'\n\nTherefore, the solution to the system of equations is $a='+f(a)+r',\,b='+f(b)+'.$'
 return prompt,solution,[a,b],['a','b'],None

def unit(name,p):
 if name=='tuple_xy':
  k,C,h=(p[z] for z in ('k','C','h'));u,v='x','y';x=(C-k*h)/(1+k);y=x+h
  first=add(u,term(k,v))+'='+number(C);second=v+'='+add(u,number(h));isolate=add(u,number(h))
  rows=[(add(u,term(k,v)),number(C)),(add(u,str(k)+'('+isolate+')'),number(C)),(add(u,term(k,u),number(k*h)),number(C)),(add(term(1+k,u),number(k*h)),number(C)),(term(1+k,u),number(C-k*h)),(u,number(x))]
  prompt='Consider the following system of equations:\n$\\{'+first+'; '+second+'$\nFind the solution $(x, y)$ to this system using the method of substitution.\n\nThe solution is\n$($\n{{field-1}}\n$, $\n{{field-2}}\n$)$'
  solution=OPEN+'\n\nNotice that the second equation is already solved for $y:$\n\n'+display(second)+'\n\nSo, we replace $y$ in the first equation and solve for $x:$\n\n'+aligned(rows)+'\n\nIf we now substitute $x='+number(x)+'$ into $'+second+',$ we can then find the value of $y:$\n\n'+aligned([(v,add('('+number(x)+')',number(h))),(v,number(y))])+'\n\nTherefore, the solution to the system of equations is $x='+number(x)+r',\,y='+number(y)+'.$'
  return prompt,solution,[x,y],[u,v],None
 if name=='direct_pq':
  k,C,n,R=(p[z] for z in ('k','C','n','R'));u,v='p','q';x=C/k;y=(R-x)/n
  first=term(k,u)+'='+number(C);second=add(u,term(n,v))+'='+number(R)
  rows=[(add(u,term(n,v)),number(R)),(add('('+number(x)+')',term(n,v)),number(R)),(term(n,v),number(R-x)),(v,number(y))]
  intro='Using the first equation, we can isolate $p$ by dividing both sides by $'+number(k)+':$\n\n'+aligned([(term(k,u),number(C)),(u,number(x))])
  result=x-y
  ending='\n\nTherefore, $p-q='+number(x)+'-('+number(y)+')='+number(result)+'.$'
  solution=OPEN+'\n\n'+intro+'\n\nThen, we substitute $p='+number(x)+'$ into the second equation and solve for $q:$\n\n'+aligned(rows)+ending
 else:
  A,B,C,S,T=(p[z] for z in ('A','B','C','S','T'));u,v=('a','b') if name=='difference_ab' else ('x','y');x=(C-B*T)/(A-B*S);y=T-S*x
  first=add(term(A,u),term(B,v))+'='+number(C);second=add(term(S,u),v)+'='+number(T);isolated=add(number(T),term(-S,u))
  rows=[(add(term(A,u),term(B,v)),number(C)),(add(term(A,u),str(B)+'('+isolated+')'),number(C)),(add(term(A,u),number(B*T),term(-B*S,u)),number(C)),(add(term(A-B*S,u),number(B*T)),number(C)),(term(A-B*S,u),number(C-B*T)),(u,number(x))]
  solution=OPEN+'\n\nUsing the second equation, we can isolate $'+v+'$:\n\n'+aligned([(add(term(S,u),v),number(T)),(v,isolated)])+'\n\nThen, we substitute $'+v+'='+isolated+'$ into the first equation and solve for $'+u+':$\n\n'+aligned(rows)+'\n\nIf we now substitute $'+u+'='+number(x)+'$ into $'+v+'='+isolated+',$ we can then find the value of $'+v+':$\n\n'+aligned([(v,add(number(T),term(-S,'('+number(x)+')'))),(v,number(y))])
  result=x-y
  solution+='\n\nTherefore, '+('$a-b='+number(x)+'-('+number(y)+')='+number(result)+'.$' if name=='difference_ab' else 'the solution to the system of equations is $x='+number(x)+r',\,y='+number(y)+'.$')
 if name=='unit_pair':prompt='Find the solution $(x,y)$ to this system using the method of substitution.\n\n$\\{'+first+'; '+second+'$\n\nThe solution is $($ {{field-1}} $, $ {{field-2}} $)$'
 else:prompt='Given the system of equations below, what is the value of $'+u+' - '+v+'$?\n\n$\\{'+first+'; '+second+'$'
 return prompt,solution,[x,y],[u,v],result

def sample(name,rng):
 if name in NEW_TEMPLATES:return sample_new(name,rng)
 if name.startswith('coefficient'):
  a=rng.randint(-12,12);sign=rng.choice([-1,1]);C=rng.randrange(12,49)*5;k=rng.randint(2,20);m=rng.randint(2,30);n=m*k+sign*rng.randint(2,20)*5
  return dict(C=C,k=k,m=m,n=n,R=m*C+(n-m*k)*a)
 if name=='tuple_xy':
  k=rng.choice([2,3,4,5,6]);x=rng.randint(-8,8);h=rng.choice([-8,-5,-3,2,4,6]);return dict(k=k,C=x+k*(x+h),h=h)
 if name=='direct_pq':
  x=rng.choice([i for i in range(-8,9) if i]);y=rng.choice([i for i in range(-8,9) if i]);k=rng.randint(2,5);n=rng.randint(2,5);return dict(k=k,C=k*x,n=n,R=x+n*y)
 A=rng.choice([-5,-3,-2,2,3,5]);B=rng.choice([-4,-3,-2,2,3,4]);S=rng.choice([-4,-3,-2,2,3,4]);T=rng.choice([i for i in range(-8,9) if i])
 if name=='unit_pair':C=rng.randint(-15,15)
 else:
  x=rng.choice([i for i in range(-7,8) if i]);C=(A-B*S)*x+B*T
 return dict(A=A,B=B,C=C,S=S,T=T)

def assemble(level,seed,name,p,profile,target="forward",assignment="original",row_order="original",bank_rank=2):
 prompt,solution,pair,variables,result=render_new(name,p) if name in NEW_TEMPLATES else coefficient(name,p,profile) if name.startswith('coefficient') else unit(name,p)
 # Canonical presentation precedes all identities; math values remain delimiter-free.
 prompt=canonical_prose(prompt);solution=canonical_prose(solution)
 kind=TEMPLATES[name][1]
 prompt,solution,pair=apply_roles(prompt,solution,pair,variables,name,assignment,row_order,kind)
 if kind=='radio':
  u,v=variables;x,y=pair
  result=x-y if target=='forward' else y-x
  requested=u+' - '+v if target=='forward' else v+' - '+u
  prompt=re.sub(r'what is the value of \$[^$]*\$',lambda m:'what is the value of $'+requested+'$',prompt)
  solution=solution[:solution.rfind('Therefore,')]+ 'Therefore, the solution is $'+u+'='+number(x)+r',\,'+v+'='+number(y)+'.$ So,\n\n'+display(requested+'='+ (number(x)+'-('+number(y)+')' if target=='forward' else number(y)+'-('+number(x)+')')+'='+number(result)+'.')
 if kind=='radio':
  x,y=pair;d=result
  if profile=='source_4133':values=[d/2,-d,-d/2,-3*d/2,d]
  elif profile=='source_5179':values=[d,-2*y,-d,y,x]
  elif profile=='source_52115':values=[y-4,x,x+y,y,d]
  else:values=[d+i-bank_rank for i in range(5)]
  if len(set(values))!=5 or sum(v==d for v in values)!=1:raise ValueError('Whole radio bank rejected: collision')
  answers=[[normalize_tex(number(z)) for z in values]];correct=[normalize_tex(number(d))];keys=['selection']
 else:answers=[[normalize_tex(number(z))] for z in pair];correct=[normalize_tex(number(z)) for z in pair];keys=['field-1','field-2']
 content=fingerprint([VERSION,level,prompt,solution,answers,kind,keys])
 fields=[]
 for key,values,c in zip(keys,answers,correct):
  fid=uid(content+'/field/'+key);bank=[{':answer/id':uid(fid+'/answer/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  cid=next(a[':answer/id'] for a in bank if a[':answer/value']==c)
  random.Random(str(seed)+'/'+key).shuffle(bank)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':bank,':answer-field/correct':[':answer/id',cid]})
 # Canonical system equations read from rendered text for independent QA. The
 # fingerprint uses normalized row-reduced equations, excluding bank/layout.
 u,v=map(sp.Symbol,variables)
 if name.startswith('coefficient'):eqs=[v-p['C']+p['k']*u,p['m']*v+p['n']*u-p['R']]
 elif name in NEW_TEMPLATES:eqs=equations_new(name,p,variables)
 elif name=='tuple_xy':eqs=[u+p['k']*v-p['C'],v-u-p['h']]
 elif name=='direct_pq':eqs=[p['k']*u-p['C'],u+p['n']*v-p['R']]
 else:eqs=[p['A']*u+p['B']*v-p['C'],p['S']*u+v-p['T']]
 if assignment=='exchanged':eqs=[e.xreplace({u:v,v:u}) for e in eqs]
 matrix,rhs=sp.linear_eq_to_matrix(eqs,[u,v]);canonical=[]
 for i in range(2):
  row=list(matrix.row(i))+[-rhs[i]];pivot=next(z for z in row[:2] if z);canonical.append([str(sp.cancel(z/pivot)) for z in row])
 canonical.sort()
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid(content),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'dependencies':{'python':'3.13.5','sympy':sp.__version__},'source_references':SOURCE_REFERENCES[name],'database':'math','basis':4610,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','template':name,'target':target,'assignment':assignment,'row_order':row_order,'bank_rank':bank_rank,'seed':seed,'parameters':{k:str(v) for k,v in p.items()},'bank_profile':profile,'origin':'source-parameter replay; missing captured fields independently completed' if profile and profile.startswith('source_') else 'authored bank/level or parameter extension','serving_eligible':not (profile and profile.startswith('source_')),'mathematical_fingerprint':fingerprint([canonical,('difference:'+target) if kind=='radio' else 'pair']),'content_fingerprint':content,'domain':'Unique real solution of supplied two-variable linear system; integer equation coefficients; exact rational answers; preisolated, unit-isolation, known-variable, or supplied-context substitution workload','plot_rating':'none'}}

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,target=None,assignment=None,row_order=None,bank_rank=None):
 if type(seed) is not int:raise TypeError('seed must be a built-in int')
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if profile:
  if profile not in PROFILES:raise ValueError('Unknown source replay profile')
  if template and template!=PROFILES[profile]:raise ValueError('Profile/template mismatch')
  template=PROFILES[profile]
 allowed=[n for n,(lev,kind) in TEMPLATES.items() if lev==level and (field_type is None or field_type==kind)]
 if not allowed or template and template not in allowed:raise ValueError('Unsupported template/field/level')
 rng=random.Random(seed);name=template or rng.choice(allowed)
 if target not in (None,'forward','reverse'):raise ValueError('Unknown requested difference target')
 if target=='reverse' and (TEMPLATES[name][1]!='radio' or (profile and profile.startswith('source_'))):raise ValueError('Reverse target requires authored radio profile')
 target=target or ('forward' if profile and profile.startswith('source_') else rng.choice(['forward','reverse']) if TEMPLATES[name][1]=='radio' else 'forward')
 if TEMPLATES[name][1]=='radio':profile=profile or 'authored_window'
 replay=bool(profile and profile.startswith('source_'))
 eligible=name not in ('coefficient_a_first','coefficient_b_first','cake_context','meeting_context')
 assignment=assignment or (rng.choice(['original','exchanged']) if eligible and not replay else 'original')
 row_order=row_order or (rng.choice(['original','reversed']) if eligible and not replay else 'original')
 bank_rank=rng.randrange(5) if bank_rank is None else bank_rank
 if assignment not in ('original','exchanged') or row_order not in ('original','reversed') or bank_rank not in range(5):raise ValueError('Invalid role assignment')
 if not eligible and (assignment!='original' or row_order!='original'):raise ValueError('Context roles are fixed')
 for attempt in range(1000):
  try:
   p=rational(parameters if parameters is not None else sample(name,rng))
   check_parameters(name,level,p,profile)
   record=assemble(level,seed,name,p,profile,target,assignment,row_order,bank_rank)
   record['generation']['sampling_attempts']=attempt+1
   return record
  except ValueError:
   if parameters is not None:raise
 raise ValueError('Complete instance sampling exhausted')

# EASY: observed preisolated substitution, simple tuple/context systems. Whole
# source_context profiles preserve the sequential source prompt; defaults supply
# its omitted first equation. Bounds retain integer arithmetic and all stages.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None,target=None):
 return generate('easy',seed,template,field_type,parameters,profile,target)

# MODERATE: observed direct difference and rational-pair forms; the unlabeled
# q-4133 difference form is conservatively assigned here. No progression.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None,target=None):
 return generate('moderate',seed,template,field_type,parameters,profile,target)

# HARD: observed isolate_xy keeps its unit-isolation solve/recovery backbone.
# Retained authored unit_pair uses exact noninteger coordinates of denominator
# 2..7 and magnitude <=12, with integer coefficients and unit y isolation.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None,target=None):
 return generate('hard',seed,template,field_type,parameters,profile,target)

def markdown(record):
 q=record['question'];lines=[q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  lines.append(f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']))
 return '\n'.join(lines)+'\n\n'+q[':question/worked-solution']

NEW_TEMPLATES={'preisolated_uv','isolate_xy','cake_context','meeting_context','known_ab','known_xy','isolate_uv'}

def canonical_prose(text):
 # Recover flattened legacy system wrappers using only their two printed rows.
 text=re.sub(r'\$\\\{([^$]*;[^$]*)\$',lambda m:display(system_tex([v.strip() for v in m[1].split(';')])),text)
 return normalize_prose(text)

def check_new(name,p):
 if name in ADDED_TEMPLATES:return check_added(name,p)
 expected={'A','B','C','S','T'} if name in ('preisolated_uv','isolate_xy') else {'F','c','I','r'} if name=='cake_context' else {'M','s','L','H'}
 if set(p)!=expected or any(v.q!=1 for v in p.values()):raise ValueError('Exact integer source-template parameters required')
 if name in ('preisolated_uv','isolate_xy'):
  A,B,C,S,T=[p[k] for k in ('A','B','C','S','T')]
  den=A*S+B if name=='preisolated_uv' else B-A*S
  if not den or not all(1<=abs(v)<=12 for v in (A,B,S)) or max(abs(C),abs(T))>100:raise ValueError('Unit-isolation bounds')
  v=(C-A*T)/den;u=S*v+T if name=='preisolated_uv' else T-S*v
  if max(abs(u),abs(v))>20 or max(u.q,v.q)>12:raise ValueError('Bounded solution')
 else:
  if min(p.values())<=0:raise ValueError('Positive contextual parameters')
  if name=='cake_context':
   n=(p['F']-p['I'])/(p['r']-p['c']) if p['r']!=p['c'] else sp.oo
   if not (n.is_Integer and 1<=n<=500 and p['F']>p['I'] and p['r']>p['c']):raise ValueError('Whole positive cakes')
  else:
   t=(p['L']-p['H'])/(p['M']+p['s'])
   if not(t.is_Integer and 1<=t<=30 and (p['H']/p['s']).q in (1,2,5,10)):raise ValueError('Positive meeting context')

def sample_new(name,rng):
 if name in ADDED_TEMPLATES:return sample_added(name,rng)
 if name in ('preisolated_uv','isolate_xy'):
  return dict(A=rng.choice([-6,-4,-3,2,3,4,6]),B=rng.choice([-6,-4,-2,1,2,3,5]),C=rng.randint(-18,18),S=rng.choice([-4,-3,-2,-1,1,2,3,4]),T=rng.choice([i for i in range(-8,9) if i]))
 if name=='cake_context':
  I=rng.randint(2,20)*4;c=rng.randint(2,8);r=c+rng.randint(5,18);n=rng.randint(20,150)
  return dict(F=I+(r-c)*n,c=c,I=I,r=r)
 M=rng.choice([40,50,60,70,80]);speed=rng.choice([30,40,50,60]);H=speed*rng.randint(2,5);t=rng.randint(3,12)
 return dict(M=M,s=speed,L=H+(M+speed)*t,H=H)

def equations_new(name,p,variables):
 if name in ADDED_TEMPLATES:return equations_added(name,p,variables)
 u,v=map(sp.Symbol,variables)
 if name=='preisolated_uv':return [p['A']*u+p['B']*v-p['C'],u-p['S']*v-p['T']]
 if name=='isolate_xy':return [p['A']*u+p['B']*v-p['C'],u+p['S']*v-p['T']]
 if name=='cake_context':return [v-p['F']-p['c']*u,v-p['I']-p['r']*u]
 return [v+p['M']*u-p['L'],v-p['s']*u-p['H']]

def render_new(name,p):
 if name in ADDED_TEMPLATES:return render_added(name,p)
 f=lambda z:number(z,True)
 if name in ('preisolated_uv','isolate_xy'):
  A,B,C,S,T=[p[k] for k in ('A','B','C','S','T')];u,v=('u','v') if name=='preisolated_uv' else ('x','y')
  slope=S if name=='preisolated_uv' else -S;den=A*slope+B;vv=(C-A*T)/den;uu=T+slope*vv
  iso=add(term(slope,v),f(T));first=add(term(A,u),term(B,v))+'='+f(C)
  second=u+'='+iso if name=='preisolated_uv' else add(u,term(S,v))+'='+f(T)
  prompt='Consider the following system of equations:\n\n'+display(system_tex([first,second]))+'\n\nFind the solution $('+u+','+v+')$ to this system using the method of substitution.\n\n$('+u+','+v+')=($\n{{field-1}}\n$,$\n{{field-2}}\n$)$'
  if name=='preisolated_uv':intro=OPEN.rstrip()+' It so happens that the second equation is already solved for $'+u+':$'
  else:
   intro=OPEN+"It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.\n\nUsing the second equation, we can isolate $"+u+'$ by '+('adding $'+term(-S,v)+'$ to' if S<0 else 'subtracting $'+term(S,v)+'$ from')+' both sides of the equation:'
  rows=[(add(term(A,u),term(B,v)),f(C)),(add(str(A)+'('+iso+')',term(B,v)),f(C)),(add(term(A*slope,v),f(A*T),term(B,v)),f(C)),(term(den,v),f(C-A*T)),(v,f(vv))]
  recovery=[(u,iso),(u,add(term(slope,'('+number(vv)+')'),f(T)))]
  if name=='isolate_xy':recovery.append((u,add(f(slope*vv),f(T))))
  recovery.append((u,f(uu)))
  solution=intro+'\n\n'+display(u+'='+iso)+'\n\nSo, we replace $'+u+'$ with $'+iso+'$ in the first equation and solve for $'+v+':$\n\n'+aligned(rows)+'\n\nIf we now substitute $'+v+'='+number(vv)+'$ into $'+u+'='+iso+',$ then we can find the value of $'+u+':$\n\n'+aligned(recovery)+'\n\nTherefore, the solution to the system of equations is $'+u+'='+number(uu)+r',\,'+v+'='+number(vv)+',$ which can be expressed as $('+number(uu)+','+number(vv)+').$'
  return prompt,solution,[uu,vv],[u,v],None
 if name=='cake_context':
  F,c,I,r=[p[k]for k in ('F','c','I','r')];n=(F-I)/(r-c);y=I+r*n;cost=add(f(F),term(c,'n'));revenue=add(f(I),term(r,'n'))
  prompt="The pastry shop's total cost and revenue per month (in dollars) from selling cakes can be modeled by the equations $y="+cost+'$ and $y='+revenue+',$ respectively, where $n$ is the number of cakes sold. \n\nSolve the system below using the substitution method to find the exact number of cakes needed to break even and the revenue made.\n\n'+display(system_tex(['y='+cost,'y='+revenue]))+'\n\nThe pastry shop breaks even when$\\,$\n{{field-1}}\n$\\,$cakes are produced. \n\nThe revenue made when selling this number of cakes is$\\,$\n{{field-2}}\n$\\,$dollars.'
  rows=[('y',revenue),(cost,revenue),(cost+'-'+f(I),revenue+'-'+f(I)),(add(f(F-I),term(c,'n')),term(r,'n')),(add(f(F-I),term(c,'n'))+'-'+term(c,'n'),term(r,'n')+'-'+term(c,'n')),(f(F-I),term(r-c,'n')),(r'\frac{'+f(F-I)+'}{'+f(r-c)+'}',r'\frac{'+term(r-c,'n')+'}{'+f(r-c)+'}'),(f(n),'n'),('n',f(n))]
  solution=OPEN+'\n\nNotice that $y$ is isolated in the first equation. Therefore, we can replace $y$ with $'+cost+'$ in the second equation and solve for $n:$\n\n'+aligned(rows)+'\n\nIf we now substitute $n='+f(n)+'$ into $y='+revenue+'$, then we can find the value of $y:$\n\n'+display(r'\begin{aligned}y='+f(I)+'+'+str(r)+'('+f(n)+')='+f(y)+r'\end{aligned}')+'\n\nHence, the solution to the system of equations is $n='+f(n)+'$ and $y='+f(y)+'.$\nTherefore, the pastry shop breaks even when $'+f(n)+'$ units are produced, and the revenue made when selling this number of units is $'+f(y)+'.$'
  return prompt,solution,[n,y],['n','y'],None
 M,speed,L,H=[p[k]for k in ('M','s','L','H')];t=(L-H)/(M+speed);d=H+speed*t;iso=add(f(H),term(speed,'t'));delay=str(float(H/speed)).rstrip('0').rstrip('.')
 prompt="Mary wonders where and when they'd meet if Sam left home $"+delay+'$ minutes earlier and walked with a speed of $'+f(speed)+'$ meters per minute. She finds that the distance $d$ from home they\'d meet can be modeled using the following system of equations.\n\n'+display(system_tex([add('d',term(M,'t'))+'='+f(L),add('d',term(-speed,'t'))+'='+f(H)+'.']))+'\n\nwhere $t$ is the time (in minutes) since Mary left the community park.\n\nMary and Sam would meet$\\,$\n{{field-1}}$\\,$minutes after Mary left the community park.\n\nMary and Sam would meet at a distance of $\\,$\n{{field-2}}$\\,$meters from home.'
 rows=[(add('d',term(M,'t')),f(L)),('('+iso+')+'+term(M,'t'),f(L)),(add(f(H),term(M+speed,'t')),f(L)),(term(M+speed,'t'),f(L)+'-'+f(H)),(term(M+speed,'t'),f(L-H)),('t',r'\frac{'+f(L-H)+'}{'+f(M+speed)+'}'),('t',f(t)+'.')]
 solution="To solve the given system of linear equations, we will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.\n\nUsing the second equation, we can isolate $d$ adding to both sides of the equation $"+term(speed,'t')+':$\n\n'+aligned([(add('d',term(-speed,'t')),f(H)),('d',iso)])+'\n\nSo, we replace $d$ with $'+iso+'$ in the first equation and solve for $t:$\n\n'+aligned(rows)+'\n\nTherefore, they would have met after $t='+f(t)+'$ minutes.\n\nIf we substitute $t='+f(t)+'$ into $d='+iso+'$, we can find the value of $d:$\n\n'+aligned([('d',iso),('',f(H)+'+'+str(speed)+'('+f(t)+')'),('',f(d))])+'\n\nTherefore, they meet at a distance of $'+f(d)+'$ meters from home.'
 return prompt,solution,[t,d],['t','d'],None

SOURCE_REFERENCES={
 'coefficient_b_first':['q-167194','q-167210'], 'coefficient_a_first':['q-167226','q-167218'],
 'tuple_xy':['q-171690'], 'direct_pq':['q-5179'], 'difference_ab':['q-4133'],
 'unit_pair':['e-13009','q-171693'], 'preisolated_uv':['q-181149'], 'isolate_xy':['q-181175'],
 'cake_context':['q-166843'], 'meeting_context':['q-166761','q-135291'],
 'known_ab':['q-52115'], 'known_xy':['q-181154'], 'isolate_uv':['q-171693']}
ADDED_TEMPLATES={'known_ab','known_xy','isolate_uv'}

def check_added(name,p):
 expected={'k','C','m','n','R'} if name!='isolate_uv' else {'A','B','C','S','T'}
 if set(p)!=expected or any(z.q!=1 for z in p.values()):raise ValueError('Integer equation parameters required')
 if name=='isolate_uv':
  if not all(1<=abs(p[k])<=6 for k in ('A','B','S')) or max(abs(p['C']),abs(p['T']))>80 or p['A']==p['B']*p['S']:raise ValueError('Unit isolation bounds')
  x=(p['C']-p['B']*p['T'])/(p['A']-p['B']*p['S']);y=p['T']-p['S']*x
  if max(abs(x),abs(y))>12 or max(x.q,y.q)>12:raise ValueError('Bounded coordinates')
 else:
  if not (1<=p['k']<=6 and 1<=abs(p['m'])<=6 and 1<=abs(p['n'])<=6 and max(abs(p['C']),abs(p['R']))<=80):raise ValueError('Known coordinate bounds')
  x=p['C']/p['k'];y=(p['R']-p['m']*x)/p['n']
  if max(abs(x),abs(y))>12 or max(x.q,y.q)>6:raise ValueError('Bounded coordinates')
  if name=='known_ab' and (x.q!=1 or y.q!=1 or p['k']!=1):raise ValueError('Integer known-variable radio')

def sample_added(name,rng):
 if name=='isolate_uv':
  return dict(A=rng.choice([-5,-3,-2,2,3,5]),B=rng.choice([-4,-3,-2,2,3,4]),C=rng.randint(-18,18),S=rng.choice([-4,-3,-2,-1,1,2,3,4]),T=rng.randint(-8,8))
 if name=='known_xy':
  # Sample integer equations, not an integer dependent answer: q-181154
  # requires a fractional known value to yield another fractional coordinate.
  k=rng.randint(2,6);C=rng.randint(-20,20)
  m=rng.choice([-3,-2,1,2,3]);n=rng.choice([-4,-2,-1,1,2,4]);R=rng.randint(-20,20)
  if abs((R-m*sp.Rational(C,k))/n)>8:raise ValueError('Dependent coordinate magnitude')
  return dict(k=k,C=C,m=m,n=n,R=R)
 x=rng.randint(-8,8);y=rng.randint(-8,8);k=1
 C=k*x
 x=sp.Rational(C,k);m=rng.choice([-3,-2,1,2,3]);n=rng.choice([-4,-2,-1,1,2,4]);R=m*x+n*y
 if R.q!=1:raise ValueError('Sampler only accepts integer equations')
 return dict(k=k,C=C,m=m,n=n,R=R)

def equations_added(name,p,variables):
 u,v=map(sp.Symbol,variables)
 if name=='isolate_uv':return [p['S']*u+v-p['T'],p['A']*u+p['B']*v-p['C']]
 return [p['k']*u-p['C'],p['m']*u+p['n']*v-p['R']]

def render_added(name,p):
 if name=='isolate_uv':
  # Reuse the retained unit-isolation substitution/recovery chain, then reorder
  # the displayed system to reproduce the source's unit equation first.
  prompt,solution,pair,variables,result=unit('unit_pair',p)
  prompt=canonical_prose(prompt)
  prompt=swap_system(prompt)
  solution=swap_references(solution)
  # Source includes its unreduced division before reduction.
  num=p['C']-p['B']*p['T'];den=p['A']-p['B']*p['S']
  old='x & ='+number(pair[0])
  raw=r'\frac{'+str(num)+'}{'+str(den)+'}'
  if abs(den)>1:solution=solution.replace(r' \\ '+old+r'\end{aligned}',r' \\ x & ='+raw+r' \\ '+old+r'\end{aligned}',1)
  prompt=swap_math_symbols(prompt,'x','u');prompt=swap_math_symbols(prompt,'y','v')
  solution=swap_math_symbols(solution,'x','u');solution=swap_math_symbols(solution,'y','v')
  prompt='Consider the following system of equations:\n\n'+display(system_tex([add(term(p['S'],'u'),'v')+'='+number(p['T']),add(term(p['A'],'u'),term(p['B'],'v'))+'='+number(p['C'])]))+'\n\nFind the solution $(u,v)$ to this system using the method of substitution.\n\n$(u,v)=($\n{{field-1}}\n$,$\n{{field-2}}\n$)$'
  solution=solution[:solution.rfind('Therefore,')]+'Therefore, the solution to the system of equations is $u='+number(pair[0])+r',\,v='+number(pair[1])+',$ which can be expressed as $('+number(pair[0])+','+number(pair[1])+').$'
  return prompt,solution,pair,['u','v'],None
 u,v=('a','b') if name=='known_ab' else ('x','y')
 k,C,m,n,R=(p[z] for z in ('k','C','m','n','R'));x=C/k;y=(R-m*x)/n
 first=term(k,u)+'='+number(C);second=add(term(m,u),term(n,v))+'='+number(R)
 if name=='known_ab':prompt='Given the system of equations below, what is the value of $a - b$?\n\n'+display(system_tex([first,second]))
 else:prompt='Consider the following system of equations:\n\n'+display(system_tex([first,second]))+'\n\nFind the solution $(x,y)$ to this system using the method of substitution.\n\n$(x,y)=($\n{{field-1}}\n$,$\n{{field-2}}\n$)$'
 if k==1:intro='It so happens that the first equation is already solved for $'+u+':$\n\n'+display(first)
 else:intro='Using the first equation, we can isolate $'+u+'$ by dividing both sides of the equation by $'+number(k)+':$\n\n'+aligned([(term(k,u),number(C)),(u,number(x))])
 rows=[(add(term(m,u),term(n,v)),number(R)),(add(term(m,'('+number(x)+')'),term(n,v)),number(R)),(term(n,v),number(R-m*x)),(v,number(y))]
 solution=OPEN+'\n\n'+intro+'\n\nIf we now substitute $'+u+'='+number(x)+'$ into $'+second+',$ then we can find the value of $'+v+':$\n\n'+aligned(rows)+'\n\nTherefore, the solution to the system of equations is $'+u+'='+number(x)+r',\,'+v+'='+number(y)+'.$'
 if name=='known_ab':solution+=' So,\n\n'+display('a-b='+number(x)+'-('+number(y)+')='+number(x-y)+'.')
 else:solution+=' This can be expressed as $('+number(x)+','+number(y)+').$'
 return prompt,solution,[x,y],[u,v],x-y if name=='known_ab' else None

def swap_references(s):
 return re.sub(r'\b(first|second)\b',lambda m:'second' if m[0]=='first' else 'first',s)

def swap_system(s):
 pattern=r'(\\left\\\{\\begin\{aligned\})(.*?)(\\end\{aligned\}\\right\.)'
 def replace(m):
  rows=m[2].split(r'\\')
  if len(rows)!=2:raise ValueError('Expected exactly two system equations')
  return m[1]+rows[1].strip()+r' \\ '+rows[0].strip()+m[3]
 return re.sub(pattern,replace,s,count=1,flags=re.S)

def swap_math_symbols(s,u,v):
 def replace(m):
  return re.sub(r'(?<![A-Za-z\\])['+u+v+r'](?![A-Za-z])',lambda n:v if n[0]==u else u,m[0])
 return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$',replace,s)

def apply_roles(prompt,solution,pair,variables,name,assignment,row_order,kind):
 u,v=variables
 if assignment=='exchanged':
  oldpair=list(pair)
  prompt=swap_math_symbols(prompt,u,v);solution=swap_math_symbols(solution,u,v)
  pair=list(reversed(pair))
  # Keep coordinates requested in conventional order, irrespective of which
  # variable occupies the initially isolated role.
  prompt=re.sub(r'\('+v+r'\s*,\s*'+u+r'\)', '('+u+','+v+')',prompt)
  prompt=prompt.replace('{{field-1}}','@@FIELD@@').replace('{{field-2}}','{{field-1}}').replace('@@FIELD@@','{{field-2}}')
  # Reorder the displayed answer blanks too, so tab order matches coordinate order.
  prompt=re.sub(r'\{\{field-2\}\}(\s*\$[^$]*\$\s*)\{\{field-1\}\}',r'{{field-1}}\1{{field-2}}',prompt)
  solution=solution.replace('('+number(oldpair[0])+','+number(oldpair[1])+')','('+number(pair[0])+','+number(pair[1])+')')
 if row_order=='reversed':
  prompt=swap_system(prompt)
  solution=swap_references(solution)
 return prompt,solution,pair


def generate_many(level,count,seed=0,**kwargs):
 if type(count) is not int or count<1:raise ValueError('count must be a positive built-in int')
 if type(seed) is not int:raise TypeError('seed must be a built-in int')
 if count>10000:raise ValueError('Requested count exceeds conservative finite capacity 10000')
 out=[];seen=set()
 for i in range(count*30+100):
  r=generate(level,seed+i,**kwargs);key=r['generation']['mathematical_fingerprint']
  if key not in seen:seen.add(key);out.append(r)
  if len(out)==count:return out
 raise ValueError('Distinct mathematical capacity exhausted')

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='moderate');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(PROFILES));ap.add_argument('--field-type',choices=['radio','blank']);a=ap.parse_args()
 if a.count<1:ap.error('Positive count required')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 if len(levels)>1 and (a.template or a.profile):ap.error('Explicit template/profile requires one difficulty')
 records=[r for l in levels for r in generate_many(l,a.count,a.seed,template=a.template,field_type=a.field_type,profile=a.profile)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186073752-source-policy.json'))

if __name__=='__main__':main()
