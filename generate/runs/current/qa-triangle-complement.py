"""Parent full-source and displayed enclosing-area/difference readback."""
import importlib.util,json,re,hashlib,math,os
from pathlib import Path
import sympy as s
from PIL import Image
os.environ.setdefault('MPLCONFIGDIR','/tmp/complement-root-mpl')
import matplotlib
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186105906
sp=importlib.util.spec_from_file_location('complementparser',R/'qa-gradients.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
def equal(a,b):return s.simplify(a-b)==0
def roundint(e):return int(s.floor(s.N(e,60)+s.Rational(1,2)))
def check():
 g=p.load(ROOT/f'generate/scratch/{K}.py','complementg');orig=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];counts=dict(prompts=0,solutions=0,values=0,keys=0)
 for c in json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text()):
  q0=next(q for q in orig if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));q=g.generate(c.get('level','hard'),template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile')))['question'];assert q[':question/problem']==q0[':question/problem'];counts['prompts']+=1
  for key in (':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in q0)
   if key in q:assert q[key]==(q0[key].get(':db/ident') if isinstance(q0[key],dict) else q0[key])
  counts['solutions']+=(':question/worked-solution' in q0);f=q[':question/answer-fields'][0];f0=q0[':question/answer-fields'][0];assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);counts['values']+=len(f[':answer-field/choices'])
  if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];counts['keys']+=1
 stats=dict(records=0,substituted_factors=0,product_rows=0,truncated_decimal_rows=0,rounded_outer_rows=0,difference_rows=0,choices=0,complete_method_banks=0,raster_edges=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];Q=int(re.search(r'area of \$ABCD\$ is \$(\d+)',prompt)[1]);blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);easy='enclosing' in prompt
  if easy:T=s.Integer(re.search(r'enclosing \$△ABD\$ is \$(\d+)',prompt)[1]);a=b=None;theta=90
  else:
   m=re.search(r'\\frac\{1\}\{2\}\\cdot ([\d.]+)\\cdot ([\d.]+)\\cdot \\operatorname\{sin\}⁡\{(\d+)\}',blocks[0]);assert m,sol;a,b=s.Rational(m[1]),s.Rational(m[2]);theta=int(m[3]);T=a*b*s.sin(s.pi*theta/180)/2;stats['substituted_factors']+=3
   product=re.search(r'&\s*=((?:\\frac\{1\}\{2\}\\cdot )?[\d.]+)\\cdot \\operatorname\{sin\}⁡\{(\d+)\}',blocks[0]);assert product and equal(p.scalar(product[1]),a*b/2) and int(product[2])==theta;stats['product_rows']+=1
   dec=re.search(r'&\s*=([\d.]+)…',blocks[0])
   if dec:assert s.Rational(dec[1])==s.floor(s.N(T,60)*1000)/1000;stats['truncated_decimal_rows']+=1
   rounded=re.search(r'≈(\d+)',blocks[0]);assert rounded and int(rounded[1])==roundint(T);stats['rounded_outer_rows']+=1
  R0=roundint(T);answer=R0-Q;assert answer>0
  m=re.search(r'&\s*=(\d+)-(\d+)',blocks[-1]);assert m and [int(m[1]),int(m[2])]==[R0,Q];final=re.search(r'&\s*=(\d+)\{',blocks[-1]);assert final and int(final[1])==answer;stats['difference_rows']+=1
  f=q[':question/answer-fields'][0];vals=[int(re.match(r'\d+',a[':answer/value'])[0]) for a in f[':answer-field/choices']]
  for opt,v in zip(f[':answer-field/choices'],vals):assert (v==answer)==(opt[':answer/id']==f[':answer-field/correct'][1]);stats['choices']+=1
  if len(vals)>1:
   expected=[answer,R0,R0+Q,Q,roundint(s.Rational(answer,2))] if easy else [answer,R0,R0+Q,roundint(2*T)-Q,roundint(T-s.Rational(Q,2)) if theta==90 else roundint(a*b/2)-Q];assert sorted(vals)==sorted(expected) and len(set(vals))==5;stats['complete_method_banks']+=1
  path=Path(re.search(r'!\[\]\((.*?)\)',prompt)[1]);spec=json.loads(path.with_suffix('.json').read_text());v=spec['vertices'];A,B,C,D=[v[z] for z in 'ABCD'];cross=lambda P,U,V:abs((U[0]-P[0])*(V[1]-P[1])-(U[1]-P[1])*(V[0]-P[0]))/2;outer=cross(A,B,D);target=cross(B,C,D);quad=cross(A,B,C)+cross(A,C,D);assert abs(outer-float(T))<1e-8 and abs(quad-Q)<1e-8 and abs(target-(float(T)-Q))<1e-8
  if not easy:
   assert abs(math.dist(A,B)-float(a))<1e-8 and abs(math.dist(A,D)-float(b))<1e-8;ang=math.degrees(math.acos(sum((B[z]-A[z])*(D[z]-A[z]) for z in (0,1))/(float(a)*float(b))));assert abs(ang-theta)<1e-8
  # Derive the axes transform independently from canvas/default subplot bounds
  # and the renderer's explicit geometric margins; verify actual PNG strokes.
  im=Image.open(path).convert('RGB');width,height=im.size;params=spec['parameters'];scale=max(params['a'],params['b']);xs=[xy[0] for xy in v.values()];ys=[xy[1] for xy in v.values()];xmin=min(xs)-.3*scale;xmax=max(xs)+.3*scale;ymin=min(ys)-.25*scale;ymax=max(ys)+.25*scale;left=width*matplotlib.rcParams['figure.subplot.left'];bottom=height*matplotlib.rcParams['figure.subplot.bottom'];w=width*(matplotlib.rcParams['figure.subplot.right']-matplotlib.rcParams['figure.subplot.left']);h=height*(matplotlib.rcParams['figure.subplot.top']-matplotlib.rcParams['figure.subplot.bottom']);ratio=min(w/(xmax-xmin),h/(ymax-ymin));left+=(w-ratio*(xmax-xmin))/2;bottom+=(h-ratio*(ymax-ymin))/2
  for pair in ('AB','BC','CD','DA'):
   U,V=[v[z] for z in pair];hits=0
   for frac in (.25,.37,.63,.75):
    xy=[U[z]+frac*(V[z]-U[z]) for z in (0,1)];px=round(left+(xy[0]-xmin)*ratio);py=round(height-bottom-(xy[1]-ymin)*ratio);hits+=any(max(im.getpixel((x,y)))<100 for x in range(max(0,px-3),min(width,px+4)) for y in range(max(0,py-3),min(height,py+4)))
   assert hits>=3,(path,pair,hits);stats['raster_edges']+=1
  stats['records']+=1
 out=dict(status='passed',kp_id=K,source=counts,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
