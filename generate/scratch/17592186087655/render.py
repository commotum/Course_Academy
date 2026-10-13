"""Private Matplotlib renderer; cached dependency fallback, no installation.
Every invocation uses unique input and temp assets, with atomic final replacement.
"""
import sys,os,json,re,subprocess,tempfile,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087655-mpl'
provenance={}
try:import matplotlib
except ImportError:
    runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
    if sys.version_info[:2]!=(3,10):
        subprocess.run([str(runtime),str(Path(__file__)),sys.argv[1]],check=True);sys.exit(0)
    cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
    for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
        paths=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
        if not paths:raise RuntimeError('Missing cached dependency '+package)
        chosen=sorted(paths,key=lambda p:tuple(map(int,re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups())) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
        sys.path.insert(0,str(chosen));provenance[package]=str(chosen)
    import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
obj=json.loads(Path(sys.argv[1]).read_text());p=obj['parameters'];h,k,r=(float(Fraction(p[s])) if 'sqrt' not in p[s] else math.sqrt(float(re.search(r'sqrt\((.*?)\)',p[s])[1])) for s in ('h','k','r'))
def label(s):
    try:
        v=Fraction(s)
        if v.denominator==1:return str(v.numerator)
        return ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'
    except ValueError:
        return re.sub(r'sqrt\((.*?)\)',r'\sqrt{\1}',s)
fig,ax=plt.subplots(figsize=(5,5));pad=max(1,r*.28)
xlim=(min(h-r,0)-pad,max(h+r,0)+pad);ylim=(min(k-r,0)-pad,max(k+r,0)+pad)
ax.set_xlim(*xlim);ax.set_ylim(*ylim);ax.set_aspect('equal');ax.axis('off')
ax.annotate('',xy=(xlim[1],0),xytext=(xlim[0],0),arrowprops={'arrowstyle':'->','color':'black','linewidth':1.3});ax.annotate('',xy=(0,ylim[1]),xytext=(0,ylim[0]),arrowprops={'arrowstyle':'->','color':'black','linewidth':1.3})
ax.text(xlim[1],-.05*(ylim[1]-ylim[0]),'$x$',ha='right');ax.text(.03*(xlim[1]-xlim[0]),ylim[1],'$y$',va='top')
t=np.linspace(0,2*np.pi,721);ax.plot(h+r*np.cos(t),k+r*np.sin(t),color='#ff2020',linewidth=1.7);ax.plot([h],[k],'o',color='#ff2020',markersize=4)
if p['orientation']=='horizontal':
    endpoint=(h+r,k);ax.plot([h,h+r],[k,k],color='blue',linestyle=(0,(3,3)),linewidth=1)
    bracket_y=k+.10*r;label_y=k+.16*r;label_x=h+r/2
    if abs(label_y)<.35*r:bracket_y=k+.40*r;label_y=k+.48*r
    if abs(label_x)<.20*r:label_x=max((h+.25*r,h+.75*r),key=abs)
    ax.annotate('',xy=(h,bracket_y),xytext=(h+r,bracket_y),arrowprops={'arrowstyle':'|-|','color':'black','linewidth':.8});ax.text(label_x,label_y,'$'+label(p['r'])+'$',ha='center',va='bottom',bbox={'facecolor':'white','edgecolor':'none','pad':1.2})
else:
    endpoint=(h,k+r);ax.plot([h,h],[k,k+r],color='blue',linestyle=(0,(3,3)),linewidth=1)
    label_x=h-.18*r;label_y=k+r/2;ha='right'
    if abs(label_x)<.25*r:label_x=h+.18*r;ha='left'
    if abs(label_y)<.20*r:label_y=max((k+.25*r,k+.75*r),key=abs)
    ax.annotate('',xy=(h-.10*r,k),xytext=(h-.10*r,k+r),arrowprops={'arrowstyle':'|-|','color':'black','linewidth':.8});ax.text(label_x,label_y,'$'+label(p['r'])+'$',ha=ha,va='center',bbox={'facecolor':'white','edgecolor':'none','pad':1.2})
ax.text(h,k-.19*r,'$C('+label(p['h'])+','+label(p['k'])+')$',ha='center',va='top',fontsize=11,bbox={'facecolor':'white','edgecolor':'none','pad':.8})
fig.tight_layout(pad=.3);output=Path(obj['output']);output.parent.mkdir(exist_ok=True)
with tempfile.NamedTemporaryFile(suffix='.png',dir=output.parent,delete=False) as f:temp=Path(f.name)
fig.savefig(temp,dpi=130,facecolor='white');os.replace(temp,output)
side={'renderer':'matplotlib','render_version':'circle-plot-2','parameters':p,'center':[h,k],'radius':r,'radius_endpoint':endpoint,'xlim':xlim,'ylim':ylim,'equal_aspect':True,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'numpy':np.__version__,'dependencies':provenance}
with tempfile.NamedTemporaryFile('w',suffix='.json',dir=output.parent,delete=False) as f:json.dump(side,f,indent=2);temp=Path(f.name)
os.replace(temp,output.with_suffix('.json'));plt.close(fig)
