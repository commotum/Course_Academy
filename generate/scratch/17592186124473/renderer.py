"""Private Matplotlib renderer; read-only cached dependencies; atomic outputs."""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186124473-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),__file__,*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates:raise RuntimeError('Missing cached '+package)
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path)
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction as F
req=json.loads(Path(sys.argv[1]).read_text());data=req['data'];out=Path(req['output'])
pieces=[[float(F(x)) if i<4 else bool(x) for i,x in enumerate(p)] for p in data['pieces']]
fig,ax=plt.subplots(figsize=(6,4.8),dpi=140)
xs=[p[i] for p in pieces for i in (0,2)];ys=[p[i] for p in pieces for i in (1,3)]
xmin,xmax=min(min(xs)-.8,-.8),max(max(xs)+.8,.8);ymin,ymax=min(min(ys)-.8,-.8),max(max(ys)+.8,.8)
ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax)
ax.set_xticks(range(int(np.floor(xmin))+1,int(np.ceil(xmax))))
ax.set_yticks(range(int(np.floor(ymin))+1,int(np.ceil(ymax))))
ax.grid(color='#d1d1d1',linewidth=.65);ax.set_axisbelow(True)
# Labels live outside the plotting rectangle; their actual text boxes are tested
# against axes, curve polylines and marker centres. No feature masks.
for side in ('left','bottom','right','top'):ax.spines[side].set_visible(False)
axis_h=ax.axhline(0,color='black',linewidth=1);axis_v=ax.axvline(0,color='black',linewidth=1)
ax.set_xlabel('$x$',fontsize=12);ax.set_ylabel('$y$',fontsize=12,rotation=0,labelpad=12)
curves=[];marks=[]
for a,b,c,d,lc,rc in pieces:
 line,=ax.plot([a,c],[b,d],color='#2674b7',linewidth=2,zorder=3);curves.append(line)
 for x,y,closed in ((a,b,lc),(c,d,rc)):
  # Avoid double drawing joins; different output values at a jump keep marks.
  key=(x,y)
  if key in [k for k,_ in marks]:continue
  mark,=ax.plot(x,y,'o',markersize=6,markerfacecolor='#2674b7' if closed else 'white',markeredgecolor='#2674b7',markeredgewidth=1.3,zorder=4)
  marks.append((key,mark))
fig.tight_layout(pad=1.7);fig.canvas.draw();renderer=fig.canvas.get_renderer()
labels=[t for t in ax.get_xticklabels()+ax.get_yticklabels()+[ax.xaxis.label,ax.yaxis.label] if t.get_visible() and t.get_text()]
boxes=[t.get_window_extent(renderer) for t in labels]
clearance=[]
for t,box in zip(labels,boxes):
 points=[]
 for curve in curves+[axis_h,axis_v]:
  path=curve.get_path().interpolated(120);points.extend(curve.get_transform().transform(path.vertices))
 for _,mark in marks:points.extend(mark.get_transform().transform(mark.get_xydata()))
 # Euclidean distance to actual bbox, with marker stroke/radius allowance.
 distances=[np.hypot(max(box.x0-x,0,x-box.x1),max(box.y0-y,0,y-box.y1)) for x,y in points]
 clearance.append({'text':t.get_text(),'bbox':[box.x0,box.y0,box.x1,box.y1],'feature_clearance_pixels':float(min(distances))})
 if min(distances)<4:raise ValueError('Plot label intersects graph '+t.get_text())
for i,b in enumerate(boxes):
 for c in boxes[i+1:]:
  if b.overlaps(c):raise ValueError('Text boxes overlap')
side={'axes_bbox_pixels':list(ax.get_window_extent(renderer).bounds),'data':data,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'dependency_paths':provenance,'label_clearances':clearance,'figure_pixels':list(fig.canvas.get_width_height()),'limits':[xmin,xmax,ymin,ymax],'minimum_feature_clearance_pixels':min(x['feature_clearance_pixels'] for x in clearance)}
fd,tmp=tempfile.mkstemp(prefix='png-',suffix='.png',dir=out.parent);os.close(fd)
fig.savefig(tmp,dpi=140)
# Read the actual saved PNG and verify the visible curve/endpoint pixels in its
# own data-to-pixel transform. This is separate from cached mathematical data.
rgba=plt.imread(tmp);height=rgba.shape[0];checks=[]
for (x,y),mark in marks:
 px,py=ax.transData.transform((x,y));ix,iy=round(px),height-1-round(py)
 pixel=rgba[iy,ix,:3];closed=mark.get_markerfacecolor()!='white'
 blue=bool(pixel[2]>pixel[0]+.2 and pixel[1]>pixel[0]+.1)
 white=bool(min(pixel)>.9)
 if (closed and not blue) or (not closed and not white):raise ValueError('Rendered endpoint mismatch')
 checks.append({'coordinate':[x,y],'closed':closed,'center_rgb':pixel.tolist()})
side['raster_endpoint_checks']=checks
for a,b,c,d,lc,rc in pieces:
 px,py=ax.transData.transform(((a+c)/2,(b+d)/2));ix,iy=round(px),height-1-round(py)
 patch=rgba[max(0,iy-2):iy+3,max(0,ix-2):ix+3,:3]
 if not np.any((patch[:,:,2]>patch[:,:,0]+.2)&(patch[:,:,1]>patch[:,:,0]+.1)):raise ValueError('PNG curve segment absent')
side['raster_curve_midpoints_verified']=len(pieces)
plt.close(fig);os.replace(tmp,out)
fd,tmp=tempfile.mkstemp(prefix='side-',suffix='.json',dir=out.parent);os.close(fd);Path(tmp).write_text(json.dumps(side,indent=2));os.replace(tmp,out.with_suffix('.json'))
