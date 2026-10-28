"""Local Matplotlib circle renderer. No runtime imports from the repository."""
import os,sys,json,re,math,tempfile
from pathlib import Path
from fractions import Fraction
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'course-academy-circle-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def render_circle(p,output):
    h,k,r=(float(Fraction(p[s])) if 'sqrt' not in p[s] else math.sqrt(float(re.search(r'sqrt\((.*?)\)',p[s])[1])) for s in ('h','k','r'))
    def label(s):
        try:
            v=Fraction(s)
            if v.denominator==1:return str(v.numerator)
            return ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'
        except ValueError:
            return re.sub(r'sqrt\((.*?)\)',r'\sqrt{\1}',s)
    fig,ax=plt.subplots(figsize=(5,5));pad=max(1,r*.28)
    xlim=(min(h-r,0)-pad,max(h+r,0)+pad);ylim=(min(k-r,0)-pad,max(k+r,0)+pad)
    ax.set_xlim(*xlim);ax.set_ylim(*ylim);ax.set_aspect('equal');ax.axis('off')
    ax.annotate('',xy=(xlim[1],0),xytext=(xlim[0],0),arrowprops={'arrowstyle':'->','color':'black','linewidth':1.3});ax.annotate('',xy=(0,ylim[1]),xytext=(0,ylim[0]),arrowprops={'arrowstyle':'->','color':'black','linewidth':1.3})
    ax.text(xlim[1],-.05*(ylim[1]-ylim[0]),'$x$',ha='right');ax.text(.03*(xlim[1]-xlim[0]),ylim[1],'$y$',va='top')
    t=[i*2*math.pi/720 for i in range(721)];ax.plot([h+r*math.cos(z) for z in t],[k+r*math.sin(z) for z in t],color='#ff2020',linewidth=1.7);ax.plot([h],[k],'o',color='#ff2020',markersize=4)
    if p['orientation']=='horizontal':
        endpoint=(h+r,k);ax.plot([h,h+r],[k,k],color='blue',linestyle=(0,(3,3)),linewidth=1)
        bracket_y=k+.10*r;label_y=k+.16*r;label_x=h+r/2
        if abs(label_y)<.35*r:bracket_y=k+.40*r;label_y=k+.48*r
        if abs(label_x)<.20*r:label_x=max((h+.25*r,h+.75*r),key=abs)
        ax.annotate('',xy=(h,bracket_y),xytext=(h+r,bracket_y),arrowprops={'arrowstyle':'|-|','color':'black','linewidth':.8});ax.text(label_x,label_y,'$'+label(p['r'])+'$',ha='center',va='bottom',bbox={'facecolor':'white','edgecolor':'none','pad':1.2})
    else:
        endpoint=(h,k+r);ax.plot([h,h],[k,k+r],color='blue',linestyle=(0,(3,3)),linewidth=1)
        label_x=h-.18*r;label_y=k+r/2;ha='right'
        if abs(label_x)<.25*r:label_x=h+.18*r;ha='left'
        if abs(label_y)<.20*r:label_y=max((k+.25*r,k+.75*r),key=abs)
        ax.annotate('',xy=(h-.10*r,k),xytext=(h-.10*r,k+r),arrowprops={'arrowstyle':'|-|','color':'black','linewidth':.8});ax.text(label_x,label_y,'$'+label(p['r'])+'$',ha=ha,va='center',bbox={'facecolor':'white','edgecolor':'none','pad':1.2})
    ax.text(h,k-.19*r,'$C('+label(p['h'])+','+label(p['k'])+')$',ha='center',va='top',fontsize=11,bbox={'facecolor':'white','edgecolor':'none','pad':.8})
    fig.tight_layout(pad=.3);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=130,facecolor='white')
    side={'renderer':'matplotlib','render_version':'circle-plot-3','parameters':p,'center':[h,k],'radius':r,'radius_endpoint':endpoint,'xlim':xlim,'ylim':ylim,'equal_aspect':True,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__}
    output.with_suffix('.json').write_text(json.dumps(side,indent=2));plt.close(fig)
