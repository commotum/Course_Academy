import copy, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
R=Path(__file__).resolve().parent
W=Path('/tmp/generator-live-pipeline/workspace')
REPO=Path('/home/jake/Developer/Course_Academy')
PY=Path('/home/jake/Developer/Course_Academy/.venv/bin/python')
sys.path.insert(0,str(REPO))
from scripts.generator_evidence import record_sha256, batch_sha256
from scripts.generator_native_build import build_inputs, ensure_native_grader
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
def save(name,value):
 (R/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def load(path):return json.loads(Path(path).read_text())
def call(argv,cwd=W,env=ENV):
 p=subprocess.run(list(map(str,argv)),cwd=cwd,env=env,capture_output=True,text=True)
 assert p.returncode==0,(argv,p.stderr[-3000:])
 return json.loads(p.stdout)
def read(record):
 q=record['question'];p=q[':question/problem']
 m=re.search(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',p,re.S)
 assert m
 a=[[int(t.strip()) for t in row.split('&')] for row in m.group(1).split(r'\\')]
 assert len(a)==2 and all(len(row)==2 for row in a)
 matches=re.findall(r'find \$a_\{([12])([12])\}',p)
 assert len(matches)==1
 i,j=map(int,matches[0]);v=a[i-1][j-1]
 # Independently inspect the complete displayed template, ignoring only neutral HTML wrappers.
 plain=re.sub(r'<[^>]+>','',p)
 assert re.fullmatch(r'For the matrix\s+\$A=\\begin\{pmatrix\}[-\d\s&\\]+\\end\{pmatrix\}\$\s+find \$a_\{[12][12]\}\$\.\s+\{\{answer\}\}',plain,re.S)
 assert 'style=' not in p and 'color' not in p
 f,=q[':question/answer-fields'];c,=f[':answer-field/choices']
 assert f[':answer-field/type']==':answer-field.type/blank' and f[':answer-field/key']=='answer'
 assert c[':answer/type']==':answer.type/math' and c[':answer/id']==f[':answer-field/correct'][-1]
 assert str(v)==c[':answer/value']
 sol=q[':question/worked-solution']
 observed=re.search(r'\$a_\{([12])([12])\}=(-?\d+)\$',sol)
 assert observed and tuple(map(int,observed.groups()))==(i,j,v)
 assert sol==(f'The first index is {i}, so use row {i}. The second index is {j}, so use column {j} of that row. $a_{{{i}{j}}}={v}$.')
 assert record['knowledge_point_id']==900001
 return a,i,j,v,observed.group(3)
initial=R/'supplied-files/f4e2cdd70726c82b96396236ac7094d8f74d21fac0ebb01521765e182285e82c/original-f4e2cdd70726c82b96396236ac7094d8f74d21fac0ebb01521765e182285e82c.json'
assert hashlib.sha256(initial.read_bytes()).hexdigest()=='f4e2cdd70726c82b96396236ac7094d8f74d21fac0ebb01521765e182285e82c'
assert (R/'source-analysis.json').read_bytes()==initial.read_bytes()
all_records=[];math_cases=[];paths=[];representatives=[]
chosen={'easy':[0,1,2],'moderate':[0,1,4],'hard':[0,1,2]}
for band in ['easy','moderate','hard']:
 records=load(R/f'delivery-{band}/accepted.json')
 for index,record in enumerate(records):
  a,i,j,v,observed=read(record)
  math_cases.append({'band':band,'index':index,'record_sha256':record_sha256(record),'matrix':a,'row':i,'column':j,'independent_value':v,'observed_solution_endpoint':observed,'keyed_answer':str(v),'derivation':f'Recall index order; select row {i}, column {j}; read {v}.','status':'passed'})
  all_records.append(record)
  if index in chosen[band]:
   representatives.append({'band':band,'index':index,'record':record})
   paths.append({'record_sha256':record_sha256(record),'field_index':0,'template':'independent-integer-entry','field_key':'answer','final_expression':observed,'keyed_answer':str(v),'domain':'2x2 integer matrix, one-based indices 1 or 2.','conclusion':f'Actual worked solution ends a_{i}{j}={observed}; integer directly matches selected cell and key.','sample_refs':[f'delivery-{band}/accepted.json','independent-math.json'],'status':'passed','conversions':[],'conversion_review':{'status':'none','reason':'Direct transcription of the integer at the requested position; no representation change is needed. No conversion negative control applies.','evidence_paths':['independent-math.json']}})
 for raw in load('/tmp/generator-live-pipeline/'+('samples.json' if band=='easy' else f'samples-{band}.json')):read(raw)
save('independent-math.json',{'cases':math_cases,'raw_and_delivered_checked':26})
save('representatives.json',representatives)
save('solution-paths.json',{'cases':paths})
# Source replay is executed through the real CLI and compared with all four original cases.
replay=call([PY,W/'generator.py','--replay','all','--format','json'])
original=load('/tmp/generator-live-pipeline/source/source-cases.json')
assert load(W/'source-cases.json')==original
source=load('/tmp/generator-live-pipeline/source/source.json')
comp=[]
for authored,original_case,captured in zip(replay,original,source['material']['synthetic_source_cases']):
 a,i,j,v,last=read(authored);p=original_case['parameters']
 assert (a,i,j,str(v))==(p['matrix'],p['row']+1,p['column']+1,original_case['answer'])
 assert authored['question'][':question/worked-solution']==captured['question'][':question/worked-solution']
 assert authored['question'][':question/difficulty']==':question.difficulty/easy'
 assert authored['question'][':question/answer-fields'][0][':answer-field/type']==captured['question'][':question/answer-fields'][0][':answer-field/type']
 comp.append({'source_id':original_case['id'],'source_db_id':captured['question'][':db/id'],'record_sha256':record_sha256(authored),'matrix':a,'displayed_indices':[i,j],'expected':original_case['answer'],'observed':str(v),'complete_blank_bank_matched':True,'solution_matched':True,'presentation':'Source escaped TeX is normalized; neutral matrix-operands layout and fresh identities preserve all numbers, indices, field key/type, answer and solution. No claim of byte equality.','status':'passed'})
save('source-replay-records.json',replay)
save('source-comparison.json',{'source_refs':['Tutorial dff2b933-538b-5a0c-acf6-09aa02994987, Lesson and Complete source practice; fixture-q11/q12/q21/q22, question IDs 910011–910014.'],'source_replay':comp,'complete_cases_matched':4,'complete_cases_total':4,'bank_count':'Each source case has one blank canonical math answer, no visible answer bank. All four complete blank contracts match.','original_context':'All four source labels are easy; prerequisite lists empty; no diagrams. No imports, source snapshots or learner state were modified.','investigation_and_anchor_comparison':'The investigation and approved anchors retain the same independent index recall, one-based spatial lookup and one-integer blank. The runtime uses the same operation with canonical matrix layout. Moderate/hard ranges are authored readability choices, uncalibrated.','task_preservation':'Prompt supplies matrix and a_ij only; learner recalls row/column order and counts from top/left. No arithmetic, multiple entries or guide is added. Exact worked row/column interpretation is confined to solutions.'})
# Test only declared runtime files outside the repository, with unrelated cwd/output roots.
manifest=load(W/'package.json');relocation=[]
with tempfile.TemporaryDirectory(prefix='generator-900001-review-') as tmp:
 tmp=Path(tmp);isolated=tmp/'package';isolated.mkdir();outside=tmp/'outside';outside.mkdir();out1=tmp/'out-one';out2=tmp/'out-two';out1.mkdir();out2.mkdir()
 for filename in manifest['files']:shutil.copy2(W/filename,isolated/filename)
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in isolated.iterdir()}
 for band,seed,count in [('easy',60419,3),('moderate',60421,5),('hard',60422,5)]:
  argv=['--difficulty',band,'--count',str(count),'--seed',str(seed),'--format','json']
  baseline=call([PY,W/'generator.py',*argv])
  moved=call([PY,'-I','-B','-c',"import runpy,sys; sys.path.insert(0,sys.argv[1]); sys.argv=sys.argv[2:]; runpy.run_path(sys.argv[0],run_name='__main__')",isolated,isolated/'generator.py',*argv],cwd=outside,env={**ENV,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(out1),'PYTHONPATH':''})
  again=call([PY,isolated/'generator.py',*argv],cwd=outside,env={**ENV,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(out2),'PYTHONPATH':''})
  saved=load('/tmp/generator-live-pipeline/'+('samples.json' if band=='easy' else f'samples-{band}.json'))
  assert moved==again==baseline==saved
  relocation.append({'band':band,'seed':seed,'count':count,'identical_repeated_relocated_records':True,'identities_preserved':True,'status':'passed'})
 assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in isolated.iterdir()}
 assert not list(out1.iterdir()) and not list(out2.iterdir())
