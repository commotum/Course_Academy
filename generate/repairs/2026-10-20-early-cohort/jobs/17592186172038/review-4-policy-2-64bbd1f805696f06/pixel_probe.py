import json,pathlib,re,math,collections
import numpy as np
from PIL import Image
from audit import parse_rhs
ROOT=pathlib.Path.cwd();JOB=ROOT.parent
save=lambda n,x:(ROOT/n).write_text(json.dumps(x,indent=2)+'\n')
def geometry(path,points,style,exclude_axis=False):
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
 for point_index,(cx,cy) in enumerate(centers):
  if exclude_axis and style=="generated" and (float(points[point_index][0])==0 or float(points[point_index][1])==0):
   out.append({"angle_degrees":None,"status":"axis overlaps segment/tick labels; raster PCA not applicable"});continue
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

def main():
 inv=json.load(open(JOB/'source/inventory.json'));src=json.load(open('source-analysis.json'));scases={v['id']:v for v in src['source_cases']};rows=[];affected=[]
 for q in inv['questions']:
  sourceid=q.get(':question/math-academy-id');style='source' if sourceid else 'generated';f=q[':question/answer-fields'][0]
  if sourceid:points=scases[sourceid]['points']
  else:
   opening=q[':question/worked-solution'].split('\n\n')[0];pts=re.findall(r'\$([^$]+)\$',opening);points=[list(parse_rhs('='+t)) for t in pts]
  choices=[]
  try:
   for a in f[':answer-field/choices']:
    geom=geometry(pathlib.Path('/media/jake/SSD/EDB/math')/a[':answer/value'],points,style);choices.append({'id':a[':answer/id'],'asset':a[':answer/value'],'geometry':geom})
  except Exception as e:
   rows.append({'id':q[':question/id'],'entity':q[':db/id'],'source_id':sourceid,'status':'unresolved pixel geometry','error':str(e)});continue
  def distance(a,b):
   d=abs(a-b);return min(d,180-d)
  pairs=[(i,j) for i in range(5) for j in range(i) if all(distance(a['angle_degrees'],-b['angle_degrees'])<2.5 for a,b in zip(choices[i]['geometry'],choices[j]['geometry']))]
  corr=f.get(':answer-field/correct');cid=(corr.get(':answer/id') if isinstance(corr,dict) else corr[1]) if corr else None
  result={'id':q[':question/id'],'entity':q[':db/id'],'source_id':sourceid,'style':style,'points':[[str(x),str(y)] for x,y in points],'choices':choices,'pairs':pairs,'correct':cid,'status':'no unique mirror pair'}
  if len(pairs)==1:
   pair=pairs[0];scores={i:sum(a['sign']==b['sign'] and a['sign']!=0 for j in range(5) if j not in pair for a,b in zip(choices[i]['geometry'],choices[j]['geometry'])) for i in pair};wins=[i for i in pair if scores[i]==max(scores.values())];result['scores']=scores
   if len(wins)==1:
    idx=wins[0];result['predicted_id']=choices[idx]['id'];result['correct_prediction']=cid==choices[idx]['id'];result['status']='prediction checked' if cid else 'key absent'
    if result['correct_prediction']:
     affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Equation-free mirror-pair / direction-consensus strategy selects the stored correct image.','reproduction':f'Run .venv/bin/python pixel_probe.py; inventory basis {inv["basis"]}; row entity {q[":db/id"]}; pair positions {[i+1 for i in pair]}, scores {scores}, selected position {idx+1}. Original canonical image geometry is measured from PNG pixels, no generator metadata.','has_math_academy_source_id':bool(sourceid),'math_academy_source_id':sourceid})
   else:result['status']='consensus tied'
  if cid:
   ci=next(i for i,a in enumerate(choices) if a['id']==cid);expr=parse_rhs(q[':question/problem']);expected=[float(expr.subs({'x':x,'y':y})) for x,y in points];result['correct_image_angle_error_degrees']=[distance(a['angle_degrees'],math.degrees(math.atan(m))) for a,m in zip(choices[ci]['geometry'],expected)]
  rows.append(result)
 save('inventory-pixel-results.json',{'basis':inv['basis'],'method':'PCA of dark segment pixels outside the central point marker; fixed 2.5 degree mirror tolerance; equations used only after predictions to verify the stored key image','records':rows});save('affected-inventory.json',{'affected_questions':affected});print('inventory tested',len(rows),'affected',len(affected),'states',dict(collections.Counter(r['status'] for r in rows)));print('max correct-image error',max((max(r.get('correct_image_angle_error_degrees',[0])) for r in rows),default=0))
if __name__=='__main__':main()
