"""Root rectangle/segment checks on corrected plot labels and leader routes."""
from pathlib import Path
import json,hashlib,itertools
from PIL import Image
R=Path(__file__).resolve().parent;K=17592186133897;D=R.parents[2]/f'generate/scratch/{K}'
def intersects(a,b,box):
 lo,hi=0.,1.
 for axis,minval,maxval in [(0,box[0],box[2]),(1,box[1],box[3])]:
  delta=b[axis]-a[axis]
  if abs(delta)<1e-12:
   if not minval<a[axis]<maxval:return False
  else:
   p,q=(minval-a[axis])/delta,(maxval-a[axis])/delta;lo=max(lo,min(p,q));hi=min(hi,max(p,q))
 return lo<hi and hi>0 and lo<1
C=dict(images=0,text_boxes=0,text_pair_checks=0,leader_segments=0,leader_text_checks=0,equal_scale=0)
for item in json.load(open(D/'plot-inspection.json'))['images']:
 path=Path(item['plot']);assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'];width,height=Image.open(path).size;side=json.load(open(path.with_suffix('.json')));boxes=list(side['text_boxes_pixels'].values())+side['axis_text_boxes_pixels']+side['tick_text_boxes_pixels']
 for box in boxes:assert 0<=box[0]<box[2]<width and 0<=box[1]<box[3]<height;C['text_boxes']+=1
 for a,b in itertools.combinations(boxes,2):assert min(a[2],b[2])<=max(a[0],b[0]) or min(a[3],b[3])<=max(a[1],b[1]);C['text_pair_checks']+=1
 for route in side['leader_paths_pixels'].values():
  for a,b in zip(route,route[1:]):
   assert all(0<=p[0]<width and 0<=p[1]<height for p in (a,b));C['leader_segments']+=1
   for box in boxes:assert not intersects(a,b,box),(item['family'],a,b,box);C['leader_text_checks']+=1
 assert abs(side['unit_pixels'][0]-side['unit_pixels'][1])<1e-8;C['equal_scale']+=1;C['images']+=1
p=R/f'qa/{K}-root-readback.json';report=json.load(open(p));report['plot_layout_readback']=C;report['plot_extremes_inspection']='Root independently viewed corrected reported cases and1/8,8/1 extreme PNGs at original resolution; source8 originalrasters alreadyinspected.';p.write_text(json.dumps(report,indent=2)+'\n');print(C)
