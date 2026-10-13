"""Private Matplotlib renderer; cached dependencies are read-only; atomic outputs."""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186179718-mpl'
paths={}
try:import matplotlib
except ImportError:
 if sys.version_info[:2]!=(3,10):
  subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit()
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));paths[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg');import matplotlib.pyplot as plt
D=json.loads(Path(sys.argv[1]).read_text());output=Path(D['output']);sidecar=output.with_suffix('.json')
fig,ax=plt.subplots(figsize=(4.7,4.1));xx=D['x'];yy=D['y'];width=max(xx)-min(xx);height=max(yy)-min(yy);pad=max(width,height,1)*.24
ax.set_xlim(min(0,min(xx))-pad,max(0,max(xx))+pad);ax.set_ylim(min(0,min(yy))-pad,max(0,max(yy))+pad);ax.set_aspect('equal',adjustable='box')
ax.axhline(0,color='black',lw=1);ax.axvline(0,color='black',lw=1)
for spine in ax.spines.values():spine.set_visible(False)
ax.set_xticks([]);ax.set_yticks([]);ax.plot(xx,yy,color='#2878bb',lw=2)
for idx in (35,70,105):ax.annotate('',xy=(xx[idx+5],yy[idx+5]),xytext=(xx[idx],yy[idx]),arrowprops=dict(arrowstyle='->',color='#2878bb',lw=1.5))
for idx,label in ((0,D['labels'][0]),(-1,D['labels'][1])):
 ax.plot(xx[idx],yy[idx],'o',color='#2878bb',ms=4)
 offset=(0,11) if idx==-1 else (18,-16) if xx[idx]==0 and yy[idx]==0 else (20,18) if xx[-1]>xx[0] and abs(xx[0])<pad/2 else (-18,10) if xx[-1]>xx[0] else (20,-8)
 ax.annotate('$'+label+'$',(xx[idx],yy[idx]),xytext=offset,textcoords='offset points',ha='center',color='#2878bb',fontsize=11)
ax.text(ax.get_xlim()[1],-.08*pad,'$x$',ha='right');ax.text(.07*pad,ax.get_ylim()[1],'$y$',va='top')
fig.tight_layout()
fd,tmp=tempfile.mkstemp(prefix='.render-',suffix='.png',dir=output.parent);os.close(fd)
try:fig.savefig(tmp,dpi=125);os.replace(tmp,output)
finally:
 if os.path.exists(tmp):os.unlink(tmp)
plt.close(fig)
D['dependencies']={'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'dependency_paths':paths}
fd,tmp=tempfile.mkstemp(prefix='.sidecar-',suffix='.json',dir=output.parent)
with os.fdopen(fd,'w') as h:json.dump(D,h,indent=2)
os.replace(tmp,sidecar)
