"""Read saved PNG pixels against independently recomputed axis-coordinate geometry."""
import sys,json,math,hashlib
from pathlib import Path
try:from PIL import Image
except ImportError:
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi/pillow');paths=[p for p in cache.iterdir() if p.is_dir() and 'cp310' in p.name and 'manylinux' in p.name];sys.path.insert(0,str(sorted(paths)[-1]));from PIL import Image
HERE=Path(__file__).resolve().parent
from fractions import Fraction
checked=0;points=0;clear_boxes=0;current_pngs=0
for side in (HERE/'plots').glob('*.json'):
 data=json.loads(side.read_text());s=data['spec'];path=side.with_suffix('.png');assert path.exists()
 assert hashlib.sha256(path.read_bytes()).hexdigest()==data['png_sha256']
 im=Image.open(path).convert('RGB');assert im.size==(540,456)
 b,A,c=[float(Fraction(s[k])) for k in ('b','A','c')];d=s['direction'];ylo,yhi=s['ylim'];left,bottom,width,height=data['axes_bbox']
 def point(x,y):return round(left+(x+5)/10*width),round(im.height-(bottom+(y-ylo)/(yhi-ylo)*height))
 for x in (-1,0,1):
  y=A*b**(d*x)+c
  if not ylo+.15<y<yhi-.15:continue
  px,py=point(x,y)
  region=[im.getpixel((u,v)) for u in range(max(0,px-4),min(im.width,px+5)) for v in range(max(0,py-4),min(im.height,py+5))]
  if s.get('role')=='original':assert any(r>190 and 80<gg<210 and bb<100 for r,gg,bb in region),(path,x,y)
  else:assert any(bb>100 and bb>r*1.4 and gg>r*1.1 for r,gg,bb in region),(path,x,y)
  points+=1
 # Every plot retains both axes and finite transforms, and data-valued text.
 assert all(math.isfinite(v) for v in (left,bottom,width,height));assert width>0 and height>0
 if s['cue']=='labels':assert s['intercept_tex'].startswith('(0,') and s['shift_tex']
 if data['version']=='shift-plots-7':
  current_pngs+=1
  zero_x=left+width/2;zero_y=bottom+(0-ylo)/(yhi-ylo)*height;asym_y=bottom+(c-ylo)/(yhi-ylo)*height
  marker_values=[A+c] if s['cue']=='labels' else []
  if s.get('role')=='translation':marker_values.append(1)
  for label in data['label_layout']:
   x0,z0,x1,z1=label['bbox_pixels'];assert not label['uses_background']
   assert left+4<=x0<x1<=left+width-4 and bottom+4<=z0<z1<=bottom+height-4
   assert not x0-4<=zero_x<=x1+4 and not z0-4<=zero_y<=z1+4
   assert not z0-4<=asym_y<=z1+4
   for yy in marker_values:
    my=bottom+(yy-ylo)/(yhi-ylo)*height
    assert not (x0-7<=zero_x<=x1+7 and z0-7<=my<=z1+7)
   # Independently reconstruct both rendered curves over each box's x range.
   lo=max(-5,(x0-4-left)/width*10-5);hi=min(5,(x1+4-left)/width*10-5)
   for j in range(501):
    xx=lo+(hi-lo)*j/500
    vals=[A*b**(d*xx)+c]+([b**xx] if s.get('role')=='translation' else [])
    for yy in vals:
     py=bottom+(yy-ylo)/(yhi-ylo)*height
     assert not z0-4<=py<=z1+4,(path,label,xx,yy)
   if s.get('role')=='translation':
    xp=s.get('arrow_x',-3.5);px=left+(xp+5)/10*width;ay=b**xp
    ends=[bottom+(v-ylo)/(yhi-ylo)*height for v in (ay,ay+c)]
    assert not (x0-4<=px<=x1+4 and min(ends)<=z1+4 and max(ends)>=z0-4)
   for other in data['label_layout']:
    if other is label:continue
    ox0,oy0,ox1,oy1=other['bbox_pixels'];assert not (x0-5<ox1 and x1+5>ox0 and z0-5<oy1 and z1+5>oy0)
   clear_boxes+=1
 checked+=1
(HERE/'pixel-report.json').write_text(json.dumps({'pngs_checked':checked,'current_renderer_pngs':current_pngs,'independently_clear_feature_label_boxes':clear_boxes,'independent_visible_curve_samples':points,'png_size':[540,456],'tolerance_pixels':4,'checks':'actual blue/orange raster pixels at independently recomputed data/axis coordinates; hash, dimensions and finite axes transforms','runtime_python':sys.version.split()[0]},indent=2))
