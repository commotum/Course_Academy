"""Parent diagram/math readback, independent of the triangle generator helpers."""
import importlib.util,json,re,hashlib,math
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
import sympy as s
from PIL import Image
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186105903
def rnd(e,d):return format(Decimal(str(s.N(e,60))).quantize(Decimal(10)**-d,rounding=ROUND_HALF_UP),f'.{d}f')
def check():
 stats=dict(records=0,individual_side_angle_inputs=0,half_product_rows=0,sine_rows=0,choices=0,complete_method_banks=0,raster_edges=0,hard_angle_sums=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];sol=q[':question/worked-solution'];m=re.search(r'[cс]\s*&\s*=AB=([\d.]+)',sol);assert m,sol;u=s.Rational(m[1]);m=re.search(r'[ab]\s*&\s*=(AC|BC)=([\d.]+)',sol);assert m,sol;edge=m[1];v=s.Rational(m[2]);m=re.search(r'm∠([AB])\s*&\s*=\{(\d+)\}',sol);assert m,sol;vertex=m[1];angle=int(m[2]);assert edge==('AC' if vertex=='A' else 'BC');stats['individual_side_angle_inputs']+=3
  m=re.search(r'where \$∠([AB])\$ is between the sides of lengths \$([ab])\$ and \$c',sol);assert m and m[1]==vertex and m[2]==('b' if vertex=='A' else 'a')
  theta=s.pi*angle/180;A=u*v*s.sin(theta)/2;digits=1 if 'nearest tenth' in q[':question/problem'] else 2;answer=rnd(A,digits)
  half=re.search(r'&\s*=\s*([\d.]+)\\cdot\s*\(0\.(\d{3})\\,(\d{3})…?\)',sol)
  if half:assert s.Rational(half[1])==u*v/2;assert '0.'+half[2]+half[3]==rnd(s.sin(theta),6);stats['half_product_rows']+=1
  sine=re.search(r'\\operatorname\{sin\}⁡\{(\d+)\}\^\{∘\}=(0\.\d{3}\\,\d{3})',sol)
  if sine:
   value=sine[2].strip().rstrip(',.').replace(r'\,','');assert int(sine[1])==angle and value==rnd(s.sin(theta),6),(angle,value);stats['sine_rows']+=1
  final=re.search(r'≈\s*([\d.]+)',sol);assert final and final[1].rstrip('.')==answer,(final,answer)
  f=q[':question/answer-fields'][0];values=[a[':answer/value'] for a in f[':answer-field/choices']];correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==answer
  if f[':answer-field/type'].endswith('/radio'):
   expected=[rnd(e,2) for e in [A,2*A,u*v/2,u*v*s.Abs(s.cos(theta))/2,u*v*s.sin(theta)**2/2]];assert sorted(values)==sorted(expected) and len(set(values))==5;stats['complete_method_banks']+=1
  stats['choices']+=len(values)
  plot=r['generation']['plot'];pts=plot['vertices'];index={v:i for i,v in enumerate(plot['vertex_labels'])};P,Q,T=[pts[index[v0]] for v0 in [vertex,'B' if vertex=='A' else 'A','C']];a=[Q[j]-P[j] for j in (0,1)];b=[T[j]-P[j] for j in (0,1)];assert abs(math.hypot(*a)-float(u))<1e-8 and abs(math.hypot(*b)-float(v))<1e-8;measured=math.degrees(math.acos(sum(a[j]*b[j] for j in (0,1))/(float(u)*float(v))));assert abs(measured-angle)<1e-8
  texts=[t[2] for t in plot['labels']]
  lengths=[s.Rational(z.replace(' ft','')) for z in texts if re.fullmatch(r'[\d.]+(?: ft)?',z)];assert sorted(lengths)==sorted([u,v])
  if r['generation']['template']=='angle_sum':
   given=[int(z[:-1]) for z in texts if z.endswith('°')];assert len(given)==2 and sum(given)+angle==180 and given[0]==given[1] and u==v;stage=re.search(r'm∠B=180\^\{\\circ\}-(\d+)\^\{\\circ\}-(\d+)\^\{\\circ\}=(\d+)\^\{\\circ\}',sol);assert stage and [int(stage[1]),int(stage[2])]==given and int(stage[3])==angle;stats['hard_angle_sums']+=1
  else:assert [z for z in texts if z.endswith('°')]==[str(angle)+'°']
  path=Path(re.search(r'!\[.*?\]\((.*?)\)',q[':question/problem'])[1]);assert hashlib.sha256(path.read_bytes()).hexdigest()==plot['png_sha256'];im=Image.open(path).convert('RGB');width,height=im.size;assert [width,height]==plot['canvas_pixels']
  # Reconstruct data-to-raster coordinates from unmasked data/label bounds and
  # measured axes. Sample each actual black edge away from labels/sectors.
  pad=.15*max(float(u),float(v));coords=pts+[[x,y] for x,y,_ in plot['labels']];xmin=min(z[0] for z in coords)-pad;xmax=max(z[0] for z in coords)+pad;ymin=min(z[1] for z in coords)-pad;ymax=max(z[1] for z in coords)+pad;left,bottom,w,h=plot['axes_bounds_pixels'];sx=w/(xmax-xmin);sy=h/(ymax-ymin);assert abs(sx-sy)<1e-7
  transform=lambda xy:(left+(xy[0]-xmin)*sx,height-(bottom+(xy[1]-ymin)*sy))
  for i,j in ((0,1),(1,2),(2,0)):
   hits=0
   for frac in (.25,.37,.63,.75):
    pos=transform([pts[i][z]*(1-frac)+pts[j][z]*frac for z in (0,1)]);px,py=map(round,pos);hits+=any(max(im.getpixel((xx,yy)))<90 for xx in range(max(0,px-3),min(width,px+4)) for yy in range(max(0,py-3),min(height,py+4)))
   assert hits>=3,(path,i,j,hits);stats['raster_edges']+=1
  stats['records']+=1
 out=dict(status='passed',kp_id=K,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
