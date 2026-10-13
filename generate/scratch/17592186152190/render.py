"""Cached read-only Matplotlib renderer; exact instance parameters in JSON."""
import json,os,re,subprocess,sys
from pathlib import Path
from fractions import Fraction
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186152190-mpl'
provenance={}
try: import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path));provenance[package]=str(path.resolve())
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageOps,ImageDraw
if sys.argv[1]=='montage':
 qs=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']
 for page in range(3):
  canvas=Image.new('RGB',(1600,1800),'white');draw=ImageDraw.Draw(canvas)
  for i,q in enumerate(qs[page*6:page*6+6]):
   refs=re.findall(r'!\[.*?\]\((.*?)\)',q[':question/problem']+q[':question/worked-solution'])
   for role,ref in enumerate(refs):
    im=Image.open(Path('/media/jake/SSD/EDB/math')/ref).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=bg.convert('RGB');im.thumbnail((760,260))
    x=role*800;y=i*300;canvas.paste(im,(x+(780-im.width)//2,y+30));draw.text((x+10,y+5),q[':question/math-academy-id']+' '+('prompt' if role==0 else 'solution'),fill='black')
  canvas.save(HERE/f'source-montage-{page}.png')
else:
 data=json.loads(Path(sys.argv[1]).read_text());p=data['parameters'];a,b,h,k=[p[z] for z in ('a','b','h','k')];lo,hi=[float(Fraction(x))*np.pi for x in (p['lo'],p['hi'])]
 for role in ('prompt','solution'):
  out=Path(data['assets'][role]);out.parent.mkdir(exist_ok=True,parents=True)
  fig,ax=plt.subplots(figsize=(5.6,4.8));theta=np.linspace(0,2*np.pi,721)
  if role=='solution' or data['prompt_context']: ax.plot(h+a*np.cos(theta),k+b*np.sin(theta),color='#337ab7',lw=1.3,ls='--')
  theta=np.linspace(lo,hi,241);ax.plot(h+a*np.cos(theta),k+b*np.sin(theta),color='#337ab7',lw=3)
  ax.scatter([h+a*np.cos(lo),h+a*np.cos(hi)],[k+b*np.sin(lo),k+b*np.sin(hi)],color='#337ab7',s=24,zorder=5)
  if role=='solution':
   ax.axhline(k,color='#777777',ls=':',lw=1);ax.axvline(h,color='#777777',ls=':',lw=1);ax.scatter([h],[k],color='black',s=18)
   for t,label in ((0,r'\theta=2\pi' if p['hi']=='2' else r'\theta=0'),(np.pi/2,r'\theta=\frac{\pi}{2}'),(np.pi,r'\theta=\pi'),(3*np.pi/2,r'\theta=\frac{3\pi}{2}')):
    x,y=h+a*np.cos(t),k+b*np.sin(t);ax.scatter([x],[y],color='#337ab7',s=16,zorder=5)
    ax.annotate('$'+label+'$',(x,y),xytext=(8 if x>=h else -30,10 if y>=k else -18),textcoords='offset points',fontsize=12,color='#ba4f86')
   ax.annotate('center',(h,k),xytext=(5,-15),textcoords='offset points',fontsize=10)
  ax.axhline(0,color='black',lw=.8);ax.axvline(0,color='black',lw=.8)
  ax.set_xticks(sorted(set([0,h-a,h,h+a])));ax.set_yticks(sorted(set([0,k-b,k,k+b])))
  ax.set_xlim(min(0,h-a)-a*.35,max(0,h+a)+a*.35);ax.set_ylim(min(0,k-b)-b*.35,max(0,k+b)+b*.35)
  ax.set_xlabel('$x$');ax.set_ylabel('$y$',rotation=0);ax.set_aspect('equal');ax.grid(alpha=.18)
  fig.tight_layout();fig.savefig(out,dpi=130);plt.close(fig)
 (HERE/'render-provenance.json').write_text(json.dumps({'python':sys.version,'matplotlib':matplotlib.__version__,'dependency_paths':provenance},indent=2)+'\n')
