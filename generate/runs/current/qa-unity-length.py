"""Root validates displayed geometric length banks/stages and native PNG traces."""
import hashlib,importlib.util,json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186162081;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);sys.modules[n]=m;spec.loader.exec_module(m);return m
G=mod('root_unity',D.with_suffix('.py'));P=mod('root_unity_parser',R/'ode-scalar-parser.py');F=mod('root_unity_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
def scalar(t):return P.scalar(t.strip().rstrip('.,:').replace('&',''))
def mask(t):
 t=re.sub(r'!\[.*?\]\(.*?\)','@ASSET@',t);t=re.sub(r'\$\$.*?\$\$','@DISPLAY@',t,flags=re.S);return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',t)).strip()
C=dict(records=0,choice_values=0,whole_bank_pairs=0,operative_sides=0,source_solution_masks=0,native_curve_probes=0,native_helper_probes=0,native_axes=0)
rows=json.load(open(R/f'qa/{K}-sampled.json'))
# Explicit coverage supplements the random sample, particularly the semicircle.
for t,p in [('semicircle',{'r':3}),('horizontal',dict(x1=1,y1=-2,x2=5,y2=-2)),('diagonal_helper',dict(x1=-1,y1=-1,x2=3,y2=1))]:rows.append(G.generate('easy',template=t,parameters=p))
for c in json.load(open(D/'source-cases.json')):
 p={k:str(s.Rational(v)*2) for k,v in c['parameters'].items()};rows.append(G.generate('easy',template=c['template'],parameters=p,profile=c['bank_profile']))

def raster(path,t,p,helper=False):
 path=Path(path);info=json.load(open(path.with_suffix('.json')));im=np.asarray(Image.open(path).convert('RGB'));H,W=im.shape[:2];assert [W,H]==[540,456];assert info['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
 A=np.array(info['data_transform']);assert abs(A[0,0]-A[1,1])<.001 and abs(A[0,1])+abs(A[1,0])<.001
 blue=(im[:,:,2]>110)&(im[:,:,0]<100)&(im[:,:,1]<160);black=im.max(2)<100
 def pixel(x,y):
  v=A@np.array([float(x),float(y),1]);return int(round(v[0])),int(round(H-v[1]))
 def probe(x,y):
  a,b=pixel(x,y);assert 3<=a<W-3 and 3<=b<H-3
  return bool(blue[b-3:b+4,a-3:a+4].any())
 if t=='semicircle':
  r=p['r'];points=[(float(r)*np.cos(u),float(r)*np.sin(u)) for u in np.linspace(0,np.pi,31)]
 else:points=[(p['x1']+u*(p['x2']-p['x1']),p['y1']+u*(p['y2']-p['y1'])) for u in np.linspace(0,1,31)]
 for x,y in points:assert probe(x,y),(path,'missing visible blue curve',x,y);C['native_curve_probes']+=1
 if helper:
  # Recover the two source right-triangle legs independently from endpoints.
  h=[probe(p['x1']+u*(p['x2']-p['x1']),p['y1']) for u in np.linspace(.05,.95,41)]
  v=[probe(p['x2'],p['y1']+u*(p['y2']-p['y1'])) for u in np.linspace(.05,.95,41)]
  assert sum(h)>12 and sum(v)>12,(path,'missing dashed helper legs');C['native_helper_probes']+=sum(h)+sum(v)
 ox,oy=pixel(0,0)
 for vert,j in [(True,ox),(False,oy)]:
  slab=black[:,max(0,j-1):j+2] if vert else black[max(0,j-1):j+2,:]
  assert slab.any(1 if vert else 0).sum()>min(H,W)*.1;C['native_axes']+=1
for r in rows:
 q,m=r['question'],r['generation'];t=m['template'];p={k:s.Rational(v) for k,v in m['parameters'].items()}
 if t=='semicircle':L=s.pi*p['r']
 else:a=abs(p['x2']-p['x1']);b=abs(p['y2']-p['y1']);L=s.sqrt(a*a+b*b)
 f=q[':question/answer-fields'][0];vals=[scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vals)==5
 assert sum(s.simplify(v-L)==0 for v in vals)==1
 for i,v in enumerate(vals):
  for w in vals[i+1:]:assert s.simplify(v-w)!=0;C['whole_bank_pairs']+=1
 if ':answer-field/correct' in f:assert scalar(next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]))==L
 C['choice_values']+=5
 if not m['evidence_only']:
  if t=='semicircle':expected=[L,2*L,L/2,2*p['r'],s.pi*p['r']**2]
  elif t in ('horizontal','vertical'):
   lo,hi=sorted([p['y1'],p['y2']] if t=='vertical' else [p['x1'],p['x2']]);expected=[L,abs(hi+lo),abs(hi),abs(lo),L**2]
  else:expected=[L,a,b,a+b,a*a+b*b]
  assert all(any(s.simplify(z-v)==0 for z in vals) for v in expected)
  level=m['level']
  if level=='moderate':assert a.q==b.q==2
  if level=='hard':assert sorted([a.q,b.q])==[3,4]
 sol=q.get(':question/worked-solution','');blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
 if sol:
  assert len(blocks)==(2 if t in ('vertical','horizontal') else 3)
  final=blocks[-1].split('=')[-1];assert scalar(final)==L;C['operative_sides']+=1
  if t.startswith('diagonal'):
   z=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','');parts=z.split(chr(92)*2);assert len(parts)==4
   for row in parts:assert scalar(row.split('=')[1])==L;C['operative_sides']+=1
   intro=re.search(r'legs have lengths \$([^$]+)\$ and \$([^$]+)',sol);assert intro and scalar(intro[1])==b and scalar(intro[2])==a
   assert '^' in parts[0] and '+' in parts[1] and '+' not in parts[2]
  if t=='semicircle':assert scalar(blocks[1].split('=')[-1].replace(r'\end{aligned}',''))==L;C['operative_sides']+=1
  if t!='semicircle':
   source=originals[next(c['source_id'] for c in json.load(open(D/'source-cases.json')) if c['template']==t)];assert mask(sol)==mask(source[':question/worked-solution']);C['source_solution_masks']+=1
 refs=re.findall(r'!\[.*?\]\((.*?)\)',q[':question/problem']+' '+sol)
 for i,path in enumerate(refs):raster(path,t,p,i==1)
 C['records']+=1
out={'passed':True,'source_fidelity':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0}
(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
