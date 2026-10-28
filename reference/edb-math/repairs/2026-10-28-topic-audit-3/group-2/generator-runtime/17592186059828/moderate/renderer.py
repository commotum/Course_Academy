"""Only deterministic Matplotlib plotting. Cached renderer libraries are read-only."""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186059828-mpl'
provenance={}
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def atomic_json(path,data):
    path=Path(path)
    with tempfile.NamedTemporaryFile('w',dir=path.parent,delete=False,suffix='.json') as f:json.dump(data,f,indent=2);tmp=Path(f.name)
    os.replace(tmp,path)

def readback(path,fit=None):
    # Detect red segment and two circular markers from actual PNG pixels.
    im=Image.open(path).convert('RGBA');background=Image.new('RGBA',im.size,'white');background.alpha_composite(im);arr=np.array(background.convert('RGB'))
    red=(arr[:,:,0]>180)&(arr[:,:,1]<100)&(arr[:,:,2]<100)
    rows=np.sum(red,axis=1)
    markerrows=np.where(rows>rows.max()*.65)[0];cy=int(round(float(np.median(markerrows))))
    residual=red.copy()
    half=2 if arr.shape[0]<60 else 4
    residual[max(0,cy-half):cy+half+1,:]=False
    xs=np.where(np.sum(residual,axis=0)>0)[0]
    groups=[]
    for x in xs:
        if not groups or x>groups[-1][-1]+(8 if arr.shape[0]<60 else 22):groups.append([int(x)])
        else:groups[-1].append(int(x))
    if len(groups)!=2:raise AssertionError(('Endpoint groups',groups))
    centers=[(run[0]+run[-1])/2 for run in groups]
    closed=[bool(red[cy,int(round(x))]) for x in centers]
    if fit is None:
        # Read tick columns from the black vertical marks above the axis.
        black=np.max(arr,axis=2)<100
        # Image drawing has fixed margins; derive tick positions without using answer metadata.
        candidates=[]
        for x in range(arr.shape[1]):
            ys=np.where(black[:,x])[0]
            if sum((ys>=cy-6)&(ys<=cy-2))>=3:candidates.append(x)
        runs=[]
        for x in candidates:
            if not runs or x>runs[-1][-1]+1:runs.append([x])
            else:runs[-1].append(x)
        ticks=[(r[0]+r[-1])/2 for r in runs]
    else:ticks=fit['tick_pixels']
    output={'width':arr.shape[1],'height':arr.shape[0],'endpoint_pixels':centers,'center_y':cy,'closed':closed,'tick_pixels':ticks}
    if fit:
        scale=(fit['anchor_pixels'][1]-fit['anchor_pixels'][0])/(fit['anchor_values'][1]-fit['anchor_values'][0]);origin=fit['anchor_pixels'][0]-fit['anchor_values'][0]*scale
        output.update({'pixels_per_unit':scale,'origin_pixel':origin,'endpoint_values':[(x-origin)/scale for x in centers]})
    return output

if sys.argv[1]=='--readback':
    config=json.loads(Path(sys.argv[2]).read_text());atomic_json(config['output'],[{'path':c['path'],'measurement':readback(c['path'],c.get('fit'))} for c in config['cases']]);sys.exit(0)
data=json.loads(Path(sys.argv[1]).read_text());g=data['geometry'];png=Path(data['png']);side=Path(data['sidecar'])
fig=plt.figure(figsize=(8,1.45),dpi=140);ax=fig.add_axes([.05,.2,.90,.65]);ax.set_xlim(g['lo']-.15*g['tick_step'],g['hi']+.15*g['tick_step']);ax.set_ylim(-.4,.3);ax.axis('off')
ax.plot([g['lo'],g['hi']],[0,0],color='black',lw=1.4)
count=round((g['hi']-g['lo'])/g['tick_step'])
for i in range(count+1):
    x=g['lo']+i*g['tick_step'];ax.plot([x,x],[-.035,.035],color='black',lw=1.2)
    if abs(x/g['label_step']-round(x/g['label_step']))<1e-8:ax.text(x,-.095,str(int(x)) if float(x).is_integer() else str(x),ha='center',va='top',fontsize=13)
ax.plot([g['left'],g['right']],[0,0],color='#ef2020',lw=3,zorder=3)
for x,c in ((g['left'],g['left_closed']),(g['right'],g['right_closed'])):ax.plot(x,0,'o',markersize=9,markeredgewidth=1.7,markeredgecolor='#ef2020',markerfacecolor='#ef2020' if c else 'white',zorder=5)
fig.canvas.draw()
# Record fitted axes only for independent readback; semantic coords are never used as readback answers.
p0=ax.transData.transform((0,0));p1=ax.transData.transform((1,0));width,height=fig.canvas.get_width_height()
with tempfile.NamedTemporaryFile(dir=png.parent,suffix='.png',delete=False) as f:tmp=Path(f.name)
fig.savefig(tmp,dpi=140);plt.close(fig);os.replace(tmp,png)
atomic_json(side,{'renderer':'Matplotlib','python':sys.version,'matplotlib':matplotlib.__version__,'dependencies':provenance,'geometry':g,'axis_pixel_fit':{'origin_pixel':float(p0[0]),'pixels_per_unit':float(p1[0]-p0[0]),'axis_y':float(height-p0[1])},'raster_readback':readback(png)})
