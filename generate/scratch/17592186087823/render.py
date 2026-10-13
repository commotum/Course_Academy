"""Private Matplotlib renderer. Unique inputs; atomic PNG and JSON sidecars.
Fallback only reads cached Python3.10/Matplotlib packages; installs nothing.
"""
import os, sys, json, subprocess, re, tempfile, hashlib, math
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087823-mpl'
provenance={}
try:
 import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates: raise RuntimeError('Missing cached renderer: '+package)
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction

def number(x):
 q=Fraction(x)
 return str(q.numerator) if q.denominator==1 else str(float(q))
def atomic_bytes(path,data):
 with tempfile.NamedTemporaryFile(dir=path.parent,prefix='atomic-',delete=False) as f: f.write(data);temp=Path(f.name)
 os.replace(temp,path)

def render(item):
 spec=item['spec'];o=spec['curve'];a,b,c,h=(float(Fraction(o[n])) for n in ('a','b','c','h'));s=o['s'];mx,my=(float(Fraction(t)) for t in o['mark']);path=Path(item['path'])
 # Bounds tied to the asymptote, labelled point, origin and exponential rise.
 lo=min(0,c,my)-max(1,abs(a)*.8);hi=max(0,c,my)+max(1,abs(a)*1.8)
 xlo=min(-3,h-2);xhi=max(2.1,h+3,mx+3)
 # Match the source's ungridded black arrow axes and blue curves.
 fig,ax=plt.subplots(figsize=(4.8,4),dpi=100);ax.set_xlim(xlo,xhi);ax.set_ylim(lo,hi);ax.axis('off');fig.patch.set_facecolor('white')
 ax.annotate('',xy=(xhi,0),xytext=(xlo,0),arrowprops={'arrowstyle':'->','color':'black','lw':1.25})
 ax.annotate('',xy=(0,hi),xytext=(0,lo),arrowprops={'arrowstyle':'->','color':'black','lw':1.25})
 ax.text(xhi,0,'  $x$',va='center',fontsize=12);ax.text(0,hi,'$y$',ha='center',va='bottom',fontsize=12)
 if c!=0: ax.axhline(c,color='black',lw=1.2,ls=(0,(4,3)))
 xs=np.linspace(xlo,xhi,4000);ys=a*b**(s*(xs-h))+c
 ax.plot(xs,ys,color='#2875bb',lw=1.7,clip_on=True)
 ax.plot(mx,my,'o',color='#2875bb',markersize=4)
 fig.subplots_adjust(left=.04,right=.93,bottom=.04,top=.93);fig.canvas.draw()
 renderer=fig.canvas.get_renderer();trans=ax.transData;bounds=ax.bbox
 zero=trans.transform((0,0));asy=trans.transform((0,c))[1]
 curve=trans.transform(np.column_stack((xs,ys))[(ys>lo-1)&(ys<hi+1)])
 marker=trans.transform((mx,my))
 occupied=[t.get_window_extent(renderer) for t in ax.texts if t.get_text()]
 layouts=[]
 def collision(box):
  left,bottom,right,top=box.extents;pad=4
  if left<bounds.x0+4 or right>bounds.x1-4 or bottom<bounds.y0+4 or top>bounds.y1-4:return 'bounds'
  if left-pad<=zero[0]<=right+pad or bottom-pad<=zero[1]<=top+pad:return 'axis'
  if c!=0 and bottom-pad<=asy<=top+pad:return 'asymptote'
  if len(curve) and np.any((curve[:,0]>=left-pad)&(curve[:,0]<=right+pad)&(curve[:,1]>=bottom-pad)&(curve[:,1]<=top+pad)):return 'curve'
  if left-7<=marker[0]<=right+7 and bottom-7<=marker[1]<=top+7:return 'marker'
  if any(left-5<old.x1 and right+5>old.x0 and bottom-5<old.y1 and top+5>old.y0 for old in occupied):return 'label'
  return None
 requests=[('point','('+number(o['mark'][0])+','+number(o['mark'][1])+')',(mx,my))]
 if c!=0:requests.append(('asymptote','y='+number(o['c']),(xlo+.22*(xhi-xlo),c)))
 for kind,content,anchor in requests:
  text=ax.text(*anchor,'$'+content+'$',ha='center',va='center',fontsize=11)
  initial=text.get_window_extent(renderer);ww,hh=initial.width,initial.height;origin=trans.transform(anchor);candidates=[]
  if kind=='point':
   for gap in (12,24,40,60,85):
    for dy in (0,hh/2+10,-hh/2-10,hh+22,-hh-22,hh+45,-hh-45,hh+70,-hh-70):
     for side in (-1,1):candidates.append((origin[0]+side*(ww/2+gap),origin[1]+dy))
  else:
   for dy in (hh/2+10,-hh/2-10,hh/2+24,-hh/2-24,hh/2+42,-hh/2-42,hh/2+65,-hh/2-65):
    for ratio in (.22,.78,.12,.88,.38,.62):candidates.append((trans.transform((xlo+ratio*(xhi-xlo),c))[0],origin[1]+dy))
  candidates.sort(key=lambda v:(v[0]-origin[0])**2+(v[1]-origin[1])**2)
  chosen=None
  for centre in candidates:
   text.set_position(trans.inverted().transform(centre));box=text.get_window_extent(renderer)
   if collision(box) is None:chosen=box;break
  if chosen is None:plt.close(fig);raise RuntimeError('No feature-clear label placement: '+kind+' '+str(spec))
  occupied.append(chosen)
  layouts.append({'kind':kind,'text':content,'anchor_data':list(anchor),'position_data':list(text.get_position()),'bbox_pixels':chosen.extents.tolist(),'clearance_pixels':4,'collision':None,'uses_background':False})
 fig.canvas.draw();label_boxes=[list(t.get_window_extent(renderer).bounds) for t in ax.texts if t.get_text()]
 for xx,yy,ww,hh in label_boxes:
  if not (0<=xx and 0<=yy and xx+ww<=480 and yy+hh<=400):raise RuntimeError('Clipped plot label')
 transform=[list(ax.transData.transform((xx,yy))) for xx,yy in ((xlo,lo),(xhi,hi),(mx,my),(0,c))]
 with tempfile.NamedTemporaryFile(dir=path.parent,suffix='.png',prefix='atomic-',delete=False) as f: tmp=Path(f.name)
 fig.savefig(tmp,dpi=100,facecolor='white');plt.close(fig);data=tmp.read_bytes();tmp.unlink();atomic_bytes(path,data)
 side={'spec':spec,'python_version':sys.version.split()[0],'matplotlib_version':matplotlib.__version__,'numpy_version':np.__version__,'dependencies':provenance,'bounds':[xlo,xhi,lo,hi],'pixel_transform':transform,'label_boxes':label_boxes,'label_layout':layouts,'axes_bbox':list(bounds.extents),'axis_origin_pixels':list(zero),'marker_pixels':list(marker),'size':[480,400],'png_sha256':hashlib.sha256(data).hexdigest(),'curve_samples':[[float(x),float(y)] for x,y in zip(xs[::100],ys[::100])]}
 atomic_bytes(path.with_suffix('.json'),(json.dumps(side,indent=2)+'\n').encode())
for item in json.loads(Path(sys.argv[1]).read_text()): render(item)
