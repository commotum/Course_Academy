"""Root full-circle equation, bank, prose, stage and actual raster readback."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','reader');x,y=p.x,p.y
counts=dict(records=0,choices=0,generic_rows=0,substitution_rows=0,prose_inputs=0,conclusions=0,pngs=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def scalar(raw):
 while re.search(r'\\sqrt\[(\d+)\]\{',raw):
  m=re.search(r'\\sqrt\[(\d+)\]\{',raw);depth=1;end=m.end()
  while depth:
   depth+=(raw[end]=='{')-(raw[end]=='}');end+=1
  raw=raw[:m.start()]+'('+raw[m.end():end-1]+r')^{\frac{1}{'+m[1]+'}}'+raw[end:]
 raw=re.sub(r'\\[A-Za-z]+|[abr]',lambda m:m[0] if m[0].startswith('\\') else {'a':'u','b':'v','r':'t'}[m[0]],raw.strip().rstrip('.,'))
 return p.scalar(raw)
def eq(raw):
 l,r=raw.replace('&','').split('=');return s.expand(scalar(l)-scalar(r))
def key(F):
 P=s.Poly(F,x,y,domain='EX');return tuple((mon,s.simplify(v/P.LC())) for mon,v in P.terms())
def raster(path,h,k,r):
 # Infer pixel origin from the actual two long black axes, then compare the
 # fitted red circle center in radius units; no metadata axes transform used.
 im=Image.open(path).convert('RGB');W,H=im.size;red=[];blackx=[0]*W;blacky=[0]*H
 for j in range(H):
  for i in range(W):
   a,b,c=im.getpixel((i,j))
   if a>180 and b<110 and c<110:red.append((i,j))
   if max(a,b,c)<80:blackx[i]+=1;blacky[j]+=1
 assert len(red)>200,path
 # Symmetric extrema robust to center dots and label white boxes.
 def fit(points):
  sx=sum(a for a,b in points);sy=sum(b for a,b in points)
  xx=sum(a*a for a,b in points);yy=sum(b*b for a,b in points);xy=sum(a*b for a,b in points)
  A=s.Matrix([[4*xx,4*xy,2*sx],[4*xy,4*yy,2*sy],[2*sx,2*sy,len(points)]])
  B=s.Matrix([sum(2*a*(a*a+b*b) for a,b in points),sum(2*b*(a*a+b*b) for a,b in points),xx+yy])
  cx,cy,c=map(float,A.inv()*B);return cx,cy,(c+cx*cx+cy*cy)**.5
 cx,cy,rr=fit(red)
 # Center dots and endpoint markers are not circumference samples.
 kept=[(a,b) for a,b in red if abs(((a-cx)**2+(b-cy)**2)**.5-rr)<3]
 cx,cy,rr=fit(kept)
 residuals=sorted(abs(((a-cx)**2+(b-cy)**2)**.5-rr) for a,b in kept)
 assert residuals[int(.95*len(residuals))]<2 and residuals[-1]<6,(path,residuals[-1],residuals[int(.95*len(residuals))])
 ox=max(range(W),key=lambda i:blackx[i]);oy=max(range(H),key=lambda j:blacky[j])
 assert abs(cx-ox-float(h/r)*rr)<5 and abs(cy-oy+float(k/r)*rr)<5,(path,(cx,cy,rr),(ox,oy),(h,k,r))
 counts['pngs']+=1
def check(rec,generator,source_parameters):
 q=rec['question'];g=rec['generation'];sid=g.get('source_id');raw=g.get('bank_profile','').startswith('raw:')
 # Source inputs were independently read from full-resolution labeled plots;
 # changed/generated inputs must agree with actual rendered geometry below.
 data=source_parameters[sid] if raw and sid and (g.get('plot') or {}).get('renderer')=='unchanged-source' else g['parameters']
 h,k,r=(s.sympify(data[z]) for z in ('h','k','r'));F=(x-h)**2+(y-k)**2-r*r
 f=q[':question/answer-fields'][0];vs=[eq(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(set(key(z) for z in vs))==len(vs)
 hits=[i for i,z in enumerate(vs) if key(z)==key(F)];assert len(hits)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][hits[0]][':answer/id']==f[':answer-field/correct'][1]
 else:assert g['evidence_only'] and not g['eligible_for_learning']
 if f[':answer-field/type'].endswith('/blank'):assert g['evidence_only'] and not g['eligible_for_learning'] and not g['grading_compatibility']['supported']
 if g['bank_profile']=='authored_sign_square':
  expected=[F,(x+h)**2+(y-k)**2-r*r,(x-h)**2+(y+k)**2-r*r,(x+h)**2+(y+k)**2-r*r,(x-h)**2+(y-k)**2-r]
  assert set(key(z) for z in vs)==set(key(z) for z in expected)
 sol=q.get(':question/worked-solution')
 if sol:
  displays=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(displays)==(3 if f[':answer-field/type'].endswith('/blank') else 2)
  generic=(x-p.u)**2+(y-p.v)**2-p.t**2;assert eq(displays[0])==s.expand(generic);counts['generic_rows']+=1
  rows=displays[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3
  assert eq(rows[0])==s.expand(generic);counts['generic_rows']+=1
  for row in rows[1:]:assert key(eq(row))==key(F);counts['substitution_rows']+=1
  center=re.search(r'(?:C)?\$?\(([^$()]*)\)\$ and the radius',sol)
  if not center:center=re.search(r'centered at \$C?\((.*?)\)\$ and the radius',sol)
  assert center,(sid,sol);a,b=center[1].split(',');assert scalar(a)==h and scalar(b)==k
  radius=re.search(r'radius of the circle is \$r=(.*?)\$',sol);assert radius and scalar(radius[1])==r
  counts['prose_inputs']+=3
  if len(displays)==3:assert key(eq(displays[2]))==key(F);counts['conclusions']+=1
 plot=g.get('plot')
 if plot and plot.get('renderer')=='matplotlib':
  path=re.findall(r'!\[\]\((.*?)\)',q[':question/problem'])[0];raster(path,h,k,r)
 counts['records']+=1;counts['choices']+=len(vs)
if __name__=='__main__':
 kp=17592186087655;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'))
 original={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 # Independently inspected seven source raster diagrams; stripped blank inputs
 # below come only from its surviving solution and remain ineligible evidence.
 inputs={'q-54187':dict(h=1,k=3,r=3),'q-54210':dict(h=-2,k=5,r=7),'q-167932':dict(h=3,k=0,r=3),'q-116929':dict(h=-4,k=-3,r=6),'q-117077':dict(h=2,k=-3,r=4),'q-117081':dict(h=-5,k=0,r=7),'q-70896':dict(h=1,k=2,r=5),'q-70898':dict(h=-2,k=-3,r=8)}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate('easy',parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec,g,inputs);q=rec['question'];o=original[c['source_id']]
  for attr in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (attr in q)==(attr in o)
   if attr in o:assert q[attr]==(o[attr][':db/ident'] if attr.endswith('difficulty') else o[attr])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert value==of[':answer-field/correct'][':answer/value'];counts['source_refs']+=1
  counts['source_prompts']+=1;counts['source_values']+=len(of[':answer-field/choices']);counts['source_solutions']+=int(':question/worked-solution' in o)
 for rec in json.load(open(D/'review.json')):check(rec,g,inputs)
 for level in ('easy','moderate','hard'):
  for seed in range(8):check(g.generate(level,seed=720000+seed),g,inputs)
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
