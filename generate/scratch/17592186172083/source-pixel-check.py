"""Independent raster endpoint/tail proximity check; never infer exact intent."""
import json,sys,math
from pathlib import Path
cache=Path('/home/jake/.cache/uv/wheels-v5/pypi/pillow');paths=[p for p in cache.iterdir() if p.is_dir() and 'cp310' in p.name and 'manylinux' in p.name];sys.path.insert(0,str(sorted(paths)[-1]))
from PIL import Image
H=Path(__file__).resolve().parent;maps=json.loads((H/'source-bank-maps.json').read_text());results=[]
for item in maps:
 if item['legacy_duplicate']:continue
 path=Path('/media/jake/SSD/EDB/math')/item['source_path'];im=Image.open(path).convert('RGBA');orange=set();blue=[]
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,a=im.getpixel((x,y))
   if not a:continue
   if r>180 and 80<g<200 and b<80:orange.add((x,y))
   if r<100 and 70<g<180 and b>120:blue.append((x,y))
 centers=[]
 while orange:
  first=orange.pop();stack=[first];cluster=[first]
  while stack:
   x,y=stack.pop()
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    z=(x+dx,y+dy)
    if z in orange:orange.remove(z);stack.append(z);cluster.append(z)
  if len(cluster)>10:centers.append((sum(x for x,y in cluster)/len(cluster),sum(y for x,y in cluster)/len(cluster)))
 assert len(centers)==3,(item['source_id'],centers)
 pts=sorted(item['points']);centers.sort();sx=(centers[-1][0]-centers[0][0])/(pts[-1][0]-pts[0][0]);ox=centers[0][0]-sx*pts[0][0]
 oy=sum(py+sx*y for (x,y),(px,py) in zip(pts,centers))/3
 assert max(abs(px-(ox+sx*x))+abs(py-(oy-sx*y)) for (x,y),(px,py) in zip(pts,centers))<2
 endpoints=[];covered=[]
 for (x,y),(u,v) in zip(item['points'],item['extracted_vectors']):
  def num(z):
   if isinstance(z,str) and '/' in z:
    a,b=z.split('/');return float(a)/float(b)
   return float(z)
  target=(ox+sx*(x+num(u)),oy-sx*(y+num(v)))
  distance=min(math.dist(target,z) for z in blue);endpoints.append(round(distance,3));covered.append(min(math.dist(target,z) for z in centers)<2)
 results.append({'source_id':item['source_id'],'source_path':item['source_path'],'endpoint_nearest_blue_pixel_distances':endpoints,'precision_limit':item['precision_limit'],'endpoint_covered_by_tail_marker':covered})
(H/'source-pixel-check.json').write_text(json.dumps({'method':'Fit unit coordinate transform from three orange tails; compare computed arrow tips with blue raster pixels. This is a proximity check, not an exact unlabelled coordinate recovery or proof of endpoint extremum.','max_tolerance_pixels':5,'covered_tail_marker_tolerance_pixels':7,'results':results},indent=2)+'\n')
for r in results:
 if any(d>5 and not(c and d<=7) for d,c in zip(r['endpoint_nearest_blue_pixel_distances'],r['endpoint_covered_by_tail_marker'])):print(r)
assert all(all(d<=5 or c and d<=7 for d,c in zip(r['endpoint_nearest_blue_pixel_distances'],r['endpoint_covered_by_tail_marker'])) for r in results)
print('PASS',len(results),'original plots /',3*len(results),'tail-derived endpoint proximity checks')
