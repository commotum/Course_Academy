"""Render the instance's quadrant sign map into the explicit output directory."""
import json, os, sys, tempfile
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'course-academy-sign-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def atomic_json(path,obj):
 with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,suffix='.json',delete=False) as tmp:
  json.dump(obj,tmp,indent=2);tmp.write('\n');name=tmp.name
 os.replace(name,path)

def render(spec,out):
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 ss=spec['signs'];assert len(ss)==4 and set(ss)<=set([-1,1])
 fig,ax=plt.subplots(figsize=(3.54,2.98),dpi=160)
 fig.subplots_adjust(0,.03,.95,.96)
 for s,(x,y) in zip(ss,[(0,0),(-1,0),(-1,-1),(0,-1)]):
  ax.add_patch(Rectangle((x,y),1,1,color='#e8f0f7' if s>0 else '#faeee8',linewidth=0))
 for start,end in [((-1,0),(1.04,0)),((0,-1),(0,1.04))]:ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','color':'black','linewidth':.65},clip_on=False)
 ax.text(1.06,-.08,'$x$',ha='center',fontsize=10);ax.text(-.06,1.09,'$y$',fontsize=10)
 for s,(x,y) in zip(ss,[(.5,.5),(-.5,.5),(-.5,-.5),(.5,-.5)]):ax.text(x,y,'$f(x,y)'+('>0' if s>0 else '<0')+'$',ha='center',va='center',fontsize=10)
 ax.set_xlim(-1,1.13);ax.set_ylim(-1,1.15);ax.axis('off')
 with tempfile.NamedTemporaryFile(dir=out.parent,suffix='.png',delete=False) as tmp:name=tmp.name
 fig.savefig(name,dpi=160,facecolor='white');plt.close(fig);os.replace(name,out)
 atomic_json(out.with_suffix('.json'),{'spec':spec,'renderer':'Matplotlib','python':sys.version,'matplotlib':matplotlib.__version__,'zero_set_is_not_an_axis_style':'The axes are coordinate axes. Actual zero sets are specified by the printed equation and solution.'})
