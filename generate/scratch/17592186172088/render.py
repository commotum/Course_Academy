"""Private Matplotlib renderer; dependency cache read-only, no installation."""
import os,sys,re,json,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186172088-mpl'
paths={}
try: import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates: raise RuntimeError('Missing cached '+package)
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));paths[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageDraw
if sys.argv[1]=='contact':
 s=json.loads((HERE/'source.json').read_text())['record'];qs=s[':knowledge-point/questions']
 refs=list(dict.fromkeys(re.findall(r'images/[^)]+','\n'.join(q[':question/problem'] for q in qs)+s[':knowledge-point/canonical-example'][':question/problem'])))
 board=Image.new('RGB',(1600,400*((len(refs)+3)//4)),'white');draw=ImageDraw.Draw(board)
 for n,r in enumerate(refs):
  im=Image.open('/media/jake/SSD/EDB/math/'+r).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB');im.thumbnail((390,365));board.paste(im,(400*(n%4),400*(n//4)+25));draw.text((400*(n%4),400*(n//4)),r[10:24],fill='black')
 board.save(HERE/'original-contact.png');sys.exit(0)
p=json.loads(Path(sys.argv[1]).read_text());output=Path(p['output']);sidecar=output.with_suffix('.json')
fig=plt.figure(figsize=(6,5.4));ax=fig.add_subplot(111,projection='3d');ax.set_proj_type('ortho')
coords=np.array([(x,y,z) for x in (-1.5,0,1.5) for y in (-1.5,0,1.5) for z in (-1.5,0,1.5)])
# A single common plotting factor scales every arrow; retain direction and relative lengths.
v=np.array(p['components'],dtype=float);length=.6/max(np.linalg.norm(v),1e-9)
u=np.tile(v,(len(coords),1));ax.quiver(*coords.T,*u.T,length=length,normalize=False,color='#2c76b8',arrow_length_ratio=.24,linewidth=1.35)
for i,label in enumerate('xyz'):
 start=np.zeros(3);end=np.zeros(3);start[i]=-2.1;end[i]=2.3
 ax.plot(*np.array([start,end]).T,color='black',linewidth=1.2)
 tail=np.zeros(3);tail[i]=2.0;direction=np.zeros(3);direction[i]=.3
 ax.quiver(*tail,*direction,length=1,normalize=False,color='black',arrow_length_ratio=.6,linewidth=1.2)
 end[i]=2.75;ax.text(*end,label,fontsize=15,color='black')
ax.set(xlim=(-2.5,2.5),ylim=(-2.5,2.5),zlim=(-2.5,2.5));ax.set_box_aspect((1,1,1));ax.view_init(elev=20,azim=35);ax.set_axis_off();fig.tight_layout()
fd,temp=tempfile.mkstemp(suffix='.png',dir=output.parent);os.close(fd);fig.savefig(temp,dpi=130,facecolor='white');plt.close(fig);os.replace(temp,output)
data={**p,'grid':coords.tolist(),'vectors':u.tolist(),'plot_scale':length,'zero_set':'empty','renderer':'Matplotlib mplot3d','axis_arrowheads':True,'renderer_version':2,'matplotlib':matplotlib.__version__,'python':sys.version,'dependency_paths':paths}
fd,temp=tempfile.mkstemp(suffix='.json',dir=output.parent);os.close(fd);Path(temp).write_text(json.dumps(data,indent=2));os.replace(temp,sidecar)
