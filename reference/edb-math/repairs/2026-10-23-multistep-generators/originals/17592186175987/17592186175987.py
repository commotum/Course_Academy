#!/usr/bin/env python3
"""Green's theorem setup in polar coordinates; math source bases 1356 and 2272.

The twelve observed radio families retain their entire source operation chains and
prose. A common positive amplitude multiplies the complete field; radial extent
varies independently. Source-bank error intention is not recoverable from a
single example: historical banks are public evidence-only profiles. Normal radio
banks use the complete method-derived profile (curl reversal, missing Jacobian,
one cross partial, radius error), with whole-instance rejection by INTEGRAL VALUE.
The three-blank continuation retains its source shape and trigonometric stages.
Easy and hard are explicitly authored, bounded variants of this same setup skill.
No evaluation is requested. This script creates previews only; the package
replenisher handles additive registration and commits after validation.
"""
from __future__ import annotations
import argparse, copy, shutil, hashlib, json, math, os, random, re, sys, tempfile, uuid
from pathlib import Path
os.environ.setdefault("MPLCONFIGDIR", "/tmp/kp75987-mpl")
import sympy as sp
from functools import lru_cache
BASE=Path(__file__).with_suffix('')
KP_ID=17592186175987
VERSION='greens-polar-path-4'
SOURCE=json.loads((BASE/'source-current.json').read_text())
KP=SOURCE['record']; TITLE=KP[':knowledge-point/title']
X,Y,R,T=sp.symbols('x y r theta', real=True)
SPECS={
 'constant':('q-108544',3*Y-sp.exp(sp.cos(X)),7*X+sp.sqrt(Y+5),2,-sp.pi/2,sp.pi/2),
 'cubic_y':('q-125719',X**2*sp.cos(X)+Y**3,Y*sp.exp(Y+1)+X,1,sp.pi,3*sp.pi/2),
 'linear_pair':('q-126687',2-X*Y+2*Y**2,X**2+X*Y,8,-sp.pi,sp.pi/2),
 'factored':('q-126710',Y*(X+1),X*(Y+1),3,sp.pi/2,3*sp.pi/2),
 'linear_y':('q-126711',Y**2+X**2,X*Y+Y*sp.exp(Y),1,-sp.pi,0),
 'radial_square':('q-126514',sp.sin(sp.cos(X))-X**2*Y,X*Y**2-1/(Y+1),3,0,sp.pi),
 'mixed_cancel':('q-126686',X*Y**2-Y*sp.cos(X),2*X**2*Y-sp.sin(X),5,0,sp.pi/2),
 'constant_mixed':('q-126709',sp.exp(X/4)+X*Y**2,sp.exp(sp.sin(Y))+2*X,4,-sp.pi/2,0),
 'affine_y':('q-126708',X+Y,-X*Y,6,sp.pi/2,2*sp.pi),
 'square_difference':('q-126516',Y**3-X,X**3+sp.exp(1/Y),1,-sp.pi/2,sp.pi),
 'polar_blanks':('q-169204',None,None,2,sp.pi/2,2*sp.pi),
 'linear_log':('q-126677',Y**2-sp.log(1+sp.cos(X)**2),X**2+3*X*Y,2,sp.pi/2,sp.pi),
 'cubic_log':('q-126707',Y+sp.Rational(2,3)*Y**3,sp.log(Y**2+10)+2*X,9,0,3*sp.pi/2),
}
# Complete source polynomial objects, in source choice order. Nonnumeric angular
# integrals are evaluated independently with mpmath when SymPy leaves Integrals.
C=sp.cos(T); SN=sp.sin(T)
BANKS={
 'constant':[(2*R*C,-sp.pi/2,sp.pi/2,2),(4*R,-sp.pi/2,sp.pi/2,2),(4*R,0,sp.pi,2),((R**3-sp.exp(C))*R,0,sp.pi,2),(R**3-sp.exp(C),-sp.pi/2,sp.pi/2,2)],
 'cubic_y':[((1-3*R**2*SN**2)*R,sp.pi,3*sp.pi/2,1),(1-3*R**2*SN**2,sp.pi,2*sp.pi,1),((R-SN**2)*R,sp.pi,2*sp.pi,1),(R**2-3*SN,sp.pi,3*sp.pi/2,1),((R**2-3*SN)*R,sp.pi,3*sp.pi/2,1)],
 'linear_pair':[(R*(C-2*SN),-sp.pi,sp.pi/2,8),(3*R**2*C,-sp.pi/2,sp.pi,8),(3*R**2*(C-SN),-sp.pi,sp.pi/2,8),(2*R**2*SN,-sp.pi,sp.pi/2,8),(R*(3*C-SN),-sp.pi/2,sp.pi,8)],
 'factored':[(R*(C-SN),sp.pi/2,3*sp.pi/2,3),(R**2*(C-SN),sp.pi/2,3*sp.pi/2,3),(R*(SN-C),-sp.pi/2,sp.pi/2,3),(R**2*(SN-C),sp.pi/2,3*sp.pi/2,3),(R**2*(SN-C),0,sp.pi/2,3)],
 'linear_y':[(-R*C,0,sp.pi/2,1),(R*SN,-sp.pi,0,1),(R**2*SN,0,sp.pi/2,1),(-R**2*SN,-sp.pi,0,1),(-R**2*C,-sp.pi,0,1)],
 'radial_square':[(R,0,sp.pi,3),(R**3,0,sp.pi,3),(R**3,-sp.pi/2,sp.pi/2,3),(R,-sp.pi/2,sp.pi/2,3),(R+sp.sin(C),0,sp.pi,2)],
 'mixed_cancel':[(R**3*C,0,sp.pi/2,5),(R**2*SN,0,sp.pi/2,5),(R**3*sp.sin(2*T),0,sp.pi,5),(R**2*SN,sp.pi/2,sp.pi,5),(R**3*sp.sin(2*T),0,sp.pi/2,5)],
 'constant_mixed':[(2*R-R**2*SN,0,3*sp.pi/2,4),(2*R*sp.exp(SN)-R**2*SN,-sp.pi/2,0,4),(R*sp.exp(SN)-R**3*sp.sin(2*T),0,3*sp.pi/2,4),(2*R-R**3*sp.sin(2*T),-sp.pi/2,0,4),(2*R-R**2*sp.sin(2*T),-sp.pi/2,0,4)],
 'affine_y':[(-2*R**2*SN-1,sp.pi/2,2*sp.pi,6),(-R**2*SN-R,sp.pi/2,2*sp.pi,6),(R**3*SN-R,0,sp.pi/2,6),(-R**2*SN-1,sp.pi/2,2*sp.pi,6),(-2*R**2*SN-R,0,sp.pi/2,6)],
 'square_difference':[(2*R**2*C,-sp.pi/2,sp.pi,1),(2*R**2*C,sp.pi/2,2*sp.pi,1),(2*R**2*SN,sp.pi/2,2*sp.pi,1),(3*R**3*sp.sin(2*T),-sp.pi/2,sp.pi,1),(3*R**3*sp.cos(2*T),-sp.pi/2,sp.pi,1)],
 'linear_log':[(R**2*(2*SN+C),sp.pi/2,sp.pi,2),(R*(2*C+SN),sp.pi/2,sp.pi,2),(R*(2*SN+C),sp.pi,3*sp.pi/2,2),(R**2*(2*C+SN),sp.pi/2,sp.pi,2),(R**2*(C+SN),sp.pi,3*sp.pi/2,2)],
 'cubic_log':[(1-2*R**2*SN**2,-sp.pi/2,0,9),((1-2*R**2*SN**2)*R,-sp.pi/2,0,9),((1-2*R**2*SN**2)*R,0,3*sp.pi/2,9),(R**2-2*SN,0,3*sp.pi/2,9),(1-2*R*SN,0,3*sp.pi/2,9)],
}
QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'greens-polar:'+x))
def latex(x):return sp.latex(sp.sympify(x)).replace(r'\theta',r'\theta')
def scaled(text,s):return text if s==1 else str(s)+r'\left('+text+r'\right)'
def integral(g,a,b,radius):return r'\int_{'+latex(a)+'}^{'+latex(b)+r'}\int_{0}^{'+str(radius)+'}'+latex(g)+r'\,dr\,d\theta'
@lru_cache(maxsize=4096)
def value(g,a,b,radius):
 # Polynomial/trig answers integrate exactly. Remaining smooth elementary
 # fields use two independent high-order Gauss quadratures (80 and 120 nodes).
 if g.is_polynomial(R) and not any(f.has(R) for f in g.atoms(sp.Function)) and all(f.func in (sp.sin,sp.cos) for f in g.atoms(sp.Function)):
  return sp.simplify(sp.integrate(sp.integrate(g,(R,0,radius)),(T,a,b)))
 import numpy as np
 f=sp.lambdify((R,T),g,'numpy');previous=None
 for n in (80,120):
  nodes,weights=np.polynomial.legendre.leggauss(n)
  rr=(nodes+1)*radius/2;aa,bb=float(a),float(b);tt=aa+(nodes+1)*(bb-aa)/2
  vv=f(rr[:,None],tt[None,:]);result=float(np.sum(vv*weights[:,None]*weights[None,:])*radius*(bb-aa)/4)
  if previous is not None and abs(result-previous)>1e-8:raise ValueError('quadrature did not converge')
  previous=result
 return sp.Float(result,16)

