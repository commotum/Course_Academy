"""Private fixed Matplotlib renderer and independent raster measurements.
All positions come from one generator instance; no sampling occurs here.
"""
import hashlib, json, math, os, sys, tempfile
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ.setdefault('MPLCONFIGDIR', '/tmp/kp17592186096700-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as DisplayPath
import numpy as np
from PIL import Image

def file_hash(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def atomic_json(path,value):
    fd,n=tempfile.mkstemp(prefix='.atomic-',suffix='.json',dir=Path(path).parent)
    try:
        with os.fdopen(fd,'w') as f:json.dump(value,f,indent=2)
        os.replace(n,path)
    finally:Path(n).unlink(missing_ok=True)

def segment_distance(p,a,b):
    p,a,b=np.array(p),np.array(a),np.array(b);d=b-a
    t=np.dot(p-a,d)/np.dot(d,d)
    return np.linalg.norm(p-(a+max(0,min(1,t))*d))

def raster_measure(path,geometry,transform,labels=None):
    """Read actual PNG blue pixels. Verify tail/tip, shaft line, arrowhead direction.
    Fit expected segment regions independently of patch objects/sidecar labels.
    """
    a=np.array(Image.open(path).convert('RGB'));height,width=a.shape[:2]
    blue=(a[:,:,2].astype(int)-a[:,:,0]>45)&(a[:,:,1].astype(int)-a[:,:,0]>20)&(a[:,:,0]<160)
    yy,xx=np.where(blue);pts=np.column_stack((xx,yy))
    x0,y0,sx,sy=transform
    results={}
    for label,g in geometry.items():
        tail=np.array([x0+float(Fraction(g['tail'][0]))*sx,y0-float(Fraction(g['tail'][1]))*sy])
        tip=np.array([x0+float(Fraction(g['tip'][0]))*sx,y0-float(Fraction(g['tip'][1]))*sy]);d=tip-tail;length=np.linalg.norm(d);e=d/length;n=np.array([-e[1],e[0]])
        along=(pts-tail)@e;cross=(pts-tail)@n
        selected=(along>-3)&(along<length+3)&(abs(cross)<12)
        # Remove all other arrows' regions, which can come close in source plots.
        q=pts[selected];qalong=(q-tail)@e;qcross=(q-tail)@n
        if len(q)<15:raise AssertionError('Arrow raster missing: '+label)
        minlong,maxlong=float(qalong.min()),float(qalong.max())
        tail_band=qcross[(qalong>1)&(qalong<min(12,length*.15))]
        head_band=qcross[(qalong>length-12)&(qalong<length-2)]
        # Original sources use small heads; generated heads have a wider silhouette.
        tail_width=float(np.ptp(tail_band)) if len(tail_band)>1 else 0
        head_width=float(np.ptp(head_band)) if len(head_band)>1 else 0
        shaft=qcross[(qalong>length*.15)&(qalong<length*.7)]
        center_error=abs(float(np.median(shaft))) if len(shaft) else 99
        if abs(minlong)>3.3 or abs(maxlong-length)>3.3:raise AssertionError(f'Tail/tip extent mismatch {label}: {minlong}, {maxlong-length}')
        if center_error>2.1:raise AssertionError('Shaft mismatch '+label)
        if head_width<tail_width+1.5:raise AssertionError(f'Arrow direction/head mismatch {label}: head{head_width} tail{tail_width}')
        actual_tail=tail+minlong*e+float(np.median(shaft))*n
        actual_tip=tail+maxlong*e+float(np.median(shaft))*n
        recovered_tail=[round((actual_tail[0]-x0)/sx),round((y0-actual_tail[1])/sy)]
        recovered_tip=[round((actual_tip[0]-x0)/sx),round((y0-actual_tip[1])/sy)]
        if any(abs((actual_tail[j]-tail[j]))>3.5 or abs((actual_tip[j]-tip[j]))>3.5 for j in (0,1)):raise AssertionError('Raster endpoint component mismatch '+label)
        results[label]={'recovered_tail_grid':recovered_tail,'recovered_tip_grid':recovered_tip,'tail_pixel':tail.tolist(),'tip_pixel':tip.tolist(),'tail_extent_error_px':minlong,'tip_extent_error_px':maxlong-length,'shaft_center_error_px':center_error,'head_width_px':head_width,'tail_width_px':tail_width,'blue_pixels':len(q)}
    label_checks={}
    for label,meta in (labels or {}).items():
        xlo,ylo,xhi,yhi=meta['bbox_pixels_bottom_origin'];margin=meta['clearance_pixels']
        left=max(0,math.floor(xlo-margin));right=min(width,math.ceil(xhi+margin))
        top=max(0,math.floor(height-yhi-margin));bottom=min(height,math.ceil(height-ylo+margin))
        blue_count=int(blue[top:bottom,left:right].sum())
        black_count=int((a[top:bottom,left:right].max(axis=2)<80).sum())
        if blue_count:raise AssertionError('Actual PNG label/arrow clearance failed '+label)
        if black_count<5:raise AssertionError('Actual PNG label missing '+label)
        label_checks[label]={'blue_pixels_within_bbox_and_3px_margin':blue_count,'black_text_pixels':black_count,'association_distance_grid':meta['shaft_association_grid_distance']}
    return {'size':[width,height],'arrows':results,'labels':label_checks,'equal_physical_scale':abs(sx-sy)<.05}

def segment_hits_bbox(a,b,bbox):
    """Clip a real displayed line segment against the measured clearance box."""
    low,high=0.,1.
    for axis,minimum,maximum in ((0,bbox.x0,bbox.x1),(1,bbox.y0,bbox.y1)):
        delta=b[axis]-a[axis]
        if abs(delta)<1e-10:
            if a[axis]<minimum or a[axis]>maximum:return False
            continue
        lo,hi=sorted(((minimum-a[axis])/delta,(maximum-a[axis])/delta))
        low=max(low,lo);high=min(high,hi)
        if low>high:return False
    return True

def arrow_hits_bbox(patch,bbox):
    """Measure actual shaft and triangle, excluding CLOSEPOLY's dummy vertex.

    FancyArrowPatch's straight shaft is a collinear quadratic subpath. Its head
    is a separate closed triangle. Matplotlib's generic multi-subpath bbox test
    can include its non-displayed (0,0) CLOSEPOLY placeholder, so test the real
    segments and filled head explicitly instead. No displayed stroke is removed.
    """
    path=patch.get_path().transformed(patch.get_transform());parts=[];part=[]
    for vertex,code in zip(path.vertices,path.codes):
        if code==DisplayPath.MOVETO:
            if part:parts.append((part,False))
            part=[vertex]
        elif code==DisplayPath.CLOSEPOLY:
            parts.append((part,True));part=[]
        else:part.append(vertex)
    if part:parts.append((part,False))
    for vertices,closed in parts:
        if not closed:
            first,last=vertices[0],vertices[-1];direction=last-first
            if any(abs(direction[0]*(v-first)[1]-direction[1]*(v-first)[0])>1e-6 for v in vertices):raise AssertionError('Unexpected curved shaft')
            if segment_hits_bbox(first,last,bbox):return True
        else:
            if len(vertices)!=3:raise AssertionError('Unexpected arrowhead structure')
            if any(segment_hits_bbox(vertices[i],vertices[(i+1)%3],bbox) for i in range(3)):return True
            for point in ((bbox.x0,bbox.y0),(bbox.x1,bbox.y0),(bbox.x1,bbox.y1),(bbox.x0,bbox.y1)):
                signs=[(vertices[(i+1)%3][0]-vertices[i][0])*(point[1]-vertices[i][1])-(vertices[(i+1)%3][1]-vertices[i][1])*(point[0]-vertices[i][0]) for i in range(3)]
                if all(x>=0 for x in signs) or all(x<=0 for x in signs):return True
    return False

def render(payload):
    config=payload['config'];geometry=config['geometry'];target=Path(payload['output'])
    pts=np.array([[float(Fraction(z)) for z in g[k]] for g in geometry.values() for k in ('tail','tip')])
    xmin=math.floor(pts[:,0].min())-2;xmax=math.ceil(pts[:,0].max())+2
    ymin=math.floor(pts[:,1].min())-2;ymax=math.ceil(pts[:,1].max())+2
    # Fixed 30 pixels per equal grid square; no option/arrow independent scale.
    unit_px=24;width=(xmax-xmin)*unit_px+50;height=(ymax-ymin)*unit_px+50
    fig=plt.figure(figsize=(width/100,height/100),dpi=100);ax=fig.add_axes([25/width,25/height,(width-50)/width,(height-50)/height])
    ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax);ax.set_aspect('equal',adjustable='box')
    ax.set_xticks(range(xmin,xmax+1));ax.set_yticks(range(ymin,ymax+1));ax.grid(color='#d5d5d5',linewidth=.6)
    ax.tick_params(bottom=False,left=False,labelbottom=False,labelleft=False)
    for spine in ax.spines.values():spine.set_color('#d5d5d5')
    patches={}
    for label,g in geometry.items():
        tail=np.array([float(Fraction(v)) for v in g['tail']]);tip=np.array([float(Fraction(v)) for v in g['tip']])
        patch=FancyArrowPatch(tail,tip,arrowstyle='-|>',mutation_scale=13,linewidth=1.8,color='#2c77b8',shrinkA=0,shrinkB=0,zorder=3)
        ax.add_patch(patch);patches[label]=patch
    fig.canvas.draw();renderer=fig.canvas.get_renderer();labels={};placed=[]
    for label,g in geometry.items():
        tail=np.array([float(Fraction(v)) for v in g['tail']]);tip=np.array([float(Fraction(v)) for v in g['tip']]);d=tip-tail;n=np.array([-d[1],d[0]])/np.linalg.norm(d)
        text=ax.text(0,0,'$'+label+'$',fontsize=14,fontweight='bold',ha='center',va='center',zorder=4)
        accepted=False
        # Search nearest local positions first; every candidate remains attached
        # to the central 35–65% of its own shaft and within 0.9 grid square.
        candidates=[(fraction,offset) for fraction in (.5,.45,.55,.4,.6,.35,.65)
                    for offset in (.32,-.32,.4,-.4,.5,-.5,.6,-.6,.7,-.7,.8,-.8,.9,-.9,1.0,-1.0,1.1,-1.1,1.2,-1.2)]
        candidates.sort(key=lambda value:((value[0]-.5)**2*np.dot(d,d)+value[1]**2,abs(value[0]-.5),value[0],value[1]<0))
        for fraction,offset in candidates:
            point=tail+fraction*d+offset*n;text.set_position(point)
            bbox=text.get_window_extent(renderer).expanded(1.12,1.15)
            clearance=bbox.padded(5)
            # 3px visible gap plus half the 2.5px stroke and antialias allowance.
            if any(clearance.overlaps(b) for b in placed):continue
            if any(arrow_hits_bbox(patch,clearance) for patch in patches.values()):continue
            if clearance.x0<25 or clearance.y0<25 or clearance.x1>width-25 or clearance.y1>height-25:continue
            placed.append(clearance);labels[label]={'position':point.tolist(),'bbox_pixels_bottom_origin':[bbox.x0,bbox.y0,bbox.x1,bbox.y1],'offset_grid':offset,'fraction':fraction,'shaft_association_grid_distance':abs(offset),'clearance_pixels':3};accepted=True;break
        if not accepted:raise AssertionError('Measured label clearance failed for '+label)
    fig.canvas.draw();xy=ax.transData.transform([[0,0],[1,1]]);sx=xy[1,0]-xy[0,0];sy=xy[1,1]-xy[0,1]
    transform=[float(xy[0,0]),float(height-xy[0,1]),float(sx),float(sy)]
    fd,tmp=tempfile.mkstemp(prefix='.png-',suffix='.png',dir=target.parent);os.close(fd)
    try:
        fig.savefig(tmp,dpi=100,facecolor='white');os.replace(tmp,target)
    finally:Path(tmp).unlink(missing_ok=True);plt.close(fig)
    measured=raster_measure(target,geometry,transform,labels)
    versions={'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'numpy':np.__version__,'pillow':Image.__version__}
    side={'config':config,'png_sha256':file_hash(target),'transform':transform,'labels':labels,'raster':measured,'runtime':versions,'unit_pixels':unit_px,'axes':False,'tick_labels':False,'background_masks':False}
    atomic_json(target.with_suffix('.json'),side)
    return side

