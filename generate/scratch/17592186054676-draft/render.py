"""Render only supplied plot data; cached read-only Matplotlib fallback."""
import json,os,re,subprocess,sys,tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186054676-draft-mpl'
provenance={}
try:import matplotlib
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):subprocess.run([str(runtime),'-B',str(Path(__file__)),*sys.argv[1:]],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in(cache/package).iterdir()if p.is_dir()and('cp310'in p.name and'manylinux'in p.name or'none-any'in p.name or p.name.startswith('4.59.1-'))]
  path=sorted(candidates,key=lambda p:tuple(int(x)for x in re.match(r'(\d+)\.(\d+)\.(\d+)',p.name).groups())if re.match(r'(\d+)\.(\d+)\.(\d+)',p.name)else(0,))[-1];sys.path.insert(0,str(path));provenance[package]=str(path)
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=json.loads(Path(sys.argv[1]).read_text());p=r['parameters'];target=Path(r['output']);xs,ys=zip(*p['points']);lo=min(-2,*xs)-1;hi=max(2,*xs)+2;bottom=min(-2,*ys)-1;top=max(2,*ys)+2
fig,ax=plt.subplots(figsize=(5,5),dpi=120);ax.set_xlim(lo,hi);ax.set_ylim(bottom,top);ax.set_aspect('equal');ax.set_xticks(range(lo,hi+1));ax.set_yticks(range(bottom,top+1));ax.grid(color='#c8c8c8',linewidth=.65);ax.set_axisbelow(True)
for name in('left','bottom'):ax.spines[name].set_position('zero')
for name in('right','top'):ax.spines[name].set_visible(False)
ax.tick_params(labelsize=8,length=2)
# Remove overlapping zero tick labels; origin is implied by crossed axes.
ax.set_xticklabels([str(x)if x else''for x in range(lo,hi+1)]);ax.set_yticklabels([str(y)if y else''for y in range(bottom,top+1)])
ax.annotate('',xy=(hi,0),xytext=(lo,0),arrowprops={'arrowstyle':'->','color':'black'});ax.annotate('',xy=(0,top),xytext=(0,bottom),arrowprops={'arrowstyle':'->','color':'black'});ax.text(hi-.3,.5,'x',fontsize=11);ax.text(.4,top-.5,'y',fontsize=11)
labels=[]
for label,(x,y)in zip('ABC',p['points']):
 ax.plot(x,y,'o',color='red',markersize=4,zorder=5);offset=(-14 if x<0 else 6,8);ann=ax.annotate(label,(x,y),xytext=offset,textcoords='offset points',fontsize=11,bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':.3});labels.append(ann)
fig.tight_layout(pad=1);fig.canvas.draw();renderer=fig.canvas.get_renderer();bounds=[list(a.get_window_extent(renderer).bounds)for a in labels];w,h=fig.canvas.get_width_height();assert all(0<=x and 0<=y and x+ww<=w and y+hh<=h for x,y,ww,hh in bounds)
with tempfile.NamedTemporaryFile(suffix='.png',dir=target.parent,delete=False)as f:temp=Path(f.name)
fig.savefig(temp,metadata={'Software':'Course Academy point-line draft2'});plt.close(fig);os.replace(temp,target)
target.with_suffix('.json').write_text(json.dumps({'parameters':p,'plotted_points':dict(zip('ABC',p['points'])),'bounds':[lo,hi,bottom,top],'label_pixel_bounds':bounds,'canvas':[w,h],'labels_not_clipped':True,'equal_aspect':True,'renderer':{'matplotlib':matplotlib.__version__,'python':sys.version,'dependency_paths':provenance}},indent=2)+'\n')
