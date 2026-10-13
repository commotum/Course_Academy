"""Matplotlib renderer; read-only cached Python 3.10 fallback; atomic assets."""
import os,sys,json,re,hashlib,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186152189-mpl'
deps={}
try:import matplotlib
except ImportError:
 if sys.version_info[:2]!=(3,10):
  import subprocess
  subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',__file__,*sys.argv[1:]],check=True);sys.exit()
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  p=sorted(candidates)[-1];sys.path.insert(0,str(p));deps[package]=str(p)
 import matplotlib
matplotlib.use('Agg');import matplotlib.pyplot as plt;import numpy as np
inp=json.load(open(sys.argv[1]));p=inp['parameters'];a,b,h,k=[p[x] for x in ('a','b','h','k')];out=Path(inp['target']);out.parent.mkdir(exist_ok=True)
fig,ax=plt.subplots(figsize=(6,5),dpi=120);pad=max(a,b)*.35+1
xmin,xmax=min(0,h-a)-pad,max(0,h+a)+pad;ymin,ymax=min(0,k-b)-pad,max(0,k+b)+pad
ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax),aspect='equal');ax.spines[['right','top']].set_visible(False);ax.spines['left'].set_position('zero');ax.spines['bottom'].set_position('zero')
step=1 if max(xmax-xmin,ymax-ymin)<18 else 2
ax.set_xticks(np.arange(np.ceil(xmin/step)*step,xmax,step));ax.set_yticks(np.arange(np.ceil(ymin/step)*step,ymax,step));ax.tick_params(labelsize=9,pad=4)
for tick in ax.get_xticklabels()+ax.get_yticklabels():
 if tick.get_text()=='0':tick.set_visible(False)
t=np.linspace(0,2*np.pi,801);ax.plot(h+a*np.cos(t),k+b*np.sin(t),color='#287bbc',lw=1.7);ax.plot([h-a,h+a],[k,k],ls='--',color='#999',lw=.8);ax.plot([h,h],[k-b,k+b],ls='--',color='#999',lw=.8)
ax.text(xmax,0,'x',ha='left',va='center');ax.text(0,ymax,'y',ha='center',va='bottom')
label=None
if inp['oriented']:
 ax.plot(h+a,k,'ko',ms=4);label=ax.annotate(f'A({h+a},{k})',(h+a,k),xytext=(12,10),textcoords='offset points',fontsize=11)
 t0=.65;t1=.80;ax.annotate('',(h+a*np.cos(t1),k+b*np.sin(t1)),(h+a*np.cos(t0),k+b*np.sin(t0)),arrowprops=dict(arrowstyle='->',color='#287bbc',lw=1.5))
fig.canvas.draw();clearance=None;tick_clearance=None
if label:
 pt=ax.transData.transform((h+a,k));ticks=[x.get_window_extent() for x in ax.get_xticklabels()+ax.get_yticklabels() if x.get_visible()]
 def gap(box,other):
  dx=max(other.x0-box.x1,box.x0-other.x1,0);dy=max(other.y0-box.y1,box.y0-other.y1,0);return float(np.hypot(dx,dy))
 for offset in ((12,10),(12,-22),(12,30),(12,-42),(30,10),(30,-22),(80,10)):
  label.set_position(offset);fig.canvas.draw();box=label.get_window_extent();tick_clearance=min(gap(box,x) for x in ticks);clearance=float(box.x0-pt[0])
  if tick_clearance>=4 and clearance>=11:break
 else:raise RuntimeError('Cannot place endpoint label clear of tick labels')
 assert clearance>=11 and tick_clearance>=4
tight=fig.get_tightbbox(fig.canvas.get_renderer());origin=ax.transData.transform((0,0));one=ax.transData.transform((1,1));origin_pixels=[float(origin[0]-(tight.x0-.1)*fig.dpi),float((tight.y1+.1)*fig.dpi-origin[1])];scale_pixels=[float(one[0]-origin[0]),float(one[1]-origin[1])]
fd,tmp=tempfile.mkstemp(suffix='.png',dir=out.parent);os.close(fd);fig.savefig(tmp,bbox_inches='tight',facecolor='white');plt.close(fig);os.replace(tmp,out)
meta={'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'dependency_paths':deps,'parameters':p,'oriented':inp['oriented'],'bounds':[xmin,xmax,ymin,ymax],'tick_increment':step,'label_clearance_pixels':clearance,'tick_label_clearance_pixels':tick_clearance,'equal_scale':True,'origin_pixels':origin_pixels,'scale_pixels':scale_pixels,'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'png_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
fd,tmp=tempfile.mkstemp(suffix='.json',dir=out.parent);os.close(fd);Path(tmp).write_text(json.dumps(meta,indent=2)+'\n');os.replace(tmp,out.with_suffix('.json'))
