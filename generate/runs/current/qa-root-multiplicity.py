"""Root actual categorical choices, solution targets and rendered functions."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186129253;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_mult_parse');x=s.Symbol('x');g=load(D.with_suffix('.py'),'root_mult_g');f=load(R/'root-source-fidelity.py','root_mult_fid');originals,S=f.check(g,K,D,asset_relocation=True)
C=dict(records=0,actual_choice_predicates=0,criterion_pairs=0,solution_target_operands=0,source_prose_masks=0,actual_curve_values=0,root_derivative_orders=0,raster_curve_probes=0,actual_zero_axes=0)
records=json.load(open(R/f'qa/{K}-sampled.json'))
records.extend(g.generate('easy',profile='completed-'+sid,parameters={'roots':[r+1],'multiplicities':[m],'orientation':o,'target':0}) for sid,(r,m,o) in g.SOURCE_DATA.items() if abs(r+1)<=9)
base=originals['q-141133'][':question/worked-solution'].split('\n\nIn our case,')[0]
for rec in records:
 q=rec['question'];sol=q[':question/worked-solution'];field=q[':question/answer-fields'][0];options=field[':answer-field/choices'];assert len(options)==5
 targets=[];kinds=[]
 for a in options:
  m=re.fullmatch(r'\$x\s*=\s*(.*?)\$ (.*)',a[':answer/value']);assert m;targets.append(p.scalar(m[1]));tail=m[2]
  kinds.append({'is a simple root':'simple','is a multiple root of even multiplicity':'even','is a multiple root of odd multiplicity':'odd','is not a root of $p(x)$':'not','is a simple root of even multiplicity':'impossible'}[tail]);C['actual_choice_predicates']+=1
 assert len(set(targets))==1 and set(kinds)=={'simple','even','odd','not','impossible'};C['criterion_pairs']+=10;target=targets[0]
 assert sol.startswith(base);C['source_prose_masks']+=1
 tail=sol[len(base):];mentions=re.findall(r'\$x=(.*?)(?:,|\.)?\$',tail);assert mentions and all(p.scalar(z.rstrip('.,'))==target for z in mentions);C['solution_target_operands']+=len(mentions)
 plot=rec['generation']['plot_data']
 if plot is None:
  sid=rec['generation']['bank_profile'].removeprefix('completed-');assert sid in originals;category={'q-140411':'simple','q-140414':'even','q-141133':'odd','q-141137':'odd','q-141142':'odd','q-141144':'even','q-141140':'simple'}[sid]
 else:
  actual=s.sympify(plot['polynomial'],locals={'x':x});poly=s.Poly(actual,x);roots=s.roots(actual,x);assert target in roots;order=roots[target];category='simple' if order==1 else 'even' if order%2==0 else 'odd'
  for k in range(order):assert s.diff(actual,x,k).subs(x,target)==0;C['root_derivative_orders']+=1
  assert s.diff(actual,x,order).subs(x,target)!=0;C['root_derivative_orders']+=1
  png=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]);im=np.array(Image.open(png).convert('RGB'));assert hashlib.sha256(png.read_bytes()).hexdigest()==plot['png_sha256'];red=(im[:,:,0]>160)&(im[:,:,1]<110)&(im[:,:,2]<110);black=(im[:,:,0]<90)&(im[:,:,1]<90)&(im[:,:,2]<90);fn=s.lambdify(x,actual,'numpy')
  for panel in plot['panels']:
   lo,hi=panel['xlim'];yl,yh=panel['ylim'];left,bottom,width,height=panel['axes_pixel_bounds'];assert abs(panel['zero_pixel_y']-(bottom-height*yl/(yh-yl)))<1e-8;C['actual_zero_axes']+=1
   vertices=np.array(panel['vertices']);assert np.allclose(fn(vertices[:,0]),vertices[:,1],rtol=1e-10,atol=1e-7);C['actual_curve_values']+=len(vertices)
   for xx,yy in vertices[20:-20:85]:
    if not yl<yy<yh:continue
    px=round(left+(xx-lo)/(hi-lo)*width);py=round(im.shape[0]-(bottom+(yy-yl)/(yh-yl)*height));assert red[max(0,py-4):py+5,max(0,px-4):px+5].any(),(png,panel['role'],xx,yy);C['raster_curve_probes']+=1
   py=round(im.shape[0]-panel['zero_pixel_y']);assert black[py-2:py+3,int(left):int(left+width)].sum()>width*.25
  # Authored levels read one target only, from 2 integer or 3 half-integer roots.
  level=q[':question/difficulty'].split('/')[-1]
  if level!='easy':assert len(roots)==(2 if level=='moderate' else 3) and all(z.q==(1 if level=='moderate' else 2) for z in roots)
 correct=next(a for a in options if a[':answer/id']==field[':answer-field/correct'][1]);assert kinds[options.index(correct)]==category
 assert ('*not* tangent' in tail)==(category=='simple')
 if category=='even':assert 'reverses direction' in tail and '*even*' in tail
 if category=='odd':assert 'crosses' in tail and '*odd*' in tail
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=14,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
