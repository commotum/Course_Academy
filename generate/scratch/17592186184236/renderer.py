"""Matplotlib only, exact-instance plotting and measured raster QA.

Use .venv driver; fallback to existing read-only cached Python3.10 wheels.
No installation, direct SVG generation, image generation or masking boxes.
"""
import hashlib,json,math,os,re,subprocess,sys,tempfile
from fractions import Fraction
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186184236-mpl'
paths={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates:raise RuntimeError('missing cached dependency '+package)
  p=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(p));paths[package]=str(p.resolve())
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def math_fraction(v,pi=False):
 v=Fraction(v);n,d=v.numerator,v.denominator
 sign='-' if n<0 else '';n=abs(n)
 if pi:
  numerator=(str(n) if n!=1 else '')+r'\pi'
 else:numerator=str(n)
 return sign+(numerator if d==1 else r'\frac{'+numerator+'}{'+str(d)+'}')

data=json.loads(Path(sys.argv[1]).read_text());p=data['instance'];B=Fraction(p['B']);D=Fraction(p['D']);c=p['calibration']
b=float(B);d=float(D);H=math.pi/(2*b)
fig,ax=plt.subplots(figsize=(5.6,4.9),dpi=130)
fig.subplots_adjust(left=.16,right=.95,bottom=.18,top=.93)
ax.set_xlim(-1.2*H,1.2*H);low=min(-4,d-3.5);high=max(4,d+3.5);ax.set_ylim(low,high);ax.axis('off')
ax.annotate('',xy=(1.18*H,0),xytext=(-1.18*H,0),arrowprops={'arrowstyle':'->','color':'black','lw':1.2})
ax.annotate('',xy=(0,high),xytext=(0,low),arrowprops={'arrowstyle':'->','color':'black','lw':1.2})
texts=[];roles=[]
def label(x,y,s,role,**kw):
 t=ax.text(x,y,'$'+s+'$',fontsize=13,**kw);texts.append(t);roles.append(role)
 return t
label(1.18*H,-.25,'x','axis-x',ha='left',va='top')
label(-.04*H,high,'y','axis-y',ha='right',va='bottom')
for a in (-H,H):ax.axvline(a,color='#9f9f9f',lw=1.1,ls=(0,(4,4)),zorder=1)
if c==1:
 for sign in (-1,1):
  ax.plot([sign*H,sign*H],[-.09,.09],color='black',lw=1)
  label(sign*H,-.31,math_fraction(sign*Fraction(1,2)/B,True),'x-asymptote',ha='center',va='top')
 # Source-shaped y-intercept label lies left of the vertical axis.
 ax.plot([-.015*H,.015*H],[d,d],color='black',lw=1)
 label(-.065*H,d+.06,math_fraction(D),'y-intercept',ha='right',va='bottom')
else:
 step=H/c
 # Light uniform grid encodes calibration, never a midline hint.
 for j in range(-c-1,c+2):
  x=j*step
  if abs(x)>1.17*H:continue
  ax.axvline(x,color='#e2e2e2',lw=.6,zorder=0)
  ax.plot([x,x],[-.09,.09],color='black',lw=.9)
  # Moderate labels one subdivision; hard labels two, making asymptotes
  # three subdivisions instead of directly giving their coordinate.
  if abs(j)==(1 if c==2 else 2):
   label(x,low-.28,math_fraction(Fraction(j,2*c)/B,True),'x-calibration',ha='center',va='top')
 ystep=.5 if c==2 else .25
 for y in np.arange(math.ceil(low/ystep)*ystep,high,ystep):
  ax.axhline(y,color='#eeeeee',lw=.6,zorder=0)
  ax.plot([-.015*H,.015*H],[y,y],color='black',lw=.6)
  if y!=0 and float(y).is_integer():
   label(-1.23*H,y,str(int(y)),'y-calibration',ha='right',va='center')
 # Tell the learner the unlabeled vertical subdivision scale explicitly.
 t=ax.text(.01,-.16,'Each vertical grid step is '+('1/2' if c==2 else '1/4')+' unit.',transform=ax.transAxes,fontsize=11)
 texts.append(t);roles.append('scale-caption')
 # Tiny marker remains an ordinary curve point, at the assessed intercept.
 ax.plot([0],[d],marker='o',ms=3,color='#2676bd',zorder=4)
