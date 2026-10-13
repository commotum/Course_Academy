import json,re,math,importlib.util
from pathlib import Path
from PIL import Image
R=Path('/home/jake/Developer/Course_Academy/generate/runs/current');sp=importlib.util.spec_from_file_location('qa',R/'qa-function-of-y-evaluation.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
D=Path('/home/jake/Developer/Course_Academy/generate/scratch/17592186179718');count=0
for rec in json.load(open(D/'review.json')):
 for name in re.findall(r'!\[.*?\]\((.*?)\)',rec['question'][':question/problem']):
  path=Path(name)
  if '17592186179718/plots' not in name:continue
  F,g,(a,b),*_=p.p.prompt(rec['question'][':question/problem']);im=Image.open(path).convert('RGB');w,h=im.size;rgb=im.load();black=lambda x,y:max(rgb[x,y])<85
  oy=max(range(h),key=lambda y:sum(black(x,y) for x in range(w)));ox=max(range(w),key=lambda x:sum(black(x,y) for y in range(h)))
  blue={(x,y) for x in range(w) for y in range(h) if rgb[x,y][2]>110 and rgb[x,y][2]-rgb[x,y][0]>65 and rgb[x,y][1]>70};groups=[]
  while blue:
   start=blue.pop();stack=[start];component=[start]
   while stack:
    x,y=stack.pop()
    for dx,dy in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)):
     point=(x+dx,y+dy)
     if point in blue:blue.remove(point);stack.append(point);component.append(point)
   groups.append(component)
  points=max(groups,key=len);xa,xb=[float(g.subs(p.t,z)) for z in (a,b)];ya,yb=float(a),float(b)
  xp=[q[0] for q in points];yp=[q[1] for q in points];scales=[]
  for c,v in ((min(xp)-ox,min(xa,xb)),(max(xp)-ox,max(xa,xb)),(oy-min(yp),yb),(oy-max(yp),ya)):
   if abs(v)>.1:scales.append(c/v)
  scale=sorted(scales)[len(scales)//2];assert scale>0
  worst=0
  for i in range(121):
   y=ya+(yb-ya)*i/120;x=float(g.subs(p.t,y));px,py=ox+scale*x,oy-scale*y;dist=min(math.hypot(px-qx,py-qy) for qx,qy in points);worst=max(worst,dist)
  assert worst<7,(name,worst,scales,ox,oy)
  count+=1
print('raster geometric checks',count)
(R/'qa/17592186179718-raster.json').write_text(json.dumps({'actual_blue_curve_geometry':count,'independent_pixel_axes':True,'all_curve_sample_pixel_distances_below':7},indent=2)+'\n')
