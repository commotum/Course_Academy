import os, sys, json, math, tempfile
from pathlib import Path
from fractions import Fraction
os.environ.setdefault("MPLCONFIGDIR", "/tmp/course-academy-circle-mpl")
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def render(data,out):
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    h,k,u,v=[float(Fraction(s)) for s in data['coordinates']];r=float(data['radius'])
    pad=max(.9,.26*r)
    bounds=[min(h-r,0)-pad,max(h+r,0)+pad,min(k-r,0)-pad,max(k+r,0)+pad]
    fig,ax=plt.subplots(figsize=(4.8,4.3),dpi=100);ax.set_aspect('equal');ax.set_xlim(bounds[:2]);ax.set_ylim(bounds[2:]);ax.axis('off')
    ax.annotate('',xy=(bounds[1],0),xytext=(bounds[0],0),arrowprops={'arrowstyle':'->','color':'black','lw':1.3})
    ax.annotate('',xy=(0,bounds[3]),xytext=(0,bounds[2]),arrowprops={'arrowstyle':'->','color':'black','lw':1.3})
    ax.annotate('$x$',(bounds[1],0),xytext=(-2,6),textcoords='offset points',fontsize=12)
    ax.annotate('$y$',(0,bounds[3]),xytext=(5,-2),textcoords='offset points',fontsize=12)
    t=[2*math.pi*i/720 for i in range(721)];ax.plot([h+r*math.cos(a) for a in t],[k+r*math.sin(a) for a in t],color='#ff2929',lw=1.7)
    ax.plot([h,u],[k,v],'o',color='#ff2929',ms=4)
    cs=1 if h>=0 else -1;cv=1 if k>0 else -1
    # Prefer the source's radial outward placement, measuring the actual text box
    # before accepting it. Other quadrants can put the label safely inside the
    # circle without crossing its boundary. Never cover an axis or the center mark.
    fig.canvas.draw();renderer=fig.canvas.get_renderer()
    origin=ax.transData.transform((0,0));center=ax.transData.transform((h,k))
    radius_pixels=abs(ax.transData.transform((h+r,k))[0]-center[0])
    def clearance(box):
        axes=not (box.x0<=origin[0]<=box.x1 or box.y0<=origin[1]<=box.y1)
        near=float(((max(box.x0-center[0],0,center[0]-box.x1))**2+(max(box.y0-center[1],0,center[1]-box.y1))**2)**.5)
        far=float(max(((xx-center[0])**2+(yy-center[1])**2)**.5 for xx in (box.x0,box.x1) for yy in (box.y0,box.y1)))
        return bool(axes),near,far
    center_label=None
    for cox,coy in ((8,14),(8,12),(8,10),(4,10),(12,10),(0,10),(16,10)):
        for alignment in ('left' if cs>0 else 'right','center'):
            annotation=ax.annotate('$'+data['labels'][0]+'$',(h,k),xytext=(cs*cox,cv*coy),ha=alignment,va='bottom' if cv>0 else 'top',textcoords='offset points',fontsize=11)
            cbox=annotation.get_window_extent(renderer).expanded(1.06,1.12)
            ca,cn,cf=clearance(cbox)
            if ca and cf<radius_pixels-3 and cn>7:
                center_label=annotation;center_box=[float(cbox.x0),float(cbox.y0),float(cbox.x1),float(cbox.y1)]
                break
            annotation.remove()
        if center_label is not None:break
    if center_label is None:raise RuntimeError('No clear placement for the exact center label')
    radial=(1 if u>=h else -1,1 if v>=k else -1)
    global_side=(1 if u>=0 else -1,1 if v>=0 else -1)
    directions=list(dict.fromkeys([radial,global_side,(1,1),(1,-1),(-1,1),(-1,-1)]))
    point_label=None
    for ox,oy in ((9,10),(16,18),(24,28),(34,38),(48,52),(70,74)):
        for sx,sy in directions:
            annotation=ax.annotate('$'+data['labels'][1]+'$',(u,v),xytext=(sx*ox,sy*oy),ha='left' if sx>0 else 'right',va='bottom' if sy>0 else 'top',textcoords='offset points',fontsize=11)
            box=annotation.get_window_extent(renderer).expanded(1.06,1.12)
            axes_clear,nearest,farthest=clearance(box)
            circle_clear=bool(nearest>radius_pixels+3 or farthest<radius_pixels-3)
            center_clear=bool(nearest>7)
            labels_clear=not box.overlaps(cbox)
            if axes_clear and circle_clear and center_clear and labels_clear:
                point_label=annotation;point_box=[float(box.x0),float(box.y0),float(box.x1),float(box.y1)]
                break
            annotation.remove()
        if point_label is not None:break
    if point_label is None:raise RuntimeError('No clear placement for the exact point label')
    fig.canvas.draw()
    tmp=tempfile.NamedTemporaryFile(dir=out.parent,suffix='.png',delete=False);tmp.close()
    fig.savefig(tmp.name,dpi=140,bbox_inches='tight',facecolor='white');plt.close(fig)
    os.replace(tmp.name,out)
    versions={'python':sys.version.split()[0],'matplotlib':matplotlib.__version__}
    for pkg in ('PIL','contourpy','kiwisolver','fontTools','cycler','packaging','pyparsing','dateutil','six'):
        mod=__import__(pkg);versions[pkg]=getattr(mod,'__version__','unknown')
    side={'renderer':'Matplotlib','versions':versions,'coordinates':data['coordinates'],'radius':data['radius'],'labels':data['labels'],'bounds':bounds,'aspect':'equal','dpi':140,'circle_points':721,'label_measurement_dpi':100,'pixel_coordinate_system':'uncropped Matplotlib canvas, bottom origin','center_label_offset_points':[cs*cox,cv*coy],'center_label_alignment':alignment,'center_label_bbox_pixels':center_box,'point_label_offset_points':[sx*ox,sy*oy],'point_label_bbox_pixels':point_box,'axis_origin_pixels':list(map(float,origin)),'circle_center_pixels':list(map(float,center)),'circle_radius_pixels':float(radius_pixels),'point_label_checks':{'axes_clear':axes_clear,'circle_boundary_clear':circle_clear,'center_mark_clear':center_clear,'other_labels_clear':labels_clear}}
    tmp=tempfile.NamedTemporaryFile(dir=out.parent,mode='w',suffix='.json',delete=False);json.dump(side,tmp,indent=2);tmp.close();os.replace(tmp.name,out.with_suffix('.json'))
