#!/usr/bin/env python3
"""Basic two-variable substitution, math basis 1356. Local review only.

Observed: coefficient_b_first / coefficient_a_first (two scalar blanks),
tuple_xy (two scalar tuple fragments), difference_ab / direct_pq (five radios).
Missing moderate/hard labels are authored; hard keeps unit-coefficient isolation
and integer coefficients, but bounded rational results. No challenging-system,
fractional-coefficient, decimal, nonlinear or modelling branch. Source numerical
radio profiles preserve full banks without claiming recovered error intent.
Default radios use one complete method-derived bank, rejecting all collisions.
See private evidence folder for fidelity, repairs, scope and native grading.
"""
import argparse, hashlib, json, random, uuid
from fractions import Fraction
import sympy as sp

KP_ID=17592186073752
KP_UUID='5e79a91b-c479-53da-9f06-59c082fa4187'
TITLE='Solving a System of Linear Equations Using Substitution'
VERSION='substitution-1356-v1'
TEMPLATES={
 'coefficient_b_first':('easy','blank'),
 'coefficient_a_first':('easy','blank'),
 'tuple_xy':('easy','blank'),
 'direct_pq':('easy','radio'),
 'difference_ab':('moderate','radio'),
 'unit_pair':('hard','blank'),
}
PROFILES={'source_context_b':'coefficient_b_first','source_context_a':'coefficient_a_first',
          'source_tuple':'tuple_xy','source_4133':'difference_ab','source_5179':'direct_pq',
          'method_bank_ab':'difference_ab','method_bank_pq':'direct_pq'}
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
 expected={'C','k','m','n','R'} if name.startswith('coefficient') else {'A','B','C','S','T'} if name in ('difference_ab','unit_pair') else {'k','C','h'} if name=='tuple_xy' else {'k','C','n','R'}
 if set(p)!=expected:raise ValueError(f'Expected parameters {sorted(expected)}')
 if name.startswith('coefficient'):
  if any(v.q!=1 for v in p.values()) or not (1<=p['k']<=30 and 1<=p['m']<=100 and 1<=p['n']<=1000 and 1<=p['C']<=600):raise ValueError('Coefficient bounds')
  a=(p['R']-p['m']*p['C'])/(p['n']-p['m']*p['k']) if p['n']!=p['m']*p['k'] else sp.oo
  b=p['C']-p['k']*a
  if not (0<p['n']-p['m']*p['k']<=500 and a.is_Integer and -15<=a<=-1 and 0<b<=1000 and p['R']>0):raise ValueError('Easy contextual integer workload')
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
  prompt='Consider the following system of equations:\n$\\{'+first+'; '+second+'$\nFind the solution $(x, y)$ to this system using the method of substitution.The solution is\n$($\n{{field-1}}\n$, $\n{{field-2}}\n$)$'
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
 if name.startswith('coefficient'):
  C=rng.randrange(12,49)*5;k=rng.randint(2,20);m=rng.randint(2,30);n=m*k+rng.randint(2,20)*5;a=-rng.randint(1,12)
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

def assemble(level,seed,name,p,profile):
 prompt,solution,pair,variables,result=coefficient(name,p,profile) if name.startswith('coefficient') else unit(name,p)
 kind=TEMPLATES[name][1]
 if kind=='radio':
  x,y=pair;d=result
  if profile=='source_4133':values=[d/2,-d,-d/2,-3*d/2,d]
  elif profile=='source_5179':values=[d,-2*y,-d,y,x]
  else:values=[d,-d,x+y,x,y]
  if len(set(values))!=5 or sum(v==d for v in values)!=1:raise ValueError('Whole radio bank rejected: collision')
  answers=[[number(z) for z in values]];correct=[number(d)];keys=['selection']
 else:answers=[[number(z)] for z in pair];correct=[number(z) for z in pair];keys=['field-1','field-2']
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
 elif name=='tuple_xy':eqs=[u+p['k']*v-p['C'],v-u-p['h']]
 elif name=='direct_pq':eqs=[p['k']*u-p['C'],u+p['n']*v-p['R']]
 else:eqs=[p['A']*u+p['B']*v-p['C'],p['S']*u+v-p['T']]
 matrix,rhs=sp.linear_eq_to_matrix(eqs,[u,v]);canonical=[]
 for i in range(2):
  row=list(matrix.row(i))+[-rhs[i]];pivot=next(z for z in row[:2] if z);canonical.append([str(sp.cancel(z/pivot)) for z in row])
 canonical.sort()
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid(content),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','template':name,'seed':seed,'parameters':{k:str(v) for k,v in p.items()},'bank_profile':profile,'origin':'observed replay profile' if profile and profile.startswith('source_') else 'authored bank/level or parameter extension','mathematical_fingerprint':fingerprint([canonical,'difference' if kind=='radio' else 'pair']),'content_fingerprint':content,'domain':'Unique real solution; integer coefficients; unit isolation except direct known-variable equation','plot_rating':'none'}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if profile:
  if profile not in PROFILES:raise ValueError('Unknown profile')
  if template and template!=PROFILES[profile]:raise ValueError('Profile/template mismatch')
  template=PROFILES[profile]
 allowed=[n for n,(lev,kind) in TEMPLATES.items() if lev==level and (field_type is None or field_type==kind)]
 if not allowed or template and template not in allowed:raise ValueError('Unsupported template/field/level')
 rng=random.Random(seed);name=template or rng.choice(allowed)
 if TEMPLATES[name][1]=='radio':profile=profile or ('method_bank_ab' if name=='difference_ab' else 'method_bank_pq')
 for _ in range(1000):
  p=rational(parameters if parameters is not None else sample(name,rng))
  try:
   check_parameters(name,level,p,profile)
   return assemble(level,seed,name,p,profile)
  except ValueError:
   if parameters is not None:raise
 raise ValueError('Complete instance sampling exhausted')

# EASY: observed preisolated substitution, simple tuple/direct systems. Whole
# source_context profiles preserve the sequential source prompt; defaults supply
# its omitted first equation. Bounds retain integer arithmetic and all stages.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)

# MODERATE (authored label): signed small integer equations with a unit y
# coefficient. Isolate y, substitute and distribute, collect, solve, backsubstitute,
# then report a-b. All instances are unordered peers with integer solutions.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)

# HARD (authored missing level): same unit-isolation method and integer-coefficient
# scope, noninteger result denominators 2..7, absolute coordinates <=12. No
# nonunit isolation or fractional coefficients from the adjacent challenging KP.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];lines=[q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  lines.append(f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']))
 return '\n'.join(lines)+'\n\n'+q[':question/worked-solution']

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(PROFILES));ap.add_argument('--field-type',choices=['radio','blank']);a=ap.parse_args()
 if a.count<1:ap.error('Positive count required')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 if len(levels)>1 and (a.template or a.profile):ap.error('Explicit template/profile requires one difficulty')
 records=[generate(l,a.seed+i,a.template,a.field_type,None,a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
