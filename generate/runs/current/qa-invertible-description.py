"""Root reads printed formulas/domains, fixed prose and actual plotted branches."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186124474'
def load(p,name):
 z=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=load(D.with_suffix('.py'),'g');p=load(R/'ode-scalar-parser.py','p');X=p.x
n=dict(records=0,choices=0,intervals=0,duplicate_witnesses=0,printed_function_equalities=0,construction_rows=0,source_prompts=0,source_solutions=0,source_values=0,pngs=0,actual_curve_targets=0,endpoint_centers=0);seen=set()
def scalar(t):
 t=t.strip().rstrip('.,');parts=t.split('|')
 if len(parts)>1:assert len(parts)==3;t=parts[0]+'Abs('+parts[1]+')'+parts[2]
 if t==r'\infty':return s.oo
 if t==r'-\infty':return -s.oo
 return p.scalar(t)
def interval(t):
 m=re.search(r'([\[(])(.*?),(.*?)([\])])',t);assert m,t;return scalar(m[2]),scalar(m[3]),m[1]=='[',m[4]==']'
def subset(t):return frozenset(re.findall(r'\bIII\b|\bII\b|\bI\b',t))
def raster(path,expr,ivs):
 path=Path(path)
 if path in seen:return
 side=json.loads(path.with_suffix('.json').read_text());a=np.asarray(Image.open(path).convert('RGB')).astype(int);h,w=a.shape[:2];blue=(a[:,:,2]>a[:,:,0]+45)&(a[:,:,2]>a[:,:,1]+15)&(a[:,:,0]<150);black=np.max(a,axis=2)<100;graphs=side['geometry']
 for i,geom in enumerate(graphs):
  left,right=int(i*w/len(graphs)),int((i+1)*w/len(graphs));bm=black[:,left:right];rows=np.where(bm.sum(axis=1)>(right-left)*.65)[0];cols=np.where(bm.sum(axis=0)>h*.60)[0];assert len(rows)>1 and len(cols)>1,(path,'actual spines')
  x0,x1=left+int(cols.min()),left+int(cols.max());y0,y1=int(rows.min()),int(rows.max());lo,hi=geom['xlim'];yl,yh=geom['ylim']
  def pixel(x,y):return round(x0+(x-lo)*(x1-x0)/(hi-lo)),round(y1-(y-yl)*(y1-y0)/(yh-yl))
  idx=geom['interval_index'];iv=ivs[idx-1] if idx else None
  if iv:
   observed=geom['interval'];assert all((float(observed[j])==float(iv[j]) or abs(float(observed[j])-float(iv[j]))<1e-10) for j in (0,1)) and tuple(observed[2:])==tuple(iv[2:])
  start=max(lo,float(iv[0])) if iv else lo;end=min(hi,float(iv[1])) if iv else hi
  for x in np.linspace(start,end,33)[2:-2]:
   yy=float(expr.subs(X,x));xx,yy=pixel(x,yy);assert blue[max(0,yy-3):yy+4,max(0,xx-3):xx+4].any(),(path,idx,x);n['actual_curve_targets']+=1
  if iv:
   for x,closed in ((iv[0],iv[2]),(iv[1],iv[3])):
    if x.is_finite:
     xx,yy=pixel(float(x),float(expr.subs(X,x)));assert bool(blue[max(0,yy-1):yy+2,max(0,xx-1):xx+2].any())==closed,(path,'endpoint inclusion',x);n['endpoint_centers']+=1
  assert all(v>=5 for v in side['label_clearance_pixels'][i].values())
 seen.add(path);n['pngs']+=1
def record(r):
 q=r['question'];gen=r['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];expr=scalar(re.search(r'f\(x\)=(.*?),\$',prompt)[1]);ivs=[interval(t) for t in re.findall(r'\$([^$]*\\in[^$]*)\$',prompt)];assert len(ivs)==3
 absolute=list(expr.atoms(s.Abs));poly=None if absolute else s.Poly(expr,X)
 if absolute:assert len(absolute)==1;vertex=s.solve(absolute[0].args[0],X)[0];folded=True
 elif poly.degree()==2:vertex=-poly.nth(1)/(2*poly.nth(2));folded=True
 else:assert poly.degree()<=1;vertex=0;folded=False
 true=set()
 for i,(lo,hi,lc,rc) in enumerate(ivs):
  assert lo<hi and not(lo==-s.oo and lc) and not(hi==s.oo and rc)
  good=hi<=vertex or lo>=vertex if folded else poly.nth(1)!=0
  if good:true.add(('I','II','III')[i])
  elif folded:
   d=min(vertex-lo if lo!=-s.oo else 1,hi-vertex if hi!=s.oo else 1)/2;u,v=vertex-d,vertex+d;assert lo<u<v<hi and s.simplify(expr.subs(X,u)-expr.subs(X,v))==0;n['duplicate_witnesses']+=1
 true=frozenset(true);fields=q.get(':question/answer-fields')
 if fields:
  f=fields[0];values=[subset(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==len(set(values))==5 and values.count(true)==1
  assert subset(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))==true;n['choices']+=5
  if gen['template'].startswith(('integer_','rational_')):assert sum(len(v)==2 for v in values)==3 and sum(len(v)==1 for v in values)==2
 else:assert gen['evidence_only'] and not gen['eligible_for_learning'] and gen['template']=='q-66785'
 assert subset(re.search(r'correct answer is "([^"]+)"',sol)[1])==true
 for t in re.findall(r'f\(x\)=([^$]+)',sol):assert s.simplify(scalar(t)-expr)==0;n['printed_function_equalities']+=1
 for line in sol.splitlines():
  for t in re.findall(r'y=([^$]+)',line):
   expected=s.Abs(X) if absolute else X**2
   if 'Reflect' in line:expected=-X**2
   elif 'Take the curve' not in line:expected=expr-expr.subs(X,vertex)
   assert s.simplify(scalar(t)-expected)==0,(line,expected);n['construction_rows']+=1
 if folded:
  for amount,word in re.findall(r'by \$(\d+)\$ units? +(?:to +the +)?(right|left|up|down)',sol):assert s.Integer(amount)*(1 if word in ('right','up') else -1)==(vertex if word in ('right','left') else expr.subs(X,vertex))
  for u,v,y in re.findall(r'inputs \$([^$]+)\$ and \$([^$]+)\$, both with output \$([^$]+)',sol):
   u,v,y=map(scalar,(u,v,y));assert u!=v and expr.subs(X,u)==expr.subs(X,v)==y;n['duplicate_witnesses']+=1
 for path in re.findall(r'!\[\]\((/home/jake/Developer/Course_Academy/[^)]+)\)',sol):raster(path,expr,ivs)
 n['records']+=1;n['intervals']+=3
source=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
for c in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(c['difficulty'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];o=next(o for o in source if o[':question/math-academy-id']==c['source_id']);assert q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'];assert (':question/answer-fields' in q)==(':question/answer-fields' in o)
 if ':question/answer-fields' in q:assert sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in o[':question/answer-fields'][0][':answer-field/choices']);n['source_values']+=5
 record(r);n['source_prompts']+=1;n['source_solutions']+=1
for item in json.loads((D/'engine-input.json').read_text()):record(item['record'])
for level in ('easy','moderate','hard'):
 for seed in range(18):record(g.generate(level,seed))
out={'status':'passed','independent_readback':n,'bank_regression':'Authored moderate/hard banks contain three plausible paired subsets and two true-member singleton omissions; no unique-length shortcut.','finite_semantic_limit':'Nonzero and constant lines give two easy semantic cases; the 72 moderate and 90 hard domain catalogs are ordered structural variations, not new methods.'};(R/'qa/17592186124474-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
