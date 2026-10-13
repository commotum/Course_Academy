"""Read-only extraction of captured raster slope segments, never image editing."""
import sys,json,pathlib
sys.path[:0]=['/home/jake/.cache/uv/archive-v0/4-AemGpMwlNQVMB0M4sW_','/home/jake/.cache/uv/archive-v0/ZFeU_a5Ava2NGErTmJIZm']
from PIL import Image
import numpy as np
H=pathlib.Path(__file__).resolve().parent
s=json.loads((H/'source.json').read_text())['record']; vals={a[':answer/value'] for q in s[':knowledge-point/questions'] for a in q[':question/answer-fields'][0][':answer-field/choices']}
result={}
for v in sorted(vals):
 im=Image.open('/media/jake/SSD/EDB/math/'+v).convert('RGBA');a=np.array(im).astype(float);rgb=a[:,:,:3]*(a[:,:,3:]/255)+255*(1-a[:,:,3:]/255)
 dark=rgb.min(2)<100; left=int(dark.sum(0).argmax());bottom=int(dark.sum(1).argmax()); right=im.width-3; top=max(1,bottom-280)
 mask=(rgb.min(2)<230)&(rgb.min(2)>90);mask[:top+2]=False;mask[bottom-2:]=False;mask[:,:left+3]=False;mask[:,right-2:]=False
 seen=set(); comps=[]
 for yy,xx in zip(*np.where(mask)):
  if (yy,xx) in seen:continue
  todo=[(yy,xx)];seen.add((yy,xx));p=[]
  while todo:
   y,x=todo.pop();p.append((x,y))
   for dy in [-1,0,1]:
    for dx in [-1,0,1]:
     q=(y+dy,x+dx)
     if 0<=q[0]<mask.shape[0] and 0<=q[1]<mask.shape[1] and mask[q] and q not in seen:seen.add(q);todo.append(q)
  if len(p)<4 or len(p)>160:continue
  p=np.array(p);mu=p.mean(0);cov=np.cov(p.T);ev,evec=np.linalg.eigh(cov);vec=evec[:,ev.argmax()];
  if vec[0]<0:vec=-vec
  u=(mu[0]-left)/(right-left);w=(bottom-mu[1])/(bottom-top)
  slope=-(vec[1]/max(vec[0],1e-9))*(right-left)/(bottom-top)
  if .015<u<.985 and .015<w<.985:comps.append([round(u,6),round(w,6),round(float(slope),6)])
 result[v]={'pixel_bounds':[left,right,top,bottom],'image_size':list(im.size),'segments_normalized':comps,'source_sha256':__import__('hashlib').sha256(pathlib.Path('/media/jake/SSD/EDB/math/'+v).read_bytes()).hexdigest()}
(H/'source-geometry.json').write_text(json.dumps(result,indent=2)+'\n')
print('Extracted',len(result),'plots;',min(len(v['segments_normalized']) for v in result.values()),'minimum segments')
