"""Private Matplotlib renderer; read-only cached dependencies, atomic artifacts."""
import sys,os,json,re,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186129200-mpl'
try: import matplotlib
except ImportError:
 runtime='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
 if sys.version_info[:2]!=(3,10):
  import subprocess
  subprocess.run([runtime,__file__,*sys.argv[1:]],check=True);sys.exit()
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for pkg in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/pkg).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  sys.path.insert(0,str(sorted(candidates)[-1]))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=json.load(open(sys.argv[1]));out=Path(p.pop('output'));side=out.with_suffix('.json')
R=p['R'];kind=p['kind'];a=p['a'];b=p['b'];fig,ax=plt.subplots(figsize=(4.8,4.8))
t=np.linspace(a,b,500)
if kind=='shift':
 s=p['sign'];rad=s*R*np.sin(t);xx=rad*np.cos(t);yy=rad*np.sin(t);lim=R*1.4
else: xx=R*np.cos(t);yy=R*np.sin(t);lim=R*1.4
ax.fill(np.r_[0,xx,0],np.r_[0,yy,0],facecolor='#dfebf4',edgecolor='#1876c1',lw=1.7)
ax.annotate('',xy=(lim,0),xytext=(-lim,0),arrowprops={'arrowstyle':'->','color':'#333'})
ax.annotate('',xy=(0,lim),xytext=(0,-lim),arrowprops={'arrowstyle':'->','color':'#333'})
ax.text(lim,0,'$x$',ha='left',va='center');ax.text(0,lim,'$y$',ha='center',va='bottom')
if kind=='shift':
 s=p['sign'];ax.text(.25*R,s*.5*R,'$D$',color='#1876c1')
 ax.text(-.05*R,s*R/2,f'${s*R/2:g}$',ha='right');ax.text(-.05*R,s*R,f'${s*R:g}$',ha='right')
 label=r'$x=\sqrt{'+('' if s>0 else '-')+f'{R:g}y-y^2'+r'}$'
 ax.text(.5*R,s*R*.87,label,ha='left',fontsize=11)
else:
 mid=(a+b)/2
 dx,dy=(.2*R,.3*R) if b-a>6 else (.2*R,.4*R) if b-a>3 else (.45*R*np.cos(mid),.45*R*np.sin(mid))
 ax.text(dx,dy,'$D$',color='#1876c1')
 for v in (-R,R):
  ax.text(v*1.12,-.08*R,f'${v:g}$',ha='center',va='top')
  ax.text(-.08*R,v+(.12*R if v<0 else .03*R),f'${v:g}$',ha='right')
ax.set(xlim=(-lim*1.05,lim*1.12),ylim=(-lim*1.05,lim*1.12),aspect='equal');ax.axis('off');fig.tight_layout()
out.parent.mkdir(exist_ok=True)
fd,tmp=tempfile.mkstemp(prefix='render-',suffix='.png',dir=out.parent);os.close(fd)
try: fig.savefig(tmp,dpi=180,facecolor='white');os.replace(tmp,out)
finally:
 if os.path.exists(tmp):os.unlink(tmp)
plt.close(fig)
fd,tmp=tempfile.mkstemp(prefix='side-',suffix='.json',dir=out.parent)
with os.fdopen(fd,'w') as f:json.dump({'parameters':p,'python':sys.version,'matplotlib':matplotlib.__version__},f,indent=2)
os.replace(tmp,side)
