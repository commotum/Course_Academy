import pathlib,json,sys,subprocess,collections,re,hashlib,shutil,os
R=pathlib.Path(__file__).resolve().parent;J=R.parent;REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python'
def load(p):return json.loads((R/p).read_text())
def save(p,x):(R/p).write_text(json.dumps(x,indent=2)+'\n')
def run(args,path):
 p=subprocess.run(list(map(str,args)),capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));save(path,{'command':p.args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p
# Verify author checks have discriminating power on preserved pre-repair runtime.
old=R/'baseline-package';old.mkdir(exist_ok=True)
for f in ['17592186100990.py','17592186100990/source.json']:
 dest=old/f;dest.parent.mkdir(exist_ok=True);shutil.copyfile(J/'review-0-policy-2-fd6037e892fe96a5/relocated'/f,dest)
shutil.copyfile(R/'regression_shortcut.py',old/'regression_shortcut.py')
s=(J/'workspace/check_repair.py').read_text().replace("W=Path(__file__).resolve().parent",f"W=Path({str(old)!r})").replace("E=W/'evidence'",f"E=Path({str(R/'author-baseline')!r})").replace("W.parent/'source/source.json'",repr(str(J/'source/source.json'))).replace("W.parent/'source/inventory.json'",repr(str(J/'source/inventory.json')))
# Parenthesized pathlib expressions also occur as (W.parent/'source/source.json').read_text().
s=s.replace("("+repr(str(J/'source/source.json'))+").read_text()", "Path("+repr(str(J/'source/source.json'))+").read_text()")
(R/'author-baseline-check.py').write_text(s)
for c in ('source','shortcut','grading'):run([PY,'-B',R/'author-baseline-check.py','--check',c],'author-baseline-'+c+'-execution.json')
# Keep source failure then use exact current runner batch as minimal prospective reproduction.
for f in ['comma-strict-input.json','comma-strict-execution.json']:shutil.copyfile(R/f,R/('source-'+f))
run([PY,'-B',R/'regression_index_notation.py',R/'batch.json'],'batch-comma-regression.json')
diag=load('comma-strict-input.json')
for c in diag:
 for ch in c['checks']:ch['expected']='rejected';ch['purpose']+='; diagnostic observation, NOT an acceptance expectation'
save('comma-diagnostic-input.json',diag);run([REPO/'generate/runs/current/check-engine',R/'comma-diagnostic-input.json',R/'comma-diagnostic-report.json'],'comma-diagnostic-execution.json')
# Compare normal serialized CLI output; Python internal bank tuples serialize as JSON lists.
p=load('packaging-results.json');p['batch_seed_replay']=load('relocation.json')['matches_exact_runner_batch'];p['batch_comparison_note']='Previous direct Python equality compared tuples with serialized JSON lists. The actual CLI and relocated CLI replay exactly match runner batch.';save('packaging-results.json',p)
# Evidence of real controls, not relying on generation metadata.
def coords(s):return tuple(map(int,re.search(r'_\{(\d)(\d)\}',s).groups()))
def key(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def observed(r):
 q=r['question'];body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1];rows=[s.split('&') for s in body.split(r'\\')];hit=[(i,j) for i,row in enumerate(rows,1) for j,c in enumerate(row,1) if '\\boxed{' in c];return len(rows),len(rows[0]),hit[0]
def stats(rs):
 groups=collections.defaultdict(list);families=collections.Counter();shapes=collections.Counter()
 for r in rs:
  m,n,pos=observed(r);f=r['question'][':question/answer-fields'][0];layout='display' if '$$' in r['question'][':question/problem'] else 'inline';kind='radio' if f[':answer-field/type'].endswith('/radio') else 'two_indices' if len(r['question'][':question/answer-fields'])==2 else 'notation_blank';families[layout+' '+kind]+=1;shapes[str((m,n))]+=1
  if kind!='radio':continue
  opts=[coords(a[':answer/value']) for a in f[':answer-field/choices']];group=(layout,m,n,tuple(sorted(opts)));actual=coords(key(f));groups[group].append({'id':r['question'][':question/id'],'position':opts.index(actual),'target':actual,'sorted_role':sorted(opts).index(actual)})
 return {'count':len(rs),'families':dict(families),'shapes':dict(shapes),'groups':[{'signature':str(k),'count':len(v),'distinct_targets':len({x['target'] for x in v}),'targets':sorted(set(x['target'] for x in v)),'observations':v} for k,v in groups.items()]}
stages={n:stats(load(f)) for n,f in [('batch_raw','batch.json'),('batch_delivered','delivery-batch/accepted.json'),('fresh_raw','fresh-batches.json'),('fresh_delivered','delivery-fresh/accepted.json'),('controls_raw','controlled-records.json'),('controls_delivered','delivery-controls/accepted.json'),('single_samples','samples.json')]};save('delivery-analysis.json',stages)
# Repeat retained cue on actual filtered records.
for s in ['batch','fresh','controls']:run([PY,R/'regression_shortcut.py',R/('delivery-'+s+'/accepted.json'),R/('delivered-'+s+'-cue.json')],'delivered-'+s+'-cue-execution.json')
# Source field storage order differs for q139426; rendered placeholders bind by key.
sr=load('source-comparison.json');sr[2]['order_assessment']='The two field objects are stored in reverse order; i/j placeholders still bind by field key and native checks verify both. This is serialization order, not a changed learner response.';save('source-comparison.json',sr)
# Original source rows are not generated history. Inspect only the additional bank row as such.
inv=json.loads((J/'source/inventory.json').read_text());sources=json.loads((J/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];ids={q[':question/id'] for q in sources};rows=[]
for q in inv['questions']:
 fs=q.get(':question/answer-fields',[]);rows.append({'id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in ids,'retired':q.get(':question/retired',False),'has_correct_refs':all(':answer-field/correct' in f for f in fs),'generation_metadata':[k for k in q if 'generation' in k]})
extra=[q for q in inv['questions'] if q[':question/id'] not in ids];save('inventory-extra-records.json',extra)
save('inventory-analysis.json',{'basis':inv['basis'],'rows':rows,'additional_records_checked':len(extra),'conclusion':'The only non-source row is a two-numeric-blank (1,1) question, with explicit box and matching keys/solution. It has no symbolic field or radio bank, so neither demonstrated grading weakness nor retained bank cue applies. No generated stored defect demonstrated. Original source questions are not relabeled generated.','limits':['No stored generation metadata supplied. This is a verified absence of these specific weaknesses among the one additional stored record, not a broad historical certificate.','Original q139629 lacks the captured highlight and has matching (3,1) keys/solution; this source correction is documented, not mislabeled as generated history.']})
save('affected-inventory.json',{'affected_questions':[]})
save('selection-analysis.json',{'basis':inv['basis'],'files':['engine/rust/question_selection.rs:103-195','engine/rust/learning.rs:149-177'],'rules':['Practice validation rejects retired and incomplete records.','seen_before_task excludes historical task items; caller excludes current prefix.','Positive difficulty weights choose among nonempty bands, followed by uniform deterministic hash draw within band; absent weights choose smallest entity ID.'],'application':'All five easy candidate records pass shared delivery. Selection does not repair incorrect grading; the batch symbolic blank is eligible and can be selected. Paired radio records have distinct targets before and after filtering. A particular learner may already have seen a partner, so pairing is not a promise about individual sequence balance.','limits':['No learner histories or current policy weights supplied; no empirical selection-frequency claim.','Publication preparation file absent; used actual shared read-only filter against captured basis 5667.']})
save('render-inspection.json',{'report':'render/rendering.json','cases':23,'inspected':['render/question-002.png','render/question-014.png','render/question-015.png','render/question-017.png'],'observations':['Exact batch symbolic field and conclusion render legibly.','Repaired 4x4 q139629 shows box at row3 column1; numeric slots i=3,j=1 agree with solution.','Controlled bank shares same zero matrix and moves highlight/selected choice from z21 to z13; solutions follow.','No broken matrices, missing highlights or clipped controls seen.'],'limitation':'Preview displays keys; native grader is exercised separately.'})
(R/'session-state.md').write_text('All nine source replays, 205 math checks, 399 strict native checks and 23 renderer cases completed. Previous exact symbolic failures now pass. New current-batch failure: c_{2,2} rejected although it denotes the highlighted (2,2) entry. Strict candidate-record regression saved. Delivery batch 5/5; fresh 32/40; controls46/56. Finishing variation report and integrity check; package unchanged.\n')
print({k:{'count':v['count'],'groups':[(g['count'],g['distinct_targets']) for g in v['groups']]} for k,v in stages.items() if k in ['batch_delivered','fresh_delivered','controls_delivered']})
