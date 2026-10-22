"""Complete pipeline, captured legacy inventory and native grader tests. Read-only."""
import importlib.util,sys
sys.dont_write_bytecode=True
from pathlib import Path
spec=importlib.util.spec_from_file_location('independent',Path(__file__).with_name('revision-audit.py'));a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
g=a.g;ROOT=a.ROOT;JOB=a.JOB;PKG=a.PKG;save=a.save;load=a.load
import json,copy,re,hashlib,subprocess,os,types
# Read-only frozen-generator replay of the already demonstrated stored defect.
old=types.ModuleType('old');old.__file__=str(PKG/'17592186119805.py');exec(compile((PKG/'evidence/generator-before.py').read_text(),str(PKG/'evidence/generator-before.py'),'exec'),old.__dict__)
inv=load(JOB/'source/inventory.json');generated=[];affected=[]
for q in inv['questions']:
 if q.get(':question/math-academy-id'):continue
 av,u,*_=a.mats(q[':question/problem']);c=int(re.search(r'if \$(\d+)',q[':question/problem'])[1]);p={'a':list(map(int,av)),'u':list(map(int,u)),'c':c,'s':None,'letter':'k'}
 r=old.generate('moderate',64193,'q-34570',p)
 assert r['question'][':question/id']==q[':question/id'] and r['question'][':question/problem']==q[':question/problem'];assert a.key(r['question'])==a.key(q);a.verify(r)
 generated.append(r);affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Historical generator v1.0.0 forced every homogeneous question to No solution. Stored arithmetic is correct; fixed-family shortcut persists in these unmodified legacy records. Current v1.1.0 normal sampling no longer forces that outcome.','reproduction':str(a.PY)+' pipeline-audit.py; frozen v1.0.0 q-34570 seed=64193 parameters='+json.dumps(p,sort_keys=True),'evidence_path':'generated-records.json'})
save('generated-records.json',generated);save('affected-inventory.json',{'affected_questions':affected,'audit_scope':{'basis':inv['basis'],'questions':len(inv['questions']),'source_questions_not_marked_generated':13,'all_non_source_entries_reproduced':len(generated),'status':'Two historical affected records remain; no database changes. This does not attribute a continuing universal defect to the repaired generator.'}})
# Instrument native batch generation without changing code or consuming extra RNG values.
counts=[]
for level in g.LEVELS:
 original=g.generate;attempts=[]
 def track(*args,**kwargs):
  r=original(*args,**kwargs);attempts.append(r);return r
 g.generate=track
 rs=g.batch(level,20,823741)
 g.generate=original
 save('resampling-'+level+'.json',{'seed':823741,'requested_count':20,'attempt_records':attempts,'accepted_records':rs});counts.append({'difficulty':level,'attempted':len(attempts),'accepted':len(rs),'skipped_fingerprint_duplicates':len(attempts)-len(rs)})
save('resampling-results.json',{'counts':counts,'inspection':'batch loops max(100,count*20), samples profile and parameters, derives complete record, rejects only repeated parameter_fingerprint; mathematical data errors are not silently swallowed. Current sampler constructs valid dimensions/nonzero unknown vectors/distinct banks; boundary validation tested separately.'})
# Shared filtering preserves all records; measure the accepted distribution independently.
stages={};delivered=[]
for name in ['easy','moderate','batch']:
 rs=load(ROOT/('delivery-'+name+'/accepted.json'));delivered+=rs
 for r in rs:a.verify(r)
 stages[name]={'delivery':load(ROOT/('delivery-'+name+'/delivery.json')),'shortcut_probes':a.stats(rs),'answers':[str(a.verify(r)) for r in rs]}
save('delivery-coverage.json',stages)
# Faithful same-band select() reproduction, with explicit synthetic numeric IDs.
# No captured live policy/history exists; these are scenario bounds, not live delivery claims.
selection=[]
for name in stages:
 rs=load(ROOT/('delivery-'+name+'/accepted.json'))
 for scenario,remaining in [('no_history',rs),('exclude_first_half',rs[len(rs)//2:])]:
  ordered=sorted(remaining,key=lambda r:r['question'][':question/id']);selected=[]
  for i in range(64):
   seed=f'independent-review/kp17592186119805/task{i}/prefix0';h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53);r=ordered[int(u*len(ordered))];selected.append({'seed':seed,'synthetic_entity_id':1000000+ordered.index(r),'question_id':r['question'][':question/id'],'answer':str(a.verify(r)),'old_shortcut_correct':a.predict(r['question'],'old-label-bank')==a.verify(r)})
  selection.append({'pool':name,'scenario':scenario,'candidate_count':len(ordered),'draws':selected,'answer_set':sorted({x['answer'] for x in selected}),'old_shortcut_correct':sum(x['old_shortcut_correct'] for x in selected),'total':len(selected)})
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs select; read-only faithful reproduction for one rated band with positive weight','rules':['Fresh usable candidates exclude history/current prefix before select.','Numeric entity IDs sorted/deduplicated.','First SHA256 uniform chooses nonempty positively weighted band.','Second uniform chooses candidate in that band.','Unconfigured weights choose first candidate; no positive rated band uses unrated fallback.'],'assumptions':['No learner histories/policy weights captured; tested no-history and half-excluded scenarios.','New questions have no database entity IDs; assign synthetic numeric IDs in UUID order, state no actual future ordering claim.','Captured inventory includes 13 original source and 2 historical generated questions; source questions are not relabeled.','Positive requested-band weights leave all fresh same-band cases eligible; arbitrary histories can shrink any finite pool, so no guarantee for every possible history.'],'scenarios':selection})
# Real learner grader, all five choices of every source/normal/batch/counterfactual/role/delivered/inventory record.
rs=[]
for file in ['normal-records.json','runner-batch.json','source-replay-records.json','counterfactual-records.json','role-records.json','generated-records.json']:rs+=load(ROOT/file)
rs+=delivered
cases=[]
for i,r in enumerate(rs):
 ans=a.verify(r);checks=[]
 for option in a.choices(r['question']):checks.append({'field_index':0,'submitted_answer_id':option[':answer/id'],'expected':'accepted' if a.value(option[':answer/value'])==ans else 'rejected','purpose':'Independent rational component consistency. Radio accepts choice UUIDs; no typed equivalent-entry contract.'})
 cases.append({'label':f'independent-{i}','record':r,'checks':checks})
save('grader-input.json',cases)
cmd=[str(a.REPO/'generate/runs/current/check-engine'),str(ROOT/'grader-input.json'),str(ROOT/'grader-report.json')];run=subprocess.run(cmd,capture_output=True,text=True,cwd=ROOT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
save('grader-execution.json',{'command':cmd,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr,'record_count':len(cases),'response_count':5*len(cases)});assert run.returncode==0,run.stderr
(ROOT/'session-state.md').write_text('Shared delivery passed: easy 128/128, moderate 64/64, runner 5/5. Native grader completed on all five choices, including all controlled pairs and delivered records. Two historical affected inventory records reproduced with original UUIDs and generation metadata. Current four retained repairs pass. Pending remaining pair rendering/screenshot inspection and final evidence contract.\n')
print(json.dumps({'legacy_affected':len(affected),'stages':{k:v['delivery']['accepted_count'] for k,v in stages.items()},'resampling':counts,'grader_cases':len(cases),'grader_responses':len(cases)*5,'grader_exit':run.returncode}))
