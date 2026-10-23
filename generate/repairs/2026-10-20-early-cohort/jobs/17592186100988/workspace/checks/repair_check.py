"""Retained regressions inspect CURRENT output, never the runner's old batch.
Run with the job Python: python checks/repair_check.py
"""
import collections, copy, importlib.util, json, os, pathlib, re, subprocess, sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[1]
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
SOURCE=ROOT.parent/'source/source.json'; INVENTORY=ROOT.parent/'source/inventory.json'
OUT=ROOT/'evidence'; OUT.mkdir(exist_ok=True); (OUT/'assets').mkdir(exist_ok=True)
ENV={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(OUT/'assets'),'PYTHONDONTWRITEBYTECODE':'1'}
COMMANDS=[]
def save(name,value): (OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def run(args):
 COMMANDS.append([str(x) for x in args]);p=subprocess.run(args,cwd=ROOT,env=ENV,text=True,capture_output=True)
 if p.returncode: raise AssertionError(f'Command failed: {args}\n{p.stdout[-2500:]}\n{p.stderr[-2500:]}')
 return p.stdout
spec=importlib.util.spec_from_file_location('candidate',ROOT/'17592186100988.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def identify(r):
 q=r['question'];text=q[':question/problem']
 m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',text,re.S)
 a=[[int(x.strip()) for x in row.split('&')] for row in m[1].split(r'\\')]
 ix=re.search(r'\$\{?([a-z])\}?_\{(\d)(\d)\}',text);i,j=int(ix[2]),int(ix[3])
 v=str(a[i-1][j-1]) if i<=len(a) and j<=len(a[0]) else 'No such entry'
 return a,i,j,v
def key(r):
 f=r['question'][':question/answer-fields'][0];ref=f.get(':answer-field/correct')
 aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1] if ref else None
 return next((a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid),None)
def math_check(records):
 for r in records:
  a,i,j,v=identify(r);q=r['question'];f=q[':question/answer-fields'][0];values=[x[':answer/value'] for x in f[':answer-field/choices']]
  assert key(r)==v,(q[':question/id'],v,key(r))
  assert len(values)==len(set(values))
  assert len(values)==(5 if f[':answer-field/type'].endswith('/radio') else 1)
  sol=q[':question/worked-solution']
  assert (f'${i}$' in sol and f'${j}$' in sol)
  assert ('no such entry' in sol.lower()) if v=='No such entry' else ('='+v+'.$') in sol
  sm=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',sol,re.S)
  assert [[int(x.strip()) for x in row.split('&')] for row in sm[1].split(r'\\')]==a
 return {'checked':len(records),'failures':[]}
def cue_report(records,require_contrast=False):
 groups={}; semantic=set();shapes=collections.Counter();numeric_3x2=0
 for r in records:
  a,i,j,v=identify(r);semantic.add((len(a),len(a[0]),i,j,v));shapes[f'{len(a)}x{len(a[0])}']+=1
  q=r['question'];f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];values=[x[':answer/value'] for x in choices]
  if f[':answer-field/type'].endswith('/radio') and 'No such entry' not in values and (len(a),len(a[0]))==(3,2):numeric_3x2+=1
  if 'No such entry' not in values:continue
  # Rendered prompt structure, not generation metadata.
  layout='display' if '$$' in q[':question/problem'] else 'inline'
  group=groups.setdefault(layout,{'valid':0,'absent':0,'key_positions':collections.Counter(),'labels':{}})
  case='absent' if v=='No such entry' else 'valid';group[case]+=1
  group['key_positions'][str(values.index(v))]+=1
  label=re.search(r'matrix \$([A-Z])',q[':question/problem'])[1]
  group['labels'].setdefault(label,{'valid':0,'absent':0})[case]+=1
 if require_contrast:
  assert groups,'No absence-bearing radio cases tested'
  assert all(x['valid'] and x['absent'] for x in groups.values()),groups
 return {'count':len(records),'semantic_instances':len(semantic),'shapes':shapes,'numeric_only_3x2':numeric_3x2,'layout_cues':groups}
