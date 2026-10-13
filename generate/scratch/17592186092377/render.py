"""Matplotlib plots and source montage; read-only cached dependencies, no install."""
import os,sys,re,json,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186092377-mpl'
try: import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):
  subprocess.run([str(runtime),str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit()
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (Path('/home/jake/.cache/uv/wheels-v5/pypi')/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
if sys.argv[1]=='sources':
 from PIL import Image,ImageOps,ImageDraw
 qs=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']
 images=[]
 for q in qs:
  for ref in re.findall(r'!\[.*?\]\((.*?)\)',q[':question/problem']):
   original=Image.open('/media/jake/SSD/EDB/math/'+ref).convert('RGBA');im=Image.new('RGBA',original.size,'white');im.alpha_composite(original);im=im.convert('RGB');im.thumbnail((370,310))
   panel=Image.new('RGB',(390,345),'white');panel.paste(im,((390-im.width)//2,25));ImageDraw.Draw(panel).text((5,5),q[':question/math-academy-id'],fill='black');images.append(panel)
 for page in range((len(images)+5)//6):
  montage=Image.new('RGB',(1170,690),'white')
  for i,im in enumerate(images[page*6:page*6+6]):montage.paste(im,((i%3)*390,(i//3)*345))
  montage.save(HERE/f'source-plots-{page}.png')
elif sys.argv[1]=='review':
 from PIL import Image,ImageDraw
 records=json.loads((HERE/'review.json').read_text())
 if (HERE/'engine-input.json').exists():records += [item['record'] for item in json.loads((HERE/'engine-input.json').read_text()) if item['label'].startswith('boundary/')]
 if (HERE/'cli-preview.json').exists():records += json.loads((HERE/'cli-preview.json').read_text())
 panels=[];seen=set()
 for r in records:
  path=r['generation'].get('plot')
  if not path or not Path(path).is_absolute() or path in seen:continue
  seen.add(path);im=Image.open(path).convert('RGB');im.thumbnail((450,350));panel=Image.new('RGB',(480,390),'white');panel.paste(im,((480-im.width)//2,32))
  meta=r['generation'];label=meta['template']+'  scale='+meta['parameters'].get('scale','1')+'  upper='+meta['parameters']['upper'];ImageDraw.Draw(panel).text((8,6),label,fill='black');panels.append(panel)
 for page in range((len(panels)+5)//6):
  canvas=Image.new('RGB',(1440,780),'white')
  for i,im in enumerate(panels[6*page:6*page+6]):canvas.paste(im,((i%3)*480,(i//3)*390))
  canvas.save(HERE/f'generated-plots-{page}.png')
else:
 data=json.loads(Path(sys.argv[1]).read_text())
 for obj in data:
  fig,ax=plt.subplots(figsize=(5.8,4.6));x=np.array(obj['x']);y=np.array(obj['y']);ax.plot(x,y,color='#2475c7',lw=2.3)
  if obj.get('context_x') is not None:ax.plot(obj['context_x'],obj['context_y'],color='#2475c7',lw=1,alpha=.45,ls=':')
  j=len(x)//2;ax.annotate('',xy=(x[j+6],y[j+6]),xytext=(x[j-6],y[j-6]),arrowprops={'arrowstyle':'->','color':'#2475c7','lw':1.5})
  ax.scatter([x[0],x[-1]],[y[0],y[-1]],s=28,color='#2475c7',zorder=3)
  for i,label in [(0,obj['start_label']),(-1,obj['end_label'])]:
   # Place endpoint labels inward and offset vertically from the other label.
   context_x=np.array(obj.get('context_x',x));context_y=np.array(obj.get('context_y',y));cx=(context_x.min()+context_x.max())/2;cy=(context_y.min()+context_y.max())/2
   dx=-8 if x[i]>cx else 8;dy=-18 if y[i]>cy else 8
   ax.annotate(label,(x[i],y[i]),xytext=(dx,dy),textcoords='offset points',fontsize=9,ha='right' if dx<0 else 'left',annotation_clip=False)
  ax.margins(.12)
  ax.axhline(0,color='black',lw=.7);ax.axvline(0,color='black',lw=.7);ax.set_xlabel('$x$');ax.set_ylabel('$y$',rotation=0);ax.set_aspect('equal',adjustable='datalim');ax.grid(alpha=.12)
  fig.tight_layout();fig.savefig(obj['path'],dpi=135);plt.close(fig)
 (HERE/'render-provenance.json').write_text(json.dumps({'python':sys.version,'matplotlib':matplotlib.__version__,'numpy':np.__version__,'renderer':'Matplotlib Agg','no_install':True},indent=2))
