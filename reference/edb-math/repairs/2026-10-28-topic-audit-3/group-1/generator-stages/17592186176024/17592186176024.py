#!/usr/bin/env python3
"""Green/polar missing-integrand generator, basis 1356; local review only.

Observed templates retain their entire prose and operative row sequences through
complete component masks. Source profiles remain publicly replayable, including
missing source attributes; opaque q-125716 is evidence only. Normal output makes
the requested pointwise integrand criterion explicit. Hard is an authored unequal
cubic extension of the observed moderate cubic family. All arithmetic uses SymPy.
"""
from __future__ import annotations
from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material
import argparse,hashlib,json,random,re,sys,uuid,os,tempfile
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
os.environ.setdefault('MPLCONFIGDIR','/tmp/green-17592186176024-mpl'); ROOT=Path(__file__).with_suffix(''); SNAPSHOT=json.loads((ROOT/'source.json').read_text()); KP=SNAPSHOT['record']
VERSION='green-circular-v2-format-audit-9837-v1'; X,Y,R,T=sp.symbols('x y r theta',real=True)
C=sp.cos(T); S=sp.sin(T)
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
CONFIG={
 'y2':('easy','q-41469',1), 'xy':('easy','q-126526',3),
 'negx2':('easy','q-126542',4), 'cross':('easy','q-126539',6),
 'cubic':('moderate','q-126567',5), 'xy_extra':('moderate','q-126564',2),
 'offset':('moderate','q-126569',4), 'unrated_cross':('moderate','q-125716',3),
 'unequal_cubic':('hard',None,5)}

def tex(e):return sp.latex(e).replace(r'\left', '').replace(r'\right','')
def coeff(n,s):return ('' if n==1 else '-' if n==-1 else str(n))+s

def parse_math(s):
 """Independent reader for displayed polynomial/trig/exponential source notation."""
 s=s.strip().replace('⁡','').replace('θ',r'\theta').replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos')
 s=s.replace('{cos}',r'\cos').replace('{sin}',r'\sin').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','').replace(' ',' ')
 # Balanced braced arguments, including nested fractions and cube roots.
 def group(z,i):
  assert z[i]=='{';depth=1;j=i+1
  while depth:
   if z[j]=='{':depth+=1
   elif z[j]=='}':depth-=1
   j+=1
  return z[i+1:j-1],j
 while r'\frac' in s:
  i=s.index(r'\frac');a,j=group(s,i+5);b,k=group(s,j);s=s[:i]+'(('+a+')/('+b+'))'+s[k:]
 while r'\sqrt[3]'in s:
  i=s.index(r'\sqrt[3]');a,j=group(s,i+8);s=s[:i]+'(('+a+')^(1/3))'+s[j:]
 s=re.sub(r'\\(sin|cos)\^\{?2\}?\s*\\theta',lambda m:' '+m[1]+'(theta)^2',s)
 s=re.sub(r'\\(sin|cos)\s*\(?\s*2\\theta\s*\)?',lambda m:' '+m[1]+'(2*theta)',s)
 s=re.sub(r'\\(sin|cos)\s*\\theta',lambda m:' '+m[1]+'(theta)',s)
 s=re.sub(r'\\(sin|cos)\s*([xy])',lambda m:' '+m[1]+'('+m[2]+')',s)
 while r'\sqrt{'in s:
  i=s.index(r'\sqrt{');a,j=group(s,i+5);s=s[:i]+'(('+a+')^(1/2))'+s[j:]
 for fn in ('sin','cos'):
  power=chr(92)+fn+'^{2}'
  while power+'{' in s:
   i=s.index(power+'{');arg,j=group(s,i+len(power));s=s[:i]+' '+fn+'('+arg+')^2'+s[j:]
  token=chr(92)+fn
  while token+'{' in s:
   i=s.index(token+'{');arg,j=group(s,i+len(token));s=s[:i]+' '+fn+'('+arg+')'+s[j:]
 s=s.replace('e^',' e^').replace(r'\pi',' pi ').replace(r'\theta','theta').replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(s,local_dict={'x':X,'y':Y,'r':R,'theta':T,'e':sp.E,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos},transformations=standard_transformations+(implicit_multiplication_application,))

