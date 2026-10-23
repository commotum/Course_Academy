import json,pathlib,subprocess,sys,shutil,collections,hashlib,copy
R=pathlib.Path(__file__).resolve().parent;J=R.parent;repo=pathlib.Path('/home/jake/Developer/Course_Academy');py=str(repo/'.venv/bin/python')
def save(n,x): (R/n).write_text(json.dumps(x,indent=2)+'\n')
def load(n):return json.load(open(R/n))
# Separate strict expectation from observational diagnostics; do not turn a failing valid answer into a pass.
cases=load('grader-input.json');ok=[];symbolic=[]
for c in cases:
 (symbolic if c['record']['generation']['template']=='notation_blank' else ok).append(c)
# Test a stale relevant counterfactual response in the real grader.
for c in ok:
 if c['record']['generation']['template']=='two_indices' and c['record']['generation']['parameters']['i']==2 and c['record']['generation']['parameters']['j']==2:
  for i in range(2): c['checks'].append({'field_index':i,'submitted':'1','expected':'rejected','purpose':'prior target coordinate must fail after highlight relocation'})
save('grader-supported-input.json',ok);save('grader-symbolic-strict.json',symbolic)
diag=copy.deepcopy(symbolic)
for c in diag:
 for chk in c['checks']:chk['expected']='unresolved';chk['purpose']+='; observational reproduction of known parser failure, NOT acceptance criterion'
save('grader-symbolic-diagnostic.json',diag)
for name in ['supported','symbolic-strict','symbolic-diagnostic']:
 src='grader-supported-input.json' if name=='supported' else 'grader-'+name+'.json'
 proc=subprocess.run([str(repo/'generate/runs/current/check-engine'),str(R/src),str(R/('grader-'+name+'-report.json'))],capture_output=True,text=True)
 save('grader-'+name+'-execution.json',{'command':proc.args,'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
# Relocation: declared runtime files copied, invoked from a new cwd, with bytecode disabled.
rel=R/'relocated';rel.mkdir(exist_ok=True);(rel/'17592186100990').mkdir(exist_ok=True)
for f in ['17592186100990.py','17592186100990/source.json']:shutil.copyfile(J/'workspace'/f,rel/f)
proc=subprocess.run([py,'-B',str(rel/'17592186100990.py'),'--difficulty','easy','--seed','3782988951','--count','5','--format','json'],cwd=rel,capture_output=True,text=True)
save('relocation.json',{'command':proc.args,'returncode':proc.returncode,'stderr':proc.stderr,'matches_runner_batch':json.loads(proc.stdout)==load('batch.json')});(R/'relocated-batch.json').write_text(proc.stdout)
# Confirm actual delivery does not remove the relevant radio signatures.
def coords(v):
 import re
 return tuple(map(int,re.search(r'_\{(\d)(\d)\}',v).groups()))
def stats(rs):
 count=collections.Counter();positions=collections.Counter();preds=[]
 for r in rs:
  f=r['question'][':question/answer-fields'][0];count[r['generation']['template']]+=1;positions[str((r['generation']['parameters']['i'],r['generation']['parameters']['j']))]+=1
  if f[':answer-field/type'].endswith('/radio'):
   cs=[coords(a[':answer/value']) for a in f[':answer-field/choices']];mi=min(x for x,y in cs);mj=min(y for x,y in cs);sig=sorted((i-mi,j-mj) for i,j in cs)
   key=next(coords(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
   table={str([(0,0),(0,1),(0,2),(1,0),(1,1)]):((0,1),'q-13498'),str([(0,2),(1,0),(1,2),(2,2),(3,2)]):((2,2),'q-13503'),str([(0,2),(1,0),(1,1),(2,3),(3,2)]):((2,3),'q-13499'),str([(0,0),(0,1),(1,0),(1,1),(1,2)]):((0,0),'ambiguous q-13489/q-125611')}
   role,label=table[str(sig)];pred=(mi+role[0],mj+role[1]);preds.append({'id':r['question'][':question/id'],'signature':label,'template':r['generation']['template'],'correct':pred==key,'prediction':pred,'actual':key})
 return {'count':len(rs),'templates':dict(count),'positions':dict(positions),'choice_only_predictions':preds,'correct':sum(x['correct'] for x in preds),'attempts':len(preds)}
results={name:stats(load(file)) for name,file in [('raw_batch','batch.json'),('delivered_batch','delivery-batch/accepted.json'),('raw_samples','samples.json'),('delivered_samples','delivery-samples/accepted.json')]}
save('delivery-analysis.json',results)
inv=json.load(open(J/'source/inventory.json'));src=json.load(open(J/'source/source.json'));ids={q[':question/id'] for q in src['material']['kp'][':knowledge-point/questions']}
rows=[]
for q in inv['questions']:
 fs=q.get(':question/answer-fields',[]);rows.append({'id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in ids,'retired':q.get(':question/retired',False),'has_all_correct_refs':all(':answer-field/correct'in f for f in fs),'types':[f[':answer-field/type'][':db/ident'] for f in fs],'generation_metadata_present':any('generation' in k for k in q)})
save('inventory-analysis.json',{'basis':inv['basis'],'records':rows,'conclusion':'Nine original source questions and one additional two-numeric-blank record. Additional record has explicit highlighted (1,1), both keys 1, matching explanation. No current radio-bank shortcut is demonstrated in a generated stored record; original source questions are not relabeled generated. Missing symbolic grader capability applies to original source blanks, recorded separately as grading limitation.','eligibility':'learning.rs validate_practice_question excludes retired and invalid/no-correct-reference records; none has retired=true. The two initial radio sources lack correct refs. Other seven original sources and the additional numeric record have complete fields. No learner history was supplied.','limits':'No stored generation metadata in captured rows; do not invent reproductions or claim original questions are generated.'})
save('affected-inventory.json',{'affected_questions':[]})
save('selection-analysis.json',{'files':['engine/rust/question_selection.rs:125-231','engine/rust/learning.rs:149-177'],'rules':['Candidates must be usable, fresh and not retired. Prior learner tasks and current prefix are excluded.','Difficulty weights select among nonempty positive-weight bands, then a deterministic uniform hash draw selects within band. Unrated fallback only if no weighted rated band remains.','Absent policy weights select smallest entity ID.'],'application':'All five batch records are valid easy records and survive actual delivery; all have selectable answer fields. Any subset retaining the q-13498 radio retains its choice-only predictor. Selection does not inspect radio bank geometry or rebalance decision cases. A learner history can remove records but cannot repair a surviving record.','limits':['Captured basis 5667 only; publication file absent.','No learner policy weights or histories supplied; no empirical claim about real learner draw rates.','The additional non-source captured record is a numeric-blank (1,1) item; no demonstrated current radio shortcut there.']})
state='Source reconstructed independently. 120 fresh samples, 39 position boundaries, 8/9 source replays; q-139629 unsupported. Math checks complete. Fixed bank shortcut demonstrated for q-13498. Exact symbolic blank grader fails. Shared delivery: batch and samples processed. Renderer initial six complete; full selected render pending. Package untouched.\n'
(R/'session-state.md').write_text(state)
print({n:{'count':v['count'],'correct':v['correct'],'attempts':v['attempts']} for n,v in results.items()})
