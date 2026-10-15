"""Root actual-PNG circle/fill/shaft readback and complete interval semantics."""
import sys,json,re,hashlib,importlib.util,copy
from pathlib import Path
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059828;D=R.parents[2]/f'generate/scratch/{K}-draft';SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
def module(name,path):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=module('root_numberline_sets',R/'interval-readback.py');s=p.s;g=module('root_numberline_draft',D.with_suffix('.py'))
C=dict(records=0,png_readbacks=0,circles=0,shaft_probes=0,choices=0,solution_sets=0,source_banks=0,source_values=0,source_keys=0,source_prose=0,inventory_records=0);tasks={l:set()for l in('easy','moderate','hard')};seen_png={}
# Numeric anchor labels independently confirmed on original contact-sheet images.
sourcefits={'a2cc171':(-3,3,25,320),'a2e3d6a':(1,6,25,271),'05b54d1':(-4,4,25,418),'e91f27d':(1,6,25,271)}
visual_fits={Path(row['path']):row['anchors']for row in json.loads((D/'rendered-readback.json').read_text())['records']if row['label'].startswith('inventory-')}
def raster(path):
 if path in seen_png:return seen_png[path]
 rgba=Image.open(path).convert('RGBA');im=Image.new('RGBA',rgba.size,'white');im.alpha_composite(rgba);a=np.array(im.convert('RGB'));red=(a[:,:,0]>180)&(a[:,:,1]<100)&(a[:,:,2]<100);rowcount=red.sum(axis=1);cy=int(np.median(np.where(rowcount>rowcount.max()*.65)[0]));rest=red.copy();radius=2 if a.shape[0]<60 else 4;rest[max(0,cy-radius):cy+radius+1]=False;columns=np.where(rest.any(axis=0))[0];groups=[]
 for xx in columns:
  if groups and xx-groups[-1][-1]<=(8 if a.shape[0]<60 else 22):groups[-1].append(int(xx))
  else:groups.append([int(xx)])
 assert len(groups)==2,(path,groups);centers=[(v[0]+v[-1])/2 for v in groups];closed=[bool(red[cy,round(xx)])for xx in centers]
 if path.with_suffix('.json').exists():
  axis=json.loads(path.with_suffix('.json').read_text())['axis_pixel_fit'];origin=axis['origin_pixel'];scale=axis['pixels_per_unit']
 else:
  if path in visual_fits:
   fit=visual_fits[path];v0,v1=fit['anchor_values'];x0,x1=fit['anchor_pixels']
  else:
   key=next(k for k in sourcefits if path.name.startswith(k));v0,v1,x0,x1=sourcefits[key]
  scale=(x1-x0)/(v1-v0);origin=x0-v0*scale
 values=[s.Rational(round(2*(xx-origin)/scale),2)for xx in centers];assert all(abs(float(v)-(xx-origin)/scale)<.035 for v,xx in zip(values,centers))
 # Detect shaft continuity and rule out an assessed red ray outside the circles.
 for xx in np.linspace(centers[0]+12,centers[1]-12,8):assert red[max(0,cy-2):cy+3,round(xx)].any();C['shaft_probes']+=1
 for xx in (max(0,round(centers[0]-20)),min(a.shape[1]-1,round(centers[1]+20))):assert not red[max(0,cy-2):cy+3,xx].any();C['shaft_probes']+=1
 target=s.Interval(*values,left_open=not closed[0],right_open=not closed[1]);seen_png[path]=target;C['png_readbacks']+=1;C['circles']+=2;return target
def check(r):
 q=r.get('record',r);q=copy.deepcopy(q.get('question',q))
 if isinstance(q.get(':question/difficulty'),dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for field in q[':question/answer-fields']:
  if isinstance(field.get(':answer-field/correct'),dict):field[':answer-field/correct']=[':answer/id',field[':answer-field/correct'][':answer/id']]
 ref=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1];path=Path(ref)
 if not path.is_absolute():path=(Path('/media/jake/SSD/EDB/math')/path)if ref.startswith('images/')else R.parents[2]/path
 assert path.is_file(),path;target=raster(path);f=q[':question/answer-fields'][0];values=[p.meaning(a[':answer/value'])for a in f[':answer-field/choices']];assert len(set(values))==len(values)==5;eligible=[a[':answer/id']for a,v in zip(f[':answer-field/choices'],values)if v==target];assert len(eligible)==1
 if f.get(':answer-field/correct'):assert f[':answer-field/correct']==[':answer/id',eligible[0]]
 else:assert ':question/difficulty'not in q and ':question/worked-solution'not in q
 if q.get(':question/worked-solution'):
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==2
  for block in blocks:assert p.meaning(block.replace(r'\lt','<'))==target,(block,target);C['solution_sets']+=1
  level=q[':question/difficulty'].split('/')[-1];tasks[level].add((target,str(ref)))
 C['records']+=1;C['choices']+=5;return q
src=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
for old in src:
 if ':question/math-academy-id'in old:
  q=check(g.replay_source(old[':question/math-academy-id']));assert q[':question/problem']==old[':question/problem'];of=old[':question/answer-fields'][0];f=q[':question/answer-fields'][0];assert {p.meaning(a[':answer/value'])for a in of[':answer-field/choices']}=={p.meaning(a[':answer/value'])for a in f[':answer-field/choices']};C['source_banks']+=1;C['source_values']+=5
  if of.get(':answer-field/correct'):assert p.meaning(of[':answer-field/correct'][':answer/value'])==next(p.meaning(a[':answer/value'])for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
  if old.get(':question/worked-solution'):assert old[':question/worked-solution']==q[':question/worked-solution'];C['source_prose']+=1
 else:
  q=copy.deepcopy(old);q[':question/difficulty']=q[':question/difficulty'][':db/ident']
  for f in q[':question/answer-fields']:f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  check({'question':q});C['inventory_records']+=1
for records in json.loads((D/'review.json').read_text()).values():
 for r in records:check(r)
for r in json.loads((D/'source-style-variants.json').read_text())+json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
proof={'status':'passed','script_sha256':SCRIPT_SHA,'source_and_readback':C,'sampled_presentations':{l:len(v)for l,v in tasks.items()},'pixel_calibration':'Root independently detected red circular centers/fills and finite shaft from actual PNG pixels. Source numeric axes manually verified; generated pixel calibration read from Matplotlib axis fit, not endpoint metadata. Original source contact reviewed.','scope':'One finite bounded segment to complete interval. Captured both-open cases retained exactly as original evidence; authored defaults half-open, signed unit/half-unit reading only. No reverse plotting, rays or solving targets.','database_writes':0};(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)
