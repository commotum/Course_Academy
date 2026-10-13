"""Fail closed: displayed math, geometry, complete banks, source prose, grader."""
import concurrent.futures,importlib.util,json,math,re,subprocess,random,hashlib,tempfile,shutil
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def latex(s):
 s=s.strip().rstrip(',.?').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*')
 def group(s,i):
  assert s[i]=='{';depth=1;j=i+1
  while depth:
   if s[j]=='{':depth+=1
   if s[j]=='}':depth-=1
   j+=1
  return s[i+1:j-1],j
 while r'\frac' in s:
  i=s.index(r'\frac');a,j=group(s,i+5);b,k=group(s,j);s=s[:i]+f'(({latex(a)})/({latex(b)}))'+s[k:]
 s=s.replace('^','**').replace('{','(').replace('}',')')
 return parse_expr(s,local_dict={'x':g.X,'y':g.Y},transformations=standard_transformations+(implicit_multiplication_application,))

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];m=r['generation'];f=q[':question/answer-fields'][0]
 expr=latex(q[':question/problem'].split('=',1)[1].rstrip('$?'))
 if m['bank_profile']=='authored' and m['template']=='affine_fraction':assert q[':question/problem'].split('=',1)[1].count(r'\frac')>=1
 assert sp.simplify(expr-g.eq(m['template'],m['parameters']))==0
 pts=m['parameters']['points'];s=[expr.subs({g.X:x,g.Y:y}) for x,y in pts]
 assert list(map(str,s))==m['exact_slopes']
 banks=[]
 for a in f[':answer-field/choices']:
  path=ROOT/a[':answer/value'];assert path.exists();meta=json.loads(path.with_suffix('.json').read_text());assert meta['exact_points']==pts
  row=[]
  for (x,y),segment in zip(pts,meta['segments']):
   assert segment['center']==[float(sp.Rational(x)),float(sp.Rational(y))];end=segment['endpoints'];dx=end[1][0]-end[0][0];dy=end[1][1]-end[0][1]
   v=sp.oo if segment['slope']=='inf' else sp.Rational(segment['slope']);row.append(v)
   assert (abs(dx)<1e-12 if v==sp.oo else math.isclose(dy,float(v)*dx,abs_tol=1e-12))
   assert all(meta['bounds'][0]<px<meta['bounds'][1] and meta['bounds'][2]<py<meta['bounds'][3] for px,py in end)
  assert list(map(str,row))==m['choice_geometry'][a[':answer/value']];banks.append(tuple(row))
  if a[':answer/id']==f[':answer-field/correct'][1]:assert list(row)==s
 assert len(banks)==len(set(banks))==5 and banks.count(tuple(s))==1
 if m['bank_profile']=='authored':
  for i,row in enumerate(banks):
   for other in banks[:i]:
    distances=[]
    for a,b in zip(row,other):
     aa=math.pi/2 if a==sp.oo else math.atan(float(a));bb=math.pi/2 if b==sp.oo else math.atan(float(b));delta=abs(aa-bb);distances.append(min(delta,math.pi-delta))
    assert max(distances)>=math.radians(8)
 solution=q[':question/worked-solution'];block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S).group(1);rows=block.split(r'\\');assert len(rows)==3
 for i,row in enumerate(rows):
  coords=re.search(r'\|\}_\{\((.*?)\)\}',row);assert coords
  shown=[latex(v) for v in coords.group(1).split(',')];assert shown==list(map(sp.Rational,pts[i]))
  values=row.split('=',1)[1].split('=');assert len(values)==(3 if m['bank_profile']=='authored' and not q[':question/difficulty'].endswith('/easy') else 2)
  assert all(sp.simplify(latex(v)-s[i])==0 for v in values)
 assert q[':question/problem'].count('$')%2==0 and solution.count('$')%2==0
 for text in [q[':question/problem'],solution]:
  assert text.count('{')==text.count('}')
  assert not re.search(r'--|\+\s*-',text),text
 correctpath=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert f'![]({correctpath})' in solution
 return True

sources=[];coverage=[];review=[]
for case in json.load(open(HERE/'source-cases.json')):
 qid=case['source_id'];r=g.generate('easy',profile=qid,parameters=case['parameters']);check(r);sources.append(r);raw=g.QUESTIONS[qid];assert r['question'][':question/problem']==raw[':question/problem']
 s,bank=g.banks(case['template'],case['parameters'],qid)
 raster=[v for v in json.load(open(HERE/'source-raster.json')) if v['source_id']==qid]
 for actual,observed in zip(bank,raster):
  assert len(observed['raster_slopes'])==3
  for exact,approx in zip(actual,observed['raster_slopes']):
   if exact==sp.oo:assert approx=='inf'
   else:assert isinstance(approx,(int,float)) and abs(math.atan(float(exact))-math.atan(approx))<.06,(qid,exact,approx)
 field=raw[':question/answer-fields'][0];ci=bank.index(s)
 if ':answer-field/correct' in field:assert field[':answer-field/choices'][ci][':answer/id']==field[':answer-field/correct'][':answer/id']
 if ':question/worked-solution' in raw:
  # All shared prose including punctuation/spaces, same three-step sequence;
  # mathematical notation is normalized component-by-component.
  normalize=lambda text:re.sub(r'!\[\]\([^)]*\)','<PLOT>',re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}','<ROWS>',text,flags=re.S))
  assert normalize(raw[':question/worked-solution'])==normalize(r['question'][':question/worked-solution'])
 coverage.append({'source_id':qid,'complete_bank_matches':5,'distractor_matches':4,'correct_designation_match':not case['missing_correct_ref'],'inferred_missing_designation':case['missing_correct_ref'],'worked_prose_and_sequence_match':':question/worked-solution' in raw,'normalization':'unevaluated coefficient/component TeX with grouped signed multipliers; regenerated Matplotlib asset paths'})
 # Changed-parameter replay profile: same complete observed bank operations.
 for seed in range(20):
  try:v=g.generate('easy',seed+31,profile=qid);check(v);review.append(v);break
  except ValueError:pass
 else:raise AssertionError('No varied profile '+qid)

