"""Read-only cached Matplotlib fallback; atomic, instance-specific rendering."""
import json, os, re, sys, tempfile
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/kp17592186096649-mpl'
try:
 import matplotlib
except ImportError:
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in ('matplotlib','numpy','pillow','contourpy','kiwisolver','fonttools','cycler','packaging','pyparsing','python-dateutil','six'):
  candidates=[p for p in (cache/package).iterdir() if p.is_dir() and ('cp310' in p.name and 'manylinux' in p.name or 'none-any' in p.name or p.name.startswith('4.59.1-'))]
  if not candidates:raise RuntimeError(package)
  sys.path.insert(0,str(sorted(candidates)[-1]))
 import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
def render_one(spec):
 out=Path(spec['output']);out.parent.mkdir(exist_ok=True)
 fig,ax=plt.subplots(figsize=(5,5),dpi=120);ax.set_position([.03,.03,.94,.94]);ax.set_xlim(*spec['bounds'][0]);ax.set_ylim(*spec['bounds'][1]);ax.set_aspect('equal');ax.axis('off')
 texts=[];arrows=[];patches=[]
 for i,v in enumerate(spec['vectors']):
  tail=np.array(v['tail'],float); tip=tail+np.array(v['vector'],float)
  arrow=FancyArrowPatch(tail,tip,arrowstyle='-|>',mutation_scale=13,linewidth=1.7,color=v['color'],shrinkA=0,shrinkB=0)
  ax.add_patch(arrow);arrows.append((tail,tip));patches.append(arrow)
  d=tip-tail;normal=np.array([-d[1],d[0]])/np.linalg.norm(d)
  loc=(tail+tip)/2+normal*spec['label_offset']
  text=ax.text(*loc,'$'+v['label']+'$',fontsize=14,ha='center',va='center',rotation=0)
  fig.canvas.draw();box=text.get_window_extent(fig.canvas.get_renderer())
  pixel_unit=np.linalg.norm(ax.transData.transform(normal)-ax.transData.transform([0,0]))
  needed=(abs(normal[0])*box.width/2+abs(normal[1])*box.height/2+12)/pixel_unit
  text.set_position((tail+tip)/2+normal*max(spec['label_offset'],needed));texts.append(text)
 fig.canvas.draw();renderer=fig.canvas.get_renderer();bboxes=[t.get_window_extent(renderer) for t in texts]
 # Actual text boxes versus every arrow stroke. Text must remain visible and clear.
 clearances=[]
 for box in bboxes:
  assert ax.bbox.contains(box.x0,box.y0) and ax.bbox.contains(box.x1,box.y1),'label clipping'
  for tail,tip in arrows:
   pts=ax.transData.transform(np.linspace(tail,tip,801))
   dx=np.maximum(np.maximum(box.x0-pts[:,0],pts[:,0]-box.x1),0)
   dy=np.maximum(np.maximum(box.y0-pts[:,1],pts[:,1]-box.y1),0)
   distance=float(np.min(np.sqrt(dx*dx+dy*dy)));clearances.append(distance)
   assert distance>3,'text touches arrow stroke'
 for i,a in enumerate(bboxes):
  for b in bboxes[i+1:]:assert not a.overlaps(b),'labels overlap'
 fd,tmp=tempfile.mkstemp(suffix='.png',dir=out.parent);os.close(fd)
 fig.savefig(tmp,dpi=120,facecolor='white');plt.close(fig);os.replace(tmp,out)
 report={'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'spec':spec,'text_boxes':[list(b.bounds) for b in bboxes],'minimum_text_arrow_clearance_px':min(clearances),'patch_vertices_pixels':[p.get_transform().transform(p.get_path().vertices).tolist() for p in patches],'patch_codes':[p.get_path().codes.tolist() for p in patches],'axes':False,'ticks':False,'arrow_tail_tip_pixels':[[list(ax.transData.transform(t)),list(ax.transData.transform(p))] for t,p in arrows],'width':600,'height':600}
 fd,tmp=tempfile.mkstemp(suffix='.json',dir=out.parent);os.close(fd);Path(tmp).write_text(json.dumps(report,indent=2)+'\n');os.replace(tmp,out.with_suffix('.json'))

source=json.loads(Path(sys.argv[1]).read_text())
for spec in (source if isinstance(source,list) else [source]):render_one(spec)
