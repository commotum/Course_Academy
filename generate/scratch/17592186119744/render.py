"""Only rendering: same-instance coordinates, cached read-only Matplotlib."""
import json,os,re,sys,subprocess,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186119744-mpl'
provenance={}
try:import matplotlib
except ImportError:
    if sys.version_info[:2]!=(3,10):
        subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',__file__,sys.argv[1]],check=True);sys.exit()
    cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
    for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
        candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
        path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
        sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
    import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=json.loads(Path(sys.argv[1]).read_text());context=np.array(p['context']);segment=np.array(p['segment']);points=np.concatenate([context,segment]);mins=np.minimum(points.min(axis=0),0);maxs=np.maximum(points.max(axis=0),0);ranges=np.maximum(maxs-mins,.5);lo=mins-ranges*.12;hi=maxs+ranges*.14
fig,ax=plt.subplots(figsize=(6.3,5.5));ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_aspect('auto' if p['template'] in ('q-77219','hard_reciprocal_affine') else 'equal',adjustable='box');ax.axis('off')
ax.annotate('',xy=(hi[0],0),xytext=(lo[0],0),arrowprops={'arrowstyle':'->','color':'black','lw':1});ax.annotate('',xy=(0,hi[1]),xytext=(0,lo[1]),arrowprops={'arrowstyle':'->','color':'black','lw':1});ax.text(hi[0],-ranges[1]*.04,'$x$',fontsize=13);ax.text(ranges[0]*.025,hi[1],'$y$',fontsize=13)
ax.plot(context[:,0],context[:,1],color='red',lw=1.8);ax.plot(segment[:,0],segment[:,1],color='blue',lw=2)
# Sources have arrowheads on axes, no traversal arrows on curves. Endpoint
# labels and blue assessed/red contextual segments retain their source roles.
for point,label,i in zip((segment[0],segment[-1]),p['labels'],(0,1)):
    ax.plot(*point,'o',color='blue',ms=4);offset=((-8,-14) if i==0 else (-8,9)) if point[0]<0 else ((7,-14) if i==0 else (7,9));ax.annotate('$t='+label+'$',xy=point,xytext=offset,textcoords='offset points',color='blue',fontsize=11,ha='right' if point[0]<0 else 'left')
fig.tight_layout();fig.canvas.draw();output=Path(p['output']);fd,tmp=tempfile.mkstemp(prefix=output.stem+'-',suffix='.png',dir=output.parent);os.close(fd)
fig.savefig(tmp,dpi=145,facecolor='white');plt.close(fig);os.replace(tmp,output)
p.update({'bounds':[lo.tolist(),hi.tolist()],'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'roles':{'blue':'assessed interval','red':'context continuation','axis_arrows':True,'curve_arrows':False,'axis_scale':'independent for reciprocal-cubic readability' if p['template'] in ('q-77219','hard_reciprocal_affine') else 'equal units'}})
fd,tmp=tempfile.mkstemp(prefix=output.stem+'-',suffix='.json',dir=output.parent)
with os.fdopen(fd,'w') as f:json.dump(p,f,indent=2)
os.replace(tmp,output.with_suffix('.json'))
