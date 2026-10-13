"""Matplotlib diagram renderer with read-only cached dependency fallback."""
import os,sys,re,json,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186096652-mpl'
provenance={}
try: import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  import subprocess
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg');import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from math import floor,ceil
p=json.loads(Path(sys.argv[1]).read_text());dest=Path(p['destination']);dest.parent.mkdir(parents=True,exist_ok=True)
O=(0.,0.);u=p['u'];v=p['v'];T=p['target'];P=p['corner']
points=[O,u,v,T,P];xmin=floor(min(x[0] for x in points))-2;xmax=ceil(max(x[0] for x in points))+2;ymin=floor(min(x[1] for x in points))-2;ymax=ceil(max(x[1] for x in points))+2
fig,ax=plt.subplots(figsize=(6,6));ax.set_aspect('equal');ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax)
ax.set_xticks(range(xmin,xmax+1));ax.set_yticks(range(ymin,ymax+1));ax.grid(color='#d8d8d8',linewidth=.7);ax.tick_params(length=0,labelbottom=False,labelleft=False)
for spine in ax.spines.values():spine.set_visible(False)
def arrow(a,b,color,label,dashed=False,offset=(0,0)):
 patch=FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=12,linewidth=1.8,color=color,linestyle='--' if dashed else '-');ax.add_patch(patch)
 x=(a[0]+b[0])/2;y=(a[1]+b[1])/2
 dx=b[0]-a[0];dy=b[1]-a[1];norm=(dx*dx+dy*dy)**.5
 ax.text(x-.4*dy/norm+offset[0],y+.4*dx/norm+offset[1],'$'+label+'$',color=color,fontsize=13,ha='center',va='center',bbox={'facecolor':'white','alpha':.75,'edgecolor':'none','pad':.2})
arrow(O,u,'#327fc1',p['names'][1]);arrow(O,v,'#e69a00',p['names'][2]);arrow(O,T,'#222222',p['names'][0],offset=(.1,-.15))
if p['solution']:
 arrow(O,P,'#6b9ccc' if p['first_index']==0 else '#dfad43',p['path_labels'][0],True)
 arrow(P,T,'#dfad43' if p['first_index']==0 else '#6b9ccc',p['path_labels'][1],True)
 centroid=[(O[i]+P[i]+T[i])/3 for i in (0,1)]
 for xy,label in ((O,'O'),(P,p['segments'][0][1]),(T,p['segments'][1][1])):
  away=[xy[i]-centroid[i] for i in (0,1)];norm=max((away[0]**2+away[1]**2)**.5,.1)
  ax.text(xy[0]+.85*away[0]/norm,xy[1]+.85*away[1]/norm,label,fontstyle='italic',fontsize=12,ha='center',va='center',bbox={'facecolor':'white','alpha':.8,'edgecolor':'none','pad':.3})
fig.tight_layout();tmp=Path(tempfile.mkstemp(suffix='.png',prefix='render-',dir=dest.parent)[1]);fig.savefig(tmp,dpi=130,facecolor='white');plt.close(fig);os.replace(tmp,dest)
p['bounds']=[xmin,xmax,ymin,ymax];p['grid_increment']=1;p['renderer']={'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance}
meta=dest.with_suffix('.json');tmpmeta=Path(tempfile.mkstemp(suffix='.json',prefix='render-',dir=dest.parent)[1]);tmpmeta.write_text(json.dumps(p,indent=2)+'\n');os.replace(tmpmeta,meta)
