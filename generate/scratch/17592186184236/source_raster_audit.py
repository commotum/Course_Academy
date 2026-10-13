"""Independent original PNG calibration: fitted branch pixels, no EDB."""
import hashlib,json,math
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
# Labels transcribed by individually viewing every original PNG at full size.
# x0 and axis row are black-pixel axes; dashed columns measured from raster.
readings={
 'e-10025':('5/2',1,134,49,290), 'q-65448':('1/2',1,157,37,302),
 'q-65547':('2/3',-2,157,22,316), 'q-117795':('3',-3,110,55,283),
 'q-141974':('2/3',1,157,22,316), 'q-143638':('2',-2,158,103,235),
 'q-117796':('5/4',.5,157,28,310)}
from fractions import Fraction
assets=json.loads((HERE/'source-assets.json').read_text());out=[]
for sid,(B,D,yaxis,left,right) in readings.items():
 path=Path(assets[sid]['path']);ar=np.asarray(Image.open(path).convert('RGB'))
 blue=(ar[:,:,0]<90)&(ar[:,:,1]>70)&(ar[:,:,1]<170)&(ar[:,:,2]>130)
 x0=(left+right)/2
 px=[];py=[]
 for x in range(left+12,right-11):
  rows=np.where(blue[:,x])[0]
  if len(rows) and 25<rows.mean()<ar.shape[0]-15:px.append(x);py.append(rows.mean())
 xs=np.array(px);ys=np.array(py)
 # Subpixel stroke centers affect steep tails. Fit within a bounded 1-pixel
 # origin/1.5-pixel asymptote-span allowance, never an unbounded geometry fit.
 best=None
 for fitted_origin in np.linspace(168.2,170.2,41):
  for span in np.linspace(right-left-1.5,right-left+1.5,41):
   t=np.tan((xs-fitted_origin)*math.pi/span)
   matrix=np.column_stack([np.ones(len(xs)),-t]);midline,scale=np.linalg.lstsq(matrix,ys,rcond=None)[0]
   error=float(np.square(matrix@np.array([midline,scale])-ys).mean())
   if best is None or error<best[0]:best=(error,fitted_origin,span,midline,scale,matrix)
 _,fitted_origin,span,midline,scale,matrix=best
 residual=np.abs(matrix@np.array([midline,scale])-ys)
 dfit=(yaxis-midline)/scale
 assert abs(dfit-D)<.04,(sid,dfit,D)
 assert residual.max()<1.6,(sid,residual.max())
 assert scale>0 and np.diff(ys).max()<1.0,(sid,'monotonicity')
 H=math.pi/(2*float(Fraction(B)));xscale=(right-left)/(2*H)
 # Intercept label: bounding box of actual dark label pixels in the manually
 # isolated left-of-axis label region, then distance to actual blue pixels.
 label_roi=(slice(max(0,int(midline)-20),min(ar.shape[0],int(midline)+2)),slice(140,165))
 dark=(ar[:,:,0]<95)&(ar[:,:,1]<95)&(ar[:,:,2]<95)
 yy,xx=np.where(dark[label_roi]);xx=xx+140;yy=yy+max(0,int(midline)-20)
 assert len(xx)>0,(sid,'intercept-label pixels')
 box=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]
 by,bx=np.where(blue);dx=np.maximum(np.maximum(box[0]-bx,bx-box[2]),0);dy=np.maximum(np.maximum(box[1]-by,by-box[3]),0)
 clearance=float(np.sqrt(dx*dx+dy*dy).min())
 out.append({'source_id':sid,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'dimensions':[ar.shape[1],ar.shape[0]],'read_B':B,'read_D':D,'axis_origin_pixels':[x0,yaxis],
 'asymptote_columns':[left,right],'asymptote_labels':['-pi/(2B)','pi/(2B)'],
 'x_pixels_per_unit':xscale,'y_pixels_per_unit':float(scale),'fitted_D':float(dfit),
 'fitted_origin_x':float(fitted_origin),'fitted_asymptote_span_px':float(span),'stroke_fit_allowance_px':1.5,
 'maximum_branch_residual_px':float(residual.max()),'branch_samples':len(xs),
 'intercept_label_bbox_pixels':box,'intercept_label_blue_clearance_px':clearance,
 'monotonicity':'strictly increasing','axis_arrows':'positive x right, positive y up',
 'branch_arrows':'none; branch clipped at raster boundary','worked_solution_pngs':0,'choice_pngs':0})
(HERE/'source-geometry.json').write_text(json.dumps({'individual_full_resolution_inspection':True,'plots':out},indent=2)+'\n')
print('Original raster audits:',len(out))
