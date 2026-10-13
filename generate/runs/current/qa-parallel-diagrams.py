"""Root reads displayed relations, whole banks, prose, and actual arrow ink."""
import hashlib,importlib.util,json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186096700'
z=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
count=dict(records=0,statements=0,choices=0,prose_ratios=0,prose_directions=0,pngs=0,arrow_ink_targets=0,source_prompts=0,source_values=0)
seen=set()
def equation(t):
 t=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',t.replace(' ',''))
 m=re.fullmatch(r'([a-e])=([+-]?(?:\d+(?:/\d+)?)?)([a-e])',t);assert m,t
 a,k,b=m.groups();return a,s.Rational('-1' if k=='-' else '1' if k in ('','+') else k),b
def subset(t):return frozenset(i for i,x in enumerate(('I','II','III')) if re.search(r'(?<!I)'+x+r'(?!I)',t))
def png(path,geometry,transform,labels=None):
 path=Path(path)
 if path in seen:return
 a=np.asarray(Image.open(path).convert('RGB')).astype(int);h,w=a.shape[:2]
 blue=(a[:,:,2]>a[:,:,0]+35)&(a[:,:,2]>a[:,:,1]+10)&(a[:,:,0]<180)
 x0,y0,sx,sy=transform;assert abs(sx-sy)<1e-8
 for name,p in geometry.items():
  tail=np.array(list(map(float,p['tail'])));tip=np.array(list(map(float,p['tip'])));v=tip-tail;assert np.linalg.norm(v)>0
  for t in np.linspace(.12,.9,13):
   q=tail+t*v;x=round(x0+sx*q[0]);y=round(y0-sy*q[1]);assert blue[max(0,y-3):y+4,max(0,x-3):x+4].any(),(path,name,t)
   count['arrow_ink_targets']+=1
  # The solid arrowhead has pixels at the tip and extends along the perpendicular.
  norm=v/np.linalg.norm(v);normal=np.array([-norm[1],norm[0]]);pix_tip=np.array([x0+sx*tip[0],y0-sy*tip[1]]);pix_norm=np.array([norm[0],-norm[1]]);pix_perp=np.array([normal[0],-normal[1]])
  def flare(point,sign):
   n=0
   for back in range(1,11):
    for off in (-5,-4,-3,-2,2,3,4,5):
     x,y=np.rint(point+sign*back*pix_norm+off*pix_perp).astype(int)
     if 0<=x<w and 0<=y<h:n+=int(blue[y,x])
   return n
  pix_tail=np.array([x0+sx*tail[0],y0-sy*tail[1]])
  assert flare(pix_tip,-1)>flare(pix_tail,1),(path,name,'actual arrowhead orientation',flare(pix_tip,-1),flare(pix_tail,1))
 if labels:
  black=np.max(a,axis=2)<110
  for label,b in labels.items():
   l,bottom,r,top=b['bbox_pixels_bottom_origin'];x1,x2=int(np.floor(l))-3,int(np.ceil(r))+3;y1,y2=h-int(np.ceil(top))-3,h-int(np.floor(bottom))+3
   assert not blue[max(y1,0):y2,max(x1,0):x2].any(),(path,label,'text touches arrow')
   assert black[h-int(np.ceil(top)):h-int(np.floor(bottom))+1,int(np.floor(l)):int(np.ceil(r))+1].sum()>4
   assert b['shaft_association_grid_distance']<=.9
 seen.add(path);count['pngs']+=1
def record(r):
 q=r['question'];gen=r['generation'];vs={k:tuple(s.Rational(b)-s.Rational(a) for a,b in zip(v['tail'],v['tip'])) for k,v in gen['geometry'].items()}
 statements=[equation(t) for t in re.findall(r'^\d\. \$(.*?)\$',q[':question/problem'],re.M)];assert len(statements)==3
 true=frozenset(i for i,(a,k,b) in enumerate(statements) if all(vs[a][j]==k*vs[b][j] for j in range(2)))
 f=q[':question/answer-fields'][0];values=[subset(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==len(set(values))==5 and values.count(true)==1
 if ':answer-field/correct' in f:assert subset(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))==true
 sol=q.get(':question/worked-solution')
 if sol:
  bullets=re.findall(r'^- Statement (I|II|III) is (true|false)\.',sol,re.M);assert bullets==[(x,'true' if i in true else 'false') for i,x in enumerate(('I','II','III'))]
  for a,k,b in re.findall(r'The magnitude of \$([a-e])\$ is \$(.*?)\$ times the magnitude of \$([a-e])\$',sol,re.I):
   k=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',k);assert s.Rational(k)**2==sum(x*x for x in vs[a])/sum(x*x for x in vs[b]);count['prose_ratios']+=1
  for a,b,word in re.findall(r'[Vv]ectors \$([a-e])\$ and \$([a-e])\$ (?:are parallel and )?have (the same direction|opposite directions)',sol):
   assert (sum(x*y for x,y in zip(vs[a],vs[b]))>0)==(word=='the same direction');count['prose_directions']+=1
  for i,bullet in enumerate(sol.split('\n\n')[0].split('\n')):
   last=re.findall(r'\$([^$]*(?:=|\\neq)[^$]*)\$',bullet)[-1];assert equation(last.replace(r'\neq','='))==statements[i]
  assert sol.endswith('Therefore, '+('only statement '+('I','II','III')[next(iter(true))]+' is true.' if len(true)==1 else 'only statements '+' and '.join(('I','II','III')[i] for i in sorted(true))+' are true.' if len(true)==2 else 'all three statements are true.' if len(true)==3 else 'none of the statements are true.'))
 p=gen['plot'];path=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]
 if p.get('source_asset'):
  sid=gen['source_ids'][0];geom=original[sid]['geometry'];assert geom==gen['geometry'];png(p['source_asset'],geom,original[sid]['transform'])
 else:png(path,gen['geometry'],p['transform'],p['labels']);assert p['png_sha256']==hashlib.sha256(Path(path).read_bytes()).hexdigest()
 count['records']+=1;count['statements']+=3;count['choices']+=5
original=json.loads((D/'original-geometry.json').read_text())
# Root full-resolution source readings: displacement tuples are translation-independent.
hand={'q-19215':{'a':(4,2),'b':(-4,-2),'c':(2,5),'d':(-2,-5),'e':(2,1)},'q-20404':{'a':(6,4),'b':(-3,-5),'c':(-3,-2),'d':(3,5),'e':(-4,0)}}
source=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
for c in g.SOURCE_CASES:
 r=g.generate(c['level'],11,c['template'],parameters=c['parameters'],profile=c['bank_profile']);o=next(q for q in source if q[':question/math-academy-id']==c['source_id']);q=r['question']
 assert q[':question/problem']==o[':question/problem'] and set(q)==set(o)-{':db/id',':question/math-academy-id'}
 f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert set(f)==set(of)-{':db/id'} and sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
 assert {k:tuple(int(s.Rational(b)-s.Rational(a)) for a,b in zip(v['tail'],v['tip'])) for k,v in r['generation']['geometry'].items()}==hand[c['source_id']]
 assert not r['generation']['eligible_for_learning'] and ':answer-field/correct' not in f
 record(r);count['source_prompts']+=1;count['source_values']+=5
for item in json.loads((D/'native-input.json').read_text()):record(item['record'])
out={'status':'passed','independent_readback':count,'source_displacements_read_by_root':hand,'renderer_regression':'Hard seed 0 now renders correctly; actual ink, arrowheads and local text clearance checked.'}
(R/'qa/17592186096700-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
