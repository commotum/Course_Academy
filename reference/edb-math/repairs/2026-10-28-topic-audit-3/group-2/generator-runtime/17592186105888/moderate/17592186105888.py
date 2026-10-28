#!/usr/bin/env python3
"""Surface integrals in polar coordinates; validated inventory generator.
Source refresh basis 2721; historical basis 1356 retained under reference/. Observed opaque banks are public evidence profiles, never defaults.
Raw templates permit a vertical plane translation h: this is deliberately an
incidental parameter, excluded from assessed-task identity. Its sparse historical
banks cannot justify new numeric error recipes. Normal families instead use
complete banks obtained from omitted/squared metric and genuine bound errors.
Easy: constant density disk. Moderate: one linear density, integer unit slopes.
Hard: observed families; linear densities require larger metric arithmetic.
All bounds apply equally to explicit parameters and deterministic samplers.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, sys, uuid
from pathlib import Path
import sympy as sp
KP=17592186105888; TITLE='Evaluating Surface Integrals Using Polar Coordinates'
VERSION='polar-surface-3'; ROOT=Path(__file__).resolve().with_suffix('')
X,Y,R,T=sp.symbols('x y r theta',real=True)
NS=uuid.UUID('65e5d5ea-f579-5871-924d-075a207c9aa7')
FAMILIES=('x','y','xy','xy2','x_over_r2','x2y','exp','linear','xy_over_r2','radialpoly','r2','radialsqrt')
REGIONS={'disk':(0,2*sp.pi),'q1':(0,sp.pi/2),'q2':(sp.pi/2,sp.pi),'q4':(3*sp.pi/2,2*sp.pi),'upper':(0,sp.pi),'right':(-sp.pi/2,sp.pi/2),'left':(sp.pi/2,3*sp.pi/2)}
SOURCE_CONFIG={
'q-161146':('x',3,1,-1,2,'q1'),'q-161302':('r2',1,2,-1,2,'disk'),
'q-161291':('y',6,1,1,1,'upper'),'q-161300':('xy',8,-2,1,2,'q1'),
'q-161301':('xy2',5,2,2,2,'right'),'q-161311':('x_over_r2',1,-1,sp.sqrt(2),3,'q2'),
'q-161318':('x2y',3,-4,sp.sqrt(8),1,'upper'),'q-161322':('exp',1,1,sp.sqrt(3),2,'disk'),
'q-161339':('linear',1,-2,2,1,'left'),'q-161316':('xy_over_r2',4,1,-sp.sqrt(2),3,'q4'),
'q-161338':('radialpoly',1,4,sp.sqrt(3),1,'disk'),
'q-161328':('radialsqrt',1,4,sp.sqrt(8),2,'disk')}
def tex(e): return sp.latex(sp.sympify(e)).replace(r'\log',r'\ln')
def canonical(e): return sp.srepr(sp.simplify(e))
def digest(o): return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(NS,s))
def expr(f,k,c=1):
 return {'constant':k,'radialsqrt':k*sp.sqrt(X**2+Y**2),'x':k*X,'y':k*Y,'xy':k*X*Y,'xy2':k*X*Y**2,'x2y':k*X**2*Y,'x_over_r2':k*X/(X**2+Y**2),'xy_over_r2':k*X*Y/(X**2+Y**2),'r2':k*(X**2+Y**2),'exp':k*sp.exp(X**2+Y**2),'linear':k*(X+Y),'radialpoly':k*(c-X**2-Y**2)}[f]
def components(f,k,c=1):
 return {'constant':(k*R,1),'radialsqrt':(k*R**2,1),'x':(k*R**2,sp.cos(T)),'y':(k*R**2,sp.sin(T)),'xy':(k*R**3,sp.sin(T)*sp.cos(T)),'xy2':(k*R**4,sp.cos(T)*sp.sin(T)**2),'x2y':(k*R**4,sp.cos(T)**2*sp.sin(T)),'x_over_r2':(k,sp.cos(T)),'xy_over_r2':(k*R,sp.cos(T)*sp.sin(T)),'r2':(k*R**3,1),'exp':(k*R*sp.exp(R**2),1),'linear':(k*R**2,sp.sin(T)+sp.cos(T)),'radialpoly':(k*(c*R-R**3),1)}[f]
def params(level,f,rng):
 reg={'constant':['disk'],'radialsqrt':['disk'],'x':['q1','q2','right'],'y':['q1','q4','upper'],'xy':['q1','q2','q4'],'xy2':['q1','q2','right'],'x2y':['q1','q4','upper'],'x_over_r2':['q1','q2','right'],'xy_over_r2':['q1','q2','q4'],'linear':['q1','left','right'],'exp':['disk'],'r2':['disk'],'radialpoly':['disk']}[f]
 slopes=[-1,1] if level!='hard' else [-4,-2,-1,1,2,4,sp.sqrt(2),-sp.sqrt(2),sp.sqrt(3),sp.sqrt(8),-sp.sqrt(8)]
 p=dict(k=rng.randint(1,6 if level!='hard' else 8),a=str(rng.choice(slopes)),b=str(rng.choice(slopes)),radius=rng.randint(1,3),region=rng.choice(reg))
 p['c']=p['radius']**2 if f=='radialpoly' else 1
 return p
def guard(level,f,p):
 if set(p)-{'k','a','b','radius','region','c'}:raise ValueError('unused parameter')
 for key in ('k','radius','c'):
  if not isinstance(p[key],int) or isinstance(p[key],bool):raise ValueError('integer workload')
 if not 1<=p['radius']<=3 or not 1<=p['k']<=(8 if level=='hard' else 6):raise ValueError('workload bound')
 a,b=sp.sympify(p['a']),sp.sympify(p['b'])
 allowed=[-1,1] if level!='hard' else [-4,-2,-1,1,2,4,sp.sqrt(2),-sp.sqrt(2),sp.sqrt(3),sp.sqrt(8),-sp.sqrt(8)]
 if a not in allowed or b not in allowed:raise ValueError('slope workload')
 if p['region'] not in REGIONS:raise ValueError('region')
 if f in ('constant','exp','r2','radialpoly','radialsqrt') and p['region']!='disk':raise ValueError('radial disk family')
 if level=='easy' and f!='constant':raise ValueError('easy constant density')
 if level=='moderate' and f not in ('x','y'):raise ValueError('moderate single linear density')
 if level=='hard' and f not in FAMILIES:raise ValueError('hard observed family')
 if level=='hard' and f in ('x','y') and a*a+b*b<5:raise ValueError('hard linear metric workload')
 if f=='radialpoly':
  if not p['radius']**2<=p['c']<=p['radius']**2+3:raise ValueError('radial polynomial workload')
 elif p['c']!=1:raise ValueError('unused c')
 return a,b

def render_plot(p,output_dir=None):
 """Fixed saved canvas; measured transforms/labels and independent raster checks.
 All concurrent outputs use private unique temporary paths. Existing caches stay.
 """
 key=digest(['region-render-5',p['radius'],p['region']]);out=(Path(output_dir) if output_dir is not None else ROOT/'plots')/f'{key}.png';side=out.with_suffix('.json')
 if out.exists() and side.exists():return str(out.relative_to(Path(__file__).resolve().parents[2]))
 os.environ.setdefault('MPLCONFIGDIR','/tmp/kp105888-mpl');import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt;import numpy as np
 from PIL import Image
 rr=p['radius'];lo,hi=map(float,REGIONS[p['region']]);theta=np.linspace(lo,hi,721)
 fig=plt.figure(figsize=(3.6,3.15),dpi=140);ax=fig.add_axes([.09,.09,.82,.82]);lim=rr*1.53
 ax.set(xlim=(-lim,lim),ylim=(-lim,lim),aspect='equal');ax.axis('off')
 fill=ax.fill(np.r_[0,rr*np.cos(theta),0],np.r_[0,rr*np.sin(theta),0],color='#e0ebf4',ec='#2471b9',lw=1.3)[0]
 arrow=lim*.88
 for tail,tip in [((-arrow,0),(arrow,0)),((0,-arrow),(0,arrow))]:ax.annotate('',xy=tip,xytext=tail,arrowprops={'arrowstyle':'->','lw':.8,'color':'black'})
 labels=[ax.text(arrow+rr*.12,-rr*.10,'$x$',fontsize=11,ha='center',va='top'),ax.text(rr*.12,arrow+rr*.10,'$y$',fontsize=11,ha='left',va='center'),ax.text(-rr*.13,-rr*.13,'$O$',fontsize=10,ha='right',va='top')]
 for vx,vy in [(rr,0),(-rr,0),(0,rr),(0,-rr)]:
  angle=np.arctan2(vy,vx)%(2*np.pi)
  if lo<=angle<=hi or lo<=angle+2*np.pi<=hi or (lo<0 and (angle>2*np.pi+lo or angle<=hi)) or p['region']=='disk':
   if vx:labels.append(ax.text(vx+np.sign(vx)*rr*.16,-rr*.19,str(vx),fontsize=9,ha='center',va='top'))
   else:labels.append(ax.text(rr*.16,vy+np.sign(vy)*rr*.17,str(vy),fontsize=9,ha='left',va='center'))
 fig.canvas.draw();rend=fig.canvas.get_renderer();width,height=fig.canvas.get_width_height();origin=ax.transData.transform((0,0));scale=(ax.transData.transform((1,1))-origin).tolist()
 boxes=[]
 for label in labels:
  b=label.get_window_extent(rend);boxes.append({'text':label.get_text(),'bbox_saved_pixels':[float(b.x0),float(height-b.y1),float(b.x1),float(height-b.y0)],'bbox_display_pixels':list(map(float,[b.x0,b.y0,b.x1,b.y1])),'mask':False})
 out.parent.mkdir(parents=True,exist_ok=True);tmp=out.with_name(out.stem+'.'+uuid.uuid4().hex+'.png');fig.savefig(tmp,dpi=fig.dpi,facecolor='white');plt.close(fig)
 saved_image=Image.open(tmp);saved_png_dpi=list(saved_image.info.get('dpi',[]));assert saved_image.size==(width,height)
 pixels=np.array(saved_image.convert('RGB'));blue=(pixels[:,:,2]>pixels[:,:,0]+20)&(pixels[:,:,0]<100)&(pixels[:,:,1]>60)
 filled=(abs(pixels[:,:,0].astype(int)-224)<3)&(abs(pixels[:,:,1].astype(int)-235)<3)&(abs(pixels[:,:,2].astype(int)-244)<3)
 black=np.max(pixels,axis=2)<100
 def clearance(mask,box):
  yy,xx=np.where(mask);x0,y0,x1,y1=box;dx=np.maximum(np.maximum(x0-xx,xx-x1),0);dy=np.maximum(np.maximum(y0-yy,yy-y1),0)
  return float(np.sqrt(dx*dx+dy*dy).min()) if len(xx) else None
 # Blue ink includes circular arc and radial sector edges. Axes are checked from
 # their actual saved-coordinate transform (text ink cannot pretend to be axes).
 saved_origin=[float(origin[0]),float(height-origin[1])];lineclear=[]
 for b in boxes:
  box=b['bbox_saved_pixels'];x0,y0,x1,y1=box
  axis_clear=min(0 if y0<=saved_origin[1]<=y1 else min(abs(y0-saved_origin[1]),abs(y1-saved_origin[1])),0 if x0<=saved_origin[0]<=x1 else min(abs(x0-saved_origin[0]),abs(x1-saved_origin[0])))
  b['axis_clearance_px']=float(axis_clear);b['blue_ink_clearance_px']=clearance(blue,box);b['black_ink_pixels_in_bbox']=int(black[max(0,int(y0)):min(height,int(np.ceil(y1))),max(0,int(x0)):min(width,int(np.ceil(x1)))].sum())
  assert b['axis_clearance_px']>=4 and b['blue_ink_clearance_px']>=4 and b['black_ink_pixels_in_bbox']>0,b
  assert 0<=x0<x1<width and 0<=y0<y1<height
 for i,b in enumerate(boxes):
  b['other_label_clearance_px']=min([float(np.hypot(max(c['bbox_saved_pixels'][0]-b['bbox_saved_pixels'][2],b['bbox_saved_pixels'][0]-c['bbox_saved_pixels'][2],0),max(c['bbox_saved_pixels'][1]-b['bbox_saved_pixels'][3],b['bbox_saved_pixels'][1]-c['bbox_saved_pixels'][3],0))) for j,c in enumerate(boxes) if i!=j])
  assert b['other_label_clearance_px']>=4
 # Arc ink at 17 interior angles must occur within a 3px antialias/stroke disk.
 arc_checks=[]
 for ang in np.linspace(lo,hi,19)[1:-1]:
  px=origin[0]+scale[0]*rr*np.cos(ang);py=height-origin[1]-scale[1]*rr*np.sin(ang);ix,iy=int(round(px)),int(round(py));present=bool(blue[iy-3:iy+4,ix-3:ix+4].any());arc_checks.append(present);assert present
 # Pixel-based area, radius and orientation use actual saved transform.
 yy,xx=np.where(filled);dx=(xx-origin[0])/scale[0];dy=(height-yy-origin[1])/scale[1];rad=np.hypot(dx,dy)
 assert len(rad)>0 and float(rad.max())<=rr+3/scale[0]
 expected_area=(hi-lo)*rr*rr*.5*scale[0]*scale[1];relative_area_error=abs(len(rad)-expected_area)/expected_area;area_stroke_allowance=(2.8*(rr*(hi-lo+2)+4*rr)*scale[0])/expected_area;assert relative_area_error<area_stroke_allowance,(p,relative_area_error,area_stroke_allowance)
 grid_y,grid_x=np.indices((height,width));gx=(grid_x-origin[0])/scale[0];gy=(height-grid_y-origin[1])/scale[1];ga=np.arctan2(gy,gx);ga=np.where(ga<lo,ga+2*np.pi,ga);interior=(np.hypot(gx,gy)<rr-4/scale[0])&(ga>lo+.035)&(ga<hi-.035)&(abs(gx)>4/scale[0])&(abs(gy)>4/scale[1])
 for box in boxes:
  x0,y0,x1,y1=box['bbox_saved_pixels'];interior&=~((grid_x>=x0-1)&(grid_x<=x1+1)&(grid_y>=y0-1)&(grid_y<=y1+1))
 interior_fill_coverage=float(filled[interior].mean());assert interior_fill_coverage>.995
 angles=np.arctan2(dy,dx);angles=np.where(angles<lo,angles+2*np.pi,angles);orientation_fraction=float(((angles>=lo-.03)&(angles<=hi+.03)).mean());assert orientation_fraction>.995
 aspect_error=abs(scale[0]/scale[1]-1);assert aspect_error<1e-10
 png_hash=hashlib.sha256(tmp.read_bytes()).hexdigest();os.replace(tmp,out)
 meta={'renderer_version':'region-render-5','radius':rr,'region':p['region'],'angles':[str(v) for v in REGIONS[p['region']]],'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'saved_dpi':140,'actual_png_dpi':saved_png_dpi,'axes_data_bounds':[-lim,lim,-lim,lim],'stroke_width_px':1.3*140/72,'fill_rgb':[224,235,244],'arc_rgb':[36,113,185],'saved_size_px':[width,height],'saved_coordinate_transform':{'origin_px':saved_origin,'x_pixels_per_unit':scale[0],'y_pixels_per_unit':-scale[1]},'png_sha256':png_hash,'text_boxes':boxes,'pixel_qa':{'arc_samples_present':arc_checks,'filled_pixels':int(len(rad)),'expected_filled_area_px':float(expected_area),'relative_area_error':float(relative_area_error),'area_stroke_allowance':float(area_stroke_allowance),'interior_fill_coverage':interior_fill_coverage,'max_filled_radius':float(rad.max()),'orientation_fraction':orientation_fraction,'aspect_error':float(aspect_error)},'geometry':'equal-scale filled sector','text_masks':False}
 tmp=side.with_name(side.stem+'.'+uuid.uuid4().hex+'.json');tmp.write_text(json.dumps(meta));os.replace(tmp,side)
 return str(out.relative_to(Path(__file__).resolve().parents[2]))

def endpoint_terms(F,var,value):
 terms=list(sp.Add.make_args(sp.expand(F)));printed=''.join(tex(F).split())
 terms.sort(key=lambda term:printed.find(''.join(tex(-term if term.could_extract_minus_sign() else term).split())))
 return [sp.simplify(t.subs(var,value)) for t in terms]
def sum_tex(terms): return '+'.join('('+tex(v)+')' for v in terms)
REGION_NAMES={'disk':'disk','q1':'quarter-circle in the first quadrant','q2':'quarter-circle in the second quadrant','q4':'quarter-circle in the fourth quadrant','upper':'upper half-circle','right':'right half-circle','left':'left half-circle'}
def density_tex(f,k,c=1):
 prefix='' if k==1 else tex(k)
 if f=='radialpoly':return prefix+'('+tex(c)+r'-x^2-y^2)'
 if f=='linear':return prefix+'(x+y)'
 if f=='r2':return prefix+r'(x^2+y^2)'
 return tex(expr(f,k,c))
def integral(body,var,lo,hi):
 return r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}{'+body+r'}\,\mathrm{d}'+('\\theta' if var==T else 'r')
def bracket(body,var,lo,hi):
 return r'\left['+body+r'\right]_{'+tex(lo)+'}^{'+tex(hi)+'}'
def aligned(lhs,rows):
 return '$$\n'+r'\begin{aligned}'+lhs+' & ='+rows[0]+''.join(r' \\ & ='+row for row in rows[1:])+r'.\end{aligned}'+'\n$$'
def dsint(body,domain='D'):
 return r'\iint_'+domain+'{'+body+r'}\,\mathrm{d}'+('S' if domain=='S' else 'A' if domain=='D' else r'r\,\mathrm{d}\theta')
def evaluated(primitive,var,lo,hi,ordered=None):
 if ordered is not None:
  upper=[sp.simplify(term.subs(var,hi)) for term in ordered];lower=[sp.simplify(term.subs(var,lo)) for term in ordered]
  return r'\left[('+sum_tex(upper)+')-('+sum_tex(lower)+r')\right]'
 return r'\left[('+sum_tex(endpoint_terms(primitive,var,hi))+')-('+sum_tex(endpoint_terms(primitive,var,lo))+r')\right]'
def source_solution(f,p):
 """Source-shaped fixed chains. No teaching helper symbols are introduced.
 Keep theta-first integration for q-161311's ratio; all other observed families
 integrate r first. Quotient denominators and Pythagorean cancellation are
 unevaluated masks, not a CAS collapse. Endpoint component rows are additions
 to the source chains, explicitly reported as normal pedagogical expansion.
 """
 k=p['k'];rr=p['radius'];c=p.get('c',1);a,b=sp.sympify(p['a']),sp.sympify(p['b']);lo,hi=REGIONS[p['region']]
 density=sp.sympify(expr(f,k,c));density_text=density_tex(f,k,c);plane=a*X+b*Y;sq=1+a*a+b*b;metric=sp.sqrt(sq);mt='('+tex(metric)+')'
 radial,angular=map(sp.sympify,components(f,k,c))
 # q-161316 retains its observed double-angle simplification.
 if f in ('xy','xy_over_r2'):radial=k*(R**3 if f=='xy' else R)/2;angular=sp.sin(2*T)
 primr=sp.integrate(radial,R);primt=sp.integrate(angular,T)
 primr_text=(r'\frac{'+tex(k*c*R**2)+r'}{2}-\frac{'+tex(k*R**4)+'}{4}') if f=='radialpoly' else tex(primr)
 primr_order=(k*c*R**2/2,-k*R**4/4) if f=='radialpoly' else None
 rv=sp.simplify(primr.subs(R,rr)-primr.subs(R,0));tv=sp.simplify(primt.subs(T,hi)-primt.subs(T,lo));result=sp.simplify(metric*rv*tv)
 text='For a surface $S$ defined by $z=g(x,y)$ with $(x,y)\\in D,$ the surface integral of a scalar function $f(x,y,z)$ over $S$ is given by\n\n'+r'$$\iint_S f(x,y,z)\,\mathrm{d}S=\iint_D f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}\,\mathrm{d}A.$$'+'\n\nFor the partial derivatives, we have\n\n'+r'$$\frac{\partial z}{\partial x}=\frac{\partial}{\partial x}('+tex(plane)+')='+tex(a)+',$$\n\nand\n\n'+r'$$\frac{\partial z}{\partial y}=\frac{\partial}{\partial y}('+tex(plane)+')='+tex(b)+'.$$\n\nTherefore, the surface integral can be expressed as follows:\n\n'
 metric_rows=[dsint(r'f(x,y,g(x,y))\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+\left(\frac{\partial z}{\partial y}\right)^2}'),dsint('('+density_text+r')\cdot\sqrt{1+('+tex(a)+')^2+('+tex(b)+')^2}'),dsint('('+density_text+r')\cdot\sqrt{'+tex(sq)+'}'),mt+dsint(density_text)]
 text+=aligned(dsint(density_text,'S'),metric_rows)
 text+='\n\nNotice that in polar coordinates $(r,\\theta),$ our domain can be expressed as\n\n'+r'$$\Delta=\{(r,\theta):0\le r\le '+str(rr)+r',\ '+tex(lo)+r'\le\theta\le '+tex(hi)+r'\}.$$'+'\n\nTherefore, using the change of variables formula for polar coordinates, where $x=r\\cos\\theta$ and $y=r\\sin\\theta,$ we obtain\n\n'
 rc=r'r\cos\theta';rs=r'r\sin\theta';den=r'r^2\cos^2\theta+r^2\sin^2\theta';K='' if k==1 else tex(k)
 sub={'constant':tex(k),'radialsqrt':K+r'\sqrt{'+den+'}','x':K+'('+rc+')','y':K+'('+rs+')','xy':K+'('+rc+')('+rs+')','xy2':K+'('+rc+')('+rs+')^2','x2y':K+'('+rc+')^2('+rs+')','x_over_r2':r'\frac{'+K+'('+rc+')}{'+den+'}','xy_over_r2':r'\frac{'+K+'('+rc+')('+rs+')}{'+den+'}','linear':K+'('+rc+'+'+rs+')','exp':K+r'e^{'+den+'}','r2':K+'('+den+')','radialpoly':K+'('+tex(c)+'-r^2'+r'\cos^2\theta-r^2\sin^2\theta)'}[f]
 rows=[mt+dsint(r'f(r\cos\theta,r\sin\theta)\cdot r',r'\Delta'),mt+dsint('('+sub+r')\cdot r',r'\Delta')];roles=['polar_formula','coordinate_substitution_with_jacobian']
 if f in ('x_over_r2','xy_over_r2'):
  numerator=K+r'r^2\cos\theta' if f=='x_over_r2' else K+r'r^3\cos\theta\sin\theta'
  rows.append(mt+dsint(r'\frac{'+numerator+r'}{r^2(\cos^2\theta+\sin^2\theta)}',r'\Delta'));roles.append('quotient_pythagorean_factor')
 radial_text=(tex(k*c*R)+'-'+tex(k*R**3)) if f=='radialpoly' else tex(radial)
 angular_text=r'\cos\theta\sin^2\theta' if f=='xy2' else r'\cos^2\theta\sin\theta' if f=='x2y' else r'\cos\theta+\sin\theta' if f=='linear' else tex(angular)
 polar_text=tex(sp.expand(radial)*angular)
 if f in ('xy2','x2y'):polar_text=tex(radial)+angular_text
 if f=='linear':polar_text=tex(radial)+'('+angular_text+')'
 if f=='radialpoly':polar_text=radial_text
 rows.append(mt+dsint(polar_text,r'\Delta'));roles.append('polar_reduction')
 if f=='x_over_r2':
  rows.append(mt+integral(integral(tex(angular),T,lo,hi),R,0,rr));roles.append('theta_first_repeated_integral')
  rows.append(mt+integral(bracket(tex(primt),T,lo,hi),R,0,rr));roles.append('angular_primitive')
  rows.append(mt+integral(evaluated(primt,T,lo,hi),R,0,rr));roles.append('angular_individual_endpoints')
  rows.append(mt+integral(tex(tv),R,0,rr));roles.append('angular_collection')
  # k belongs to the radial component; it must not disappear in theta-first rows.
  if k!=1:
   for i in range(4,len(rows)):rows[i]= '('+tex(k*metric)+')'+rows[i][len(mt):]
  rows.append('('+tex(metric*tv)+')'+bracket(primr_text,R,0,rr));roles.append('radial_primitive')
  rows.append('('+tex(metric*tv)+')'+evaluated(primr,R,0,rr,primr_order));roles.append('radial_individual_endpoints')
 else:
  angular_factor='' if angular==1 else '('+angular_text+')'
  rows.append(mt+integral(angular_factor+integral(radial_text,R,0,rr),T,lo,hi));roles.append('r_first_repeated_integral')
  rows.append(mt+integral(angular_factor+bracket(primr_text,R,0,rr),T,lo,hi));roles.append('radial_primitive')
  rows.append(mt+integral(angular_factor+evaluated(primr,R,0,rr,primr_order),T,lo,hi));roles.append('radial_individual_endpoints')
  rows.append(mt+integral(tex(rv*angular),T,lo,hi));roles.append('radial_collection')
  angular_primitive=-sp.cos(2*T) if f in ('xy','xy_over_r2') else -sp.cos(T)**3 if f=='x2y' else primt
  angular_coefficient=metric*rv/2 if f in ('xy','xy_over_r2') else metric*rv/3 if f=='x2y' else metric*rv
  rows.append('('+tex(angular_coefficient)+')'+bracket(tex(angular_primitive),T,lo,hi));roles.append('angular_primitive')
  rows.append('('+tex(angular_coefficient)+')'+evaluated(angular_primitive,T,lo,hi));roles.append('angular_individual_endpoints')
 if f=='x_over_r2':arithmetic='('+tex(metric)+r')\cdot('+tex(tv)+r')\cdot('+tex(rv)+')'
 else:
  arithmetic_primitive=sp.sin(T)**3 if f=='xy2' else angular_primitive
  arithmetic_coefficient=metric*rv/3 if f=='xy2' else angular_coefficient
  arithmetic='('+tex(arithmetic_coefficient)+r')\cdot(('+tex(sp.simplify(arithmetic_primitive.subs(T,hi)))+')-('+tex(sp.simplify(arithmetic_primitive.subs(T,lo)))+'))'
 rows.append(arithmetic);roles.append('final_arithmetic')
 rows.append(tex(result));roles.append('final_value')
 text+=aligned(mt+dsint(density_text),rows)+'\n\nTherefore, the surface integral is $'+tex(result)+'$.'
 return text,{'family':f,'metric_roles':['formal_surface','metric_substitution','metric_radicand','metric_extracted'],'polar_roles':roles,'inner_variable':'theta' if f=='x_over_r2' else 'r','endpoint_expansion':'individual primitive terms at both endpoints'}

def normal(level,seed,f,p,profile):
 a,b=guard(level,f,p);k=p['k'];radius=p['radius'];lo,hi=REGIONS[p['region']];density=sp.sympify(expr(f,k,p['c']));plane=a*X+b*Y;metric=sp.sqrt(1+a*a+b*b)
 U,V=map(sp.sympify,components(f,k,p['c']));F=sp.integrate(U,R);G=sp.integrate(V,T);fr=sp.simplify(F.subs(R,radius)-F.subs(R,0));gt=sp.simplify(G.subs(T,hi)-G.subs(T,lo));correct=sp.simplify(metric*fr*gt)
 # Whole bank chosen before parameters. Every wrong result is the integral after
 # a specific method error, rather than a perturbation of the final scalar.
 if profile=='bounds': wrong=[sp.simplify(fr*gt),sp.simplify(metric**2*fr*gt),sp.simplify(metric*fr*sp.integrate(V,(T,lo,(lo+hi)/2))),sp.simplify(metric*sp.integrate(U,(R,0,sp.Rational(radius,2)))*gt)]
 else:raise ValueError('unknown authored complete bank')
 bank=[correct]+wrong
 if any(v.has(sp.oo,sp.nan,sp.zoo) or v.is_real is False for v in bank) or correct==0 or any(sp.simplify(v-w)==0 for i,v in enumerate(bank) for w in bank[:i]):raise ValueError('whole bank rejected: domain/collision')
 plot=render_plot(p)
 prompt=f'![]({plot})\n\nEvaluate the surface integral\n\n$$\\iint_S {density_tex(f,k,p['c'])}\\,\\mathrm{{d}}S,$$\n\nwhere $S$ is defined by $z={tex(plane)}$ and whose domain is the {REGION_NAMES[p["region"]]} of radius ${radius}$ centered at $O$, as shown above. Give an exact answer.'
 if f.endswith('over_r2'):prompt+=' The value at $O$ may be assigned arbitrarily; it does not affect the integral.'
 sol,layout=source_solution(f,p)

 vals=[tex(v) for v in bank];math_key=digest([canonical(density),canonical(plane),radius,canonical(lo),canonical(hi)])
 rec=assemble(level,seed,f,p,prompt,sol,vals,0,math_key,profile,True)
 sidecar=Path(__file__).resolve().parents[2]/Path(plot).with_suffix('.json')
 rec['generation']['solution_layout']=layout
 rec['generation']['plot']={'path':plot,'sidecar':str(Path(plot).with_suffix('.json')),'geometry':json.loads(sidecar.read_text())}
 rec['generation']['dependencies']['matplotlib']=rec['generation']['plot']['geometry']['matplotlib']
 return rec

def assemble(level,seed,f,p,prompt,sol,vals,correct_index,math_key,profile,eligible,raw=None):
 content=digest([VERSION,level,prompt,sol,sorted(vals), None if correct_index is None else vals[correct_index]])
 q={':question/id':uid(content),':question/problem':prompt}
 if level is not None:q[':question/difficulty']=':question.difficulty/'+level
 if sol is not None:q[':question/worked-solution']=sol
 field_id=uid(content+':selection');answers=[{':answer/id':uid(content+':selection:'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
 field={':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if correct_index is not None:field[':answer-field/correct']=[':answer/id',answers[correct_index][':answer/id']]
 random.Random(seed).shuffle(answers);q[':question/answer-fields']=[field]
 if raw:q[':question/math-academy-id']=raw
 return {'knowledge_point':{'db_id':KP,'id':str(NS),'title':TITLE},'question':q,'generation':{'version':VERSION,'template':f,'profile':profile,'parameters':p,'seed':seed,'mathematical_fingerprint':math_key,'content_fingerprint':content,'eligible_for_learning':eligible,'evidence_only':not eligible,'source':{'database':'math','basis':2721,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def raw_replay(source_id,seed,parameters):
 """Interpolate extracted full-component surface slots; preserve omissions/banks.
 h translates the plane vertically, changing the displayed surface and derivative
 arguments but no evaluated density/metric/integral. No inferred key is inserted.
 """
 spec=json.loads((ROOT/'raw-templates.json').read_text())[source_id];p={'h':0} if parameters is None else dict(parameters)
 if set(p)!={'h'} or not isinstance(p['h'],int) or isinstance(p['h'],bool) or not -3<=p['h']<=3:raise ValueError('raw h integer -3..3')
 def interpolate(s):
  if s is None:return None
  plane=spec['plane']; translated=plane if p['h']==0 else '('+plane+')'+('+' if p['h']>0 else '')+str(p['h'])
  return s.replace('@@PLANE@@',translated)
 prompt=interpolate(spec['problem']);sol=interpolate(spec.get('solution'));values=spec['values'];idx=spec.get('correct_index');f,k,a,b,rr,reg=SOURCE_CONFIG[source_id]
 lo,hi=REGIONS[reg]
 key=digest([canonical(expr(f,k)),canonical(a*X+b*Y),rr,canonical(lo),canonical(hi)])
 return assemble(spec.get('level'),seed,source_id,p,prompt,sol,values,idx,key,'original:'+source_id,False,source_id)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 if profile and profile.startswith('original:'):
  sid=profile.split(':',1)[1]
  if template not in (None,sid):raise ValueError('raw template/profile conflict')
  return raw_replay(sid,seed,parameters)
 rng=random.Random(seed);families=['constant'] if level=='easy' else ['x','y'] if level=='moderate' else list(FAMILIES)
 f=template or rng.choice(families)
 if f not in families:raise ValueError('family level')
 # Profile selected once, before sampling. Bound bank serves all families.
 chosen=profile or 'bounds'
 if parameters is not None:
  p=dict(parameters);p.setdefault('c',1);return normal(level,seed,f,p,chosen)
 for _ in range(200):
  p=params(level,f,rng)
  try:return normal(level,seed,f,p,chosen)
  except ValueError:pass
 raise ValueError('no whole-bank eligible instance')
# Easy: authored constant density and elementary radial primitive, no trig primitive.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: authored one linear term; unit slopes; one familiar trig primitive.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: observed integrand families, signed/radical metrics or rational/radial reduction.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(rec):
 q=rec['question'];s=q[':question/problem'];import re
 s=re.sub(r'!\[\]\((.*?)\)',lambda m:'![]('+str((Path(__file__).resolve().parents[2]/m[1]).resolve())+')' if m[1].startswith('generate/scratch/') else '![](/media/jake/SSD/EDB/math/'+m[1]+')',s)
 s+='\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices'])
 return s+'\n\n'+q.get(':question/worked-solution','[Source has no worked solution.]')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
