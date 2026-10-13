"""Read-only cached Matplotlib fallback; one unique input per invocation."""
import json,os,re,sys
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186087657-mpl'
paths={}
try: import matplotlib
except ImportError:
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for pkg in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/pkg).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  p=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(p));paths[pkg]=str(p)
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
p=json.loads(Path(sys.argv[1]).read_text());x1,y1,x2,y2=[p[k] for k in ('x1','y1','x2','y2')]
h=(x1+x2)/2;k=(y1+y2)/2;r=((x1-x2)**2+(y1-y2)**2)**.5/2
lo_x=min(0,h-r)-1.5;hi_x=max(0,h+r)+1.5;lo_y=min(0,k-r)-1.5;hi_y=max(0,k+r)+1.5
fig,ax=plt.subplots(figsize=(5,5));ax.set_aspect('equal');ax.set_xlim(lo_x,hi_x);ax.set_ylim(lo_y,hi_y);ax.axis('off')
ax.annotate('',xy=(hi_x-.2,0),xytext=(lo_x,0),arrowprops={'arrowstyle':'->','color':'black','lw':1.1});ax.annotate('',xy=(0,hi_y-.2),xytext=(0,lo_y),arrowprops={'arrowstyle':'->','color':'black','lw':1.1})
ax.text(hi_x-.1,-.3,'$x$');ax.text(.2,hi_y-.2,'$y$')
ax.add_patch(Circle((h,k),r,fill=False,color='red',lw=1.5));ax.plot([x1,x2],[y1,y2],color='blue',lw=.7,ls=(0,(6,5)));ax.plot([x1,x2],[y1,y2],'.',color='red',ms=6)
for name,x,y in [('X',x1,y1),('Y',x2,y2)]:
 dx=x-h;dy=y-k;ox=7 if dx>=0 else -7;oy=8 if dy>=0 else -9
 ax.annotate(f'${name}({x},{y})$',(x,y),xytext=(ox,oy),textcoords='offset points',ha='left' if ox>0 else 'right',va='bottom' if oy>0 else 'top',fontsize=10)
fig.tight_layout(pad=.6);fig.canvas.draw();scale=110/fig.dpi;pixel_center=[float(v)*scale for v in ax.transData.transform((h,k))];pixel_edge=[float(v)*scale for v in ax.transData.transform((h+r,k))];pixel_endpoints=[[float(v)*scale for v in ax.transData.transform(pt)] for pt in ((x1,y1),(x2,y2))];pixel_radius=pixel_edge[0]-pixel_center[0];out=Path(p['output']);tmp=out.with_name(out.stem+'.'+str(os.getpid())+'.png');fig.savefig(tmp,dpi=110,facecolor='white');plt.close(fig);tmp.replace(out)
side={'renderer_version':'diameter-3','parameters':{k:p[k] for k in ('x1','y1','x2','y2')},'center':[h,k],'radius':r,'bounds':[lo_x,hi_x,lo_y,hi_y],'equal_aspect':True,'pixel_center_bottom_origin':pixel_center,'pixel_radius':pixel_radius,'pixel_endpoints_bottom_origin':pixel_endpoints,'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':paths}
tmp=out.with_name(out.stem+'.'+str(os.getpid())+'.json');tmp.write_text(json.dumps(side,indent=2)+'\n');tmp.replace(out.with_suffix('.json'))
