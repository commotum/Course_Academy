"""Parent independent displayed positive reciprocal functions and full image banks."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068813;D=R.parents[2]/f'generate/scratch/{K}'
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
G=load(D.with_suffix('.py'),'root_stretch');fid=load(R/'root-source-fidelity.py','root_stretch_fid');originals,S=fid.check(G,K,D)
# Independently transcribed from ALL 21 native source raster coordinate labels.
COEFF={'e80865b0f32a':'1','b7b1fe93de79':'7/2','d5d93e12275c':'-1','e2a1274fc653':'-1/2','a32495fcca94':'1','8974b1f9f7fe':'2','f3a1cac41b2f':'1/2','79b496d28a01':'3','5a43656a35d4':'3/2','89233072deb8':'-3/2','42560d0e8acf':'3/5','475caaf8128e':'-5/3','1296c3a09ca4':'-3/5','98920680f0cf':'5/3','ffe0cdd09cce':'-2','eeb158823a32':'5','fdc3e5ca668f':'-5','0fe642f3c787':'1','1c62cf53292f':'10','6c7b719326bf':'1/5','b3a79a8dbe82':'1'}
C=dict(records=0,actual_prompt_functions=0,solution_functions=0,stretch_factors=0,complete_banks=0,criterion_pairs=0,source_label_coefficients=0,source_raster_curve_points=0,normal_raster_probes=0,actual_zero_axes=0,point_constraints=0,source_prose_masks=0)
def img(p):
 a=Image.open(p).convert('RGBA');im=np.asarray(Image.alpha_composite(Image.new('RGBA',a.size,'white'),a).convert('RGB')).astype(int)
 return im,(im[:,:,2]>im[:,:,0]+30)&(im[:,:,0]<150),(im.max(2)<100)
for z in json.load(open(D/'plot-spec.json')):
 c=F(COEFF[Path(z['asset']).stem[:12]]);assert c==F(z['coefficient']);C['source_label_coefficients']+=1
 im,blue,black=img(Path('/media/jake/SSD/EDB/math')/z['asset']);ox,oy=z['origin'];sx,sy=z['pixels_per_x_unit'],z['pixels_per_y_unit'];assert abs(ox-169)<1 and abs(oy-162.5)<1
 # Independently locate both black coordinate axes in the source raster.
 assert abs(np.argmax(black[40:280,160:179].sum(0))+160-ox)<2
 assert abs(np.argmax(black[155:170,30:315].sum(1))+155-oy)<2;C['actual_zero_axes']+=2
 yy,xx=np.where(blue);sel=(abs(xx-ox)>15)&(abs(yy-oy)>8);err=abs(((xx[sel]-ox)/sx)*((oy-yy[sel])/sy)/float(c)-1);assert np.median(err)<.1;C['source_raster_curve_points']+=len(err)
 for sign in (-1,1):
  px=round(ox+sign*sx);py=round(oy-sign*float(c)*sy);assert blue[py-3:py+4,px-3:px+4].sum()>=10;C['point_constraints']+=1

def frac(t):
 if re.fullmatch(r'-?\d+',t):return F(t)
 z=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',t);assert z,t;return F((-1 if z[1] else 1)*int(z[2]),int(z[3]))
def function(t):
 z=re.fullmatch(r'\\frac\{(\d+)\}\{(\d*)x\}',t);assert z,t;return F(int(z[1]),int(z[2] or 1))
def mask(t):
 t=re.sub(r'y=\\frac\{\d+\}\{\d*x\}','y=<FUNCTION>',t);t=re.sub(r'scale factor of \$.*?\$', 'scale factor of $<FACTOR>$',t);return re.sub(r'!\[\]\(.*?\)','![](<PLOT>)',t)
source_masks={mask(q[':question/worked-solution']) for q in originals.values()};assert len(source_masks)==1
recipes={
 'raw_q-16506':lambda a,n,d:[-1,-a,1,1/a,a],
 'raw_q-99064':lambda a,n,d:[-F(1,d),F(1,d),n,a,-a],
 'raw_q-113328':lambda a,n,d:[1,1/a,-a,-1/a,a],
 'raw_q-97952':lambda a,n,d:[-1,1/a,1,-a,a],
 'raw_q-113324':lambda a,n,d:[a,-a,1,2*a,1/a],
 'integer_reversal':lambda a,n,d:[-1,1/a,1,-a,a],
 'unit_numerator_reversal':lambda a,n,d:[-1,-a,1,1/a,a],
 'rational_denominator':lambda a,n,d:[-F(1,d),F(1,d),n,a,-a],
 'rational_reversal':lambda a,n,d:[1,1/a,-a,-1/a,a],
 'nonunit_point_reversal':lambda a,n,d:[a,-a,1/a,1,n],
 'nonunit_point_denominator':lambda a,n,d:[a,-a,F(1,d),n,-1/a]}
records=json.load(open(R/f'qa/{K}-sampled.json'))
for c in json.load(open(D/'source-cases.json')):
 level=c['difficulty'];records.append(G.generate(level,parameters=c['parameters'],profile=c['bank_profile']))
 for seed in [49,78]:records.append(G.generate(level,seed,profile=c['bank_profile']))
for rec in records:
 q=rec['question'];sol=q[':question/worked-solution'];p=rec['generation']['parameters'];profile=rec['generation']['bank_profile'];n,d=p['n'],p['d'];a=F(n,d)
 z=re.fullmatch(r'Which of the following is the graph of \$y=(.*?)\?\$',q[':question/problem']);assert z and function(z[1])==a>0;C['actual_prompt_functions']+=1
 fns=re.findall(r'y=(\\frac\{\d+\}\{\d*x\})',sol);assert list(map(function,fns))==[a,F(1),a];C['solution_functions']+=3
 factor=re.search(r'scale factor of \$(.*?)\$',sol);assert factor and frac(factor[1])==a;C['stretch_factors']+=1
 assert mask(sol) in source_masks;C['source_prose_masks']+=1
 level=q[':question/difficulty'].split('/')[-1];m=F(2 if level=='hard' else 1)
 if level=='easy':assert (d==1 and 2<=n<=12) or (n==1 and 2<=d<=12)
 elif level=='moderate':assert 2<=d<=5 and n>=2
 else:assert 6<=d<=12 and n>=2
 bank=[];f=q[':question/answer-fields'][0]
 for ans in f[':answer-field/choices']:
  path=Path(ans[':answer/value']);assert ans[':answer/type']==':answer.type/image'
  if str(path).startswith('images/'):
   c=F(COEFF[path.stem[:12]])
  else:
   side=json.load(open(path.with_suffix('.json')));c=F(side['coefficient']);assert F(side['mark_x'])==m
   assert [[F(x),F(y)] for x,y in side['points']]==[[-m,-c/m],[m,c/m]];C['point_constraints']+=2
   im,blue,black=img(path);assert im.shape==(304,360,3);xl=side['xlim'][1];yl=side['ylim'][1]
   def pix(x,y):return round(360*.07+360*.86*(x+xl)/(2*xl)),round(304-(304*.09+304*.84*(y+yl)/(2*yl)))
   ox,oy=pix(0,0)
   assert black[oy-2:oy+3,30:325].sum()>200 and black[30:275,ox-2:ox+3].sum()>190;C['actual_zero_axes']+=2
   for sign in (-1,1):
    for k in [.55,.8,1,1.3,1.8,2.5,3.5]:
     xx=float(sign*m)*k;yy=float(c)/xx;px,py=pix(xx,yy);assert blue[py-3:py+4,px-3:px+4].any(),(path,xx,yy);C['normal_raster_probes']+=1
   assert all(0<=b[0] and 0<=b[1] and b[0]+b[2]<360 and b[1]+b[3]<304 for b in side['labels'])
  bank.append(c)
 assert sorted(bank)==sorted(recipes[profile](a,n,d));assert len(set(bank))==5;C['complete_banks']+=1;C['criterion_pairs']+=10
 if ':answer-field/correct' in f:
  ans=next(v for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1]);idx=f[':answer-field/choices'].index(ans);assert bank[idx]==a
 else:assert profile=='raw_q-99064' and rec['generation']['evidence_only']
 if profile=='raw_q-113324':assert rec['generation']['evidence_only'] and not rec['generation']['eligible_for_learning']
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=21,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
