"""Parent source raster readings, actual displayed isolation rows and complete banks."""
import json,re,hashlib,sys,importlib.util,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068780;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=load(D.with_suffix('.py'),'root_unknown');fid=load(R/'root-source-fidelity.py','root_unknown_fid');P=load(R/'ode-scalar-parser.py','root_unknown_parse');originals,S=fid.check(G,K,D)
C=dict(records=0,source_curves=0,actual_graph_points=0,actual_asymptote_labels=0,source_blue_pixels=0,normal_blue_pixels=0,normal_raster_probes=0,actual_zero_axes=0,actual_solution_equations=0,actual_math_islands=0,source_prose_masks=0,scalar_answer_values=0,criterion_pairs=0,authored_level_domains=0)
# Own readings from all nine full native originals; values not imported from generator.
ANCHORS={'e-5926':[3,2,-1,3,2],'q-39046':[4,0,0,4,1],'q-39047':['3/2',0,1,1,'5/2'],'q-113479':[3,1,2,2,5],'q-113476':[2,0,'3/2',1,'7/2'],'q-113478':['-1/2',0,'-3/2',1,-2],'q-113482':[-2,3,'1/2',1,'3/2'],'q-270750':['5/2',0,1,1,'7/2'],'q-320718':[-3,-2,'5/2',-5,'7/2']}
def rgb(path):
 im=Image.open(path).convert('RGBA');im=np.asarray(Image.alpha_composite(Image.new('RGBA',im.size,'white'),im).convert('RGB')).astype(int)
 return im,(im[:,:,2]>im[:,:,0]+40)&(im[:,:,0]<140),im.max(2)<100

def curve(im,blue,a,b,k,ox,oy,sx,sy):
 a,b,k=map(float,[a,b,k]);yy,xx=np.where(blue);X=(xx-ox)/sx;Y=(oy-yy)/sy;f=(X-b)*(Y-k)-float(a);dist=abs(f)/np.hypot((Y-k)/sx,(X-b)/sy);assert np.percentile(dist,99)<3,(a,b,k,np.percentile(dist,99));assert sum(X<b)>20 and sum(X>b)>20;return len(X)
for sid,z in json.load(open(D/'plot-extraction.json'))['plots'].items():
 a,b,k,px,py=map(s.Rational,ANCHORS[sid]);assert py==a/(px-b)+k;assert {t:str(v) for t,v in zip(['a','b','k','px','py'],[a,b,k,px,py])}==z['parameters']
 im,blue,black=rgb(Path('/media/jake/SSD/EDB/math')/z['asset']);ox,oy=z['calibration']['origin'];sx=z['calibration']['pixels_per_x_unit'];sy=z['calibration']['pixels_per_y_unit']
 assert black[round(oy)-2:round(oy)+3,20:330].sum()>200 and black[30:275,round(ox)-2:round(ox)+3].sum()>150;C['actual_zero_axes']+=2
 C['source_blue_pixels']+=curve(im,blue,a,b,k,ox,oy,sx,sy);C['source_curves']+=1
 X=round(ox+float(px)*sx);Y=round(oy-float(py)*sy);assert blue[Y-3:Y+4,X-3:X+4].sum()>10;C['actual_graph_points']+=1

def scalar(t):
 # a is the assessed unknown; map it to a supported symbolic u only for parsing.
 t=re.sub(r'(?<![A-Za-z])a(?![A-Za-z])','u',t.strip().rstrip('.,'));t=re.sub(r'(?<![A-Za-z])b(?![A-Za-z])','v',t);return P.scalar(t)
