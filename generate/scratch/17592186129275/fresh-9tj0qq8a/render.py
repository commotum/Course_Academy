"""Matplotlib plot renderer. Uses cached read-only wheels if needed; no SVG writing."""
import json,os,re,subprocess,sys,pathlib,tempfile
os.environ['MPLCONFIGDIR']='/tmp/kp17592186129275-mpl'
try:import matplotlib
except ImportError:
 runtime='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
 if sys.version_info[:2]!=(3,10):subprocess.run([runtime,__file__,*sys.argv[1:]],check=True);sys.exit(0)
 cache=pathlib.Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  options=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(options,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1];sys.path.insert(0,str(path))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt,numpy as np
p=json.loads(pathlib.Path(sys.argv[1]).read_text());a=p['a'];sg=p['sign'];axis=p['axis'];lo,hi=p['bounds'];theta=np.linspace(lo,hi,401);rr=2*a*sg*(np.cos(theta) if axis=='x' else np.sin(theta));xx=rr*np.cos(theta);yy=rr*np.sin(theta)
for role,path in zip(('region','radius','angle'),p['paths']):
 fig,ax=plt.subplots(figsize=(4.8,4.1)); ax.fill(np.r_[0,xx,0],np.r_[0,yy,0],color='#dceaf5');ax.plot(xx,yy,color='#488fce',lw=1.5)
 ax.plot([0,xx[0]],[0,yy[0]],color='#488fce');ax.plot([0,xx[-1]],[0,yy[-1]],color='#488fce')
 xmin=min(0,min(xx));xmax=max(0,max(xx));ymin=min(0,min(yy));ymax=max(0,max(yy));pad=.65*a
 ax.set_xlim(xmin-pad,xmax+pad);ax.set_ylim(ymin-pad,ymax+pad);ax.set_aspect('equal');ax.axis('off')
 ax.annotate('',(xmax+pad*.85,0),(xmin-pad*.8,0),arrowprops={'arrowstyle':'->','color':'#333','lw':1});ax.annotate('',(0,ymax+pad*.8),(0,ymin-pad*.8),arrowprops={'arrowstyle':'->','color':'#333','lw':1})
 ax.text(xmax+pad*.85,.07*a,'$x$',fontsize=11);ax.text(.07*a,ymax+pad*.8,'$y$',fontsize=11)
 cx=sg*a if axis=='x' else 0;cy=sg*a if axis=='y' else 0
 for z in (sg*a,sg*2*a):
  if axis=='x':ax.text(z,-.15*a,'$'+('%g'%z)+'$',ha='center',va='top',fontsize=10)
  else:ax.text(-.13*a,z,'$'+('%g'%z)+'$',ha='right',va='center',fontsize=10)
 ax.text(cx+(0 if axis=='x' else (-.35*a if p['part']=='left' else .35*a)),cy+(0 if axis=='y' else (-.35*a if p['part']=='lower' else .35*a)),'$D$',color='#488fce',fontsize=12)
 ax.set_title('$'+p['boundary_tex']+'='+p['radius_tex']+'^2$',fontsize=12,pad=5)
 if role=='radius':
  th=(lo+hi)/2+.18*(hi-lo);rad=2*a*sg*(np.cos(th) if axis=='x' else np.sin(th));end=(rad*np.cos(th),rad*np.sin(th));ax.annotate('',end,(0,0),arrowprops={'arrowstyle':'->','color':'#c586b2','lw':1.5});ax.text(end[0]*.5,end[1]*.5+(.3*a if end[1]>=0 else -.3*a),'$0\\leq r\\leq '+p['upper_tex']+'$',ha='center',color='#b96d9f',fontsize=10)
 if role=='angle':
  th=np.linspace(lo,hi,150);aa=.25*a;ax.plot(aa*np.cos(th),aa*np.sin(th),color='#ddb448');ax.annotate('',(aa*np.cos(hi),aa*np.sin(hi)),(aa*np.cos(hi-.12),aa*np.sin(hi-.12)),arrowprops={'arrowstyle':'->','color':'#ddb448'});ax.text(.5*a,np.sign((lo+hi)/2 if (lo+hi)/2 else 1)*.25*a,'$'+p['bounds_tex'][0]+r'\leq\theta\leq '+p['bounds_tex'][1]+'$',color='#bf9427',fontsize=10)
 fd,tmp=tempfile.mkstemp(suffix='.png',dir=pathlib.Path(path).parent);os.close(fd)
 fig.savefig(tmp,dpi=130,bbox_inches='tight',facecolor='white');plt.close(fig);os.replace(tmp,path)
 side=pathlib.Path(path).with_suffix('.json');fd,tmp=tempfile.mkstemp(suffix='.json',dir=side.parent);os.close(fd);pathlib.Path(tmp).write_text(json.dumps({'geometry':p,'role':role,'python':sys.version,'matplotlib':matplotlib.__version__},indent=2));os.replace(tmp,side)
