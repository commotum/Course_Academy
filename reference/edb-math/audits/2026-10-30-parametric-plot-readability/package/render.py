import json,os,sys,tempfile
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-parametric-mpl')
import matplotlib
provenance={}
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
D=json.loads(Path(sys.argv[1]).read_text());out=Path(D['output_dir']);out.mkdir(parents=True,exist_ok=True)
def evaluate(s,t):
 env={'t':t,'sqrt':np.sqrt,'cos':np.cos,'sin':np.sin,'pi':np.pi}
 return np.broadcast_to(eval(s,{'__builtins__':{}},env),t.shape).copy()
def scalar(s):return eval(s,{'__builtins__':{}},{'pi':np.pi,'oo':np.inf})
curves=[]
for s in D['bank']:
 lo,hi=scalar(s['lo']),scalar(s['hi'])
 # Infinite positive reciprocal domain is viewport-clipped, never truncated as
 # an assessed closed segment and never joined across its singularity.
 t=np.geomspace(.002,2000,3000) if s['kind']=='rational' else np.linspace(lo,hi,1601)
 x=evaluate(s['x'],t);y=evaluate(s['y'],t);curves.append((s,t,x,y))
if any(s['kind']=='rational' for s,*_ in curves):
 # Meaningful observed table points set a common window for all five options.
 points=[]
 for s,*_ in curves:
  t=np.array([scalar(v) for v in D['ts']]);points.extend(zip(evaluate(s['x'],t),evaluate(s['y'],t)))
 xs,ys=zip(*points);xl=(min(0,min(xs))-1,max(xs)+2);yl=(min(0,min(ys))-1,max(ys)+2)
else:
 xs=np.concatenate([x for _,_,x,_ in curves]);ys=np.concatenate([y for _,_,_,y in curves]);dx=max(2,np.ptp(xs));dy=max(2,np.ptp(ys));xl=(min(0,np.min(xs))-.1*dx,max(0,np.max(xs))+.1*dx);yl=(min(0,np.min(ys))-.1*dy,max(0,np.max(ys))+.1*dy)
# Equal numeric axis aspect across all options, with same union bounds.
for i in range(6):
 file=out/(f"solution-{D.get('correct',0)}.png" if i==5 else f'choice-{i}.png')
 if file.exists() and file.with_suffix('.json').exists():continue
 s,t,x,y=curves[D.get('correct',0) if i==5 else i]
 fig,ax=plt.subplots(figsize=(4.4,4.4),dpi=120);ax.set_xlim(xl);ax.set_ylim(yl);ax.set_aspect('equal',adjustable='box')
 ax.xaxis.set_major_locator(MaxNLocator(9,integer=True));ax.yaxis.set_major_locator(MaxNLocator(9,integer=True));ax.grid(color='#c8c8c8',linewidth=.65)
 for spine in ax.spines.values():spine.set_visible(False)
 ax.tick_params(length=0,labelsize=9)
 ax.annotate('',(xl[1],0),(xl[0],0),arrowprops={'arrowstyle':'->','color':'#222','lw':1.1},annotation_clip=False)
 ax.annotate('',(0,yl[1]),(0,yl[0]),arrowprops={'arrowstyle':'->','color':'#222','lw':1.1},annotation_clip=False)
 ax.text(xl[1],0,'$x$',ha='left',va='bottom',fontsize=12);ax.text(0,yl[1],'$y$',ha='left',va='bottom',fontsize=12)
 ax.plot(x,y,color='#2477bc',lw=1.5)
 endpoints=[]
 if s['kind'] not in ('ellipse','rational'):
  ax.plot([x[0],x[-1]],[y[0],y[-1]],'o',color='#2477bc',markersize=3);endpoints=[[float(x[0]),float(y[0])],[float(x[-1]),float(y[-1])]]
 if i==5:
  tt=np.array([scalar(v) for v in D['ts']]);ax.plot(evaluate(s['x'],tt),evaluate(s['y'],tt),'o',color='#2477bc',markersize=3.8)
 fig.subplots_adjust(left=.12,right=.90,bottom=.12,top=.90);fig.canvas.draw()
 file=out/(f"solution-{D.get('correct',0)}.png" if i==5 else f'choice-{i}.png')
 fd,tmp=tempfile.mkstemp(prefix=file.stem+'-',suffix='.png',dir=out);os.close(fd)
 try:fig.savefig(tmp,dpi=120,facecolor='white');os.replace(tmp,file)
 finally:Path(tmp).unlink(missing_ok=True);plt.close(fig)
 side={'shape':s,'bounds':[list(xl),list(yl)],'endpoints':endpoints,'curve_arrows':False,'axis_arrows':True,'solution_points':D['ts'] if i==5 else [],'samples':len(t),'renderer':'matplotlib','version':matplotlib.__version__,'python':sys.version,'dependency_paths':provenance}
 fd,tmp=tempfile.mkstemp(prefix=file.stem+'-',suffix='.json',dir=out)
 with os.fdopen(fd,'w') as f:json.dump(side,f,indent=2)
 os.replace(tmp,file.with_suffix('.json'))
