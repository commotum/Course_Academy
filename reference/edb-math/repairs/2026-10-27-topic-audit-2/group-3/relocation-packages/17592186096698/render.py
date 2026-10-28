"""Matplotlib renderer. One immutable unique request per subprocess invocation."""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186096698-mpl-'+str(os.getpid())
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
request=json.loads(Path(sys.argv[1]).read_text())
for item in request:
 dest=Path(item['path']);side=dest.with_suffix('.json');spec=item['spec']
 if dest.exists() and side.exists():continue
 xmin,xmax,ymin,ymax=spec['bounds'];fig,ax=plt.subplots(figsize=(4.0,3.4));ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax)
 for direction in ['right','top']:ax.spines[direction].set_visible(False)
 ax.spines['left'].set_position(('data',0));ax.spines['bottom'].set_position(('data',0));ax.tick_params(labelsize=9)
 tick=spec['tick'];xtick=spec.get('xtick',tick);ax.set_xticks(np.arange(np.ceil(xmin/xtick)*xtick,xmax,xtick));ax.set_yticks(np.arange(np.ceil(ymin/tick)*tick,ymax,tick));
 ax.annotate('',xy=(xmax,0),xytext=(xmin,0),arrowprops=dict(arrowstyle='->',color='black',lw=1.1));ax.annotate('',xy=(0,ymax),xytext=(0,ymin),arrowprops=dict(arrowstyle='->',color='black',lw=1.1));ax.text(xmax,0,' x',fontsize=11);ax.text(0,ymax,'y',fontsize=11)
 xs=np.linspace(xmin,xmax,1400)
 env={'x':xs,'exp':np.exp,'log':np.log,'sqrt':np.sqrt}
 with np.errstate(all='ignore'):
  for i,(curve,color) in enumerate(zip(spec['curves'],spec['colors'])):
   ys=eval(curve,{'__builtins__':{}},env);ys=np.broadcast_to(ys,xs.shape).astype(float).copy()
   ys[(~np.isfinite(ys))|(abs(ys)>max(abs(ymin),abs(ymax))*4)]=np.nan
   # Explicit positive branch domain, and discontinuities individually.
   domain=spec.get('domain_minima',[None]*len(spec['curves']))[i]
   if domain is not None:ys[xs<=domain]=np.nan
   dy=np.abs(np.diff(ys));ys[1:][dy>(ymax-ymin)/2]=np.nan
   ax.plot(xs,ys,color=color,lw=1.7)
   if spec.get('labels'):
    candidates=np.where((xs>xmin+.25*(xmax-xmin))&(xs<xmax-.1*(xmax-xmin))&(ys>ymin+.12*(ymax-ymin))&(ys<ymax-.12*(ymax-ymin)))[0]
    if 'label_x' in spec:candidates=np.array([int(np.argmin(abs(xs-spec['label_x'])))])
    if len(candidates):j=candidates[int(len(candidates)*.55)];ax.annotate('C = '+spec['labels'][i],(xs[j],ys[j]),xytext=tuple(spec.get('label_offsets',[[4,5]]*len(spec['curves']))[i]),textcoords='offset points',color=color,fontsize=9,bbox=dict(facecolor='white',edgecolor='none',alpha=.9,pad=1))
 ax.set_facecolor('white');fig.tight_layout(pad=.8)
 fd,tmp=tempfile.mkstemp(prefix='png-',suffix='.png',dir=dest.parent);os.close(fd)
 fig.savefig(tmp,dpi=135,facecolor='white');plt.close(fig);os.replace(tmp,dest)
 payload={'spec':spec,'python':sys.version,'matplotlib':matplotlib.__version__,'numpy':np.__version__}
 fd,tmp=tempfile.mkstemp(prefix='side-',suffix='.json',dir=dest.parent)
 with os.fdopen(fd,'w') as f:json.dump(payload,f,indent=2)
 os.replace(tmp,side)
