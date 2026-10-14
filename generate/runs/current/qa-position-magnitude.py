"""Root reads rendered endpoints, every subtraction/norm stage and complete banks."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059715;D=R.parents[2]/f'generate/scratch/{K}-draft';ROOT=R.parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
P=module('position_scalar',R/'ode-scalar-parser.py');G=module('position_generator',D.with_suffix('.py'));F=module('position_fidelity',R/'root-source-fidelity.py')
originals,fidelity=F.check(G,K,D)
C=dict(records=0,endpoint_pairs=0,position_vectors=0,subtraction_rows=0,signed_square_rows=0,evaluated_square_rows=0,root_rows=0,actual_values=0,criterion_pairs=0,whole_method_banks=0,level_checks=0,prose_masks=0,raster_markers=0,raster_axes=0,raster_ray_probes=0)
def scalar(t):return P.scalar(t.strip().rstrip('.'))
def vec(t):return P.vector(t.strip().rstrip('.'))[:2,:]
def equal(a,b):return a.shape==b.shape and all(s.simplify(x-y)==0 for x,y in zip(a,b))
def mask(t):
 t=re.sub(r'The displacement components are .*?\n\n','',t,flags=re.S)
 t=re.sub(r'\$\$.*?\$\$','@DISPLAY@',t,flags=re.S)
 return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',t)).strip()
def pixel_near(im,xy,predicate,radius=4):
 x,y=xy;x,y=int(round(x)),int(round(im.height-y));return any(predicate(im.getpixel((xx,yy))) for xx in range(max(0,x-radius),min(im.width,x+radius+1)) for yy in range(max(0,y-radius),min(im.height,y+radius+1)))
blue=lambda p:p[2]>p[0]+40 and p[2]>p[1]+10 and p[0]<110
black=lambda p:max(p[:3])<100
orange=lambda p:p[0]>150 and p[1]>60 and p[2]<100 and p[0]>p[1]+20

def check(r,raw=False):
 q,m=r['question'],r['generation'];asset=m['assets'][0];mid=m['source_ids'][0];style=asset['style'];labels=G.SPECS[mid]['labels']
 if style=='grid':
  # Actual rendered markers, calibrated by independently tested zero axes and
  # unit transforms, supply the otherwise unprinted graph coordinates.
  points=asset['points']
 else:
  matches=re.findall(r'\b[A-Z]\((-?\d+),\s*(-?\d+)\)',q[':question/problem']);assert len(matches)==2
  points=[[int(x),int(y)] for x,y in matches]
 p,z=points;delta=[z[i]-p[i] for i in range(2)];n=sum(v*v for v in delta);target=s.sqrt(n);C['endpoint_pairs']+=1
 assert points==asset['points']
 if not raw:
  level=q[':question/difficulty'].split('/')[-1];flat=p+z;assert all(delta) and abs(delta[0])!=abs(delta[1])
  if level=='easy':assert style!='grid' and all(0<=a<=6 for a in flat) and all(abs(a)<=6 for a in delta)
  elif level=='moderate':
   assert all(abs(a)<=5 for a in flat) and all(abs(a)<=8 for a in delta)
   if style=='grid':assert all(1<=a<=4 for a in flat) and asset['grid_increment']==1
   else:assert min(flat)<0
  else:assert style=='grid' and asset['grid_increment']==2 and min(flat)<0 and any(a%2 for a in flat) and all(abs(a)<=8 for a in flat) and all(abs(a)<=12 for a in delta)
  C['level_checks']+=1
  path=ROOT/asset['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==asset['sha256'];im=Image.open(path).convert('RGB');assert im.size==(720,600)
  axes=asset['axes'];o=axes['origin_pixel'];ux=axes['unit_x_pixel'];uy=axes['unit_y_pixel'];sx=ux[0]-o[0];sy=uy[1]-o[1];assert sx>0 and abs(sx-sy)<1e-8 and ux[1]==o[1] and uy[0]==o[0]
  assert pixel_near(im,o,black,3);C['raster_axes']+=1
  for pt,xy in zip(points,axes['endpoint_pixels']):
   assert abs((xy[0]-o[0])/sx-pt[0])<1e-8 and abs((xy[1]-o[1])/sy-pt[1])<1e-8
   assert pixel_near(im,xy,blue,4);C['raster_markers']+=1
  if style!='grid':
   for pt in points:
    if any(pt):
     for f in (.24,.72):
      xy=(o[0]+sx*pt[0]*f,o[1]+sy*pt[1]*f)
      # Unit basis can overprint a collinear blue vector close to origin.
      if not pixel_near(im,xy,blue,4):assert (pt[0]==0 or pt[1]==0) and pixel_near(im,xy,orange,4)
      C['raster_ray_probes']+=1
   if style=='position-displacement':
    xy=(o[0]+sx*(p[0]+z[0])/2,o[1]+sy*(p[1]+z[1])/2);assert pixel_near(im,xy,orange,4);C['raster_ray_probes']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==3
  position=blocks[0];rows=position.removeprefix('\n').split(chr(92)*2)
  assert len(rows)==2
  for row,pt in zip(rows,points):
   rhs=row.split('=')[-1].replace(r'\end{aligned}','').strip();assert equal(vec(rhs),s.Matrix(pt));C['position_vectors']+=1
  rows=blocks[1].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2);assert len(rows)==4
  assert labels[1] in rows[0] and labels[0] in rows[0] and '-' in rows[0]
  assert labels[1].lower() in rows[1] and labels[0].lower() in rows[1] and '-' in rows[1]
  operands=re.findall(r'\(([^()]*)\)',rows[2]);assert len(operands)==2 and equal(vec(operands[0]),s.Matrix(z)) and equal(vec(operands[1]),s.Matrix(p)) and ')-(' in rows[2].replace(' ','')
  assert equal(vec(rows[3].split('=')[-1]),s.Matrix(delta));C['subtraction_rows']+=4
  normrows=blocks[2].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2)
  assert len(normrows) in (3,4)
  actual=normrows[0].split('=')[-1].replace(' ','');mt=re.fullmatch(r'\\sqrt\{(?:\(([-\d]+)\)|\{([-\d]+)\})\^\{2\}\+\(([-\d]+)\)\^\{2\}\}',actual);assert mt,(mid,actual)
  assert [int(mt[1] or mt[2]),int(mt[3])]==delta;C['signed_square_rows']+=1
  mt=re.fullmatch(r'\\sqrt\{(\d+)\+(\d+)\}',normrows[1].split('=')[-1].strip());assert mt and list(map(int,mt.groups()))==[a*a for a in delta];C['evaluated_square_rows']+=1
  for row in normrows[2:]:assert scalar(row.split('=')[-1])==target;C['root_rows']+=1
  if not raw:
   sub=re.findall(r'\$\((-?\d+)\)-\((-?\d+)\)=(-?\d+)\$',sol);assert sub==[(str(z[i]),str(p[i]),str(delta[i])) for i in range(2)]
  if style=='grid':
   tuples=re.findall(r'\b[PQ]\((-?\d+),\s*(-?\d+)\)',sol);assert [[int(a),int(b)] for a,b in tuples]==points
  old=originals[mid]
  if ':question/worked-solution' in old:assert mask(sol)==mask(old[':question/worked-solution']);C['prose_masks']+=1
 if q.get(':question/answer-fields'):
  f=q[':question/answer-fields'][0];values=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and all(v>=0 and v.is_real for v in values)
  assert sum(s.simplify(v-target)==0 for v in values)==1
  if not raw:
   expected=[target,s.sqrt(sum((z[i]+p[i])**2 for i in range(2))),s.Integer(sum(abs(a) for a in delta)),s.Integer(n),s.sqrt(sum(abs(a) for a in delta))]
   assert all(sum(s.simplify(v-e)==0 for v in values)==1 for e in expected);C['whole_method_banks']+=1
  if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if s.simplify(v-target)==0]==[f[':answer-field/correct'][1]]
  for v,w in itertools.combinations(values,2):assert s.simplify(v-w)!=0;C['criterion_pairs']+=1
  C['actual_values']+=5
 C['records']+=1
records=json.loads((R/f'qa/{K}-sampled.json').read_text())
for r in json.loads((D/'review.json').read_text()):
 if not r['generation'].get('evidence_only'):records.append(r)
for r in records:check(r)
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']),True)
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0}
(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
