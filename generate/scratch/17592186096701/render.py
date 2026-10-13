"""Private Matplotlib rendering; cached dependencies read only, atomic assets."""
import os,sys,json,re,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp17592186096701-mpl'
try: import matplotlib
except ImportError:
 if sys.version_info[:2]!=(3,10):
  subprocess.run(['/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10',__file__,*sys.argv[1:]],check=True);sys.exit()
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x) for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name) else (0,))[-1]
  sys.path.insert(0,str(path))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageDraw

def atomic(path,writer):
 fd,tmp=tempfile.mkstemp(prefix='.atomic-',dir=path.parent,suffix=path.suffix);os.close(fd)
 try: writer(tmp);os.replace(tmp,path)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
if sys.argv[1]=='sources':
 r=json.load(open(HERE/'source.json'))['record'];qs=r[':knowledge-point/questions']
 canvas=Image.new('RGB',(1600,len(qs)*265),'white');d=ImageDraw.Draw(canvas)
 for i,q in enumerate(qs):
  d.text((5,i*265),q[':question/math-academy-id']+' '+q[':question/difficulty'][':db/ident'],fill='black')
  for j,k in enumerate((':question/problem',':question/worked-solution')):
   path=re.findall(r'!\[\]\((.*?)\)',q[k])[0]
   im=Image.open('/media/jake/SSD/EDB/math/'+path).convert('RGBA');im.thumbnail((760,240));bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);canvas.paste(bg.convert('RGB'),(j*800,i*265+20))
 canvas.save(HERE/'source-contact.png')
elif sys.argv[1]=='audit':
 review=json.load(open(HERE/'review.json'));selected=[];audited=0
 for entry in review:
  r=entry['record'];path=Path(r['generation']['plots']['prompt']);side=path.with_suffix('.json')
  if not side.exists():continue
  geom=json.load(open(side))['plot_data'];im=np.array(Image.open(path).convert('RGB'));height,width=im.shape[:2]
  for name,color in [('A','blue'),('B','gold'),('C','black')]:
   pos=np.array(geom['pixel_endpoints'][name])*1.4;x,y=int(round(pos[0])),height-int(round(pos[1]));patch=im[max(0,y-10):y+11,max(0,x-10):x+11]
   if color=='blue':mask=(patch[:,:,2]>130)&(patch[:,:,0]<100)&(patch[:,:,1]>70)
   elif color=='gold':mask=(patch[:,:,0]>140)&(patch[:,:,1]>60)&(patch[:,:,1]<190)&(patch[:,:,2]<80)
   else:mask=(patch.max(2)<100)
   if not mask.any():raise AssertionError('Actual PNG lacks '+name+' arrowhead: '+str(path))
  audited+=1
  if entry['label'].startswith('authored') and len([x for x in selected if x['record']['question'][':question/difficulty']==r['question'][':question/difficulty']])<2:selected.append(entry)
 canvas=Image.new('RGB',(1200,420*3),'white');draw=ImageDraw.Draw(canvas)
 for idx,entry in enumerate(selected):
  im=Image.open(entry['record']['generation']['plots']['prompt']).convert('RGB');im.thumbnail((580,370));row=idx//2;col=idx%2;canvas.paste(im,(col*600,row*420+30));draw.text((col*600+10,row*420+5),entry['label'],fill='black')
 canvas.save(HERE/'generated-contact.png')
 (HERE/'raster-audit.json').write_text(json.dumps({'generated_prompt_pngs_audited':audited,'checks':'Actual raster contains blue, gold and black arrowhead pixels near independently expected transformed endpoints; exact math/geometry checked by validator; manual contact-sheet review supplements raster checks.'},indent=2)+'\n')

else:
 data=json.load(open(sys.argv[1]));target=Path(data['target']);a=np.array(data['a'],float);b=np.array(data['b'],float);ca=data['ca'];cb=data['cb'];C=ca*a+cb*b;O=np.zeros(2)
 fig,ax=plt.subplots(figsize=(6,4.2));ax.set_aspect('equal');ax.axis('off')
 known=data['unknown'];P=ca*a if known=='b' else cb*b
 # Unit coordinate grid is the assessed reading aid, like every source.
 pts=np.array([O,a,b,C,P]);lo=pts.min(0);hi=pts.max(0);span=np.maximum(hi-lo,1)
 ax.set_xlim(lo[0]-1.5,hi[0]+1.5);ax.set_ylim(lo[1]-1.5,hi[1]+1.5)
 ax.set_xticks(np.arange(np.floor(lo[0]-1),np.ceil(hi[0]+2),1));ax.set_yticks(np.arange(np.floor(lo[1]-1),np.ceil(hi[1]+2),1))
 ax.grid(True,color='#dddddd',lw=.65);ax.tick_params(left=False,bottom=False,labelleft=False,labelbottom=False)
 ax.set_axis_on()
 for spine in ax.spines.values():spine.set_visible(False)
 def arrow(start,end,label,color,off):
  ax.annotate('',xy=end,xytext=start,arrowprops={'arrowstyle':'-|>','color':color,'lw':1.8,'mutation_scale':13})
  mid=(start+end)/2;ax.text(*(mid+np.array(off)),label,fontsize=13,color=color,ha='center',va='center',bbox={'facecolor':'white','edgecolor':'none','pad':1})
 arrow(O,a,'$a$','#2897d2',(0,-.35));arrow(O,b,'$b$','#db9200',(-.35,0));arrow(O,C,'$c$','#222222',(.0,.35))
 if data['solution']:
  ax.plot(*np.array([O,P]).T,color='#db9200' if known=='a' else '#2897d2',ls='--',lw=1.2)
  ax.plot(*np.array([P,C]).T,color='#2897d2' if known=='a' else '#db9200',ls='--',lw=1.2)
  if np.linalg.norm(P-(b if known=='a' else a))>0.5:ax.text(*((O+P)/2+np.array([-.6,.4])),data['known_label'],fontsize=12,bbox={'facecolor':'white','edgecolor':'none'})
  ax.text(*((P+C)/2+np.array([.15,.45])),data['remaining_label'],fontsize=12,bbox={'facecolor':'white','edgecolor':'none'})
  ax.text(*(P+np.array([.25,-.3])),data['endpoint'],fontsize=13)
 ax.text(-.35,-.23,'O',fontsize=13);ax.text(*(a+np.array([-.35,.18])),'A',fontsize=13);ax.text(*(b+np.array([.15,-.3])),'B',fontsize=13);ax.text(*(C+np.array([.2,.15])),'C',fontsize=13)
 if data.get('lengths'):
  ax.text(.02,.98,data['lengths'],transform=ax.transAxes,ha='left',va='top',fontsize=12,bbox={'facecolor':'white','edgecolor':'none'})
 fig.canvas.draw();data['pixel_endpoints']={k:ax.transData.transform(v).tolist() for k,v in [('O',O),('A',a),('B',b),('C',C),('P',P)]};target.parent.mkdir(exist_ok=True)
 atomic(target,lambda t:fig.savefig(t,dpi=140,facecolor='white'));plt.close(fig)
 atomic(target.with_suffix('.json'),lambda t:Path(t).write_text(json.dumps({'plot_data':data,'matplotlib':matplotlib.__version__,'python':sys.version},indent=2)))
