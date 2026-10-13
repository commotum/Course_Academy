"""Matplotlib 3D recreation from exact-instance endpoint data; atomic output."""
import sys,json,os,re,subprocess,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186119860-mpl'
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):subprocess.run([str(runtime),__file__,sys.argv[1]],check=True);sys.exit()
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates:raise RuntimeError('Cached dependency absent: '+package)
  sys.path.insert(0,str(sorted(candidates,key=lambda p:tuple(map(int,re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups())) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=json.load(open(sys.argv[1]));a,b=p['a'],p['b'];fig=plt.figure(figsize=(5,5));ax=fig.add_subplot(projection='3d')
def curve(t):return np.log(t),2*t,t*t
lo=max(.08,a*.65);hi=b*1.15
for left,right,color in [(lo,a,'red'),(a,b,'blue'),(b,hi,'red')]:
 t=np.linspace(left,right,200);ax.plot(*curve(t),color=color,lw=2)
for idx,(t,label) in enumerate([(a,p['a_label']),(b,p['b_label'])]):
 x,y,z=curve(t);ax.scatter([x],[y],[z],color='blue',s=20);ax.text(x,y,z,' $t='+label+'$',fontsize=11)
 # Dashed orthogonal guides from the actual endpoint to z and y axes.
 for points in [[(x,y,z),(0,y,z),(0,0,z)],[(x,y,z),(x,y,0),(0,y,0)]]:
  points=np.array(points);ax.plot(points[:,0],points[:,1],points[:,2],color='.55',ls=(0,(4,4)),lw=.9)
 xl,yl,zl=p['coordinate_labels'][idx]
 ax.text(0,0,z,' $'+zl+'$',fontsize=10,ha='right',va='bottom')
 ax.text(0,y,0,' $'+yl+'$',fontsize=10,ha='left',va='top')
 if abs(x)>1e-8:ax.text(x,0,0,' $'+xl+'$',fontsize=10,ha='center',va='top')
for t in np.linspace(a,b,5)[1:-1]:
 x,y,z=curve(t);vec=np.array([1/t,2,2*t]);vec=vec/np.linalg.norm(vec)*(hi-lo)*.10;ax.quiver(x,y,z,*vec,color='blue',arrow_length_ratio=.6)
# Explicit origin axes and arrowheads match the source semantic coordinate frame.
axis_ends=[max(1,np.log(hi))*1.12,2*hi*1.08,hi**2*1.05]
for idx,name in enumerate(('x','y','z')):
 vec=np.zeros(3);vec[idx]=axis_ends[idx];ax.quiver(0,0,0,*vec,color='black',arrow_length_ratio=.035,linewidth=1.1);ax.text(*vec,' $'+name+'$',fontsize=12)
ax.plot([min(0,np.log(lo)),0],[0,0],[0,0],color='black',lw=1)
ax.set_xlim(min(np.log(lo),0)*1.15,axis_ends[0]*1.08);ax.set_ylim(-.25,axis_ends[1]*1.1);ax.set_zlim(-.15,axis_ends[2]*1.07)
ax.view_init(elev=19,azim=-65);ax.set_box_aspect((1,1,1));ax.set_axis_off();fig.tight_layout()
out=Path(p['output']);out.parent.mkdir(parents=True,exist_ok=True)
fd,tmp=tempfile.mkstemp(suffix='.png',dir=out.parent);os.close(fd)
try:fig.savefig(tmp,dpi=150,facecolor='white');os.replace(tmp,out)
finally:
 if os.path.exists(tmp):os.unlink(tmp)
plt.close(fig)
sidecar={**p,'renderer':'Matplotlib','matplotlib':matplotlib.__version__,'numpy':np.__version__,'python':sys.version,'curve':'(log(t),2*t,t**2)','segment':[a,b]}
fd,tmp=tempfile.mkstemp(suffix='.json',dir=out.parent);os.close(fd)
try:Path(tmp).write_text(json.dumps(sidecar,indent=2)+'\n');os.replace(tmp,out.with_suffix('.json'))
finally:
 if os.path.exists(tmp):os.unlink(tmp)
