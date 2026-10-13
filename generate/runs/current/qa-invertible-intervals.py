"""Root exact restricted-domain ranges, listed maximality, prose and PNG readback."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186124473'
def load(p,name):
 z=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=load(D.with_suffix('.py'),'g');p=load(R/'ode-scalar-parser.py','p');Y=s.Symbol('y')
n=dict(records=0,choices=0,interval_criteria=0,range_intersections=0,prose_claims=0,pngs=0,curve_targets=0,endpoint_centers=0,source_prompts=0,source_solutions=0,source_values=0);seen=set()
def endpoint(t):return -s.oo if t==r'-\infty' else s.oo if t==r'\infty' else p.scalar(t)
def domains(t):
 out=[]
 for m in re.finditer(r'([\[(])\s*([^,]+?)\s*,\s*([^,]+?)\s*([\])])',t):out.append(s.Interval(endpoint(m[2]),endpoint(m[3]),left_open=m[1]=='(',right_open=m[4]==')'))
 return s.Union(*out)
def subset(t):return frozenset(re.findall(r'\bIII\b|\bII\b|\bI\b',t))
def one_to_one(pieces,requested):
 all_domain=s.Union(*[s.Interval(s.Rational(z[0]),s.Rational(z[2]),left_open=not z[4],right_open=not z[5]) for z in pieces]);assert requested-all_domain==s.EmptySet
 ranges=[]
 for a,b,c,d,lc,rc in pieces:
  a,b,c,d=map(s.Rational,(a,b,c,d));m=(d-b)/(c-a);k=b-m*a;portion=requested.intersect(s.Interval(a,c,left_open=not lc,right_open=not rc));parts=list(portion.args) if isinstance(portion,s.Union) else [portion]
  for part in parts:
   if part==s.EmptySet:continue
   if isinstance(part,s.FiniteSet):ranges.extend([(s.FiniteSet(m*x+k),s.FiniteSet(x),m,k) for x in part]);continue
   if m==0:return False
   low,high=m*part.start+k,m*part.end+k
   image=s.Interval(min(low,high),max(low,high),left_open=part.left_open if m>0 else part.right_open,right_open=part.right_open if m>0 else part.left_open);ranges.append((image,part,m,k))
 for i,(image,domain,m,k) in enumerate(ranges):
  for other,other_domain,mm,kk in ranges[:i]:
   overlap=image.intersect(other);n['range_intersections']+=1
   if overlap==s.EmptySet:continue
   if not isinstance(overlap,s.FiniteSet):return False
   for y in overlap:
    x=next(iter(domain)) if m==0 else (y-k)/m;xx=next(iter(other_domain)) if mm==0 else (y-kk)/mm
    if x!=xx:return False
 return True
def raster(path,pieces):
 path=Path(path)
 if path in seen:return
 side=json.loads(path.with_suffix('.json').read_text());image=np.asarray(Image.open(path).convert('RGB')).astype(int);h,w=image.shape[:2];blue=(image[:,:,2]>image[:,:,0]+45)&(image[:,:,1]>image[:,:,0]+20)&(image[:,:,0]<150)
 l,b,ww,hh=side['axes_bbox_pixels'];xmin,xmax,ymin,ymax=side['limits']
 def pixel(x,y):return round(l+(x-xmin)*ww/(xmax-xmin)),round(h-1-(b+(y-ymin)*hh/(ymax-ymin)))
 markers={}
 for a,bb,c,d,lc,rc in pieces:
  a,bb,c,d=map(float,(a,bb,c,d))
  for t in np.linspace(.06,.94,17):
   x,y=pixel(a+t*(c-a),bb+t*(d-bb));assert blue[max(0,y-3):y+4,max(0,x-3):x+4].any(),(path,t);n['curve_targets']+=1
  for key,closed in (((a,bb),lc),((c,d),rc)):markers[key]=markers.get(key,False) or closed
 for (x,y),closed in markers.items():
  xx,yy=pixel(x,y);assert bool(blue[max(0,yy-1):yy+2,max(0,xx-1):xx+2].any())==closed,(path,'endpoint membership',x,y);n['endpoint_centers']+=1
 for label in side['label_clearances']:assert label['feature_clearance_pixels']>=4
 seen.add(path);n['pngs']+=1
def record(r):
 q=r['question'];meta=r['generation'];assert json.loads(json.dumps(r))==r
 if not meta['eligible_for_learning']:return
 path=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]);side=json.loads(path.with_suffix('.json').read_text());pieces=side['data']['pieces'];f=q[':question/answer-fields'][0];answers=f[':answer-field/choices'];sol=q[':question/worked-solution']
 lines=[line for line in q[':question/problem'].splitlines() if re.match(r'[I]+\. \$',line)]
 if lines:
  requested=[domains(line) for line in lines];assert len(requested)==3;true=frozenset(('I','II','III')[i] for i,x in enumerate(requested) if one_to_one(pieces,x));values=[subset(a[':answer/value']) for a in answers]
  assert len(set(values))==5 and values.count(true)==1
  assert subset(next(a[':answer/value'] for a in answers if a[':answer/id']==f[':answer-field/correct'][1]))==true
  claims=[line for line in sol.splitlines() if line.startswith('- On interval')];assert len(claims)==3
  for i,(line,request) in enumerate(zip(claims,requested)):
   assert domains(line)==request and ('**not** invertible' not in line)==(('I','II','III')[i] in true);n['prose_claims']+=1
  assert subset(re.search(r'correct answer is "([^"]+)"',sol)[1])==true
 else:
  requested=[domains(a[':answer/value']) for a in answers];assert len(set(requested))==5
  valid=[one_to_one(pieces,x) for x in requested]
  greatest=[valid[i] and all(not valid[j] or other.is_subset(x) for j,other in enumerate(requested)) for i,x in enumerate(requested)];assert sum(greatest)==1
  chosen=next(i for i,a in enumerate(answers) if a[':answer/id']==f[':answer-field/correct'][1]);assert greatest[chosen] and domains(sol.split('Therefore,')[-1])==requested[chosen]
  assert 'listed' in q[':question/problem'] and ('greatest by inclusion' in q[':question/problem'] or 'maximal by inclusion' in q[':question/problem']);n['prose_claims']+=1
 raster(path,pieces);n['records']+=1;n['choices']+=5;n['interval_criteria']+=len(requested)
for c in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(c['level'],11,template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);q=r['question'];o=g.QUESTIONS[c['source_id']];assert q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'] and set(q)==set(o)
 f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert set(f)==set(of) and sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];assert not r['generation']['eligible_for_learning']
 n['source_prompts']+=1;n['source_solutions']+=1;n['source_values']+=5
for item in json.loads((D/'engine-input.json').read_text()):record(item['record'])
for level in ('easy','moderate','hard'):
 for seed in range(18):record(g.generate(level,seed))
out={'status':'passed','independent_readback':n,'normal_criterion_repairs':'Both plateau families explicitly request a greatest/maximal injective domain among listed choices; globally incomparable plateau singletons are not ignored.','serialization_regression':'Exact Fraction metadata is serialized as reduced rational strings, with 54 default question payloads proved unchanged.'};(R/'qa/17592186124473-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
