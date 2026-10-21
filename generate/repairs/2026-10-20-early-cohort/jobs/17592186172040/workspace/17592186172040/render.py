"""Matplotlib renderer. Frozen read-only cached Python 3.10 dependencies.
Unique render inputs and atomic outputs are supplied by the main generator.
"""
import sys,os,json,pathlib,tempfile
H=pathlib.Path(__file__).resolve().parent
P=json.loads((H/'render-provenance.json').read_text())
sys.path[:0]=list(P['dependency_paths'].values())
os.environ['MPLCONFIGDIR']='/tmp/kp17592186172040-mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
assert matplotlib.__version__==P['matplotlib']
for item in json.loads(pathlib.Path(sys.argv[1]).read_text()):
 path=pathlib.Path(item['path']);fig,ax=plt.subplots(figsize=(3.8,3.5));bounds=item['bounds'];x0,x1,y0,y1=bounds
 segments=[]
 for x,y,m in item['points']:
  # constant length in data coordinates; direction follows exact instance slope
  dx=.115/(1+m*m)**.5;dy=m*dx;segments.append([(x-dx,y-dy),(x+dx,y+dy)])
 ax.add_collection(LineCollection(segments,colors='#909090',linewidths=.8))
 ax.set(xlim=(x0,x1),ylim=(y0,y1),xlabel='$x$',ylabel='$y$');ax.set_aspect('equal');ax.tick_params(labelsize=8,length=2);ax.xaxis.label.set_size(11);ax.yaxis.label.set_size(11);ax.yaxis.label.set_rotation(0)
 for spine in ax.spines.values():spine.set_color('#666666');spine.set_linewidth(.7)
 if item.get('guide') in ('both','x'):ax.axvline(.75,color='#6666ff',lw=1)
 if item.get('guide') in ('both','y'):ax.axhline(-.75,color='#6666ff',lw=1)
 fig.tight_layout(pad=.6)
 with tempfile.NamedTemporaryFile(dir=path.parent,suffix='.png',delete=False) as f:tmp=pathlib.Path(f.name)
 fig.savefig(tmp,dpi=120,facecolor='white');plt.close(fig);os.replace(tmp,path)
