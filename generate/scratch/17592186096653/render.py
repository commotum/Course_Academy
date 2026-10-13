"""Private Matplotlib renderer; cached Python 3.10 wheels are read only."""
import os,sys,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR']='/tmp/kp96653-mpl'
try:import matplotlib
except ImportError:
 runtime='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
 if sys.version_info[:2]!=(3,10):
  subprocess.run([runtime,__file__,*sys.argv[1:]],check=True);sys.exit()
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  sys.path.insert(0,str(sorted(candidates)[-1]))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
if sys.argv[1]=='contact':
 from PIL import Image,ImageOps,ImageDraw
 s=json.load(open(HERE/'source.json'));qs=s['record'][':knowledge-point/questions'];sheet=Image.new('RGB',(1200,1500),'white');d=ImageDraw.Draw(sheet)
 for i,q in enumerate(qs):
  ref=re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1);im=Image.open(Path('/media/jake/SSD/EDB/math')/ref).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);bg=ImageOps.contain(bg.convert('RGB'),(280,210));x=i%4*300;y=i//4*250;sheet.paste(bg,(x,y+25));d.text((x+10,y+5),q[':question/math-academy-id'],fill='black')
 sheet.save(HERE/'source-contact.png');sys.exit()
p=json.load(open(sys.argv[1]));target=Path(sys.argv[2]);r,s=p['r'],p['s'];A=(0,0);B=(4,0);O=(.6,2.2);X=(4*r/(r+s),0)
fig,ax=plt.subplots(figsize=(5,3.3));ax.set_aspect('equal');ax.axis('off')
ax.plot([0,4],[0,0],color='black',lw=1.5)
for end,v in [(A,p['u']),(B,p['v'])]:
 ax.annotate('',end,O,arrowprops={'arrowstyle':'->','color':'#258bc3','lw':2});ax.text((end[0]+O[0])/2-.25,(end[1]+O[1])/2+.03,'$'+v+'$',fontsize=15)
ax.annotate('',X,O,arrowprops={'arrowstyle':'->','color':'#e69b00','lw':1.8})
for pt,label,off in [(O,'O',(-.12,.15)),(A,p['A'],(-.15,-.28)),(B,p['B'],(.02,-.28)),(X,p['X'],(-.08,-.28))]:ax.text(pt[0]+off[0],pt[1]+off[1],label,fontsize=14)
ax.plot(*X,'o',color='#258bc3',ms=4);ax.set_xlim(-.5,4.5);ax.set_ylim(-.55,2.75)
fig.savefig(target,dpi=125,facecolor='white',bbox_inches='tight');plt.close(fig)
Path(str(target)+'.json').write_text(json.dumps({'renderer':'Matplotlib','version':matplotlib.__version__,'python':sys.version,'parameters':p,'O':O,'A':A,'B':B,'X':X,'ratio':[r,s]},indent=2))