def delivery(name,records):
 save(name+'.json',records)
 run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',OUT/(name+'.json'),'--source',SOURCE,'--inventory',INVENTORY,'--difficulty','easy','--output',OUT/(name+'-delivery'),'--asset-root',OUT/'assets','--math-root','/media/jake/SSD/EDB/math'])
 return json.loads((OUT/(name+'-delivery')/'accepted.json').read_text())
def cli(seed,count):
 return json.loads(run([sys.executable,ROOT/'17592186100988.py','--difficulty','easy','--count',str(count),'--seed',str(seed),'--format','json']))
# Exact retained failures from the independent review.
run([sys.executable,ROOT/'checks/source_regression.py','--package',ROOT,'--output',OUT/'source-regression-results.json'])
original_results=json.loads((OUT/'source-regression-results.json').read_text())
controls=[x['record'] for x in original_results['cases']]
assert set(x[':answer/value'] for x in controls[1]['question'][':question/answer-fields'][0][':answer-field/choices'])=={'1','-3','4','-1','5'}
# Whole affected domains: eight canonical cells; six two-column numeric-bank cells.
for m,n,profile in [(2,4,'blank'),(3,2,'four_locations')]:
 a=[[row*n+col-4 for col in range(n)] for row in range(m)]
 for i in range(1,m+1):
  for j in range(1,n+1):controls.append(g.generate('easy',981,profile=profile,parameters={'matrix':a,'i':i,'j':j,'letter':'E'}))
# Same layout/label/matrix/seed, relevant index changes; irrelevant changes preserve answer.
p={'matrix':[[1,2,3],[4,5,6]],'i':1,'j':2,'letter':'A'}
pairs=[]
for style in ('inline_radio','inline_no_entry_radio','display_radio','display_should_radio','display_noperiod_radio'):
 before=g.generate('easy',981,template=style,profile='location_no_entry',parameters=p)
 for change,profile,expected in [({'i':3},'overflow_locations','No such entry'),({'j':4},'overflow_locations','No such entry'),({'i':2},'location_no_entry','5'),({'letter':'Y'},'location_no_entry','2'),({'matrix':[[1,2,8],[4,5,6]]},'location_no_entry','2')]:
  pp=copy.deepcopy(p);pp.update(change);after=g.generate('easy',981,template=style,profile=profile,parameters=pp)
  assert identify(before)[3]=='2' and identify(after)[3]==expected
  controls.extend([before,after]);pairs.append({'style':style,'change':change,'before':before['question'][':question/id'],'after':after['question'][':question/id'],'expected':expected})
math_check(controls);save('counterfactuals.json',pairs)
# Replay every source bank and all available fields, preserving missing attributes.
source=json.loads(SOURCE.read_text());replay=[]
def ty(x):return x[':db/ident'] if isinstance(x,dict) else x
def norm(x):return re.sub(r'\s+','',x.replace('[\\begin{aligned}','\\begin{bmatrix}').replace('\\end{aligned}]','\\end{bmatrix}'))
for q in source['material']['kp'][':knowledge-point/questions']:
 r=g.generate('easy',profile='raw:'+q[':question/math-academy-id']);rq=r['question'];f=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
 checks={'prompt':norm(q[':question/problem'])==norm(rq[':question/problem']),'solution':norm(q.get(':question/worked-solution',''))==norm(rq.get(':question/worked-solution','')),'bank':sorted((ty(a[':answer/type']),a[':answer/value']) for a in f[':answer-field/choices'])==sorted((ty(a[':answer/type']),a[':answer/value']) for a in rf[':answer-field/choices']),'key':key({'question':q})==key(r),'difficulty':ty(q.get(':question/difficulty'))==ty(rq.get(':question/difficulty')),'field':ty(f[':answer-field/type'])==ty(rf[':answer-field/type'])}
 assert all(checks.values()),(q[':question/id'],checks)
 replay.append({'source_id':q[':question/id'],'checks':checks,'record':r})
