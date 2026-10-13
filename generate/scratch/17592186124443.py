#!/usr/bin/env python3
"""Gradient calculations, frozen math basis 1356; local steps 3–7 only.
Observed masks retain each family's prose, held-coordinate zero terms, formal
operators, substitution and reduction stages. Raw profiles preserve attribute
omissions and legacy banks; normal profiles repair legacy presentation. No plots.
Easy: direct polynomial/root and two-term log/trig partials. Moderate: quotient,
atan chain, radial-log evaluation, or supplied component assembly. Hard is an
explicitly authored two-component quotient evaluation workload: both components
require numerator product and denominator quotient terms, then substitution.
Whole banks are selected before parameters; reject entire collisions. All public
explicit parameters obey the same documented bounds. No DB dependencies.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).with_suffix(''); SRC=json.loads((ROOT/'source.json').read_text()); KP=SRC['record']; VERSION='gradient-two-variables-1'
x,y=s.symbols('x y',real=True)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
TEMPLATES={'polynomial':('easy','q-35990'),'root':('easy','q-71349'),'log_cos':('easy','q-71348'),'sin_log':('easy','q-71350'),'atan_product':('moderate','q-71228'),'radial_log':('moderate','q-71229'),'atan_ratio':('moderate','q-351616'),'quotient':('moderate','q-35988'),'components':('moderate','q-168115'),'hard_quotient':('hard',None)}
# Resolve source IDs from captured db identities (not guessed MA numbering).
for name,db in {'root':17592186323860,'log_cos':17592186323861,'sin_log':17592186385501,'atan_product':17592186323738,'radial_log':17592186323740,'atan_ratio':17592186383083}.items():
 TEMPLATES[name]=(TEMPLATES[name][0],next(q[':question/math-academy-id'] for q in SOURCES.values() if q[':db/id']==db))
BASE={'polynomial':dict(a=4,b=-3,c=2,d=1,u=2,v=3),'root':dict(c=3,u=2,v=1),'log_cos':dict(n=2,a=1,b=1),'sin_log':dict(n=2,a=1,b=1),'atan_product':dict(a=4,u=1,v=1),'radial_log':dict(u='1/2',v=0),'atan_ratio':dict(k=1),'quotient':dict(a=3,b=2,k=1),'components':dict(u=1,v=1,P=4,Q=2),'hard_quotient':dict(a=2,b=1,u=2,v=1)}
def L(e):return s.latex(s.sympify(e),ln_notation=True).replace(r'\operatorname{atan}',r'\operatorname{arctan}').replace(r'\pi',r'\pi ')
def num(e):return '('+L(e)+')' if s.sympify(e)<0 else L(e)
def power(v,n):return '{'+v+'}^{'+str(n)+'}'
def vec(A,B,style='tuple'):
 if style=='tuple':return '⟨'+L(A)+r',\,'+L(B)+'⟩'
 return '('+L(A)+r')\text{ }i+('+L(B)+r')\text{ }j'
def block(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def remask(text,m):
 # One pass: complete math component masks cannot overwrite newly inserted slots.
 keys=sorted(m,key=len,reverse=True)
 return re.sub('|'.join(re.escape(k) for k in keys),lambda z:m[z[0]],text) if keys else text

def bounds(t,p):
 if set(p)!=set(BASE[t]):raise ValueError('exact parameter keys required')
 for k,v in p.items():
  if k=='u' and t=='radial_log' or k=='k' and t in ('atan_ratio','quotient'):continue
  if not isinstance(v,int) or isinstance(v,bool):raise ValueError('integer parameters required')
 if t=='polynomial' and not(all(1<=abs(p[k])<=6 for k in 'abcd') and all(1<=abs(p[k])<=4 for k in 'uv')):raise ValueError('polynomial bounds')
 if t=='root' and not(1<=p['c']<=24 and 1<=abs(p['u'])<=5 and -4<=p['v']<=9 and p['v']+p['c'] in [4,9,16,25]):raise ValueError('root perfect square bounds')
 if t in ('log_cos','sin_log') and not (2<=p['n']<=6 and 1<=p['a']<=6 and 1<=p['b']<=6 and s.gcd(p['a'],p['b'])==1):raise ValueError('power/coefficient bounds')
 if t=='atan_product' and not(2<=p['a']<=8 and 1<=abs(p['u'])<=5 and abs(p['v'])==1):raise ValueError('familiar atan evaluation bounds')
 if t=='radial_log' and not(p['v']==0 and s.Rational(p['u'])!=0 and abs(s.Rational(p['u']).p)<=8 and s.Rational(p['u']).q<=8):raise ValueError('radial point bounds')
 if t=='atan_ratio' and not (s.Rational(p['k'])>0 and s.Rational(p['k']).p<=8 and s.Rational(p['k']).q<=8):raise ValueError('primitive rational ratio bounds')
 if t=='quotient' and not(all(1<=p[k]<=8 for k in ('a','b')) and s.Rational(p['k'])>0 and s.Rational(p['k']).p<=8 and s.Rational(p['k']).q<=8):raise ValueError('quotient bounds')
 if t=='components' and not(all(1<=abs(p[k])<=8 for k in ('P','Q')) and all(-4<=p[k]<=4 for k in ('u','v'))):raise ValueError('component bounds')
 if t=='hard_quotient' and not(1<=p['a']<=5 and 1<=p['b']<=4 and 1<=p['u']<=4 and 1<=p['v']<=4):raise ValueError('hard bounds')

def sample(t,r):
 if t=='polynomial':return dict(a=r.randint(1,6),b=-r.randint(1,6),c=r.randint(1,6),d=r.choice([-2,-1,1,2]),u=r.randint(1,4),v=r.randint(1,4))
 if t=='root':
  v=r.randint(-3,3);return dict(c=r.choice([4,9,16])-v,u=r.choice([-4,-3,-2,2,3,4]),v=v)
 if t in ('log_cos','sin_log'):
  a,b=r.choice([(a,b) for a in range(1,7) for b in range(1,7) if s.gcd(a,b)==1]);return dict(n=r.randint(2,6),a=a,b=b)
 if t=='atan_product':return dict(a=r.randint(2,8),u=r.choice([-4,-3,-2,1,2,3,4]),v=r.choice([-1,1]))
 if t=='radial_log':return dict(u=str(s.Rational(r.choice([-8,-7,-5,-3,-2,-1,1,2,3,5,7,8]),r.randint(1,8))),v=0)
 if t=='atan_ratio':return dict(k=str(r.choice(sorted({s.Rational(a,b) for a in range(1,9) for b in range(1,9)}))))
 if t=='quotient':return dict(a=r.randint(1,8),b=r.randint(1,8),k=str(r.choice(sorted({s.Rational(a,b) for a in range(1,9) for b in range(1,9)}))))
 if t=='components':return dict(P=r.choice([-8,-6,-4,-3,-2,2,3,4,6,8]),Q=r.choice([-8,-5,-3,-2,2,3,5,8]),u=r.randint(-4,4),v=r.randint(-4,4))
 return dict(a=r.randint(1,5),b=r.randint(1,4),u=r.randint(1,4),v=r.randint(1,4))

def data(t,p):
 a,b,c,d,u,v,n,k=[s.sympify(p.get(z,1)) for z in ('a','b','c','d','u','v','n','k')]
 point=None
 if t=='polynomial':F=a*x*x+b*x*y+c*y*y+d*y;point=(u,v)
 elif t=='root':F=x*x*s.sqrt(y+c);point=(u,v)
 elif t=='log_cos':F=a*s.log(x*y)+b*s.cos(y**n)
 elif t=='sin_log':F=a*s.sin(x*y)+b*x**n*s.log(y)
 elif t=='atan_product':F=a*x*s.atan(y);point=(u,v)
 elif t=='radial_log':F=s.log(x*x+y*y);point=(u,v)
 elif t=='atan_ratio':F=s.atan(y/(k*x))
 elif t=='quotient':F=(a*x+b*y)/(x-k*y)
 elif t=='hard_quotient':F=(x*x*y+a*y*y)/(x+b*y);point=(u,v)
 else:return None,None,(s.Integer(p['P']),s.Integer(p['Q'])),None
 D=(s.diff(F,x),s.diff(F,y));V=tuple(s.simplify(z.subs({x:point[0],y:point[1]},simultaneous=True)) for z in D) if point else D
 return F,D,V,point

def observed_mask(t,p):
 """Compile complete source math components into parameter slots. No source branch."""
 sid=TEMPLATES[t][1];q=SOURCES[sid];m={}; F,D,V,point=data(t,p)
 if t=='polynomial':
  a,b,c,d,u,v=[p[z] for z in 'abcduv'];sg=lambda z:('+' if z>=0 else '-')+str(abs(z))
  formula=f'{a}{{x}}^{{2}}{sg(b)}xy+{c}{{y}}^{{2}}'+('' if d==1 else sg(d) if d<0 else '+'+str(d))+'y';formula=formula.replace('}+y','}+y')
  if d==1:formula=f'{a}{{x}}^{{2}}{sg(b)}xy+{c}{{y}}^{{2}}+y'
  dx=f'{2*a}x{sg(b)}y';dy=f'{2*c}y{sg(b)}x{sg(d)}'
  m={'4{x}^{2}-3xy+2{y}^{2}+y':formula,'8x-3y+0+0':dx+'+0+0','8x-3y':dx,'0-3x+4y+1':f'0{sg(b)}x+{2*c}y{sg(d)}','4y-3x+1':dy,'8\\cdot 2-3\\cdot 3':f'{2*a}\\cdot {num(u)}{sg(b)}\\cdot {num(v)}','4\\cdot 3-3\\cdot 2+1':f'{2*c}\\cdot {num(v)}{sg(b)}\\cdot {num(u)}{sg(d)}','7\\text{ }i+7\\text{ }j':L(V[0])+r'\text{ }i+'+L(V[1])+r'\text{ }j','(2,3)':f'({L(u)},{L(v)})'}
 elif t=='root':
  c,u,v=[p[z] for z in ('c','u','v')]
  m={'y+3':f'y+{c}','1+3':f'{num(v)}+{c}','2\\cdot 2':f'2\\cdot {num(u)}','{2}^{2}':power(num(u),2),'(2,1)':f'({L(u)},{L(v)})','⟨8,\\,1⟩':vec(*V)}
 elif t in ('log_cos','sin_log'):
  n,a,b=[p[z] for z in ('n','a','b')];cm=lambda k,e:e if k==1 else str(k)+e
  xn=power('x',n);yn=power('y',n);xp='x' if n==2 else power('x',n-1);yp='y' if n==2 else power('y',n-1)
  if t=='log_cos':
   formula=cm(a,r'\operatorname{ln}⁡(xy)')+'+'+cm(b,r'\operatorname{cos}⁡('+yn+')')
   first=r'\frac{'+str(a)+'}{xy}'+r'\cdot y+0'
   dy=r'\frac{'+str(a)+'}{y}-'+str(b*n)+yp+r'\operatorname{sin}⁡('+yn+')'
   m={r'\operatorname{ln}⁡(xy)+\operatorname{cos}⁡({y}^{2})':formula,r'\frac{1}{xy}\cdot y+0':first,r'\frac{1}{x}':r'\frac{'+str(a)+'}{x}',r'\frac{1}{xy}\cdot x-\operatorname{sin}⁡({y}^{2})\cdot 2y':r'\frac{'+str(a)+'}{xy}'+r'\cdot x-'+cm(b,r'\operatorname{sin}⁡('+yn+')')+r'\cdot '+str(n)+yp,r'\frac{1}{y}-2y\operatorname{sin}⁡({y}^{2})':dy}
  else:
   formula=cm(a,r'\operatorname{sin}⁡(xy)')+'+'+cm(b,xn+r'\operatorname{ln}⁡y')
   dx=cm(a,r'y\operatorname{cos}⁡(xy)')+'+'+str(b*n)+xp+r'\operatorname{ln}⁡y'
   dy=cm(a,r'x\operatorname{cos}⁡(xy)')+'+'+r'\frac{'+cm(b,xn)+'}{y}'
   m={r'\operatorname{sin}⁡(xy)+{x}^{2}\operatorname{ln}⁡y':formula,r'y\operatorname{cos}⁡(xy)+2x\operatorname{ln}⁡y':dx,r'x\operatorname{cos}⁡(xy)+{x}^{2}\cdot \frac{1}{y}':cm(a,r'x\operatorname{cos}⁡(xy)')+'+'+cm(b,xn)+r'\cdot \frac{1}{y}',r'x\operatorname{cos}⁡(xy)+\frac{{x}^{2}}{y}':dy}
 elif t=='atan_product':
  a,u,v=[p[z] for z in ('a','u','v')];m={'4x':f'{a}x','4\\operatorname{arctan}⁡1':f'{a}\\operatorname{{arctan}}⁡'+num(v),'4\\operatorname{arctan}':f'{a}\\operatorname{{arctan}}','4\\cdot 1':f'{a}\\cdot {num(u)}','{1}^{2}':power(num(v),2),'4\\cdot \\frac{\\pi }{4}':f'{a}\\cdot '+num(s.atan(v)), '\\frac{4}{2}':r'\frac{'+str(a*u)+'}{2}','⟨\\pi ,\\,2⟩':vec(*V),'(1,1)':f'({L(u)},{L(v)})','\\operatorname{arctan}⁡1':r'\operatorname{arctan}⁡'+num(v)}
 elif t=='radial_log':
  u=s.Rational(p['u']);m={r'\frac{1}{2}':L(u),r'\frac{1}{4}':L(u*u),'8⟨':L(2/u**2)+'⟨','⟨4,\\,0⟩':vec(*V)}
 elif t=='atan_ratio':
  k=s.Rational(p['k']);den=power('x',2)+'+'+power('y',2) if k==1 else power(L(k)+'x',2)+'+'+power('y',2)
  # Slot the whole function, every chain factor and final component separately.
  m={r'\frac{y}{x}':r'\frac{y}{'+('x' if k==1 else L(k)+'x')+'}',r'\frac{y}{{x}^{2}}':r'\frac{y}{'+('' if k==1 else L(k))+power('x',2)+'}',r'\frac{1}{x}':r'\frac{1}{'+('x' if k==1 else L(k)+'x')+'}',r'\frac{{x}^{2}}{{x}^{2}+{y}^{2}}':r'\frac{'+('' if k==1 else L(k*k))+power('x',2)+'}{'+den+'}',r'\frac{y}{{x}^{2}+{y}^{2}}':r'\frac{'+('y' if k==1 else L(k)+'y')+'}{'+den+'}',r'\frac{x}{{x}^{2}+{y}^{2}}':r'\frac{'+('x' if k==1 else L(k)+'x')+'}{'+den+'}'}
 elif t=='quotient':m={r'\frac{3x + 2y}{x - y}':r'\frac{'+str(p['a'])+'x + '+str(p['b'])+'y}{x - '+('' if s.Rational(p['k'])==1 else L(s.Rational(p['k'])))+'y}'}
 elif t=='components':
  # Full value/vector and point masks; never replace isolated short constants.
  m={'(1,1)':f"({p['u']},{p['v']})",r'(1,\,1)':f"({p['u']},\\,{p['v']})",' & =4 ':' & ='+str(p['P'])+' ',' & =2\\end':' & ='+str(p['Q'])+r'\end',r'4\,i+2\,j':str(p['P'])+r'\,i+'+str(p['Q'])+r'\,j','⟨4,\\,2⟩':vec(p['P'],p['Q'])}
 return remask(q[':question/problem'],m), remask(q.get(':question/worked-solution',''),m)

def banks(t,p,profile):
 F,D,V,point=data(t,p);A,B=V;u,v=[s.sympify(p.get(z,1)) for z in ('u','v')]
 if t=='components':return [[(A,)],[(B,)]]
 if profile=='raw' and t=='root':return [[(A/2,B/2),(u,0),(B,A),(2*A,B),V]]
 if profile=='raw' and t=='atan_product':return [[(A,B/p['a']),(u,v),(2*A,0),V,(A/p['a'],B/p['a'])]]
 if profile=='raw' and t=='radial_log':return [[V,(u,u),(2/(u*u),0),(u,v),(2/(u*u),u)]]
 if t=='polynomial':
  a,b,c,d=[p[z] for z in 'abcd'];return [[(2*a*u,2*c*v),(-b*v,b*u),V,(-b*v,2*c*v),(2*a*u,2*c*v+b*u)]]
 if t=='log_cos':
  n,a,b=p['n'],p['a'],p['b'];return [[(a*x,a*y-b*n*s.sin(y**n)),V,(a/x,a/y+b*n*y**(n-1)*s.sin(y)),(a/x,a/y),(a/x,n*y**(n-1)*(a/y-b*s.sin(y**n)))]]
 if t=='sin_log':
  n,a,b=p['n'],p['a'],p['b'];return [[(a*y*s.sin(x*y)+b*n*x**(n-1)*s.log(y),a*x*s.sin(x*y)+b*x**n/y),(a*x*s.cos(x*y)+b*n*x**(n-1)*s.log(y),a*y*s.cos(x*y)+b*x**n/y),(a*y*s.cos(x*y),b*x**n/y),(a*x*s.sin(x*y)+b*n*x**(n-1)*s.log(y),a*y*s.sin(x*y)+b*x**n/y),V]]
 if t=='atan_ratio':
  k=s.Rational(p['k']);den=k*k*x*x+y*y;return [[(-k*x/den,k*y/den),(k*x/den,-k*y/den),(-k*y*y/den,k*x*x/den),V,(-A,-B)]]
 if t=='quotient':
  a,b,k=[s.sympify(p[z]) for z in ('a','b','k')];z=a*k+b;den=(x-k*y)**2;return [[V,(-z*x/den,z*y/den),(z*y/den,z*x/den),(-z*x,z*y),(-z*y,z*x)]]
 # Authored complete method banks, not fitted historical scalar recipes.
 if t=='root':return [[V,(A/2,B),(A,2*B),(B,A),(A,-B)]]
 if t=='atan_product':return [[V,(A/p['a'],B),(A,B/p['a']),(B,A),(-A,B)]]
 if t=='radial_log':return [[V,(A/2,B),(2*A,B),(B,A),(-A,B)]]
 # Two numerator products and two quotient subtractions define hard workload.
 a,b=p['a'],p['b'];N=x*x*y+a*y*y;den=x+b*y;sub={x:u,y:v};val=lambda e:s.simplify(e.subs(sub))
 return [[V,(val(s.diff(N,x)/den),val(s.diff(N,y)/den)),(val((s.diff(N,x)*den+N)/den**2),B),(A,val((s.diff(N,y)*den+b*N)/den**2)),(B,A)]]

def normal_solution(t,p,prompt,solution):
 F,D,V,point=data(t,p)
 if t=='components':
  prompt=f"At $({p['u']},{p['v']})$, the scalar expansion rate $E(x,y)$ has partial derivatives $E_x={p['P']}$ and $E_y={p['Q']}$. Find its gradient. Do not normalize the answer.\n\n$∇E=⟨$ {{{{field-1}}}} $,$ {{{{field-2}}}} $⟩.$"
  solution='The gradient is the vector of the supplied partial derivatives:\n\n'+block([r'∇E & =E_x\,i+E_y\,j',r' & ='+str(p['P'])+r'\,i+'+str(p['Q'])+r'\,j',r' & ='+vec(*V)])
 elif t=='atan_ratio':solution=solution.replace('{f}', '{h}').replace('∇f','∇h')
 elif t in ('quotient','hard_quotient'):
  name='f';u,v=point if point else (x,y);N,den=s.fraction(F)
  nr=L(N);dr=L(den);formula=r'\frac{'+nr+'}{'+dr+'}'
  if t=='hard_quotient':prompt=f'Evaluate $∇f(x,y)$ at $({L(u)},{L(v)})$ if $f(x,y)={formula}.$'
  rows=[]
  for coord,der in zip((x,y),D):
   rows += [r'{f}_{'+str(coord)+r'}(x,y) & =\frac{∂}{∂'+str(coord)+'}('+formula+')',r' & =\frac{('+L(s.diff(N,coord))+')('+dr+')-('+nr+')('+L(s.diff(den,coord))+')}{('+dr+')^{2}}',r' & ='+L(s.factor(der))]
  grows=[r'∇f(x,y) & ={f}_{x}(x,y)\text{ }i+{f}_{y}(x,y)\text{ }j',r' & ='+vec(*D,'basis')]
  if point:
   # unevaluated substitution preserves individual numerator/denominator operations
   sub=lambda raw:re.sub(r'\b[xy]\b',lambda z:'('+L(u if z[0]=='x' else v)+')',raw)
   grows += ['∇f('+L(u)+','+L(v)+r') & ='+sub(vec(*D,'basis')),r' & ='+vec(*V,'basis')]
  solution='First, we find the partial derivatives:\n\n'+block(rows)+'\n\nHence, the gradient is:\n\n'+block(grows)
 return prompt,solution

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 r=random.Random(seed);eligible=[t for t,z in TEMPLATES.items() if z[0]==level and (field_type is None or field_type==('blank' if t=='components' else 'radio'))]
 if template is None:template=r.choice(eligible)
 if template not in eligible:raise ValueError('template/level/field mismatch')
 t=template;raw=profile=='raw';profile=profile or 'method'
 if profile not in ('raw','method'):raise ValueError('profile must be raw or method')
 if raw and t=='hard_quotient':raise ValueError('no observed hard profile')
 for attempt in range(500):
  p=dict(parameters) if parameters is not None else sample(t,r);bounds(t,p);F,D,V,point=data(t,p);bs=banks(t,p,profile)
  valid=all(not any(all(s.simplify(a-b)==0 for a,b in zip(v,w)) for i,v in enumerate(bank) for w in bank[:i]) for bank in bs)
  if valid:break
  if parameters is not None:raise ValueError('whole-bank collision')
 else:raise ValueError('sampler failed')
 q0=SOURCES.get(TEMPLATES[t][1]);prompt,solution=observed_mask(t,p) if q0 else ('','')
 if not raw:
  prompt,solution=normal_solution(t,p,prompt,solution)
 prompt=prompt.replace('+-','-');solution=solution.replace('+-','-')
 # Source style is preserved by answer value masks as complete-vector slots.
 style='basis' if t in ('polynomial','log_cos','sin_log','atan_ratio','quotient','hard_quotient') else 'tuple'
 values=[[L(v[0]) if t=='components' else vec(*v,style) for v in bank] for bank in bs]
 if raw and t=='polynomial':values=values*2;bs=bs*2
 q={':question/problem':prompt}
 if not raw or ':question/worked-solution' in q0:q[':question/worked-solution']=solution
 if not raw or ':question/difficulty' in q0:q[':question/difficulty']=':question.difficulty/'+level
 # Mathematical task identity normalizes common output scaling, excludes banks,
 # symbols, coordinate aliases and source-only component location.
 objs=[s.simplify(z) for z in (D if D else V)];scale=next((s.factor(z).as_coeff_Mul()[0] for z in objs if z!=0),s.Integer(1));canonical=[s.srepr(s.simplify(z/scale)) for z in objs]
 task=hashlib.sha256(json.dumps([t,canonical,[str(z) for z in point] if point else None],sort_keys=True).encode()).hexdigest()
 identity=json.dumps([VERSION,level,prompt,solution if ':question/worked-solution' in q else None,sorted([sorted(v) for v in values]),sorted(q),[(':answer-field/correct' in f) for f in q0[':question/answer-fields']] if raw else [True]*len(values)],sort_keys=True)
 uid=str(uuid.uuid5(uuid.NAMESPACE_URL,identity));q[':question/id']=uid;fields=[]
 for fi,vals in enumerate(values):
  key='field-'+str(fi+1) if t=='components' else 'selection';fid=str(uuid.uuid5(uuid.UUID(uid),'field/'+str(fi)));answers=[]
  for z in vals:answers.append({':answer/id':str(uuid.uuid5(uuid.UUID(fid),z)),':answer/type':':answer.type/math',':answer/value':z})
  correct=next(a[':answer/id'] for a,vv in zip(answers,bs[fi]) if all(s.simplify(a-b)==0 for a,b in zip(vv,(V[fi],) if t=='components' else V)))
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+('blank' if t=='components' else 'radio'),':answer-field/choices':answers}
  if not raw or ':answer-field/correct' in q0[':question/answer-fields'][fi]:f[':answer-field/correct']=[':answer/id',correct]
  if t!='components':r.shuffle(answers)
  fields.append(f)
 q[':question/answer-fields']=fields
 opaque=raw and t in ('root','atan_product','radial_log','components')
 return {'knowledge_point':{'db_id':KP[':db/id'],'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':t,'profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':task,'source':{k:SRC[k] for k in ('database','basis','lineage')},'source_ids':[TEMPLATES[t][1]] if q0 else [],'authored':t=='hard_quotient' or not raw and t=='components','eligible_for_learning':not raw,'evidence_only':raw,'opaque_bank':opaque,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'domain':'xy>0' if t=='log_cos' else 'y>0' if t=='sin_log' else 'real partial derivatives on the displayed function domain'}}
# Easy: independent held-coordinate derivatives; symbolic n changes actual rule.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: familiar-angle/rational-point evaluations or one nested quotient.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: both quotient components plus a genuine nonzero evaluation point.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];out=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):out+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n'
 return out+'\n'+q.get(':question/worked-solution','[Worked solution absent in raw source.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args();records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)];print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