def model(name,p):
 a,b=p['a'],p['b'];h=p.get('h',1)
 if name=='y2':return a*Y**2,b*X
 if name=='xy':return a*X*Y,b*X+1
 if name=='negx2':return a*Y,-b*X**2
 if name=='cross':return a*X*Y**2,b*X**2*Y
 if name in ('cubic','unequal_cubic'):return a*Y**3+sp.exp(X),(Y**2+10)**sp.Rational(1,3)-b*X**3
 if name=='xy_extra':return a*X*Y-(X+5)**sp.Rational(1,3),b*X+2*Y
 if name=='offset':return a*Y*(X-h),b*X*(Y-h)
 if name=='unrated_cross':return a*X*Y**2,b*X+sp.exp(sp.cos(Y))
 raise ValueError(name)

def pieces(name,p):
 """Ordered unevaluated stages; simplify only after each source operation."""
 a,b=p['a'],p['b'];h=p.get('h',1)
 cs=lambda n,z:coeff(n,z)
 if name=='y2':
  P=cs(a,'{y}^{2}');Q=cs(b,'x');dp=cs(2*a,'y');dq=str(b);curl=f'{b}-{2*a}y';pol=f'{b}-{2*a}\\cdot r\\operatorname{{sin}}⁡\\theta ';last=cs(b,'r')+'-'+cs(2*a,'{r}^{2}\\operatorname{sin}⁡\\theta ');raw=curl;reduced=curl
 elif name in ('xy','xy_extra'):
  P=cs(a,'xy')+(r'-\sqrt[3]{x+5}' if name=='xy_extra' else '');Q=cs(b,'x')+('+2y'if name=='xy_extra'else'+1');dp=cs(a,'x');dq=str(b);curl=str(b)+'-'+cs(a,'x');pol=str(b)+'-'+cs(a,r'r\operatorname{cos}⁡\theta ');last=cs(b,'r')+'-'+cs(a,r'{r}^{2}\operatorname{cos}⁡\theta ');raw=curl;reduced=curl
 elif name=='negx2':
  P=cs(a,'y');Q=cs(-b,'{x}^{2}');dp=str(a);dq=cs(-2*b,'x');curl=dq+'-'+str(a);pol=cs(-2*b,r'\cdot r\operatorname{cos}⁡\theta ')+'-'+str(a);last=cs(-2*b,r'{r}^{2}\operatorname{cos}⁡\theta ')+'-'+cs(a,'r');raw=curl;reduced=curl
 elif name=='cross':
  d=b-a;P=cs(a,'x{y}^{2}');Q=cs(b,'{x}^{2}y');dp=cs(2*a,'xy');dq=cs(2*b,'xy');raw=dq+'-'+dp;reduced=cs(2*d,'xy');pol=cs(2*d,r'\cdot r\operatorname{cos}⁡\theta \cdot r\operatorname{sin}⁡\theta ');last=cs(d,r'{r}^{3}\operatorname{sin}⁡(2\theta )')
 elif name=='offset':
  P=cs(a,f'y(x-{h})');Q=cs(b,f'x(y-{h})');dp=(f'x-{h}'if a==1 else f'{a}(x-{h})');dq=(f'y-{h}'if b==1 else f'{b}(y-{h})');raw='('+dq+')-('+dp+')';reduced=('y-x'if a==1 else f'{a}(y-x)');pol=cs(a,r'r\operatorname{sin}⁡\theta -r\operatorname{cos}⁡\theta ') if a==1 else f'{a}(r\\operatorname{{sin}}⁡\\theta -r\\operatorname{{cos}}⁡\\theta )';last=cs(a,r'{r}^{2}(\operatorname{sin}⁡\theta -\operatorname{cos}⁡\theta )')
 else:
  P=cs(a,'{y}^{3}')+'+{e}^{x}';Q=r'\sqrt[3]{{y}^{2}+10}'+'-'+cs(b,'{x}^{3}');dp=cs(3*a,'{y}^{2}');dq=cs(-3*b,'{x}^{2}');raw=dq+'-'+dp;reduced=raw;pol=cs(-3*b,r'\cdot (r\operatorname{cos}⁡\theta )^{2}')+'-'+cs(3*a,r'\cdot (r\operatorname{sin}⁡\theta )^{2}');last=cs(-3*a,'{r}^{3}') if a==b else cs(-3*b,r'{r}^{3}{cos}^{2}⁡\theta ')+'-'+cs(3*a,r'{r}^{3}{sin}^{2}⁡\theta ')
 return dict(P=P,Q=Q,dp=dp,dq=dq,raw=raw,reduced=reduced,pol=pol,last=last)

