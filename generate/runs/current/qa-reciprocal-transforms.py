"""Root full native original geometry, source masks and changed complete graph banks."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068779;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,n):
 z=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load(D.with_suffix('.py'),'root_transform');P=load(R/'ode-scalar-parser.py','root_transform_parse');fid=load(R/'root-source-fidelity.py','root_transform_fid');O,S=fid.check(G,K,D);x=P.scalar('x')
# Own full-native label/asymptote readings for every source asset; opaque503f
# has incoherent point labels and only its vertical asymptote is certain.
TEXT='''2560fc488346 -1 -1 0
5d24b48ce1c0 2 -1 0
5a266218ee01 -2 1 0
c82a01ba019b -2 -1 0
0082eec12acf -1 1 0
13b0cb8176d1 -1/2 0 1
e08cb2c7cdb6 -1 0 1
3f86645950cd -1/2 1 0
9c29f33fa6bd 1/2 0 1
5c4d29ae5547 1/2 1 0
e6798ba049ab 4/5 0 3
7273872baaf6 -4/5 0 3
ea9bd36b532b 4/5 0 0
e7c180f664a7 -4/5 0 0
3c8dd0e47267 -1 2 0
177afbf4d02a 2 2 0
0fba58dd8034 -2 2 0
23a24a5d620c 2 -2 0
97cf018efcc6 -2 -2 0
259f3b708829 5/2 -2 0
a64e70fd5a66 -5/2 0 2
9c7701cbc6cd 5/2 0 2
626fbb611d42 -5/2 0 -2
08925ef54932 5/2 0 -2
939f0f3aab7c 1/4 0 1
befeef541734 -1/4 0 -1
e1777e170fe2 1/4 0 -1
e5d9d1fe85e2 1 0 -1
ade3c2528695 -1/4 0 1
f34ce2cbe8be -2 1 0
8c2c3300cfb1 2 -1 0
614fb6c9f65b -2 -1 0
4309ca72d597 2 1 0
8f2a42430ac3 1 1 0
edb61b0239e9 -5 0 2
65e24bd4cada 5 -2 0
6c4c728e59e4 -5 -2 0
4612933db2d2 -5 0 0
d14d6a75f24a -5 0 -2
47a63204ef63 3/4 -1 0
3a8f77e96f83 -3/4 -1 0
f558777e9ec3 3/4 1 0
0bb082b243d9 -3/4 1 0
b9683bcc1b55 1 -1 0
804eac3df073 -1/2 -1 0
a2af9de8793d 1/2 1 0
c52f56886832 1/2 -1 0
40490df9d6ec -1/2 1 0
a32495fcca94 1 0 0
9da0db2e6c97 -1 0 0
207dec9757b6 -2 2 0
027b68fffd15 1/4 0 0
e80865b0f32a 1 0 0
049f9c306c00 1 -1 0
8ce8c53f202f -1 1 0
c9b708a20d9c -2 1 0
e100b552adb7 -2 1 -1'''
REF={z[0]:tuple(map(s.Rational,z[1:])) for line in TEXT.splitlines() if (z:=line.split())}
C=dict(records=0,actual_prompt_functions=0,actual_solution_functions=0,translation_factors=0,stretch_factors=0,complete_banks=0,criterion_pairs=0,source_native_geometries=0,source_marker_constraints=0,source_raster_pixels=0,normal_raster_pixels=0,normal_marker_constraints=0,actual_zero_axes=0,solution_prose_masks=0)
def form(t):
 a,h,k=t;return a/(x-h)+k

def img(path):
 im=Image.open(path).convert('RGBA');im=np.asarray(Image.alpha_composite(Image.new('RGBA',im.size,'white'),im).convert('RGB')).astype(int);return im,(im[:,:,2]>im[:,:,0]+40)&(im[:,:,0]<140),im.max(2)<100

def fit(blue,t,ox,oy,sx,sy,limit):
 a,h,k=map(float,t);yy,xx=np.where(blue);X=(xx-ox)/sx;Y=(oy-yy)/sy;d=abs((X-h)*(Y-k)-a)/np.hypot((Y-k)/sx,(X-h)/sy);assert np.percentile(d,95)<limit,(t,np.percentile(d,95));assert sum(X<h)>15 and sum(X>h)>15;return len(X)
SPECS=json.load(open(D/'plot-extraction.json'))
for asset,z in SPECS.items():
 prefix=Path(asset).stem[:12]
 if prefix=='503f584dd13e':assert not z['eligible_for_symbolic_source_equivalence'];continue
 t=REF[prefix];assert tuple(s.Rational(z[k]) for k in ['a','h','k'])==t
 im,blue,black=img(Path('/media/jake/SSD/EDB/math')/asset);ox,oy=z['origin_px'];sx,sy=z['units_px'];C['source_raster_pixels']+=fit(blue,t,ox,oy,sx,sy,2.7);C['source_native_geometries']+=1
 a,h,k=t
 for xx,yy in z['printed_points']:
  xx,yy=map(s.Rational,[xx,yy]);assert yy==a/(xx-h)+k;ix=round(ox+float(xx)*sx);iy=round(oy-float(yy)*sy);assert blue[iy-4:iy+5,ix-4:ix+5].sum()>8;C['source_marker_constraints']+=1
 assert black[round(oy)-2:round(oy)+3,25:320].sum()>200 and black[35:275,round(ox)-2:round(ox)+3].sum()>160;C['actual_zero_axes']+=2

def plotted(path):
 if path.startswith('images/'):
  key=Path(path).stem[:12];return REF.get(key)
 side=json.load(open(Path(path).with_suffix('.json')));points=np.array(side['points']);h,k=map(s.Rational,map(str,points.mean(0)));dd=s.Rational(side['distance']);a=s.Rational(side['triple'][0]);t=tuple(map(s.Rational,side['triple']));assert abs(float(h-t[1]))<1e-9 and abs(float(k-t[2]))<1e-9
 for xx,yy in points:assert abs(yy-(float(t[0])/(xx-float(t[1]))+float(t[2])))<1e-9
 im,blue,black=img(path);xl,xh,yl,yh=side['bounds'];sx=384/(xh-xl);sy=324/(yh-yl);ox=67.2-xl*sx;oy=348+yl*sy;C['normal_raster_pixels']+=fit(blue,t,ox,oy,sx,sy,2.7)
 for xx,yy in points:
  ix=round(ox+xx*sx);iy=round(oy-yy*sy);assert blue[iy-4:iy+5,ix-4:ix+5].sum()>15;C['normal_marker_constraints']+=1
 assert black[round(oy)-2:round(oy)+3,75:430].sum()>250 and black[40:340,round(ox)-2:round(ox)+3].sum()>220;C['actual_zero_axes']+=2
 return t

def parse(t):return P.scalar(t.strip().rstrip('.,?'))
def mask(t):
 t=re.sub(r'\$[^$]*\$','<MATH>',t);t=re.sub(r'!\[\]\(.*?\)','![](<PLOT>)',t);t=t.replace('unit ','units ');return re.sub(r'\b(?:left|right|up|down)\b','<DIRECTION>',t)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for case in json.load(open(D/'source-cases.json')):
 records.append(G.generate(case['level'],parameters=case['parameters'],profile=case['bank_profile']))
 if case['source_math_academy_id']!='q-113372':
  for seed in [56,79]:records.append(G.generate(case['level'],seed,profile='normal:'+case['source_math_academy_id']))
for rec in records:
 q=rec['question'];gen=rec['generation'];level=gen['difficulty'];raw=gen['evidence_only'];profile=gen['profile'];p=gen['parameters'];a,h,k=[s.Rational(p[z]) for z in ['a','h','k']];target=form((a,h,k));sign=s.sign(a)
 actual=parse(re.search(r'\$y\s*=\s*(.*?)\$',q[':question/problem'])[1]);assert s.cancel(actual-target)==0;C['actual_prompt_functions']+=1
 field=q[':question/answer-fields'][0];bank=[]
 for ans in field[':answer-field/choices']:
  t=plotted(ans[':answer/value']);bank.append(t)
  if t is not None:assert tuple(map(s.Rational,gen['bank_geometry'][ans[':answer/value']]))==t
 assert len(bank)==5
 for l,r in itertools.combinations(bank,2):
  if l is None or r is None:assert profile=='raw:q-113372' and (r if l is None else l)[1]!=-3
  else:assert s.cancel(form(l)-form(r))!=0
 C['criterion_pairs']+=10;C['complete_banks']+=1
 if ':answer-field/correct' in field:
  ci=next(i for i,z in enumerate(field[':answer-field/choices']) if z[':answer/id']==field[':answer-field/correct'][1]);assert s.cancel(form(bank[ci])-actual)==0
 else:assert raw
 if not raw:
  sol=q[':question/worked-solution'];rows=[parse(z) for z in re.findall(r'\$y\s*=\s*(.*?)\$',sol)];want=[target,sign/x]
  if h:want+=[sign/(x-h)]+([a/(x-h)] if abs(a)!=1 else [])
  else:want+=([a/x] if abs(a)!=1 else [])+[target]
  assert len(rows)==len(want) and all(s.cancel(u-v)==0 for u,v in zip(rows,want));C['actual_solution_functions']+=len(rows)
  for num,direction in re.findall(r'Translate it by \$(.*?)\$ units? (?:to the )?(left|right|up|down)',sol):
   assert parse(num)==abs(h if h else k);assert direction==('right' if h>0 else 'left') if h else direction==('up' if k>0 else 'down');C['translation_factors']+=1
  for num in re.findall(r'scale factor of \$(.*?)\$',sol):assert parse(num)==abs(a);C['stretch_factors']+=1
  if profile.startswith('normal:'):
   sid=profile.split(':')[1]
   if ':question/worked-solution' in O[sid]:assert mask(sol)==mask(O[sid][':question/worked-solution']);C['solution_prose_masks']+=1
  last=re.findall(r'!\[\]\((.*?)\)',sol)[-1];assert s.cancel(form(plotted(last))-target)==0
  if level=='easy':assert abs(a)==1 and bool(h)!=bool(k)
  elif level=='moderate':assert k and not h and abs(a)!=1
  else:assert h and not k and abs(a)!=1
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=58,opaque_source_geometry='503f labels inconsistent: only vertical asymptote−3 used for wrongness; exacta/k are not asserted',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
