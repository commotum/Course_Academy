"""Typography QA only; parses actual prompt and renders its grid/box with Matplotlib.
No generated question uses this asset. This does not claim frontend MathJax QA.
"""
from pathlib import Path
import importlib.util,json,sys
import os
os.environ.setdefault('MPLCONFIGDIR',str(h) if 'h' in globals() else '/tmp/matrix-index-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
h=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('validation',h/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
fig,axs=plt.subplots(3,1,figsize=(10,12));records=[]
for ax,level,seed in zip(axs,v.g.LEVELS,(33,44,55)):
 r=v.check(v.g.generate(level,seed,template='display_radio'));a,l,pos=v.read_display(r['question'][':question/problem']);m,n=len(a),len(a[0]);i,j=pos[0]
 ax.set_xlim(-2,n+.6);ax.set_ylim(-m-.7,.7);ax.axis('off');ax.set_aspect('equal');ax.set_title(level.title()+f' — {m}×{n}; box at row{i}, column{j}',fontsize=14)
 for rr,row in enumerate(a,1):
  for cc,x in enumerate(row,1):ax.text(cc-1,-rr+1,str(x),ha='center',va='center',fontsize=18,bbox={'facecolor':'#ddd','edgecolor':'#444','boxstyle':'square,pad=0.18'} if (rr,cc)==(i,j) else None)
 ax.plot([-.3,-.5,-.5,-.3],[.35,.35,-m+.65,-m+.65],color='black');ax.plot([n-.7,n-.5,n-.5,n-.7],[.35,.35,-m+.65,-m+.65],color='black');ax.text(-1.25,-(m-1)/2,l+' =',fontsize=18,ha='center',va='center')
 records.append({'level':level,'record':r,'parsed_shape':[m,n],'parsed_box':[i,j]})
fig.tight_layout();fig.savefig(h/'typography-preview.png',dpi=140);plt.close(fig)
(h/'rendering-validation.json').write_text(json.dumps({'purpose':'Manual typography QA from independently parsed actual displayed prompts; not frontend MathJax certification','dependencies':{'python':sys.version.split()[0],'matplotlib':matplotlib.__version__},'records':records},indent=2)+'\n')