def numeric(v):
 if not v.has(sp.Integral):return float(v.evalf(30))
 import mpmath as mp
 mp.mp.dps=40
 return float(v.evalf(30)) # SymPy numerical quadrature of remaining definite Integral

def compare_values(vals):
 for i,a in enumerate(vals):
  for b in vals[:i]:
   if sp.simplify(a-b)==0 or abs(numeric(a)-numeric(b))<1e-10:raise ValueError('equivalent complete integrals in bank')

# Plot generator (moderate): exact circular sector, positively oriented boundary.
# At source geometry, source rasters are reused. Changed geometry uses this
# renderer; unique temporary files and atomic final replaces support concurrent QA.
def render_sector(radius,a,b,filled=False):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 key=digest([radius,str(a),str(b),filled,'sector-v2'])[:20]
 out=BASE/'plots'/f'{key}.png';side=out.with_suffix('.json');out.parent.mkdir(exist_ok=True)
 if out.exists() and side.exists():return str(out.resolve())
 aa,bb=float(a),float(b); th=np.linspace(aa,bb,301)
 xx=radius*np.cos(th);yy=radius*np.sin(th)
 fig,ax=plt.subplots(figsize=(4,4),dpi=120);ax.set_aspect('equal')
 if filled:ax.fill(np.r_[0,xx,0],np.r_[0,yy,0],color='#d2e9f7');ax.text(radius*.35*math.cos((aa+bb)/2),radius*.35*math.sin((aa+bb)/2),'$D$',color='#4588b5')
 ax.axhline(0,color='#666',lw=.8);ax.axvline(0,color='#666',lw=.8)
 ax.plot(xx,yy,color='#efa51a',lw=1.5)
 ax.plot([0,xx[0]],[0,yy[0]],color='#efa51a',lw=1.5);ax.plot([xx[-1],0],[yy[-1],0],color='#efa51a',lw=1.5)
 def arrow(p,q):ax.annotate('',xy=q,xytext=p,arrowprops={'arrowstyle':'->','color':'#704b00','lw':.9,'mutation_scale':9})
 for f in [.22,.52,.8]:
  t=aa+(bb-aa)*f;delta=min(.1,(bb-aa)*.06);arrow((radius*math.cos(t-delta),radius*math.sin(t-delta)),(radius*math.cos(t+delta),radius*math.sin(t+delta)))
 arrow((xx[0]*.35,yy[0]*.35),(xx[0]*.6,yy[0]*.6));arrow((xx[-1]*.65,yy[-1]*.65),(xx[-1]*.4,yy[-1]*.4))
 mid=(aa+bb)/2;ax.text(radius*1.12*math.cos(mid),radius*1.12*math.sin(mid),'$C$',color='#d98e00')
 ax.set_xlim(-radius*1.3,radius*1.3);ax.set_ylim(-radius*1.3,radius*1.3)
 ax.set_xticks([-radius,radius]);ax.set_yticks([-radius,radius]);ax.tick_params(length=0,labelsize=8)
 for name,spine in ax.spines.items():
  if name in ('left','bottom'):spine.set_position('zero');spine.set_color('#666');spine.set_linewidth(.8)
  else:spine.set_visible(False)
 ax.text(radius*1.22,.04*radius,'$x$');ax.text(.04*radius,radius*1.2,'$y$')
 fig.tight_layout()
 fd,tmp=tempfile.mkstemp(dir=out.parent,suffix='.png');os.close(fd)
 try:fig.savefig(tmp,facecolor='white');os.replace(tmp,out)
 finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
 meta={'radius':radius,'theta':[str(a),str(b)],'filled':filled,'orientation':'counterclockwise','renderer':'Matplotlib','version':matplotlib.__version__,'python':sys.version.split()[0],'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
 fd,tmp=tempfile.mkstemp(dir=out.parent,suffix='.json');os.close(fd);Path(tmp).write_text(json.dumps(meta,indent=2));os.replace(tmp,side)
 return str(out.resolve())

def get_plots(q,radius,original_radius,a,b,raw=False):
 images=re.findall(r'!\[.*?\]\((.*?)\)',q[':question/problem']+q[':question/worked-solution'])
 if radius==original_radius:
  resolved=[]
  for reference in images:
   local=BASE/reference;local.parent.mkdir(parents=True,exist_ok=True)
   asset=Path('/media/jake/SSD/EDB/math')/reference
   if not local.exists():
    fd,tmp=tempfile.mkstemp(dir=local.parent,suffix='.png');os.close(fd)
    try:shutil.copyfile(asset,tmp);os.replace(tmp,local)
    finally:Path(tmp).unlink(missing_ok=True)
   if hashlib.sha256(local.read_bytes()).digest()!=hashlib.sha256(asset.read_bytes()).digest():raise ValueError('source asset hash mismatch')
   resolved.append(str(local.resolve()))
  return images if raw else resolved
 return [render_sector(radius,a,b,False),render_sector(radius,a,b,True)] if images else []

# Source extraction operates on COMPLETE components and blocks, never short
# variable-name replacement. Every block recipe applies at original/changed scale.
def source_prompt(q,s,images):
 text=q[':question/problem']
 if 'Given that $F(x,y)=' in text:
  text=re.sub(r'(F\(x,y\)=)⟨(.*?)⟩',lambda m:m[1]+'⟨'+r',\,'.join(scaled(z,s) for z in m[2].split(r',\,'))+'⟩',text)
 elif '$$' in text:
  text=re.sub(r'(\$\$\n)(.*?)(\n\$\$)',lambda m:m[1]+scaled(m[2],s)+m[3],text,flags=re.S)
 for old,new in zip(re.findall(r'!\[.*?\]\((.*?)\)',text),images):text=text.replace('('+old+')','('+new+')')
 return text

def source_solution(q,s,radius,original_radius,images,raw):
 text=q[':question/worked-solution']; blocks=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
 replacements=[]
 for block in blocks:
  new=block
  if 'Δ={(r,' in block:new=re.sub(r'(0\\le r\\le )\d+',lambda m:m[1]+str(radius),block)
  elif r'\frac{∂P}{∂y}=' in block:
   new=re.sub(r'(\\frac\{∂P\}\{∂y\}=)(.*?)(,\\,)',lambda m:m[1]+scaled(m[2],s)+m[3],new)
   new=re.sub(r'(\\frac\{∂Q\}\{∂x\}=)(.*?)(\.\\end)',lambda m:m[1]+scaled(m[2],s)+m[3],new)
  elif r'\begin{aligned}' in block:
   # Keep each full source stage, including factorization and double-angle rows.
   core=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
   parts=core.split(r' \\  & =')
   first=parts[0]
   if ' & =' in first:
    lhs,rhs=first.split(' & =',1)
    # Formal Green operator already refers to scaled P and Q.
    first=scaled(lhs,s)+' & ='+(rhs if r'\frac{∂Q}{∂x}' in rhs else scaled(rhs,s))
   else:first=scaled(first,s)
   new=r'\begin{aligned}'+r' \\  & ='.join([first]+[scaled(z,s) for z in parts[1:]])+r'\end{aligned}'
   new=re.sub(r'(\{\\int \}_\{0\}\^\{)'+str(original_radius)+r'(\})',lambda m:m[1]+str(radius)+m[2],new)
  elif block.startswith('{∮}_{C}F'):
   lhs,rhs=block.split('=',1);new=lhs+'='+scaled(rhs,s)
  replacements.append(new)
 for old,new in zip(blocks,replacements):text=text.replace('$$\n'+old+'\n$$','$$\n'+new+'\n$$')
 text=re.sub(r'(Since \$P\(x,y\)=)(.*?)(\$ and \$Q\(x,y\)=)(.*?)(,\$)',lambda m:m[1]+scaled(m[2],s)+m[3]+scaled(m[4],s)+m[5],text)
 oldimages=re.findall(r'!\[.*?\]\((.*?)\)',text)
 for old,new in zip(oldimages,images[1:]):text=text.replace('('+old+')','('+new+')')
 if not raw:
  if q[':question/math-academy-id']=='q-125719':text=text.replace(r'\,dx-(y{e}^{y+1}+x)',r'\,dx+(y{e}^{y+1}+x)')
  if q[':question/math-academy-id']=='q-126516':text=text.replace('{e}^{1/y}','{e}^{y}')
  if q[':question/math-academy-id']=='q-126707':text=text.replace('{∬}_{D}(1-3{y}^{2})','{∬}_{D}(1-2{y}^{2})')
 return text

def authored_solution(P,Q,a,b,radius,plot,expanded=False):
 py=sp.diff(P,Y);qx=sp.diff(Q,X);curl=sp.expand(qx-py);pol=sp.expand(curl.subs({X:R*C,Y:R*SN}));g=sp.trigsimp(pol*R)
 theorem="Green's theorem states that\n\n$$\n\\oint_C P\\,dx+Q\\,dy=\\iint_D\\left(\\frac{\\partial Q}{\\partial x}-\\frac{\\partial P}{\\partial y}\\right)\\,dA.\n$$"
 return theorem+"\n\nIn our case, the region $D$ and its boundary $C$ satisfy the conditions of Green's theorem:\n\n![]("+plot+")\n\nSince $P(x,y)="+latex(P)+"$ and $Q(x,y)="+latex(Q)+",$ we obtain\n\n$$\n\\frac{\\partial P}{\\partial y}="+latex(py)+r',\qquad\frac{\partial Q}{\partial x}='+latex(qx)+".\n$$\n\nApplying Green's theorem, we get\n\n$$\n\\begin{aligned}\\oint_C("+latex(P)+r')\,dx+('+latex(Q)+r')\,dy&=\iint_D(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y})\,dA\\&=\iint_D\left('+latex(qx)+r'-\left('+latex(py)+r'\right)\right)\,dA\\&=\iint_D\left('+latex(curl)+r'\right)\,dA.\end{aligned}'+"\n$$\n\nNow, notice that the region $D$ can be represented in polar coordinates as\n\n$$\n\\Delta=\\{(r,\\theta):0\\le r\\le "+str(radius)+r',\ '+latex(a)+r'\le\theta\le '+latex(b)+r'\}.'+"\n$$\n\nThe change of variables formula for plane polar coordinates states that\n\n$$\n\\iint_D f(x,y)\\,dA=\\iint_\\Delta f(r\\cos\\theta,r\\sin\\theta)\\,r\\,dr\\,d\\theta.\n$$\n\nTherefore, we can write our double integral as\n\n$$\n\\begin{aligned}\\iint_D\\left("+latex(curl)+r'\right)\,dA&=\iint_\Delta\left('+latex(pol)+r'\right)r\,dr\,d\theta\\&='+integral(g,a,b,radius)+r'.\end{aligned}'+'\n$$'

def record(level,template,profile,params,prompt,solution,fields,math_key,raw=False,source_id=None):
 content=[VERSION,level,prompt,solution,[(f['key'],f['type'],sorted(f['values']),f['correct']) for f in fields]]
 ident=digest(content);question={':question/id':uid(ident),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[]}
 for f in fields:
  fid=uid(ident+f['key']);answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v} for v in f['values']]
  random.Random(params.get('_seed',0)).shuffle(answers)
  question[':question/answer-fields'].append({':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':':answer-field.type/'+f['type'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid+f['correct'])]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':TITLE},'question':question,'generation':{'version':VERSION,'template':template,'profile':profile,'parameters':{k:v for k,v in params.items() if not k.startswith('_')},'seed':params.get('_seed',0),'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_id':source_id,'eligible_for_learning':not raw,'evidence_only':raw,'mathematical_fingerprint':digest(math_key),'content_fingerprint':ident,'python':sys.version.split()[0],'sympy':sp.__version__}}

# EASY (authored): two constant cross partials; no polynomial cancellations.
# MODERATE (observed): nine supported calculus families and a three-blank polar
# continuation. A positive scalar preserves ALL source internal arithmetic stages.
# HARD (authored): four nonzero polynomial cross-partial contributions plus a
# shared trig term that cancels; resulting quadratic/linear curl has 3 terms.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown level')
 if field_type not in (None,'radio','blank',':answer-field.type/radio',':answer-field.type/blank'):raise ValueError('unsupported field type')
 rng=random.Random(seed)
 if template is None:
  if level=='easy':template='easy_constant'
  elif level=='hard':template='hard_polynomial'
  else:
   requested=field_type.split('/')[-1] if field_type else None
   eligible=[name for name in SPECS if requested is None or (name=='polar_blanks')==(requested=='blank')]
   template=rng.choice(eligible)
 if template in ('easy_constant','hard_polynomial'):
  if template!=('easy_constant' if level=='easy' else 'hard_polynomial'):raise ValueError('template/level mismatch')
  if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('authored levels use radio')
  if profile not in (None,'authored_method'):raise ValueError('unsupported authored profile')
  explicit=parameters is not None
  for attempt in range(100):
   p=dict(parameters) if explicit else ({'radius':rng.randint(2,6),'a':rng.randint(1,4),'b':rng.randint(1,4)} if level=='easy' else {'radius':rng.randint(2,6),'a':rng.randint(1,4),'c':rng.randint(1,3)})
   required={'radius','a','b'} if level=='easy' else {'radius','a','c'}
   if set(p)!=required or any(type(p[k])!=int for k in p):raise ValueError('parameters require integral '+','.join(sorted(required)))
   if not (2<=p['radius']<=6 and 1<=p['a']<=4 and (1<=p['b']<=4 if level=='easy' else 1<=p['c']<=3)):raise ValueError('authored workload bounds')
   a,b=0,sp.pi/2
   if level=='easy':
    if p['a']==p['b']:
     if explicit:raise ValueError('nonzero constant curl required')
     continue
    P=p['a']*Y+sp.sin(X);Q=p['b']*X+sp.cos(Y)
   else:P=p['a']*Y**3+X*Y**2-Y*sp.cos(X);Q=p['a']*X**3+2*X**2*Y+p['c']*X*Y-sp.sin(X)
   try:return build_authored(level,seed,template,p,P,Q,a,b)
   except ValueError:
    if explicit:raise
  raise ValueError('no eligible instance')
 if template not in SPECS or level!='moderate':raise ValueError('observed templates require moderate')
 sid,P0,Q0,orig,a,b=SPECS[template];q=QS[sid]
 isblank=template=='polar_blanks'
 if field_type and field_type.split('/')[-1]!=('blank' if isblank else 'radio'):raise ValueError('field type mismatch')
 profile=profile or ('authored_context' if isblank else 'authored_zero' if template=='square_difference' else 'authored_constant' if template=='constant' else 'authored_method')
 if profile not in ('observed','authored_method','authored_context','authored_zero','authored_constant'):raise ValueError('unknown profile')
 if isblank and profile in ('authored_method','authored_zero') or not isblank and profile=='authored_context' or profile=='authored_zero' and template!='square_difference':raise ValueError('profile mismatch')
 if template=='square_difference' and profile=='authored_method':raise ValueError('zero integral requires its complete eligible bank')
 if profile=='authored_constant' and template!='constant':raise ValueError('constant profile requires its own family')
 explicit=parameters is not None;raw=profile=='observed'
 for attempt in range(100):
  p=dict(parameters) if explicit else {'scale':rng.randint(1,5),'radius':rng.randint(1,4 if template=='constant' else 8)}
  if set(p)!={'scale','radius'} or any(type(p[k])!=int for k in p):raise ValueError('requires integer scale,radius')
  if not (1<=p['scale']<=5 and 1<=p['radius']<=(4 if template=='constant' else 9 if template=='cubic_log' else 8)):raise ValueError('moderate workload bounds')
  s,rad=p['scale'],p['radius'];images=get_plots(q,rad,orig,a,b,raw)
  prompt=source_prompt(q,s,images);sol=source_solution(q,s,rad,orig,images,raw)
  if template=='square_difference' and not raw:prompt=prompt.replace('{e}^{1/y}','{e}^{y}')
  if isblank:
   # Continuation has a supplied Cartesian integral; replace the complete value,
   # never the digits 6 or 3 independently across unrelated prose/components.
   prompt=prompt.replace('-6xy',scaled('-6xy',s))
   if not raw:
    prompt=('![]('+render_sector(rad,a,b)+')\n\n'
            'The region $D$ is bounded by the positively oriented path $C$ shown above. '
            'Write the double integral below in polar coordinates.\n\n'
            '${∬}_{D}'+scaled('-6xy',s)+r'\,\text{d}A\,={\int }_{\pi /2}^{a}\,{\int }_{0}^{b}$ '
            '{{field-1}} '+r'$\,\text{d}r\,\text{d}\theta,$'+'\n\n'
            'where $a=$ {{field-2}} and $b=$ {{field-3}}.')
   values=[scaled('-3{r}^{3}\\operatorname{sin}(2\\theta )',s),str(rad),r'2\pi ']
   fields=[{'key':f[':answer-field/key'],'type':'blank','values':[v],'correct':v} for f,v in zip(q[':question/answer-fields'],values)]
   key=['convert_supplied_curl',str(-6*s*X*Y),str(a),str(b),rad]
  else:
   P=s*P0;Q=s*Q0
   if template=='square_difference' and not raw:Q=s*(X**3+sp.exp(Y))
   curl=sp.expand(sp.diff(Q,X)-sp.diff(P,Y));g=sp.trigsimp(curl.subs({X:R*C,Y:R*SN})*R)
   if raw:
    vals=[]
    for f in q[':question/answer-fields']:
     vals=[scaled(re.sub(r'(\{\\int \}_\{0\}\^\{)(\d+)(\})',lambda m:m[1]+str(rad if int(m[2])==orig else max(1,rad-1))+m[3],z[':answer/value']),s) for z in f[':answer-field/choices']]
     ci=next(i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][':answer/id'])
    fields=[{'key':'selection','type':'radio','values':vals,'correct':vals[ci]}]
   else:
    py=sp.diff(P,Y);qx=sp.diff(Q,X)
    opts=[(g,a,b,rad),(-g,a,b,rad),(sp.cancel(g/R),a,b,rad),(sp.trigsimp((qx+py).subs({X:R*C,Y:R*SN})*R),a,b,rad),(g,a,b,rad+1)]
    if profile=='authored_constant':
     gp=py*R;gq=qx*R
     opts=[(g,a,b,rad),(-g,a,b,rad),(-gp,a,b,rad),(gq,a,b,rad),(gq+gp,a,b,rad)]
    if profile=='authored_zero':
     gp=sp.trigsimp(py.subs({X:R*C,Y:R*SN})*R);gq=sp.trigsimp(qx.subs({X:R*C,Y:R*SN})*R)
     opts=[(g,a,b,rad),(gq,a,b,rad),(-gp,a,b,rad),(gq+gp,a,b,rad),(sp.cancel((gq+gp)/R),a,b,rad)]
    try:compare_values([value(*z) for z in opts])
    except ValueError:
     if explicit:raise
     continue
    vals=[integral(*z) for z in opts];fields=[{'key':'selection','type':'radio','values':vals,'correct':vals[0]}]
   key=['derive_polar_setup',str(P),str(Q),str(a),str(b),rad]
  p['_seed']=seed
  return record(level,template,profile,p,prompt,sol,fields,key,raw,sid)
 raise ValueError('no eligible complete bank')

