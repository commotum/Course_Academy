# Run after audit.py. Reuse its independent parser and retained sample files.
exec(compile(open('audit.py').read().split('records=[];domain_report=[]')[0],'audit.py','exec'))
base=copy.deepcopy(g.CASES['q-34249']);positive=dict(copy.deepcopy(base),s=2)
positive_record=g.generate('easy',64193,'q-34249',positive)
pairs=load(ROOT/'counterfactual-records.json');pairs.append(positive_record);save('counterfactual-records.json',pairs)
# A one-coordinate change of u changes a homogeneous source from inconsistent to consistent.
mp=copy.deepcopy(g.CASES['q-34570']);consistent=copy.deepcopy(mp);consistent['u'][0]=1
failure=None
try:g.generate('moderate',64193,'q-34570',consistent)
except Exception as e:failure=type(e).__name__
assert failure=='AssertionError'
rr=load(ROOT/'counterfactual-results.json');rr['role_change']={'parameters_before':base,'parameters_after':positive,'before_answer':'-2','after_answer':key(positive_record['question']),'independent_after':str(solve(positive_record['question'])[0]),'sampler_reaches_after':positive in g.domain('q-34249'),'construction_accepts_after':True,'shortcut_after':shortcut(positive_record['question']),'result':'failed sampler coverage: the same valid unique-coefficient operation supports the opposite answer sign but normal domain never draws it'}
rr['homogeneous_consistency']={'parameters_before':mp,'parameters_after':consistent,'mathematical_after_answer':'-6','verification':'3*[2,4]+(-6)*[1,2]=[0,0]','generator_after':failure,'result':'consistent homogeneous same-operation case rejected; every normal homogeneous item remains No solution'}
save('counterfactual-results.json',rr)
# Delivered pool comparison and faithful reproduction of select() for positive easy-only weights.
stages={};all_delivered=[]
for name in ['batch','easy','moderate']:
 recs=load(ROOT/('delivery-'+name+'/accepted.json'));all_delivered+=recs
 stages[name]={'report':load(ROOT/('delivery-'+name+'/delivery.json')),'shortcuts':stats(recs)}
save('delivery-coverage.json',stages)
selection=[]
for name in ['batch','easy','moderate']:
 recs=load(ROOT/('delivery-'+name+'/accepted.json'))
 # All candidates are same band, so any positive weight selects that band; native selector
 # uses the second 53-bit uniform for the sorted fresh usable candidate list.
 for scenario,eligible in [('no_history',recs),('exclude_first_half',recs[len(recs)//2:])]:
  ordered=sorted(eligible,key=lambda r:r['question'][':question/id']) # synthetic IDs assigned in UUID order; no future DB IDs claimed
  outcomes=[]
  for task in range(1,33):
   seed=f'task-{task}/kp-17592186119805/slot-0';h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(h[8:16],'big')>>11)/(1<<53);r=ordered[int(u*len(ordered))];pred,cue=shortcut(r['question']);outcomes.append({'seed':seed,'selected_uuid':r['question'][':question/id'],'cue':cue,'shortcut_correct':pred==key(r['question'])})
  selection.append({'pool':name,'scenario':scenario,'candidate_count':len(ordered),'draws':outcomes,'shortcut_correct':sum(x['shortcut_correct'] for x in outcomes),'total':len(outcomes)})
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs select(), and learning.rs 594–622 prefilter; read only faithful same-band reproduction','rules':['Remove seen and invalid questions before select.','Sort and deduplicate numeric entity IDs.','Choose a nonempty positively weighted difficulty band by SHA256 first 53-bit uniform.','Choose an index by SHA256 second 53-bit uniform.','If no configured weights, first candidate; if rated positive bands absent, unrated fallback only.'],'assumptions':['No learner history or policy weights were captured. Two explicitly assumed history scenarios tested. New records have no database IDs: UUID order used to assign synthetic sorted numeric IDs. Every member satisfies the demonstrated shortcut, so all numeric orders, positive band weights and eligible subsets preserve the defect.','Existing stored pool has source and generated records: only two generated records are attributed to the generator; source records are not relabeled. A mixed learner pool is not claimed universally shortcut-solvable.'],'scenarios':selection})
# Add native grading for delivered normalized questions, the new role counterfactual and boundary counterexample.
cases=load(ROOT/'grader-input.json')
for i,r in enumerate(all_delivered+[positive_record]):
 ans,_=solve(r['question']);checks=[]
 for a in r['question'][':question/answer-fields'][0][':answer-field/choices']:
  val=a[':answer/value'];ok=(val==ans if val=='No solution' else scalar(val)==ans)
  checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if ok else 'rejected','purpose':'Independent math on delivered records or sign-role counterfactual'})
 cases.append({'label':f'delivered-or-role-{i}','record':r,'checks':checks})
boundary=load(ROOT/'boundary-subtraction-c2.json')[0];bf=boundary['question'][':question/answer-fields'][0];correctid=bf[':answer-field/correct'][1]
cases.append({'label':'FAIL: subtraction c=2 accepted construction stores 2 for inconsistent prompt','record':boundary,'checks':[{'submitted_answer_id':correctid,'expected':'rejected','purpose':'Prompt implies no solution, so stored value 2 must be rejected; accepted means concrete construction defect'}]})
save('grader-input.json',cases)
# Render the unexamined pair members, all remaining templates and sign-role counterfactual.
original=load(ROOT/'render-records.json');save('render-followup-records.json',original[6:]+[positive_record,boundary])
save('scope-results.json',{'normal_sample_count':54,'runner_batch_count':5,'observed_dimensions':[2,3,4],'response':'five-choice single radio','normal_operations':['known integer scalar multiplication','vector addition/subtraction','component scalar division','component consistency comparison in moderate'],'within_source_workload':True,'unsupported_source_cases':['q-34572','q-105153','q-105156'],'unrated_gap':'q-34250 missing source key, solution and rating; independently answer 4; not called generator failure','canonical_example':'fd3cb5b1-f16e-5a52-82e4-25bbbd1c4fe7 is readable source evidence but no replay entrypoint exists for its complete original parameters/label'} )
(ROOT/'session-state.md').write_text('Delivery complete: batch 5/5, easy controls 36/36, moderate controls 17/18 (one duplicate). Native normal grading 320/320 as expected. First six UI cases rendered and screenshot inspected. Saved follow-up checks for actual delivered IDs, opposite-sign counterfactual, accepted invalid subtraction parameters. Pending final native/render follow-up and evidence/report finalization.\n')
print(json.dumps({'delivery':{k:v['report']['accepted_count'] for k,v in stages.items()},'role_change':rr['role_change'],'homogeneous_consistency':rr['homogeneous_consistency'],'grader_records':len(cases),'render_followup':len(original[6:])+2}))
