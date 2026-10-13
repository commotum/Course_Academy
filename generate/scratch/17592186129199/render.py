"""Matplotlib only, read-only cached Python 3.10 dependency fallback.
Each invocation owns its input, temp PNG and temp sidecar. Final writes atomic.
"""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186129199-mpl'
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
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
j=json.loads(Path(sys.argv[1]).read_text());p=j['instance'];png=Path(j['png']);n=p['radius_squared'];rad=n**.5
def fraction(x):
 if '/' in x:a,b=x.split('/');return int(a)/int(b)
 return float(x)
a=fraction(p['alpha_pi'])*np.pi;b=fraction(p['beta_pi'])*np.pi
full=abs(b-a-2*np.pi)<1e-9
fig,ax=plt.subplots(figsize=(4.5,4.2));lim=1.45*rad;ax.set_xlim(-lim,lim);ax.set_ylim(-lim,lim);ax.set_aspect('equal');ax.axis('off')
for end in [(lim*.98,0),(0,lim*.98)]:ax.annotate('',end,(-lim*.95,0) if end[1]==0 else (0,-lim*.95),arrowprops={'arrowstyle':'->','lw':1,'color':'black'})
ax.text(lim*.98,-rad*.08,'$x$',fontsize=12);ax.text(rad*.08,lim*.98,'$y$',fontsize=12)
t=np.linspace(a,b,401);xy=np.column_stack([rad*np.cos(t),rad*np.sin(t)])
vertices=xy if full else np.vstack([[0,0],xy,[0,0]])
ax.add_patch(Polygon(vertices,closed=True,facecolor='#e0edf5',edgecolor='#2677bf',lw=1.5,zorder=0))
# All marked axis intercepts derive from the actual sector; suppress unassessed
# absent-circle intercepts rather than suggesting a full disk for a quarter.
label='\\sqrt{'+str(n)+'}' if int(rad)!=rad else str(int(rad))
for angle in [0,np.pi/2,np.pi,3*np.pi/2]:
 eligible=full or any(a-1e-8<=angle+k*2*np.pi<=b+1e-8 for k in range(-2,3))
 if not eligible:continue
 xx,yy=rad*np.cos(angle),rad*np.sin(angle)
 if abs(xx)>.1:ax.text(xx+np.sign(xx)*.20*rad,-.09*rad,'$'+('−' if xx<0 else '')+label+'$',ha='center',va='top',fontsize=11)
 else:ax.text(-.09*rad,yy+np.sign(yy)*.10*rad,'$'+('−' if yy<0 else '')+label+'$',ha='right',va='bottom' if yy>0 else 'top',fontsize=11)
mid=(a+b)/2 if not full else np.pi/4
if abs(b-a-np.pi)<1e-9:mid+=np.pi/6
ax.text(.5*rad*np.cos(mid),.5*rad*np.sin(mid),'$D$',color='#2677bf',fontsize=13)
if full:ax.text(.54*rad,.98*rad,'$x^2+y^2='+str(n)+'$',fontsize=11)
fig.canvas.draw()
fd,tmp=tempfile.mkstemp(prefix='plot-',suffix='.png',dir=png.parent);os.close(fd)
try:fig.savefig(tmp,dpi=140,bbox_inches='tight',facecolor='white');os.replace(tmp,png)
finally:Path(tmp).unlink(missing_ok=True);plt.close(fig)
meta={'renderer':'Matplotlib','python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'instance':p,'bounds':[-lim,lim,-lim,lim],'arc_points':401,'full_disk':full}
fd,tmp=tempfile.mkstemp(prefix='sidecar-',suffix='.json',dir=png.parent)
try:
 with os.fdopen(fd,'w') as f:json.dump(meta,f,indent=2)
 os.replace(tmp,png.with_suffix('.json'))
finally:Path(tmp).unlink(missing_ok=True)
