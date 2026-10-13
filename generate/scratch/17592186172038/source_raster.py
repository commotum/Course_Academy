"""Independent raster orientation check; source images composited on white."""
exec(open(__file__.replace('source_raster.py','render_plots.py')).read().split('for item in json.load')[0])
import numpy as np
from PIL import Image
s=json.load(open(Path(__file__).parent/'source.json'))['record'];cases=json.load(open(Path(__file__).parent/'source-cases.json'))
byid={c['source_id']:c for c in cases};results=[]
for q in s[':knowledge-point/questions']:
 qid=q[':question/math-academy-id'];points=byid[qid]['parameters']['points']
 for i,c in enumerate(q[':question/answer-fields'][0][':answer-field/choices']):
  im=Image.open(Path('/media/jake/SSD/EDB/math')/c[':answer/value']).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);a=np.asarray(bg.convert('RGB')).mean(2);h,w=a.shape
  # Axes maximize dark-pixel line counts; periodic pale grid determines scale.
  ox=int(np.argmax((a<120).sum(0)));oy=int(np.argmax((a<120).sum(1)))
  gs=((a>180)&(a<245)).sum(0);peaks=np.where(gs>h*.35)[0];clusters=[]
  for v in peaks:
   if not clusters or v-clusters[-1][-1]>2:clusters.append([v])
   else:clusters[-1].append(v)
  centers=[np.mean(c) for c in clusters];diff=np.diff(centers);scale=float(np.median(diff[diff>10]))
  vals=[]
  for x,y in points:
   px=ox+x*scale;py=oy-y*scale;radius=scale*(.40 if x==0 else .30)
   yy,xx=np.indices(a.shape);mask=(a<180)&((xx-px)**2+(yy-py)**2<radius**2)&((xx-px)**2+(yy-py)**2>6**2)&(abs(xx-ox)>2)&(abs(yy-oy)>2)
   if x==0:mask &= xx>ox+2
   if y==0:mask &= yy<oy-2
   pixels=np.array([xx[mask]-px,py-yy[mask]]).T
   if len(pixels):pixels=pixels-pixels.mean(0)
   if len(pixels)<5:val=None
   else:
    eigenvalues,eigenvectors=np.linalg.eigh(pixels.T@pixels);vx,vy=eigenvectors[:,-1];val='inf' if abs(vx)<.06 else float(vy/vx)
   vals.append(val)
  results.append({'source_id':qid,'choice_index':i,'asset':c[':answer/value'],'origin_px':[ox,oy],'scale_px':scale,'raster_slopes':vals})
Path(__file__).with_name('source-raster.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
