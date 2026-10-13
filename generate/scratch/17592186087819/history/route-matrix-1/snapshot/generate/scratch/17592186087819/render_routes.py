"""Matplotlib-only direct-route renderer; diagram geometry tied to adjacency matrix.

Cached Python 3.10 wheels are read-only fallback; no environment changes.
Atomic asset and sidecar writes use private unique temporary files.
"""
import json,os,re,subprocess,sys,tempfile,math
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087819-mpl'
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
        sys.path.insert(0,str(path));provenance[package]=str(path)
    import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,FancyArrowPatch,PathPatch
from matplotlib.path import Path as MPath
p=json.loads(Path(sys.argv[1]).read_text());m=p['matrix'];n=len(m);out=Path(p['output'])
# Four stations occupy square corners; triangle for three. Labels stay in nodes,
# endpoints are shortened to node boundaries, every route is its own arrow.
coords=[(-1,-.7),(0,1),(1,-.7)] if n==3 else [(-1,-1),(1,-1),(1,1),(-1,1)]
fig,ax=plt.subplots(figsize=(6.5,6.5));ax.set_aspect('equal');ax.axis('off')
edges=[]
for r,row in enumerate(m):
    x,y=coords[r]
    for c,count in enumerate(row):
        tx,ty=coords[c]
        for k in range(count):
            if r==c:
                # Separate loops by angular offsets on the outer side of node.
                theta=math.atan2(y,x)+(k-(count-1)/2)*.50
                ux,uy=math.cos(theta),math.sin(theta);vx,vy=-uy,ux
                a=(x+.15*ux+.105*vx,y+.15*uy+.105*vy);b=(x+.15*ux-.105*vx,y+.15*uy-.105*vy)
                length=.58+.08*k
                c1=(x+length*ux+.42*vx,y+length*uy+.42*vy);c2=(x+length*ux-.42*vx,y+length*uy-.42*vy)
                path=MPath([a,c1,c2,b],[MPath.MOVETO,MPath.CURVE4,MPath.CURVE4,MPath.CURVE4])
                patch=FancyArrowPatch(path=path,arrowstyle='-|>',mutation_scale=17,color='#2878b8',linewidth=1.8,zorder=1)
            else:
                rad=.11+.15*k
                patch=FancyArrowPatch((x,y),(tx,ty),connectionstyle='arc3,rad='+str(rad),arrowstyle='-|>',shrinkA=19,shrinkB=19,mutation_scale=17,color='#2878b8',linewidth=1.8,zorder=1)
            ax.add_patch(patch);edges.append({'from':r,'to':c,'index':k})
for i,(x,y) in enumerate(coords):
    ax.add_patch(Circle((x,y),.18,facecolor='#e8c8dc',edgecolor='black',linewidth=1.3,zorder=2));ax.text(x,y,'ABCD'[i],ha='center',va='center',fontsize=20,zorder=3)
ax.set_xlim(-1.9,1.9);ax.set_ylim(-1.9,1.9)
fig.canvas.draw()
with tempfile.NamedTemporaryFile(suffix='.png',prefix='route-png-',dir=out.parent,delete=False) as f:tmp=Path(f.name)
try:fig.savefig(tmp,dpi=130,bbox_inches='tight',facecolor='white');os.replace(tmp,out)
finally:tmp.unlink(missing_ok=True)
plt.close(fig)
side={'matrix':m,'edges':edges,'coordinates':coords,'renderer':'Matplotlib FancyArrowPatch','matplotlib':matplotlib.__version__,'python':sys.version,'dependency_paths':provenance}
with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='route-sidecar-',dir=out.parent,delete=False) as f:json.dump(side,f,indent=2);tmp=Path(f.name)
try:os.replace(tmp,out.with_suffix('.json'))
finally:tmp.unlink(missing_ok=True)
