"""Matplotlib diagram renderer; no sampling, image models, or SVG generation.

The cached Python3.10 wheels are used read-only when primary Python lacks MPL.
Each caller supplies a unique input path; figure and metadata writes are atomic.
"""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

os.environ['MPLCONFIGDIR']='/tmp/kp17592186172041-mpl'
provenance={}
try:
    import matplotlib
except ImportError:
    runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
    if sys.version_info[:2]!=(3,10):
        subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True)
        sys.exit(0)
    cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
    for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
        candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
        if not candidates:raise RuntimeError('Missing cached renderer dependency '+package)
        path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
        sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
    import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

data=json.loads(Path(sys.argv[1]).read_text());p=data['parameters']
h,k=p['h'],p['k'];lo_x,hi_x=min(-3,h-2),max(3,h+2);lo_y,hi_y=min(-3,k-2),max(3,k+2)
regions=[]
for sx,sy in ((-1,-1),(-1,1),(1,-1),(1,1)):
    xa,xb=(lo_x,h) if sx<0 else (h,hi_x);ya,yb=(lo_y,k) if sy<0 else (k,hi_y)
    xt,yt=(xa+xb)/2,(ya+yb)/2
    value=(p['ox']*(xt-h))**p['px']*(p['oy']*(yt-k))**p['py'];sign=1 if value>0 else -1
    regions.append({'side':[sx,sy],'bounds':[xa,xb,ya,yb],'test_point':[xt,yt],'value':value,'sign':sign})
for role,destination in data['paths'].items():
    path=Path(destination);path.parent.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(5.2,5.2));ax.set_xlim(lo_x,hi_x);ax.set_ylim(lo_y,hi_y);ax.set_aspect('equal');ax.axis('off')
    if role=='signs':
        for r in regions:
            xa,xb,ya,yb=r['bounds'];ax.add_patch(Rectangle((xa,ya),xb-xa,yb-ya,facecolor='#e8f1f7' if r['sign']==1 else '#fbefe9',edgecolor='none'))
            xt,yt=r['test_point']
            # Keep sign text off the coordinate axes even when a region's
            # geometric midpoint is exactly zero. Labels are not test points.
            if abs(xt)<.55:xt=(3*xa+xb)/4 if xa<0 else (xa+3*xb)/4
            if abs(yt)<.55:yt=(3*ya+yb)/4 if ya<0 else (ya+3*yb)/4
            ax.text(xt,yt,r'$f(x,y)'+('>0$' if r['sign']==1 else '<0$'),ha='center',va='center',fontsize=11)
    axis_color='#777777' if role=='signs' else '#151515'
    ax.annotate('',xy=(hi_x,0),xytext=(lo_x,0),arrowprops={'arrowstyle':'->','color':axis_color,'lw':1})
    ax.annotate('',xy=(0,hi_y),xytext=(0,lo_y),arrowprops={'arrowstyle':'->','color':axis_color,'lw':1})
    ax.text(hi_x-.15,-.28,'$x$',ha='right',fontsize=12);ax.text(-.18,hi_y-.2,'$y$',va='top',ha='right',fontsize=12)
    ax.axvline(h,color='#2581c4',lw=1.4);ax.axhline(k,color='#2581c4',lw=1.4)
    ax.text(h,hi_y+.12,'$x='+str(h)+'$',ha='center',va='bottom',fontsize=11,clip_on=False)
    ax.text(hi_x+.12,k,'$y='+str(k)+'$',rotation=90,ha='left',va='center',fontsize=11,clip_on=False)
    fig.subplots_adjust(left=.04,right=.90,bottom=.04,top=.92);fig.canvas.draw()
    with tempfile.NamedTemporaryFile(suffix='.png',dir=path.parent,delete=False) as f:temp=Path(f.name)
    try:fig.savefig(temp,dpi=140,facecolor='white');os.replace(temp,path)
    finally:temp.unlink(missing_ok=True);plt.close(fig)
    sidecar={'renderer':'Matplotlib','matplotlib_version':matplotlib.__version__,'python':sys.version,'dependency_paths':provenance,'role':role,'parameters':{z:p[z] for z in ('h','k','ox','oy','px','py')},'geometry_fingerprint':data['geometry_fingerprint'],'limits':[lo_x,hi_x,lo_y,hi_y],'zero_lines':{'x':h,'y':k},'regions':regions,'dimensions':[728,728]}
    with tempfile.NamedTemporaryFile(mode='w',suffix='.json',dir=path.parent,delete=False) as f:json.dump(sidecar,f,indent=2);temp=Path(f.name)
    try:os.replace(temp,path.with_suffix('.json'))
    finally:temp.unlink(missing_ok=True)
