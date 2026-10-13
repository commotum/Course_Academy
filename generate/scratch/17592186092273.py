#!/usr/bin/env python3
"""Diagram-based polar conversion. Frozen math basis 1356; steps 3–7 only.

Observed masks retain complete prose and all ordered coordinate-calculation stages.
Public observed-* profiles preserve absent attributes and complete opaque banks;
these are evidence-only, never selected for learning. Normal profiles use a whole
method bank (correct, reversed route, A rather than B, x-sign, y-sign), rejecting
collisions. Missing easy/moderate are authored curriculum-grounded design claims.
See the private evidence directory for exact scope and validation.
"""
from __future__ import annotations
from functools import lru_cache
import argparse, hashlib, json, math, os, random, re, sys, tempfile, uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/kp17592186092273-mpl')
import sympy as sp
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
from PIL import Image
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
REC=SOURCE['record']; KP=17592186092273; VERSION='diagram-cartesian-v2'
QUESTIONS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
# Radius, initial degrees, unsigned swept degrees, signed route, source angle units.
DATA={
'q-40920':('8',45,75,1,'radian'), 'q-40922':('6',210,75,-1,'degree'),
'q-120593':('6',30,90,1,'radian'),'q-120595':('4',150,30,-1,'radian'),
'q-120597':('4*sqrt(2)',150,165,1,'degree'),'q-120598':('2',240,195,-1,'degree'),
'q-277012':('4',240,210,-1,'degree'),'q-277027':('10',60,60,1,'degree'),
'q-81221':('5',210,150,-1,'radian'),'q-81224':('10',60,180,1,'radian')}
MATH=re.compile(r'\$\$([\s\S]*?)\$\$|\$([^$]*?)\$')
def exact(v): return sp.sympify(v,locals={'sqrt':sp.sqrt})
def tex(v): return sp.latex(sp.simplify(v))
def angle(v,unit): return tex(sp.Rational(v,180)*sp.pi) if unit=='radian' else '{'+str(v)+r'}^{∘}'
@lru_cache(maxsize=4096)
def xy(r,b): return tuple(sp.simplify(r*f(sp.Rational(b,180)*sp.pi)) for f in (sp.cos,sp.sin))
def pair(t): return '('+','.join(tex(x) for x in t)+')'
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(v,sort_keys=True,ensure_ascii=False)))
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def source_params(qid):
 r,a,d,s,u=DATA[qid];return {'radius':r,'alpha':a,'delta':d,'direction':s,'units':u}
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
def render_math_slots(text,slots):
 """Only replace whole complete math spans, never a digit or variable in prose."""
 def sub(m):
  body=m.group(1) if m.group(1) is not None else m.group(2)
  if body not in slots:return m.group(0)
  delim='$$' if m.group(1) is not None else '$';return delim+slots[body]+delim
 return MATH.sub(sub,text)
def display(old,new,unchanged): return old if unchanged else new

def source_prompt(qid,p,asset):
 q=QUESTIONS[qid];p0=source_params(qid); r=exact(p['radius']);a=p['alpha'];d=p['delta'];u=p['units']
 raw=q[':question/problem']; spans=list(MATH.finditer(raw));slots={}
 for m in spans:
  s=m.group(2)
  if s is None:continue
  if s.startswith('(') and ',' in s:
   tail=s[s.rfind(')')+1:];slots[s]=display(s,'('+tex(r)+','+angle(a,u)+')'+tail,r==exact(p0['radius']) and a==p0['alpha'] and u==p0['units'])
  elif 'AOB' in s:
   tail=',' if s.endswith(',') else '.' if s.endswith('.') else ''
   slots[s]=display(s,'m∠AOB='+angle(d,u)+tail,d==p0['delta'] and u==p0['units'])
 out=render_math_slots(raw,slots)
 return re.sub(r'!\[\]\([^)]*\)', '![]('+asset+')',out)

def calculation_rows(c,r,b,u):
 f=sp.cos if c=='x' else sp.sin;fn='cos' if c=='x' else 'sin';v=f(sp.Rational(b,180)*sp.pi)
 return '\n'+r'\begin{aligned}'+c+r' & =r\operatorname{'+fn+r'}⁡\theta  \\  & ='+tex(r)+r'\operatorname{'+fn+r'}⁡('+angle(b,u)+r') \\  & ='+tex(r)+r'\cdot ('+tex(v)+r') \\  & ='+tex(r*v)+r'\end{aligned}'+'\n'

