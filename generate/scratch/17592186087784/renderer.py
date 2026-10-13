"""Matplotlib only; read-only cached Python 3.10 dependencies, input instance stdin."""
import json,os,re,sys,subprocess
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087784-mpl'
raw=sys.stdin.read();provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__))],input=raw,text=True,check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction
D=json.loads(raw);p=D['parameters'];r,h,k=p['r'],p['h'],p['k'];a,b=float(Fraction(p['start']))*np.pi,float(Fraction(p['end']))*np.pi;out=Path(D['output_dir'])
def xy(t):return h+r*np.cos(t),k+r*np.sin(t)
def theta_text(t):
 c=Fraction(t/np.pi).limit_denominator(24);n,d=c.numerator,c.denominator
 if n==0:return '0'
 top=('' if n==1 else str(n))+r'\pi'
 return top if d==1 else r'\frac{'+top+'}{'+str(d)+'}'
for role in ('prompt','solution'):
 fig,ax=plt.subplots(figsize=(5.3,4.9));pad=r*.55
 xmin=min(0,h-r)-pad;xmax=max(0,h+r)+pad;ymin=min(0,k-r)-pad;ymax=max(0,k+r)+pad
 ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax);ax.set_aspect('equal');ax.axis('off')
 ax.annotate('',(xmax,0),(xmin,0),arrowprops={'arrowstyle':'->','color':'black','lw':1});ax.annotate('',(0,ymax),(0,ymin),arrowprops={'arrowstyle':'->','color':'black','lw':1});ax.text(xmax,.04*r,'$x$');ax.text(.04*r,ymax,'$y$')
 color='#2879bb'
 if role=='solution':
  t=np.linspace(0,2*np.pi,300);ax.plot(*xy(t),ls=(0,(3,3)),color=color,lw=1.4)
 t=np.linspace(a,b,250);ax.plot(*xy(t),color=color,lw=1.6)
 ax.scatter(*xy(np.array([a,b])),s=20,color=color,zorder=5)
 if h or k:
  ax.plot([h-r,h+r],[k,k],ls=(0,(4,3)),color='#999',lw=.8);ax.plot([h,h],[k-r,k+r],ls=(0,(4,3)),color='#999',lw=.8)
  ax.scatter([h],[k],s=8,color='#777');ax.text(h+.07*r,k-.12*r,f'$({h},{k})$',fontsize=9)
 for x in sorted(set([h-r,h,h+r])):
  if x:ax.plot([x,x],[-.025*r,.025*r],color='#aaa',lw=.7);ax.text(x,-.12*r,f'${x}$',ha='center',va='top',fontsize=10)
 for y in sorted(set([k-r,k,k+r])):
  if y:ax.plot([-.025*r,.025*r],[y,y],color='#aaa',lw=.7);ax.text(-.08*r,y,f'${y}$',ha='right',va='center',fontsize=10)
 # Source noncardinal arcs carry a dashed endpoint ray and a small orange angle.
 for endpoint in (a,b):
  if abs(endpoint/(np.pi/2)-round(endpoint/(np.pi/2)))>1e-8:
   ref=np.ceil(endpoint/(np.pi/2))*np.pi/2;tt=np.linspace(endpoint,ref,70)
   ex,ey=xy(endpoint);ax.plot([h,ex],[k,ey],ls=(0,(4,3)),color='#888',lw=.8)
   ax.plot(h+.27*r*np.cos(tt),k+.27*r*np.sin(tt),color='#dba02c',lw=1)
   mid=(endpoint+ref)/2;ax.text(h+.38*r*np.cos(mid),k+.38*r*np.sin(mid),'$'+theta_text(ref-endpoint)+'$',ha='center',va='center',fontsize=11)
 if role=='solution':
  # Arrow tangent follows increasing theta, never independently sampled.
  m=a+.37*(b-a);ax.annotate('',xy(m+.06),xy(m-.06),arrowprops={'arrowstyle':'->','color':color,'lw':1.3})
  labels=sorted(set([0,np.pi/2,np.pi,3*np.pi/2,a,b]))
  labels=[t for t in labels if abs(t-2*np.pi)>1e-8]
  for t in labels:
   x,y=xy(t);ax.scatter([x],[y],s=10,color=color,zorder=4)
   lx=h+1.17*r*np.cos(t);ly=k+1.17*r*np.sin(t)
   label=theta_text(t)
   if t==0 and abs(b-2*np.pi)<1e-8:label=r'2\pi'
   ax.text(lx,ly,r'$\theta='+label+'$',fontsize=10,ha='left' if np.cos(t)>.2 else 'right' if np.cos(t)<-.2 else 'center',va='bottom' if np.sin(t)>=0 else 'top')
 fig.savefig(out/(role+'.png'),dpi=135,bbox_inches='tight',facecolor='white');plt.close(fig)
(out/'spec.json').write_text(json.dumps({'parameters':p,'sample_count':250,'closed_endpoints':True,'orientation':'counterclockwise','angular_speed':1,'bounds':[xmin,xmax,ymin,ymax],'solid_interval':[p['start'],p['end']],'renderer':'Matplotlib','python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance},indent=2)+'\n')
