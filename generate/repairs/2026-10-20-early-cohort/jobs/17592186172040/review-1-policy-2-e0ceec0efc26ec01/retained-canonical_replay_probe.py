"""Retained ef9fcb18c9498adb4987: original composite and all four panels."""
import importlib.util,json,pathlib,re,sys,os
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent
W=pathlib.Path(os.environ.get('REVIEW_PACKAGE',str(ROOT.parent/'workspace')))
E=ROOT/os.environ.get('REVIEW_CASE','retained-canonical');E.mkdir(exist_ok=True)
s=importlib.util.spec_from_file_location('g',W/'17592186172040.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
source=json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/canonical-example']
r=g.generate('easy',seed=991,profile='e-8507');q=r['question'];f=q[':question/answer-fields'][0]
assert q[':question/problem']==source[':question/problem']
assert q[':question/worked-solution']==source[':question/worked-solution']
choices=f[':answer-field/choices'];assert len(choices)==4
assert sorted(a[':answer/value'] for a in choices)==['I','II','III','IV']
asset=re.findall(r'!\[\]\((.*?)\)',q[':question/problem'])[0]
# Independently recover slope orientations from the visible composite, not the
# generator's declared equation, plot metadata, or correct answer designation.
im=np.asarray(Image.open(pathlib.Path('/media/jake/SSD/EDB/math')/asset).convert('RGBA'),dtype=float)
rgb=im[:,:,:3]*im[:,:,3:]/255+255*(1-im[:,:,3:]/255)
def panel(left,right,top,bottom):
 a=rgb[top+3:bottom-3,left+3:right-3];gray=a.min(2);mask=(gray>90)&(gray<230);seen=set();points=[]
 for yy,xx in zip(*np.where(mask)):
  if (yy,xx) in seen:continue
  todo=[(yy,xx)];seen.add((yy,xx));pts=[]
  while todo:
   y,x=todo.pop();pts.append((x,y))
   for dy in (-1,0,1):
    for dx in (-1,0,1):
     v=(y+dy,x+dx)
     if 0<=v[0]<mask.shape[0] and 0<=v[1]<mask.shape[1] and mask[v] and v not in seen:seen.add(v);todo.append(v)
  if not 4<=len(pts)<=160:continue
  pts=np.array(pts);mu=pts.mean(0);ev,vec=np.linalg.eigh(np.cov(pts.T));v=vec[:,ev.argmax()]
  if v[0]<0:v=-v
  angle=np.arctan2(-v[1],v[0]);points.append((round(mu[0]/22.5),round(mu[1]/18.5),float(angle)))
 spreads=[]
 for k in (0,1):
  groups={}
  for p in points:groups.setdefault(p[k],[]).append(p[2])
  spreads.append(float(np.median([max(v)-min(v) for v in groups.values() if len(v)>=6])))
 return {'segments':len(points),'column_spread':spreads[0],'row_spread':spreads[1]}
results={label:panel(*bounds) for label,bounds in zip(('I','II','III','IV'),[(48,318,6,229),(403,674,6,229),(48,318,300,525),(403,674,300,525)])}
qualifying=[k for k,v in results.items() if v['column_spread']>.3 and v['row_spread']>.3]
assert len(qualifying)==1,results
key=next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);assert key==qualifying[0],(key,results)
(E/'canonical-records.json').write_text(json.dumps([r],indent=2)+'\n')
(E/'canonical-result.json').write_text(json.dumps({'source_id':source[':question/id'],'profile':'e-8507','seed':991,'prompt_exact':True,'solution_exact':True,'complete_bank':['I','II','III','IV'],'pixel_witness':results,'independent_qualifying_panel':qualifying,'key':key,'captured_field_missing':True,'authored_easy_assignment':True},indent=2)+'\n')
print('PASS: exact canonical content, four-panel bank, independently measured qualifying panel',key)
