"""Deterministic Matplotlib plot from exact radii; no resampling or publication."""
from pathlib import Path
from fractions import Fraction
import json
import math
import os
import tempfile

def render_plot(spec, png, sidecar):
    os.environ.setdefault('MPLCONFIGDIR',str(Path(png).parent/'mpl-cache'))
    import matplotlib
    matplotlib.use('Agg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    a,b = (Fraction(spec[k]) for k in ('a','b'))
    limit=float(b)*1.2
    fig=Figure(figsize=(4.8,4),dpi=100,facecolor='white')
    FigureCanvasAgg(fig)
    ax=fig.add_subplot(111)
    ax.set_aspect('equal');ax.set_xlim(-limit,limit);ax.set_ylim(-limit,limit);ax.axis('off')
    ts=[2*math.pi*i/640 for i in range(641)]
    ax.plot([float(a)*math.cos(t) for t in ts],[float(b)*math.sin(t) for t in ts],color='#2675b5',linewidth=1.8)
    for end,start in [((limit,0),(-limit,0)),((0,limit),(0,-limit))]:
        ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'->','color':'black','lw':1.2})
    labels=[]
    for value,axis in [(a,'x'),(-a,'x'),(b,'y'),(-b,'y')]:
        number=float(value);delta=limit*.014
        if axis=='x':
            ax.plot([number,number],[-delta,delta],color='black',lw=.8)
            pos=(number,-limit*.065);ha='center';va='top'
        else:
            ax.plot([-delta,delta],[number,number],color='black',lw=.8)
            pos=(-limit*.045,number);ha='right';va='center'
        # Supported radii have denominator 1 or 2, so this is exact.
        label=str(value.numerator) if value.denominator==1 else str(float(value))
        ax.text(*pos,label,fontsize=11,ha=ha,va=va,bbox={'facecolor':'white','edgecolor':'none','pad':1.2},zorder=8)
        labels.append({'axis':axis,'value':str(value),'text':label})
    ax.text(limit*.97,limit*.035,'$x$',ha='left',va='bottom',fontsize=13)
    ax.text(limit*.035,limit*.97,'$y$',ha='left',va='bottom',fontsize=13)
    fig.subplots_adjust(left=.04,right=.94,bottom=.06,top=.94)
    png=Path(png);sidecar=Path(sidecar)
    with tempfile.NamedTemporaryFile(suffix='.png',dir=png.parent,delete=False) as f: temporary=f.name
    try:
        fig.savefig(temporary,dpi=100,facecolor='white');os.replace(temporary,png)
    finally:
        Path(temporary).unlink(missing_ok=True);fig.clear()
    data={**spec,'renderer':'Matplotlib','matplotlib_version':matplotlib.__version__,'labels':labels,'bounds':[-limit,limit,-limit,limit], 'curve':{'x':'a cos(t)','y':'b sin(t)','samples':641}}
    with tempfile.NamedTemporaryFile(mode='w',suffix='.json',dir=sidecar.parent,delete=False) as f:
        json.dump(data,f,indent=2);temporary=f.name
    try:os.replace(temporary,sidecar)
    finally:Path(temporary).unlink(missing_ok=True)
