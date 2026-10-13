"""Private Matplotlib renderer: unique caller input, versioned atomic PNG+sidecar."""
import os,sys,json,re,subprocess,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp87824-mpl'
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
from PIL import Image
import hashlib,math
p=json.load(open(sys.argv[1]));b,k,c,step=[float(Fraction(p[x])) for x in ('b','k','c','step')];u=k+c
# Hard always uses a small calibrated grid; easy/moderate retain source labels.
xmin=-4;xmax=math.log(1+5/k,b);ymin=min(-1,c-1);ymax=max(2,u+2)
fig,ax=plt.subplots(figsize=(5.4,4.2),dpi=140);ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax));ax.axis('off');fig.patch.set_facecolor('white')
ax.annotate('',(xmax,0),(xmin,0),arrowprops={'arrowstyle':'->','color':'black','lw':1.4});ax.annotate('',(0,ymax),(0,ymin),arrowprops={'arrowstyle':'->','color':'black','lw':1.4})
xx=np.linspace(xmin,xmax,1500);yy=k*np.power(b,xx)+c;mask=yy<ymax-.08
ax.plot(xx[mask],yy[mask],color='#2875b9',lw=1.8);ax.plot(0,u,'o',color='#2875b9',markersize=5)
ax.axhline(c,color='black',linestyle=(0,(4,3)),lw=1)
labels=[];ticks=[];requests=[]
def ft(v):
 f=Fraction(v);return str(f.numerator) if f.denominator==1 else ('-' if f<0 else '')+r'\frac{'+str(abs(f.numerator))+'}{'+str(f.denominator)+'}'
if p['level']!='hard':
 ct=ft(p['c']);ut=ft(str(Fraction(p['c'])+Fraction(p['k'])))
 if (Fraction(p['c'])+Fraction(p['k'])).denominator in (2,4):ut=str(float(Fraction(p['c'])+Fraction(p['k'])))
 requests=[('intercept','(0,'+ut+')',(0,u)),('asymptote','y='+ct,(xmax-.2,c))]
else:
 for i in range(math.ceil(ymin/step),math.floor(ymax/step)+1):
  y=i*step;ax.axhline(y,color='#dddddd',lw=.55,zorder=-2)
  if y==0:continue
  ax.plot([-.04,.04],[y,y],color='black',lw=.8)
  ticks.append({'index':i,'value':str(Fraction(p['step'])*i),'labeled':False})
fig.subplots_adjust(left=.07,right=.97,bottom=.07,top=.97);fig.canvas.draw();tr=ax.transData;renderer=fig.canvas.get_renderer();bounds=ax.bbox
zero=tr.transform((0,0));asypixel=tr.transform((0,c))[1];marker=tr.transform((0,u));curve=tr.transform(np.column_stack([xx[mask],yy[mask]]))
occupied=[];layouts=[]
def collision(box):
 left,bottom,right,top=box.extents;pad=4
 if left<bounds.x0+4 or right>bounds.x1-4 or bottom<bounds.y0+4 or top>bounds.y1-4:return 'bounds'
 if left-pad<=zero[0]<=right+pad or bottom-pad<=zero[1]<=top+pad:return 'axis'
 if bottom-pad<=asypixel<=top+pad:return 'asymptote'
 if np.any((curve[:,0]>=left-8)&(curve[:,0]<=right+8)&(curve[:,1]>=bottom-8)&(curve[:,1]<=top+8)):return 'curve'
 if left-10<=marker[0]<=right+10 and bottom-10<=marker[1]<=top+10:return 'marker'
 for old in occupied:
  if left-5<old.x1 and right+5>old.x0 and bottom-5<old.y1 and top+5>old.y0:return 'label'
 return None
# Axis letters have measured positions inside the plot, clear of their strokes.
for content,anchor in [('x',(bounds.x1,zero[1])),('y',(zero[0],bounds.y1))]:
 text=ax.text(*tr.inverted().transform(anchor),'$'+content+'$',ha='center',va='center',fontsize=10)
 candidates=[(bounds.x1-dx,zero[1]+dy) for dx in (12,24,40) for dy in (18,-18,34,-34)] if content=='x' else [(zero[0]+dx,bounds.y1-dy) for dx in (18,-18,34,-34) for dy in (16,30,45)]
 candidates.sort(key=lambda v:(v[0]-anchor[0])**2+(v[1]-anchor[1])**2)
 chosen=None
 for centre in candidates:
  text.set_position(tr.inverted().transform(centre));box=text.get_window_extent(renderer)
  if collision(box) is None:chosen=box;break
 if chosen is None:raise RuntimeError('No clear axis-letter position')
 occupied.append(chosen)
 layouts.append({'kind':'axis_name','text':content,'position_data':list(text.get_position()),'bbox_pixels':chosen.extents.tolist(),'uses_background':False,'collision':None})
if p['level']=='hard':
 # Tick text stays on the true grid coordinate. Measure fractional text first
 # and choose a regular naming stride with enough vertical pixel space.
 probe=ax.text(0,0,r'$-\frac{11}{4}$',fontsize=9,ha='right',va='center');fig.canvas.draw();maxheight=probe.get_window_extent(renderer).height;probe.remove()
 pixels_per_step=abs(tr.transform((0,step))[1]-zero[1]);stride=2
 while stride*pixels_per_step<maxheight+10:stride*=2
 for t in ticks:
  value=float(Fraction(t['value']));origin=tr.transform((0,value));t['pixel_y']=float(origin[1]);t['regular_named_stride']=stride
  if t['index']%stride or abs(value-c)<1e-8 or abs(value-u)<1e-8:continue
  content=ft(t['value']);text=ax.text(0,value,'$'+content+'$',fontsize=9,ha='right',va='center');text.set_position(tr.inverted().transform((zero[0]-14,origin[1])))
  box=text.get_window_extent(renderer);why=collision(box)
  if why:text.remove();t['suppressed_collision']=why;continue
  t['labeled']=True;t['bbox_pixels']=box.extents.tolist();t['text_position_data']=list(text.get_position());occupied.append(box);labels.append(t['value'])
  layouts.append({'kind':'tick','text':content,'value':t['value'],'anchor_data':[0,value],'position_data':list(text.get_position()),'bbox_pixels':box.extents.tolist(),'clearance_pixels':4,'collision':None,'uses_background':False})
 if sum(t['labeled'] for t in ticks)<2:raise RuntimeError('Insufficient calibrated named ticks')
