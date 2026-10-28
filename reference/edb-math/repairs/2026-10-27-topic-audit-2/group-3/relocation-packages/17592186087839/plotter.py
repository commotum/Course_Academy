"""Portable Matplotlib plot construction from the shared exact instance."""
import json,math,os,tempfile
from fractions import Fraction
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'course-academy-ellipse-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def render_plot(data,path,color='#2576bc'):
    path=Path(path);side=path.with_suffix('.json')
    if path.exists() and side.exists() and color=='#2576bc':return
    a,b=map(lambda k:float(Fraction(data[k])),('a','b'))
    fig,ax=plt.subplots(figsize=(6,4.5));ax.set_aspect('equal');ax.axis('off')
    xmax=a*1.35;ymax=max(b*1.5,a*.7)
    ax.set_xlim(-xmax,xmax);ax.set_ylim(-ymax,ymax)
    t=[2*math.pi*i/1200 for i in range(1201)]
    ax.plot([a*math.cos(v) for v in t],[b*math.sin(v) for v in t],color=color,linewidth=1.7)
    ax.annotate('',xy=(xmax*.97,0),xytext=(-xmax,0),arrowprops={'arrowstyle':'->','linewidth':1.2,'color':'black'})
    ax.annotate('',xy=(0,ymax*.97),xytext=(0,-ymax),arrowprops={'arrowstyle':'->','linewidth':1.2,'color':'black'})
    ax.text(xmax*.98,.08*ymax,'$x$',fontsize=13);ax.text(.05*xmax,ymax*.94,'$y$',fontsize=13)
    label=lambda v:format(v,'g').replace('-','−')
    for x in (-a,a):
        ax.plot([x,x],[-.026*ymax,.026*ymax],color='black',lw=1)
        ax.text(x,-.09*ymax,label(x),ha='center',va='top',fontsize=11)
    for y in (-b,b):
        ax.plot([-.024*xmax,.024*xmax],[y,y],color='black',lw=1)
        ax.text(-.07*xmax,y,label(y),ha='right',va='center',fontsize=11)
    fig.subplots_adjust(left=.04,right=.96,bottom=.05,top=.95)
    fd,tmp=tempfile.mkstemp(suffix='.png',dir=path.parent);os.close(fd)
    try:
        fig.savefig(tmp,dpi=140,facecolor='white');plt.close(fig);os.replace(tmp,path)
        side.write_text(json.dumps({**data,'intercepts':[[-a,0],[a,0],[0,-b],[0,b]],'bounds':[-xmax,xmax,-ymax,ymax],'equal_aspect':True,'matplotlib':matplotlib.__version__},indent=2)+'\n')
    finally:Path(tmp).unlink(missing_ok=True)
