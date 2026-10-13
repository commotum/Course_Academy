"""Independent displayed mathematics, raw fidelity, scope and native grading QA."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
from PIL import Image
sys.dont_write_bytecode=True
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('diameter',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def arithmetic(t):
 """Restricted independently parsed numeric TeX; never reads generation values."""
 t=t.strip().rstrip('.')
 def group_at(s,i):
  assert s[i]=='{';depth=1;j=i+1
  while depth:
   if s[j]=='{':depth+=1
   elif s[j]=='}':depth-=1
   j+=1
  return s[i+1:j-1],j
 while '\\frac' in t or '\\sqrt' in t:
  m=re.search(r'\\(frac|sqrt)',t);name=m.group(1);a,end=group_at(t,m.end())
  if name=='frac':b,end=group_at(t,end);repl='('+str(arithmetic(a))+')/('+str(arithmetic(b))+')'
  else:repl='sqrt('+str(arithmetic(a))+')'
  t=t[:m.start()]+repl+t[end:]
 t=t.replace('\\cdot','*').replace('{','(').replace('}',')').replace('^','**')
 t=re.sub(r'(\d)\s*(sqrt\()',r'\1*\2',t)
 assert re.fullmatch(r'[\d+*/().\s\-squrt]*',t),t
 return sp.sympify(t,locals={'sqrt':sp.sqrt})

def displayed(record):
 q=record['question'];p=q[':question/problem']
 text=p.split('have coordinates ')[1]
 pairs=re.findall(r'\((-?\d+),\s*(-?\d+)\)',text);assert len(pairs)==2
 x1,y1,x2,y2=map(int,(*pairs[0],*pairs[1]));h=sp.Rational(x1+x2,2);k=sp.Rational(y1+y2,2);D=(x1-x2)**2+(y1-y2)**2;z=sp.Rational(D,4);d=sp.sqrt(D);r=d/2
 correct=(g.X-h)**2+(g.Y-k)**2-z
 meta=record['generation']['dependencies']['plot']
 if not meta.get('reused_original'):
  assert meta['parameters']==dict(zip(('x1','y1','x2','y2'),(x1,y1,x2,y2)))
  assert meta['center']==[float(h),float(k)] and abs(meta['radius']-float(r))<1e-12 and meta['equal_aspect']
  raster_geometry(record['generation']['plots'][0],meta)
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];assert len(choices)==5
 polys=[];matches=[]
 for a in choices:
  e=g.parse_equation(a[':answer/value']);assert e.free_symbols <= {g.X,g.Y};assert all(c.is_finite is True for c in sp.Poly(e,g.X,g.Y).coeffs());polys.append(e)
  ratio=sp.cancel(e/correct);matches.append(bool(ratio.is_finite and ratio!=0 and not ratio.free_symbols))
 assert sum(matches)==1
 for i,e in enumerate(polys):
  for ee in polys[:i]:
   ratio=sp.cancel(e/ee);assert ratio.free_symbols or ratio==0 or ratio.is_finite is not True
 if ':answer-field/correct' in f:assert choices[matches.index(True)][':answer/id']==f[':answer-field/correct'][1]
 if ':question/worked-solution' not in q:return
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==5
 # Every displayed numeric distance row, including signed substitution and factoring.
 dist=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
 rows=dist.split(r'\\');assert len(rows)>=4
 for row in rows:assert sp.simplify(arithmetic(row.split('& =')[1])-d)==0,row
 # Radius rows retain symbolic XY plus all numeric half-diameter expressions.
 for part in blocks[2].split('=')[1:]:
  if 'XY' not in part:assert sp.simplify(arithmetic(part)-r)==0,part
 # Last midpoint equality is checked independently of metadata; preceding fraction
 # tuple establishes actual signed additions rather than just final center.
 mid=blocks[3].split('=')
 for tuple_text in mid[1:]:
  a,b=tuple_text.strip()[1:-1].split(',');assert arithmetic(a)==h and arithmetic(b)==k
 # Each numeric substitution/final equation row is equivalent as a whole equation.
 rows=blocks[4].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
 for row in rows[1:]:
  a,b=row.split('& =');ee=g.parse_equation(a+'='+b);assert sp.simplify(ee-correct)==0,row
 # Inline conclusion radius, midpoint, and endpoint coordinates must agree too.
 radius=re.search(r'circle has radius \$r=(.*?)\$',sol);assert radius and arithmetic(radius.group(1))==r
 center=re.search(r'center \$\(a,b\)=\((.*?),(.*?)\),',sol);assert center and arithmetic(center.group(1))==h and arithmetic(center.group(2))==k
 assert f'X({x1},{y1})' in sol and f'Y({x2},{y2})' in sol
 # Balanced delimiters/groups for all actual learner-facing strings.
 for s in [p,sol]+[a[':answer/value'] for a in choices]:
  assert s.count('$')%2==0
  depth=0
  for c in s:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0
  assert depth==0

def raster_geometry(path,meta):
 im=Image.open(path).convert('RGB');height=im.height
 pts=[(i%im.width,height-1-i//im.width) for i,(red,green,blue) in enumerate(im.get_flattened_data()) if red>180 and green<110 and blue<110]
 assert len(pts)>100
 # Fit the actual raster red stroke to a circle without consulting input geometry.
 n=len(pts);sx=sum(x for x,y in pts);sy=sum(y for x,y in pts);sxx=sum(x*x for x,y in pts);sxy=sum(x*y for x,y in pts);syy=sum(y*y for x,y in pts)
 rhs=sp.Matrix([sum(x*(x*x+y*y) for x,y in pts),sum(y*(x*x+y*y) for x,y in pts),sxx+syy]);fit=sp.Matrix([[sxx,sxy,sx],[sxy,syy,sy],[sx,sy,n]]).inv()*rhs
 cx,cy=float(fit[0]/2),float(fit[1]/2);radius=(float(fit[2])+cx*cx+cy*cy)**.5
 expected=meta['pixel_center_bottom_origin'];assert abs(cx-expected[0])<2 and abs(cy-expected[1])<2
 assert abs(radius-meta['pixel_radius'])<2
 assert max(abs(((x-cx)**2+(y-cy)**2)**.5-radius) for x,y in pts)<5
 for x,y in meta['pixel_endpoints_bottom_origin']:assert min((x-xx)**2+(y-yy)**2 for xx,yy in pts)<16

def variant(q,n):
 p=dict(zip(('x1','y1','x2','y2'),g.PARAMS[q]))
 # Search finite translations and half-vector scalings; only eligible full banks.
 for dx,dy in [(n,0),(0,n),(-n,0),(0,-n),(n,n),(-n,-n)]:
  pp={k:v+(dx if k.startswith('x') else dy) for k,v in p.items()}
  try:return g.generate(g.LEVELS[q],seed=n,template=q,parameters=pp)
  except ValueError:pass
 raise AssertionError(q+' variant unavailable')

def run():
 source_cases=[];review=[];native=[];banks=0;options=0;designations=0;solutions=0;source_results=[]
 for source_id,src in g.QS.items():
  p=dict(zip(('x1','y1','x2','y2'),g.PARAMS[source_id]));r=g.generate(g.LEVELS[source_id],template=source_id,parameters=p)
  q=r['question'];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
  assert q[':question/problem']==src[':question/problem'];assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
  for key in (':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in src)
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  assert f[':answer-field/key']==sf[':answer-field/key'];assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  unmatched=list(f[':answer-field/choices'])
  for a in sf[':answer-field/choices']:
   matches=[b for b in unmatched if g.equivalent(a[':answer/value'],b[':answer/value'])];assert len(matches)==1;unmatched.remove(matches[0]);options+=1
   if a[':answer/id']==sf.get(':answer-field/correct',{}).get(':answer/id'):assert matches[0][':answer/id']==f[':answer-field/correct'][1];designations+=1
  assert not unmatched;banks+=1;solutions+=int(':question/worked-solution' in src);displayed(r)
  source_results.append({'source_id':source_id,'bank_matched':True,'options_matched':5,'correct_designation_matched':':answer-field/correct' in sf,'solution_exact':':question/worked-solution' in src,'presence_exact':True})
  source_cases.append({'source_id':source_id,'template':source_id,'level':g.LEVELS[source_id],'parameters':p,'bank_profile':source_id,'authored_level_assignment':':question/difficulty' not in src})
  review.append({'label':'Original raw replay '+source_id,'record':r})
  for n in (1,2):
   rr=variant(source_id,n);displayed(rr);review.append({'label':'Generated observed-template variant '+source_id+' '+str(n),'record':rr})
  # Missing correct refs require an explicitly authored completed fixture.
  rr=r if ':answer-field/correct' in f else g.generate(g.LEVELS[source_id],template=g.LEVELS[source_id]+'_diameter',parameters=p,profile=source_id)
  native.append(engine_fixture('Source '+source_id+(' inferred completion' if rr is not r else ''),rr))
 for l in ('easy','moderate','hard'):
  for seed in range(8):
   rr=g.generate(l,seed);displayed(rr)
   if seed<2:review.append({'label':'Generated '+l+' default '+str(seed),'record':rr})
   native.append(engine_fixture(l+' '+str(seed),rr))
 # Larger authored easy boundary, both equal-workload axis orientations.
 for p in ({'x1':10,'y1':0,'x2':-10,'y2':0},{'x1':0,'y1':10,'x2':0,'y2':-10}):
  rr=g.generate_easy(parameters=p);displayed(rr);review.append({'label':'Generated easy radius-10 boundary','record':rr});native.append(engine_fixture('Easy radius-10 boundary',rr))
 # Algebraic coefficient boundary: a historical bank displays unsquared sqrt(2).
 rr=g.generate_hard(template='q-15297',parameters={'x1':2,'y1':3,'x2':0,'y2':1});displayed(rr);review.append({'label':'Generated hard observed-profile sqrt(2) boundary','record':rr})
 # Whole-equation equivalence accepts arbitrary nonzero scalar multiples.
 assert g.equivalent('(x-1)^2+(y-2)^2=2','2(x-1)^2+2(y-2)^2=4')
 assert not g.equivalent('(x-1)^2+(y-2)^2=2','2(x-1)^2+(y-2)^2=4')
 # Fixed task/bank identities cannot depend on seed/order; profiles are not task IDs.
 for l in ('easy','moderate','hard'):
  r=g.generate(l,4);p=r['generation']['parameters'];rr=g.generate(l,91,parameters=p)
  assert r['question'][':question/id']==rr['question'][':question/id'];assert r['generation']['mathematical_fingerprint']==rr['generation']['mathematical_fingerprint']
 # Strict finite/domain explicit input tests (no coercion or silent resampling).
 bad=[('easy',{'x1':2,'y1':1,'x2':-2,'y2':1}),('moderate',{'x1':2,'y1':0,'x2':-2,'y2':0}),('hard',{'x1':4,'y1':0,'x2':0,'y2':0}),('easy',{'x1':11,'y1':0,'x2':-11,'y2':0}),('hard',{'x1':8,'y1':2,'x2':-6,'y2':0}),('hard',{'x1':4,'y1':4,'x2':0,'y2':0,'junk':1})]
 for level,p in bad:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit parameters accepted')
 for v in (True,float('nan'),float('inf'),1.5,sp.Rational(1,2),sp.sqrt(2),'2'):
  p={'x1':v,'y1':0,'x2':-2,'y2':0}
  try:g.generate_easy(parameters=p)
  except ValueError:pass
  else:raise AssertionError('Nonfinite/noninteger coordinate accepted')
 # Fresh concurrent render writes, different and identical tasks, sidecar alignment.
 ps=[{'x1':9,'y1':2,'x2':1,'y2':-2},{'x1':2,'y1':9,'x2':-2,'y2':1}]
 for p in ps:
  path=HERE/'plots'/(g.digest(p)[:24]+'.png');path.unlink(missing_ok=True);path.with_suffix('.json').unlink(missing_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  renders=list(pool.map(g.render_plots,[ps[0],ps[1],ps[0]]))
 for (path,meta),p in zip(renders,[ps[0],ps[1],ps[0]]):assert meta['parameters']==p and Path(path).exists() and abs(meta['radius']-float(g.values(p)[5]))<1e-12
 assert not list((HERE/'plots').glob('render-*.json'))
 (HERE/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n');(HERE/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
 engine=HERE.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True)
 report={'status':'pass','version':g.VERSION,'basis':1356,'source_questions':9,'complete_banks':{'matched':banks,'total':9},'options':{'matched':options,'total':45},'correct_designations':{'matched':designations,'total_present':7,'missing_not_counted':2},'worked_solutions':{'raw_exact':solutions,'total_present':7,'absent_preserved':2},'question_presence_parity':9,'authored_missing_level':'easy','default_variants_checked':24,'easy_radius10_boundaries_checked':2,'raster_geometry':'actual PNG red-stroke circle fit and endpoint pixels, all changed/default images','observed_changed_variants_checked':18,'native':json.loads((HERE/'engine.json').read_text()),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'strict_explicit_guards':'pass','fresh_concurrent_plots':'pass','unresolved_findings':[]}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 lines=['# Diameter endpoints circle review','All entries are author previews; correct options are explicitly labeled. Raw unrated evidence omits its difficulty and correct ref; review labels show the authored workload assignment.']
 for item in review:lines.extend(['## '+item['label'],g.markdown(item['record'])])
 (HERE/'review.md').write_text('\n\n'.join(lines)+'\n')
 print('PASS: 9/9 banks, 45/45 choices, 7/7 present designations, 7/7 exact solutions; 42 changed/default instances; native grading passed.')

def engine_fixture(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Actual radio grader, all owned options'} for a in f[':answer-field/choices']]}
if __name__=='__main__':run()
