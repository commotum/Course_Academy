"""Root reads graph flux, complete ordered integrals and polar stage arithmetic."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
RDIR=Path(__file__).resolve().parent;D=RDIR.parents[2]/'generate/scratch/17592186133927'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=load(D.with_suffix('.py'),'g');p=load(RDIR/'ode-scalar-parser.py','p');X,Y,Z=p.x,p.y,p.z;RR,TH=p.u,p.t
n=dict(records=0,choices=0,partial_operators=0,curl_substitution_components=0,flux_stages=0,ordered_option_integrals=0,polar_stages=0,individual_endpoints=0,source_prompts=0,source_solutions=0,source_choices=0,source_keys=0,pngs=0,edge_pixel_targets=0,arrow_pixel_targets=0);seen=set();plots=set()
def scalar(t):
 t=t.replace(r'\theta','t').replace('[','(').replace(']',')');t=re.sub(r'\\[A-Za-z]+|r',lambda m:m[0] if m[0].startswith('\\') else 'u',t);return p.scalar(t)
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def vector(t):return s.Matrix([scalar(z) for z in t.split(r',\,')])
def ordered(t):
 t=t.replace('$$','').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().rstrip('.')
 m=re.fullmatch(r'\\int_\{(.*?)\}\^\{(.*?)\}\\int_\{(.*?)\}\^\{(.*?)\}\\left\((.*?)\\right\)\\,\\mathrm\{d\}y\\,\\mathrm\{d\}x',t);assert m,t;return tuple(map(scalar,m.groups()))
def value(parts):
 x0,x1,y0,y1,e=parts
 factor=s.simplify(e/s.sqrt(X**2+Y**2))
 if not factor.has(X,Y) and x1==y0==0 and x0==-y1:return factor*y1**3*(s.sqrt(2)+s.log(1+s.sqrt(2)))/3
 return s.simplify(s.integrate(s.integrate(e,(Y,y0,y1)),(X,x0,x1)))
def raster(path,parts):
 path=Path(path)
 if path in plots:return
 side=json.loads(path.with_suffix('.json').read_text());assert side['renderer_version']==4 and not side['background_masks'] and side['png_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
 image=np.asarray(Image.open(path).convert('RGB')).astype(int);h,w=image.shape[:2];assert list((w,h))==side['figure_pixels'];l,b,ww,hh=side['axes_bbox_pixels'];xmin,xmax,ymin,ymax=side['limits'];assert abs(ww/(xmax-xmin)-hh/(ymax-ymin))<1e-6
 blue=(image[:,:,2]>image[:,:,0]+70)&(image[:,:,2]>image[:,:,1]+25);black=np.max(image,axis=2)<100;orange=(image[:,:,0]>210)&(image[:,:,1]>60)&(image[:,:,1]<220)&(image[:,:,2]<70)
 def pixel(x,y):return round(l+(x-xmin)*ww/(xmax-xmin)),round(h-(b+(y-ymin)*hh/(ymax-ymin)))
 vertices=side['vertices'];x0,x1,y0,y1,_=parts
 for x,y in vertices:assert x0<=x<=x1 and y0.subs(X,x)<=y<=y1.subs(X,x)
 for i,a in enumerate(vertices):
  z=vertices[(i+1)%len(vertices)]
  for t in np.linspace(.1,.9,9):
   x,y=pixel(a[0]+t*(z[0]-a[0]),a[1]+t*(z[1]-a[1]));assert (blue|black)[max(0,y-3):y+4,max(0,x-3):x+4].any();n['edge_pixel_targets']+=1
 aa,bb=side['arrow_data'];assert aa[0]==bb[0] and y0.subs(X,aa[0])<aa[1]<bb[1]<y1.subs(X,bb[0])
 for t in np.linspace(.12,.82,7):
  x,y=pixel(aa[0],aa[1]+t*(bb[1]-aa[1]));assert orange[max(0,y-3):y+4,max(0,x-3):x+4].any();n['arrow_pixel_targets']+=1
 for key in ('label_clearance_px','equation_edge_clearance_px','equation_arrow_clearance_px','minimum_text_axis_clearance_px'):assert side[key]>8
 plots.add(path);n['pngs']+=1
def normal(r):
 if not r['generation']['eligible_for_learning']:return
 q=r['question'];qid=q[':question/id']
 if qid in seen:return
 sol=q[':question/worked-solution'];prompt=q[':question/problem'];graph=scalar(re.search(r'\$\$z=g\(x,y\)=(.*?)\.\$\$',sol)[1]);curl=vector(re.search(r'\\text\{curl\}\\,F=\\langle (.*?)\\rangle',prompt)[1]);assert len(curl)==3 and s.simplify(sum(s.diff(c,v) for c,v in zip(curl,(X,Y,Z))))==0
 if 'surface $z=' in prompt:assert same(scalar(re.search(r'surface \$z=(.*?)\$',prompt)[1]),graph)
 gx,gy=s.diff(graph,X),s.diff(graph,Y);sub=curl.subs(Z,graph);flux=s.simplify(-sub[0]*gx-sub[1]*gy+sub[2])
 operators=re.findall(r'\\frac\{\\partial\}\{\\partial ([xy])\}\\left\((.*?)\\right\)=(.*?)(?:\\\\|\.\\end)',sol,re.S);assert len(operators)==2
 for axis,arg,out in operators:assert same(scalar(arg),graph) and same(scalar(out),s.diff(graph,X if axis=='x' else Y));n['partial_operators']+=1
 vs=re.findall(r'&=\\langle (.*?)\\rangle',sol);assert len(vs)==3
 for i,v in enumerate(vs):assert all(same(a,b) for a,b in zip(vector(v),curl if i==0 else sub));n['curl_substitution_components']+=3
 fr=re.findall(r'&=\\iint_D\\left\((.*?)\\right\)\\,\\mathrm\{d\}A',sol,re.S);assert len(fr)==3
 for row in fr:assert same(scalar(row),flux);n['flux_stages']+=1
 f=q[':question/answer-fields'][0];answers=f[':answer-field/choices'];correct=next(a[':answer/value'] for a in answers if a[':answer/id']==f[':answer-field/correct'][1]);integrals=[a[':answer/value'] for a in answers if r'\int_' in a[':answer/value']]
 if integrals:
  parts=[ordered(v) for v in integrals];true=ordered(correct);assert same(true[-1],flux)
  if r['generation']['template']=='reciprocal':
   x0,x1,y0,y1,e=true;assert all(v[:4]==true[:4] for v in parts);assert x0==-x1 and y0==-y1 and x1==y1 and x1 in (1,2,3)
   # Exact proof: all five are multiples of -2 I0, -4 I0, 0, +J, -J.
   denom=(1+X**2+Y**2)**2;scale=s.simplify(-e*denom/2);assert not scale.has(X,Y) and scale>0
   forms=[s.simplify(v[-1]*denom/scale) for v in parts];assert set(forms)=={-2,-4,-X*Y,X**2,-Y**2}
   # J/I0<2: for a=1 pointwise r²<2 except corners; for a=2,3
   # compare the containing disk's I1 to the contained disk's I0. log19<3
   # follows from the positive exponential series through its sixth term.
   assert sum(s.Rational(3)**j/s.factorial(j) for j in range(7))>19
   if x1>1:assert (3-2*x1**2/(1+2*x1**2))/(2*x1**2/(1+x1**2))<2
  else:
   vals=[value(v) for v in parts];expected=value(true);assert all(not same(a,b) for i,a in enumerate(vals) for b in vals[:i]) and sum(same(v,expected) for v in vals)==1
  n['ordered_option_integrals']+=len(parts)
  for path in re.findall(r'!\[\]\((.*?)\)',sol):raster(path,true)
 elif f[':answer-field/type'].endswith('/blank'):
  assert same(scalar(correct),flux);true=ordered(re.findall(r'\$\$(\\int_.*?)\.\$\$',sol,re.S)[-1]);assert same(true[-1],flux)
  for path in re.findall(r'!\[\]\((.*?)\)',sol):raster(path,true)
 else:
  radius2=scalar(re.search(r'circle \$x\^2\+y\^2=(.*?)\.\$',sol)[1]);radius=s.sqrt(radius2);polar=s.expand_trig(flux.subs({X:RR*s.cos(TH),Y:RR*s.sin(TH)},simultaneous=True)*RR);answer=s.simplify(s.integrate(s.integrate(polar,(TH,0,2*s.pi)),(RR,0,radius)))
  assert same(scalar(correct),answer);values=[scalar(a[':answer/value']) for a in answers];assert all(not same(a,b) for i,a in enumerate(values) for b in values[:i]) and sum(same(v,answer) for v in values)==1
  block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[-1];rows=[v.strip().rstrip('.') for v in block.split('&=')[1:]];assert len(rows)==8
  rows=[v.removesuffix(r'\\').strip().replace(r'\left','').replace(r'\right','') for v in rows]
  prefix=r'\int_0^{'+g.tex(s.sqrt(radius2))+r'}\int_0^{2\pi}'
  for row in rows[:2]:
   assert row.startswith(prefix);body=row[len(prefix):].removesuffix(r'\,\mathrm{d}\theta\,\mathrm{d}r');assert same(scalar(body),polar);n['polar_stages']+=1
  m=re.search(r'\[(.*?)\]_0\^\{2\\pi\}',rows[2]);assert m;primitive=scalar(m[1]);assert same(s.diff(primitive,TH),polar);n['polar_stages']+=1
  ep=re.search(r'\[\((.*?)\)-\((.*?)\)\]',rows[3]);assert ep and same(scalar(ep[1]),primitive.subs(TH,2*s.pi)) and same(scalar(ep[2]),primitive.subs(TH,0));n['individual_endpoints']+=2
  angular=s.simplify(primitive.subs(TH,2*s.pi)-primitive.subs(TH,0));body=re.search(r'\((.*?)\)\\,\\mathrm\{d\}r',rows[4])[1];assert same(scalar(body),angular);n['polar_stages']+=1
  m=re.fullmatch(r'\[(.*?)\]_0\^\{(.*?)\}',rows[5]);assert m;radial=scalar(m[1]);assert same(s.diff(radial,RR),angular) and same(scalar(m[2]),radius);n['polar_stages']+=1
  ep=re.fullmatch(r'\[(.*)\]-\[(.*)\]',rows[6]);assert ep;terms=s.Add.make_args(radial)
  for text,endpoint in ((ep[1],radius),(ep[2],0)):
   vals=re.findall(r'\((.*?)\)',text);assert len(vals)==len(terms)
   for val,term in zip(vals,terms):assert same(scalar(val),term.subs(RR,endpoint));n['individual_endpoints']+=1
  assert same(scalar(rows[6]),answer) and same(scalar(rows[7]),answer)
 seen.add(qid);n['records']+=1;n['choices']+=len(answers)
for c in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];o=g.Q[c['source_id']];assert q[':question/problem']==o[':question/problem'] and (':question/worked-solution' in q)==(':question/worked-solution' in o) and (':question/difficulty' in q)==(':question/difficulty' in o)
 if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
 assert len(q[':question/answer-fields'])==len(o[':question/answer-fields'])
 for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']) and (':answer-field/correct' in f)==(':answer-field/correct' in of);n['source_choices']+=len(f[':answer-field/choices'])
  if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_keys']+=1
 assert not r['generation']['eligible_for_learning'];n['source_prompts']+=1
for item in json.loads((D/'engine-input.json').read_text()):normal(item['record'])
for level in ('easy','moderate','hard'):
 for seed in range(18):normal(g.generate(level,seed))
out={'status':'passed','independent_readback':n,'source_plots':'Root viewed all five original region plots at full resolution. V4 retains the vertical integration cue with an arrow inside its true slice, plain text and actual DPI-calibrated geometry.','reciprocal_bank':'Exact positive-integral bounds prove the five complete integrals unequal; no quadrature-only equivalence claim.'};(RDIR/'qa/17592186133927-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
