"""Matplotlib rendering only, using exact worker-supplied vector data.

Read-only fallback to cached Python3.10 wheels; install/download nothing.
Each call gets its own input, PNG temp, JSON temp. Final assets replace atomically.
"""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186172084-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates:raise RuntimeError('missing '+package)
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path)
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fractions import Fraction
data=json.loads(Path(sys.argv[1]).read_text())
points=[[float(Fraction(z)) for z in row] for row in data['points']]
maximum=max((u*u+v*v)**.5 for x,y,u,v in points)
scale=.85/maximum
fig,ax=plt.subplots(figsize=(4.2,3.7),dpi=140)
fig.patch.set_facecolor('white');ax.set_aspect('equal');ax.axis('off')
ax.set_xlim(*data['bounds']);ax.set_ylim(*data['bounds'])
ax.quiver([p[0] for p in points],[p[1] for p in points],
 [p[2]*scale for p in points],[p[3]*scale for p in points],
 angles='xy',scale_units='xy',scale=1,pivot='tail',color='#2478b9',width=.0034,
 headwidth=4,headlength=5,headaxislength=4,minlength=0)
for xy,start in [((5.25,0),(-5.6,0)),((0,5.25),(0,-5.6))]:
 ax.annotate('',xy=xy,xytext=start,arrowprops=dict(arrowstyle='->',color='black',linewidth=1.2))
ax.text(5.4,-.12,'$x$',fontsize=12);ax.text(-.16,5.45,'$y$',fontsize=12)
fig.subplots_adjust(left=.02,right=.98,bottom=.02,top=.98)
png=Path(data['output']);sidecar=Path(data['sidecar'])
with tempfile.NamedTemporaryFile(prefix='png-',suffix='.png',dir=png.parent,delete=False) as f:temporary_png=Path(f.name)
with tempfile.NamedTemporaryFile(mode='w',prefix='sidecar-',suffix='.json',dir=png.parent,delete=False) as f:
 temporary_json=Path(f.name)
 json.dump({**data,'display_scale':scale,'renderer':'Matplotlib','matplotlib':matplotlib.__version__,'python':sys.version,'dependency_paths':provenance},f,indent=2)
try:
 fig.savefig(temporary_png,dpi=140);plt.close(fig)
 os.replace(temporary_png,png);os.replace(temporary_json,sidecar)
finally:
 temporary_png.unlink(missing_ok=True);temporary_json.unlink(missing_ok=True)
