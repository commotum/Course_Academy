"""Private Matplotlib renderer: unique caller input, versioned atomic PNG+sidecar."""
import os,sys,json,re,subprocess,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp87822-mpl'
paths={}
try:import matplotlib
except ImportError:
 runtime='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
 if sys.version_info[:2]!=(3,10):
  subprocess.run([runtime,__file__,sys.argv[1]],check=True);sys.exit()
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));paths[package]=str(path)
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction
p=json.load(open(sys.argv[1]));b=float(Fraction(p['b']));c=float(Fraction(p['c']));step=float(Fraction(p['step']))
xmin=float(p['xmin']);xmax=float(Fraction(p['xmax'])) if '/' in p['xmax'] else float(p['xmax'])
ymin=float(Fraction(p['ymin']));ymax=float(Fraction(p['ymax']))
fig,ax=plt.subplots(figsize=(5.4,4.2),dpi=140);fig.patch.set_facecolor('white')
fig.subplots_adjust(left=.07,right=.97,bottom=.07,top=.97)
ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax));ax.axis('off')
ax.annotate('',(xmax,0),(xmin,0),arrowprops={'arrowstyle':'->','color':'black','lw':1.4})
ax.annotate('',(0,ymax),(0,ymin),arrowprops={'arrowstyle':'->','color':'black','lw':1.4})
ax.text(xmax,.15,'$x$',ha='right');ax.text(.10,ymax-.1,'$y$',va='top')
xx=np.linspace(xmin,xmax,1200);curve_y=np.power(b,xx)+c;valid=curve_y<ymax-.15
ax.plot(xx[valid],curve_y[valid],color='#2b75b8',lw=1.8)
ax.axhline(c,color='black',linestyle=(0,(4,3)),lw=1)
labels=[];ticks=[];feature_boxes=[]
if p['level']!='hard':
 f=Fraction(p['c']);ct=str(f.numerator) if f.denominator==1 else r'\frac{'+str(abs(f.numerator))+'}{'+str(f.denominator)+'}'
 if f<0 and f.denominator!=1:ct='-'+ct
 # Measure actual text at final axes layout. Near-zero fractional labels must
 # clear the x-axis rather than use a fixed data offset or hide it with a box.
 label=ax.text(xmax-.15,c,'$y='+ct+'$',ha='right',va='top',fontsize=12)
 transform=ax.transData;origin=transform.transform((0,0));asym=transform.transform((0,c))[1]
 curve_pixels=transform.transform(np.column_stack([xx[valid],curve_y[valid]]))
 placed=False
 for gap in (12,20,28,36,48,64,80,96):
  for direction in (-1,1):
   label.set_verticalalignment('top' if direction<0 else 'bottom')
   label.set_position(transform.inverted().transform((transform.transform((xmax-.15,c))[0],asym+direction*gap)))
   fig.canvas.draw();box=label.get_window_extent(fig.canvas.get_renderer());bounds=(box.x0,box.y0,box.x1,box.y1)
   if box.y0<ax.bbox.y0+4 or box.y1>ax.bbox.y1-4:continue
   if box.y0-4<=origin[1]<=box.y1+4 or box.y0-4<=asym<=box.y1+4:continue
   if box.x0-4<=origin[0]<=box.x1+4:continue
   if np.any((curve_pixels[:,0]>=box.x0-4)&(curve_pixels[:,0]<=box.x1+4)&(curve_pixels[:,1]>=box.y0-4)&(curve_pixels[:,1]<=box.y1+4)):continue
   others=[t.get_window_extent(fig.canvas.get_renderer()) for t in ax.texts if t is not label]
   if any(box.x0-4<t.x1 and box.x1+4>t.x0 and box.y0-4<t.y1 and box.y1+4>t.y0 for t in others):continue
   feature_boxes.append({'text':'y='+p['c'],'bounds':list(bounds),'axis_clearance_px':4,'asymptote_clearance_px':4,'curve_clearance_px':4});placed=True;break
  if placed:break
 if not placed:raise ValueError('No clear asymptote label placement')
 labels.append('y='+p['c'])
else:
 # Actual fraction labels, alternating positions. c is an odd tick for half-grid
 # cases and may be even for others; suppress its label universally.
 for k in range(int(np.ceil(ymin/step))+1,int(np.floor(ymax/step))):
  yy=k*step
  if abs(yy)<1e-9:continue
  ax.plot([-.06,.06],[yy,yy],color='black',lw=1)
  ax.plot([xmin,xmax],[yy,yy],color='#dddddd',lw=.6,zorder=-2)
  ticks.append({'k':k,'value':str(Fraction(p['step'])*k),'pixel_y':float(ax.transData.transform((0,yy))[1])})
  if k%2==0 and abs(yy-c)>1e-8:
   f=Fraction(p['step'])*k;t=str(f.numerator) if f.denominator==1 else ('-' if f<0 else '')+r'\frac{'+str(abs(f.numerator))+'}{'+str(f.denominator)+'}'
   ax.text(-.12,yy,'$'+t+'$',ha='right',va='center',fontsize=10);labels.append(str(f))
fig.subplots_adjust(left=.07,right=.97,bottom=.07,top=.97);fig.canvas.draw()
trans=ax.transData
for t in ticks:t['pixel_y']=float(trans.transform((0,float(Fraction(t['value']))))[1])
geometry={'asymptote_pixel_y':float(trans.transform((0,c))[1]),'origin_pixel':trans.transform((0,0)).tolist(),'intercept_pixel':trans.transform((0,c+1)).tolist(),'curve_pixels':trans.transform(np.column_stack([xx[valid],curve_y[valid]])).tolist(),'bounds':[xmin,xmax,ymin,ymax]}
output=Path(p['output']);fd,tmp=tempfile.mkstemp(prefix='atomic-',suffix='.png',dir=output.parent);os.close(fd)
fig.savefig(tmp,dpi=140);plt.close(fig);os.replace(tmp,output)
side=dict(parameters={k:v for k,v in p.items() if k!='output'},renderer='Matplotlib',python=sys.version.split()[0],matplotlib=matplotlib.__version__,numpy=np.__version__,dependency_paths=paths,geometry=geometry,ticks=ticks,labels=labels,width=756,height=588,axes_arrows=['positive_x','positive_y'],curve_arrows=[],intercept_marked=False,feature_label_boxes=feature_boxes)
fd,tmp=tempfile.mkstemp(prefix='atomic-',suffix='.json',dir=output.parent)
with os.fdopen(fd,'w') as f:json.dump(side,f,indent=2)
os.replace(tmp,output.with_suffix('.json'))