save('relocation.json',{'cases':relocation,'only_declared_files':manifest['files'],'repository_or_ambient_imports_needed':False,'immutable_package_unchanged':True,'asset_result':'No assets by source task; both externally selected output directories remain empty.','dependencies':{'python':sys.version.split()[0],'packages':{}},'manifest_python':manifest['dependencies']['python']})
# Explicit edge cases and sampler coverage, independently judged from displayed content.
sys.path.insert(0,str(W));import generator
risk=[]
for band in ['easy','moderate','hard']:
 for matrix in [[[0,0],[0,0]],[[-2,-2],[-2,-2]],[[2,-3],[0,7]]]:
  for i in range(2):
   for j in range(2):
    record=generator.generate(matrix,i,j,band);read(record);risk.append(record)
save('risk-records.json',risk)
coverage=[];ordinary=[]
for band in ['easy','moderate','hard']:
 records=generator.sample(band,200,80701)
 expected=4*len(generator.values(band))**4
 assert generator.capacity(band)==load(W/'generation-limits.json')['maximum_distinct_batch'][band]==expected
 assert len({record['question'][':question/problem'] for record in records})==200
 parsed=[read(record) for record in records];ordinary.extend(records)
 for invalid in [(True,0),(2,0),(-1,0),(0,2)]:
  try:generator.generate([[1,2],[3,4]],invalid[0],invalid[1],band)
  except ValueError:pass
  else:raise AssertionError('Invalid index was accepted')
 try:generator.sample(band,expected+1,0)
 except ValueError:pass
 else:raise AssertionError('Over-capacity request accepted')
 coverage.append({'band':band,'seed':80701,'count':200,'capacity':expected,'positions':{str((i,j)):sum((x[1],x[2])==(i,j) for x in parsed) for i in [1,2] for j in [1,2]},'negative_targets':sum(x[3]<0 for x in parsed),'zero_targets':sum(x[3]==0 for x in parsed),'positive_targets':sum(x[3]>0 for x in parsed),'method':'Uniform sample without replacement from base-N four-cell codes with position as independent radix-4 digit. No rejection, sign, uniqueness or answer-rank guards.','status':'passed'})
