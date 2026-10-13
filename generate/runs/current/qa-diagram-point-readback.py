"""Root derives angle routes from raster labels/rays/arcs, then reads the math."""
import importlib.util,json,re,hashlib,math,subprocess
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186092273
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
P=load(R/'qa-polar-point-readback.py','diagram_p');H=load(R/'qa-sinusoidal-properties.py','diagram_source');g=load(ROOT/f'generate/scratch/{K}.py','diagram_g');p=P.p
class Replay:
 @staticmethod
 def generate(level,**kwargs):return g.generate('hard',**kwargs)
source=H.source(Replay,K)
def read(text,env=None):return P.read(text.replace(r'{\theta }_{B}','k'),env)
def pair(text):
 text=text.strip().rstrip('.,').removeprefix('(').removesuffix(')');parts=text.split(',');assert len(parts)==2;return tuple(read(v) for v in parts)
def same(a,b):return s.simplify(a-b)==0
def geometry(prompt):
 m=re.search(r'polar coordinates of the point \$A\$ are \$\((.*?),(.*?)\)',prompt);assert m,prompt;radius,alpha=map(read,m.groups());delta=read(re.search(r'm∠AOB\s*=\s*(.*?)\$',prompt)[1]);path=Path(re.search(r'!\[\]\((.*?)\)',prompt)[1]);meta=json.loads(path.with_suffix('.json').read_text());im=Image.open(path);pixels=np.array(im.convert('RGB'));height,width=pixels.shape[:2];assert [width,height]==meta['size_px'] and meta['sha256']==hashlib.sha256(path.read_bytes()).hexdigest();assert all(abs(v-160)<.02 for v in im.info['dpi'])
 T=np.array(meta['transform']);inv=np.linalg.inv(T);ox,oy=meta['origin_px'];assert np.allclose(T[:2,2],[ox,oy]) and abs(T[0,0]/T[1,1]-1)<1e-10
 blue=(pixels[:,:,2].astype(int)-pixels[:,:,0]>30)&(pixels[:,:,0]<100)&(pixels[:,:,1]>60)
 def hit(x,y,allow=3,axis=False):
  mask=np.max(pixels,axis=2)<90 if axis else blue
  px,py=(T@np.array([x,y,1]))[:2];ix,iy=round(px),round(height-py);return bool(mask[max(0,iy-allow):iy+allow+1,max(0,ix-allow):ix+allow+1].any())
 def near(a,b):return abs(math.atan2(math.sin(a-b),math.cos(a-b)))
 b0=meta['text_bboxes']['B'];bc=(inv@np.array([(b0[0]+b0[2])/2,(b0[1]+b0[3])/2,1]))[:2];beta_picture=math.atan2(bc[1],bc[0])%(2*math.pi);aa,dd=float(alpha),float(delta)
 candidates=[]
 for direction in [-1,1]:
  bb=aa+direction*dd
  arcscore=sum(hit(.30*math.cos(t),.30*math.sin(t)) for t in np.linspace(aa,bb,19)[1:-1])/17
  candidates.append((near(beta_picture,bb),arcscore,direction,bb))
 closest=min(v[0] for v in candidates);eligible=[v for v in candidates if v[0]<closest+.03];best=max(eligible,key=lambda v:v[1]);distance,arcscore,direction,bb=best;assert distance<.03 and arcscore>.9,(prompt,candidates)
 beta=s.simplify(alpha+direction*delta);assert 0<beta<2*s.pi
 # Distinct labels must belong to the actual dashed radial rays, not just
 # to the always-blue circumference at their expected angles.
 for label,ang in [('A',aa),('B',bb)]:
  hits=sum(hit(float(v)*math.cos(ang),float(v)*math.sin(ang),2,axis=label=='A' and aa==0) for v in np.linspace(.42,.93,31));assert hits>=12,(label,hits,meta)
  b=meta['text_bboxes'][label];point=(inv@np.array([(b[0]+b[2])/2,(b[1]+b[3])/2,1]))[:2];assert near(math.atan2(point[1],point[0]),ang)<(.18 if label=='A' and aa==0 else .03)
 for ang in np.linspace(.09,2*math.pi-.09,37):assert hit(math.cos(ang),math.sin(ang))
 # Recompute unmasked bounding-box clearance from actual blue raster ink.
 by,bx=np.where(blue)
 for label,b in meta['text_bboxes'].items():
  x0,y0,x1,y1=b;x0,y0,x1,y1=x0,height-y1,x1,height-y0
  assert 0<=x0<x1<width and 0<=y0<y1<height
  clear=np.hypot(np.maximum(np.maximum(x0-bx,bx-x1),0),np.maximum(np.maximum(y0-by,by-y1),0)).min();assert clear>=2,(label,clear)
 return radius,alpha,delta,direction,beta,path,arcscore
