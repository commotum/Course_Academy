"""Targeted native-resolution review: hard seed1 and lowest supported y coordinate."""
import sys;sys.dont_write_bytecode=True
from pathlib import Path
import types,json,math,hashlib
from PIL import Image,ImageDraw
import numpy as np
D=Path(__file__).resolve().parent;g=types.ModuleType('g');g.__file__=str(D.with_suffix('.py'));exec(compile(D.with_suffix('.py').read_text(),g.__file__,'exec'),g.__dict__)
records=[('hard seed1',g.generate('hard',1)),('readable .14 boundary',g.generate('moderate',0,template='q-124750',parameters={'b':10,'r':2},profile='method-sign')),('low-angle hard',g.generate('hard',0,template='q-65062',parameters={'b':15,'r':8},profile='method-sign'))]
rows=[];pictures=[]
for label,rec in records:
 for role,a in rec['generation']['assets'].items():
  assert a['renderer_revision']==g.RENDERER_REVISION
  point=list(map(float,map(g.sp.sympify,a['point'])));pos=a['theta_label']['position'];angle=math.degrees(math.atan2(point[1],point[0]));distance=abs(point[0]*pos[1]-point[1]*pos[0])
  image=Image.open(a['path']).convert('RGB');pix=np.array(image);blue=(pix[:,:,2].astype(int)>pix[:,:,0].astype(int)+20)&(pix[:,:,2].astype(int)>pix[:,:,1].astype(int)+15)&(pix[:,:,0]<160);yy,xx=np.where(blue);rad=(xx.max()-xx.min())/2
  if angle<25:assert distance*rad>=11,(label,role,distance*rad)
  assert a['theta_label']['centered'] and a['theta_label']['white_backing']
  rows.append({'case':label,'role':role,'angle_degrees':angle,'theta_center_distance_from_ray_pixels':float(distance*rad),'path':a['path'],'png_sha256':a['sha256'],'renderer_revision':g.RENDERER_REVISION,'native_visual_review':'pending'})
  pictures.append((label+' '+role,image))
w=max(im.width for _,im in pictures);h=max(im.height for _,im in pictures)+25;out=Image.new('RGB',(w*2,h*3),'white');dr=ImageDraw.Draw(out)
for i,(label,im) in enumerate(pictures):x=i%2*w;y=i//2*h;out.paste(im,(x,y+25));dr.text((x+8,y+7),label,fill='black')
out.save(D/'theta-label-native-review.png');(D/'theta-label-review.json').write_text(json.dumps({'records':rows,'generated_records':[r for _,r in records]},indent=2)+'\n');print('Theta placement pixel-clearance checks:',len(rows),'passed')
