"""Render exact finite sign diagrams using read-only cached Matplotlib.
No installs, downloads or shared writes. Unique temp files and atomic replace
support simultaneous identical/different instance rendering. Inputs come from
one generator instance; the renderer never resamples or evaluates answers.
"""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186172039-mpl'
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
from matplotlib.patches import Rectangle

def atomic_json(path,obj):
 with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,suffix='.json',delete=False) as tmp:
  json.dump(obj,tmp,indent=2);tmp.write('\n');name=tmp.name
 os.replace(name,path)

spec=json.loads(sys.argv[1]);out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True)
ss=spec['signs'];assert len(ss)==4 and set(ss)<=set([-1,1])
fig,ax=plt.subplots(figsize=(3.54,2.98),dpi=160)
fig.subplots_adjust(0,.03,.95,.96)
for s,(x,y) in zip(ss,[(0,0),(-1,0),(-1,-1),(0,-1)]):
 ax.add_patch(Rectangle((x,y),1,1,color='#e8f0f7' if s>0 else '#faeee8',linewidth=0))
for start,end in [((-1,0),(1.04,0)),((0,-1),(0,1.04))]:ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','color':'black','linewidth':.65},clip_on=False)
ax.text(1.06,-.08,'$x$',ha='center',fontsize=10);ax.text(-.06,1.09,'$y$',fontsize=10)
for s,(x,y) in zip(ss,[(.5,.5),(-.5,.5),(-.5,-.5),(.5,-.5)]):ax.text(x,y,'$f(x,y)'+('>0' if s>0 else '<0')+'$',ha='center',va='center',fontsize=10)
ax.set_xlim(-1,1.13);ax.set_ylim(-1,1.15);ax.axis('off')
with tempfile.NamedTemporaryFile(dir=out.parent,suffix='.png',delete=False) as tmp:name=tmp.name
fig.savefig(name,dpi=160,facecolor='white');plt.close(fig);os.replace(name,out)
atomic_json(out.with_suffix('.json'),{'spec':spec,'renderer':'Matplotlib','python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'zero_set_is_not_an_axis_style':'The axes are coordinate axes. Actual zero sets are specified by the printed equation and solution.'})
atomic_json(HERE/'render-provenance.json',{'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'fallback':'cached read-only wheels, no installation or shared changes'})
