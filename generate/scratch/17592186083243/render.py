"""Parameterized parametric-curve plots; cached dependencies read-only."""
import json,os,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186083243-mpl'
provenance={}
try: import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates: raise RuntimeError('Missing cached dependency '+package)
  p=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(p));provenance[package]=str(p.resolve())
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
record=json.loads(Path(sys.argv[1]).read_text());p=record['parameters'];f=record['family'];a,b=int(p['a']),int(p['b'])
if f=='cubic':
 fold_x=4*a**3/27;fold_y=4*a*a*b/9
 xmax=max(5,1.3*fold_x);ymax=max(6*b,1.15*a*a*b)
 t=np.unique(np.concatenate([np.linspace(-max(3,1.15*a),max(a,xmax**(1/3)),3500),[-a,-2*a/3,0]]))
 x=t**3+a*t**2;y=b*t**2
 bounds=(-max(2,.3*fold_x),xmax,-b,ymax)
 assert bounds[0]<fold_x<bounds[1] and bounds[2]<fold_y<bounds[3]
elif f=='harmonic':
 t=np.linspace(0,2*np.pi,2400);x=a*np.cos(t);y=b*np.sin(p['n']*t);bounds=(-a-1,a+1,-b-1,b+1)
elif f=='ellipse':
 t=np.linspace(0,2*np.pi,2400);x=a*np.sin(t);y=b*np.cos(t);bounds=(-a-1,a+1,-b-1,b+1)
else: raise ValueError(f)
height=max(4,min(14,4*(bounds[3]-bounds[2])/(bounds[1]-bounds[0]))) if f=='cubic' else 4
fig,ax=plt.subplots(figsize=(4.4,height),dpi=120)
ax.plot(x,y,color='#2c78b9',lw=1.8);ax.set_xlim(bounds[:2]);ax.set_ylim(bounds[2:]);ax.set_aspect('equal',adjustable='box')
ax.spines[['left','bottom']].set_position('zero');ax.spines[['right','top']].set_visible(False)
ax.set_xticks(np.arange(np.ceil(bounds[0]),bounds[1]+.1,max(1,int(np.ceil((bounds[1]-bounds[0])/10)))));ax.set_yticks(np.arange(np.ceil(bounds[2]),bounds[3]+.1,max(1,int(np.ceil((bounds[3]-bounds[2])/10)))))
ax.grid(color='#bbbbbb',linewidth=.7);ax.set_axisbelow(True);ax.tick_params(length=0,labelsize=9,pad=4)
ax.annotate('x',(bounds[1],0),xytext=(4,-6),textcoords='offset points');ax.annotate('y',(0,bounds[3]),xytext=(4,0),textcoords='offset points')
fig.savefig(record['target'],bbox_inches='tight');plt.close(fig)
(HERE/'render-provenance.json').write_text(json.dumps({'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance},indent=2)+'\n')