def masks(name,p):
 """Source prose remains intact; replace full formal/operative math blocks."""
 _,sid,anchorR=CONFIG[name];q=SOURCES[sid];base={'a':1,'b':2 if name=='cross' else 1,'radius':anchorR,'h':1}
 old=pieces(name,base);new=pieces(name,p)
 sol=q.get(':question/worked-solution','');problem=q[':question/problem']
 # Whole inline P/Q definitions and whole line-integral components first.
 def line(z):
  if name=='negx2':return z['P']+r'\,dx'+z['Q']+r'\,dy'
  def g(s):return '('+s+')'if '+'in s or '-'in s else s
  return g(z['P'])+r'\,dx+'+g(z['Q'])+r'\,dy'
 replacements={line(old):line(new),f'P(x,y)={old["P"]}':f'P(x,y)={new["P"]}',f'Q(x,y)={old["Q"]}':f'Q(x,y)={new["Q"]}'}
 # The offset source prints the two operands without grouping parentheses.
 # Update both source spellings from the same parameter data.
 if name=='offset':
  replacements[old['P']+r'\,dx+'+old['Q']+r'\,dy']=new['P']+r'\,dx+'+new['Q']+r'\,dy'
 replacements[r'\frac{∂P}{∂y}='+old['dp']]=r'\frac{∂P}{∂y}='+new['dp']
 replacements[r'\frac{∂Q}{∂x}='+old['dq']]=r'\frac{∂Q}{∂x}='+new['dq']
 for k in ('raw','reduced','pol','last'):
  z=old[k];v=new[k]
  # Assessed operands adjacent to integral or grouped integral operands.
  replacements['{∬}_{D}('+z+')']='{∬}_{D}('+v+')'
  replacements['{∬}_{D}'+z]='{∬}_{D}'+v
  replacements['{∬}_{Δ}('+z+')']='{∬}_{Δ}('+v+')'
  replacements['{∬}_{Δ}'+z]='{∬}_{Δ}'+v
  replacements['{\\int }_{0}^{'+str(anchorR)+'}'+z]='{\\int }_{0}^{'+str(p['radius'])+'}'+v
 if name=='cross':
  replacements[r'{∬}_{Δ}2{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta ']=r'{∬}_{Δ}'+coeff(2*(p['b']-p['a']),r'{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta ')
 if name=='cubic':
  replacements[r'{∬}_{Δ}(-3{r}^{2}{cos}^{2}⁡\theta -3{r}^{2}{sin}^{2}⁡\theta )']=r'{∬}_{Δ}('+coeff(-3*p['a'],r'{r}^{2}{cos}^{2}⁡\theta ')+'-'+coeff(3*p['a'],r'{r}^{2}{sin}^{2}⁡\theta ')+')'
  replacements[r'{∬}_{Δ}-3{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )']=r'{∬}_{Δ}'+coeff(-3*p['a'],r'{r}^{3}({cos}^{2}⁡\theta +{sin}^{2}⁡\theta )')
 if name in ('cubic','xy_extra','offset'):
  replacements['F(x,y)=⟨'+old['P']+r',\,'+old['Q']+'⟩']='F(x,y)=⟨'+new['P']+r',\,'+new['Q']+'⟩'
 replacements['{\\int }_{0}^{'+str(anchorR)+'}']='{\\int }_{0}^{'+str(p['radius'])+'}'
 replacements['0\\le r\\le '+str(anchorR)]= '0\\le r\\le '+str(p['radius'])
 replacements['{x}^{2}+{y}^{2}='+str(anchorR**2)]='{x}^{2}+{y}^{2}='+str(p['radius']**2)
 # Atomic masking avoids replacements acting on inserted components.
 pattern=re.compile('|'.join(re.escape(k)for k in sorted(replacements,key=len,reverse=True)))
 return pattern.sub(lambda m:replacements[m[0]],problem),pattern.sub(lambda m:replacements[m[0]],sol)

