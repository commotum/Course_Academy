#!/usr/bin/env python3
"""Seeded diagram-based polar conversion; runtime assets require explicit output dir."""
from __future__ import annotations
from functools import lru_cache
import argparse, copy, hashlib, json, math, os, random, re, sys, tempfile, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-polar-mpl')
import sympy as sp
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
from PIL import Image
from math_format import normalize_prose, normalize_tex, validate_generated_record
ROOT=Path(__file__).resolve().parent
SOURCE=json.loads((ROOT/'source_cases.json').read_text())
KP=17592186092273
VERSION='diagram-cartesian-v4'
def exact(v): return sp.sympify(v,locals={'sqrt':sp.sqrt})
def tex(v): return sp.latex(sp.simplify(v))
def angle(v,unit): return tex(sp.Rational(v,180)*sp.pi) if unit=='radian' else '{'+str(v)+r'}^{∘}'
@lru_cache(maxsize=4096)
def xy(r,b): return tuple(sp.simplify(r*f(sp.Rational(b,180)*sp.pi)) for f in (sp.cos,sp.sin))
def pair(t): return '('+','.join(tex(x) for x in t)+')'
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(v,sort_keys=True,ensure_ascii=False)))
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def latex_expr(v):
 # Small exact source coordinate grammar, including nested radical fractions.
 v=v.replace('π','pi').replace(r'\pi','pi').replace(' ', '')
 def group(t,i):
  if t[i]!='{':raise ValueError('Expected TeX group')
  depth=1;j=i+1
  while depth:
   if t[j]=='{':depth+=1
   elif t[j]=='}':depth-=1
   j+=1
  return t[i+1:j-1],j
 def decode(t):
  out='';i=0
  while i<len(t):
   if t.startswith(r'\frac',i):
    n,j=group(t,i+5);d,i=group(t,j);out+='(('+decode(n)+')/('+decode(d)+'))'
   elif t.startswith(r'\sqrt',i):
    rad,i=group(t,i+5);out+='sqrt('+decode(rad)+')'
   else:out+=t[i];i+=1
  return out
 v=decode(v)
 v=re.sub(r'(?<=[0-9)])(?=sqrt|pi|\()', '*',v)
 return sp.sympify(v)
