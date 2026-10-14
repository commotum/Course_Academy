#!/usr/bin/env python3
"""Domain of a planar vector field, captured math basis 1356.

Observed moderate sections retain component-domain/intersection stages. Hard
sections retain the graphical bank layouts and all three solution diagrams.
Easy is an authored single-restricted-component reduction, grounded in the
canonical example and the prerequisite multivariable-domain lesson.

Historical profiles observed:q-ID are PUBLIC EVIDENCE ONLY, even when a bank
has an opaque error interpretation. They are parameterized masks/geometry
recipes, not literal question samplers. Normal defaults choose every supported
family and a complete method-derived bank before sampling. No DB writes.

CLI: .venv/bin/python generate/scratch/17592186172086.py --difficulty all
QA: .venv/bin/python generate/scratch/17592186172086/validate.py
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, random, re, sys, tempfile, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186172086
TITLE='Finding the Domain of a Vector Field'
KP_UUID='67b7ea90-38e0-54b5-b76e-816beb0d48f9'
VERSION='vector-field-domain-4'
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
x,y=sp.symbols('x y',real=True)
TEMPLATES={
 'sqrt_axis':('easy',None), 'log_axis':('easy',None), 'reciprocal_axis':('easy',None),
 'sum_difference':('moderate','q-122474'), 'log_halfplane':('moderate','q-122657'),
 'atan_circle_line':('moderate','q-122660'), 'log_parabola':('moderate','q-122663'),
 'open_disk_puncture':('hard','q-122518'), 'closed_disk_puncture':('hard','q-122671'),
 'rectangle':('hard','q-122710'), 'half_disk':('hard','q-122677'),
 'disk_line':('hard','q-122554')}
ANCHORS={'sum_difference':{'m':1,'n':1},'log_halfplane':{'m':1,'b':0},
 'atan_circle_line':{'r2':4,'c':1},'log_parabola':{'m':1,'b':0},
 'open_disk_puncture':{'r2':9},'closed_disk_puncture':{'r2':1},
 'rectangle':{'a':1,'b':1},'half_disk':{'r2':2,'m':1},'disk_line':{'r2':3,'m':1}}

def hash_obj(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+s))
def latex(e):return sp.latex(e).replace(r'\log',r'\ln')
def power(t):return '{'+t+'}^{2}'
def multi(k,t):return t if k==1 else ('-'+t if k==-1 else str(k)+t)
def shifted(t,b):return t if b==0 else t+('-'+str(b) if b>0 else '+'+str(-b))
def affine(m,b):
 t=multi(m,'y');return t if b==0 else t+'+'+str(b)
def settex(c):return r'{(x,y)\in {R}^{2}\,|\,'+c+'}'

def guards(template,p):
 if template.startswith(('sqrt_','log_axis','reciprocal_')):
  assert set(p)=={'axis','a'} and p['axis'] in ('x','y') and type(p['a']) is int and -6<=p['a']<=6
 else:
  assert set(p)==set(ANCHORS[template])
  assert all(type(v) is int for v in p.values())
  if 'r2' in p:assert 1<=p['r2']<=16
  if template=='sum_difference':assert 1<=p['m']<=6 and 1<=p['n']<=6 and math.gcd(p['m'],p['n'])==1
  if template=='log_halfplane':assert 1<=abs(p['m'])<=6 and 0<=p['b']<=6
  if template=='log_parabola':assert 1<=p['m']<=12 and 0<=p['b']<=6
  if template=='atan_circle_line':assert -3<=p['c']<=3 and p['c']**2<p['r2']
  if template=='rectangle':assert 1<=p['a']<=6 and 1<=p['b']<=6
  if template in ('half_disk','disk_line'):assert 1<=abs(p['m'])<=4

def sample(template,rng):
 if TEMPLATES[template][0]=='easy':return {'axis':rng.choice(['x','y']),'a':rng.randint(-6,6)}
 if template=='sum_difference':return rng.choice([{'m':m,'n':n} for m in range(1,7) for n in range(1,7) if math.gcd(m,n)==1])
 if template=='log_halfplane':return {'m':rng.choice([i for i in range(-6,7) if i]),'b':rng.randint(0,6)}
 if template=='log_parabola':return {'m':rng.randint(1,12),'b':rng.randint(0,6)}
 if template=='atan_circle_line':return rng.choice([{'r2':r,'c':c} for r in range(1,17) for c in range(-3,4) if c*c<r])
 if template=='rectangle':return {'a':rng.randint(1,6),'b':rng.randint(1,6)}
 p={'r2':rng.randint(1,16)}
 if template in ('half_disk','disk_line'):p['m']=rng.choice([i for i in range(-4,5) if i])
 return p

# Complete domains are conjunctions of elementary restrictions. Boundary
# inclusion/exclusion belongs to the object, including line-circle endpoints.
def model(template,p):
 rho=x*x+y*y
 if TEMPLATES[template][0]=='easy':
  z=x if p['axis']=='x' else y;u=z-p['a'];poly=y*y if p['axis']=='x' else x*x
  if template=='sqrt_axis':return sp.sqrt(u),poly,[sp.Ge(u,0)],[],[sp.Ge(u,0)]
  if template=='log_axis':return sp.log(u),poly,[sp.Gt(u,0)],[],[sp.Gt(u,0)]
  return sp.Pow(u,-1,evaluate=False),poly,[sp.Ne(u,0)],[],[sp.Ne(u,0)]
 if template=='sum_difference':
  m,n=p['m'],p['n'];return y/rho,sp.Mul(x,sp.Pow(n*n*x*x-m*m*y*y,-1,evaluate=False),evaluate=False),[sp.Ne(rho,0)],[sp.Ne(n*n*x*x-m*m*y*y,0)],[sp.Ne(n*n*x*x-m*m*y*y,0)]
 if template=='log_halfplane':
  u=x-p['m']*y-p['b'];return sp.log(u),1/rho,[sp.Gt(u,0)],[sp.Ne(rho,0)],[sp.Gt(u,0)]
 if template=='log_parabola':
  u=x-p['m']*y*y-p['b'];return sp.log(u),rho*sp.exp(1/x),[sp.Gt(u,0)],[sp.Ne(x,0)],[sp.Gt(u,0)]
 if template=='atan_circle_line':
  r,c=p['r2'],p['c'];return sp.atan(1/(rho-r)),sp.Mul(x*y,sp.Pow(x-c,-1,evaluate=False),evaluate=False),[sp.Ne(rho,r)],[sp.Ne(x,c)],[sp.Ne(rho,r),sp.Ne(x,c)]
 if template=='rectangle':
  a,b=p['a'],p['b'];d1=[sp.Gt(a*a-x*x,0)];d2=[sp.Ge(b-sp.Abs(y),0)]
  return y*sp.log(a*a-x*x),x*sp.sqrt(b-sp.Abs(y)),d1,d2,d1+d2
 r=p['r2'];closed=template in ('closed_disk_puncture','half_disk');disk=sp.Le(rho,r) if closed else sp.Lt(rho,r)
 if template=='half_disk':
  line=y-p['m']*x;return sp.Pow(sp.sqrt(line),-1,evaluate=False),sp.sqrt(r-rho),[sp.Gt(line,0)],[disk],[sp.Gt(line,0),disk]
 if template=='disk_line':
  return sp.Pow(sp.sqrt(r-rho),-1,evaluate=False),sp.Mul(rho,sp.Pow(p['m']*x-y,-1,evaluate=False),evaluate=False),[disk],[sp.Ne(y,p['m']*x)],[disk,sp.Ne(y,p['m']*x)]
 P=sp.sqrt(r-rho) if closed else sp.Pow(sp.sqrt(r-rho),-1,evaluate=False)
 Q=sp.exp(x)/rho if closed else x*y/rho
 return P,Q,[disk],[sp.Ne(rho,0)],[disk,sp.Ne(rho,0)]

def domain_tex(template,p):
 if TEMPLATES[template][0]=='easy':return p['axis']+{'sqrt_axis':r'\ge ','log_axis':'>','reciprocal_axis':r'\ne '}[template]+str(p['a'])
 if template=='sum_difference':
  k=sp.Rational(p['n'],p['m']);t='x' if k==1 else latex(k)+'x';return r'y\ne \pm '+t
 if template=='log_halfplane':return 'x>'+affine(p['m'],p['b'])
 if template=='log_parabola':return 'x>'+('' if p['m']==1 else str(p['m']))+power('y')+('' if p['b']==0 else '+'+str(p['b']))
 if template=='atan_circle_line':return power('x')+'+'+power('y')+r'\ne '+str(p['r2'])+r',\,x\ne '+str(p['c'])
 if template=='rectangle':return str(-p['a'])+'<x<'+str(p['a'])+r',\,'+str(-p['b'])+r'\le y\le '+str(p['b'])
 c=power('x')+'+'+power('y')+(r'\le ' if template in ('half_disk','closed_disk_puncture') else '<')+str(p['r2'])
 if template in ('open_disk_puncture','closed_disk_puncture'):return c+r',\,(x,y)\ne (0,0)'
 return c+(r',\,y>' if template=='half_disk' else r',\,y\ne ')+multi(p['m'],'x')

# Reusable source masks: replace ONLY complete components, constraints, radius
# phrases, and image slots. Each source family's operative rows remain intact.
def masks(template,p):
 if template=='sum_difference':
  m,n=p['m'],p['n'];den=(power('x') if n==1 else str(n*n)+power('x'))+'-'+(power('y') if m==1 else str(m*m)+power('y'))
  old=power('x')+'-'+power('y');ratio=sp.Rational(n,m);line='x' if ratio==1 else latex(ratio)+'x'
  return [(old,den),(r'y=\pm x',r'y=\pm '+line),(r'y\ne \pm x',r'y\ne \pm '+line),(r'y\ne x',r'y\ne '+line)]
 if template in ('log_halfplane','log_parabola'):
  m,b=p['m'],p['b'];old='x-y' if template=='log_halfplane' else 'x-'+power('y');yt='y' if template=='log_halfplane' else power('y');new='x-'+('' if m==1 else ('-' if m==-1 else str(m)))+yt
  if m<0:new='x+'+('' if m==-1 else str(-m))+yt
  if b:new+='-'+str(b)
  rhs=affine(m,b) if template=='log_halfplane' else ('' if m==1 else str(m))+yt+('' if b==0 else '+'+str(b))
  rel='y' if template=='log_halfplane' else power('y')
  return [(old,new),('x>'+rel,'x>'+rhs),('x<'+rel,'x<'+rhs),(r'x\ne '+rel,r'x\ne '+rhs),(r'x\ge '+rel,r'x\ge '+rhs)]
 if template=='atan_circle_line':
  r,c=p['r2'],p['c'];rr=power('x')+'+'+power('y');return [(rr+'-4',shifted(rr,r)),(rr+'=4',rr+'='+str(r)),(rr+r'\ne 4',rr+r'\ne '+str(r)),(rr+'<4',rr+'<'+str(r)),(rr+'>4',rr+'>'+str(r)),('x-1',shifted('x',c)),('x=1','x='+str(c)),(r'x\ne 1',r'x\ne '+str(c))]
 if template=='rectangle':
  a,b=p['a'],p['b'];return [('1-'+power('x'),str(a*a)+'-'+power('x')),('1-|y|',str(b)+'-|y|'),('-1<x<1',str(-a)+'<x<'+str(a)),(r'-1\le y\le 1',str(-b)+r'\le y\le '+str(b))]
 r=p['r2'];anchor=ANCHORS[template]['r2'];rr=power('x')+'+'+power('y')
 replacements=[(str(anchor)+'-'+power('x')+'-'+power('y'),str(r)+'-'+power('x')+'-'+power('y')),(rr+'<'+str(anchor),rr+'<'+str(r)),(rr+r'\le '+str(anchor),rr+r'\le '+str(r))]
 oldradius={1:'1',2:r'\sqrt{2}',3:r'\sqrt{3}',9:'3'}[anchor]
 replacements.append(('radius $'+oldradius+'$', 'radius $'+latex(sp.sqrt(r))+'$'))
 if template=='half_disk':
  m=p['m'];u='y-'+multi(m,'x') if m>0 else 'y+'+multi(-m,'x')
  replacements += [('y-x',u),('y>x','y>'+multi(m,'x'))]
 if template=='disk_line':
  m=p['m'];u=multi(m,'x')+'-y';replacements += [('x-y',u),('x=y','x=y' if m==1 else 'y='+multi(m,'x')),('$y=x$','$y='+multi(m,'x')+'$')]
 return replacements

def apply_masks(text,replacements):
 # simultaneous longest-first masks prevent substitution inside replacements.
 mapping=dict(replacements);keys=sorted(mapping,key=len,reverse=True)
 return re.sub('|'.join(re.escape(k) for k in keys),lambda m:mapping[m[0]],text) if keys else text

# Graph objects: r2 / disk closure / line or point removal / sided half-plane;
# rectangle closure is separate in x and y. Complete observed bank recipes.
def graph_banks(template,p,observed):
 r=p.get('r2');m=p.get('m',1)
 def disk(closed=False,puncture=False,line=None,side=None):return {'shape':'disk','r2':r,'closed':closed,'puncture':puncture,'line':line,'side':side}
 if template=='open_disk_puncture':
  bank=[disk(False,True,1),disk(False,True),disk(False,False,1),disk(True,True),disk(True)]
  if not observed:bank[0]=disk(False)
  return bank,1
 if template=='closed_disk_puncture':return [disk(False,False,1),disk(True),disk(False),disk(False,True),disk(True,True)],4
 if template=='disk_line':return [disk(False),disk(False,False,-m),disk(False,False,m),disk(True),disk(True,False,m)],2
 if template=='half_disk':return [disk(True,False,None,('ge',m)),disk(True,False,None,('gt',m)),disk(False,False,m),disk(True,False,None,('lt',m)),disk(True,False,m)],1
 a,b=p['a'],p['b']
 def rect(cx,cy,lower=None):return {'shape':'rectangle','a':a,'b':b,'cx':cx,'cy':cy,'lower':lower}
 upper=rect(False,False,0);upper['lower_closed']=True
 return [rect(True,True,0),upper,rect(True,True),rect(True,False),rect(False,True)],4

def graph_constraints(g):
 rho=x*x+y*y
 if g['shape']=='plane':return [sp.Ne(rho,0)] if g.get('puncture') else ([sp.Ne(y,g['line']*x)] if g.get('line') else [])
 if g['shape']=='halfplane':return [sp.Gt(y-g['m']*x,0)]
 if g['shape']=='strip_x':return [sp.Lt(x*x,g['a']**2)]
 if g['shape']=='strip_y':return [sp.Le(sp.Abs(y),g['b'])]
 if g['shape']=='rectangle':
  a,b=g['a'],g['b'];lo=-b if g.get('lower') is None else g['lower'];return [(sp.Le if g['cx'] else sp.Lt)(sp.Abs(x),a),(sp.Ge if g.get('lower_closed',g['cy']) else sp.Gt)(y,lo),(sp.Le if g['cy'] else sp.Lt)(y,b)]
 cs=[(sp.Le if g['closed'] else sp.Lt)(rho,g['r2'])]
 if g.get('puncture'):cs.append(sp.Ne(rho,0))
 if g.get('line'):cs.append(sp.Ne(y,g['line']*x))
 if g.get('side'):
  op,m=g['side'];cs.append({'ge':sp.Ge,'gt':sp.Gt,'lt':sp.Lt}[op](y,m*x))
 return cs

def render_graph(g):
 """Matplotlib raster, equal axes, exact derived geometry, atomic PNG+sidecar.

 Fresh calls use independent temp names. No shared input file or SVG output.
 """
 os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'mpl-cache'))
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 out=ROOT/'plots';out.mkdir(exist_ok=True)
 digest=hash_obj({'version':VERSION,'geometry':g});path=out/(digest+'.png');side=out/(digest+'.json')
 if path.exists() and side.exists():return str(path.relative_to(Path.cwd()))
 scale=math.sqrt(g['r2']) if g['shape']=='disk' else max(g.get('a',1),g.get('b',1),1)
 lim=max(2,scale*1.65);fig,ax=plt.subplots(figsize=(3.6,3.04),dpi=150)
 ax.set_aspect('equal');ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);blue='#287cc0'
 # Fill from actual geometric membership, not a sampled/rescaled picture.
 vv=np.linspace(-lim,lim,700);xx,yy=np.meshgrid(vv,vv)
 cs=graph_constraints(g);mask=np.ones_like(xx,dtype=bool)
 for c in cs:mask &= np.asarray(sp.lambdify((x,y),c,'numpy')(xx,yy),dtype=bool)
 ax.contourf(xx,yy,mask.astype(float),levels=[.5,1.5],colors=['#dceaf4'])
 if g['shape']=='disk':
  r=math.sqrt(g['r2']);theta=np.linspace(0,2*math.pi,1000)
  if g.get('side'):
   op,m=g['side'];start=math.atan(m);theta=np.linspace(start,start+math.pi,600) if op in ('gt','ge') else np.linspace(start+math.pi,start+2*math.pi,600)
  ax.plot(r*np.cos(theta),r*np.sin(theta),color=blue,ls='-' if g['closed'] else '--',lw=1.6)
  line=g.get('line') or (g['side'][1] if g.get('side') else None)
  if line:
   t=r/math.sqrt(1+line*line);included=g.get('side') and g['side'][0]=='ge';ax.plot([-t,t],[-line*t,line*t],color=blue,ls='-' if included else '--',lw=1.5)
   if g['closed'] and not included:ax.plot([-t,t],[-line*t,line*t],'o',mfc='white',mec=blue,ms=4,zorder=7)
  if g.get('puncture'):ax.plot(0,0,'o',mfc='white',mec=blue,ms=5,zorder=8)
  ax.set_xticks([]);ax.set_yticks([])
  for sign in [-1,1]:
   label='$'+('-' if sign<0 else '')+latex(sp.sqrt(g['r2']))+'$'
   ax.annotate(label,(sign*r,0),xytext=(sign*8,-5),textcoords='offset points',ha='right' if sign<0 else 'left',va='top',fontsize=9)
   ax.annotate(label,(0,sign*r),xytext=(-5,sign*8),textcoords='offset points',ha='right',va='bottom' if sign>0 else 'top',fontsize=9)
 elif g['shape']=='rectangle':
  a,b=g['a'],g['b'];lo=-b if g.get('lower') is None else g['lower']
  for v in [-a,a]:ax.plot([v,v],[lo,b],color=blue,ls='-' if g['cx'] else '--',lw=1.5)
  for v,included in [(lo,g.get('lower_closed',g['cy'])),(b,g['cy'])]:ax.plot([-a,a],[v,v],color=blue,ls='-' if included else '--',lw=1.5)
  if not(g['cx'] and g['cy']):ax.plot([-a,a,-a,a],[lo,lo,b,b],'o',mfc='white',mec=blue,ms=4,zorder=8)
  ax.set_xticks([-a,a]);ax.set_yticks([lo,b])
 elif g['shape']=='plane':
  if g.get('line'):ax.plot([-lim,lim],[-g['line']*lim,g['line']*lim],ls='--',color=blue)
  if g.get('puncture'):ax.plot(0,0,'o',mfc='white',mec=blue,ms=5,zorder=8)
  ax.set_xticks([]);ax.set_yticks([])
 elif g['shape']=='halfplane':ax.plot([-lim,lim],[-g['m']*lim,g['m']*lim],ls='--',color=blue);ax.set_xticks([]);ax.set_yticks([])
 elif g['shape']=='strip_x':
  for v in [-g['a'],g['a']]:ax.axvline(v,ls='--',color=blue)
  ax.set_xticks([-g['a'],g['a']]);ax.set_yticks([])
 elif g['shape']=='strip_y':
  for v in [-g['b'],g['b']]:ax.axhline(v,color=blue)
  ax.set_yticks([-g['b'],g['b']]);ax.set_xticks([])
 for spine in ['left','bottom']:ax.spines[spine].set_position('zero');ax.spines[spine].set_color('#444')
 ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
 ax.tick_params(length=0,labelsize=9,pad=5);ax.annotate('x',(lim,0),xytext=(-4,7),textcoords='offset points');ax.annotate('y',(0,lim),xytext=(7,-7),textcoords='offset points')
 ax.annotate('',(lim,0),(-lim,0),arrowprops={'arrowstyle':'->','color':'#444','lw':.7});ax.annotate('',(0,lim),(0,-lim),arrowprops={'arrowstyle':'->','color':'#444','lw':.7})
 fig.tight_layout(pad=.45);fig.canvas.draw();axes_bbox=list(ax.bbox.bounds)
 fd,tmp=tempfile.mkstemp(prefix=digest+'-',suffix='.png',dir=out);os.close(fd)
 try:fig.savefig(tmp,facecolor='white');os.replace(tmp,path)
 finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
 fd,tmp=tempfile.mkstemp(prefix=digest+'-',suffix='.json',dir=out);os.close(fd)
 Path(tmp).write_text(json.dumps({'geometry':g,'constraints':[str(c) for c in cs],'renderer':'Matplotlib','matplotlib':matplotlib.__version__,'python':sys.version.split()[0],'limits':[-lim,lim],'equal_aspect':True,'axes_bbox':axes_bbox,'png_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2));os.replace(tmp,side)
 return str(path.relative_to(Path.cwd()))

def source_asset(p):
 assert (Path('/media/jake/SSD/EDB/math')/p).exists();return p

def solution_graphs(template,p):
 bank,idx=graph_banks(template,p,False);correct=bank[idx]
 if template=='rectangle':return [{'shape':'strip_x','a':p['a']},{'shape':'strip_y','b':p['b']},correct]
 if template=='half_disk':return [{'shape':'halfplane','m':p['m']},{'shape':'disk','r2':p['r2'],'closed':True},correct]
 disk={'shape':'disk','r2':p['r2'],'closed':template=='closed_disk_puncture'}
 plane={'shape':'plane','line':p['m']} if template=='disk_line' else {'shape':'plane','puncture':True}
 return [disk,plane,correct]

# Moderate full-bank builders. Wrong operations relate to the assessed domain
# rules; opaque observed circle distractors stay only in their evidence profile.
def math_bank(template,p):
 correct=domain_tex(template,p);rho=power('x')+'+'+power('y')
 if TEMPLATES[template][0]=='easy':
  z,a=p['axis'],str(p['a']);op={'sqrt_axis':r'\ge ','log_axis':'>','reciprocal_axis':r'\ne '}[template]
  if template=='sqrt_axis':wrong=[z+'>'+a,z+'<'+a,z+r'\le '+a,z+r'\ne '+a]
  elif template=='log_axis':wrong=[z+r'\ge '+a,z+'<'+a,z+r'\le '+a,z+r'\ne '+a]
  else:wrong=[z+'>'+a,z+'<'+a,z+'='+a,r'\text{all real }(x,y)']
 elif template=='sum_difference':
  ratio=sp.Rational(p['n'],p['m']);k='x' if ratio==1 else latex(ratio)+'x';wrong=[r'(x,y)\ne (0,0)',r'y\ne '+k,r'y\ne -'+k,r'\text{all real }(x,y)']
 elif template=='log_halfplane':
  rhs=affine(p['m'],p['b']);wrong=['x<'+rhs,r'x\ne '+rhs,r'(x,y)\ne (0,0),\,x\ge '+rhs,r'(x,y)\ne (0,0)']
 elif template=='log_parabola':
  rhs=correct[2:];wrong=['x<'+rhs,'x>'+str(p['b']),r'x\ge '+rhs,correct+',\\,x>'+str(p['b']+1)]
 elif template=='atan_circle_line':
  r,c=str(p['r2']),str(p['c']);wrong=[rho+'<'+r+r',\,x\ne '+c,rho+r'\ne '+r,rho+'<'+r,rho+'>'+r]
 return [settex(c) for c in [correct]+wrong],0

def build_text(template,p,observed):
 level,sid=TEMPLATES[template]
 if level=='easy':
  z=p['axis'];v=shifted(z,p['a']);poly=power('y' if z=='x' else 'x')
  P={'sqrt_axis':r'\sqrt{'+v+'}','log_axis':r'\ln('+v+')','reciprocal_axis':r'\frac{1}{'+v+'}'}[template]
  prompt='Determine the domain of the vector field $F$ on ${R}^{2},$ given by\n\n$$\nF(x,y)='+P+r'\,i+'+poly+'\\,j\\,.\n$$'
  opening='The function $F$ can be expressed in terms of its components $P(x,y)$ and $Q(x,y)$ as\n\n$$\nF(x,y)=P(x,y)\\,i+Q(x,y)\\,j,\n$$\n\nwhere\n\n$$\nP(x,y)='+P+r',\,Q(x,y)='+poly+'.\n$$\n\nWe first find the domain of each component function. Then, we compute their intersection to find the domain of $F:$\n\n'
  rule={'sqrt_axis':'The function $P(x,y)$ is defined when the expression under the radical is positive or equal to zero. So, to find the domain, we solve the following inequality:', 'log_axis':'The function $P(x,y)$ is defined when the expression under the logarithm is positive. So, to find the domain, we solve the following inequality:', 'reciprocal_axis':'The function $P(x,y)$ is defined everywhere other than when the denominator vanishes. To find where the denominator vanishes, we set it equal to zero and solve:'}[template]
  op={'sqrt_axis':r'\ge 0','log_axis':'>0','reciprocal_axis':'=0'}[template]
  evaluated=z+'='+str(p['a']) if template=='reciprocal_axis' else domain_tex(template,p)
  sol=opening+'- '+rule+'\n\n$$\n'+v+op+r'\,⟹\,'+evaluated+'.\n$$\n\nTherefore, the domain of $P$ is given by\n\n$$\n{D}_{1}='+settex(domain_tex(template,p))+'.\n$$\n\n- The polynomial function $Q(x,y)$ is defined on the entire plane ${R}^{2}.$ Therefore, ${D}_{2}={R}^{2}.$\n\nFinally, the domain $D$ of $F$ is given by\n\n$$\nD={D}_{1}\\cap {D}_{2}='+settex(domain_tex(template,p))+'\\,.\n$$'
  return prompt,sol
 q=QUESTIONS[sid];prompt=apply_masks(q[':question/problem'],masks(template,p));sol=apply_masks(q[':question/worked-solution'],masks(template,p))
 if not observed:
  if template=='sum_difference':sol=sol.replace(r'Q(x,y)=\frac{y}',r'Q(x,y)=\frac{x}')
  if template=='log_parabola':sol=sol.replace('Therefore, the domain of $P$ is given by\n\n$$\n{D}_{2}', 'Therefore, the domain of $Q$ is given by\n\n$$\n{D}_{2}')
  if template=='rectangle':sol=sol.replace('is defined the expression','is defined when the expression')
  if template=='disk_line':sol=sol.replace('This defines the region ${D}_{1},$ which is the entire plane','This defines the region ${D}_{2},$ which is the entire plane')
  if template=='closed_disk_puncture':sol=sol.replace('which is the interior of a circle','which is the closed disk of radius').replace('of radius of radius','of radius')
 if level=='hard':
  oldimgs=re.findall(r'!\[\]\(([^)]+)\)',sol);geoms=solution_graphs(template,p)
  for old,g in zip(oldimgs,geoms):
   path=source_asset(old) if observed and p==ANCHORS[template] else render_graph(g)
   sol=sol.replace('![]('+old+')','![]('+path+')')
 return prompt,sol

def visible_sets(text):
 # Escape only complete outer set braces, preserving inner TeX groups.
 cursor=0
 while (match:=re.search(r'(?<!\\)\{\(x,y\)',text[cursor:])):
  start=cursor+match.start();end=start+1;depth=1
  while depth:
   if text[end]=='{':depth+=1
   elif text[end]=='}':depth-=1
   end+=1
  text=text[:start]+chr(92)+text[start:end-1]+chr(92)+text[end-1:];cursor=end+2
 return text

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed)
 if profile and profile.startswith('observed:'):
  sid=profile.split(':',1)[1];matching=[t for t,v in TEMPLATES.items() if v[1]==sid]
  if not matching:raise ValueError('Unknown observed profile')
  if template and template!=matching[0]:raise ValueError('Profile/template mismatch')
  template=matching[0]
 if profile and not profile.startswith('observed:') and profile!='method':raise ValueError('Unknown profile')
 allowed_types=(None,'radio',':answer-field.type/radio','answer-field.type/radio')
 if field_type not in allowed_types:raise ValueError('Only observed radio fields are supported')
 choices=[t for t,v in TEMPLATES.items() if v[0]==level]
 if not choices:raise ValueError('Unknown difficulty')
 template=template or rng.choice(choices)
 if template not in choices:raise ValueError('Template/difficulty mismatch')
 p=dict(parameters) if parameters is not None else sample(template,rng)
 try:guards(template,p)
 except (AssertionError,KeyError,TypeError):raise ValueError('Parameters violate the documented family workload bounds')
 observed=bool(profile and profile.startswith('observed:'));profile=profile or 'method'
 prompt,sol=build_text(template,p,observed);level,sid=TEMPLATES[template]
 geometry=[]
 if level=='hard':
  geometry,correct_index=graph_banks(template,p,observed)
  if observed and p==ANCHORS[template]:values=[source_asset(a[':answer/value']) for a in QUESTIONS[sid][':question/answer-fields'][0][':answer-field/choices']]
  else:values=[render_graph(g) for g in geometry]
  typ=':answer.type/image'
 elif observed:
  orig=QUESTIONS[sid][':question/answer-fields'][0];values=[apply_masks(a[':answer/value'],masks(template,p)) for a in orig[':answer-field/choices']]
  correct_index=next(i for i,a in enumerate(orig[':answer-field/choices']) if a[':answer/id']==orig[':answer-field/correct'][':answer/id']);typ=':answer.type/math'
 else:values,correct_index=math_bank(template,p);typ=':answer.type/math'
 if not observed:
  prompt,sol=visible_sets(prompt),visible_sets(sol);values=[visible_sets(v) for v in values]
 # Content identity has no seed/profile alias; domain task excludes the bank.
 identity=hash_obj({'version':VERSION,'difficulty':level,'problem':prompt,'solution':sol,'bank':sorted(values),'type':typ})
 qid=uid('question:'+identity);fid=uid('field:'+qid+':selection')
 answers=[{':answer/id':uid('answer:'+fid+':'+v),':answer/type':typ,':answer/value':v} for v in values]
 correct=answers[correct_index][':answer/id'];rng.shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 if observed:
  original_field=QUESTIONS[sid][':question/answer-fields'][0]
  q[':question/answer-fields'][0][':db/id']=original_field[':db/id']
  for answer in answers:
   original_index=values.index(answer[':answer/value'])
   answer[':db/id']=original_field[':answer-field/choices'][original_index][':db/id']
  # Preserve all captured question-attribute presence; original IDs are provenance.
  for key in (':db/id',':question/math-academy-id'):q[key]=QUESTIONS[sid][key]
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
   if key not in QUESTIONS[sid]:q.pop(key,None)
 P,Q,d1,d2,domain=model(template,p)
 task=hash_obj({'assessed':'domain','level':level,'components':[sp.srepr(P),sp.srepr(Q)],'domain':[sp.srepr(c) for c in domain]})
 rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':p,'source_id':sid,'provenance':{k:SOURCE[k] for k in ['database','basis','lineage']},'evidence_only':observed,'eligible_for_learning':not observed,'authored_level':level=='easy','mathematical_fingerprint':task,'content_identity':identity,'domain':[str(c) for c in domain],'geometry':geometry,'correct_geometry_index':correct_index if geometry else None,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'bank_interpretation':'explicit historical expression/geometry masks; intentions unresolved where documented' if observed else 'complete method-derived operation bank'}}
 # Normal validity is checked from displayed content, not only model metadata.
 if not observed:
  from importlib.util import spec_from_file_location,module_from_spec
  spec=spec_from_file_location('domain_validator',ROOT/'independent.py');mod=module_from_spec(spec);spec.loader.exec_module(mod);mod.check_record(rec)
 return rec

# Easy: authored one restricted component, polynomial second component;
# axis in x/y, integer offset -6..6, fixed one-rule/component/intersection work.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: two source-shaped component restrictions, symbolic intersection;
# primitive square coefficients 1..6; slope ±1..6/offset0..6; parabola1..12;
# circle squared radius1..16 and excluded vertical line -3..3.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: source-shaped raster region choice, strict/non-strict intersection and
# omitted point/line or mixed rectangle boundaries; r²1..16, slope±1..4,
# rectangle halfwidth/halfheight1..6. These are unordered equal-workload tasks.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def preview_path(path):
 p=Path(path)
 return str(p.resolve()) if p.exists() else str(Path('/media/jake/SSD/EDB/math')/path)
def markdown(r):
 q=r['question'];text=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  for i,a in enumerate(f[':answer-field/choices']):text+=str(i+1)+'. '+('![]('+preview_path(a[':answer/value'])+')' if a[':answer/type']==':answer.type/image' else '$'+a[':answer/value']+'$')+'\n'
 solution=re.sub(r'!\[\]\(([^)]+)\)',lambda m:'![]('+preview_path(m[1])+')',q.get(':question/worked-solution',''))
 return text+'\nWorked solution:\n\n'+solution+'\n'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty];rows=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(rows,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n'.join(markdown(r) for r in rows))
if __name__=='__main__':main()
