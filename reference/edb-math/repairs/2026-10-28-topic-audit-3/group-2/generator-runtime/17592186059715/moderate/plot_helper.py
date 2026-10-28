"""Matplotlib endpoint renderer retained and localized from the supplied draft."""
import os,json,hashlib,tempfile
from pathlib import Path
VERSION="position-magnitude-v2"
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def render_plots(points,labels,style,tick=1):
    """Same endpoint data, equal units, unique temporary PNG + atomic sidecar.
    Native source snapshots are reused ONLY for exact source anchors.
    """
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    key=digest({'points':points,'labels':labels,'style':style,'tick':tick,'version':VERSION,'render_revision':4 if any(pt[0]==0 and pt[1]>0 for pt in points) else 3})[:24]
    directory=Path(os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']).resolve();directory.mkdir(parents=True,exist_ok=True)
    path=directory/(key+'.png');side=path.with_suffix('.json')
    if path.exists() and side.exists():return json.loads(side.read_text())
    p,q=points;xs=[0,p[0],q[0]];ys=[0,p[1],q[1]]
    margin=2.0;xl=[min(xs)-margin,max(xs)+margin];yl=[min(ys)-margin,max(ys)+margin]
    fig,ax=plt.subplots(figsize=(6,5),dpi=120);ax.set_xlim(xl);ax.set_ylim(yl);ax.set_aspect('equal',adjustable='box')
    if style=='grid':
        ax.set_xticks(range(int(xl[0])//tick*tick,int(xl[1])+1,tick));ax.set_yticks(range(int(yl[0])//tick*tick,int(yl[1])+1,tick))
        ax.grid(color='#b8b8b8',lw=.7);ax.spines[['top','right']].set_visible(False)
        ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero')
        ax.tick_params(labelsize=10,pad=5)
        for axis in [ax.xaxis,ax.yaxis]:
            from matplotlib.ticker import FuncFormatter
            axis.set_major_formatter(FuncFormatter(lambda v,pos: '' if v==0 else str(int(v))))
    else:ax.axis('off')
    ax.annotate('',xy=(xl[1],0),xytext=(xl[0],0),arrowprops={'arrowstyle':'->','color':'black','lw':1.3})
    ax.annotate('',xy=(0,yl[1]),xytext=(0,yl[0]),arrowprops={'arrowstyle':'->','color':'black','lw':1.3})
    ax.annotate('$x$',(xl[1],0),xytext=(-6,11) if style=='grid' else (-3,-18),textcoords='offset points');ax.annotate('$y$',(0,yl[1]),xytext=(8,-6),textcoords='offset points')
    origin_offset=(-16,-17)
    if style!='grid':
        import math
        rays=[(1,0),(0,1)]+[tuple(pt) for pt in points if any(pt)]
        candidates=[(-16,-17),(-16,12),(10,-17),(10,12)]
        def overlap(offset):
            return max((offset[0]*x+offset[1]*y)/(math.hypot(*offset)*math.hypot(x,y)) for x,y in rays)
        origin_offset=min(candidates,key=overlap)
    ax.annotate('$O$',(0,0),xytext=origin_offset,textcoords='offset points')
    for label,(x,y) in zip(labels,points):
        ax.plot(x,y,'o',color='#2779b8',ms=5,zorder=5)
        # Grid family contains labels alone: coordinates must be read from scale.
        text=label if style=='grid' else f'{label}({x},{y})'
        ax.annotate('$'+text+'$',(x,y),xytext=(9,12 if y>=0 else -20),textcoords='offset points',fontsize=12,zorder=6,bbox={'facecolor':'white','edgecolor':'none','pad':.4})
        if style!='grid':
            ax.annotate('',xy=(x,y),xytext=(0,0),arrowprops={'arrowstyle':'->','color':'#2876b9','lw':1.8})
            length=(x*x+y*y)**.5
            letter_offset=(9,0) if x==0 and y>0 else ((-9*y/length,9*x/length) if length else (8,8))
            ax.annotate('$'+label.lower()+'$',(x*.56,y*.56),xytext=letter_offset,textcoords='offset points',color='#2876b9')
    if style=='position-displacement':ax.annotate('',xy=q,xytext=p,arrowprops={'arrowstyle':'->','color':'#e69800','lw':1.8})
    if style!='grid':
        for endpoint,name in [((1,0),'i'),((0,1),'j')]:
            ax.annotate('',xy=endpoint,xytext=(0,0),arrowprops={'arrowstyle':'->','color':'#d96a28','lw':1.3})
            ax.annotate('$'+name+'$',endpoint,xytext=(5,-15) if name=='i' else (-12,5),textcoords='offset points',color='#d96a28')
    fig.tight_layout(pad=.9);fig.canvas.draw()
    pixel_points=[ax.transData.transform(pt).tolist() for pt in points]
    origin=ax.transData.transform((0,0)).tolist();unitx=ax.transData.transform((1,0)).tolist();unity=ax.transData.transform((0,1)).tolist()
    fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.png',dir=directory);os.close(fd)
    try:fig.savefig(tmp,metadata={'Software':VERSION});os.replace(tmp,path)
    finally:plt.close(fig);Path(tmp).unlink(missing_ok=True)
    asset={'path':str(path),'reference':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'role':'prompt','points':points,'labels':labels,'style':style,'grid_increment':tick,'renderer':'matplotlib','renderer_version':matplotlib.__version__,'dimensions':[720,600],'axes':{'xlim':xl,'ylim':yl,'equal_scale':True,'origin_pixel':origin,'unit_x_pixel':unitx,'unit_y_pixel':unity,'endpoint_pixels':pixel_points}}
    fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.json',dir=directory);os.close(fd);Path(tmp).write_text(json.dumps(asset,indent=2)+'\n');os.replace(tmp,side)
    return asset
