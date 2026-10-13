"""Root whole-domain preimage and actual plotted-curve readback."""
import hashlib,importlib.util,json,re,sys
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186124472';X=s.Symbol('x',real=True)
z=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
n=dict(records=0,choices=0,graphs=0,exact_preimage_levels=0,pngs=0,curve_ink_targets=0,endpoint_centers=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0);cache={};seen=set()
def expression(p):return s.sympify(p['expression'],locals={'x':X}) if 'expression' in p else sum(s.Rational(v)*X**i for i,v in enumerate(p['coefficients']))
def injective(graph):
 key=json.dumps(graph['segments'],sort_keys=True)
 if key in cache:return cache[key]
 heights=set();pieces=[]
 for p in graph['segments']:
  a,b=s.Rational(str(p['a'])),s.Rational(str(p['b']));expr=expression(p);domain=s.Interval(a,b,left_open=not p['left_closed'],right_open=not p['right_closed']);pieces.append((expr,domain))
  if not expr.has(X):cache[key]=False;return False
  critical=s.solveset(s.diff(expr,X),X,domain=s.Interval.open(a,b));assert critical.is_FiniteSet
  heights.update(expr.subs(X,t) for t in [a,b]+list(critical))
 hs=sorted(heights,key=float);hs+= [(a+b)/2 for a,b in zip(hs,hs[1:])]
 for y in hs:
  preimages=set()
  for expr,domain in pieces:
   roots=s.solveset(expr-y,X,domain=domain);assert roots.is_FiniteSet,(expr,y,roots)
   preimages.update(s.simplify(t) for t in roots)
  n['exact_preimage_levels']+=1
  if len(preimages)>1:cache[key]=False;return False
 cache[key]=True;return True
def mask(v):return frozenset(re.findall(r'\bIV\b|\bIII\b|\bII\b|\bI\b',v))
def raster(path,graphs):
 p=Path(path)
 if p in seen:return
 side=json.loads(p.with_suffix('.json').read_text());assert side['graphs']==graphs and side['sha256']==hashlib.sha256(p.read_bytes()).hexdigest()
 a=np.asarray(Image.open(p).convert('RGB')).astype(int);h,w=a.shape[:2];blue=(a[:,:,2]>a[:,:,0]+50)&(a[:,:,0]<110)&(a[:,:,1]>65)&(a[:,:,2]>125)
 for graph,(l,b,ww,hh) in zip(graphs,side['axes_boxes']):
  def pixel(x,y):return round(l+(x+4.7)*ww/9.4),round(h-(b+(y+4.7)*hh/9.4))
  for seg in graph['segments']:
   expr=expression(seg);f=s.lambdify(X,expr,'numpy')
   for x in np.linspace(float(seg['a']),float(seg['b']),33)[1:-1]:
    y=float(f(x));xx,yy=pixel(x,y);assert blue[max(0,yy-3):yy+4,max(0,xx-3):xx+4].any(),(p,x,y);n['curve_ink_targets']+=1
   for x,closed in [(seg['a'],seg['left_closed']),(seg['b'],seg['right_closed'])]:
    xx,yy=pixel(float(x),float(expr.subs(X,s.Rational(str(x)))));assert bool(blue[max(0,yy-1):yy+2,max(0,xx-1):xx+2].any())==closed,(p,'endpoint inclusion');assert blue[max(0,yy-6):yy+7,max(0,xx-6):xx+7].any();n['endpoint_centers']+=1
 seen.add(p);n['pngs']+=1
def record(r):
 q=r['question'];meta=r['generation']
 if not meta['eligible_for_learning']:return
 graphs=meta['graphs'];true=frozenset(label for label,graph in zip(('I','II','III','IV'),graphs) if injective(graph));f=q[':question/answer-fields'][0];values=[mask(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(values)==len(set(values))==5 and values.count(true)==1
 assert mask(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))==true
 sol=q[':question/worked-solution'];assert sol.startswith(g.OPENING)
 assert mask(re.search(r'correct answer is "([^"]+)"',sol)[1])==true
 for line in sol.splitlines():
  if line.startswith('- For graph'):
   labels=mask(line.split(', any horizontal')[0].split(', some horizontal')[0]);assert labels==(true if 'at most once' in line else frozenset(('I','II','III','IV'))-true)
 level=q[':question/difficulty'].split('/')[-1]
 for graph in graphs:
  assert graph['level']==level
  if level!='easy':assert len(graph['segments'])==(2 if level=='moderate' else 3)
 raster(re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1],graphs)
 raster(re.search(r'!\[\]\((.*?)\)',sol)[1],graphs)
 n['records']+=1;n['graphs']+=4;n['choices']+=5
source=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'];hand={'8e62':{'I','II'},'caee':{'I'},'89b0':{'III'},'a6e3':{'II'},'1dd5':{'II'},'3897':{'I','III'},'91f0':set(),'2394':{'I','IV'},'be5b':{'IV'},'f650':{'III'}}
for c in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(c['level'],profile=c['profile'],parameters=c['parameters']);q=r['question'];o=next(x for x in source if x[':question/math-academy-id']==c['source_id']);assert q[':question/problem']==o[':question/problem'];assert {k for k in q if k.startswith(':question/')}=={k for k in o if k.startswith(':question/')}
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
 f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
 asset=re.search(r'images/\w+/([a-f0-9]+)',o[':question/problem'])[1][:4];expected=hand[asset]
 if ':answer-field/correct' in f:assert mask(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))==expected;n['source_refs']+=1
 assert not r['generation']['eligible_for_learning'];n['source_prompts']+=1;n['source_values']+=5
for item in json.loads((D/'engine-input.json').read_text()):record(item['record'])
for level in ('easy','moderate','hard'):
 for seed in range(18):record(g.generate(level,seed))
out={'status':'passed','independent_readback':n,'source_visual_scope':'All 18 original prompt/solution rasters, including canonical pair, viewed at full resolution. Only the displayed domain counts; disconnected curves and filled/open boundary points are included. Exact source formulas remain underidentified evidence.'};(R/'qa/17592186124472-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