def parse_pair(v): return tuple(latex_expr(x) for x in v.strip('()').split(','))
def render_plots(p,output_dir=None):
 out=Path(output_dir or os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']);out.mkdir(parents=True,exist_ok=True)
 geometry={'alpha':p['alpha'],'delta':p['delta'],'direction':p['direction'],'version':VERSION}
 name=digest(geometry);png=out/(name+'.png');side=out/(name+'.json')
 if png.exists() and side.exists():
  saved=json.loads(side.read_text())
  if 'saved_dpi' not in saved:
   saved['saved_dpi']=list(Image.open(png).info['dpi'])
   fd,st=tempfile.mkstemp(prefix=name+'-',suffix='.json',dir=out);os.close(fd);Path(st).write_text(json.dumps(saved,indent=2));os.replace(st,side)
  return str(png.resolve())
 fig=Figure(figsize=(4.4,4.0),dpi=160);FigureCanvasAgg(fig);ax=fig.add_axes([.04,.04,.92,.92]);ax.set(xlim=(-1.52,1.52),ylim=(-1.4,1.4));ax.set_aspect('equal');ax.axis('off')
 color='#2777bb';tau=np.linspace(0,2*math.pi,1600);circle=np.array([np.cos(tau),np.sin(tau)]).T
 ax.plot(circle[:,0],circle[:,1],color=color,lw=1.7)
 axes=[]
 for tail,tip in [((-1.42,0),(1.42,0)),((0,-1.30),(0,1.30))]:
  ax.annotate('',xy=tip,xytext=tail,arrowprops={'arrowstyle':'->','lw':1.5,'color':'black'});axes.append(np.linspace(tail,tip,1000))
 a=math.radians(p['alpha']);b=math.radians(p['alpha']+p['direction']*p['delta'])
 endpoints=np.array([[math.cos(a),math.sin(a)],[math.cos(b),math.sin(b)]])
 paths=[circle,*axes]
 for pt in endpoints:
  path=np.linspace((0,0),pt,500);paths.append(path);ax.plot(path[:,0],path[:,1],linestyle=(0,(1.4,2.0)),color=color,lw=1.4)
 ax.scatter(*endpoints.T,color=color,s=17,zorder=4);ax.scatter([0],[0],color=color,s=15,zorder=4)
 arc_t=np.linspace(a,b,500);arc=np.array([.30*np.cos(arc_t),.30*np.sin(arc_t)]).T;ax.plot(arc[:,0],arc[:,1],color=color,lw=1.5);paths.append(arc)
 texts=[]
 def label(t,x,y):texts.append(ax.text(x,y,t,fontsize=14,fontfamily='DejaVu Serif',fontstyle='italic',ha='center',va='center'))
 label('x',1.47,.09);label('y',.08,1.33);label('O',.14,-.14)
 for lab,pt,ang in zip(('A','B'),endpoints,(a,b)):
  # Whole labels are placed outside the circumference, away from axes.
  pos=1.17*pt
  if abs(pos[1])<.14:pos[1]+=.18
  if abs(pos[0])<.14:pos[0]+=.18
  label(lab,*pos)
 fig.canvas.draw();renderer=fig.canvas.get_renderer()
 pixelpaths=[ax.transData.transform(path) for path in paths];markers=ax.transData.transform(np.vstack((endpoints,[0,0])))
 def bbox_distance(bb,pts):
  x0,y0,x1,y1=bb;dx=np.maximum(np.maximum(x0-pts[:,0],pts[:,0]-x1),0);dy=np.maximum(np.maximum(y0-pts[:,1],pts[:,1]-y1),0);return float(np.min(np.hypot(dx,dy)))
 # O may not lie across an incident dashed radius. Select the full unmasked
 # text box with maximal measured clearance among positions near the origin.
 origin_text=texts[2];oldbox=origin_text.get_window_extent(renderer).extents;oldanchor=ax.transData.transform(origin_text.get_position());candidates=[]
 for theta in np.linspace(0,2*math.pi,32,endpoint=False):
  point=(.21*math.cos(theta),.21*math.sin(theta));shift=ax.transData.transform(point)-oldanchor;box=oldbox+np.tile(shift,2)
  score=min([bbox_distance(box,path) for path in pixelpaths]+[bbox_distance(box,markers)])
  candidates.append((score,point))
 origin_text.set_position(max(candidates,key=lambda v:v[0])[1]);fig.canvas.draw();renderer=fig.canvas.get_renderer();bbs=[t.get_window_extent(renderer).extents.tolist() for t in texts]
 trans=ax.transData.get_affine().get_matrix().tolist()
 clears=[{'label':t.get_text(),'curve_axis_clearance_px':min(bbox_distance(bb,path) for path in pixelpaths),'marker_clearance_px':bbox_distance(bb,markers)} for t,bb in zip(texts,bbs)]
 # Unique render temps plus atomic replace; no shared input or pruning.
 fd,tmp=tempfile.mkstemp(prefix=name+'-',suffix='.png',dir=out);os.close(fd)
 try:
  fig.savefig(tmp,dpi=160,facecolor='white');os.replace(tmp,png)
  metadata={'geometry':geometry,'dpi':160,'saved_dpi':list(Image.open(png).info['dpi']),'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'size_px':[704,640],'transform':trans,'text_bboxes':dict(zip([t.get_text() for t in texts],bbs)),'clearances':clears,'endpoints_data':endpoints.tolist(),'endpoints_px':markers[:2].tolist(),'origin_px':ax.transData.transform((0,0)).tolist(),'circle_data':[-1,1,-1,1],'sha256':hashlib.sha256(png.read_bytes()).hexdigest()}
  fd,st=tempfile.mkstemp(prefix=name+'-',suffix='.json',dir=out);os.close(fd);Path(st).write_text(json.dumps(metadata,indent=2));os.replace(st,side)
 finally:
  if Path(tmp).exists():Path(tmp).unlink()
 return str(png.resolve())

SPECIAL=(30,45,60,120,135,150,210,225,240,300,315,330)
PROFILES={'omit-double':('omit_radius','double'), 'half-double':('half','double'),
          'omit-half':('omit_radius','half'), 'double-square':('double','radius_squared')}
SOURCE_PARAMS=[('6',30,90,1,'radian'),('4',150,30,-1,'radian'),
 ('4*sqrt(2)',150,165,1,'degree'),('2',240,195,-1,'degree'),
 ('4',240,210,-1,'degree'),('10',60,60,1,'degree'),
 ('5',210,150,-1,'radian'),('10',60,180,1,'radian'),
 ('2*sqrt(2)',150,105,-1,'radian'),('6',330,30,-1,'radian'),
 ('5',180,60,1,'radian')]

def parameters(radius,alpha,delta,direction,units):
 return dict(radius=radius,alpha=alpha,delta=delta,direction=direction,units=units)

def angle(v,unit):
 return tex(sp.Rational(v,180)*sp.pi) if unit=='radian' else str(v)+r'^\circ'

def bank(p,profile,rng):
 """A whole authored bank: 3 familiar rays, 2 errors in radial scaling."""
 r=exact(p['radius']);b=p['alpha']+p['direction']*p['delta'];q=b//90
 rays=[90*q+t for t in (30,45,60)]
 recipes=['angle_'+str(t) for t in rays]
 values=[xy(r,t) for t in rays]
 factors={'omit_radius':1/r,'half':sp.Rational(1,2),'double':sp.Integer(2),'radius_squared':r}
 for error_index,recipe in enumerate(PROFILES[profile]):
  # Always retain a competing diagonal scale: shape alone must not bypass r.
  # This assignment is bank-wide, independent of which ray is the target.
  t=90*q+45 if error_index==0 else rng.choice(rays);values.append(xy(r*factors[recipe],t));recipes.append(recipe+'@'+str(t))
 if len(set(values))!=5:raise ValueError('Distinct complete bank required')
 assert values.count(xy(r,b))==1
 return values,recipes

def normalise_question(q):
 for k in (':question/problem',':question/worked-solution'):q[k]=normalize_prose(q[k])
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']:a[':answer/value']=normalize_tex(a[':answer/value'])
 return q

def own_record(q,meta):
 q=normalise_question(q)
 # Identities use normalized content and a logical asset name, not deployment path.
 identity=copy.deepcopy(q)
 identity[':question/problem']=re.sub(r'!\[\]\([^)]*?([^/()]+\.png)\)',r'![](\1)',identity[':question/problem'])
 for f in identity[':question/answer-fields']:
  f.pop(':answer-field/id',None)
  f[':answer-field/correct']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  for a in f[':answer-field/choices']:a.pop(':answer/id',None)
 content=digest(identity);qid=uid(content);q[':question/id']=qid
 for i,f in enumerate(q[':question/answer-fields']):
  correct=f[':answer-field/correct'][1];fid=uid([qid,i]);f[':answer-field/id']=fid
  for a in f[':answer-field/choices']:
   was=a[':answer/id'];a[':answer/id']=uid([fid,a[':answer/value']])
   if was==correct:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
 record={'knowledge_point':SOURCE['knowledge_point'],'question':q,'generation':dict(meta,version=VERSION,content_identity=content)}
 return validate_generated_record(record)

def make_field(key,kind,values,correct,rng):
 answers=[{':answer/id':str(i),':answer/type':':answer.type/math',':answer/value':v} for i,v in enumerate(values)]
 correct_id=str(values.index(correct));rng.shuffle(answers)
 return {':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,
 ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}

def derivation(p):
 r=exact(p['radius']);a=p['alpha'];d=p['delta'];s=p['direction'];u=p['units'];b=a+s*d
 result=xy(r,b);operation='+' if s==1 else '-';direction='counterclockwise' if s==1 else 'clockwise'
 # Preserve the actual operator input, with exact familiar-angle values.
 compose=angle(a,u)+operation+angle(d,u)
 if u=='radian':
  ar=sp.Rational(a,180);dr=sp.Rational(d,180);den=sp.ilcm(ar.q,dr.q)
  common=lambda z: r'\frac{'+str(z*den)+r'\pi}{'+str(den)+'}'
  if ar.q!=dr.q:compose+='='+common(ar)+operation+common(dr)
 compose+='='+angle(b,u)
 rows=[]
 for name,fn in [('x',sp.cos),('y',sp.sin)]:
  value=fn(sp.Rational(b,180)*sp.pi)
  rows.append(name+' &='+tex(r)+'\\'+('cos' if name=='x' else 'sin')+r'\left('+angle(b,u)+r'\right)='+tex(r)+r'\left('+tex(value)+r'\right)='+tex(result[0 if name=='x' else 1]))
 solution=(f'Both points lie on the same circle, so $B$ has radius ${tex(r)}$. Along the marked arc, moving from $A$ to $B$ is {direction}; '+('add' if s==1 else 'subtract')+' the marked angle.\n\n$$\n\\theta_B='+compose+'.\n$$\n\n'
 +f'Thus $B$ has polar coordinates $({tex(r)},{angle(b,u)})$. Using $x=r\\cos\\theta$ and $y=r\\sin\\theta$,\n\n$$\n\\begin{{aligned}}\n'
 +r',\\'.join(rows)+'.\n\\end{aligned}\n$$\n\nThe Cartesian coordinates of $B$ are $'+pair(result)+'$.')
 return solution

def generate(level,p,rng=None,profile=None):
 rng=rng or random.Random(0)
 r=exact(p['radius']);a=p['alpha'];d=p['delta'];s=p['direction'];b=a+s*d;u=p['units']
 if r<=0 or a not in (*SPECIAL,0,90,180,270) or b not in SPECIAL or not 0<d<=210 or s not in (-1,1):raise ValueError('Outside supported geometry')
 image=render_plots(p)
 prompt=(f'![]({image})\n\nThe diagram shows $A$ and $B$ on a circle centered at the origin $O$. Point $A$ has polar coordinates $({tex(r)},{angle(a,u)})$ and the marked angle is $\\angle AOB={angle(d,u)}$.\n\n')
 if level=='easy':
  prompt+=('Moving from $A$ to $B$ along the marked arc is '+('counterclockwise, so add' if s==1 else 'clockwise, so subtract')+' the marked angle. Use $x=r\\cos\\theta$ and $y=r\\sin\\theta$ to find the Cartesian coordinates of $B$.\n\n')
 elif level=='moderate':
  prompt+='Use the marked arc and the positions of $A$ and $B$ to decide whether to increase or decrease the angle of $A$.\n\n'
 target=xy(r,b)
 if level=='hard':
  prompt+='Determine the exact Cartesian coordinates of $B$.\n\nThe Cartesian coordinates of $B$ are $(${{field-1}}$,$ {{field-2}}$)$.'
  fields=[make_field('field-'+str(i+1),'blank',[tex(v)],tex(v),rng) for i,v in enumerate(target)];recipes=['x=r*cos(theta_B)','y=r*sin(theta_B)'];profile='exact-entry'
 else:
  profile=profile or rng.choice(list(PROFILES));vals,recipes=bank(p,profile,rng)
  prompt+='Which ordered pair gives the Cartesian coordinates of $B$?'
  fields=[make_field('selection','radio',[pair(v) for v in vals],pair(target),rng)]
 q={':question/problem':prompt,':question/worked-solution':derivation(p),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
 return own_record(q,{'parameters':p,'profile':profile,'bank_recipes':recipes,'correct_mathematics':[sp.sstr(x) for x in target],'source_support':['f0c5bd75-dd47-5028-8eff-38c87e7411bf','ec6a7f4f-9f9a-5a0c-bdce-ef6083c2204a','0eb03380-bb2e-5373-833c-3b08aac5da8c'],'template':'diagram-'+level})

def replay_sources():
 records=[]
 replay_items=list(zip(SOURCE['questions'],SOURCE_PARAMS))+list(zip(SOURCE['exemplars'],[('6',30,30,1,'degree'),('6',150,30,-1,'degree'),('6',150,105,-1,'radian')]))
 for q0,p0 in replay_items:
  q=copy.deepcopy(q0)
  for k in list(q):
   if k not in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):q.pop(k)
  q[':question/difficulty']=q[':question/difficulty'][':db/ident']
  for f in q[':question/answer-fields']:
   f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
   for a in f[':answer-field/choices']:a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident']
  records.append(own_record(q,{'source_question_id':q0[':question/id'],'parameters':parameters(*p0),'template':'source-replay','profile':q0.get(':question/math-academy-id',q0[':question/id'])}))
 return records

def angular_roles(level):
 starts=SPECIAL if level!='hard' else (*SPECIAL,0,90,180,270)
 for a in starts:
  for b in SPECIAL:
   delta=abs(b-a)
   if 0<delta<=(90 if level!='hard' else 210):yield (a,delta,1 if b>a else -1)

def batch(level,count,seed):
 rng=random.Random(seed);records=[];seen=set();roles=list(angular_roles(level));attempts=0
 directions=[]
 # Pick relation/profile before incidental radius and option order. Reject whole collisions.
 while len(records)<count:
  attempts+=1
  if attempts>10000:raise ValueError('Requested batch exceeds supported distinct main calculations')
  if len(directions)<=len(records):
   block=[-1,1];rng.shuffle(block);directions.extend(block)
  wanted=directions[len(records)]
  a,d,s=rng.choice([role for role in roles if role[2]==wanted]);profile=rng.choice(list(PROFILES))
  r=str(rng.randrange(2,11))
  if level=='hard' and (a+s*d)%90==45 and rng.randrange(2):r+='*sqrt(2)'
  p=parameters(r,a,d,s,'radian' if level=='hard' else 'degree');fingerprint=(r,a+s*d)
  if fingerprint in seen:continue
  try:record=generate(level,p,rng,profile)
  except ValueError as err:
   if str(err)!='Distinct complete bank required':raise
   continue
  seen.add(fingerprint);record['generation']['seed']=seed;record['generation']['batch_index']=len(records);records.append(record)
 return records

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified','all'],default='hard');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');args=ap.parse_args()
 if args.count<0:ap.error('count must be nonnegative')
 if not os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'):ap.error('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR must name an output directory outside the package')
 output=Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']).resolve()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else ['hard' if args.difficulty=='unclassified' else args.difficulty]
 print(json.dumps([r for level in levels for r in batch(level,args.count,args.seed)],indent=2))
if __name__=='__main__':main()
