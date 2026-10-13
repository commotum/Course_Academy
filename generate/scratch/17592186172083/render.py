"""Private Matplotlib renderer; cached dependencies read only."""
import json,os,re,sys
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186172083-mpl'
cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
 paths=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
 path=sorted(paths,key=lambda p:tuple(int(z) for z in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
 sys.path.insert(0,str(path))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image,ImageOps,ImageDraw
H=Path(__file__).resolve().parent
if sys.argv[1]=='montage':
 src=json.loads((H/'source.json').read_text())['record'][':knowledge-point/questions']
 for q in src:
  sheet=Image.new('RGB',(1800,400),'white');d=ImageDraw.Draw(sheet)
  for i,a in enumerate(q[':question/answer-fields'][0][':answer-field/choices']):
   im=Image.open('/media/jake/SSD/EDB/math/'+a[':answer/value']).convert('RGBA'); bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);bg=ImageOps.contain(bg.convert('RGB'),(350,350));sheet.paste(bg,(i*360,40));d.text((i*360+10,5),str(i+1)+' '+a[':answer/value'][7:12],fill='black')
  sheet.save(H/(q[':question/math-academy-id']+'-original.png'))
else:
 data=json.loads(Path(sys.argv[1]).read_text())
 for item in data:
  fig,ax=plt.subplots(figsize=(5,5));bounds=item['bounds'];ax.set(xlim=bounds[:2],ylim=bounds[2:]);ax.set_aspect('equal');ax.set_xticks(range(int(bounds[0]),int(bounds[1])+1));ax.set_yticks(range(int(bounds[2]),int(bounds[3])+1));ax.grid(color='#b7dbe1',linewidth=.6);
  if item['grid_increment']<1:
   from matplotlib.ticker import MultipleLocator
   ax.xaxis.set_minor_locator(MultipleLocator(item['grid_increment']));ax.yaxis.set_minor_locator(MultipleLocator(item['grid_increment']));ax.grid(which='minor',color='#d8e8eb',linewidth=.4)
  ax.axhline(0,color='black',lw=.8);ax.axvline(0,color='black',lw=.8);ax.tick_params(labelsize=7);ax.set_xlabel('x');ax.set_ylabel('y',rotation=0)
  for (x,y),(u,v) in zip(item['points'],item['vectors']):
   ax.scatter([x],[y],s=12,color='#15518d',zorder=4);ax.annotate('',xy=(x+u,y+v),xytext=(x,y),arrowprops={'arrowstyle':'-|>','color':'#174a84','lw':1.6,'mutation_scale':11},zorder=3)
  fig.tight_layout();out=Path(item['path']);tmp=out.with_name(out.stem+'-'+str(os.getpid())+'.png');fig.savefig(tmp,dpi=120);plt.close(fig);os.replace(tmp,out)
  side=out.with_suffix('.json');temp=side.with_name(side.stem+'-'+str(os.getpid())+'.tmp');temp.write_text(json.dumps({**item,'renderer':'Matplotlib','matplotlib':matplotlib.__version__,'python':sys.version},indent=2));os.replace(temp,side)
