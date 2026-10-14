"""Root original topology and actual generated graph/claim/solution readback."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068697;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_nb_parser');g=load(D.with_suffix('.py'),'root_nb_g');f=load(R/'root-source-fidelity.py','root_nb_fid');originals,S=f.check(g,K,D,asset_relocation=True)
FACTS={'q-48042':(2,2,-s.oo,3,3),'q-48064':(2,2,1,-2,1),'q-48063':(2,2,3,3,1),'q-104049':(2,2,2,2,2),'q-104051':(5,5,2,4,2),'q-104052':(0,0,3,3,None),'q-104124':(-2,-2,5,5,5),'q-48040':(-1,-1,2,1,1),'q-48062':(1,1,1,1,None),'q-48065':(2,2,1,1,1),'q-48067':(1,1,1,1,1),'q-48068':(1,-1,1,1,None)}
def math(z):
 z=z.strip().rstrip('.,').replace(r'\,','');z=z.replace(r'\infty','INFINITY');z=re.sub(r'\s+','',z);return s.oo if z=='INFINITY' else -s.oo if z=='-INFINITY' else p.scalar(z)
def subset(z):return frozenset(re.findall(r'\b(?:III|II|I)\b',z))
def continuous(left,right,value):return value is not None and left not in (-s.oo,s.oo) and left==right==value
C=dict(records=0,actual_claims=0,statement_truths=0,option_subsets=0,criterion_pairs=0,displayed_limit_values=0,displayed_function_values=0,source_prose_masks=0,raster_markers=0,zero_axes=0,actual_curve_limits=0)
records=json.load(open(R/f'qa/{K}-sampled.json'));records.extend(g.generate('easy',template=sid,parameters={'shift':2}) for sid in FACTS)
for rec in records:
 q=rec['question'];md=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];level=q[':question/difficulty'].split('/')[-1];geom=rec['generation']['plot_geometry'];a,b=map(lambda z:s.Rational(str(z)),geom['targets']);markers=geom['markers']
 if level=='easy':
  oa,ob,left,right,value=FACTS[family];shift=rec['generation']['parameters']['shift'];assert a==oa+shift and b==ob+shift
  secondary=True if family=='q-48068' else continuous(left,right,value)
  source=originals[family].get(':question/worked-solution')
  if source:
   clean=lambda z:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',z,flags=re.S)).strip();assert clean(sol)==clean(source);C['source_prose_masks']+=1
 else:
  limits=[]
  for xx,yy in geom['curves']:
   xx=np.asarray(xx);yy=np.asarray(yy);side=-1 if xx.mean()<float(a) else 1;finite=abs(yy[0])<9.9
   if finite:
    coeff=np.polyfit(xx[:30]-float(a),yy[:30],2);assert abs(coeff[0]-.35)<1e-8 and abs(coeff[1])<1e-8;lim=s.Integer(round(coeff[2]));assert abs(float(lim)-coeff[2])<1e-8
   else:
    idx=np.flatnonzero(abs(yy)<9.5);assert len(idx)>10;product=yy[idx[:20]]*abs(xx[idx[:20]]-float(a));assert np.allclose(product,product[0]) and abs(abs(product[0])-1)<1e-8;lim=s.oo if product[0]>0 else -s.oo
   limits.append((side,lim));C['actual_curve_limits']+=1
  left=dict(limits)[-1];right=dict(limits)[1];assigned=[s.Rational(str(my)) for mx,my,filled in markers if s.Rational(str(mx))==a and filled];assert len(assigned)<=1;value=assigned[0] if assigned else None
  secondary=not any(s.Rational(str(mx))==b and not filled for mx,my,filled in markers) if b!=a else continuous(left,right,value)
 claims=re.findall(r'^[I]{1,3}\. (.*)$',md,re.M);assert len(claims)==3;bits=[]
 for claim in claims:
  if 'finite' in claim:
   sign='-' if re.search(r'\^\{?-',claim) else '+';lim=left if sign=='-' else right;truth=lim not in (-s.oo,s.oo);truth=not truth if '**not** finite' in claim else truth
   # Actual directed target remains a, including source nested TeX braces.
   token=re.search(r'\\to\s*(.*?)\^',claim)[1];token=token[1:-1] if token.startswith('{') and token.endswith('}') else token;assert math(token)==a
  elif 'defined at' in claim:truth=value is not None;truth=not truth if '**not** defined' in claim else truth;assert math(re.search(r'\$x\s*=\s*(.*?)\$',claim)[1])==a
  elif 'continuous at' in claim or 'discontinuous at' in claim or 'discontinuity at' in claim:
   target=math(re.search(r'\$x\s*=\s*(.*?)\$',claim)[1]);assert target in (a,b);truth=secondary if target==b and b!=a else continuous(left,right,value);truth=not truth if 'discontinu' in claim else truth
  elif 'exists' in claim:truth=left==right and left not in (-s.oo,s.oo)
  else:
   assert 'f(' in claim and 'lim' in claim,(family,claim);exists=left==right and left not in (-s.oo,s.oo);truth=exists and value is not None and left==value
   if r'\ne' in claim or r'\neq' in claim:truth=exists and value is not None and left!=value
  bits.append(bool(truth));C['actual_claims']+=1
 actual=[v=='true' for v in re.findall(r'Statement [I]{1,3} is (true|false)',sol)];assert actual==bits,(family,actual,bits);C['statement_truths']+=3
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];subsets=[subset(z[':answer/value']) for z in choices];assert len(set(subsets))==5;wanted=frozenset(z for z,v in zip(['I','II','III'],bits) if v);assert [a[':answer/id'] for a,z in zip(choices,subsets) if z==wanted]==[field[':answer-field/correct'][1]];C['option_subsets']+=5;C['criterion_pairs']+=10
 for m in re.finditer(r'\{lim\}_\{x\\to\s*(.*?)\}\s*f\(x\)\s*(?:&\s*)?=\s*([^,$]+)',sol):
  raw=m[1];direction='-' if raw.endswith('^{-}') or raw.endswith('^-') else '+' if raw.endswith('^{+}') or raw.endswith('^+') else None;token=re.sub(r'\^\{?[+-]\}?$','',raw).replace(r'\,','');token=token[1:-1] if token.startswith('{') and token.endswith('}') else token;assert math(token)==a;want=left if direction=='-' else right if direction=='+' else left;assert math(m[2].split('=')[0].split(r'\end')[0])==want;C['displayed_limit_values']+=1
 for token,raw in re.findall(r'f\(([^()]+)\)\s*=\s*([^$.,]+)',sol):
  if token=='x':continue
  assert math(token)==a and value is not None and math(raw)==value;C['displayed_function_values']+=1
 png=Path(re.search(r'!\[\]\((.*?)\)',md)[1]);side=png.with_suffix('.json')
 if side.exists():
  meta=json.load(open(side));im=np.array(Image.open(png).convert('RGB'));red=(im[:,:,0]>170)&(im[:,:,1]<130)&(im[:,:,2]<130);T=np.array(meta['transform']);H=im.shape[0]
  for mx,my,filled in markers:
   px,py=(T@np.array([mx,my,1]))[:2];px=round(px);py=round(H-py);patch=red[py-2:py+3,px-2:px+3];assert patch.any()==filled,(family,mx,my,filled);assert red[py-7:py+8,px-7:px+8].sum()>15;C['raster_markers']+=1
  xmin,xmax,ymin,ymax=geom['bounds'];assert xmin<0<xmax and ymin<0<ymax;assert np.allclose((T@np.array([0,0,1]))[:2],meta['origin']);C['zero_axes']+=2
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=13,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
