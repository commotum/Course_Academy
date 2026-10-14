"""Root qualitative graph criterion for EVERY displayed polynomial option."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186129145;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_gtp_parser');x=p.x;g=load(D.with_suffix('.py'),'root_gtp_g');f=load(R/'root-source-fidelity.py','root_gtp_fid');originals,S=f.check(g,K,D,asset_relocation=True)
def polynomial(z):return p.scalar(z.split('=',1)[1].replace('{)}',')'))
def signature(expr):
 roots=s.roots(expr,x);assert sum(roots.values())==s.degree(expr,x)
 return tuple((r,'simple' if m==1 else 'even' if m%2==0 else 'odd') for r,m in sorted(roots.items())),s.sign(s.Poly(expr,x).LC())
C=dict(records=0,actual_polynomial_choices=0,graph_criterion_pairs=0,solution_root_coordinates=0,solution_local_behavior_claims=0,solution_concluding_equations=0,source_prose_masks=0,raster_curve_probes=0,true_zero_axes=0)
records=json.load(open(R/f'qa/{K}-sampled.json'));records.extend(g.generate(d[0],template=t,seed=n) for t,d in g.DATA.items() if not t.endswith('-raw') and t not in g.RAW_COLLISION_PROFILES for n in (631,917))
for rec in records:
 q=rec['question'];sol=q[':question/worked-solution'];field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];assert len(choices)==5;expressions=[polynomial(a[':answer/value']) for a in choices];signatures=[signature(v) for v in expressions];assert len(set(signatures))==5;C['graph_criterion_pairs']+=10;C['actual_polynomial_choices']+=5
 meta=rec['generation']['plot'];rs=list(map(s.Integer,meta['roots']));ms=meta['multiplicities'];actual=s.Rational(meta['coefficient'])*s.prod((x-r)**m for r,m in zip(rs,ms));want=signature(actual);assert signatures.count(want)==1;index=signatures.index(want);assert choices[index][':answer/id']==field[':answer-field/correct'][1]
 mentioned=[s.Integer(z) for z in re.findall(r'x=(-?\d+)',sol.split('\n\n')[0])];assert mentioned==rs;C['solution_root_coordinates']+=len(rs)
 bullets=sol.split('\n\n- ')[1:];assert len(bullets)==len(rs)
 for block,r,m in zip(bullets,rs,ms):
  assert set(map(s.Integer,re.findall(r'x=(-?\d+)',block.split('\n\n')[0])))=={r}
  if m==1:assert '*not* tangent' in block and 'simple root' in block
  elif m%2==0:assert 'reverses direction' in block and 'even multiplicity' in block
  else:assert 'passes through' in block and 'greater than one' in block
  C['solution_local_behavior_claims']+=1
 final=re.findall(r'\$(y\s*=.*?)\$',sol)[-1].rstrip('.');assert s.expand(polynomial(final)-expressions[index])==0;C['solution_concluding_equations']+=1
 family=rec['generation']['template'].removesuffix('-authored');source=originals.get(family,{}).get(':question/worked-solution')
 if source:
  clean=lambda z:re.sub(r'\s+',' ',re.sub(r'\$.*?\$','',z)).strip();assert clean(sol)==clean(source);C['source_prose_masks']+=1
 png=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]);im=np.array(Image.open(png).convert('RGB'));red=(im[:,:,0]>170)&(im[:,:,1]<115)&(im[:,:,2]<115);black=(im[:,:,0]<90)&(im[:,:,1]<90)&(im[:,:,2]<90);lo,hi=meta['xlim'];yl,yh=meta['ylim'];assert lo<0<hi and yl<0<yh
 axisx=im.shape[1]*(.06-lo/(hi-lo)*.88);axisy=im.shape[0]*(1-(.1-yl/(yh-yl)*.84));assert abs(black.sum(0).argmax()-axisx)<3 and abs(black.sum(1).argmax()-axisy)<3;C['true_zero_axes']+=2;fn=s.lambdify(x,actual,'numpy')
 for sample in meta['raster_points']:
  X=sample['x'];Y=float(fn(X));assert abs(Y-sample['y'])<1e-7*max(1,abs(Y));px=round(im.shape[1]*(.06+(X-lo)/(hi-lo)*.88));py=round(im.shape[0]*(1-(.1+(Y-yl)/(yh-yl)*.84)));assert red[py-4:py+5,px-4:px+5].any();C['raster_curve_probes']+=1
 level=q[':question/difficulty'].split('/')[-1]
 if level=='hard':assert len(rs)==4 and sorted('simple' if m==1 else 'even' if m%2==0 else 'odd' for m in ms)==['even','odd','simple','simple']
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=11,source_wrong_bank_collisions_preserved_ineligible=['q-38671','q-38774'],script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
