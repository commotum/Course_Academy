"""Independent PNG coordinate-to-axis extraction for generated point placement."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
D=Path(__file__).resolve().parent
rows=[]
for side in sorted((D/'plots').glob('*.json')):
 s=json.loads(side.read_text());a=np.array(Image.open(side.with_suffix('.png')).convert('RGB'));blue=(a[:,:,2].astype(int)>a[:,:,0].astype(int)+20)&(a[:,:,2].astype(int)>a[:,:,1].astype(int)+15)&(a[:,:,0]<160);yy,xx=np.where(blue);cx=(int(xx.min())+int(xx.max()))/2;cy=(int(yy.min())+int(yy.max()))/2;rx=(int(xx.max())-int(xx.min()))/2;ry=(int(yy.max())-int(yy.min()))/2
 b,r=s['p']['b'],s['p']['r'];k=math.sqrt(r)/b;m=math.sqrt(1-k*k);x,y=(m,k) if s['axis']=='y' else (k,m);ex=cx+rx*x;ey=cy-ry*y;crop=a[round(ey)-5:round(ey)+6,round(ex)-5:round(ex)+6];assert (crop.max(axis=2)<100).sum()>3,(side,s)
 assert abs(rx-ry)<=2,'Equal axes scale failed'
 rows.append({'path':str(side.with_suffix('.png')),'derived_from_coordinate':s['p'],'independent_expected_point':[x,y],'native_raster_circle_center':[cx,cy],'native_raster_radius':[rx,ry],'black_pixels_in_5px_point_window':int((crop.max(axis=2)<100).sum()),'passed':True})
(D/'generated-raster-geometry.json').write_text(json.dumps(rows,indent=2)+'\n');print('Independent generated raster geometry:',len(rows),'passed')
