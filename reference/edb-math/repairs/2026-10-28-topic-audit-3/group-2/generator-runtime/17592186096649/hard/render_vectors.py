"""Read-only cached Matplotlib fallback; atomic, instance-specific rendering."""
import json, os, sys, tempfile
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir())/'parallel-vectors-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
def render_one(spec):
 out=Path(spec['output']);out.parent.mkdir(exist_ok=True)
 fig,ax=plt.subplots(figsize=(1.8,1.8),dpi=100);ax.set_position([.03,.03,.94,.94]);ax.set_xlim(*spec['bounds'][0]);ax.set_ylim(*spec['bounds'][1]);ax.set_aspect('equal');ax.axis('off')
 texts=[];arrows=[];patches=[]
 for v in spec['vectors']:
  tail=np.array(v['tail'],float);tip=tail+np.array(v['vector'],float)
  arrow=FancyArrowPatch(tail,tip,arrowstyle='-|>',mutation_scale=min(6,max(2,0.4*float(np.linalg.norm(ax.transData.transform(tip)-ax.transData.transform(tail))))),linewidth=1.2,color=v['color'],shrinkA=0,shrinkB=0)
  ax.add_patch(arrow);arrows.append((tail,tip));patches.append(arrow)
 fig.canvas.draw()
 occupied=[]
 def clearance(box):
  distances=[]
  for tail,tip in arrows:
   pts=ax.transData.transform(np.linspace(tail,tip,401));dx=np.maximum(np.maximum(box.x0-pts[:,0],pts[:,0]-box.x1),0);dy=np.maximum(np.maximum(box.y0-pts[:,1],pts[:,1]-box.y1),0);distances.append(float(np.min(np.sqrt(dx*dx+dy*dy))))
  return min(distances)
 for v,(tail,tip) in zip(spec['vectors'],arrows):
  d=tip-tail;normal=np.array([-d[1],d[0]])/np.linalg.norm(d);mid=(tail+tip)/2
  text=ax.text(*mid,'$'+v['label']+'$',fontsize=9,ha='center',va='center')
  fig.canvas.draw();box=text.get_window_extent(fig.canvas.get_renderer());pixel_unit=np.linalg.norm(ax.transData.transform(normal)-ax.transData.transform([0,0]));needed=(abs(normal[0])*box.width/2+abs(normal[1])*box.height/2+4)/pixel_unit
  found=False
  for factor in (1,1.2,1.5,1.8,2.2):
   for side in (1,-1):
    for shift in (0,.15,-.15,.3,-.3):
     text.set_position(mid+normal*side*max(spec['label_offset'],needed)*factor+d*shift);fig.canvas.draw();box=text.get_window_extent(fig.canvas.get_renderer())
     if ax.bbox.contains(box.x0,box.y0) and ax.bbox.contains(box.x1,box.y1) and clearance(box)>3 and all(not box.overlaps(old) for old in occupied):found=True;break
    if found:break
   if found:break
  assert found,('no clear compact label position',spec)
  occupied.append(box);texts.append(text)
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
 fig.savefig(tmp,dpi=100,facecolor='white');plt.close(fig);os.replace(tmp,out)
 report={'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'spec':spec,'text_boxes':[list(b.bounds) for b in bboxes],'minimum_text_arrow_clearance_px':min(clearances),'patch_vertices_pixels':[p.get_transform().transform(p.get_path().vertices).tolist() for p in patches],'patch_codes':[p.get_path().codes.tolist() for p in patches],'axes':False,'ticks':False,'arrow_tail_tip_pixels':[[list(ax.transData.transform(t)),list(ax.transData.transform(p))] for t,p in arrows],'width':180,'height':180}
 fd,tmp=tempfile.mkstemp(suffix='.json',dir=out.parent);os.close(fd);Path(tmp).write_text(json.dumps(report,indent=2)+'\n');os.replace(tmp,out.with_suffix('.json'))

if __name__ == '__main__':
 source=json.loads(Path(sys.argv[1]).read_text())
 for spec in (source if isinstance(source,list) else [source]):render_one(spec)