else:
 for kind,content,anchor in requests:
  text=ax.text(*anchor,'$'+content+'$',fontsize=12,ha='center',va='center');fig.canvas.draw();box=text.get_window_extent(renderer);w0,h0=box.width,box.height;origin=tr.transform(anchor);candidates=[]
  if kind=='intercept':
   for gap in (12,24,40,60,85):
    for dy in (0,h0/2+10,-h0/2-10,h0+22,-h0-22,h0+45,-h0-45,h0+70,-h0-70):
     for sign in (-1,1):candidates.append((origin[0]+sign*(w0/2+gap),origin[1]+dy))
  else:
   for dy in (h0/2+10,-h0/2-10,h0/2+24,-h0/2-24,h0/2+42,-h0/2-42,h0/2+65,-h0/2-65):
    for fraction in (.8,.65,.45,.25,.12):candidates.append((bounds.x0+fraction*bounds.width,origin[1]+dy))
  candidates.sort(key=lambda point:(point[0]-origin[0])**2+(point[1]-origin[1])**2)
  chosen=None
  for centre in candidates:
   text.set_position(tr.inverted().transform(centre));box=text.get_window_extent(renderer)
   if collision(box) is None:chosen=box;break
  if chosen is None:raise RuntimeError('No genuinely clear feature-label placement: '+kind+' '+str(p))
  occupied.append(chosen);labels.append(content)
  layouts.append({'kind':kind,'text':content,'anchor_data':list(anchor),'position_data':list(text.get_position()),'bbox_pixels':chosen.extents.tolist(),'clearance_pixels':4,'collision':None,'uses_background':False,'selection':'nearest clear measured candidate'})
fig.canvas.draw()
geometry={'origin':tr.transform((0,0)).tolist(),'intercept':tr.transform((0,u)).tolist(),'asymptote':tr.transform((0,c)).tolist(),'axes_box':list(ax.bbox.bounds),'bounds':[xmin,xmax,ymin,ymax],'curve_pixels':curve.tolist()}
for t in ticks:t['pixel_y']=float(tr.transform((0,float(Fraction(t['value']))))[1])
output=Path(p['output']);fd,tmp=tempfile.mkstemp(prefix='atomic-',suffix='.png',dir=output.parent);os.close(fd);fig.savefig(tmp,dpi=140);plt.close(fig);os.replace(tmp,output)
def atomic(path,obj):
 fd,tmp=tempfile.mkstemp(prefix='atomic-',suffix='.json',dir=path.parent)
 with os.fdopen(fd,'w') as f:json.dump(obj,f,indent=2)
 os.replace(tmp,path)
side={'parameters':{x:y for x,y in p.items() if x!='output'},'renderer':'Matplotlib','python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'numpy':np.__version__,'dependency_paths':paths,'geometry':geometry,'ticks':ticks,'labels':labels,'label_layout':layouts,'label_clearance_pixels':4,'tick_labels_detached':False,'axes_arrows':['positive_x','positive_y'],'curve_arrows':[]}
atomic(output.with_suffix('.json'),side)
# Independent raster readback: actual blue pixels at x=0 recover the marked
# intercept; left-side dashed black pixels recover c; curve sample geometry is
# checked against raster colors with stroke-width allowance. Text is visually
# reviewed separately, not claimed to be machine-OCRed.
a=np.asarray(Image.open(output).convert('RGB')).astype(int);h,w=a.shape[:2];xp=int(round(geometry['intercept'][0]));yp=h-geometry['intercept'][1];cp=h-geometry['asymptote'][1]
blue=(a[:,:,2]>a[:,:,0]+45)&(a[:,:,1]>a[:,:,0]+25)&(a[:,:,2]>90)
ys,xs=np.where(blue[:,max(0,xp-2):xp+3]);near=[float(y) for y in ys if abs(y-yp)<=7]
if not near:raise RuntimeError('PNG intercept marker absent')
left=int(geometry['axes_box'][0])+5;right=xp-45;dark=np.max(a[:,left:right,:],axis=2)<110;rows=np.sum(dark,axis=1);found=min(range(max(0,round(cp)-5),min(h,round(cp)+6)),key=lambda row:-rows[row])
if abs(found-cp)>3 or rows[found]<.25*(right-left):raise RuntimeError('PNG dashed asymptote absent')
checked=0
for px,py in geometry['curve_pixels'][::100]:
 px=int(round(px));py=int(round(h-py))
 if 4<=px<w-4 and 4<=py<h-4:
  if not blue[py-4:py+5,px-4:px+5].any():raise RuntimeError('PNG curve mismatch')
  checked+=1
qa={'pass':True,'actual_png_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'png_dimensions':[w,h],'intercept_blue_row_error':min(abs(y-yp) for y in near),'dashed_asymptote_row_error':abs(found-cp),'curve_samples_checked':checked,'label_validation':'Matplotlib actual artist strings captured; human full-resolution review, no OCR claim'}
atomic(output.with_suffix('.qa.json'),qa)
