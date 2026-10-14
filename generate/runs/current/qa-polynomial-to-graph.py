"""Root full polynomial-to-graph banks, source prose and actual plot pixels."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186129147;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_ptg_parser');x=p.x;g=load(D.with_suffix('.py'),'root_ptg_g');f=load(R/'root-source-fidelity.py','root_ptg_fid');originals,S=f.check(g,K,D,asset_relocation=True)
def signature(expr):
 roots=s.roots(expr,x);assert sum(roots.values())==s.degree(expr,x)
 return tuple((r,'simple' if m==1 else 'even' if m%2==0 else 'odd') for r,m in sorted(roots.items())),s.sign(s.Poly(expr,x).LC())
def coordinates(z):
 out=[]
 for t in z.split(','):
  t=t.strip()
  if t.startswith(r'\pm'):v=p.scalar(t[3:]);out.extend([-v,v])
  else:out.append(p.scalar(t))
 return out
C=dict(records=0,prompt_polynomials=0,actual_panel_functions=0,all_graph_criterion_pairs=0,root_derivative_orders=0,solution_multiplicity_operands=0,solution_end_behaviors=0,source_prose_masks=0,actual_sample_values=0,actual_zoom_values=0,raster_curve_probes=0,choice_values=0)
records=json.load(open(R/f'qa/{K}-sampled.json'));records.extend(g.generate(d['level'],template=t,seed=n) for t,d in g.DATA.items() for n in (631,917))
for rec in records:
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];actual=p.scalar(re.search(r'\$y=(.*?)\$',prompt)[1].rstrip('?').replace('{)}',')'));want=signature(actual);roots=s.roots(actual,x);C['prompt_polynomials']+=1
 plot=rec['generation']['plot'];assert plot['sidecar'];data=json.load(open(plot['sidecar']));panels=data['panels'];assert len(panels)==4
 signatures=[]
 image=np.array(Image.open(plot['prompt']).convert('RGB'));assert tuple(data['pixel_size'])==(image.shape[1],image.shape[0]);red=(image[:,:,0]>170)&(image[:,:,1]<110)&(image[:,:,2]<110)
 for index,panel in enumerate(panels):
  expr=s.sympify(panel['expression'],locals={'x':x});sig=signature(expr);signatures.append(sig);C['actual_panel_functions']+=1
  assert panel['label']==['I','II','III','IV'][index]
  for root,multiplicity in s.roots(expr,x).items():
   assert all(s.diff(expr,x,k).subs(x,root)==0 for k in range(multiplicity));assert s.diff(expr,x,multiplicity).subs(x,root)!=0;C['root_derivative_orders']+=multiplicity+1
  fn=s.lambdify(x,expr,'numpy');xx=np.asarray(panel['sample_x']);yy=np.asarray(panel['sample_y']);assert np.allclose(fn(xx),yy,rtol=1e-10,atol=1e-7);C['actual_sample_values']+=len(xx)
  for zoom in panel['zooms']:
   zx=np.asarray(zoom['x']);zy=np.asarray(zoom['y']);assert np.allclose(fn(zx),zy,rtol=1e-10,atol=1e-7);assert zoom['root'] in roots;C['actual_zoom_values']+=len(zx)
  # Independently reconstruct fixed Figure subplot positions (not sidecar).
  col=index%2;row=index//2;left=.125+col*(.775/2.2)*1.2;width=.775/2.2;bottom=.53 if row==0 else .11;height=.35;bottom+=height*.3;height*=.7
  lo,hi=panel['xlim'];yl,yh=panel['ylim']
  for X,Y in zip(xx[25:-25:95],yy[25:-25:95]):
   if not yl*.93<Y<yh*.93:continue
   px=round(image.shape[1]*(left+(X-lo)/(hi-lo)*width));py=round(image.shape[0]*(1-(bottom+(Y-yl)/(yh-yl)*height)));axis_y=image.shape[0]*(1-(bottom-yl/(yh-yl)*height))
   if abs(py-axis_y)<3:continue # black zero-axis legitimately occludes flat red curve
   assert red[py-5:py+6,px-5:px+6].any(),(family,index,X,Y,px,py);C['raster_curve_probes']+=1
  for n,zoom in enumerate(panel['zooms']):
   zleft=left+n*width/len(panel['zooms'])+.015;zwidth=width/len(panel['zooms'])-.03;zbottom=(.53 if row==0 else .11)+.02;zheight=.35*.21;zl,zh=zoom['x'][0],zoom['x'][-1];zylo,zyhi=zoom['ylim']
   for X,Y in zip(zoom['x'][30:-30:65],zoom['y'][30:-30:65]):
    px=round(image.shape[1]*(zleft+(X-zl)/(zh-zl)*zwidth));py=round(image.shape[0]*(1-(zbottom+(Y-zylo)/(zyhi-zylo)*zheight)));assert red[py-4:py+5,px-4:px+5].any(),('zoom',family,index,n,px,py);C['raster_curve_probes']+=1
 assert len(set(signatures))==4 and signatures.count(want)==1;C['all_graph_criterion_pairs']+=6;correct=['I','II','III','IV'][signatures.index(want)]
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];assert len(choices)==5;assert {a[':answer/value'] for a in choices}=={r'\text{'+v+'}' for v in ['I','II','III','IV']}|{'None of the given graphs are correct'};assert next(a[':answer/value'] for a in choices if a[':answer/id']==field[':answer-field/correct'][1])==r'\text{'+correct+'}';C['choice_values']+=5
 described={}
 for zs,m in re.findall(r'multiplicity of the roots? \$x=([^$]+)\$ is \$([1-4]),\$',sol):
  for root in coordinates(zs):assert roots[root]==int(m);described[root]=int(m);C['solution_multiplicity_operands']+=1
 assert described==roots
 leading=s.Poly(actual,x).LC();assert ('coefficient is positive' in sol)==(leading>0);assert ('coefficient is negative' in sol)==(leading<0);end=s.oo if leading>0 else -s.oo;claimed=re.search(r'\$y\$ approaches \$(.*?) \.\$',sol);assert claimed;token=claimed[1].replace(r'\infty','INFINITY').replace(' ','');assert token==('INFINITY' if end==s.oo else '-INFINITY');assert 'graph $'+r'\text{'+correct+'}' in sol;C['solution_end_behaviors']+=1
 if family in originals:
  clean=lambda z:re.sub(r'coefficient is (positive|negative)','coefficient is <SIGN>',re.sub(r'\s+',' ',re.sub(r'\$.*?\$','',z))).strip();source=originals[family][':question/worked-solution'];assert clean(sol)==clean(source),(family,clean(sol),clean(source));C['source_prose_masks']+=1
 C['records']+=1
out=dict(status='passed',source=S,readback=C,original_assets_full_resolution=8,source_panel_labels='all I–IV present; false anomaly report corrected',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
