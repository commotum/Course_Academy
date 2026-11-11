"""Deterministic square-grid diagrams; geometry is supplied, never resampled here."""
import os,tempfile
os.environ.setdefault('MPLCONFIGDIR',str(__import__('pathlib').Path(tempfile.gettempdir())/'ca-vector-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from fractions import Fraction as F
from math import floor,ceil,hypot
from label_layout import endpoint_labels
import json

def tex(x):
 x=F(x)
 return str(x.numerator) if x.denominator==1 else ('-' if x<0 else '')+r'\frac{'+str(abs(x.numerator))+'}{'+str(x.denominator)+'}'
def render(s,dest,solution):
 if dest.exists():return
 o=s['origin'];at=lambda p:[p[i]+o[i] for i in (0,1)]
 u,v,t,c=map(at,[s['u'],s['v'],s['target'],s['corner']])
 points=[o,u,v,t,c];lo=[floor(min(p[i] for p in points))-2 for i in (0,1)];hi=[ceil(max(p[i] for p in points))+2 for i in (0,1)]
 # Equal scale and a bounded square grid maintain countable grid cells at UI width.
 width=max(hi[i]-lo[i] for i in (0,1));width=max(width,8)
 mid=[(hi[i]+lo[i])/2 for i in (0,1)];lo=[floor(x-width/2) for x in mid];hi=[x+width for x in lo]
 fig,ax=plt.subplots(figsize=(5.4,5.4),dpi=130);ax.set(xlim=(lo[0],hi[0]),ylim=(lo[1],hi[1]),aspect='equal')
 ax.set_xticks(range(lo[0],hi[0]+1));ax.set_yticks(range(lo[1],hi[1]+1));ax.grid(color='#d4d9df',linewidth=.65);ax.tick_params(length=0,labelbottom=False,labelleft=False)
 for sp in ax.spines.values():sp.set_color('#bdc6d0')
 colors=['#2467aa','#a56a00'];labels=[]
 def arrow(p,q,color,label,solution_segment=False):
  ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=12,linewidth=1.7 if solution_segment else 2,color=color,linestyle='--' if solution_segment else '-',shrinkA=0,shrinkB=0,zorder=3))
  dx,dy=q[0]-p[0],q[1]-p[1];norm=hypot(dx,dy)
  # Reference labels nearer arrow tips; route labels sit outside the triangle.
  f=.53 if solution_segment else .77
  x=p[0]+f*dx;y=p[1]+f*dy
  offset=width*.035
  if solution_segment:
   centroid=[(o[i]+c[i]+t[i])/3 for i in (0,1)];side=1 if (-dy*(x-centroid[0])+dx*(y-centroid[1]))>=0 else -1
  else:side=1
  labels.append((p,q,side,'$'+label+'$',color,solution_segment))
 if solution:
  coeff=[s['a'],s['b']];names=['a','b'];j=s['first'];k=1-j
  arrow(o,c,colors[j],tex(coeff[j])+r'\mathbf{'+names[j]+'}',True)
  arrow(c,t,colors[k],tex(coeff[k])+r'\mathbf{'+names[k]+'}',True)
 arrow(o,u,colors[0],r'\mathbf{a}');arrow(o,v,colors[1],r'\mathbf{b}');arrow(o,t,'#202833',r'\mathbf{c}')
 for point,label in [(o,'O')]+([(c,'X')] if solution else []):
  ax.annotate('$'+label+'$',point,xytext=(-12,-15) if label=='O' else (6,5),textcoords='offset points',fontsize=11,bbox=dict(facecolor='white',edgecolor='none',pad=.5),zorder=6)
 # Place reference labels before route annotations. Test real font boxes against
 # every other label and the arrows, so a dense origin does not hide a label.
 fig.subplots_adjust(left=.035,right=.965,bottom=.035,top=.965)
 fig.canvas.draw();renderer=fig.canvas.get_renderer()
 occupied=[artist.get_window_extent(renderer).expanded(1.15,1.15) for artist in ax.texts]
 segments=[(o,u),(o,v),(o,t)]+([(o,c),(c,t)] if solution else [])
 def cuts(box,p,q):
  p=ax.transData.transform(p);q=ax.transData.transform(q)
  # Liang-Barsky segment/box intersection, including endpoints.
  lower,upper=0.,1.
  for j,bounds in enumerate(((box.x0,box.x1),(box.y0,box.y1))):
   delta=q[j]-p[j]
   if abs(delta)<1e-12:
    if not bounds[0]<=p[j]<=bounds[1]:return False
   else:
    a,b=sorted(((bounds[0]-p[j])/delta,(bounds[1]-p[j])/delta));lower=max(lower,a);upper=min(upper,b)
    if lower>upper:return False
  return True
 for p,q,side,label,color,is_route in sorted(labels,key=lambda x:x[5]):
  if not is_route:continue
  dx,dy=q[0]-p[0],q[1]-p[1];norm=hypot(dx,dy)
  artist=ax.text(0,0,label,color=color,fontsize=12,ha='center',va='center',bbox=dict(facecolor='white',edgecolor='none',pad=.7,alpha=.97),zorder=5)
  options=[]
  for f in ((.53,.65,.38,.8,.2) if is_route else (.77,.5,1.04)):
   for sign in (side,-side):
    for distance in (.035,.055,.075,.10,.14,.18):
     x=p[0]+f*dx-sign*width*distance*dy/norm;y=p[1]+f*dy+sign*width*distance*dx/norm
     artist.set_position((x,y));box=artist.get_window_extent(renderer).expanded(1.16,1.18)
     score=100*sum(box.overlaps(other) for other in occupied)+sum(cuts(box,a,b) for a,b in segments)
     score+=100*int(not ax.bbox.contains(box.x0,box.y0) or not ax.bbox.contains(box.x1,box.y1))
     options.append((score,x,y,box))
  score,x,y,box=min(options,key=lambda v:v[0]);artist.set_position((x,y));occupied.append(box)
  if score>=100:raise ValueError(str(('Could not place label',label,s['u'],s['v'],s['target'],score)))
 witness=endpoint_labels(fig,ax,[('A','a',u,colors[0]),('B','b',v,colors[1]),('C','c',t,'#202833')])
 dest.with_suffix('.json').parent.mkdir(parents=True,exist_ok=True)
 dest.with_suffix('.json').write_text(json.dumps(dict(renderer_version=5,labels=witness,solution=solution,geometry=s),indent=2))
 ax.plot(*o,'o',color='#202833',markersize=3,zorder=6);fig.subplots_adjust(left=.035,right=.965,bottom=.035,top=.965)
 dest.parent.mkdir(parents=True,exist_ok=True);fig.savefig(dest,facecolor='white',metadata={'Software':'Course Academy vector generator'});plt.close(fig)
