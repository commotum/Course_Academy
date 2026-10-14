from pathlib import Path
import json,re,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).parent
S=json.load(open(P/'source.json'))['record']
# Independently transcribed visible asymptotes and marked coordinates, in original option order.
banks=[
[[-1,-1,0],[2,-1,0],[-2,1,0],[-2,-1,0],[-1,1,0]],
[[-.5,0,1],[-1,0,1],[-.5,1,0],[.5,0,1],[.5,1,0]],
[[.8,0,3],[-.8,0,3],[.8,0,0],[-.8,0,0],[4,-3,0]],
[[-1,2,0],[2,2,0],[-2,2,0],[2,-2,0],[-2,-2,0]],
[[2.5,-2,0],[-2.5,0,2],[2.5,0,2],[-2.5,0,-2],[2.5,0,-2]],
[[.25,0,1],[-.25,0,-1],[.25,0,-1],[1,0,-1],[-.25,0,1]],
[[-2,1,0],[2,-1,0],[-2,-1,0],[2,1,0],[1,1,0]],
[[-5,0,2],[5,-2,0],[-5,-2,0],[-5,0,0],[-5,0,-2]],
[[.75,-1,0],[-.75,-1,0],[.75,1,0],[1,1,0],[-.75,1,0]],
[[1,-1,0],[-.5,-1,0],[.5,1,0],[.5,-1,0],[-.5,1,0]]]
params=[{'a':'-2','h':-1,'k':0},{'a':'-1/2','h':0,'k':1},{'a':'4/5','h':0,'k':3},{'a':'-2','h':2,'k':0},{'a':'5/2','h':0,'k':-2},{'a':'1/4','h':0,'k':-1},{'a':'2','h':1,'k':0},{'a':'-5','h':0,'k':2},{'a':'3/4','h':1,'k':0},{'a':'1/2','h':-1,'k':0}]
# Exact rational tokens are normalized from explicitly visible terminating decimals.
from fractions import Fraction
rat=lambda x:str(Fraction(str(x)))
assets={}; cases=[]
def analyze(path,triple,dist=1):
 f=Path('/media/jake/SSD/EDB/math')/path
 im=Image.open(f).convert('RGBA');white=Image.new('RGBA',im.size,'white');white.alpha_composite(im);rgb=np.asarray(white.convert('RGB'))
 dark=(rgb[:,:,:3].max(2)<100); x0=int(np.argmax(dark.sum(0)));y0=int(np.argmax(dark.sum(1)))
 blue=(rgb[:,:,0]<100)&(rgb[:,:,1]>80)&(rgb[:,:,2]>140)&(rgb[:,:,2]>rgb[:,:,1]*1.15)
 # Dense circular source marker centers: isolated connected pixels of the 5x5 density mask.
 pad=np.pad(blue,3);density=sum(pad[dy:dy+blue.shape[0],dx:dx+blue.shape[1]] for dy in range(7) for dx in range(7))
 mask=density>=24;seen=set();centers=[]
 for y,x in zip(*np.where(mask)):
  if (y,x) in seen:continue
  queue=[(y,x)];seen.add((y,x));comp=[]
  while queue:
   yy,xx=queue.pop();comp.append((yy,xx))
   for yy2,xx2 in [(yy+1,xx),(yy-1,xx),(yy,xx+1),(yy,xx-1)]:
    if 0<=yy2<mask.shape[0] and 0<=xx2<mask.shape[1] and mask[yy2,xx2] and (yy2,xx2) not in seen:seen.add((yy2,xx2));queue.append((yy2,xx2))
  centers.append([float(np.mean([c[1] for c in comp])),float(np.mean([c[0] for c in comp]))])
 centers.sort();a,h,k=map(float,triple);points=[[h-dist,k-a/dist],[h+dist,k+a/dist]]
 if len(centers)!=2:raise ValueError((path,centers))
 sx=(centers[1][0]-centers[0][0])/(2*dist);sy=abs((centers[1][1]-centers[0][1])/(2*a/dist))
 ox=sum(px-sx*x for (px,py),(x,y) in zip(centers,points))/2;oy=sum(py+sy*y for (px,py),(x,y) in zip(centers,points))/2
 if path.startswith('images/50/'):
  ox=float(x0);oy=float(y0);sx=(x0-169.5)/3;sy=abs(centers[1][1]-centers[0][1])/10
 if abs(ox-x0)>2 or abs(oy-y0)>2:raise ValueError((path,'axis disagreement',ox,x0,oy,y0))
 # Every blue curve pixel is checked against the reciprocal relation in its own axes calibration.
 ys,xs=np.where(blue);xx=(xs-ox)/sx;yy=(oy-ys)/sy;safe=abs(xx-h)>.15
 residual=abs((xx[safe]-h)*(yy[safe]-k)-a)/np.sqrt(((yy[safe]-k)/sx)**2+((xx[safe]-h)/sy)**2)
 return {'asset':path,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'coefficient_status':'illustrative_model_not_uniquely_recovered' if path.startswith('images/50/') else 'determined_within_reciprocal_family_from_coherent_visible_points','eligible_for_symbolic_source_equivalence':not path.startswith('images/50/'),'native_size':list(im.size),'a':rat(triple[0]),'h':rat(triple[1]),'k':rat(triple[2]),'marked_points':[[rat(x),rat(y)] for x,y in points],'pixel_marker_centers':centers,'origin_px':[ox,oy],'axis_black_px':[x0,y0],'units_px':[sx,sy],'visible_bounds':[(0-ox)/sx,(340-ox)/sx,(oy-303)/sy,(oy-22)/sy],'curve_residual_px_p95':float(np.quantile(residual,.95)),'printed_points':[['-2.2','3'],['-3.8','-7']] if path.startswith('images/50/') else [[rat(x),rat(y)] for x,y in points],'anomaly': 'inconsistent printed y labels; model coefficient 4 and y-scale are not uniquely recoverable' if path.startswith('images/50/') else None,'branch_signs_relative_to_horizontal':[-int(np.sign(a)),int(np.sign(a))],'vertical_limit_left':'infinity' if a<0 else '-infinity','vertical_limit_right':'infinity' if a>0 else '-infinity'}
