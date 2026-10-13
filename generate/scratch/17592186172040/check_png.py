"""Independently read rendered PNG line slopes, not generator point metadata."""
import sys,json,math,pathlib
P=json.load(open(pathlib.Path(__file__).resolve().parent/'render-provenance.json'));sys.path[:0]=list(P['dependency_paths'].values())
from PIL import Image
import numpy as np

def inspect(path,bounds):
 a=np.array(Image.open(path).convert('RGB'));gray=a.min(2);black=gray<130
 cols=np.where(black.sum(0)>170)[0];rows=np.where(black.sum(1)>170)[0]
 if len(cols)<2 or len(rows)<2:raise ValueError('Cannot locate axes '+path)
 left,right=int(cols[0]),int(cols[-1]);top,bottom=int(rows[0]),int(rows[-1])
 mask=(gray>132)&(gray<165);mask[:top+3]=False;mask[bottom-3:]=False;mask[:,:left+3]=False;mask[:,right-3:]=False
 seen=set();points=[];x0,x1,y0,y1=bounds
 for yy,xx in zip(*np.where(mask)):
  if (yy,xx) in seen:continue
  todo=[(yy,xx)];seen.add((yy,xx));p=[]
  while todo:
   y,x=todo.pop();p.append((x,y))
   for dy in [-1,0,1]:
    for dx in [-1,0,1]:
     t=(y+dy,x+dx)
     if 0<=t[0]<mask.shape[0] and 0<=t[1]<mask.shape[1] and mask[t] and t not in seen:seen.add(t);todo.append(t)
  if len(p)<6 or len(p)>100:continue
  p=np.array(p);mu=p.mean(0);ev,vec=np.linalg.eigh(np.cov(p.T));v=vec[:,ev.argmax()]
  if v[0]<0:v=-v
  if v[0]<1e-5:angle=math.copysign(math.pi/2,-v[1])
  else:angle=math.atan(-v[1]/v[0]*(right-left)/(bottom-top)*(y1-y0)/(x1-x0))
  points.append([x0+(x1-x0)*(mu[0]-left)/(right-left),y0+(y1-y0)*(bottom-mu[1])/(bottom-top),angle])
 return {'bounds_pixels':[left,right,top,bottom],'points':points}
if __name__=='__main__':
 records=json.load(open(sys.argv[1]));output={}
 for r in records:
  for path in [a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]+__import__('re').findall(r'!\[\]\((.*?)\)',r['question'][':question/worked-solution']):
   if path.startswith('/'):output[path]=inspect(path,[-2,2,-2,2])
 pathlib.Path(sys.argv[2]).write_text(json.dumps(output)+'\n')
 print('Independently read',len(output),'PNGs')
