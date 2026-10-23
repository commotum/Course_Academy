"""Portable Matplotlib renderer; output path is supplied by the generator."""
import os
from pathlib import Path

def render_curve(f,p,target):
    # Keep Matplotlib's disposable cache next to the explicit asset output.
    os.environ.setdefault('MPLCONFIGDIR',str(Path(target).parent/'.mpl-cache'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    a,b=int(p['a']),int(p['b'])
    if f=='cubic':
        fold_x=4*a**3/27;fold_y=4*a*a*b/9
        xmax=max(5,1.3*fold_x);ymax=max(6*b,1.15*a*a*b)
        t=np.unique(np.concatenate([np.linspace(-max(3,1.15*a),max(a,xmax**(1/3)),3500),[-a,-2*a/3,0]]))
        x=t**3+a*t**2;y=b*t**2
        bounds=(-max(2,.3*fold_x),xmax,-b,ymax)
    elif f in ('harmonic','ellipse'):
        t=np.linspace(0,2*np.pi,2400)
        x=a*np.cos(t) if f=='harmonic' else a*np.sin(t)
        y=b*np.sin(int(p['n'])*t) if f=='harmonic' else b*np.cos(t)
        bounds=(-a-1,a+1,-b-1,b+1)
    elif f=='exp_log':
        # x>0; sample the entire visible log branch including its lower tail.
        t=np.linspace(-b+1e-5,np.log(6)/a,4000)
        x=np.exp(a*t);y=np.log(t+b)
        bounds=(-1,6,-3,max(3,float(np.log(b+np.log(6)/a))+1))
    elif f=='log_product':
        t=np.linspace(-1/a+1e-5,2,4000)
        x=np.log(a*t+1);y=b*t*np.exp(t)
        bounds=(-4, max(3,float(np.log(2*a+1))+1),-b,max(5,3*b))
    else:raise ValueError(f)
    height=max(4,min(9,4*(bounds[3]-bounds[2])/(bounds[1]-bounds[0])))
    fig,ax=plt.subplots(figsize=(4.4,height),dpi=120)
    ax.plot(x,y,color='#2c78b9',lw=1.8)
    ax.set_xlim(bounds[:2]);ax.set_ylim(bounds[2:]);ax.set_aspect('equal',adjustable='box')
    ax.spines[['left','bottom']].set_position('zero');ax.spines[['right','top']].set_visible(False)
    for axis,lo,hi in [(ax.xaxis,*bounds[:2]),(ax.yaxis,*bounds[2:])]:
        step=max(1,int(np.ceil((hi-lo)/8)))
        axis.set_ticks(np.arange(np.ceil(lo/step)*step,hi+.01,step))
    ax.grid(color='#bbbbbb',linewidth=.7);ax.set_axisbelow(True);ax.tick_params(length=0,labelsize=9,pad=4)
    ax.annotate('x',(bounds[1],0),xytext=(4,-6),textcoords='offset points')
    ax.annotate('y',(0,bounds[3]),xytext=(4,0),textcoords='offset points')
    fig.savefig(target,bbox_inches='tight');plt.close(fig)
