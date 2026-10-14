"""Root visible markers/asymptotes, every response set and actual origin pixels."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186068696;D=R.parents[2]/f'generate/scratch/{K}'
def load(p,n):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
fidelity=load(R/'root-source-fidelity.py','discontinuity_fidelity');g=load(D.with_suffix('.py'),'discontinuity_generator');originals,S=fidelity.check(g,K,D)
def coordset(text):
 text=text.replace('$','').replace(r'\pm','±').replace(chr(92)*2+'pm','±')
 if '±' in text:
  n=s.Rational(re.search(r'±\s*(\d+(?:\.\d+)?)',text)[1]);return frozenset((-n,n))
 return frozenset(s.Rational(z) for z in re.findall(r'(?<![a-zA-Z])-?\d+(?:\.\d+)?',text))
def discontinuities(geom):
 # An excluded finite curve point or a vertical asymptote breaks these captured
 # functions; filled singleton values never restore an unequal curve limit.
 result={s.Rational(str(v)) for v in geom.get('vertical_asymptotes',[])}
 for marker in geom['markers']:
  if marker['kind']=='open':result.add(s.Rational(str(marker['x'])))
 return frozenset(result)
C=dict(records=0,actual_graphs=0,actual_markers=0,actual_asymptotes=0,choices=0,criterion_pairs=0,conclusion_coordinates=0,full_shared_prose_masks=0,raster_markers=0,actual_zero_axis_intersections=0,authored_half_unit_guards=0,original_markers=0,original_asset_hashes=0)
for asset,geom in g.PLOTS.items():
 path=g.ASSET_ROOT/asset;assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==geom['sha256'];C['original_asset_hashes']+=1
 assert discontinuities(geom)==frozenset(s.Rational(str(v)) for v in geom['breaks']);C['original_markers']+=len(geom['markers'])
records=json.load(open(R/f'qa/{K}-sampled.json'));records+=json.load(open(D/'zero-axes-review.json'))
for rec in records:
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];level=q[':question/difficulty'].split('/')[-1]
 paths=[];expected=None
 if family=='select_graph':
  requested=coordset(prompt);assert len(requested)==1
  f=q[':question/answer-fields'][0];flags=[];graphs=[]
  for a in f[':answer-field/choices']:
   paths.append(a[':answer/value']);geom=json.load(open(Path(paths[-1]).with_suffix('.json')))['geometry'];graphs.append(geom);flags.append(requested<=discontinuities(geom))
  assert sum(flags)==1 and [a[':answer/id'] for a,flag in zip(f[':answer-field/choices'],flags) if flag]==[f[':answer-field/correct'][1]]
  # The complete graphs have distinct traced functions or point domains.
  for a,b in itertools.combinations(graphs,2):assert a['curves']!=b['curves'] or a['markers']!=b['markers'] or a['vertical_asymptotes']!=b['vertical_asymptotes'];C['criterion_pairs']+=1
  assert coordset(sol.split('\n\n')[0])==requested;C['conclusion_coordinates']+=len(requested);C['choices']+=5
 else:
  paths=re.findall(r'!\[\]\((.*?)\)',prompt);assert len(paths)==1;geom=json.load(open(Path(paths[0]).with_suffix('.json')))['geometry'];expected=discontinuities(geom);assert expected
  fields=q[':question/answer-fields']
  if all(f[':answer-field/type'].endswith('/blank') for f in fields):
   values=[]
   for f in fields:
    assert '{{'+f[':answer-field/key']+'}}' in prompt;assert len(f[':answer-field/choices'])==1;values.append(s.Rational(f[':answer-field/choices'][0][':answer/value']));C['choices']+=1
   assert frozenset(values)==expected and values==sorted(values)
  else:
   for f in fields:
    values=[coordset(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(values))==len(values)==5
    assert [a[':answer/id'] for a,vals in zip(f[':answer-field/choices'],values) if vals==expected]==[f[':answer-field/correct'][1]];C['choices']+=5
    for a,b in itertools.combinations(values,2):assert a!=b;C['criterion_pairs']+=1
    ordered=tuple(sorted(expected))
    if len(ordered)==3:want=[ordered,ordered[1:],(ordered[0],ordered[2]),ordered[:2],(ordered[1],)]
    elif len(ordered)==2:a,b=ordered;want=[ordered,(a,),(b,),(a,b+1),(b,b+1)]
    else:raise AssertionError('unsupported whole-bank workload')
    assert set(values)=={frozenset(v) for v in want}
  assert coordset(sol.split('\n\n')[0])==expected
  if 'Therefore' in sol:assert coordset(sol.split('Therefore',1)[1])==expected
  C['conclusion_coordinates']+=len(expected)
  if level!='easy':
   vals=sorted(expected);assert len(vals)==3 and vals[0]<0<vals[-1] and min(b-a for a,b in zip(vals,vals[1:]))>=s.Rational(3,2);assert sum(v.q==2 for v in vals)==(1 if level=='moderate' else 2);C['authored_half_unit_guards']+=1
 if level=='easy':
  profile=rec['generation']['profile'];sid=profile.split(':',1)[1];original=originals[sid][':question/worked-solution'];clean=lambda z:re.sub(r'\s+',' ',re.sub(r'!\[\]\([^)]+\)|\$[^$]*\$','',z)).strip();assert clean(sol)==clean(original);C['full_shared_prose_masks']+=1
 for path in set(paths):
  side=json.load(open(Path(path).with_suffix('.json')));geom=side['geometry'];axes=side['axes'];lo,hi=axes['xlim'];bot,top=axes['ylim'];assert lo<0<hi and bot<0<top;assert side['png_sha256']==hashlib.sha256(Path(path).read_bytes()).hexdigest()
  C['actual_graphs']+=1;C['actual_markers']+=len(geom['markers']);C['actual_asymptotes']+=len(geom.get('vertical_asymptotes',[]))
  arr=np.array(Image.open(path).convert('RGB'));height,width=arr.shape[:2];left,bottom,pw,ph=axes['pixel_bounds']
  def pixel(xx,yy):return round(left+(xx-lo)*pw/(hi-lo)),round(height-bottom-(yy-bot)*ph/(top-bot))
  ox,oy=pixel(0,0);black=(arr[:,:,0]<90)&(arr[:,:,1]<90)&(arr[:,:,2]<90)
  assert black[oy-2:oy+3,ox+10:ox+26].sum()>6 and black[oy+10:oy+26,ox-2:ox+3].sum()>6,(path,ox,oy,'axes away from point-marker occlusion');C['actual_zero_axis_intersections']+=1
  colored=((arr[:,:,0]>140)&(arr[:,:,1]<140)&(arr[:,:,2]<140))|((arr[:,:,2]>140)&(arr[:,:,0]<120)&(arr[:,:,1]<120))
  for marker in geom['markers']:
   yy=marker.get('y',(geom.get('origin_pixel',[0,0])[1]-marker.get('y_pixel',0))/geom.get('pixels_per_x_unit',1));px,py=pixel(marker['x'],yy);assert 8<px<width-8 and 8<py<height-8
   center=colored[py-1:py+2,px-1:px+2].sum();ring=colored[py-7:py+8,px-7:px+8].sum();assert ring>=12 and (center<=3 if marker['kind']=='open' else center>=5);C['raster_markers']+=1
 C['records']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
