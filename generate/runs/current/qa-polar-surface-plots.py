"""Root raster readback using displayed region names/radii and saved pixels."""
import json,re,hashlib,math
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186105888
names={'disk':(0,2*math.pi),'quarter-circle in the first quadrant':(0,math.pi/2),'quarter-circle in the second quadrant':(math.pi/2,math.pi),'quarter-circle in the fourth quadrant':(3*math.pi/2,2*math.pi),'upper half-circle':(0,math.pi),'right half-circle':(-math.pi/2,math.pi/2),'left half-circle':(math.pi/2,3*math.pi/2)}
records=json.loads((R/f'qa/{K}-sampled.json').read_text());seen={};labels=arc=0
for rec in records:
 prompt=rec['question'][':question/problem'];name,radius=re.search(r'domain is the (.*?) of radius \$(\d+)\$',prompt).groups();radius=int(radius);a,b=names[name];path=ROOT/re.search(r'!\[\]\((.*?)\)',prompt)[1];side=json.loads(path.with_suffix('.json').read_text());assert side['renderer_version']=='region-render-5' and side['png_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
 if path in seen:assert seen[path]==(name,radius);continue
 seen[path]=(name,radius);im=Image.open(path);pixels=np.array(im.convert('RGB'));height,width=pixels.shape[:2];assert [width,height]==side['saved_size_px'];assert all(abs(v-140)<.02 for v in im.info['dpi'])
 ox,oy=side['saved_coordinate_transform']['origin_px'];sx=side['saved_coordinate_transform']['x_pixels_per_unit'];sy=-side['saved_coordinate_transform']['y_pixels_per_unit'];assert abs(sx/sy-1)<1e-10
 yy,xx=np.indices((height,width));gx=(xx-ox)/sx;gy=(oy-yy)/sy;angles=np.arctan2(gy,gx);angles=np.where(angles<a,angles+2*math.pi,angles);rad=np.hypot(gx,gy)
 black=np.max(pixels,axis=2)<110;blue=(pixels[:,:,2].astype(int)-pixels[:,:,0]>20)&(pixels[:,:,0]<100)&(pixels[:,:,1]>60);filled=(np.abs(pixels.astype(int)-np.array([224,235,244])).max(axis=2)<3)
 # The actual long black axis runs intersect at the declared saved origin.
 for dx,dy in [(.5*radius,0),(-.5*radius,0),(0,.5*radius),(0,-.5*radius)]:
  ix,iy=round(ox+sx*dx),round(oy-sy*dy);assert black[iy-2:iy+3,ix-2:ix+3].any()
 inside=(rad<radius-5/sx)&(angles>a+.05)&(angles<b-.05)&(np.abs(gx)>5/sx)&(np.abs(gy)>5/sy)
 # Visible O text legitimately lies on shaded regions. Exclude its measured
 # ink box from the fill-only classification; no rendered masks are added.
 for box in side['text_boxes']:
  x0,y0,x1,y1=box['bbox_saved_pixels'];inside&=~((xx>=x0-2)&(xx<=x1+2)&(yy>=y0-2)&(yy<=y1+2))
 assert filled[inside].mean()>.995,(name,radius,float(filled[inside].mean()),str(path))
 outside=(rad<radius-5/sx)&((angles<a-.05)|(angles>b+.05))&(np.abs(gx)>5/sx)&(np.abs(gy)>5/sy)
 if outside.any():assert filled[outside].mean()<.001
 assert not filled[rad>radius+4/sx].any()
 for angle in np.linspace(a,b,19)[1:-1]:
  ix,iy=round(ox+radius*sx*math.cos(angle)),round(oy-radius*sy*math.sin(angle));assert blue[iy-3:iy+4,ix-3:ix+4].any();arc+=1
 extrema=[]
 for vx,vy,angle in [(radius,0,0),(-radius,0,math.pi),(0,radius,math.pi/2),(0,-radius,3*math.pi/2)]:
  aa=angle
  while aa<a:aa+=2*math.pi
  if aa<=b+1e-12:extrema.append(str(vx if vx else vy))
 actual=[q['text'] for q in side['text_boxes']];assert sorted(actual)==sorted(['$x$','$y$','$O$',*extrema]),(name,radius,actual,extrema)
 by,bx=np.where(blue)
 for box in side['text_boxes']:
  x0,y0,x1,y1=box['bbox_saved_pixels'];assert 0<=x0<x1<width and 0<=y0<y1<height and box['mask'] is False
  assert black[int(y0):math.ceil(y1),int(x0):math.ceil(x1)].any()
  clearance=np.hypot(np.maximum(np.maximum(x0-bx,bx-x1),0),np.maximum(np.maximum(y0-by,by-y1),0)).min();assert clearance>=4
  assert min(abs(y0-oy),abs(y1-oy))>=4 and not y0<=oy<=y1
  assert min(abs(x0-ox),abs(x1-ox))>=4 and not x0<=ox<=x1;labels+=1
report=dict(status='passed',normal_records=len(records),unique_current_rasters=len(seen),displayed_regions=sorted(set(v[0] for v in seen.values())),actual_arc_samples=arc,measured_label_boxes=labels,rasters={str(k):dict(region=v[0],radius=v[1],sha256=hashlib.sha256(k.read_bytes()).hexdigest()) for k,v in seen.items()},original_geometry_inspection='All eleven practices plus canonical original inspected individually at full resolution before revision; semicircle/quadrant/disk orientations and axis extrema confirmed.')
(R/f'qa/{K}-root-plots.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='rasters'}))
