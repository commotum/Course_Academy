"""Retained reviewer pixel extraction; only equation-parser import adapted.
Source: review-3-policy-2-b6fc68f59ef8c5ba/pixel_probe.py geometry().
"""
import json,pathlib,re,math,collections
import numpy as np
from PIL import Image
from verify_record import latex
parse_rhs=lambda text:latex(text.split("=",1)[1].rstrip("$?"))
ROOT=pathlib.Path.cwd();JOB=ROOT.parent
save=lambda n,x:(ROOT/n).write_text(json.dumps(x,indent=2)+'\n')
def geometry(path,points,style):
 im=np.asarray(Image.open(path).convert('RGB'));gray=im.min(axis=2);h,w=gray.shape
 if style=='generated':
  xs=[0]+[float(x) for x,y in points];ys=[0]+[float(y) for x,y in points];xmin=min(xs)-1;xmax=max(xs)+1;ymin=min(ys)-1;ymax=max(ys)+1
  unit=.83*w/max(xmax-xmin,ymax-ymin);left=.08*w+(.83*w-unit*(xmax-xmin))/2;top=.09*h+(.83*h-unit*(ymax-ymin))/2
  centers=[(left+(float(x)-xmin)*unit,top+(ymax-float(y))*unit) for x,y in points]
 else:
  dark=gray<100;axisx=int(np.argmax(dark.sum(axis=0)));axisy=int(np.argmax(dark.sum(axis=1)))
  light=(gray>=180)&(gray<=230);cols=np.flatnonzero(light.sum(axis=0)>h*.4);rows=np.flatnonzero(light.sum(axis=1)>w*.4)
  def peaks(vals):
   groups=[]
   for v in vals:
    if not groups or v-groups[-1][-1]>2:groups.append([int(v)])
    else:groups[-1].append(int(v))
   return [sum(g)/len(g) for g in groups]
  cp=peaks(cols);rp=peaks(rows);dist=[b-a for a,b in zip(cp,cp[1:])]+[b-a for a,b in zip(rp,rp[1:])];unit=float(np.median(dist));centers=[(axisx+float(x)*unit,axisy-float(y)*unit) for x,y in points]
 out=[]
 for cx,cy in centers:
  # Restrict to the short drawn segment away from its central dot.
  yy,xx=np.indices(gray.shape);dx=xx-cx;dy=yy-cy;rad=np.sqrt(dx*dx+dy*dy);mask=(gray>= (0 if style=='source' else 30))&(gray<75)&(rad>max(5,unit*.105))&(rad<unit*.32)
  if style=='source':
   dark_pixels=gray<75
   dil=dark_pixels.copy()
   for offy in (-2,-1,0,1,2):
    for offx in (-2,-1,0,1,2):dil |= np.roll(np.roll(dark_pixels,offy,axis=0),offx,axis=1)
   reflx=np.clip(np.rint(2*cx-xx).astype(int),0,w-1);refly=np.clip(np.rint(2*cy-yy).astype(int),0,h-1)
   mask=mask & (np.abs(xx-axisx)>2) & (np.abs(yy-axisy)>2) & dil[refly,reflx]
  xx1=dx[mask];yy1=dy[mask]
  if len(xx1)<4:
   if style=='source' and (abs(cx-axisx)<2 or abs(cy-axisy)<2):
    angle=90 if abs(cx-axisx)<2 else 0;out.append({'angle_degrees':angle,'sign':0 if angle==0 else 1,'pixels':int(len(xx1)),'axis_ratio':None,'on_axis_inference':True});continue
   raise ValueError(('insufficient pixels',str(path),cx,cy,unit,len(xx1)))
  arr=np.array([xx1,-yy1]);cov=arr@arr.T;values,vec=np.linalg.eigh(cov);vx,vy=vec[:,np.argmax(values)];angle=math.atan2(vy,vx)
  while angle>math.pi/2:angle-=math.pi
  while angle<=-math.pi/2:angle+=math.pi
  # Zero is excluded from sign counting; exact horizontal geometry should be close.
  sign=0 if abs(angle)<math.radians(2) else (1 if angle>0 else -1)
  out.append({'angle_degrees':math.degrees(angle),'sign':sign,'pixels':int(len(xx1)),'axis_ratio':float(max(values)/max(min(values),1e-9))})
 return out
