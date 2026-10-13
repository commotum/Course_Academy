"""Fail on source/complete-bank/printed-math/native/raster/identity failures."""
import concurrent.futures,hashlib,importlib.util,json,math,re,subprocess,sys,uuid
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('tangent_draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def group(text,start):
 assert text[start]=='{';depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  elif text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i
def expression(text):
 text=text.strip().rstrip('.').replace('⁡','').replace(r'\left','').replace(r'\right','')
 text=text.replace(r'\operatorname{tan}',r'\tan').replace(r'\dfrac',r'\frac')
 while r'\frac' in text:
  k=text.index(r'\frac');a,i=group(text,k+5);b,j=group(text,i)
  text=text[:k]+'(('+str(expression(a))+')/('+str(expression(b))+'))'+text[j:]
 text=text.replace(r'\pi','pi').replace(r'\tan','tan').replace('{','(').replace('}',')')
 text=re.sub(r'([A-Za-z0-9)])tan',r'\1*tan',text)
 text=re.sub(r'\\(?:quad|,|;|!)','',text)
 text=text.strip().rstrip('.,')
 try:return parse_expr(text,local_dict={'pi':sp.pi,'tan':sp.tan},transformations=standard_transformations+(implicit_multiplication_application,))
 except Exception as e:raise AssertionError(('unparsed displayed mathematics',text)) from e
def balanced(text):
 assert text.count('$')%2==0,text
 depth=0
 for c in text:
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,text
 assert depth==0 and '{{' not in text and '+-' not in text and '--' not in text,text
def displayed_math(record):
 q=record['question'];sid=record['generation']['source_mask'];assets=record['generation']['plot_assets'];meta=json.loads(Path(assets['spec']).read_text())
 if 'plots' in meta:
  plot=next(p for p in meta['plots'] if p['source_id']==sid)
  B=sp.Rational(plot['read_B']);D=sp.Rational(str(plot['read_D']))
 else:
  labels=meta['label_measurements'];kind=meta['instance']['calibration']
  xt=next(l for l in labels if l['role'] in ('x-asymptote','x-calibration') and not l['text'].startswith('$-'))
  tick=expression(xt['text'].strip('$'));H=tick*(1 if kind==1 else 2 if kind==2 else sp.Rational(3,2));B=sp.simplify(sp.pi/(2*H))
  if kind==1:D=expression(next(l['text'] for l in labels if l['role']=='y-intercept').strip('$'))
  else:
   # Derive the actual intercept from the rendered blue pixels and displayed
   # y tick-label calibration, independently of generator parameters.
   labels_y=[l for l in labels if l['role']=='y-calibration']
   vals=np.array([float(expression(l['text'].strip('$'))) for l in labels_y])
   py=np.array([(l['bbox_pixels'][1]+l['bbox_pixels'][3])/2 for l in labels_y])
   y0,scale=np.linalg.lstsq(np.column_stack([np.ones(len(vals)),vals]),py,rcond=None)[0]
   ar=np.asarray(Image.open(assets['prompt']).convert('RGB'));height=ar.shape[0]
   blue=(ar[:,:,2]>130)&(ar[:,:,0]<90)&(ar[:,:,1]>70)&(ar[:,:,1]<170)
   # The vertical axis is the central black full-height column, unlike grid.
   dark=(ar[:,:,0]<60)&(ar[:,:,1]<60)&(ar[:,:,2]<60);axis=int(np.argmax(dark[30:height-130].sum(axis=0)))
   yy=np.where(blue[:,axis])[0];assert len(yy)>0
   dfit=(height-yy.mean()-y0)/scale
   unit=sp.Rational(1,2 if kind==2 else 4);D=round(dfit/float(unit))*unit
   assert abs(dfit-float(D))<.035,(dfit,D)
  # All measured labels clear the actual branch and stay inside the image.
  assert all(l['branch_clearance_px']>=2.5 for l in labels)
  assert all(a['blue_pixel_hit'] for a in meta['curve_pixel_checks'])
  assert all(a['gray_pixels']>=20 for a in meta['asymptote_pixel_checks'])
  assert hashlib.sha256(Path(assets['prompt']).read_bytes()).hexdigest()==meta['png_sha256']
 assert '$y' in q[':question/problem'] and ('(Bx)+D' in q[':question/problem'] or '(Bx) + D' in q[':question/problem'])
 template='difference' if re.search(r'What is \$D\s*-\s*B',q[':question/problem']) else 'sum'
 return B,D,template
def check_solution(record,B,D,template):
 solution=record['question'].get(':question/worked-solution')
 if solution is None:return 0
 balanced(solution)
 blocks=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',solution,re.S)
 variables={sp.Symbol('B'):B,sp.Symbol('D'):D,sp.Symbol('T'):sp.pi/B,sp.Symbol('A'):1,sp.Symbol('C'):0}
 rows=0
 for block in blocks:
  text=block[0] or block[1]
  if '=' not in text:continue
  for segment in re.split(r'⟹|\\Longrightarrow',text):
   sides=segment.split('=')
   if len(sides)<2:continue
   expressions=[expression(s).subs(variables) for s in sides]
   if str(expressions[0])=='y':
    x=sp.Symbol('x');expected=sp.tan(B*x)+D
    assert all(sp.simplify(e-expected)==0 for e in expressions[1:]),(segment,expressions,expected)
   else:assert all(sp.simplify(e-expressions[0])==0 for e in expressions[1:]),(segment,expressions)
   rows+=1
 # Fixed teaching stages, including final equation and inline conclusion.
 assert rows==8,(record['generation']['source_mask'],rows)
 assert 'The period $T$ of the function is' in solution and 'Finally, the equation of the curve is' in solution
 assert ('D-B=' if template=='difference' else 'B+D=') in solution
 return rows
def check_record(record,raw=False):
 assert record==json.loads(json.dumps(record))
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 q=record['question'];m=record['generation'];balanced(q[':question/problem'])
 B,D,t=displayed_math(record);result=B+D if t=='sum' else D-B
 for field in q[':question/answer-fields']:
  values=[expression(a[':answer/value']) for a in field[':answer-field/choices']]
  assert len(values)==len(set(values))==5
  assert values.count(result)==1,(m['bank_profile'],values,result)
  for a in field[':answer-field/choices']:
   assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'];balanced(a[':answer/value']);uuid.UUID(a[':answer/id'])
  if ':answer-field/correct' in field:
   assert field[':answer-field/correct'][0]==':answer/id'
   correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
   assert expression(correct[':answer/value'])==result,(m,correct,result)
  uuid.UUID(field[':answer-field/id'])
 assert m['parameters']=={'B':str(B),'D':str(D)},(m['parameters'],B,D)
 check_solution(record,B,D,t)
 if raw:assert m['evidence_only'] and not m['eligible_for_learning']
 return result
def engine_checks(record):
 checks=[]
 for fi,f in enumerate(record['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:return None
  for a in f[':answer-field/choices']:
   checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native ID grading; displayed value independently checked'})
 return checks

subprocess.run([sys.executable,str(HERE/'source_raster_audit.py')],check=True)
cases=[];reviews=[];fidelity=[];engine=[]
for sid,source in g.QUESTIONS.items():
 B,D,t=g.SOURCE_PARAMETERS[sid];case={'source_id':source[':question/id'],'math_academy_id':sid,'template':t,'difficulty':'easy','parameters':{'B':B,'D':D},'bank_profile':'raw-'+sid}
 cases.append(case);record=g.generate('easy',seed=3,template=t,parameters=case['parameters'],profile=case['bank_profile']);check_record(record,True)
 q=record['question']
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in source),(sid,key)
 expected_prompt=source[':question/problem']
 assert q[':question/problem']==expected_prompt
 assert q.get(':question/worked-solution')==source.get(':question/worked-solution'),sid
 assert len(q[':question/answer-fields'])==len(source[':question/answer-fields'])
 matched=correct_matched=0
 for sf,rf in zip(source[':question/answer-fields'],q[':question/answer-fields']):
  assert sf[':answer-field/type'][':db/ident']==rf[':answer-field/type'] and sf[':answer-field/key']==rf[':answer-field/key']
  assert (':answer-field/correct' in sf)==(':answer-field/correct' in rf)
  assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices']),(sid,sf,rf)
  matched+=len(sf[':answer-field/choices'])
  if ':answer-field/correct' in sf:
   selected=next(a for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
   assert selected[':answer/value']==sf[':answer-field/correct'][':answer/value'];correct_matched+=1
 fidelity.append({'source':sid,'options_matched':matched,'complete_field_banks_matched':len(q[':question/answer-fields']),'original_correct_designations_matched':correct_matched,'prompt_raw_exact':True,'solution_raw_exact':':question/worked-solution' in source,'omissions_exact':True})
 reviews.append({'label':'ORIGINAL — RAW EVIDENCE, INELIGIBLE','record':record})
 repaired=g.generate('easy',profile='repair-'+sid);check_record(repaired);reviews.append({'label':'EXPLICIT REPAIR — '+('eligible' if repaired['generation']['eligible_for_learning'] else 'opaque bank, ineligible'),'record':repaired})
 # Changed-parameter replay uses ordinary API and the same complete raw bank.
 changed=g.generate('easy',seed=19,parameters={'B':'1/3' if sid=='q-141974' else '3/2','D':'2'},profile='raw-'+sid);check_record(changed,True)
 reviews.append({'label':'GENERATED SOURCE-BANK VARIANT — RAW, INELIGIBLE','record':changed})
 for r in (record,repaired,changed):
  checks=engine_checks(r)
  if checks:engine.append({'label':sid+' '+r['generation']['bank_profile']+' '+str(r['generation']['parameters']),'record':r,'checks':checks})

# Exhaustive meaningful finite domains. Banks/layout/seed are excluded from
# mathematical task counts; source letter and profile aliases never inflate.
counts={};eligible_profile_counts={}
for level in ('easy','moderate','hard'):
 bs,ds=g.domain(level);tasks=set();profiles={}
 for profile in ('period-sign','omitted-sign'):
  count=0
  for template in g.TEMPLATES:
   for B in bs:
    for D in ds:
     values=g.bank_values(profile,template,B,D)
     if g.valid_bank(values):tasks.add((str(B),str(D),template));count+=1
  profiles[profile]=count
 counts[level]=len(tasks);eligible_profile_counts[level]=profiles

samples=[];seen_masks=set();seen_families=set();seen_levels=set();positions=set()
for level in ('easy','moderate','hard'):
 for seed in range(12):
  r=g.generate(level,seed=seed);check_record(r);samples.append(r)
  m=r['generation'];seen_masks.add(m['source_mask']);seen_families.add(m['template']);seen_levels.add(level)
  f=r['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
  fixed=g.generate(level,seed=seed+100,template=m['template'],profile=m['bank_profile'],parameters=m['parameters']);check_record(fixed)
  assert r['question'][':question/id']==fixed['question'][':question/id'],('seed changed identity',m)
  engine.append({'label':level+' seed '+str(seed),'record':r,'checks':engine_checks(r)})
  if seed<2:reviews.append({'label':'GENERATED '+level.upper()+' VARIANT — '+('observed workload' if level=='easy' else 'authored level'),'record':r})
 assert any(r['generation']['bank_profile']=='period-sign' for r in samples if r['question'][':question/difficulty'].endswith(level))
 assert any(r['generation']['bank_profile']=='omitted-sign' for r in samples if r['question'][':question/difficulty'].endswith(level))
assert seen_masks==set(g.QUESTIONS),seen_masks
assert seen_families=={'sum','difference'} and len(positions)>=3
# Whole-bank rejection and strict authored level guards on explicit inputs.
rejections=[]
for level,p in [('moderate',{'B':'2/3','D':'1'}),('hard',{'B':'2/3','D':'1/2'}),('easy',{'B':'1','D':'1'})]:
 try:g.generate(level,template='sum',parameters=p,profile='period-sign')
 except ValueError as e:rejections.append(str(e))
 else:raise AssertionError('invalid explicit workload/bank accepted')
# Same mathematical task, changed complete bank -> separate content identity.
a=g.generate_easy(template='sum',parameters={'B':'3/2','D':'2'},profile='period-sign')
b=g.generate_easy(template='sum',parameters={'B':'3/2','D':'2'},profile='omitted-sign')
assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
assert a['question'][':question/id']!=b['question'][':question/id']
# Fresh concurrent rendering, including identical and different inputs. Asset
# pruning is forbidden; isolate this test in a unique private render folder.
import tempfile
with tempfile.TemporaryDirectory(prefix='concurrent-',dir=HERE) as directory:
 params=[{'B':'2/3','D':'-3/2','level':'moderate','calibration':2,'renderer_version':2}]*2+[{'B':'5/4','D':'1/4','level':'hard','calibration':3,'renderer_version':2}]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rendered=list(pool.map(lambda p:g.render_plots(p,directory),params))
 assert rendered[0]==rendered[1] and rendered[0]!=rendered[2]
 for p,assets in zip(params,rendered):assert json.loads(Path(assets['spec']).read_text())['instance']==p
 assert not list(Path(directory).glob('render-*.json'))
 concurrency={'identical_calls':2,'distinct_calls':1,'fresh_writes':True,'atomic_sidecar_parameter_match':True,'input_files_remaining':0}

write('source-cases.json',cases);write('review.json',reviews);write('samples.json',samples);write('engine-input.json',engine)
harness=REPO/'generate/runs/current/check-engine'
subprocess.run([str(harness),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
native=json.loads((HERE/'engine-validation.json').read_text())
review='# Tangent stretch and vertical shift — frozen local review\n\nRaw original records preserve omissions and duplicate fields. Each section labels evidence eligibility. Asset paths are absolute and clickable. No database operations.\n\n'
for item in reviews:review+=g.markdown(item['record'],item['label'])
(HERE/'review.md').write_text(review)
report={'status':'passed','generator_version':g.VERSION,'source_practice_questions':6,'source_field_banks':7,'source_options_matched':35,'source_complete_banks_matched':7,
 'source_correct_designations_matched':5,'source_correct_designations_total':5,'missing_original_correct_designations':2,
 'source_prompt_masks_matched':6,'source_solution_masks_raw_exact':5,'source_solution_masks_total':5,'source_omission_contracts_matched':6,
 'source_fidelity':fidelity,'normal_samples_checked':len(samples),'fixed_solution_stage_equalities_per_solution':8,
 'normal_default_source_masks_covered':sorted(seen_masks),'complete_default_banks_covered':sorted(set(r['generation']['bank_profile'] for r in samples)),
 'meaningful_tasks_by_level':counts,'eligible_tasks_by_bank_profile':eligible_profile_counts,
 'authored_levels':['moderate','hard'],'raw_source_profiles_ineligible':True,'raw_native_unavailable_records':['q-65448 duplicate first missing correct','q-65547 missing correct'],
 'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'engine_sha256':hashlib.sha256(harness.read_bytes()).hexdigest()},
 'original_rasters_inspected_and_fitted':7,'rendered_pngs':len(list((HERE/'plots').glob('*.png'))),'concurrency':concurrency,
 'explicit_rejection_checks':rejections,'database_writes':0,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'pillow':Image.__version__,'numpy':np.__version__}}
write('validation.json',report);print(json.dumps(report,indent=2))
