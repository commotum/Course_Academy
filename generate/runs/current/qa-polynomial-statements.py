"""Root independently evaluates printed graph statements from rendered function."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186129154;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_ps_parser');x=p.x;g=load(D.with_suffix('.py'),'root_ps_g');f=load(R/'root-source-fidelity.py','root_ps_fid');originals,S=f.check(g,K,D,asset_relocation=True)
def subset(z):return frozenset(re.findall(r'\b(?:III|II|I)\b',z))
def evaluate(claim,actual,roots):
 if 'p(0)' in claim:
  if 'positive' in claim:return actual.subs(x,0)>0
  val=re.search(r'p\(0\)\s*=\s*([^$]+)',claim)[1].rstrip('.');return actual.subs(x,0)==p.scalar(val)
 if 'p(x)' in claim:
  text=claim.replace(r'\to','→').replace(r'\infty','∞');rhs=re.search(r'p\(x\)\s*→\s*(-?∞)',text)[1];direction=re.search(r'x\s*→\s*(-?∞)',text)[1];return s.limit(actual,x,-s.oo if direction=='-∞' else s.oo)==(-s.oo if rhs=='-∞' else s.oo)
 coords=[]
 for raw in re.findall(r'\$x\s*=\s*(.*?)\$',claim):
  if '±' in raw:z=p.scalar(raw.replace('±',''));coords.extend([-z,z])
  else:coords.append(p.scalar(raw))
 assert coords and all(v in roots for v in coords)
 if 'even multiplicity' in claim:return all(roots[z]%2==0 for z in coords)
 if 'odd multiplicity' in claim:return all(roots[z]%2==1 for z in coords)
 assert 'simple root' in claim;truth=all(roots[z]==1 for z in coords);return not truth if '**not**' in claim else truth
C=dict(records=0,actual_statement_predicates=0,solution_truths=0,choice_subsets=0,criterion_pairs=0,actual_root_derivative_orders=0,source_prose_masks=0,raster_curve_probes=0,true_zero_axes=0)
records=json.load(open(R/f'qa/{K}-sampled.json'));records.extend(g.generate(d['level'],template=t,seed=n) for t,d in g.RECIPES.items() for n in (631,917))
for rec in records:
 q=rec['question'];md=q[':question/problem'];sol=q[':question/worked-solution'];png=Path(re.search(r'!\[\]\((.*?)\)',md)[1]);data=json.load(open(png.with_suffix('.json')));actual=s.sympify(data['polynomial'],locals={'x':x});roots=s.roots(actual,x);assert sum(roots.values())==s.degree(actual,x)
 for root,m in roots.items():assert all(s.diff(actual,x,k).subs(x,root)==0 for k in range(m)) and s.diff(actual,x,m).subs(x,root)!=0;C['actual_root_derivative_orders']+=m+1
 claims=re.findall(r'^(?:[I]{1,3}\.|[-]|[123]\.)\s*(?:-\s*)?(.*)$',md,re.M);assert len(claims)==3;bits=[bool(evaluate(c,actual,roots)) for c in claims];C['actual_statement_predicates']+=3
 truth=[z=='true' for z in re.findall(r'Statement [I]{1,3} is (true|false)',sol)];assert truth==bits,(rec['generation']['template'],truth,bits);C['solution_truths']+=3
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];subsets=[subset(a[':answer/value']) for a in choices];assert len(choices)==5 and len(set(subsets))==5;want=frozenset(z for z,v in zip(['I','II','III'],bits) if v);assert [a[':answer/id'] for a,z in zip(choices,subsets) if z==want]==[field[':answer-field/correct'][1]];C['choice_subsets']+=5;C['criterion_pairs']+=10
 conclusion=re.search(r'correct answer is "(.*?)"',sol)
 if conclusion:assert subset(conclusion[1])==want
 family=rec['generation']['template'];source=originals.get(family,{}).get(':question/worked-solution')
 if source:
  clean=lambda z:re.sub(r'\s+',' ',re.sub(r'\$.*?\$','',z)).strip();assert clean(sol)==clean(source);C['source_prose_masks']+=1
 im=np.array(Image.open(png).convert('RGB'));red=(im[:,:,0]>170)&(im[:,:,1]<120)&(im[:,:,2]<120);black=(im[:,:,0]<90)&(im[:,:,1]<90)&(im[:,:,2]<90);lo,hi=data['xlim'];yl,yh=data['ylim'];left,bottom,width,height=data['axes_bbox_pixels'];assert lo<0<hi and yl<0<yh;ax=left-lo/(hi-lo)*width;ay=im.shape[0]-(bottom-yl/(yh-yl)*height);assert abs(black.sum(0).argmax()-ax)<3 and abs(black.sum(1).argmax()-ay)<3;C['true_zero_axes']+=2
 fn=s.lambdify(x,actual,'numpy')
 for X in np.linspace(lo,hi,73)[2:-2]:
  Y=float(fn(X))
  if not yl*.94<Y<yh*.94:continue
  px=left+(X-lo)/(hi-lo)*width;py=bottom+(Y-yl)/(yh-yl)*height
  if any(a-4<=px<=c+4 and b-4<=py<=d+4 for a,b,c,d in data['label_boxes_pixels']):continue
  px=round(px);py=round(im.shape[0]-py);assert red[py-4:py+5,px-4:px+5].any(),(family,X,Y);C['raster_curve_probes']+=1
 if data['marked_intercept']:assert actual.subs(x,0)!=0
 if q[':question/difficulty'].endswith('/hard'):assert len(roots)==4 and set('simple' if m==1 else 'even' if m%2==0 else 'odd' for m in roots.values())=={'simple','even','odd'}
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=11,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
