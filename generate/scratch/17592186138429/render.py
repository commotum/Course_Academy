"""Read-only cached Matplotlib runtime, unique atomic graph rendering."""
import json, os, re, subprocess, sys, tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186138429-mpl'
provenance={}
try: import matplotlib
except ImportError:
    runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
    if sys.version_info[:2]!=(3,10):
        subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
    cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
    for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
        candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
        path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
        sys.path.insert(0,str(path));provenance[package]=str(path)
    import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fractions import Fraction
v=json.loads(Path(sys.argv[1]).read_text()); spec=v['spec'];p={k:Fraction(x) for k,x in spec['parameters'].items()};target=Path(v['output']);cfg=spec['labels']; t,y=map(Fraction,spec['intersection'])
fig,ax=plt.subplots(figsize=(6.4,4.9));fig.subplots_adjust(left=.14,bottom=.16,right=.96,top=.93)
ax.set_xlim(0,float(p['xmax']));ax.set_ylim(0,float(p['ymax']))
xs=list(range(0,int(p['xmax'])+1,int(p['dx'])));ys=list(range(0,int(p['ymax'])+1,int(p['dy'])))
ax.set_xticks(xs);ax.set_xticklabels([str(x) if x and x%p['xlabel_step']==0 else '' for x in xs]);ax.set_yticks(ys);ax.set_yticklabels([str(x) if x and x%p['ylabel_step']==0 else '' for x in ys]);ax.grid(color='#cccccc',linewidth=.8);ax.set_axisbelow(True)
for key,color,label in zip(('a','b'),('#eda600','#2474b4'),cfg['labels']):
    x=[0,float(p['xmax'])];yy=[float(p[key+'0']),float(p[key+'0']+p[key+'1']*p['xmax'])]
    ax.plot(x,yy,color=color,lw=2)
    pos=.18*float(p['xmax']);yp=float(p[key+'0']+p[key+'1']*Fraction(str(pos)))
    offset=(12 if key=='a' else -19) if spec['template'] in ('cars','planes','tanks') else (12 if key=='b' else -19)
    if yp/float(p['ymax'])<.12 and offset<0:offset=12
    box=dict(facecolor='white',edgecolor='none',alpha=1,pad=1) if spec['template'] in ('planes','tanks') else None
    ax.annotate(label,(pos,yp),xytext=(0,offset),textcoords='offset points',color=color,fontsize=12,bbox=box)
for spine in ('top','right'):ax.spines[spine].set_color('#cccccc')
ax.set_xlabel(cfg['x_label'],fontsize=12);ax.set_ylabel(cfg['y_label'],fontsize=12)
ax.annotate('',xy=(float(p['xmax']),0),xytext=(0,0),arrowprops=dict(arrowstyle='->',color='black'))
ax.annotate('',xy=(0,float(p['ymax'])),xytext=(0,0),arrowprops=dict(arrowstyle='->',color='black'))
if spec['annotated']:
    ax.plot(float(t),float(y),'o',color='black',ms=5);ax.plot([float(t),float(t)],[0,float(y)],'--',color='#777777',lw=1)
    ax.plot([0,float(t)],[float(y),float(y)],'--',color='#777777',lw=1)
    ax.annotate('('+str(t)+', '+str(y)+')',(float(t),float(y)),xytext=(10,13),textcoords='offset points',fontsize=12,bbox=dict(facecolor='white',edgecolor='none',alpha=.9))
with tempfile.NamedTemporaryFile(suffix='.png',dir=target.parent,delete=False) as f:temp=Path(f.name)
fig.savefig(temp,dpi=130,facecolor='white');plt.close(fig);os.replace(temp,target)
side={**spec,'renderer_revision':'wordgraphs5' if spec['template'] in ('planes','tanks') else 'wordgraphs4','grid_x_ticks':xs,'numbered_x_ticks':[x for x in xs if x and x%p['xlabel_step']==0],'plotted_line_endpoints':{key:[[0,str(p[key+'0'])],[str(p['xmax']),str(p[key+'0']+p[key+'1']*p['xmax'])]] for key in ('a','b')},'annotation_point':[str(t),str(y)] if spec['annotated'] else None,'renderer':{'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance}}
with tempfile.NamedTemporaryFile(mode='w',suffix='.json',dir=target.parent,delete=False) as f:json.dump(side,f,indent=2);temp=Path(f.name)
os.replace(temp,target.with_suffix('.json'))
