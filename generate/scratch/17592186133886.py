#!/usr/bin/env python3
"""Constant-curl Green's theorem over regions with holes, frozen math basis 1356.

Eight observed practice families are kept separate because their ordered area
arithmetic differs. Raw public profiles preserve historical omissions, duplicate
fields and two erroneous line-integral LHSs. Historical opaque scalar banks use
explicit proportional coefficient recipes for evidence only, never default
learning. Normal banks implement complete method errors and reject collisions.
Hard is authored: two holes, still constant curl times geometric area; no polar
integration or advanced polynomial-curl integration. See evidence folder.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR','/tmp/greens-holes-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, Wedge

KP_ID=17592186133886
KP_UUID='c67da0d8-518b-5fdb-b6ba-6c1c95c22d9b'
TITLE="Applying Green's Theorem to Regions With Holes"
VERSION='greens-holes-1'
DIR=Path(__file__).with_suffix('')
CAPTURE=json.loads((DIR/'source.json').read_text())
SOURCE=CAPTURE['record']
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
X,Y=sp.symbols('x y', real=True)
FORMAL=r'{∬}_{D}(\frac{∂Q}{∂x}-\frac{∂P}{∂y})\,\text{d}A'
INTRO=QUESTIONS['q-126853'][':question/worked-solution'].split('We have that')[0]
# Each observed family has its own operative solution sequence.
SPECS={
 'square_unrated':dict(source='q-126515',level='easy',shape='square',a=-1,b=1,W=4,H=4,s=2),
 'annulus_constant':dict(source='q-126578',level='moderate',shape='annulus',a=1,b=1,R=2,r=1,constant=True),
 'rectangle_square':dict(source='q-126853',level='easy',shape='rectangle',a=2,b=4,W=6,H=4,s=2),
 'annulus_negative':dict(source='q-126856',level='moderate',shape='annulus',a=3,b=2,R=3,r=1),
 'square_square':dict(source='q-126860',level='easy',shape='square',a=-5,b=8,W=8,H=8,s=6),
 'annulus_positive':dict(source='q-126894',level='moderate',shape='annulus',a=6,b=9,R=3,r=2),
 'circle_semicircle':dict(source='q-126891',level='moderate',shape='semicircle',a=5,b=11,R=4,r=2),
 'diamond_square':dict(source='q-126880',level='easy',shape='diamond',a=8,b=13,W=6,H=6,s=2),
 'circle_two_holes':dict(level='hard',shape='two_circles',a=3,b=7,R=7,r=1,t=2),
 'rectangle_two_holes':dict(level='hard',shape='two_squares',a=-3,b=5,W=14,H=8,s=2,t=4),
}

def parameters_for(template):
 return {k:v for k,v in SPECS[template].items() if k not in ('source','level','shape','constant')}

def canon(p):return dict(p)
def tex(v):return sp.latex(sp.sympify(v))
def scalar(v):return tex(sp.simplify(v)).replace(' \\pi',r'\pi').replace('- ','-')
def final(v):return scalar(v)+(' ' if sp.sympify(v).has(sp.pi) else '')+'.'
def term(c,var):
 if c==1:return var
 if c==-1:return '-'+var
 return str(c)+var

def field_parts(template,p):
 constant=SPECS[template].get('constant',False)
 return (str(p['a']) if constant else term(p['a'],'y'),term(p['b'],'x'),0 if constant else p['a'],p['b'])

def integrand(template,p,raw=False):
 P,Q,da,db=field_parts(template,p)
 if template in ('square_unrated','square_square'):
  if raw and template=='square_unrated':return Q+'dy - '+term(-p['a'],'y')+'dx'
  return Q+r'\,dy'+('+' if p['a']>=0 else '-')+term(abs(p['a']),'y')+r'\,dx'
 qterm=('+'+Q if not Q.startswith('-') else Q)+r'\,dy'
 return (('' if P=='1' else P)+r'dx'+qterm) if SPECS[template].get('constant') else P+r'\,dx'+qterm

def areas(template,p):
 shape=SPECS[template]['shape']
 if shape in ('annulus','semicircle','two_circles'):
  outer=sp.pi*p['R']**2
  holes=[sp.pi*p['r']**2/(2 if shape=='semicircle' else 1)]
  if shape=='two_circles':holes.append(sp.pi*p['t']**2)
 else:
  outer=sp.Rational(p['W']*p['H'],2 if shape=='diamond' else 1)
  holes=[sp.Integer(p['s']**2)]
  if shape=='two_squares':holes.append(sp.Integer(p['t']**2))
 return outer,holes,outer-sum(holes)

def validate_parameters(level,template,p,raw=False):
 expected=set(parameters_for(template))
 if set(p)!=expected:raise ValueError(f'Expected parameters {sorted(expected)}')
 if any(type(v)!=int for v in p.values()):raise ValueError('Integer parameters required')
 if not raw and level!=SPECS[template]['level']:raise ValueError('Template difficulty mismatch')
 if not 1<=abs(p['a'])<=13 or not 1<=abs(p['b'])<=13:raise ValueError('Coefficient bounds 1..13 in magnitude')
 shape=SPECS[template]['shape']
 if shape in ('annulus','semicircle'):
  if not 1<=p['r']<p['R']<=7:raise ValueError('Nested radii 1..7')
 elif shape=='two_circles':
  if not (1<=p['r']<=3 and 1<=p['t']<=3 and p['r']!=p['t'] and 2*(p['r']+p['t'])<p['R']*2-1 and p['R']<=10 and p['R']>2*max(p['r'],p['t'])):raise ValueError('Two strictly contained disjoint unequal holes')
 else:
  if not (2<=p['s']<min(p['W'],p['H'])<=16 and all(p[k]%2==0 for k in ('W','H','s'))):raise ValueError('Even geometric lengths 2..16')
  if shape=='square' and p['W']!=p['H']:raise ValueError('Square sides equal')
  if shape=='diamond' and (p['W']!=p['H'] or p['s']*2>=p['W']):raise ValueError('Square strictly within diamond')
  if shape=='two_squares' and not (2<=p['t']<=6 and p['t']%2==0 and p['s']!=p['t'] and p['s']+p['t']+2<p['W'] and max(p['s'],p['t'])+2<p['H'] and 2*max(p['s'],p['t'])<p['W']):raise ValueError('Two disjoint contained unequal square holes')
 if areas(template,p)[2]<=0:raise ValueError('Positive remaining area')
 k=field_parts(template,p)[3]-field_parts(template,p)[2]
 if k==0:raise ValueError('Nonzero curl')
 if not raw and template=='annulus_negative' and k>=0:raise ValueError('Negative curl family')
 if not raw and template in ('annulus_positive','circle_semicircle') and k<=0:raise ValueError('Positive curl family')

# Matplotlib-only renderer, immutable hash-addressed files and atomic sidecars.
def render_plot(template,p):
 shape=SPECS[template]['shape'];geometry={k:v for k,v in p.items() if k not in ('a','b')}
 digest=hashlib.sha256(json.dumps([shape,geometry],sort_keys=True).encode()).hexdigest()[:20]
 folder=DIR/'plots';folder.mkdir(exist_ok=True)
 target=folder/(digest+'.png');side=target.with_suffix('.json')
 if target.exists() and side.exists():return str(target.resolve())
 fig,ax=plt.subplots(figsize=(5,4.4),dpi=140);ax.set_aspect('equal');color='#d6e9f7';edge='#e99a00'
 boundaries=[];arrows=[]
 def curve(coords,orientation,role,patch):
  ax.add_patch(patch);boundaries.append(dict(role=role,orientation=orientation,points=coords))
 def arrow(a,b,role):
  ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',color=edge,lw=1.8));arrows.append(dict(tail=list(a),tip=list(b),role=role))
 if shape in ('annulus','semicircle','two_circles'):
  R=p['R'];curve(dict(center=[0,0],radius=R),'counterclockwise','outer',Circle((0,0),R,facecolor=color,edgecolor=edge,lw=1.5));arrow((R*.71,R*.71),(R*.62,R*.79),'outer')
  if shape=='two_circles':
   centers=[[-R/2,0],[R/2,0]];radii=[p['r'],p['t']]
  else:centers=[[0,0]];radii=[p['r']]
  for i,(c,r) in enumerate(zip(centers,radii)):
   if shape=='semicircle':
    curve(dict(center=c,radius=r,angle=[0,180],diameter=[[-r,0],[r,0]]),'clockwise','hole',Wedge(c,r,0,180,facecolor='white',edgecolor=edge,lw=1.5));arrow((-r*.6,r*.8),(-r*.48,r*.88),'hole')
    # Dashed lower semicircle is an auxiliary guide, not part of ∂D.
    theta=__import__('numpy').linspace(__import__('numpy').pi,2*__import__('numpy').pi,100);ax.plot(r*__import__('numpy').cos(theta),r*__import__('numpy').sin(theta),'--',color='#b5b5b5',lw=1)
   else:
    curve(dict(center=c,radius=r),'clockwise','hole',Circle(c,r,facecolor='white',edgecolor=edge,lw=1.5));arrow((c[0]+r*.62,r*.79),(c[0]+r*.71,r*.71),'hole')
   ax.text(c[0],-(r+.28),f'$r_{i+1}={r}$',ha='center',fontsize=10)
  ax.text(R*.55,-R*.65,f'$R={R}$',fontsize=10);limx=limy=R*1.22
 else:
  W,H=p['W'],p['H'];limx=W*.63;limy=H*.66
  if shape=='diamond':
   vertices=[[-W/2,0],[0,-H/2],[W/2,0],[0,H/2]];patch=Polygon(vertices,closed=True,facecolor=color,edgecolor=edge,lw=1.5)
  else:vertices=[[-W/2,-H/2],[W/2,-H/2],[W/2,H/2],[-W/2,H/2]];patch=Polygon(vertices,closed=True,facecolor=color,edgecolor=edge,lw=1.5)
  curve(dict(vertices=vertices),'counterclockwise','outer',patch)
  if shape=='diamond':arrow((W*.28,-H*.22),(W*.33,-H*.17),'outer')
  else:arrow((W*.2,-H/2),(W*.32,-H/2),'outer')
  centers=[[-W/4,0],[W/4,0]] if shape=='two_squares' else [[0,0]];sizes=[p['s'],p['t']] if shape=='two_squares' else [p['s']]
  for c,s in zip(centers,sizes):
   vertices=[[c[0]-s/2,-s/2],[c[0]+s/2,-s/2],[c[0]+s/2,s/2],[c[0]-s/2,s/2]]
   curve(dict(vertices=vertices),'clockwise','hole',Polygon(vertices,closed=True,facecolor='white',edgecolor=edge,lw=1.5));arrow((c[0]-s*.15,s/2),(c[0]+s*.15,s/2),'hole');ax.text(c[0],-s/2-.28,f'$s={s}$',ha='center',fontsize=10)
  ax.text(W*.34,H*.43,f'$W={W}$',fontsize=10);ax.text(-W*.55,H*.32,f'$H={H}$',fontsize=10)
 ax.axhline(0,color='#333333',lw=.7,zorder=0);ax.axvline(0,color='#333333',lw=.7,zorder=0)
 ax.set_xlim(-limx,limx);ax.set_ylim(-limy,limy);ax.text(-limx*.75,limy*.65,'$D$',color='#287cb7',fontsize=14)
 ax.set_xlabel('$x$');ax.set_ylabel('$y$',rotation=0);ax.tick_params(labelsize=9);ax.spines[['top','right']].set_visible(False);fig.tight_layout()
 with tempfile.NamedTemporaryFile(dir=folder,suffix='.png',delete=False) as f:tmp=Path(f.name)
 fig.savefig(tmp);transform=ax.transData.transform([[0,0],[1,0],[0,1]]).tolist();plt.close(fig);os.replace(tmp,target)
 data=dict(renderer='Matplotlib',version=matplotlib.__version__,python=sys.version.split()[0],shape=shape,geometry=geometry,boundaries=boundaries,arrows=arrows,axes_transform=transform,limits=[[-limx,limx],[-limy,limy]],png_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
 with tempfile.NamedTemporaryFile(dir=folder,suffix='.json',mode='w',delete=False) as f:json.dump(data,f,indent=2);tmp=Path(f.name)
 os.replace(tmp,side);return str(target.resolve())

def line(template,p,raw=False):return '{∮}_{∂D}'+integrand(template,p,raw)

def source_prefix(template,p):
 q=QUESTIONS[SPECS[template]['source']];old=parameters_for(template);P,Q,da,db=field_parts(template,p);P0,Q0,da0,db0=field_parts(template,old)
 prefix=q.get(':question/worked-solution','').split(r'\begin{aligned}')[0]
 if not prefix:return ''
 # Complete components, including function names and held-coordinate operators.
 prefix=prefix.replace('P(x,y)='+P0,'P(x,y)='+P).replace('Q(x,y)='+Q0,'Q(x,y)='+Q)
 prefix=prefix.replace(r'\frac{∂P}{∂y}='+str(da0)+r',\,\frac{∂Q}{∂x}='+str(db0),r'\frac{∂P}{∂y}='+str(da)+r',\,\frac{∂Q}{∂x}='+str(db))
 return prefix

def numeric_outer_holes(template,p):
 shape=SPECS[template]['shape']
 if shape in ('annulus','semicircle','two_circles'):
  out=r'\pi \cdot {'+str(p['R'])+r'}^{2}';hole=r'\pi \cdot {'+str(p['r'])+r'}^{2}'
  if shape=='semicircle':hole=r'\frac{'+hole+'}{2}'
  if shape=='two_circles':hole+=r'-\pi \cdot {'+str(p['t'])+r'}^{2}'
  return out,hole
 if shape=='diamond':out=r'\frac{'+str(p['W'])+r'\cdot '+str(p['H'])+'}{2}'
 elif shape=='square':out='{'+str(p['W'])+'}^{2}'
 else:out=str(p['W'])+r'\cdot '+str(p['H'])
 hole='{'+str(p['s'])+'}^{2}'
 if shape=='two_squares':hole+='-{'+str(p['t'])+'}^{2}'
 return out,hole

def rows(template,p,raw=False):
 P,Q,a,b=field_parts(template,p);k=b-a;O,holes,A=areas(template,p);C=k*A
 diff=str(b)+'-'+('('+str(a)+')' if a<0 else str(a))
 lhs=line(template,p,raw)
 # Two captured LHS copy/paste errors stay in raw evidence only.
 if raw and template in ('annulus_positive','circle_semicircle'):lhs=r'{∮}_{∂D}dx+x\,dy'
 out,hole=numeric_outer_holes(template,p)
 s=[lhs+' & ='+FORMAL,r'{∬}_{D}('+diff+r')\,\text{d}A']
 if template=='annulus_constant':
  coef='' if k==1 else str(k)
  factor='' if k==1 else str(k)+r'\cdot '
  s += [r'{∬}_{D}'+coef+r'\,\text{d}A',factor+r'\text{Area}(D)',out+'-'+hole if k==1 else factor+'('+out+'-'+hole+')',scalar(O)+' -'+scalar(holes[0])+' ' if k==1 else factor+'('+scalar(O)+' -'+scalar(holes[0])+' )',final(C)]
 elif template=='annulus_negative':
  factor='-' if k==-1 else str(k)+r'\cdot '
  s += [r'{∬}_{D}'+str(k)+r'\,\text{d}A',('-' if k==-1 else str(k))+r'{∬}_{D}\,\text{d}A',factor+r'\text{Area}(D)',factor+'('+out+'-'+hole+')',factor+'('+scalar(O)+' -'+scalar(holes[0])+' )',final(C)]
 else:
  s.append(r'{∬}_{D}'+str(k)+r'\,\text{d}A')
  if template not in ('annulus_positive','circle_semicircle'):
   gap=r'\,' if template=='diamond_square' else ''
   s.append(str(k)+gap+r'{∬}_{D}\,\text{d}A')
  s.append(str(k)+(r'\,' if template in ('annulus_positive','circle_semicircle') else r'\cdot ')+r'\text{Area}(D)')
  s.append(str(k)+r'\cdot ('+out+'-'+hole+')')
  if template in ('annulus_positive','circle_semicircle'):
   s.append(str(k)+r'\cdot '+scalar(A)+' ')
  else:
   s.append(str(k)+r'\cdot ('+scalar(O)+'-'+ '-'.join(scalar(h) for h in holes)+')')
   if template not in ('diamond_square',):s.append(str(k)+r'\cdot '+scalar(A))
  s.append(final(C))
 return s

def source_solution(template,p,raw=False):
 if template=='square_unrated' and raw:return None
 prefix=source_prefix(template,p) if 'source' in SPECS[template] and template!='square_unrated' else ''
 if not prefix:
  P,Q,a,b=field_parts(template,p)
  prefix=INTRO+f'We have that $P(x,y)={P}$ and $Q(x,y)={Q}.$ So,\n\n$$\n'+r'\frac{∂P}{∂y}='+str(a)+r',\,\frac{∂Q}{∂x}='+str(b)+'.\n$$\n\nTherefore, applying Green\'s theorem, we get\n\n$$\n'
 return prefix+r'\begin{aligned}'+r' \\  & ='.join(rows(template,p,raw))+r'\end{aligned}'+'\n$$'

# Complete authored banks are chosen before parameter sampling, never pooled.
def bank(template,p,profile):
 _,_,a,b=field_parts(template,p);k=b-a;O,holes,A=areas(template,p)
 if profile=='constant_operations':return [('correct',k*A),('reverse_orientation',-k*A),('ignore_hole',k*O),('integrate_hole_only',k*sum(holes)),('add_hole',k*(O+sum(holes)))]
 if profile=='semicircle_operations':return [('correct',k*A),('reverse_orientation',-k*A),('ignore_hole',k*O),('use_full_circle_hole',k*(O-2*holes[0])),('add_hole',k*(O+holes[0]))]
 if profile=='two_hole_operations':return [('correct',k*A),('reverse_orientation',-k*A),('ignore_second_hole',k*(O-holes[0])),('ignore_first_hole',k*(O-holes[1])),('add_holes',k*(O+sum(holes)))]
 if profile!='linear_operations':raise ValueError('Unknown complete bank profile')
 return [('correct',k*A),('reverse_orientation',-k*A),('ignore_hole',k*O),('add_hole',k*(O+sum(holes))),('omit_P_partial',b*A)]

def eligible_profile(template):
 if template=='annulus_constant':return 'constant_operations'
 if template=='circle_semicircle':return 'semicircle_operations'
 if SPECS[template]['level']=='hard':return 'two_hole_operations'
 return 'linear_operations'

def sample(template,rng):
 p=parameters_for(template);shape=SPECS[template]['shape'];p['a']=rng.choice([i for i in range(-13,14) if i]);p['b']=rng.choice([i for i in range(-13,14) if i])
 if shape in ('annulus','semicircle'):
  p['R']=rng.randint(2,7);p['r']=rng.randint(1,p['R']-1)
 elif shape=='two_circles':
  p['R']=rng.randint(6,10);p['r'],p['t']=rng.sample([1,2,3],2)
 elif shape=='two_squares':
  p['W']=rng.choice([12,14,16]);p['H']=rng.choice([8,10,12]);p['s'],p['t']=rng.sample([2,4,6],2)
 elif shape=='diamond':
  p['W']=p['H']=rng.choice([6,8,10,12,14,16]);p['s']=rng.choice([s for s in [2,4,6] if 2*s<p['W']])
 else:
  p['W']=rng.choice([4,6,8,10,12,14,16]);p['H']=p['W'] if shape=='square' else rng.choice([4,6,8,10,12,14,16]);p['s']=rng.choice([s for s in [2,4,6,8,10,12,14] if s<min(p['W'],p['H'])])
 return p

def historical_values(template,p):
 q=QUESTIONS[SPECS[template]['source']];old=parameters_for(template)
 _,_,a,b=field_parts(template,p);_,_,a0,b0=field_parts(template,old)
 # Explicit opaque bank extension: dimensional rescaling of its complete scalar
 # coefficients, with NO inferred distractor intent and NO learning eligibility.
 ratio=sp.cancel((b-a)*areas(template,p)[2]/((b0-a0)*areas(template,old)[2]))
 allfields=[]
 for f in q[':question/answer-fields']:
  values=[]
  for ans in f[':answer-field/choices']:
   oldv=ans[':answer/value'];v=sp.sympify(oldv.replace('\\pi','*pi').replace('π','*pi').strip())*ratio
   if ratio==1:rendered=scalar(v).replace('\\pi', 'π') if 'π' in oldv else scalar(v)+( ' ' if oldv.endswith(' ') else '')
   else:rendered=scalar(v)
   values.append((ans[':answer/id'],rendered))
  allfields.append(values)
 return allfields

def identity(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio fields')
 rng=random.Random(seed)
 if template is None:
  if parameters is not None:raise ValueError('Explicit parameters require a template')
  template=rng.choice([t for t,s in SPECS.items() if s['level']==level])
 if template not in SPECS:raise ValueError('Unknown template')
 raw=profile=='observed_raw';profile=profile or eligible_profile(template)
 if raw and 'source' not in SPECS[template]:raise ValueError('No observed raw profile')
 if not raw and profile!=eligible_profile(template):raise ValueError('Profile not eligible for this family')
 explicit=parameters is not None
 for attempt in range(1000):
  p=canon(parameters) if explicit else sample(template,rng)
  try:
   validate_parameters(level,template,p,raw)
   if not raw:
    values=bank(template,p,profile)
    if len({sp.srepr(sp.simplify(v)) for _,v in values})!=5:raise ValueError('Whole bank collision')
   break
  except ValueError:
   if explicit:raise
 else:raise ValueError('No valid complete instance')
 spec=SPECS[template];sourceq=QUESTIONS[spec['source']] if 'source' in spec else None
 old=parameters_for(template);anchor=p==old
 plot=sourceq[':question/problem'].split(')')[0]+')' if raw and anchor else '![]('+render_plot(template,p)+')'
 # Prompt is source-shaped, including exact source punctuation in public raw replay.
 if template=='square_unrated' and raw:
  problem=plot+'\n\nCalculate $∮_(∂D)'+integrand(template,p,True)+'$, where $D$ is the region shown above.'
 else:
  problem=plot+'\n\nCalculate $'+line(template,p)+',$ where $D$ is the '+('annular region' if spec['shape'] in ('annulus','semicircle') else 'region')+' shown above.'
 if not raw:problem+='\n\nThe outer boundary is counterclockwise and each hole boundary is clockwise.'
 solution=source_solution(template,p,raw)
 content=dict(problem=problem,solution=solution,level=(sourceq.get(':question/difficulty',{}).get(':db/ident') if raw else level))
 if raw:
  vals=historical_values(template,p);content['banks']=[[v for _,v in f] for f in vals]
 else:content['banks']=[[scalar(v) for _,v in values]]
 content['banks']=[sorted(v) for v in content['banks']]
 cid=hashlib.sha256(json.dumps([VERSION,content],sort_keys=True).encode()).hexdigest()
 q={':question/id':identity(cid),':question/problem':problem}
 if not raw or ':question/difficulty' in sourceq:q[':question/difficulty']=':question.difficulty/'+(sourceq[':question/difficulty'][':db/ident'].split('/')[-1] if raw else level)
 if solution is not None:q[':question/worked-solution']=solution
 fields=[]
 if raw:
  for i,(f,vals) in enumerate(zip(sourceq[':question/answer-fields'],vals)):
   fid=identity(cid+f'/field/{i}');answers=[{':answer/id':identity(fid+'/'+oldid),':answer/type':':answer.type/math',':answer/value':v} for oldid,v in vals]
   out={':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
   if ':answer-field/correct' in f:
    oldid=f[':answer-field/correct'][':answer/id'];out[':answer-field/correct']=[':answer/id',identity(fid+'/'+oldid)]
   rng.shuffle(answers);fields.append(out)
 else:
  fid=identity(cid+'/field/selection');answers=[{':answer/id':identity(fid+'/'+r),':answer/type':':answer.type/math',':answer/value':scalar(v)} for r,v in values]
  correct=answers[0][':answer/id'];rng.shuffle(answers);fields=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]
 q[':question/answer-fields']=fields
 P,Q,da,db=field_parts(template,p);O,holes,A=areas(template,p)
 task=hashlib.sha256(json.dumps([spec['shape'],P,Q,{k:v for k,v in p.items() if k not in ('a','b')}],sort_keys=True).encode()).hexdigest()
 return {'knowledge_point':dict(db_id=KP_ID,id=KP_UUID,title=TITLE),'question':q,'generation':dict(version=VERSION,seed=seed,template=template,parameters=p,profile=profile,source=spec.get('source'),basis=1356,lineage=CAPTURE['lineage'],difficulty_design='observed' if level!='hard' else 'authored two-hole bookkeeping',eligible_for_learning=not raw,evidence_only=raw,mathematical_fingerprint=task,content_fingerprint=cid,operations=[r for r,_ in values] if not raw else 'opaque proportional historical coefficients; intent unresolved',outer_area=str(O),hole_areas=[str(h) for h in holes],area=str(A),curl=db-da,python=sys.version.split()[0],sympy=sp.__version__,matplotlib=matplotlib.__version__)}

# EASY: one polygon hole, constant partial derivatives, geometric subtraction.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: circular or semicircular hole; preserve exact π area arithmetic.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): two unequal holes; identical constant-curl method, two signed contributions.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];s=q[':question/problem']+'\n\n'
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  s+=f'Field {i+1}:\n'+ '\n'.join(f'- ${a[":answer/value"]}$' for a in f[':answer-field/choices'])+'\n\n'
 return s+q.get(':question/worked-solution','[No worked solution in raw capture.]')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+n,template=args.template,profile=args.profile) for l in levels for n in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
