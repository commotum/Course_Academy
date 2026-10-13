"""Atomic private Matplotlib renderer; exact instance input, no resampling."""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087840-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),sys.argv[1]],check=True);sys.exit(0)
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
v=json.loads(Path(sys.argv[1]).read_text());s=v['spec'];a,b=map(lambda z:float(Fraction(z)),(s['a'],s['b']));limit=b*1.2
fig,ax=plt.subplots(figsize=(4.8,4),dpi=100);fig.patch.set_facecolor('white');ax.set_aspect('equal');ax.set_xlim(-limit,limit);ax.set_ylim(-limit,limit);ax.axis('off')
t=np.linspace(0,2*np.pi,641);ax.plot(a*np.cos(t),b*np.sin(t),color='#2675b5',linewidth=1.8)
for end in ((limit,0),(0,limit)):ax.annotate('',xy=end,xytext=(-limit,0) if end[1]==0 else (0,-limit),arrowprops={'arrowstyle':'->','color':'black','lw':1.2})
for val,axis in ((a,'x'),(-a,'x'),(b,'y'),(-b,'y')):
 delta=limit*.014
 if axis=='x':
  ax.plot([val,val],[-delta,delta],color='black',lw=.8);pos=(val,-limit*.085);ha='center';va='top'
 else:
  ax.plot([-delta,delta],[val,val],color='black',lw=.8);pos=(-limit*.05,val);ha='right';va='center'
 frac=Fraction(str(val)).limit_denominator(12)
 label=str(frac.numerator) if frac.denominator==1 else (str(val).rstrip('0').rstrip('.') if frac.denominator==2 else rf'$\frac{{{frac.numerator}}}{{{frac.denominator}}}$')
 ax.text(*pos,label,fontsize=11,ha=ha,va=va,bbox={'facecolor':'white','edgecolor':'none','pad':1.5},zorder=8)
ax.text(limit*.98,limit*.035,'$x$',ha='left',va='bottom',fontsize=13);ax.text(limit*.035,limit*.98,'$y$',ha='left',va='bottom',fontsize=13)
fig.subplots_adjust(left=.04,right=.94,bottom=.06,top=.94)
# Each producer has unique temp paths; publish PNG and sidecar atomically.
png=Path(v['png']);side=Path(v['sidecar'])
with tempfile.NamedTemporaryFile(suffix='.png',prefix='atomic-',dir=png.parent,delete=False) as f:tmp=f.name
try:fig.savefig(tmp,dpi=100,facecolor='white');os.replace(tmp,png)
finally:Path(tmp).unlink(missing_ok=True);plt.close(fig)
s.update({'renderer':'Matplotlib','matplotlib_version':matplotlib.__version__,'dependency_paths':provenance,'curve':{'x':'a cos(t)','y':'b sin(t)','t':[0,2*np.pi]},'label_background':'opaque white','axis_arrows':'positive x and positive y'})
with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='atomic-',dir=side.parent,delete=False) as f:json.dump(s,f,indent=2);tmp=f.name
try:os.replace(tmp,side)
finally:Path(tmp).unlink(missing_ok=True)
