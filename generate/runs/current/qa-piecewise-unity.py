"""Root reads complete scalar banks, displayed component/sum chains and PNG traces."""
import hashlib,importlib.util,json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186162082;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);sys.modules[n]=m;spec.loader.exec_module(m);return m
G=mod('root_pw_unity',D.with_suffix('.py'));P=mod('root_pw_scalar',R/'ode-scalar-parser.py');F=mod('root_pw_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
def scalar(t):return P.scalar(t.strip().rstrip('.,').replace('&',''))
def mask(t):
 t=re.sub(r'!\[.*?\]\(.*?\)','@ASSET@',t);t=re.sub(r'\$\$.*?\$\$','@DISPLAY@',t,flags=re.S);return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',t)).strip()
C=dict(records=0,choice_values=0,bank_pairs=0,component_sides=0,sum_sides=0,source_prose_masks=0,native_curve_probes=0,native_axes=0,arc_sweeps=0)
rows=json.load(open(R/f'qa/{K}-sampled.json'))
for c in json.load(open(D/'source-cases.json')):
 rows.append(G.generate(c['level'],template=c['template'],parameters=c['parameters']))
 # Source expression masks must also work at changed parameters, not literal snapshots.
 p={k:str(s.Rational(v)*2) for k,v in c['parameters'].items()};rows.append(G.generate(c['level'],template=c['template'],parameters=p,profile=c['profile']))

def curves(t,p):
 if 'r' in p:
  r=float(p['r']);sweep=np.pi if t=='semi' else 3*np.pi/2 if t=='three_quarter' else np.pi/2
  lo=-np.pi/2 if t=='quarter_open' else 0;cy=1 if t=='semi' else 0
  u=np.linspace(lo,lo+sweep,61);cs=[np.column_stack([r*np.cos(u),cy+r*np.sin(u)])]
  pts=[[-r,1],[r,1]] if t=='semi' else [[0,-r],[r,-r]] if t=='three_quarter' else [[0,r],[r,0]] if t=='quarter_closed' else [[r,0],[0,r]]
  C['arc_sweeps']+=1
 else:
  a,b=float(p['a']),float(p['b']);cs=[]
  pts=[[0,0],[0,a],[b,0],[b,a]] if t=='three_segments' else [[-a,0],[0,float(p['h'])],[b,0]]
 for a,b in zip(pts,pts[1:]):cs.append(np.array(a)+np.linspace(0,1,61)[:,None]*(np.array(b)-a))
 return cs

def raster(path,t,p):
 path=Path(path);info=json.load(open(path.with_suffix('.json')));im=np.asarray(Image.open(path).convert('RGB'));H,W=im.shape[:2];assert (W,H)==(432,364)
 cs=curves(t,p);full=np.concatenate(cs);x0,x1=min(0,full[:,0].min()),max(0,full[:,0].max());y0,y1=min(0,full[:,1].min()),max(0,full[:,1].max());span=max(x1-x0,y1-y0,1);pad=.23*span
 xmin,xmax,ymin,ymax=x0-pad,x1+pad,y0-pad,y1+pad
 assert np.allclose(info['bounds'],[xmin,xmax,ymin,ymax]);scale=min(.87*432/(xmax-xmin),.82*364.8/(ymax-ymin));left=.07*432+(.87*432-(xmax-xmin)*scale)/2;bottom=.1*364.8+(.82*364.8-(ymax-ymin)*scale)/2
 blue=(im[:,:,2]>110)&(im[:,:,0]<100)&(im[:,:,1]<170);black=im.max(2)<100
 def pixel(x,y):return int(round(left+(x-xmin)*scale)),int(round(364.8-bottom-(y-ymin)*scale))
 for c in cs:
  for x,y in c:
   a,b=pixel(x,y);assert 3<=a<W-3 and 3<=b<H-3;assert blue[b-3:b+4,a-3:a+4].any(),(path,x,y,a,b);C['native_curve_probes']+=1
 ox,oy=pixel(0,0)
 for vert,j in [(True,ox),(False,oy)]:
  slab=black[:,max(0,j-3):j+4] if vert else black[max(0,j-3):j+4,:];assert slab.any(1 if vert else 0).sum()>min(H,W)*.1,(path,vert,j,slab.any(1 if vert else 0).sum(),scale);C['native_axes']+=1
 assert info['labels']==(['C_'+str(i+1) for i in range(len(cs))] if info['role']=='solution' else [])
for rec in rows:
 q,m=rec['question'],rec['generation'];p={k:s.Rational(v) for k,v in m['parameters'].items()};t=m['template']
 if 'r' in p:
  r=p['r'];Ls=[s.pi*r if t=='semi' else 3*s.pi*r/2 if t=='three_quarter' else s.pi*r/2,2*r if t=='semi' else r if t=='three_quarter' else s.sqrt(2)*r]
 elif t=='three_segments':Ls=[p['a'],s.sqrt(p['a']**2+p['b']**2),p['a']]
 else:Ls=[s.sqrt(p['a']**2+p['h']**2),s.sqrt(p['b']**2+p['h']**2)]
 total=s.simplify(sum(Ls));f=q[':question/answer-fields'][0];vals=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5 and sum(s.simplify(v-total)==0 for v in vals)==1
 for i,v in enumerate(vals):
  for w in vals[i+1:]:assert s.simplify(v-w)!=0;C['bank_pairs']+=1
 if ':answer-field/correct' in f:assert scalar(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))==total
 C['choice_values']+=5
 if not m.get('evidence_only'):
  expected=[total,Ls[0],sum(Ls[1:]),2*Ls[0]+sum(Ls[1:]),Ls[0]+2*sum(Ls[1:])]
  assert all(any(s.simplify(v-w)==0 for w in vals) for v in expected)
 sol=q.get(':question/worked-solution','');bs=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
 if sol:
  # Two shared facts, per-piece chains, final addition; three_segments combines C1=C3.
  assert len(bs)==5,(t,len(bs))
  for block in bs[2:-1]:
   ids=re.findall(r'\{C\}_\{(\d)\}',block);assert ids
   expected=Ls[int(ids[0])-1]
   for side in block.split('=')[1:]:
    if r'\int' in side:
     idx=re.search(r'\{C\}_\{(\d)\}',side);assert expected==Ls[int(idx[1])-1]
    else:
     side=re.sub(r'(?<![A-Za-z])r(?![A-Za-z])',str(p.get('r','r')),side);assert s.simplify(scalar(side)-expected)==0,(t,side,expected);C['component_sides']+=1
  for side in bs[-1].split('=')[1:]:assert s.simplify(scalar(side)-total)==0;C['sum_sides']+=1
  sid=next(c['source_id'] for c in json.load(open(D/'source-cases.json')) if c['template']==t)
  if ':question/worked-solution' in originals[sid]:assert mask(sol)==mask(originals[sid][':question/worked-solution']);C['source_prose_masks']+=1
 paths=re.findall(r'!\[.*?\]\((.*?)\)',q[':question/problem']+' '+sol)
 assert len(paths)==(2 if sol else 1)
 for path in paths:raster(path,t,p)
 C['records']+=1
out={'passed':True,'source_fidelity':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
