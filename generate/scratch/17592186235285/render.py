"""Private atomic Matplotlib renderer; cached CPython3.10 dependencies are read-only."""
import json,os,re,sys,tempfile
from fractions import Fraction
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186235285-mpl'
try: import matplotlib
except ImportError:
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  ps=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  sys.path.insert(0,str(sorted(ps,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
payload=json.load(open(sys.argv[1]));out=Path(payload['out']);a=np.array(payload['a'],float);b=np.array(payload['b'],float);k=float(Fraction(payload['k']));r=float(Fraction(payload['r']));c=k*b-r*a;p=k*b
points=np.stack([[0,0],a,b,c,p]);lo=np.floor(points.min(0))-2;hi=np.ceil(points.max(0))+2
fig,ax=plt.subplots(figsize=(5,5));ax.set_aspect('equal');ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_xticks(np.arange(lo[0],hi[0]+1));ax.set_yticks(np.arange(lo[1],hi[1]+1));ax.grid(color='#dddddd',linewidth=.6);ax.tick_params(length=0,labelbottom=False,labelleft=False)
for spine in ax.spines.values():spine.set_visible(False)
def arrow(start,end,color,label,dashed=False,offset=.35):
 ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle='->',color=color,lw=1.5,linestyle='--' if dashed else '-'),zorder=4)
 delta=end-start;normal=np.array([-delta[1],delta[0]])/np.linalg.norm(delta);mid=(start+end)/2+normal*offset
 ax.text(*mid,label,color=color,fontsize=12,ha='center',va='center',bbox=dict(facecolor='white',edgecolor='none',alpha=.85,pad=.2),zorder=5)
zero=np.array([0.,0.]);arrow(zero,a,'#2878b5','a');arrow(zero,b,'#dd9900','b',offset=-.35);arrow(zero,c,'black','c')
if payload['role']=='solution':
 arrow(zero,p,'#edbe58',payload['k_label']+'b',True,offset=-.55);arrow(p,c,'#80b0dc',r'$\lambda a$',True,offset=.55)
 for pt,name,delta in [(zero,'O',(-.5,-.35)),(p,'P',(.4,-.4)),(c,'C',(.4,.45))]:
  ax.text(*(pt+np.array(delta)),name,fontsize=12,fontstyle='italic',bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=.3),zorder=6)
fig.tight_layout(pad=.5);out.parent.mkdir(parents=True,exist_ok=True)
fd,tmp=tempfile.mkstemp(prefix='.render-',suffix='.png',dir=out.parent);os.close(fd)
try:fig.savefig(tmp,dpi=110,facecolor='white');os.replace(tmp,out)
finally:
 if os.path.exists(tmp):os.unlink(tmp)
plt.close(fig)
meta={k:v for k,v in payload.items() if k!='out'};meta.update({'python':sys.version,'matplotlib':matplotlib.__version__,'c':c.tolist(),'p':p.tolist(),'bounds':[lo.tolist(),hi.tolist()]})
fd,tmp=tempfile.mkstemp(prefix='.sidecar-',suffix='.json',dir=out.parent)
with os.fdopen(fd,'w') as f:json.dump(meta,f,indent=2)
os.replace(tmp,out.with_suffix('.json'))
