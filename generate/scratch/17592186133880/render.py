"""Private Matplotlib quiver renderer; exact supplied instance, atomic assets."""
import json,os,re,sys,subprocess,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186133880-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):subprocess.run([str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]],check=True);sys.exit()
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path)
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
request=json.loads(Path(sys.argv[1]).read_text());data=request['data'];output=Path(request['output'])
M=np.array(data['matrix'],dtype=float);b=np.array(data['drift'],dtype=float);scale=data['scale']
grid=np.arange(-3,4,dtype=float) if data['domain']=='plane' else np.arange(.5,4,.5)
X,Y=np.meshgrid(grid,grid);U=scale*(M[0,0]*X+M[0,1]*Y+b[0]);V=scale*(M[1,0]*X+M[1,1]*Y+b[1])
# Uniform normalization preserves relative arrow lengths, never direction-only normalization.
plot_scale=max(1,float(np.sqrt(U**2+V**2).max()))/0.58
fig,ax=plt.subplots(figsize=(5.5,5.5));ax.set_aspect('equal')
q=ax.quiver(X,Y,U,V,angles='xy',scale_units='xy',scale=plot_scale,color='#708797',pivot='tail',width=.005,headwidth=3.5,headlength=4.5,minlength=0)
if data['domain']=='plane':bounds=[-3.8,3.8]
else:bounds=[0,4.2]
ax.set_xlim(bounds);ax.set_ylim(bounds);ax.axhline(0,color='black',lw=.8);ax.axvline(0,color='black',lw=.8)
ax.set_xticks([]);ax.set_yticks([]);ax.set_xlabel('$x$',loc='right');ax.set_ylabel('$y$',loc='top',rotation=0)
for spine in ax.spines.values():spine.set_visible(False)
fig.canvas.draw()
# Read actual quiver display paths after draw: endpoint geometry in data coordinates.
# q.scale converts supplied U/V; path geometry is independently checked by worker.
paths=q.get_paths(); offsets=q.get_offsets(); trans=q.get_transform()
polygons=[]
for offset,path in zip(offsets,paths):
 vertices=trans.transform(path.vertices)+ax.transData.transform(offset)
 polygons.append(ax.transData.inverted().transform(vertices).tolist())
side={'data':data,'grid':grid.tolist(),'samples':[[float(x),float(y),float(u),float(v)] for x,y,u,v in zip(X.ravel(),Y.ravel(),q.U,q.V)],'rendered_arrow_polygons':polygons,'plot_scale':plot_scale,'bounds':bounds,'python':sys.version,'matplotlib':matplotlib.__version__,'dependencies':provenance}
with tempfile.NamedTemporaryFile(suffix='.png',dir=output.parent,delete=False) as f:tmp=Path(f.name)
try:fig.savefig(tmp,dpi=140,bbox_inches='tight',facecolor='white');os.replace(tmp,output)
finally:tmp.unlink(missing_ok=True)
plt.close(fig)
side['png_sha256']=__import__('hashlib').sha256(output.read_bytes()).hexdigest()
with tempfile.NamedTemporaryFile(mode='w',suffix='.json',dir=output.parent,delete=False) as f:json.dump(side,f,indent=2);tmp=Path(f.name)
os.replace(tmp,output.with_suffix('.json'))
