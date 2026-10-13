"""Matplotlib circle renderer; unique private inputs and atomic output writes."""
import json,os,re,sys,tempfile,math
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/circle-slope-66865-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  import subprocess
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit()
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  paths=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(paths,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path)
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
p=json.loads(Path(sys.argv[1]).read_text());png,side=map(Path,sys.argv[2:])
def number(v):return math.sqrt(float(v[5:-1])) if v.startswith('sqrt(') else float(Fraction(v))
def label(v):
 if v.startswith('sqrt('):return r'\sqrt{'+v[5:-1]+'}'
 q=Fraction(v)
 return str(q.numerator) if q.denominator==1 else ('-' if q<0 else '')+r'\frac{'+str(abs(q.numerator))+'}{'+str(q.denominator)+'}'
h,k,r=[number(p[s]) for s in ('h','k','r')];margin=.8*r+.6
bounds=[min(0,h-r)-margin,max(0,h+r)+margin,min(0,k-r)-margin,max(0,k+r)+margin]
fig,ax=plt.subplots(figsize=(5.4,5.0));ax.set_aspect('equal');ax.set_xlim(bounds[:2]);ax.set_ylim(bounds[2:]);ax.axis('off')
t=np.linspace(0,2*np.pi,1200);ax.plot(h+r*np.cos(t),k+r*np.sin(t),color='#2177bc',lw=1.6)
ax.annotate('',xy=(bounds[1],0),xytext=(bounds[0],0),arrowprops=dict(arrowstyle='->',color='black',lw=1));ax.annotate('',xy=(0,bounds[3]),xytext=(0,bounds[2]),arrowprops=dict(arrowstyle='->',color='black',lw=1))
ax.text(bounds[1]+.06*r,0,'$x$',fontsize=13,ha='left',va='center');ax.text(0,bounds[3]+.08*r,'$y$',fontsize=13,ha='center')
if h==k==0:
 for val,pos in [(r,(r,-.13*r)),(-r,(-r,-.13*r)),(r,(-.1*r,r)),(-r,(-.1*r,-r))]:
  lv=label(p['r']);lv=('-'+lv) if val<0 else lv
  ax.text(*pos,'$'+lv+'$',fontsize=12,ha='right' if pos[0]<0 else 'left',va='bottom' if pos[1]>0 else 'top')
else:
 ax.plot([h,h+r],[k,k],ls=(0,(4,4)),lw=.8,color='gray');ax.scatter([h],[k],s=23,color='#df9e00',zorder=4)
 ax.text(h,k-.13*r,'$('+label(p['h'])+','+label(p['k'])+')$',fontsize=12,ha='center',va='top')
 # A horizontal radius brace, with exact radius above and center below.
 xx=np.linspace(h,h+r,121); u=(xx-h)/r
 yy=k+.11*r+.025*r*(1-np.cos(4*np.pi*u))
 ax.plot(xx,yy,color='black',lw=.7);ax.text(h+r/2,k+.21*r,'$'+label(p['r'])+'$',fontsize=12,ha='center',va='bottom')
fig.canvas.draw()
geometry={'parameters':p,'bounds':bounds,'axes_origin':[0,0],'center':[h,k],'radius':r,'circle_extents':[h-r,h+r,k-r,k+r],'axes_transform':ax.transData.get_matrix().tolist(),'labels':{'h':label(p['h']),'k':label(p['k']),'r':label(p['r'])},'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance}
with tempfile.NamedTemporaryFile(dir=png.parent,suffix='.png',delete=False) as temp:tmp=Path(temp.name)
try:fig.savefig(tmp,dpi=140,facecolor='white');os.replace(tmp,png)
finally:tmp.unlink(missing_ok=True)
plt.close(fig)
with tempfile.NamedTemporaryFile(dir=side.parent,suffix='.json',mode='w',delete=False) as temp:json.dump(geometry,temp,indent=2);temp.write('\n');tmp=Path(temp.name)
try:os.replace(tmp,side)
finally:tmp.unlink(missing_ok=True)
