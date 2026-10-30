"""Matplotlib bank rendering with readable, target-independent coordinate grids."""
import hashlib,json,os,sys,tempfile
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/course-academy-parametric-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
from parametric_plot_policy import plot_plan,coordinates,scalar,IMAGE_PIXELS,AXES_RECT,LABEL_POINTS

def render(data):
    out=Path(data['output_dir']);out.mkdir(parents=True,exist_ok=True)
    bank=data['bank'];plan=plot_plan(bank,data['ts']);xl,yl=plan['bounds']
    for i in range(6):
        role=data['correct'] if i==5 else i;shape=bank[role]
        t=np.geomspace(.002,2000,3000) if shape['kind']=='rational' else np.linspace(scalar(shape['lo']),scalar(shape['hi']),1601)
        xy=coordinates(shape,t)
        fig=plt.figure(figsize=(IMAGE_PIXELS/120,IMAGE_PIXELS/120),dpi=120);ax=fig.add_axes(AXES_RECT)
        ax.set_xlim(xl);ax.set_ylim(yl);ax.set_aspect('equal',adjustable='box')
        for axis in (ax.xaxis,ax.yaxis):
            axis.set_major_locator(MultipleLocator(plan['major_step']));axis.set_minor_locator(MultipleLocator(1))
        ax.grid(which='major',color='#bcbcbc',linewidth=.7);ax.grid(which='minor',color='#dedede',linewidth=.55)
        ax.set_axisbelow(True)
        for spine in ax.spines.values():spine.set_visible(False)
        ax.tick_params(which='both',length=0,labelsize=LABEL_POINTS,pad=5)
        ax.annotate('',(xl[1],0),(xl[0],0),arrowprops={'arrowstyle':'->','color':'#222','lw':1.1},annotation_clip=False)
        ax.annotate('',(0,yl[1]),(0,yl[0]),arrowprops={'arrowstyle':'->','color':'#222','lw':1.1},annotation_clip=False)
        ax.annotate('$x$',(xl[1],0),xytext=(5,-6),textcoords='offset points',ha='left',va='top',fontsize=LABEL_POINTS+1)
        ax.annotate('$y$',(0,yl[1]),xytext=(5,2),textcoords='offset points',ha='left',va='bottom',fontsize=LABEL_POINTS+1)
        ax.plot(xy[:,0],xy[:,1],color='#2477bc',lw=1.6)
        if i==5:
            points=np.array(plan['checkpoints'][role]);ax.plot(points[:,0],points[:,1],'o',color='#2477bc',markersize=4)
        fig.canvas.draw();bbox=list(ax.get_window_extent().bounds)
        file=out/(f'solution-{role}.png' if i==5 else f'choice-{i}.png')
        fd,tmp=tempfile.mkstemp(prefix=file.stem+'-',suffix='.png',dir=out);os.close(fd)
        try:fig.savefig(tmp,dpi=120,facecolor='white');os.replace(tmp,file)
        finally:Path(tmp).unlink(missing_ok=True);plt.close(fig)
        side={'shape':shape,'plot_plan':plan,'bounds':plan['bounds'],'axes_pixel_bounds':bbox,'major_ticks':[ax.get_xticks().tolist(),ax.get_yticks().tolist()],'endpoints':[],'coordinate_labels':False,'curve_arrows':False,'axis_arrows':True,'solution_points':data['ts'] if i==5 else [],'samples':len(t),'renderer':'matplotlib','version':matplotlib.__version__,'image_sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
        file.with_suffix('.json').write_text(json.dumps(side,indent=2)+'\n')

if __name__=='__main__':render(json.loads(Path(sys.argv[1]).read_text()))
