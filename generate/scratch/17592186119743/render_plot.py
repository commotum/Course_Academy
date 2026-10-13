"""Read-only cached Matplotlib dependencies; question parameters supplied by caller.
Atomic image/sidecar outputs and unique input files make concurrent calls safe.
"""
import json,os,re,sys,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186119743-mpl'
cache=Path('/home/jake/.cache/uv/wheels-v5/pypi');deps={}
for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
 candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
 path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
 sys.path.insert(0,str(path));deps[package]=str(path.resolve())
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
inp=json.loads(Path(sys.argv[1]).read_text());p=inp['parameters'];kind=inp['template'];a=p['a'];n=p['n']
def number(x):return float(eval(str(x),{'__builtins__':{}},{'pi':np.pi}))
lo,hi=number(p['lo']),number(p['hi'])
def curve(ts):
 if kind=='trig2':return [a*np.sin(n*ts),p['b']*np.cos(p['m']*ts)]
 if kind=='spiral':return [a*ts*np.sin(n*ts),p['h']-a*ts*np.cos(n*ts)]
 return [a*np.cos(n*ts),a*np.sin(n*ts),p['c']*ts]
context=(min(0,lo),max(2*np.pi/min(n,p.get('m',n)),hi)) if kind=='trig2' else ((lo,hi+.75*(hi-lo)) if kind=='spiral' else (lo-.25*(hi-lo),hi+.25*(hi-lo)))
fig=plt.figure(figsize=(5.6,4.6));ax=fig.add_subplot(111,projection='3d' if kind=='helix_basis' else None)
if kind!='trig2':ax.plot(*curve(np.linspace(*context,700)),color='red',lw=1.5)
pts=curve(np.linspace(lo,hi,700));ax.plot(*pts,color='blue',lw=2)
for value,label in ((lo,'$t = '+inp['endpoint_tex'][0]+'$'),(hi,'$t = '+inp['endpoint_tex'][1]+'$')):
 point=[v[0] for v in curve(np.array([value]))];ax.scatter(*point,color='blue',s=22)
 if len(point)==2:ax.annotate(label,point,xytext=(7,7),textcoords='offset points',fontsize=10,color='blue')
 else:
  label_point=point.copy()
  if value==lo:label_point[2]-=.10*(hi-lo)*p['c']
  ax.text(*label_point,label,fontsize=10,color='blue',ha='right' if value==lo else 'left')
for frac in (() if kind=='spiral' else (.25,.6,.85)):
 ts=lo+frac*(hi-lo);pair=curve(np.array([ts,ts+.018*(hi-lo)]))
 if len(pair)==2:ax.annotate('',xy=[v[1] for v in pair],xytext=[v[0] for v in pair],arrowprops={'arrowstyle':'->','color':'blue','lw':1.6})
 else:ax.quiver(*[v[0] for v in pair],*[v[1]-v[0] for v in pair],color='blue',arrow_length_ratio=.6,length=1)
allpts=curve(np.linspace(*context,1200));bounds=[]
for j,(values,setter) in enumerate(zip(allpts,(ax.set_xlim,ax.set_ylim,*([ax.set_zlim] if len(allpts)==3 else [])))):
 low=min(0,float(values.min()));high=max(0,float(values.max()));margin=max((high-low)*.14,.3);setter(low-margin,high+margin);bounds.append([low-margin,high+margin])
if kind=='helix_basis':
 ax.set_axis_off();ax.view_init(elev=22,azim=-58)
 for index,label in enumerate(('x','y','z')):
  low,high=bounds[index];axis=[0.,0.,0.];axis[index]=high*.92
  neg=[0.,0.,0.];neg[index]=low
  ax.plot([neg[0],0],[neg[1],0],[neg[2],0],color='black',lw=1)
  ax.quiver(0,0,0,*axis,color='black',arrow_length_ratio=.055,lw=1.2)
  ax.text(*axis,label,fontsize=11,color='black')
else:
 ax.spines[['top','right','left','bottom']].set_visible(False)
 ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero')
 ax.annotate('',xy=(bounds[0][1],0),xytext=(bounds[0][0],0),arrowprops={'arrowstyle':'->','color':'black','lw':1.1})
 ax.annotate('',xy=(0,bounds[1][1]),xytext=(0,bounds[1][0]),arrowprops={'arrowstyle':'->','color':'black','lw':1.1})
 ax.text(bounds[0][1],-.05*(bounds[1][1]-bounds[1][0]),'x',ha='right',fontsize=11)
 ax.text(.03*(bounds[0][1]-bounds[0][0]),bounds[1][1],'y',va='top',fontsize=11)
 ax.set_aspect('equal',adjustable='box')
 from matplotlib.ticker import FuncFormatter
 for axis in (ax.xaxis,ax.yaxis):axis.set_major_formatter(FuncFormatter(lambda value,pos:'' if abs(value)<1e-10 else format(value,'g')))
ax.grid(False);fig.tight_layout()
out=Path(inp['output']);out.parent.mkdir(exist_ok=True)
with tempfile.NamedTemporaryFile(suffix='.png',dir=out.parent,delete=False) as f:tmp=Path(f.name)
fig.savefig(tmp,dpi=130,facecolor='white');plt.close(fig);os.replace(tmp,out)
metadata={'template':kind,'parameters':p,'components':inp['components'],'assessed_interval':[lo,hi],'context_interval':list(context),'bounds':bounds,'blue':'assessed segment increasing t','red':'context only','endpoint_labels':inp['endpoint_tex'],'axis_arrows':len(allpts),'axes':'black origin axes; no panes/grid; 2D ticks authored placement','arrows':0 if kind=='spiral' else 3,'renderer':'Matplotlib','matplotlib':matplotlib.__version__,'python':sys.version,'dependencies':deps}
with tempfile.NamedTemporaryFile(mode='w',suffix='.json',dir=out.parent,delete=False) as f:json.dump(metadata,f,indent=2);name=f.name
os.replace(name,out.with_suffix('.json'))
