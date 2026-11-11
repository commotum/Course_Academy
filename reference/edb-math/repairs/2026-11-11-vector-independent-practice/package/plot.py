"""Equal-grid vector diagrams. All coordinates are derived from one instance."""
import hashlib,json,math,os,tempfile
from pathlib import Path
from fractions import Fraction
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'course-academy-vector-mpl'))
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def render_plots(p):
 root=Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']);root.mkdir(parents=True,exist_ok=True)
 a=list(map(float,p['a']));b=list(map(float,p['b']));k=float(Fraction(p['k']));r=float(Fraction(p['r']));P=[k*x for x in b];C=[P[i]-r*a[i] for i in (0,1)];zero=[0,0]
 assets={}
 for role in ('prompt','solution'):
  path=role=='solution';data={'version':'grid-v3-independent','a':a,'b':b,'P':P,'C':C,'path':path,'k':k}
  name=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()[:28]+'.png';out=root/name;assets[role]=name
  if out.exists():continue
  points=[zero,a,b,P,C];lo=[math.floor(min(x[i] for x in points))-2 for i in (0,1)];hi=[math.ceil(max(x[i] for x in points))+2 for i in (0,1)]
  fig,ax=plt.subplots(figsize=(4.6,4.6));ax.set_aspect('equal');ax.set_xlim(lo[0],hi[0]);ax.set_ylim(lo[1],hi[1]);ax.set_xticks(range(lo[0],hi[0]+1));ax.set_yticks(range(lo[1],hi[1]+1));ax.grid(color='#dedede',lw=.65);ax.tick_params(length=0,labelbottom=False,labelleft=False)
  for s in ax.spines.values():s.set_visible(False)
  def arrow(start,end,color,label,dashed=False,offset=.4):
   dx,dy=end[0]-start[0],end[1]-start[1];length=math.hypot(dx,dy)
   ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle='->',color=color,lw=1.7,linestyle='--' if dashed else '-'),zorder=3)
   x=(start[0]+end[0])/2-dy/length*offset;y=(start[1]+end[1])/2+dx/length*offset
   ax.text(x,y,label,color=color,fontsize=12,ha='center',va='center',bbox=dict(facecolor='white',edgecolor='none',alpha=.85,pad=.2),zorder=5)
  arrow(zero,a,'#2878b5',r'$\mathbf{a}$');arrow(zero,b,'#c17e00',r'$\mathbf{b}$',offset=-.5);arrow(zero,C,'#202020',r'$\mathbf{c}$')
  if path:
   kval=('-' if k==-1 else '' if k==1 else str(int(k)))
   arrow(zero,P,'#c18c22','$'+kval+r'\mathbf{b}$',True,offset=-.6)
   arrow(P,C,'#5792c4',r'$\lambda\mathbf{a}$',True,offset=.65)
   for pt,n,d in [(zero,'O',(-.6,-.6)),(P,'P',(.6,-.6)),(C,'C',(.6,.6))]:
    ax.text(pt[0]+d[0],pt[1]+d[1],n,fontsize=11,fontstyle='italic',bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=.2),zorder=6)
  fig.tight_layout(pad=.35)
  fd,tmp=tempfile.mkstemp(prefix='.plot-',suffix='.png',dir=root);os.close(fd)
  try:fig.savefig(tmp,dpi=115,facecolor='white',metadata={'Software':'Course Academy grid-v3-independent'});os.replace(tmp,out)
  finally:
   plt.close(fig)
   if Path(tmp).exists():Path(tmp).unlink()
  out.with_suffix('.json').write_text(json.dumps(data|{'bounds':[lo,hi]},indent=2))
 return assets