records=json.loads((R/f'qa/{K}-sampled.json').read_text());counts=dict(records=0,plot_rays=0,arc_samples=0,prose_radii=0,theta_equalities=0,coordinate_equalities=0,choices=0,blank_components=0,conclusions=0);plots=set();native=[]
for rec in records:
 q=rec['question'];radius,alpha,delta,direction,beta,path,arcscore=geometry(q[':question/problem']);plots.add(str(path));xy=(s.simplify(radius*s.cos(beta)),s.simplify(radius*s.sin(beta)));env={p.u:radius,p.v:beta,p.x:xy[0],p.y:xy[1],p.k:beta};sol=q[':question/worked-solution'];counts['plot_rays']+=2;counts['arc_samples']+=17
 assert ('counterclockwise' in sol or 'counter-clockwise' in sol)==(direction==1)
 for value in re.findall(r'circle of radius \$(.*?)\$',sol):assert same(read(value),radius);counts['prose_radii']+=1
 for value in re.findall(r'\$r=(.*?)\$',sol):assert same(read(value),radius);counts['prose_radii']+=1
 for value in re.findall(r'\$r=([^$]+)\$',sol):assert same(read(value),radius)
 at=re.search(r'coordinate of \$A\$ is \$(.*?)\$',sol);assert at and same(read(at[1]),alpha)
 polar=re.search(r'polar coordinates of \$B\$ are \$(.*?)\$',sol);assert polar and pair(polar[1])==(radius,beta)
 theta_block=re.search(r'\$\$\s*\{\\theta \}_\{B\}=(.*?)\$\$',sol,re.S);assert theta_block
 for term in theta_block[1].strip().rstrip('.').split('='):assert same(read(term),beta);counts['theta_equalities']+=1
 aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(aligned)==2
 for ix,block in enumerate(aligned):
  for row in block.split(r'\\'):
   lhs,rhs=row.replace('&','').split('=',1);assert not lhs.strip() or lhs.strip()==('x','y')[ix];assert same(read(rhs,env),xy[ix]);counts['coordinate_equalities']+=1
 end=re.search(r'Cartesian coordinates of \$B\$ are \$(.*?)\$',sol);assert end and pair(end[1])==xy;counts['conclusions']+=1
 checks=[]
 for fi,f in enumerate(q[':question/answer-fields']):
  if f[':answer-field/type'].endswith('/blank'):
   ix=0 if f[':answer-field/key']=='field-1' else 1;assert read(f[':answer-field/choices'][0][':answer/value'])==xy[ix];counts['blank_components']+=1
   checks += [dict(field_index=fi,submitted=s.sstr(radius)+'*('+s.sstr((s.cos(beta),s.sin(beta))[ix])+')',expected='accepted',purpose='unreduced shared radius times target trig value'),dict(field_index=fi,submitted=s.sstr(xy[ix]+1),expected='rejected',purpose='wrong coordinate')]
  else:
   x,y=xy;expected=[xy,(s.simplify(radius*s.cos(alpha)),s.simplify(radius*s.sin(alpha))),(-x,y),(x,-y),(s.cos(beta),s.sin(beta))] if alpha==0 else [xy,(s.simplify(radius*s.cos(alpha-direction*delta)),s.simplify(radius*s.sin(alpha-direction*delta))),(s.simplify(radius*s.cos(alpha)),s.simplify(radius*s.sin(alpha))),(-x,y),(x,-y)]
   vals=[pair(v[':answer/value']) for v in f[':answer-field/choices']];assert set(vals)==set(expected) and len(set(vals))==5
   for val,choice in zip(vals,f[':answer-field/choices']):assert (val==xy)==(choice[':answer/id']==f[':answer-field/correct'][1]);counts['choices']+=1
 if checks:native.append(dict(label=q[':question/id'],record=rec,checks=checks))
 counts['records']+=1
ip=R/f'qa/{K}-root-equivalent-input.json';op=R/f'qa/{K}-root-equivalent-report.json';ip.write_text(json.dumps(native,indent=2)+'\n');subprocess.run([str(R/'check-engine'),str(ip),str(op)],check=True)
report=dict(status='passed',kp_id=K,source=source,readback=counts,unique_current_rasters=len(plots),native_typed_equivalents=str(op),script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
