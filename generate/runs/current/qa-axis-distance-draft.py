"""Root reads actual prompt/solution, complete banks and raster geometry."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186073810;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
G=mod('root_axis_generator',D.with_suffix('.py'));P=mod('root_axis_parser',R/'ode-scalar-parser.py');F=mod('root_axis_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
C=dict(records=0,givens=0,solution_references=0,absolute_difference_rows=0,values=0,pairs=0,whole_banks=0,raster_points=0,raster_lines=0,raster_segments=0,grade_guards=0)
def scalar(t):return P.scalar(t.strip().rstrip('.,'))
def geometry(t):
 p=re.search(r'point \$\((.*?),(.*?)\)\$',t);l=re.search(r'line \$([xy])\s*=\s*(.*?)\$',t);assert p and l
 return l[1],scalar(p[1]),scalar(p[2]),scalar(l[2])
def raster(asset,a,x,y,c):
 p=Path(asset['local_path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==asset['sha256'];im=np.array(Image.open(p).convert('RGB'));h,w=im.shape[:2];assert (w,h)==(600,600)
 z=json.loads(p.with_suffix('.json').read_text());fx,fy=(c,y) if a=='x' else (x,c);d=abs((x if a=='x' else y)-c)
 assert list(map(scalar,z['parameters'][1:]))==[x,y,c] and z['parameters'][0]==a and list(map(scalar,z['foot']))==[fx,fy] and scalar(z['distance'])==d
 b=z['bounds'];assert all(b[0]+2<=float(t)<=b[1]-2 for t in (0,x,fx)) and all(b[2]+2<=float(t)<=b[3]-2 for t in (0,y,fy)) and abs(b[1]-b[0]-b[3]+b[2])<1e-9
 blue=(im[:,:,2]>110)&(im[:,:,2]>im[:,:,0].astype(int)+60)&(im[:,:,2]>im[:,:,1].astype(int)+15);red=(im[:,:,0]>150)&(im[:,:,1]<100)&(im[:,:,2]<100)
 # The actual blue line's long run supplies the native square plotting extent.
 sums=blue.sum(axis=0 if a=='x' else 1);index=int(sums.argmax());assert sums[index]>350
 run=np.flatnonzero(blue[:,index] if a=='x' else blue[index,:]);lo,hi=int(run.min()),int(run.max());unit=(hi-lo)/(b[1]-b[0]);assert unit>20
 if a=='x':left=index-(float(c)-b[0])*unit;top=lo;expected=(left+(float(x)-b[0])*unit,top+(b[3]-float(y))*unit)
 else:left=lo;top=index-(b[3]-float(c))*unit;expected=(left+(float(x)-b[0])*unit,top+(b[3]-float(y))*unit)
 yy,xx=np.where(red);assert len(xx)>20 and abs(xx.mean()-expected[0])<3 and abs(yy.mean()-expected[1])<3;C['raster_points']+=1;C['raster_lines']+=1
 # Axes give an independent check that the line position uses c, not the point.
 black=im.max(axis=2)<100;zx=round(left+(0-b[0])*unit);zy=round(top+b[3]*unit)
 assert black[max(0,round(top)):min(h,round(top)+hi-lo),max(0,zx-4):min(w,zx+5)].sum()>250,(asset['local_path'],a,x,y,c,b,index,lo,hi,left,top,zx,zy)
 assert black[max(0,zy-4):min(h,zy+5),max(0,round(left)):min(w,round(left)+hi-lo)].sum()>250
 px,py=map(round,expected);n=abs((px if a=='x' else py)-index);assert n>=12
 if a=='x':seg=black[max(0,py-2):py+3,min(px,index)+5:max(px,index)-4]
 else:seg=black[min(py,index)+5:max(py,index)-4,max(0,px-2):px+3]
 assert seg.sum()>max(2,n*.1);C['raster_segments']+=1
def check(r,raw=False):
 q,m=r['question'],r['generation'];a,x,y,c=geometry(q[':question/problem']);t,o=(x,y) if a=='x' else (y,x);d=abs(t-c);assert d>0;C['givens']+=1
 if not raw:
  level=q[':question/difficulty'].split('/')[-1];assert max(abs(v) for v in (x,y,c))<=8 and 1<=d<=12
  if level=='easy':assert all(v.q==1 for v in (x,y,c))
  elif level=='moderate':assert t.q==c.q==2 and max(x.q,y.q)<=2
  else:assert t.q!=c.q and t.q in (2,3,4) and c.q in (2,3,4) and max(x.q,y.q)<=4
  C['grade_guards']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];assert geometry(sol)==(a,x,y,c)
  assert ('vertical line' in sol)==(a=='x') and ('horizontal line' in sol)==(a=='y') and f'${a}$-coordinate' in sol
  prosevalue=re.search(r'coordinate of the point and \$(.*?)\$',sol);assert prosevalue and scalar(prosevalue[1])==c;C['solution_references']+=4
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==1
  line=blocks[0].strip().rstrip('.');v=re.fullmatch(r'd=\|(.*)\|=(.*)',line);assert v
  # First displayed coordinate and explicitly subtracted line constant separately.
  expected=G.tex(t)+'-'+('('+G.tex(c)+')' if c<0 else G.tex(c));assert v[1]==expected and abs(scalar(v[1]))==d and scalar(v[2])==d;C['absolute_difference_rows']+=1
  assert len(m['assets'])==1 and re.findall(r'!\[\]\((.*?)\)',sol)==[m['assets'][0]['path']]
  if not raw:raster(m['assets'][0],a,x,y,c)
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio';vals=[scalar(v[':answer/value']) for v in f[':answer-field/choices']];assert len(vals)==5
 if not raw:
  assert all(v>0 for v in vals) and sum(v==d for v in vals)==1
  for v,w in itertools.combinations(vals,2):assert v!=w;C['pairs']+=1
  expected=[d,abs(o-c),abs(t+c),abs(t) if m['profile']=='coordinate-errors' else abs(o),abs(c)];assert sorted(vals)==sorted(expected);C['whole_banks']+=1
 if ':answer-field/correct' in f:assert next(scalar(v[':answer/value']) for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1])==d
 C['values']+=5;C['records']+=1
records=json.loads((R/f'qa/{K}-sampled.json').read_text())
for l in ('easy','moderate','hard'):
 for template in G.TEMPLATES:
  for profile in G.PROFILES:records.append(G.generate(l,37,template=template,profile=profile))
for r in records:check(r)
for case in json.loads((D/'source-cases.json').read_text()):check(G.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['profile']),True)
# Native-sized source/normal contacts are saved for direct root inspection.
def contact(paths,dest):
 imgs=[Image.open(p).convert('RGB') for p in paths];ww=max(i.width for i in imgs);hh=max(i.height for i in imgs);out=Image.new('RGB',(ww*2,hh*((len(imgs)+1)//2)),'white')
 for n,im in enumerate(imgs):out.paste(im,((n%2)*ww,(n//2)*hh))
 out.save(dest)
src=json.loads((D/'source.json').read_text())['record'];qs=[src[':knowledge-point/canonical-example']]+list(originals.values());paths=[Path('/media/jake/SSD/EDB/math')/p for q in qs for p in re.findall(r'!\[\]\((.*?)\)',q.get(':question/worked-solution',''))];contact(paths,R/f'qa/{K}-original-native.png')
paths=[e['asset']['local_path'] for e in json.loads((D/'plot-review.json').read_text())['normal_native_images_inspected']];contact(paths,R/f'qa/{K}-normal-native.png')
result=dict(status='passed',source=fidelity,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
