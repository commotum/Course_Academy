import json,re,hashlib,shutil
from pathlib import Path
from PIL import Image
import numpy as np
D=Path('generate/scratch/17592186068696');D.mkdir(exist_ok=True)
s=json.load(open('generate/runs/current/sources/17592186068696.json'));(D/'source.json').write_text(json.dumps(s,indent=2)+'\n')
# Independently visually read discontinuities and every marked point; y is deliberately
# a pixel location because these rasters have no numbered vertical scale.
info={
'05ad37':(-2,[( -2,136,'open'),(-2,42,'filled')],[-2]),
'21e0c6':(-2,[],[]),'25dbe2':(-2,[(-2,195,'filled'),(1,195,'open'),(1,120,'filled')],[-2,1,3]),
'2d3426':(-2,[(-1,112,'open'),(-1,277,'filled'),(2,165,'open'),(2,198,'filled')],[-1,2]),
'2f5337':(-2,[(-2,180,'open'),(-2,100,'filled')],[-2,2]),
'36cecf':(-1,[(-1,118,'open'),(-1,229,'filled')],[-1]),
'374abc':(-2,[(0,182,'open'),(0,102,'filled')],[-2,0]),
'3c8a19':(1,[(1,174,'open'),(1,105,'filled')],[1]),
'3e494c':(-2,[],[]),'455cdb':(1,[],[1]),
'492341':(-1,[(-1,127,'open'),(-1,238,'filled')],[-1]),'49e7b3':(1,[],[]),
'4c3513':(-2,[(0,197,'open'),(0,117,'filled'),(2,117,'open'),(2,237,'filled')],[0,2]),
'5cebe6':(1,[],[]),'69ad36':(-2,[],[]),
'6d0d3c':(1,[(0,203,'open'),(0,163,'filled'),(1,203,'open'),(1,245,'filled')],[0,1,2.5]),
'701e65':(-3,[],[]),'88b379':(-2,[],[]),
'8ee061':(-2,[(-2,118,'filled'),(-2,238,'open'),(0,78,'open'),(0,198,'filled')],[-2,0]),
'8f88e7':(-1,[],[]),'904f84':(-1,[],[]),'9eb014':(-3,[],[]),
'a3026f':(-3,[],[]),'a9d867':(1,[],[]),'bd662a':(1,[],[]),'c9ba1e':(1,[],[]),
'caa671':(-2,[(-2,130,'open'),(-2,36,'filled')],[-2]),
'd366ad':(1,[],[]),'d4ea3f':(-1,[],[]),'d9185f':(1,[],[]),'db4660':(-1,[],[]),
'deacb7':(-3,[(-3,70,'open'),(-3,245,'filled')],[-3]),
'e111be':(-3,[(-3,151,'open'),(0,151,'filled')],[-3,0]),
'e56e3c':(-3,[],[]),'eb8803':(1,[(1,182,'open'),(1,107,'filled'),(4,145,'open'),(4,107,'filled')],[1,2,4]),
'fc1d42':(1,[(1,174,'open'),(1,105,'filled')],[1])}
paths=sorted(set(re.findall(r'images/[a-z0-9/]+\.png',json.dumps(s))))
plots={}
for p in paths:
 a=np.array(Image.open('/media/jake/SSD/EDB/math/'+p).convert('RGBA'));rgb=a[:,:,:3];alpha=a[:,:,3];black=(rgb.max(2)<100)&(alpha>128)
 x0=int(np.argmax(black.sum(0)));y0=int(np.argmax(black.sum(1)))
 prefix=Path(p).stem[:6];tick,markers,breaks=info[prefix]
 # One-unit tick scale is read from graph labels; x tick positions independently read.
 scales={'05ad37':46.5,'21e0c6':46.5,'25dbe2':37.5,'36cecf':35,'3e494c':46.5,'6d0d3c':68,'701e65':35,'9eb014':35,'a3026f':35,'caa671':46.5,'deacb7':35,'e56e3c':35,'eb8803':37.5,'492341':35}
 scale=scales.get(prefix,40)
 # Source canonical bounds differ; direct label read gives x origin=103 unit=68.
 if prefix=='6d0d3c':x0=103;y0=283
 red=(rgb[:,:,0]>150)&(rgb[:,:,1]<120)&(rgb[:,:,2]<120)&(alpha>128)
 blue=(rgb[:,:,2]>150)&(rgb[:,:,0]<100)&(rgb[:,:,1]<100)&(alpha>128)
 # Refine manually estimated y pixels locally to actual point center: ring/filled
 # patterns use nearby rows at the exact manually read x coordinate.
 refined=[]
 for xx,yy,kind in markers:
  px=round(x0+scale*xx);best=None
  for cy in range(6,len(red)-6):
   patch=(red|blue)[cy-4:cy+5,px-4:px+5]
   center=int(patch[3:6,3:6].sum()); card=sum(bool(patch[dy:dy+2,dx:dx+2].any()) for dy,dx in [(0,3),(7,3),(3,0),(3,7)]); score=int(patch.sum())+5*center if kind=='filled' else int(patch.sum())-10*center+20*card
   if best is None or score>best[0]:best=(score,cy)
  cy=best[1];refined.append({'x':xx,'y_pixel':cy,'kind':kind,'color':'blue' if blue[cy-4:cy+5,px-4:px+5].sum()>red[cy-4:cy+5,px-4:px+5].sum() else 'red'})
  red[max(0,cy-6):cy+7,max(0,px-6):px+7]=False
 # Flood connected curve components, then ordered x-column center samples.
 seen=set();curves=[]
 for py,px in zip(*np.where(red)):
  if (int(py),int(px)) in seen:continue
  todo=[(int(py),int(px))];seen.add(todo[0]);comp=[]
  while todo:
   y,x=todo.pop();comp.append((x,y))
   for dy in (-1,0,1):
    for dx in (-1,0,1):
     ny,nx=y+dy,x+dx
     if 0<=ny<red.shape[0] and 0<=nx<red.shape[1] and red[ny,nx] and (ny,nx) not in seen:seen.add((ny,nx));todo.append((ny,nx))
  if len(comp)<25:continue
  by={}
  for x,y in comp:by.setdefault(x,[]).append(y)
  if len(by)<8:continue
  curves.append([[round((x-x0)/scale,6),round((y0-sum(v)/len(v))/scale,6)] for x,v in sorted(by.items())])
 plots[p]={'source':p,'sha256':hashlib.sha256(Path('/media/jake/SSD/EDB/math/'+p).read_bytes()).hexdigest(),'dimensions':[a.shape[1],a.shape[0]],'origin_pixel':[x0,y0],'pixels_per_x_unit':scale,'markers':refined,'breaks':breaks,'curves':curves,'bounds':[-x0/scale,(a.shape[1]-x0)/scale,(y0-a.shape[0])/scale,y0/scale],'vertical_asymptotes':{'25dbe2':[-2,3],'2f5337':[2],'36cecf':[-1],'374abc':[-2],'455cdb':[1],'492341':[-1],'6d0d3c':[2.5],'eb8803':[2],'e111be':[0]}.get(prefix,[]),'edges':'All red branches solid; no red branch arrowheads. Black positive x/y axis arrowheads. No inclusion implied at cropped edges. Unmarked joins/corners remain connected.'}
(D/'plot-spec.json').write_text(json.dumps(plots,indent=2)+'\n')
print('wrote',len(plots),'plots')
