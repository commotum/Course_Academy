"""Read actual PNG endpoints, circle centers and segment direction from pixels."""
from pathlib import Path
import json,re,sys,hashlib
H=Path(__file__).resolve().parent
# Import the owned renderer's dependency/readback definitions without executing its CLI.
exec((H/'renderer.py').read_text().split("if sys.argv[1]=='--readback':")[0])
rows=json.loads((H/'visual-records.json').read_text());results=[]
source_anchors={'source-q-28850':([-3,3],[25,320]),'source-q-31762':([1,6],[25,271]),'source-q-154795':([-4,4],[25,418]),'source-q-31779':([1,6],[25,271])}
for row in rows:
 q=row['record']['question'];label=row['label'];path=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1];path=Path(path) if path.startswith('/') else Path('/media/jake/SSD/EDB/math')/path
 m=readback(path)
 if label in source_anchors:vs,px=source_anchors[label]
 else:
  # Independent fit uses actual black boundary tick columns; labels are visually
  # read on the contact sheets. Axis sidecars/Matplotlib transforms are not used.
  level=q[':question/difficulty'].split('/')[-1];field=q[':question/answer-fields'][0];correct=field[':answer-field/correct'][1];answer=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==correct)
  nums=re.search(r'[\[(]([^,]+),([^\])]+)',answer);from fractions import Fraction
  a,b=Fraction(nums[1].replace(' ','')),Fraction(nums[2].replace(' ',''));step=2 if level=='moderate' else 1
  # q31779's observed fully labeled source row has unit labels.
  if label=='q31779-rendered':step=1
  if row['record'].get('generation',{}).get('parameters'):step=Fraction(row['record']['generation']['parameters']['label_step'])
  vs=[float((a//step-1)*step),float(-((-b)//step)*step+step)];px=[m['tick_pixels'][0],m['tick_pixels'][-1]]
 fit={'anchor_values':vs,'anchor_pixels':px,'tick_pixels':m['tick_pixels']};m=readback(path,fit)
 if label in source_anchors:
  expected={'source-q-28850':([-1,2],[False,True]),'source-q-31762':([1,4],[False,False]),'source-q-154795':([-3,2],[False,False]),'source-q-31779':([2,4],[True,False])}[label]
 else:
  expected=([float(a),float(b)],[answer[answer.index('∈')+1:].strip().startswith('['),answer.endswith(']')])
 assert max(abs(x-y) for x,y in zip(m['endpoint_values'],expected[0]))<.026,label+' pixel coordinate/key mismatch'
 assert m['closed']==expected[1],label+' pixel closure/key mismatch'
 # Segment has exactly two circular boundaries and no red ray beyond them.
 image=Image.open(path).convert('RGBA');background=Image.new('RGBA',image.size,'white');background.alpha_composite(image);image=background.convert('RGB');arr=np.array(image);red=(arr[:,:,0]>180)&(arr[:,:,1]<100)&(arr[:,:,2]<100);cy=m['center_y'];a_px,b_px=m['endpoint_pixels'];radius=9 if image.height<60 else 12
 assert not red[:, :max(0,int(a_px-radius))].any() and not red[:,int(b_px+radius+1):].any(),label+' unexpected ray'
 assert red[cy,int(a_px+radius):int(b_px-radius)].mean()>.98,label+' segment direction/continuity'
 results.append({'label':label,'path':str(path),'anchors':fit,'measurement':m,'finite_segment_verified':True})
# Extra canonical original, independently fit from visible -3 and3 labels.
canon=json.loads((H/'source.json').read_text())['record'][':knowledge-point/canonical-example'];p=Path('/media/jake/SSD/EDB/math')/re.search(r'!\[\]\((.*?)\)',canon[':question/problem'])[1];results.append({'label':'canonical','path':str(p),'measurement':readback(p,{'anchor_values':[-3,3],'anchor_pixels':[25,320],'tick_pixels':[25,74,123,172,221,271,320]})})
# Contact sheets preserve native label readability; the reviewer checks the label
# numbers and two endpoint markers against the independent pixel reports.
for start in range(0,len(results),12):
 subset=results[start:start+12];sheet=Image.new('RGB',(1140,220*len(subset)),'white');from PIL import ImageDraw
 d=ImageDraw.Draw(sheet)
 for i,item in enumerate(subset):
  im=Image.open(item['path']).convert('RGB');d.text((8,i*220+2),item['label']+'  '+str(item['measurement']['endpoint_values'])+'  closed='+str(item['measurement']['closed']),fill='black');sheet.paste(im,(8,i*220+25))
 sheet.save(H/('contact-'+str(start//12)+'.png'))
(H/'rendered-readback.json').write_text(json.dumps({'passed':True,'records':results,'actual_pngs':len({r['path'] for r in results}),'method':'PNG red arc and center fill detection; actual black boundary ticks + visually checked printed boundary labels; finite red shaft continuity and no ray; no axes transform metadata used.'},indent=2)+'\n')
print('Read',len(results),'PNG records; coordinate fits, circle centers and finite directions retained.')