# Exactly one branch, separately evaluated inside its two asymptotes. Solve
# window endpoints by arctan so sampling never crosses an asymptote.
xlo=math.atan(low-d)/b;xhi=math.atan(high-d)/b
xs=np.linspace(xlo,xhi,1800);ys=np.tan(b*xs)+d
ax.plot(xs,ys,color='#2676bd',lw=1.8,zorder=3)
fig.canvas.draw();canvas=np.asarray(fig.canvas.buffer_rgba()).copy();height,width=canvas.shape[:2]
renderer=fig.canvas.get_renderer()
clearances=[]
blue=(canvas[:,:,2]>130)&(canvas[:,:,0]<90)&(canvas[:,:,1]>70)&(canvas[:,:,1]<170)
blue_y,blue_x=np.where(blue)
for t,role in zip(texts,roles):
 box=t.get_window_extent(renderer);coords=[box.x0,box.y0,box.x1,box.y1]
 if box.x0<2 or box.y0<2 or box.x1>width-2 or box.y1>height-2:raise AssertionError(('clipped label',role,coords,[width,height]))
 # Measure actual blue pixels against text bounds, no white masking box.
 dx=np.maximum(np.maximum(box.x0-blue_x,blue_x-box.x1),0)
 py=height-blue_y
 dy=np.maximum(np.maximum(box.y0-py,py-box.y1),0)
 clearance=float(np.sqrt(dx*dx+dy*dy).min()) if len(blue_x) else None
 clearances.append({'text':t.get_text(),'role':role,'bbox_pixels':coords,'branch_clearance_px':clearance})
 if clearance is not None and clearance<2.5:raise AssertionError(('label overlaps actual branch',role,t.get_text(),clearance))
for i,(t,r) in enumerate(zip(texts,roles)):
 for t2,r2 in list(zip(texts,roles))[i+1:]:
  if t.get_window_extent(renderer).overlaps(t2.get_window_extent(renderer)):raise AssertionError(('labels overlap',r,r2))
# Actual rendered blue pixels at independently computed central/quarter points.
checks=[]
for u in (-.55,-.3,0,.3,.55):
 x=u*H;y=math.tan(b*x)+d
 if low+.2<y<high-.2:
  px,py=ax.transData.transform((x,y));iy=int(round(height-py));ix=int(round(px))
  hit=bool(blue[max(0,iy-3):iy+4,max(0,ix-3):ix+4].any());checks.append({'x':x,'y':y,'blue_pixel_hit':hit})
  if not hit:raise AssertionError(('missing rendered curve point',x,y))
asymptotes=[]
for a in (-H,H):
 px,py=ax.transData.transform((a,0));col=int(round(px));crop=canvas[20:height-50,max(0,col-1):col+2,:3]
 gray=((crop[:,:,0]>100)&(crop[:,:,0]<210)&(abs(crop[:,:,0].astype(int)-crop[:,:,1].astype(int))<3))
 hits=int(gray.sum());asymptotes.append({'x':a,'pixel_column':col,'gray_pixels':hits})
 if hits<20:raise AssertionError('asymptote missing in raster')
png=Path(data['png']);side=Path(data['sidecar'])
with tempfile.NamedTemporaryFile(suffix='.png',dir=png.parent,delete=False) as tmp:tmp_path=Path(tmp.name)
try:fig.savefig(tmp_path,dpi=130,facecolor='white');os.replace(tmp_path,png)
finally:tmp_path.unlink(missing_ok=True)
metadata={'instance':p,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'numpy':np.__version__,'dependency_paths':paths,
 'size':[width,height],'axes_bounds':[float(-1.2*H),float(1.2*H),low,high],'adjacent_asymptotes':[-H,H],
 'period':2*H,'vertical_intercept':d,'monotonicity':'strictly increasing','branch_pixels':int(blue.sum()),
 'label_measurements':clearances,'curve_pixel_checks':checks,'asymptote_pixel_checks':asymptotes,
 'png_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'white_masking_boxes':0}
with tempfile.NamedTemporaryFile('w',suffix='.json',dir=side.parent,delete=False) as tmp:json.dump(metadata,tmp,indent=2);tmp_path=Path(tmp.name)
os.replace(tmp_path,side);plt.close(fig)