def bank(name,p,profile):
 a,b=p['a'],p['b'];correct=sp.trigsimp((sp.diff(model(name,p)[1],X)-sp.diff(model(name,p)[0],Y)).subs({X:R*C,Y:R*S})*R)
 if profile=='authored':
  P,Q=model(name,p);dp=sp.diff(P,Y).subs({X:R*C,Y:R*S});dq=sp.diff(Q,X).subs({X:R*C,Y:R*S})
  return [correct,sp.trigsimp(dq-dp),sp.trigsimp((dq+dp)*R),sp.trigsimp(dq*R),sp.trigsimp(-dp*R)],0
 if name=='y2':return [b*R-2*a*R**2*S,b*R-a*R**2*C,b*R-a*R**2*S,b-2*a*R*S,a*R**2*S-b*R*C],0
 if name=='xy':return [b-a*R*C,b-a*R*S,b*R-a*R**2*S,correct,b*R-a*R**2*sp.sin(2*T)/2],3
 if name=='negx2':return [-2*b*R**2*C,-2*b*R*C-a,correct,-2*b*R*S-a,-2*b*R**2*S-a*R],2
 if name=='cross':
  k=b-a;return [R-k*R**3*sp.sin(2*T),1-k*R**2*sp.sin(2*T),k*R**2*sp.sin(2*T),1-k*R**3*sp.sin(2*T),correct],4
 if name=='cubic':return [-3*a*R,-3*a*R**3*sp.cos(2*T),correct,-3*a*R**2,-3*a*R**2*sp.cos(2*T)],2
 if name=='xy_extra':return [b-a*R*S,b*R-a*R**2*S,2*R*S-a*R**2*C,b-a*R*C,correct],4
 if name=='offset':return [a*R*(S-C),a*R**2*sp.cos(2*T),a*R**2*(S-C),a*R**2,a*R*sp.cos(2*T)],2
 if name=='unrated_cross':return [correct,b*sp.exp(C)-a*S**2,b*R-a*R**2*S,b*R+a*R**2*S,R*(b*sp.exp(C)-a*S**2)],0
 raise ValueError('Unsupported original profile')

