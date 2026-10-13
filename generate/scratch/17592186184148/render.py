"""Private Matplotlib PNG renderer. Cached dependencies are read-only.

The primary environment is Python 3.13; the installed cache provides Matplotlib
for Python 3.10. No package installs or shared environment changes are made.
Every input filename is call-specific; PNG and metadata replace atomically.
"""
import hashlib,json,math,os,re,subprocess,sys,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186184148-mpl'
dependency_paths={}
try:import matplotlib
except ImportError:
    runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
    if sys.version_info[:2]!=(3,10):
        subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
    cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
    for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
        candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
        path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
        sys.path.insert(0,str(path));dependency_paths[package]=str(path.resolve())
    import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction

def rational_tex(x,pi=False):
    x=Fraction(x);n=abs(x.numerator);d=x.denominator;sgn='-' if x<0 else ''
    num=(str(n) if n!=1 or not pi else '')+(r'\pi' if pi else '')
    return sgn+(num if d==1 else r'\frac{'+num+'}{'+str(d)+'}')

item=json.loads(Path(sys.argv[1]).read_text());g=item['instance'];path=Path(item['path'])
b=float(Fraction(g['B']));d=float(Fraction(g['D']));T=math.pi/b;M=T/2
ymin=min(-3,d-3);ymax=max(3,d+3);yrange=ymax-ymin
fig,ax=plt.subplots(figsize=(6,4.8),dpi=120)
fig.subplots_adjust(left=.15,right=.94,bottom=.10,top=.91)
ax.set_xlim(-.08*T,1.16*T);ax.set_ylim(ymin,ymax);ax.axis('off')
ax.annotate('',xy=(1.13*T,0),xytext=(-.07*T,0),arrowprops={'arrowstyle':'->','linewidth':1.2,'color':'black'})
ax.annotate('',xy=(0,ymax),xytext=(0,ymin),arrowprops={'arrowstyle':'->','linewidth':1.2,'color':'black'})
ax.plot([T,T],[ymin,ymax],ls=(0,(5,5)),color='.60',lw=.8)
ax.plot([0,M],[d,d],ls=(0,(5,5)),color='.60',lw=.8)
ax.plot([M,M],[0,d],ls=(0,(5,5)),color='.60',lw=.8)
ax.plot([M,M],[0-.012*yrange,0+.012*yrange],color='black',lw=.9)
ax.plot([T,T],[0-.012*yrange,0+.012*yrange],color='black',lw=.9)
ax.plot([-.013*T,.013*T],[d,d],color='black',lw=.9)
# Endpoints meet the clip boundary exactly. These are tails of an unbounded
# curve, not marked finite endpoints; no open/closed circles are drawn.
xlo=math.atan2(1,ymax-d)/b;xhi=math.atan2(1,ymin-d)/b
x=np.linspace(xlo,xhi,1800);y=1/np.tan(b*x)+d
curve=ax.plot(x,y,color='#2676bc',lw=1.65)[0]
labels=[]
side=-1 if d>0 else 1;offset=.025*yrange
labels.append(ax.text(M+.025*T,side*offset,'$'+rational_tex(g['x_mid_pi'],True)+'$',ha='left',va='top' if side<0 else 'bottom',fontsize=13))
labels.append(ax.text(T+.028*T,side*offset,'$'+rational_tex(g['x_asymptote_pi'],True)+'$',ha='left',va='top' if side<0 else 'bottom',fontsize=13))
labels.append(ax.text(-.035*T,d,'$'+rational_tex(g['D'])+'$',ha='right',va='center',fontsize=13))
labels.append(ax.text(1.14*T,-.02*yrange,'$x$',ha='left',va='top',fontsize=14))
labels.append(ax.text(-.01*T,ymax+.015*yrange,'$y$',ha='right',va='bottom',fontsize=14))
fig.canvas.draw();renderer=fig.canvas.get_renderer();xy=ax.transData.transform(np.column_stack([x,y]))
boxes=[]
for t in labels:
    box=t.get_window_extent(renderer);boxes.append({'text':t.get_text(),'bounds':list(box.bounds)})
    assert box.x0>=0 and box.y0>=0 and box.x1<=fig.bbox.width and box.y1<=fig.bbox.height,'Label clipped'
    # Measure actual raster-space distances; no label masks or white boxes.
    dx=np.maximum(np.maximum(box.x0-xy[:,0],xy[:,0]-box.x1),0)
    dy=np.maximum(np.maximum(box.y0-xy[:,1],xy[:,1]-box.y1),0)
    assert float(np.min(np.hypot(dx,dy)))>3,'Curve/text clearance below 3px'
for i,a in enumerate(labels):
    for bb in labels[i+1:]:assert not a.get_window_extent(renderer).overlaps(bb.get_window_extent(renderer)),'Text overlap'
fd,tmp=tempfile.mkstemp(prefix='plot-',suffix='.png',dir=path.parent);os.close(fd)
try:fig.savefig(tmp,facecolor='white');os.replace(tmp,path)
finally:Path(tmp).unlink(missing_ok=True)
metadata={'instance':g,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'dependency_paths':dependency_paths,'width_px':int(fig.bbox.width),'height_px':int(fig.bbox.height),'axes_bounds_px':list(ax.bbox.bounds),'limits':{'x':list(ax.get_xlim()),'y':list(ax.get_ylim())},'branch':{'xlo':xlo,'xhi':xhi,'monotonicity':'strictly decreasing','asymptotes':[0,T],'midpoint':[M,d],'x_intercept':math.atan2(1,-d)/b,'y_intercept':None,'endpoints':'none; clipped unbounded tails'},'labels':boxes,'curve_samples_px':xy[::10].tolist(),'clearance_assertion':'every label >3px from curve and no overlapping text','png_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
fd,tmp=tempfile.mkstemp(prefix='sidecar-',suffix='.json',dir=path.parent)
try:
    with os.fdopen(fd,'w') as f:json.dump(metadata,f,indent=2)
    os.replace(tmp,path.with_suffix('.json'))
finally:Path(tmp).unlink(missing_ok=True)
plt.close(fig)
