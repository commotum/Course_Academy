#!/usr/bin/env python3
"""Basis-1356 local generator, steps 3–7 only. See private evidence directory.
Raw profiles retain all captured omissions and source mistakes, marked ineligible.
Normal families share the source's four stages, with exact integration arithmetic.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, os, random, re, sys, tempfile, uuid, threading
from pathlib import Path
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR',str(ROOT_CACHE := Path('/tmp/typei-mpl-cache')))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
KP=17592186129197
ROOT=Path(__file__).with_suffix('')
SRC=json.loads((ROOT/'source.json').read_text())
R=SRC['record']; TITLE=R[':knowledge-point/title']; VERSION='type-I-area-1'
Q={q[':question/math-academy-id']:q for q in R[':knowledge-point/questions']}
CURRENT=json.loads((ROOT/'current-source.json').read_text())
CURRENT_Q={q[':question/math-academy-id']:q for q in CURRENT['material']['kp'][':knowledge-point/questions']}
x,y,u,v=sp.symbols('x y u v', real=True)
FAMILIES={'simple':('q-38374','easy'), 'mixed':(None,'moderate'),'quartic':('q-82874','hard'),'hyper_y':('q-160885','hard'),'down':('q-82878','hard'),'up':('q-83943','hard'),'vertical':('q-83947','hard'),'hyper_x':('q-160710','hard')}
ANCHORS={'q-38374':{'a':1,'h':1,'k':0},'q-82874':{'a':1,'h':1,'k':0},'q-160885':{'a':2,'h':4,'k':1},'q-82878':{'a':1,'h':2,'k':1},'q-83943':{'a':2,'h':1,'k':2},'q-83947':{'a':3,'h':4,'k':-3},'q-160710':{'a':1,'h':2,'k':1}}
def tex(z):
 return sp.latex(z).replace(r'\log',r'\ln')
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,f'{KP}/{s}'))
def eq(a,b):return sp.simplify(a-b)==0
def parse(z):
 z=z.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('⁡','').replace(r'\operatorname{ln}',r'\ln').replace(' ', '')
 while '\\frac' in z:
  start=z.index('\\frac'); i=start+5
  def group(i):
   if z[i]!='{':raise ValueError(z)
   depth=1;j=i+1
   while depth:
    depth+=(z[j]=='{')-(z[j]=='}');j+=1
   return z[i+1:j-1],j
  aa,j=group(i);bb,k=group(j);z=z[:start]+'(('+aa+')/('+bb+'))'+z[k:]
 z=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',z)
 z=re.sub(r'\\ln(?:\{([^{}]+)\}|([0-9]+))',lambda m:'log('+str(m[1] or m[2])+')',z)
 z=z.replace(r'\ln','log');z=z.replace('{','(').replace('}',')').replace('^','**')
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 return parse_expr(z,local_dict={'u':u,'v':v,'x':x,'y':y},transformations=standard_transformations+(implicit_multiplication_application,))
def format_ok(s):
 assert not any(ord(c)<32 and c not in '\n\t' for c in s),'control characters'
 assert s.count('$$')%2==0 and s.replace('$$','').count('$')%2==0,'math delimiters'
 # Escaped set glyphs are not TeX grouping braces.
 z=re.sub(r'\\[{}]','',s);depth=0
 for c in z:
  depth+=(c=='{')-(c=='}');assert depth>=0,'closing brace'
 assert depth==0,'opening brace'
def aligned(rows):return r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
def display(s):return '$$\n'+s+'\n$$'
def swap_math(text,scale):
 """Similarity source recipe: complete math variables x,y become x/s,y/s.
 At s=1 every mask reinserts its original single variable, preserving raw bytes.
 """
 def sub(m):
  t=m.group();s=tex(scale)
  if scale!=1 and '∂' not in t and r'\to' not in t:
   t=re.sub(r'(?<![A-Za-z\\])([xy])(?![A-Za-z])',lambda n:rf'\frac{{{n[1]}}}{{{s}}}',t)
  return t
 return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$',sub,text)
def raw_generate(level,seed,source,parameters,historical=False):
 q=(Q if historical else CURRENT_Q)[source]; p=dict(parameters or {'scale':1})
 if set(p)!={'scale'} or not isinstance(p['scale'],int) or not 1<=p['scale']<=4:raise ValueError('raw scale: integer 1..4 only')
 s=sp.Integer(p['scale']); out={k:copy.deepcopy(val) for k,val in q.items() if k not in [':db/id',':question/math-academy-id',':question/id',':question/answer-fields']}
 if ':question/difficulty' in out:out[':question/difficulty']=out[':question/difficulty'][':db/ident']
 out[':question/problem']=swap_math(q[':question/problem'],s)
 if ':question/worked-solution' in q:
  sol=swap_math(q[':question/worked-solution'],s)
  # Source solution is a full math/prose template. A similarity scales the
  # forward determinant by s² and every area-chain RHS by s². All transformations
  # are applied to complete blocks, never scattered numeric literals.
  if s!=1:
   if source not in ANCHORS:raise ValueError('current source supports exact scale=1 replay only')
   family=next(f for f,z in FAMILIES.items() if z[0]==source)
   m=model(family,ANCHORS[source]); det=m['det']; inv=m['J']
   start=sol.index('**Step 2**'); end=sol.index('**Step 3**')
   sec=sol[start:end]
   matrix=[sp.diff(m[z],t)/s for z in ['U','V'] for t in [x,y]]
   block=aligned([r'\frac{∂(u,v)}{∂(x,y)} &=\left|\begin{matrix}\frac{∂u}{∂x}&\frac{∂u}{∂y}\\\frac{∂v}{∂x}&\frac{∂v}{∂y}\end{matrix}\right|', r'&=\left|\begin{matrix}'+tex(matrix[0])+'&'+tex(matrix[1])+r'\\'+tex(matrix[2])+'&'+tex(matrix[3])+r'\end{matrix}\right|',r'&='+tex(det/(s*s))+'.'])
   sec=re.sub(r'\$\$[\s\S]*?\$\$',lambda _:display(block),sec,count=1)
   sol=sol[:start]+sec+sol[end:]
   start=sol.index('**Step 3**');end=sol.index('**Step 4**');sec=sol[start:end]
   sec=re.sub(r'\$\$[\s\S]*?\$\$',lambda _:display(r'\frac{∂(x,y)}{∂(u,v)}=(\frac{∂(u,v)}{∂(x,y)})^{-1}=('+tex(det/(s*s))+r')^{-1}='+tex(inv*s*s)+'.'),sec,count=1)
   sol=sol[:start]+sec+sol[end:]
   start=sol.index('**Step 4**');sec=sol[start:]
   # Keep inner integrations and arithmetic as original ordered stages; scale
   # each complete RHS after the generic change-of-variables row.
   def scaled_chain(match):
    block=match.group();rows=block.split(r'\\')
    for i in range(1,len(rows)):
     rows[i]=rows[i].replace('& =','& ='+tex(s*s)+r'\cdot ',1)
    return r'\\'.join(rows)
   sec=re.sub(r'\$\$[\s\S]*?\$\$',scaled_chain,sec)
   sol=sol[:start]+sec
  out[':question/worked-solution']=sol
 specs=[]
 for sourcefield in q[':question/answer-fields']:
  bank=[parse(a[':answer/value'])*s*s for a in sourcefield[':answer-field/choices']]
  spell=[a[':answer/value'] if s==1 else tex(z) for a,z in zip(sourcefield[':answer-field/choices'],bank)]
  original_correct=sourcefield.get(':answer-field/correct')
  correct=parse(original_correct[':answer/value'])*s*s if original_correct else None
  attributes={key:copy.deepcopy(value)for key,value in sourcefield.items()if key not in [':db/id',':answer-field/id',':answer-field/choices',':answer-field/correct']}
  attributes[':answer-field/type']=sourcefield[':answer-field/type'][':db/ident']
  answer_attributes=[{key:copy.deepcopy(value)for key,value in answer.items()if key not in [':db/id',':answer/id',':answer/type',':answer/value']}for answer in sourcefield[':answer-field/choices']]
  answer_types=[answer[':answer/type'][':db/ident']for answer in sourcefield[':answer-field/choices']]
  specs.append({'bank':bank,'spelling':spell,'correct':correct,'attributes':attributes,'answer_attributes':answer_attributes,'answer_types':answer_types})
 first=specs[0]
 return record(out,first['bank'],first['correct'],first['spelling'],level,seed,source,p,('historical:' if historical else 'raw:')+source,False,{'source':{key:(SRC if historical else CURRENT)[key] for key in ['database','basis','lineage']},'replay_capture':'historical' if historical else 'current','source_omissions':sorted(set([':question/difficulty',':question/worked-solution'])-set(q)), 'source_field_omissions':[sorted(set([':answer-field/correct'])-set(field))for field in q[':question/answer-fields']]},field_specs=specs)
def model(f,p):
 a,h,k=map(sp.Integer,(p['a'],p['h'],p['k']))
 if f in ['simple','down','up']:
  U=x-a*y;V=y+(k if f=='down' else 0);det=1
 elif f=='mixed':U=a*x-2*y;V=x+y;det=a+2
 elif f=='vertical':U=y+a*x;V=x;det=-1
 elif f=='quartic':U=x+a*y;V=x-a*y;det=-2*a
 elif f=='hyper_y':U=y+a*x;V=y-a*x;det=2*a
 else:U=x-a*y;V=x+a*y;det=2*a
 if f in ['hyper_x','hyper_y']:
  lo=k;hi=h/k;low=k;high=h/u;prim=h*sp.log(u)-k*u
 elif f=='quartic':
  lo=0;hi=h;low=u**4/h**3;high=u;prim=u**2/2-u**5/(5*h**3)
 else:
  lo=-sp.sqrt(h);hi=sp.sqrt(h)
  if f=='down':low=k;high=k+h-u*u
  else:low=u*u+k;high=k+h
  prim=h*u-u**3/3
 J=1/sp.Integer(det);width=sp.expand(high-low);A=sp.simplify(abs(J)*sp.integrate(width,(u,lo,hi)))
 return dict(U=U,V=V,det=det,J=J,lo=lo,hi=hi,low=low,high=high,prim=prim,A=A,width=width)
def guards(f,p):
 if set(p)!={'a','h','k'} or any(type(p[t]) is not int for t in p):raise ValueError('parameters must be integer a,h,k')
 a,h,k=p['a'],p['h'],p['k']
 if not 1<=a<=8:raise ValueError('a:1..8')
 if f=='simple' and (h not in [1,4,9,16,25,36] or k!=0):raise ValueError('easy: square gap and zero shift')
 if f=='mixed' and (h not in [1,4,9,16,25,36] or k!=0 or a<2):raise ValueError('moderate: square gap, zero shift, nonunit determinant')
 if f in ['up','vertical'] and (h not in [1,2,3,4,5,6,7,8,9,10,12,16] or k==0 or abs(k)>5):raise ValueError('hard parabola: nonzero signed shift')
 if f=='down' and (h not in [2,3,5,6,7,8,10,12] or not 1<=k<=4):raise ValueError('hard downward: positive translation, nonsquare gap')
 if f=='quartic' and (h not in [1,2,3] or k!=0):raise ValueError('quartic: endpoint 1..3 and k=0')
 if f.startswith('hyper') and (not 1<=k<=3 or not 2<=h<=12 or h<=k*k):raise ValueError('hyperbola requires h>k²')
def sample(f,rng):
 a=rng.randint(1,8)
 if f=='simple':return {'a':a,'h':rng.choice([1,4,9,16,25,36]),'k':0}
 if f=='mixed':return {'a':rng.randint(2,8),'h':rng.choice([1,4,9,16,25,36]),'k':0}
 if f=='quartic':return {'a':a,'h':rng.randint(1,3),'k':0}
 if f.startswith('hyper'):
  k=rng.randint(1,3);return {'a':a,'h':rng.randint(k*k+1,12),'k':k}
 if f=='down':return {'a':a,'h':rng.choice([2,3,5,6,7,8,10,12]),'k':rng.randint(1,4)}
 return {'a':a,'h':rng.choice([1,2,3,4,5,6,7,8,9,10,12,16]),'k':rng.choice([-5,-4,-3,-2,-1,1,2,3,4,5])}
def candidate_instances(f,rng):
 """Choose a bank without assigning the correct-answer role to any member."""
 candidates=[]
 for _ in range(1000):
  p=sample(f,rng);d=model(f,p)
  if all(not eq(d['A'],other['A']) for _,other in candidates):
   candidates.append((p,d))
   if len(candidates)==5:return candidates
 raise ValueError('could not construct five distinct counterfactual areas')
def recipes(f,d,p,profile,candidates):
 if profile!='method':raise ValueError('normal profile is method')
 bank=[other['A'] for _,other in candidates]
 # Explicit parameter calls retain the same bank whenever their area is a
 # member, allowing all five target assignments with the same choice values.
 if not any(eq(d['A'],value) for value in bank):bank[-1]=d['A']
 return bank
RENDERER_VERSION='type-I-region-pixel-calibration-5'
_PLOT_LOCK=threading.RLock()
def plot(f,p,d,output_dir=None):
 # Matplotlib's global mathtext parser is not thread-safe. Serialize rendering
 # within one process; independent process calls still use unique atomic files.
 with _PLOT_LOCK:return _plot_impl(f,p,d,output_dir)
def _plot_impl(f,p,d,output_dir=None):
 output_dir=output_dir or os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
 if not output_dir:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required for generated assets')
 folder=Path(output_dir)/'plots';folder.mkdir(parents=True,exist_ok=True)
 key=digest({'renderer_version':RENDERER_VERSION,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'f':f,'p':p,'geometry':str((d['lo'],d['hi'],d['low'],d['high']))})[:24]
 dst=folder/(key+'.png');side=folder/(key+'.json')
 if dst.exists() and side.exists():return str(dst.resolve())
 us=np.linspace(float(d['lo']),float(d['hi']),401)
 evals=lambda z:np.full_like(us,float(z)) if not z.has(u) else np.asarray(sp.lambdify(u,z,'numpy')(us),dtype=float)
 yl,yh=evals(d['low']),evals(d['high']);xmin=min(0,float(us.min()));xmax=max(0,float(us.max()));ymin=min(0,float(yl.min()));ymax=max(0,float(yh.max()))
 dx=max(xmax-xmin,1);dy=max(ymax-ymin,1)
 # Each axis is calibrated independently; source geometry need not use equal units.
 fig,ax=plt.subplots(figsize=(5.2,4.2),dpi=130)
 lower_color,upper_color=('blue','red')if f=='quartic'else('red','blue')
 ax.fill_between(us,yl,yh,color='#dce9f1');ax.plot(us,yl,color=lower_color,lw=1.5);ax.plot(us,yh,color=upper_color,lw=1.5)
 if f.startswith('hyper'):ax.plot([us[0],us[0]],[yl[0],yh[0]],color=lower_color,lw=1.5)
 ax.axhline(0,color='black',lw=0.8);ax.axvline(0,color='black',lw=0.8)
 ax.set_xlim(xmin-.18*dx,xmax+.18*dx);ax.set_ylim(ymin-.15*dy,ymax+.22*dy)
 ax.set_xlabel('$u$');ax.set_ylabel('$v$',rotation=0)
 ax.set_xticks(sorted(set([0,float(d['lo']),float(d['hi'])])));ax.set_xticklabels([f'${tex(sp.nsimplify(n))}$' for n in sorted(set([sp.Integer(0),d['lo'],d['hi']]))])
 ax.set_yticks(sorted(set([0,float(d['low'].subs(u,d['lo'])),float(d['high'].subs(u,d['lo']))])))
 mid=(float(d['lo'])+float(d['hi']))/2;bottom=float(d['low'].subs(u,mid));top=float(d['high'].subs(u,mid))
 # A full zero-axis view cannot fit readable text and a slice arrow inside a
 # very narrow hyperbola wedge. Draw the identical region in a labelled local
 # view rather than shrink glyphs below readable size or move them off-domain.
 detail=None;annotation_axes=ax
 if f.startswith('hyper') and (float(d['hi'])-float(d['lo']))/dx<.25:
  detail=ax.inset_axes([.07,.43,.5,.43]);detail.set_in_layout(False)
  detail.fill_between(us,yl,yh,color='#dce9f1');detail.plot(us,yl,color=lower_color,lw=1.5);detail.plot(us,yh,color=upper_color,lw=1.5)
  detail.plot([us[0],us[0]],[yl[0],yh[0]],color=lower_color,lw=1.5)
  span=float(d['hi']-d['lo']);yspan=float(yh.max()-yl.min())
  detail.set_xlim(float(d['lo'])-.12*span,float(d['hi'])+.12*span)
  detail.set_ylim(float(yl.min())-.12*yspan,float(yh.max())+.12*yspan)
  detail.set_xticks([float(d['lo']),float(d['hi'])]);detail.set_xticklabels([f'${tex(d["lo"])}$',f'${tex(d["hi"])}$'],fontsize=8)
  detail.set_yticks([float(yl.min()),float(yh.max())]);detail.set_yticklabels([f'${tex(d["low"])}$',f'${tex(d["high"].subs(u,d["lo"]))}$'],fontsize=8)
  detail.set_title('Same region: local view',fontsize=9,pad=4)
  annotation_axes=detail
 parabola=f in ['simple','mixed','up','down','vertical']
 label_x=float(d['lo'])+.7*(float(d['hi'])-float(d['lo']))if parabola else mid
 label_low=float(d['low'].subs(u,label_x));label_high=float(d['high'].subs(u,label_x))
 label_y=(label_low+label_high)/2 if parabola else bottom+.45*(top-bottom)
 region_label=annotation_axes.text(label_x,label_y,r'$\Delta$',ha='center',va='center'if detail is not None or parabola else'baseline',color='#226aaa',fontsize=13)
 slice_x=mid-.12*(float(d['hi'])-float(d['lo']))
 slice_low=float(d['low'].subs(u,slice_x));slice_high=float(d['high'].subs(u,slice_x))
 arrow_head=(slice_x,slice_low+.88*(slice_high-slice_low));arrow_tail=(slice_x,slice_low+.12*(slice_high-slice_low))
 slice_arrow=annotation_axes.annotate('',xy=arrow_head,xytext=arrow_tail,arrowprops={'arrowstyle':'->','lw':1})
 upper_label=ax.text(.03,.96,f'$v={tex(d["high"])}$',transform=ax.transAxes,va='top',color=upper_color,fontsize=11,bbox={'facecolor':'white','alpha':.8,'edgecolor':'none'})
 lower_label=ax.text(.98,.06,f'$v={tex(d["low"])}$',transform=ax.transAxes,ha='right',color=lower_color,fontsize=11,bbox={'facecolor':'white','alpha':.8,'edgecolor':'none'})
 for z in ['top','right']:ax.spines[z].set_visible(False)
 fig.tight_layout();fig.canvas.draw()
 region_layout=None
 if parabola:
  # Text is a finite-size object: a nonzero anchor alone does not prevent its
  # glyph from crossing a zero axis or either curved boundary. Keep the font
  # readable and choose among the same region's eligible nonzero positions.
  origin=ax.transData.transform((0,0));inverse=ax.transData.inverted()
  sy=float(ax.transData.get_affine().get_matrix()[1,1]);clearance=4.0
  accepted=False
  for x_fraction in [.7,.75,.65,.8,.6,.3,.25,.35]:
   candidate_x=float(d['lo'])+x_fraction*float(d['hi']-d['lo'])
   candidate_low=float(d['low'].subs(u,candidate_x));candidate_high=float(d['high'].subs(u,candidate_x))
   for height_fraction in [.5,.4,.6,.3,.7,.2,.8]:
    candidate_y=candidate_low+height_fraction*(candidate_high-candidate_low)
    region_label.set_position((candidate_x,candidate_y));fig.canvas.draw()
    glyph=region_label.get_window_extent(fig.canvas.get_renderer())
    xclear=glyph.x1<origin[0]-clearance or glyph.x0>origin[0]+clearance
    yclear=glyph.y1<origin[1]-clearance or glyph.y0>origin[1]+clearance
    if not (xclear and yclear):continue
    corners=inverse.transform([[glyph.x0,glyph.y0],[glyph.x1,glyph.y0],[glyph.x0,glyph.y1],[glyph.x1,glyph.y1]])
    inside=all(float(d['lo'])<cu<float(d['hi'])and float(d['low'].subs(u,cu))+2/sy<cv<float(d['high'].subs(u,cu))-2/sy for cu,cv in corners)
    if not inside:continue
    region_layout={'axes_clearance_px':clearance,'boundary_clearance_px':2.0,'x_fraction':x_fraction,'height_fraction':height_fraction,'bbox_inside_region':True,'bbox_clear_of_zero_axes':True}
    accepted=True;break
   if accepted:break
  if not accepted:
   plt.close(fig);raise ValueError('no eligible readable region-label placement')
 renderer=fig.canvas.get_renderer();width_px,height_px=fig.canvas.get_width_height()
 def image_point(point,axis=ax):
  px,py=axis.transData.transform(point)
  return [float(px),float(height_px-py)]
 def image_bbox(bbox):
  bx,by,bw,bh=map(float,bbox.bounds)
  return [bx,float(height_px-by-bh),bw,bh]
 labels=[]
 for role,artist,coordinates in [('region',region_label,'detail-data'if detail is not None else'data'),('upper_boundary',upper_label,'axes'),('lower_boundary',lower_label,'axes'),('u_axis',ax.xaxis.label,'axes-label'),('v_axis',ax.yaxis.label,'axes-label')]+[('u_tick',z,'tick-label')for z in ax.get_xticklabels()]+[('v_tick',z,'tick-label')for z in ax.get_yticklabels()]+([('detail_title',detail.title,'axes-label')]+[('detail_u_tick',z,'tick-label')for z in detail.get_xticklabels()]+[('detail_v_tick',z,'tick-label')for z in detail.get_yticklabels()]if detail is not None else[]):
  bbox=artist.get_window_extent(renderer)
  labels.append({'role':role,'text':artist.get_text(),'position':list(map(float,artist.get_position())),'coordinate_system':coordinates,'bbox_display':list(map(float,bbox.bounds)),'bbox_pixel':image_bbox(bbox),'color':artist.get_color(),'visible':artist.get_visible()})
 transform=ax.transData.get_affine().get_matrix()
 to_image=np.array([[1,0,0],[0,-1,height_px],[0,0,1]],dtype=float)@transform
 axes_bbox=ax.get_window_extent(renderer)
 annotation_matrix=np.array([[1,0,0],[0,-1,height_px],[0,0,1]],dtype=float)@annotation_axes.transData.get_affine().get_matrix()
 data={'renderer':'Matplotlib','renderer_version':RENDERER_VERSION,'version':matplotlib.__version__,'python':sys.version.split()[0],'runtime':{'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'sympy':sp.__version__},'family':f,'parameters':p,'bounds':[str(d[t]) for t in ['lo','hi','low','high']],'axis_calibration':{'xlim':list(map(float,ax.get_xlim())),'ylim':list(map(float,ax.get_ylim()))},'axes_bbox_display':list(map(float,axes_bbox.bounds)),'axes_pixel_bbox':image_bbox(axes_bbox),'origin_display':list(map(float,ax.transData.transform((0,0)))),'origin_pixel':image_point((0,0)),'data_to_display_matrix':transform.tolist(),'data_to_pixel_matrix':to_image.tolist(),'pixel_coordinate_convention':'top-left origin, x rightward, y downward; display coordinates use bottom-left origin','artist_labels':labels,'slice_arrow':{'axes_role':'detail'if detail is not None else'primary','data_to_pixel_matrix':annotation_matrix.tolist(),'tail_data':list(map(float,arrow_tail)),'head_data':list(map(float,arrow_head)),'tail_pixel':image_point(arrow_tail,annotation_axes),'head_pixel':image_point(arrow_head,annotation_axes),'artist_bbox_pixel':image_bbox(slice_arrow.arrow_patch.get_window_extent(renderer))},'boundaries':'all bounding segments included/solid','arrow':'vertical upward slice','pixel_size':[width_px,height_px]}
 data['boundary_colors']={'lower':lower_color,'upper':upper_color,'left_vertical':lower_color if f.startswith('hyper')else None}
 if region_layout is not None:data['region_label_layout']=region_layout
 if detail is not None:
  data['detail_view']={'title':detail.title.get_text(),'axes_pixel_bbox':image_bbox(detail.get_window_extent(renderer)),'data_to_pixel_matrix':annotation_matrix.tolist(),'xlim':list(map(float,detail.get_xlim())),'ylim':list(map(float,detail.get_ylim())),'bounds':data['bounds'],'same_region':True}
 fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.png',dir=folder);os.close(fd)
 fig.savefig(tmp);plt.close(fig);os.replace(tmp,dst)
 fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.json',dir=folder);os.close(fd);Path(tmp).write_text(json.dumps(data,indent=2));os.replace(tmp,side)
 return str(dst.resolve())
def prompt(f,p,d):
 U,V=tex(d['U']),tex(d['V']);h,k=sp.Integer(p['h']),sp.Integer(p['k'])
 if f.startswith('hyper'):
  first,second=(V,U)if f=='hyper_x'else(U,V)
  eqs=f'the lines ${first}={tex(k)},$ ${second}={tex(k)}$ and the curve ${tex(sp.expand(d["U"]*d["V"]))}={tex(h)}.$'
 elif f=='quartic':
  power=f'({U})^{{4}}' if h==1 else rf'\frac{{({U})^{{4}}}}{{{tex(h**3)}}}'
  eqs=f'the curve ${power}{tex(-d["V"])}=0$ and the line $y=0.$'
 elif f=='down':eqs=f'the curve $({U})^{{2}}+y={tex(h)}$ and the line $y=0.$'
 else:eqs=f'the curve $({U})^{{2}}-({V})={tex(-k)}$ and the line ${V}={tex(k+h)}.$'
 return 'Using the change of variables \n\n'+display(f'u={U},\\,v={V},')+'\n\ncalculate the area of the finite region $D$ bounded by '+eqs
# Shared prose is the captured source template with complete mathematical blocks.
def solution(f,p,d,asset):
 anchor=FAMILIES[f][0] or 'q-83943';src=Q[anchor].get(':question/worked-solution',Q['q-83943'][':question/worked-solution'])
 opening=src[:src.index('**Step 1**')]
 opening=re.sub(r'\$\$\nu=.*?\n\$\$',lambda m:display('u='+tex(d['U'])+r',\,v='+tex(d['V'])),opening,flags=re.S)
 U,V=tex(d['U']),tex(d['V']);h,k=sp.Integer(p['h']),sp.Integer(p['k']);lo,hi=d['lo'],d['hi'];J=d['J'];weight=abs(J);pr=d['prim']
 out=opening+'**Step 1**: Find $Δ,$ which is the image of $D$ under the action of ${T}^{-1}.$\n\n'
 if f.startswith('hyper'):
  first_expr,first_var,second_expr,second_var=(V,'v',U,'u')if f=='hyper_x'else(U,'u',V,'v')
  out+=f'Substituting ${first_expr}={first_var}$ into the equation of the first line, we get\n\n'+display(f'{first_expr}={tex(k)}\\,⟹\\,{first_var}={tex(k)}.')
  out+=f'\n\nwhile substituting ${second_expr}={second_var}$ into the equation of the second line, we obtain\n\n'+display(f'{second_expr}={tex(k)}\\,⟹\\,{second_var}={tex(k)}.')
  curve_substitutions=f'${V}=v$ and ${U}=u$'if f=='hyper_x'else f'$u={U}$ and $v={V}$'
  out+='\n\nSubstituting '+curve_substitutions+' into the equation of curve, we get\n\n'+display(f'{tex(sp.expand(d["U"]*d["V"]))}={tex(h)}\\,⟹\\,({U})({V})={tex(h)}\\,⟹\\,uv={tex(h)}.')
  out+=f'\n\nThe intersection point of the two lines in the $uv$-plane is $({tex(k)},{tex(k)}).$'
  for index,(fixed,unknown) in enumerate([('v','u'),('u','v')]if f=='hyper_x'else[('u','v'),('v','u')]):
   intersection_word,line_word=('intersection','first')if index==0 else('intersections','second')
   out+=f'\n\nTo find the {intersection_word} of the curve with the {line_word} line in the $uv$-plane, we solve the following system:\n\n'+display(aligned([f'\\left\\{{\\begin{{aligned}}uv={tex(h)} \\\\ {fixed}={tex(k)}\\end{{aligned}}\\right.\\,⟹\\,\\left\\{{\\begin{{aligned}}{fixed}={tex(k)} \\\\ {unknown}={tex(h/k)}\\end{{aligned}}\\right.']))
  pts=f'$({tex(k)},{tex(k)}),$ $({tex(k)},{tex(h/k)})$ and $({tex(h/k)},{tex(k)}).$'
 else:
  out+=f'Substituting ${U}=u$ and ${V}=v$ into the equation of the first curve, we get\n\n'
  if f=='quartic':
   power=f'({U})^{{4}}'if h==1 else rf'\frac{{({U})^{{4}}}}{{{tex(h**3)}}}'
   out+=display(power+tex(-d['V'])+r'=0\,⟹\,'+power+f'-({V})=0'+r'\,⟹\,v='+tex(d['low'])+'.')
   inverse_y=rf'\frac{{u-v}}{{{tex(2*sp.Integer(p["a"]))}}}'
   out+='\n\nNow,\n\n'+display(aligned([r'\left\{\begin{aligned}'+U+r'=u \\ '+V+r'=v\end{aligned}\right.\,⟹\,y='+inverse_y+'.']))
   out+='\n\nSubstituting this value into the equation of the given line yields:\n\n'+display(r'y=0\,⟹\,'+inverse_y+r'=0\,⟹\,v=u.')
   sys=f'u(u^{{3}}-{tex(h**3)})=0';pts=f'$(0,0)$ and $({tex(h)},{tex(h)}).$'
  else:
   curve=f'({U})^{{2}}+y={tex(h)}' if f=='down' else f'({U})^{{2}}-({V})={tex(-k)}'
   transformed=f'v={tex(d["high"] if f=="down" else d["low"])}'
   middle=(f'(y+{tex(k)})={tex(h+k)}-({U})^{{2}}' if f=='down' else f'u^{{2}}-v={tex(-k)}')
   out+=display(curve+r'\,⟹\,'+middle+r'\,⟹\,'+transformed+'.')
   second_boundary_word='line'if f=='down'else'second curve'
   out+=f'\n\nwhile substituting ${V}=v$ into the equation of the {second_boundary_word}, we obtain\n\n'+display(f'v={tex(k if f=="down" else k+h)}.')
   sys=f'u=\\pm {tex(hi)}';pts=f'$(\\pm {tex(hi)},{tex(k if f=="down" else k+h)}).$'
  out+='\n\nTo find the intersections of the curves in the $uv$-plane, we solve the following system:\n\n'+display(aligned([r'\left\{\begin{aligned}v='+tex(d['low'])+r' \\ v='+tex(d['high'])+r'\end{aligned}\right.\,⟹\,'+sys]))
 out+='\n\nSo, the intersection points are '+pts+'\n\nTherefore, our domain in the $uv$-plane has the type I representation\n\n'+display(r'Δ=\{(u,v)\,:\,'+tex(lo)+r'\le u\le '+tex(hi)+r',\,'+tex(d['low'])+r'\le v\le '+tex(d['high'])+r'\}.')+'\n\n![]('+asset+')\n\n'
 out+='**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$\n\nThe Jacobian determinant corresponding to ${T}^{-1}$ is\n\n'
 mat=[sp.diff(d[z],t) for z in ['U','V'] for t in [x,y]]
 out+=display(aligned([r'\frac{∂(u,v)}{∂(x,y)} & =\left|\begin{matrix}\frac{∂u}{∂x}&\frac{∂u}{∂y}\\\frac{∂v}{∂x}&\frac{∂v}{∂y}\end{matrix}\right|',r'&=\left|\begin{matrix}'+tex(mat[0])+'&'+tex(mat[1])+r'\\'+tex(mat[2])+'&'+tex(mat[3])+r'\end{matrix}\right|',r'&='+tex(d['det'])]))
 out+='\n\n**Step 3**: Compute the Jacobian determinant corresponding to $T:$\n\nThe Jacobian determinant corresponding to $T$ is\n\n'+display(r'\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=('+tex(d['det'])+r')^{-1}='+tex(J)+'.')
 out+='\n\nNote that $\\frac{∂(x,y)}{∂(u,v)}\\ne 0$ everywhere inside $Δ.$  In other words, $T$ has no critical points inside $Δ.$\n\n**Step 4**: Compute the required area.\n\nWe calculate the required area by performing the change of variables:\n\n'
 # Separate structural masks: inner integration, boundary substitution, width,
 # primitive, every endpoint component, collection, final exact scalar.
 t=tex;factor=t(weight);bounds='_{'+t(lo)+'}^{'+t(hi)+'}'
 low,high=t(d['low']),t(d['high'])
 if f.startswith('hyper'):components=[h*sp.log(u),-k*u]
 elif f=='quartic':components=[u**2/2,-u**5/(5*h**3)]
 else:components=[h*u,-u**3/3]
 def endpoint(z):return '('+'+'.join('('+t(c.subs(u,z))+')' for c in components)+')'
 substituted='('+high+')-('+low+')'
 rows=[r'\iint_D dxdy &=\iint_Δ |\frac{∂(x,y)}{∂(u,v)}|\,dudv',r'&=\iint_Δ |'+t(J)+r'|\,dudv',r'&='+factor+r'\int'+bounds+r'[\int_{'+low+'}^{'+high+r'}dv]du',r'&='+factor+r'\int'+bounds+r'[v]_{'+low+'}^{'+high+r'}du',r'&='+factor+r'\int'+bounds+substituted+'du']
 if f not in ['hyper_x','hyper_y','quartic']:rows+=[r'&='+factor+r'\int'+bounds+'('+t(d['width'])+')du']
 rows+=[r'&='+factor+'['+t(pr)+']'+bounds,r'&='+factor+'('+endpoint(hi)+'-'+endpoint(lo)+')',r'&='+factor+'('+t(sp.simplify(pr.subs(u,hi)-pr.subs(u,lo)))+')',r'&='+t(d['A'])]
 out+=display(aligned(rows))
 return out

def record(question,bank,correct,spelling,level,seed,f,p,profile,eligible,extra=None,field_specs=None):
 content={'version':VERSION,'question':question,'bank':sorted(spelling),'correct':tex(correct)if correct is not None else None,'field_type':'radio','level':question.get(':question/difficulty')}
 if field_specs is not None:
  content={'version':VERSION,'question':question,'fields':[{'attributes':z['attributes'],'answers':sorted([{'value':val,'type':typ,**attrs}for val,typ,attrs in zip(z['spelling'],z['answer_types'],z['answer_attributes'])],key=lambda a:a['value']),'correct':tex(z['correct'])if z['correct']is not None else None}for z in field_specs]}
 fp=digest(content);qid=uid(fp);fid=uid(fp+'/selection')
 answers=[{':answer/id':uid(fid+'/'+val),':answer/type':':answer.type/math',':answer/value':val} for val in spelling]
 cid=next(z[':answer/id'] for z,m in zip(answers,bank) if eq(m,correct)) if correct is not None else None;random.Random(seed).shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}
 if cid is None:field.pop(':answer-field/correct')
 fields=[field]
 if field_specs is not None:
  fields=[]
  for index,z in enumerate(field_specs):
   owned_id=uid(fp+'/raw-field/'+str(index)+'/'+z['attributes'][':answer-field/key'])
   owned_answers=[{':answer/id':uid(owned_id+'/'+value),':answer/type':typ,':answer/value':value,**attrs}for value,typ,attrs in zip(z['spelling'],z['answer_types'],z['answer_attributes'])]
   owned_correct=next(answer[':answer/id']for answer,value in zip(owned_answers,z['bank'])if eq(value,z['correct']))if z['correct']is not None else None
   random.Random(seed+index).shuffle(owned_answers)
   owned_field={**z['attributes'],':answer-field/id':owned_id,':answer-field/choices':owned_answers}
   if owned_correct is not None:owned_field[':answer-field/correct']=[':answer/id',owned_correct]
   fields.append(owned_field)
 question[':question/id']=qid;question[':question/answer-fields']=fields
 task=digest({'f':f,'p':p,'level':question.get(':question/difficulty')})
 meta={'version':VERSION,'template':f,'profile':profile,'seed':seed,'parameters':p,'mathematical_fingerprint':task,'content_fingerprint':fp,'source':{k:SRC[k] for k in ['database','basis','lineage']},'eligible_for_learning':eligible,'evidence_only':not eligible,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}
 meta.update(extra or {})
 return {'knowledge_point':{'db_id':KP,'id':R[':knowledge-point/id'],'title':TITLE},'question':question,'generation':meta}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('level')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('radio only')
 rng=random.Random(seed)
 if profile and profile.startswith(('raw:','historical:')):
  prefix,sid=profile.split(':',1); historical=prefix=='historical'
  if sid not in (Q if historical else CURRENT_Q):raise ValueError('source id')
  return raw_generate(level,seed,sid,parameters,historical)
 allowed=[f for f,z in FAMILIES.items() if z[1]==level]
 f=template or rng.choice(allowed)
 if f not in allowed:raise ValueError('family difficulty mismatch')
 selected=profile or 'method'
 if selected!='method':raise ValueError('profile')
 candidates=candidate_instances(f,rng)
 target=rng.randrange(len(candidates))
 for _ in range(1):
  p=dict(parameters) if parameters is not None else dict(candidates[target][0]);guards(f,p);d=model(f,p);bank=recipes(f,d,p,selected,candidates)
  if all(not eq(bank[i],bank[j]) for i in range(5) for j in range(i)):
   asset=plot(f,p,d);sol=solution(f,p,d,asset);pr=prompt(f,p,d)
   for z in [pr,sol]+list(map(tex,bank)):format_ok(z)
   q={':question/problem':pr,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level}
   return record(q,bank,d['A'],list(map(tex,bank)),level,seed,f,p,selected,True,{'bank_construction':'compatible-instance-areas','bank_parameters':[cp for cp,_ in candidates],'source_question':FAMILIES[f][0],'plot':asset,'domain':{z:str(d[z]) for z in ['lo','hi','low','high']}})
  if parameters is not None:raise ValueError('complete bank collision')
 raise ValueError('no eligible instance')
# Easy: authored unit-determinant, zero-shift square-gap family.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: authored canonical mixed map and nonunit determinant.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: six observed backbones, with their distinct operative stages.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 fields=q.get(':question/answer-fields',[])
 for index,field in enumerate(fields):
  if len(fields)>1:s+='Captured field '+str(index)+' (`'+field[':answer-field/key']+'`)\n\n'
  for a in field.get(':answer-field/choices',[]):s+='- $'+a[':answer/value']+'$\n'
 if ':question/worked-solution'in q:s+='\n'+q[':question/worked-solution']
 return s
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
 if args.count<1:a.error('--count must be positive')
 results=[]
 for level in (['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty]):
  capacities={'simple':48,'mixed':42,'quartic':24,'hyper_y':176,'hyper_x':176,'down':256,'up':960,'vertical':960}
  limit=1 if args.profile and args.profile.startswith(('raw:','historical:')) else capacities[args.template] if args.template else sum(capacities[f]for f,(_,band)in FAMILIES.items()if band==level)
  if args.count>limit:a.error(f'finite catalog limit for {level}: {limit}; requested {args.count}')
  seen=set();selected=[]
  for offset in range(500+args.count*200):
   rec=generate(level,args.seed+offset,template=args.template,profile=args.profile)
   task=rec['generation']['mathematical_fingerprint']
   if task in seen:continue
   seen.add(task);selected.append(rec)
   if len(selected)==args.count:break
  if len(selected)!=args.count:
   a.error(f'bounded sampling exhausted: {len(selected)} distinct {level} questions; requested {args.count}')
  results.extend(selected)
 print(json.dumps(results,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n---\n\n'.join(map(markdown,results)))
