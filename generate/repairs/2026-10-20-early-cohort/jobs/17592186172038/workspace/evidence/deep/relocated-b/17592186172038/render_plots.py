"""Matplotlib renderer using declared dependencies; atomic output files."""
import sys,os,json,math,tempfile,re
from fractions import Fraction
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186172038-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def atomic(path,write):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(dir=path.parent,suffix=path.suffix);os.close(fd)
 try:write(tmp);os.replace(tmp,path)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)

for item in json.load(open(sys.argv[1])):
 path=Path(item['path']);points=item['points'];slopes=item['slopes'];bounds=item['bounds'];length=.8
 fig,ax=plt.subplots(figsize=(4.3,4.3));ax.set_xlim(bounds[:2]);ax.set_ylim(bounds[2:]);ax.set_aspect('equal');ax.set_axisbelow(True)
 ax.xaxis.set_major_locator(MultipleLocator(1));ax.yaxis.set_major_locator(MultipleLocator(1));ax.grid(color='#dedede',linewidth=.65)
 for name in ['top','right']:ax.spines[name].set_visible(False)
 ax.spines['bottom'].set_position('zero');ax.spines['left'].set_position('zero');ax.spines['bottom'].set_color('#555555');ax.spines['left'].set_color('#555555');ax.tick_params(length=0,labelsize=9)
 ax.annotate('',xy=(bounds[1],0),xytext=(bounds[1]-.2,0),arrowprops=dict(arrowstyle='->',color='#555555'));ax.annotate('',xy=(0,bounds[3]),xytext=(0,bounds[3]-.2),arrowprops=dict(arrowstyle='->',color='#555555'));ax.text(bounds[1]+.1,0,'$x$',fontsize=12);ax.text(0,bounds[3]+.1,'$y$',fontsize=12)
 segments=[]
 for (x,y),s in zip(points,slopes):
  if s=='inf':dx,dy=0,length/2
  else:m=float(Fraction(s));dx=length/2/math.sqrt(1+m*m);dy=m*dx
  ends=[[x-dx,y-dy],[x+dx,y+dy]];segments.append({'center':[x,y],'slope':s,'endpoints':ends});ax.plot([v[0] for v in ends],[v[1] for v in ends],color='#333333',lw=1);ax.plot(x,y,'ko',ms=4)
 if item.get('coordinate_labels'):
  for i,((x,y),exact) in enumerate(zip(points,item['exact_points'])):
   def mathcoord(v):
    f=Fraction(v);return str(f.numerator) if f.denominator==1 else ('-' if f<0 else '')+r'\frac{'+str(abs(f.numerator))+'}{'+str(f.denominator)+'}'
   label='$('+','.join(mathcoord(v) for v in exact)+')$'
   ax.annotate(label,(x,y),xytext=(8,-20 if slopes[i]!='inf' and float(Fraction(slopes[i]))>=0 else 15),textcoords='offset points',fontsize=8,bbox=dict(facecolor='white',alpha=.8,edgecolor='none',pad=.5))
 ax.set_xticks([v for v in ax.get_xticks() if bounds[0]<v<bounds[1] and v!=0]);ax.set_yticks([v for v in ax.get_yticks() if bounds[2]<v<bounds[3] and v!=0])
 fig.subplots_adjust(.08,.08,.91,.91);atomic(path,lambda p:fig.savefig(p,dpi=140,facecolor='white'));plt.close(fig)
 meta={**item,'segments':segments,'renderer':'Matplotlib','python':sys.version,'matplotlib':matplotlib.__version__}
 atomic(path.with_suffix('.json'),lambda p:Path(p).write_text(json.dumps(meta,indent=2)+'\n'))
