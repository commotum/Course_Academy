"""Private frozen Matplotlib renderer. Only native PNG output, no SVG or models.
Already-cached read-only dependencies are pinned by resolved archive paths.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186138428-mpl'
RUNTIME='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
PATHS={
 'matplotlib':'/home/jake/.cache/uv/archive-v0/HviZFZ2pIH08XddX2mgqD',
 'numpy':'/home/jake/.cache/uv/archive-v0/ZFeU_a5Ava2NGErTmJIZm',
 'pillow':'/home/jake/.cache/uv/archive-v0/4-AemGpMwlNQVMB0M4sW_',
 'contourpy':'/home/jake/.cache/uv/archive-v0/rOiyUUTbFpH57t4ICTJgT',
 'kiwisolver':'/home/jake/.cache/uv/archive-v0/qVJjUi_V8kDkQnQcYpnTb',
 'fonttools':'/home/jake/.cache/uv/archive-v0/-uFuYxk4cG7E3BDHUN7Jv',
 'cycler':'/home/jake/.cache/uv/archive-v0/THj4ufV8-Vg8ZUf0r46Xe',
 'packaging':'/home/jake/.cache/uv/archive-v0/NqjZ3HMA44qm2M3tJ5BU-',
 'pyparsing':'/home/jake/.cache/uv/archive-v0/DNk-eXaXMzMFzYuxpGXhw',
 'python-dateutil':'/home/jake/.cache/uv/archive-v0/7_D0IBUmHeCF7hBJvV_D9',
 'six':'/home/jake/.cache/uv/archive-v0/60QjE0Dy59cO7A995nTnS'}
if sys.version_info[:2] != (3,10):
    subprocess.run([RUNTIME,str(Path(__file__)),*sys.argv[1:]],check=True)
    sys.exit(0)
for path in PATHS.values(): sys.path.insert(0,path)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def atomic(path, content):
    with tempfile.NamedTemporaryFile(dir=path.parent,prefix='atomic-',suffix='.json',mode='w',delete=False) as f:
        json.dump(content,f,indent=2); temp=Path(f.name)
    os.replace(temp,path)

def draw(data, role, path):
    xmin,xmax,ymin,ymax=data['bounds']; x,y=data['intersection']
    # Unit-sized Cartesian squares, matching the source's equal-scale axes.
    fig,ax=plt.subplots(figsize=(6.2,5.4),dpi=100)
    ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax),aspect='equal')
    ticksx=np.arange(np.ceil(xmin),np.floor(xmax)+1,dtype=int); ticksy=np.arange(np.ceil(ymin),np.floor(ymax)+1,dtype=int)
    step=data['tick_increment']
    majorx=[t for t in ticksx if t % step == 0]; majory=[t for t in ticksy if t % step == 0]
    ax.set_xticks(majorx); ax.set_yticks(majory)
    if step > 1:
        ax.set_xticks([t for t in ticksx if t % step],minor=True); ax.set_yticks([t for t in ticksy if t % step],minor=True)
    ax.set_xticklabels([str(t) if t else '' for t in majorx]); ax.set_yticklabels([str(t) if t else '' for t in majory])
    ax.grid(which='both',color='#d5d5d5',linewidth=1)
    ax.spines[['right','top']].set_visible(False)
    ax.spines['left'].set_position('zero'); ax.spines['bottom'].set_position('zero')
    ax.spines[['left','bottom']].set_linewidth(1.3)
    ax.tick_params(which='both',length=0,pad=6,labelsize=11)
    ax.annotate('',(xmax,0),(xmin,0),arrowprops={'arrowstyle':'->','color':'black','linewidth':1.3})
    ax.annotate('',(0,ymax),(0,ymin),arrowprops={'arrowstyle':'->','color':'black','linewidth':1.3})
    ax.text(xmax+.25,0,'$x$',fontsize=15,va='center',clip_on=False)
    ax.text(0,ymax+.2,'$y$',fontsize=15,ha='center',clip_on=False)
    plotted=[]; placements=[]; label_artists=[]
    for i,((a,b,c),label,color) in enumerate(zip(data['rows'],data['labels'],data['colors'])):
        xs=np.linspace(xmin,xmax,301); ys=(c-a*xs)/b
        ax.plot(xs,ys,color=color,linewidth=2,zorder=3)
        plotted.append({'a':a,'b':b,'c':c,'samples':[[float(xx),float(yy)] for xx,yy in zip(xs[::30],ys[::30])]})
        if data['intersection']==[3,-2] and data['rows']==[[1,1,1],[2,1,4]]:
            lx,ly=(5.1,-3.85) if i==0 else (2.15,2.45)
        elif data['intersection']==[3,0] and data['rows']==[[4,-1,12],[3,1,9]]:
            lx,ly=(4.1,2.9) if i==0 else (4.1,-2.7)
        else:
            # Candidate anchors stay in-frame and away from the answer/axes.
            candidates=[]
            for frac in np.linspace(.08,.92,23):
                yy=ymin+(ymax-ymin)*frac; xx=(c-b*yy)/a
                if xmin+.3 < xx < xmax-.3 and abs(yy-y)>1.2 and abs(yy)>.5:
                    candidates.append((abs(yy-y),xx,yy))
            _,xx,yy=(max(candidates,key=lambda c:c[2]) if i==0 else min(candidates,key=lambda c:c[2]))
            lx=xx+.3; ly=yy+.2
        artist=ax.text(lx,ly,'$'+label+'$',color=color,fontsize=12,zorder=7,
                bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':1})
        label_artists.append(artist); placements.append([lx,ly])
    if role=='solution':
        ax.plot([x,x],[0,y],linestyle='--',color='#888888',linewidth=1.1,zorder=4)
        ax.plot([0,x],[y,y],linestyle='--',color='#888888',linewidth=1.1,zorder=4)
        ax.plot(x,y,'o',color='black',markersize=5,zorder=8)
        # Coordinate label is an explicit authored solution cue; canonical also uses guides.
        ax.annotate(f'({x},{y})',(x,y),xytext=(10,10),textcoords='offset points',fontsize=11,
                    bbox={'facecolor':'white','edgecolor':'none','alpha':.85})
    fig.tight_layout(pad=1.3)
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer(); frame=ax.get_window_extent(renderer)
    axis_x=ax.transData.transform((0,0))[0]
    for artist in label_artists:
        box=artist.get_window_extent(renderer)
        # Keep text inside the actual raster frame using measured text width,
        # rather than a fixed estimated-width clamp that can detach a label.
        if box.x1 > frame.x1-5:
            px=box.x0-(box.x1-frame.x1+5)
            artist.set_x(ax.transData.inverted().transform((px,box.y0))[0])
        elif box.x0 < frame.x0+5:
            artist.set_x(ax.transData.inverted().transform((frame.x0+5,box.y0))[0])
        box=artist.get_window_extent(renderer)
        # Keep equation boxes away from y-axis tick numerals as well as the
        # intersection; color identifies the displaced label's correct line.
        if box.x0 < axis_x+14 and box.x1 > axis_x-14:
            right=frame.x1-axis_x-20; left=axis_x-frame.x0-20
            prefer_right=(box.x0+box.x1)/2 >= axis_x
            use_right=right >= box.width and (prefer_right or left < box.width)
            pixel_x=axis_x+16 if use_right else axis_x-16-box.width
            new_x=ax.transData.inverted().transform((pixel_x,box.y0))[0]
            artist.set_x(new_x)
    placements=[list(artist.get_position()) for artist in label_artists]
    with tempfile.NamedTemporaryFile(dir=path.parent,prefix='atomic-',suffix='.png',delete=False) as f: tmp=Path(f.name)
    fig.savefig(tmp,dpi=100,facecolor='white'); plt.close(fig); os.replace(tmp,path)
    from PIL import Image
    with Image.open(path) as image: dimensions=list(image.size)
    atomic(path.with_suffix('.json'),{'data':data,'role':role,'plotted_equations':plotted,'label_positions':placements,
      'major_ticks':{'x':[int(t) for t in majorx],'y':[int(t) for t in majory]},'minor_unit_grid':True,'png_dimensions':dimensions,'renderer':'Matplotlib','matplotlib':matplotlib.__version__,'python':sys.version,'dependency_paths':PATHS})

job=json.loads(Path(sys.argv[1]).read_text())
for role,path in job['paths'].items(): draw(job['data'],role,Path(path))