for i,q in enumerate(S[':knowledge-point/questions']):
 profile=q[':question/math-academy-id'];field=q[':question/answer-fields'][0]
 for j,(ans,triple) in enumerate(zip(field[':answer-field/choices'],banks[i])):
  dist=.8 if i==2 and j==4 else .5 if i==4 and j==0 else 1
  assets[ans[':answer/value']]=analyze(ans[':answer/value'],triple,dist)
 level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/hard' if params[i]['h'] else ':question.difficulty/moderate').split('/')[-1]
 cases.append({'source_id':q[':db/id'],'source_math_academy_id':profile,'template':'horizontal_then_scale' if params[i]['h'] else 'scale_then_vertical','level':level,'parameters':params[i],'bank_profile':'raw:'+profile,'authored_level_assignment':':question/difficulty' not in q})
# Solution assets reuse image specs if available. Additional stages transcribed from full raster inspection.
extra={'027b68':(.25,0,0),'049f9c':(1,-1,0),'207dec':(-2,2,0),'3c8dd0':(-1,2,0),'461293':(-5,0,0),'8ce8c5':(-1,1,0),'8f2a42':(1,1,0),'9da0db':(-1,0,0),'a32495':(1,0,0),'c9b708':(-2,1,0),'e100b5':(-2,1,-1),'e80865':(1,0,0)}
for q in S[':knowledge-point/questions']+[S[':knowledge-point/canonical-example']]:
 for path in re.findall(r'!\[\]\((.*?)\)',q.get(':question/worked-solution','')):
  if path in assets:continue
  match=[t for prefix,t in extra.items() if path.split('/')[-1].startswith(prefix)]
  if len(match)!=1:raise ValueError(path)
  assets[path]=analyze(path,match[0])
(P/'plot-extraction.json').write_text(json.dumps(assets,indent=2));(P/'source-cases.json').write_text(json.dumps(cases,indent=2))
print('assets',len(assets),'cases',len(cases),'maximum p95 curve residual',max(a['curve_residual_px_p95'] for a in assets.values()))
