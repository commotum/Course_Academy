"""Local, parameter-only Matplotlib diagram renderer; never publishes assets."""
import json
import math
import os
from pathlib import Path
import tempfile


def render(p, output):
    os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'diameter-circle-mpl'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    x1, y1, x2, y2 = [p[a] for a in ('x1', 'y1', 'x2', 'y2')]
    h, k = (x1+x2)/2, (y1+y2)/2
    r = math.hypot(x1-x2, y1-y2)/2
    # Generous margin leaves room for outward endpoint labels at all orientations.
    margin = max(2.2, r * .42)
    bounds = [min(0,h-r)-margin, max(0,h+r)+margin,
              min(0,k-r)-margin, max(0,k+r)+margin]
    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_aspect('equal')
    ax.set_xlim(bounds[:2]); ax.set_ylim(bounds[2:]); ax.axis('off')
    ax.annotate('', xy=(bounds[1]-.25,0), xytext=(bounds[0],0),
                arrowprops={'arrowstyle':'->','color':'black','lw':1.1})
    ax.annotate('', xy=(0,bounds[3]-.25), xytext=(0,bounds[2]),
                arrowprops={'arrowstyle':'->','color':'black','lw':1.1})
    ax.annotate('$x$',(bounds[1]-.25,0),xytext=(-2,-15),textcoords='offset points')
    ax.annotate('$y$',(0,bounds[3]-.25),xytext=(7,-2),textcoords='offset points')
    ax.add_patch(Circle((h,k),r,fill=False,color='red',lw=1.5))
    ax.plot([x1,x2],[y1,y2],color='blue',lw=.8,ls=(0,(5,4)))
    ax.plot([x1,x2],[y1,y2],'.',color='red',ms=6)
    labels=[]
    for name,x,y in [('X',x1,y1),('Y',x2,y2)]:
        dx,dy=x-h,y-k
        ox=7 if dx>=0 else -7
        oy=9 if dy>=0 else -9
        labels.append(ax.annotate(f'${name}({x},{y})$',(x,y),xytext=(ox,oy),
               textcoords='offset points',ha='left' if ox>0 else 'right',
               va='bottom' if oy>0 else 'top',fontsize=10))
    fig.tight_layout(pad=.8); fig.canvas.draw()
    # Verify label bounds in image coordinates as well as recording the geometry.
    extent=fig.bbox
    boxes=[t.get_window_extent(fig.canvas.get_renderer()) for t in labels]
    if not all(b.x0>=extent.x0 and b.x1<=extent.x1 and b.y0>=extent.y0 and b.y1<=extent.y1 for b in boxes):
        plt.close(fig)
        raise ValueError('Endpoint label would clip')
    fig.savefig(output,dpi=110,facecolor='white'); plt.close(fig)
    meta={'renderer_version':'diameter-portable-1','parameters':p,'center':[h,k],
          'radius':r,'bounds':bounds,'equal_aspect':True,'labels_inside_image':True,
          'matplotlib':matplotlib.__version__}
    output.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
    return meta
