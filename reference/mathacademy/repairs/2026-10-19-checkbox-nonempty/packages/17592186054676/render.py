"""Render supplied coordinates; never sample or encode membership visually."""
import json, os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/course-academy-pointline-mpl')

def render_plot(p, target):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 xs,ys=zip(*p['points'])
 lo=min(-2,*xs)-2;hi=max(2,*xs)+2
 bottom=min(-2,*ys)-2;top=max(2,*ys)+2
 fig,ax=plt.subplots(figsize=(5,5),dpi=120)
 ax.set_xlim(lo,hi);ax.set_ylim(bottom,top);ax.set_aspect('equal')
 ax.set_xticks(range(lo,hi+1));ax.set_yticks(range(bottom,top+1))
 ax.grid(color='#c8c8c8',linewidth=.65);ax.set_axisbelow(True)
 for name in ('left','bottom'):ax.spines[name].set_position('zero')
 for name in ('right','top'):ax.spines[name].set_visible(False)
 ax.tick_params(labelsize=8,length=2)
 ax.set_xticklabels([str(x) if x else '' for x in range(lo,hi+1)])
 ax.set_yticklabels([str(y) if y else '' for y in range(bottom,top+1)])
 ax.annotate('',xy=(hi,0),xytext=(lo,0),arrowprops={'arrowstyle':'->','color':'black'})
 ax.annotate('',xy=(0,top),xytext=(0,bottom),arrowprops={'arrowstyle':'->','color':'black'})
 ax.text(hi-.5,.5,'x',fontsize=11);ax.text(.4,top-.7,'y',fontsize=11)
 labels=[]
 for label,(x,y) in zip('ABC',p['points']):
  ax.plot(x,y,'o',color='red',markersize=4,zorder=5)
  labels.append(ax.annotate(label,(x,y),xytext=(6,8),textcoords='offset points',fontsize=11,bbox={'facecolor':'white','edgecolor':'none','alpha':.9,'pad':.3}))
 fig.tight_layout(pad=1);fig.canvas.draw();renderer=fig.canvas.get_renderer()
 bounds=[list(a.get_window_extent(renderer).bounds) for a in labels];w,h=fig.canvas.get_width_height()
 assert all(0<=x and 0<=y and x+ww<=w and y+hh<=h for x,y,ww,hh in bounds)
 for i,(x,y,ww,hh) in enumerate(bounds):
  for xx,yy,www,hhh in bounds[i+1:]:assert x+ww<=xx or xx+www<=x or y+hh<=yy or yy+hhh<=y
 target=Path(target);fig.savefig(target,metadata={'Software':'Course Academy point-line v3'});plt.close(fig)
 target.with_suffix('.json').write_text(json.dumps({'parameters':p,'plotted_points':dict(zip('ABC',p['points'])),'bounds':[lo,hi,bottom,top],'label_pixel_bounds':bounds,'canvas':[w,h],'labels_not_clipped':True,'equal_aspect':True,'renderer':{'matplotlib':matplotlib.__version__}},indent=2)+'\n')