def render_plots(radius,output_dir=ROOT/'plots'):
 """Atomic deterministic PNG and sidecar; parameter generation never resamples."""
 import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;import numpy as np
 output_dir=Path(output_dir);output_dir.mkdir(exist_ok=True,parents=True);key=f'circle-{radius}';path=output_dir/(key+'.png');meta=output_dir/(key+'.json')
 if path.exists()and meta.exists():return str(path.resolve())
 fig,ax=plt.subplots(figsize=(4,3.5),dpi=160);t=np.linspace(0,2*np.pi,500)
 ax.fill(radius*np.cos(t),radius*np.sin(t),color='#d5e8f6');ax.plot(radius*np.cos(t),radius*np.sin(t),color='orange',lw=1.5)
 lim=radius*1.42;ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);ax.set_aspect('equal');ax.axis('off')
 for direction in [(lim,0),(0,lim)]:ax.annotate('',xy=direction,xytext=(-direction[0],-direction[1]),arrowprops={'arrowstyle':'->','lw':.8})
 for ang in [np.pi/4,3*np.pi/4,5*np.pi/4,7*np.pi/4]:
  ax.annotate('',xy=(radius*np.cos(ang+.08),radius*np.sin(ang+.08)),xytext=(radius*np.cos(ang-.08),radius*np.sin(ang-.08)),arrowprops={'arrowstyle':'->','lw':1,'color':'black'})
 for v in [-radius,radius]:
  ax.text(v,-.08*radius,str(v),ha='center',va='top',fontsize=10);ax.text(-.06*radius,v,str(v),ha='right',va='center',fontsize=10)
 ax.text(.3*radius,.22*radius,'$D$',color='#2679b2');ax.text(.84*radius,.84*radius,'$C$',color='orange');ax.text(lim,.06*radius,'$x$');ax.text(.05*radius,lim,'$y$')
 fd,tmp=tempfile.mkstemp(suffix='.png',dir=output_dir);os.close(fd)
 try:fig.savefig(tmp,bbox_inches='tight',facecolor='white');os.replace(tmp,path)
 finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
 data={'radius':radius,'orientation':'counterclockwise','renderer':'Matplotlib','matplotlib':matplotlib.__version__,'python':sys.version.split()[0],'equal_aspect':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 fd,tmp=tempfile.mkstemp(suffix='.json',dir=output_dir);os.close(fd);Path(tmp).write_text(json.dumps(_ca_material(data),indent=2));os.replace(tmp,meta);return str(path.resolve())

def authored_solution(name,p):
 # Hard preserves the cubic formal -> substituted -> expansion -> distribution
 # chain, with no false radial identity for unequal weights.
 z=pieces('unequal_cubic',p);radius=p['radius'];P,Q=z['P'],z['Q']
 return rf'''First, notice that we can rewrite our integral as

$$
{{∮}}_{{C}}F\cdot dr={{∮}}_{{C}}({P})\,dx+({Q})\,dy.
$$

Green's theorem states that

$$
{{∮}}_{{C}}P\,dx+Q\,dy={{∬}}_{{D}}(\frac{{∂Q}}{{∂x}}-\frac{{∂P}}{{∂y}})\,\text{{d}}A.
$$

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![]({render_plots(radius)})

Since $P(x,y)={P}$ and $Q(x,y)={Q},$ we obtain

$$
\begin{{aligned}}\frac{{∂P}}{{∂y}}={z['dp']},\,\frac{{∂Q}}{{∂x}}={z['dq']}.\end{{aligned}}
$$

Applying Green's theorem, we get

$$
\begin{{aligned}}{{∮}}_{{C}}({P})\,dx+({Q})\,dy & ={{∬}}_{{D}}(\frac{{∂Q}}{{∂x}}-\frac{{∂P}}{{∂y}})\text{{d}}A \\ & ={{∬}}_{{D}}({z['raw']})\,\text{{d}}A.\end{{aligned}}
$$

Now, notice that the region $D$ can be represented in polar coordinates as

$$
Δ=\{{(r,\theta )\,:\,0\le r\le {radius},\,0\le \theta \le 2\pi \}}.
$$

The change of variables formula for plane polar coordinates states that

$$
{{∬}}_{{D}}f(x,y)\,dA={{∬}}_{{Δ}}f(r\cos\theta,r\sin\theta)\,r\,drd\theta.
$$

Therefore, we can write our double integral as

$$
\begin{{aligned}}{{∬}}_{{D}}({z['raw']})\,\text{{d}}A & ={{∬}}_{{Δ}}({z['pol']})\,r\,\text{{d}}r\text{{d}}\theta \\ & ={{∬}}_{{Δ}}(-{3*p['b']}{{r}}^{{2}}{{cos}}^{{2}}⁡\theta -{3*p['a']}{{r}}^{{2}}{{sin}}^{{2}}⁡\theta )\,r\,\text{{d}}r\text{{d}}\theta \\ & ={{∬}}_{{Δ}}({z['last']})\,\text{{d}}r\text{{d}}\theta \\ & ={{\int }}_{{0}}^{{2\pi }}\,{{\int }}_{{0}}^{{{radius}}}{z['last']}\,\text{{d}}r\,\text{{d}}\theta .\end{{aligned}}
$$'''

def guard(level,name,p):
 if set(p)-{'a','b','radius','h'}:raise ValueError('Unknown parameters')
 if not all(type(p.get(k))is int for k in ('a','b','radius')):raise ValueError('Integer coefficients and radius required')
 if not (1<=p['a']<=6 and 1<=p['b']<=6 and 1<=p['radius']<=6):raise ValueError('Bounds: coefficients/radius 1..6')
 if name=='cross'and p['b']<=p['a']:raise ValueError('Cross requires b>a')
 if name in ('cubic','offset')and p['a']!=p['b']:raise ValueError('Equal coefficients preserve source cancellation')
 if name=='unequal_cubic'and p['a']==p['b']:raise ValueError('Hard requires unequal cubic weights')
 if name=='offset'and not(type(p.get('h',1))is int and 1<=p.get('h',1)<=4):raise ValueError('Offset 1..4')
 if name=='xy_extra'and p['radius']>=5:raise ValueError('Cube root x+5 must be smooth on disk')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Invalid difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio shape supported')
 rng=random.Random(seed);names=[k for k,v in CONFIG.items()if v[0]==level]
 name=template or rng.choice(names)
 if name not in names:raise ValueError('Template incompatible with difficulty')
 if profile is None:profile='authored'if name in ('unequal_cubic','unrated_cross')else 'normal'
 if profile=='normal' and name in ('unequal_cubic','unrated_cross'):profile='authored'
 if profile not in ('normal','original','authored'):raise ValueError('Unknown profile')
 if name=='unequal_cubic'and profile=='original':raise ValueError('No observed hard bank')
 if parameters is None:
  for attempt in range(1000):
   p={'a':rng.randint(1,6),'b':rng.randint(1,6),'radius':rng.randint(1,4 if name=='xy_extra'else 6)}
   if name in ('offset','cubic'):p['b']=p['a']
   if name=='offset':p['h']=rng.randint(1,4)
   try:guard(level,name,p);values,ci=bank(name,p,profile);eligible(values);break
   except ValueError:continue
  else:raise ValueError('No eligible instance')
 else:
  p=dict(parameters);guard(level,name,p);values,ci=bank(name,p,profile)
  if profile!='original':eligible(values)
 raw=profile=='original';sid=CONFIG[name][1];src=SOURCES.get(sid)
 if name=='unequal_cubic':
  z=pieces(name,p);problem=rf'Given that ${{∮}}_C F\cdot dr=\int_0^{{2\pi}}\int_0^{{{p["radius"]}}}\boxed{{}}\,dr\,d\theta$, where $F(x,y)=⟨{z["P"]},\,{z["Q"]}⟩$ and $C$ is the circle $x^2+y^2={p["radius"]**2}$ oriented counterclockwise, what expression belongs in the blank after applying Green’s theorem and changing to polar coordinates, simplified pointwise before integration?';solution=authored_solution(name,p)
 elif name=='unrated_cross':
  a,b=p['a'],p['b'];rad=p['radius'];problem=src[':question/problem'].replace('xy^{2}',coeff(a,'xy^{2}')).replace('x + e^{',coeff(b,'x')+' + e^{').replace('^{3}AAAA','^{'+str(rad)+'}AAAA').replace('= 9','= '+str(rad**2));solution=''
 else:problem,solution=masks(name,p)
 if not raw:
  problem=problem.replace('AAAAAAAA',r'\boxed{}')
  if 'simplified pointwise'in problem:pass
  else:problem=problem+r' Use $x=r\cos\theta$, $y=r\sin\theta$, and simplify the integrand pointwise before integration.'
  if name=='unrated_cross':solution=unrated_solution(p)
  if solution:
   solution=re.sub(r'!\[\]\([^)]*\)',lambda m:'![]('+render_plots(p['radius'])+')',solution)
  solution=solution.replace('Δ={(r,','Δ=\\{(r,').replace('2\\pi }.','2\\pi \\}.')
 if raw and solution and p['radius']!=CONFIG[name][2]:
  solution=re.sub(r'!\[\]\([^)]*\)',lambda m:'![]('+render_plots(p['radius'])+')',solution)
 # Source answer values are normalized notation but mathematically recipe-derived.
 values_tex=[tex(v)for v in values]
 if not raw:problem=_ca_problem(problem);solution=_ca_prose(solution);values_tex=_ca_values(values_tex)
 identity={'version':VERSION,'level':None if raw and ':question/difficulty'not in src else level,'prompt':problem,'solution':None if raw and ':question/worked-solution'not in src else solution,'bank':sorted(values_tex),'correct':values_tex[ci]if not(raw and ':answer-field/correct'not in src[':question/answer-fields'][0])else None}
 digest=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest();qid=str(uuid.uuid5(uuid.NAMESPACE_URL,digest));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v}for v in values_tex]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers.copy()}
 if not(raw and ':answer-field/correct'not in src[':question/answer-fields'][0]):field[':answer-field/correct']=[':answer/id',answers[ci][':answer/id']]
 rng.shuffle(field[':answer-field/choices']);question={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
 if not(raw and ':question/difficulty'not in src):question[':question/difficulty']=':question.difficulty/'+level
 if not(raw and ':question/worked-solution'not in src):question[':question/worked-solution']=solution
 P,Q=model(name,p);task={'P':sp.srepr(P),'Q':sp.srepr(Q),'criterion':'pointwise missing polar integrand','difficulty':level}
 # Radius does not affect the missing integrand operation; field-insensitive terms
 # and cancelled common offsets are incidental to this response.
 task['P']=sp.srepr(sp.diff(P,Y));task['Q']=sp.srepr(sp.diff(Q,X))
 if name=='offset':
  py,qx=sp.diff(P,Y),sp.diff(Q,X)
  task['P']=sp.srepr(py-py.subs({X:0,Y:0}))
  task['Q']=sp.srepr(qx-qx.subs({X:0,Y:0}))
 record={'knowledge_point':{'db_id':17592186176024,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':name,'profile':profile,'seed':seed,'parameters':p,'source_id':sid,'source_provenance':{k:SNAPSHOT[k]for k in ('database','basis','lineage')},'authored_difficulty':name=='unequal_cubic' or name=='unrated_cross','evidence_only':raw and name=='unrated_cross','eligible_for_learning':not(raw and name=='unrated_cross'),'mathematical_fingerprint':hashlib.sha256(json.dumps(task,sort_keys=True).encode()).hexdigest(),'content_fingerprint':digest,'python':sys.version.split()[0],'sympy':sp.__version__}}
 return record

def eligible(v):
 if len(v)!=5:raise ValueError('Incomplete bank')
 for i,e in enumerate(v):
  for f in v[:i]:
   if sp.trigsimp(sp.expand(e-f))==0:raise ValueError('Pointwise equivalent bank')

def unrated_solution(p):
 P,Q=model('unrated_cross',p);dp=sp.diff(P,Y);dq=sp.diff(Q,X);curl=dq-dp;pol=curl.subs({X:R*C,Y:R*S});last=sp.trigsimp(pol*R)
 return rf'''First, notice that we can rewrite our integral as $\oint_C F\cdot dr=\oint_C({tex(P)})\,dx+({tex(Q)})\,dy$.

Green's theorem states that $\oint_C P\,dx+Q\,dy=\iint_D(\frac{{\partial Q}}{{\partial x}}-\frac{{\partial P}}{{\partial y}})\,dA$.

In our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:

![]({render_plots(p['radius'])})

Since $P(x,y)={tex(P)}$ and $Q(x,y)={tex(Q)}$, we obtain $\frac{{\partial P}}{{\partial y}}={tex(dp)}$, $\frac{{\partial Q}}{{\partial x}}={tex(dq)}$.

Applying Green's theorem, we get $\oint_C F\cdot dr=\iint_D({tex(dq)}-({tex(dp)}))\,dA=\iint_D({tex(curl)})\,dA$.

Now, notice that the region $D$ can be represented in polar coordinates as $\Delta=\{{(r,\theta):0\le r\le {p['radius']},0\le\theta\le2\pi\}}$.

The change of variables formula for plane polar coordinates states that $\iint_D f(x,y)\,dA=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,dr\,d\theta$.

Therefore, we can write our double integral as $\iint_D({tex(curl)})\,dA=\iint_\Delta({tex(pol)})r\,dr\,d\theta=\int_0^{{2\pi}}\int_0^{{{p['radius']}}}{tex(last)}\,dr\,d\theta$.'''

# Easy: direct polynomial Pdx+Qdy, two partials, subtraction, polar/Jacobian.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: vector-field rewrite plus ignored held-coordinate terms or offset
# cancellation; cubic source retains expansion and cos²+sin² identity.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard (authored): vector rewrite, two unequal cubic derivatives, two squared
# polar products, expansion/distribution; unequal weights forbid radial collapse.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(rec):
 q=rec['question'];s=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:s+='- $'+a[':answer/value']+'$\n'
 return s+'\n'+q.get(':question/worked-solution','[No original worked solution.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile)for l in (['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty])for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False)if args.format=='json'else '\n\n---\n\n'.join(markdown(r)for r in records))
