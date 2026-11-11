"""Endpoint callouts with explicit leaders, sized in display points.

No geometry is rejected or resampled. Each caption identifies both the named
endpoint and its vector; its leader terminates at that arrow's exact endpoint.
"""
from math import hypot,atan2,cos,sin,pi
import json

def endpoint_labels(fig,ax,items):
    fig.canvas.draw();renderer=fig.canvas.get_renderer();occupied=[];witness=[]
    # Prefer outward radial callouts. Test actual rendered text boxes in pixels;
    # nearby endpoints receive separate captions and explicit unambiguous leaders.
    for endpoint,symbol,point,color in items:
        px,py=ax.transData.transform(tuple(map(float,point)))
        ox,oy=ax.transData.transform((0,0));angle=atan2(py-oy,px-ox)
        text='$'+endpoint+r'\ (\mathbf{'+symbol+'})$'
        artist=ax.annotate(text,tuple(map(float,point)),xytext=(0,0),textcoords='offset points',
            color=color,fontsize=17,ha='center',va='center',zorder=10,
            bbox=dict(facecolor='white',edgecolor=color,linewidth=.7,pad=2,alpha=.98),
            arrowprops=dict(arrowstyle='-',color=color,lw=1.2,shrinkA=2,shrinkB=0))
        choices=[]
        for radius in (22,32,44,58):
            for turn in (0,pi/6,-pi/6,pi/3,-pi/3,pi/2,-pi/2,pi):
                offset=(radius*cos(angle+turn),radius*sin(angle+turn));artist.set_position(offset)
                box=artist.get_window_extent(renderer)
                # Annotation's extent includes the leader, so compare the text
                # patch alone and retain the true endpoint separately.
                artist.update_bbox_position_size(renderer);box=artist.get_bbox_patch().get_window_extent(renderer).expanded(1.08,1.15)
                outside=max(0,ax.bbox.x0-box.x0)+max(0,box.x1-ax.bbox.x1)+max(0,ax.bbox.y0-box.y0)+max(0,box.y1-ax.bbox.y1)
                collisions=sum(box.overlaps(b) for b in occupied)
                # Covering any arrow endpoint hides the exact leader attachment.
                covered=sum(box.contains(*ax.transData.transform(tuple(map(float,p)))) for _,_,p,_ in items)
                choices.append((10000*collisions+1000*covered+100*outside+radius+abs(turn)*3,offset,box))
        score,offset,box=min(choices,key=lambda c:c[0]);artist.set_position(offset);occupied.append(box)
        witness.append(dict(endpoint=endpoint,symbol=symbol,arrow_endpoint=list(map(str,point)),leader_xy=list(map(float,point)),offset_points=list(offset),font_points=17,text=text,score=score))
    return witness
