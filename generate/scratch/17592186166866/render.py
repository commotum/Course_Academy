"""Private atomic Matplotlib renderer; reuses already cached read-only dependencies."""
import json,os,re,sys,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186166866-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
r=json.loads(Path(sys.argv[1]).read_text());p=r['parameters'];h,k,a,b=[p[t] for t in ('h','k','a','b')]
fig,ax=plt.subplots(figsize=(5.4,5.4));theta=np.linspace(0,2*np.pi,801)
x=h+a*np.cos(theta);y=k+b*np.sin(theta)
ax.plot(x,y,color='#2679bf',linewidth=1.8)
xlim=[min(h-a,0)-1,max(h+a,0)+1];ylim=[min(k-b,0)-1,max(k+b,0)+1]
ax.set(xlim=xlim,ylim=ylim,aspect='equal');ax.set_xticks(range(xlim[0],xlim[1]+1));ax.set_yticks(range(ylim[0],ylim[1]+1))
ax.grid(True,color='#e5e5e5',linewidth=.6);ax.tick_params(labelsize=8)
for spine in ax.spines.values():spine.set_visible(False)
ax.annotate('',xy=(xlim[1],0),xytext=(xlim[0],0),arrowprops=dict(arrowstyle='->',color='black'))
ax.annotate('',xy=(0,ylim[1]),xytext=(0,ylim[0]),arrowprops=dict(arrowstyle='->',color='black'))
ax.text(xlim[1]-.2,.28,'$x$',fontsize=13);ax.text(.22,ylim[1]-.25,'$y$',fontsize=13)
if h or k:
 ax.plot(h,k,'o',color='#e6a000',ms=4);ax.text(h,k-.45,f'({h},{k})',ha='center',fontsize=10)
 ax.plot([h,h+a],[k,k],color='#aaa',linestyle='--',linewidth=.8);ax.plot([h,h],[k,k+b],color='#aaa',linestyle='--',linewidth=.8)
 ax.text(h+a/2,k+.2,str(a),ha='center',fontsize=10);ax.text(h-.18,k+b/2,str(b),ha='right',fontsize=10)
fig.tight_layout();fig.canvas.draw()
origin_px=ax.transData.transform((0,0)).tolist();unit_x=ax.transData.transform((1,0)).tolist();unit_y=ax.transData.transform((0,1)).tolist();canvas_size=list(fig.canvas.get_width_height())
# Each concurrent producer owns a unique temporary file; final assets atomically replace.
with tempfile.NamedTemporaryFile(suffix='.png',dir=Path(r['png']).parent,delete=False) as f:tmp=Path(f.name)
fig.savefig(tmp,dpi=120);os.replace(tmp,r['png']);plt.close(fig)
side={'parameters':p,'center':[h,k],'semiaxes':[a,b],'axis_unit_scales':[1,1],'bounds':[xlim,ylim],'axis_arrows':['positive x','positive y'],'renderer':'Matplotlib','python':sys.version,'matplotlib':matplotlib.__version__,'dependencies':provenance,'extrema':[h-a,h+a,k-b,k+b],'pixel_transform':{'origin':origin_px,'unit_x':unit_x,'unit_y':unit_y,'canvas_size':canvas_size}}
with tempfile.NamedTemporaryFile('w',suffix='.json',dir=Path(r['side']).parent,delete=False) as f:json.dump(side,f,indent=2);tmp=Path(f.name)
os.replace(tmp,r['side'])
