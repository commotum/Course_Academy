"""Matplotlib plots from a shared exact contextual instance, no resampling."""
import json
import os
from pathlib import Path
import tempfile
from fractions import Fraction

os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'course-academy-word-graphs-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def render(spec,target):
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    p={k:Fraction(v) for k,v in spec['parameters'].items()}
    t,y=map(Fraction,spec['intersection']);cfg=spec['labels']
    fig,ax=plt.subplots(figsize=(6.4,4.9))
    fig.subplots_adjust(left=.14,bottom=.15,right=.97,top=.87)
    ax.set_xlim(0,float(p['xmax']));ax.set_ylim(0,float(p['ymax']))
    xs=list(range(0,int(p['xmax'])+1,int(p['dx'])))
    ys=list(range(0,int(p['ymax'])+1,int(p['dy'])))
    ax.set_xticks(xs);ax.set_xticklabels([str(x) if x%p['xlabel_step']==0 else '' for x in xs])
    ax.set_yticks(ys);ax.set_yticklabels([str(v) if v%p['ylabel_step']==0 else '' for v in ys])
    ax.grid(color='#ccc',linewidth=.7);ax.set_axisbelow(True)
    colors=('#1659bd','#d72b28') if spec['template']=='walkers' else ('#bd8500','#2474b4')
    endpoints={}
    for key,color,label in zip(('a','b'),colors,cfg['labels']):
        intercept,rate=p[key+'0'],p[key+'1']
        end=min(p['xmax'],-intercept/rate) if rate<0 else min(p['xmax'],(p['ymax']-intercept)/rate)
        if spec['template']=='tanks':
            # Both amounts stop changing when the donor is empty.
            end=min(end,-p['a0']/p['a1'])
        elif spec['template']=='walkers' and key=='a':
            # Mary's starting distance identifies the community park.
            end=min(end,(p['b0']-intercept)/rate)
        ax.plot([0,float(end)],[float(intercept),float(intercept+rate*end)],color=color,lw=2,label=label)
        endpoints[key]=[['0',str(intercept)],[str(end),str(intercept+rate*end)]]
    ax.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,frameon=False,fontsize=11)
    ax.set_xlabel(cfg['x_label'],fontsize=12);ax.set_ylabel(cfg['y_label'],fontsize=12)
    for side in ('top','right'):ax.spines[side].set_color('#ccc')
    if spec['annotated']:
        ax.plot(float(t),float(y),'o',color='black',ms=5)
        ax.plot([float(t),float(t)],[0,float(y)],'--',color='#666',lw=1)
        ax.plot([0,float(t)],[float(y),float(y)],'--',color='#666',lw=1)
        ax.annotate(f'({t}, {y})',(float(t),float(y)),xytext=(9,13),textcoords='offset points',fontsize=11,bbox=dict(facecolor='white',edgecolor='none',alpha=.95))
    with tempfile.NamedTemporaryFile(suffix='.png',dir=target.parent,delete=False) as f: tmp=Path(f.name)
    try:
        fig.savefig(tmp,dpi=130,facecolor='white');os.replace(tmp,target)
    finally:
        plt.close(fig);tmp.unlink(missing_ok=True)
    target.with_suffix('.json').write_text(json.dumps({**spec,'plotted_line_endpoints':endpoints,'annotation_point':list(map(str,(t,y))) if spec['annotated'] else None,'matplotlib':matplotlib.__version__},indent=2))
