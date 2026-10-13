"""Versioned Matplotlib renderer; read-only cached dependencies; atomic PNG/sidecar."""
import json,os,re,sys,subprocess,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186152187-mpl'
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates:raise RuntimeError('Missing cached dependency '+package)
  def key(p):
   m=re.match(r'(\d+)\.(\d+)\.(\d+)',p.name);return tuple(map(int,m.groups())) if m else (0,)
  sys.path.insert(0,str(sorted(candidates,key=key)[-1]))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
j=json.loads(Path(sys.argv[1]).read_text());a=float(Fraction(j['a']));b=float(Fraction(j['b']));marked=j['marked'];hard=j['hard'];dest=Path(j['output']);dest.parent.mkdir(exist_ok=True)
fig,ax=plt.subplots(figsize=(5,5),dpi=140);fig.subplots_adjust(left=.06,right=.94,bottom=.06,top=.94)
R=max(a,b);bounds=(-R*1.70,R*1.70,-R*1.70,R*1.70);ax.set(xlim=bounds[:2],ylim=bounds[2:],aspect='equal');ax.axis('off')
ax.annotate('',(bounds[1]*.96,0),(bounds[0]*.96,0),arrowprops={'arrowstyle':'->','lw':1.25,'color':'black'})
ax.annotate('',(0,bounds[3]*.96),(0,bounds[2]*.96),arrowprops={'arrowstyle':'->','lw':1.25,'color':'black'})
t=np.linspace(0,2*np.pi,1201);curve=np.column_stack((a*np.cos(t),b*np.sin(t)));ax.plot(curve[:,0],curve[:,1],color='#2677b9',lw=1.6)
if hard:
 # half-unit lattice, with integer tick labels; endpoints must be read between labels.
 for v in np.arange(-R,R+.01,.5):
  if v==0:continue
  ax.plot([v,v],[-R,R],color='#d7d7d7',lw=.45,zorder=0);ax.plot([-R,R],[v,v],color='#d7d7d7',lw=.45,zorder=0)
  ax.plot([v,v],[-.025*R,.025*R],color='black',lw=.6);ax.plot([-.025*R,.025*R],[v,v],color='black',lw=.6)
texts=[]
def label(x,y,s,ha='center',va='center',direction=(0,1)):
 obj=ax.text(x,y,s,fontsize=12,ha=ha,va=va);texts.append((obj,direction));return obj
if not hard:
 for v in (-a,a):label(v,-.06*R,str(int(v)) if v.is_integer() else str(v),va='top',direction=(0,-1))
 for v in (-b,b):
  # Keep the vertical intercept label beside its own y-axis endpoint.
  # Move outward vertically if needed, never far along the horizontal axis.
  sign=1 if v>0 else -1
  label(-.05*R,v+sign*.04*R,str(int(v)) if v.is_integer() else str(v),ha='right',va='bottom' if sign>0 else 'top',direction=(0,sign))
else:
 for v in range(-int(R),int(R)+1):
  if v==0 or v%2:continue
  label(v,-1.13*R,str(v),va='top',direction=(0,-1));label(-1.13*R,v,str(v),ha='right',direction=(-1,0))
label(bounds[1]*.87,.09*R,'x',direction=(0,1));label(.08*R,bounds[3]*.87,'y',direction=(1,0))
if marked:
 ax.plot(a,0,'ko',ms=4)
 label(a+.10*R,.14*R,j['point'] if hard else f"{j['point']}({j['a']},0)",ha='left',va='bottom',direction=(1,1))
 z=.65;ax.annotate('',(a*np.cos(z+.08),b*np.sin(z+.08)),(a*np.cos(z-.08),b*np.sin(z-.08)),arrowprops={'arrowstyle':'->','color':'#2677b9','lw':1.5})
# Actual rendered text boxes must clear the curve, axes, markers and other labels.
fig.canvas.draw();cp=ax.transData.transform(curve);origin=ax.transData.transform((0,0));placed=[];boxes=[]
for obj,direction in texts:
 for attempt in range(50):
  fig.canvas.draw();bb=obj.get_window_extent(fig.canvas.get_renderer()).expanded(1.06,1.12)
  curve_hit=np.any((cp[:,0]>=bb.x0)&(cp[:,0]<=bb.x1)&(cp[:,1]>=bb.y0)&(cp[:,1]<=bb.y1))
  axes_hit=bb.x0<=origin[0]<=bb.x1 or bb.y0<=origin[1]<=bb.y1
  other=any(bb.overlaps(x) for x in placed)
  if not(curve_hit or axes_hit or other):break
  x,y=obj.get_position();obj.set_position((x+direction[0]*R*.022,y+direction[1]*R*.022))
 else:raise RuntimeError('Could not clear labels '+str((obj.get_text(),obj.get_position(),bb.extents.tolist(),origin.tolist(),curve_hit,axes_hit,other)))
 if not (ax.bbox.contains(bb.x0,bb.y0) and ax.bbox.contains(bb.x1,bb.y1)):raise RuntimeError('Label clipped')
 placed.append(bb);boxes.append({'text':obj.get_text(),'bbox':list(bb.extents),'data_position':list(obj.get_position())})
fig.canvas.draw();trans=ax.transData;center=trans.transform((0,0));extents=trans.transform([(-a,-b),(a,b)])
fd,tmp=tempfile.mkstemp(prefix='ellipse-',suffix='.png',dir=dest.parent);os.close(fd)
try:fig.savefig(tmp,dpi=140);os.replace(tmp,dest)
finally:
 if os.path.exists(tmp):os.unlink(tmp)
side={'renderer_version':'ellipse-v7','python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'numpy':np.__version__,'a':j['a'],'b':j['b'],'marked':marked,'hard':hard,'bounds':bounds,'curve_pixel_extents':extents.tolist(),'origin_pixel':center.tolist(),'png_size':[700,700],'labels':boxes,'label_clearance_pass':True}
fd,tmp=tempfile.mkstemp(prefix='sidecar-',suffix='.json',dir=dest.parent);os.close(fd);Path(tmp).write_text(json.dumps(side,indent=2));os.replace(tmp,dest.with_suffix('.json'));plt.close(fig)
