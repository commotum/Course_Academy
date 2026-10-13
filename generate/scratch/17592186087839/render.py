"""Matplotlib renderer; cached Python3.10 dependencies read-only, atomic artifacts."""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087839-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]],check=True);sys.exit(0)
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
from fractions import Fraction
payload=json.loads(Path(sys.argv[1]).read_text());data=payload['data'];output=Path(payload['output']);a=float(Fraction(data['a']));b=float(Fraction(data['b']))
fig,ax=plt.subplots(figsize=(6,4.5));ax.set_aspect('equal');ax.axis('off')
xmax=a*1.35;ymax=max(b*1.5,a*.7);ax.set_xlim(-xmax,xmax);ax.set_ylim(-ymax,ymax)
t=np.linspace(0,2*np.pi,1201);ax.plot(a*np.cos(t),b*np.sin(t),color='#2576bc',linewidth=1.7)
ax.annotate('',xy=(xmax*.97,0),xytext=(-xmax,0),arrowprops={'arrowstyle':'->','linewidth':1.2,'color':'black'})
ax.annotate('',xy=(0,ymax*.97),xytext=(0,-ymax),arrowprops={'arrowstyle':'->','linewidth':1.2,'color':'black'})
ax.text(xmax*.98,.08*ymax,'$x$',fontsize=13);ax.text(.05*xmax,ymax*.94,'$y$',fontsize=13)
label=lambda v:format(v,'g').replace('-','−')
for x in (-a,a):
 ax.plot([x,x],[-.026*ymax,.026*ymax],color='black',lw=1);ax.text(x,-.09*ymax,label(x),ha='center',va='top',fontsize=11)
for y in (-b,b):
 ax.plot([-.024*xmax,.024*xmax],[y,y],color='black',lw=1);ax.text(-.07*xmax,y,label(y),ha='right',va='center',fontsize=11)
fig.subplots_adjust(left=.04,right=.96,bottom=.05,top=.95)
fd,tmp=tempfile.mkstemp(prefix='atomic-',suffix='.png',dir=output.parent);os.close(fd)
side=output.with_suffix('.json');fd2,tmp2=tempfile.mkstemp(prefix='atomic-',suffix='.json',dir=output.parent);os.close(fd2)
try:
 fig.savefig(tmp,dpi=140,facecolor='white');plt.close(fig)
 metadata={**data,'intercepts':[[-a,0],[a,0],[0,-b],[0,b]],'bounds':[-xmax,xmax,-ymax,ymax],'equal_aspect':True,'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance}
 Path(tmp2).write_text(json.dumps(metadata,indent=2)+'\n');os.replace(tmp,output);os.replace(tmp2,side)
finally:
 Path(tmp).unlink(missing_ok=True);Path(tmp2).unlink(missing_ok=True)
