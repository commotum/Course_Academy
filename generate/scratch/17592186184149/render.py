"""Matplotlib private renderer. Exact rational input; atomic outputs and pixel QA."""
import os,sys,json,re,subprocess,uuid,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186184149-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates:raise RuntimeError('Missing cached dependency '+package)
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
from PIL import Image
p=json.load(open(sys.argv[1]));B=float(Fraction(p['B']));c=float(Fraction(p['c']));fn=p['fn'];h=-c*math.pi/B;P=math.pi/B;z0=0 if fn=='tan' else P/2;z=z0+h;left=z-P/2;right=z+P/2

def label(v):
 q=Fraction(v/math.pi).limit_denominator(2000)
 if q==0:return '0'
 sign='-' if q<0 else '';q=abs(q);n=q.numerator;d=q.denominator
 num=('' if n==1 else str(n))+r'\pi'
 return sign+(num if d==1 else r'\frac{'+num+'}{'+str(d)+'}')

def draw_branch(ax,shift,style):
 zz=z0+shift;ll=zz-P/2;rr=zz+P/2
 # Branch parameter at y=±3.4 avoids clipping and no cross-pole connections.
 if fn=='tan':xx=np.linspace(zz-math.atan(3.4)/B,zz+math.atan(3.4)/B,1000);yy=np.tan(B*(xx-shift))
 else:xx=np.linspace(ll+math.atan(1/3.4)/B,rr-math.atan(1/3.4)/B,1000);yy=1/np.tan(B*(xx-shift))
 ax.plot(xx,yy,color='#2878b8',lw=2.3,ls=style,zorder=3)
 return xx,yy

for role,target in p['targets'].items():
 overlay=role=='solution' or p['level']=='easy'
 xmin=min(left,0,z0-P/2 if overlay else left)-P*.13;xmax=max(right,0,z0+P/2 if overlay else right)+P*.13
 fig=plt.figure(figsize=(8,6.4),dpi=100);ax=fig.add_axes([.10,.26,.85,.55]);ax.set_xlim(xmin,xmax);ax.set_ylim(-3.7,3.7);ax.axis('off')
 ax.annotate('',xy=(xmax,0),xytext=(xmin,0),arrowprops={'arrowstyle':'->','lw':1.2,'color':'black'})
 ax.annotate('',xy=(0,3.65),xytext=(0,-3.65),arrowprops={'arrowstyle':'->','lw':1.2,'color':'black'})
 ax.text(xmax,0,'$x$',va='bottom',fontsize=14);ax.text(0,3.65,'$y$',ha='right',fontsize=14)
 for t in [left,right]:ax.plot([t,t],[-3.4,3.4],color='#999999',lw=1,ls=(0,(5,4)),zorder=1)
 if overlay:
  draw_branch(ax,0,'--')
 xx,yy=draw_branch(ax,h,'-')
 feature_values=sorted(set([left,z,right]+([z0] if overlay else [])))
 # Exterior calibration strip: no masks; explicit coordinate tick positions.
 texts=[];boxes=[];fig.canvas.draw();renderer=fig.canvas.get_renderer()
 for i,t in enumerate(feature_values):
  ax.plot([t,t],[-.08,.08],color='black',lw=1)
  txt=ax.text(t,-4.1,'$'+label(t)+'$',ha='center',va='top',fontsize=15,clip_on=False)
  fig.canvas.draw();box=txt.get_window_extent(renderer)
  if any(box.expanded(1.20,1.15).overlaps(old.expanded(1.20,1.15)) for old in boxes):
   txt.set_y(-5.25);fig.canvas.draw();box=txt.get_window_extent(renderer)
  if any(box.expanded(1.20,1.15).overlaps(old.expanded(1.20,1.15)) for old in boxes):raise RuntimeError('Label strip collision')
  texts.append(txt);boxes.append(box)
 bq=Fraction(p['B']);arg=(str(bq.numerator)+'x' if bq.denominator==1 else r'\frac{'+('' if bq.numerator==1 else str(bq.numerator))+'x}{'+str(bq.denominator)+'}')
 formula='$y=\\'+fn+'('+arg+'+C)$'
 fig.text(.52,.94,formula,ha='center',fontsize=16,color='#2878b8')
 if overlay:fig.text(.52,.875,'Dashed: $y=\\'+fn+'('+arg+')$',ha='center',fontsize=15,color='#2878b8')
 fig.canvas.draw();rgba=np.asarray(fig.canvas.buffer_rgba())[:,:,:3]
 # Read actual rendered blue curve pixels at independent test coordinates.
 samples=[]
 for off in [-.19,-.07,.07,.19]:
  xt=z+off*P;yt=math.tan(B*(xt-h)) if fn=='tan' else 1/math.tan(B*(xt-h))
  px,py=ax.transData.transform((xt,yt));px=int(round(px));py=rgba.shape[0]-int(round(py));patch=rgba[max(0,py-4):py+5,max(0,px-4):px+5]
  blue=(patch[:,:,2]>patch[:,:,0]+30)&(patch[:,:,2]>patch[:,:,1]+10)
  if not blue.any():raise RuntimeError('Rendered curve failed independent pixel sample')
  samples.append({'x':xt,'y':yt,'pixel':[px,py],'blue_pixels':int(blue.sum())})
 asym=[]
 for t in [left,right]:
  px,py=ax.transData.transform((t,2.8));px=int(round(px));py=rgba.shape[0]-int(round(py));patch=rgba[py-20:py+20,px-2:px+3];gray=(patch.max(2)-patch.min(2)<8)&(patch.min(2)<230)&(patch.min(2)>60)
  if not gray.any():raise RuntimeError('Missing actual asymptote pixels')
  asym.append({'x':t,'gray_pixels':int(gray.sum())})
 # Measure actual label bboxes against rendered curve region; exterior strip.
 lowest_curve_pixel=ax.transData.transform((0,-3.4))[1]
 clearance=min(lowest_curve_pixel-b.y1 for b in boxes)
 if clearance<10:raise RuntimeError('Insufficient label/curve clearance')
 temp=Path(target).with_name('.'+uuid.uuid4().hex+'.png');fig.savefig(temp,dpi=100);os.replace(temp,target)
 report={'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'input':{k:p[k] for k in ['B','c','fn','level']},'role':role,'bounds':[xmin,xmax,-3.7,3.7],'branch_domain':[left,right],'zero':z,'monotonicity':'increasing' if fn=='tan' else 'decreasing','labels':[{'value':label(t),'bbox':[float(v) for v in box.bounds]} for t,box in zip(feature_values,boxes)],'minimum_label_curve_clearance_px':clearance,'curve_pixel_samples':samples,'asymptote_pixels':asym,'size':[800,640]}
 side=Path(target).with_suffix('.json');tmp=side.with_name('.'+uuid.uuid4().hex+'.json');tmp.write_text(json.dumps(report,indent=2)+'\n');os.replace(tmp,side);plt.close(fig)
