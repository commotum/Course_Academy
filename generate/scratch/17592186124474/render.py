"""Private Matplotlib renderer, cached Python3.10 dependencies read-only.

Plots illustrate already supplied formulas; they never determine the assessed
prompt. Each restriction panel explicitly labels its interval and endpoint marks.
"""
import json,os,re,sys,uuid
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186124474-mpl'
cache=Path('/home/jake/.cache/uv/wheels-v5/pypi');deps={}
for pkg in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
 candidates=[p for p in (cache/pkg).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
 chosen=sorted(candidates,key=lambda p:tuple(map(int,re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups())) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
 sys.path.insert(0,str(chosen));deps[pkg]=str(chosen)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
D=json.loads(Path(sys.argv[1]).read_text());p=D['parameters'];a,h,k=[float(p[x]) for x in ('a','h','k')];kind=D['kind']
def val(x):return a*x+k if kind=='linear' else a*(x-h)**2+k if kind=='quadratic' else a*np.abs(x-h)+k
def bound(v):return float('-inf') if v=='-oo' else float('inf') if v=='oo' else float(eval(v,{'__builtins__':{}},{'sqrt':np.sqrt}))
ivs=[(bound(lo),bound(hi),l,r) for lo,hi,l,r in D['intervals']]
finite=[x for iv in ivs for x in iv[:2] if np.isfinite(x)]
lo=min([h-3,0]+finite)-1;hi=max([h+3,0]+finite)+1
if kind=='linear':lo,hi=-max(3,abs(k/a)+1),max(3,abs(k/a)+1)
x=np.linspace(lo,hi,1500);y=val(x);yl=min(0,float(y.min()))-1;yh=max(0,float(y.max()))+1
for index,(role,out) in enumerate(zip(D['roles'],D['outputs'])):
 groups=role or [None];fig,axes=plt.subplots(1,len(groups),figsize=(4.8*len(groups),4.1),squeeze=False);clearances=[];geometries=[]
 for ax,j in zip(axes[0],groups):
  ax.set_xlim(lo,hi);ax.set_ylim(yl,yh);ax.set_xlabel('$x$',labelpad=9);ax.set_ylabel('$y$',rotation=0,labelpad=13)
  ax.axhline(0,color='black',lw=.8);ax.axvline(0,color='black',lw=.8)
  ax.annotate('',xy=(hi,0),xytext=(hi-(hi-lo)*.025,0),arrowprops={'arrowstyle':'->','lw':.8})
  ax.annotate('',xy=(0,yh),xytext=(0,yh-(yh-yl)*.025),arrowprops={'arrowstyle':'->','lw':.8})
  ax.grid(alpha=.14);ax.tick_params(labelsize=8)
  ax.plot(x,y,color='#74a9de',ls=':',lw=1.4)
  if j is None:
   ax.plot(x,y,color='#2678bc',lw=1.7);title='Given function';iv=None
  else:
   iv=ivs[j-1];left,right,cl,cr=iv;mask=(x>=left)&(x<=right);ax.plot(x[mask],y[mask],color='#2678bc',lw=1.9)
   for value,closed in ((left,cl),(right,cr)):
    if np.isfinite(value):ax.plot(value,val(value),'o',ms=6,mec='#2678bc',mfc='#2678bc' if closed else 'white',mew=1.3)
   def fmt(v):return '-\\infty' if v==-np.inf else '\\infty' if v==np.inf else f'{v:g}'
   title=['I','II','III'][j-1]+'. $x\\in '+('[' if cl else '(')+fmt(left)+','+fmt(right)+(']' if cr else ')')+'$'
  ax.set_title(title,fontsize=11,pad=13)
  # Same-side witness for HLT or duplicate-output witness on both sides.
  if kind=='linear':witness=val((lo+hi)/4)
  elif iv is None:witness=None
  else:
   left,right,_,_=iv
   if left<h<right:d=min(h-left if np.isfinite(left) else 2,right-h if np.isfinite(right) else 2)/2
   else:
    sample=(left+right)/2 if np.isfinite(left) and np.isfinite(right) else right-1 if np.isfinite(right) else left+1
    d=sample-h
   witness=val(h+d)
  if witness is not None:ax.axhline(witness,color='black',ls='--',lw=.9)
  geometries.append({'interval_index':j,'curve':kind,'a':a,'h':h,'k':k,'xlim':[lo,hi],'ylim':[yl,yh],'interval':list(iv) if iv else None,'horizontal_line':witness})
 fig.tight_layout(pad=1.4);fig.canvas.draw();renderer=fig.canvas.get_renderer()
 for ax in axes[0]:
  # Titles and coordinate labels have measured positive axes-box clearance.
  box=ax.get_window_extent(renderer);title=ax.title.get_window_extent(renderer);xlabel=ax.xaxis.label.get_window_extent(renderer);ylabel=ax.yaxis.label.get_window_extent(renderer)
  margins={'title':title.y0-box.y1,'xlabel':box.y0-xlabel.y1,'ylabel':box.x0-ylabel.x1}
  if min(margins.values())<5:raise RuntimeError('Insufficient label clearance '+str(margins))
  clearances.append(margins)
 out=Path(out);tmp=out.with_name(out.stem+'-'+uuid.uuid4().hex+'.png');fig.savefig(tmp,dpi=120);os.replace(tmp,out);plt.close(fig)
 meta={'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'dependency_paths':deps,'geometry':geometries,'label_clearance_pixels':clearances,'renderer':'Matplotlib','dpi':120}
 side=out.with_suffix('.json');tmp=side.with_name(side.stem+'-'+uuid.uuid4().hex+'.json');tmp.write_text(json.dumps(meta,indent=2));os.replace(tmp,side)