x,y,u=(P.scalar(t) for t in ['x','y','u'])
def mask(t):return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$','<MATH>',t)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for c in json.load(open(D/'source-cases.json')):
 o=originals[c.get('math_academy_id',c.get('source_ma_id',c.get('source_id')))];level=c.get('difficulty',c.get('level',c['template'].split('_')[0]))
 records.append(G.generate(level,template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile'))))
 for seed in [45,77]:records.append(G.generate(level,seed,template=c['template'],profile=c.get('bank_profile',c.get('profile'))))
for rec in records:
 q=rec['question'];gen=rec['generation'];sid=gen['source_ids'][0];level=gen['template'].split('_')[0];raw=gen['evidence_only'];path=gen['plot_asset'];plot=gen['plot']
 if 'source_asset' in plot:a,b,k,px,py=map(s.Rational,ANCHORS[sid])
 else:
  # Read actual text artists: point label and numeric asymptote labels, paired
  # with the rendered transform; independently confirm every blue curve pixel.
  a,b,k,px,py=[s.Rational(plot['parameters'][t]) for t in ['a','b','k','px','py']]
  arts=plot['artist_text_readback'];points=[z for z in arts if re.fullmatch(r'\([^()]+,[^()]+\)',z['text'])];assert len(points)==1
  xx,yy=map(s.Rational,points[0]['text'][1:-1].split(','));assert xx==px and yy==py;C['actual_graph_points']+=1
  numeric=[z['text'] for z in arts if re.fullmatch(r'-?\d+(?:\.\d+)?',z['text'])];assert sorted(map(s.Rational,numeric))==sorted(v for v in [b,k] if v!=0);C['actual_asymptote_labels']+=len(numeric)
  assert a==(py-k)*(px-b)
  im,blue,black=rgb(path);h,w=im.shape[:2];lo,hi,bot,top=plot['bounds'];sx=w*.86/(hi-lo);sy=(5.07*120)*.86/(top-bot);ox=w*.07-lo*sx;oy=h-((5.07*120)*.07-bot*sy)
  assert np.allclose(plot['origin_pixel_bottom'],[ox,h-oy]);assert black[round(oy)-2:round(oy)+3,int(w*.1):int(w*.9)].sum()>w*.4 and black[int(h*.1):int(h*.9),round(ox)-2:round(ox)+3].sum()>h*.4;C['actual_zero_axes']+=2
  fitblue=blue.copy();ix=round(ox+float(px)*sx);iy=round(oy-float(py)*sy);fitblue[iy-5:iy+6,ix-5:ix+6]=False;C['normal_blue_pixels']+=curve(im,fitblue,a,b,k,ox,oy,sx,sy)
  for dx in [-2,-1,1,2]:
   X=float(b)+dx*abs(float(px-b));Y=float(a)/(X-float(b))+float(k)
   if lo<X<hi and bot<Y<top:
    ix=round(ox+X*sx);iy=round(oy-Y*sy);assert blue[iy-4:iy+5,ix-4:ix+5].any();C['normal_raster_probes']+=1
  for z in arts:
   l,bb,ww,hh=z['bbox_pixels_bottom'];assert l>=0 and bb>=0 and l+ww<=w and bb+hh<=h
  if b!=0:
   ix=round(ox+float(b)*sx);gray=(im[:,:,0]>105)&(im[:,:,0]<190)&(abs(im[:,:,0]-im[:,:,1])<4)&(abs(im[:,:,0]-im[:,:,2])<4);assert gray[int(h*.12):int(h*.88),ix-2:ix+3].sum()>h*.15
  if k!=0:
   iy=round(oy-float(k)*sy);assert gray[iy-2:iy+3,int(w*.12):int(w*.88)].sum()>w*.15 if b!=0 else True
 # Formula in actual prompt specifies exactly which coefficients are unknown.
 demand='a' if level=='easy' else 'a+k' if level=='moderate' else 'a+b+k'
 assert ('\\frac{a}{x-b}' in q[':question/problem'])==(level=='hard')
 target=a if level=='easy' else a+k if level=='moderate' else a+b+k
 if not raw:
  if level=='easy':assert b==k==0 and a>0 and a.q==1 and px.q==py.q==1 and 2<=abs(px)<=8 and 1<=abs(py)<=4
  elif level=='moderate':assert b==0 and k!=0 and px==1
  else:assert b!=0 and k!=0 and b.q==1 and 1<=abs(px-b)<=3 and (px-b).q==1
  C['authored_level_domains']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];sub={x:px,y:py,u:a,P.scalar('v'):b,P.scalar('k'):k}
  if sid!='q-39046':assert mask(sol)==mask(originals[sid][':question/worked-solution']);C['source_prose_masks']+=1
  if sid=='q-39046':assert sol.startswith('We are given that the point ')
  # Every complete expression in every inline math island and aligned row,
  # including final sums, must agree with the actual graph/marked point.
  for island in re.findall(r'\$\$([\s\S]*?)\$\$|\$([^$]*?)\$',sol):
   body=(island[0] or island[1]).strip();C['actual_math_islands']+=1
   if body.startswith(r'\begin{aligned}'):
    rows=body.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r'\\')
    for row in rows:
     row=row.replace('&','').strip().rstrip('.');parts=row.split('=');assert len(parts)>=2
     vals=[scalar(p).subs(sub) for p in parts];assert all(s.simplify(v-vals[0])==0 for v in vals[1:]),(sid,row,sub,vals);C['actual_solution_equations']+=len(vals)-1
   elif '=' in body:
    parts=body.rstrip('.,').split('=');local=dict(sub)
    if parts[0].strip()=='y' and not scalar(parts[1]).free_symbols:local[y]=k
    if parts[0].strip()=='x' and not scalar(parts[1]).free_symbols:local[x]=b
    vals=[scalar(p).subs(local) for p in parts];assert all(s.simplify(v-vals[0])==0 for v in vals[1:]),(sid,body,vals);C['actual_solution_equations']+=len(vals)-1
   elif body.startswith('(') and ',' in body:
    point=body.rstrip('.,')[1:-1].split(',');assert list(map(scalar,point))==[px,py]
  assert len(re.findall(r'&',sol))==(2 if level=='easy' else 4)
 fs=q.get(':question/answer-fields',[])
 for field in fs:
  vals=[scalar(z[':answer/value']) for z in field[':answer-field/choices']];C['scalar_answer_values']+=len(vals)
  if field[':answer-field/type'].endswith('/radio'):
   assert len(vals)==5 and len(set(vals))==5;C['criterion_pairs']+=10
   if not raw:
    if level=='easy':want=[a,px+py,px-py,py,py/px] if gen['profile']=='method-unit' else [a,px+py,px-py,px/py,py/px]
    elif level=='moderate':want=[a+k,a,k,a-k,-a+k]
    else:want=[a+b+k,a-b+k,-a+b+k,a+b-k,a+b]
    assert sorted(vals)==sorted(want)
   expected=target
  else:
   assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem'];expected={'field-1':a,'field-2':b if level=='hard' else k,'field-3':k}[field[':answer-field/key']];assert vals==[expected]
  if ':answer-field/correct' in field:
   z=next(z for z in field[':answer-field/choices'] if z[':answer/id']==field[':answer-field/correct'][1]);assert scalar(z[':answer/value'])==expected
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=9,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