def source_solution(qid,p):
 q=QUESTIONS[qid]
 if ':question/worked-solution' not in q:return None
 p0=source_params(qid);r=exact(p['radius']);a=p['alpha'];d=p['delta'];s=p['direction'];u=p['units'];b=a+s*d
 r0=exact(p0['radius']);a0=p0['alpha'];b0=a0+p0['direction']*p0['delta'];u0=p0['units']
 same_r=r==r0;same_a=a==a0 and u==u0;same_b=b==b0 and u==u0
 raw=q[':question/worked-solution'];slots={}; tuple_index=0
 for m in MATH.finditer(raw):
  body=m.group(1) if m.group(1) is not None else m.group(2)
  if m.group(1) is not None:
   if 'theta' in body and '_{B}' in body:
    new='\n'+r'{\theta }_{B}='+angle(a,u)+('+' if s==1 else '-')+angle(d,u)+'='+angle(b,u)+'.\n'
    slots[body]=display(body,new,same_a and d==p0['delta'] and s==p0['direction'])
   elif r'\begin{aligned}x' in body:slots[body]=display(body,calculation_rows('x',r,b,u),same_r and same_b)
   elif r'\begin{aligned}y' in body:slots[body]=display(body,calculation_rows('y',r,b,u),same_r and same_b)
   continue
  if body.startswith('(') and ',' in body:
   # Source's three ordered tuples: A polar, B polar, final Cartesian.
   tuple_index+=1;tail=body[body.rfind(')')+1:]
   if tuple_index==1: val='('+tex(r)+','+angle(a,u)+')';unch=same_r and same_a
   elif tuple_index==2:val='('+tex(r)+','+angle(b,u)+')';unch=same_r and same_b
   else:val=pair(xy(r,b));unch=same_r and same_b
   slots[body]=display(body,val+tail,unch)
  elif body.startswith('r='):slots[body]=display(body,'r='+tex(r)+('.' if body.endswith('.') else ''),same_r)
  elif body.replace(' ','').rstrip('.,')==tex(r0).replace(' ',''):
   tail=body[-1] if body.endswith(('.',',')) else ''
   slots[body]=display(body,tex(r)+tail,same_r)
  elif ('pi' in body or '∘' in body) and 'theta' not in body:slots[body]=display(body,angle(a,u)+(',' if body.endswith(',') else ''),same_a)
 out=render_math_slots(raw,slots)
 old='counter-clockwise' if 'counter-clockwise' in raw else 'counterclockwise' if 'counterclockwise' in raw else 'clockwise'
 new='counter-clockwise' if s==1 and old=='counter-clockwise' else 'counterclockwise' if s==1 else 'clockwise'
 return out.replace('circle '+old+' to','circle '+new+' to')

def authored_solution(p):
 r=exact(p['radius']);a=p['alpha'];d=p['delta'];s=p['direction'];u=p['units'];b=a+s*d
 return (f'First, since $A$ has polar coordinates $({tex(r)},{angle(a,u)}),$ we must have $r={tex(r)}.$ Also, since the points $A$ and $B$ both lie on a circle of radius ${tex(r)},$ the $r$-coordinate of $B$ must also be ${tex(r)}.$\n\n'
 +f'Notice that one must traverse the circle {"counterclockwise" if s==1 else "clockwise"} to move from the point $A$ to point $B.$ Since the $\\theta $-coordinate of $A$ is ${angle(a,u)},$ the $\\theta $-coordinate of $B$ must be\n\n$$\n'
 +r'{\theta }_{B}='+angle(a,u)+('+' if s==1 else '-')+angle(d,u)+'='+angle(b,u)+'.\n$$\n\n'
 +f'So, the polar coordinates of $B$ are $({tex(r)},{angle(b,u)})$\n\nNow, we convert $B$ to Cartesian coordinates. To convert from polar coordinates to Cartesian coordinates, we use\n\n$$\nx=r\\operatorname{{cos}}⁡\\theta ,\\,y=r\\operatorname{{sin}}⁡\\theta .\n$$\n\nFirst, we calculate the $x$-coordinate of $B:$\n\n$$'
 +calculation_rows('x',r,b,u)+'$$\n\nThen, we calculate the $y$-coordinate of $B:$\n\n$$'+calculation_rows('y',r,b,u)+'$$\n\nTherefore, the Cartesian coordinates of $B$ are $'+pair(xy(r,b))+'.$')