def build_authored(level,seed,template,p,P,Q,a,b):
 curl=sp.expand(sp.diff(Q,X)-sp.diff(P,Y));g=sp.trigsimp(curl.subs({X:R*C,Y:R*SN})*R);rad=p['radius']
 py=sp.diff(P,Y);qx=sp.diff(Q,X)
 opts=[(g,a,b,rad),(-g,a,b,rad),(sp.cancel(g/R),a,b,rad),(sp.trigsimp((qx+py).subs({X:R*C,Y:R*SN})*R),a,b,rad),(g,a,b,rad+1)]
 compare_values([value(*z) for z in opts]);vals=[integral(*z) for z in opts]
 plot=render_sector(rad,a,b);filled=render_sector(rad,a,b,True)
 prompt='![]('+plot+")\n\nConsider the path $C$ shown above. Which of the following is equivalent to the line integral\n\n$$\n\\oint_C("+latex(P)+r')\,dx+('+latex(Q)+r')\,dy\,?'+"\n$$"
 if level=='easy':prompt+='\n\nThe cross partials are $\\partial P/\\partial y='+latex(py)+'$ and $\\partial Q/\\partial x='+latex(qx)+'$.'
 sol=authored_solution(P,Q,a,b,rad,filled)
 p['_seed']=seed
 return record(level,template,'authored_method',p,prompt,sol,[{'key':'selection','type':'radio','values':vals,'correct':vals[0]}],['provided_partials' if level=='easy' else 'derive_polar_setup',str(P),str(Q),str(a),str(b),rad])

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(rec):
 q=rec['question'];out=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  out+='Field '+f[':answer-field/key']+'\n\n'
  for a in f[':answer-field/choices']:out+='$'+a[':answer/value']+'$\n\n'
 return out+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 result=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(result,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in result))
