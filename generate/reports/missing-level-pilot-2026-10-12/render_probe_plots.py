#!/usr/bin/env python3
"""Render matching unit-circle figures for the exact x=5/13 probe."""
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Wedge

folder=Path(__file__).resolve().parent/'assets'
folder.mkdir(exist_ok=True)
x,y=5/13,12/13
theta=math.degrees(math.atan2(y,x))
for role,label in [('prompt','$P$'),('solution',r'$P(\cos\theta,\sin\theta)$')]:
    fig,ax=plt.subplots(figsize=(4.1,4.12))
    ax.set_aspect('equal');ax.set_xlim(-1.5,1.65);ax.set_ylim(-1.5,1.55)
    ax.set_xticks([-1,0,1]);ax.set_yticks([-1,0,1]);ax.grid(color='#dedede',linewidth=.7)
    ax.tick_params(length=0,labelbottom=False,labelleft=False)
    ax.add_patch(Circle((0,0),1,fill=False,color='#2076bd',linewidth=1.5))
    ax.add_patch(Wedge((0,0),.35,0,theta,color='#e1a000'))
    ax.annotate('',(1.53,0),(-1.48,0),arrowprops=dict(arrowstyle='->',color='black',lw=1.3))
    ax.annotate('',(0,1.48),(0,-1.48),arrowprops=dict(arrowstyle='->',color='black',lw=1.3))
    ax.plot([0,x],[0,y],color='black',linewidth=1.5)
    ax.plot(x,y,'o',color='black',markersize=3)
    ax.text(x+.05,y+.03,label,fontsize=10)
    ax.text(.2,.14,r'$\theta$',fontsize=10)
    ax.text(1.53,-.12,'$x$');ax.text(.08,1.48,'$y$')
    for v in (-1,1):
        ax.text(v-.06,-.16,str(v),fontsize=9)
        ax.text(-.19,v-.035,str(v),fontsize=9)
    for spine in ax.spines.values():spine.set_color('#dddddd')
    fig.savefig(folder/f'probe-reciprocal-{role}.png',dpi=150,bbox_inches='tight')
    plt.close(fig)
