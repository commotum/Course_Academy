"""Private Matplotlib renderer: measured text placement, unique atomic writes."""
import sys,os,json,re,tempfile,hashlib,math
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087821-mpl'
try: import matplotlib
except ImportError:
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for pkg in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  paths=[p for p in (cache/pkg).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  sys.path.insert(0,str(sorted(paths)[-1]))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
VERSION='shift-plots-7'
def atomic(path,data):
 fd,tmp=tempfile.mkstemp(dir=path.parent,suffix='.tmp');os.close(fd)
 try: Path(tmp).write_text(data);os.replace(tmp,path)
 finally: Path(tmp).unlink(missing_ok=True)
def render(s):
 out=Path(s['path']);side=out.with_suffix('.json')
 if out.exists() and side.exists():
  old=json.loads(side.read_text())
  if old['spec']==s and old['version']==VERSION and old['png_sha256']==hashlib.sha256(out.read_bytes()).hexdigest(): return
 b,A,c=map(lambda v:float(Fraction(v)),(s['b'],s['A'],s['c']));direction=s['direction'];step=float(Fraction(s['grid']))
 xmin,xmax=-5,5;ymin,ymax=s['ylim']
 fig,ax=plt.subplots(figsize=(4.5,3.8),dpi=120);fig.subplots_adjust(left=.14,right=.96,bottom=.13,top=.93)
 ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax));ax.spines[['top','right']].set_visible(False);ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero')
 ax.set_xticks([-4,-2,2,4]);yt=np.arange(np.ceil(ymin/step)*step,ymax,step)
 ax.set_yticks([v for v in range(math.ceil(ymin),math.ceil(ymax)) if v!=0]);ax.set_yticks(yt,minor=True)
 if s['cue']=='grid':ax.grid(which='both',color='#d9dde1',lw=.55)
 else:ax.set_xticks([]);ax.set_yticks([]);ax.tick_params(which='both',left=False,bottom=False)
 # These guards preserve calibrated hard tick labels; feature labels below do
 # not use backgrounds and must genuinely clear all plotted objects.
 for tick in ax.get_xticklabels()+ax.get_yticklabels():tick.set_bbox({'facecolor':'white','edgecolor':'none','pad':.3})
 ax.annotate('',(xmax,0),(xmax-.2,0),arrowprops={'arrowstyle':'->','color':'black'});ax.annotate('',(0,ymax),(0,ymax-.15),arrowprops={'arrowstyle':'->','color':'black'})
 axis_labels=[ax.text(xmax-.05,-.04*(ymax-ymin),'x',ha='right'),ax.text(.18,ymax-.05,'y',va='top')]
 x=np.linspace(xmin,xmax,4000);y=A*b**(direction*x)+c
 ax.plot(x,y,color='#ffae18' if s.get('role')=='original' else '#2877b8',lw=1.8)
 curve_arrays=[np.column_stack((x,y))];markers=[];arrows=[];requests=[]
 if s.get('role')=='translation':
  old=b**x;ax.plot(x,old,color='#ffae18',lw=1.5);curve_arrays.append(np.column_stack((x,old)))
  ax.plot(0,1,'o',ms=4,color='#ffae18');markers.append((0,1))
  xp=s.get('arrow_x',-3.5);yp=b**xp;ax.annotate('',(xp,yp+c),(xp,yp),arrowprops={'arrowstyle':'->','color':'red','lw':1.1});arrows.append(((xp,yp),(xp,yp+c)))
  requests.append(('original_intercept','(0,1)',(0,1)))
 ax.axhline(c,color='black',ls=(0,(4,3)),lw=.8)
 if s['cue']=='labels':
  ax.plot(0,A+c,'o',ms=4,color=s.get('marker_color','#2877b8'));markers.append((0,A+c))
  # Place assessed point first, then original coordinate, then asymptote.
  requests.insert(0,('intercept',s['intercept_tex'],(0,A+c)))
  requests.append(('asymptote','y='+s['shift_tex'],(2.75,c)))
 fig.canvas.draw();renderer=fig.canvas.get_renderer();trans=ax.transData
 bounds=ax.bbox;zero=trans.transform((0,0));asy=trans.transform((0,c))[1]
 curves=[trans.transform(arr[(arr[:,1]>ymin-1)&(arr[:,1]<ymax+1)]) for arr in curve_arrays]
 marker_pixels=trans.transform(markers) if markers else np.empty((0,2))
 arrow_pixels=[trans.transform(np.linspace(a,z,300)) for a,z in arrows]
 occupied=[t.get_window_extent(renderer) for t in axis_labels+ax.get_xticklabels()+ax.get_yticklabels() if t.get_visible() and t.get_text()]
 def collision(box):
  # Measured text plus 4 px clearance from strokes and axes, 7 px from dots.
  left,bottom,right,top=box.extents;pad=4
  if left<bounds.x0+4 or right>bounds.x1-4 or bottom<bounds.y0+4 or top>bounds.y1-4:return 'bounds'
  if left-pad<=zero[0]<=right+pad or bottom-pad<=zero[1]<=top+pad:return 'axis'
  if bottom-pad<=asy<=top+pad:return 'asymptote'
  for pts in curves+arrow_pixels:
   if len(pts) and np.any((pts[:,0]>=left-pad)&(pts[:,0]<=right+pad)&(pts[:,1]>=bottom-pad)&(pts[:,1]<=top+pad)):return 'curve_or_arrow'
  if len(marker_pixels) and np.any((marker_pixels[:,0]>=left-7)&(marker_pixels[:,0]<=right+7)&(marker_pixels[:,1]>=bottom-7)&(marker_pixels[:,1]<=top+7)):return 'marker'
  for old in occupied:
   if left-5<old.x1 and right+5>old.x0 and bottom-5<old.y1 and top+5>old.y0:return 'label'
  return None
 layouts=[]
 for kind,content,anchor in requests:
  text=ax.text(0,0,'$'+content+'$',fontsize=10,ha='center',va='center',transform=None)
  # Matplotlib owns the final measured mathtext box. Candidate centres are in
  # display pixels, then converted to data coordinates to keep normal artists.
  text.set_transform(ax.transData);text.set_position(anchor);fig.canvas.draw()
  initial=text.get_window_extent(renderer);w,h=initial.width,initial.height
  origin=trans.transform(anchor);candidates=[]
  if kind!='asymptote':
   for gap in (12,24,40,60,85):
    for dy in (0,h/2+10,-h/2-10,h+22,-h-22,h+45,-h-45,h+70,-h-70):
     for sign in (-1,1):candidates.append((origin[0]+sign*(w/2+gap),origin[1]+dy))
  else:
   for dy in (h/2+10,-h/2-10,h/2+24,-h/2-24,h/2+42,-h/2-42,h/2+65,-h/2-65):
    for xp in (2.75,3.7,1.5,-2.75,-3.7,-1.5):candidates.append((trans.transform((xp,c))[0],origin[1]+dy))
  # Choose the nearest genuinely clear box, rather than accepting a far
  # vertical candidate before a nearer candidate in another quadrant.
  candidates.sort(key=lambda p:(p[0]-origin[0])**2+(p[1]-origin[1])**2)
  chosen=None
  for centre in candidates:
   text.set_position(trans.inverted().transform(centre));box=text.get_window_extent(renderer)
   if collision(box) is None:chosen=box;break
  if chosen is None:
   plt.close(fig);raise RuntimeError('No genuinely clear text placement: '+kind+' '+str(s))
  occupied.append(chosen)
  layouts.append({'kind':kind,'text':content,'anchor_data':list(anchor),'position_data':list(text.get_position()),'bbox_pixels':chosen.extents.tolist(),'clearance_pixels':4,'collision':None,'uses_background':False})
 fig.canvas.draw()
 samples=[{'x':v,'y':A*b**(direction*v)+c,'pixel':trans.transform((v,A*b**(direction*v)+c)).tolist()} for v in (-1,0,1)]
 fd,tmp=tempfile.mkstemp(dir=out.parent,suffix='.png');os.close(fd)
 try:fig.savefig(tmp);os.replace(tmp,out)
 finally:Path(tmp).unlink(missing_ok=True);plt.close(fig)
 atomic(side,json.dumps({'version':VERSION,'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'numpy':np.__version__,'spec':s,'samples':samples,'axes_bbox':ax.bbox.bounds,'label_layout':layouts,'png_sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2))
for s in json.loads(Path(sys.argv[1]).read_text()):render(s)

atomic(Path(__file__).resolve().parent/"renderer-runtime.json",json.dumps({"renderer_version":VERSION,"python":sys.version.split()[0],"matplotlib":matplotlib.__version__,"numpy":np.__version__},indent=2))