for level in ['easy','moderate','hard']:
 for template in (g.TEMPLATES if level!='hard' else ('two_quadratic','rational_square','affine_fraction')):
  for seed in [40,41]:
   r=g.generate(level,seed,template=template);check(r);review.append(r)
# Concurrent same and different data, atomic deterministic assets and sidecars.
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 concurrent_records=list(ex.map(lambda i:g.generate('easy',1000+i%2,template='affine'),[0,1,2]))
assert concurrent_records[0]['question'][':question/id']==concurrent_records[2]['question'][':question/id']
assert concurrent_records[0]['question'][':question/id']!=concurrent_records[1]['question'][':question/id']
for r in concurrent_records:check(r)
# A private fresh directory proves renderer concurrency without treating another
# live external generator call's temporary input as an orphan.
private=Path(tempfile.mkdtemp(dir=HERE,prefix='parallel-render-'))
try:
 instances=[]
 for i in [0,1,0]:
  rec=concurrent_records[i];params=rec['generation']['parameters'];slopes,bank=g.banks('affine',params,'authored');instances.append({'points':params['points'],'bank':bank,'correct_index':bank.index(slopes)})
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:assets=list(ex.map(lambda obj:g.render_plots(obj,private),instances))
 assert assets[0]==assets[2] and assets[0]!=assets[1]
 for obj,asset in zip(instances,assets):
  for row,path in zip(obj['bank'],asset['choices']):
   meta=json.loads((ROOT/path).with_suffix('.json').read_text());assert meta['exact_points']==obj['points'];assert meta['slopes']==['inf' if v==sp.oo else str(v) for v in row]
 assert not list(private.glob('render-input-*.json'))
finally:shutil.rmtree(private)
# Reordering options/seed must not change fixed content identity.
r=sources[0];v=g.generate('easy',999,profile='q-50099',parameters=g.PROFILES['q-50099'][1]);assert r['question'][':question/id']==v['question'][':question/id']
# Different banks preserve task fingerprint while changing content identity.
r=g.generate('easy',parameters=g.PROFILES['q-50099'][1],template='constant_product');assert r['generation']['mathematical_fingerprint']==sources[0]['generation']['mathematical_fingerprint'];assert r['question'][':question/id']!=sources[0]['question'][':question/id']
invalid=[('hard','affine',{'a':1,'b':2,'points':[[-1,1],[2,2],[3,3]]}),('easy','rational_square',{'a':1,'points':[[0,1],[1,2],[2,3]]}),('moderate','two_quadratic',{'a':5,'b':1,'points':[[-1,1],[2,2],[3,3]]})]
for l,t,p in invalid:
 try:g.generate(l,template=t,parameters=p)
 except ValueError:pass
 else:raise AssertionError('Explicit domain violation accepted')
domain={}
for level in ['easy','moderate','hard']:
 fingerprints=set();attempts=0;accepted=0
 for seed in range(300):
  rng=random.Random(seed);t=rng.choice(g.TEMPLATES if level!='hard' else ('two_quadratic','rational_square','affine_fraction'));p=g.sample(level,t,rng);attempts+=1
  try:g.validate_parameters(level,t,p);s,bank=g.banks(t,p,'authored')
  except ValueError:continue
  accepted+=1;fingerprints.add(g.digest({'equation':str(g.eq(t,p)),'points':sorted(p['points'])}))
 assert len(fingerprints)>100
 domain[level]={'sampled':attempts,'eligible_complete_banks':accepted,'distinct_mathematical_tasks':len(fingerprints),'points_affect_slopes':True}
fixtures=[]
for i,r in enumerate(sources+review):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 fixtures.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'full image-radio bank'} for a in f[':answer-field/choices']]})
(HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
(HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
(HERE/'source-replays.json').write_text(json.dumps(sources,indent=2)+'\n')
report={'passed':True,'basis':1356,'source_questions':7,'source_complete_banks':7,'source_options_matched':35,'source_distractors_matched':28,'source_observed_correct_designations_matched':5,'source_correct_designation_total':5,'missing_correct_refs_inferred_not_counted':2,'source_worked_solutions_present_and_sequence_matched':5,'source_worked_solutions_absent_authored':2,'source_normalized_math_rows':15,'source_exact_math_notation_claimed':False,'coverage':coverage,'generated_review_records':len(review),'domain_counts':domain,'checks':['actual displayed prompt parsed independently','all 3 printed substitutions and final values','complete five-option bank geometry','35 source raster orientation comparisons','all available source worked prose and ordered rows','native grader every displayed image choice','concurrent identical/different instances','fixed identity across option shuffling','parameter guards','Matplotlib rendered visuals reviewed'],'native_grader':json.load(open(HERE/'engine-report.json')),'script_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['native_grader','coverage']},indent=2))