# Geometry is normalized by radius: source axes have no coordinate ticks.
# Actual saved pixel transformation/clearances are measured without masking.
def render_plots(p,output_dir=None):
 out=Path(output_dir or ROOT/'plots');out.mkdir(parents=True,exist_ok=True)
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
def allowed(level,p,evidence=False):
 if set(p)!={'radius','alpha','delta','direction','units'}:raise ValueError('Exact parameter keys required')
 r=exact(p['radius']);a=p['alpha'];d=p['delta'];s=p['direction'];u=p['units']
 if r.has(sp.Float) or r.is_number is not True or r.is_real is not True:raise ValueError('A positive exact real radius is required')
 if any(type(v)!=int for v in (a,d,s)) or s not in (-1,1) or u not in ('degree','radian'):raise ValueError('Invalid angles/direction/units')
 if r<=0 or r>10*sp.sqrt(2) or not (0<=a<360 and 0<d<=210 and 0<a+s*d<360) or a+s*d not in SPECIAL:raise ValueError('Outside exact-angle workload bounds')
 if evidence:return
 if level=='easy':
  if a!=0 or s!=1 or d not in (30,45,60) or u!='degree' or r not in range(2,11):raise ValueError('Easy: A on positive x axis; one first-quadrant familiar angle; integer radius 2–10')
 elif level=='moderate':
  if a not in SPECIAL or a//90!=(a+s*d)//90 or d>60 or u!='degree' or r not in range(2,11):raise ValueError('Moderate: non-axis A and B in same quadrant; degree angle sum/difference <=60; integer radius 2–10')
 elif level=='hard':
  # Source hard q-120595 uses a same-quadrant 30-degree difference; observed
  # replay keeps its label. Authored hard draws cross-quadrant / long sweeps.
  if a not in SPECIAL or (a//90==(a+s*d)//90 and d<90):raise ValueError('Authored hard requires cross-quadrant or at least 90-degree sweep')
  if r not in [sp.Integer(k)*z for k in range(2,11) for z in (1,sp.sqrt(2))]:raise ValueError('Hard radius: integer or integer sqrt(2), coefficient 2–10')
 else:raise ValueError('Unknown level')

def domain(level):
 starts=(0,) if level=='easy' else SPECIAL
 radii=[str(k) for k in range(2,11)] if level!='hard' else [str(k)+suffix for k in range(2,11) for suffix in ('','*sqrt(2)')]
 units=('degree',) if level!='hard' else ('degree','radian')
 for a in starts:
  for b in SPECIAL:
   delta=abs(b-a);s=1 if b>a else -1
   for u in units:
    base={'radius':'2','alpha':a,'delta':delta,'direction':s,'units':u}
    try:allowed(level,base)
    except ValueError:continue
    for r in radii:yield dict(base,radius=r)
def method_bank(p):
 r=exact(p['radius']);a=p['alpha'];s=p['direction'];d=p['delta'];b=a+s*d;c=xy(r,b)
 if a!=0 and (a-s*d)%360 not in (*SPECIAL,0,90,180,270):raise ValueError('Reversed-route bank would require a new trig-angle identity')
 bank=([c,xy(r,a),(-c[0],c[1]),(c[0],-c[1]),xy(sp.Integer(1),b)] if a==0 else [c,xy(r,a-s*d),xy(r,a),(-c[0],c[1]),(c[0],-c[1])])
 if len(set(bank))!=5:raise ValueError('Complete method bank collision')
 return bank

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed);profile=profile or 'authored-method';evidence=profile.startswith('observed-')
 if evidence:
  if level!='hard':raise ValueError('Observed labels and authored unrated assignment require hard replay')
  qid=profile.removeprefix('observed-')
  if qid not in QUESTIONS:raise ValueError('Unknown observed profile')
  if template not in (None,qid):raise ValueError('Observed template/profile mismatch')
  template=qid;p=dict(parameters or source_params(qid));allowed(level,p,True)
  p0=source_params(qid)
  if any(p[k]!=p0[k] for k in ('alpha','delta','direction','units')):raise ValueError('Opaque evidence banks support radius scaling only')
  ft='blank' if len(QUESTIONS[qid][':question/answer-fields'])==2 else 'radio'
 else:
  if profile!='authored-method':raise ValueError('Unknown bank profile')
  ft=field_type or ('blank' if rng.randrange(2) else 'radio')
  if ft not in ('radio','blank'):raise ValueError('Only observed radio or two-blank response')
  if template is None:
   # Choose supported source-shaped layout/family before parameter sampling.
   eligible=[k for k in QUESTIONS if ('blank' if len(QUESTIONS[k][':question/answer-fields'])==2 else 'radio')==ft]
   template=rng.choice(eligible) if level=='hard' else 'authored-'+level
  if template in QUESTIONS:
   source_ft='blank' if len(QUESTIONS[template][':question/answer-fields'])==2 else 'radio'
   if field_type and field_type!=source_ft:raise ValueError('Source template field layout is fixed')
   ft=source_ft
  if template not in QUESTIONS and template!='authored-'+level:raise ValueError('Unknown or wrong-level template')
  if level!='hard' and template in QUESTIONS:raise ValueError('Observed templates belong to hard')
  if parameters is None:
   # Choose a complete eligible bank before sampling; reject whole collisions.
   choices=list(domain(level));rng.shuffle(choices)
   p=next((p for p in choices if _valid_bank(p,ft)),None)
   if p is None:raise ValueError('No eligible instances')
  else:p=dict(parameters);allowed(level,p);method_bank(p) if ft=='radio' else None
  allowed(level,p)
 if field_type and field_type!=ft:raise ValueError('Wrong field layout for source profile')
 r=exact(p['radius']);b=p['alpha']+p['direction']*p['delta'];correct=xy(r,b)
 if evidence:
  q=QUESTIONS[template];asset=re.search(r'!\[\]\(([^)]*)\)',q[':question/problem'])[1]
  asset=asset if exact(p['radius'])==exact(source_params(template)['radius']) else render_plots(p)
  prompt=source_prompt(template,p,asset);solution=source_solution(template,p)
 else:
  asset=render_plots(p)
  if template in QUESTIONS:prompt=source_prompt(template,p,asset);solution=source_solution(template,p) or authored_solution(p)
  else:prompt=f'![]({asset})\n\nThe diagram above shows a circle of radius $r$ centered at the origin. If the polar coordinates of the point $A$ are $({tex(r)},{angle(p["alpha"],p["units"])}),$ and $m∠AOB={angle(p["delta"],p["units"])},$ what are the Cartesian coordinates of $B?$';solution=authored_solution(p)
  # Source-family field layout stays available; normal field override also supports
  # the exact two-blank layout, with presentation masks changed as a whole.
  prompt=re.sub(r'\n\nThe Cartesian coordinates of \$B\$ are [\s\S]*$','',prompt)
  if ft=='blank':prompt+='\n\nThe Cartesian coordinates of $B$ are $(${{field-1}}$,$\n{{field-2}}$).$'
 fields=[];banks=[]
 if evidence:
  scale=r/exact(source_params(template)['radius'])
  for f in q[':question/answer-fields']:
   vals=[]
   for a in f[':answer-field/choices']:
    value=a[':answer/value'];v=parse_pair(value) if ft=='radio' else (latex_expr(value),)
    scaled=tuple(sp.simplify(scale*x) for x in v)
    vals.append(value if scale==1 else pair(scaled) if ft=='radio' else tex(scaled[0]))
   banks.append(vals)
 else:banks=[[pair(v) for v in method_bank(p)]] if ft=='radio' else [[tex(correct[0])],[tex(correct[1])]]
 identity={'version':VERSION,'level':level if not evidence or ':question/difficulty' in q else None,'prompt':prompt,'solution':solution,'banks':banks,'types':ft}
 content=digest(identity);qid=uid(content)
 for i,values in enumerate(banks):
  key='selection' if ft=='radio' else 'field-'+str(i+1);fid=uid([qid,key]);answers=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
  if ft=='radio':rng.shuffle(answers)
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers}
  raw_f=q[':question/answer-fields'][i] if evidence else None
  if not evidence or ':answer-field/correct' in raw_f:
   target=correct if ft=='radio' else (correct[i],)
   matches=[a for a in answers if (parse_pair(a[':answer/value']) if ft=='radio' else (latex_expr(a[':answer/value']),))==target]
   if len(matches)!=1:raise ValueError('Missing or ambiguous correct answer')
   f[':answer-field/correct']=[':answer/id',matches[0][':answer/id']]
  fields.append(f)
 question={':question/id':qid,':question/problem':prompt,':question/answer-fields':fields}
 if not evidence or ':question/difficulty' in q:question[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:question[':question/worked-solution']=solution
 task={'radius':sp.sstr(r),'alpha':p['alpha'],'delta':p['delta'],'direction':p['direction'],'response_demand':'diagram-route-and-convert'}
 return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':p,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'evidence_only':evidence,'eligible_for_learning':not evidence,'bank_recipes':(['opaque_radius_scaled_complete_source_bank'] if evidence and ft=='radio' else ['correct_B','use_A','negate_x','negate_y','omit_radius'] if ft=='radio' and p['alpha']==0 else ['correct_B','reverse_route','use_A','negate_x','negate_y'] if ft=='radio' else ['x=r*cos(theta_B)','y=r*sin(theta_B)']),'content_identity':content,'mathematical_fingerprint':digest(task),'correct_mathematics':[sp.sstr(x) for x in correct],'plot':asset,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}}
def _valid_bank(p,ft):
 if ft=='blank':return True
 try:method_bank(p);return True
 except ValueError:return False
# EASY — authored: A on positive x axis; no signed angle arithmetic; radius 2–10.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — authored: same-quadrant signed angle sum/difference, degree units.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — observed conversion masks, authored cross-quadrant/long-sweep bounds.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record):
 q=record['question'];chunks=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):chunks+=['\n'+f[':answer-field/key'],*[a[':answer/value'] for a in f[':answer-field/choices']]]
 if ':question/worked-solution' in q:chunks+=['\nWorked solution',q[':question/worked-solution']]
 return '\n'.join(chunks)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