save('ordinary-probe-records.json',ordinary)
save('sampler-coverage.json',{'coverage':coverage,'limits':'200 records per band are diagnostic samples, not exhaustive finite catalogs. Each band includes zero and both signs in its bank by code inspection; no per-batch coverage quota is imposed.','risk_cases':len(risk),'risk_cases_purpose':'Preserve repeated values, all-zero matrices and every requested position in every band, without adding operations. Explicit parameter tests are not evidence about sampler frequencies.'})
# Native grading uses application helper; this script only constructs independently justified inputs.
native=[]
for label,records in [('delivered',all_records),('replay',replay),('risk',[risk[n] for n in [0,7,12,19,24,31]])]:
 for index,record in enumerate(records):
  a,i,j,v,_=read(record)
  other=next((x for row in a for x in row if x!=v),v+1)
  reversed_value=a[j-1][i-1]
  wrong=reversed_value if reversed_value!=v else other
  controls=[{'field_index':0,'submitted':str(v),'expected':'accepted','purpose':f'Independent row {i}, column {j} lookup gives {v}.'},{'field_index':0,'submitted':f'{v}/1','expected':'accepted','control':'equivalent','purpose':f'{v}/1 is exactly the same integer; no form restriction is asked.'},{'field_index':0,'submitted':str(wrong),'expected':'rejected','control':'wrong','purpose':f'Wrong-cell lookup or distinct integer {wrong} differs from the requested {v}.'}]
  if v:controls.append({'field_index':0,'submitted':str(-v),'expected':'rejected','control':'wrong','purpose':f'Sign reversal {-v} differs from selected {v}.'})
  native.append({'label':f'{label}-{index}','record':record,'checks':controls})
save('grading-input.json',native)
# Include all nine deliberately selected delivered representatives and source zero endpoint.
save('render-input.json',[x['record'] for x in representatives]+[replay[2]])
# Exercise actual durable checker with bad key, bad support, and bad solution, retaining the concrete inputs.
from check_refill import check
base=copy.deepcopy(all_records[0]);assert check([base])['status']=='passed'
mutants={}
mutants['wrong-key']=copy.deepcopy(base);mutants['wrong-key']['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='1000001'
mutants['supplied-target-work']=copy.deepcopy(base);mutants['supplied-target-work']['question'][':question/problem']='Use row 2, column 1.\n'+mutants['supplied-target-work']['question'][':question/problem']
mutants['wrong-solution']=copy.deepcopy(base);mutants['wrong-solution']['question'][':question/worked-solution']='The answer is 1000001.'
checks=[]
for name,record in mutants.items():
 try:check([record])
 except (AssertionError,ValueError,KeyError):rejected=True
 else:rejected=False
 assert rejected
 checks.append({'control':name,'expected':'rejected','observed':'rejected','status':'passed'})
save('refill-negative-records.json',mutants)
save('refill-negative-controls.json',{'valid_original_passed':True,'controls':checks,'nearby_valid_cases':'Actual source zero, all-zero and repeated-value matrices pass the unmodified checker.','all_risk_records_passed':check(risk)['status']})
# Required evidence filenames are the current package plan's citations, populated with actual review work.
save('author-checks.json',{'producer':'independent final verifier, not an adopted author report','status':'passed','checks':['13 displayed delivery values and worked endpoints independently verified','all 4 original complete source cases replayed and matched','declared-file-only relocation and repeated deterministic CLI output in all bands','600 ordinary sampled records checked against displayed data','36 valid repeated/zero/all-position explicit cases checked','durable checker rejects wrong key, supplied location instructions and false solution; permits valid nearby cases'], 'evidence_paths':['independent-math.json','source-comparison.json','relocation.json','sampler-coverage.json','refill-negative-controls.json']})
# Confirm the native build used in this evaluation matches production exactly, without a shared-tree write.
isolated=W/'evidence/native-root';assert build_inputs(isolated)==build_inputs(REPO)
built=ensure_native_grader(isolated)
save('native-build.json',built)
print(json.dumps({'delivered_cases':len(all_records),'source_cases':len(replay),'representatives':len(representatives),'risk_cases':len(risk),'ordinary_samples':len(ordinary),'refill_failure_controls':len(checks),'native_build':built['binary_sha256'],'status':'passed'}))