save('source-replay.json',replay)
# Review's exact ordinary-sampling window, including rejection/resampling paths.
samples=[g.generate('easy',s) for s in range(720010,720130)]
math_check(samples);sample_after=delivery('samples',samples);math_check(sample_after)
coverage={'samples_before':cue_report(samples,True),'samples_after':cue_report(sample_after,True)}
assert coverage['samples_after']['numeric_only_3x2']>0
assert coverage['samples_after']['shapes'].get('2x4',0)>0
# Explicitly inspect every template's absence decision, not merely aggregate layouts.
for style in ('inline_radio','inline_no_entry_radio','display_radio','display_should_radio','display_noperiod_radio'):
 rows=[r for r in samples if r['generation']['template']==style]
 cue_report(rows,True)
# Current CLI prospective batch at exact job inputs plus the other reported seed.
for seed in (4036014604,4036014606):
 records=cli(seed,5);assert records==cli(seed,5),'Non-deterministic CLI'
 math_check(records);name='prospective-batch' if seed==4036014604 else 'second-batch';after=delivery(name,records)
 math_check(after);assert len(after)==5
 coverage[name]={'before':cue_report(records,True),'after':cue_report(after,True)}
# Small seed/count regression: deterministic construction, no unpaired layout cue.
for seed,count in ((0,2),(1,3),(2,4),(3,6),(4,7),(5,8)):
 rows=cli(seed,count);math_check(rows);cue_report(rows,True)
# Controlled tests must survive publication too (deduplicating repeated base records).
control_after=delivery('controls',controls);math_check(control_after);cue_report(control_after,True)
save('coverage.json',coverage)
# Actual native grader inputs: all distinct affected controls and prospective records.
unique={r['question'][':question/id']:r for r in controls+json.loads((OUT/'prospective-batch.json').read_text())}
grading=[]
for r in unique.values():
 v=identify(r)[3];f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==v else 'rejected','purpose':'independent visible row/column or bounds witness'} for a in f[':answer-field/choices']]
 else:
  checks=[{'submitted':s,'expected':e,'purpose':'scalar entry and equivalent notation'} for s,e in [(v,'accepted'),(str(2*int(v))+'/2','accepted'),(v+'.0','accepted'),(str(int(v)+1),'rejected')]]
 grading.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
save('grader-input.json',grading)
run([REPO/'generate/runs/current/check-engine',OUT/'grader-input.json',OUT/'grader-results.json'])
# Six representatives cover both layouts, both existence decisions, new shape/bank and blank.
render=[controls[0],controls[1],controls[2],controls[3]]
for layout,case in [('inline','valid'),('inline','absent')]:
 render.append(next(r for r in controls if ('$$' not in r['question'][':question/problem']) and (identify(r)[3]=='No such entry')==(case=='absent')))
save('render-records.json',render)
inv=json.loads(INVENTORY.read_text());generated=[q for q in inv['questions'] if any('generat' in k for k in q)]
assert not generated,'Inventory requires separate generated-record investigation'
save('inventory-analysis.json',{'basis':inv['basis'],'original_questions':[{'id':q[':question/id'],'entity_id':q[':db/id'],'source':q.get(':question/math-academy-id'),'eligible':key({'question':q}) is not None and not q.get(':question/retired',False)} for q in inv['questions']],'generated_records':0,'finding':'Verified captured inventory contains only original source records; no historical generated-pool defects demonstrated.'})
save('affected-inventory.json',{'affected_questions':[]})
save('commands.json',COMMANDS)
save('repair-results.json',{'status':'passed','source_banks':len(replay),'control_records':len(controls),'distinct_controls_after_delivery':len(control_after),'normal_samples':len(samples),'prospective_batch':5,'native_grader_records':len(grading),'native_grader_checks':sum(len(x['checks']) for x in grading),'retained_findings':['6fe521c09fbe226f09cf','05aea05dfa8bdd6f4d11','dd308c275d525eec01fa'],'limitations':['No learner-specific history or live inventory supplied; shared delivery filtering uses captured inventory.']})
print((OUT/'repair-results.json').read_text())
