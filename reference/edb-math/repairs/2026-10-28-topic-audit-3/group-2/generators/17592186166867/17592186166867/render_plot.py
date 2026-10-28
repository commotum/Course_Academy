"""Read-only cached Matplotlib runtime; unique caller input and atomic outputs."""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186166867-mpl'
dependency_paths={}
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
p=json.loads(Path(sys.argv[1]).read_text());a,b=p['a'],p['b'];c=b*b/a
out=Path(p['out']);out.parent.mkdir(exist_ok=True)
# Scale from the marked point, both branches and the origin remain visible.
xend=abs(a)*2.6;yend=abs(b)*1.65
bounds=[(-.6*abs(a),xend) if a>0 else (-xend,.6*abs(a)),(-yend,yend)]
fig,ax=plt.subplots(figsize=(5.2,4.2));ax.set_xlim(*bounds[0]);ax.set_ylim(*bounds[1]);ax.axis('off')
ax.annotate('',(bounds[0][1],0),(bounds[0][0],0),arrowprops={'arrowstyle':'->','color':'black','lw':1})
ax.annotate('',(0,bounds[1][1]),(0,bounds[1][0]),arrowprops={'arrowstyle':'->','color':'black','lw':1})
ys=np.linspace(-yend,yend,601);xs=ys*ys/c;ax.plot(xs,ys,color='#1c73b9',lw=1.6)
ax.scatter([a],[b],s=28,color='#efa000',zorder=3)
ax.annotate(f'({a}, {b})',(a,b),xytext=(8,-18 if a*b>0 else 8),textcoords='offset points',fontsize=11)
ax.annotate('O',(0,0),xytext=(-13,-14),textcoords='offset points',fontsize=11)
ax.text(bounds[0][1],0,'  x',fontsize=12);ax.text(0,bounds[1][1],' y',fontsize=12)
fig.subplots_adjust(left=.06,right=.94,top=.94,bottom=.06)
with tempfile.NamedTemporaryFile(suffix='.png',dir=out.parent,delete=False) as f: tmp=Path(f.name)
fig.savefig(tmp,dpi=125,facecolor='white');plt.close(fig);os.replace(tmp,out)
side={'parameters':{'a':a,'b':b},'equation_coefficient':str(c),'bounds':bounds,'renderer':'Matplotlib','matplotlib':matplotlib.__version__,'python':sys.version,'dependencies':{'python':sys.version,'matplotlib':matplotlib.__version__,'numpy':np.__version__,'matplotlib_module':matplotlib.__file__,'numpy_module':np.__file__,'cached_dependency_paths':dependency_paths},'curve_samples':[[float(x),float(y)] for x,y in zip(xs[::30],ys[::30])]}
with tempfile.NamedTemporaryFile(mode='w',suffix='.json',dir=out.parent,delete=False) as f:json.dump(side,f,indent=2);tmp=Path(f.name)
os.replace(tmp,out.with_suffix('.json'))
